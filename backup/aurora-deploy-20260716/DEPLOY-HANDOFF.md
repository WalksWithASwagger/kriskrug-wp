# WordPress Theme Upload Package — Aurora 1.3.40

**Status:** package-ready; production not deployed  
**Prepared:** 2026-07-16 (Cursor Cloud morning workplan)

## Why 1.3.40 (not the older 1.3.39 zip)

Issue #351 prepared a hashed **1.3.39** SEO-metadata package. `main` has since merged Aurora **1.3.40** search-title rendering (#357 / PR #358). Uploading the old 1.3.39 zip would miss that module. This package is built from current `main` theme tree + rollback from `ba8101e` (live 1.3.37 social-metadata owner).

## Artifacts (local / agent workspace; zips are gitignored)

| Role | File | SHA-256 |
|---|---|---|
| Deploy | `backup/aurora-deploy-20260716/kk-aurora-seo-search-titles-1.3.40-1.3.40-20260716.zip` | `8e1c1321f94b1caf5d899697f5ddef6256d1274c74a67cd64d84645b1c24fad5` |
| Rollback | `backup/aurora-deploy-20260716/kk-aurora-live-1.3.37-1.3.37-20260716.zip` | `cfa1307e68db77c9bd8b9423fbd35be984a1d98b6d4f6829b3a540b701a1d1b4` |

Machine-readable: `backup/aurora-deploy-20260716/package-report.json`

**Verified (agent, 2026-07-16T00:43:21Z):** both SHA-256 values above still match the local zips; live public theme remains `1.3.37`. Evidence: `docs/current-state/reports/aurora-140-package-verify-20260716-004321Z.md`. Re-hash immediately before any KK upload.

Rebuild anytime:

```bash
ALLOW_DIRTY=1 make aurora-package \
  LABEL=seo-search-titles-1.3.40 \
  OUTPUT_DIR=backup/aurora-deploy-20260716 \
  ROLLBACK_REF=ba8101e \
  ROLLBACK_LABEL=live-1.3.37 \
  REPORT=backup/aurora-deploy-20260716/package-report.json
```

## Included scope

- #36 / #333: standard meta description ownership repairs (in 1.3.39 line)
- #346 / #349: homepage Open Graph title preservation
- #347 / #350: Blog pagination canonical + matching `og:url`
- #357 / #358: approved `jetpack_seo_html_title` document titles on singulars

## Explicitly excluded

- #316 schema Code Snippet deployment
- #345 WordPress `blogname` change
- Any content / #339 publisher-batch writes
- Search Console indexing requests

## Manual upload gate (KK only)

Production upload requires exact approval of **this** zip + checksum (not the 2026-07-13 1.3.39 hashes).

1. Reconfirm live Aurora is still `1.3.37` via public `style.css`.
2. Upload the 1.3.40 deploy zip through wp-admin theme replace.
3. Confirm WordPress reports `1.3.40`; purge PressCACHE.
4. Smoke `/`, `/blog/`, `/blog/page/2/`, `/about/`, `/speaking/`, and one article (normal + Googlebot/Twitterbot/Facebook).
5. Confirm regression titles from `docs/current-state/AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md`.
6. Roll back with the 1.3.37 zip immediately if any invariant fails.

wp-admin upload URL: https://kriskrug.co/wp-admin/theme-install.php?browse=upload
