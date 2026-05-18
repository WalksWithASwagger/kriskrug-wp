# Polish Verification - 2026-05-18

Second-pass polish for `Speaking`, `Work`, and `About` after KK requested tighter information design, thumbnails, archive photos, video proof, and richer speaker authority.

## Rollback Evidence

Fresh page-level snapshots were captured before the live write:

- `backup/20260518-123159/page-snapshots/page-1208-about.json`
- `backup/20260518-123159/page-snapshots/page-1208-about.html`
- `backup/20260518-123159/page-snapshots/page-1887-speaking.json`
- `backup/20260518-123159/page-snapshots/page-1887-speaking.html`
- `backup/20260518-123159/page-snapshots/page-2672-work.json`
- `backup/20260518-123159/page-snapshots/page-2672-work.html`
- `backup/20260518-123159/page-snapshots/sha256sums.txt`

## Live Deploy

Authenticated WordPress REST deploy completed with slug checks before each update:

| Page | ID | Slug | Title | Status | Comments/pings |
| --- | ---: | --- | --- | --- | --- |
| Speaking | `1887` | `speaking` | `AI Keynote Speaker Kris Krüg` | `publish` | `closed/closed` |
| Work | `2672` | `recent-projects-include` | `Work` | `publish` | `closed/closed` |
| About | `1208` | `about` | `About Kris Krüg` | `publish` | `closed/closed` |

Authenticated readback confirmed all three pages have exposed Jetpack SEO meta, closed comments/pings, and no in-body `<h1>` in the raw payload.

## Public Checks

| URL | Result |
| --- | --- |
| `https://kriskrug.co/speaking/` | `200`; video, CBC, stage-energy, and booking markers present; no `Leave a Reply` |
| `https://kriskrug.co/recent-projects-include/` | `200`; thumbnails, archive highlights, current-work markers present; no `Leave a Reply` |
| `https://kriskrug.co/work/` | `200` after redirect to `https://kriskrug.co/recent-projects-include/` |
| `https://kriskrug.co/work/?utm_source=codex` | `200` after redirect to `https://kriskrug.co/recent-projects-include/` |
| `https://kriskrug.co/about/` | `200`; wild-index, photo-proof, publication/client-list markers present; no `Leave a Reply` |

External URL/media preflight checked 31 unique targets from the payloads; all returned `200`, including YouTube embeds, WP-hosted images, `bc-ai.ca`, `bothhandsfull.com`, `punkrockai.com`, and `developinganaimindset.com`.

## Privacy Scan

Publishable payload scan was clean for:

`visa`, `boarding`, `passport`, `hotel`, `phone`, `whatsapp`, `private emails`, `travel contacts`, `notion.s3`, `amazonaws`, `X-Amz`, `wpcomstaging`, `password`, `secret`, `token`, and the typo `developinganaimset`.

The broader source-pack scan found only public transcript vocabulary false positives such as `phone`, `token`, `passport` as a metaphor, and `secret sauce`; none appear in live page payloads as private logistics.

## Screenshots

Fresh Playwright screenshots were reviewed with an auto-scroll lazy-load pass. The durable evidence is kept as compact contact sheets:

- `content/source-packs/keynotes-2026/verification/screenshots-polish-20260518-123159-scrolled/contact-sheet-top.png`
- `content/source-packs/keynotes-2026/verification/screenshots-polish-20260518-123159-scrolled/contact-sheet-full.png`

Auto-scroll image verification reported `unloadedCount: 0` for all six desktop/mobile page captures. The large individual full-page captures were reviewed and discarded after generating the contact sheets to avoid adding oversized PNGs to the repo.

## Source Pack Additions

- Added `video-research/` with metadata, thumbnails, and public-caption transcript text for LaSalle, Bass Coast, ChannelNext, and Whistler Institute videos.
- Added `video-research/README.md` to make the transcript/video research reusable.
- Added `wp-draft-candidates-2026-05-18.md` with authenticated draft candidates for future speaking/AI authority posts.
