# Aurora Header Logo Closeout - 2026-06-03

## Summary

The Aurora header wordmark is shipped to the canonical repo line but is not yet live on production.

- Repo commit: `8530a10 theme: add Aurora header wordmark`
- Local `main`: synced to `origin/main` at `8530a10`
- Theme package: `/Users/kk/Desktop/kk-aurora-header-logo-1.3.9-20260603.zip`
- Fresh truth report: `docs/current-state/reports/morning-truth-20260603-164415Z.md`
- Production status: still serving the old `KK` badge header until the theme zip is uploaded and caches are purged

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

Live production readback after the blocked upload:

- `kriskrug-wordmark.png`: not present
- `.aurora-brand-mark`: still present
- old header `<span class="aurora-brand-mark">KK</span>`: still present
- REST site identity: `site_logo=0`, `site_icon=0`, `site_icon_url=''`
- WP smoke from morning truth: failures `0`, warnings `0`, WordPress `6.9.4`

## Deploy Blocker

The wp-admin SSO path worked and reached `https://kriskrug.co/wp-admin/theme-install.php?upload`, but Chrome could not attach the local zip through the Codex extension. The file chooser returned `Not allowed`.

WordPress REST does not provide a theme upload path on this install. `OPTIONS /wp-json/wp/v2/themes` reports `GET` only, matching the prior 1.3.4 deploy notes that theme upload is wp-admin/Pagely gated.

## Production Handoff

To finish the live logo deploy:

1. Upload `/Users/kk/Desktop/kk-aurora-header-logo-1.3.9-20260603.zip` in wp-admin:
   `Appearance -> Themes -> Add New -> Upload Theme -> Install Now`.
2. Choose `Replace current with uploaded`.
3. In Pagely, run `Purge All Caches + CDN`.
4. Verify with a cache-busted public readback:
   - public HTML contains `kriskrug-wordmark.png`
   - public HTML no longer contains `.aurora-brand-mark`
   - public theme assets report Aurora version `1.3.9`

Optional admin follow-up after deploy: upload the wordmark to Media Library and set `site_logo`. Do not set `site_icon` from this wide wordmark.

## Workspace Cleanup

The pre-sync dirty side work was preserved before syncing `main`.

- Safety branch: `codex/pre-sync-main-20260603-aurora-logo`
- Stash: `stash@{0}: On main: pre-sync aurora article/blog side work 2026-06-03`
- Backup directory: `/tmp/kriskrug-wp-cleanup-20260603T163838Z`
- Backup files include `dirty.patch`, `untracked-files.txt`, and `untracked-files.tgz`

The stash includes the Track B article/blog theme edits, the untracked article pattern files, the `2026-06-01-long-road-to-future-proof` draft pack, and the stale `morning-truth-20260602-173134Z.md` report. Treat that work as a separate review branch; do not fold it into the logo closeout.

## Next Polish Queue

Good next fixes after the live logo deploy:

- `#127` mobile/responsive QA
- `#120` Both Hands Full proof-card text/image overlap
- `#126` and `#68` Work page OG/social metadata
- `#122` generic page polish
- `#8` and `#9` small accessibility wins
- `#48`, `#36`, and `#43` accessibility/SEO metadata polish
