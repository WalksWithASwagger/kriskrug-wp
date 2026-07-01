# Performance Recovery Closeout - 2026-07-01

**Lane:** Track B theme performance with Track A media evidence
**Live writes:** theme package replacements through wp-admin; homepage template REST update
**Theme packages:** `/Users/kk/Desktop/kk-aurora-performance-1.3.25-20260701.zip`, `/Users/kk/Desktop/kk-aurora-readability-1.3.26-20260701.zip`, `/Users/kk/Desktop/kk-aurora-readability-1.3.27-20260701.zip`
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
- Deep diagnostic audit with URL hygiene/script matrices: `docs/current-state/reports/performance-audit-20260701-deep-diagnostic.md`.

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

## Live readability reset deployment - 2026-07-01

- Built and verified `/Users/kk/Desktop/kk-aurora-readability-1.3.26-20260701.zip` from branch `codex/aurora-readability-reset`.
- WordPress theme replace confirmed installed `KK Aurora` version `1.3.25` and uploaded version `1.3.26`; replacement completed successfully.
- Live CSS verification after `1.3.26`: `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=<timestamp>` reported `Version: 1.3.26` and contained `--aurora-readable-measure`.
- PressCACHE purge after `1.3.26` returned `Cache Purge: Success`.
- Initial live readability audit found real misses at the tablet/mobile boundary: standard page H1s at `768px`, one-off kicker text below the body floor, mobile brand tap height below `44px`, and featured archive card media overflow at `768px`.
- Built corrective package `/Users/kk/Desktop/kk-aurora-readability-1.3.27-20260701.zip` with the targeted fixes and verified the zip contents.
- WordPress theme replace confirmed installed `KK Aurora` version `1.3.26` and uploaded version `1.3.27`; replacement completed successfully.
- Live CSS verification after `1.3.27`: `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=<timestamp>` reported `Version: 1.3.27`, contained `--aurora-readable-measure`, and included the `!important` page-title override.
- PressCACHE purge after `1.3.27` returned `Cache Purge: Success`.
- Jetpack Boost Critical CSS did complete the earlier generation pass once, reporting `6 files generated 7 minutes ago`, then a final regeneration was started after `1.3.27`; after repeated polling and refresh it remained at `Generating Critical CSS. Please do not leave this page until completed.`
- Final readability audit: `docs/current-state/reports/readability-audit-20260701-post-live.md` and `docs/current-state/reports/readability-audit-20260701-post-live.json`.
- Final readability result: `0` failures across Home, Blog, article, Work, About, Vancouver AI category, and Contact at `1440x1100`, `768x900`, `390x844`, and `360x740`.
- Screenshot evidence:
  - `docs/current-state/reports/screenshots/aurora-readability-work-mobile-20260701.png`
  - `docs/current-state/reports/screenshots/aurora-readability-about-mobile-20260701.png`
  - `docs/current-state/reports/screenshots/aurora-readability-blog-desktop-20260701.png`
  - `docs/current-state/reports/screenshots/aurora-readability-article-desktop-20260701.png`
- Post-readability performance audit: `docs/current-state/reports/performance-audit-20260701-post-readability-live.md`.
- Supporting performance diagnostics: `docs/current-state/reports/performance-audit-20260701T183901Z-cold-ttfb-cleanup-before.md` and `docs/current-state/reports/performance-deep-diagnostic-findings-20260701.md`.
- `make status-readonly` passed WP smoke with `0` failures and `0` warnings; it still reports open issues `#125` and `#86`.
- Current route truth after the final evidence refresh: `/work/` returns `200` directly, while `/projects/` makes one redirect hop to `/work/`.
- Authenticated diagnostic snapshots appeared during evidence staging; they were not committed because they contain admin/user/snippet data and were preserved outside the repo at `/tmp/kriskrug-wp-sensitive-snapshots/20260701T184126Z-cold-ttfb-cleanup` and `/tmp/kriskrug-wp-sensitive-snapshots/20260701T184425Z-work-canonical-change`.

