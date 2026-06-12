# Microsite Implementation Brief

## Goal

Build a standalone Next.js microsite that functions as a futuristic photo essay for the Becker x KK Vancouver World Cup 2026 AI fashion project. The site should be suitable for a separate repo such as `/Users/athena/code/world-cup-fashion-cake`, then later deployable to Vercel or another static-friendly host.

This source pack is the handoff. Do not implement the microsite inside `kriskrug-wp`.

## Recommended Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- Local static assets under `public/assets/`
- Static content module, for example `src/content/project.ts`
- Optional Framer Motion only if the build agent can keep motion restrained and performant

## Routes

- `/` - main photo essay.
- `/process` - optional process appendix with prompt workflow, mood boards, and motion-test notes.
- `/prompts` - prompt archive and calibration log.

The first implementation can ship only `/` if time is tight, as long as the content model leaves room for `/process` and `/prompts`.

## Content Model

Use a small typed content object rather than hard-coded page fragments:

- `site`: title, short title, dek, collaborator credits, canonical URL, social image.
- `chapters[]`: id, eyebrow, title, body, pull quote, asset IDs.
- `assets[]`: id, src, alt, caption, credit, status, promptId, chapterId.
- `prompts[]`: id, title, original prompt, calibration notes, selected asset IDs.
- `sources[]`: label, URL, use.

Asset statuses:

- `reference-only`
- `final-select`
- `process`
- `motion-test`

## Editorial Structure

1. **The Mood Board**
   - Establish Becker hair language: sculptural, severe, wind-carved, couture sports energy.
   - Use mood boards as process material only unless approved for public display.

2. **The Prompt Machine**
   - Explain the workflow: reference images, GPT/Claude prompts, Midjourney batches, Lightroom selects, motion tests.
   - Keep it concrete and fast. Avoid tool worship.

3. **Vancouver Match Fever**
   - Anchor the story in Vancouver's 2026 match days at BC Place.
   - Use rain, turf, floodlights, concrete, glass, mountains, and transit-night energy.

4. **Lost Angels Meets Vancouver**
   - Bring LA glamour into the Pacific Northwest: palm ghosts, red lips, wet pavement, stadium light, editorial flash.

5. **Army of Robots**
   - Close with the meta-story: two fashion-industry collaborators using AI as a creative studio, not a replacement for taste.

## Visual System

Direction:

- Full-bleed image-first layout.
- Editorial typography with tight rhythm, not a SaaS landing page.
- Dark base with stadium-white, rain-gray, turf-green, chrome-silver, and selective lipstick-red accents.
- Hard chapter cuts, visible image sequencing, no decorative gradient blobs.
- Use real image assets, not SVG hero illustrations.

Avoid:

- Official FIFA/World Cup/team/sponsor logos.
- Generic AI circuit-board visuals.
- Marketing hero-card layouts.
- Explaining the UI on screen.
- Overly cute sports metaphors.

## Required Components

- Full-viewport hero with final hero select.
- Sticky or minimal chapter navigation.
- Image sequence/gallery component that handles portrait and landscape images without layout shift.
- Pull-quote component for curated chat/process lines.
- Prompt card component for `/prompts` or inline prompt annotations.
- Video component for the motion test, muted and optional, with poster fallback.
- Footer with collaborator credits and image/provenance note.

## Accessibility And Performance

- Every image needs meaningful alt text before public release.
- Maintain readable text contrast over image overlays.
- Respect `prefers-reduced-motion`.
- Use optimized local images and avoid shipping huge originals.
- Verify desktop and mobile screenshots before handoff.

## Acceptance Criteria

- The microsite renders locally with no broken assets.
- The first viewport immediately signals fashion, Vancouver, World Cup 2026, and Becker x KK collaboration.
- The site uses final Midjourney selects when available and marks process/reference material clearly.
- The project can be deployed independently of WordPress.
- The source content can be updated without hunting through component markup.
- No live WordPress content is changed by the microsite build.

