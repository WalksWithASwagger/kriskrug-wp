# Current State Snapshot - 2026-07-30

**Snapshot time:** 2026-07-30 truth reset; live counters and versions refreshed 2026-08-28 22:46Z: WordPress `7.0.4`; Aurora live and repo `main` both `1.6.9`.
**Branch:** `main` (docs PR lands from lane-scoped branch)
**Mode:** Ops hygiene (Phases 0–3) then Track A / Track B product lanes.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN` / `WORK_PLAN_DEFAULT`).

Master sequence: [`MASTER-PLAN-2026-07-30.md`](MASTER-PLAN-2026-07-30.md). Latest dated runbook: [`WORK-PLAN-2026-08-25.md`](WORK-PLAN-2026-08-25.md).

## Verified State

> **Counters refreshed 2026-08-28T22:46Z after retiring #481 and merging the #339 guard refresh.** These are the values `make current-state-drift-check` compares against. They can move as soon as a PR or issue changes, so re-read with the commands below before treating drift as a regression.

- `origin/main` was clean and synchronized before this docs-truth branch; its latest commit was PR #929 (`71fac0e`).
- Open PRs: `0` (`gh pr list --state open --limit 100 --json number --jq 'length'`, 2026-08-28T22:46Z).
- Open issues: `35` (`gh issue list --state open --limit 300 --json number --jq 'length'`, 2026-08-28T22:46Z). #481 is retired; #339 remains open with refreshed exact guards and no live write.
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
| Alt-text residual correction | #4 | Media 6985, 7637, and 8871 have current reviewed proposals and exact authenticated dry runs; live writes require fresh approval naming those three IDs |
| Measured publisher batch | #339 | All nine identities are current; exact approval is still required for two SEO overwrites and five content payloads |
| Testimonials live deploy | #602 | Reopened 2026-08-28; live page 2409 is still the legacy 19-card body and needs its snapshot/editorial/approval gate |
| Site redesign epic | #403 | Track B roadmap; split into lane-scoped PRs |

## What changed since CURRENT-STATE-2026-07-16

- Aurora advanced to **1.6.9** on `main` and live; the live↔repo parity check remains the authority.
- Issue #4 completed the broad Batch 3 media pass, restored two wrong-identity writes, and stopped safely with three reviewed/corrected targets remaining.
- The Speaking rebuild is live with two click-to-load privacy-hosted video facades. #640 closed after two same-method mobile Lighthouse runs stayed within 2.62% of the 3,032.93 ms baseline, identified the first-party hero image as LCP, and passed the live embed contract.
- Testimonials issue #602 was reopened because its runbook-only PR closed it while the live page remained undeployed.
- Issue #318 closed as a verified no-delete result: all three WordPress objects are drafts, so the exact removal allow-list is empty and all 13 tracked images remain in place.
- Issue #749 closed after its exact approved pair-safe cleanup removed three local capture directories, reclaimed 927,688 KiB (~906 MiB), retained the `044445Z → 045150Z` comparison pair, and passed the 11-route visual preflight plus storage guard.
- Issue #706 closed after KK accepted the documented PSI caveat: TBT moved from 160 ms to 10 ms and the Facebook tasks disappeared; a fresh eight-route readback found zero pixel/eager-gtag markers and one delayed loader per route.
- Issue #740 closed with no file moves; its obsolete 26-file archive table is explicitly retired and must not be reused.
- Issue #481 closed as not planned after a fresh audit reconfirmed that the global class rename would require a coordinated live-content migration without product benefit.
- Issue #339's two stale guards were refreshed from authenticated raw content; all packet tests and the full repo verification pass, with live execution still approval-gated.
- Open issues moved ~77 → **35**; open PRs were **0** at the 2026-08-28 refresh.
- Competing work plans are historical; this snapshot plus `WORK-PLAN-2026-08-25.md` and a fresh `make status-readonly` run are the front door.

## Stash / secrets notes

- Cloud agents need process env `WP_USER` / `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Laptop Varlock does not inject into Cloud.
- Prefer [`.env.schema`](../../.env.schema); do not commit plaintext secrets. Rollout: [`VARLOCK-ROLLOUT-2026-07-16.md`](VARLOCK-ROLLOUT-2026-07-16.md).
- `git stash list` was empty on 2026-08-28. Issue #738 is closed: the stale `/private/tmp` registrations and approved merged branch refs are gone, and the registered worktree/local branch/remote-head inventories each contain only `main`.
