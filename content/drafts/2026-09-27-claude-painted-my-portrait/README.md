# I Made Claude Paint My Portrait in MS Paint. No Scripts.

**PUBLISHED 2026-09-27.** Post 12870.

- Live: https://kriskrug.co/2026/09/27/claude-painted-my-portrait-ms-paint/
- Edit: https://kriskrug.co/wp-admin/post.php?post=12870&action=edit
- Slug: `claude-painted-my-portrait-ms-paint`
- Categories: 1665 `ai-creatives`, 1755 `creative-technology-making` (IDs pinned, see below)

## What this is

A process dispatch about handing Claude a profile photo, pointing it at
[JSPaint](https://jspaint.app), and banning the javascript tool so it had to
paint with brush drags and clicks instead of scripting the canvas. Four
sessions. The post is about the failure modes and about losing the undo history.

## Provenance

Everything here is KK's own: the source photo is his profile picture, the
painting was made under his direction in this repo's own working sessions, and
the hero is derived from that painting. Nothing generated, nothing licensed in.
JSPaint is credited to [Isaiah Odhner](https://isaiahodhner.io) in the body.

Originals live on KK's Desktop (`kk-portrait-timelapse.mp4`,
`kk-portrait-final.png`, `jspaint-portrait-timelapse-FULL-600px.gif`). The raw
834-frame history export is the source for the "before" still, frame 833.

## Media (already in the WP library, so `images/` and `img/` are gitignored)

| id | file | notes |
|----|------|-------|
| 12867 | `jspaint-portrait-timelapse.mp4` | 600x600, 41s, self-hosted, `accept-ranges: bytes` |
| 12868 | `jspaint-portrait-final.png` | 600x600, also the video poster |
| 12869 | `jspaint-portrait-before-last-rounds.png` | where the recorded history stops |
| 12871 | `hero-c2-wash.png` | 1600x900 featured image |

## The hero

The painting is a 600x600 square and cannot be a featured image on its own.
`make-hero.py` mats it onto a 1600x900 ground at 780px, leaving 60px of vertical
margin. That margin is load-bearing: the 1.91:1 OG crop eats 31px top and bottom,
and the first attempt (square at the full 900 height) cut the crown off the
beanie. Caught in the crop pass, not in review.

featured-image-forge mechanical gates passed on every candidate. All four crop
previews were looked at, including `thumb-300` at native size. Rejected:
`hero-b-edgestretch` (stretching the art's edge columns produced hard horizontal
banding that reads as a render glitch). Runner-up kept: `hero-a2-blurfill`.

Regenerate with `python3 make-hero.py` from this folder. Reproduces byte-for-byte.

## Publish record

KK approved and published 2026-09-27. `hero-c2-wash` shipped;
`hero-a2-blurfill` remains the alternate.

Post-publish readback, logged out:

- `200` on the permalink, `x-gateway-cache-status: MISS` then `HIT` on the
  second request, so no stale-cache purge was needed.
- `og:image` = `hero-c2-wash.png` via Photon at `fit=1024,576`, landscape,
  resolves `200 image/png`. `twitter:card` = `summary_large_image`.
- `<video>` present with its poster, gallery images present, no em dash in the
  rendered article.
- Rendered page checked in a browser: hero, pullquotes, video with controls at
  0:00/0:40, and the two-up before/after all render as intended.

Still worth a human pass: the closing take in "What I take from this" is the
draft's opinion written in KK's voice, not a quote from him.

## Verified 2026-09-27

Both voice gates clean (`make voice-check`, 0 violations; `kk-voice/voicecheck.py`,
0 flags). All 20 post-write assertions in the publish script pass, covering
no em dashes, the umlaut in Kris Krüg, both cross-links, JSPaint attribution,
lightbox on both gallery images, pinned category IDs, and the Jetpack SEO meta.

Category IDs are pinned rather than resolved by name on purpose. REST returns
"Creative Technology &amp; Making" HTML-encoded, so `ensure_term`'s name branch
misses it and only the slug branch prevents a duplicate category being created
on production.
