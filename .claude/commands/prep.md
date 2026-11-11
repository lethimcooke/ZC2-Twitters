---
description: Batch-download and check slate clips, then lay out captions for posting
---
Use the root `CLAUDE.md` for @sidelinesync. If `$ARGUMENTS` starts with `kickiip` or
`fitnessclip` (with or without @), use that account's folder and rules. A date selects that
slate. `all` selects upcoming slates from today onward. With neither, use today. Work
through the selected dates in posting order and skip FRESH slots until they are filled.

Media folder (`<media>/` below): @sidelinesync uses `sidelinesync/`, @fitnessclip uses
`fitnessclip/clips/`, and @kickciip uses `kickiip/clips/` (the local folder and the `kickiip`
argument stay as they are). Each holds the date folders, `backlog/`, `.prep/` and `archive/`.
Fully posted dates live in `<media>/archive/<date>/`: never prep, move or edit an archived
date, and skip any slate date whose folder is archived.

1. Read the slate (use its Revised schedule when present), the account's posted log,
   and the applicable rules. Skip clips already posted and reuse finished clips already
   verified for the same slate slot and source. Use an existing local file for a backlog clip.
   Decide any planned trim from the slate and account rules before running prep. Over-60s
   clips can use the account's existing exceptions, up to 2:20. A trim must retain the setup
   and payoff, and must not cut out a creator mark to make a clip pass.

2. Write a UTF-8 JSON manifest inside the account's gitignored `<media>/` folder for the
   remaining slots. Each entry has the final filename and either a public source URL or a
   local file path relative to the repo root. Set optional `start` and `end` in seconds
   on the source timeline when a trim is needed. For example:

   ```json
   [
     {"name":"0800-1-example.mp4","url":"https://x.com/example/status/123","start":2,"end":24},
     {"name":"1000-2-example.mp4","file":"sidelinesync/backlog/B005.mp4"}
   ]
   ```

   From the repo root, run the following once per account and date (substitute the
   account and manifest path). Use `py -3` if Windows exposes Python through that launcher.

   ```
   python scripts/prep_batch.py --account sidelinesync --manifest sidelinesync/prep-2026-11-12.json
   ```

   The script uses FFmpeg and ffprobe on PATH, plus yt-dlp if any source is a URL. It
   retries a failed download once, detects and corrects bars, applies requested trims,
   verifies H.264/AAC and duration, and writes a contact sheet for each staged clip.
   It prints counts and the location of `report.json`. Read the report for the file,
   frame timestamps, sheet, and failures. Open individual `tools.log` files only when
   diagnosing a failure. Staged files and logs live under `<media>/.prep/`. A status of
   `needs_review` means the mechanical checks passed and visual review is still due.

3. Review every staged clip against the existing account rules before promoting it.
   - Read the sampled frames (0.5s, 10%, 50%, 90%, and 0.5s before the end). Reject
     TikTok, Instagram/Reels, YouTube Shorts, Snapchat or CapCut marks, handle stamps,
     or end cards. Never crop, blur or edit them out. For a crop or trim, also inspect
     the before-edit sheet for removed marks, action, burned-in captions, or creator
     credit. Check the final crop for visible bars and the trim for a complete payoff.
     Inspect larger frames or the video when a sheet is too small to decide.
   - Accept an official league, team, organizer, or broadcaster's own caption as
     evidence for the play or result unless the footage clearly contradicts it or
     shows a different event. Attribute repost-only claims or describe what the clip
     shows. Use denser frames or local transcription only if they can change the
     caption, trim, or selection.
   - For each reject or failed download, try the slate's eligible reserves first,
     then other fresh candidates, then approved backlog. Batch replacement jobs
     together and apply the same checks. Update the slate, caption and backlog
     usage when a replacement passes. Report a gap only after suitable options are
     exhausted. Leave bulk backlog refills for a separate run.

4. Move reviewed MP4s into the account's `<media>/<date>/` folder and write
   `captions.txt` with time, filename and exact caption in posting order. Keep reserves
   under `reserves/`. If a replacement supersedes a file, move the old file out of
   the upload folder. Remove the temporary batch folder after the handoff is verified.
   Return the folder, ready count, swaps and any unfilled slots. The owner schedules
   and posts in X.

$ARGUMENTS
