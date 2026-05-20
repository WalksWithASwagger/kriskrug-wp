# Tomorrow Roadmap - 2026-05-20

**Prepared after:** 2026-05-19 credential-history rewrite execution, queue recovery, and merge pass  
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
   - Issue `#81` remains open pending explicit acceptance closeout comment.
10. Roadmap-to-issue conversion completed:
   - `#95` media appearances backup gate and private WP draft
   - `#96` Aurora post-`#87` smoke/review packet refresh
   - `#97` Aurora/legacy design issue reconciliation
   - `#98` Aurora issue-swarm handoff refresh
   - `#99` next keynote source-pack draft batch

## Non-Negotiable Guardrails

1. Track separation stays strict: no theme edits on `main`, no content-payload rewrites on Track B branches.
2. Keep Notion -> WP writes dry-run first, slug-verified, and no `--publish` without explicit approval.
3. Keep rollback snapshots before production writes.
4. No casual history rewrites; today’s rewrite is complete and should be treated as a closed operation.

## Next Session Priority Order

### 1) Aurora Wave 2 serial launch (P0, Track B)

Goal: execute Track B only, one lane at a time, with evidence-gated merges.

Do:

- Reconcile new issue `#96` with the already-merged `#93/#94` evidence before opening another Aurora review PR.
- Run `#81` explicit closure checklist comment first (close only if complete).
- Execute `#82` in an isolated `aurora/v2` worktree.
- After `#82` merge, execute `#83` in a fresh worktree rebased from updated `origin/aurora/v2`.
- Keep scope strict to theme/templates/components; no Track A publish operations in this wave.

Done when:

- `#82` and `#83` each have artifacts, PR merge evidence, and scoped Track B diffs.

### 2) Queue bookkeeping and Wave 3 gate prep (P1)

Goal: leave the board explicitly ready for the next Aurora hardening wave.

Do:

- Use `#97` and `#98` to refresh issue/PR counts, issue labels, and Aurora handoff docs after `#82/#83` merges.
- Confirm `#84` and `#85` are queued as the next implementation pair.
- Keep `#86` as the final QA gate after both `#84` and `#85` merge.

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

- No accidental Track A writes happened during Track B Wave 2 execution.

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
