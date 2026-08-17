# Aurora 1.6.8 live deploy receipt — 2026-08-17

**Status:** live. CSS and homepage HTML both read back as 1.6.8.
**Track:** Track B theme deploy (SFTP + FSE template write). This file is the docs closeout.
**Issues:** homepage cluster #411–#416 (source on `main` via PR #844). Boost regen #731 still owed.

No new live WordPress write is required for review or merge of this receipt.

## What went live

1. SFTP swap of `wp-content/themes/kk-aurora` to repo 1.6.8 (`scripts/deploy_theme_sftp.py deploy` under `varlock run --inject vars`, venv Python with paramiko). Latest rollback directory on the host: `./wp-content/themes/kk-aurora.bak-1786942075` (1.6.7). An earlier same-evening swap left `kk-aurora.bak-1786942015`.
2. Public `style.css` Version header: **1.6.8**. Later unversioned + cache-busted identity: all 8 harness CSS files match `main` (`style.css` md5 `a02cf12be8ec`, `revive-port.css` `e10e375afbfe`).
3. Theme file deploy did not change `/` until the customized FSE template was updated. Live `front-page` is `source=custom`, REST id `kk-aurora//front-page`, **wp_id 12661**. Snapshot then POST of theme `front-page.html` at 2026-08-17 04:51 UTC. Public `/` then had `aurora-creative-labs`, `aurora-logo-soup`, `aurora-stages-band`, `aurora-people-say-band`, heading `BC + AI. Futureproof`. Title stayed `Kris Krüg | AI Keynote Speaker & Creative Technologist`.

## Pixel gate

Authoritative comparison is pre-HTML 1.6.7 vs post-HTML 1.6.8:

| | Run |
|---|---|
| Baseline | `reports/visual-baseline/manifest-20260817T044445Z.json` |
| Candidate | `reports/visual-baseline/manifest-20260817T045150Z.json` |
| Diff / report | `diff-20260817T045150Z.json` / `report-20260817T045150Z.md` |

**29 pass / 1 warn / 3 fail.** Homepage mobile 58.1% / tablet 62.0% / desktop 55.4% with height +46–57%. That is the intended #411–#416 band rewrite, not a rollback trigger. `/blog/` tablet 0.4929% warn; mobile and desktop `/blog/` were sha256-identical (likely post-list churn or a mask miss, not a theme-wide break). All other 10 routes × 3 viewports were sha256-identical.

A CSS-only capture from the first SFTP swap (before the template POST) is kept as `044333Z` → `044820Z`: homepage fail 17–24%, Boost hash still `d4faec73b4`. After the HTML write, Boost CSS bundle moved `d4faec73b4` → `0f9e6b2840`. That is not a substitute for the explicit Jetpack Boost critical-CSS regen in wp-admin (#731). App password cannot session-login.

Harness capture-time CSS identity still printed live 1.6.7 / DRIFT because it fetches unversioned URLs. Post-capture identity is MATCH. See the footnote on `report-20260817T045150Z.md`.

PNG captures are gitignored. Do not commit them.

## Rollback

- Theme files: SFTP rename `kk-aurora.bak-1786942075` back to `kk-aurora`.
- Homepage HTML: restore snapshot `backup/20260817T045123Z-front-page-template-12661/` (JSON is tracked; HTML sibling is gitignored). POST that `content.raw` back to `https://kriskrug.co/wp-json/wp/v2/templates/kk-aurora/front-page?context=edit`. Identity check before write: slug `front-page`, wp_id `12661`, id `kk-aurora//front-page`. GET `/templates/12661` 404s; the slug path works.

## Still KK

- #731 Boost critical-CSS regen in wp-admin.
- Homepage copy confirm (labs list, ten-name client soup, real marks vs wordmarks).
- Content applies #764 / #729 / #612 / #706.
- #745 14-draft cull and #740 26-file MOVE table: not this deploy.
