---
description: Draft replies to fresh posts from big accounts
---
Account: if "$ARGUMENTS" starts with an account name, this run is for that account: "kickiip" or "@kickIIP" uses the
`kickiip/` folder, and "fitnessclip" or "@fitnessclip" uses the `fitnessclip/` folder. Read and follow that folder's CLAUDE.md
instead of the root CLAUDE.md, and use that folder's copy of every file and folder named below (`<account>/watchlist.md`,
`<account>/posted.md`, `<account>/backlog.md`, `<account>/slates/`, `<account>/clips/`). Treat the rest of "$ARGUMENTS" as the
normal arguments. Otherwise this run is for @sidelinesync and uses the root files.

Following CLAUDE.md, use Playwright (read only) to find 8–10 posts from the watchlist accounts or the X search queries
that went up in the last 30–60 minutes and are picking up engagement fast.

For each one, give me the link, what the post is, and 2 reply options for @sidelinesync: one funny, one that adds something
(context, a stat, a comparison). Keep replies under 120 characters, with no links and no self-promotion.
Add them to today's slate file under "Replies". I'll post them myself.

$ARGUMENTS
