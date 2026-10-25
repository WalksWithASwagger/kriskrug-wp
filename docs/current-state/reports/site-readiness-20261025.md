# kriskrug.co readiness receipt — October 25, 2026

## Events: live

[PR #1134](https://github.com/WalksWithASwagger/kriskrug-wp/pull/1134) merged as
`16fc6742948e1889573894820e232568bf55cc97` after the required summary, Python,
JavaScript, browser, voice and docs jobs passed. PHP/CSS/security jobs were skipped
by path selection, not reported as passes.

Kris explicitly approved the prepared page-2250 update. The apply verified
`2250 / events / page / publish`, checked the preflight content hash immediately
before writing, saved a private exact snapshot and verified stored content.
Only `content` was written. All 74 existing live event identities and the
evergreen shell were preserved. An unrelated catalog addition was excluded.

Normal and uncached public GETs at 18:47 UTC both returned 200 with three
spotlights: Futureproof, Prompt Victoria, AMPA. September's spotlight was absent,
the hidden-card rule was present and Get tickets linked directly to
`https://www.futureproof.website/tickets/`.

Validation: 88 focused Events tests; JavaScript behavior/syntax; docs truth;
Chromium at 1440, 768 and 390px. No horizontal overflow or script errors; visible
ticket-button focus; advancing the clock and resuming the tab retired the festival
and released its photo. The same browser checks were repeated against the actual
post-apply public HTML at all three widths: three initial cards, two after the
October 31 cutoff, released festival photo, no overflow or script errors and
visible keyboard focus. Public GETs and authenticated readback confirm delivery.

Rollback remains `deploy_events_page.py --restore <private page-2250 snapshot>`,
preview first, then execute only with the observed current hash. No unrelated
catalog/status/counter implementation was included; #1100 stays open.

## Approved image repair: applied, visually accepted and publicly delivered

The existing image-only approval in #1114 was retained. The documented SFTP route
authenticated with a verified host key. Before applying, exact live files and the
database-owned front-page override (WordPress 12661) were captured privately.

Applied at 18:49 UTC:

- Packaged `assets/img/bcai-living-ecosystem.jpg` from merged #1118.
- One source/dimension replacement in the file and active database homepage.
- The two reviewed Work social-image fallback lines in `functions.php`.

All other live source was preserved. PHP syntax passed, uploaded bytes and the
database readback matched the prepared hashes. The image URL returns 200 JPEG;
normal and uncached homepage responses use the packaged image with 1200×800
dimensions. The uncached Work response uses it as og:image with 1200×800 metadata.
The normal Work URL initially served the old cached og:image. At 19:16 UTC its
cache expired and both the normal and uncached responses delivered the packaged
image. This closes the Work social-image delivery check.

The WordPress MCP session was expired and the available admin browser sessions
required sign-in. Discovery of the site's registered REST routes found Jetpack
Boost's `page-cache/action/clear-page-cache`; the existing application credentials
received HTTP 403 on that action. No successful cache purge is claimed.
An authenticated Pagely/WordPress operator is still needed for the remaining
shared-header/footer cache follow-through described below.

Visual baseline `20261025T184522Z` versus after `20261025T184946Z`:

- 30 route/viewport pairs are SHA-256 identical.
- Only the homepage image card changed. All page heights are unchanged.
- Mobile 2.2259% and desktop 1.1922% exceed the automatic failure threshold;
  tablet 0.6847% is a warning. The original FAIL report is retained.
- Image loading on the homepage improved from 21/22 to 22/22. These observations
  do not establish LCP/CLS improvement.

The changed regions were inspected and are confined to the repaired artwork.
Kris explicitly answered **“Accept repaired image baseline”** on October 25.
Following that approval, full baseline `20261025T190433Z` was frozen: 33 captures,
all expected route statuses, manifest retained in this PR. The original automatic
FAIL remains recorded; this is explicit acceptance, not a rewritten pass result.
The unchanged Boost CSS hash is expected for this image/PHP-only scope: no CSS
was changed. The generated report's generic CSS-deployment warning does not
override the exact stored bytes, public image source and observed pixel change.
The image-only rollback script checks the current file/template hashes before
restoring the private originals and removing only the newly added image. Since
the later copy release also touches the homepage, restore that release first
before using the earlier image rollback; do not bypass the hash guard.

Aurora's public header remains 1.6.12; this is a bounded hunk apply, not 1.6.13.
The Work page's body image is a separate old reference and was not included in
the approved social-image fallback repair.

## Festival copy and shared links: approved and applied; some edge caches pending

Kris separately answered **“Approve prepared copy and link update.”** Exact
current-source diffs, private rollback snapshots and 390/1440px public-shell
previews were prepared before approval, with no overflow and correct link/focus
checks. At 19:16 UTC the trusted SFTP route applied only these reviewed changes:

- Homepage festival copy: “come together in Vancouver, October 28–30, 2026”.
- Footer YouTube: `https://www.youtube.com/kriskrug10000` (direct public 200).
- Eight Services hrefs across homepage/header/footer: `/generative-ai-services/`.
- Footer festival href: `https://www.futureproof.website/`.

The three live template files and the custom front-page override were verified
against their prepared hashes before writing; exact byte/content readbacks
matched after writing. Header/footer remained theme-owned. Functions, CSS,
version headers and schema were not changed by this release. Rollback restores
these three files and this database payload only, preserving the image repair.

Full live comparison `20261025T190433Z` → `20261025T191650Z`: **33 PASS, zero WARN,
FAIL or ERROR**, with zero height changes. Homepage differences were 0.0758%
mobile, 0.0624% tablet and 0.0134% desktop, within the automatic threshold.
The accepted image baseline and original image FAIL report remain retained.

Six public routes were checked both normally and uncached at 19:28 UTC. All
twelve returned 200. Homepage, Events and Work normal URLs deliver the changes.
All six uncached responses have the corrected shared links. Normal Speaking,
Services and Contact responses still have their cached earlier header/footer.
Events' corrected cards and direct ticket link are also present.

Kris requested cache clearing through Varlock. That route authenticates as a
WordPress administrator with `manage_options`, but the installed Boost REST
action additionally verifies `X-Jetpack-WP-JS-Sync-Nonce`. The application
password cannot supply that browser-session nonce, and the request returned 403.
The alternative Boost cache-clear ability exists in installed plugin source but
is not registered on this site (404); Pagely's installed purge form also requires
an admin-session nonce. No purge completed, no authentication checks were changed
and no credentials were exposed. A signed-in admin purge or natural cache expiry
remains necessary for those three normal URLs. Source apply and uncached delivery
are not represented as full edge convergence.

## Schema and sitemap handoffs

The unchanged approved Snippet 5 candidate remains SHA-256
`a6037656daabafd5afacddea3885357e5d042ff204aa5ce01222bb1b8f8db0e6`, 14,765 bytes.
Authenticated readback confirmed active global `KK Schema`, ID 5, as the sole
active schema emitter. Exact private source/state backup, paste-ready text,
diff and rollback are prepared. PHP syntax and 16 schema/preflight tests passed.
The save is still assigned to Kris by #1089. No live VideoObjects or validator
success is claimed.

Sitemap reconciliation was prepared privately for #1130. At 18:48 UTC, the
intentional 301 handoff led to a 200 XML index with 986 post and 46 page entries.
The three maintained category/tag/author samples were 200 and noindex,follow.
The September 3 #331 v2 deployment receipt already records the selected policy.
Recommendation: reconcile the old checklist and narrow closure/evidence work;
do not redeploy taxonomy policy. No new GSC access, issue closure or public
comment was performed. Sitemap entries are not Google-indexed page counts.

## Repository verification and reserve draft

Full `make python-test` passed: 184 publisher, 841 operational, 12 SEO inventory
and 68 SEO backfill/link-safety tests. CI's first Python run caught four tests
still treating September as the active snapshot; those fixtures now exercise
October's guidance. Ruff, docs truth and visual storage guards pass.

[Draft PR #1141](https://github.com/WalksWithASwagger/kriskrug-wp/pull/1141)
contains the bounded #402 ALL IN navigation proposal. Current inspection found
existing series links and an extra duplicate block on Day Two. The draft
consolidates those blocks, includes the existing final dispatch, and proposes
relevant next steps. It preserves article media/captions/quotations and remains
unmerged and unpublished for editorial review. Conversion instrumentation and
the #1090 selection remain separate; no production forms were submitted.
