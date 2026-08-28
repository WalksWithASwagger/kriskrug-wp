# #749 visual-baseline prune proposal — 2026-08-28

**Status:** proposal only. No capture directory has been deleted.

`make visual-prune KEEP=2 DRY_RUN=1` now retains a tracked diff pair as one
logical unit. The current dry-run keeps the newest complete pair
`20260817T044445Z` → `20260817T045150Z` and proposes three older local PNG
directories for deletion. Top-level manifests, diff JSON, and reports are
tracked audit records and stay.

## Keep

| Run | Role | Size | Evidence |
|---|---|---:|---|
| `20260817T044445Z` | baseline | 272,488 KiB | `diff-20260817T045150Z.json` baseline |
| `20260817T045150Z` | candidate | 295,808 KiB | newest tracked diff and report |

Retained total: **568,296 KiB** (about **555 MiB**).

## Exact delete list awaiting approval

| Path | Role | Size |
|---|---|---:|
| `docs/current-state/reports/visual-baseline/20260811T033217Z/` | older candidate | 367,524 KiB |
| `docs/current-state/reports/visual-baseline/20260817T044333Z/` | older baseline | 272,488 KiB |
| `docs/current-state/reports/visual-baseline/20260817T044820Z/` | older candidate paired with `044333Z` | 287,676 KiB |

Proposed reclaim: **927,688 KiB** (about **906 MiB**; the CLI reports
**949.6 MB** in decimal units).

## Verification already completed

```text
would remove docs/current-state/reports/visual-baseline/20260811T033217Z
would remove docs/current-state/reports/visual-baseline/20260817T044333Z
would remove docs/current-state/reports/visual-baseline/20260817T044820Z
kept 2 run dir(s); would free 949.6 MB
```

All five directories were still present after the dry-run. The implementation
has focused regression coverage for pair retention and non-destructive preview.

## Approval phrase

```text
Approved: delete the exact three #749 capture directories in the 2026-08-28
proposal with make visual-prune KEEP=2. Keep the 044445Z → 045150Z pair and all
tracked manifests, diff JSON, and reports.
```
