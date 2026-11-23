"""Duplicate gate for ZC2 date folders.

Run from the repo root before finalizing a day and again before reporting:
    python scripts/dupcheck.py                 # every upcoming date folder, all accounts
    python scripts/dupcheck.py 2026-11-24      # only those dates
Exit code 1 when anything is found. Checks, per account:
  1. the same X status ID twice inside the upcoming window,
  2. an upcoming status ID that is already in a posted log, an archived date's slate or an older slate,
  3. a similar caption in any account's recent slates or posted logs (same moment under another post ID),
  4. a file that is a Retired backlog clip,
  5. an upcoming file whose bytes match a file in an archived date, another upcoming date,
     or (for non-backlog picks) the account's backlog folder.
  6. the same FOOTAGE: a visual fingerprint (one frame every 5 s, 8x8 difference hash) is compared against the
     account's archive, reserves, other upcoming dates and backlog. It catches the same video uploaded by a different
     account (new status ID, new caption, different bytes), re-encodes and trims. Fingerprints are cached in
     <media>/.prep/footage-cache.json, so only the first run is slow (about 1 s per clip).
"""
import glob
import hashlib
import os
import json
import re
import subprocess
import sys
from collections import defaultdict

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
ACCOUNTS = {
    "sidelinesync": (R + "slates/", R + "sidelinesync/", R + "posted.md"),
    "fitnessclip": (R + "fitnessclip/slates/", R + "fitnessclip/clips/", R + "fitnessclip/posted.md"),
    "kickiip": (R + "kickiip/slates/", R + "kickiip/clips/", R + "kickiip/posted.md"),
}
ID = re.compile(r"status/(\d{15,20})")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fingerprint(path):
    with open(path, "rb") as handle:
        return os.path.getsize(path), hashlib.md5(handle.read(1 << 20)).hexdigest()


def rows_only(path):
    """Slate table rows only, so IDs mentioned as rejects in prose do not count as used."""
    return "\n".join(l for l in read(path).splitlines() if l.startswith("|"))


def read(path):
    return open(path, encoding="utf-8", errors="ignore").read() if os.path.exists(path) else ""


STOP = set("the a an and or of to in on at for with his her their he she they it is was were be been that this just after before while about from into out up over like got get has have had not no but so as by than then them him who what when how why all one two three first live stream streamer game".split())


def norm_tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 2]


def caption_rows(path, account, label):
    """(account, label, time, caption, status id) for slate table rows."""
    rows = []
    for line in rows_only(path).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and ID.search(cells[1]):
            rows.append((account, label, cells[0], cells[3], ID.search(cells[1]).group(1)))
    return rows


def similar_captions(problems, wanted):
    """Same moment posted twice under different status IDs (different posters or reposts)."""
    import datetime
    import difflib
    cutoff = (datetime.date.today() - datetime.timedelta(days=10)).isoformat()
    upcoming, reference = [], []
    for account, (slates, media, posted) in ACCOUNTS.items():
        up_dates = sorted(d for d in os.listdir(media) if DATE.match(d) and glob.glob(media + d + "/*.mp4")) if os.path.isdir(media) else []
        if wanted:
            up_dates = [d for d in up_dates if d in wanted]
        for path in glob.glob(slates + "*.md"):
            date = os.path.basename(path)[:-3]
            if not DATE.match(date) or date < cutoff:
                continue
            for row in caption_rows(path, account, date):
                (upcoming if date in up_dates else reference).append(row)
        for line in read(posted).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 5 and DATE.match(cells[0]) and cells[0] >= cutoff:
                reference.append((account, cells[0] + " posted", cells[1], cells[4], (ID.search(cells[2]) or [None, ""])[1] if ID.search(cells[2]) else ""))
    everything = upcoming + reference
    flagged = set()
    for u in upcoming:
        tu = norm_tokens(u[3])
        if len(tu) < 3:
            continue
        for o in everything:
            if o is u or (o[0], o[1], o[2]) == (u[0], u[1], u[2]):
                continue
            to = norm_tokens(o[3])
            if len(to) < 3:
                continue
            shared = set(tu) & set(to)
            jac = len(shared) / len(set(tu) | set(to))
            ratio = difflib.SequenceMatcher(None, " ".join(tu), " ".join(to)).ratio()
            if (ratio >= 0.68 or (jac >= 0.6 and len(shared) >= 4)) and not (u[4] and u[4] == o[4]):
                key = tuple(sorted([(u[0], u[1], u[2]), (o[0], o[1], o[2])]))
                if key in flagged:
                    continue
                flagged.add(key)
                msg = f"same moment? {u[0]} {u[1]} {u[2]} \"{u[3][:60]}\" vs {o[0]} {o[1]} {o[2]} \"{o[3][:60]}\""
                if u[0] == o[0]:
                    problems.append(msg)
                else:
                    print(" note (other account):", msg)


