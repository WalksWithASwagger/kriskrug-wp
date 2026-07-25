=== KK Aurora ===
Contributors: kriskrug
Requires at least: 6.4
Tested up to: 6.9
Requires PHP: 8.0
License: GPLv2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html

== Description ==

KK Aurora is a WordPress FSE theme for Kris Krug. Version 1.4.5 clears the remaining pre-cream foreground colour literals and adds a regression test that requires every hardcoded foreground colour to declare the surface it renders on.

Built for Full Site Editing with WCAG 2.1 AA accessibility.

== Features ==

* Full Site Editing (FSE) block theme
* Cream / ink Revive brand layer (1.4.0)
* Woven marquee chrome + scroll progress
* CSS/JS scroll reveals (no GSAP dependency on main; GSAP removed in 1.3.15)
* High contrast accessibility
* Mobile-first responsive design
* Custom block patterns

== Installation ==

1. Upload the theme folder to `/wp-content/themes/`
2. Activate the theme through the 'Themes' menu in WordPress
3. Start customizing with the Site Editor

== Color Palette ==

* Cream surface: #efe6d2
* Ink text: #171310
* Burnt orange accent (text/AA): #9a2f14
* Burnt orange control fill: #c03f18
* Burnt orange decorative: #d94a1f
* Riso yellow: #e8b53a
* Rainbow accents: teal / cyan / cobalt / violet / magenta

== Changelog ==

= 1.4.5 =
* a11y: `.aurora-inline-link:hover` was #ff735d — 2.15:1 on cream, i.e. hovering made the link less legible than its 6.06:1 resting state. Now ink (14.88:1).
* a11y: form validation errors were #ffb4b4 (1.36:1 on cream) and are now a new `--aurora-error-text` token, #8a1f1f (7.37:1).
* a11y: search and form submit labels were #041013 on the signal fill (2.56:1) and now use the control-label token (7.29:1).
* a11y: homepage work-card copy raised from 78% to 84% cream, so it clears 4.5:1 over the worst-case scrim (4.36:1 -> 4.78:1).
* tokens: `--aurora-signal-control-label` is now the single definition site for control label text; revive-port.css aliases it instead of repeating #fffaf6.
* cleanup: dropped dead pre-cream literals from `.aurora-meta-divider` and `.aurora-single-2026 .aurora-article-dek` (both lost the cascade, so neither was rendering).
* test: `scripts/tests/test_aurora_css_literal_contrast.py` now requires every hardcoded foreground colour in the front-end CSS to be registered with the surface it renders against and to clear its contrast floor.
* Note: section-head links ("Photography →", "Full index →") were already ink at 14.88:1 — see #470 for the corrected diagnosis.

= 1.4.4 =
* a11y: darken the accent orange to #9a2f14 so accent text clears 4.5:1 on every cream surface (was 2.69:1 on #d9cdb0).
* a11y: darken `Ink Muted` to #5c5044 (3.93:1 -> 4.96:1 on the darkest cream surface).
* a11y: primary control fill #c03f18 / hover #a52918 with #fffaf6 labels (was 4.09:1, now 5.11:1 / 6.91:1).
* a11y: restore the theme skip link to #aurora-main and suppress the duplicate core skip link.

= 1.4.3 =
* R5: full-bleed header shell so brand pins left of the viewport, not mid-column on ultrawide.
* R6: larger italic rainbow “message” word + riso gradient rule under homepage section heads.

= 1.4.2 =
* Fix leftover dark meta: `color-scheme: light` + cream `theme-color`.
* Preload Space Grotesk / DM Sans instead of unused Inter / Clash Display.

= 1.4.1 =
* Cream a11y polish: AA-safe accent text for kickers, visible focus rings on paper.
* Remove duplicate theme skip link (keep WordPress core `#wp-skip-link`).
* Tighter header nav tracking + horizontal scroll instead of awkward wrap.

