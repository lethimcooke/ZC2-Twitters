"""Prepare a ZC2 slate's media for visual review in one command."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
ACCOUNTS = {"sidelinesync": ROOT, "fitnessclip": ROOT / "fitnessclip", "kickiip": ROOT / "kickiip"}
DOWNLOAD_FORMAT = "bv*[vcodec^=avc]+ba[acodec^=mp4a]/b[ext=mp4]/b"


def run(command, log, step):
    with log.open("a", encoding="utf-8") as output:
        print(subprocess.list2cmdline(command), file=output, flush=True)
        try:
            result = subprocess.run(
                command, capture_output=True, encoding="utf-8", errors="replace",
                timeout=300, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            print(error, file=output)
            raise ValueError(f"{step} failed to run or timed out") from error
        print(result.stdout, result.stderr, file=output)
    if result.returncode:
        raise ValueError(f"{step} failed (exit {result.returncode})")
    return result


def probe(path, log):
    result = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,codec_name,width,height,pix_fmt:stream_side_data=rotation",
        "-of", "json", str(path),
    ], log, "ffprobe")
    data = json.loads(result.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    duration = float(data.get("format", {}).get("duration", 0))
    if not video or not math.isfinite(duration) or duration <= 0:
        raise ValueError("no playable video with a known duration")
    rotation = next((item["rotation"] for item in video.get("side_data_list", [])
                     if "rotation" in item), 0)
    if rotation % 180 == 90:
        video["width"], video["height"] = video["height"], video["width"]
    video["rotation"] = rotation
    return video, audio, duration


def crop_region(path, start, length, video, log):
    result = run([
        "ffmpeg", "-hide_banner", "-nostdin", "-ss", str(start), "-i", str(path),
        "-t", str(min(length, 20)), "-map", "0:v:0", "-an",
        "-vf", "cropdetect=24:2:0", "-f", "null", "-",
    ], log, "crop detection")
    regions = re.findall(r"\bcrop=(\d+):(\d+):(\d+):(\d+)", result.stderr)
    if not regions:
        return None
    width, height, x, y = map(int, Counter(regions).most_common(1)[0][0])
    if width < video["width"] * 0.98 or height < video["height"] * 0.98:
        return f"{width}:{height}:{x}:{y}"
    return None


def download(url, folder, log):
    for attempt in range(2):
        # Separate directories keep a failed attempt's partial files out of the retry.
        download_dir = folder / f"download-{attempt}"
        download_dir.mkdir()
        try:
            result = run([
                "yt-dlp", "--no-playlist", "--no-progress", "--no-simulate",
                "--retries", "0", "--fragment-retries", "0",
                "-f", DOWNLOAD_FORMAT, "--merge-output-format", "mp4",
                "-P", f"temp:{download_dir}", "-o", str(download_dir / "source.%(ext)s"),
                "--print", "after_move:filepath",
                "--", url,
            ], log, "download")
            paths = result.stdout.strip().splitlines()
            if len(paths) != 1 or not Path(paths[0]).is_file():
                raise ValueError("download did not produce one video")
            return Path(paths[0])
        except ValueError:
            if attempt:
                raise


def contact_sheet(path, times, output, log):
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin"]
    filters = []
    for index, time in enumerate(times):
        command += ["-ss", f"{time:.3f}", "-threads", "1", "-i", str(path)]
        filters.append(
            f"[{index}:v:0]trim=end_frame=1,setpts=PTS-STARTPTS,"
            "scale=240:160:force_original_aspect_ratio=decrease,"
            f"pad=240:160:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuvj420p[f{index}]"
        )
    filters.append("".join(f"[f{i}]" for i in range(len(times))) + f"hstack=inputs={len(times)}[sheet]")
    run(command + [
        "-filter_complex_threads", "1", "-filter_complex", ";".join(filters),
        "-map", "[sheet]", "-frames:v", "1", "-q:v", "3", "-update", "1", str(output),
    ], log, "contact sheet")
    if not output.is_file():
        raise ValueError("contact sheet could not sample all frames")


def prepare(job, batch_dir):
    folder = batch_dir / job["name"].removesuffix(".mp4")
    folder.mkdir()
    log = folder / "tools.log"
    result = {"name": job["name"], "log": str(log)}
    try:
        source = Path(job["file"]) if "file" in job else download(job["url"], folder, log)
        video, audio, source_duration = probe(source, log)
        start = job.get("start", 0)
        end = min(job.get("end", source_duration), source_duration)
        length = end - start
        trimmed = start > 0 or end < source_duration
        if not 5 < length <= 140:
            raise ValueError("clip must be over 5 seconds and at most 140 seconds after trimming")
        crop = crop_region(source, start, length, video, log)
        staged = folder / job["name"]
        if (
            not trimmed and crop is None and not video["rotation"] and source.suffix.lower() == ".mp4"
            and video["codec_name"] == "h264" and video["pix_fmt"] == "yuv420p"
            and audio and audio["codec_name"] == "aac"
        ):
            shutil.copyfile(source, staged)
        else:
            command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
                       "-ss", str(start), "-i", str(source)]
            if audio is None:
                command += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            filters = [f"crop={crop}"] if crop else []
            filters += ["scale=trunc(iw/2)*2:trunc(ih/2)*2"]
            run(command + [
                "-t", str(length), "-map", "0:v:0", "-map", "0:a:0" if audio else "1:a:0",
                "-vf", ",".join(filters), "-c:v", "libx264", "-threads", "2",
                "-preset", "veryfast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-movflags", "+faststart", str(staged),
            ], log, "encode")
        video, audio, duration = probe(staged, log)
        if (
            video["codec_name"] != "h264" or not audio or audio["codec_name"] != "aac"
            or not 5 < duration <= 140
        ):
            raise ValueError("final codec or duration check failed")
        times = [0.5, duration * 0.1, duration * 0.5, duration * 0.9, duration - 0.5]
        sheet = folder / "review.jpg"
        contact_sheet(staged, times, sheet, log)
        if crop or trimmed:
            # Include source endpoints so trimming cannot hide an end card.
            original_sheet = folder / "before-edit.jpg"
            original_times = [start + t for t in times]
            if trimmed:
                original_times = sorted(set([0.5, *original_times, source_duration - 0.5]))
            contact_sheet(source, original_times, original_sheet, log)
            result["before_edit_sheet"] = str(original_sheet)
        result.update(
            status="needs_review", file=str(staged), sheet=str(sheet),
            frame_seconds=[round(time, 3) for time in times], crop=crop,
        )
    except (OSError, ValueError, KeyError, TypeError) as error:
        result.update(status="failed", reason=str(error))
    finally:
        for download_dir in folder.glob("download-*"):
            shutil.rmtree(download_dir, ignore_errors=True)
    return result


def read_jobs(manifest, clips):
    jobs = json.loads(manifest.read_text(encoding="utf-8-sig"))
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("manifest must be a nonempty JSON array")
    names = set()
    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError("each job must be a JSON object")
        name = job.get("name", "")
        if not isinstance(name, str) or not re.fullmatch(r"\d{4}-\d{1,2}-[a-z0-9-]+\.mp4", name):
            raise ValueError("each job needs a filename like 0800-1-example.mp4")
        if name in names:
            raise ValueError(f"duplicate filename: {name}")
        names.add(name)
        if ("file" in job) == ("url" in job):
            raise ValueError(f"{name}: specify exactly one of file or url")
        if "file" in job:
            path = (ROOT / job["file"]).resolve()
            if not path.is_relative_to(clips.resolve()) or not path.is_file():
                raise ValueError(f"{name}: local file must exist inside this account's clips folder")
            job["file"] = str(path)
        else:
            url = urlsplit(job["url"])
            if url.scheme != "https" or not url.hostname or url.username or url.password:
                raise ValueError(f"{name}: use a public HTTPS source URL")
        for key in ("start", "end"):
            if key in job:
                value = job[key]
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    raise ValueError(f"{name}: {key} must be a nonnegative number of seconds")
        if "end" in job and job["end"] <= job.get("start", 0):
            raise ValueError(f"{name}: end must come after start")
    return jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account", choices=ACCOUNTS, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    clips = ACCOUNTS[args.account] / "clips"
    try:
        jobs = read_jobs(args.manifest, clips)
        tools = ["ffmpeg", "ffprobe"]
        if any("url" in job for job in jobs):
            tools.append("yt-dlp")
        missing = [tool for tool in tools if not shutil.which(tool)]
        if missing:
            raise ValueError("missing on PATH: " + ", ".join(missing))
        staging = clips / ".prep"
        staging.mkdir(parents=True, exist_ok=True)
        batch_dir = Path(tempfile.mkdtemp(prefix="batch-", dir=staging))
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda job: prepare(job, batch_dir), jobs))
    report = batch_dir / "report.json"
    report.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    ready = sum(result["status"] == "needs_review" for result in results)
    print(f"{ready} awaiting visual review, {len(results) - ready} failed. Report: {report}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
