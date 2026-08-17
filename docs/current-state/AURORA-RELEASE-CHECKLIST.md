# Aurora Theme Release Checklist

Use this checklist for every manual `kk-aurora` production deploy on Pagely: wp-admin zip upload, no SFTP/SSH.

## Pre-release (repo)

- [ ] Bump `Version:` in `theme/kk-aurora/style.css`
- [ ] Bump `KK_AURORA_VERSION` in `theme/kk-aurora/functions.php` to match
- [ ] Add changelog entry in `theme/kk-aurora/readme.txt` with PR/commit references
- [ ] Add a version line to `theme/kk-aurora/CHANGELOG.md` and set its deploy-status marker (this is the deploy ledger)
- [ ] Run `make verify` (or at minimum `make test` + `make validate`)
- [ ] Visual spot-check on Local WP (`http://localhost:10003`) if available

## Package

- [ ] Build and verify the upload package:
  ```bash
  make aurora-package LABEL=<short-release-label> ROLLBACK_REF=<previous-good-ref> COPY_PATH=1 OPEN_ADMIN=1
  ```
- [ ] Confirm the helper reports the expected deploy `Version:`, rollback `Version:`, and SHA256 checksums.
- [ ] Retain the rollback zip printed by the helper.

## Deploy (wp-admin)

- [ ] Upload zip via Appearance → Themes → Add New → Upload
- [ ] Confirm active theme version in wp-admin matches expected
- [ ] Remove Customizer "Additional CSS" safety-net if present (masks reveal bugs)

## Post-deploy verification

- [ ] Purge Pagely cache
- [ ] Logged-out spot-check: homepage, `/blog/`, one real post
- [ ] `make status-readonly`: confirm GSAP CDN check if version includes GSAP removal
- [ ] Cross-post evidence to open issues (#125, #127, #189 as applicable)

## Rollback

- [ ] Re-upload previous version zip from retained artifact
- [ ] Purge Pagely cache again
- [ ] Re-verify logged-out render

## Current release note (2026-08-17)

- Live Aurora **1.6.8** (public `style.css` 2026-08-17; SFTP rollback `kk-aurora.bak-1786942075`). Homepage HTML matches theme `front-page.html` after FSE template 12661 POST.
- Pre-HTML 1.6.7 baseline: `reports/visual-baseline/manifest-20260817T044445Z.json`. Post-HTML candidate: `manifest-20260817T045150Z.json` / `diff-20260817T045150Z.json` / `report-20260817T045150Z.md`. Homepage 55–62% fail is the #411–#416 bands; 29 other pairs passed; `/blog/` tablet warn 0.49%.
- `/marquee/` currently returns 404 and is not a valid live release gate. The visual runbook uses `/category/vancouver-ai-ecosystem/` as the live archive-template substitute until the marquee route exists.
- Jetpack Boost critical-CSS regen (#731) still needs a wp-admin session. Bundle hash did change `d4faec73b4` → `0f9e6b2840` after the HTML write; that is not a substitute for the explicit regen.
