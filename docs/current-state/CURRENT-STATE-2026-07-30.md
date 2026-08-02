# Current State Snapshot - 2026-07-30

**Snapshot time:** 2026-07-30 (truth reset after debt/docs/bloat audit; Aurora 1.5.0 live==repo).
**Branch:** `main` (docs PR lands from lane-scoped branch)
**Mode:** Ops hygiene (Phases 0–3) then Track A / Track B product lanes.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN` / `WORK_PLAN_DEFAULT`).

Master sequence: [`MASTER-PLAN-2026-07-30.md`](MASTER-PLAN-2026-07-30.md). Day runbook: [`WORK-PLAN-2026-07-30.md`](WORK-PLAN-2026-07-30.md).

## Verified State

> **Counters refreshed 2026-08-02** after the voice-sweep / events / testimonials swarm. The 2026-07-30 narrative below the counters still stands; only the numbers and theme versions moved.

- `origin/main` includes Aurora **1.5.0** cascade scaffold (PR #493 / #474) and AGENTS version reconcile (`a6608e3`).
- Open PRs: `0` (2026-08-02; the whole swarm queue merged, #556/#560/#561/#562 Dependabot included).
- Open issues: `54` (2026-08-02; ~30 were minted by the 2026-08-01 swarm packets and most have since closed).
- Production still publicly reports WordPress `7.0.2`.
- Live Aurora theme (`style.css` Version header): `1.5.7` (readback 2026-08-02 → `Version: 1.5.7`), deployed 2026-08-01 with the full-bleed portrait hero (PR #618).
- Repo Aurora theme (`theme/kk-aurora/` on `main`): `1.5.8`. Repo is **one patch ahead** of live: 1.5.8 adds the `aurora-tstm` testimonials CSS (PR #629), built but not deployed, gated on #601.
- Theme deploy ledger: `theme/kk-aurora/CHANGELOG.md`. The public `style.css` readback is authoritative for what production runs, never the repo header.
- WordPress draft queue: `0` scheduled posts, `67` draft posts, `4` draft pages.
  - Counters above are the authenticated shape read on 2026-08-02. Unauthenticated cloud reads report `unavailable` / false zeros until `WP_USER` + `WP_APP_PASSWORD` are present — that zero is a **false zero**, not an empty queue.
- WP public smoke: `0` failures / `0` warnings (`make morning-truth` 2026-08-02).
- `/projects/` → `301` to `/work/`.
- Homepage reveal safety net: absent. GSAP/ScrollTrigger CDN: absent.

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Docs front door + archive | #549 | In progress via MASTER-PLAN Phase 0–1 |
| Binary reclaim A+D | #318 / #369 | Inventory done; execute after allow-list (plan locks A+D) |
| Theme rebuild next step | #475 | Unblocked after #474/#493; Aurora **1.5.1** (reset/base + drop cap) |
| Futureproof Festival post | #496–#500 | Track A; draft-only, needs human review |
| Stylesheet Path A epic | #423 | Decision already Path A; retitle from DECISION shell |

## What changed since CURRENT-STATE-2026-07-16

- Aurora **1.5.0** landed on `main` and live (cascade `@layer` + `--kk-*` tokens); #545 closed; live↔repo parity check exists (`make check-live-parity`).
- Homepage newsletter rewrite (#416 / PR #505) is on `main` at 1.4.9 lineage and shipped with/under the 1.5.0 line.
- Morning-truth cadence restored (#547 / #553).
- Open issues moved ~77 → **43**; open PRs **1** (Dependabot).
- Competing “active” work plans (07-16 / 07-19 / 07-26) demoted; this snapshot + WORK-PLAN-2026-07-30 are the front door.

## Stash / secrets notes

- Cloud agents need process env `WP_USER` / `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Laptop Varlock does not inject into Cloud.
- Prefer [`.env.schema`](../../.env.schema); do not commit plaintext secrets. Rollout: [`VARLOCK-ROLLOUT-2026-07-16.md`](VARLOCK-ROLLOUT-2026-07-16.md).
- Local laptop may still hold untracked draft packets (`no-one-knows…`, `the-unmakable…`) and IndexNow fix files — treat as Track A local WIP, not as absent from the product backlog.
