# Aurora Content Recovery - 2026-05-25

## What happened

The rich page content was not mostly deleted. It was masked by Aurora theme templates.

Authenticated production checks on 2026-05-25 showed:

- Active production theme is `kk-aurora` version `1.3.0`.
- Production `home` template source is `theme`, not a Site Editor DB override.
- Production `home` still contains `aurora-home-2026`, so `/blog/` is serving a stale theme template rather than the repo writing archive.
- Production page templates for Work, Speaking, Services, and Publications are theme-sourced hardcoded `page-*` templates without `wp:post-content`.
- WordPress REST content for Work, Speaking, Services, About, and now Publications contains the richer recovered page content.

Conclusion: this is stale theme deployment plus template masking, not a wholesale content loss.

## Repo recovery changes

- Retired hardcoded content-page templates from `theme/kk-aurora/templates/`:
  - `page-2672.html`
  - `page-recent-projects-include.html`
  - `page-work.html`
  - `page-speaking.html`
  - `page-services.html`
  - `page-generative-ai-services.html`
  - `page-publications.html`
- Kept homepage and blog theme-owned:
  - `front-page.html`
  - `home.html`
- Kept ordinary content pages editable through `page.html`, which includes `wp:post-content`.
- Bumped Aurora cache-bust version to `1.3.3`.
- Added `content/source-packs/keynotes-2026/wp-payloads/publications.html`.
- Added Publications to `content/source-packs/keynotes-2026/wp-payloads/page-meta.json`.
- Re-expanded About photo proof with restored Mette-Marit, Trailer Park Boys, Roy Henry Vickers / Chief Ted Walkus, and Amanda Tapping details.

## Live writes completed

Snapshots were taken before live REST writes:

`backup/20260525-201025Z/page-snapshots/`

The snapshot set includes public HTML and authenticated REST JSON for:

- `/blog/`
- `/recent-projects-include/`
- `/speaking/`
- `/generative-ai-services/`
- `/publications/`
- `/about/`

Authenticated REST updates were applied only to:

- About page ID `1208`, slug `about`, modified `2026-05-25T12:11:17`
- Publications page ID `1895`, slug `publications`, modified `2026-05-25T12:11:19`

Work, Speaking, and Services already had rich DB content, so no redundant REST overwrite was needed.

## Verification snapshot

After the REST writes:

- `/about/` public HTML and REST both contain `Mette-Marit`, `Trailer Park Boys`, `Amanda Tapping`, and `Roy Henry Vickers`.
- `/publications/` REST contains `The public record behind the rooms`, `Popular Science: NASA Needs`, and `Georgia Straight: Geek Speak`.
- `/publications/` public HTML still shows the old hardcoded Publications template until the theme deploy lands.
- `/recent-projects-include/`, `/speaking/`, and `/generative-ai-services/` REST contain recovered rich content markers, while public HTML is still masked by live theme templates.
- `/blog/` public HTML still contains `aurora-home-2026` and does not contain `aurora-writing-archive`.

## Deploy artifact

Installable recovery theme package:

`/Users/kk/Desktop/kk-aurora-content-recovery-1.3.3.zip`

`unzip -t` passed with no compressed-data errors.

## Production closeout

KK uploaded the recovery theme and purged caches. A follow-up Aurora `1.3.4` package was then prepared, uploaded, and purged:

`/Users/kk/Desktop/kk-aurora-live-qa-polish-1.3.4.zip`

Final live checks on 2026-05-25 confirmed:

- Active theme is `kk-aurora` version `1.3.4`.
- `/blog/` renders the writing archive, not the homepage clone.
- Work, Speaking, Services, Publications, About, Podcast EPK, Events, and Contact render through the recovered generic page path with one visible H1 each.
- Events content hero is now H2, leaving the generic `Events` page title as the single H1.
- Contact no longer has the oversized drop cap; computed `::first-letter` style is normal paragraph text.
- `/work/` redirects to `/recent-projects-include/`, preserving query strings.
- `/services/` redirects to `/generative-ai-services/`, now preserving query strings after updating Redirection rule ID `4` from `flag_query=exact` to `flag_query=pass`.

Post-upload screenshots and metrics:

`backup/20260525-qa-visual-134/`

Remaining note: Contact still reports Jetpack/CDN CORS console errors for Jetpack form module scripts. The form is visible and styled, but the CORS issue is host/plugin-side rather than Aurora CSS/content recovery work.
