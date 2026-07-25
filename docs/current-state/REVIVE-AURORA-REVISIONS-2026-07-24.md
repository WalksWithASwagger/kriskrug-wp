# Revive → Aurora revision plan (post 1.4.0)

**Date:** 2026-07-24  
**Baseline:** Live Aurora **1.4.0** (commit `819f182`) + full theme sync media **#12632**  
**Evidence:** `backup/aurora-deploy-20260724/e2e/`  
**Contract:** [REVIVE-AURORA-PORT-2026-07-24.md](REVIVE-AURORA-PORT-2026-07-24.md)

## Goal

Close the gap between “stranger recognizes Revive direction” (done) and “editorial polish + a11y + pack density match Revive about/services” (not done).

## Priority stack

### P0 — Accessibility / trust (Track B)

| ID | Issue | Evidence | Proposed fix | Done when |
|---|---|---|---|---|
| R1 | Burnt-orange kickers fail AA normal (3.42:1) | Contrast math on `#d94a1f` / `#efe6d2` | Darken accent for text to ≥4.5:1 (e.g. `#b53c18`) while keeping bright orange for large/CTA fills; or use ink for small kickers + orange underline | pa11y/contrast spot-check pass on kickers |
| R2 | Focus rings weak/missing on cream controls | CTA `outline: none` under focus probe | Force `--focus-ring` / `outline: 2px solid var(--revive-accent)` on `:focus-visible` for header/footer buttons + nav | Keyboard tab through header shows clear ring |
| R3 | Duplicate Skip links | DOM count = 2 | Deduplicate theme + FSE/plugin skip link | Exactly one skip link |

### P1 — Chrome density (Track B)

| ID | Issue | Evidence | Proposed fix | Done when |
|---|---|---|---|---|
| R4 | Primary nav wraps awkwardly (esp. ≤768 / wide with Photography) | Screenshots; 7-item nav | Compact tracking, optional “More” disclosure on small screens, or two-row intentional masthead nav | Single coherent header composition at 375/768/1280 |
| R5 | Header shell feels logo-centered vs Revive sticky left brand | Visual QA | Tighten grid (`auto 1fr auto`), reduce shell padding, ensure brand stays left of content max | Matches Revive site-header silhouette |
| R6 | Rainbow word / riso motifs underused vs Revive | Homepage “message” gradient exists but easy to miss | Slightly larger italic rainbow span; optional riso rule under section heads | Stranger notices rainbow accent without hunting |

### P2 — Inner page packs (Track A, separate commits)

| ID | Issue | Evidence | Proposed fix | Done when |
|---|---|---|---|---|
| R7 | Contact still shows cyan bar / old accent chrome | Contact screenshot | Rewrite Contact pack to cream/ink density (after #421 portrait keep) | No cyan SaaS bars; portrait-led Revive density |
| R8 | Services cards keep drop-cap / rounded SaaS card feel | Services screenshot | Rewrite Services HTML pack to Revive “Strategic intervention” ribbon cards | Matches homepage services band language |
| R9 | Speaking / About / Work / Photography / Sponsor-deck uneven | Spot checks | One pack per commit: restyle to `.kk-page` tokens + remove leftover cyan | Each route screenshot passes cream/ink smell test |
| R10 | Blog archive H1 still “Field notes…” | `/blog/` HTML | Rename to **Writing** (KK rejected Field notes on WP chrome) | No “Field notes” in archive title |
| R11 | Work page body still says “Field notes, talks…” | `/work/` HTML | Soft rewrite to “Writing, talks…” | No Field notes phrasing |

### P3 — Performance / cleanup (Ops)

| ID | Issue | Proposed fix |
|---|---|---|
| R12 | Jetpack Boost concatenates theme CSS | After each theme ship, confirm Boost hash refreshes; document in release checklist |
| R13 | Temp media 12631/12632 + snippets 14/15 | Delete after 7-day rollback window |
| R14 | Self-host latin-ext fonts if non-Latin names render poorly | Add latin-ext woff2 for Space Grotesk / DM Sans |
| R15 | pa11y not in CI for cream surfaces | Add `make a11y-cream-spot` with 4 URLs |

## Sequencing (recommended)

```text
Week slice A (Track B only)
  R2 focus rings → R1 accent contrast → R3 skip link → R4/R5 header
  Version bump 1.4.1, package, sync, e2e

Week slice B (Track A only)
  R10 blog title → R11 work copy → R7 Contact → R8 Services
  Then Speaking / About / Work / Photography / Sponsor-deck as capacity allows
```

Do **not** mix Track A pack rewrites with Track B theme commits.

## Non-goals (still)

- Leaving WordPress / Pagely
- Porting TanStack / Lovable / Supabase MCP
- Rewriting 900 post interiors
- Restoring “Dispatch” subscribe UI or Field notes chrome labels

## Definition of done for “revisions complete”

- Accent text meets AA on cream; focus rings visible on paper.
- Header reads as one composition at 375/768/1440 with Photography in IA.
- Contact + Services packs no longer look like dark/cyan SaaS islands.
- Blog/Work no longer say “Field notes” unless KK reverses that decision.
- E2E report regenerated green; rollback zip retained.

## Immediate next step

Open Track B issue/PR for **1.4.1**: R1 + R2 + R3 (+ R4 if quick). Hold Track A pack rewrites until chrome a11y lands.
