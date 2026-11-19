"""Duplicate gate for ZC2 date folders.

Run from the repo root before finalizing a day and again before reporting:
    python scripts/dupcheck.py                 # every upcoming date folder, all accounts
    python scripts/dupcheck.py 2026-11-24      # only those dates
Exit code 1 when anything is found. Checks, per account:
  1. the same X status ID twice inside the upcoming window,
  2. an upcoming status ID that is already in a posted log, an archived date's slate or an older slate,
  3. a similar caption in any account's recent slates or posted logs (same moment under another post ID),
  4. an upcoming file whose bytes match a file in an archived date, another upcoming date,
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
        for key, files in index.items():
            if len(files) > 1 and any(not x.startswith("archive/") for x in files):
                problems.append(f"{account}: identical file in {', '.join(files)}")
        for d in dates:
            for f in glob.glob(media + d + "/*.mp4"):
                name = os.path.basename(f)
                if fingerprint(f) in backlog and "-B" not in name and "-K" not in name and "FB" not in name:
                    notes.append(f"{account} {d}/{name}: backlog use of {backlog[fingerprint(f)]} (60-day rule; the archive check above catches recent repeats)")
    similar_captions(problems, wanted)
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
