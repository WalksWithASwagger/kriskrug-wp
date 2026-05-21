# Issue #10 CTA Hover States Deployment Notes

## Scope

Repo-side CSS artifact only. No live WordPress writes were made.

`fixes/issue-10-cta-hover-states.css` is intended for Appearance -> Customize -> Additional CSS or a CSS snippet after the backup/restore proof gate is satisfied.

## Selector Evidence

- `.kk-button` appears in the May page snapshots for Work, About, and Speaking, plus the current keynotes source-pack payloads.
- `.kk-home-button` appears in `content/source-packs/keynotes-2026/wp-payloads/homepage-hero.html`.
- `.kk-services-button` appears in `content/source-packs/keynotes-2026/wp-payloads/services.html`.
- `.wp-block-button__link` and `.wp-element-button` appear in public raw captures for WordPress block buttons, Contact, and subscription CTAs.
- `.button`, `.btn`, and `input[type="submit"]`/`button[type="submit"]` cover the older prepared snippets and Catch Responsive form buttons.
- `.more-link` gets link-style hover/focus treatment only, because public Blog snapshots render it as a text CTA rather than a filled button.

## Deployment

1. Confirm the production backup/restore proof gate is complete.
2. In WordPress Admin, open Appearance -> Customize -> Additional CSS, or use the approved CSS snippet deploy path.
3. Paste the full contents of `fixes/issue-10-cta-hover-states.css` after existing button/color CSS.
4. Publish the CSS change.
5. Hard-refresh the tested pages to avoid cached CSS hiding the result.

## Verification

- Desktop hover: on About, Work, Speaking, Services, Contact, and one post page, hover primary CTAs and confirm the button darkens, lifts slightly, and transitions smoothly.
- Keyboard focus: tab through each page until CTA buttons receive focus; confirm the blue focus ring is visible and not clipped.
- Active state: press and hold a CTA with mouse/trackpad; confirm it returns to baseline instead of staying lifted.
- Mobile touch: on a coarse pointer device or emulator, tap primary and secondary CTAs; confirm pressed feedback without relying on hover.
- Contrast spot-checks used by this patch:
  - `#ffffff` on `#003A99`: 10.17:1.
  - `#ffffff` on `#002F7A`: 12.44:1.
  - `#0052CC` focus ring on white: 6.82:1.
  - `#ffffff` on `#171717`: 17.93:1.
- Reduced motion: with reduced motion enabled, confirm buttons still change state without animated transition.

## Closure Recommendation

Keep issue #10 open until the CSS is deployed after backup proof and verified in browser on desktop and mobile. After deploy evidence is attached, close as a Track A current-site UX fix.
