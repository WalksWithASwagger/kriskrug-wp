# AGENTS.md — Orientation for AI agents working in this repo

This file is the entry point for any AI agent (Claude Code, Cursor, Codex, etc.) landing in `kriskrug-wp`. Read this *first*. It's intentionally short.

## What this repo is

The operations + content hub for [kriskrug.co](https://kriskrug.co/) — a Pagely-hosted WordPress site running Catch Responsive. The repo is **adjacent to** the live site, not a mirror of it. There is no theme code, plugin code, database, or media in this repo. There is one custom WP module (`inc/digital-composting.php`) which is merged but not yet deployed to prod.

## Read this in order (top of repo, top of context)

1. [`docs/current-state/README.md`](docs/current-state/README.md) — index of the May-2026 baseline snapshot
2. [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) — the active operating model
3. [`docs/current-state/REPO_STATE.md`](docs/current-state/REPO_STATE.md) — what's actually built vs. just documented
4. [`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md) — postmortem with the safety rules every agent must follow

After those four, the rest of the repo will make sense.

## Two tracks — pick one per session

| | Track A — Content + SEO | Track B — Aurora v2 theme |
|---|---|---|
| Branch | `main` | `aurora/v2` |
| Touches | Posts, pages, media, taxonomies, Code Snippets (PHP/CSS), schema JSON-LD, redirects, alt text | `theme/kk-aurora/`, FSE templates, theme.json |
| Lives in | `content/drafts/`, `fixes/`, `scripts/notion-to-wp/`, `docs/current-state/` | `theme/`, `demo/`, `docs/current-state/AURORA-*` |
| Owner | Publisher-mode session | Architect-mode session |

**Decision rule:** Editing a post / page / media / category / schema / redirect → Track A. Editing theme files / FSE templates / theme.json → Track B. If you're doing both in one session, you've scope-crept — finish one, commit, then start the other in a fresh session.

Full decision tree: [`TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md#how-to-know-which-track-youre-in).

## Hard safety rules (post 2026-05-15 incident)

1. **Backup before destructive operations.** No exceptions for "small" changes. See [`BACKUP_PLAN.md`](docs/current-state/BACKUP_PLAN.md).
2. **Slug-based idempotency** for the Notion → WP connector. Never PATCH a WP post without first verifying that the slug match is the intended target. See [`INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md).
3. **No theme file changes on `main`.** Theme work belongs on `aurora/v2`.
4. **Don't run the connector on production without `--dry-run` first.**

## What's dormant (don't get distracted)

- **`.github/agents/` + `.github/workflows/`** — the older GitHub Actions agent swarm (orchestrator → analyzer → test-writer → implementer → QA → reviewer → PR creator). It produced PRs #71 and #72 in May 2026 and is not used by current sessions.
- **`docs/architecture.md`, `docs/automation-guide.md`** — reference docs for the dormant swarm.
- **`docs/cloudways-setup.md`, `docs/local-development-setup.md`, `.claude/context/wordpress-setup.md`** — Cloudways dev-server setup that was never used as planned. Relevant if/when Track B needs staging, otherwise ignore.
- **`docs/vision.md`, `docs/roadmap.md`** — early planning docs. The current roadmap is [`docs/current-state/ROADMAP.md`](docs/current-state/ROADMAP.md).

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

---

**Last verified:** 2026-05-17. If you're reading this much later than that and the rest of the repo has drifted, treat `docs/current-state/` as the source of truth and flag the drift for a fresh audit.
