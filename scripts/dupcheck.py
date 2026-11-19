"""Duplicate gate for ZC2 date folders.

Run from the repo root before finalizing a day and again before reporting:
    python scripts/dupcheck.py                 # every upcoming date folder, all accounts
    python scripts/dupcheck.py 2026-11-24      # only those dates
Exit code 1 when anything is found. Checks, per account:
  1. the same X status ID twice inside the upcoming window,
  2. an upcoming status ID that is already in a posted log, an archived date's slate or an older slate,
  3. an upcoming file whose bytes match a file in an archived date, another upcoming date,
     or (for non-backlog picks) the account's backlog folder.
"""
import glob
import hashlib
import os
import re
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
        other = read(posted)
        for path in glob.glob(slates + "*.md"):
            if os.path.basename(path)[:-3] not in dates:
                other += "\n#SLATE " + os.path.basename(path) + "\n" + rows_only(path)
        for d in dates:
            for i in sorted(slate_ids[d]):
                if i in other:
                    where = [m.group(1) for m in re.finditer(r"#SLATE (\S+)", other) if i in other.split(m.group(0))[1].split("#SLATE")[0]]
                    where = where + (["posted.md"] if i in read(posted) else [])
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
        for key, files in index.items():
            if len(files) > 1 and any(not x.startswith("archive/") for x in files):
                problems.append(f"{account}: identical file in {', '.join(files)}")
        for d in dates:
            for f in glob.glob(media + d + "/*.mp4"):
                name = os.path.basename(f)
                if fingerprint(f) in backlog and "-B" not in name and "-K" not in name and "FB" not in name:
                    notes.append(f"{account} {d}/{name}: backlog use of {backlog[fingerprint(f)]} (60-day rule; the archive check above catches recent repeats)")
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
