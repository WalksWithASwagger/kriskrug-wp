# Aurora Header Logo Closeout - 2026-06-03

## Summary

The Aurora header wordmark is shipped to the canonical repo line and is live on production.

- Repo commit: `8530a10 theme: add Aurora header wordmark`
- Prior closeout commit: `3ce45a2 docs: record aurora logo closeout`
- Theme package: `/Users/kk/Desktop/kk-aurora-header-logo-1.3.9-20260603.zip`
- Fresh truth report: `docs/current-state/reports/morning-truth-20260603-170932Z.md`
- Production status: `kk-aurora` version `1.3.9` is active and the header loads `kriskrug-wordmark.png`
- Residual caveat: Jetpack Boost critical CSS still contains stale `.aurora-brand-mark` rules in inline CSS, but the old `KK` header markup is gone

## What Changed

- The header link now keeps one accessible name with `aria-label="Kris Krug home"`.
- The image is decorative with `alt=""` and includes explicit `width="468" height="229" decoding="async"`.
- The old `.aurora-brand-mark` placeholder and subtitle markup are gone from `origin/main`.
- The new asset lives at `theme/kk-aurora/assets/img/kriskrug-wordmark.png`.
- `site_icon` was left alone; the wide wordmark is not a favicon.

## Verification

Passed locally:

- `php -l theme/kk-aurora/functions.php`
- `unzip -t /Users/kk/Desktop/kk-aurora-header-logo-1.3.9-20260603.zip`
- Static preview at `http://127.0.0.1:8765/`
- Desktop preview: logo loaded, old brand mark count `0`, CTA visible, no horizontal overflow
- Mobile preview: logo loaded, old brand mark count `0`, CTA visible, no horizontal overflow
- `make morning-truth`

Passed on production after wp-admin theme replacement and cache purge:

- `style.css?cachebust=codex-style-live`: reports `Version: 1.3.9`
- Direct origin asset: `https://kriskrug.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png?cachebust=codex-logo-live` returned `HTTP/2 200`, `content-type: image/png`, `content-length: 63437`, and `x-gateway-cache-status: MISS`
- CDN asset: `https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png?cachebust=codex-cdn-live` returned `HTTP/2 200`, `content-length: 63437`, and `x-cache: Miss from cloudfront`
- Cache-busted public HTML contains the header image:
  `<img fetchpriority="high" class="aurora-brand-logo" src="https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png" alt="" width="468" height="229" decoding="async">`
- old header `<span class="aurora-brand-mark">KK</span>`: not present
- REST site identity: `site_logo=0`, `site_icon=0`, `site_icon_url=''`
- WP smoke from morning truth: failures `0`, warnings `0`, WordPress `6.9.4`

## Production Caveat

The string `.aurora-brand-mark` still appears in the cache-busted public source inside an inline `jetpack-boost` Critical CSS block. That is stale generated CSS, not live header markup. The Jetpack Boost admin page was regenerating Critical CSS and had advanced to about `55.95238%`; REST attempts against `jetpack-boost-ds` returned `403 rest_forbidden` with application-password auth, matching earlier deploy notes.

## Deploy Notes

- WordPress wp-admin upload reached the existing theme replacement screen:
  - installed: `KK Aurora` version `1.3.7`
  - uploaded: `KK Aurora` version `1.3.9`
  - destination: `/dom5102/wp-content/themes/kk-aurora/`
- The replacement action completed with `Theme updated successfully.`
- Pagely PressCACHE purge completed and reported `Cache Purge: Success`.
- The PressCDN admin screen showed CDN rewrite/config fields but no separate purge control. CDN readback was verified through the cache-busted `s5102.pcdn.co` asset URL.

## Production Handoff

The live logo deploy is complete. Remaining follow-ups:

1. Let Jetpack Boost finish/regenerate Critical CSS in wp-admin, then re-check cache-busted source for the stale `.aurora-brand-mark` CSS string.
2. Optional admin polish: upload the wordmark to Media Library and set `site_logo`.
3. Do not set `site_icon` from this wide wordmark.

## Workspace Cleanup

The pre-sync dirty side work was preserved before syncing `main`.

- Safety branch: `codex/pre-sync-main-20260603-aurora-logo`
- Stash: `stash@{0}: On main: pre-sync aurora article/blog side work 2026-06-03`
- Backup directory: `/tmp/kriskrug-wp-cleanup-20260603T163838Z`
- Backup files include `dirty.patch`, `untracked-files.txt`, and `untracked-files.tgz`

`git stash show --include-untracked --name-status stash@{0}` confirms the Track B article/blog theme edits, untracked article pattern files, the `2026-06-01-long-road-to-future-proof` draft pack, and the stale `morning-truth-20260602-173134Z.md` report are preserved in the safety stash. Current dirty Track B article/blog files remain present in the worktree and are intentionally left unstaged for a separate review branch.

## Next Polish Queue

Good next fixes now that the live logo deploy is done:

- `#125` Jetpack Boost Critical CSS regeneration/performance follow-up
- `#127` mobile/responsive QA
- `#120` Both Hands Full proof-card text/image overlap
- `#126` and `#68` Work page OG/social metadata
- `#122` generic page polish
- `#8` and `#9` small accessibility wins
- `#48`, `#36`, and `#43` accessibility/SEO metadata polish
