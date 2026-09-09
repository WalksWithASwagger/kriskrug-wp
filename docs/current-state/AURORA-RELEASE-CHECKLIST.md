# Aurora Theme Release Checklist

Use this checklist for every `kk-aurora` production deploy on Pagely. A merge
is not a deploy. Every live theme change still needs explicit KK approval, a
rollback artifact or named rollback path, package or upload verification, a
Pagely cache purge, and a logged-out public readback.

Do not treat this file as a live version ledger. Confirm production with a
public `style.css` `Version:` header and `make check-live-parity`. The deploy
marker lives in [`theme/kk-aurora/CHANGELOG.md`](../../theme/kk-aurora/CHANGELOG.md).

## Supported channels

Both channels already exist in this repo. Use the one KK names for that
release; do not invent a third path.

1. **wp-admin zip** via `make aurora-package`, then Appearance → Themes → Add New → Upload.
2. **Pagely SFTP** via [`scripts/deploy_theme_sftp.py`](../../scripts/deploy_theme_sftp.py). Authentication is `WP_SFTP_PASSWORD` in process env or the documented macOS Keychain service. See [`ACCESS_CHANNELS.md`](ACCESS_CHANNELS.md). Availability must be verified at execution time.

REST `WP_APP_PASSWORD` cannot upload themes.

## Pre-release (repo)

- [ ] KK approved this specific Version and named the deploy channel
- [ ] Bump `Version:` in `theme/kk-aurora/style.css`
- [ ] Bump `KK_AURORA_VERSION` in `theme/kk-aurora/functions.php` to match
- [ ] Add changelog entry in `theme/kk-aurora/readme.txt` with PR/commit references
- [ ] Add a version line to `theme/kk-aurora/CHANGELOG.md` and set its deploy-status marker (this is the deploy ledger)
- [ ] Run `make verify` (or at minimum `make test` + `make validate`)
- [ ] Visual spot-check on Local WP if available

## Package (wp-admin zip path)

- [ ] Build and verify the upload package:
  ```bash
  make aurora-package LABEL=<short-release-label> ROLLBACK_REF=<previous-good-ref> COPY_PATH=1 OPEN_ADMIN=1
  ```
- [ ] Confirm the helper reports the expected deploy `Version:`, rollback `Version:`, and SHA256 checksums.
- [ ] Retain the rollback zip printed by the helper.

## Deploy

- [ ] Use only the KK-named channel (wp-admin zip or SFTP)
- [ ] Confirm the active live `style.css` Version after upload
- [ ] Remove Customizer "Additional CSS" safety-net if present (masks reveal bugs)

## Post-deploy verification

- [ ] Purge Pagely cache
- [ ] Logged-out spot-check: homepage, `/blog/`, one real post
- [ ] Public `style.css` readback matches the expected Version
- [ ] `make check-live-parity`
- [ ] `make status-readonly` if the release claimed GSAP/CDN removal
- [ ] Cross-post evidence to the owning issue

## Rollback

- [ ] Restore the retained wp-admin zip or the named SFTP rollback seat
- [ ] Purge Pagely cache again
- [ ] Re-verify logged-out render and the public `style.css` Version
