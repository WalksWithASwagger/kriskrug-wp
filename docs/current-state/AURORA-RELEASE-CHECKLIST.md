# Aurora Theme Release Checklist

Use this checklist for every manual `kk-aurora` production deploy on Pagely (wp-admin zip upload — no SFTP/SSH).

## Pre-release (repo)

- [ ] Bump `Version:` in `theme/kk-aurora/style.css`
- [ ] Bump `KK_AURORA_VERSION` in `theme/kk-aurora/functions.php` to match
- [ ] Add changelog entry in `theme/kk-aurora/readme.txt` with PR/commit references
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

## Notes

- Versions **1.3.16–1.3.18** (PR #185 synthetic.ai refactor) are merged to `main`; repo `main` is now **1.3.18**.
- Production was at **1.3.12** as of 2026-06-09 morning-truth.
- 2026-06-14: deploy package staged at `backup/aurora-deploy-20260614/` (1.3.18 zip + git-rebuilt 1.3.12 rollback + checksums + `DEPLOY-HANDOFF.md`). Awaiting KK wp-admin upload (#204/#189).
