# GitHub Queue Recovery — 2026-05-19

## Why this exists

The credential-history rewrite force-push (documented in `CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md`) auto-closed open PRs whose head/base commit ancestry changed.

This note records the queue recovery actions so reviewers have a clean audit trail.

## Recovery actions completed

1. Re-opened Aurora redesign review as replacement PR #87.
2. Rebuilt the sidebar promos lane from rewritten `main` as replacement PR #88 (old PR #73 branch was heavily diverged).
3. Fixed CI workflow gating in `.github/workflows/test-pr.yml` so WPCS install works with Composer allow-plugins.
4. Merged replacement PRs:
   - #87 -> `aurora/v2`
   - #88 -> `main`
5. Deleted temporary recovery branches after merge:
   - `codex/aurora-redesign-2026-05-18`
   - `codex/sidebar-promos-recovery-2026-05-19`
6. Added recovery comments on closed PRs #77 and #73 linking to their replacement merges.

## Current queue state after recovery

- Open PRs: none
- `main`: includes sidebar promos plugin + CI allow-plugins fix from PR #88
- `aurora/v2`: includes Aurora redesign merge from PR #87

## Remaining branch hygiene (manual decision)

Remote branches still present that were not touched in this recovery:

- `claude/automate-sidebar-graphics-55OBU`
- `claude/setup-wordpress-rebuild-KVLxh`

Recommend deciding whether to archive/delete these in a separate branch-hygiene pass.
