---
description: Build slates for several days ahead (default 3)
---
Build posting slates for the next several days for @sidelinesync, following CLAUDE.md.
Number of days: the number in "$ARGUMENTS" if there is one, otherwise 3. Never more than 5: clips go stale.
Start from tomorrow unless I say "starting today".

1. Read `posted.md`, `watchlist.md` and every file in `slates/`. A clip that appears in any slate or in `posted.md` can't be used again.
2. Search the same way as `/daily` (X queries with the exclusion list, watchlist accounts, vidIQ outlier searches),
   but collect about 10 candidates per day plus 5 spares. Run the niche check and find the original creator for each.
3. Label every clip:
   - **timely**: tied to a specific game, result or moment from the last 48 hours. It must be scheduled on the first day.
   - **evergreen**: trick shots, skills, fails, crowd moments, kids, wholesome, funny. These can go on any day.
4. Each day has 10 slots (times in CLAUDE.md).
   - Day 1: fill all 10, putting timely clips first.
   - Day 2 onward: fill 8 with evergreen clips and leave the 8:00 AM and 8:30 PM slots as **FRESH**.
     I fill those the morning of with `/daily fresh`, so each day still has something from the night before.
   - Follow the mix and per-sport limits for each day separately. Spread the strongest clips across days
     instead of front-loading them, so every day has strong 12:00, 7:00 and 10:00 PM posts.
5. Write one file per day, `slates/<date>.md`, with the schedule table (time, #, clip, link, credit, timely/evergreen)
   and the caption for each slot. Put the spares under "Reserves" in the last day's file.
6. Show me a summary: one line per day with its 3 primetime clips, plus anything you're unsure about.
