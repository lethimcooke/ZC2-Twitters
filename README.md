# @sidelinesync workspace

The daily workflow for running @sidelinesync with Claude Code.

## Setup (once)
1. Install Playwright for Claude Code (in a normal terminal, not a Claude chat):
   ```
   claude mcp add playwright -s user -- npx @playwright/mcp@latest
   ```
2. Start `claude` in this folder, type `/mcp`, and check that `playwright`, `vidIQ` and `MCP Market Hub` are listed.
3. Tell Claude "Use Playwright to open x.com/login", then log into the research account yourself in the browser window that opens.

## Daily use
One-time for `/prep`: `winget install yt-dlp` and `winget install Gyan.FFmpeg`, then open a new terminal.

Run `claude` in this folder, then:
- `/slates 3`: build all 30 posts for the next 3 days at once. Do this every 3 days (a reminder fires each time).
- `/backlog 20`: download 20 proven viral clips into `clips/backlog/` to fall back on.
- `/daily fresh`: fill any FRESH slots the morning of, or swap one (`/daily fresh 8:00 AM`).
- `/daily`: find clips, pick the 10 best and write captions. Saved to `slates/<date>.md`.
- `/replies`: draft replies to fresh posts from big accounts. Run it 2–3 times a day.
- `/prep all`: download every upcoming slate's clips (or `/prep` for today only) into `clips/<date>/` with a captions file, ready to upload.
- `/logpost`: record what you posted so we never post the same clip twice.

After you finish for the day, run `git add -A && git commit -m "slate <date>" && git push` so the log stays in sync.
