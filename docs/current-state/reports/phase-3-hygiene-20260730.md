# Phase 3 hygiene — 2026-07-30

Master plan Phase 3 (issue/branch hygiene). Cloud agent App token **cannot** edit issues (`Resource not accessible by integration`). Branch deletes succeeded via `git push --delete`.

## Done in this session

Deleted stale remotes:

- `codex/415-homepage-trust-identity`
- `codex/approved-community-photo-20260720`
- `codex/publications-editorial-archive`
- `cursor/494-pixel-gate-f196` (actual name; plan listed `cursor/494-pixel-gate`)

Remaining lane remotes after cleanup: `cursor/truth-reclaim-lanes-6351` (PR #557), `cursor/reclaim-ad-369-6351` (PR #558).

## KK paste-ready (needs write PAT / GH_TOKEN)

```bash
# Retitle Path A epic (decision already recorded in AURORA-STYLESHEET-REBUILD-PLAN)
gh issue edit 423 --title "[EPIC] Stylesheet hierarchy Path A rebuild (cascade → components) — Aurora 1.5.x+"

# Closed #474 should not stay blocked
gh issue edit 474 --remove-label blocked

# Dependents are not swarm-ready while blocked
for n in 476 477 478 479 480 481 424; do
  gh issue edit "$n" --remove-label swarm-ready
done

# Label reclaim execute issue
gh issue edit 369 --add-label tech-debt --add-label priority:medium

# Point #369 at the reclaim PR
gh issue comment 369 --body 'A+D reclaim PR: https://github.com/WalksWithASwagger/kriskrug-wp/pull/558 (MASTER-PLAN Phase 2).'
```

## Related PRs

- Docs truth + archive: https://github.com/WalksWithASwagger/kriskrug-wp/pull/557
- Reclaim A+D: https://github.com/WalksWithASwagger/kriskrug-wp/pull/558
