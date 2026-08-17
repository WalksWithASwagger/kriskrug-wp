# DECISION brief — stylesheet hierarchy (#423)

**Date:** 2026-07-26  
**Lane:** Track B (docs only — no theme CSS/PHP/`theme.json` changes in this commit)  
**Issue:** [#423 — Stylesheet hierarchy: rebuild from the ground up vs incremental repair](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423)  
**For:** KK comment on #423 (confirm or override the recommendation below)  
**Measured against:** repo `main` @ `a552142` (Aurora **1.4.8**), live `https://kriskrug.co` logged-out readback same day (repo `style.css` **byte-identical** to live)

---

## Ask (one comment unblocks the lane)

Please reply on #423 with one of:

1. **Confirm Path B** — continue the staged cascade scaffold already in [PR #493](https://github.com/WalksWithASwagger/kriskrug-wp/pull/493) / [#474](https://github.com/WalksWithASwagger/kriskrug-wp/issues/474) (recommended).
2. **Override to pure Path A** — abandon wrap-and-migrate; authorize a throwaway rewrite of the five front-end sheets (not started; would park #493).
3. **Pause** — freeze theme CSS work after current Wave 2 boy-scouts; revisit after redesign content ships.

---

## Verdict (agent recommendation)

**Path B — staged repair via the Aurora 1.5.0 cascade scaffold.**

PR #493 already implements step 2 of [`AURORA-STYLESHEET-REBUILD-PLAN.md`](../AURORA-STYLESHEET-REBUILD-PLAN.md): `@layer` order, wrap existing sheets (contents untouched), unused `--kk-*` token aliases, empty `09-late.css`. That is **not** a ground-up rewrite. It is incremental repair with an explicit hierarchy — operationally Path B, even though the 2026-07-24 #423 comment labeled the epic “Path A.”

Do not throw the sheets away. Keep paying debt down behind the pixel gate (#473 harness closed; #494 still gates deploy of #493).

---

## Why this brief exists (history in one paragraph)

| When | What happened |
|---|---|
| 2026-07-17 | KK teardown: “maybe throw them away and rebuild.” Filed as #423. |
| 2026-07-19 | Agent memo on #423 recommended **B/C** (boy-scout / targeted consolidation). |
| 2026-07-24 | KK recorded **Path A** (ground-up token rebuild). |
| 2026-07-25 | Plan of record landed: staged migration labeled “Path A,” but sequence is wrap → migrate → delete — i.e. **staged**. Sub-issues #472–#481 filed. |
| 2026-07-26 | #472 + #473 **closed**. #474 implementation is open as **PR #493** (Aurora 1.5.0 scaffold), awaiting pixel-gate merge (#494). |

This memo re-asks the binary with measured inventory **and** with the scaffold already in flight, so the label matches the work.

---

## 1. CSS surface inventory (measured)

### 1.1 Theme sheets (repo = live at 1.4.8)

`make css-inventory` / `scripts/css_inventory.py` on this worktree:

| File | Lines | Bytes | `!important` (code) | Role |
|---|---:|---:|---:|---|
| `theme/kk-aurora/style.css` | 4,602 | 117,636 | 71 | Monolith + custom props + components |
| `assets/css/revive-port.css` | 1,179 | 28,670 | 82 | Revive cream/ink brand layer (loads last) |
| `assets/css/typography-refined.css` | 685 | 16,735 | 6 | Type refinements / drop cap |
| `assets/css/bleeding-edge.css` | 561 | 12,390 | 0 | Progressive enhancement |
| `assets/css/animations.css` | 352 | 7,540 | 0 | Motion / keyframes |
| `assets/css/editor.css` | 175 | 5,343 | 1 | Editor only |
| **Front-end subtotal (5)** | **7,379** | **182,971** | **159** | CI ratchet baseline |
| **All six** | **7,554** | **188,314** | **160** | — |

Debt signals (same inventory + prior audits):

- **316** selectors declared more than once; **75** across multiple files.
- **~.aurora-writing-card` still multi-sited** in `style.css` (base + archive override + breakpoint/motion passes) — the doubling #408/#409 hit.
- Coverage ratchet (`.css-budget.json`): **88** high-confidence dead authored classes (~33%); ~22 KB removable rule blocks when step 6 runs.
- `!important` growth under “boy-scout only”: **79 → ~160** from 2026-07-19 → Revive 1.4.x (`revive-port.css` alone ≈ half). Surgical fixes worked in `style.css`; the brand layer swamped the net.

### 1.2 Enqueue / intended load order (`functions.php`)

| # | Handle | Source | Declared deps (1.4.8 `main`) |
|---|---|---|---|
| 1 | `kk-aurora-style` | `style.css` | none |
| 2 | `kk-aurora-typography` | `typography-refined.css` | none |
| 3 | `kk-aurora-animations` | `animations.css` | none |
| 4 | `kk-aurora-bleeding-edge` | `bleeding-edge.css` | none |
| 5 | `kk-aurora-revive-port` | `revive-port.css` | all of 1–4 (forced last) |
| editor | `kk-aurora-editor` + `add_editor_style(style.css, editor.css)` | editor canvas | **does not** load typography / animations / revive |

PR #493 fixes the missing deps and adds `kk-aurora-tokens` + `kk-aurora-late` (late depends on WP `global-styles`).

### 1.3 What actually loads (logged out, 2026-07-26)

Jetpack Boost concatenates theme CSS. Key routes serve **one** Pagely CDN bundle:

`https://s5102.pcdn.co/wp-content/boost-cache/static/c2441c2909.min.css` — **138,153 B**, **159** `!important`, contains `aurora` ×2133 / `revive` ×169.

Typical head stack on `/`:

1. `jetpack-boost-critical-css` — **7,474 B**, 1 `!important` (home; blog has a larger critical block)
2. Boost concatenated bundle (`<link>` ×2 async pattern)
3. Core block library / template-part inline styles
4. `global-styles-inline-css` — **28,067 B**, **137** `!important` (from `theme.json`) — **prints after** the theme bundle
5. `core-block-supports` / skip-link inlines

**Implication:** equal-specificity fights are often theme-vs-`theme.json`, not sheet-vs-sheet. A rebuild that ignores late unlayered `09-late.css` (or feeding `theme.json` correctly) recreates today’s `!important` habit.

### 1.4 Inline / page-content CSS

| Surface | Status |
|---|---|
| Theme templates | **0** `<style>` blocks |
| Theme parts | **1** — `parts/marquee-current.html` (~49 CSS lines); generated by `scripts/marquee/build.py` |
| Track A page-content `<style>` (anonymous) | **6 of 8** key routes (re-measured 2026-07-26): |

| Route | Anon `<style>` bytes | `!important` in that block |
|---|---:|---:|
| `/about/`, `/speaking/`, `/work/` | 959 each | 14 each |
| `/services/` | 4,418 | 13 |
| `/photography/` | 5,024 | 12 |
| `/contact/` | 5,422 | 17 |
| `/`, `/blog/` | 0 | 0 |

These blocks mostly suppress the theme drop cap and re-declare cream/ink locals. Owned by [#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480) (Track A), not by throwing away theme sheets.

### 1.5 Code Snippets / Asset Diet (documented; live wp-admin still owed)

From deploy backup + #256 / dead-code audit (not re-auth’d this session):

| Snippet | Role | CSS inject? |
|---|---|---|
| #5 Schema, #7/#8 SEO/GSC, #13 news sitemap | PHP | No |
| #10 KK Asset Diet | Dequeues plugin assets | No (keep unless replacement proven) |
| #9 / #11 contrast hotfixes | CSS | **Inactive** |
| **#14 creamfix file-apply** | Overwrites `style.css` + `revive-port.css` from media **#12631** at `init` | Hazard — **verify retired + delete media before any 1.5.0 upload** (plan risk R-3) |

### 1.6 Jetpack Boost

- Serves the only public stylesheet link visitors see.
- Critical CSS is a separate inline surface (staleness vs rebuild selectors = open risk R-2 / plan §7).
- After every theme deploy: purge Boost + PressCACHE; confirm **bundle URL hash changed**.

### 1.7 Scaffold already started (#474 / PR #493)

On `theme/474-cascade-layers-scaffold` (open, CI green as of this brief):

- Declares `@layer reset, tokens, base, primitives, components, patterns, utilities, overrides;`
- Wraps all five existing sheets in `@layer components { … }` — **+wrapper lines only, 0 rules removed/renamed**
- Adds `02-tokens.css` (`--kk-*` aliases over `--wp--*`, **not yet consumed**)
- Adds empty `09-late.css` (unlayered escape hatch for `global-styles`)
- Rebaselines css-ratchet: front-end lines **7379 → 7458** under #494 waiver; `!important` still **159**
- **Not deployable** until `make visual-diff` clears (#494 / pixel gate)

Sources: #256 audit, [`CSS-DEADCODE-OVERLAP-AUDIT.md`](../archive/CSS-DEADCODE-OVERLAP-AUDIT.md), [`AURORA-STYLESHEET-REBUILD-PLAN.md`](../AURORA-STYLESHEET-REBUILD-PLAN.md), [`REVIVE-AURORA-PORT-2026-07-24.md`](../archive/REVIVE-AURORA-PORT-2026-07-24.md), live curl this session.

---

## 2. Two costed paths

### Path A — Ground-up rewrite (“throw them away”)

**Meaning:** Author a new layered token system and **replace** current rule bodies as net-new CSS; treat the five sheets as disposable. Visual parity is the product of rewriting, not of wrapping.

| Dimension | Estimate |
|---|---|
| Calendar | **3–6 weeks** focused Track B before Wave 2 theme PRs are safe again |
| Agent / PR cost | New primitives + every homepage/page component re-authored; ~8–15 theme PRs plus full re-baseline after each major cut |
| User-visible benefit alone | **None** until Wave 2 rides the new sheets |
| Regression risk | **High** — every route can shift; no working rule retained by default |
| Rollback | Previous theme zip (proven), but mid-rewrite state is hard to reason about if big-bang |
| Wave 2 impact | Styling work **stalls** behind parity; content-only issues can proceed |
| Relation to #493 | **Park or revert** the wrap scaffold; tokens might survive, wrappers do not define the strategy |

**When A would be right:** proof that wrap-and-migrate cannot beat `global-styles` without `!important`, or that doubled layers make per-component PRs more expensive than rewrite. Neither has been proven; #493 exists to spike the former.

### Path B — Staged repair (cascade scaffold + migrate) — RECOMMENDED

**Meaning:** Keep rules that render correctly. Introduce hierarchy (`@layer`, `--kk-*`, explicit enqueue deps, `09-late.css`). Migrate/delete debt **one component or layer per PR** behind visual-diff. Delete dead CSS after coverage. Retire page-content CSS in Track A (#480). Rename classes last (#481).

| Dimension | Estimate |
|---|---|
| Calendar | Step 2 (1.5.0) = **days** after pixel gate; full sequence to 1.6.1 ≈ **2–4 weeks** interleaved with Wave 2 |
| Agent / PR cost | Already spent: #472, #473 closed; #493 authored. Remaining: #475→#481 as planned (~1 PR per step + N component PRs under #477) |
| User-visible benefit alone | Low early (behavior-neutral scaffold); rises as components consolidate and dead CSS drops (~22 KB high-confidence) |
| Regression risk | **Medium → low per PR** — each step independently revertible via prior zip |
| Rollback | Per-step zip + `git revert`; abandon anytime after any shipped step |
| Wave 2 impact | **Parallel** for content; theme-touching sections land rules in `@layer components` after 1.5.0 |
| Relation to #493 | **#493 is Path B step 1 of shipping** — confirm and finish the gate |

This matches the plan’s own discipline (“Delete no rule. Rename no class” at scaffold; migrate later) and the evidence that incremental edits *do* shrink debt where applied (#408/#409), while unstructured boy-scout **without** hierarchy lost to Revive (`!important` doubled).

---

## 3. Recommendation detail

**Confirm Path B.** Align #423’s recorded decision text with the work already started:

1. Merge/deploy **PR #493** only after #494 pixel gate (11 routes × 3 viewports).
2. Preflight R-3: KK verifies snippet #14 + media #12631 gone.
3. Continue sequence #475 → #481; do not open a parallel throwaway rewrite.
4. Boy-scout CSS only when a content/UX issue requires it; new theme rules post-1.5.0 go in `@layer components` with **0** new `!important` (ratchet enforces).

**Label hygiene:** treat the 2026-07-24 “Path A” comment as “rebuild the *hierarchy* (tokens + layers),” not “delete every rule and rewrite from zero.” The implementation epic already encodes B.

---

## 4. Acceptance mapping (#423)

| Criterion | This brief |
|---|---|
| Complete CSS surface inventory + load order | §1 (theme, Boost, global-styles, page-content, snippets, marquee inline) |
| Recommendation memo A vs B with effort, risk, rollback | §2–§3 |
| KK decision recorded | **Awaiting your comment on #423** |
| No live theme changes under this issue before decision | Honored — docs only |

---

## 5. Comment template (paste on #423)

```markdown
## Decision (2026-07-26) — stylesheet hierarchy

**Path B — staged repair via the 1.5.0 cascade scaffold (PR #493 / #474).**

Clarifies the 2026-07-24 “Path A” note: we rebuild hierarchy (layers + tokens + late sheet),
we do **not** throw away and rewrite the five sheets from zero.

Next: finish #494 pixel gate → merge #493 → continue #475–#481.
Preflight: confirm snippet #14 + media #12631 retired before upload.

Brief: `docs/current-state/reports/stylesheet-hierarchy-decision-brief-20260726.md`
```

---

**Prepared:** 2026-07-26 swarm Track B agent.  
**Related:** #423 · #256 · #472 · #473 · #474 · PR #493 · #494 · #475–#481 · plan `AURORA-STYLESHEET-REBUILD-PLAN.md`.
