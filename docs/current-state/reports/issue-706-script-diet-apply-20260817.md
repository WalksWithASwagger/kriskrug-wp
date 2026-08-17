# #706 script diet apply receipt — 2026-08-17

**Status:** live at origin on the main routes. PSI mobile rerun captured 2026-08-16 11:59 PDT (`qx4j9jir1j`).
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

## Browser Network (Playwright, Chrome for Testing, 390×844, 2026-08-17 05:49 UTC)

Logged-out `https://kriskrug.co/?cb=…`. `#kk-gtag-delayed` 1, `#google_gtagjs-js` 0.

| Path | Facebook / fbevents | gtag |
|---|---|---|
| Load + 2.5 s, no input | **0** requests | **0** requests |
| Then a click | 0 | **1** `gtag/js?id=G-X7JE8B32L7` |
| Separate idle run, no input | **0** | first `gtag/js` at **2874 ms** after Playwright `load` (3 s timer is from the document `load` event, which fires slightly before Playwright's callback) |

Pixel ID `1720755522050230` did not appear in the network log.

## PSI mobile (2026-08-16 11:59 PDT)

Report: [`psi-mobile-2026-08-16.md`](psi-mobile-2026-08-16.md) / [qx4j9jir1j](https://pagespeed.web.dev/analysis/https-kriskrug-co/qx4j9jir1j?form_factor=mobile).

| #706 claim | Result |
|---|---|
| TBT should move | **160 ms → 10 ms** |
| Facebook long tasks gone | **gone** |
| gtag out of the PSI trace | **not gone** (176.9 KiB / 72.4 KiB unused; 1 long task). Matches the delay-from-`load` caveat. Network check still passes. |
| LCP / CLS should not move | **they moved** (7.6 s → 3.9 s, 0.43 → 0). Do not credit the diet; 1.6.8 homepage landed the same evening. |

Do not GitHub-close #706 until KK accepts the gtag-in-trace caveat.

## Still owed

1. #731 Jetpack Boost critical-CSS regen in wp-admin. Prep: `reports/issue-731-boost-critical-css-blocked-20260817.md`. Local/free module confirmed 2026-08-17; cloud regen is a no-op here.
