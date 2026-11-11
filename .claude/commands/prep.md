---
description: Download today's slate clips and lay out captions for posting
---
Account: if "$ARGUMENTS" starts with an account name, this run is for that account: "kickiip" or "@kickIIP" uses the
`kickiip/` folder, and "fitnessclip" or "@fitnessclip" uses the `fitnessclip/` folder. Read and follow that folder's CLAUDE.md
instead of the root CLAUDE.md, and use that folder's copy of every file and folder named below (`<account>/watchlist.md`,
`<account>/posted.md`, `<account>/backlog.md`, `<account>/slates/`, `<account>/clips/`). Treat the rest of "$ARGUMENTS" as the
normal arguments. Otherwise this run is for @sidelinesync and uses the root files.

Get posts ready to upload, following CLAUDE.md.
Which days: if "$ARGUMENTS" names a date, do that day; if it says "all", do every slate from today onward; otherwise do today.
Run the steps below for each day, using `clips/<that day's date>/`. Skip FRESH slots that haven't been filled yet. For a backlog clip, copy its file from `clips/backlog/` instead of downloading it again.

1. Read the day's slate in `slates/` (use the "Revised schedule" section if there is one) and `posted.md`.
   Skip anything already in `posted.md`.
2. Check `yt-dlp --version` works. If it doesn't, stop and tell me to run `winget install yt-dlp` and `winget install Gyan.FFmpeg`.
3. For each scheduled clip, download it with yt-dlp into `clips/<date>/` named `<time>-<#>-<short-name>.mp4`
   (e.g. `1200-6-tapeball-catch.mp4`), as an mp4 X accepts (H.264 video, AAC audio):
   `yt-dlp -f "bv*[vcodec^=avc]+ba[acodec^=mp4a]/b[ext=mp4]/b" --merge-output-format mp4 -P "temp:clips/.tmp" -o "<path>" "<link>"`
   (`-P temp:` keeps yt-dlp's temporary files on this drive instead of C:, which is nearly full. Delete `clips/.tmp` when done.)
   Never use a watermark-removal tool or service.
   After each download, run every check below yourself. **The owner never edits, trims, crops or re-checks a video
   (owner's rule, 11/5):** what you leave in the folder gets posted as-is, so a clip either passes every check or is dropped.
   - **Watermark check:** grab frames at 0.5s, 10%, 50%, 90% and 0.5s before the end
     (`ffmpeg -ss <t> -i <file> -frames:v 1 <frame>.jpg`) and look at them. The first and last frames catch TikTok/Reels
     end-cards. If a TikTok, Instagram/Reels, YouTube Shorts, Snapchat or CapCut logo, handle stamp or end-card is on the
     video, delete the file and drop the clip. Never crop, blur or edit a watermark out.
   - **Black bars:** run `ffmpeg -i <file> -vf cropdetect=24:2:0 -t 20 -f null -` and take the most common `crop=W:H:X:Y`.
     If it removes more than 2% of the width or height, re-encode with
     `ffmpeg -i <file> -vf "crop=W:H:X:Y,scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 18 -preset veryfast -c:a copy <out>`
     and replace the file. Check a frame of the result: if the crop cut into the action, a burned-in caption, or the
     creator's logo, drop the clip.
   - **Length:** if the slate says to trim, or the clip is over 60s and the rules call for a trim, do the trim here with ffmpeg
     (`-ss <start> -to <end>`, H.264/AAC) and check frames of the result. Never leave a trim, plug cut or edit for the owner.
     Anything over 2:20 after trimming is dropped.
   - **Final check of the finished file:** it plays (ffprobe shows H.264 video and AAC audio, a duration over 5s), there are no
     bars, no other platform's marks, and nothing in it breaks the account's niche or reject list. If you're unsure about
     any check, drop the clip; don't hand the question to the owner.
   - **Caption claims (owner, 11/11, all accounts):** when an official league, team, event organizer or broadcaster describes the
     play or result in the caption of its own post, that caption is sufficient evidence. Use its description in our caption
     (if the NBA calls it a buzzer-beater, or MLB says two baseballs collided, we say so). A contact sheet or dense frames that
     miss the exact instant are not a reason to drop the clip or to keep trying to prove it. If the claim comes only from a
     repost or fan account, attribute it ("per @account") or stick to what the footage shows. Investigate only when the footage
     clearly contradicts the caption or seems to show a different event. All other checks on this list still apply.
   - **Dropped clips get replaced, not flagged.** Fill the slot from the slate's Reserves first (download and run these same
     checks), then from other fresh clips found in this batch, then from `backlog.md` (checked the same way). Update the
     slate's schedule and caption for that slot, clear or fill "Used on" in `backlog.md`, and list the swap in your summary.
     Only leave a slot empty if nothing passes, and say so at the top of the summary.
4. If a download fails, retry once; if it still fails, replace the slot the same way as a dropped clip and say why in the summary.
5. Write `clips/<date>/captions.txt`: for each clip in posting order, the time, file name, and the exact caption to paste.
   Every file in the day folder must be one that gets posted; move reserves to `clips/<date>/reserves/`.
6. Show me the list of files and captions, plus the swaps you made and why. The folder must be ready to upload as-is: no
   "check this", "trim this" or "needs swap" notes for the owner. Don't post or open X; I'll upload and schedule them myself.

$ARGUMENTS
