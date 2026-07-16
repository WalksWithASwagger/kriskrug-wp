# Documentation + crust audit — 2026-07-16

**Mode:** docs/code hygiene only. No live WP writes.  
**Companion:** `repo-hygiene-prune-triage-20260716.md`, orchestra Monday queue report.

## What this pass fixed (in PR #367)

| Area | Change |
|---|---|
| `docs/current-state/README.md` | Front door counts/links; `.env.schema` + 1.3.40 deploy paths; TL;DR marked historical; May-24 links → `archive/` |
| `docs/INDEX.md` | Active plan → 2026-07-16; morning-truth → 20260716; archive path fixes |
| Historical banners | `WORK-PLAN-2026-07-01`, `CURRENT-STATE-2026-06-23`, `HANDOFF-2026-06-17`, `SITE_INVENTORY`, `REPO_STATE`, `DRAFT-QUALITY-RESET`, `POST-SHIP-AUDIT-WORKPLAN` |
| Root `README.md` | WordPress **7.0.1** |
| `CONTRIBUTING.md` | Drop Cloudways as primary Track B path |
| `Makefile` | `wp7-smoke` help example → `EXPECT_VERSION=7.0.1` |
| `CURRENT-STATE-2026-07-16.md` | Internal contradiction on open PR/issue counts |

## Human closeout candidates (GitHub UI — agent cannot close)

| Issue | Action |
|---|---|
| **#361** | **Close** — PR #359 merged |
| **#254** | **Close** — shipped via #312/#315 (`publish_common` on main) |
| **#322** | **Close** after #367 merges — writer safety tests landed |
| **#269** / **#270** | **Close or fold** into #290 |
| **#351** | **Retitle** toward Aurora **1.3.40** (keep open until deploy) |
| **#36** | Measure/closeout only — July SEO wave largely shipped |
| **#48** | Prefer #288/#365 as active a11y draft lane |

## Crusty code — leave alone unless KK asks

| Path | Note |
|---|---|
| `.github/agents/` + parked `agent-pr-generator.yml` | Dormant May swarm evidence |
| `publish_*.py` one-offs | Already on `publish_common`; keep for publisher runs |
| `scripts/mcp-wordpress-remote.sh`, `wordcamp-mcp-smoke.py` | Secrets-gated; not day path |
| `marquee/weekly-proposals`, `fix/jetpack-open-graph-enable` | Remote heads — keep/kill via **#368** |

## Still useful agent fillers (no secrets)

1. #256 CSS dead-code / schema-snippets reconcile (repo-only)
2. #46 public pa11y five-route refresh
3. #4 public image-alt inventory (no media PATCH)
4. After #367 merges: delete `cursor/orchestra-monday-queue-2853`
