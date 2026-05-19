# Aurora Redesign Smoke Report - 2026-05-18

Track: B - Aurora v2 theme  
Branch: `codex/aurora-redesign-2026-05-18`  
Worktree: `/Users/kk/Code/kriskrug-wp-aurora-redesign`

## Scope

This pass turns the Aurora v2 prototype from a rudimentary theme shell into a photo-led personal brand surface:

- Rebuilt the header and footer as stable custom HTML parts.
- Reworked the front page/home template around a large photographic hero, proof strip, project cards, speaking band, writing feed, and final CTA.
- Added a matching `front-page.html` because the Local site is configured with a static front page.
- Upgraded the page and single-post templates for premium long-form reading.
- Added the main Aurora design layer to `style.css` and explicitly enqueued it from `functions.php`.
- Removed negative letter-spacing values from the theme surface.

## 2026 Benchmark Read

This is a May 18, 2026 pre-summer scan, so the benchmark is current-state 2026 rather than a claim about the future summer market.

Sources checked:

- Webflow, 2026 trends: dynamic text treatments, guided scrolling, and intentional interaction design as ways to earn attention without overwhelming the reader. <https://webflow.com/blog/web-design-trends-2026>
- Squarespace, 2026 examples: tactile digital design, glassmorphism, motion narrative, and modular card systems for personal story and creator/consultant sites. <https://www.squarespace.com/blog/web-design-trends>
- Creative Bloq, 2026 graphic design trends: human craft, tactile imperfection, multisensory identity, and type as a primary brand vehicle. <https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026>
- Line25, 2026 guide: controlled glassmorphism as depth hierarchy, idiosyncratic anti-template attitude, and micro-interactions as a quality signal. <https://line25.com/articles/web-design-trends-2026/>

Design translation for Aurora:

- Lead with real KK photos and evidence, not abstract AI gloss.
- Use glass effects only where they clarify hierarchy and interactivity.
- Treat the hero headline and editorial typography as core brand assets.
- Keep motion purposeful: reveal, guide, and reward attention rather than decorating every surface.
- Preserve a human-made, field-notes sensibility so the site feels like Kris, not a generic AI speaker template.

## Local Safety

No production writes were made.

Local theme backup before sync:

`/tmp/kk-aurora-local-before-redesign-20260518-120450.tgz`

Local database backup before temporary QA URL rewrite:

`/tmp/kriskrug-local-before-aurora-url-qa-20260518-122500.sql`

The Local WordPress `home` and `siteurl` options were temporarily set to `http://127.0.0.1:10003` so headless screenshots could load same-origin assets. They were restored to:

`http://kriskrug-local.local`

## Preview

Local preview:

`http://kriskrug-local.local`

Screenshot artifacts:

- `docs/current-state/aurora-smoke-2026-05-18/aurora-home-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-18/aurora-home-mobile.png`

Next-session roadmap:

`docs/current-state/AURORA-TOMORROW-ROADMAP-2026-05-19.md`

## Smoke Results

Local HTTP checks:

```text
200 /
200 /about/
200 /speaking/
200 /recent-projects-include/
200 /2026/05/15/your-taste-is-your-moat/
200 /2026/05/16/make-culture-not-content/
```

Markup checks:

- Home includes `kk-aurora-style-css`.
- Home includes `aurora-hero-2026`, `aurora-signal-strip`, `aurora-work-grid`, and `aurora-footer-2026`.
- Single post includes `aurora-single-2026`, `aurora-reading-progress`, `aurora-author-panel`, and `Keep reading`.

Static checks:

```text
jq empty theme/kk-aurora/theme.json
php -l theme/kk-aurora/functions.php
git diff --check
rg -n 'letter-spacing:\s*-|"letterSpacing"\s*:\s*"-' theme/kk-aurora
```

The first three passed. The negative letter-spacing search returned no matches.

## Known Follow-Ups

- Replace borrowed/external imagery with the final KK photo/video asset set once selected.
- Add the actual video layer or reels module after the media source of truth is chosen.
- Expand motion beyond CSS reveal/hover states only after we decide how much animation belongs in the production theme.
- Run a second review with human eyeballs on brand fit, story hierarchy, and mobile polish.
