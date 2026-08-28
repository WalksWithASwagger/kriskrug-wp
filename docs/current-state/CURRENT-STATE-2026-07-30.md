# Current State Snapshot - 2026-07-30

**Snapshot time:** 2026-07-30 truth reset; live counters and versions refreshed 2026-08-28 20:38Z: WordPress `7.0.4`; Aurora live and repo `main` both `1.6.9`.
**Branch:** `main` (docs PR lands from lane-scoped branch)
**Mode:** Ops hygiene (Phases 0–3) then Track A / Track B product lanes.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN` / `WORK_PLAN_DEFAULT`).

Master sequence: [`MASTER-PLAN-2026-07-30.md`](MASTER-PLAN-2026-07-30.md). Latest dated runbook: [`WORK-PLAN-2026-08-25.md`](WORK-PLAN-2026-08-25.md).

## Verified State

> **Counters refreshed 2026-08-28T20:38Z after the verified #318 closeout.** These are the values `make current-state-drift-check` compares against. They can move as soon as a PR or issue changes, so re-read with the commands below before treating drift as a regression.

- `origin/main` was clean and synchronized before this docs-truth branch; its latest commit was PR #921 (`648a942`).
- Open PRs: `0` (`gh pr list --state open --limit 100 --json number --jq 'length'`, 2026-08-28T20:38Z).
- Open issues: `39` (`gh issue list --state open --limit 300 --json number --jq 'length'`, 2026-08-28T20:38Z). This includes the correctly open Testimonials deploy issue #602 and local visual-prune gate #749; #318 is closed after authenticated proof classified all three packages as unpublished and retained all 13 images.
- Production still publicly reports WordPress `7.0.4`.
- Live Aurora theme (`style.css` Version header): `1.6.9` (public readback 2026-08-28).
- Repo Aurora theme (`theme/kk-aurora/` on `main`): `1.6.9`; live and repo are in parity.
- Theme deploy ledger: `theme/kk-aurora/CHANGELOG.md`. The public `style.css` readback is authoritative for what production runs, never the repo header.
- WordPress draft queue: `0` scheduled posts, `66` draft posts, `4` draft pages.
  - Authenticated read 2026-08-28. Unauthenticated reads report `unavailable`, not a trustworthy empty queue.
- WP public smoke passes with expected WordPress `7.0.4` (`make status-readonly`, 2026-08-28).
- `/projects/` → `301` to `/work/`.
- Homepage reveal safety net: absent. GSAP/ScrollTrigger CDN: absent.

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Alt-text residual correction | #4 | Three media writes remain; media 7637 needs a corrected reviewed proposal before a new live approval |
| Testimonials live deploy | #602 | Reopened 2026-08-28; live page 2409 is still the legacy 19-card body and needs its snapshot/editorial/approval gate |
| Third-party script performance receipt | #706 | Script diet is live; matching post-change PSI evidence remains incomplete |
| Local visual capture prune | #749 | Pair-safe dry-run is merged; three exact directories (~906 MiB) await separate deletion approval |
| Site redesign epic | #403 | Track B roadmap; split into lane-scoped PRs |

## What changed since CURRENT-STATE-2026-07-16

- Aurora advanced to **1.6.9** on `main` and live; the live↔repo parity check remains the authority.
- Issue #4 completed the broad Batch 3 media pass, restored two wrong-identity writes, and stopped safely with three reviewed/corrected targets remaining.
- The Speaking rebuild is live with two click-to-load privacy-hosted video facades. #640 closed after two same-method mobile Lighthouse runs stayed within 2.62% of the 3,032.93 ms baseline, identified the first-party hero image as LCP, and passed the live embed contract.
- Testimonials issue #602 was reopened because its runbook-only PR closed it while the live page remained undeployed.
- Issue #318 closed as a verified no-delete result: all three WordPress objects are drafts, so the exact removal allow-list is empty and all 13 tracked images remain in place.
- Open issues moved ~77 → **39**; open PRs were **0** at the 2026-08-28 refresh.
- Competing work plans are historical; this snapshot plus `WORK-PLAN-2026-08-25.md` and a fresh `make status-readonly` run are the front door.

## Stash / secrets notes

- Cloud agents need process env `WP_USER` / `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Laptop Varlock does not inject into Cloud.
- Prefer [`.env.schema`](../../.env.schema); do not commit plaintext secrets. Rollout: [`VARLOCK-ROLLOUT-2026-07-16.md`](VARLOCK-ROLLOUT-2026-07-16.md).
- `git stash list` was empty on 2026-08-28. Issue #738 is closed: the stale `/private/tmp` registrations and approved merged branch refs are gone, and the registered worktree/local branch/remote-head inventories each contain only `main`.
