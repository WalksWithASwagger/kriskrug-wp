# Aurora Issue Swarm - 2026-05-19

**Track:** B - Aurora v2 theme
**Scope:** GitHub issue hygiene, PR review packet, and next Track B work lanes.
**Production status:** No production WordPress writes. No theme activation. No merge to `main`.

## Summary

The January design tickets are no longer the right unit of work for the redesign. They were broad, generic, and still labeled `auto-implement`, which made them look ready for agents even though Aurora now has a more specific Track B direction.

This pass created the current Aurora epic layer and routed the old tickets into it.

## New Aurora Epics Filed

Filed from `issues-to-create/aurora-v2-redesign-epics.md`:

| Issue | Title | Purpose |
|---|---|---|
| #80 | [AURORA P0] Rescue staging header/nav render | First blocker: make Aurora mechanically reviewable on real WordPress content. |
| #81 | [AURORA P1] Define the 2026 visual system | Type, color, buttons, focus, glass rules, and motion tokens. |
| #82 | [AURORA P1] Build a media-led homepage | First-viewport brand authority, real media, project proof, responsive behavior. |
| #83 | [AURORA P1] Create Work and Speaking media templates | Reusable Work/Speaking modules for project proof and booking paths. |
| #84 | [AURORA P2] Upgrade long-form article and media-heavy post templates | Long-form reading, embeds, captions, galleries, related posts. |
| #85 | [AURORA P2] Build the restrained component library | Smaller component system without card-everything drift. |
| #86 | [AURORA P2] Run performance and accessibility QA on real staging | Reduced motion, keyboard nav, contrast, media loading, console capture. |

Created labels:

- `track-b`
- `aurora-v2`

## Old Design Tickets Routed

Issues #24 through #35 were updated:

- removed `auto-implement`
- added `track-b`
- added `aurora-v2`
- added a routing comment pointing to the controlling Aurora epic(s)

Current mapping:

| Old issue | Routed to |
|---|---|
| #24 Full Homepage Redesign | #82, #86 |
| #25 Modern Component Library | #85 |
| #26 Typography System Update | #81 |
| #27 Color Palette Refinement | #81 |
| #28 Navigation Redesign | #80, #86 |
| #29 Footer Redesign | #85 |
| #30 Photography Showcase Component | #82, #83 |
| #31 Project Card Design Pattern | #82, #83 |
| #32 Form Design Updates | #85 |
| #33 Mobile-First Responsive System | #80, #86 |
| #34 Hero Section Visual Treatment | #82 |
| #35 CTA Button Design System | #81, #85 |

Verification after routing:

- open `aurora-v2` issues: 19
- old design issues #24-#35 still carrying `auto-implement`: 0

## PR State

Open PRs after refresh:

| PR | State | Read |
|---|---|---|
| #77 `[codex] Redesign Aurora visual system` | Draft, clean, base `aurora/v2` | This is the active Aurora review surface. Keep draft until human review and next polish pass. |
| #73 `Auto-managed sidebar promos` | Open, merge state `DIRTY`, base `main` | Keep parked. It is production-adjacent plugin work and needs its own staging/backup/deploy lane. |

## Aurora Review Packet

PR #77 branch: `codex/aurora-redesign-2026-05-18`
Worktree: `/Users/kk/Code/kriskrug-wp-aurora-redesign`

Branch-only review docs and screenshots:

- `docs/current-state/AURORA-REDESIGN-SMOKE-2026-05-18.md`
- `docs/current-state/AURORA-TOMORROW-ROADMAP-2026-05-19.md`
- `docs/current-state/aurora-smoke-2026-05-18/aurora-home-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-18/aurora-home-mobile.png`

Important: those files currently live on PR #77's branch, not on `main`.

Review read:

- Desktop screenshot is much closer to the desired direction: real photo-led hero, clear first-viewport identity, high-contrast nav, and obvious booking CTA.
- Mobile screenshot needs polish before calling it review-ready: header/nav takes a lot of vertical space, the hero crop cuts off awkwardly, and the final proof chips run below the screenshot edge.
- The smoke report says imagery is still temporary/borrowed and needs a final KK media source of truth before production planning.

## Next Agent Lanes

Run Track B work in isolated Aurora worktrees only.

1. **#80 P0 staging rescue:** confirm current PR #77 header/nav state against Local, fix mobile/header density and any desktop regressions, then rerun six-page smoke.
2. **#82 homepage polish:** choose final hero media, tighten mobile crop, validate CTA hierarchy.
3. **#81 visual system:** document tokens, focus states, glass usage, and motion rules before adding more effects.
4. **#86 QA:** capture browser console, reduced-motion behavior, keyboard nav, and desktop/mobile screenshots.

Do not:

- activate Aurora on production,
- merge Aurora into `main`,
- use old #24-#35 tickets as standalone automation work,
- close old design tickets until the new epic acceptance criteria are actually met.
