# Aurora Theme Release Checklist

Use this checklist for every manual `kk-aurora` production deploy on Pagely (wp-admin zip upload — no SFTP/SSH).

## Pre-release (repo)

- [ ] Bump `Version:` in `theme/kk-aurora/style.css`
- [ ] Bump `KK_AURORA_VERSION` in `theme/kk-aurora/functions.php` to match
- [ ] Add changelog entry in `theme/kk-aurora/readme.txt` with PR/commit references
- [ ] Run `make verify` (or at minimum `make test` + `make validate`)
- [ ] Visual spot-check on Local WP (`http://localhost:10003`) if available

## Package

- [ ] Zip `theme/kk-aurora/` (exclude `.DS_Store`, editor cruft)
- [ ] Record zip checksum: `shasum -a 256 kk-aurora.zip`
- [ ] Retain previous zip as rollback artifact (name with version)

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

- Versions **1.3.16–1.3.18** are on branch `aurora/synthetic-feel-refactor` (PR #185) pending merge to `main`.
- Production was at **1.3.12** as of 2026-06-09 morning-truth; repo `main` is **1.3.15**.
