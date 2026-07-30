# Aurora Issue #86 Staging QA Gate - 2026-05-21

**Issue:** [#86](https://github.com/WalksWithASwagger/kriskrug-wp/issues/86)
**Track:** Track B / Aurora v2 assessment
**Current branch inspected:** `main` with read-only checks against `origin/aurora/v2`
**Decision:** #86 is not ready to close. Aurora has useful local QA evidence, but the required staging and activation-safety evidence is still missing.

## Scope And Assumptions

- This artifact is a gate checklist only.
- No theme files were edited.
- No live WordPress, staging WordPress, or Local WordPress writes were made in this lane.
- The locked Aurora worktree at `.claude/worktrees/agent-aec50fddbd7207f80` was not touched.
- Existing dirty Track A/source-pack/fixes work in the shared checkout was treated as other-worker work and left alone.

## Evidence Found

| Evidence | Source | Status |
|---|---|---|
| #86 is still open and labeled `track-b`, `aurora-v2`, `accessibility`, `performance`, `mobile`, `swarm-ready`, and `swarm-wave-3`. | `gh issue view 86` | Confirmed |
| Issue acceptance requires Local or staging with Aurora active and production-like content, screenshots, keyboard, reduced-motion, contrast, media strategy, console errors, and backup/rollback gate. | `gh issue view 86 --json body` | Confirmed |
| `origin/aurora/v2` contains local QA artifacts from PR #106. | `git ls-tree -r --name-only origin/aurora/v2` | Confirmed |
| PR #106 added `docs/current-state/aurora-qa-2026-05-20/` screenshots and `aurora-qa-checks.json`. | `git show --stat origin/aurora/v2` | Confirmed |
| Local QA covered Home, About, Work, Speaking, Make Culture, and Calling Us All In on desktop and mobile. | `origin/aurora/v2:docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md` | Local-only pass |
| Local QA found and fixed mobile horizontal overflow on About. | `origin/aurora/v2:docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md` | Fixed on Aurora branch |
| Keyboard focus, reduced-motion behavior, and major contrast pairs were checked locally. | `origin/aurora/v2:docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md` | Local-only pass |
| Local QA still had missing media: About 13 incomplete images, Work 1, Make Culture 1, Calling Us All In 7. | `origin/aurora/v2:docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md` and `aurora-qa-checks.json` | Blocks staging sign-off |
| Earlier Aurora staging report found desktop header/nav render problems on Local WordPress. | `docs/current-state/AURORA-STAGING-REPORT-2026-05-18.md` | Must be revalidated after later fixes |
| The current work plan says #86 is done only when staging uses production-like media and QA notes are recorded. | `docs/current-state/WORK-PLAN-2026-05-23.md` | Not yet satisfied |
| Backup archive set exists for 2026-05-16, but uploads are missing and restore proof is absent. | `make backup-check BACKUP_DIR=backup/2026-05-16` | Resilience gap; not a blanket launch blocker after 2026-05-22 gate retirement |
| Rollback playbook exists, but no Aurora-specific activation rollback drill/proof was found. | `docs/current-state/ROLLBACK_PLAYBOOK.md` | Needs activation-specific proof |

## Current Gate Checklist

### 1. Staging Surface

- [ ] Staging URL is recorded.
- [ ] Staging admin access is available to the reviewer/operator.
- [ ] Aurora is active only on staging, not production.
- [ ] Staging content/database is production-like enough to exercise real pages, posts, menus, plugin output, and media.
- [ ] Staging uploads/media are present or missing media is explicitly resolved before screenshots are accepted.
- [ ] Environment notes document host, WP version, PHP version if available, active theme, active plugins, and any staging-only differences.

### 2. Backup And Restore Proof

- [ ] Fresh backup exists before staging activation or any production-adjacent operation.
- [ ] Backup accounts for database, themes, plugins, mu-plugins, other `wp-content`, and uploads.
- [ ] Activation rollback plan is documented.
- [ ] Existing active theme/options state is captured before cutover.
- [ ] Restored copy verifies homepage, one recent post, wp-admin, and plugin settings.

Current state: `backup/2026-05-16` can be inspected, but uploads are absent and restore proof is missing. The strict backup gate is retired; Aurora still needs an activation-specific rollback plan before production cutover.

### 3. Screenshot Matrix

Required captures on real staging with production-like media:

- [ ] Home desktop.
- [ ] Home mobile.
- [ ] About desktop.
- [ ] About mobile.
- [ ] Work desktop.
- [ ] Work mobile.
- [ ] Speaking desktop.
- [ ] Speaking mobile.
- [ ] At least two posts desktop and mobile, including one long-form/media-heavy post.
- [ ] Screenshot artifact paths are listed in the final issue comment.

Local PR #106 screenshots are useful baseline evidence, but they do not satisfy this staging gate.

### 4. Accessibility And Interaction

- [ ] Keyboard traversal covers skip link, header, desktop nav, mobile nav, cards, CTAs, forms, newsletter/search utilities, and footer.
- [ ] Focus is visible and not hidden by animation timing.
- [ ] Reduced-motion pass confirms no essential content depends on motion.
- [ ] Reading progress, reveals, view transitions, and loading animation behavior are checked with `prefers-reduced-motion: reduce`.
- [ ] Contrast spot checks cover body text, muted text, links, buttons, cards, forms/errors, nav, and footer.
- [ ] Mobile overflow/text clipping check passes at a narrow viewport.

### 5. Console, Media, And Performance

- [ ] Browser console errors are captured.
- [ ] Network/media errors are captured.
- [ ] Any errors are resolved or documented with an owner and reason.
- [ ] Hero/poster dimensions, lazy loading behavior, and embed/media strategy are documented.
- [ ] Basic Core Web Vitals notes are recorded for LCP, INP, and CLS on representative desktop and mobile.
- [ ] Any heavy motion/media decision is accepted or cut under `AURORA-MOTION-GOVERNANCE-2026-05-20.md`.

### 6. Activation Rollback Plan

- [ ] Current production active theme and version are recorded immediately before any activation.
- [ ] Catch Responsive remains installed and known-good.
- [ ] Aurora activation steps are written as a timed checklist.
- [ ] Rollback steps are written as a timed checklist: reactivate Catch Responsive, clear cache, verify homepage, verify a recent post, verify admin, verify one form or CTA path.
- [ ] Rollback owner and stop conditions are named.
- [ ] Low-traffic cutover window is chosen only after staging QA passes and KK signs off.
- [ ] 24-hour post-cutover monitoring checklist exists.

## Closure Criteria For #86

#86 can close only when all of these are true:

1. Real staging URL/admin access is available and documented.
2. Aurora staging QA is rerun after the latest `origin/aurora/v2` changes are deployed to staging.
3. Production-like uploads/media are present or missing assets are intentionally replaced.
4. Desktop/mobile screenshot matrix is attached or linked.
5. Keyboard, focus, reduced-motion, contrast, overflow, console, media, and perf notes are recorded.
6. Activation rollback plan and post-cutover verification are ready.
7. Activation rollback plan is documented and accepted.
8. Any remaining launch blockers are filed separately with clear owners.

## Gate Decision

Do not close #86 now.

The repo proves Aurora is healthier after the local Wave 3 work and PR #106, but the current evidence is still local-only and has known media gaps. There is no verified staging URL/admin evidence in this lane, no production-like media pass, and no activation-specific rollback drill. Aurora activation, staging promotion, or production cutover should remain blocked until those items are complete.

## Verification Run For This Artifact

```bash
git fetch --prune
git status --short --branch
git worktree list --porcelain
git rev-list --left-right --count origin/aurora/v2...origin/main
gh issue view 86 --repo WalksWithASwagger/kriskrug-wp --json number,title,state,labels,body,url
gh issue view 86 --repo WalksWithASwagger/kriskrug-wp --comments
git ls-tree -r --name-only origin/aurora/v2 | rg 'aurora-qa|AURORA|theme/kk-aurora|screens|smoke|qa'
git show origin/aurora/v2:docs/current-state/AURORA-SWARM-86-QA-2026-05-20.md
git show origin/aurora/v2:docs/current-state/aurora-qa-2026-05-20/aurora-qa-checks.json
make backup-check BACKUP_DIR=backup/2026-05-16
git diff --check
git diff --no-index --check /dev/null docs/current-state/AURORA-ISSUE-86-STAGING-QA-GATE-2026-05-21.md
```
