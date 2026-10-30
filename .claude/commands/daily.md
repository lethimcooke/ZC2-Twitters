---
description: Find today's clips and build the 10-post slate
---
Account: if "$ARGUMENTS" starts with an account name, this run is for that account: "kickiip" or "@kickIIP" uses the
`kickiip/` folder, and "fitnessclip" or "@fitnessclip" uses the `fitnessclip/` folder. Read and follow that folder's CLAUDE.md
instead of the root CLAUDE.md, and use that folder's copy of every file and folder named below (`<account>/watchlist.md`,
`<account>/posted.md`, `<account>/backlog.md`, `<account>/slates/`, `<account>/clips/`). Treat the rest of "$ARGUMENTS" as the
normal arguments. Otherwise this run is for @sidelinesync and uses the root files.

Run today's clip search for @sidelinesync, following CLAUDE.md.

If "$ARGUMENTS" contains "fresh": today's slate already exists from `/slates`. Only fill its FRESH slots, with clips from the
last 24 hours (last night's games first), using steps 1, 2 and 4 below with a shortlist of 5. Write the clips and captions into
those slots in today's slate file and show me just those. Skip the rest of this list.
If "$ARGUMENTS" also names times (e.g. "fresh 8:00 AM"), replace the clips in those slots with fresh ones the same way,
moving the clip that was there to Reserves.

1. Read `posted.md` and `watchlist.md`.
2. With Playwright, run the X search queries in `watchlist.md` (replace `<exclusions>` with the exclusion list) and skim the watchlist accounts.
   Only read; don't interact with anything.
3. With vidIQ, run outlier searches on TikTok and Instagram for a few of the vidIQ terms.
4. Run the niche check and the Video rules (no other platforms' watermarks, no black bars that can't be cropped cleanly) from CLAUDE.md on every candidate and drop anything that fails. Find the original creator for each one that passes.
   Make a shortlist of 15 clips we haven't posted. Show it as a table: #, link, original creator, found via, platform, views/likes, age, length, category, why it should do well.
   Under the table, list how many candidates you rejected and why (e.g. "6 politics, 2 graphic"), so I can see the filter working.
5. Pick your top 10 and assign them to the posting times in CLAUDE.md, with the strongest clips at 12:00, 7:00 and 10:00 PM.
6. Write a caption for each one following the caption style (hook, credit line, a question on some).
7. Save everything to `slates/<today's date>.md`, then show me the slate.

$ARGUMENTS
