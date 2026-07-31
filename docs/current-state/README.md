# Current State of kriskrug.co

Ops truth for [kriskrug.co](https://kriskrug.co/). Treat dated May–June plans as history (many now live under [`archive/`](archive/)). Prefer the front door below plus the newest `reports/morning-truth-*.md`.

## Current Front Door (verified 2026-07-30)

Read these first:

1. **[CURRENT-STATE-2026-07-30.md](CURRENT-STATE-2026-07-30.md)** — declared snapshot for `make morning-truth` / drift (Makefile default)
2. **[WORK-PLAN-2026-07-30.md](WORK-PLAN-2026-07-30.md)** — active day/week runbook
3. **[MASTER-PLAN-2026-07-30.md](MASTER-PLAN-2026-07-30.md)** — truth → reclaim → product lanes
4. Newest **[reports/morning-truth-*.md](reports/)** — or run `make status-readonly` / `make morning-truth`
5. **[TWO-TRACK-MODEL.md](TWO-TRACK-MODEL.md)** — Track A vs Track B
6. **[INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md)** — slug/idempotency safety rules
7. **[../../.env.schema](../../.env.schema)** + **[VARLOCK-ROLLOUT-2026-07-16.md](VARLOCK-ROLLOUT-2026-07-16.md)** — env contract (never read plaintext `.env`)

**Live readback 2026-07-30:** WordPress `7.0.2`, Aurora **`1.5.0`** (live == repo `main`).

## Durable process docs (keep at top level)

| File | What it covers |
|---|---|
| [SEO-INDEXING-RUNBOOK.md](SEO-INDEXING-RUNBOOK.md) | Indexing/distribution checklist (#426) |
| [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md) | Schema/publisher rules (`make seo-publisher-smoke`) |
| [AURORA-STYLESHEET-REBUILD-PLAN.md](AURORA-STYLESHEET-REBUILD-PLAN.md) | Path A rebuild plan of record (#423) |
| [AURORA-VISUAL-BASELINE-RUNBOOK.md](AURORA-VISUAL-BASELINE-RUNBOOK.md) | Pixel gate harness (#473) |
| [CSS-DEADCODE-OVERLAP-AUDIT.md](CSS-DEADCODE-OVERLAP-AUDIT.md) | Measured CSS debt feeding the rebuild |
| [RECLAIM-LIST-2026-07-24.md](RECLAIM-LIST-2026-07-24.md) | #318/#369 reclaim proposal |
| [reports/repo-bloat-318-next-steps-20260726.md](reports/repo-bloat-318-next-steps-20260726.md) | Executable A+D reclaim runbook |
| [AGENT-MERGE-PATH-2026-07-26.md](AGENT-MERGE-PATH-2026-07-26.md) | Cloud merge / review path |
| [ROLLBACK_PLAYBOOK.md](ROLLBACK_PLAYBOOK.md) | Prod undo order |
| [BACKUP_PLAN.md](BACKUP_PLAN.md) | Backup pieces + gaps |
| [ACCESS_CHANNELS.md](ACCESS_CHANNELS.md) | How we reach the site |
| [REPO-HYGIENE-AUDIT-2026-07-12.md](REPO-HYGIENE-AUDIT-2026-07-12.md) | Docs/branch/cruft audit |
| [CONTENT-ARCHITECTURE-RESET-2026-07-01.md](CONTENT-ARCHITECTURE-RESET-2026-07-01.md) | Trust/Offers/Topic Hubs wave |
| [SESSION-CLOSEOUT-2026-07-24.md](SESSION-CLOSEOUT-2026-07-24.md) | Recent Track A closeout |
| [REVIVE-AURORA-PORT-2026-07-24.md](REVIVE-AURORA-PORT-2026-07-24.md) / [REVIVE-AURORA-REVISIONS-2026-07-24.md](REVIVE-AURORA-REVISIONS-2026-07-24.md) | Revive cream port context |
| [AURORA-RELEASE-CHECKLIST.md](AURORA-RELEASE-CHECKLIST.md) | Theme release checklist |

## Historical / demoted (not the front door)

- Bannered July predecessors: [CURRENT-STATE-2026-07-16.md](CURRENT-STATE-2026-07-16.md), [WORK-PLAN-2026-07-16.md](WORK-PLAN-2026-07-16.md), [WORK-PLAN-2026-07-19.md](WORK-PLAN-2026-07-19.md), [WORK-PLAN-2026-07-25.md](WORK-PLAN-2026-07-25.md), [WORK-PLAN-2026-07-26.md](WORK-PLAN-2026-07-26.md), [WORK-PLAN-LONG-RUN-2026-07-16.md](WORK-PLAN-LONG-RUN-2026-07-16.md)
- May–June plans and one-shot closeouts: [`archive/`](archive/) (#549)
- May baseline archaeology (`FIX_QUEUE`, `ROADMAP`, `SITE_INVENTORY`, …): under `archive/` after #549

## Reports

`reports/` holds timestamped `make morning-truth` outputs and ops evidence. Prefer the newest `morning-truth-*.md`. Screenshot binaries are reclaim targets (#369 bucket D) — markdown stays.

## Side-worktree safety

Canonical new work starts from `main` on a lane-scoped branch. Do not edit legacy side worktrees (`aurora/v2`, `aurora/v3-reconcile`, aurora-keynote) unless a maintainer explicitly resumes one.