= 1.4.0 =
* Port Revive cream/ink visual system into kk-aurora (Track B).
* Retokenize theme.json + style.css; Space Grotesk / DM Sans / JetBrains Mono.
* Rebuild sticky header (woven marquee, scroll progress), footer, and homepage section order.
* Global page CSS bridge so Track A packs inherit cream/ink.
* CTA remains Work with me → `/services/`; newsletter remains Beehiiv; no Field notes/Dispatch chrome labels.

= 1.3.41 =
* Primary CTA becomes "Work with me" → `/services/` (#422).
* Includes footer bento (#417/#449) and Wave 1 homepage theme fixes already on main.

= 1.3.40 =
* Render approved `jetpack_seo_html_title` values as exact singular document titles while preserving existing fallbacks (#357).

= 1.3.39 =
* Preserve the keynote-first homepage Open Graph title when the front-page object title is empty (#346).
* Give every Blog archive page a clean self-canonical and matching Open Graph URL (#347).

= 1.3.38 =
* Restore one standard search description from the existing Jetpack SEO fields and align social descriptions to the same source.

= 1.3.37 =
* Add direct Open Graph and Twitter Card metadata with a safe handoff from the temporary production snippet.

= 1.3.36 =
* Extended the homepage creative-lab contrast floor to customized FSE templates that still render the live section without the newer contrast class, using plain selectors for cache and audit compatibility.

= 1.3.34 =
* Added an opaque contrast floor for the homepage creative-lab feature band after the 1.3.33 pa11y closeout.

= 1.3.22 =
* Darkened Aurora primary CTA colors to meet WCAG AA contrast with off-white button text.

= 1.3.21 =
* Added late Twitter Card fallbacks so missing title, description, image, and site fields mirror available Open Graph metadata.

= 1.3.20 =
* Forced Writing archive Jetpack metadata overrides to late priority so archive Open Graph descriptions cannot inherit a post excerpt.

= 1.3.19 =
* Added Writing archive category feed discovery links and search accessibility regression coverage (PR #231).
* Aligned Writing archive Jetpack standard, Open Graph, and Twitter descriptions to the posts-page SEO description.

= 1.3.18 =
* Fixed stagger-reveal sections rendering invisible (found in visual QA).

= 1.3.17 =
* QA cleanup: un-chained stylesheets and pruned dead CSS/presets.

= 1.3.16 =
* Synthetic.ai restraint pass (PR #185): dialed back ambient red glow, added soft SVG film-grain overlay, increased section rhythm, self-hosted Inter + JetBrains Mono (Google Fonts removed).

= 1.3.15 =
* GSAP CDN removed; one-accent signal/wildcard color scheme refactor (PR #184).
* Self-hosted Clash Display; micro-interactions use native IntersectionObserver reveals.

= 1.3.14 =
* Global footer social links (PR #164).
* Aurora prose rhythm on generic pages (PR #166).

= 1.3.13 =
* Photography showcase gallery pattern (PR #162).
* Mobile QA pass and dead mobile-menu JS removal (PR #163).
* Shopify Buy Button pattern for Shop page (PR #159).

= 1.3.12 =
* Stabilized Article Map active-section tracking during mobile and scripted scroll.

= 1.3.11 =
* Wrapped long Article Modules bookmark/source-trail links at narrow widths.
* Softened the GSAP/ScrollTrigger boot guard so optimized script timing does not emit a false warning.

= 1.3.10 =
* Rebalanced single-post and writing-archive composition for a calmer premium editorial read.
* Added Article Modules patterns and styles for Short Version, Field Note, Source Trail, Pull Quote, callouts, bookmarks, and lead paragraphs.
* Replaced generic no-image blog fallbacks with varied CSS-generated editorial image plates.
* Softened article module surfaces, hover depth, reveal timing, card sheen, and featured-media glow.

= 1.0.0 =
* Initial release