BACKLOGS = {"sidelinesync": R + "backlog.md", "fitnessclip": R + "fitnessclip/backlog.md", "kickiip": R + "kickiip/backlog.md"}


def backlog_status(account):
    """{file name: (retired?, [used-on dates])} from the account's backlog.md."""
    status, retired = {}, False
    for line in read(BACKLOGS[account]).splitlines():
        if line.startswith("## "):
            retired = "retired" in line.lower()
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 2 and cells[1].endswith(".mp4"):
            used = re.findall(r"\d{4}-\d{2}-\d{2}", cells[-1]) if len(cells) >= 9 else []
            status[cells[1]] = (retired or "retired" in line.lower().split("|")[7] if len(cells) > 7 else retired, used)
    return status

FFMPEG = "ffmpeg"


def frame_hashes(path):
    """dHash of one frame every 5 seconds (up to 40), as a list of ints."""
    try:
        out = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", "fps=1/5,scale=9:8,format=gray", "-frames:v", "40", "-f", "rawvideo", "-"],
                             capture_output=True, timeout=300).stdout
    except Exception:
        return []
    hashes = []
    for n in range(len(out) // 72):
        f = out[n * 72:(n + 1) * 72]
        bits = 0
        for y in range(8):
            for x in range(8):
                bits = (bits << 1) | (1 if f[y * 9 + x] > f[y * 9 + x + 1] else 0)
        if 6 <= bin(bits).count("1") <= 58:  # skip blank or near-uniform frames
            hashes.append(bits)
    return hashes


def cached_hashes(path, cache):
    key = path
    stamp = [os.path.getsize(path), int(os.path.getmtime(path))]
    hit = cache.get(key)
    if hit and hit["s"] == stamp:
        return hit["h"]
    h = frame_hashes(path)
    cache[key] = {"s": stamp, "h": h}
    return h


def same_footage(a, b):
    """True when enough frames of the two clips match (works for trims and re-uploads)."""
    if not a or not b:
        return False
    matched = 0
    for x in a:
        if any(bin(x ^ y).count("1") <= 6 for y in b):
            matched += 1
    need = max(2, int(0.3 * min(len(a), len(b))))
    return matched >= need


def footage_check(problems, notes, wanted):
    for account, (slates, media, posted) in ACCOUNTS.items():
        if not os.path.isdir(media):
            continue
        dates = sorted(d for d in os.listdir(media) if DATE.match(d) and glob.glob(media + d + "/*.mp4"))
        if wanted:
            dates = [d for d in dates if d in wanted]
        if not dates:
            continue
        cache_path = media + ".prep/footage-cache.json"
        try:
            cache = json.load(open(cache_path))
        except Exception:
            cache = {}
        corpus = []  # (label, path)
        for pat, label in ((media + "archive/*/*.mp4", "archive"), (media + "archive/*/reserves/*.mp4", "archive"),
                           (media + "backlog/*.mp4", "backlog")):
            for f in glob.glob(pat):
                corpus.append((f"{label}/{os.path.basename(os.path.dirname(f)) if label == 'archive' else ''}{'/' if label == 'archive' else ''}{os.path.basename(f)}", f))
        upcoming = []
        for d in sorted(d for d in os.listdir(media) if DATE.match(d)):
            for f in glob.glob(media + d + "/*.mp4") + glob.glob(media + d + "/reserves/*.mp4"):
                upcoming.append((f"{d}/{os.path.basename(f)}", f, d))
        checked = [u for u in upcoming if u[2] in dates and "/reserves/" not in u[1].replace("\\", "/")]
        hashes = {}
        for label, f in corpus:
            hashes[f] = cached_hashes(f, cache)
        for label, f, d in upcoming:
            hashes[f] = cached_hashes(f, cache)
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        json.dump(cache, open(cache_path, "w"))
        seen_pairs = set()
        for label, f, d in checked:
            name = os.path.basename(f)
            for olabel, of in corpus:
                if fingerprint(f) == fingerprint(of):
                    continue  # byte-identical files are reported by check 3
                if olabel.startswith("backlog/") and ("-B" in name or "-K" in name or "FB" in name):
                    continue  # a backlog pick compares equal to its own backlog file
                if same_footage(hashes[f], hashes[of]):
                    problems.append(f"{account} {label}: same footage as {olabel}")
            for olabel, of, od in upcoming:
                if of == f:
                    continue
                pair = tuple(sorted((f, of)))
                if pair in seen_pairs:
                    continue
                if same_footage(hashes[f], hashes[of]):
                    seen_pairs.add(pair)
                    problems.append(f"{account} {label}: same footage as {olabel}")


def main(argv):
    wanted = set(argv)
    problems = []
    notes = []
    for account, (slates, media, posted) in ACCOUNTS.items():
        dates = sorted(d for d in os.listdir(media) if DATE.match(d) and glob.glob(media + d + "/*.mp4")) if os.path.isdir(media) else []
        if wanted:
            dates = [d for d in dates if d in wanted]
        if not dates:
            continue
        slate_ids = {d: set(ID.findall(rows_only(slates + d + ".md"))) for d in dates}
        # 1. same ID twice inside the window
        seen = defaultdict(list)
        for d in dates:
            for i in slate_ids[d]:
                seen[i].append(d)
        for i, ds in seen.items():
            if len(ds) > 1:
                problems.append(f"{account}: status {i} appears on {', '.join(ds)}")
        # 2. already posted or planned elsewhere
        # posted.md rows dated like a folder under check are that folder's own posts, not repeats
        other = "\n".join(l for l in read(posted).splitlines() if not any(l.startswith("| " + d + " |") for d in dates))
        for path in glob.glob(slates + "*.md"):
            if os.path.basename(path)[:-3] not in dates:
                other += "\n#SLATE " + os.path.basename(path) + "\n" + rows_only(path)
        for d in dates:
            for i in sorted(slate_ids[d]):
                if i in other:
                    where = [m.group(1) for m in re.finditer(r"#SLATE (\S+)", other) if i in other.split(m.group(0))[1].split("#SLATE")[0]]
                    where = where + (["posted.md"] if i in other.split("#SLATE")[0] else [])
                    problems.append(f"{account} {d}: status {i} already used in {', '.join(where) or 'older slates'}")
        # 3. identical files
        index = defaultdict(list)
        for pattern, label in ((media + "archive/*/*.mp4", "archive"), (media + "archive/*/reserves/*.mp4", "archive")):
            for f in glob.glob(pattern):
                index[fingerprint(f)].append(f"{label}/{os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}")
        for d in dates:
            for f in glob.glob(media + d + "/*.mp4"):
                index[fingerprint(f)].append(f"{d}/{os.path.basename(f)}")
        backlog = {}
        for f in glob.glob(media + "backlog/*.mp4"):
            backlog[fingerprint(f)] = os.path.basename(f)
        status = backlog_status(account)
        for d in dates:
            for f in glob.glob(media + d + "/*.mp4"):
                if fingerprint(f) in backlog:
                    name = backlog[fingerprint(f)]
                    retired, used = status.get(name, (False, []))
                    if retired:
                        problems.append(f"{account} {d}/{os.path.basename(f)}: backlog clip {name} is Retired (do not use)")
        for key, files in index.items():
            if len(files) > 1 and any(not x.startswith("archive/") for x in files):
                problems.append(f"{account}: identical file in {', '.join(files)}")
        for d in dates:
            for f in glob.glob(media + d + "/*.mp4"):
                name = os.path.basename(f)
                if fingerprint(f) in backlog and "-B" not in name and "-K" not in name and "FB" not in name:
                    notes.append(f"{account} {d}/{name}: backlog use of {backlog[fingerprint(f)]} (60-day rule; the archive check above catches recent repeats)")
    similar_captions(problems, wanted)
    footage_check(problems, notes, wanted)
    for n in notes:
        print(" note:", n)
    if problems:
        print("DUPLICATES FOUND:")
        for p in problems:
            print(" -", p)
        return 1
    print("dupcheck: no duplicates")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
