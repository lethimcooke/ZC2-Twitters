---
description: Build slates for several days ahead (default 3)
---
Account: if "$ARGUMENTS" starts with an account name, this run is for that account: "kickiip" or "@kickIIP" uses the
`kickiip/` folder, and "fitnessclip" or "@fitnessclip" uses the `fitnessclip/` folder. Read and follow that folder's CLAUDE.md
instead of the root CLAUDE.md, and use that folder's copy of every file and folder named below (`<account>/watchlist.md`,
`<account>/posted.md`, `<account>/backlog.md`, `<account>/slates/`, `<account>/clips/`). Treat the rest of "$ARGUMENTS" as the
normal arguments. Otherwise this run is for @sidelinesync and uses the root files.

Build posting slates for the next several days for @sidelinesync, following CLAUDE.md.

Weekly rhythm (all accounts): I build slates only on weekdays and do no scheduling work on Saturdays or Sundays.
- **Monday batch:** Tuesday, Wednesday, Thursday (3 days).
- **Thursday batch:** Friday, Saturday, Sunday, Monday (4 days), so the weekend and Monday are scheduled before Friday starts.
If "$ARGUMENTS" has no number of days: run on a Monday builds Tue–Thu, run on a Thursday builds Fri–Mon, and any other day
builds through the next Monday or Thursday batch day, whichever comes first, so no day is ever left uncovered.
A number in "$ARGUMENTS" overrides this. Never more than 5 days: clips go stale. Start from tomorrow unless I say "starting today".

Weekend rules (Saturday and Sunday must need zero work from me):
- Fill all 10 slots on Saturday and Sunday. Never leave a weekend slot FRESH, and never write "swap this in with
  `/daily fresh`" as something to do on a weekend; a weekend swap can only be an optional extra.
- Weekend and Monday slots use fresh evergreen clips found in this batch (posted in the last few days, not tied to one game or
  news moment), not timely ones that will be stale by then. Backlog is the last resort here too (see the backlog rule below).
- The Monday after a weekend is built in the Thursday batch, also fully filled, so nothing has to be done before Monday's posts.
- If the account's backlog has fewer than 20 unused clips when a Thursday batch starts, say so first: the weekend depends on it.

1. Read `posted.md`, `watchlist.md` and every file in `slates/`. A clip that appears in any slate or in `posted.md` can't be used again.
2. Search the same way as `/daily` (X queries with the exclusion list, watchlist accounts, vidIQ outlier searches),
   but collect about 12 candidates per day plus 5 spares. Run the niche check and the Video rules (no other platforms' watermarks, no black bars that can't be cropped cleanly) and find the original creator for each.
3. Label every clip:
   - **timely**: tied to a specific game, result or moment from the last 48 hours. It must be scheduled on the first day.
   - **evergreen**: trick shots, skills, fails, crowd moments, kids, wholesome, funny. These can go on any day.
4. Each day has 10 slots (times in CLAUDE.md), and all 10 get filled: I schedule all 30 posts at once.
   - Day 1 gets the timely clips first. Days 2 and 3 are mostly evergreen; a timely clip can only go on a later day
     if it will still be under ~72 hours old when it posts.
   - Follow the mix and per-sport limits for each day separately.
   - Evergreen clips age too: put the biggest outliers and the oldest clips on the earliest days, but keep a strong
     clip at 12:00, 7:00 and 10:00 PM every day.
   - **Fresh first, backlog last (owner's rule, 11/5).** Backlog clips are always the least fresh, so a batch fills every day
     with new clips found in this run before touching `backlog.md`. Keep searching until you have about 12 fresh candidates per
     day: more queries, more watchlist and clip accounts, vidIQ, and evergreen posts from the last 3–5 days for the later days.
     Scan at least 300–400 posts before deciding fresh supply has run out.
   - Backlog: no fixed cap. Weigh each slot on viral potential: a fresh clip with real viral potential beats a backlog clip, and
     a proven viral backlog clip or throwback (even weeks old) beats a weak fresh clip. Use backlog only when the search can't
     find fresh clips good enough. Backlog clips must not have been used in the last 60 days. Copy the file path and caption
     into the slate, and fill in "Used on" in `backlog.md`. In the summary, say why each day's backlog clips beat what you found.
   - The backlog's main job is emergency cover: when a day's posts are missed, I may ask for "x clips from the backlog" to fill it.
   - Only leave a slot FRESH (filled the morning of with `/daily fresh`) if I ask for it, or if the only clips left
     for it are weak, creator-unknown or borderline. Say so in the summary if you do.
   - Collect about 12 candidates per day plus 5 spares so there's room to drop weak ones.
5. Write one file per day, `slates/<date>.md`, with the schedule table (time, #, clip, link, credit, timely/evergreen)
   and the caption for each slot. Put the spares under "Reserves" in the last day's file.
6. Show me a summary: one line per day with its 3 primetime clips, the number of fresh vs backlog clips per day, how many posts
   you scanned, plus anything you're unsure about.

Clip-account scouting (every run, every account): whenever you come across a clipping or repost account posting viral clips in
this account's niche that isn't already in the watchlist, add it under "Discovered" in the account's watchlist.md with its
handle, what it posts, its typical likes/views, and the date. If a discovered account turns up with viral posts in 2 or more
runs, move it up to the account's main list of accounts to check first. Report the new ones in your summary.
