# Issue Swarm Roadmap - 2026-05-19

**Prepared:** 2026-05-19
**Last refreshed:** 2026-05-20 (UTC)
**Queue snapshot (as of 2026-05-20 04:49 UTC):** 67 open issues, 0 open PRs
**Scope:** Convert the current backlog into bounded parallel lanes with clear stop rules.

## Assumptions

1. Track B (Aurora) is the current demo-critical lane.
2. Track A issues should be draft-first and repo-first before production publish actions.
3. `needs-human-review` issues remain blocked unless explicitly unblocked by KK.

## Queue Baseline

- Open issues: `67`
- `auto-implement`: `51`
- `track-b` + `aurora-v2`: `13`
- `priority:high`: `31`
- `needs-human-review`: `3` (`#23`, `#75`, `#95`)
- `swarm-ready`: `17`
- `swarm-parked`: `11`

## Roadmap Issues Added

- `#95` `[CONTENT P0] Clear backup gate and create private AI media appearances WP draft` - blocked until a fresh full-site backup is available.
- `#96` `[AURORA P1] Refresh review packet and smoke artifacts after #87 merge` - closed after the refreshed review packet landed.
- `#97` `[QUEUE P2] Reconcile Aurora and legacy design issues after rewrite recovery` - closed after the legacy routing decision was recorded.
- `#98` `[DOCS] Refresh Aurora issue-swarm handoff after #87 merge` - closed after repo-local handoff docs were refreshed.
- `#99` `[CONTENT P2] Build next review-ready keynote source-pack draft batch` - Track A Wave 2 local draft prep.

## Canonical 72-Hour Swarm

### Lane 0 - Queue Control (first 4-6 hours)

Goal: remove ambiguity before implementation.

- Normalize canonical issue mappings (old design tickets to Aurora epics).
- Mark issues as `swarm-ready` vs `swarm-parked`.
- Keep `#23` and `#75` explicitly blocked for human review.

Primary issues:

- `#75`, `#23`, `#95`
- `#96`, `#97`, `#98`
- `#81-#86`
- legacy design set `#24-#35`

### Lane 1 - Aurora Wave 1 (parallel, Track B)

Goal: mechanical stability + visual system verification.

- `#96` `[AURORA P1] Refresh review packet and smoke artifacts after #87 merge`
- `#81` `[AURORA P1] Define the 2026 visual system`

Current status (2026-05-20):

- `#80` closed after PR `#94` merged into `aurora/v2`.
- `#81` closed after PR `#93` implementation evidence plus PR `#102` acceptance reconciliation.

Done when:

- P0 smoke and screenshot evidence are landed on `aurora/v2` (`AURORA-P0-STAGING-RESCUE-2026-05-19.md` + `aurora-smoke-2026-05-19/`).
- Visual-system checklist evidence is posted and issue `#81` is closed or left open with an explicit blocker.

### Lane 2 - Aurora Wave 2 (parallel, Track B)

Goal: homepage + Work/Speaking authority surfaces.

- `#82` media-led homepage
- `#83` Work/Speaking media templates

Current status (2026-05-20):

- `#82` closed after PR `#100` merged to `aurora/v2`.
- `#83` closed after PR `#101` merged to `aurora/v2`.

Done when:

- Responsive behavior is validated across mobile/tablet/desktop/wide.
- Media proof modules include fallback/alt/source behavior evidence.

### Lane 3 - Aurora Wave 3 + QA Gate (Track B)

Goal: long-form/template hardening, then final QA gate.

- `#84` long-form/media-heavy post templates
- `#85` restrained component library
- `#86` staging QA gate (final)

Done when:

- Component/state matrix exists.
- Long-form validation evidence is attached.
- QA packet confirms keyboard/focus/reduced-motion/contrast/perf readiness.

Current gate note (2026-05-20):

- `#84` closed after PR `#104` merged to `aurora/v2`.
- `#85` closed after PR `#103` inventory plus PR `#105` component implementation merged to `aurora/v2`.
- `#86` has local QA evidence from PR `#106` and remains open for real staging QA with production-like media, backup, and rollback evidence.

### Lane 4 - Track A Content Sprint (parallel after Aurora Wave 1)

Goal: high-impact content surfaces using draft-first workflow.

- `#65`, `#66`, `#67`, `#68`
- `#99` next review-ready keynote source-pack draft batch
- Supersede/merge intent from `#12`, `#16`, `#17` where duplicated

Done when:

- Draft artifacts are review-ready.
- No production publish writes were made without explicit approval.

### Lane 5 - Track A SEO/A11Y Quick Wins (parallel after Aurora Wave 1)

Goal: bounded improvements with clear verification.

- `#8`, `#9`, `#10`, `#36`, `#43`, `#48`

Done when:

- Each issue has a narrow proof artifact or patch.
- Any broad/refactor-shaped scope is split into smaller follow-up issues.

## Stop Rules

1. One lane, one track: never mix Track A and Track B edits in one branch.
2. Max two active implementation issues per lane at a time.
3. Every lane must produce artifacts before taking more scope.
4. No silent closure: close only when checklist evidence is attached.
5. `needs-human-review` stays blocked until explicit human approval.

## Current Labeling Convention

- `swarm-ready`: safe for bounded autonomous execution now
- `swarm-parked`: intentionally deferred / broad / dependency-heavy
- `swarm-wave-1`: Aurora Wave 1 + first Track A quick wins
- `swarm-wave-2`: second execution wave
- `swarm-wave-3`: final hardening/QA wave

## Notes

- Legacy design issues `#24-#35` remain open but routed; they are not standalone build targets.
- `docs/current-state/AURORA-ISSUE-SWARM-2026-05-19.md` now reflects Wave 1/2/3 progress through PRs `#93/#94/#100/#101/#102/#103/#104/#105/#106`.
- Media appearances are parked in `#95` until the fresh full-site backup gate is cleared; see `APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md`.
