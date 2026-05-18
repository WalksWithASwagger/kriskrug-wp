# Full Audit And Roadmap - 2026-05-18

**Mode:** Read-only audit plus documentation closeout.
**No production writes:** No WordPress writes, connector live runs, theme activation, issue mutation, or PR merge was performed for this audit.
**Source of truth:** Current `main`, GitHub issue/PR state, current-state docs, local draft packs, and the known Track A / Track B operating model.

## Executive Read

The project is now in a much better place than it looked at the start of the day.

The old problem was fog: public posts, Notion rows, local draft packs, GitHub issues, dormant workflows, and redesign ideas were all competing to be "truth." The current problem is coordination: the truth is now mostly documented, but the backlog still has stale automation labels, the publishing connector needs two more safety gates, and Aurora needs one focused Track B sprint before anyone should think about cutover.

My current recommendation:

1. Finish the publishing-trust gate around issue `#75`.
2. Start Track B on `aurora/v2` with the Aurora P0 header/nav rescue.
3. In parallel, prep the next Track A post as a WordPress draft only, starting with `Sovereign AI for Whom?`
4. Run issue hygiene before broad agent swarms so agents do not execute stale January issues against May production reality.

## Current Repo And Remote State

Verified on 2026-05-18:

| Surface | Status |
|---|---|
| Local branch | `main` |
| Remote sync | `main...origin/main` is `0 0` after fetch |
| `main` head at audit start | `6b2e036 docs: audit aurora redesign roadmap` |
| Working tree before this doc | Clean |
| Open PRs | 2 |
| Open issues | 64 |
| Open issues with `auto-implement` | 62 |
| Open issues with `needs-human-review` | 2 |
| Local/remote Aurora branch | `aurora/v2` at `159ac2a docs: aurora v2 next-session playbook` |

Existing local worktrees:

| Worktree | Branch | Notes |
|---|---|---|
| `/Users/kk/Code/kriskrug-wp` | `main` | Track A/docs command surface |
| `/Users/kk/Code/kriskrug-wp-aurora-redesign` | `codex/aurora-redesign-2026-05-18` | Based on `origin/aurora/v2` |
| `/Users/kk/Code/kriskrug-wp-aurora-staging-qa` | `codex/aurora-staging-qa-2026-05-18` | Based on `origin/aurora/v2` |
| `.claude/worktrees/agent-aec50fddbd7207f80` | `aurora/v2` | Locked Claude worktree |

## What Is Actually Done

### Safety and credential remediation

Done:

- The exposed WordPress application password was revoked.
- The older `MCP AI` application password was revoked.
- A replacement connector password exists only in gitignored `scripts/notion-to-wp/.env`.
- Current tracked docs no longer contain the pasted password.
- The connector docs now warn against pasting credentials into docs, issues, commits, or chat.

Still open:

- Git history still contains the old leaked value unless KK explicitly approves a coordinated history rewrite and force-push.
- Issue `#75` is still open because the acceptance criteria include category routing and pre-publish review/diff gates.

### Track A page overhaul

Issue `#76` is closed.

Done:

- Speaking, Work, and About were verified against authenticated REST readback.
- `/work/` and `/work/?utm_source=codex-test` redirect to `/recent-projects-include/`.
- Rollback snapshots, checksum manifest, and desktop/mobile screenshot evidence are committed.
- Verification artifact: `content/source-packs/keynotes-2026/verification/DEPLOY-VERIFICATION-2026-05-18.md`.

Implication:

- The refreshed Work/Speaking/About pages can become the real-content test set for Aurora.

### Track A publishing pipeline

The publishing work is paused in the right place: local prep and dry-run packs exist, but the next connector live run should not happen until issue `#75` is closed or deliberately narrowed.

Current draft-pack state:

