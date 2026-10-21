# @sidelinesync: viral repost account

Goal: 10 posts a day of the most viral clips we can find, with credit to the creator.
The niche is all sports and anything else that's going viral (crazy moments, fails, crowd moments, wholesome stuff, funny clips).
We don't need to be first with news. We need clips that make people stop scrolling, reply and repost.

## Tools
- **Playwright**: a browser logged into the separate research account. Use it to search and read X only.
  Never like, follow, post, reply or DM from it. Scroll at a human pace; don't open hundreds of pages in a row.
- **vidIQ**: TikTok and Instagram clips getting far more views than usual for their creator
  (`vidiq_instagram_tiktok_outlier_search`, `vidiq_trending_videos`). Use these as a second source.
  To check a TikTok or Instagram clip, open its public page in Playwright without logging in. Close any login or app pop-up.
  Never log into TikTok or Instagram. If a page won't show without a login, judge the clip from vidIQ's data and thumbnail
  (and say so in the shortlist), or skip it.
- **MCP Market Hub social-content**: hook formulas, caption templates and engagement routines.

## Files
- `watchlist.md`: accounts to check and X search queries to run.
- `posted.md`: every clip we've posted. Check it before suggesting anything so we never repost a clip.
- `slates/YYYY-MM-DD.md`: each day's shortlist, captions and reply drafts.
- `backlog.md`: proven viral clips already downloaded to `clips/backlog/`, used when a slate is short or a planned clip goes stale.
  A backlog clip can be reposted once every 60 days.

## Niche check (run on every candidate before it goes on a shortlist)
A clip is in the niche only if it's one of these:
- **Sports**: games, highlights, athletes, fans, stadiums, youth/high school/college, extreme and action sports, trick shots.
- **Viral physical/skill moments**: stunts, near misses, fails, impressive skills, crowd moments.
- **Feel-good or funny** clips that aren't about news.

Reject it, whatever its numbers, if it's:
- politics, politicians, elections or political memes
- war, military, police, crime, protests or breaking news
- graphic injuries, blood, fights outside a sport, or mocking someone who's hurt
- celebrity gossip with no sports or skill angle, ads, giveaways, AI-generated clips, or staged clips passed off as real
  (obvious comedy skits are fine).

Before suggesting a clip, look at the video itself (open the post and check the thumbnail/first frames), not just the post text.
If you're unsure which bucket it's in, leave it out.

## Finding the original creator
- Big repost accounts (e.g. @HaterReport, @DailyLoud, @PopBase, @OnlyBangers, @crazyclips_) are where we *find* clips, not who we credit.
- Look for the original: a watermark or handle on the video, "🎥:" or "via" in the post or replies, or the earliest post of the same clip.
- Credit the original creator: `🎥: @creator`. If you can't find them, mark the clip "creator unknown" in the shortlist
  and rank it lower; if it's used, credit the account we found it on: `via @account`.

## Rules for picking clips
- Prefer clips from the last 24–48 hours with high engagement for their account size (an outlier for that account, not just a big account).
- 5–60 seconds, understandable with the sound off, the payoff in the first 3 seconds.
- Mix: about 6 sports, 4 general viral. No more than 2 from one creator or one sport per day.
- Skip anything already all over the timeline for 2+ days.
- Always record the original creator's handle and link. Keep the creator's original watermark on the video.

## Caption style
- Hook first, under ~100 characters. Short, punchy and conversational.
- Emojis on most captions (1–2, at the end of the hook line). Match the clip: 😭😂 funny, 🤯😳 unreal, 🔥 big play, 🥹 wholesome, 💀 fail.
- No hashtags (or 1 at most), and no links in the post.
- Credit on its own line: `🎥: @creator`
- Only state facts you checked from the clip or post (names, "rookie", he/she, the score). If unsure, leave it out.
- Say "touchdown"/"TD", not "for six", for football.
- Every few posts, end with a question that gets people replying ("Rate this 1–10", "Who you got?", "Would you have caught that?").

## Posting times (ET, adjust from results)
8:00, 10:00, 12:00, 1:30, 3:00, 5:00, 7:00, 8:30, 10:00, 11:30 PM.
Put the strongest clips (highest outlier ratio, not raw views) at 12:00, 7:00 and 10:00 PM.
Clips about last night's games lose value fast: post them in the morning slots.
Put NFL clips during or right after a prime-time NFL game (Thursday, Sunday or Monday night) when one is on.
Creator-unknown clips go in reserves unless the slate is short.
