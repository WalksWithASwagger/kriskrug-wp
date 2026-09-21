# AGENTS.md — Orientation for AI agents working in this repo

This file is the entry point for any AI agent (Claude Code, Cursor, Codex, etc.) landing in `kriskrug-wp`. Read this *first*. It's intentionally short.

## What this repo is

The operations + content hub for [kriskrug.co](https://kriskrug.co/) — a Pagely-hosted WordPress site running the Aurora theme (`kk-aurora`). Live WordPress and theme versions change independently of this repo. Run `make status-readonly` and use the public `style.css` readback before making a current-state claim; never treat the repo version as production proof. The repo is **adjacent to** the live site, not a mirror of it. `main` contains the canonical tracked theme line, plus content/ops tooling and docs. Custom repo-side WP code includes `inc/digital-composting.php` and `plugins/kk-sidebar-promos/` (deploy only with an explicit rollback path and KK approval).

## Read this in order (top of repo, top of context)

1. [`docs/current-state/README.md`](docs/current-state/README.md) — current-state front door; run `make status-readonly` for live counters
2. [`docs/current-state/CURRENT-STATE-2026-07-30.md`](docs/current-state/CURRENT-STATE-2026-07-30.md) — declared snapshot for drift/morning-truth (Makefile default)
3. [`docs/current-state/WORK-PLAN-2026-09-09.md`](docs/current-state/WORK-PLAN-2026-09-09.md) — active day runbook
4. [`docs/current-state/MASTER-PLAN-2026-07-30.md`](docs/current-state/MASTER-PLAN-2026-07-30.md) — hygiene + lane sequencing plan
5. [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) — Track A / Track B decision rule
6. [`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md) — standing publisher safety rules
7. [`docs/current-state/AGENT-RUNTIME-REFERENCE.md`](docs/current-state/AGENT-RUNTIME-REFERENCE.md) and [`.env.schema`](.env.schema) — runtime and secret-handling reference

Older May–June plans live under [`docs/current-state/archive/`](docs/current-state/archive/) (#549). Bannered July predecessors (`WORK-PLAN-2026-07-16.md`, `CURRENT-STATE-2026-07-16.md`, etc.) are historical unless a newer doc says otherwise.

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

## Current versus historical

Use `docs/current-state/README.md`, the active workflow files, and fresh
GitHub readback for current operating state. Bannered historical documents,
the retired GitHub Actions swarm, old Cloudways setup, and `aurora/v2` branch
references are evidence only. Do not revive their commands or workflows.

## How to publish a post (Track A)

See [`scripts/notion-to-wp/README.md`](scripts/notion-to-wp/README.md). Short version: dry-run first, slug-match second, publish third.

## How to file an issue

`issues-to-create/` holds markdown drafts. Filed issues live at [github.com/WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues).

## How to commit

- Commit messages: `<area>: <short imperative>` — e.g. `content: ...`, `docs: ...`, `feat: ...`, `fix: ...`.
- One concern per commit. Don't bundle content edits with doc edits with theme edits.
- Don't push to `main` without KK's go-ahead if the change touches prod-rendering code (schema, redirects, custom snippets).
- PRs start as drafts unless the lane is tiny and fully verified. Repo `allow_auto_merge` is `false`, so nothing merges itself; an agent still has to run the merge.
- **Theme / plugins / `inc/` / live deploy PRs:** ask KK before merging, and run the pixel gate when required. As of 2026-08-23 this is a **convention, not an enforced gate** - no CI job blocks those paths, so it rests on you following it. Deploying to live WordPress is a separate act from merging and still needs explicit KK approval every time.
- **Content/docs-only PRs:** agents may merge these directly. `main` requires **0 approving reviews**, **`Test PR / summary` green**, and the branch **up to date with `main`** (`strict: true`). Merge with `gh pr merge <n> --squash --delete-branch` — **no `--admin`**. Use `--admin` only when KK explicitly asks to override a red or stale check. Force pushes and branch deletion on `main` stay blocked.

## When in doubt

Read [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md). If that doesn't answer it, stop and ask the human.

## Session start

Run `make doctor`, then `make status-readonly`, before execution. Use
`make morning-truth` only for a local ignored report; use
`make morning-truth-checkpoint` only for an explicit release, incident,
durable decision, or handoff.
