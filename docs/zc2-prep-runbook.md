# ZC2 prep runbook

One workflow for the Monday and Thursday scheduled prep runs and for any manual batch. It is the workflow that produced
Friday 11-13 through Monday 11-16 (120 of 120 clips ready). The scheduled tasks read this file at the start of each run.

## Scope and targets
- Accounts: @sidelinesync (media in `sidelinesync/`), @fitnessclip (`fitnessclip/clips/`), @kickciip (local folder `kickiip/`, media in `kickiip/clips/`, `/prep` and script argument `kickiip`).
- Each account needs 10 upload-ready clips per day.
- Monday run prepares Tuesday, Wednesday and Thursday (90 clips). Thursday run prepares Friday, Saturday, Sunday and Monday (120 clips).
- If a run starts late, keep the original dates and skip slots that have already passed.
- The owner schedules and posts in X. Never post, like, follow, reply or DM from the research account.

## Before sourcing
1. `git pull --ff-only` from the repo root. If it is blocked, keep local work and raise a blocker.
2. Read the latest `sidelinesync/checkpoint-*.md` if one exists for these dates and resume from it. Skip batches already finished.
3. Use one signed-in Playwright session for the whole run. If it reports "browser already in use", find the owner first
   (look for the Chrome process whose `--user-data-dir` ends in `mcp-chrome-5b3266f` and trace its parent MCP server to a session).
   Ask that session to close its browser. Never kill unknown processes.
4. Never log into TikTok, Instagram, Kick or Twitch. Leave the browser on `x.com/home` when the run ends.

## Per-day loop (one day at a time, all three accounts together)
1. **Source.** For the day, gather links and engagement for all three accounts in batches, using each account's `watchlist.md`
   queries, approved accounts and the clip accounts it lists. Scroll 4 or 5 screens per query. Timely clips for the first day,
   strong fresh evergreen clips for later days. Pick 10 per account plus alternates.
2. **Dedupe once.** Check every status ID against `posted.md` files, all `slates/` files and existing `prep-*.json` manifests
   (`grep -l <id>`). Check duration with `yt-dlp --skip-download --print duration`. Drop anything over 140 seconds unless it will be trimmed.
3. **Save picks before opening any sheet.** Write one manifest per account and batch in the account's media folder, for example
   `fitnessclip/clips/prep-2026-11-14.json`, then `-14b`, `-14c` for refill batches. Entry names look like `1330-4-short-name.mp4`
   (HHMM slot, number, name). Use `url` for X posts and `file` for local backlog or saved candidate files inside the same media folder.
4. **Batch-prep.** From the repo root, one command per account and manifest:
   `python scripts/prep_batch.py --account <sidelinesync|fitnessclip|kickiip> --manifest <media folder>/prep-<date>.json`
   Reuse successful downloads and existing contact sheets. Never write ad hoc ffmpeg crops or montages for a whole batch.
5. **Review last.** Stack the `review.jpg` sheets from `report.json` into one image per batch and read them (see rejects below).
   Open `tools.log` only to diagnose a failure.
6. **Reopen slots.** Every failed download, length failure or rejected clip goes back on the open-slot list immediately.
   Fill from fresh alternates, then a targeted fresh search for just those slots, then eligible reserves, and only then backlog.
7. **Finalize.** Copy the accepted staged MP4s into `<media>/<date>/` named by slot, write `captions.txt`, keep reserves in `reserves/`.
   Staging stays in `<media>/.prep/`. Verify every final file is H.264/AAC and 5 to 140 seconds, 10 per account.
8. **Write the slate** for each account and date (`slates/`, `fitnessclip/slates/`, `kickiip/slates/`): schedule table, links, credits, rejects.
9. **Commit and push** the slates and tracking edits only (`git add` the specific files). Media, manifests, checkpoints and `.prep/` stay local and ignored.
10. **Checkpoint** (below), then start the next day.

## Review rejects (learned in the Nov 13-16 batch)
Reject and reopen the slot for:
- TikTok, Instagram, Shorts, Snapchat or CapCut marks, app UI overlays, or another account's handle stamp. Never crop or blur them out.
- Black bars or pillarboxing that cannot be cropped without losing action or the creator's mark.
- AI-generated or CGI mannequin clips, composite clips, and app or paid-program promo end cards.
- Injuries or someone on the ground, kids in distress, and clips filmed off a TV screen.
- Thirst or physique-pose framing with no real training, and stranger-filming or call-out clips.
- A repeat of a clip, play or story already used within the window (same play from a different account, a third Cousins clip in four days).
- Anything unclear after reading the sheet. If unsure, leave it out.
Account rules still apply: fitness `fitnessclip/CLAUDE.md`, kick `kickiip/CLAUDE.md`, sports root `CLAUDE.md`. Official league, team or broadcaster captions count as evidence.

## Captions
- Hook under about 100 characters, one or two emojis, credit on its own line (`🎥: @creator` or `via @account`).
- State only what the post text, official caption or frames show. Attribute repost-only claims ("reported", "per @account", `via`).
- Vary wording against the last week of slates and avoid the stock phrases listed in each account's `CLAUDE.md`. Rotate emojis.
- Run the stop-slop skill over captions and any written report before delivering: no em dashes, no filler, no adverbs.

## Checkpoints
After each day, append to `sidelinesync/checkpoint-<first-date>-<last-date>.md` (gitignored, local):
- which day and stage is complete, ready count out of 30 (10 per account),
- exact open slots (account, date, time) and why,
- unused saved alternates with links, and weak slots to swap first,
- timings (sourcing, prep, review) and the number of permission prompts.
If usage runs out mid-day, leave staged files, captions drafted and the open-slot list here so the next run resumes from it.

## Folder layout and archiving
- Final MP4s and `captions.txt` in `<media>/<date>/`, reserves in `<media>/<date>/reserves/`, staging in `<media>/.prep/`, backlog in `<media>/backlog/`.
- The @kickciip 12:30 AM slot posts after midnight but lives in the prior day's folder as `2430-...`; log it on the next calendar date.
- Archive a date to `<media>/archive/<date>/` only after every post for it is confirmed in `posted.md`, including @kickciip's after-midnight slot.
  Never prep, move or edit an archived date.

## Backlog
Use backlog only as a last resort for a slot. Build or refill it only after the whole batch is ready and there is time and usage left.
Start from strong unused candidates already found in the run, dedupe, run the usual media checks, and save passing clips with source and caption.
Stop when usage is tight and report the count added per account.

## Permissions and mode
- Scheduled prep runs should run in Auto mode.
- `.claude/settings.local.json` holds three narrow allow rules, one per account: `python scripts/prep_batch.py --account <acct> --manifest <media folder>/prep-*.json`.
  The file is ignored by git and must stay local. Do not widen the rules or add broad shell access. Record the exact command once if something still prompts, then keep working on whatever can proceed.

## Blockers and notifications
Send a push notification (the PushNotification tool: desktop, plus phone when Remote Control is on) only for a blocker that threatens coverage
or needs the owner. One line, under 200 characters, this shape:
`ZC2 <Mon|Thu> prep BLOCKED: <date> <account> ready <n>/10. Action: <exact action>.`
Examples of real blockers: Playwright profile locked by another session and not releasable, sign-in expired, git pull blocked, usage limit with open slots, a tool prompt that stops all prep.
No notification for routine progress or a clean finish. Test messages start with `TEST ALERT:`.

## Final report (keep it short)
Per day: ready out of 30, folder paths, open slots, weak slots, time spent sourcing, prepping and reviewing, permission prompts.
Then remaining blockers and the next run time. Scheduling and posting stay with the owner.
