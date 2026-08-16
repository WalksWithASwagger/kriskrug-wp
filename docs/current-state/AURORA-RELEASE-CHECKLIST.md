# Aurora Theme Release Checklist

Use this checklist for every manual `kk-aurora` production deploy on Pagely (wp-admin zip upload — no SFTP/SSH).

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
- [ ] `make status-readonly` — confirm GSAP CDN check if version includes GSAP removal
- [ ] Cross-post evidence to open issues (#125, #127, #189 as applicable)

## Rollback

- [ ] Re-upload previous version zip from retained artifact
- [ ] Purge Pagely cache again
- [ ] Re-verify logged-out render

## Current release note (2026-08-16)

- Public `style.css` reports Aurora **1.6.5**. Aurora **1.6.6** for #733 and #743 is merged on `main` via PR #751; deploy remains a KK gate.
- The committed pre-deploy baseline manifest is `reports/visual-baseline/manifest-20260816T151617Z.json`. It captures `/` and `/speaking/` at 200 across mobile, tablet, and desktop.
- `/marquee/` currently returns 404 and is not a valid live release gate. Verify the marquee archive copy in source; the visual runbook uses `/category/vancouver-ai-ecosystem/` as the live archive-template substitute until the marquee route exists.
- A post-deploy candidate diff, cache purge, public 1.6.6 readback, rollback receipt, and Jetpack Boost regeneration are still required. This checklist and PR do not authorize those actions.
