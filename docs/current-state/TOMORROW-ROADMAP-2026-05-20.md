# Tomorrow Roadmap - 2026-05-20

**Prepared after:** 2026-05-19 credential-history rewrite execution, queue recovery, and merge pass
**Last refreshed:** 2026-05-20 (UTC, post PR `#103/#104`)
**Use for:** Next operating session (date can drift; treat as next-session plan)
**Tracks:** Track A on `main`; Track B on `aurora/v2`

## Where We Ended (Verified)

1. Credential-history rewrite is complete and documented:
   - `CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md`
2. Post-rewrite PR recovery is complete and documented:
   - `GITHUB-QUEUE-RECOVERY-2026-05-19.md`
3. Replacement PR merges:
   - `#87` merged to `aurora/v2` (Aurora redesign lane)
   - `#88` merged to `main` (KK Sidebar Promos plugin + CI fix)
   - `#89` merged to `main` (queue-recovery documentation)
4. Open PR queue: none.
5. Branch hygiene follow-through completed:
   - Remaining `claude/*` remotes were deleted after local backup refs were created.
   - Aurora side worktrees were repointed to fresh branches off `origin/aurora/v2`.
6. Current remote branches:
   - `origin/main`
   - `origin/aurora/v2`
7. Issue-swarm roadmap landed:
   - PR `#92` merged to `main`
   - `docs/current-state/ISSUE-SWARM-ROADMAP-2026-05-19.md`
8. Media appearances WP draft is prepared but not created:
   - Local package: `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/`
   - Blocker note: `content/source-packs/keynotes-2026/verification/APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md`
   - Reason: fresh full-site backup gate was not satisfied, so no live WordPress write happened.
   - GitHub issue: `#95`
9. Aurora Wave 1 state after queue reconciliation:
   - PR `#93` merged (`#80/#81` wave implementation baseline).
   - PR `#94` merged (P0 rescue closeout), and issue `#80` is now closed.
   - Issue `#81` is now closed after PR `#102` acceptance reconciliation.
10. Roadmap-to-issue conversion completed:
   - `#95` media appearances backup gate and private WP draft
   - `#96` Aurora post-`#87` smoke/review packet refresh
   - `#97` Aurora/legacy design issue reconciliation
   - `#98` Aurora issue-swarm handoff refresh
   - `#99` next keynote source-pack draft batch
11. Aurora Wave 2 completed:
   - PR `#100` merged (`#82` media-led homepage lane)
   - PR `#101` merged (`#83` Work/Speaking media templates lane)
   - issues `#82` and `#83` are now closed
12. Aurora Wave 3 current state:
   - PR `#103` merged (component inventory foundation for `#85`; issue still open)
   - PR `#104` merged (long-form lane for `#84`; issue now closed)
   - `#85` and `#86` are now the remaining Track B gates

## Non-Negotiable Guardrails

1. Track separation stays strict: no theme edits on `main`, no content-payload rewrites on Track B branches.
2. Keep Notion -> WP writes dry-run first, slug-verified, and no `--publish` without explicit approval.
3. Keep rollback snapshots before production writes.
4. No casual history rewrites; today’s rewrite is complete and should be treated as a closed operation.

## Next Session Priority Order

### 1) Aurora Wave 3 closeout (P0, Track B)

Goal: finish the last implementation lane, then run the final QA gate.

Do:

- Execute `#85` implementation in an isolated `aurora/v2` worktree using the inventory in `AURORA-COMPONENT-INVENTORY-2026-05-20.md`.
- After `#85` merges, execute `#86` as the staging QA gate with explicit accessibility/performance evidence.
- Keep scope strict to theme/templates/components and proof artifacts.
- Keep Track A publish operations out of this wave.

Done when:

- `#85` is closed with evidence and `#86` has a complete QA packet plus close/hold decision.

### 2) Queue bookkeeping and QA gate prep (P1)

Goal: leave the board explicitly ready for the final QA gate.

Do:

- Refresh issue/PR counts and Aurora handoff docs after each Track B merge.
- Keep `#86` as the final QA gate and run it only after `#85` implementation lands.
- Preserve prior closeouts (`#81`, `#82`, `#83`, `#84`) as closed unless a regression is verified.

Done when:

- Wave 3 start conditions are explicit in both GitHub comments and `docs/current-state/`.

### 3) Track A backlog remains queued (P2, deferred this wave)

Goal: preserve Track A readiness without mixing tracks.

Do:

- Keep media-appearance draft lane blocked on fresh full-site backup gate in `#95`.
- Keep next keynote source-pack draft-batch work queued in `#99`.
- Keep authority/content prep artifacts as review-ready local docs only.
- Revisit Track A content issues (`#65-#68`) after Wave 2 completion.

Done when:

- No accidental Track A writes happened during Track B Wave 3 closeout.

## Suggested Opening Commands

```bash
git fetch --all --prune
git worktree list --porcelain
gh pr list --state open
git branch -r
```

## Human Checkpoints

Ask KK before:

- Any production publish operation from draft packs.
- Any Aurora move that changes public production theme state.
