# Current State of kriskrug.co

Ops truth for [kriskrug.co](https://kriskrug.co/). Every May and June 2026 plan now lives under [`archive/`](archive/) (#549, see the close-out section at the bottom). Read the front door below, then run `make status-readonly` for current runtime signals.

## Current Front Door (verified 2026-08-28)

Read these first:

1. **[WORK-PLAN-2026-08-25.md](WORK-PLAN-2026-08-25.md)**, active runbook (issue #4 restored the two wrong-identity writes and applied corrected media 6014/6126 before stopping safely; correct media 7637 repo-side, then seek a new approval for remaining media 6985/7637/8871 before authority-hub applies; use `make status-readonly` for live counters)
2. **[CURRENT-STATE-2026-07-30.md](CURRENT-STATE-2026-07-30.md)**, declared snapshot for morning-truth drift checks (compare it with a fresh `make status-readonly` run)
3. **[MASTER-PLAN-2026-07-30.md](MASTER-PLAN-2026-07-30.md)**, truth then reclaim then product lanes (hygiene phases complete)
4. Run `make status-readonly` for current signals; use the newest **[reports/morning-truth-*.md](reports/)** only as durable checkpoint evidence
5. **[TWO-TRACK-MODEL.md](TWO-TRACK-MODEL.md)**, Track A vs Track B
6. **[INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md)**, slug/idempotency safety rules. Dated May, deliberately kept at top level: it is a standing safety rule, not a plan.
7. **[../../.env.schema](../../.env.schema)** plus **[VARLOCK-ROLLOUT-2026-07-16.md](VARLOCK-ROLLOUT-2026-07-16.md)**, env contract (never read plaintext `.env`)

**Live readback 2026-08-28 21:19Z:** WordPress `7.0.4`; Aurora live and repo `main` both `1.6.9`; 0 open PRs, 37 open issues, 0 scheduled posts, 66 draft posts, and 4 draft pages. Issue #602 is open after public page 2409 still showed the undeployed 19-card Testimonials body. #706 closed after KK accepted its documented delayed-gtag PSI caveat; TBT moved from 160 ms to 10 ms, Facebook tasks disappeared, and a fresh eight-route readback found zero pixel/eager-gtag markers with one delayed loader per route ([receipt](reports/issue-706-script-diet-apply-20260817.md)). #749 closed after its exact approved pair-safe cleanup reclaimed 927,688 KiB (~906 MiB) while retaining the newest complete comparison pair; the 11-route visual preflight and storage guard passed. #318 closed as a no-delete result because authenticated status proof found all three packages still in draft; all 13 tracked images remain ([receipt](reports/issue-318-publish-status-20260828.md)). Content applies #764 / #729 / #612 / **#826** / **#827** are live. The Speaking rebuild is live, and #640 closed after its same-method LCP receipt and live embed contract passed. Lab webring chrome (Dark Crystal + unofficial.city) is live on the homepage footer and `/work/` (surgical card insert, not a full `work.html` replace). Historical receipts: [`reports/gate0-content-apply-20260817.md`](reports/gate0-content-apply-20260817.md), [`reports/issue-826-applied-20260818.md`](reports/issue-826-applied-20260818.md), [`reports/issue-827-applied-20260818.md`](reports/issue-827-applied-20260818.md), [`reports/aurora-168-live-deploy-20260817.md`](reports/aurora-168-live-deploy-20260817.md), [`reports/aurora-169-live-deploy-20260818.md`](reports/aurora-169-live-deploy-20260818.md). Re-run `make status-readonly`; the public `style.css` readback remains authoritative for production theme state.

## Durable process docs (keep at top level)

| File | What it covers |
|---|---|
| [SEO-INDEXING-RUNBOOK.md](SEO-INDEXING-RUNBOOK.md) | Indexing/distribution checklist (#426) |
| [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md) | Schema/publisher rules (`make seo-publisher-smoke`) |
| [SEO-STRIKING-DISTANCE-2026-08-02.md](SEO-STRIKING-DISTANCE-2026-08-02.md) | #249 re-measure. **Read before running `make seo-audit`:** Jetpack is deactivated, the theme now owns SEO titles, and that target reports a false 1016/1016 missing |
| [AURORA-STYLESHEET-REBUILD-PLAN.md](AURORA-STYLESHEET-REBUILD-PLAN.md) | Path A rebuild plan of record (#423) |
| [AURORA-VISUAL-BASELINE-RUNBOOK.md](AURORA-VISUAL-BASELINE-RUNBOOK.md) | Pixel gate harness (#473) |
| [AURORA-RELEASE-CHECKLIST.md](AURORA-RELEASE-CHECKLIST.md) | Theme release checklist |
| [CSS-DEADCODE-OVERLAP-AUDIT.md](CSS-DEADCODE-OVERLAP-AUDIT.md) | Measured CSS debt feeding the rebuild |
| [RECLAIM-LIST-2026-07-24.md](RECLAIM-LIST-2026-07-24.md) | #318/#369 reclaim proposal |
| [reports/repo-bloat-318-next-steps-20260726.md](reports/repo-bloat-318-next-steps-20260726.md) | Executable A+D reclaim runbook |
| [ROLLBACK_PLAYBOOK.md](ROLLBACK_PLAYBOOK.md) | Prod undo order |
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

## Archive (#549 close-out, verified 2026-08-02)

At the #549 close-out, [`archive/`](archive/) held **89 markdown files**: 4 that were already there plus **84 moved in commit `c369eef`** (PR #557, merged 2026-07-31). It holds 102 as of 2026-08-28 after later plan archivals. Every #549 move was a `git mv` rename, so history is preserved and the moves are reversible. The diff for that commit against `docs/current-state/` is 84 `R`, 9 `M`, 6 `A`, and **zero `D`**. Verify with:

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

**Top-level surface:** 43 `docs/current-state/*.md` files as of 2026-08-28. The #549 close-out scan found 0 broken relative links across the then-current top-level surface plus `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and `docs/INDEX.md`; re-run the link check before making a new current claim.

**Still broken, and out of scope for #549.** A repo-wide scan of 921 tracked `.md` files (509 relative link targets) finds 114 unresolved: 37 inside `archive/` itself, 77 elsewhere. None of the 77 is archive-move rot. They break down as pseudo-scheme placeholders the publisher rewrites (`photo:7750`, `media:11920`, `poster:3`, `img:mcluhan`), root-relative live-site URLs that resolve on kriskrug.co and never on disk (`/contact`, `/speaking/`), regex fragments inside fenced code blocks that a naive link scanner misreads, and `images/` binaries referenced by `content/drafts/` posts that were never committed (they exist in some working copies as untracked files, so this count is worktree-sensitive). The 37 inside `archive/` are the real move damage: 33 lost one directory level and resolve by prefixing `../`, 4 point at `fixes/` artifacts that no longer exist. Both sets sit outside `docs/current-state/` top level, nothing on the front door reads them, and repairing them is its own issue.

## Reports and subdirectories

- `.generated/current-state/`, gitignored local `make morning-truth` output. Routine startup telemetry stays here and is not committed.
- `reports/`, durable checkpoint and ops evidence. `make morning-truth-checkpoint` writes here only for an explicit release, incident, durable decision, or handoff. Existing morning-truth Markdown remains tracked historical evidence; screenshot binaries are reclaim targets (#369 bucket D).
- `raw/`, unprocessed captures feeding the audits.
- `marketing/`, `portal/`, `templates/`, scoped working sets, not startup context.
- `archive/`, everything above.

## Side-worktree safety

Canonical new work starts from `main` on a lane-scoped branch. Run `git worktree list --porcelain` before editing or cleaning up; treat every listed side worktree as owned until its branch, PR, and filesystem state are verified.
