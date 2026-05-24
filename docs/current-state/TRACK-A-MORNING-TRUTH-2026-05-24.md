# Track A Morning Truth - 2026-05-24

**Scope:** Track A on `main`, read-only verification and repo-side stabilization only.
**Snapshot window:** 2026-05-24 (America/Vancouver and UTC checks)
**Production writes:** none

## Why this exists

This memo captures the exact live and repo evidence needed to avoid startup drift. It supersedes older "current count" claims where they conflict with live command output.

## Verified Startup Truth

- `main` vs `origin/main`: `0 0` (in sync).
- Open PRs: `0`.
- Open issues: `67`.
- Draft queue (WordPress): `1` scheduled post, `43` draft posts, `5` draft pages.
- Public WordPress version (smoke): `6.9.4`.

Command evidence:

```bash
git rev-list --left-right --count origin/main...main
gh pr list --state open --limit 50 | wc -l
gh issue list --state open --limit 200 | wc -l
make draft-queue-audit
make wp7-smoke EXPECT_VERSION=6.9.4
```

## Verified Live Surface Truth

- `/projects/` still returns `404`.
- `/recent-projects-include/` still emits `og:image=https://s0.wp.com/i/blank.jpg`.
- Homepage visibility still depends on an inline "Aurora reveal safety net" override.
- GSAP and ScrollTrigger are loaded from jsDelivr CDN.

Command evidence:

```bash
curl -sI https://kriskrug.co/projects/
curl -sL https://kriskrug.co/recent-projects-include/ | rg -n "og:image"
curl -sL https://kriskrug.co/ | rg -n "Aurora reveal safety net|gsap.min.js|ScrollTrigger.min.js"
```

## Aurora Divergence Risk (Read-Only)

- `origin/aurora/v2...origin/main`: `18 112`.
- Local locked `aurora/v2` worktree vs `origin/aurora/v2`: `50 38`.
- Locked worktree has a dirty artifact (`theme/kk-aurora.zip`).

Command evidence:

```bash
git rev-list --left-right --count origin/aurora/v2...origin/main
git -C .claude/worktrees/agent-aec50fddbd7207f80 rev-list --left-right --count origin/aurora/v2...aurora/v2
git -C .claude/worktrees/agent-aec50fddbd7207f80 status --short --branch
```

## Drift vs `WORK-PLAN-2026-05-23.md`

The following fields have drifted and must be treated as historical snapshot values:

- Open issues (`61` declared vs `67` observed).
- Scheduled posts (`0` declared vs `1` observed).
- Cross-track reality (Aurora is now live; 2026-05-24 handoffs are authoritative).

Run this before execution to detect drift automatically:

```bash
make current-state-drift-check
```

## Startup Command Surface (Track A)

- `make morning-truth` writes a timestamped read-only report to `docs/current-state/reports/`.
- `make current-state-drift-check` compares declared snapshot values vs live checks.

## Stop Rules Reaffirmed

- No production WordPress writes in this stabilization slice.
- No theme changes on `main`.
- No Aurora branch reconciliation/deploy in the locked worktree during Track A startup truth work.
