# Aurora Mobile / Responsive QA — Issue #127

**STATUS: Superseded (2026-08-16).** Live pass is in [`reports/issue-127-mobile-qa-2026-08-16.md`](reports/issue-127-mobile-qa-2026-08-16.md). Original acceptance criteria passed on Aurora **1.6.5**. Do not treat this file as a pending device-QA checklist. Breakpoints, pill-nav, and “≤700px” notes below are pre-#479 / pre-Revive.

**Historical test plan** (kept for the keyboard/overflow checklist shape). Scope was verification of the *current* horizontal-scroll nav contract (not a hamburger — see #28). Visual checks belong in device mode, not a plain window resize.

## 1. Code-level audit (what's already implemented)

| Area | Finding | Evidence |
|---|---|---|
| Keyboard nav | Roving focus implemented: ArrowLeft/Right wrap, Home/End jump, `scrollIntoView` keeps the focused pill visible | `assets/js/theme.js` `initPrimaryNavKeyboard()` |
| Focus indicators | `:focus-visible` outlines on nav links, utility link, CTA, cards | `style.css:692`, plus per-component `:focus-visible` rules |
| Skip link | Present and styled (`.skip-link` → `#aurora-main`) | `parts/header.html`, `style.css:419` |
| Mobile nav layout | ≤700px: `.aurora-primary-nav` becomes a full-width horizontal `overflow-x:auto` row of pill links (scrollbar hidden); actions stay top-right | `style.css:2605–2662` |
| Reduced motion | Covered in CSS (`@media (prefers-reduced-motion: reduce)` at `style.css:78, 3791`) and JS (smooth-scroll + reading-progress in `theme.js`, all of `aurora-animations.js`) | grep-confirmed |
| Dead code | Removed orphan `initMobileMenu()` (targeted `.aurora-menu-toggle`/`.aurora-mobile-menu`, which exist in no template/part) in this branch | this PR |

**Breakpoints in play:** 360, 700, 781/782, 980, 1180px (+ `min-width:900`).

### Likely findings to confirm on device
1. **Touch-target sizing (probable fail).** Mobile nav pills are `padding:0.46rem 0.58rem` + `font-size:0.76rem; line-height:1` → computed height ≈ **27px**; `.aurora-utility-link` is `min-height:36px`; `.aurora-header-cta` is `min-height:40px`. All are **below the 44–48px** touch-target guideline. (Relevant to #33/#28 criteria; recommend bumping nav-pill vertical padding and raising utility/CTA min-heights to ≥44px.)
2. **768px is a transitional band.** The ≤700px mobile-nav rules do **not** apply at 768px, so the nav renders in a tablet/desktop-ish state there. Verify it neither wraps awkwardly nor overflows at exactly 768.

## 2. Manual QA checklist — run at 360 / 390 / 768 (desktop as control)

Use Chrome DevTools device mode (or a real phone). For each width:

### Navigation & keyboard
- [ ] Primary nav is reachable and all links are operable.
- [ ] `Tab` reaches the first nav link; `ArrowRight`/`ArrowLeft` move focus and wrap; `Home`/`End` jump to first/last.
- [ ] The focused pill scrolls into view (no focus lost off-screen).
- [ ] Focus indicators are clearly visible on nav links, Dispatch link, and the CTA.
- [ ] Skip link appears on first `Tab` and jumps to main content.
- [ ] Touch targets ≥ 44px (see finding #1 — expected to fail until padding bumped).

### Layout & overflow
- [ ] No horizontal page overflow on **home, work, speaking, contact** (`document.documentElement.scrollWidth === clientWidth`).
- [ ] Hero image crop/scale is acceptable; headline not clipped.
- [ ] Work "Public artifacts" cards stack to one column; no image/text overlap (cross-check #120, verified clean on live).
- [ ] No element bleeds past the viewport edge (tables, code blocks, embeds, wide images).

### Motion & a11y
- [ ] With OS "Reduce Motion" on, GSAP/scroll animations are disabled and no content depends on them.
- [ ] Color contrast holds on header, nav pills, CTA, and card text (spot-check with DevTools).

## 3. Process
- File **one bug issue per failure**, labeled `aurora-v2`, `mobile`, `track-b`, referencing #127 — do **not** fix inside #127.
- When all boxes pass (or failures are filed), record the results back in this doc and close #127.
- Remember: the live site reflects the *deployed* theme, which may lag `main` — confirm the build under test matches before filing theme bugs (see the repo↔live drift note).
