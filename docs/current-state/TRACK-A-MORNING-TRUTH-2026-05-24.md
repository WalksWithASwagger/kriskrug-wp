# Track A Morning Truth - 2026-05-24

**Scope:** startup truth refresh after PR #129 merged Aurora into `main`.
**Snapshot window:** 2026-05-24 (America/Vancouver and UTC checks)
**Production writes:** none

## Why this exists

This memo captures the exact live and repo evidence needed to avoid startup drift.
It supersedes stale count/branch claims in older work-plan docs.

## Verified Startup Truth

- Canonical theme/content branch is `origin/main` at `5c5e11c`.
- Clean execution worktree: `/Users/kk/Code/kriskrug-wp-main-canonical-20260524` on `codex/main-canonical-truth-20260524`.
- Open PRs: `0`.
- Open issues: `67`.
- Draft queue (WordPress): `1` scheduled post, `43` draft posts, `5` draft pages.
- Public WordPress version (smoke): `6.9.4`.

Command evidence:

```bash
git -C /Users/kk/Code/kriskrug-wp-main-canonical-20260524 fetch --prune
git -C /Users/kk/Code/kriskrug-wp-main-canonical-20260524 status --short --branch
git -C /Users/kk/Code/kriskrug-wp-main-canonical-20260524 log --oneline -n 20
gh pr list --repo WalksWithASwagger/kriskrug-wp --state open --limit 50
gh issue list --repo WalksWithASwagger/kriskrug-wp --state open --limit 200 | wc -l
git -C /Users/kk/Code/kriskrug-wp-main-canonical-20260524 worktree list --porcelain
/Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --repo-root /Users/kk/Code/kriskrug-wp-main-canonical-20260524 --format markdown
make -C /Users/kk/Code/kriskrug-wp-main-canonical-20260524 wp7-smoke EXPECT_VERSION=6.9.4
/Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests
```

## Verified Live Surface Truth

- `/projects/` still returns `404`.
- `/recent-projects-include/` still emits `og:image=https://s0.wp.com/i/blank.jpg`.
- Homepage source still includes GSAP + ScrollTrigger from jsDelivr CDN.

Command evidence:

```bash
curl -sI https://kriskrug.co/projects/
curl -sL https://kriskrug.co/recent-projects-include/ | rg -n "canonical|og:image|twitter:image"
curl -sL https://kriskrug.co/ | rg -n "gsap.min.js|ScrollTrigger.min.js|data-reveal"
```

## Tooling Baseline

- `make health`: pass.
- `make validate`: fails because `phpcs` is not installed locally.

## Drift vs historical docs

The following are now historical/stale and must not be used as startup truth without refresh:

- `WORK-PLAN-2026-05-23.md` counts and branch assumptions.
- Any instruction that says "no theme files on `main`".
- Any claim that `aurora/v2` is the canonical production source line.

## Stop Rules Reaffirmed

- No production write without rollback notes and explicit approval for risky mutations.
- Keep Track A and Track B edits lane-scoped per commit.
- Do not use stale counts without re-running startup truth checks.
