---
description: Download today's slate clips and lay out captions for posting
---
Get posts ready to upload, following CLAUDE.md.
Which days: if "$ARGUMENTS" names a date, do that day; if it says "all", do every slate from today onward; otherwise do today.
Run the steps below for each day, using `clips/<that day's date>/`. Skip FRESH slots that haven't been filled yet.

1. Read the day's slate in `slates/` (use the "Revised schedule" section if there is one) and `posted.md`.
   Skip anything already in `posted.md`.
2. Check `yt-dlp --version` works. If it doesn't, stop and tell me to run `winget install yt-dlp` and `winget install Gyan.FFmpeg`.
3. For each scheduled clip, download it with yt-dlp into `clips/<date>/` named `<time>-<#>-<short-name>.mp4`
   (e.g. `1200-6-tapeball-catch.mp4`), as an mp4 X accepts (H.264 video, AAC audio):
   `yt-dlp -f "bv*[vcodec^=avc]+ba[acodec^=mp4a]/b[ext=mp4]/b" --merge-output-format mp4 -P "temp:clips/.tmp" -o "<path>" "<link>"`
   (`-P temp:` keeps yt-dlp's temporary files on this drive instead of C:, which is nearly full. Delete `clips/.tmp` when done.)
   For TikTok, pick the format that keeps the creator's watermark where yt-dlp lists one (run `-F` to see formats).
   Never use a watermark-removal tool or service.
4. If a download fails, say which one and why, and move on to the next. Don't retry more than once.
5. Write `clips/<date>/captions.txt`: for each clip in posting order, the time, file name, and the exact caption to paste.
6. Show me the list of files and captions. Don't post or open X; I'll upload and schedule them myself.

$ARGUMENTS
