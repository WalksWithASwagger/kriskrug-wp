# Services page audit - #420

**Status:** draft only. Public HTML + Playwright height readback. No live WP write.  
**Fetched:** 2026-07-26  
**Entry:** `GET https://kriskrug.co/services/` → **301** → `https://kriskrug.co/generative-ai-services/` (**200**)  
**WP page ID:** 2666  
**Evidence:** `evidence/public-entry-content-2026-07-26.html`, `evidence/snapshot-meta.json`, `evidence/height-baseline-playwright.json`

## Issue claim (KK teardown 2026-07-17)

> The language is weak and the boxes are weak. There's a lot of scroll. The stylesheet's fucked up. This page needs a rethinking from the ground up.

## Live structure (2026-07-26)

Page body is a single custom HTML pack (`.kk-services-2026`) with **4,418 bytes** of inline `<style>` (matches the #423 rebuild inventory for this URL).

1. **Hero** - kicker `AI services`, display H2, two lead paragraphs  
2. **How I can help** - 4× `.kk-services-ribbon-card` in a 2×2 grid (I–IV)  
3. **Proof in motion** - 2× `.kk-services-proof-card` (image + blurb) linking `/work/` and `/speaking/`  
4. **Start here** - CTA card: Book an AI strategy session → `/contact/`

WP post title above the pack: **Generative AI Creative Services & Strategy** (separate from pack H2).

Source-pack HTML in-repo (`content/source-packs/content-architecture-2026/wp-payloads/services.html`) still uses `.aurora-*` classes. Live has diverged to the `kk-services-*` pack. Treat live HTML as truth for #420.

## Finding 1 - Language is soft / abstract (confirmed)

Hero and offer cards lean on filler frames instead of concrete offers:

| Phrase (live) | Problem |
|---|---|
| still care about culture | vibe headline; not an offer |
| practical fluency | abstract outcome |
| sensemaking | consultant fog |
| creative courage | motivational filler |
| capacity building | NGO-speak |
| vendor fog | cute, unclear |
| slightly electric | adjective flex, zero information |

Offer cards state **what** in one sentence. They do **not** state **who it is for** or **what to do next**. Page-level NEXT exists only once at the bottom CTA. That fails acceptance: every service block needs what / who / next.

Em dashes in pack body: **0**. Document `<title>` still uses an em dash in the SEO chrome (Yoast/title pattern); out of scope for pack copy unless KK wants a title rewrite.

## Finding 2 - Boxes are weak (confirmed)

Ribbon cards are left-border ribbons on transparent background (no real surface, no CTA, no who-line). They read as labeled blurbs, not offers.

Proof cards are stronger visually (photo + border) but they are proof, not offers, and they add a large image plane to scroll depth.

## Finding 3 - Scroll depth is high (measured)

Playwright Chromium headless, logged-out, `scrollHeight`:

| Viewport | `document` px | `.kk-services-2026` pack px | Hero | Ribbon grid | Proof grid | CTA |
|---|---:|---:|---:|---:|---:|---:|
| **1440×900** | **3548** | **2064** | 580 | 377 | 457 | 269 |
| 768×900 | 4485 | 2942 | 490 | 639 | 1191 | 249 |
| 375×812 | 4833 | 2827 | 662 | 734 | 799 | 266 |

Acceptance target (cut at least one third at 1440):

| Scope | Before | Target (≤ 2/3) | Cut needed |
|---|---:|---:|---:|
| Full document | 3548 | **2365** | ≥ 1183 |
| Pack only | 2064 | **1376** | ≥ 688 |

Scroll drivers at 1440 (largest first inside the pack): **hero 580**, proof 457, ribbon 377, CTA 269, plus section padding/margins (`2.4rem` bottom + `2.4rem` margin on hero/sections). Site header + WP title + footer sit outside the pack and inflate document height.

Above-the-fold at 1440 barely clears the hero lead. Offers require scroll. That matches the teardown.

## Finding 4 - Stylesheet issues (confirmed; do not double-build)

| Fact | Detail |
|---|---|
| Inline CSS size | **4,418 B** inside page content |
| Rebuild plan | `AURORA-STYLESHEET-REBUILD-PLAN.md` lists this block for **step 7 deletion** after theme layers land (#423) |
| Parallel rule | Copy + layout may proceed now; **do not** invent a second Services stylesheet in `theme/` |
| Live vs source-pack | Live `kk-services-*` pack is not the repo `aurora-*` payload |

Any page-scoped CSS edits for #420 should stay minimal, prefer HTML/structure density wins, and expect the inline block to die in the rebuild. No new `!important`.

## Finding 5 - CTA / link smoke (logged out)

| URL | Result |
|---|---|
| `/services/` | 301 → `/generative-ai-services/` then **200** |
| `/generative-ai-services/` | **200** |
| `/contact/` (primary CTA) | **200** |
| `/work/`, `/speaking/` (proof) | **200** |
| Proof images (i0.wp.com) | **200** |
| Beehiiv (footer chrome, not pack CTA) | curl **403** (bot wall); treat as browser-check at apply time |

## Root cause summary

| Problem | Root cause | Fix lane |
|---|---|---|
| Weak language | Abstract hero + offer blurbs without who/next | Track A copy (`language-options.md`) |
| Weak boxes | Ribbon cards are decoration, not offers | Track A HTML structure |
| Too much scroll | Tall hero + section chrome + large proof images | Track A layout (`layout-scroll-plan.md`) |
| Stylesheet fucked | 4.4 KB page-owned CSS diverged from theme / rebuild path | Coordinate with #423; tighten in content, do not rebuild theme CSS here |

## Recommended direction

1. **Language:** Option A in `language-options.md` (concrete offers; what / who / next on every block).  
2. **Layout:** Plan A in `layout-scroll-plan.md` (collapse hero, denser offer grid, shrink proof, pull CTA up).  
3. **CSS:** touch only what density requires; leave #423 as the stylesheet owner.

See `verification-checklist.md` for apply gates. No live write from this package.
