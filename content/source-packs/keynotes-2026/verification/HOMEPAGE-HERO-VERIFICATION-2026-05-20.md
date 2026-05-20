# Homepage Hero Verification - 2026-05-20

## Scope

- Track A content/copy package only.
- No live WordPress write, media upload, theme edit, or production activation performed in this pass.
- Target page for future publish: page ID `3930`, slug `empowering-events-organizations-for-the-ai-age`, public URL `https://kriskrug.co/`.
- New payload: `content/source-packs/keynotes-2026/wp-payloads/homepage-hero.html`.
- Metadata pointer updated: `content/source-packs/keynotes-2026/wp-payloads/page-meta.json`.

## Current Homepage Extraction

- XML export source: `/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml`.
- Current front page item starts around line `161660`.
- Current page ID is `3930`; it renders at `https://kriskrug.co/`.
- Current hero/body starts with:
  - `I believe in the power of connection.`
  - `not just about revealing moments through photographs or managing social media feeds`
  - `a patchwork quilt of creative awesomeness`
- The current page is still rooted in event photography, digital engagement, social media, and older services positioning.
- The separate `/home/` page ID `2315` is the old `Recent Posts & Updates:` latest-posts page and was not targeted.

## What Changed

- Added a paste-ready homepage hero block that leads with:
  - `Bridging art, AI, Indigenous wisdom, and justice.`
  - Community-serving technology instead of extraction.
  - Equal role badges for BC + AI Ecosystem, Indigenomics AI, and The Upgrade AI.
  - Primary CTA: `Explore My Work` -> `/recent-projects-include/`.
  - Secondary CTA: `Let's Connect` -> `/contact/`.
- De-emphasized photography by moving the frame to 20+ years of art, technology, media, and community work.
- Kept the tone professional, warm, and direct.

## Metric Grounding

- The issue text requested `2,000+ members`, `Fortune 500`, and `$200B`; public/source-backed evidence in this pass supports different wording.
- BC + AI live stats checked at `https://bc-ai.ca/` on 2026-05-20:
  - `250+` members.
  - `3,000+` event attendees.
  - `94+` events hosted.
  - `4` BC regions.
- Older XML/source material supports `13 monthly meetups with over 2,000 total attendees` as a 2024 historical attendee stat, not a current member count.
- Indigenomics public post supports the dashboard, sovereign-data framing, and Carol Anne Hilton's `$100 billion Indigenous economy` vision.
- The Upgrade live site supports live/on-demand courses, coaching, team trainings, certification cohorts, and visible enterprise/global-brand logo proof. The hero uses `Enterprise teams` rather than an unqualified `Fortune 500` claim.

## Issue Comment Copy

Posted to issue `#66`: `https://github.com/WalksWithASwagger/kriskrug-wp/issues/66#issuecomment-4495271077`.

Use this concise comment on issue `#66`:

```md
Drafted the ready-to-implement homepage hero package in `content/source-packs/keynotes-2026/wp-payloads/homepage-hero.html`.

Recommended hero:

**Bridging art, AI, Indigenous wisdom, and justice.**

I build technology programs, communities, keynotes, and learning systems that serve people instead of extraction. My work connects creative practice, responsible AI, Indigenous economic sovereignty, and the messy human work of building trust.

Roles:
- BC + AI Ecosystem: Executive Director building responsible, inclusive AI infrastructure across British Columbia.
- Indigenomics AI: CTO work around sovereign data, economic evidence, and Indigenous-led technology futures.
- The Upgrade AI: Co-founder helping professionals and teams build practical AI fluency without losing judgment or taste.

Impact markers:
- 250+ BC + AI members
- 3,000+ BC + AI event attendees
- 94+ community events hosted
- $100B Indigenous economy vision supported through Indigenomics AI
- 20+ years bridging art, technology, media, and community
- Enterprise teams trained/coached through The Upgrade AI

CTAs:
- Explore My Work -> `/recent-projects-include/`
- Let's Connect -> `/contact/`

Note: I used current source-backed stats instead of the stale/mislabeled `2,000+ members`, `Fortune 500`, and `$200B` wording. Verification is in `content/source-packs/keynotes-2026/verification/HOMEPAGE-HERO-VERIFICATION-2026-05-20.md`.
```

## Verification

- External URL check from `homepage-hero.html`: all links returned `200`.
- Payload privacy scan: no sensitive-string matches found in `homepage-hero.html`.
- Content marker checks found:
  - `Bridging art, AI, Indigenous wisdom, and justice.`
  - `BC + AI Ecosystem`
  - `Indigenomics AI`
  - `The Upgrade AI`
  - `250+`
  - `3,000+`
  - `94+`
  - `$100B`
  - `Explore My Work`
  - `Let's Connect`

## Publish Gate

Before applying this hero to live page ID `3930`, follow the repo live-write rules:

1. Take a fresh backup or stop.
2. Snapshot page ID `3930` to rollback JSON/HTML.
3. Verify REST target fields: `id=3930`, slug `empowering-events-organizations-for-the-ai-age`, public link `https://kriskrug.co/`.
4. Insert the hero before the existing page content, or replace the existing top copy only after KK approval.
5. REST-read back title, slug, status, comment settings, SEO meta, and content markers.
6. Browser-check desktop and mobile after publish.
