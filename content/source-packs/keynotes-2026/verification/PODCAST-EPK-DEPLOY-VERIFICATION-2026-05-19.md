# Podcast EPK Deploy Verification - 2026-05-19

Live Track A update for `/podcast-guesting-page-epk/`, page ID `3609`.

## Rollback Evidence

Fresh page-level rollback snapshots were captured before the live write:

- `backup/20260519-105949/page-snapshots/page-3609-podcast-guesting-page-epk.json`
- `backup/20260519-105949/page-snapshots/page-3609-podcast-guesting-page-epk.html`
- `backup/20260519-105949/page-snapshots/sha256sums.txt`

The HTML snapshot was sanitized before staging to remove transient security keys, tracking signatures, and header contact details that are not needed for rollback.

Checksum verification passed:

```bash
cd backup/20260519-105949/page-snapshots
shasum -a 256 -c sha256sums.txt
```

## Payload

- `../wp-payloads/podcast-guesting-page-epk.html`
- `../wp-payloads/page-meta.json`

The live page keeps the existing slug and updates the title to `Podcast Guest, AI Commentator, Event Host`.

## Live REST Readback

Authenticated WordPress REST readback confirmed:

| Field | Result |
|---|---|
| ID | `3609` |
| Slug | `podcast-guesting-page-epk` |
| Status | `publish` |
| Title | `Podcast Guest, AI Commentator, Event Host` |
| Comments/pings | `closed/closed` |
| SEO title | `Podcast Guest, AI Commentator, Event Host \| Kris Krug` |
| SEO description | `Book Kris Krug for podcasts, interviews, broadcasts, panels, hosting, and emcee work on AI, creativity, community, media, ethics, and the future of work.` |

Public REST readback confirmed the expected content markers:

- `Bring me in when your audience needs AI to sound human`
- `CBC AI Sandbox`
- `Horizons: Exploring AI Models`
- `Producer notes`
- `Start a booking conversation`

## Public URL And Media Checks

`https://kriskrug.co/podcast-guesting-page-epk/` returned `200`.

The payload link/media check returned `200` for all live payload URLs, including:

- CBC AI Sandbox owned post
- Horizons by Compass Datacenters
- IndigiGenius / CBC
- Human Biography Podcast
- E-ChannelNews
- Rachel Thexton Connects
- Kurty D Show
- Teen2Life Experience via Amazon Music
- Vancouver AI Pods
- Both Hands Full
- Punk Rock AI
- selected WP-hosted image assets
- YouTube embed `T5ANAthZewE`

The older Podtail Teen2Life URL remains in source-pack history only as a fallback because curl sees `403`; the live page uses the crawler-friendlier Amazon Music listing.

## Browser Evidence

Playwright screenshots were captured with Chromium after the live update:

- `screenshots-podcast-epk-20260519-105949/podcast-epk-desktop.png`
- `screenshots-podcast-epk-20260519-105949/podcast-epk-mobile.png`

The first screenshot pass exposed a Catch Responsive list-style collision on the proof-strip badges. The payload CSS was patched and re-applied; the final screenshots show the proof items as badges on desktop and mobile.

## Privacy And Safety Checks

Passed:

```bash
jq '.' content/source-packs/keynotes-2026/wp-payloads/page-meta.json >/dev/null
git diff --check -- content/source-packs/keynotes-2026/wp-payloads/podcast-guesting-page-epk.html content/source-packs/keynotes-2026/wp-payloads/page-meta.json content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting backup/20260519-105949/page-snapshots
rg -n -i "<standard source-pack sensitive-string pattern>" content/source-packs/keynotes-2026/wp-payloads/podcast-guesting-page-epk.html content/source-packs/keynotes-2026/wp-payloads/page-meta.json content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting backup/20260519-105949/page-snapshots
rg -n "chat\\.openai\\.com|Leave a Reply|Notion S3|podtail\\.se|channelnext-chaos-creativity" content/source-packs/keynotes-2026/wp-payloads/podcast-guesting-page-epk.html content/source-packs/keynotes-2026/media-appearances content/drafts/2026-05-19-ai-media-appearances-podcast-guesting
```

No private Notion material, personal contact details, travel data, placeholder ChatGPT links, Notion S3 URLs, or stale Podtail live link remain in the live payload.
