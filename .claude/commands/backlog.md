---
description: Add proven viral clips to the fallback backlog (default 20)
---
Grow the backlog of proven, evergreen viral clips for @sidelinesync, following CLAUDE.md.
How many to add: the number in "$ARGUMENTS" if there is one, otherwise 20. A category in "$ARGUMENTS" (e.g. "fails", "trick shots") narrows the search.

These don't need to be new. We want clips that have already gone viral many times in the niche and still work every time
they're reposted: all-time great catches, dunks, trick shots, fails, crowd moments, wholesome moments, funny animals at games.

1. Read `backlog.md` and `posted.md`. Skip anything already in either.
2. Find candidates with Playwright (read only) and vidIQ:
   - X searches with no time limit and high thresholds, e.g. `filter:native_video min_faves:50000 (catch OR dunk OR "trick shot" OR fail OR crowd) <exclusions>`
     (use the exclusion list from `watchlist.md`), and the same with min_faves:20000 for each category.
   - Repost accounts' most-liked clips, and clips that show up again and again from different accounts (proof it's a proven repost).
   - vidIQ outlier searches on TikTok and Instagram without a recent-only filter.
3. Run the niche check from CLAUDE.md on each one, look at the video itself, and find the original creator.
   A clip qualifies if it has gone viral more than once or has huge numbers (100K+ likes or 5M+ views somewhere), and nothing in it
   is tied to a date (no "last night", no season-specific stakes, no injured players since).
4. Download each one with yt-dlp into `clips/backlog/` as `<id>-<short-name>.mp4` (ids B001, B002, ... continuing from `backlog.md`),
   using the same command and rules as `/prep` (keep the creator's watermark, temp files on this drive).
5. Add a row to `backlog.md` for each: id, file, link, original creator, category, sport (or "general"), why it's proven, and a caption
   written for a repost of a classic (e.g. "This will never get old 😭", "Still can't believe this was real 🤯"). Leave "Used on" empty.
6. Show me what was added and the backlog's totals by category.
