# AGENTS.md — Orientation for AI agents working in this repo

This file is the entry point for any AI agent (Claude Code, Cursor, Codex, etc.) landing in `kriskrug-wp`. Read this *first*. It's intentionally short.

## What this repo is

The operations + content hub for [kriskrug.co](https://kriskrug.co/) — a Pagely-hosted WordPress site running the Aurora theme (`kk-aurora`) as of 2026-05-24. The repo is **adjacent to** the live site, not a mirror of it. `main` now contains the canonical tracked theme line (merged via PR #129), plus content/ops tooling and docs. Custom repo-side WP code includes `inc/digital-composting.php` (merged, not yet deployed to prod) and `plugins/kk-sidebar-promos/` (packaged helper plugin, deploy only with an explicit rollback path and KK approval).

## Read this in order (top of repo, top of context)

1. [`docs/current-state/README.md`](docs/current-state/README.md) — index of the May-2026 baseline snapshot
2. [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) — the active operating model
3. [`docs/current-state/REPO_STATE.md`](docs/current-state/REPO_STATE.md) — what's actually built vs. just documented
4. [`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md) — postmortem with the safety rules every agent must follow
5. [`docs/current-state/HANDOFF-2026-05-24.md`](docs/current-state/HANDOFF-2026-05-24.md) — 2026-05-24 Aurora/theme/content handoff
6. [`docs/current-state/AURORA-V3-QA-ROADMAP-2026-05-24.md`](docs/current-state/AURORA-V3-QA-ROADMAP-2026-05-24.md) — reconciled Aurora v1.3.0 QA + rollout status
7. [`docs/current-state/SESSION-HANDOFF-2026-05-24.md`](docs/current-state/SESSION-HANDOFF-2026-05-24.md) — Track A/Track B ownership and latest lane handoff
8. [`docs/current-state/TRACK-A-MORNING-TRUTH-2026-05-24.md`](docs/current-state/TRACK-A-MORNING-TRUTH-2026-05-24.md) — latest normalized startup truth memo; verify against the newest committed `docs/current-state/reports/morning-truth-*.md`
9. [`docs/current-state/WORK-PLAN-2026-05-23.md`](docs/current-state/WORK-PLAN-2026-05-23.md) — historical roadmap context (stale counts/branch assumptions)

For the detailed diagnostic behind that plan, read [`docs/current-state/DIAGNOSTIC-POLISH-2026-05-20.md`](docs/current-state/DIAGNOSTIC-POLISH-2026-05-20.md).

After those five, the rest of the repo will make sense.

## Two lanes — pick one per commit

| | Track A — Content + SEO | Track B — Aurora theme |
|---|---|---|
| Branch | `main` (or feature branch from `main`) | `main` (or feature branch from `main`) |
| Touches | Posts, pages, media, taxonomies, Code Snippets (PHP/CSS), schema JSON-LD, redirects, alt text | `theme/kk-aurora/`, FSE templates, theme.json |
| Lives in | `content/drafts/`, `fixes/`, `scripts/notion-to-wp/`, `docs/current-state/` | `theme/kk-aurora/`, `docs/current-state/AURORA-*` |
| Owner | Publisher-mode session | Architect-mode session |

**Decision rule:** Editing a post / page / media / category / schema / redirect → Track A. Editing theme files / FSE templates / theme.json → Track B. If you're doing both in one session, you've scope-crept — finish one, commit, then start the other in a fresh session.

Legacy branch split context is in [`TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md). Treat branch-specific rules there as historical unless reconfirmed by a newer handoff.

## Hard safety rules (post 2026-05-15 incident)

1. **Rollback path before destructive operations.** The strict backup/restore proof gate was retired on 2026-05-22. Use dry-runs, slug/ID checks, page/post snapshots, reversible deploy steps, and KK approval for risky live changes. Use a full backup when the blast radius justifies it, but do not block ordinary publish/review work solely on restore-drill proof.
2. **Slug-based idempotency** for the Notion → WP connector. Never PATCH a WP post without first verifying that the slug match is the intended target. See [`INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md).
3. **Keep commits lane-scoped.** `main` is now canonical for both content and theme truth; do not mix unrelated Track A + Track B edits in one commit.
4. **Don't run the connector on production without `--dry-run` first.**

## What's historical or parked (don't get distracted)

- **`.github/agents/`** — the older GitHub Actions agent swarm (orchestrator → analyzer → test-writer → implementer → QA → reviewer → PR creator). It produced PRs #71 and #72 in May 2026 and is not used by current sessions.
- **`.github/workflows/agent-pr-generator.yml`** — parked on 2026-05-20. It is now a manual, read-only diagnostic stub and no longer auto-runs when `auto-implement` is labeled.
- **`.github/workflows/test-pr.yml`** — still active PR validation. Do not describe all workflows as dormant.
- **`docs/architecture.md`, `docs/automation-guide.md`** — reference docs for the dormant swarm.
- **`docs/cloudways-setup.md`, `docs/local-development-setup.md`, `.claude/context/wordpress-setup.md`** — Cloudways dev-server setup that was never used as planned. Relevant if/when Track B needs staging, otherwise ignore.
- **`docs/vision.md`, `docs/roadmap.md`** — early planning docs. Use the 2026-05-24 handoff set first (`HANDOFF`, `AURORA-V3-QA-ROADMAP`, `TRACK-A-MORNING-TRUTH`) plus the newest committed morning-truth report, and keep `WORK-PLAN-2026-05-23.md` as historical context.

Anything banner-tagged `STATUS: Historical` at the top is reference-only.

## How to publish a post (Track A)

See [`scripts/notion-to-wp/README.md`](scripts/notion-to-wp/README.md). Short version: dry-run first, slug-match second, publish third.

## How to file an issue

`issues-to-create/` holds markdown drafts. Filed issues live at [github.com/WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues).

## How to commit

- Commit messages: `<area>: <short imperative>` — e.g. `content: ...`, `docs: ...`, `feat: ...`, `fix: ...`.
- One concern per commit. Don't bundle content edits with doc edits with theme edits.
- Don't push to `main` without KK's go-ahead if the change touches prod-rendering code (schema, redirects, custom snippets).

## When in doubt

Read [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md). If that doesn't answer it, stop and ask the human.

## Morning truth command

Run `make morning-truth` at session start (or before execution) to emit a timestamped read-only report under `docs/current-state/reports/` with git/issue/worktree state, WP smoke, draft queue counts, and current-state drift flags.

If the task explicitly forbids file changes, run `make status-readonly` instead. It prints the same startup truth shape to stdout and does not write a report file.

---

**Last verified:** 2026-05-25 02:19 UTC via `make morning-truth`. If you're reading this much later than that and the rest of the repo has drifted, treat `docs/current-state/` plus the newest committed `docs/current-state/reports/morning-truth-*.md` as the source of truth and flag the drift for a fresh audit.
