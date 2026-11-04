# Writing release: Pagely caches purged and public verification passed

KK approved merging #1172, deploying it, and checking the live blog and a long article on desktop/mobile on November 3, 2026 (Vancouver time).

## Source and deployment

- #1172 merged as `964ebcb051be6bd0206f8ee09bf04b74c2c5aa69`.
- Live testing exposed a production inline-style ordering conflict. #1173 scopes journal components beneath the existing journal page class, preserving the approved typography above WordPress inline defaults. It also stores the saved-template back arrow as an HTML entity after production character normalization.
- #1173 merged as `3fa675a7e578e2f2c8ba256e61001f2f8711d7bf`. All required hosted checks passed on `3879578043e655ea600c88d6e8426ac767514d18`; conditional security scan skipped.
- Aurora 1.7.1 deployed via the documented Pagely SFTP channel. The host key was verified before authentication. All 65 staged files matched committed source before the atomic swap.
- Saved single template `kk-aurora//single`, WordPress ID 12415, was synchronized. WordPress expanded its journal-entry pattern and added template-part theme bindings normally. Other saved templates and the two source posts checked were unchanged.

## Verification completed

Canonical browser URLs (not local previews) were checked:

- https://kriskrug.co/blog/ at 1440×900 and 390×844: titles 25px/22px, thumbnails 188px/94px, summaries 16px/15px, 19 posts, no horizontal overflow or hidden summaries.
- https://kriskrug.co/2026/11/02/you-cant-rent-a-social-licence/ at both sizes: 680px desktop reading measure, 20px/34.4px desktop paragraphs, 18px/30.6px mobile paragraphs, 68 paragraphs with none hidden, no paragraph reveal classes, 12 contents links, three related entries. The authored introductory photo caption remains 13px. Mobile contents start collapsed; contents navigation moved keyboard focus to the selected section.
- Mobile menu opens with Enter; Escape closes it and retains focus. Search for Futureproof navigates to native results using the journal layout.
- Page two, the Vancouver AI category, empty search, an older July article, and About return HTTP 200. Empty search displays the no-results state. About retains ordinary page chrome.
- Homepage desktop/mobile retain the old section design and have no horizontal document overflow after styles settle.
- `make verify PYTHON=.venv/bin/python` passed for the correction. CSS ratchet remains 7,142 lines and 162 important declarations. `git diff --check` passed.

These are manual live browser checks and source/readback checks, not a completed full-route frozen pixel comparison. The visual preflight passed using the installed browser cache after `/opt/pw-browsers` was absent. Browser interactions/captures used computer-use tooling. Brave was contended by concurrent interaction; responsive tests used the in-app browser.

## Remaining release work

The November 3 follow-up found the current journal layout on both canonical public URLs. The unversioned `style.css` now returns 1.7.1 and matches the local file byte for byte. `make check-live-parity` passed. Both pages reference Boost bundle `733ad59d41.min.css`, which contains the scoped journal rules. Fresh logged-out browser checks passed at 1440×900 and 390×844. The archive showed 19 entries with 188px and 94px thumbnails. The long post rendered 61 visible paragraphs with 20px desktop and 18px mobile body text. Neither page overflowed horizontally.

The signed-in PressCACHE page reported “Cache Purge: Success.” On November 4, the Pagely App Dashboard also reported “CDN Purge: Success” for the CDN-only action and indicated three to five minutes for propagation. The canonical blog and long post returned HTTP 200 with the current journal layout. The shared Boost stylesheet returned HTTP 200 on a CloudFront MISS and contained the deployed journal rules. Unversioned stylesheet parity passed. Logged-out browser checks at 1440×900 and 390×844 showed 19 archive entries, 188px and 94px thumbnails, and 61 article paragraphs with none hidden. Neither page overflowed horizontally.

Boost showed its setup screen with terms and site data sync. The setup screen was left open in Brave for KK. Critical CSS regeneration remains pending. CDN and browser evidence is in `cdn-purge-success.png`, `post-cdn-purge-http.json`, `post-cdn-purge-browser.json` and the four `cdn-purge-*.jpg` captures.

## Rollback and retained evidence

Private local evidence: `/private/tmp/kriskrug-blog-redesign-20261103/.generated/blog-review/release/` (ignored, not published).

- Exact pre-release theme: `live-theme-before.zip` and `live-theme-manifest.json`.
- Pre-release live theme retained remotely at `./wp-content/themes/kk-aurora.bak-1793751411` (1.6.12); this is the rollback seat for the entire design release.
- Intermediate 1.7.0 retained remotely at `./wp-content/themes/kk-aurora.bak-1793751958`.
- Saved template rollback: `single-before.json` / `single-before.html`; original raw SHA256 `b9b4f73f7fc2026b16433a0b91dbc13b13ad63ed741eb490b62760446b85c0a6`.
- `single-after.json`, `deployed-file-manifest.json`, `final-swap.json`, browser screenshots and `browser-checks.json` preserve readback.

A full rollback must restore both the 1.6.12 theme and saved template 12415, then refresh the same caches. Do not restore only the theme while leaving the new database template referring to journal patterns/parts. Preserve the unrelated saved front-page template.

The primary checkout and other owners' worktrees were not changed. No posts were edited for this release. The review fixture is retained for comparison; no task-owned recovery evidence has been deleted.