| Pack | Current read | Next action |
|---|---|---|
| `2026-05-13-sovereign-ai-for-whom` | Best next candidate; 3,648 words, 6 images; high fact-check risk | Prep locally, fact-check, category decision, create WP draft only |
| `2026-05-16-why-we-built-the-responsible-ai-professional-certification` | Useful but may overlap live RAP post `11620`; 1,418 words, 13 images | Compare against live RAP post before deciding replacement vs follow-up |
| `2026-05-06-comox-valley-ai-is-becoming-its-own-thing` | Strong community value; 3,188 words, no images; still has editorial TODOs | Editorial cleanup, image decision, internal links |
| `2026-05-07-web-summit-vancouver-2026` | Already published as WP `11826` | No publish action |
| `2026-05-14-calling-us-all-in` | Already published as WP `11765` | No publish action |
| `wp-draft-10594-post-10594` | Historical capture for live WP `10594` | Treat as historical |
| `wp-draft-11178-post-11178` | Historical capture for live WP `11178` | Treat as historical |

### Track B Aurora redesign

Aurora is real, but not cutover-ready.

Done:

- `origin/aurora/v2` contains `theme/kk-aurora/`, `theme/kk-aurora.zip`, `demo/index.html`, templates, CSS, JS, and docs.
- Local WordPress with Aurora active returned 200s for homepage, About, and recent posts.
- The current design audit is committed at `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`.
- Local epic drafts exist at `issues-to-create/aurora-v2-redesign-epics.md`.

Blocked:

- Local rendered desktop header/nav is not clean.
- Aurora does not yet have a media-led homepage or final visual system.
- No production activation should happen until mechanical and brand gates pass.

## GitHub Queue Audit

### Issues

Current open issue count: 64.

The core queue problem is label drift:

| Label | Open count | Audit read |
|---|---:|---|
| `auto-implement` | 62 | Unsafe as-is; many issues touch live WordPress, strategic choices, or stale January assumptions |
| `enhancement` | 60 | Too broad to prioritize |
| `priority:high` | 29 | Inflated by old issue batches |
| `needs-human-review` | 2 | Underused; many issues should require human review before agents run |

Important issue states:

| Issue | State | Recommendation |
|---:|---|---|
| `#75` | Open P0 | Finish connector trust gate before live publishing |
| `#76` | Closed | Done; evidence committed |
| `#24-#35` | Open stale design issues | Reframe under Aurora epics; remove `auto-implement` until acceptance criteria are current |
| `#65-#68` | Open content/page issues | Mostly superseded or partly satisfied by the Work/Speaking/About overhaul; review before closing or reframing |
| `#49-#58` | Open marketing system issues | Need human strategy decisions before agents execute |
| `#59-#64` | Open archive/platform issues | Big product lanes; not suitable for casual `auto-implement` |

### Pull requests

| PR | State | Checks | Audit read |
|---:|---|---|---|
| `#73` | Open | `gh pr checks` reports no checks on branch | Interesting sidebar-promo plugin, but production/plugin lane; needs code review and WP staging before merge |
| `#74` | Open | Checks pass | Static design preview only; useful input for Track B, but should not be mistaken for Aurora implementation |
| `#71`, `#72` | Merged | N/A | Older transcript/digital-composting work; not currently deployed to production |

### Dormant automation

There are 11 `.github/agent-state/*/state.json` files that still say `in_progress`, but AGENTS.md correctly marks the GitHub Actions agent swarm as dormant. Treat those as historical artifacts unless we deliberately revive or replace that system.

## Roadmap From Here

### P0 - Trust, backup, and queue hygiene

Goal: make future agent work safe.

1. Finish issue `#75`.
2. Add connector category routing or explicit category override for `Type=Feature`.
3. Add a pre-publish diff/review gate for `--update`, or document the manual equivalent.
4. Decide whether to rewrite public git history to remove the revoked leaked password.
5. Confirm the backup path before any new production writes: page snapshots are useful, but a full backup/restore drill is still the real insurance.
6. Remove misleading `auto-implement` labels from stale/live-WP-gated issues.

### P1 - Aurora P0 sprint on `aurora/v2`

Goal: turn Aurora from prototype into a design surface we can judge.

