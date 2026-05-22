# Appearances Roundup Draft Verification - 2026-05-19

Scope: local Track A draft polish only. No live WordPress writes, no new public post, no page-payload changes, and no theme edits.

## What Changed

Polished the standalone support-post package:

- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.html`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/seo-meta.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/internal-links.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/alt-text.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/publish-gate.md`

Updated source-pack routing and status:

- `../media-appearances/README.md`
- `../media-appearances/public-source-inventory-2026-05-19.md`
- `../post-packages/cbc-ai-sandbox-and-appearance-queue.md`

## Editorial Status

- `/podcast-guesting-page-epk/` remains the primary producer-facing booking surface.
- The standalone roundup is positioned as a supporting authority/archive post.
- The draft now includes the user-requested Vancouver AI Meetup March 2026 video: `https://www.youtube.com/watch?v=T5ANAthZewE`.
- Publishing remains gated behind KK review, featured-image decision, and fresh live WordPress target checks.

## Link Check Results

Command:

```bash
rg -o 'https?://[^" )]+' content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.html | sort -u | while read url; do code=$(curl -L -sS -o /dev/null -w '%{http_code}' --max-time 20 "$url" || true); printf '%s %s\n' "$code" "$url"; done
```

Results:

| Status | URL |
| --- | --- |
| 200 | `https://bc-ai.ca/` |
| 200 | `https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/` |
| 200 | `https://kriskrug.co/2024/07/03/new-segment-on-cbc-radio-early-edition-ai-sandbox-with-kris-krug/` |
| 200 | `https://kriskrug.co/about/` |
| 200 | `https://kriskrug.co/contact/` |
| 200 | `https://kriskrug.co/motleykrug-podcast/` |
| 200 | `https://kriskrug.co/podcast-guesting-page-epk/` |
| 200 | `https://kriskrug.co/recent-projects-include/` |
| 200 | `https://kriskrug.co/speaking/` |
| 200 | `https://music.amazon.com/es-ar/podcasts/efb24614-5724-4412-a377-755e3b3ebdd4/episodes/cd1d024c-e3d4-496f-ace3-2901c89c3882/rachel-thexton-connects-03x08-kris-kr%C3%BCg-one-of-canada%27s-leading-ai-voices-talks-tech-and-tells-his-story` |
| 200 | `https://music.amazon.com/es-us/podcasts/ba75295d-60de-4701-8eb6-12e17e49838a/teen2life-experience` |
| 200 | `https://music.amazon.com/podcasts/369594c8-9548-47ed-9dee-b61dae6c7c5a/vancouver-ai-pods` |
| 200 | `https://podcasts.apple.com/us/podcast/053-widen-the-lens-with-kris-krug/id1575595225?i=1000634160006` |
| 200 | `https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/` |
| 200 | `https://www.iheart.com/podcast/338-the-human-biography-podcas-108140410/episode/kris-krug-live-with-curiosity-256487014/` |
| 200 | `https://www.indigigenius.org/media-appearances/michaelandkrisinterview` |
| 200 | `https://www.youtube.com/watch?v=T5ANAthZewE` |

## Privacy Scan

Command:

```bash
rg -n -i 'visa|boarding|passport|hotel|whatsapp|phone|tel:|mailto:|@[A-Za-z0-9._%+-]+\.[A-Za-z]{2,}|778|898|3076|secret_|api[_-]?key|password|nonce|token|sig=' content/drafts/2026-05-19-ai-media-appearances-podcast-guesting content/source-packs/keynotes-2026/media-appearances || true
```

Result: no matches.

## Remaining Gate

Before any live WordPress write:

- confirm KK wants the standalone roundup published,
- choose a WP-hosted featured image or embed-only treatment,
- snapshot/check the target slug before creating or updating anything live,
- avoid third-party podcast art, CBC art, Horizons art, or YouTube thumbnail imports unless rights are confirmed,
- add backlinks from `/speaking/`, `/about/`, and `/podcast-guesting-page-epk/` only after the post URL exists.

Follow-up note: a WP draft publisher pass on 2026-05-19 stopped before the live write because a fresh full-site backup was unavailable. The strict backup gate was retired on 2026-05-22, and private WP draft `11879` was created at <https://kriskrug.co/wp-admin/post.php?post=11879&action=edit>. See `APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md` for the older stopped attempt.
