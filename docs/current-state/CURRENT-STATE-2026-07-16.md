# Current State Snapshot - 2026-07-16

**Snapshot time:** 2026-07-16 (orchestra refresh after PR #359 merge + Monday queue #360–#366).
**Branch:** `main` (tip `1b5ca7d` — merge of PR #359)
**Mode:** Track A ops + Track B deploy gate.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN`).

## Verified State

- `origin/main` is at `1b5ca7d` (merge of PR #359, 2026-07-16).
- Open PRs: `1` (this orchestra/hygiene stack — #367).
- Open issues: `42` (Monday day-queue #360–#366 plus long-run ops #368–#369).
- Production still publicly reports WordPress `7.0.1`.
- Live Aurora theme (`style.css` Version header): `1.3.37`.
- Repo Aurora theme (`theme/kk-aurora/`): `1.3.40`.
- WordPress draft queue: `5` scheduled posts, `64` draft posts, `4` draft pages.
  - Counts above are the last **authenticated** shape retained from earlier morning-truth runs. Unauthenticated cloud reads still report missing `.env` / false zeros until `WP_USER` + `WP_APP_PASSWORD` are present — that zero is a **false zero**, not an empty queue.
- WP public smoke: route checks pass; version gate fails only when tools still expect `6.9.4`.
- `/projects/` → `301` to `/work/`.
- Monday orchestra agent-safe slices: `docs/current-state/reports/orchestra-monday-queue-20260716-004321Z.md`.
- Stale branch prune + triage: `docs/current-state/reports/repo-hygiene-prune-triage-20260716.md` (25 remote heads deleted; #368 keep/kill leftovers).
- Long-run day unlock order: `docs/current-state/WORK-PLAN-LONG-RUN-2026-07-16.md`.

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Aurora SEO metadata deploy | #351 / #362 | **1.3.40** package + checksums verified (`backup/aurora-deploy-20260716/DEPLOY-HANDOFF.md`). Live still **1.3.37**. Do not upload the 2026-07-13 **1.3.39** zip. |
| Measured July publisher batch | #339 / #363 | Repo handoffs ready; blocked on live `1.3.40`, refreshed checklist (1.3.40 hashes), secrets, KK ticks. |
| Topic-hub internal links | #278 / #284 / #364 | Handoff + 2026-07-16 public recheck green; write needs KK `patch_id` list. |
| Accessibility statement | #288 / #48 / #365 | Draft packet on `main`; WP draft create blocked on human gates + secrets. `/accessibility/` still 404. |
| About/bio archive module | #290 | Plans on `main` (parking lot). |

## What changed since CURRENT-STATE-2026-06-23

- WordPress upgraded live to **7.0.1**.
- Aurora advanced on `main` through **1.3.40**; production remains on **1.3.37**.
- July SEO wave merged (#332–#358 family): descriptions, OG/canonical repairs, schema identity prep, publisher handoffs, body-H1 migration tooling, search-title module.
- July agent ops stack merged: `publish_common` (#312/#315), content packets (#311), Cloud AGENTS notes (#310).
- Front-door docs + day runbook merged via PR #359; Monday GitHub queue filed as #360–#366; long-run ops #368–#369.
- Open issues moved ~33 → **42** after Monday + long-run queue filing; open PRs are **1** while the orchestra/hygiene stack (#367) is open.
- Declared draft-page count normalized to `4` (was `5` in the June snapshot).

## Stash / secrets notes

- Cloud agents still need `scripts/notion-to-wp/.env` or injected `WP_USER` / `WP_APP_PASSWORD` (and optional `NOTION_TOKEN`).
- Prefer the committed [`.env.schema`](../../.env.schema) as the agent-readable env contract; do not commit plaintext secrets.
