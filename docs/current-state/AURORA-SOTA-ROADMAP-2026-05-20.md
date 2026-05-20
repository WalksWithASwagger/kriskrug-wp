# Aurora State-of-the-Art Roadmap - Summer 2026

**Prepared:** 2026-05-20
**Snapshot time:** 2026-05-20 17:30 UTC
**Track:** B (`aurora/v2`)
**Purpose:** Step back from issue-by-issue execution and align Aurora to a true summer-2026 quality bar.

## Current Truth (before new implementation)

- Open PRs: `0`
- Open issues: `63`
- Open `track-b` + `aurora-v2` issues: `13` (`#24-#35`, `#86`)
- Active Aurora hard gate: `#86` (staging performance/accessibility QA)
- Working rule remains: no Track A content writes mixed into Track B theme lanes.
- Motion budget addendum: `AURORA-MOTION-GOVERNANCE-2026-05-20.md`.

## What "State of the Art" Means for Aurora (Summer 2026)

The bar is no longer "has animation." The bar is:

1. unmistakable identity in the first viewport,
2. real media proof (photo/video/projects) instead of decorative gradients,
3. motion as usability and narrative, not spectacle,
4. measurable performance/accessibility quality on real devices.

### Benchmark Signals and Implications

| Signal (2026) | What it means for us |
|---|---|
| Award-level portfolio/personal-brand work is still judged on craft + UX + innovation together, not visuals alone. | Aurora must pair visual polish with clear IA, clear CTAs, and fast comprehension. |
| View Transitions are now practical across same-origin page navigation (progressive enhancement). | Keep transition polish, but ship fallbacks and test real WordPress route behavior. |
| Scroll-driven CSS animation is production-usable as enhancement. | Prefer CSS timeline/reveal primitives for lightweight effects; reserve JS for high-value interactions. |
| Core Web Vitals remain explicit and unforgiving (`LCP <=2.5s`, `INP <=200ms`, `CLS <=0.1` at the 75th percentile). | Every visual decision (hero media, motion, script weight) must pass a budget, not just taste review. |
| WCAG 2.2 is the accessibility baseline, including reduced-motion and moving-content control expectations. | Any morph/glass/motion layer needs keyboard, focus, contrast, and pause/reduce behavior by default. |
| Autoplay restrictions and user preference constraints are mainstream browser behavior. | No heavy autoplay-default hero strategy; poster-first and explicit play affordances win. |

## Strategic Product Direction (Aurora)

Aurora should feel like a premium editorial studio for AI-era leadership:

- **Editorial authority:** sharp type, confident hierarchy, less generic "AI theme" styling.
- **Media truth:** real photos, speaking footage, project evidence, event context.
- **Restrained morphism:** glass/morphism only where it helps controls, overlays, metadata, and navigation.
- **Narrative motion:** transitions and reveals that guide attention; no motion-only meaning.
- **Conversion clarity:** primary CTA hierarchy stays stable across homepage, Work, Speaking, and Contact.

## Feature Stack: Prioritized Build Order

## P0 - Finish the non-negotiable gate (Now)

**Issue:** `#86`  
**Outcome:** production-like QA evidence, not local-only confidence.

Ship criteria:

- staging screenshot matrix (desktop/mobile: Home, Work, Speaking, long-form template)
- keyboard/focus traversal pass
- reduced-motion pass
- contrast spot checks against WCAG 2.2 expectations
- media load behavior evidence (hero, cards, embeds)
- perf notes with explicit LCP/INP/CLS observations

If P0 fails, pause feature expansion and fix debt first.

## P1 - Signature Experience Layer (Next)

Target: move from "good prototype" to "recognizable Kris Krug experience."

1. **Hero media orchestration**
   - canonical hero asset set (video poster + still fallback + mobile crop)
   - art-directed crops by breakpoint
   - no autoplay-default heavy payload

2. **Speaking authority module**
   - reel block (poster-first embed)
   - topics + outcomes + social proof
   - one booking CTA path that does not fragment

3. **Work proof rail**
   - project cards with proof metadata (`role`, `context`, `result`, `link`)
   - clear split between flagship projects and archive breadth

4. **Reading/essay polish**
   - long-form templates that support image-rich essays and embeds cleanly
   - improved in-article hierarchy and related-next paths

## P2 - System Quality Layer (Immediately after P1)

Target: make polish consistent and maintainable.

1. **Motion governance**
   - inventory each animation and assign purpose (`reveal`, `transition`, `feedback`, `delight`)
   - remove redundant overlaps between CSS/GSAP/micro-interaction scripts

2. **Component governance**
   - finalize restrained component inventory (buttons, cards, forms, footer, callouts)
   - remove card-over-card drift and keep section-level layouts unframed

3. **Media pipeline**
   - source-of-truth manifest for hero/work/speaking assets
   - AVIF/WebP + JPEG fallback strategy
   - alt text + caption + rights metadata workflow

## P3 - Launch Readiness Layer

Target: safely decide go-live timing.

1. **Staging-to-production checklist**
   - backup and rollback proof attached
   - environment parity notes
   - QA regression checklist rerun after final content/media swap

2. **Issue hygiene**
   - close or relabel legacy design tickets `#24-#35` based on acceptance evidence, not age
   - keep one canonical epic path to prevent duplicate execution

3. **Feedback loop**
   - gather external review on:
     - first-impression authority,
     - clarity of offerings,
     - media credibility,
     - motion comfort,
     - conversion confidence.

## Recommended Issue Model (to reduce queue entropy)

Current open Track B set still includes both new epic-style work (`#86`) and old granular tickets (`#24-#35`).  
Recommendation:

1. keep `#86` as the active gate issue,
2. treat `#24-#35` as checklist references unless they hold unique acceptance criteria,
3. avoid opening more Track B implementation lanes until `#86` evidence is complete.

## 7-Day Execution Plan

### Day 1-2
- complete `#86` on real staging and publish one canonical QA packet.

### Day 3-4
- implement hero media orchestration + speaking authority module.

### Day 5
- implement work proof rail + long-form polish deltas.

### Day 6
- run perf/a11y regression pass; remove non-essential motion weight.

### Day 7
- reviewer walk-through + decision memo: `ship`, `polish one more cycle`, or `hold`.

## Decision Gates (must be explicit)

1. **Brand gate:** Does first viewport instantly signal Kris Krug authority?
2. **Usability gate:** Can a new visitor understand offers and navigate in under 30 seconds?
3. **Performance gate:** Are LCP/INP/CLS within acceptable range on representative mobile?
4. **Accessibility gate:** Are keyboard, focus, reduced-motion, and contrast behavior reliable?
5. **Operations gate:** Are backup/rollback and QA artifacts complete enough to recover from mistakes?

If any gate is red, do not launch.

## Sources Used for Summer-2026 Benchmark

- [Awwwards - Sites of the Day](https://www.awwwards.com/websites/sites_of_the_day/)
- [Chrome Developers - View transitions in 2025](https://developer.chrome.com/blog/view-transitions-in-2025)
- [Chrome Developers - Cross-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document)
- [MDN - View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)
- [MDN - prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [MDN - Autoplay guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
- [W3C - WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)
- [W3C - Understanding SC 2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
- [W3C - Understanding SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum)
- [web.dev - LCP](https://web.dev/articles/lcp)
- [web.dev - INP](https://web.dev/articles/inp)
- [web.dev - CLS](https://web.dev/articles/cls)
- [WordPress - Block themes documentation](https://wordpress.org/documentation/article/block-themes/)
