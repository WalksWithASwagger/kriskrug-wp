# Promo Graphic Specs

Keep these consistent and the sidebar will look like a system instead of a scrapbook.

## Dimensions

| Use case            | Size        | Aspect | Notes                                               |
| ------------------- | ----------- | ------ | --------------------------------------------------- |
| Sidebar default     | 800 × 600   | 4:3    | What the widget renders (`aspect-ratio: 4 / 3`).    |
| Square (alt layout) | 800 × 800   | 1:1    | If you switch the CSS aspect later.                 |
| Retina source       | 1600 × 1200 | 4:3    | Export at 2× so it stays sharp on high-DPI screens. |

Save as JPG (~80% quality) for photos, PNG for flat illustrations. Keep each under ~150 KB if possible.

## Layout rules

- **Title-safe area:** keep critical text inside the centre 80% of the image.
- **Top-left corner** is reserved — that's where the "X days left" badge sits on Featured promos.
- **Don't bake in a CTA button.** The widget renders the CTA text and arrow separately.

## Brand guardrails

- Use the existing site type stack — no novel display fonts per promo.
- Pick one accent color per **tone**:
  - Event → blue
  - Course → purple
  - Community → green
  - Default → site primary
- High contrast on any text overlay (WCAG AA at minimum).

## Templates to set up once

Create one template per tone in Canva/Figma with:
- Title slot (≤ 5 words)
- Subtitle slot (≤ 8 words)
- Background image area
- Brand mark in a fixed corner

Then producing a new promo is just "duplicate template, swap text and image." That's the change-them-more-often part.

## Naming convention for uploads

`promo-{slug}-{yyyymmdd}.jpg` — e.g. `promo-rap-cohort-2-20260601.jpg`.

Makes it obvious in the media library which promo it belongs to and when it was made.
