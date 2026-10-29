# @kickIIP: streamer and celebrity clip account

This file replaces the root `CLAUDE.md` whenever a command is run for @kickIIP. Ignore the @sidelinesync rules
(including its niche check, which rejects streamer and celebrity clips) when working on this account.

Goal: 10 posts a day of the most viral **streamer** clips, with credit. Narrowed 10/29: streamers only.
We don't need to be first. We need clips that make people stop scrolling, reply, quote-post and repost.

## Tools
Same as @sidelinesync: Playwright (the same research account, read only: never like, follow, post, reply or DM),
vidIQ (TikTok/Instagram/YouTube outliers), and yt-dlp for downloads. Never log into TikTok, Instagram, Kick or Twitch.
Kick, Twitch and YouTube clip links can be downloaded with yt-dlp the same way as X and TikTok.

## Files (all inside `kickiip/`)
- `kickiip/watchlist.md`: clip accounts, streamers, and X search queries.
- `kickiip/posted.md`: every clip posted on @kickIIP. Never repost a clip.
- `kickiip/slates/YYYY-MM-DD.md`: each day's slate.
- `kickiip/backlog.md` and `kickiip/clips/backlog/`: proven classics to fall back on (60 days between reposts).
- `kickiip/clips/<date>/`: downloaded videos (on the PC only).

## Niche check
A clip is in the niche if it's one of these:
- **Streamer moments**: big reactions, IRL stream chaos, collabs, pranks, challenges, fails, funny or wholesome moments
  from popular streamers (Kick, Twitch, YouTube), including streamers at sports events.
- **Streamers with celebrities**: a celebrity on a stream, at a streamer's event, or meeting a streamer IRL counts.
  A celebrity clip with no streamer in it (talk shows, red carpets, concerts, interviews) does not.
- **Streamer culture**: streamer collabs, events, IRL trips, fan run-ins, chat moments, clips from streamer podcasts.

Reject it, whatever its numbers, if it's:
- politics, elections or political memes
- slurs, hate, harassment, or a pile-on against a private person
- sexual content or nudity, or anything sexualizing or demeaning a minor
- gambling or casino streams, betting promos, sponsor reads, ads or giveaways
- graphic violence or injuries, real fights, crime, police, or mocking someone who's hurt
- doxxing or anything showing someone's private info (addresses, phone numbers, messages)
- AI-generated or deepfake clips, fake quotes, or edits made to look real
- rumors or accusations about a real person presented as fact

Profanity in the clip is fine; slurs are not. Look at the video itself before suggesting it. If unsure, leave it out.

## Credit
- Credit the streamer or celebrity's channel and the clipper if there is one: `🎥: @streamer (clip: @clipper)`.
- If the clip came from a show, podcast or broadcast, credit that: `🎥: @show`.
- Repost accounts are where we find clips, not who we credit. If the source can't be found, use `via @account` and rank it lower.
- Keep the original watermark on the video.

## Rules for picking clips
- Prefer clips from the last 24–48 hours with high engagement for their account size.
- 5–60 seconds, the payoff in the first 3 seconds. Clips that need sound are fine here if burned-in captions or the
  caption text set up the joke.
- Mix: all 10 are streamer clips. No more than 2 from one streamer per day, and aim for at least 5 different streamers a day,
  so the feed isn't only Kai and Speed.
- Skip anything already all over the timeline for 2+ days.

## Caption style
- Hook first, under ~100 characters, conversational. Emojis on most captions (1–2): 😭😂 funny, 💀 fail, 😳 wild, 🥹 wholesome.
- No hashtags (or 1 at most), no links.
- Credit on its own line.
- Only describe what happens in the clip. No claims about anyone's private life, motives, or behavior off camera.
- Every few posts, end with a question that gets replies ("Who had the better reaction?", "Would you do this?").

## Backlog classics (for `/backlog kickiip`)
What counts as a proven classic here: iconic stream moments that get reposted again and again: legendary streamer reactions,
famous IRL stream moments, all-time collab and chat moments. Celebrity-only clips don't count.
- Search X with no date limit and high thresholds, e.g.
  `(stream OR streamer OR "on stream") filter:native_video min_faves:50000 <exclusions>`,
  `("Kai Cenat" OR IShowSpeed OR "Adin Ross" OR xQc OR Kick OR Twitch) filter:native_video min_faves:50000 <exclusions>`,
  plus the clip accounts' most-liked posts. Use the exclusion list from `kickiip/watchlist.md`.
- It must still land today: no references to a feud, relationship, lawsuit or news story that has since changed,
  and nothing from a person who is now known mainly for a scandal.
- Same niche check and credit rules as above. Captions written for a classic: "This will never get old 😭",
  "Still the funniest stream moment ever 💀", "The internet will never let this go 😂".

## Posting times (ET, adjust from results)
10:00 AM, 12:00, 1:30, 3:00, 5:00, 7:00, 8:30, 10:00, 11:00 PM, 12:30 AM.
This audience is later than sports: strongest clips at 7:00, 10:00 and 11:00 PM.
