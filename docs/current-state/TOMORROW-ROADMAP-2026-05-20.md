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

## Non-Negotiable Guardrails

1. Track separation stays strict: no theme edits on `main`, no content-payload rewrites on Track B branches.
2. Keep Notion -> WP writes dry-run first, slug-verified, and no `--publish` without explicit approval.
3. Keep rollback snapshots before production writes.
4. No casual history rewrites; today’s rewrite is complete and should be treated as a closed operation.

## Next Session Priority Order

### 1) Aurora review prep refresh (P1, Track B)

Goal: keep Aurora demo narrative current after merge to `aurora/v2`.

Do:

- Re-run Aurora smoke screenshots on current `aurora/v2`.
- Update the review packet if visuals or behavior shifted after merge.
- Confirm nav/header render and mobile quality baseline.

Done when:

- Fresh smoke artifacts and one current review packet are present under `docs/current-state/`.

### 2) Track A content lane continuation (P2)

Goal: continue authority/support content without crossing into risky publish actions.

Do:

- Keep building review-ready draft packages from `content/source-packs/keynotes-2026/`.
- Prioritize source-backed proofs and internal linking quality.
- Keep publish actions gated behind explicit review.
- Treat `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/` as review-ready local support content, not yet a live post. It now includes the Vancouver AI March 2026 video and all current draft links returned `200` during the 2026-05-19 polish pass.

Done when:

- Next draft batch has clear review verdicts and no accidental publish.

### 3) Issue queue alignment for swarming (P2)

Goal: keep the issue board trustworthy for agentic execution.

Do:

- Re-check open Aurora issues `#80-#86` against merged state.
- Close, relabel, or split issues whose acceptance criteria drifted.
- Keep labels consistent with Track A/Track B ownership.

Done when:

- Top-of-queue issues map cleanly to current code reality.

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