1. Fix desktop header/nav render in `theme/kk-aurora/parts/header.html` and supporting CSS.
2. Re-run the six-page Local smoke from `AURORA-STAGING-REPORT-2026-05-18.md`.
3. Capture desktop/mobile screenshots.
4. Create a media inventory for hero, project, speaking, portrait, and long-form article assets.
5. Build a media-led homepage concept using real KK/project media.
6. Keep all this off `main` until Track B review passes.

### P2 - Next post batch as safe drafts

Goal: restart publishing without repeating the incident.

1. Prep `Sovereign AI for Whom?` locally.
2. Fact-check high-stakes claims and fix category/alt/opening formatting.
3. Create a WordPress draft only after dry-run and target checks.
4. Compare the RAP follow-up against live WP `11620` before deciding whether it is a new post.
5. Clean Comox Valley third, after images/internal links are decided.

### P3 - Track A current-site fixes after backup

Goal: improve the current Catch Responsive site while Aurora matures.

1. Apply the Track A quick-fix pack only after backup approval.
2. Deploy `llms.txt` and chosen `robots.txt` AI-crawler stance.
3. Fix title separator and social-handle drift.
4. Run the broken-link scan as a one-shot, export results, then disable the scanner.
5. Continue category cleanup so recent posts stop disappearing into `Misc`.

### P4 - PR and issue cleanup

Goal: reduce backlog noise before swarming.

1. Review PR `#74`; merge only if we want static preview pages on `main`.
2. Review PR `#73` in a staging/plugin lane, not as a casual docs merge.
3. File or approve the Aurora epics from `issues-to-create/aurora-v2-redesign-epics.md`.
4. Comment on stale design issues `#24-#35` with the new Aurora audit and remove `auto-implement` until they are reframed.
5. Close or re-scope page/content issues already satisfied by the Work/Speaking/About overhaul.

## Human Decisions Needed

These are the questions where KK should steer before agents run too far:

1. **Git history:** Do you want to force-rewrite public git history to remove the already-revoked application password, or is revocation plus current-tree cleanup enough?
2. **Backup gate:** Can we treat page-level snapshots as enough for small Track A fixes, or do you want a full Updraft/Pagely backup and restore drill before any more production writes?
3. **Aurora hero media:** Which asset should lead the redesign: keynote stage, portrait, community room, photography/action shot, or project montage?
4. **Primary CTA:** Should Aurora optimize first for "Book a keynote", "Work with Kris", "Explore my work", or something campaign-specific?
5. **Brand edge:** Should Aurora lean more premium/editorial/human, or keep more cyberpunk/AI weirdness?
6. **Photography role:** Is photography a supporting credibility band, a full section, or a major pillar in v1?
7. **Next post:** Should `Sovereign AI for Whom?` be the next WP draft, or should the lower-risk RAP/Comox lane go first?
8. **Issue strategy:** Should I mutate existing issues `#24-#35`, or file clean Aurora epics and leave old issues as references until each is replaced?
9. **PR #74:** Do you want static preview pages merged into `main`, or should they stay as PR-only design references?
10. **PR #73:** Do you want to pursue the sidebar-promo plugin now, or park it until Aurora/current-site priorities settle?

## Recommended Swarm Shape

Run bounded swarms, not one giant backlog blast.

| Worker | Track | Scope | Output |
|---|---|---|---|
| Connector safety | A | `scripts/notion-to-wp/`, issue `#75` | Category routing, diff/review gate, tests, docs |
| Draft prep | A | `content/drafts/2026-05-13-sovereign-ai-for-whom/` | Clean local draft pack, fact-check checklist, no WP write |
| Aurora P0 | B | `aurora/v2` only | Header/nav fix, six-page smoke, screenshots |
| Issue hygiene | GitHub | Issues and labels only | Stale labels removed, current epics filed/commented |
| PR triage | GitHub | PRs `#73` and `#74` | Merge/close/park recommendation with evidence |

My bias: run Aurora P0 and Draft Prep in parallel, but keep production publishing serialized behind the safety gate.
