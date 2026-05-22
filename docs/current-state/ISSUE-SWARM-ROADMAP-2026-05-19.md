# Issue Swarm Roadmap - 2026-05-19

**Prepared:** 2026-05-19
**Last refreshed:** 2026-05-21 (post-PR `#113` and branch cleanup)
**Queue snapshot (as of 2026-05-21):** 63 open issues, 0 open PRs
**Scope:** Convert the current backlog into bounded parallel lanes with clear stop rules.

## Assumptions

1. Track B (Aurora) is the current demo-critical lane.
2. Track A issues should be draft-first and repo-first before production publish actions.
3. `needs-human-review` issues remain blocked unless explicitly unblocked by KK.

## Queue Baseline

- Open issues: `63`
- `auto-implement`: `47` (historical readiness label; does not start the parked Agent PR Generator)
- `track-b` + `aurora-v2`: `13`
- `priority:high`: `28`
- `needs-human-review`: `3` (`#23`, `#75`, `#95`)
- `swarm-ready`: `13`
- `swarm-parked`: `11`
- `swarm-wave-1`: `7`
- `swarm-wave-2`: `4`
- `swarm-wave-3`: `2`
- Open PRs: `0`
- Branch hygiene: merged remote `codex/swarm-*` branches from PRs `#102`-`#106` were deleted; only `main` and `aurora/v2` remain as remote heads.

## Swarm Launch Protocol

Use this before assigning agents:

1. Run `git fetch --prune`, `gh pr list --state open --limit 50`, `gh issue list --state open --limit 200`, and `git worktree list --porcelain`.
2. Keep the main checkout clean; create one isolated worktree per lane.
3. If PRs appear, inspect checks, draft state, scope, and issue linkage before editing.
4. Do not start `needs-human-review`, live WordPress, or Aurora activation work without the relevant target checks, rollback plan, and human approval.
5. Leave concise GitHub breadcrumbs for start, blocker, fix, and final state.

## Roadmap Issues Added

- `#95` `[CONTENT P0] Clear backup gate and create private AI media appearances WP draft` - backup gate retired; private create-only draft work can proceed after dry-run and slug checks. Public publish still needs KK review and a rollback note.
- `#96` `[AURORA P1] Refresh review packet and smoke artifacts after #87 merge` - closed after the refreshed review packet landed.
- `#97` `[QUEUE P2] Reconcile Aurora and legacy design issues after rewrite recovery` - closed after the legacy routing decision was recorded.
- `#98` `[DOCS] Refresh Aurora issue-swarm handoff after #87 merge` - closed after repo-local handoff docs were refreshed.
- `#99` `[CONTENT P2] Build next review-ready keynote source-pack draft batch` - Track A Wave 2 local draft prep.

## Canonical 72-Hour Swarm

### Lane 0 - Queue Control (first 4-6 hours)

Goal: remove ambiguity before implementation.

- Normalize canonical issue mappings (old design tickets to Aurora epics).
- Mark issues as `swarm-ready` vs `swarm-parked`.
- Keep `#23`, `#75`, and public/destructive parts of `#95` explicitly blocked for human review, target checks, and rollback notes. Private create-only draft review can proceed with dry-run and slug checks.
- Keep branch cleanup evidence in the handoff before deleting more refs.

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
- `#86` has local QA evidence from PR `#106` and remains open for real staging QA with production-like media, backup, and rollback evidence. Do not treat it as a generic quick-win issue.

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
- No lane performs public publish, existing-content updates, destructive cleanup, plugin/theme/schema/robots changes, media-heavy imports, bulk writes, or `--update` without target checks, rollback notes, and explicit deploy intent. Private create-only drafts for review are allowed with dry-run and slug checks.

### Lane 6 - Duplicate and shipped-scope reconciliation

Goal: reduce queue noise before another broad wave.

- Verify whether `#3`, `#12`, and `#16` are already satisfied by merged work; close only with evidence.
- Consolidate Work/Projects scope across `#17` and `#68`.
- Consolidate photography/archive scope across `#21`, `#30`, and `#59`.

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

Note: `auto-implement` is now a historical intent label only. `agent-pr-generator.yml` no longer auto-runs from that label.

## Notes

- Legacy design issues `#24-#35` remain open but routed; they are not standalone build targets.
- `docs/current-state/AURORA-ISSUE-SWARM-2026-05-19.md` now reflects Wave 1/2/3 progress through PRs `#93/#94/#100/#101/#102/#103/#104/#105/#106`.
- Media appearances in `#95` are unparked for private create-only draft review after dry-run and slug checks; public publish still needs KK review and a rollback note. See `APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md` for the older blocked state.
- PR `#113` satisfies the Feature/category routing slice of the publishing-trust gate, but `#75` remains open for credential, scan, inventory, and publish sign-off evidence.
