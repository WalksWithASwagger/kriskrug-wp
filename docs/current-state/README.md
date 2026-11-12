# Current State of kriskrug.co

Start with the [November 11 roadmap](ROADMAP-2026-11-11.md), then run
`make doctor` and `make status-readonly`. The [maintenance report](reports/repo-maintenance-2026-11-11.md)
records the issue reconciliation, source drift fix, verification and initial
branch recovery. The [same-day follow-through](reports/morning-followthrough-2026-11-11.md)
adds the remaining branch cleanup and the HSTS, Events and BC + AI decisions.
The October 25 snapshot remains the declared drift baseline;
its old counts and theme version are dated evidence.

## Current front door — 2026-11-11

1. [ROADMAP-2026-11-11.md](ROADMAP-2026-11-11.md): remaining work, owners and completion gates.
2. [CURRENT-STATE-2026-10-25.md](CURRENT-STATE-2026-10-25.md): Makefile drift baseline, to compare with a fresh readback.
3. [WORK-PLAN-2026-09-09.md](WORK-PLAN-2026-09-09.md): retained identity, snapshot and approval procedures. Its September queue is historical; #834 is complete.
4. [TWO-TRACK-MODEL.md](TWO-TRACK-MODEL.md): content versus theme boundaries.
5. [INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md): standing slug/idempotency rules, with later approval policy in AGENTS.md.
6. [AGENT-RUNTIME-REFERENCE.md](AGENT-RUNTIME-REFERENCE.md), [environment schema](../../.env.schema) and [Varlock rollout](VARLOCK-ROLLOUT-2026-07-16.md): runtime, auth and validation.

November 11 startup observed WordPress 7.0.8 and public Aurora 1.7.1 matching
`origin/main`. About, Photography, MØTLEYKRÜG and Contact source matches the
approved live bodies. Publications' approved redesign is reconciled separately
from its later private polish preview. Current priorities are the remaining
Canada Now knowledge work, the missing Events cadence and the HSTS decision.
Futureproof's approved BC + AI reciprocal link is now live. Do not repeat
completed page redesigns, #331's archive policy, or the dependency security patches.

## Earlier release evidence

These receipts explain shipped changes; their counts and automation status are
not current promises. Re-run the owning check before relying on them.

