# Current State Snapshot - 2026-07-30

**Snapshot time:** 2026-07-30 (truth reset after debt/docs/bloat audit). Live counters and versions refreshed 2026-08-15: WordPress `7.0.4`; Aurora live and repo `main` in sync at `1.6.5`.
**Branch:** `main` (docs PR lands from lane-scoped branch)
**Mode:** Ops hygiene (Phases 0–3) then Track A / Track B product lanes.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN` / `WORK_PLAN_DEFAULT`).

Master sequence: [`MASTER-PLAN-2026-07-30.md`](MASTER-PLAN-2026-07-30.md). Latest dated runbook: [`WORK-PLAN-2026-08-15.md`](WORK-PLAN-2026-08-15.md).

## Verified State

> **Counters refreshed 2026-08-13T00:46Z.** The two GitHub counters are the values `make current-state-drift-check` compares against. They can move as soon as a PR or issue changes, so re-read with the commands below before treating drift as a regression.

- `origin/main` includes Aurora **1.6.5** and the merged Gorgeous Ghost draft package (PR #722).
- Open PRs: `1` (`gh pr list --state open --limit 100 --json number --jq 'length'`, 2026-08-13T00:46Z): draft PR #710, intentionally parked for cherry-pick review rather than raw merge.
- Open issues: `40` (`gh issue list --state open --limit 300 --json number --jq 'length'`, 2026-08-13T00:46Z).
- Production still publicly reports WordPress `7.0.4`.
- Live Aurora theme (`style.css` Version header): `1.6.5` (public readback 2026-08-15).
- Repo Aurora theme (`theme/kk-aurora/` on `main`): `1.6.5`. Live and repo are **in sync**.
- Theme deploy ledger: `theme/kk-aurora/CHANGELOG.md`. The public `style.css` readback is authoritative for what production runs, never the repo header.
- WordPress draft queue: `0` scheduled posts, `65` draft posts, `4` draft pages.
  - Authenticated read 2026-08-12. Unauthenticated cloud reads report `unavailable` / false zeros until `WP_USER` + `WP_APP_PASSWORD` are present — that zero is a **false zero**, not an empty queue.
- WP public smoke: all eight public surfaces pass with expected WordPress `7.0.4` (`make wp7-smoke`, 2026-08-12).
- `/projects/` → `301` to `/work/`.
- Homepage reveal safety net: absent. GSAP/ScrollTrigger CDN: absent.

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Third-party script performance diet | #706 | High priority; swarm-ready; needs human review |
| Speaking rebuild | #419 | High priority; content/UX; needs human review |
| Testimonials live deploy | #602 | High priority; snapshot-gated production change |
| Repo bloat reduction | #318 | Inventory exists; cleanup remains a separate approved operation |
| Site redesign epic | #403 | Track B roadmap; split into lane-scoped PRs |

## What changed since CURRENT-STATE-2026-07-16

- Aurora **1.5.0** landed on `main` and live (cascade `@layer` + `--kk-*` tokens); #545 closed; live↔repo parity check exists (`make check-live-parity`).
- Homepage newsletter rewrite (#416 / PR #505) is on `main` at 1.4.9 lineage and shipped with/under the 1.5.0 line.
- Morning-truth cadence restored (#547 / #553).
- Open issues moved ~77 → **40**; open PRs **1** (parked draft #710).
- Competing “active” work plans (07-16 / 07-19 / 07-26) demoted; this snapshot + WORK-PLAN-2026-07-30 are the front door.

## Stash / secrets notes

- Cloud agents need process env `WP_USER` / `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Laptop Varlock does not inject into Cloud.
- Prefer [`.env.schema`](../../.env.schema); do not commit plaintext secrets. Rollout: [`VARLOCK-ROLLOUT-2026-07-16.md`](VARLOCK-ROLLOUT-2026-07-16.md).
- `git stash list` was empty on 2026-08-12. The merged #722 feature worktree still exists locally; preserve it until cleanup is explicitly approved.
