# theBreaker.news 460: AI as a Vancouver election issue

Track A packet built 2026-09-07 from theBreaker.news Podcast edition 460 (published 2026-08-09), in which Bob Mackin interviews Kris Krüg and Dave Olson outside the H.R. MacMillan Space Centre after the July 29 Vancouver AI Community Meetup.

## Files

- `post.md`: 2,300 word recap article with WordPress frontmatter. Markers: `>>>` pullquote, `![alt](media:ID)`, `![alt](stage:file|caption)`, `[[AUDIO:url]]`, `[[YOUTUBE:url]]`, `- ` list.
- `source-manifest.md`: nine sources, the ASR artifact table, the claim ledger, and three open flags for KK.
- Transcripts are **gitignored here**. `kriskrug-wp` is a public repo and the episode audio is theBreaker's, so a verbatim transcript does not belong in it. The canonical copies live in the private `kk-kb` repo (see Knowledge base below). Local working copies are `transcript-clean.txt`, `transcript-raw.txt` and `transcript-timestamped.vtt`.
- `seo-meta.md`: title, description, excerpt, schema note, and the Jetpack blocker.
- `internal-links.md`: every link with its HTTP status as of 2026-09-07.
- `image-brief.md`: featured image direction, and the two real-asset options that beat generating one.
- `social-content.md`: draft-only LinkedIn, X, and Bluesky copy.
- `publish-gate.md`: what has to be true before this is drafted in WordPress and before it publishes.

## Staging images (not committed)

`images/` is gitignored, matching `2026-06-28-context-creators`. All three are already in the WordPress media library and re-stageable:

- `thebreaker-460-episode-clip.jpg` — copy of `content/source-packs/keynotes-2026/assets/press-2026-08-09-thebreaker-460-context.jpg`, which **is** committed. WP media 12745.
- `vancouver-ai-meetup-31-cover.png` — from `kk-kb/content/media/meetups/2026-07-29-vancouver-ai-meetup-31/vancouver-ai-meetup-31-cover-recovered-luma-1254.png`. 3 MB, kept out of this repo. WP media 12746.
- `dave-olson-kris-krug-mackin-photo.jpg` — theBreaker's episode image, **their asset, used with credit**. WP media 12748.

## Knowledge base

The transcript is ingested canonically at:

- `kk-kb/content/media/interviews/2026-08-09-thebreaker-460-bob-mackin-transcript.md`
- `kk-kb/content/media/interviews/2026-08-09-thebreaker-460-bob-mackin-recap.md` (themes, quotable moments, entities, numbers, flags, reconciliation)

## Current state

**PUBLISHED** 2026-09-07 as post **12747**:
https://kriskrug.co/2026/09/07/ai-already-campaign-issue-vancouver/

Published and verified with `scripts/notion-to-wp/publish_breaker_460_recap.py`, 21 automated checks green. Carries the episode audio, the YouTube preview, four images, five pull quotes, and 23 article links across kriskrug.co and bc-ai.ca.

The article deliberately carries no meetup number, because the recording and every written record disagree. See flag 1 in `source-manifest.md`.

## The spine of the piece

Mackin asked whether AI would be an election issue. Kris said it would be the primary one, because council punted the data centre file past the campaign. **Two days after the episode published, The Tyee ran a seven-party AI scorecard.** The article uses that to show the prediction was tested and held, and then turns it into a self-criticism: Kris is not quoted in that coverage, and the anti-data-centre beat and the AI-ecosystem beat are still running as separate stories.

## Companion work in this same commit range

The media clipping was added to the Publications tear sheet: `content/source-packs/keynotes-2026/`. theBreaker is now the "Right now" lead card and sits on the "Heard on" podcast shelf. Repo-side only, and it needs its own separate approval before it deploys to page 1895.
