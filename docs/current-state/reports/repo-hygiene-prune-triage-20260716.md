# Repo hygiene — stale branch prune + issue triage (2026-07-16)

**Mode:** agent-only; no live WP writes.  
**Companion:** Monday orchestra `orchestra-monday-queue-20260716-004321Z.md`.

## Branch prune (executed)

Deleted **25** remote heads that were already **MERGED** or **CLOSED** (or abandoned `codex/system-coherence-cleanup-20260712` with no PR). Kept:

| Branch | Why kept |
|---|---|
| `main` | canonical |
| `cursor/orchestra-monday-queue-2853` | open PR #367 |
| `marquee/weekly-proposals` | experimental Marquee lane — needs KK keep/kill call |
| `fix/jetpack-open-graph-enable` | pre-Aurora OG experiment — needs KK keep/kill call |

After #367 merges, delete `cursor/orchestra-monday-queue-2853`.

## Issue triage (Track A / Track B vs noise)

### Ship-when-unlocked (high leverage)

| # | Track | Gate |
|---|---|---|
| #362 / #351 | B | KK upload 1.3.40 SHA |
| #339 / #363 | A | live 1.3.40 + refreshed checklist + secrets |
| #284 / #364 | A | KK `patch_id` list + secrets |
| #288 / #365 | A | human wording gates + secrets → **draft only** |
| #316 | A/ops | live snippet write |
| #345 | A/ops | live `blogname` |
| #353 | A | one target at a time after #339 |
| #331 | A/ops | human archive policy |

### Agent-safe now (repo)

| # | Action this session |
|---|---|
| **#322** | Writer safety contract tests (**done** in this PR) |
| **#318** | Bloat reclaim inventory (**done** below) — no mass delete |
| #256 | CSS/snippets audit — later slice |
| #46 / #4 | Public pa11y / alt inventory — later slice |

### Close / fold (human UI — agent cannot close)

| # | Why |
|---|---|
| #361 | Done via #359 |
| #254 | Shipped via #312/#315 |
| #269 / #270 | Fold into #290 |
| #351 title | Rename toward 1.3.40 (stale “1.3.39”) |
| #36 | Mostly shipped by July SEO wave — closeout/measure only |

### Parking / low day leverage

#122 undesigned pages · #222 umbrella epic · #95 swarm-parked · #127 blocked mobile · #276 Jetpack delete · #274 GSC human

## #318 reclaim inventory (read-only)

| Path | Approx size | Hot spots |
|---|---:|---|
| `content/drafts/` | **247 MB** / 559 files | PNGs dominate (~197 MB). Largest drafts: sovereign-ai-for-whom, god-skills, data-center-protest-signs, human-element-shane-loki |
| `docs/current-state/reports/` | **28 MB** / 203 files | PNGs ~25 MB under screenshots / smoke captures |
| `backup/` | **18 MB** / 231 files | HTML + JSON snapshots + a few zips |

**KK-gated prune plan (do not execute without approval):**

1. Gitignore future non-md spill under `docs/current-state/reports/` (screenshots/json dumps) — already partially discussed in `REPO-HYGIENE-AUDIT-2026-07-12.md`.
2. Move published draft image folders to git-lfs or external media once posts are live — do not rewrite history in-session.
3. Age-out `backup/` snapshots older than the active rollback windows after confirming no open deploy depends on them.
4. Keep morning-truth markdown reports; they are the startup source of truth.

## Remaining remote branches needing a keep/kill call

- `marquee/weekly-proposals`
- `fix/jetpack-open-graph-enable`
