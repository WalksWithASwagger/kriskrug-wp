# Aurora P0 Staging Rescue - 2026-05-19

Track: B - Aurora v2 theme
Branch: `codex/aurora-p0-staging-rescue-2026-05-19`
Base: `origin/aurora/v2` at `88da99a`
Issue: `#80` - `[AURORA P0] Rescue staging header/nav render`

## Status

Ready for PR review against `aurora/v2`. This slice does not touch production WordPress, Track A content, the Notion connector, or `main`.

## What Changed

- Stabilized the desktop header grid so brand, primary nav, newsletter, and booking CTA stay in their lanes.
- Added no-wrap behavior for nav/action labels to avoid awkward desktop/tablet wrapping.
- Added a two-row tablet header pattern below `1180px`.
- Tightened mobile header density while keeping the newsletter utility visible at normal phone width.
- Added a `max-width: 360px` fallback that drops only the newsletter utility to avoid overflow on very narrow screens.
- Kept keyboard focus visibly rounded on header controls.
- Disabled header backdrop blur under `prefers-reduced-motion: reduce`.
- Refreshed `theme/kk-aurora.zip` from the updated theme folder.
- Rebased on PR `#93` so the P0 branch includes the merged swarm-wave header and visual-system work.

## Local QA Setup

Local WordPress was running the active `kk-aurora` theme on `http://localhost:10003`.

For same-origin asset QA only, local `home` and `siteurl` were temporarily changed from `http://kriskrug-local.local` to `http://localhost:10003`, because the local HTML otherwise served stylesheet URLs on a different host than the QA browser. They were restored after QA:

```text
home:    http://kriskrug-local.local
siteurl: http://kriskrug-local.local
```

Local theme backup before syncing the patched branch theme into Local:

```text
/tmp/kk-aurora-local-before-p0-20260519-152406.tgz
```

The in-app browser verified DOM/navigation state, but its screenshot capture path timed out after the first successful pass. Screenshots were captured with local Brave headless through `puppeteer-core` instead.

## Screenshot Artifacts

- Desktop: `docs/current-state/aurora-smoke-2026-05-19/aurora-home-desktop.png`
- Mobile: `docs/current-state/aurora-smoke-2026-05-19/aurora-home-mobile.png`
- Layout metrics: `docs/current-state/aurora-smoke-2026-05-19/aurora-home-metrics.json`
- Focus/reduced-motion checks: `docs/current-state/aurora-smoke-2026-05-19/aurora-accessibility-checks.json`

## Smoke Matrix

All checked URLs returned `200` and included both `kk-aurora-style-css` and `aurora-header-2026`.

| URL | Result |
|---|---|
| `/` | 200, Aurora markers present |
| `/about/` | 200, Aurora markers present |
| `/speaking/` | 200, Aurora markers present |
| `/recent-projects-include/` | 200, Aurora markers present |
| `/2026/05/16/make-culture-not-content/` | 200, Aurora markers present |
| `/2026/05/15/your-taste-is-your-moat/` | 200, Aurora markers present |
| `/2026/05/14/calling-us-all-in/` | 200, Aurora markers present |
| `/2026/05/07/web-summit-vancouver-2026/` | 200, Aurora markers present |

## Responsive Results

- Desktop `1440x1000`: header height `74px`, no horizontal overflow, newsletter visible.
- Tablet `900x900`: header height `108px`, no horizontal overflow, newsletter visible.
- Mobile `390x844`: header height `138px`, no horizontal overflow, newsletter visible.
- Narrow `320x720`: header height `138px`, no horizontal overflow, newsletter hidden by the narrow fallback.

## Accessibility And Motion

- First six keyboard tab stops showed visible focus treatment.
- Reduced-motion emulation reported `prefers-reduced-motion: reduce = true`.
- Header backdrop filter resolved to `none` in reduced-motion mode.
- Sampled animated/button/media elements reported `animationName: none` and near-zero transition duration.

## Verification Commands

```bash
git diff --check
php -l theme/kk-aurora/functions.php
jq empty theme/kk-aurora/theme.json
unzip -t theme/kk-aurora.zip
rg -n 'letter-spacing:\s*-|"letterSpacing"\s*:\s*"-' theme/kk-aurora || true
```

All checks passed.

## Next Round

1. Review and merge the P0 branch into `aurora/v2`.
2. Close or update issue `#80` after the PR lands and artifacts are accepted.
3. Start the next Aurora issue on final media/source-of-truth: replace temporary or externally sourced imagery with KK-owned or approved assets.
4. Then move to first-viewport mobile CTA/content polish and deeper page template checks.
