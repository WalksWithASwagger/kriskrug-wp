# #740 docs archive proposal — 2026-08-16

> **STATUS: RETIRED 2026-08-28. DO NOT EXECUTE THIS MOVE TABLE.** Issue #740
> closed after a fresh audit found that this proposal would move active records
> and miss its own top-level-count target. Any future sweep requires a new dated,
> per-file allow-list with current owning-issue and inbound-link evidence.

**Issue:** [#740](https://github.com/WalksWithASwagger/kriskrug-wp/issues/740)
**Status:** historical proposal only. No files were moved from this table.
**Inventory:** top-level `docs/current-state/*.md` = **42** files (2026-08-16).
**Already archived (do not move again):** `WORK-PLAN-2026-08-05.md`, `WORK-PLAN-2026-07-30.md`, the May–June #549 set.

Inbound counts below are `rg -l` hits **excluding** `docs/current-state/archive/`.

## KEEP (durable front door + runbooks)

| File | Why |
|---|---|
| `README.md` | Front door index |
| `CURRENT-STATE-2026-07-30.md` | Declared snapshot / Makefile default |
| `MASTER-PLAN-2026-07-30.md` | Plan of record |
| `WORK-PLAN-2026-08-16.md` | Active day runbook |
| `TWO-TRACK-MODEL.md` | Operating model |
| `INCIDENT-2026-05-15-overwritten-post.md` | Standing safety rule |
| `AGENT-MERGE-PATH-2026-07-26.md` | Cloud merge path |
| `VARLOCK-ROLLOUT-2026-07-16.md` | Env contract |
| `ACCESS_CHANNELS.md` / `BACKUP_PLAN.md` / `ROLLBACK_PLAYBOOK.md` | Ops runbooks |
| `AURORA-RELEASE-CHECKLIST.md` | Theme release |
| `AURORA-VISUAL-BASELINE-RUNBOOK.md` | Pixel gate |
| `AURORA-STYLESHEET-REBUILD-PLAN.md` | #423 plan of record |
| `SEO-INDEXING-RUNBOOK.md` / `SEO-PUBLISHER-SCHEMA-2026-07-19.md` | SEO runbooks |

`WORK-PLAN-2026-08-15.md` stays at top level until KK approves moving it (it is now bannered SUPERSEDED, same pattern as 08-09). After approval it joins the MOVE list.

## MOVE after KK approval (`git mv` into `docs/current-state/archive/`)

| File | Inbound (ex-archive) | Reason |
|---|---:|---|
| `WORK-PLAN-2026-08-09.md` | 6 | Explicitly superseded by 08-15, then 08-16 |
| `AGENTIC-CRUSH-PLAN-2026-07-31.md` | 1 | One-shot; crush window closed |
| `LABEL-HYGIENE-2026-08-02.md` | 1 | One-shot label sweep |
| `A11Y-WCAG-AUDIT-2026-08-02.md` | 0 | Evidence; decisions live in issues |
| `AURORA-STYLESHEET-DECISION-2026-08-02.md` | 1 | Decision recorded; plan of record is the rebuild plan |
| `CSS-DEADCODE-OVERLAP-AUDIT.md` | 5 | Measurement feeding the rebuild plan |
| `INTERACTION-STATES-GAP-INVENTORY.md` | 1 | #424 first AC, dated 2026-07-25 / 08-05 |
| `SEO-STRIKING-DISTANCE-2026-08-02.md` | 1 | #249 re-measure |
| `SEO-ARCHIVE-INDEXABILITY-2026-08-02.md` | 0 | One-shot |
| `UNDESIGNED-PAGES-INVENTORY-2026-08-02.md` | 0 | One-shot |
| `REPO-BLOAT-REMEASURE-2026-08-02.md` | 0 | One-shot |
| `DECISION-GIT-HISTORY-REWRITE-2026-08-02.md` | 0 | Settled by #572 |
| `DECISION-PARKED-PLUGINS-2026-08-02.md` | 2 | Settled decision |
| `RECLAIM-LIST-2026-07-24.md` | 2 | #369 waves shipped |
| `SESSION-CLOSEOUT-2026-07-24.md` | 2 | One-shot closeout |
| `REVIVE-AURORA-PORT-2026-07-24.md` | 7 | Port shipped |
| `REVIVE-AURORA-REVISIONS-2026-07-24.md` | 4 | Port shipped |
| `PERFORMANCE-RECOVERY-2026-07-01.md` | 3 | Closeout |
| `AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md` | 1 | Closeout |
| `AURORA-HOMEPAGE-BC-AI-FUTUREPROOF-2026-07-03.md` | 1 | Closeout |
| `AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md` | 3 | Handoff |
| `AURORA-MOBILE-QA-127.md` | 1 | Test plan; #127 still open — move the doc, keep the issue |
| `AURORA-TEMPLATE-CONTENT-HANDOFF.md` | 1 | 2026-05-23 unfinished handoff, not a plan |
| `WP-AUTH-CLIENT-INVENTORY-2026-07-08.md` | 1 | Inventory |
| `CONTENT-ARCHITECTURE-RESET-2026-07-01.md` | 4 | Wave closeout |
| `REPO-HYGIENE-AUDIT-2026-07-12.md` | 6 | Audit; #318 residue lives in issues |

**26 files** in this pass (27 if KK also moves superseded `WORK-PLAN-2026-08-15.md`).
Predicted top-level count after the 26-file move: **16** (42 − 26), which is under the issue's "~30" target.

## Inbound-link repair plan

Same PR as the moves, after approval:

1. `git mv` the MOVE list into `archive/`.
2. Update `docs/current-state/README.md` one-shot table to point at `archive/…`.
3. `rg` the 26 basenames from repo root excluding `archive/`; retarget every remaining relative link.
4. `make docs-truth-check`.

No deletions. History stays via rename.

## Paste-ready KK approve comment

```text
Approved: git mv the 26-file MOVE table in
docs/current-state/reports/docs-archive-proposal-740-2026-08-16.md
into docs/current-state/archive/. Also move WORK-PLAN-2026-08-15.md.
Repair inbound links in the same PR. No deletions.
```

Strike the 08-15 sentence if that file should stay at top level as the immediate predecessor.
