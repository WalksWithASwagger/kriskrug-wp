# #749 visual-baseline prune proposal — 2026-08-16

**Issue:** [#749](https://github.com/WalksWithASwagger/kriskrug-wp/issues/749)
**Status:** proposal only. No capture directories were deleted.
**This Cloud VM:** `make visual-list` shows **0 PNG on disk** for every run. The ~2.3 GB the issue measured is laptop-local (`docs/current-state/reports/visual-baseline/<run-id>/`). Tracked manifests and diff JSON stay.

## Current baseline

Newest tracked baseline: **`20260816T151617Z`** (Aurora **1.6.5**, Boost `8d99a2084d`, 6 routes).
Newest tracked diff pair: **`20260814T185057Z` → `20260814T190349Z`** (1.6.4 → 1.6.5).

The official gate is still post-deploy live vs pre-deploy live. For the owed 1.6.6 window, freeze a fresh baseline on live 1.6.5 immediately before SFTP, then diff after the 1.6.6 readback. `20260816T151617Z` is the newest 1.6.5 snapshot on record, not a substitute for that pair.

## Disposition

| Run id | Kind | Theme | Referenced by tracked diff/report? | PNG on this VM | Proposal |
|---|---|---|---|---|---|
| BASE1 / BASE2 | 1.4.3 pair | 1.4.3 | `diff-BASE2.json`, `report-BASE2.md` | 0 | prune PNGs |
| 20260726T194734Z | baseline | 1.4.8 | manifest only | 0 | prune PNGs |
| 20260803T033115Z | baseline | 1.5.7 | manifest only | 0 | prune PNGs |
| 20260810T043948Z | baseline | 1.5.9 | manifest only | 0 | prune PNGs |
| 20260810T054311Z | candidate | 1.6.0 | `diff-20260810T054311Z.json` | 0 | prune PNGs |
| 20260810T164654Z | baseline | 1.6.0 | manifest only | 0 | prune PNGs |
| 20260810T164933Z | candidate | 1.6.0 | `diff-20260810T164933Z.json` | 0 | prune PNGs |
| 20260811T022807Z | baseline | 1.6.0 | manifest only | 0 | prune PNGs |
| 20260811T033217Z | candidate | 1.6.4 | `diff-20260811T033217Z.json` | 0 | prune PNGs |
| 20260814T185057Z | baseline | 1.6.4 | pair with 190349Z | 0 | **keep until 1.6.6 window closes** |
| 20260814T190349Z | candidate | 1.6.5 | `diff-20260814T190349Z.json`, report | 0 | **keep until 1.6.6 window closes** |
| 20260816T151617Z | baseline | 1.6.5 | newest baseline | 0 | **keep** |

Exact delete paths (laptop, untracked only):

```text
docs/current-state/reports/visual-baseline/BASE1/
docs/current-state/reports/visual-baseline/BASE2/
docs/current-state/reports/visual-baseline/20260726T194734Z/
docs/current-state/reports/visual-baseline/20260803T033115Z/
docs/current-state/reports/visual-baseline/20260810T043948Z/
docs/current-state/reports/visual-baseline/20260810T054311Z/
docs/current-state/reports/visual-baseline/20260810T164654Z/
docs/current-state/reports/visual-baseline/20260810T164933Z/
docs/current-state/reports/visual-baseline/20260811T022807Z/
docs/current-state/reports/visual-baseline/20260811T033217Z/
```

Operator command after approval (keeps newest 2 PNG dirs; leaves manifests):

```bash
make visual-prune KEEP=2
```

Do not touch tracked `manifest-*.json`, `diff-*.json`, or `report-*.md`.

## Paste-ready KK approve comment

```text
Approved: on the laptop, prune PNG dirs listed in
docs/current-state/reports/visual-baseline-prune-proposal-749-2026-08-16.md
via `make visual-prune KEEP=2`. Keep 20260816T151617Z and the 20260814 pair
until the 1.6.6 deploy window closes. Do not delete tracked manifests.
```
