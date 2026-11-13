# Aurora 1.7.2 production deploy: 2026-11-12

Kris approved the deploy in chat on 2026-11-12 and named the channel (Pagely
SFTP with an atomic swap). He also approved pruning old theme backups on the
server to the newest three. This receipt follows
[`AURORA-RELEASE-CHECKLIST.md`](../AURORA-RELEASE-CHECKLIST.md).

## What shipped

Aurora 1.7.2 (PR #1261, plus the #1239 template removal), live since
17:52 America/Vancouver (2026-11-13 00:52 UTC):

- Archive pages emit their own `og:url` and description (#1228).
- The homepage loads `marquee.js` only when a marquee board is on the page (#1237).
- `readme.txt` and the theme `CHANGELOG.md` deploy markers reconciled (#1243).
- The unused `blank` and `no-title` custom templates removed from `theme.json` (#1239).

## Before the swap

- Repo `main` at `9ce8e70`, theme tree clean, `style.css` and `KK_AURORA_VERSION` both 1.7.2. Live read 1.7.1.
- #1239 gate: an authenticated, read-only, all-status read found no page (50 checked) and no post (1,060 checked) using `blank` or `no-title`.
- SFTP probe connected through `sftp.pressftp.com` with the host key verified.
- Public baseline: the homepage loaded `marquee.js`, and a category archive's `og:url` pointed at the homepage.

## Deploy

`scripts/deploy_theme_sftp.py deploy`: 67 files uploaded to `kk-aurora-deploy-1.7.2`, then swapped in. The previous 1.7.1 theme was renamed to `kk-aurora.bak-1794531136`, the rollback seat.

Cache: the Pagely edge kept serving 1.7.1 HTML on the canonical homepage. A
snapshot-first no-op save of page 2418 (Contact: title written back unchanged;
title, content and status hashes identical before and after; only `modified`
moved) refreshed the homepage and Contact at the edge. `/blog/` and older posts
still returned cached HTML that references `style.css?ver=1.7.1` for up to the
one-hour edge TTL. 1.7.2 changed no CSS rules, so that stale HTML renders the
same.

## After the swap

| Check | Result |
|---|---|
| Public `style.css` | `Version: 1.7.2` |
| `make check-live-parity` | PASS, live and `origin/main` agree on 1.7.2 |
| `make wp7-smoke` | 8 PASS, 0 FAIL |
| `make seo-publisher-smoke` | all PASS |
| Homepage (logged out, cache-busted) | 200, no `marquee.js`, no `kkm-board` markup |
| Category archive `og:url` | `https://kriskrug.co/category/ai-ethics-philosophy/` (was the homepage) |
| Category archive `og:description` | the Writing description, not the retired tagline |
| Visual spot-check (homepage, category archive, newest post) | rendered normally |

Not run: the pixel gate. `make visual-preflight` stops because the cached
Chromium build (1248) no longer matches the Playwright module the gate uses
(1.62.1 expects 1234). Fixing it means installing a newer Playwright module
locally; no visual baseline was frozen before this deploy.

## Server cleanup

With Kris's approval, 23 old `kk-aurora.bak-*` folders were deleted from the
server after the deploy was verified. Three remain:
`kk-aurora.bak-1793751411`, `kk-aurora.bak-1793751958` and
`kk-aurora.bak-1794531136` (the 1.7.1 rollback seat). The live `kk-aurora`
folder was confirmed present and serving 1.7.2 afterwards.

## Rollback

Over SFTP, rename `kk-aurora` aside and rename `kk-aurora.bak-1794531136` back
to `kk-aurora`, then refresh the edge with a no-op page save and re-check the
public `style.css` version.
