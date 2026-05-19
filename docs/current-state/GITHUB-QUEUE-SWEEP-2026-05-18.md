# GitHub Queue Sweep - 2026-05-18

Snapshot time: 2026-05-18 22:10 PDT  
Repo: `WalksWithASwagger/kriskrug-wp`  
Mode: read-first queue sweep with bounded subagent review

## Current State

- `main` is the Track A branch for content, SEO, media, taxonomies, snippets, schema, redirects, and connector work.
- `aurora/v2` is the Track B branch for Aurora theme work.
- The shared `main` checkout had unrelated dirty content-source and backup files during this sweep. They were not edited or reverted.
- Open PRs at sweep time: `#77`, `#73`, and the now-merged `#74`.
- Open issues: 64.
- `auto-implement` issues: 62.
- `needs-human-review` issues: `#75`, `#23`.

## PR Classification

| PR | Status | Decision | Reason |
|---|---:|---|---|
| `#77` `[codex] Redesign Aurora visual system` | Draft, mergeable, base `aurora/v2` | Keep open as Track B draft | Active Aurora visual redesign. Do not merge to `main` until review, final media direction, mobile polish, and staging smoke are complete. |
| `#78` `[codex] Revert static preview pages from main` | Open, base `main` | Merge after checks/review | Corrects the accidental merge of PR `#74` preview pages into Track A. Deletes only `preview/batch-1-as-planned.html` and `preview/editorial-alt.html`. |
| `#73` `Auto-managed sidebar promos` | Open, conflicting, base `main` | Park | Production-adjacent plugin work. Needs conflict resolution, capability hardening, staging activation test, backup confirmation, and explicit deployment approval before merge. |
| `#74` `Add editorial and batch-1 design preview pages` | Merged during sweep, then reverted by `#78` | Treat as harvested/closed input | Current docs say static preview pages should inform Aurora, not land on `main`. |

## Branch Classification

| Branch | Decision | Notes |
|---|---|---|
| `main` | Keep | Default Track A branch. |
| `aurora/v2` | Keep | Active Track B base branch. |
| `codex/aurora-redesign-2026-05-18` | Keep | Head of PR `#77`; active Aurora draft. |
| `codex/revert-pr74-track-drift` | Keep until PR `#78` merges | Reverts PR `#74` preview pages from `main`. |
| `claude/automate-sidebar-graphics-55OBU` | Keep parked | Head of PR `#73`; blocked plugin lane. |
| `claude/kriskrug-redesign-planning-fgdhB` | Delete after PR `#78` merges and no unique artifacts remain | Head of PR `#74`; preview ideas should live in Aurora docs/issues, not `main`. |
| `claude/setup-wordpress-rebuild-KVLxh` | Archival deletion candidate | Old Aurora rebuild work; docs warn it would regress Track A if merged. Confirm no unique artifacts remain before deleting. |

## Best Agentic Candidates

### Track A, Low-Risk Prep

These can be swarmed as repo-local drafts, reports, or snippet-prep without live writes:

- `#36` Add Unique Meta Descriptions: prepare exact meta descriptions and update docs/fixes; publisher applies live changes later.
- `#43` Add Twitter Card Tags: prepare/review snippet or docs; deployment remains backup-gated.
- `#38` Internal Linking Strategy: generate a link map and recommendation report from current inventory.
- `#48` Accessibility Statement: draft page copy for human/legal review.
- `#44` Glossary Page: draft local content artifact for editorial review.

### Track B, Aurora Consolidation

The stale January design issues should not be implemented on `main`; fold them into Aurora:

- `#24` Full Homepage Redesign.
- `#28` Navigation Redesign.
- `#33` Mobile-First Responsive System.
- `#34` Hero Section Visual Treatment.
- `#26` Typography System Update.
- `#27` Color Palette Refinement.
- `#29` Footer Redesign.
- `#31` Project Card Design Pattern.

Use PR `#77` and `docs/current-state/AURORA-TOMORROW-ROADMAP-2026-05-19.md` as the active implementation surface.

### Human-Gated Or Broad

Do not auto-merge or auto-implement without further scoping:

- `#75` Notion-to-WordPress publishing lockdown: P0 and `needs-human-review`; connector runs and policy choices are gated.
- `#23` Blog category reorg: taxonomy/bulk live-post decisions are human-gated.
- `#73` Sidebar promos plugin: production-adjacent plugin lane; requires staging and approval.
- `#49`-`#58`: marketing systems need business positioning choices.
- `#59`-`#64`: archive/portal lanes are product-scale and need data/integration scoping.
- `#4`, `#40`, `#42`, `#46`, `#47`: valid goals, but require live verification/media/theme inventory before implementation.

## Recommended Next Swarm

1. Merge PR `#78` once checks are green, restoring `main` to Track A shape.
2. Keep PR `#77` draft and run an Aurora Track B review/polish swarm against `aurora/v2`.
3. Start a Track A prep swarm for `#36`, `#38`, `#43`, `#44`, and `#48`, limited to docs, fixes, and drafts only.
4. Park PR `#73` until plugin deployment is explicitly approved, then resolve conflicts in an isolated worktree and add capability/staging checks before review.
