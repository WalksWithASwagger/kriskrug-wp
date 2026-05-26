# Aurora Live QA - 2026-05-25

## Scope

Live post-deploy QA after uploading `kk-aurora` 1.3.3, then the 1.3.4 polish package, and purging caches.

Checked:

- `/`
- `/blog/`
- `/recent-projects-include/`
- `/speaking/`
- `/generative-ai-services/`
- `/publications/`
- `/about/`
- `/podcast-guesting-page-epk/`
- `/events/`
- `/contact/`
- `/work/`
- `/services/`

Desktop viewport: `1280x720`.
Mobile viewport: `390x844`.

Screenshots and machine-readable metrics:

- `backup/20260525-qa-visual/qa-results.json`
- `backup/20260525-qa-visual/qa-contact-sheet.png`
- `backup/20260525-qa-visual/qa-main-nav-contact-sheet.png`
- `backup/20260525-qa-visual-134/qa-results.json`
- `backup/20260525-qa-visual-134/qa-summary.json`

## Passes

- Active theme reads `kk-aurora` version `1.3.3`.
- Recovery templates are clean: production template inventory shows only `front-page`, `home`, and generic `page` among the relevant page templates.
- `/blog/` renders the writing archive with one H1: `Field notes for the age of generative everything.`
- Work, Speaking, Services, Publications, and About render their rich DB content rather than the retired hardcoded templates.
- No checked page had horizontal overflow at desktop or mobile viewport.
- No checked page reported broken visible images.
- No checked page had visible missing-alt images in the first-pass metric scan.
- No browser console errors were captured during the page loads.
- Internal kriskrug.co link check covered `49` URLs from the audited pages with no 4xx failures.
- `/work/` redirects to `/recent-projects-include/`.
- `/services/` redirects to `/generative-ai-services/`.

## Page Notes

| Page | Status | Notes |
|---|---|---|
| `/` | Pass | Homepage still owns the `aurora-home-2026` keynote surface. Desktop and mobile first view look coherent. |
| `/blog/` | Pass | Writing archive is live. Old homepage-clone headline is gone. |
| `/recent-projects-include/` | Pass with polish note | Recovered Work content appears on desktop and mobile. Generic page title creates extra top spacing before the custom hero, especially mobile. |
| `/speaking/` | Pass with polish note | Recovered Speaking content appears. Same generic-title spacing issue as Work. |
| `/generative-ai-services/` | Pass with polish note | Recovered Services content appears. Same generic-title spacing issue as Work. |
| `/publications/` | Pass with polish note | Restored Publications archive content appears. Same generic-title spacing issue as Work. |
| `/about/` | Pass with polish note | Restored photo proof markers are present: Mette-Marit, Trailer Park Boys, Amanda Tapping, Roy Henry Vickers. Same generic-title spacing issue as Work. |
| `/podcast-guesting-page-epk/` | Pass with polish note | Content is intact. Generic page title makes first screen quieter than the custom hero. |
| `/events/` | Resolved in 1.3.4 polish pass | Initial QA found two visible H1s. The content hero is now H2, leaving `Events` as the single public H1. |
| `/contact/` | Pending 1.3.4 upload | Form is visible and no broken links/images were detected. The 1.3.4 theme package neutralizes the oversized drop-cap `P`; verify after upload. |
| `/work/` | Pass | Alias redirects to `/recent-projects-include/` and recovered Work markers are present. |
| `/services/` | Pass | Alias redirects to `/generative-ai-services/` and recovered Services markers are present. |

## Recommended Follow-Up From 1.3.3 QA

1. Create a small Aurora 1.3.4 polish patch for generic page surfaces:
   - tighten `.aurora-page-2026` top padding on ordinary pages,
   - reduce `.aurora-page-header` bottom spacing on mobile,
   - either integrate the generic page title with custom hero rhythm or visually reduce it.
2. Fix Events H1 semantics by changing the content hero H1 to H2 or by adjusting the generic page template strategy.
3. Neutralize the theme drop-cap on Contact and other non-overhauled generic pages.
4. Optional: run a later external-link audit for legacy Publications links. Internal links checked clean; old offsite interview links were not exhaustively audited in this pass.

## 1.3.4 Polish Pass

Started on branch `codex/aurora-live-qa-polish` after preserving the dirty 1.3.3 recovery checkout.

Completed:

- Events live content was snapshotted and patched via authenticated REST. Page ID `2250`, slug `events`, status `publish`, title `Events` were verified before the write.
- The Events content hero heading changed from H1 to H2. Public regular and cache-busted checks now show exactly one H1 on `/events/`: `Events`.
- Snapshot/readback files are under `backup/20260525-220404Z/page-snapshots/`.
- Pre-upload public checks passed:
  - `make wp7-smoke EXPECT_VERSION=6.9.4`,
  - corrected marker/H1 checks for `/blog/`, `/recent-projects-include/`, `/speaking/`, `/generative-ai-services/`, `/publications/`, `/about/`, and `/events/`.
- Aurora `1.3.4` theme patch prepared locally:
  - reduced generic page top/title spacing,
  - reduced mobile page header spacing,
  - neutralized the page-content drop-cap from `assets/css/typography-refined.css`,
  - kept the generic `wp:post-title` visible as the canonical page H1.
- Installable package built at `/Users/kk/Desktop/kk-aurora-live-qa-polish-1.3.4.zip`; `unzip -t` passed.

Pre-upload gate, later resolved:

- WordPress REST exposes only read-only theme routes for this install, so the `1.3.4` theme upload still needs wp-admin/Pagely upload.
- Jetpack Boost cache clear endpoint exists but returns `403` with application-password auth; purge remains wp-admin/Pagely-gated.
- KK uploaded the 1.3.4 zip and purged caches; post-upload QA below is the current truth.

## 1.3.4 Post-Upload Closeout

KK uploaded the 1.3.4 package and purged caches. Post-upload checks confirmed:

- Authenticated theme inventory reports active `kk-aurora` version `1.3.4`.
- Deployed `style.css` reports `Version: 1.3.4`.
- Deployed `assets/css/typography-refined.css` contains the `.aurora-page-content > p:first-of-type::first-letter` drop-cap override.
- `make wp7-smoke EXPECT_VERSION=6.9.4` passed.
- Desktop and mobile browser QA passed for `/`, `/blog/`, `/recent-projects-include/`, `/speaking/`, `/generative-ai-services/`, `/publications/`, `/about/`, `/podcast-guesting-page-epk/`, `/events/`, `/contact/`, `/work/`, and `/services/`.

Post-upload browser QA results:

- Every checked page returned `200` after redirects resolved.
- Every checked page had exactly one visible H1.
- `/events/` has `#aurora-events-title` as H2.
- `/contact/` first-letter computed style is normal text (`float: none`, inherited font size/weight).
- No checked page had horizontal overflow.
- No checked page reported broken visible images or visible images missing an `alt` attribute.
- `/work/` redirects to `/recent-projects-include/` with query strings preserved.
- `/services/` redirects to `/generative-ai-services/` with query strings preserved after updating Redirection rule ID `4` from `flag_query=exact` to `flag_query=pass`.

Residual note:

- `/contact/` still logs Jetpack/CDN CORS errors for Jetpack form module scripts from `s5102.pcdn.co`; the form renders and the Aurora drop-cap issue is fixed, but the module-script CORS noise should be handled as a separate host/plugin investigation if form submission behavior misbehaves.
