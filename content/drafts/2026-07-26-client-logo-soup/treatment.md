# Proposed treatment (#413)

Monochromatic client logo band with keyboard-safe interaction. Matches Revive cream homepage language already in `revive-port.css` (grayscale hover patterns on contact sheet / work cards).

## Visual

- **At rest:** every logo rendered monochrome. Prefer CSS on full-color assets so one media upload serves both states:
  - `filter: grayscale(1) contrast(1.05); opacity: 0.82;`
  - Optional `brightness(0)` path if logos are already dark-on-transparent and need a hard ink silhouette on cream.
- **Consistency rule:** no logo may sit in full color while others are gray. Same filter stack on every `.aurora-logo-soup__item img`.
- **Cell size:** fixed logo box (`clamp(5.5rem, 12vw, 7.5rem)` wide, ~2.5-3rem tall content box) with `object-fit: contain`. Prevents layout shift on hover.
- **Grid:** flex wrap, centered, gap `1.25rem 1.75rem`. On 375px expect 2-3 per row; 768 ~4; 1440 ~6-8.
- **Background:** soft cream strip, light signal rule top/bottom (same family as `.aurora-proof-strip`), so it reads as proof, not a marketing carousel.

## Interaction (mouse + keyboard)

Recommended default: **both** color restore and a one-line note.

1. Each logo is a `<button type="button">` (or `<a>` only if KK wants outbound brand links; default is button so focus stays on-page).
2. `:hover` and `:focus-visible` (and `.is-active` for sticky tap on touch):
   - `filter: none; opacity: 1;`
   - reveal `.aurora-logo-soup__note` under the row or as a single shared readout region (`aria-live="polite"`).
3. Shared readout avoids eight expanding cells (no CLS). One line under the grid updates with client name + note.
4. `prefers-reduced-motion: reduce`: skip transform; keep filter/opacity instant.

### Why shared readout beats per-logo expand

- CLS-safe (evals require no layout shift on hover).
- One place for screen readers.
- Mobile: first tap activates; second tap can dismiss or cycle.

## Markup shape

See `proposed-html.html`. Section id: `clients`. Class root: `aurora-logo-soup`. Independent of `#newsletter`.

## Assets

- Host on kriskrug.co media (Jetpack CDN OK).
- Prefer SVG; else PNG with transparent background, min ~320px wide.
- `alt` = client name only (e.g. `Lululemon`). Decorative treatment lives in CSS, not empty alt.
- Width/height attributes set to intrinsic ratio; CSS constrains display size.

## A11y

- Section `aria-labelledby` pointing at the H2.
- Buttons: `aria-label` = client name; `aria-describedby` optional when note is shown.
- Focus ring: 2px signal outline, offset 3px (match existing Aurora button focus).
- Contrast: mono logos on cream must stay readable; if a mark disappears when grayed, use a prepared mono SVG instead of filter.

## Theme apply notes (Track B follow-up)

- CSS goes in `revive-port.css` near `.aurora-proof-strip` (same visual family).
- Do not edit newsletter rules introduced by #505.
- Aurora version bump only when theme files actually change (separate Track B commit after this draft package).

## Non-goals

- Marquee / infinite scroll logo carousel.
- Auto-playing color cycling.
- Replacing `#stages` text strip.
- Shipping with placeholder brand SVGs scraped from the web (rights + quality risk).
