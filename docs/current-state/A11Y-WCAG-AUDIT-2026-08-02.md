# WCAG 2.1 AA audit, kriskrug.co, 2026-08-02

**Issue:** [#46](https://github.com/WalksWithASwagger/kriskrug-wp/issues/46)
**Type:** read-only audit. No live writes, no theme deploy, no content edit was made in this pass.
**Live theme at audit time:** Aurora 1.5.7 (`curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i Version` returned `Version: 1.5.7`). Repo `main` is 1.5.8. Line numbers below point at repo `main` files; the failing declarations exist identically in the live 1.5.7 bundle unless noted.

**Revision 2026-08-03:** corrected after an adversarial verification pass. Eleven defects were raised against revision 1. Ten are corrected in place and one is rebutted with evidence. The changes are: a real 50-criterion enumeration replacing a false "nothing was silently skipped" claim, three added findings, a disclosed overlap with two earlier in-repo reports, and four corrected figures. The disposition of every charge is on PR [#659](https://github.com/WalksWithASwagger/kriskrug-wp/pull/659).

## Headline: one CSS cascade bug produces the worst failures on the site

Every theme stylesheet is wrapped in `@layer components`. WordPress's `global-styles-inline-css` is unlayered. In the CSS cascade an unlayered normal declaration beats a layered normal declaration at any specificity, so the theme loses control of every heading and link colour to theme.json presets.

Measured live on `https://kriskrug.co/` at 1440x900, re-confirmed 2026-08-03:

- `.aurora-service-card h3` renders `rgb(23,19,16)` on a `rgb(23,19,16)` band. **1.00:1.** The three homepage service tier names ("Keynote", "Workshop", "Ecosystem") are invisible. Not low contrast, invisible.
- `.aurora-button-primary` renders `rgb(154,47,20)` on `rgb(192,63,24)`. **1.42:1**, against a 4.5 requirement.

CDP `CSS.getMatchedStylesForNode` on that h3 returns the winning rule directly:

```
.aurora-theme :where(h1,h2,h3,h4,h5,h6)  color:var(--revive-ink)                  layer=components
.aurora-service-card h3                  color:var(--revive-surface)              layer=components
h1, h2, h3, h4, h5, h6                   color:var(--wp--preset--color--text-primary)  layer=(unlayered)   <-- wins
```

Detail and the two fix options are in [the root cause section](#the-one-root-cause-behind-most-of-this).

## What was actually done

11 routes fetched read-only and audited. Every contrast number in this document came out of a real browser, not out of reading CSS. Method, in order of authority:

1. **Static markup pass.** BeautifulSoup over the fetched HTML for headings, landmarks, forms, link names, tabindex, ARIA, tables, duplicate ids, media.
2. **Computed-style pass.** Google Chrome for Testing **151.0.7922.34** via `playwright-core` at 1440x900. Walked every text node, read `getComputedStyle` colour, resolved the effective background by walking ancestors and compositing alpha layers, computed the ratio. Revision 1 of this document wrote the browser as "Chrome for Testing 1234". `1234` is the Playwright browser build revision (the directory is `~/Library/Caches/ms-playwright/chromium-1234`), not a Chrome version, and it read as one. The version string above is what `"$HOME/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" --version` prints.
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

One route was checked and is not in the table because it does not exist: **`/accessibility/` returns HTTP 404**. `curl -sI https://kriskrug.co/accessibility/` on 2026-08-03 returned `HTTP/2 404`. There is no public accessibility statement. The 2026-07-26 report already flagged this under [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288) / [#48](https://github.com/WalksWithASwagger/kriskrug-wp/issues/48); revision 1 of this document dropped it. It is not a WCAG 2.1 success criterion, but it is the first thing a regulator or a disabled user looks for, and it stays open.

## Prior evidence in this repo, and what is actually new here

Revision 1 said: "The last automated `pa11y --standard WCAG2AA` evidence on this repo is from 2026-07-02 in issue #289." That was wrong. Two later pa11y runs are committed here:

| Report | Date | Scope | Result |
|---|---|---|---|
| [`reports/issue-46-pa11y-five-routes-20260716.md`](reports/issue-46-pa11y-five-routes-20260716.md) | 2026-07-16 | `/`, `/about/`, `/blog/`, `/work/`, `/contact/` on live 1.3.37 | 0 pa11y issues on all five |
| [`reports/wcag-smoke-audit-20260726.md`](reports/wcag-smoke-audit-20260726.md) | 2026-07-26 | 7 routes plus `/accessibility/` on live 1.4.8 | 2 live contrast failures, alt and statement gaps |

Both are `npx pa11y --standard WCAG2AA`. Neither was cited in revision 1. The 2026-07-16 run reporting zero issues on `/` and `/contact/` while the 2026-07-26 run reports failures on both is itself worth knowing: pa11y's verdict on this site is not stable across theme versions, which is part of why this pass measured in-browser instead.

### Overlap with the 2026-07-26 report, stated plainly

Revision 1 presented 16 findings without disclosing that the 2026-07-26 smoke had already recorded several of them a week earlier. Corrected split:

| # | Status vs 2026-07-26 | Note |
|---|---|---|
| F12 contact email 4.24:1 | **RECONFIRMED** | Byte-identical, ratio included. That report's S0 #2 reads "Contact `.kk-contact-email` `#b53c18` on card `#e6dcc2` \| **4.24:1** \| **fail**" |
| F16 Facebook pixel missing `alt` | **RECONFIRMED** | That report's S2 #6, same wording, "every page" |
| F19 services-band kickers 2.45:1 | **RECONFIRMED**, cause changed | See below |
| F1 to F11, F13 to F15, F17, F18 | **NEW** | Not present in either prior report |

Four "passes" that revision 1 presented as fresh verification were also already established on 2026-07-26: one `h1` per route, `lang="en-US"`, the core duplicate skip link suppressed in `functions.php`, and form-label criteria being N/A because there are no forms. They are re-verified here on 11 routes instead of 7, but they are re-verification, not discovery.

**Honest headline count: 19 findings, of which 16 are new to this pass and 3 reconfirm the 2026-07-26 report.** Revision 1 said "16 findings" with no split, which overstated the delta on the 3 and understated the total by leaving out F17, F18 and F19.

### The services-band overlap is not what it looks like

The 2026-07-26 report failed the services-band roman-numeral kickers ("I.", "II.", "III.") at **2.45:1**, and attributed it to `revive-port.css:733` `.aurora-services-band .aurora-kicker { color: rgba(239, 230, 210, 0.55) !important }`.

F4 in this document is a **different element** at the same ratio in the same band: `.aurora-services-band .aurora-service-card a` ("Work with me"), `#9a2f14` on `#171310`, also 2.45:1. Same ratio, different colour, different element.

Measuring the kickers again on 2026-08-03 found something revision 1 missed entirely. They are **still failing, and the recorded cause is now stale**:

- Live computed colour of `.aurora-services-band .aurora-kicker` is `rgb(154, 47, 20)`, not `rgba(239,230,210,0.55)`. On the `rgb(23,19,16)` band that is **2.45:1**.
- `revive-port.css:732-734` still declares the cream `0.55` value with `!important`, but it loses to a later, higher-specificity important rule in the same layer: `revive-port.css:1242-1245` `body.aurora-theme #aurora-main :where(.aurora-kicker, .aurora-section-kicker) { color: var(--revive-accent-text) !important }`, and `--revive-accent-text` is `#9a2f14` (`revive-port.css:22`).
- So anyone who fixes the line the 2026-07-26 report names will change nothing on screen.

That is recorded below as **F19**. Fixing the cream rule alone will not close it.

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

Nineteen findings, ranked by users harmed times routes affected. Severity is my call, not a WCAG term. F17, F18 and F19 were added in revision 2; F12, F16 and F19 reconfirm the 2026-07-26 report rather than discovering anything.

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
| F17 | 1.4.1 Use of Color | **A** | High | every route with prose (`/glossary/`, `/about/`, post, and all posts) | `.aurora-prose p a` and equivalent in-body links | Resting state is **colour only**: `text-decoration: none`, `border-bottom: 0px`, `font-weight: 400`, identical to the paragraph around it. Link `#9a2f14` versus composited body text `rgb(71,65,59)` is **1.34:1**. Technique G183 permits colour-only links only at **3:1 or better** against the surrounding text | Give resting in-body links a non-colour cue. An underline is the direct fix; a bottom border or a weight bump also works. Hover and focus already add `text-decoration: underline`, so only the resting state is failing | B |
| F18 | 4.1.1 Parsing | A | Trivial | `/`, `/blog/` | Two `<link rel="stylesheet">` in `<head>` share `id="all-css-81648fd3816053fb325b5707e2918c23"` | Duplicate `id` on 2 of 11 routes. Emitted by Jetpack Boost's critical-CSS pair (`.../boost-cache/static/ec2a031717.min.css`), once with `media="all"` and once with `media="not all"` plus an `onload` swap | Plugin-side. No assistive technology references these ids, so real-world impact is close to zero, and WCAG 2.2 removed 4.1.1 entirely. Recorded for completeness because 4.1.1 is normative in WCAG 2.1 | B |
| F19 | 1.4.3 | AA | High | `/` | `.aurora-services-band .aurora-kicker` x3 ("I.", "II.", "III.") | **2.45:1** (`#9a2f14` on `#171310`). **Reconfirms** the 2026-07-26 report's S0 #1, but the colour has changed since then and the cause recorded there is now stale | The winning rule is `revive-port.css:1242-1245`, not the `revive-port.css:732-734` cream rule that report names. Either exempt the dark band from the `#aurora-main` kicker override or give the band its own light kicker token | B |

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

Added in revision 2, measured 2026-08-03 on the live site:

```
 2.45  FAIL  services-band roman kickers (F19)  #9a2f14 on #171310
 1.34  FAIL  in-prose link vs body text  (F17)  #9a2f14 vs rgba(23,19,16,.78) -> (71,65,59)
                                                this is the 1.4.1 differentiation ratio, not a 1.4.3 ratio
```

For F17 the link itself is legible: `#9a2f14` on the `#efe6d2` paper is **6.06:1**, so 1.4.3 passes. The failure is that nothing except hue tells you it is a link.

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
| 4.1.2 Name, Role, Value | A | Zero unnamed interactive elements. Both post iframes carry a `title`. **Every `<nav>` on every route carries a distinct `aria-label`**, with zero duplicate labels on any route. Revision 1 said "all 5 `<nav>` elements per page", which is wrong on 2 of 11 routes: 9 routes have 5 navs, `/blog/` has **7** (adds "Pagination" and "Category RSS feeds") and the post has **6** (adds "Article sections"). The count was wrong, the verdict is not |
| 2.5.3 Label in Name | A | **Passes, with a usability caveat.** See the dedicated section below |
| 3.3.1, 3.3.2, 3.3.3, 3.3.4 form criteria | A/AA | **Not applicable.** Zero `<form>` elements on any of the 11 routes. `/contact/` is `mailto:` based, the newsletter signup is an off-site beehiiv link. There is also nothing on the site that creates a legal or financial commitment, which is the second half of 3.3.4 |

### 2.5.3 Label in Name, evaluated properly

Revision 1 never evaluated 2.5.3, and it should have, because its own F14 evidence sits on top of the exact pattern the criterion governs: `/work/` has four card anchors carrying an `aria-label` that overrides their visible content.

Measured on the live `/work/` HTML:

| `aria-label` (accessible name) | Visible heading inside the link | Heading contained in name? |
|---|---|---|
| `Explore Both Hands Full` | "Both Hands Full" | yes |
| `Explore Punk Rock AI` | "Punk Rock AI" | yes |
| `Explore Ethos and MADE ON` | "Ethos and MADE ON" | yes |
| `Explore the photography archive` | "Photography archive" | yes (case-insensitive) |

**Verdict: not a 2.5.3 failure.** The normative failure technique is F96, "the accessible name does not contain the visible label text". In all four cases it does. A speech-input user saying the card heading gets a substring match.

Two things are still worth writing down:

1. **Best practice is not met.** WCAG advises putting the visible label at the *start* of the accessible name. These prefix it with "Explore" (and "the" on the fourth). Any voice-control implementation that anchors at the start of the name rather than doing substring matching will miss all four.
2. **Automated tools will flag these.** axe-core's `label-content-name-mismatch` rule compares the accessible name against the element's whole visible subtree text, not just the heading. The whole subtree here is "Keynote portal Both Hands Full A keynote, album, and operating metaphor for staying human while the tools get faster", which is obviously not contained in "Explore Both Hands Full". Anyone who runs axe on `/work/` will get four serious 2.5.3 hits. They are false positives against the normative text of the criterion, but they will cost somebody an afternoon, so: recorded here, not filed as a finding.

The cheap change that resolves both is to drop the `aria-label` entirely and let the links take their name from content, or to reword it as "Both Hands Full, explore". No finding filed.

These four anchors are the only elements on any of the 11 routes where an `aria-label` overrides visible text. Verified by walking every `a`, `button`, `input`, `select`, `textarea` and `summary` on all 11 fetched documents.

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
- **Coverage.** 11 routes, not 100% of public pages. `/photography/` and the individual project and post pages beyond the one sampled were not audited. The findings that live in the theme (F1 through F9, F13, F15, F17, F19) apply everywhere the theme renders, and F17 in particular applies to **every post on the site**, not just the one sampled. The content findings (F10 through F12, F14, F16) are route-specific and other pages may carry their own. F18 is plugin-emitted and appears wherever Jetpack Boost serves its critical-CSS pair.
- **Assistive technology.** No VoiceOver, NVDA or JAWS pass was run. No axe or pa11y run in this pass either; the tooling here is hand-rolled. The most recent committed `pa11y --standard WCAG2AA` evidence in this repo is **2026-07-26**, in `docs/current-state/reports/wcag-smoke-audit-20260726.md`, with a **2026-07-16** five-route run in `docs/current-state/reports/issue-46-pa11y-five-routes-20260716.md` before it. Revision 1 of this document said the last such evidence was 2026-07-02 in issue [#289](https://github.com/WalksWithASwagger/kriskrug-wp/issues/289), which skipped both. Running axe or pa11y over these 11 routes remains worth doing, if only to see how much a rule-based tool catches versus the in-browser measurement used here.
- **Forced colors / Windows High Contrast.** Not tested. The global `:focus-visible` rule at `style.css:129-131` uses `box-shadow` for its ring, and `box-shadow` is dropped in forced-colors mode. The per-component `outline` rule at `style.css:627-631` covers this in practice, but it was not verified in forced-colors.

Also not a WCAG 2.1 criterion but worth knowing: WCAG 2.2 adds **2.4.11 Focus Not Obscured** and **2.5.8 Target Size (Minimum, 24px)**.

Revision 1 asserted here that "the sticky header is 80px tall and does not offset anchor targets", with no receipt behind either half. Both halves are wrong. Measured at 1440x900 on `/` and on the post:

- The header is **76.2px**, not 80. There is no 80px literal or header-height token anywhere in `theme/kk-aurora/style.css` or `assets/css/revive-port.css`.
- It is declared `position: sticky; top: 0` (`style.css:692`) but **it does not actually stay pinned**. Its parent is `<header class="wp-block-template-part">`, which is exactly 76.2px tall, so the sticky containment block gives it zero travel. Scrolling to y=1500 puts the header's `top` at **-1457**: it scrolls away with the page. This is the same duplicated template-part wrapper that F13 reports as a landmark problem, now with a second consequence.
- Anchor targets **are** offset, at least in prose. `.aurora-prose :where(h2, h3, h4)` carries `scroll-margin-top: 7rem` (`style.css:2828`), which resolves to **112px**. Clicking the three article-map links on the 2026-07-31 post lands each `h2` well clear of the header. `scroll-padding-top` on the root is `auto`, i.e. unset, so headings outside `.aurora-prose` have no such offset.

So there is no 2.4.11 exposure today, for the accidental reason that the sticky header does not work. If someone fixes the template-part nesting for F13 the header may start behaving as designed, and 2.4.11 becomes live at that moment. Note it in the F13 fix.

The mobile nav pills are set to `min-height: 44px` (`style.css:3431`), which is fine for 2.5.8.

## All 50 WCAG 2.1 A and AA success criteria, one row each

Revision 1 claimed "Every AA criterion was either tested, marked not applicable with a reason, or listed under 'could not assess'. Nothing was silently skipped." **That was false.** Grepping the 50 SC numbers against revision 1 found **18 that never appear in the document at all**: 1.4.1, 1.4.2, 2.1.4, 2.2.1, 2.3.1, 2.5.1, 2.5.2, 2.5.3, 2.5.4, 3.3.1, 3.3.2, 4.1.1 at Level A, and 1.2.4, 1.3.4, 1.3.5, 1.4.5, 3.3.3, 3.3.4 at Level AA. Four of those (the 3.3.x set) were covered by a generic "3.3.x not applicable" line, so **14 criteria were genuinely skipped in silence**.

WCAG 2.1 has 30 Level A and 20 Level AA criteria. Here are all 50. Rows marked "new in rev 2" were tested for this correction pass.

### Level A (30)

| SC | Name | Disposition | Basis |
|---|---|---|---|
| 1.1.1 | Non-text Content | **FAIL** | F16, Facebook pixel `<img>` with no `alt`. Every content image on all 11 routes has an alt |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | could not assess | Only one post surveyed; the archive was not |
| 1.2.2 | Captions (Prerecorded) | **FAIL** | F10, both post YouTube embeds expose only `kind: asr` tracks |
| 1.2.3 | Audio Description or Media Alternative | could not assess | Did not watch the two videos |
| 1.3.1 | Info and Relationships | **FAIL** | F13, duplicate banner and contentinfo landmarks. Headings and tables pass |
| 1.3.2 | Meaningful Sequence | could not assess | Needs a screen reader read-through |
| 1.3.3 | Sensory Characteristics | could not assess | Needs a screen reader read-through |
| 1.4.1 | Use of Color | **FAIL** | F17, in-prose links are colour-only at 1.34:1 against body text. New in rev 2 |
| 1.4.2 | Audio Control | not applicable | Zero `<audio>` and `<video>` elements and zero `autoplay=1` iframes across all 11 routes. New in rev 2 |
| 2.1.1 | Keyboard | pass | 28-stop tab pass on `/` and the post, no positive `tabindex` anywhere |
| 2.1.2 | No Keyboard Trap | could not assess | No trap hit, but no modals or widgets exist to stress; YouTube iframes not entered |
| 2.1.4 | Character Key Shortcuts | pass | The only `keydown` handler in the theme is `theme.js:22`, arrow/Home/End roving focus scoped to `.aurora-primary-nav`. Those are not character keys, and it is not a global shortcut. Zero `accesskey` attributes on any route. New in rev 2 |
| 2.2.1 | Timing Adjustable | not applicable | No `<meta http-equiv="refresh">` on any route, no session, no time limit anywhere. New in rev 2 |
| 2.2.2 | Pause, Stop, Hide | **residual risk** | F15, 28s marquee, decorative and `aria-hidden`, stopped only under `prefers-reduced-motion` |
| 2.3.1 | Three Flashes or Below Threshold | pass | No `<blink>` or `<marquee>` elements. The one animation is a linear `translate` scroll, not a luminance flash. New in rev 2 |
| 2.4.1 | Bypass Blocks | pass | Skip link present, `#aurora-main` target exists on all 11 |
| 2.4.2 | Page Titled | pass | Unique `<title>` on all 11 |
| 2.4.3 | Focus Order | pass | Matches visual order on the two routes driven |
| 2.4.4 | Link Purpose (In Context) | pass | Zero empty accessible names, zero generic link text across all 11 |
| 2.5.1 | Pointer Gestures | not applicable | No path-based or multipoint gestures. Zero `touchstart`, `pointerdown` or `gesturestart` handlers in the theme JS or in the live 21KB minified bundle. New in rev 2 |
| 2.5.2 | Pointer Cancellation | pass | No down-event activation anywhere. Zero `mousedown` and `pointerdown` handlers; every control is a native anchor or button. New in rev 2 |
| 2.5.3 | Label in Name | pass, caveat | See the dedicated section above. Four `/work/` cards prefix the visible heading rather than omitting it. New in rev 2 |
| 2.5.4 | Motion Actuation | not applicable | Zero `devicemotion` and `deviceorientation` listeners in the theme JS or the live bundle. New in rev 2 |
| 3.1.1 | Language of Page | pass | `<html lang="en-US">` on all 11 |
| 3.2.1 | On Focus | could not assess | Focus-triggered context change was not systematically driven |
| 3.2.2 | On Input | not applicable | No form controls exist |
| 3.3.1 | Error Identification | not applicable | Zero `<form>` elements on any of the 11 routes |
| 3.3.2 | Labels or Instructions | not applicable | Zero form controls |
| 4.1.1 | Parsing | **FAIL** | F18, duplicate `id` on `/` and `/blog/`. Trivial impact, and WCAG 2.2 removed this criterion. New in rev 2 |
| 4.1.2 | Name, Role, Value | pass | Zero unnamed interactive elements, every `<nav>` distinctly labelled, both iframes titled |

### Level AA (20)

| SC | Name | Disposition | Basis |
|---|---|---|---|
| 1.2.4 | Captions (Live) | not applicable | No live or streaming media on any route. New in rev 2 |
| 1.2.5 | Audio Description (Prerecorded) | could not assess | Same gap as 1.2.3 |
| 1.3.4 | Orientation | pass | No orientation media query hides content and no orientation lock exists; the layout reflows in both. New in rev 2 |
| 1.3.5 | Identify Input Purpose | not applicable | No `<input>` fields, so there is nothing to autocomplete. New in rev 2 |
| 1.4.3 | Contrast (Minimum) | **FAIL** | F1 to F9, F11, F12, F19. Twelve of the 19 findings |
| 1.4.4 | Resize text | pass | No horizontal scroll at 640px CSS width; viewport meta sets no `maximum-scale` or `user-scalable=no` |
| 1.4.5 | Images of Text | **could not assess** | Needs a human to look at the images. The wordmark `kriskrug-wordmark.png` is a logotype and is exempt. The real candidates are `/events/` share and promo graphics with alt text like "Panelist social graphic for Brands for Better Foundation How Can We Help pitch night" and "Vancouver AI Meetup #30", plus the `/work/` "MADE ON double silver graphic". Event posters usually carry dates, names and times as baked-in pixels. New in rev 2 |
| 1.4.10 | Reflow | pass | `document.scrollWidth === clientWidth === 320` on all 11 |
| 1.4.11 | Non-text Contrast | pass | Focus indicator 6.06:1 |
| 1.4.12 | Text Spacing | pass | WCAG spacing overrides applied, no content loss |
| 1.4.13 | Content on Hover or Focus | could not assess | Hover CSS exists on cards, not driven with a pointer for dismiss/hover/persist |
| 2.4.5 | Multiple Ways | could not assess | Nav, blog archive and glossary exist; no search form found in any route's markup, and whether search is reachable was not confirmed |
| 2.4.6 | Headings and Labels | could not assess | Structurally correct; whether each is descriptive is an editorial judgement |
| 2.4.7 | Focus Visible | pass | `outline: 2px solid #9a2f14` on every focusable, no bare `outline: none` |
| 3.1.2 | Language of Parts | could not assess | No `lang` on any element except `<html>`. If a post quotes a non-English passage, that is an uncaught failure. Not surveyed across the archive |
| 3.2.3 | Consistent Navigation | pass | Same primary nav, same order, all 11 |
| 3.2.4 | Consistent Identification | **FAIL** | F14, 3 of 18 new-tab links on `/work/` unannotated while 15 are |
| 3.3.3 | Error Suggestion | not applicable | No forms |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | not applicable | No forms, and nothing on the site creates a legal or financial commitment |
| 4.1.3 | Status Messages | could not assess | No `aria-live` regions exist, and no dynamic status content exists either, so probably vacuous rather than failing |

**Tally across both levels: 7 fail, 1 residual risk (2.2.2), 18 pass, 11 not applicable, 13 could not assess. 7 + 1 + 18 + 11 + 13 = 50.**

The 13 "could not assess" rows are the honest reason the "all criteria evaluated" acceptance criterion is **not** met, and why it is now unchecked below. Nine of the 13 need a human, not a better script: five need a screen reader (1.3.2, 1.3.3, 2.1.2, 3.1.2, 4.1.3), three need somebody to watch the two videos (1.2.1, 1.2.3, 1.2.5), and one needs somebody to look at the event graphics (1.4.5). That is exactly the specialist-audit gap, and it is not closable from a headless browser.

## Remediation plan

### Track B, theme, one PR

All of these are `theme/kk-aurora/` edits. They ship together behind the #601 pixel gate and need KK approval plus a deploy.

1. **Fix the cascade layer relationship.** This is the highest-leverage change and it needs the most care, because it will move colours site-wide. Two options:
   - Narrow option, lower blast radius: add an `@layer overrides { ... }` block (the layer is already declared at `style.css:20`) that re-asserts the button label colour and the service-card heading colour. Layered still loses to unlayered, so this alone is **not enough**; it would need `!important` on those specific declarations.
   - Correct option: stop wrapping theme CSS in `@layer components`, or dequeue / neutralise the conflicting `global-styles` declarations for `a` and `h1-h6`. This is the real fix and it must be pixel-gated across all 11 routes.
   Closes F1, F3, F4.
2. **`revive-port.css:996`**: change `.aurora-footer-2026 p, .aurora-footer-2026 a` to `.aurora-footer-2026 p, .aurora-footer-2026 a:not(.aurora-button)`. Closes F2.
3. **`style.css:1741-1747`**: replace the `#07090b` band background, or add light text tokens for `.aurora-final-cta h2 / p / .aurora-kicker / .aurora-button-secondary`. Closes F5.
4. **Two different alpha values, not one.** Revision 1 told an implementer to "replace `rgba(22, 24, 32, 0.84)`" at both `style.css:4215-4232` and `style.css:2855`. Only the first is `0.84`. Grepping the literal would have silently missed the second. The correct targets, from `grep -n "rgba(22, 24, 32" theme/kk-aurora/style.css`:
   - **`style.css:4221`** (inside the `.aurora-prose .wp-block-quote, .aurora-prose blockquote` rule opening at 4215): `rgba(22, 24, 32, 0.84)`
   - **`style.css:2858`** (inside the `.aurora-prose :where(.wp-block-quote, blockquote)` rule opening at 2855): `rgba(22, 24, 32, **0.8**)`

   Replace both with a paper-era panel colour. Closes F6 and F7.
5. **`style.css:4093`**: same treatment for `rgba(22, 24, 32, 0.82)`. Closes F8. **`style.css:4340`** carries the identical value and should be changed in the same pass. The full set the grep returns is lines 2775 (`0.78`), 2858 (`0.8`), 4093 (`0.82`), 4221 (`0.84`), 4340 (`0.82`).
6. **`style.css:1273`** (rule opens at 1271): same treatment for `rgba(18, 20, 27, 0.76)`. Closes F9.
7. **`parts/header.html:2` and `parts/footer.html`**: remove the duplicate landmark. Closes F13. **Watch for a side effect:** the header's `position: sticky` currently does nothing because its `wp-block-template-part` wrapper is exactly the header's own height. Un-nesting may make it genuinely sticky for the first time, at which point WCAG 2.2 SC 2.4.11 Focus Not Obscured becomes live for every anchor target outside `.aurora-prose`. Add `scroll-padding-top` to the root in the same PR.
8. **`revive-port.css:1242-1245`**: the `body.aurora-theme #aurora-main :where(.aurora-kicker, .aurora-section-kicker)` important override forces `--revive-accent-text` (`#9a2f14`) onto kickers inside the dark services band, where it measures 2.45:1. Exempt the band or give it a light kicker token. Closes F19. Do **not** just edit `revive-port.css:732-734`; that rule already loses.
9. **F17, in-prose link affordance.** Give resting `.aurora-prose` links a non-colour cue. `text-decoration: underline` in the resting state is the direct fix, since hover and focus already apply exactly that. This is the single highest-reach fix in the list because it touches every post on the site.
10. Optional, F15: add a pause control to the marquee, or accept the residual risk in writing.

**Suggested sweep before shipping:** grep the theme for the remaining dark-theme leftovers. `rgba(22, 24, 32,`, `rgba(18, 20, 27,`, `#07090b`, `#050708`, `rgba(9, 12, 17,`, `rgba(14, 17, 23,`, `rgba(3, 4, 5,` all still appear as backgrounds under light-theme text. Only the ones on live-rendered elements were confirmed failing; the rest are latent and will surface the moment those components get used.

**Verification gate:** re-run the rendered-pixel measurement on all 11 routes after deploy. A finding is closed when the glyph-versus-background ratio at 1440x900 is at or above 4.5 for body text and 3.0 for large text.

### Track A, content, separate PRs

11. `/contact/` page inline `<style>`: darken `--kk-muted` and `--kk-accent-text`. Closes F11 and F12. Note `/generative-ai-services/` carries the same token block; check it in the same edit even though no failure surfaced there in this pass. **F12 is a reconfirmation, not a discovery.** The 2026-07-26 report recorded the same 4.24:1 and it has not moved in a week.
12. `/work/`: add the "(opens in new tab)" sr-only span to the three "Explore ..." links. Closes F14. While in there, consider dropping the four `aria-label` attributes so the cards take their name from content; see the 2.5.3 section for why.
13. Post `2026/07/31/ai-lands-inside-every-profession/`: get real captions onto the two YouTube videos, or publish transcripts. Closes F10. This is Level A and, together with F16 and F17, one of three Level A failures.
14. Facebook pixel `<img>`: add `alt=""`. Closes F16. This is injected by the tracking snippet, not by post content. Also a reconfirmation of the 2026-07-26 report.
15. **Publish an accessibility statement.** `/accessibility/` is still 404, a week after the 2026-07-26 report flagged it. Not a WCAG criterion, but it is where a complaint starts. Owned by [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288) and [#48](https://github.com/WalksWithASwagger/kriskrug-wp/issues/48), not by this document. This report gives it something honest to say.

### Not in this document

Image alt text inventory is [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4) and is owned by a separate lane. What this audit can add to it: across the 11 routes, **every content image carries an alt attribute**. The only `<img>` without one is the Facebook tracking pixel (F16), and there is exactly one `alt=""` on the audited post. No filename-shaped alt text was found. So the remaining `#4` work is alt text *quality*, not alt text *presence*, at least on these routes.

## Acceptance criteria from #46: 3 of 7 met

Revision 1 claimed 4 of 7 and the fourth was not true. Corrected:

- [ ] **Audit covers 100% of public pages.** No. 11 routes. Theme-level findings generalise, content findings do not.
- [ ] **All WCAG 2.1 AA criteria evaluated.** **No, and revision 1 was wrong to tick this.** All 50 A and AA criteria now carry an explicit disposition in the table above, which revision 1 did not provide for 14 of them. But "has a disposition" is not "evaluated": **13 of 50 are "could not assess"**, and 9 of those need a human with a screen reader, a human watching the two videos, or a human looking at the event graphics. This criterion stays open until those 13 are closed.
- [ ] **Automated + manual testing complete.** **Partial, so no.** Automated browser measurement is done and is more rigorous than axe for contrast. Manual assistive-technology testing is not done: no VoiceOver, NVDA or JAWS, no forced-colors, no pointer-driven hover pass.
- [x] **Critical issues prioritised.** Ranked by users harmed times routes affected, in the findings table. Severity is a judgement call, stated as such.
- [x] **Remediation roadmap created.** Split by lane, with file and line references, 15 numbered items.
- [x] **Report deliverables complete.** This document, plus the per-criterion table and the delta against the two prior in-repo reports.
- [ ] **Audit by accessibility specialist.** No. This is an agent audit. If legal exposure is the driver, a certified human audit is still required, and this document is a useful input to it rather than a substitute.

**Honest total: 3 of 7.** #46 does not close on this document. What it does close is "we do not know what is broken": 19 findings with selectors, line numbers and measured ratios, and a named list of the 13 criteria still dark.

## Related, already closed

- [#289](https://github.com/WalksWithASwagger/kriskrug-wp/issues/289) WCAG smoke on core routes, **closed 2026-07-05** (`gh issue view 289 --json closedAt` returns `2026-07-05T20:16:49Z`). Revision 1 said 2026-07-02, which is the date of the pa11y comments on the issue, not the close date
- [#293](https://github.com/WalksWithASwagger/kriskrug-wp/issues/293) Aurora opal contrast failures, closed
- [#294](https://github.com/WalksWithASwagger/kriskrug-wp/issues/294) header brand accessible name, closed

F1 through F9 are all regressions or leftovers from the dark-to-paper theme flip that happened after those issues closed. #293 fixed the opal palette; it did not catch the panel backgrounds that stayed dark underneath light text, and it predates the `@layer` wrapper.
