# Performance Recovery Closeout - 2026-07-01

**Lane:** Track B theme performance with Track A media evidence
**Live writes:** none
**Theme package:** `/Users/kk/Desktop/kk-aurora-performance-1.3.25-20260701.zip`
**Baseline report:** `docs/current-state/reports/performance-audit-20260701-153109Z.md`

## What Changed

- Added `scripts/performance_audit.py`, a repeatable read-only performance baseline tool.
- Added `make performance-audit` for the standard route and asset matrix.
- Updated `theme/kk-aurora/templates/front-page.html` so the homepage Vancouver AI card no longer loads the 1.8 MB source PNG by default.
- Added explicit dimensions to the homepage hero/card images inspected in the baseline.
- Bumped `kk-aurora` from `1.3.24` to `1.3.25` in `style.css` and `functions.php`.

## Baseline Findings

The first run was written to `docs/current-state/reports/performance-audit-20260701-153109Z.md`.

| Surface | Finding |
|---|---|
| `/` cold load | p50 TTFB `3.982s`, p50 total `4.085s` |
| `/` warm load | p50 TTFB `0.321s`, p50 total `0.516s` |
| `/about/` cold load | p50 TTFB `3.853s`, p50 total `4.081s` |
| `/work/` cold load | p50 TTFB `4.181s`, p50 total `4.363s` |
| Cache layer | Warm homepage hits expose `x-jetpack-boost-cache=hit` and `x-gateway-cache-status=HIT` |
| Largest homepage image | `june-meetup-30-full-lineup-hero-1024x1024.png`, `1,795,047` bytes, no width/height in live HTML |
| Blocking candidates | Google tag, Jetpack Boost generated JS, and WordPress.com stats are present on homepage and latest post |

The main diagnosis is unchanged: warm cache is acceptable; cold cache / cache-bypass paths are the biggest search-viability risk. The lowest-risk media win is now live through the custom Site Editor front-page template and also packaged in Aurora `1.3.25` for source parity.

## Package Verification

```bash
php -l theme/kk-aurora/functions.php
unzip -t /Users/kk/Desktop/kk-aurora-performance-1.3.25-20260701.zip
```

Both checks passed on 2026-07-01.

## Deploy Checklist

1. Optional source-parity deploy: upload `/Users/kk/Desktop/kk-aurora-performance-1.3.25-20260701.zip` in wp-admin using the theme replace flow once browser file upload access is available.
2. Purge Pagely / PressCACHE and Jetpack Boost cache if a theme package deploy follows.
3. Regenerate Jetpack Boost Critical CSS during the Track B pass.
4. If the theme package is uploaded, confirm live `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=<timestamp>` reports `Version: 1.3.25`.
5. Re-run `make performance-audit OUTPUT=docs/current-state/reports/performance-audit-<timestamp>.md` after any theme/cache/critical-CSS work.
6. Compare Matrix A route timings and Matrix B image requests against the 2026-07-01 baseline and post-REST-deploy report.

## Issue Gates

Issue #125 should not close until:

- Jetpack Boost Critical CSS is regenerated after `1.3.25` is live.
- A fresh performance audit report is attached or linked.
- Homepage latest Matrix B no longer shows the Vancouver AI PNG at ~1.8 MB.
- Lighthouse or PageSpeed records LCP, INP, CLS, and TBT for homepage and `/blog/`.
- Any remaining blocking script decision is documented as keep, defer, or remove.

Issue #86 should not close until:

- Real staging or production-like QA captures the route matrix from the performance audit.
- Desktop/mobile screenshots include homepage, About, Work or Speaking, and at least two posts.
- Keyboard, reduced-motion, contrast, overflow, console, media loading, LCP, INP, and CLS notes are recorded.
- Rollback and post-cutover verification are ready before any broader Aurora deploy.

## Live REST deployment pass - 2026-07-01 15:56Z

- Live write path used: WordPress REST `templates/kk-aurora//front-page` content-only update.
- Reason: the live homepage is a custom Site Editor template, so a theme zip upload alone would not reliably update the rendered homepage.
- Rollback snapshot before write: `docs/current-state/reports/front-page-template-before-rest-update-20260701-155623Z.json` and `docs/current-state/reports/front-page-template-before-rest-update-20260701-155623Z.html`.
- Post-write snapshot: `docs/current-state/reports/front-page-template-after-rest-update-20260701-155623Z.json` and `docs/current-state/reports/front-page-template-after-rest-update-20260701-155623Z.html`.
- Public readback evidence: `docs/current-state/reports/front-page-public-readback-20260701-155643Z.json`.
- Post-deploy audit: `docs/current-state/reports/performance-audit-20260701-post-rest-deploy.md`.
- Result: canonical homepage and cache-busted homepage both render the resized Vancouver AI image URL, no longer render the direct heavy PNG `src`, and include explicit hero/card dimensions.
- Remaining performance focus: cold TTFB and render-path/plugin work remain Track B/staging candidates; image payload quick win is live.

## Live theme package deployment - 2026-07-01

- Uploaded `/Users/kk/Desktop/kk-aurora-performance-1.3.25-20260701.zip` through wp-admin after enabling local file upload access.
- WordPress confirmation showed current `KK Aurora` version `1.3.24` and uploaded version `1.3.25`, then completed `Replace installed with uploaded` successfully.
- Live theme verification: `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=<timestamp>` reported `Version: 1.3.25`.
- Homepage verification after theme upload: optimized Vancouver AI image remained present, direct heavy PNG `src` remained absent, and explicit hero/card dimensions remained present.
- PressCACHE purge after theme upload returned `Cache Purge: Success`.
- Jetpack Boost Critical CSS regeneration was started after the theme upload, but the UI remained at `Generating Critical CSS. Please do not leave this page until completed.` after repeated polling and refresh.
- Post-theme public audit: `docs/current-state/reports/performance-audit-20260701-post-theme-live.md`.
- Follow-up refresh audit: `docs/current-state/reports/performance-audit-20260701-refresh.md`.

Post-theme audit highlights:

| Route | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Redirects |
|---|---:|---:|---:|---:|---:|
| `/` | `3.675s` | `3.762s` | `0.425s` | `0.528s` | `0` |
| `/about/` | `4.355s` | `4.450s` | `0.427s` | `0.515s` | `0` |
| `/blog/` | `0.863s` | `1.047s` | `0.432s` | `0.606s` | `0` |
| `/projects/` | `1.165s` | `1.301s` | `0.717s` | `0.868s` | `1` |
| `/work/` | `4.966s` | `5.135s` | `0.777s` | `0.868s` | `1` |

Remaining blockers:

- Jetpack Boost Critical CSS needs a completed post-theme generation timestamp before issue #125 can close.
- Cold-cache TTFB remains the biggest search-viability risk, especially `/`, `/about/`, and `/work/`.
- `/projects/` and `/work/` still redirect to `/recent-projects-include/`; decide whether those should become direct canonical routes or whether internal/sitemap references should normalize to the final URL.
