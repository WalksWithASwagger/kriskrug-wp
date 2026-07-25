# Reclaim list — #369 / #318 (2026-07-24)

**Status:** ranked proposal for KK path-by-path approval. **No deletes in this commit.**

Source inventory: `docs/current-state/reports/repo-hygiene-prune-triage-20260716.md`.

## Rules

- Do not `git filter-repo` / force-push without a separate thread.
- Prefer deleting unreferenced PNG/screenshot binaries; keep markdown morning-truth reports.
- Confirm no open deploy/rollback depends on a `backup/` path before removing it.

## Tier 1 — safe after spot-check (largest win)

| Path pattern | Why |
|---|---|
| `content/drafts/**/screenshots/**/*.png` | Local QA captures; not runtime |
| `content/drafts/**/*.png` where post is already live and assets are in WP media | Duplicate of CDN |
| `docs/current-state/reports/**/screenshots/**/*.png` | Smoke/visual archives |

## Tier 2 — keep markdown, drop binary noise

| Path pattern | Why |
|---|---|
| `docs/current-state/reports/*-smoke*.png` | One-off visual proofs |
| Older `docs/current-state/reports/morning-truth-*.md` older than 60 days | Optional archive; keep newest 3 |

## Tier 3 — backup age-out (confirm first)

| Path | Gate |
|---|---|
| `backup/` snapshots older than active rollback windows | Confirm no open Pagely/theme rollback references them |

## Untracked-by-design (no reclaim needed, but budget for the disk)

| Path | Why it is here |
|---|---|
| `docs/current-state/reports/visual-baseline/<run-id>/` | Visual-regression captures (#473). **Never tracked** — the whole artifact root is git-ignored one level down and `make visual-guard` re-asserts that against the index after every run. Only `manifest-*.json`, `diff-*.json` and `report-*.md` at the top level are committed. |

These directories cost nothing in `.git`, but a full 11-route × 3-viewport run at
device scale 2 is roughly 250–450 MB of PNG **on disk**. Baselines regenerate in
one command, so there is no archival argument for keeping old ones: run
`make visual-prune KEEP=2` (or `KEEP=1`) after a rebuild step lands.

## Explicit keep

- Newest `docs/current-state/reports/morning-truth-*.md`
- `fixes/`, active `content/source-packs/`, theme deploy zips under Desktop (outside repo)
- `content/source-packs/site-photography-2026/` (ingested 2026-07-24)

## Next step

Reply on #369 with an exact allow-list of paths (or “approve Tier 1”). Then open a focused delete PR.
