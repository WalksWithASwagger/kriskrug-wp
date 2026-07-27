# Layout and scroll plan - Services page (#420)

**Mode:** DRAFT ONLY. No live WP write.  
**Target:** page ID `2666`, slug `generative-ai-services`, URLs `/services/` → `/generative-ai-services/`  
**Baseline (Playwright, 2026-07-26):** at **1440**, document **3548 px**, pack **2064 px**.  
**Acceptance:** cut total page height by **at least one third** at 1440 without losing offers → document ≤ **2365 px** (cut ≥ **1183 px**). Pack-only guide: ≤ **1376 px**.

## Stylesheet coordination (#423)

- Live pack owns **4,418 B** of inline CSS (`.kk-services-2026*`).  
- Rebuild plan schedules that block for **step 7 deletion**.  
- **Do not** add a parallel Services stylesheet under `theme/kk-aurora/`.  
- Prefer HTML structure + tighter spacing tokens inside the existing page block.  
- No new `!important`. Expect the inline block to shrink or vanish when #423 step 7 lands.

## What burns height today (1440)

| Block | Height px | Notes |
|---|---:|---|
| Hero | 580 | Biggest pack offender: large display + two long paragraphs + section chrome |
| Proof grid | 457 | 16/10 images in two columns |
| Ribbon grid | 377 | 2×2 offer cards with airy type |
| CTA | 269 | Separate band after proof |
| Section chrome | ~ (included above) | `padding-bottom: 2.4rem` + `margin-bottom: 2.4rem` on hero/sections |
| Outside pack | ~1484 | Header, WP post title, footer (document − pack) |

Footer/header are site chrome. #420 wins most of the cut **inside the pack** (hero + proof + section spacing). Title shortening is a bonus if KK approves.

## Plan A - Recommended: denser single page (no tabs)

Keep all four offers visible. Compress vertical rhythm.

### Structure

1. **Hero (short)** - kicker + one H2 + one lead paragraph. Drop the second support paragraph or fold one sentence into the lead (Option A/B language).  
2. **Offer grid** - 2×2 cards. Each card: title, what (1 line), who (1 line), next (text link). Optional thin left ribbon kept for brand continuity.  
3. **Proof row** - same two links, but image aspect **21/9** or fixed max-height ~160 px at desktop; blurbs one line.  
4. **CTA** - merge into the offer section foot or a compact band directly under the grid (no second long essay). Button stays `/contact/`.

### Spacing targets (page-scoped)

| Token | Live | Proposed |
|---|---|---|
| Section pad/margin stack | 2.4rem + 2.4rem | **1rem + 1.25rem** |
| Display size | clamp(2rem, 4.5vw, 3rem) | clamp(1.6rem, 3.5vw, 2.25rem) |
| Offer H3 | 1.65rem | **1.25rem** |
| Proof image | aspect-ratio 16/10 | **21/9** or `max-height: 160px` |
| Pack max-width | 72rem | keep (or 56rem if KK wants tighter rail with About) |

### Height budget (1440, estimated after Plan A)

| Block | Target px |
|---|---:|
| Hero | ~220 |
| Offer grid | ~420 |
| Proof | ~220 |
| CTA | ~160 |
| Pack total | ~**1020–1200** (under 1376 guide) |

Document height also depends on footer. If pack drops ~800–1000 px, document lands near or under **2365**. Confirm with Playwright after draft HTML is built; record before/after in the apply PR.

### Offers not lost

All four offers remain on-canvas (I–IV). No tabs required.

## Plan B - Tabs / segmented control

Hero (short) + tablist for four offers (one panel visible) + compact proof + CTA.

| Pros | Cons |
|---|---|
| Largest scroll cut | Hides three offers until click/tap |
| Clear what/who/next per panel | Needs keyboard a11y (tabs, aria-selected, focus) |

Use only if Plan A measured after draft still misses the one-third cut, or if KK prefers progressive disclosure.

## Plan C - Merge sections (pairs with language Option C)

Three offers in one row on desktop (or 2+1), proof as text links without large images, CTA inline.

Biggest cut. Loses a named fourth offer and most proof imagery.

## Out of scope

- Theme file CSS rewrite (#423)  
- Changing the `/services/` → `/generative-ai-services/` redirect  
- Beehiiv footer band  
- Restoring pre-2026 mega services lists from `fixes/issue-67-services-page-expanded.md` unless KK asks

## Implementation notes for apply-ready HTML (next session after KK picks)

1. Start from live `evidence/public-entry-content-2026-07-26.html`, not the stale `aurora-*` source pack.  
2. Rewrite copy from the chosen language option.  
3. Apply Plan A spacing + proof shrink.  
4. Measure Playwright heights at 1440/768/375; paste into PR.  
5. Keep pack marker / class `kk-services-2026` unless #423 migration says otherwise.

## KK picker

- [ ] **Plan A (recommended)** - denser single page, four offers visible  
- [ ] Plan B - tabs  
- [ ] Plan C - three offers + text proof  
- [ ] Custom: _______________________
