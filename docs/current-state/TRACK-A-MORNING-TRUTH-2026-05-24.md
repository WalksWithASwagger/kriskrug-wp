# Track A Morning Truth - 2026-05-24

**Scope:** Track A startup truth (read-only) after PR #129 and same-day queue/theme follow-through.
**Last refreshed in this file:** 2026-05-25 02:19 UTC
**Authoritative artifact:** `docs/current-state/reports/morning-truth-20260525-021945Z.md`
**Production writes:** none

## Why this exists

This memo records a dated startup snapshot and a reliable command surface.
Counts can drift quickly; rerun `make morning-truth` before execution and treat the newest report file as canonical.

## Snapshot (from the 2026-05-25 02:19 UTC report)

- Open PRs: `0`
- Open issues: `66`
- WordPress version: `6.9.4`
- Draft queue (REST counts): `0` future posts, `71` draft posts, `5` draft pages
- Repo state at capture time: `codex/docs-reliability-normalization` with docs edits in progress after `git fetch --prune`.

## Live surface snapshot

- `/projects/` returns `301` to `/recent-projects-include/`.
- Cache-busted Work-page readback reports a non-blank `og:image`.
- Homepage source does **not** include the `Aurora reveal safety net` marker.
- GSAP + ScrollTrigger are still loaded from jsDelivr CDN.

## Startup command surface

```bash
make morning-truth
make current-state-drift-check
make draft-queue-audit
make wp7-smoke EXPECT_VERSION=6.9.4
git fetch --prune
git status --short --branch
gh pr list --state open --limit 100
gh issue list --state open --limit 200
```

## Surface verification commands

```bash
curl -sI https://kriskrug.co/projects/
curl -sL "https://kriskrug.co/recent-projects-include/?cachebust=<ts>" | rg -n "og:image"
curl -sL https://kriskrug.co/ | rg -n "Aurora reveal safety net|gsap.min.js|ScrollTrigger.min.js"
```

## Tooling baseline (this sweep)

- `make health`: pass.
- `make test`: pass.
- `make validate`: fails locally because `phpcs` is not installed.

## Drift notes vs historical docs

- `WORK-PLAN-2026-05-23.md` is historical, but its queue counts were normalized to the 2026-05-25 truth snapshot so `make current-state-drift-check` has a reliable declared baseline.
- Re-check issue/draft counts at session start; do not copy prior numbers forward without rerunning truth commands.

## Stop rules reaffirmed

- No production write without rollback notes and explicit approval for risky mutations.
- Keep Track A and Track B edits lane-scoped per commit.
- Do not use stale counts without re-running startup truth checks.
