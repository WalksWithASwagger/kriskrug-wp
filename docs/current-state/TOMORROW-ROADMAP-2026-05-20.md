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

## Non-Negotiable Guardrails

1. Track separation stays strict: no theme edits on `main`, no content-payload rewrites on Track B branches.
2. Keep Notion -> WP writes dry-run first, slug-verified, and no `--publish` without explicit approval.
3. Keep rollback snapshots before production writes.
4. No casual history rewrites; today’s rewrite is complete and should be treated as a closed operation.

## Next Session Priority Order

### 1) Clear the media-appearance draft backup gate (P0, Track A)

Goal: finish the private WordPress draft safely, not publicly publish.

Do:

- Take a fresh full-site backup through wp-admin/UpdraftPlus, Pagely SSH, or another approved full-site backup path.
- Re-run the existing slug/category/tag/link/privacy preflight from `APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md`.
- Create only a private WP draft for `ai-media-appearances-podcast-guesting`, with embed-only media and `featured_media=0`.
- Do not publish and do not add backlinks until KK reviews the draft in wp-admin.

Done when:

- WP draft ID, edit URL, REST readback, rollback/delete note, and verification evidence are documented.

### 2) Aurora review prep refresh (P1, Track B)

Goal: keep Aurora demo narrative current after merge to `aurora/v2`.

Do:

- Start with issues `#80` and `#81`.
- Re-run Aurora smoke screenshots on current `aurora/v2`.
- Update the review packet if visuals or behavior shifted after merge.
- Confirm nav/header render and mobile quality baseline.

Done when:

- Fresh smoke artifacts and one current review packet are present under `docs/current-state/`.
- Header/nav render and visual-system decisions are clear enough to unblock the next Aurora wave.

### 3) Track A content lane continuation (P2)

Goal: continue authority/support content without crossing into risky publish actions.

Do:

- Keep building review-ready draft packages from `content/source-packs/keynotes-2026/`.
- Prioritize source-backed proofs and internal linking quality.
- Keep publish actions gated behind explicit review.
- Treat `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/` as review-ready local support content, not yet a live post. It includes the Vancouver AI March 2026 video, all current draft links returned `200`, and the private WP draft pass is blocked only by the fresh full-site backup gate documented in `content/source-packs/keynotes-2026/verification/APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md`.
- Prioritize content issues `#65-#68` after Aurora Wave 1: About, Homepage hero, Services, and Work/Projects.

Done when:

- Next draft batch has clear review verdicts and no accidental publish.

### 4) Issue queue alignment for swarming (P2)

Goal: keep the issue board trustworthy for agentic execution.

Do:

- Re-check open Aurora issues `#80-#86` against merged state.
- Close, relabel, or split issues whose acceptance criteria drifted.
- Keep labels consistent with Track A/Track B ownership.
- Current live snapshot before shutdown: `70` open issues, `0` open PRs, `50` `auto-implement` issues, and `2` human-review blockers (`#23`, `#75`).

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