Final blockers:

- Issue #125 remains open because the final Jetpack Boost Critical CSS regeneration had not completed after the `1.3.27` deploy.
- Lighthouse/PageSpeed LCP, INP, CLS, and TBT were not captured in this pass; the local performance script records route timing, cache headers, image payload, blocking-script candidates, URL hygiene, and live theme version.
- Cold-cache TTFB remains high on `/`, `/about/`, and `/work/` in the final audit, while warm cache remains acceptable.

## Aurora Opal 1.3.28 live deployment - 2026-07-01

- Reviewed PR #280 before merge: GitHub reported `mergeStateStatus: CLEAN`, required checks were green, and the diff was limited to `theme/kk-aurora/` plus public audit evidence/screenshots.
- Marked PR #280 ready and merged it to `main` with merge commit `0456d84a32bb092bd7af058bb9fd4cf1e0e7e4ac`.
- Synced local `main` to the merged commit and built `/Users/kk/Desktop/kk-aurora-opal-1.3.28-20260701.zip` from `theme/` so the archive root is `kk-aurora/`.
- Verified rollback package `/Users/kk/Desktop/kk-aurora-readability-1.3.27-20260701.zip` with `unzip -t` and confirmed it reports `Version: 1.3.27`.
- Verified the `1.3.28` package with `unzip -t`; package readback showed `Version: 1.3.28`, `--aurora-opal-void`, and `--aurora-readable-measure`.
- WordPress theme upload/replace confirmed installed `KK Aurora` version `1.3.27` and uploaded `KK Aurora` version `1.3.28`; the `Replace installed with uploaded` flow completed with `Theme updated successfully.`
- Live cache-busted CSS readback after deploy reported `Version: 1.3.28` and contained both `--aurora-opal-void` and `--aurora-readable-measure`.
- PressCACHE purge after `1.3.28` returned `Cache Purge: Success`.
- `make status-readonly` passed WP public smoke with `0` failures and `3` warnings.

Post-deploy visual/readability evidence:

- Live audit report: `docs/current-state/reports/aurora-opal-live-audit-20260701.md`.
- Machine-readable audit: `docs/current-state/reports/aurora-opal-live-audit-20260701.json`.
- Screenshot set: `docs/current-state/reports/screenshots/aurora-opal-live-20260701/`.
- Result: threshold failure count `0` across Article, Blog, About, Vancouver AI, Services, and Contact at `1440x1100`, `768x900`, `390x844`, and `360x740`.
- The first Contact mobile screenshot hit a transient `503`; it was replaced with a screenshot gated on HTTP `200`.

Jetpack Boost / issue #125 status:

- Jetpack Boost no longer exposed the previous Critical CSS generation UI during this pass.
- The authenticated Boost page routed to `#/getting-started`; probes for `#/dashboard`, `#/settings`, `#/performance`, `#/modules`, and `#/critical-css` all stayed on the getting-started/onboarding view.
- No `Critical CSS` control was available, and the `Start for free` onboarding action was not clicked because this deploy only approved Critical CSS regeneration, not Jetpack product onboarding or settings changes.
- Issue #125 remains open.

Follow-up discovered during live evidence:

- The deployed `single.html` includes `aurora-reader-pane`, but public article HTML renders `.aurora-article` without `.aurora-reader-pane`.
- Interpretation: production appears to have a customized/stale Site Editor single-post template shape for the article wrapper, similar to the earlier homepage source-parity finding.
- Effect: the core opal tokens, typography, contrast, and page/card surfaces are live, but the single-post pane/sheen interaction does not bind on production.
- Recommended Track B follow-up: either reset/port the live single-post template to the merged theme template after snapshot/rollback approval, or add a theme fallback that targets `.aurora-single-2026 .aurora-article` for the reader-pane surface and JS interaction.
