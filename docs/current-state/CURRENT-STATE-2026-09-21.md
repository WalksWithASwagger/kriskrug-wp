# Current State Snapshot - 2026-09-21

**Snapshot time:** 2026-09-21 truth reset; live counters and versions refreshed 2026-09-21T16:24Z via `make status-readonly`: WordPress `7.0.5`; Aurora live and repo `main` both `1.6.12`.
**Branch:** `main` (docs PR lands from lane-scoped branch)
**Mode:** Ops hygiene (Phases 0–3) then Track A / Track B product lanes.

This file is the declared snapshot for `make current-state-drift-check` / `make morning-truth` / `make status-readonly` (via `WORK_PLAN` / `WORK_PLAN_DEFAULT`). It supersedes [`CURRENT-STATE-2026-07-30.md`](CURRENT-STATE-2026-07-30.md), which is now historical evidence.

Master sequence: [`MASTER-PLAN-2026-07-30.md`](MASTER-PLAN-2026-07-30.md). Latest dated runbook: [`WORK-PLAN-2026-09-09.md`](WORK-PLAN-2026-09-09.md) — no newer dated work plan exists as of this snapshot. The `1.6.12` Aurora figure and issue-count figures below are the 2026-09-21 snapshot values, not a durable claim; confirm with a fresh `make status-readonly` and `make check-live-parity`.

## Verified State

> **Counters refreshed 2026-09-21T16:24Z via `make status-readonly`.** These are the values `make current-state-drift-check` compares against. They can move as soon as a PR or issue changes, so re-read with the commands below before treating drift as a regression.