| Evidence | What it records |
|---|---|
| [October 25 readiness](reports/site-readiness-20261025.md) | The earlier site readiness checkpoint |
| [Schema #1089](reports/schema-1089-release-2026-10-25.md) | Person/Speaking schema saved and validated |
| [Sitemap reconciliation](reports/sitemap-1130-reconciliation-2026-10-25.md) | Post/page-only sitemap and archive policy; #331 has since closed |
| [November/ALL IN Events release](reports/events-november-allin-release-2026-10-25.md) | Approved event additions and media preservation |
| [Events catalog](reports/events-catalog-1099-2026-10-25.md), [record/counters](reports/events-record-1100-2026-10-25.md), [documentation](reports/events-documentation-1101-2026-10-25.md) | Completed system work; follow #1102 for maintenance |
| [Work/Subscribe](reports/work-subscribe-release-2026-10-25.md), [Publications layout](reports/publications-layout-release-2026-10-25.md) | Earlier page repairs, before the November redesigns |
| [KRÜG measurement](reports/krug-conversion-1090-2026-10-25.md) | Installed measurement; organic signup delivery still needs current evidence |
| [Brand navigation](reports/brand-navigation-834-release-2026-10-25.md) | Completed #834 links; no new apply remains |
| [First-practice preparation](reports/practice-release-preparation-1105-2026-10-25.md) | Prepared #983 packet, not participant evidence or publication approval |
| [September audit closeout](REPO-HEALTH-REMEDIATION-2026-09-21.md) | Completed repo remediation and remaining external checks |

The [November 4 plan](WORK-PLAN-2026-11-04.md), [September weekly plan](WEEK-PLAN-2026-09-28.md)
and [July master plan](MASTER-PLAN-2026-07-30.md) are historical planning context.
May–June plans live under [archive/](archive/).

## Durable process docs (keep at top level)

Approved product transformation: [Connected portfolio of practice](CONNECTED-PORTFOLIO-PLAN.md).
This records the north star, non-goals, roadmap and North House proof milestone.
It authorizes a reviewable proof PR, not a live deployment.

| File | What it covers |
|---|---|
| [SEO-INDEXING-RUNBOOK.md](SEO-INDEXING-RUNBOOK.md) | Indexing/distribution checklist (#426). Public #274 refresh: `make sitemap-followthrough` and [reports/issue-274-sitemap-followthrough-20260921.md](reports/issue-274-sitemap-followthrough-20260921.md) |
| [templates/owned-distribution-backlink-checklist.md](templates/owned-distribution-backlink-checklist.md) | Per-article owned-distribution + backlink launch record (#1026). Copy into the draft package; does not authorize live posts |
| [CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md](CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md) | #1025 robots/sitemap/noindex recommendations. In-repo only; does not authorize live apply |
| [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md) | Schema/publisher rules (`make seo-publisher-smoke`) |
| [SEO-STRIKING-DISTANCE-2026-08-02.md](SEO-STRIKING-DISTANCE-2026-08-02.md) | #249 re-measure. **Read before running `make seo-audit`:** Jetpack is deactivated, the theme now owns SEO titles, and that target reports a false 1016/1016 missing |
| [AURORA-STYLESHEET-REBUILD-PLAN.md](AURORA-STYLESHEET-REBUILD-PLAN.md) | Path A rebuild plan of record (#423) |
| [AURORA-VISUAL-BASELINE-RUNBOOK.md](AURORA-VISUAL-BASELINE-RUNBOOK.md) | Pixel gate harness (#473) |
| [AURORA-RELEASE-CHECKLIST.md](AURORA-RELEASE-CHECKLIST.md) | Theme release checklist |
| [CSS-DEADCODE-OVERLAP-AUDIT.md](CSS-DEADCODE-OVERLAP-AUDIT.md) | Measured CSS debt feeding the rebuild |
| [RECLAIM-LIST-2026-07-24.md](RECLAIM-LIST-2026-07-24.md) | #318/#369 reclaim proposal |
| [reports/repo-bloat-318-next-steps-20260726.md](reports/repo-bloat-318-next-steps-20260726.md) | Executable A+D reclaim runbook |
| [ROLLBACK_PLAYBOOK.md](ROLLBACK_PLAYBOOK.md) | Prod undo order |
| [SECURITY-HEADERS-PHASE-1-APPLY-RUNBOOK.md](SECURITY-HEADERS-PHASE-1-APPLY-RUNBOOK.md) | #1001 phase-1 nosniff + Referrer-Policy apply (Pagely ARES). Docs only; does not authorize live apply. Parent #709 stays open |
| [XML-RPC-CONSTRAIN-DECISION-2026-09-08.md](XML-RPC-CONSTRAIN-DECISION-2026-09-08.md) | #1002 XML-RPC constrain packet. Prep only; host/WAF deny preferred. Do not apply live. Related #767 / #709 |
| [BACKUP_PLAN.md](BACKUP_PLAN.md) | Backup pieces and gaps |
| [ACCESS_CHANNELS.md](ACCESS_CHANNELS.md) | How we reach the site |
| [REPO-HYGIENE-AUDIT-2026-07-12.md](REPO-HYGIENE-AUDIT-2026-07-12.md) | Docs/branch/cruft audit |
| [CONTENT-ARCHITECTURE-RESET-2026-07-01.md](CONTENT-ARCHITECTURE-RESET-2026-07-01.md) | Trust/Offers/Topic Hubs wave |

## One-shot closeouts and handoffs (reference, not the front door)

These are finished or single-issue documents that still sit at top level because a newer doc or an open issue cites them. None of them is a plan you should execute from. Most are July 2026; `AURORA-TEMPLATE-CONTENT-HANDOFF.md` is the outlier at 2026-05-23, and `AURORA-MOBILE-QA-127.md` carries no date at all.

| File | What it was |
|---|---|
| [SESSION-CLOSEOUT-2026-07-24.md](SESSION-CLOSEOUT-2026-07-24.md) | Track A closeout |
| [AGENT-MERGE-PATH-2026-07-26.md](AGENT-MERGE-PATH-2026-07-26.md) | Historical record of the deleted `agent-safe-merge` workflow; current policy lives in `AGENTS.md` and `CONTRIBUTING.md` |
| [REVIVE-AURORA-PORT-2026-07-24.md](REVIVE-AURORA-PORT-2026-07-24.md) / [REVIVE-AURORA-REVISIONS-2026-07-24.md](REVIVE-AURORA-REVISIONS-2026-07-24.md) | Revive cream port context |
| [INTERACTION-STATES-GAP-INVENTORY.md](INTERACTION-STATES-GAP-INVENTORY.md) | First acceptance criterion of #424, dated 2026-07-25 |
| [AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md](AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md) | #357 search-title handoff |
| [WP-AUTH-CLIENT-INVENTORY-2026-07-08.md](WP-AUTH-CLIENT-INVENTORY-2026-07-08.md) | #306 auth client inventory |
| [AURORA-HOMEPAGE-BC-AI-FUTUREPROOF-2026-07-03.md](AURORA-HOMEPAGE-BC-AI-FUTUREPROOF-2026-07-03.md) | Homepage BC+AI / Futureproof closeout |
| [AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md](AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md) | Readability reset, shipped |
| [PERFORMANCE-RECOVERY-2026-07-01.md](PERFORMANCE-RECOVERY-2026-07-01.md) | Performance closeout |
| [AURORA-MOBILE-QA-127.md](AURORA-MOBILE-QA-127.md) | #127 mobile QA test plan, **superseded** by [`reports/issue-127-mobile-qa-2026-08-16.md`](reports/issue-127-mobile-qa-2026-08-16.md) |
| [AURORA-TEMPLATE-CONTENT-HANDOFF.md](AURORA-TEMPLATE-CONTENT-HANDOFF.md) | FSE template copy handoff, dated 2026-05-23 in the body |

## Historical, banner-tagged, not the front door

Every file below carries a `STATUS: Historical` banner in its first lines pointing at the 2026-07-30 trio:

- [CURRENT-STATE-2026-07-16.md](archive/CURRENT-STATE-2026-07-16.md)
- [WORK-PLAN-2026-07-01.md](archive/WORK-PLAN-2026-07-01.md)
- [WORK-PLAN-2026-07-16.md](archive/WORK-PLAN-2026-07-16.md)
- [WORK-PLAN-LONG-RUN-2026-07-16.md](archive/WORK-PLAN-LONG-RUN-2026-07-16.md)
- [WORK-PLAN-2026-07-19.md](archive/WORK-PLAN-2026-07-19.md)
- [WORK-PLAN-2026-07-25.md](archive/WORK-PLAN-2026-07-25.md)
- [WORK-PLAN-2026-07-26.md](archive/WORK-PLAN-2026-07-26.md)
- [WORK-PLAN-2026-08-09.md](archive/WORK-PLAN-2026-08-09.md)
- [WORK-PLAN-2026-08-15.md](archive/WORK-PLAN-2026-08-15.md)
- [WORK-PLAN-2026-08-16.md](archive/WORK-PLAN-2026-08-16.md)
- [WORK-PLAN-2026-08-17.md](archive/WORK-PLAN-2026-08-17.md)
- [AGENTIC-CRUSH-PLAN-2026-07-31.md](archive/AGENTIC-CRUSH-PLAN-2026-07-31.md)
- [WORK-PLAN-2026-08-23.md](archive/WORK-PLAN-2026-08-23.md)
- [WORK-PLAN-2026-08-24.md](archive/WORK-PLAN-2026-08-24.md)
- [WORK-PLAN-2026-08-25.md](archive/WORK-PLAN-2026-08-25.md)

## Archive (#549 close-out, verified 2026-08-02)

At the #549 close-out, [`archive/`](archive/) held **89 markdown files**: 4 that were already there plus **84 moved in commit `c369eef`** (PR #557, merged 2026-07-31). It holds 105 as of 2026-09-03 after later plan archivals. Every #549 move was a `git mv` rename, so history is preserved and the moves are reversible. The diff for that commit against `docs/current-state/` is 84 `R`, 9 `M`, 6 `A`, and **zero `D`**. Verify with:

```
git diff --name-status --find-renames c369eef^1 c369eef -- docs/current-state | cut -c1-1 | sort | uniq -c
```

No May or June 2026 **plan** is left at top level. Two top-level files still carry May 2026 dates and both stay here on purpose:

- `INCIDENT-2026-05-15-overwritten-post.md`, date in the filename. A standing safety rule, read-order item 6 in `AGENTS.md`.
- `AURORA-TEMPLATE-CONTENT-HANDOFF.md`, undated filename, `**Date:** 2026-05-23` on line 3 of the body. An unfinished FSE template copy handoff, listed in the one-shot table above.

Neither is a plan you execute from. Check with `ls docs/current-state/*.md | grep -E "2026-0[56]"` for filenames and `grep -l "2026-0[56]-" docs/current-state/*.md` for body dates.

**Inbound link debt from the move: fixed 2026-08-02 (#566).** Five markdown links in three files outside `docs/current-state/` still pointed at pre-`c369eef` top-level paths. All five now point into `archive/` and resolve on disk:

- `issues-to-create/jetpack-seo-audit-all-posts.md` lines 5, 57, 102, to `archive/SEO_AUDIT.md` (twice) and `archive/CONTENT_AUDIT.md`
- `issues-to-create/README.md` line 5, to `archive/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md`
- `backup/2026-05-16/manifest.md` line 47, to `archive/FIX_QUEUE.md`

**Top-level surface:** 40 `docs/current-state/*.md` files as of 2026-09-03. The #549 close-out scan found 0 broken relative links across the then-current top-level surface plus `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and `docs/INDEX.md`; re-run the link check before making a new current claim.

**Repo-wide relative-link sweep completed 2026-09-03.** A scan of all 1,110 tracked Markdown files now finds zero unresolved relative link targets. The sweep repaired 69 paths across archived plans, issue drafts, superseded content drafts, and one active source-pack runbook. The scanner ignores fenced code, external URLs, root-relative live-site routes, fragments, and publisher pseudo-schemes (`photo:`, `media:`, `poster:`, `img:`), because those are not repository file targets.

## Reports and subdirectories

- `.generated/current-state/`, gitignored local `make morning-truth` output. Routine startup telemetry stays here and is not committed.
- `reports/`, durable checkpoint and ops evidence. `make morning-truth-checkpoint` writes here only for an explicit release, incident, durable decision, or handoff. Existing morning-truth Markdown remains tracked historical evidence; screenshot binaries are reclaim targets (#369 bucket D).
- `raw/`, unprocessed captures feeding the audits.
- `marketing/`, `portal/`, `templates/`, scoped working sets, not startup context. `templates/owned-distribution-backlink-checklist.md` is the #1026 per-article launch record; copy it into a draft package rather than treating the blank as a completed post.
- `archive/`, everything above.

## Side-worktree safety

Canonical new work starts from `main` on a lane-scoped branch. Run `git worktree list --porcelain` before editing or cleaning up; treat every listed side worktree as owned until its branch, PR, and filesystem state are verified.
