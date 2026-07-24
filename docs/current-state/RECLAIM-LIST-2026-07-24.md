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

## Explicit keep

- Newest `docs/current-state/reports/morning-truth-*.md`
- `fixes/`, active `content/source-packs/`, theme deploy zips under Desktop (outside repo)
- `content/source-packs/site-photography-2026/` (ingested 2026-07-24)

## Next step

Reply on #369 with an exact allow-list of paths (or “approve Tier 1”). Then open a focused delete PR.
