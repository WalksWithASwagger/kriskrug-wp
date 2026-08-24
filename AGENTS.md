# AGENTS.md — Orientation for AI agents working in this repo

This file is the entry point for any AI agent (Claude Code, Cursor, Codex, etc.) landing in `kriskrug-wp`. Read this *first*. It's intentionally short.

## What this repo is

The operations + content hub for [kriskrug.co](https://kriskrug.co/) — a Pagely-hosted WordPress site running the Aurora theme (`kk-aurora`). Live WordPress and theme versions change independently of this repo. Run `make status-readonly` and use the public `style.css` readback before making a current-state claim; never treat the repo version as production proof. The repo is **adjacent to** the live site, not a mirror of it. `main` contains the canonical tracked theme line, plus content/ops tooling and docs. Custom repo-side WP code includes `inc/digital-composting.php` and `plugins/kk-sidebar-promos/` (deploy only with an explicit rollback path and KK approval).

## Read this in order (top of repo, top of context)

1. [`docs/current-state/README.md`](docs/current-state/README.md) — current-state front door; run `make status-readonly` for live counters
2. [`docs/current-state/CURRENT-STATE-2026-07-30.md`](docs/current-state/CURRENT-STATE-2026-07-30.md) — declared snapshot for drift/morning-truth (Makefile default)
3. [`docs/current-state/WORK-PLAN-2026-08-23.md`](docs/current-state/WORK-PLAN-2026-08-23.md) — **day runbook** (Aurora 1.6.9 live/repo parity; hub packs #829-#832 next; normal protected merge lane is open; supersedes 2026-08-17)
4. [`docs/current-state/MASTER-PLAN-2026-07-30.md`](docs/current-state/MASTER-PLAN-2026-07-30.md) — hygiene + lane sequencing plan of record
5. [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) — the active operating model
6. [`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md) — postmortem with the safety rules every agent must follow
7. [`.env.schema`](.env.schema) — Varlock env contract (names/sensitivity only; never read/print `.env`)

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

## What's historical or parked (don't get distracted)

- **`.github/agents/`** — the older GitHub Actions agent swarm (orchestrator → analyzer → test-writer → implementer → QA → reviewer → PR creator). It produced PRs #71 and #72 in May 2026 and is not used by current sessions.
- **`.github/workflows/agent-pr-generator.yml`, `sync-projects.yml`, `agent-safe-merge.yml`** — deleted 2026-08-23. The first two were parked diagnostic stubs; the third never merged a single PR. `docs/architecture.md` and `docs/automation-guide.md` still describe them and are reference-only.
- **`docs/current-state/AGENT-MERGE-PATH-2026-07-26.md`** — historical record of the deleted `agent-safe-merge` workflow, not current merge guidance.
- **`.github/workflows/test-pr.yml`** — still active PR validation. Do not describe all workflows as dormant.
- **`docs/architecture.md`, `docs/automation-guide.md`** — reference docs for the dormant swarm.
- **`docs/cloudways-setup.md`, `docs/local-development-setup.md`, `.claude/context/wordpress-setup.md`** — Cloudways dev-server setup that was never used as planned. Relevant if/when Track B needs staging, otherwise ignore.
- **`docs/vision.md`, `docs/roadmap.md`** — early planning docs. Use `CURRENT-STATE-2026-07-30.md`, `WORK-PLAN-2026-08-23.md`, `MASTER-PLAN-2026-07-30.md`, and a fresh `make status-readonly` run for current truth. May–June handoffs live under `docs/current-state/archive/`.

Anything banner-tagged `STATUS: Historical` at the top is reference-only.

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

## Morning truth command

Run `make doctor` first: it reports in one screen whether WP credentials resolve (under either name pair), whether the venv and `gh` are usable, whether the tree is clean, and whether other worktrees are live. Then run `make status-readonly` (or before execution). It prints git/issue/worktree state, WP smoke, draft queue counts, and current-state drift flags without writing a file.

Use `make morning-truth` only when a local copy is useful. It writes the same report to the gitignored `.generated/current-state/` directory.

Use `make morning-truth-checkpoint` only for an explicit release, incident, durable decision, or handoff checkpoint. That deliberate mode writes under `docs/current-state/reports/`; review and commit the report with the related work. Existing committed reports remain historical evidence, not a freshness requirement for routine sessions.

## Cursor Cloud specific instructions

This repo is CLI tooling + a WordPress theme/plugins line — there is **no local web app or server to boot**. "Running" it means executing the Python CLIs (`scripts/notion-to-wp/`, `scripts/*.py`) and the PHP lint/smoke checks. Standard commands (`make test`, `make validate`, `make verify`, connector usage) are already documented in `CONTRIBUTING.md`, `Makefile`, and `scripts/notion-to-wp/README.md`; use those.

Non-obvious caveats for future agents (the update script already installs deps):

- The Python venv lives at `scripts/notion-to-wp/.venv` and **many `Makefile` targets call `scripts/notion-to-wp/.venv/bin/python` directly** (e.g. `seo-audit`, `seo-backfill`, `draft-queue-audit`). If that venv is missing those targets break, so it must exist — the update script (re)creates it.
- PHP is **8.3** here (CI pins 8.2). This does not affect linting: `phpcs.xml.dist` sets `testVersion 8.1-` as a static target, so `make validate` / `make plugin-smoke` run fine on 8.3.
- Pixel gate (`make visual-preflight` / `visual-baseline` / `visual-diff`): Chromium is **not** always at `/opt/pw-browsers` in every Cloud image. If preflight FATAL, install Playwright locally under `~/.local/pw` with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`, point `PLAYWRIGHT_BROWSERS_PATH=~/.local/pw-browsers`, and symlink Playwright's `chromium-1148` (+ headless shell) binaries to the system Chrome at `/opt/google/chrome/chrome`. Export `NODE_PATH=$HOME/.local/pw/node_modules` when invoking make targets. Official gate still compares **post-deploy live vs pre-deploy live** — a frozen baseline alone is not merge proof.
- Theme SFTP deploy (`scripts/deploy_theme_sftp.py`): accepts `WP_SFTP_PASSWORD` in process env (Cloud), else macOS Keychain service `pagely-sftp-kriskrug`. Needs `paramiko` installed. REST `WP_APP_PASSWORD` cannot upload themes via Appearance → Themes.
- Authenticated work needs **either** `WP_USER` + `WP_APP_PASSWORD` **or** `WP_API_USERNAME` + `WP_API_PASSWORD` (optional `NOTION_TOKEN`). Every script accepts both pairs as of 2026-08-23; `scripts/common.py` aliases the API names onto the legacy ones. On KK's laptop the Varlock vault supplies only the `WP_API_*` pair, so **do not conclude credentials are missing because `WP_USER` is unset** - run `make doctor`. Cursor Cloud secrets may use either pair. Laptop Varlock/1Password does **not** inject into this VM. After secret entry, verify with a redacted presence check (`WP_USER` length only) before assuming auth works; a long-lived agent pod that started before secrets were saved may still see them as unset until a new session boots with the secrets attached.
- **GitHub CLI from Cloud:** use normal `gh` authentication. If the session has no stored auth, an optional `GH_TOKEN` with repo scope can authenticate `gh`; it does not bypass branch protection. Confirm auth with `gh auth status` and follow the same green-check, up-to-date-branch merge path documented above.
- Without those env vars (and without a gitignored `scripts/notion-to-wp/.env` cache), connector/publisher paths stay unauthenticated: the live publisher and `create_local_wp_draft.py` **hard-exit requiring creds even in dry-run**. Use credential-free paths instead — `LOCAL_ONLY=1 make draft-queue-audit` and `make status-readonly`.
- Read [`.env.schema`](.env.schema) and [`docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md`](docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md) for the Varlock env contract. Do **not** read, print, or commit `.env` / `.env.local`. Use `make env-check` when `varlock` is on `PATH` (soft-OK if secrets are absent). Prefer `make varlock-run CMD='…'` / `varlock run --inject vars -- …` when secrets are resolved. Sibling-path `KKAI_ENV_PATH` fallbacks are **compat only**, not the secret source of truth.
- `make morning-truth`, `make status-readonly`, and the audit targets make live HTTP calls to `https://kriskrug.co` when reachable; they degrade gracefully but expect outbound network for the WP smoke portions.
- Live Aurora and repo Aurora drift in **either** direction. Do not treat `theme/kk-aurora/style.css` Version as proof of production without a public `style.css` readback, and do not assume the direction of any future drift. Read back, don't assume.

---

**Instruction review:** 2026-08-13. Runtime state is deliberately not pinned here. Run `make status-readonly`, consult the current-state front door, and use public readback evidence before acting on live-state assumptions.
