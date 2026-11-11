# ZC2 operations: local handoff (11/10, 8 PM ET)

Operations move from the cloud review session to Claude Code on the Windows PC (`D:\Workspace\ZC2 Twitters`).
Branch: `claude/intelligent-hamilton-tmwo13`. Video files live only on the PC (`sidelinesync/`, `fitnessclip/clips/` and `kickiip/clips/` are gitignored); this repo holds rules,
logs, slates and backlogs.

## Immediate goal
Find and prepare **Wed 11/11 and Thu 11/12** for all three accounts, 10 posts a day each (60 posts). **Zero videos are ready.**
Wednesday's first posts are at 6:30 AM (@fitnessclip) and 8:00 AM (@sidelinesync), so build Wednesday first.

## Accounts

| Account | Folder | Rules | Watchlist | Posted log | Backlog | Latest slate | Logged through | Unused backlog |
|---|---|---|---|---|---|---|---|---|
| @sidelinesync (sports) | repo root | [CLAUDE.md](../CLAUDE.md) | [watchlist.md](../watchlist.md) | [posted.md](../posted.md) | [backlog.md](../backlog.md) | [slates/2026-11-10.md](../slates/2026-11-10.md) | 11/9 | 16 (almost all basketball) |
| @kickciip (streamers) | `kickiip/` | [kickiip/CLAUDE.md](../kickiip/CLAUDE.md) | [watchlist](../kickiip/watchlist.md) | [posted](../kickiip/posted.md) | [backlog](../kickiip/backlog.md) | [2026-11-10.md](../kickiip/slates/2026-11-10.md) | 11/9 (incl. 12:30 AM 11/10) | 38 (11 are celebrity-only KB007–KB030, off-niche) |
| @fitnessclip (fitness) | `fitnessclip/` | [fitnessclip/CLAUDE.md](../fitnessclip/CLAUDE.md) | [watchlist](../fitnessclip/watchlist.md) | [posted](../fitnessclip/posted.md) | [backlog](../fitnessclip/backlog.md) | [2026-11-10.md](../fitnessclip/slates/2026-11-10.md) | 11/9 | 11 |

Commands: [.claude/commands/](../.claude/commands/) (`/slates`, `/prep`, `/viral`, `/backlog`, `/logpost`, `/daily`, `/replies`).
Prefix the account (`kickiip`, `fitnessclip`); no prefix = @sidelinesync.

## Rules changed recently (details are in the linked files)
- **Fresh first** ([slates.md](../.claude/commands/slates.md)): backlog only when it beats what the search finds; scan 300–400 posts. No cap.
- **Prep is fully automated** ([prep.md](../.claude/commands/prep.md)): a clip passes every check (watermarks incl. first/last
  frames, black bars, trims, final ffprobe) or is dropped and replaced. Nothing is left for the owner to edit.
- **Caption variety** (each CLAUDE.md, "Caption style"): no repeated stock phrases ("lost it" etc.), rotate structures and emojis.
- **@kickciip**: suggestive stream clips are in; skip only for the hard limits ([kickiip/CLAUDE.md](../kickiip/CLAUDE.md)).
  Credit clip accounts as `via @account`. 12:30 AM posts are named `2430-` and belong to the previous day's folder.
- Run on **Sonnet**, `/clear` between accounts, to save usage.

## Next action (paste into Claude Code on the PC)
```
/clear
/model sonnet
git pull --no-rebase. Log 11/10 for all three accounts with /logpost exactly as slates/2026-11-10.md, kickiip/slates/2026-11-10.md and fitnessclip/slates/2026-11-10.md show (ask me whether kickiip K03 and K09 were swapped between 1:30 PM and 11:00 PM).
Then for sidelinesync, kickiip, fitnessclip in that order (/clear between accounts):
/slates <account> 2 starting 2026-11-11, then /prep <account> for 2026-11-11 and 2026-11-12. Fresh first; caption variety; kickiip 12:30 AM posts as 2430-.
Commit, git pull --no-rebase, git push. List each day's files, captions and fresh vs backlog count.
```

## Open tasks
1. Build and prep 11/11 and 11/12 (above), then schedule in X from each date folder (`sidelinesync/<date>/`, `fitnessclip/clips/<date>/`, `kickiip/clips/<date>/`) and its `captions.txt`.
2. Log 11/10 posts (all three accounts).
3. `/backlog fitnessclip 20` (11 unused). `/backlog 15` for @sidelinesync, favouring non-basketball sports and throwbacks.
   For @kickciip, move KB007–KB030 (celebrity-only) to "Retired".
4. Next regular batch: Thursday 11/12 builds Fri 11/13 – Mon 11/16.
5. `posts/josh allen 10.19.mp4` is a video file committed before the media folders were ignored. Untracking it would delete it from the
   PC on the next pull, so it was left alone; decide whether to move it out of the repo.

## Scheduled reminders (cloud)
- Re-up reminder Mon and Thu 8:15 AM ET; payday ($400 total) Mon 9:45 AM ET. They post into the cloud session; disable them
  there if they are no longer wanted.
