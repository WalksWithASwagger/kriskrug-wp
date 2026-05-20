# Aurora Swarm #85 Components - 2026-05-20

Track: B - Aurora v2 theme
Issue: [#85](https://github.com/WalksWithASwagger/kriskrug-wp/issues/85)
Branch: `codex/swarm-85-component-library-2026-05-20`

## Scope

Restrained component-library hardening after issue `#84` merged.

No production WordPress writes, no Track A content edits, no Aurora activation, and no merge to `main`.

## What Changed

- Added a reusable utility pattern:
  - `theme/kk-aurora/patterns/component-utility-system.php`
  - Covers search, newsletter, and a contact-intent form shell.
- Upgraded the 404 page search into a named search utility:
  - `theme/kk-aurora/templates/404.html`
- Added a footer newsletter utility with fallback Beehiiv CTA:
  - `theme/kk-aurora/parts/footer.html`
- Added component state CSS in `theme/kk-aurora/style.css`:
  - focus-visible states for links, buttons, cards, search, and form controls
  - active states for buttons/cards
  - disabled and loading button states
  - empty-state component classes
  - search, newsletter, form, Gravity Forms, and Jetpack/contact-form styling hooks
  - reduced-motion guard for loading spinner animation

## Acceptance Readback

- [x] Component inventory is documented before implementation.
  - `docs/current-state/AURORA-COMPONENT-INVENTORY-2026-05-20.md`

- [x] Component coverage exists for project card, talk card, media band, proof chip, CTA row, article card, testimonial, form, footer section, newsletter utility, and search utility.
  - Existing: Work/Speaking proof modules, media cards, proof chips, CTA rows, article rows, testimonial cards, footer sections.
  - Added: utility pattern, search utility, newsletter utility, form shell/style contract.

- [x] Cards are only used for repeated items.
  - No page-level band was converted into a card.
  - The new utility pattern uses grid utilities and restrained surfaces, not nested card shells.

- [x] No card-inside-card layouts.
  - The implementation did not nest `.aurora-media-card`, `.aurora-proof-module`, `.aurora-topic-card`, or `.aurora-quote-card` inside one another.

- [x] Components have hover, focus, active, disabled, loading/empty, mobile, and reduced-motion states where applicable.
  - Added explicit focus/active/disabled/loading/empty coverage.
  - Existing mobile collapse rules were extended to utilities.
  - Reduced-motion disables loading spinner animation.

- [x] Forms are accessible and conversion-oriented.
  - The pattern form uses a label, select, button, and message text.
  - CSS targets generic Aurora forms, Gravity Forms, and Jetpack/contact-form controls for label, focus, error, success, and disabled/loading states.

- [x] Footer supports primary utility IA and project network links.
  - Preserved existing Site/Projects/Utility columns and added a contained newsletter utility.

## Verification

```bash
git diff --check
php -l theme/kk-aurora/functions.php
php -l theme/kk-aurora/patterns/component-utility-system.php
jq empty theme/kk-aurora/theme.json
rg -n "aurora-(utility-grid|search-utility|newsletter-utility|form|empty-state|component-empty|is-loading|is-disabled)" theme/kk-aurora/style.css theme/kk-aurora/templates/404.html theme/kk-aurora/parts/footer.html theme/kk-aurora/patterns/component-utility-system.php
```

`make validate` is still blocked in this environment because `phpcs` is not installed.

Local browser smoke:

- Base URL: `http://localhost:10003`
- Home desktop/mobile returned `200`
- 404 desktop/mobile returned `404` with the Aurora 404 template rendered
- Footer newsletter utility was present on home and 404
- Search utility and search form were present on the 404 template
- No horizontal overflow was detected at `1440x1000` or `390x844`

Artifacts:

- `docs/current-state/aurora-smoke-2026-05-20/aurora-component-checks.json`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-components-404-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-components-404-mobile.png`

Full staging QA is still owned by issue `#86`, after this component lane merges.
