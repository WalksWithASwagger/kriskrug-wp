# Media Appearance Source Verification - 2026-05-19

Scope: local source-pack and draft prep only. No live WordPress writes, no page payload changes, no theme edits.

## What Changed

Created a media appearance source pack:

- `../media-appearances/README.md`
- `../media-appearances/public-source-inventory-2026-05-19.md`
- `../media-appearances/podcast-epk-refresh-package.md`

Created a local draft candidate:

- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.html`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/seo-meta.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/internal-links.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/alt-text.md`
- `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/publish-gate.md`

## Source Links Checked

| Status | URL |
| --- | --- |
| 200 | `https://kriskrug.co/2024/07/03/new-segment-on-cbc-radio-early-edition-ai-sandbox-with-kris-krug/` |
| 200 | `https://www.indigigenius.org/media-appearances/michaelandkrisinterview` |
| 200 | `https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/` |
| 200 | `https://www.iheart.com/podcast/338-the-human-biography-podcas-108140410/episode/kris-krug-live-with-curiosity-256487014/` |
| 200 | `https://music.amazon.com/es-ar/podcasts/efb24614-5724-4412-a377-755e3b3ebdd4/episodes/cd1d024c-e3d4-496f-ace3-2901c89c3882/rachel-thexton-connects-03x08-kris-kr%C3%BCg-one-of-canada%27s-leading-ai-voices-talks-tech-and-tells-his-story` |
| 200 | `https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/` |
| 200 | `https://podcasts.apple.com/us/podcast/053-widen-the-lens-with-kris-krug/id1575595225?i=1000634160006` |
| 403 by curl, browser/search fetch succeeded | `https://podtail.se/podcast/teen2life-experience/047-ceo-of-future-proof-creatives-artist-kris-krug/` |
| 200 | `https://kriskrug.co/podcast-guesting-page-epk/` |
| 200 | `https://kriskrug.co/speaking/` |

## Verification Commands

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
git diff --check -- content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting content/source-packs/keynotes-2026/post-packages/cbc-ai-sandbox-and-appearance-queue.md content/source-packs/keynotes-2026/README.md docs/current-state/NEXT-ROUND-WORK-2026-05-19.md
LC_ALL=C rg -n "[^\\x00-\\x7F]" content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting content/source-packs/keynotes-2026/post-packages/cbc-ai-sandbox-and-appearance-queue.md
rg -n -i "<standard source-pack sensitive-string pattern>" content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting
```

## Publish Gate

Follow-up completed: `/podcast-guesting-page-epk/` was refreshed and verified on 2026-05-19; see `PODCAST-EPK-DEPLOY-VERIFICATION-2026-05-19.md`.

Follow-up completed: the standalone local appearances roundup was polished and re-verified on 2026-05-19; see `APPEARANCES-ROUNDUP-DRAFT-VERIFICATION-2026-05-19.md`.

Before any live write:

- snapshot the current Podcast EPK page,
- confirm target page ID and slug,
- choose a WP-hosted headshot, interview still, or embed-only treatment,
- confirm final source list and ordering with KK,
- avoid third-party transcript dumps and third-party art unless rights are clear,
- verify `/speaking/` still links cleanly to the EPK after update.
