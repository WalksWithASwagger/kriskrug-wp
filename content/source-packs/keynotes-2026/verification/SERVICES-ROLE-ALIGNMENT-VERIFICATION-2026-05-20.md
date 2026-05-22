# Services Role Alignment Verification - 2026-05-20

Issue: https://github.com/WalksWithASwagger/kriskrug-wp/issues/67
Issue comment: https://github.com/WalksWithASwagger/kriskrug-wp/issues/67#issuecomment-4500142718

## Status

Prepared, committed locally, and ready for publication review. No live WordPress write was made in this pass.

## Target

- Page ID: `2666`
- Current slug: `generative-ai-services`
- Current public URL: `https://kriskrug.co/generative-ai-services/`
- Current live title readback: `Generative AI Creative Services & Strategy`
- Proposed title: `AI Services, Training & Strategy`
- Proposed payload: `content/source-packs/keynotes-2026/wp-payloads/services.html`
- Proposed metadata: `content/source-packs/keynotes-2026/wp-payloads/page-meta.json`

## Source Grounding

- Current Services page was extracted from `docs/current-state/raw/pages/generative-ai-services.html`.
- Public REST readback confirmed page ID `2666`, slug `generative-ai-services`, status `publish`, and link `https://kriskrug.co/generative-ai-services/`.
- Current live page content is heavily weighted toward media, photography, older generic AI consulting, creative workshops, Discord/community management, and photography/video production.
- BC+AI source check confirmed public site positioning and stats:
  - `250+` members
  - `3,000+` event attendees
  - `94+` events hosted
  - `4` BC regions
- The Upgrade AI source check confirmed public positioning around live/on-demand courses, 1:1 and group coaching, team trainings, Creative Pros, PR/Communications Pros, and Sales Leaders.
- Indigenomics AI public post check confirmed the dashboard, sovereign data governance, and the `$100 billion Indigenous economy` frame.

## Content Changes Prepared

- Reframed Services from a photography/media-first page into a current 2026 offer around AI capacity, community strategy, training, Indigenomics advisory, and speaking/workshops.
- Added five service categories:
  - `AI Strategy Consulting`
  - `Community & Ecosystem Building`
  - `The Upgrade AI Training`
  - `Indigenomics Advisory`
  - `Keynotes, Workshops & Executive Briefings`
- Each service category includes:
  - ideal-client language
  - what the service does
  - practical outcomes
  - a direct CTA
- Added engagement models instead of invented pricing:
  - Advisory Sprint
  - Team Training / Cohort
  - Ecosystem Buildout
  - Keynote + Workshop
- Added social proof:
  - BC+AI public ecosystem stats
  - Indigenomics `$100B` economy context
  - existing named Holly Rosenfeld quote from the current page
  - source links to BC+AI, The Upgrade AI, Indigenomics AI, Speaking, Work, and About
- Added a clear photography de-emphasis section: photography remains available when it strengthens an event, training, community program, archive, or campaign, but is no longer the center of the offer.

## SEO Metadata Prepared

```json
{
  "id": 2666,
  "slug": "generative-ai-services",
  "title": "AI Services, Training & Strategy",
  "comment_status": "closed",
  "ping_status": "closed",
  "content_file": "services.html",
  "meta": {
    "jetpack_seo_html_title": "AI Services, Training & Strategy | Kris Krüg",
    "advanced_seo_description": "AI strategy, responsible AI consulting, BC+AI community building, The Upgrade AI training, Indigenomics advisory, and keynote/workshop support with Kris Krüg."
  }
}
```

## Checks Run

- `python3 -m json.tool content/source-packs/keynotes-2026/wp-payloads/page-meta.json` passed.
- `git diff --check` passed.
- Sensitive-string scan across the payload, metadata, checklist, README, and asset-manifest changes returned no matches for the requested sensitive/privacy patterns.
- Temporary Notion/cloud-asset scan returned no matches.
- Content marker checks passed for:
  - `AI Strategy Consulting`
  - `Community &amp; Ecosystem Building`
  - `The Upgrade AI Training`
  - `Indigenomics Advisory`
  - `Keynotes, Workshops &amp; Executive Briefings`
  - `Engagement Models`
  - `Where Photography Fits Now`
  - `Start a conversation`

## URL Checks

All returned `200`:

- `https://bc-ai.ca/`
- `https://www.theupgrade.ai/`
- `https://kriskrug.co/contact/`
- `https://kriskrug.co/speaking/`
- `https://kriskrug.co/recent-projects-include/`
- `https://kriskrug.co/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/`
- `https://kriskrug.co/podcast-guesting-page-epk/`
- `https://kriskrug.co/about/`
- `https://kriskrug.co/generative-ai-services/`
- `https://kriskrug.co/work/` redirected to `https://kriskrug.co/recent-projects-include/`

## Media Checks

All selected image URLs returned `200` with image content types:

- `https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1`
- `https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg?w=1200&ssl=1`
- `https://i0.wp.com/kriskrug.co/wp-content/uploads/2025/04/image-19.png?w=1200&ssl=1`
- `https://i0.wp.com/kriskrug.co/wp-content/uploads/2025/07/ai-courses-workshops-trainings.png?w=1200&ssl=1`
- `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg?w=1200&ssl=1`
- `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-25-scaled.jpg?w=1200&ssl=1`

## Publish Gate

Before any live WordPress update:

1. Capture the relevant page snapshots or get explicit KK approval for a narrower rollback path.
2. Snapshot page ID `2666` to JSON and HTML.
3. Dry-run the REST payload.
4. Patch only page `2666` after slug readback confirms `generative-ai-services`.
5. Recheck title, slug, status, SEO meta, comment status, ping status, page content markers, URL status, and image URLs.
