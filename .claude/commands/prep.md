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
   After each download:
   - **Watermark check:** grab frames at 10%, 50% and 90% of the clip
     (`ffmpeg -ss <t> -i <file> -frames:v 1 <frame>.jpg`) and look at them. If a TikTok, Instagram/Reels, YouTube Shorts,
     Snapchat or CapCut logo or handle stamp is on the video, delete the file, mark the slot "needs swap: platform watermark"
     in the slate, and tell me. Don't crop or edit it out.
   - **Black bars:** run `ffmpeg -i <file> -vf cropdetect=24:2:0 -t 20 -f null -` and take the most common `crop=W:H:X:Y`.
     If it removes more than 2% of the width or height, re-encode with
     `ffmpeg -i <file> -vf "crop=W:H:X:Y,scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 18 -preset veryfast -c:a copy <out>`
     and replace the file. Check a frame of the result: if the crop cut into the action, a burned-in caption, or the
     creator's logo, keep the original, mark the slot "needs swap: black bars", and tell me.
4. If a download fails, say which one and why, and move on to the next. Don't retry more than once.
5. Write `clips/<date>/captions.txt`: for each clip in posting order, the time, file name, and the exact caption to paste.
6. Show me the list of files and captions, plus any slots marked "needs swap". Don't post or open X; I'll upload and schedule them myself.

$ARGUMENTS
