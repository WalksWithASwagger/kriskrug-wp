# Current State Snapshot - 2026-07-16

**Snapshot time:** 2026-07-16 (from `make status-readonly` plus live public probes in the Cursor Cloud session).
**Branch:** `main` (tip `b07eece` — merge of PR #358)
**Mode:** Track A ops + Track B deploy gate.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN`).

## Verified State

- `origin/main` is at `b07eece` (merge of PR #358, 2026-07-14).
- Open PRs: `0`.
- Open issues: `33`.
- Production still publicly reports WordPress `7.0.1`.
- Live Aurora theme (`style.css` Version header): `1.3.37`.
- Repo Aurora theme (`theme/kk-aurora/`): `1.3.40`.
- WordPress draft queue: `5` scheduled posts, `64` draft posts, `4` draft pages.
  - Counts above are the last **authenticated** shape retained from earlier morning-truth runs. Unauthenticated cloud reads still report missing `.env` / false zeros until `WP_USER` + `WP_APP_PASSWORD` are present — that zero is a **false zero**, not an empty queue.
- WP public smoke: route checks pass; version gate fails only when tools still expect `6.9.4`.
- `/projects/` → `301` to `/work/`.

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Aurora SEO metadata deploy | #351 | Package prepared as **1.3.39**; repo has since moved to **1.3.40** (search titles). Live still **1.3.37**. Zip artifacts live on KK machine under `backup/aurora-deploy-20260713/` (not in git). |
| Measured July publisher batch | #339 | Repo handoffs ready; live writes blocked on explicit checklist approval + Aurora deploy. |
| Topic-hub internal links | #278 / #284 | Handoff on `main` (`fixes/issue-284-*`). |
| Accessibility statement | #288 / #48 | Draft packet on `main` (`content/drafts/accessibility-statement-2026-07/`). |
| About/bio archive module | #290 | Plans on `main`. |

## What changed since CURRENT-STATE-2026-06-23

- WordPress upgraded live to **7.0.1**.
- Aurora advanced on `main` through **1.3.40**; production remains on **1.3.37**.
- July SEO wave merged (#332–#358 family): descriptions, OG/canonical repairs, schema identity prep, publisher handoffs, body-H1 migration tooling, search-title module.
- July agent ops stack merged: `publish_common` (#312/#315), content packets (#311), Cloud AGENTS notes (#310).
- Open issues dropped from 48 → ~33; open PRs remain 0.
- Declared draft-page count normalized to `4` (was `5` in the June snapshot).

## Stash / secrets notes

- Cloud agents still need `scripts/notion-to-wp/.env` or injected `WP_USER` / `WP_APP_PASSWORD` (and optional `NOTION_TOKEN`).
- Prefer the committed [`.env.schema`](../../.env.schema) as the agent-readable env contract; do not commit plaintext secrets.
