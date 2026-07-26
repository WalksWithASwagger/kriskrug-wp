# Pixel-gate handoff — #494 / PR #493 (Aurora 1.5.0)

**Date:** 2026-07-26  
**Agent branch:** `cursor/494-pixel-gate-f196`  
**PR branch updated:** `theme/474-cascade-layers-scaffold` (same tip)  
**Refs:** #474, #493, #494, #473

## Verdict

| Gate | Status |
|---|---|
| Merge conflicts vs `main` | **Resolved** (version → 1.5.0 on top of Aurora 1.4.8) |
| css-ratchet | **Green** after intentional rebaseline |
| `!important` code-only | **160** (unchanged); front-end gated metric **159** |
| visual-diff (11×3) | **Blocked — no Chromium harness** (`/opt/pw-browsers` missing) |
| Ready for KK merge? | **No** — pixel gate still owed |

## What landed on the branch

1. Merged `theme/474-cascade-layers-scaffold` onto current `main` (1.4.8). Conflicts only in `theme/kk-aurora/style.css` + `functions.php` version constants → kept **1.5.0** + `#474` enqueue/layer work.
2. Extended inventory/coverage/visual file lists to include `02-tokens.css` + `09-late.css`.
3. Rebaselined `.css-budget.json`: `front_end_lines` **7379 → 7458** (+79) under waiver **#494** (scaffold wrappers + new sheets). Zero new `!important` declarations.

### Commits

- `a614f4f` — `feat(#474): cascade @layer scaffold + --kk-* tokens (Aurora 1.5.0)` (merge + conflict resolve)
- `cc6041c` — `fix(#494): rebaseline css-ratchet for Aurora 1.5.0 scaffold`

### Files touched (Track B only)

- `theme/kk-aurora/style.css` — `@layer` order + `@layer components` wrap; Version 1.5.0
- `theme/kk-aurora/functions.php` — version 1.5.0; tokens + late enqueue; explicit deps
- `theme/kk-aurora/assets/css/02-tokens.css` — new (`@layer tokens`)
- `theme/kk-aurora/assets/css/09-late.css` — new (unlayered, empty)
- `theme/kk-aurora/assets/css/{animations,bleeding-edge,revive-port,typography-refined}.css` — `@layer components` wrappers only
- `.css-budget.json` — waiver + new ceiling
- `scripts/css_coverage_audit.py`, `scripts/css_inventory.py`, `scripts/visual_baseline.py`, `scripts/tests/test_aurora_css_literal_contrast.py` — include new sheets in scope

## css-ratchet budget (new)

| Metric | Was | Now |
|---|---:|---:|
| `front_end_lines` | 7379 | **7458** |
| `front_end_important` | 159 | **159** |

Breakdown of +79: ~+18 wrapper lines across five sheets + 38 (`02-tokens.css`) + 23 (`09-late.css`). Matches the “~+83 structural” expectation in #494.

## Visual gate — what KK / harness env must still run

This pod has `scripts/visual_baseline.py` but **no** `/opt/pw-browsers`. `make visual-preflight` exits FATAL and refuses to download Chromium (by design).

On an env with the harness:

```bash
# 1) Baseline against current prod (read-only GETs)
make visual-baseline EXPECT_THEME=1.4.7   # or whatever live reports

# 2) Render / deploy this branch's theme as the candidate (no live write from agent)
#    then diff:
make visual-diff BASE=<baseline-run-id>

# 3) If any route flips: add ONE commented rule to
#    theme/kk-aurora/assets/css/09-late.css (unlayered, no new !important)
#    and re-run until 0 changed pixels above tolerance (11 routes × 3 viewports)

# 4) PR body:
make visual-diff-report DIFF=<diff-run-id>
```

Do **not** resolve pixel diffs by adding `!important` or editing layered sheets — only `09-late.css` per plan §2.4.

## Local checks this agent could / could not run

| Check | Result |
|---|---|
| Brace balance (7 CSS files) | OK |
| `python3 scripts/css_inventory.py --check --base-ref origin/main` | Green |
| `python3 -m unittest scripts.tests.test_aurora_css_literal_contrast` | 12 OK |
| `make visual-preflight` | FATAL — missing `/opt/pw-browsers` |
| `make validate` / `theme-smoke` / `plugin-smoke` | Blocked — `php` not on PATH in this pod |

CI on the updated PR should still run PHP + css-ratchet; css-ratchet is expected green after the waiver commit.

## Residual blockers

1. **Pixel gate** — must run in Chromium harness env; 0px above tolerance required before merge.
2. **PHP lint/smoke** — not runnable here; rely on CI `php-validation` / `validate`.
3. **Do not merge** until green visual-diff is recorded on the PR (issue #494 acceptance).
4. Parallel agents briefly contaminated this branch with an unrelated docs commit; tip was force-reset to `cc6041c` (Track B only). Prefer exclusive checkout of `cursor/494-pixel-gate-f196` / the PR branch during further gate work.
