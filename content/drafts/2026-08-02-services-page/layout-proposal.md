# Services page layout proposal, issue #420

**Status:** draft. No CSS proposed, no theme files touched.
**Measured:** 2026-08-02, Playwright Chromium headless, logged out, light scheme, reduced motion, scroll-settle pass.
**Prototype:** `pack-proposed.html` injected into the live page, then re-measured under identical conditions.

## The constraint that shaped this

The stylesheet decision is #423 and it is open. So this proposal is built to a hard rule: **the height cut must come from HTML structure and copy only, with the existing stylesheet untouched.** Every number below was measured with the live 4,418 byte inline block exactly as it is today. Nothing here needs a CSS change to work, and nothing here blocks #423 from deleting that block later.

That rule turned out to be a feature. It forced the design into the space the current CSS already provides, which is why the biggest win is free.

## Section order, before and after

**Before, 4 sections:**

1. Hero: kicker, display H2, two lead paragraphs
2. How I can help: 4 ribbon cards, 2 x 2
3. Proof in motion: 2 photo cards, 2 x 1
4. Start here: CTA card

**After, 3 sections:**

1. Open: display H2, one lead, primary button
2. Offers: 4 ribbon cards, 2 x 2, each carrying audience, offer, and next step
3. How to start: CTA card

**Section count 4 to 3. Boxed surfaces 7 to 5. Images 2 to 0. Links 3 to 6.**

Why this order. The page is the destination of the site's primary "Work with me" CTA, so its only job is to name what you can buy and route you one click deeper. Open states the four things exist. Offers lets you self-select. How to start tells you what to put in the email. There is nothing else a front door needs.

## The four mechanisms

### M1. Delete "Proof in motion", move proof into the cards

The largest single item on the page. Two `<a>` cards each wrapping a 16:10 image, linking `/work/` and `/speaking/`.

Those are the same two destinations the offer cards now link to. The section was a second, taller navigation to places the offers already had to point at. So it becomes the offer cards' link targets.

| Viewport | Height removed |
|---|---:|
| 1440 | 532 |
| 768 | 1258 |
| 375 | 868 |

The image plane is why 768 is the worst viewport on the live page: the grid drops to one column, so both 16:10 images render at full container width, 459px each. The proof section alone is 1258px there, larger than the entire proposed page body at that viewport.

Side effect, free: this also removes the bold-text bug. The proof card is an `<a>`, so `.kk-services-2026 a:not(.kk-services-button) { font-weight: 700 }` currently forces both card headings and both blurbs to weight 700. Deleting the cards deletes the symptom. #423 should still fix the cause.

### M2. Repurpose the wasted kicker slot for the audience line

This is the important one and it costs nothing.

Each offer card already renders three stacked elements: a `.kk-services-kicker`, an `h3`, and a `p`. The kicker currently holds `I.` `II.` `III.` `IV.` Roman numerals. They carry no information and they occupy a styled, spaced, already-paid-for row.

Put the audience there.

```
BEFORE                          AFTER
I.                              CONFERENCES, FESTIVALS, OFFSITES
AI strategy                     Keynote talks
Map where AI can actually       A 30 to 60 minute talk built for
help, where it should stay      your room ... [Topics and formats]
out, and how your team can
move without chaos or
vendor fog.
```

The "next step" goes inline at the end of the blurb, inside the existing `p`, which already has link styling (`a:not(.kk-services-button)`, accent colour, weight 700, underline on hover).

Result: all four cards satisfy the issue's acceptance test (what it is, who it is for, what to do next) with **zero new CSS and zero added height**. The card grid is 343px before and 373px after at 1440. Thirty pixels for four audience lines and four links.

This is the answer to "the boxes are weak". The boxes were not weak because they lacked a surface. They were weak because one of their three slots was a roman numeral.

### M3. Collapse the hero

Remove the "AI services" kicker, since the H1 immediately above it says the same word. Cut the two lead paragraphs to one, since the first was a table of contents for the grid below and the second defined the work by what it is not. Pull the primary CTA button up into the hero so there is a way to act above the fold.

1440: 449 to 356. 768: 403 to 321. 375: 563 to 365.

### M4. Tighten the closer

`h2` plus two paragraphs plus a button becomes `h2` plus one paragraph plus a button, with the pricing mechanics folded into the same paragraph.

1440: 297 section height retained but the CTA card itself carries more information in less space. 768: 277 to 249. 375: 294 to 319 (mobile grows slightly because the merged paragraph wraps to more lines at 375; net still strongly positive).

## Measured result

Same page, same stylesheet, same fonts, same theme header and footer. Only `.kk-services-2026` innerHTML differs.

