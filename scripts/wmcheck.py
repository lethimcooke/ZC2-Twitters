"""OCR watermark gate for ZC2 date folders (needs ffmpeg and Tesseract on PATH or in Program Files).

    python scripts/wmcheck.py                 # every upcoming date folder, all accounts
    python scripts/wmcheck.py 2026-11-24      # only those dates
    python scripts/wmcheck.py --file clip.mp4 # a single file
Samples 8 frames per clip (start, end and between) and flags other platforms' marks:
TikTok, Instagram, Reels, Shorts, Snapchat, CapCut, Douyin. Exit code 1 on any hit.
A hit means: reject the clip or find a clean copy. It never replaces a human look at the sheet.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
MEDIA = [R + "sidelinesync/", R + "fitnessclip/clips/", R + "kickiip/clips/"]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BAD = re.compile(r"tik\s?tok|instagram|\breels?\b|youtube\s?shorts|snapchat|capcut|douyin", re.I)
TESS = shutil.which("tesseract") or "C:/Program Files/Tesseract-OCR/tesseract.exe"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True)
    try:
        return float(out.stdout.decode().strip())
    except ValueError:
        return 0.0


def scan(path):
    length = duration(path)
    if length <= 0:
        return path, ["unreadable"]
    times = [0.3] + [length * k / 7 for k in range(1, 7)] + [max(length - 0.6, 0.3)]
    hits = set()
    with tempfile.TemporaryDirectory() as tmp:
        for index, t in enumerate(times):
            image = f"{tmp}/f{index}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                            "-vf", "scale=iw*2:ih*2:flags=lanczos,format=gray", image], capture_output=True)
            if not os.path.exists(image):
                continue
            for psm in ("11",):
                text = subprocess.run([TESS, image, "stdout", "--psm", psm], capture_output=True).stdout.decode("utf-8", "ignore")
                for match in BAD.finditer(text):
                    hits.add(f"{match.group(0).lower()} @ {t:.1f}s")
    return path, sorted(hits)


def main(argv):
    if argv[:1] == ["--file"]:
        files = argv[1:]
    else:
        wanted = set(argv)
        files = []
        for media in MEDIA:
            if not os.path.isdir(media):
                continue
            for d in sorted(os.listdir(media)):
                if DATE.match(d) and (not wanted or d in wanted):
                    files += glob.glob(media + d + "/*.mp4")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(scan, files))
    bad = [(p, h) for p, h in results if h]
    print(f"wmcheck: scanned {len(files)} clips")
    for p, h in bad:
        print(" -", p.replace(R, ""), "->", "; ".join(h))
    if bad:
        print("WATERMARK TEXT FOUND: reject or replace these clips.")
        return 1
    print("wmcheck: no platform marks found in sampled frames")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
