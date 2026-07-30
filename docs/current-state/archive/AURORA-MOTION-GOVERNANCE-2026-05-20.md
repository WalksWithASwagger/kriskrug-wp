# Aurora Motion Governance - 2026-05-20

**Purpose:** Keep Aurora's "human-made" feel expressive without letting motion become a performance, accessibility, or maintenance liability.
**Scope:** Track B guidance only. Do not edit `theme/kk-aurora/` from `main`.

## Motion budget

Aurora gets three intentional motion layers:

1. **Navigation continuity:** native View Transitions where supported, no hard dependency for navigation.
2. **Reading orientation:** low-cost reading progress and section reveal behavior.
3. **Proof affordance:** restrained hover/focus treatment for talks, projects, event cards, and CTAs.

Everything else is suspect until it earns its place in QA. Cursor glows, ripple effects, overlapping scroll libraries, and decorative parallax should be removed unless they pass the checks below.

## Allowed implementation preferences

- Prefer CSS transitions and CSS scroll-driven animation for simple progress/reveal effects.
- Use GSAP only for a named interaction that CSS cannot express cleanly.
- Do not run multiple reveal systems on the same element.
- Honor `prefers-reduced-motion: reduce` by removing non-essential animation, not merely slowing it down.
- Keep focus states instant and visible; never hide keyboard focus behind motion timing.
- Avoid motion that changes layout or causes late content shifts.

## QA gate for issue #86

Before Aurora can be considered launchable, capture evidence for:

- Desktop and mobile screenshots for homepage, Work, Speaking, and one long-form page.
- Keyboard navigation through header, mobile nav, cards, forms, and CTAs.
- Reduced-motion behavior on the same surfaces.
- Console and network errors.
- Image/media loading with production-like assets.
- Basic Core Web Vitals notes, with special attention to INP and LCP.
- Overflow/text clipping checks on mobile.

## Keep or cut rule

Keep an effect only if it improves orientation, confidence, delight, or proof comprehension and does not make the page harder to read, navigate, or measure. Cut it when the only argument is "it looks cool."
