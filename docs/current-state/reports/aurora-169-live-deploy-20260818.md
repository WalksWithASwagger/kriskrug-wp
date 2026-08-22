# Aurora 1.6.9 live deploy receipt — 2026-08-18

**Status:** live. Public `style.css` reads 1.6.9. `/work/` cards include Dark Crystal and unofficial.city.
**Track:** Track B theme SFTP plus a bounded Track A page write.
**Source:** PR #861 on `main`, then this production apply.

No new live WordPress write is required for review or merge of this receipt.

## What went live

1. SFTP swap of `wp-content/themes/kk-aurora` to repo 1.6.9 (`scripts/deploy_theme_sftp.py deploy`). Previous theme preserved at `./wp-content/themes/kk-aurora.bak-1787021714` (1.6.8).
2. Public `style.css` Version header: **1.6.9**. Homepage Projects footer links `https://darkcrystal.app/` and `https://unofficial.city/`. The `vancouver-made.vercel.app` alias is gone from chrome.
3. Work page 2672 (`/work/`) received a surgical insert of Dark Crystal and unofficial.city cards before Photography. The full content-architecture `work.html` payload was **not** applied; it is a shorter grid and would have dropped live lab cards. Pre-write snapshot: `backup/20260818T025650Z-work-lab-cards/page-2672-work-before.json`.

## Verification

Cache-busted public readback on 2026-08-18:

- `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=` → `Version: 1.6.9`
- `https://kriskrug.co/` footer → Dark Crystal + unofficial.city; no Vercel alias
- `https://kriskrug.co/work/?cb=` → `Explore Dark Crystal` and `Explore unofficial.city`; Photography card still present

## Rollback

- Theme files: SFTP rename `kk-aurora.bak-1787021714` back to `kk-aurora`.
- Work page: POST `content.raw` from `backup/20260818T025650Z-work-lab-cards/page-2672-work-before.json` to `pages/2672`. Identity check: id `2672`, slug `work`, status `publish`.

## Still KK

- Search Console **Verify** for `https://unofficial.city/` (file already 200).
- Do not submit an unofficial.city sitemap until [vancouver-made #92](https://github.com/WalksWithASwagger/vancouver-made/issues/92) deploys `robots.txt` and `sitemap.xml`.
- June 18 Creative AI Human Lab network post stays draft.
- Jetpack Boost critical-CSS regen (#731) still owed.
