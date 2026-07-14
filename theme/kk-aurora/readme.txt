=== KK Aurora ===
Contributors: kriskrug
Requires at least: 6.4
Tested up to: 6.9
Requires PHP: 8.0
License: GPLv2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html

== Description ==

KK Aurora is a cyberpunk-inspired WordPress theme featuring flowing gradients, deep space aesthetics, and purposeful motion design.

Built for Full Site Editing with WCAG 2.1 AA accessibility.

== Features ==

* Full Site Editing (FSE) block theme
* Dark mode by default
* Animated gradient accents
* CSS/JS scroll reveals (no GSAP dependency on main; GSAP removed in 1.3.15)
* High contrast accessibility
* Mobile-first responsive design
* Custom block patterns

== Installation ==

1. Upload the theme folder to `/wp-content/themes/`
2. Activate the theme through the 'Themes' menu in WordPress
3. Start customizing with the Site Editor

== Color Palette ==

* Deep Space: #0D0D12 (primary background)
* Surface: #12121A (cards, elevated surfaces)
* Cyan: #00E5FF (primary accent)
* Teal: #00BFA5 (secondary accent)
* Purple: #8B5CF6 (tertiary accent)
* Pink: #EC4899 (highlights)

== Changelog ==

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
