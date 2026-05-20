# Aurora Issue Swarm - 2026-05-19

**Track:** B - Aurora v2 theme
**Scope:** GitHub issue hygiene, PR review packet, and next Track B work lanes.
**Production status:** No production WordPress writes. No theme activation. No merge to `main`.
**Refresh:** 2026-05-20 queue + merge reconciliation pass (through PR `#106`).

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

- open `aurora-v2` issues: 14
- old design issues #24-#35 still carrying `auto-implement`: 0

## PR State (post-rewrite recovery)

The old open-PR references are superseded:

- Aurora redesign was recovered as replacement PR `#87` and merged into `aurora/v2`.
- Wave 1 implementation landed through PR `#93` to `aurora/v2`.
- P0 staging rescue landed through PR `#94` to `aurora/v2` and issue `#80` is now closed.
- Wave 2 homepage lane landed through PR `#100` and issue `#82` is now closed.
- Wave 2 Work/Speaking templates lane landed through PR `#101` and issue `#83` is now closed.
- Visual-system acceptance reconciliation landed through PR `#102` and issue `#81` is now closed.
- Component inventory foundation landed through PR `#103`.
- Long-form template lane landed through PR `#104`; issue `#84` is now closed.
- Restrained component library implementation landed through PR `#105`; issue `#85` is now closed.
- Local Aurora QA packet landed through PR `#106`; issue `#86` remains open for real staging QA, production-like media, and backup/rollback evidence.
- Sidebar promos was recovered as replacement PR `#88` and merged into `main`.
- Queue recovery and follow-through are documented in:
  - `docs/current-state/GITHUB-QUEUE-RECOVERY-2026-05-19.md`
  - `docs/current-state/TOMORROW-ROADMAP-2026-05-20.md`

## Aurora Review Packet

Merged Aurora evidence now lives on `aurora/v2` and is no longer tied to old PR `#77`.

Current review anchors:

- `docs/current-state/AURORA-P0-STAGING-RESCUE-2026-05-19.md`
- `docs/current-state/AURORA-SWARM-81-VISUAL-SYSTEM-2026-05-19.md`
- `docs/current-state/AURORA-REVIEW-PACKET-2026-05-19.md`
- `docs/current-state/aurora-smoke-2026-05-19/aurora-home-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-19/aurora-home-mobile.png`
- `docs/current-state/aurora-smoke-2026-05-19/aurora-home-metrics.json`
- `docs/current-state/aurora-smoke-2026-05-19/aurora-accessibility-checks.json`
- `docs/current-state/AURORA-SWARM-82-SMOKE-2026-05-20.md`
- `docs/current-state/AURORA-SWARM-83-TEMPLATES-2026-05-20.md`
- `docs/current-state/AURORA-COMPONENT-INVENTORY-2026-05-20.md`
- `docs/current-state/AURORA-SWARM-84-LONGFORM-2026-05-20.md`
- `docs/current-state/AURORA-SWARM-85-COMPONENTS-2026-05-20.md`
- `docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-work-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-work-mobile.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-speaking-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-speaking-mobile.png`
- `docs/current-state/aurora-qa-2026-05-20/aurora-qa-checks.json`

Review read:

- Desktop screenshot is much closer to the desired direction: real photo-led hero, clear first-viewport identity, high-contrast nav, and obvious booking CTA.
- Mobile screenshot needs polish before calling it review-ready: header/nav takes a lot of vertical space, the hero crop cuts off awkwardly, and the final proof chips run below the screenshot edge.
- The smoke report says imagery is still temporary/borrowed and needs a final KK media source of truth before production planning.

## Next Agent Lanes

Run Track B work in isolated Aurora worktrees only.

1. **#86 real staging QA gate:** use PR `#106` as the local baseline, then rerun screenshots, keyboard/focus, reduced-motion, contrast, console/media, and performance checks on a staging surface with production-like media.
2. **Backup/rollback gate:** confirm a fresh backup and rollback path before any production theme activation or merge-to-main cutover.
3. **Queue truth refresh:** keep `docs/current-state/` lane docs aligned with live issue/PR state after each merge.

Do not:

- activate Aurora on production,
- merge Aurora into `main`,
- use old #24-#35 tickets as standalone automation work,
- close old design tickets until the new epic acceptance criteria are actually met.
