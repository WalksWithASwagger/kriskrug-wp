# WordPress Theme Upload Package

**Status:** package-ready; production not deployed

- Source: `/Users/kk/.codex/worktrees/kriskrug-wp-issue-351/theme/kk-aurora`
- Slug: `kk-aurora`
- Label: `seo-metadata`
- Version: `1.3.39`
- Deploy zip: `/Users/kk/Code/kriskrug-wp/backup/aurora-deploy-20260713/kk-aurora-seo-metadata-1.3.39-20260713.zip`
- Deploy SHA256: `d4a812abe51a1d879be4a290a7381b6d9222a08a4fd1cc2145b1adf67019e86d`
- Rollback zip: `/Users/kk/Code/kriskrug-wp/backup/aurora-deploy-20260713/kk-aurora-live-rollback-1.3.37-20260713.zip`
- Rollback version: `1.3.37`
- Rollback SHA256: `aef9c779b216d04fe5c500868137822f598c8036e31f15477ebb4f5f0e9b62d9`
- wp-admin upload URL: https://kriskrug.co/wp-admin/theme-install.php?browse=upload
- Clipboard: not requested
- Browser: not requested

## Manual Upload Gate

1. Open the wp-admin upload URL.
2. Upload `kk-aurora-seo-metadata-1.3.39-20260713.zip`.
3. Choose the WordPress replace/update flow for the existing artifact.
4. Confirm WordPress reports the expected uploaded version.
5. Purge PressCACHE/cache layers and run the route-specific verification for the change.

Production upload requires this exact approval:

> Deploy Aurora 1.3.39 to kriskrug.co using the prepared SEO metadata package and run the documented verification.

This package must not be uploaded based only on issue or pull-request approval.

## Release Scope

Included:

- #36: emit one standard meta description from the existing Jetpack SEO fields.
- #346: preserve the keynote-first homepage Open Graph title when the front-page object title is empty.
- #347: emit a clean self-canonical and matching `og:url` for every Blog archive page.

Explicitly excluded:

- #316: Person and WebSite schema Code Snippet deployment.
- #345: WordPress `blogname` change.
- Any content, analytics, Search Console, DNS, permissions, credential, plugin, or unrelated WordPress write.

## Package Verification

- `make test`: 293 tests passed, including publisher, operational, inventory, Python, JavaScript, and plugin smoke checks.
- Documentation truth checks passed.
- PHP syntax checks passed.
- `make verify` completed the available test and documentation gates, then stopped only because local `phpcs` is not installed. Pull-request CI must run the PHP validation gate before merge.
- Both archives passed `unzip -t` with no compressed-data errors.
- Deploy package readback reports Aurora `1.3.39` and contains the homepage-title and Blog-canonical repairs.
- Rollback package readback reports Aurora `1.3.37`.

## Production Preflight

Fresh read-only evidence from 2026-07-13 records Aurora `1.3.37` as the live theme and Code Snippet 12 as inactive. Immediately before an approved upload:

1. Reconfirm the public theme version is still `1.3.37`.
2. Reconfirm Code Snippet 12 is inactive and Aurora remains the sole social metadata owner.
3. Confirm the deploy and rollback hashes still match this handoff.
4. Stop if any value differs or another WordPress edit is in progress.

## Post-Deploy Verification

After the approved upload, purge PressCACHE and inspect each route in normal, cache-busted, Googlebot, Twitterbot, and Facebook crawler reads:

| Route | Required result |
| --- | --- |
| `https://kriskrug.co/` | `200`; one non-empty `og:title`; existing document title unchanged |
| `https://kriskrug.co/blog/` | `200`; canonical and `og:url` both equal `https://kriskrug.co/blog/` |
| `https://kriskrug.co/blog/page/2/` | `200`; canonical and `og:url` both equal `https://kriskrug.co/blog/page/2/` |
| `https://kriskrug.co/about/` | `200`; title and existing social metadata remain unchanged |
| `https://kriskrug.co/speaking/` | `200`; title and existing social metadata remain unchanged |
| `https://kriskrug.co/2026/01/24/both-hands-full/` | `200`; one standard description and existing social metadata remain valid |

Across the matrix:

- standard descriptions appear exactly once where configured;
- titles remain byte-for-byte unchanged from the preflight capture;
- every page has only one active metadata owner;
- Blog page N canonicals and `og:url` values agree;
- JSON-LD remains valid;
- no route regresses from `200`.

Run read-only Search Console URL Inspection for `/` and `/blog/` after public verification. Do not request indexing for this release.

## Rollback

If any route status, title, description, canonical, Open Graph, ownership, or JSON-LD invariant fails:

1. Upload `kk-aurora-live-rollback-1.3.37-20260713.zip` through the WordPress replace/update flow.
2. Confirm WordPress reports version `1.3.37`.
3. Purge PressCACHE and repeat the full route and crawler matrix.
4. Record the failure and rollback evidence on #351 before any further production write.
