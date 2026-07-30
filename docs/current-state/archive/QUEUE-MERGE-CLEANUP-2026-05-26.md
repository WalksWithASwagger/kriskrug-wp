# Queue Merge Cleanup - 2026-05-26

## Summary

Balanced queue cleanup completed on 2026-05-26. The nearby mergeable work landed through GitHub PRs, old dirty Aurora branches were preserved as evidence, and branch/worktree cleanup avoided clobbering unrelated local files.

## Merged PRs

- PR #134, `feature/cotton-underwear-paradox-post` -> `main`: Cotton draft content. This had already merged before the cleanup pass resumed, and includes the intended local WIP: grounded JPG protest imagery, updated `post.md`/`post.html`, and `scripts/notion-to-wp/prepare_review_draft.py`.
- PR #135, `codex/aurora-live-qa-polish` -> `main`: Aurora content recovery and 1.3.4 live QA polish.
- PR #133, `codex/tech-debt-modernization-phase1` -> `main`: modernization guardrails, Composer/PHPCS validation, workflow cleanup, and the follow-up sanitization fix for the Aurora `/writing/` redirect.
- PR #136, `codex/aurora-v3-ia-rollout-salvage` -> `main`: salvaged the 2025+ single-post IA/media rollout report and support script from `aurora/v3-reconcile` without merging the deferred theme-polish commit.

## Branch And Worktree Cleanup

Deleted after merge:

- Remote/local PR branches: `feature/cotton-underwear-paradox-post`, `codex/aurora-live-qa-polish`, `codex/tech-debt-modernization-phase1`, `codex/aurora-v3-ia-rollout-salvage`.
- Local merged branches: `codex/aurora-content-recovery`, `content/you-cant-drink-data`.
- Clean temp/detached worktrees: `/private/tmp/kriskrug-wp-cotton-pr`, `/tmp/kriskrug-wp-modernization-pr`, `/tmp/kriskrug-wp-v3-salvage`, `/Users/kk/Code/kriskrug-wp-main-canonical-20260524`.

Preserved on purpose:

- `aurora/v2`: still highly diverged and has a locked Claude worktree with modified `theme/kk-aurora.zip`; do not merge wholesale.
- `aurora/v3-reconcile`: now acts as deferred evidence for the single-post Aurora theme polish only; the report/script commit was split out and merged via PR #136.
- `codex/aurora-keynote-redesign`: worktree still has untracked `demo/` and `theme/` content, so it was left alone.
- `backup/*`: historical safety branches remain preserved.

## Issue Queue Notes

Open PRs were reduced to zero before this documentation branch. Open issues remained at 66; no issues were closed because the touched tickets still have acceptance items that need specific follow-up proof.

Evidence comments were added to:

- #68 Work canonical/OG/proof metadata.
- #86 Aurora staging/performance/accessibility QA.
- #120 Both Hands Full proof-card overlap.
- #122 generic content pages.
- #126 Work OG image.
- #127 mobile/responsive QA.

Notable live evidence from the cleanup pass:

- `/recent-projects-include/` canonical is `https://kriskrug.co/recent-projects-include/`.
- `/recent-projects-include/` has H1 `Work` and a nonblank `og:image` using the BC+AI ecosystem image.
- `/work/` redirects to `/recent-projects-include/` with query strings preserved.
- PR #135 live QA documented one visible H1 per checked page, no horizontal overflow, no broken visible images, and no visible missing-alt images in the recorded scan.

## Verification

Ran during the cleanup pass:

- `git fetch --prune origin`
- `git diff --check`
- `make wp7-smoke EXPECT_VERSION=6.9.4`
- Notion publisher tests through the existing venv: `21` tests passed.
- `php plugins/kk-sidebar-promos/tests/smoke.php`
- PHP syntax lint for Aurora and sidebar promo PHP files.
- `make validate` after installing Composer locally into `/tmp` for the temp PR #133 worktree.
- `python3 -m py_compile scripts/wp_post_ia_rollout.py`
- `make docs-truth-check`
- `gitleaks dir --redact`
- GitHub checks for PRs #135, #133, and #136.

Local caveat: the system shell still lacks a global `composer`, and `make verify` with the system Python still fails without `python-dotenv`. The equivalent repo-owned checks passed using `/tmp/composer-kriskrug` plus the existing Notion publisher venv, and GitHub CI passed the Composer-backed validation before merge.