- `origin/main` was clean and synchronized before this snapshot branch; `git rev-list --left-right --count origin/main...main` reports `0  0`.
- Open PRs: `0` (`gh api repos/WalksWithASwagger/kriskrug-wp/pulls?state=open`, 2026-09-21T16:24Z). **Environment note:** in this session's sandbox, plain `gh pr list` / `gh issue list` (including their `--json` forms, which `make status-readonly` calls) hit `HTTP 403: GitHub GraphQL is not available from Claude Code sessions` from the agent proxy, so the drift checker's PR/issue rows below render as `unavailable`. The REST fallback (`gh api repos/{owner}/{repo}/pulls` / `.../issues`) still works and was used to fill this snapshot's PR/issue counts. A future session with GraphQL access should see the same numbers through `make status-readonly` directly.
- Open issues: `56` (`gh api repos/WalksWithASwagger/kriskrug-wp/issues?state=open&per_page=100`, filtered to non-PR issues, 2026-09-21T16:24Z) — up from `34` on 2026-08-29. See "What changed" below for the shape of the increase.
- Production still publicly reports WordPress `7.0.5` (drift from this file's prior declared `7.0.4`; `make status-readonly` now fails its version gate against the old expectation).
- Live Aurora theme (`style.css` Version header): `1.6.12` (public readback 2026-09-21, `make check-live-parity` reports live and repo in parity).
- Repo Aurora theme (`theme/kk-aurora/style.css` on `main`): `1.6.12`; live and repo are in parity.
- Theme deploy ledger: `theme/kk-aurora/CHANGELOG.md`. The public `style.css` readback is authoritative for what production runs, never the repo header.
- WordPress draft queue: **unavailable this session** (no WP credentials in this sandbox — `scripts/notion-to-wp/.env` absent and `WP_USER`/`WP_APP_PASSWORD` unset). Carrying forward the last authenticated read as dated evidence, not a current claim: `0` scheduled posts, `66` draft posts, `4` draft pages (authenticated read 2026-08-29). Re-verify with `make status-readonly` from a session with WP credentials before treating these as current.
- WP public smoke: all sampled routes (`/`, `/blog/`, `/speaking/`, `/work/`, `/contact/`, `/wp-json/`, `/sitemap.xml`, `/?s=ai`) return `200` and pass; the only failure is the version-gate check above (`expected WordPress 7.0.4, observed 7.0.5`), which is this file's own stale expectation, not a site defect.
- `/projects/` → `301` to `/work/` (unchanged).
- Homepage reveal safety net: absent. GSAP/ScrollTrigger CDN: absent. (unchanged)

## Highest-leverage open gates

| Gate | Issue | Status |
|---|---|---|
| Alt-text residual correction | #4 | Still open, unchanged since 2026-08-29: the broad authenticated media dry run is 78/78 `already-applied`, while separate body-image, archive, `/home/`, and WCAG lanes remain open |
| Authority-hub sequence | #402 | #829-#833 are live and closed; #834 (brand-navigation for the `krug ai` query) remains open and still needs a fresh authenticated preflight before any apply |
| Measured publisher batch | #339 | Still open; last updated 2026-09-06. All identities were current as of the July snapshot; exact approval for the remaining SEO/content payloads has not been recorded as executed |
| ~~Testimonials live deploy~~ | #602 | **Closed 2026-09-03.** KK approved the dry-run, `content_architecture_deploy.py --page testimonials --execute` updated live page 2409, and KK signed off on the logged-out visual review the same day. No longer an open gate. |
| Site redesign epic | #403 | Still open; Track B roadmap, still split into lane-scoped PRs |
| Crawl-waste / authority-hub cleanup | #1025 | **Closed 2026-09-20** (new since July). Recommendations landed in [`CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md`](CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md); repo-only, does not itself authorize a live apply |
| P1 engineering hardening batch | #1034-#1037 | New since July, still open. SFTP host-key verification (#1034), Events restore/rollback guardrails (#1035), stop auto-replay of ambiguous WP writes (#1036), fail JS syntax gate on any checked-file failure (#1037) |

## What changed since CURRENT-STATE-2026-07-30

- Aurora advanced **1.6.9 → 1.6.11 (2026-09-09 per `WORK-PLAN-2026-09-09.md`) → 1.6.12** on `main` and live; the live↔repo parity check remains the authority and still reports in-sync.
- Production WordPress moved **7.0.4 → 7.0.5**; this is a real drift against the version this file previously declared, not a session artifact.
- Open issues moved **34 → 56**. The increase is mostly new work, not reopenings: a September docs-hygiene audit ("Wave 1" through "Wave 6b", commits `2011e23`…`a333fe8`) that bannered stale plans and closed several hub/SEO packets; a new P1/P2 engineering-hardening batch (#1034-#1041, security/rollback/CI-gate items); a content backlog wave from the Plaud archive (#959-#968, #969 epic) and several showpiece rewrites (#950-#955); Open Studio product-transformation issues (#977, #983); and standalone additions such as #985 (favicon), #1015/#1016 (making-of posts), #1018 (Prompt Victoria talk), #1023 (ALL IN photo batch), #1024 (twitter:site tag fix), and #1027 (Article 3 review). Open PRs remain **0**.
- Testimonials issue **#602 closed 2026-09-03**: KK approved a dry run, the deploy script updated live page 2409, and KK signed off on the logged-out visual review the same day. This is the most significant status change from the July snapshot's open-gates table — that snapshot listed #602 as reopened and still blocking a legacy 19-card body; it is no longer blocking anything.
- Issue #1025 (crawl waste / authority hub) closed 2026-09-20, one day before this snapshot, with its recommendations captured in a standalone doc rather than a live apply.
- Authority-hub sequence #829-#833 remain closed as of the July snapshot; #834 is still the one open remainder and still needs a fresh authenticated preflight — unchanged from `WORK-PLAN-2026-09-09.md`.
- Issues #4, #339, #402, and #403 remain open with no verified status change since the July snapshot; carried forward as-is rather than guessed.
- 50 commits landed on `main` between the prior snapshot's reference commit (PR #936, `fa4a1ab`, 2026-08-29) and this one (`aeca1ad`), spanning the September docs-hygiene waves, the #274 sitemap follow-through receipt, several `#1025`-adjacent SEO commits, ALL IN content-drafting work, and dependency bumps.
- Competing work plans are still historical; this snapshot plus `WORK-PLAN-2026-09-09.md` (still the latest dated runbook — none newer exists) and a fresh `make status-readonly` run are the front door.

## Stash / secrets notes

- Cloud agents need process env `WP_USER` / `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Laptop Varlock does not inject into Cloud. This session had neither, so the authenticated draft-queue figures above are carried forward, not re-verified.
- Prefer [`.env.schema`](../../.env.schema); do not commit plaintext secrets. Rollout: [`VARLOCK-ROLLOUT-2026-07-16.md`](VARLOCK-ROLLOUT-2026-07-16.md).
- `gh` was not preinstalled in this session's sandbox and was installed via `apt-get install gh` to run `make status-readonly`; its GraphQL-backed subcommands (`gh pr list`, `gh issue list`, with or without `--json`) are blocked by this environment's agent proxy (`HTTP 403: GitHub GraphQL is not available from Claude Code sessions`). The REST fallback (`gh api repos/{owner}/{repo}/pulls` and `.../issues`) worked and supplied the PR/issue counts in this snapshot. A future session should still run `make status-readonly` first and only fall back to `gh api` REST calls if it sees the same GraphQL 403.
- Not re-verified this session: `git stash list` state and worktree/local-branch/remote-head inventories. The July snapshot reported `git stash list` empty on 2026-08-28 and issue #738 closed on that basis; carried forward as-is.
