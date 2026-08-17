# #706 script diet apply receipt — 2026-08-17

**Status:** live at origin on the main routes. PSI mobile rerun still owed (wait ≥30 min after purge).
**Track:** Track A snippet/plugin surfaces. Not a theme deploy.
**KK ruling (2026-08-10):** drop Facebook pixel `1720755522050230`; delay gtag to first interaction or 3 s idle.

## What is live

| Half | Surface | Live state |
|---|---|---|
| Pixel | WPCode Lite CPT **7917** (`META PIXEL`, `site_wide_header`) | Drafted. Public HTML no longer emits `fbevents` / `fbq(` / `1720755522050230`. IHAF export still contains the body for rollback. Do not delete until after soak. |
| Gtag delay | Code Snippets **id 22** `KK Script Diet`, front-end | Active. `code` sha256 prefix `946e108e63485aed` matches `fixes/issue-706-script-diet-snippet.php` with the opening `<?php` stripped. `code_error` null. Other snippet active flags unchanged vs the pre-apply snapshot. |

Canonical HTML 2026-08-17 05:30 UTC (no query string):

| Route | `kk-gtag-delayed` | `google_gtagjs-js` | pixel id |
|---|---:|---:|---:|
| `/` | 1 | 0 | 0 |
| `/about/` | 1 | 0 | 0 |
| `/blog/` | 1 | 0 | 0 |
| `/speaking/` | 1 | 0 | 0 |
| `/work/` | 1 | 0 | 0 |
| `/photography/` | 1 | 0 | 0 |
| `/contact/` | 1 | 0 | 0 |
| `/generative-ai-services/` | 1 | 0 | 0 |

`G-X7JE8B32L7` remains inside the delayed loader. Site Kit settings were not touched. Google site-verification WPCode snippet **5820** was not touched.

## Snapshots (outside the repo, mode 0600)

`~/kk-snapshots/code-snippets-before-706-*.json`
`~/kk-snapshots/wpcode-ihaf-before-706-*.json`
`~/kk-snapshots/706-home-before-*.html` / `706-about-before-*.html`
Page edit snapshots `~/kk-snapshots/page-*-before-706-purge-*.json` for the no-op title-saves used to bust PressCACHE (3930, 1208, 1887, 12013, 2418, 2672). Titles and slugs were unchanged.

## Rollback

- Gtag: `POST /wp-json/code-snippets/v1/snippets/22/deactivate` (or toggle `KK Script Diet` inactive).
- Pixel: reactivate WPCode 7917. Do not invent a Code Snippets pixel id.
- Then cache-bust. PressCACHE/Atomic if the canonical URL stays stale.

## Still owed

1. Browser/GA4 checks from the runbook (Network: no `googletagmanager` during load; click then `gtag/js?id=G-X7JE8B32L7`; idle path after 3 s).
2. PSI mobile vs `docs/current-state/reports/psi-mobile-2026-08-10.md`. TBT / third-party should move. LCP and CLS should not. Do not close #706 on HTML greps alone.
3. #731 Jetpack Boost critical-CSS regen in wp-admin.
