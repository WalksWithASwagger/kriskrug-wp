# Issue #4 Batch 3 media-alt apply — 2026-08-24

Track A execution evidence for the reviewed Batch 3 media-library lane. This
report does not close issue #4 or authorize the parked archive batches.

> **Correction, 2026-08-25:** path-aware authenticated edit context found five
> duplicate-filename joins. Three protected rows map to actual attachments 6126,
> 6985, and 7637. Two writes to duplicates 6729 and 11774 should have targeted
> 6014 and 8871 and require approval-gated rollback. Treat this report as the
> historical execution record for the 73 writes; use
> [`issue-4-residual-audit-20260825.md`](issue-4-residual-audit-20260825.md)
> for current residual identities and next steps.

## Result

- Reviewed Batch 3 scope: 75 unique attachments from 76 historical inventory
  rows.
- Applied and exact: 73 attachments.
- Protected no-write skips: media 6481 and 8211. Their non-empty,
  context-specific library alts were preserved; three historical rows were
  reclassified to `investigate-shared-media-context`.
- Earlier media targets 6835 and 12646 remained exact.
- Final corrected media selector: 75 targets, 75 `already-applied`, zero
  identity failures.
- Batch 3 snapshots: 73 files, all mode 0600.
- Live writes to #829-#832: zero.

## Safety sequence

Every written attachment used its exact `--only-media-id` selector. Each
target was dry-run first, verified by media ID and filename, snapshotted before
the write, then checked through authenticated WordPress edit context.

The first five canaries (12597, 12593, 12541, 12536, 12528) exposed a cached
public-REST false failure: their immediate reports said
`WRITTEN-READBACK-MISMATCH`, while authenticated edit context, cache-bypassed
public REST, and rendered-page checks all held the proposed values. PR #900
changed media preflight and readback to authenticated `context=edit` and added
cache busting to unauthenticated dry runs. All later writes reported
`written-verified` directly.

Media 5375 exposed a second safety gap. Its existing alt was an inventoried
filename-style violation rather than an empty string. PR #901 allows that one
kind of replacement only when the live value exactly matches the reviewed
`media_library_alt` baseline. The live 5375 replacement used that path and
returned `replacement_basis=inventory-baseline`, `written-verified`, snapshot
mode 0600.

The same review caught media 6481 and 8211 before write. Their existing alts
were meaningful strings used by other contexts, so the exact-baseline rule
refused them. Neither attachment was changed.

## Encoding checkpoint

Media 5024 was the first NCR-bearing target. Authenticated and cache-bypassed
public REST both preserved the exact proposed string, including literal
`Kr&#252;g`. Later NCR-bearing media 6497, 6750, and 7363 were also exact in the
final authenticated dry run.

## Verification

Final authenticated media dry run before the inventory reclassification:

- 77 selected targets;
- 75 `already-applied`;
- two expected conflicts: 6481 and 8211;
- zero ID or filename failures.

After reclassifying the three unsafe historical rows, the media selector has
75 targets and all 75 are already applied. The two skipped attachment IDs are
no longer media-write targets.

Full `recount_live.py` result:

| Signal | Value |
|---|---:|
| Routes requested / fetched | 216 / 216 |
| Fetch errors | 0 |
| Rendered image occurrences | 1,959 |
| Unique page-source pairs | 1,936 |
| Violation occurrences | 1,078 |
| Unique page-source violations | 1,077 |
| Has-alt occurrences | 878 |
| Empty-alt violations | 953 |
| Filename-style violations | 107 |
| Missing-alt-attribute violations | 18 |

The 2026-08-02 baseline was 1,186 violation occurrences / 1,185 unique
violations across 2,161 rendered image occurrences. The current violation
count is 108 lower, but total rendered images are also 202 lower because the
live site changed between crawls. Treat the delta as a current-state comparison,
not as 108 findings causally fixed by this batch.

## Repository evidence

- PR #899: visually reviewed Batch 3 drafts and execution plan.
- PR #900: authenticated media readback and cache-busted public fallback.
- PR #901: exact inventoried filename-style replacement rule.
- `make test`: 546 repository unit tests and 68 SEO tests passed after PR #901.
- `make validate`: PHP syntax and WordPress coding standards passed.

Gitignored local evidence remains under `.generated/alt-text-backfill/`,
including each private snapshot, per-item report, the final media dry-run JSON,
and the 216-route recount JSON. Those files are operational rollback material,
not repository artifacts.

## Remaining issue #4 scope

1. Reproduce and assign the real owning surface for the three protected rows
   involving media 6481 and 8211.
2. Handle the known page-6815 baked in-content alt separately.
3. Decide whether `/home/` should redirect, unpublish, or be maintained.
4. Classify the current 18 missing-alt-attribute findings.
5. Decide whether archive batches 4-6 are completed, traffic-prioritized, or
   permanently parked.
6. Complete screen-reader testing and WCAG 2.1 AA verification.
