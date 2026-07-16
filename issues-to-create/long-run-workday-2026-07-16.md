# Long-run workday issues — 2026-07-16

Parent context: `docs/current-state/WORK-PLAN-LONG-RUN-2026-07-16.md` and Monday epic #360.

These are **not** duplicates of #360–#366. They extend the day once live gates open, or capture ops cleanup that Monday deferred.

---

## Issue: [OPS] Keep/kill leftover remote branches after 2026-07-16 prune

### Labels
`tech-debt`, `needs-human-review`

### Body

## Context

Cloud agent deleted 25 MERGED/CLOSED remote branches on 2026-07-16 (report: `docs/current-state/reports/repo-hygiene-prune-triage-20260716.md`). Two heads remain without an open PR and need an explicit keep/kill:

- `marquee/weekly-proposals`
- `fix/jetpack-open-graph-enable`

Also delete `cursor/orchestra-monday-queue-2853` after PR #367 merges.

## Goal

Record KK decision and delete or document retention.

## Acceptance

- [ ] KK keep/kill for both branches
- [ ] Remote heads match the decision
- [ ] Note added to newest morning-truth or CURRENT-STATE

## Out of scope

Rewriting git history; deleting `main`.

---

## Issue: [OPS] Execute KK-approved #318 reclaim list (drafts images / report PNGs / old backups)

### Labels
`tech-debt`, `needs-human-review`, `priority:medium`

### Body

## Context

Read-only inventory in `docs/current-state/reports/repo-hygiene-prune-triage-20260716.md`:

- `content/drafts/` ≈ **247 MB** (PNG-heavy)
- `docs/current-state/reports/` ≈ **28 MB** (screenshots)
- `backup/` ≈ **18 MB**

#318 remains open. Do **not** delete without an exact approved path list.

## Goal

Produce a checked delete/move list, get KK approval, then execute in a dedicated PR (no history rewrite unless separately approved).

## Acceptance

- [ ] Ranked reclaim list committed
- [ ] KK approves exact paths
- [ ] PR removes only approved paths
- [ ] Morning-truth still works; no active deploy rollback broken

## Out of scope

`git filter-repo` / force-push without a separate KK thread.
