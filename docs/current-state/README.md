# Current State of kriskrug.co

Ops truth for [kriskrug.co](https://kriskrug.co/). Every May and June 2026 plan now lives under [`archive/`](archive/) (#549, see the close-out section at the bottom). Read the front door below, then the newest `reports/morning-truth-*.md`.

## Current Front Door (verified 2026-08-02)

Read these first:

1. **[CURRENT-STATE-2026-07-30.md](CURRENT-STATE-2026-07-30.md)**, declared snapshot for `make morning-truth` / drift (the Makefile default `WORK_PLAN`)
2. **[WORK-PLAN-2026-07-30.md](WORK-PLAN-2026-07-30.md)**, active day/week runbook
3. **[MASTER-PLAN-2026-07-30.md](MASTER-PLAN-2026-07-30.md)**, truth then reclaim then product lanes
4. **[AGENTIC-CRUSH-PLAN-2026-07-31.md](AGENTIC-CRUSH-PLAN-2026-07-31.md)**, audit-backed execution waves. Wave 0 landed: PR [#557](https://github.com/WalksWithASwagger/kriskrug-wp/pull/557) merged 2026-07-31, PR [#558](https://github.com/WalksWithASwagger/kriskrug-wp/pull/558) merged.
5. Newest **[reports/morning-truth-*.md](reports/)**, or run `make status-readonly` / `make morning-truth`
6. **[TWO-TRACK-MODEL.md](TWO-TRACK-MODEL.md)**, Track A vs Track B
7. **[INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md)**, slug/idempotency safety rules. Dated May, deliberately kept at top level: it is a standing safety rule, not a plan.
8. **[../../.env.schema](../../.env.schema)** plus **[VARLOCK-ROLLOUT-2026-07-16.md](VARLOCK-ROLLOUT-2026-07-16.md)**, env contract (never read plaintext `.env`)

**Live readback 2026-08-02:** WordPress `7.0.2`. Aurora live **`1.5.7`**, repo `main` **`1.5.8`**. The repo is one patch ahead: `1.5.8` is the `aurora-tstm` testimonials CSS, built but not deployed, gated on the #601 pixel gate. Verified with `curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i version` against `theme/kk-aurora/style.css`, and `make current-state-drift-check` for the WP version. Do not treat the repo `style.css` version as proof of production. Read back the public file, in either direction.

## Durable process docs (keep at top level)

| File | What it covers |
|---|---|
| [SEO-INDEXING-RUNBOOK.md](SEO-INDEXING-RUNBOOK.md) | Indexing/distribution checklist (#426) |
| [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md) | Schema/publisher rules (`make seo-publisher-smoke`) |
| [AURORA-STYLESHEET-REBUILD-PLAN.md](AURORA-STYLESHEET-REBUILD-PLAN.md) | Path A rebuild plan of record (#423) |
| [AURORA-VISUAL-BASELINE-RUNBOOK.md](AURORA-VISUAL-BASELINE-RUNBOOK.md) | Pixel gate harness (#473) |
| [AURORA-RELEASE-CHECKLIST.md](AURORA-RELEASE-CHECKLIST.md) | Theme release checklist |
| [CSS-DEADCODE-OVERLAP-AUDIT.md](CSS-DEADCODE-OVERLAP-AUDIT.md) | Measured CSS debt feeding the rebuild |
| [RECLAIM-LIST-2026-07-24.md](RECLAIM-LIST-2026-07-24.md) | #318/#369 reclaim proposal |
| [reports/repo-bloat-318-next-steps-20260726.md](reports/repo-bloat-318-next-steps-20260726.md) | Executable A+D reclaim runbook |
| [AGENT-MERGE-PATH-2026-07-26.md](AGENT-MERGE-PATH-2026-07-26.md) | Cloud merge / review path |
| [ROLLBACK_PLAYBOOK.md](ROLLBACK_PLAYBOOK.md) | Prod undo order |
| [BACKUP_PLAN.md](BACKUP_PLAN.md) | Backup pieces and gaps |
| [ACCESS_CHANNELS.md](ACCESS_CHANNELS.md) | How we reach the site |
| [REPO-HYGIENE-AUDIT-2026-07-12.md](REPO-HYGIENE-AUDIT-2026-07-12.md) | Docs/branch/cruft audit |
| [CONTENT-ARCHITECTURE-RESET-2026-07-01.md](CONTENT-ARCHITECTURE-RESET-2026-07-01.md) | Trust/Offers/Topic Hubs wave |

## One-shot July closeouts and handoffs (reference, not the front door)

These are finished or single-issue documents that still sit at top level because a newer doc or an open issue cites them. None of them is a plan you should execute from.

| File | What it was |
|---|---|
| [SESSION-CLOSEOUT-2026-07-24.md](SESSION-CLOSEOUT-2026-07-24.md) | Track A closeout |
| [REVIVE-AURORA-PORT-2026-07-24.md](REVIVE-AURORA-PORT-2026-07-24.md) / [REVIVE-AURORA-REVISIONS-2026-07-24.md](REVIVE-AURORA-REVISIONS-2026-07-24.md) | Revive cream port context |
| [INTERACTION-STATES-GAP-INVENTORY.md](INTERACTION-STATES-GAP-INVENTORY.md) | First acceptance criterion of #424, dated 2026-07-25 |
| [AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md](AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md) | #357 search-title handoff |
| [WP-AUTH-CLIENT-INVENTORY-2026-07-08.md](WP-AUTH-CLIENT-INVENTORY-2026-07-08.md) | #306 auth client inventory |
| [AURORA-HOMEPAGE-BC-AI-FUTUREPROOF-2026-07-03.md](AURORA-HOMEPAGE-BC-AI-FUTUREPROOF-2026-07-03.md) | Homepage BC+AI / Futureproof closeout |
| [AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md](AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md) | Readability reset, shipped |
| [PERFORMANCE-RECOVERY-2026-07-01.md](PERFORMANCE-RECOVERY-2026-07-01.md) | Performance closeout |
| [AURORA-MOBILE-QA-127.md](AURORA-MOBILE-QA-127.md) | #127 mobile QA test plan, device pass still pending |
| [AURORA-TEMPLATE-CONTENT-HANDOFF.md](AURORA-TEMPLATE-CONTENT-HANDOFF.md) | FSE template copy handoff, dated 2026-05-23 in the body |

## Historical, banner-tagged, not the front door

Every file below carries a `STATUS: Historical` banner in its first lines pointing at the 2026-07-30 trio:

- [CURRENT-STATE-2026-07-16.md](CURRENT-STATE-2026-07-16.md)
- [WORK-PLAN-2026-07-01.md](WORK-PLAN-2026-07-01.md)
- [WORK-PLAN-2026-07-16.md](WORK-PLAN-2026-07-16.md)
- [WORK-PLAN-LONG-RUN-2026-07-16.md](WORK-PLAN-LONG-RUN-2026-07-16.md)
- [WORK-PLAN-2026-07-19.md](WORK-PLAN-2026-07-19.md)
- [WORK-PLAN-2026-07-25.md](WORK-PLAN-2026-07-25.md)
- [WORK-PLAN-2026-07-26.md](WORK-PLAN-2026-07-26.md)

## Archive (#549 close-out, verified 2026-08-02)

[`archive/`](archive/) holds **89 markdown files**: 4 that were already there plus **84 moved in commit `c369eef`** (PR #557, merged 2026-07-31). Every one was a `git mv` rename, so history is preserved and the moves are reversible. The diff for that commit against `docs/current-state/` is 84 `R`, 9 `M`, 6 `A`, and **zero `D`**. Verify with:

```
git diff --name-status --find-renames c369eef^1 c369eef -- docs/current-state | cut -c1-1 | sort | uniq -c
```

No May or June 2026 plan is left at top level. The one dated-May file that stays here on purpose is `INCIDENT-2026-05-15-overwritten-post.md`, a standing safety rule.

**Known link debt left by the move (open, not fixed here).** A repo-wide scan of 921 tracked markdown files found 497 relative link targets, 96 of them aimed at a file `c369eef` moved. 91 resolve. Four targets in three files outside `docs/current-state/` still point at the old top-level paths:

- `issues-to-create/jetpack-seo-audit-all-posts.md` to `../docs/current-state/SEO_AUDIT.md` (twice) and `../docs/current-state/CONTENT_AUDIT.md`
- `issues-to-create/README.md` to `../docs/current-state/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md`
- `backup/2026-05-16/manifest.md` to `../../docs/current-state/FIX_QUEUE.md`

All four now live under `archive/`, so the fix is inserting `archive/` into the path. Separately, 37 of the 101 relative links **inside** archived files are broken: 33 lost one directory level and resolve by prefixing `../`, and 4 point at `fixes/` artifacts that no longer exist. Those are all inside historical documents and nothing current reads them.

## Reports and subdirectories

- `reports/`, timestamped `make morning-truth` output and ops evidence. Prefer the newest `morning-truth-*.md`. Markdown stays tracked; screenshot binaries are reclaim targets (#369 bucket D).
- `raw/`, unprocessed captures feeding the audits.
- `marketing/`, `portal/`, `templates/`, scoped working sets, not startup context.
- `archive/`, everything above.

## Side-worktree safety

Canonical new work starts from `main` on a lane-scoped branch. Do not edit legacy side worktrees (`aurora/v2`, `aurora/v3-reconcile`, aurora-keynote) unless a maintainer explicitly resumes one.
