# Publish gate

Track A (content). Nothing here is live. Nothing has been pushed to WordPress.

## Before a draft is created in WordPress

- [ ] KK rules on the **meetup number** flag in `source-manifest.md` (spoken "32 in a row" vs written "#31" everywhere else). `post.md` currently sidesteps it.
- [ ] KK reads `post.md` for voice. It is written first person as him and makes a political prediction under his name in an active municipal campaign.
- [ ] Confirm he is comfortable being on record that AI will be "probably the primary" election issue. That is his own recorded quote, but a blog post carries further than a podcast.

## Timing

The episode is from 2026-08-09 and the meetup from 2026-07-29. This draft is dated 2026-09-07. The month of lag is now **load-bearing rather than a liability**: the piece uses it to show the prediction was tested and held, via The Tyee's Aug 11 party scorecard.

- [ ] Re-check the data centre file before publish. If council, planners, or the consultation timeline moved since Aug 11, the second and third sections need updating. This is the load-bearing claim in the piece.
- [ ] Re-check whether any of the seven parties has changed position since Aug 11.
- [ ] Kris's recorded commitments (demonstrations, town hall) are written in past tense on purpose. Do not "freshen" them into the present.

## Political exposure

The piece now names seven civic parties and characterizes their positions during an active municipal campaign.

- [ ] KK confirms he is comfortable naming parties under his own byline. The characterizations come from The Tyee and are linked, but the aggregation is his.
- [ ] Positions are reported, not ranked or endorsed. Keep it that way through any edit.
- [ ] This stays a **personal** post. It must not read as a BC + AI Ecosystem Association position on a municipal election. See the note at the bottom of `social-content.md`.

## Before publish

- [ ] Featured image through `featured-image-forge` with multi-ratio QC and explicit approval. No hero ships without it.
- [ ] SEO title and description set **by hand in the editor**, not via REST. Jetpack is deactivated, so REST writes silently no-op.
- [ ] Logged-out readback of the published URL to confirm title, description, and body render.
- [ ] Pagely page cache purge, then verify the public render while logged out. REST edits do not auto-purge.
- [ ] Re-run the link check in `internal-links.md`. Guard against `daveolson.ca` creeping back in.
- [ ] Known voice-checker false positive: "TEAM" flags as the banned word *team*. It is the civic party TEAM for a Livable Vancouver. Leave it.

## Third-party courtesy

- [ ] Give Bob Mackin a heads up before this goes live. The post quotes his questions, leans on his episode, and sends traffic to his paywall. A note costs nothing and he is a working journalist who covered Kris fairly.
- [x] Do not republish theBreaker's audio. The published post embeds their own Seriously Simple Podcasting stream URL, so the bytes come off their server and the play counts on their tracker. Nothing is rehosted.
- [x] Do not host a copy of the transcript publicly. `kriskrug-wp` is a **public** repo, so the transcripts are gitignored out of it; the canonical copies live in the private `kk-kb` repo.
- [ ] The post uses theBreaker's episode photo of Kris and Dave, credited to Bob Mackin with a link back. Ordinary editorial practice, but it was Claude's call. Confirm KK is happy with it, and take it down on request.

## Related, separate approval

The Publications page change (theBreaker as the new lead card) is a **different deploy** and needs its own KK sign-off. See the repo diff on `content/source-packs/keynotes-2026/`. Do not bundle the two.
