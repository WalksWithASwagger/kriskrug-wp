# IA Polish Continuation Verification - 2026-05-18

Continuation pass after the Horizons speaking proof update. Scope stayed in Track A: WordPress page payloads only, no theme edits, no slug migration, no new plugins.

## What Changed

- `Work` got a clearer top-level structure:
  - hero copy tightened to frame the page as a portfolio, not a loose project list
  - quick-jump cards added for `Featured work`, `Public artifacts`, `Archive highlights`, and contact
  - `Current focus` became `Featured work`
  - BC+AI, AI Keynotes, and The Upgrade AI are now visually prioritized above the portal grid
  - the text-only `Selected bodies of work` callouts became thumbnail-led cards under `How the work shows up`
  - archive section received a stable `archive-highlights` anchor
- `About` got stronger SEO/interlinking structure:
  - added `Find the right thread` pathway cards to Work, Speaking, Services, Publications, Testimonials, and Podcast EPK
  - added a publication-page link inside the open publication proof list
  - added explanatory copy below the proof lists so the giant lists have a reason to exist
  - fixed the collapsed proof-list details so closed panels do not stretch to the height of the open publication list
- `Speaking` got a stronger booking-lanes section:
  - Keynotes
  - Workshops and custom trainings
  - Podcast and video guesting
  - Hosting, emcee, and moderation

## Rollback Evidence

Fresh page snapshots were captured before the three-page live write:

- `backup/20260518-223014/page-snapshots/page-1208-about.json`
- `backup/20260518-223014/page-snapshots/page-1208-about.html`
- `backup/20260518-223014/page-snapshots/page-1887-speaking.json`
- `backup/20260518-223014/page-snapshots/page-1887-speaking.html`
- `backup/20260518-223014/page-snapshots/page-2672-work.json`
- `backup/20260518-223014/page-snapshots/page-2672-work.html`
- `backup/20260518-223014/page-snapshots/sha256sums.txt`

Checksums were verified successfully.

After the About proof-list layout fix, a second About-only rollback snapshot was captured and verified:

- `backup/20260518-224340/page-snapshots/page-1208-about.json`
- `backup/20260518-224340/page-snapshots/page-1208-about.html`
- `backup/20260518-224340/page-snapshots/sha256sums.txt`

## Local Preflight

- `git diff --check` passed.
- Publishable payload privacy scan returned no matches for:
  - `visa`
  - `boarding`
  - `passport`
  - `hotel`
  - `phone`
  - `whatsapp`
  - private email pattern
  - `notion.s3`
  - `amazonaws`
  - `X-Amz`
  - `wpcomstaging`
  - `password`
  - `secret`
  - `token`
- HTML payload parser counts after edits:
  - `about.html`: `h1=0`, `h2=9`, `img=13`, `links=20`
  - `work.html`: `h1=0`, `h2=6`, `img=17`, `links=20`
  - `speaking.html`: `h1=0`, `h2=12`, `img=15`, `iframe=6`, `links=27`
- Payload URL/media preflight checked 46 unique targets; all returned `200`.

## Live Deploy

Authenticated WordPress REST updates completed with ID/slug checks before each write:

| Page | ID | Slug | Status | Comments/pings |
| --- | ---: | --- | --- | --- |
| Speaking | `1887` | `speaking` | `publish` | `closed/closed` |
| Work | `2672` | `recent-projects-include` | `publish` | `closed/closed` |
| About | `1208` | `about` | `publish` | `closed/closed` |

After the About proof-list layout fix, page `1208` was updated again with a fresh About-only rollback snapshot first.

## Authenticated Readback

Authenticated REST readback confirmed:

- `raw_matches_local: true` for all three pages after the three-page deploy.
- `raw_matches_local: true` for About after the follow-up proof-list fix.
- Slugs unchanged.
- Titles unchanged.
- comments/pings remained closed.
- Jetpack SEO meta remained populated.

## Public Checks

Public checks confirmed:

- `https://kriskrug.co/speaking/` returned `200` and contained:
  - `Keynotes`
  - `Workshops and custom trainings`
  - `Podcast and video guesting`
  - `Hosting, emcee, and moderation`
  - no `Leave a Reply`
- `https://kriskrug.co/recent-projects-include/` returned `200` and contained:
  - `Featured work`
  - `Public artifacts`
  - `How the work shows up`
  - `Archive highlights`
  - no `Leave a Reply`
- `https://kriskrug.co/work/` returned `301` to `/recent-projects-include/`, then `200`.
- `https://kriskrug.co/about/` returned `200` and contained:
  - `Find the right thread`
  - `legacy proof archive`
  - `The wild index`
  - no `Leave a Reply`

## Browser QA

Playwright desktop/mobile checks covered:

- `/speaking/`
- `/recent-projects-include/`
- `/work/`
- `/about/`

Results:

- all target pages returned `200`
- `/work/` ended at `/recent-projects-include/`
- one rendered H1 per page
- `unloadedCount: 0` for images after lazy-load scroll
- no `Leave a Reply`
- expected IA markers present
- no tiny/zero-size `.kk-card`, `.kk-lane`, `.kk-mini-nav a`, or `.kk-pathways a` boxes

Screenshot evidence:

- `content/source-packs/keynotes-2026/verification/screenshots-ia-polish-20260518-223014/contact-sheet-top.png`
- `content/source-packs/keynotes-2026/verification/screenshots-ia-polish-20260518-223014/contact-sheet-sections.png`
- `content/source-packs/keynotes-2026/verification/screenshots-ia-polish-20260518-223014/results.json`

The About wild-index follow-up check reported `detailsHeights: [585, 70, 70]`, confirming the closed proof panels no longer stretch to match the open publication panel.