| Viewport | Scope | Before | After | Change |
|---|---|---:|---:|---:|
| **1440 x 900** | entry content | 1860 | 1184 | **-36.3%** |
| | services block | 1819 | 1143 | **-37.2%** |
| | full document | 3737 | 3061 | -18.1% |
| **768 x 900** | entry content | 2758 | 1335 | **-51.6%** |
| | services block | 2716 | 1293 | **-52.4%** |
| | full document | 4812 | 3389 | -29.6% |
| **375 x 812** | entry content | 2644 | 1758 | **-33.5%** |
| | services block | 2602 | 1716 | **-34.1%** |
| | full document | 5326 | 4440 | -16.6% |

Section by section at 1440:

| Section | Before | After |
|---|---:|---:|
| Hero / Open | 449 | 356 |
| How I can help / Offers | 426 | 412 |
| Proof in motion | 532 | removed |
| Start here / How to start | 297 | 297 |
| **Block total** | **1819** | **1143** |

## Above the fold

| Viewport | First offer card top, before | After | Fold |
|---|---:|---:|---:|
| 1440 x 900 | 935 | **799** | 900 |
| 375 x 812 | 941 | **700** | 812 |

Today, at both the desktop and the mobile reference viewport, you cannot see a single purchasable thing without scrolling. After, the first offer is on the first screen at both.

## The acceptance criterion needs a ruling

The issue says "Total page height reduced by at least a third at 1440". Against the full document that means 3737 to 2491, a 1246px cut.

The page body is 1819px. The theme footer is 1384px. Hitting 1246px out of the document while the footer is fixed means removing 68 percent of everything this page owns.

| At 1440 | px | Share of document |
|---|---:|---:|
| Theme header | 76 | 2% |
| Theme H1 block | 179 | 5% |
| Services block, before | 1819 | 49% |
| Theme footer | 1384 | **37%** |

At 375 the footer is 2344px, **44 percent** of the document, for 105 words.

Recommendation: **score #420 on entry content at 1440**, where this delivers 36.3 percent, clear of the bar. Then file the footer as its own issue. It is 1384px of chrome on every page of the site, it is Track B, and this lane has not touched it.

## Dependency on #423, and how it is contained

Nothing here adds, edits, or deletes a CSS rule. The proposal is deliberately built inside the styling the page already has, so it lands cleanly whichever way #423 goes.

`AURORA-STYLESHEET-REBUILD-PLAN.md` lists this page's inline block for step 7 deletion. When that happens, three existing behaviours must be preserved or rehomed or this layout degrades:

| Class | What the layout needs from it | If it disappears |
|---|---|---|
| `.kk-services-kicker` | small mono uppercase label above the `h3` | the audience line reads as body copy and the card loses its scan hierarchy |
| `.kk-services-ribbon-card::before` | the 8px colour ribbon on the left edge | the cards lose their only visual boundary, since they have no background or border |
| `.kk-services-button` | inverted solid CTA button | the two CTAs render as plain accent links |

Also for #423, observed on the live page and **not fixed here**:

1. `a:not(.kk-services-button) { font-weight: 700 }` cascades into whole-card links, so the proof cards render entirely bold. Removed by M1, but the rule is still wrong.
2. `.kk-services-cta { border-top: 2px solid accent; max-width: 40rem }` stacks directly under the previous section's full-width 1px bottom border, producing two horizontal rules with the section kicker floating between them. Still present in the proposed layout, because fixing it is a CSS change.
3. Eight `!important` declarations on `:where(p, li)::first-letter` exist only to cancel a theme drop cap, plus `max-width: 72rem` to escape the `aurora-prose` measure. This is the page fighting the theme, which is the condition #423 is meant to end.

**Order of operations:** this layout can land before or after #423. It does not need the stylesheet decision, and it does not pre-empt it. If #423 lands first, re-measure before applying, since the numbers above were taken against today's CSS.

## Rejected alternatives

**Tabs or an accordion over the four offers.** Would have got the block under 800px at 1440. Rejected: it hides every offer behind a click on the page the site's primary CTA points at, and it drops four offer names out of the initial HTML for search. Density beat disclosure here.

**Four across in a single row at 1440.** Rejected: at 72rem max-width each card gets roughly 250px, the 1.65rem `h3` wraps to three lines, and the 2 x 2 grid it replaces is only 343px tall to begin with. It would have traded readability for about 150px.

**Keeping one proof image.** Rejected: a single 16:10 image is still 299px at 1440 and 459px at 768, which is most of one mechanism's savings for one photograph that already appears on `/work/`.
