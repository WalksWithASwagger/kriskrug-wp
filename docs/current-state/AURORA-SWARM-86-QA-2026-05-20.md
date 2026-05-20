# Aurora Swarm #86 QA Gate - 2026-05-20

Track: B - Aurora v2 theme
Issue: [#86](https://github.com/WalksWithASwagger/kriskrug-wp/issues/86)
Branch: `codex/swarm-86-aurora-qa-2026-05-20`

## Scope

Run the post-Wave-3 Aurora QA gate after issues `#84` and `#85` merged.

No production WordPress writes, no Aurora production activation, no merge to `main`, and no Track A content edits.

## Small Fix Included

QA found mobile horizontal overflow on `/about/`. The source was legacy page-content images wrapped in links with fixed intrinsic widths.

Fix:

- `theme/kk-aurora/style.css`
  - set page/prose media to `height: auto`
  - constrained linked images with `a:has(> img)` inside page/prose content

## Local QA Setup

Local theme synced from this branch into:

`/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora`

Backup before sync:

`/tmp/kk-aurora-local-before-86-20260520.tgz`

Local WordPress `home` and `siteurl` were temporarily switched to:

`http://localhost:10003`

They were restored after QA.

## Screenshots

Captured at `1440x1000` and `390x844`:

- `docs/current-state/aurora-qa-2026-05-20/home-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/home-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/about-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/about-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/work-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/work-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/speaking-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/speaking-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/makeCulture-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/makeCulture-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/callingUsAllIn-desktop.png`
- `docs/current-state/aurora-qa-2026-05-20/callingUsAllIn-mobile.png`

Machine-readable results:

- `docs/current-state/aurora-qa-2026-05-20/aurora-qa-checks.json`

## Result Summary

| Surface | Desktop | Mobile | Overflow | Notes |
|---|---:|---:|---|---|
| Home | 200 | 200 | No | External hero/project media loaded in Local smoke. |
| About | 200 | 200 | Fixed | Local upload media missing; layout no longer overflows. |
| Work | 200 | 200 | No | One Local image unavailable. |
| Speaking | 200 | 200 | No | Main media loaded. |
| Make Culture | 200 | 200 | No | Local featured image unavailable. |
| Calling Us All In | 200 | 200 | No | Local post images unavailable. |

## Accessibility Checks

- Keyboard pass on the homepage reached skip link, brand, nav links, newsletter, and Book Kris CTA with visible `2px` outlines.
- Reduced-motion emulation matched `prefers-reduced-motion: reduce`.
- Reduced-motion hid the reading progress bar on a post.
- Major contrast pairs passed AA:
  - text on black: `19.09`
  - soft text on black: `12.45`
  - muted text on black: `6.82`
  - cyan on black: `13.34`
  - black on cyan: `12.54`
  - error on black: `12.15`
  - teal on black: `8.79`

## Console And Media Findings

Console errors were captured and are currently dominated by Local media `404` responses:

- About: `13` incomplete images.
- Work: `1` incomplete image.
- Make Culture: `1` incomplete image.
- Calling Us All In: `7` incomplete images.

This appears to be a Local dataset/media-library problem, not a newly introduced Aurora template error. It still blocks a true production-readiness sign-off because the final staging surface must prove real media availability.

## Verification

```bash
git diff --check
php -l theme/kk-aurora/functions.php
jq empty theme/kk-aurora/theme.json
jq empty docs/current-state/aurora-qa-2026-05-20/aurora-qa-checks.json
```

`make validate` remains blocked because `phpcs` is not installed in this environment.

## Gate Decision

Aurora is materially healthier after Wave 3, but production cutover remains blocked.

Remaining blockers:

- Run this same QA pass on a staging surface with production-like uploads/media available.
- Confirm backup and rollback gates before any production theme activation.
- Resolve or replace missing Local/staging media before human sign-off.
