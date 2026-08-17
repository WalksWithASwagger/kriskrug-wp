# Aurora Homepage BC + AI / Futureproof Closeout - 2026-07-03

## Scope

Updated the front page so Kris's current work is centered on two equal pillars:

- BC + AI as the year-round, member-supported, province-wide responsible AI ecosystem.
- Futureproof Festival as the October 28-30 flagship public gathering where that ecosystem becomes visible.

The tracked source of truth is `theme/kk-aurora/templates/front-page.html`. The live WordPress Site Editor template `kk-aurora//front-page` was also updated by REST after each snapshot.

## What changed

- Hero proof row now names:
  - `Executive Director, BC + AI`
  - `Founder / Lead Curator, Futureproof Festival`
- Hero copy now frames the work as the trust layer and public room for responsible AI in British Columbia.
- Replaced the mixed "Living projects" grid with a two-pillar band:
  - `BC + AI Ecosystem`
  - `Futureproof Festival`
- Added primary links to:
  - `https://bc-ai.ca/`
  - `https://bc-ai.ca/membership/`
  - `https://www.futureproof.website/`
  - `https://www.futureproof.website/program/`
- Moved Vancouver AI, Punk Rock AI, Both Hands Full, and The Upgrade AI into a lower `Related creative lab` band.
- Removed stale `2,000+ members` copy.
- Added homepage-scoped mobile CSS so the longer role labels, hero copy, and two-pillar section do not overflow at narrow widths.
- Polished the hero headline to `Authored judgment for generative everything.` with mobile-only line spans for cleaner wrapping.

## Live update evidence

Rollback/original pre-change live template:

- `docs/current-state/reports/front-page-template-before-feature-pillars-20260703-161729Z.html`
- `docs/current-state/reports/front-page-template-before-feature-pillars-20260703-161729Z.json`

Final pre-polish snapshot:

- `docs/current-state/reports/front-page-template-before-mobile-line-polish-20260703-165403Z.html`
- `docs/current-state/reports/front-page-template-before-mobile-line-polish-20260703-165403Z.json`

Final live template readback:

- `docs/current-state/reports/front-page-template-after-mobile-line-polish-20260703-165403Z.html`
- `docs/current-state/reports/front-page-template-after-mobile-line-polish-20260703-165403Z.json`

Public marker readback:

- `docs/current-state/reports/front-page-public-readback-final-polish-20260703-165618Z.json`

Final visual evidence:

- `docs/current-state/reports/front-page-feature-pillars-final-polish-desktop-20260703-165421Z.png`
- `docs/current-state/reports/front-page-feature-pillars-final-polish-mobile-20260703-165421Z.png`

## Verification

Commands run:

```bash
git diff --check -- theme/kk-aurora/templates/front-page.html
/opt/homebrew/opt/python@3.14/bin/python3.14 scripts/wp7-public-smoke.py --base-url https://kriskrug.co --expect-version 6.9.4 --timeout 20 --json
```

Results:

- Public readback confirmed the polished headline, BC + AI role, Futureproof role, both feature headings, related creative lab, membership link, Futureproof program link, and no `2,000+ members` string.
- Desktop and mobile screenshots confirmed the two pillars are visible immediately after the hero and the mobile hero no longer clips its main text.
- WP smoke had zero failures. Existing OG/Twitter metadata warnings remain on `/`, `/speaking/`, and `/work/`; this was pre-existing and outside this homepage hierarchy change.
- Direct command-line checks against `bc-ai.ca` returned Vercel bot-challenge `403`; the hrefs are correct and browser/web access resolved the public BC + AI pages.

## Remaining notes

- The live front-page template is a Site Editor override, so future source changes to `theme/kk-aurora/templates/front-page.html` still need an explicit REST sync or theme/template deployment path.
- Keep the rollback snapshot above until the next homepage template change has its own fresh snapshot.
