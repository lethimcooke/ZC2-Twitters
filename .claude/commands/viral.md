---
description: Swap in the hottest viral clips right before scheduling (on demand)
---
Account: if "$ARGUMENTS" starts with an account name, this run is for that account: "kickiip" or "@kickciip" uses the
`kickiip/` folder, and "fitnessclip" or "@fitnessclip" uses the `fitnessclip/` folder. Read and follow that folder's CLAUDE.md
instead of the root CLAUDE.md, and use that folder's copy of every file and folder named below. Otherwise this run is for
@sidelinesync and uses the root files.

The owner runs this on demand ("force feed viral videos") just before scheduling: grab what's blowing up right now and swap
it into the slates.

How many and which days: a number in "$ARGUMENTS" is how many posts to swap per day (default 4); dates in "$ARGUMENTS" are the
days to change (default: the next day that hasn't been scheduled yet). "all" means every slot on those days.

1. git pull. Read the account's CLAUDE.md, watchlist.md, posted.md and the slates for those days.
2. Sweep the big clip accounts listed in watchlist.md (and the account's other sources) for posts from the last 24–48 hours
   that are taking off. Rank by views and likes for the account. Run the niche check and the video rules on each.
3. For each day, replace the weakest slots (backlog clips first, then the lowest-potential new clips) with the hottest finds,
   keeping each day at 10 posts and the account's mix and per-person limits. Put the hottest at the primetime slots.
   Swapped-out backlog clips get their "Used on" cleared; swapped-out new clips go to Reserves.
4. Download each new clip into that day's clips folder with the slot's time prefix and run every `/prep` check on it
   (watermarks including first/last frames, black bars, trims, final file check). A clip that fails is dropped and the next
   find takes the slot; nothing is left for the owner to edit or check. Delete the replaced files by name, and rewrite that
   day's captions.txt.
5. Add a "Viral swap (<date/time>)" section to each slate, commit "viral swap <dates>", git pull --no-rebase, git push, and
   leave the research browser on x.com/home.
6. Show me a table: date, time, old clip, new clip file, caption, so I can schedule (or swap) them in X.

Clip-account scouting (every run, every account): whenever you come across a clipping or repost account posting viral clips in
this account's niche that isn't already in the watchlist, add it under "Discovered" in the account's watchlist.md with its
handle, what it posts, its typical likes/views, and the date. If a discovered account turns up with viral posts in 2 or more
runs, move it up to the account's main list of accounts to check first. Report the new ones in your summary.
