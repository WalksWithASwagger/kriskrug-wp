# WCAG 2.1 AA audit, kriskrug.co, 2026-08-02

**Issue:** [#46](https://github.com/WalksWithASwagger/kriskrug-wp/issues/46)
**Type:** read-only audit. No live writes, no theme deploy, no content edit was made in this pass.
**Live theme at audit time:** Aurora 1.5.7 (`curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i Version` returned `Version: 1.5.7`). Repo `main` is 1.5.8. Line numbers below point at repo `main` files; the failing declarations exist identically in the live 1.5.7 bundle unless noted.

## What was actually done

11 routes fetched read-only and audited. Every contrast number in this document came out of a real browser, not out of reading CSS. Method, in order of authority:

1. **Static markup pass.** BeautifulSoup over the fetched HTML for headings, landmarks, forms, link names, tabindex, ARIA, tables, duplicate ids, media.
2. **Computed-style pass.** Chrome for Testing 1234 via playwright-core at 1440x900. Walked every text node, read `getComputedStyle` colour, resolved the effective background by walking ancestors and compositing alpha layers, computed the ratio.
3. **Rendered-pixel pass.** For text sitting on photos, gradients or translucent panels, screenshot the element box, then force `color: transparent` and screenshot the same box again. Diff the two images, take the strongest-changed pixels as glyph cores, and compare glyph pixel against background pixel at the same coordinate. This is the only method that survives background images, `background-clip: text` and blend modes.
4. **Cascade forensics.** Chrome DevTools Protocol `CSS.getMatchedStylesForNode` to find which rule actually wins, including with `:focus` force-applied.

A first static-CSS cascade model was written and then **thrown away** because it got several answers wrong. It flagged the hero headline, hero dek and hero kicker as failures (they sit on a dark photograph and actually pass at 8 to 10:1), and it missed that the theme is wrapped in `@layer components`. Everything below is from methods 2 to 4.

## Route set

Each URL was status-checked with curl before auditing.

| Key | URL | Status |
|---|---|---|
| home | `/` | 200 |
| about | `/about/` | 200 |
| speaking | `/speaking/` | 200 |
| work | `/work/` | **200 direct, not a redirect** |
| services | `/services/` | 301 to `/generative-ai-services/` (200); audited at the target |
| events | `/events/` | 200 |
| testimonials | `/testimonials/` | 200 |
| glossary | `/glossary/` | 200 |
| blog | `/blog/` | 200 |
| contact | `/contact/` | 200 |
| post | `/2026/07/31/ai-lands-inside-every-profession/` | 200 |

Note on `/work/`: the issue brief said it redirects to `/recent-projects-include/`. It does not. `curl -sIL https://kriskrug.co/work/` returns a single `HTTP/2 200` with no `location` header. Whatever the routing was, it is not a redirect today.

`/contact/` was added because it is the conversion page. `/blog/` was added because it is the archive template.

## The one root cause behind most of this

`theme/kk-aurora/style.css:20-21` opens with:

```
@layer reset, tokens, base, primitives, components, patterns, utilities, overrides;
@layer components {
```

and `theme/kk-aurora/assets/css/revive-port.css:1` opens with `@layer components {`.

WordPress's `global-styles-inline-css` block is **unlayered** (verified live: it reports 0 `CSSLayerBlockRule` and 0 `CSSLayerStatementRule`). In the CSS cascade, unlayered normal declarations beat layered normal declarations no matter how specific the layered rule is. So every colour the theme sets on a heading or a link inside `@layer components` loses to theme.json presets.

Proof, from `CSS.getMatchedStylesForNode` on the live homepage:

- `.aurora-service-card h3` matches `.aurora-service-card h3 { color: var(--revive-surface) }` (cream, `#efe6d2`) but computes to `rgb(23, 19, 16)`, which is `--wp--preset--color--text-primary` from the unlayered `h1, h2, h3, h4, h5, h6` rule.
- `.aurora-button-primary` matches `.aurora-button-primary { color: var(--revive-accent-control-label) }` (`#fffaf6`) but computes to `rgb(154, 47, 20)`, which is `--wp--preset--color--signal` from the unlayered `a:where(:not(.wp-element-button))` rule.

Fixing the layer relationship fixes F1, F3 and F4 at once. Everything else is a separate dark-theme leftover.

## Findings

Ranked by users harmed times routes affected. Severity is my call, not a WCAG term.

| # | SC | Level | Sev | Routes | Element / selector | Measured | Fix | Lane |
|---|---|---|---|---|---|---|---|---|
| F1 | 1.4.3 Contrast (Minimum) | AA | Critical | `/`, `/about/`, `/events/`, `/testimonials/`, `/blog/` (17 buttons total) | `a.aurora-button.aurora-button-primary` outside header and footer | **1.42:1** (`#9a2f14` on `#c03f18`), need 4.5 | Make the theme's button label colour win. Either move theme CSS out of `@layer components`, or add an `@layer overrides` block that re-asserts `color: var(--revive-accent-control-label)` on `.aurora-button-primary` | B |
| F2 | 1.4.3 | AA | Critical | all 11 | `.aurora-footer-2026 .aurora-button-primary` | **2.88:1** (`rgba(23,19,16,.78)` on `#c03f18`), need 4.5 | `revive-port.css:996` is `.aurora-footer-2026 p, .aurora-footer-2026 a { color: var(--revive-ink-soft) !important }`. Exclude buttons: `:not(.aurora-button)` | B |
| F3 | 1.4.3 | AA | Critical | `/` | `.aurora-service-card h3` x3 ("Keynote", "Workshop", "Ecosystem") | **1.00:1** (`#171310` on `#171310`). The three service tier names are literally invisible. See `theme/kk-aurora/templates/front-page.html:125,132,139` for the markup | Same layer fix as F1. `revive-port.css:773-777` already sets the right colour, it just loses | B |
| F4 | 1.4.3 | AA | High | `/` | `.aurora-services-band .aurora-service-card a` x3 ("Work with me →") | **2.45:1** (`#9a2f14` on `#171310`), need 4.5 | Same layer fix. Band background is `revive-port.css:710` | B |
| F5 | 1.4.3 | AA | Critical | `/events/` | `.aurora-final-cta` whole band | h2 **1.08:1**, body p **1.06:1**, kicker **2.65:1**, secondary button **2.65:1**, primary button **1.42:1**. Text is `--aurora-ink` on `#07090b` | `style.css:1741-1747` still paints this band with the retired dark-theme background. Change `#07090b` to the paper or panel token, or set light text tokens for everything inside the band | B |
| F6 | 1.4.3 | AA | High | `/testimonials/` (19 cards) | `.aurora-quote-card` inside `.aurora-prose` | body **1.49:1**, cite **1.47:1**, cite link **1.53:1**. Card background composites to `rgb(57,57,60)` | `style.css:4215-4232` sets `background: ..., rgba(22, 24, 32, 0.84)` with `color: var(--aurora-ink)`. Dark-theme leftover. Also at `style.css:2855` | B |
| F7 | 1.4.3 | AA | High | `/glossary/` (2 callouts) | `.aurora-prose .wp-block-quote.is-style-callout-*` | body **1.49:1**, bold lead **1.53:1** | Same rule as F6 | B |
| F8 | 1.4.3 | AA | Medium | single-post template (verified on the 2026-07-31 post) | `.aurora-article-map summary` | **1.71:1** (`#171310` on `rgb(61,61,64)`) | `style.css:4090-4093` `background: ..., rgba(22, 24, 32, 0.82)`. Same leftover | B |
| F9 | 1.4.3 | AA | Medium | `/work/` (4 chips) | `span.aurora-card-label` | **1.25:1** (`#9a2f14` on `rgba(18,20,27,.76)` over the cream card, composites to `rgb(71,70,71)`) | `style.css:1271-1273`. Same leftover. Note the same class on `/events/` computes 7.62:1 because a different rule wins there, so fix the `/work/` context specifically | B |
| F10 | 1.2.2 Captions (Prerecorded) | **A** | High | post template | 2 YouTube iframes, `MB3YnobJcEU` and `T5ANAthZewE` | Both expose **only** `kind: asr` (auto-generated) caption tracks. Auto-captions do not satisfy 1.2.2 | Upload corrected caption files to the two YouTube videos, or publish a transcript on the post | A |
| F11 | 1.4.3 | AA | Medium | `/contact/` | `figcaption` | **3.75:1** (`--kk-muted: rgba(23,19,16,0.55)` on `--kk-card: #e6dcc2`), need 4.5. Same token on paper is 3.84:1 | Darken `--kk-muted` to about `rgba(23,19,16,0.68)` in the page's inline `<style>` block | A |
| F12 | 1.4.3 | AA | Medium | `/contact/` | `a.kk-contact-email` | **4.24:1** (`--kk-accent-text: #b53c18` on `#e6dcc2`), need 4.5. The same colour on paper is 4.67:1, so it passes on paper and fails on cards | Use `#9a2f14` (the theme signal, 5.51:1 on the card) or darken `--kk-accent-text` | A |
| F13 | 1.3.1 Info and Relationships | A | Low | all 11 | `<header class="wp-block-template-part">` wraps `<header class="aurora-header" role="banner">`; same nesting for footer | Two `banner` landmarks and two `contentinfo` landmarks per page. Screen reader landmark lists show duplicates | Either drop `role="banner"` / `role="contentinfo"` from the inner elements, or change the inner elements to `<div>`. `theme/kk-aurora/parts/header.html:2`, `parts/footer.html` | B |
| F14 | 3.2.4 Consistent Identification | AA | Low | `/work/` | 3 of 18 `target="_blank"` links carry no "opens in new tab" note: "Explore Both Hands Full", "Explore Punk Rock AI", "Explore Ethos and MADE ON" | The other 15 on the same page, and every external link on the other 10 routes, do carry the note | Add the same sr-only "(opens in new tab)" span used elsewhere | A |
| F15 | 2.2.2 Pause, Stop, Hide | A | Low | all 11 | `.aurora-woven-marquee-track`, `animation: aurora-woven-scroll 28s linear infinite` (`revive-port.css:238-243`) | Moves continuously, far past 5 seconds, in parallel with other content. It is `aria-hidden="true"` and decorative, and it is stopped under `prefers-reduced-motion: reduce` (`revive-port.css:257-261` plus the universal guard at `style.css:80-93`) | A media query is a mitigation, not the "mechanism" 2.2.2 asks for. Residual risk. Lowest priority here, but do not call it a pass | B |
| F16 | 1.1.1 Non-text Content | A | Trivial | all 11 | Facebook pixel `<img>` inside `<noscript>` with no `alt` attribute | 1 per page | Add `alt=""` | A |

### Contrast numbers, receipts

Computed with the WCAG 2.x relative-luminance formula. Translucent foregrounds and backgrounds are alpha-composited before the ratio, which is what the browser actually paints.

```
 1.00  FAIL  home services-band h3 titles     #171310 on #171310
 1.06  FAIL  events final-cta body p          rgba(23,19,16,.78) -> (19,17,15) on #07090b
 1.08  FAIL  events final-cta h2              #171310 on #07090b
 1.25  FAIL  work card-label chip             #9a2f14 on rgb(71,70,71)
 1.42  FAIL  primary button label             #9a2f14 on #c03f18
 1.47  FAIL  testimonials cite                #5c5044 on rgb(57,57,60)
 1.49  FAIL  testimonials / glossary quote    rgba(23,19,16,.78) -> (30,27,26) on rgb(57,57,60)
 1.53  FAIL  testimonials cite link           #9a2f14 on rgb(57,57,60)
 1.71  FAIL  post article-map summary         #171310 on rgb(61,61,64)
 2.45  FAIL  services-band CTA link           #9a2f14 on #171310
 2.65  FAIL  events final-cta kicker + ghost  #9a2f14 on #07090b
 2.88  FAIL  footer primary button label      rgba(23,19,16,.78) -> (60,29,18) on #c03f18
 3.75  FAIL  contact figcaption               rgba(23,19,16,.55) -> (116,109,96) on #e6dcc2
 4.24  FAIL  contact email link               #b53c18 on #e6dcc2
```

Rendered-pixel confirmations, glyph pixel against the background pixel underneath it:

```
 1.42  .aurora-hero-2026 .aurora-button-primary   glyph (153,47,20) vs bg (191,63,24)
 1.56  .wp-block-quote p (glossary)               glyph (31,28,28)  vs bg (58,61,70)
 1.61  .aurora-quote-card p (testimonials)        glyph (33,29,29)  vs bg (66,63,68)
 1.36  .aurora-quote-card cite                    glyph (148,48,22) vs bg (62,62,67)
```

### Things that look like failures and are not

Recorded so nobody re-files them.

- **Hero text on the portrait photo.** `h1#aurora-home-title` measures **8.5 to 10:1** against the actual photo pixels. `p.aurora-hero-dek` is **9.88:1**. `.aurora-hero-2026 .aurora-kicker` (gold `#e8b53a`) is **8.48:1**. `span.aurora-rainbow-word` uses `background-clip: text` with `color: transparent`, so `getComputedStyle` reports `rgba(0,0,0,0)`; measured at the pixel level it is **6.52:1**. All pass.
- **Skip link.** A first pass said the focused skip link stayed off-screen at y=-44. That was wrong. `.skip-link` has `transition: top 150ms` (`style.css:449`); the measurement was taken mid-transition. After the transition settles the link sits at **top: 16px, y=16, fully in view**, `#fffaf6` on `#c03f18` at **5.11:1** with a 2px `#171310` outline. Verified with a screenshot on `/` and `/blog/`. SC 2.4.1 and 2.4.7 both pass here.
- **`.aurora-card-label` on `/events/`.** 74 instances, all **7.62:1**. Different rule wins there.
- **Blog category chips.** `.aurora-writing-card-category a` measures **4.97:1** on the card. Pass.
- **Focus ring token.** `--focus-ring` outer stop `#d94a1f` is **3.42:1** on the paper, and the actual applied outline is `2px solid #9a2f14` at **6.06:1** on paper and **5.51:1** on cards. Passes SC 1.4.11.
- **Marquee overflow at 320px.** The only element wider than the viewport at 320px is the decorative `aria-hidden` marquee track. It does not cause document horizontal scroll.

## What passed

Verified, not assumed.

| SC | Level | Result |
|---|---|---|
| 1.3.1 heading structure | A | Every one of the 11 routes has **exactly one h1** and **zero skipped heading levels**. Sequences checked programmatically |
| 1.3.1 tables | A | No `<table>` on any audited route |
| 1.4.4 Resize text | AA | No horizontal scroll at 640px CSS width, which is 200% of a 1280px layout. Checked on `/`, `/events/`, post |
| 1.4.10 Reflow | AA | No document horizontal scroll at 320px on any of the 11 routes. `document.scrollWidth === clientWidth === 320` everywhere |
| 1.4.11 Non-text Contrast | AA | Focus indicator 6.06:1. See caveat below on decorative borders |
| 1.4.12 Text Spacing | AA | Applied the WCAG spacing overrides (line-height 1.5, letter-spacing .12em, word-spacing .16em, paragraph margin 2em). Page height grows, no horizontal scroll, no content clipped except `.sr-only` spans which are clipped by design |
| 2.1.1 Keyboard | A | 28-stop tab pass on `/` and the post. Logical DOM order, no traps encountered, no positive `tabindex` anywhere on any route |
| 2.4.1 Bypass Blocks | A | One skip link, target `#aurora-main` exists on all 11 routes, core's duplicate skip link is suppressed |
| 2.4.2 Page Titled | A | Unique `<title>` on all routes |
| 2.4.3 Focus Order | A | Matches visual order on the two routes tested |
| 2.4.4 Link Purpose | A | **Zero** links with an empty accessible name across all 11 routes. **Zero** generic "read more" / "click here" link text. Image links get their name from `alt` (11 on `/`, 18 on `/blog/`), all descriptive |
| 2.4.7 Focus Visible | AA | Every focusable gets `outline: 2px solid #9a2f14`. No `outline: none` without a replacement |
| 3.1.1 Language of Page | A | `<html lang="en-US">` on all 11 |
| 3.2.3 Consistent Navigation | AA | Same primary nav, same order, all routes |
| 4.1.2 Name, Role, Value | A | Zero unnamed interactive elements. Both post iframes carry a `title`. All 5 `<nav>` elements per page carry distinct `aria-label` values ("Primary navigation", "Projects", "Site", "Utility", "Elsewhere", plus "Article sections" on posts) |
| 3.3.x form criteria | A/AA | **Not applicable.** Zero `<form>` elements on any of the 11 routes. `/contact/` is `mailto:` based, the newsletter signup is an off-site beehiiv link |

## What I could not assess without a screen reader or more time

Listing these so the gap is visible instead of implied as a pass.

- **1.2.3 / 1.2.5 Audio Description.** Both post videos are talking-head meetup recordings, so the visual channel probably adds little, but I did not watch them. Needs a human call.
- **1.2.1 Audio-only and Video-only.** Not surveyed beyond the one post.
- **1.3.2 Meaningful Sequence** and **1.3.3 Sensory Characteristics.** Need a screen reader read-through, not markup inspection.
- **1.4.13 Content on Hover or Focus.** No tooltip patterns found in markup, but hover-triggered CSS exists on cards. Not driven with a pointer.
- **2.1.2 No Keyboard Trap.** No trap hit in a 28-stop pass, but there are no modals or embedded widgets on the audited routes to stress. The YouTube iframes were not entered.
- **2.4.5 Multiple Ways.** Nav plus blog archive plus glossary exist. Whether a site search is reachable was not confirmed; no search form was found in the markup of any audited route.
- **2.4.6 Headings and Labels.** Headings are structurally correct. Whether each one is descriptive is an editorial judgement I did not make.
- **3.1.2 Language of Parts.** No `lang` attribute appears on any element other than `<html>`. If any published post quotes a non-English passage of any length, that is an uncaught A-level failure. Not surveyed across the full post archive.
- **3.2.1 On Focus** and **3.2.2 On Input.** No forms, so 3.2.2 is close to moot, but focus-triggered context change was not systematically driven.
- **4.1.3 Status Messages.** No `aria-live` regions exist anywhere. There is also no dynamic status content on the audited routes, so this is probably vacuous rather than failing.
- **Coverage.** 11 routes, not 100% of public pages. `/photography/` and the individual project and post pages beyond the one sampled were not audited. The findings that live in the theme (F1 through F9, F13, F15) apply everywhere the theme renders; the content findings (F10 through F12, F14, F16) are route-specific and other pages may carry their own.
- **Assistive technology.** No VoiceOver, NVDA or JAWS pass was run. No axe or pa11y run either; the tooling here is hand-rolled. The last automated `pa11y --standard WCAG2AA` evidence on this repo is from 2026-07-02 in issue [#289](https://github.com/WalksWithASwagger/kriskrug-wp/issues/289).
- **Forced colors / Windows High Contrast.** Not tested. The global `:focus-visible` rule at `style.css:129-131` uses `box-shadow` for its ring, and `box-shadow` is dropped in forced-colors mode. The per-component `outline` rule at `style.css:627-631` covers this in practice, but it was not verified in forced-colors.

Also not a WCAG 2.1 criterion but worth knowing: WCAG 2.2 adds **2.4.11 Focus Not Obscured** and **2.5.8 Target Size (Minimum, 24px)**. The sticky header is 80px tall and does not offset anchor targets, which is a 2.4.11 risk if you ever move to 2.2. The mobile nav pills are set to `min-height: 44px` (`style.css:3431`), which is fine.

## Remediation plan

### Track B, theme, one PR

All of these are `theme/kk-aurora/` edits. They ship together behind the #601 pixel gate and need KK approval plus a deploy.

1. **Fix the cascade layer relationship.** This is the highest-leverage change and it needs the most care, because it will move colours site-wide. Two options:
   - Narrow option, lower blast radius: add an `@layer overrides { ... }` block (the layer is already declared at `style.css:20`) that re-asserts the button label colour and the service-card heading colour. Layered still loses to unlayered, so this alone is **not enough**; it would need `!important` on those specific declarations.
   - Correct option: stop wrapping theme CSS in `@layer components`, or dequeue / neutralise the conflicting `global-styles` declarations for `a` and `h1-h6`. This is the real fix and it must be pixel-gated across all 11 routes.
   Closes F1, F3, F4.
2. **`revive-port.css:996`**: change `.aurora-footer-2026 p, .aurora-footer-2026 a` to `.aurora-footer-2026 p, .aurora-footer-2026 a:not(.aurora-button)`. Closes F2.
3. **`style.css:1741-1747`**: replace the `#07090b` band background, or add light text tokens for `.aurora-final-cta h2 / p / .aurora-kicker / .aurora-button-secondary`. Closes F5.
4. **`style.css:4215-4232` and `style.css:2855`**: replace `rgba(22, 24, 32, 0.84)` with a paper-era panel colour. Closes F6 and F7.
5. **`style.css:4090-4093`**: same treatment for `rgba(22, 24, 32, 0.82)`. Closes F8. Line 4340 carries the same value and should be checked in the same pass.
6. **`style.css:1271-1273`**: same treatment for `rgba(18, 20, 27, 0.76)`. Closes F9.
7. **`parts/header.html:2` and `parts/footer.html`**: remove the duplicate landmark. Closes F13.
8. Optional, F15: add a pause control to the marquee, or accept the residual risk in writing.

**Suggested sweep before shipping:** grep the theme for the remaining dark-theme leftovers. `rgba(22, 24, 32,`, `rgba(18, 20, 27,`, `#07090b`, `#050708`, `rgba(9, 12, 17,`, `rgba(14, 17, 23,`, `rgba(3, 4, 5,` all still appear as backgrounds under light-theme text. Only the ones on live-rendered elements were confirmed failing; the rest are latent and will surface the moment those components get used.

**Verification gate:** re-run the rendered-pixel measurement on all 11 routes after deploy. A finding is closed when the glyph-versus-background ratio at 1440x900 is at or above 4.5 for body text and 3.0 for large text.

### Track A, content, separate PRs

9. `/contact/` page inline `<style>`: darken `--kk-muted` and `--kk-accent-text`. Closes F11 and F12. Note `/generative-ai-services/` carries the same token block; check it in the same edit even though no failure surfaced there in this pass.
10. `/work/`: add the "(opens in new tab)" sr-only span to the three "Explore ..." links. Closes F14.
11. Post `2026/07/31/ai-lands-inside-every-profession/`: get real captions onto the two YouTube videos, or publish transcripts. Closes F10. This one is Level A and is the only Level A content failure found.
12. Facebook pixel `<img>`: add `alt=""`. Closes F16. This is injected by the tracking snippet, not by post content.

### Not in this document

Image alt text inventory is [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4) and is owned by a separate lane. What this audit can add to it: across the 11 routes, **every content image carries an alt attribute**. The only `<img>` without one is the Facebook tracking pixel (F16), and there is exactly one `alt=""` on the audited post. No filename-shaped alt text was found. So the remaining `#4` work is alt text *quality*, not alt text *presence*, at least on these routes.

## Acceptance criteria from #46, marked honestly

- [ ] **Audit covers 100% of public pages.** No. 11 routes. Theme-level findings generalise, content findings do not.
- [x] **All WCAG 2.1 AA criteria evaluated.** Every AA criterion was either tested, marked not applicable with a reason, or listed under "could not assess". Nothing was silently skipped.
- [ ] **Automated + manual testing complete.** Automated browser measurement: yes, and more rigorous than axe for contrast. Manual assistive-technology testing: no.
- [x] **Critical issues prioritised.** Ranked by users harmed times routes affected.
- [x] **Remediation roadmap created.** Above, split by lane, with file and line references.
- [x] **Report deliverables complete.** This document.
- [ ] **Audit by accessibility specialist.** No. This is an agent audit. If legal exposure is the driver, a certified human audit is still required, and this document is a useful input to it rather than a substitute.

## Related, already closed

- [#289](https://github.com/WalksWithASwagger/kriskrug-wp/issues/289) WCAG smoke on core routes, closed 2026-07-02
- [#293](https://github.com/WalksWithASwagger/kriskrug-wp/issues/293) Aurora opal contrast failures, closed
- [#294](https://github.com/WalksWithASwagger/kriskrug-wp/issues/294) header brand accessible name, closed

F1 through F9 are all regressions or leftovers from the dark-to-paper theme flip that happened after those issues closed. #293 fixed the opal palette; it did not catch the panel backgrounds that stayed dark underneath light text, and it predates the `@layer` wrapper.
