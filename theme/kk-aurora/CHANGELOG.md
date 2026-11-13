# kk-aurora Changelog

Version history for the `kk-aurora` theme, doubling as a deploy ledger. This
repo is adjacent to the live site, not a mirror of it, so the "Deployed" marker
on each entry is the single answer to "what is live, and what changed."

Format is loosely [Keep a Changelog](https://keepachangelog.com/). Newest first.
Deploy status uses:

- **LIVE** confirmed on production by a public `style.css` readback
- **On main** merged to `main`, deploy status not confirmed
- **Superseded** no longer the deploy target; kept for history

Entry detail is derived from `theme/kk-aurora/readme.txt` and the version-bump
commit subjects (`git log --oneline -- theme/kk-aurora/style.css`). Older
1.3.x history lives in `readme.txt`.

When you cut a new release, add a line here and follow
`docs/current-state/AURORA-RELEASE-CHECKLIST.md`.

---

## 1.7.3
**Deployed:** Not deployed. Repo-only release candidate; production stays on 1.7.2 until KK approves the merge and a deploy. The live `kk-aurora//front-page` template is a database override that beats the theme file, so the homepage band needs a separate check and approved update at deploy time.
The footer newsletter tile, the homepage newsletter band and the /blog/ eyebrow promise a monthly letter instead of a weekly email, following KK's 2026-11-12 ruling (#1278). Wording only; no links, classes or block markup changed.

## 1.7.2
**Deployed:** LIVE via SFTP on 2026-11-12 at 17:52 America/Vancouver (2026-11-13 00:52 UTC) after KK's in-chat approval. 67 files staged, then atomically swapped; the 1.7.1 rollback seat is `kk-aurora.bak-1794531136`. Before the swap, an authenticated all-status read found no page (50) or post (1,060) using the removed `blank` or `no-title` templates. Public `style.css` reads 1.7.2, `make check-live-parity`, `make wp7-smoke` (8/8) and `make seo-publisher-smoke` pass, the homepage no longer loads `marquee.js`, and category archives emit their own `og:url`. The pixel gate did not run (cached Chromium build no longer matches the installed Playwright). See `docs/current-state/reports/aurora-172-deploy-2026-11-12.md`.
Load `marquee.js` only when the rendered front page contains a marquee board (#1237). The check runs on rendered blocks, so it also holds under the saved `kk-aurora//front-page` template. Archive, taxonomy, date, author, post type and search routes emit their canonical URL as `og:url`, built from the query rather than the request path (#1228). Routes without a description stop showing the retired site tagline and fall back to existing copy: the Writing archive description (the posts page SEO description) on journal routes, and elsewhere the theme's hard-coded `homepage_meta_description()` text, which is the RSS channel description and not the live homepage meta description. The fallback copy awaits KK approval. New `tests/functions-smoke.php` covers both, plus the `/writing` and `/projects` redirects. Reconciles the readme and changelog deploy markers and sets Tested up to 7.0 (#1243). Removes the `blank` and `no-title` custom templates from `theme.json`: neither template file ever existed, and no published page or post uses them; a new `tests/theme-json-smoke.php` requires a template file for every declared custom template (#1239, KK ruling 2026-11-12). PHP, `theme.json`, tests and metadata only; no CSS, template, part or pattern file changed.

## 1.7.1
**Deployed:** LIVE via SFTP on 2026-11-03 after KK's #1172 release approval. All 65 files were verified before the swap. PressCACHE and CDN purges succeeded. Boost generated six Critical CSS files, and the canonical blog and long post served the regenerated styles after the page cache refresh. Stylesheet parity and desktop/mobile journal checks passed. See `docs/current-state/AURORA-WRITING-RELEASE-2026-11-03.md`.
Scope journal component rules beneath the journal page class so WordPress inline block/global styles cannot override the approved typography and spacing. Store the saved-template back arrow as an HTML entity to preserve it through production database normalization.

## 1.7.0
**Deployed:** Superseded by 1.7.1 the same day. Was deployed via SFTP on 2026-11-03 after KK approval, then replaced by the 1.7.1 production style-order correction. PR #1172 merged as 964ebcb0.
Rebuild the Writing index, search and archives around a shared thumbnail/title/excerpt row. Add a calm article layout with a 680px reading measure, 20px desktop / 18px mobile prose, and a responsive contents list. Replace blog chrome with the approved compact header and footer. Remove superseded blog grids, panel treatments, paragraph reveals, image fades and reading-pane effects; other site sections retain their existing styles. Keep native WordPress search, pagination, taxonomy feeds, authored content and related-post exclusions.

Production has a saved `kk-aurora//single` template (wp_id 12415) that must be snapshotted and synchronized during the approved release. Regenerate Jetpack Boost critical CSS and purge the page/CDN caches after the theme/template swap. The review packet documents local verification and rollback; local rendering is not a live pixel-gate pass. This release also contains main's undeployed 1.6.13 URL corrections.

## 1.6.13
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-11-03 1.7.0/1.7.1 SFTP release, whose pre-release rollback seat held 1.6.12). See `docs/current-state/AURORA-WRITING-RELEASE-2026-11-03.md`.
Point sitewide header, footer, and homepage CTAs at `/generative-ai-services/` and `https://www.futureproof.website/` so chrome stops hopping through 301/308s (#1131). Href-only; copy unchanged.

## 1.6.12
**Deployed:** Superseded by the 2026-11-03 1.7.0/1.7.1 SFTP release, which records 1.6.12 as the pre-release live theme. Was LIVE (public `style.css` readback 2026-09-30 via `make check-live-parity`; same Version was already recorded 2026-09-21 in `CURRENT-STATE-2026-09-21.md`). Method not recorded in that verification; that marker was version-readback only.
Adds The Sky Smoked Back to the sitewide Projects footer so the released film shares the same project-network path as the Work page and AI Garden (#1042).

## 1.6.11
**Deployed:** Superseded by 1.6.12 (public `style.css` 2026-09-21 and 2026-09-30). Was LIVE (public `style.css` readback 2026-09-09). Method not recorded in that verification; that marker was version-readback only.
Reverts the 1.6.10 event-artboard CSS in full. It should never have shipped. The `/events/` art direction was **not** missing its styles: `scripts/events_page/render_events_page.py` emits a complete page-scoped design system in a `<style>` block with its own `--events-*` token set, and it has done since the art-direction work in PR #943. The 1.6.10 rules were added on the false premise that no CSS existed, and every one of them lost to the page-scoped rules on specificity (`.aurora-events-page .aurora-event-art` beats `.aurora-event-art`), so they were inert on the only page those classes appear. Removing 130 dead front-end lines and retiring the #943 budget waiver; budget back to 7489 / 173 exactly.

## 1.6.10
**Deployed:** Superseded by 1.6.11, which reverts it. Was live 2026-09-03 for roughly 30 minutes (rollback seat `kk-aurora.bak-1788461588`).
Events artboards and editorial marks (#943). PR #943 shipped the renderer markup for `/events/` with no CSS at all, so the generated posters and the twelve editorial marks had nothing to style them and the page could not ship. This adds it: `.aurora-event-art` and its `--image` / `--generated` / `--cover` / `--contain` variants, four `--palette-N` gradients, the date/mark/role spans, `.aurora-event-compact-media`, and `.aurora-editorial-mark`. Event photos crop at 4:3 rather than inheriting `.aurora-proof-media`'s 16:9, which guillotines a portrait frame. +130 front-end lines in `style.css`, `!important` held at 173, and zero new color literals: the four palettes use `color-mix` over existing `var(--aurora-*)` tokens, so the contrast registry needed no new entries. Budget waived 7489 to 7619 against #943.

## 1.6.9
**Deployed:** Superseded by 1.6.11 (public `style.css` 2026-09-09). Was LIVE (SFTP 2026-08-18, rollback `kk-aurora.bak-1787021714`). Public `style.css` then read 1.6.9. Projects footer links Dark Crystal and `https://unofficial.city/`. Work page 2672 got a surgical card insert (not a full `work.html` replace) so the live lab grid kept Skywhale, Gorgeous Ghost, Wedges, Ghost Radio, and Ethos. Snapshot: `backup/20260818T025650Z-work-lab-cards/`. Receipt: `docs/current-state/reports/aurora-169-live-deploy-20260818.md`.

## 1.6.8
**Deployed:** Superseded (was live 2026-08-17 until the 1.6.9 swap; rollback seat `kk-aurora.bak-1786942075`; prior swap `kk-aurora.bak-1786942015`). Public `style.css` then read 1.6.8. Custom FSE `front-page` (wp_id 12661) was snapshotted then POSTed from theme `front-page.html` at 2026-08-17 04:51 UTC; homepage now renders labs / logo soup / stages / What People Say. Pixel vs pre-HTML 1.6.7 (`20260817T044445Z` → `20260817T045150Z`): homepage fail 55–62% (expected height + new bands); 29 other pairs pass; `/blog/` tablet warn 0.49%. Boost CSS bundle hash moved `d4faec73b4` → `0f9e6b2840`. Explicit #731 wp-admin regen still owed.
Homepage cluster: rewrite the Join BC / Futureproof work-band copy, align the triptych, and quiet the card numerals (#411); restore a Creative Labs band with text-below-image cards (#412); bring back a monochrome interactive client logo soup (#413). Stages, What People Say, and newsletter follow in the same cut (#414–#416).

## 1.6.7
**Deployed:** Superseded (was live 2026-08-17 until the 1.6.8 swap; rollback seat `kk-aurora.bak-1786938401`)
Chrome copy: sitewide `<title>` separator becomes a pipe and the surname takes the umlaut (#756). Front page keeps the full descriptor; inner pages take a short `Kris Krüg` tail. Writing-archive og/twitter titles, `public_site_name()`, header, footer, and shipped patterns follow the same ruling. Live chrome uses `BC + AI` (spaces) per #735. Descriptors are not unified. No CSS change. 1.6.6 copy/orphan cleanup shipped in the same swap. Jetpack Boost critical-CSS regen (#731) still owed (wp-admin; app password cannot session-login).

## 1.6.6
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-17 1.6.7 deploy)
Copy and dead-file cleanup, no layout or CSS change. Strips the five user-visible em dashes from theme copy: the homepage hero dek and services lede, the marquee archive lede, and the photo-gallery pattern's lede plus its placeholder alt text (#733). Removes the orphaned speaking proof-grid template part and its `theme.json` registration; the part was placed by zero templates and live proof-grid content is DB page content, not this part (#743).

## 1.6.5
**Deployed:** Superseded (was live 2026-08-14 to 2026-08-17; replaced by the 1.6.7 deploy)
Add AI Garden to the project footer and ship the previously merged Creative AI Human Lab links with an explicit versioned release. Pagely page and CDN caches were purged successfully. The post-purge visual comparison confirmed live/repo CSS identity and a refreshed Jetpack Boost bundle; its threshold failures are confined to the intentional project-footer expansion documented in `report-20260814T190349Z.md`.

## 1.6.4
**Deployed:** Superseded by later 1.6.x deploys (was LIVE on public readback 2026-08-11; the 2026-08-11 window shipped 1.6.1 through 1.6.4 together, rollback `kk-aurora.bak-1786415439`). Do not treat this dated LIVE marker as current production.
CLS/LCP fix: critical-geometry guard in the header part pins marquee + header layout during the stale-Boost-critical-CSS window; reveal hide moves from stylesheet to JS ownership with synchronous above-fold reveal (#701, PR pending). After deploying, regenerate Jetpack Boost critical CSS.

## 1.6.3
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-11 1.6.4 deploy)
PSI perf round: right-sized WebP theme assets (#702, PR #711), display-sized Photon variants in the contact sheet (#704, PR #714), self-hosted Futureproof key art (#705, PR #712), composited-only transitions (#707, PR #713), and the five homepage WCAG contrast fixes (#708, PR #715). Merged 2026-08-10.

## 1.6.2
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-11 1.6.4 deploy)
Collapse 12 width breakpoints to the 480/768/1200 token scale; CSS budget lowered to 6902 lines / 162 importants (#479, PR #703, merged 2026-08-10).

## 1.6.1
**Deployed:** Built, not deployed (superseded in repo by 1.6.2 the same day)
Detach form error/success selectors the #681 purge left glued to the footer rule and restore their color rules (#698, PR #699, merged 2026-08-10).

## 1.6.0
**Deployed:** Superseded (was live 2026-08-10 to 2026-08-11; replaced by the 1.6.4 deploy)
Delete 97 dead CSS classes and 9 dead `@keyframes` from `style.css` (#478, PR #681, merged 2026-08-07).

## 1.5.11
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-10 1.6.0 deploy)
Primitives layer plus block-editor parity so the editor canvas renders cream/ink instead of the pre-Revive dark palette (#476, PR #680, merged 2026-08-05).

## 1.5.10
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-10 1.6.0 deploy)
Focus-visible states on work and service cards for WCAG 2.4.7, plus the `functions.php` version catch-up missed in 1.5.9 (PR #676, merged 2026-08-05).

## 1.5.9
**Deployed:** Superseded (live 2026-08-05 to 2026-08-10 per public readbacks; replaced by the 1.6.0 deploy)
Retire the drop cap (#475, PR #672, merged 2026-08-05).

## 1.5.8
**Deployed:** Superseded (never live as 1.5.8; deploy was gated on #601, and its CSS first shipped inside the later 1.5.9 deploy)
`aurora-tstm` testimonials showpiece CSS (#596, PR #629, merged 2026-08-02).

## 1.5.7
**Deployed:** Superseded (SFTP-deployed live 2026-08-01 pre-merge; PR #618 synced the repo to live; replaced by the 1.5.9 deploy)
Full-bleed `krug-1` portrait hero on Home and About (PR #618, merged 2026-08-01).

## 1.5.1 through 1.5.6
**Deployed:** Never released (skipped numbers)
Reserved by the stylesheet rebuild plan (#475 as 1.5.1, #476 as 1.5.2, #477 as 1.5.3+) and skipped when the hero shipped straight to 1.5.7; the reserved work later landed as 1.5.9 and 1.5.11.

## 1.5.0
**Deployed:** Superseded (was live 2026-07-27 to 2026-08-01; source PR #493 merged 2026-07-27, resolving #545)
Cascade `@layer` scaffold plus `--kk-*` tokens (#474).

## 1.4.9
**Deployed:** On main; deploy status unknown
Homepage newsletter band rewritten with an honest weekly-email CTA and three recent-post thumbnails; blog-index band drops the dispatch/field-notes chrome (#416, #505).

## 1.4.8
**Deployed:** Superseded
Replace the "authored judgment" copy on the homepage (#410).

## 1.4.7
**Deployed:** Superseded
Responsive `srcset` for the homepage hero image (#407).

## 1.4.6
**Deployed:** Superseded
Convert `.aurora-writing-card` (the blog-index card) to the cream system across all six declaration sites, fixing an archive listing that was effectively blank under cream-era ink (#485).

## 1.4.5
**Deployed:** Superseded
Contrast fixes for inline-link hover, form validation errors, and submit labels; raise homepage work-card copy over the scrim; tokenize the control-label color; drop dead pre-cream literals; add a CSS literal-contrast test.

## 1.4.4
**Deployed:** Superseded
Darken the accent orange to #9a2f14 and the primary control fills so accent text clears AA on every cream surface; darken Ink Muted; restore the theme skip link and suppress the duplicate core one.

## 1.4.3
**Deployed:** Superseded
Full-bleed header shell so the brand pins left on ultrawide; larger italic rainbow "message" word and a riso gradient rule under homepage section heads (R5/R6).

## 1.4.2
**Deployed:** Superseded
Fix leftover dark meta with `color-scheme: light` and a cream `theme-color`; preload Space Grotesk and DM Sans instead of the unused Inter and Clash Display.

## 1.4.1
**Deployed:** Superseded
Cream accessibility polish: AA-safe accent text for kickers, visible focus rings on paper, removal of the duplicate theme skip link, and tighter header nav (R1 to R4).

## 1.4.0
**Deployed:** Superseded
Port the Revive cream/ink visual system into kk-aurora; retokenize `theme.json` and `style.css` (Space Grotesk / DM Sans / JetBrains Mono); rebuild the sticky header (woven marquee, scroll progress), footer, and homepage section order; add a global page CSS bridge so Track A packs inherit cream/ink.
