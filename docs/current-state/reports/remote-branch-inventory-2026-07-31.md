# Remote branch inventory — 2026-07-31

Issue: [#568](https://github.com/WalksWithASwagger/kriskrug-wp/issues/568)  
Inventory only — **no branches deleted**.  
Base: `origin/main` @ `c69012d` (fetched 2026-07-31T22:40Z).  
Method: `git fetch origin --prune`, `git rev-list --count main..origin/<branch>`, `gh pr list --state all --head <branch>`.

## Summary

| Metric | Count |
|---|---|
| Non-`main` origin branches | **7** |
| `origin/codex/*` | **0** (none present) |
| `origin/cursor/*` | **0** (none present) |
| `origin/feature/*` | **2** |
| `origin/dependabot/*` | **4** |
| Other non-`main` remotes | **1** (`chore/…`) |
| **Delete candidates** | **2** |
| **Keep** | **5** |

Issue #568 named leftover `codex/*` / `cursor/*` lanes (`codex/415-homepage-trust-identity`, `codex/approved-community-photo-20260720`, `codex/publications-editorial-archive`, `cursor/494-pixel-gate-f196`, and peers). After `git fetch --prune`, **none of those refs remain on `origin`** — already gone before this inventory.

Spot-check on delete candidates: `git log origin/main..origin/<branch>` is empty for both merged feature branches (fully superseded).

## Delete candidates

Safe remote deletes after KK gate (separate step; not done here):

| Branch | PR | Unique vs `main` | Rationale |
|---|---|---|---|
| `feature/2940-ai-lands-essay` | [#564](https://github.com/WalksWithASwagger/kriskrug-wp/pull/564) MERGED | 0 | PR merged; tip is ancestor of `main`; no unique commits |
| `feature/2942-biv-publications-payload` | [#563](https://github.com/WalksWithASwagger/kriskrug-wp/pull/563) MERGED | 0 | PR merged; tip is ancestor of `main`; no unique commits |

## Keep list

Anything with open work or unmerged unique commits:

| Branch | PR | Unique vs `main` | Rationale |
|---|---|---|---|
| `chore/wp-api-credential-aliases` | [#574](https://github.com/WalksWithASwagger/kriskrug-wp/pull/574) OPEN | 1 | Active open PR with unique commit; keep until merge/close |
| `dependabot/composer/wp-coding-standards/wpcs-3.4.1` | [#556](https://github.com/WalksWithASwagger/kriskrug-wp/pull/556) OPEN | 1 | Open Dependabot PR; keep for review/merge |
| `dependabot/github_actions/actions/setup-node-7.0.0` | [#562](https://github.com/WalksWithASwagger/kriskrug-wp/pull/562) OPEN | 1 | Open Dependabot PR; keep for review/merge |
| `dependabot/github_actions/actions/upload-artifact-7.0.1` | [#561](https://github.com/WalksWithASwagger/kriskrug-wp/pull/561) OPEN | 1 | Open Dependabot PR; keep for review/merge |
| `dependabot/github_actions/peter-evans/create-pull-request-8.1.1` | [#560](https://github.com/WalksWithASwagger/kriskrug-wp/pull/560) OPEN | 1 | Open Dependabot PR; keep for review/merge |

## Full table

| Branch | PR | State | Unique commits (`main..branch`) | Behind `main` | Fully merged into `main`? | Verdict | One-line rationale |
|---|---|---|---|---|---|---|---|
| `chore/wp-api-credential-aliases` | [#574](https://github.com/WalksWithASwagger/kriskrug-wp/pull/574) | OPEN | 1 | 3 | no | **keep** | Open PR with unique work |
| `dependabot/composer/wp-coding-standards/wpcs-3.4.1` | [#556](https://github.com/WalksWithASwagger/kriskrug-wp/pull/556) | OPEN | 1 | 9 | no | **keep** | Open Dependabot bump |
| `dependabot/github_actions/actions/setup-node-7.0.0` | [#562](https://github.com/WalksWithASwagger/kriskrug-wp/pull/562) | OPEN | 1 | 9 | no | **keep** | Open Dependabot bump |
| `dependabot/github_actions/actions/upload-artifact-7.0.1` | [#561](https://github.com/WalksWithASwagger/kriskrug-wp/pull/561) | OPEN | 1 | 9 | no | **keep** | Open Dependabot bump |
| `dependabot/github_actions/peter-evans/create-pull-request-8.1.1` | [#560](https://github.com/WalksWithASwagger/kriskrug-wp/pull/560) | OPEN | 1 | 9 | no | **keep** | Open Dependabot bump |
| `feature/2940-ai-lands-essay` | [#564](https://github.com/WalksWithASwagger/kriskrug-wp/pull/564) | MERGED | 0 | 8 | yes | **delete-candidate** | Merged; empty `main..branch` |
| `feature/2942-biv-publications-payload` | [#563](https://github.com/WalksWithASwagger/kriskrug-wp/pull/563) | MERGED | 0 | 6 | yes | **delete-candidate** | Merged; empty `main..branch` |

### Already absent (named in #568; not on `origin` after prune)

| Named branch | Status on `origin` |
|---|---|
| `codex/415-homepage-trust-identity` | gone |
| `codex/approved-community-photo-20260720` | gone |
| `codex/publications-editorial-archive` | gone |
| `cursor/494-pixel-gate-f196` | gone |

### Out of scope note

Local-only branches / worktrees (e.g. `ops/565-morning-truth-20260731`, this inventory lane) were not counted as `origin` inventory. No remote deletes were performed.
