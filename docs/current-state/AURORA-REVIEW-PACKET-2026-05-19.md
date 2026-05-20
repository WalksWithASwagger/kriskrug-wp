# Aurora Review Packet - 2026-05-19

Track: B - Aurora v2 theme
Branch: `codex/aurora-redesign-2026-05-18`
PR: `#77`

Status update: PR `#77` was superseded after the 2026-05-19 credential-history rewrite. The replacement PR `#87` merged this design direction into `aurora/v2`. For the current P0 header/nav rescue evidence, use `AURORA-P0-STAGING-RESCUE-2026-05-19.md`.

## Purpose

Use this packet to get fast human feedback on whether Aurora is moving in the right personal-brand direction before deeper implementation continues.

This is not a production cutover review. It is a design-direction review for brand fit, story hierarchy, media, motion, and mobile feel.

## Current Preview

Primary reviewer URL, when the Local app is running:

`http://kriskrug-local.local`

QA fallback used by this run:

`http://localhost:10003`

Why the fallback matters: this runner could reach Local on `localhost:10003`, but not on `kriskrug-local.local`. For browser QA only, the local WordPress `home` and `siteurl` options were temporarily switched to `http://localhost:10003`, then restored to `http://kriskrug-local.local`.

Local DB backup before the temporary URL switch:

`/tmp/kriskrug-local-before-aurora-review-20260518-2342.sql`

## Fresh Screenshot Evidence

- Desktop: `docs/current-state/aurora-review-2026-05-19/aurora-home-desktop-live.png`
- Mobile: `docs/current-state/aurora-review-2026-05-19/aurora-home-mobile-live.png`
- Smoke JSON: `docs/current-state/aurora-review-2026-05-19/smoke.json`

Marker check from this run:

```json
{
  "hero": 1,
  "signalStrip": 1,
  "workGrid": 1,
  "footer": 1,
  "stylesheets": 1
}
```

## What Looks Promising

- The hero finally feels like a real personal-brand signal instead of a generic AI template.
- The photo direction is strong: stage presence, bias wall, and community-room energy do more work than abstract AI visuals.
- The headline has enough ambition and specificity to anchor a premium redesign.
- The top nav and booking CTA are clear on desktop.
- The homepage has the right sections for the first review pass: hero, proof strip, work grid, speaking band, writing feed, and final CTA.

## Review Concerns To Test With Humans

- Mobile header density: the stacked nav consumes a lot of first-viewport height before the hero.
- Mobile hero crop: the face/photo composition is dramatic, but the right side can feel tight on narrower screens.
- CTA visibility: on desktop, the primary hero CTAs sit close to the bottom edge of the first viewport; on mobile, they begin below the first fold.
- Media authenticity: borrowed/external imagery must be replaced with final KK-owned or approved photo/video assets before production.
- Motion bar: current motion is restrained. Reviewers should say whether the site needs more cinematic scroll/morphing interaction or whether this is already the right amount.

## Questions For Reviewers

1. Does this immediately feel like Kris Krug in 2026?
2. Does the first viewport sell AI speaker, creative technologist, community builder, and photographer without feeling overloaded?
3. Is the hero image the right emotional direction, or should Aurora lead with a different photo/video moment?
4. Are the labels `Book Kris` and `Explore the work` the right primary paths?
5. Does mobile feel premium, or does the nav need to collapse into a tighter menu?
6. What feels too generic, too loud, too quiet, or too AI-template?
7. What media would make this unmistakably KK?

## Recommended Next Implementation Slice

Do this only after the first feedback pass:

1. Tighten mobile header/nav into a premium compact pattern.
2. Move or duplicate the primary CTAs so one clear action is visible in the first mobile viewport.
3. Replace placeholder/borrowed media with final KK-owned assets.
4. Add one video or motion module only where it strengthens the personal-brand proof.
5. Re-smoke home, About, Speaking, Work, and two long-form posts.

## Stop Rules

- Do not use PR `#77` for current decision-making; it was superseded by PR `#87`.
- Do not merge Aurora into `main`; Track B merges to production are cutover events.
- Do not activate Aurora on production.
- Do not do Track A content edits from the Aurora branch.
