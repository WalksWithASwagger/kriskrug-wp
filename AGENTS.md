# AGENTS.md — Orientation for AI agents working in this repo

This file is the entry point for any AI agent (Claude Code, Cursor, Codex, etc.) landing in `kriskrug-wp`. Read this *first*. It's intentionally short.

## What this repo is

The operations + content hub for [kriskrug.co](https://kriskrug.co/) — a Pagely-hosted WordPress site running the Aurora theme (`kk-aurora`). **Live** theme (`style.css` Version) as of 2026-08-11 public readback: **1.6.4**, **in sync** with repo `main` (SFTP-deployed 2026-08-11, shipping 1.6.1 through 1.6.4 — form-message colors, breakpoint consolidation, the PSI perf round, and the #701 CLS/LCP guard — in one window; server-side rollback at `kk-aurora.bak-1786415439`). **Post-deploy step still owed: regenerate Jetpack Boost critical CSS** (stale-snapshot geometry was the #701 root cause). WordPress publicly reports **7.0.3**. How verified: `curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i version` against `theme/kk-aurora/style.css`. Do not treat the repo `style.css` version as proof of production. Read back the public file, in either direction. The repo is **adjacent to** the live site, not a mirror of it. `main` contains the canonical tracked theme line, plus content/ops tooling and docs. Custom repo-side WP code includes `inc/digital-composting.php` and `plugins/kk-sidebar-promos/` (deploy only with an explicit rollback path and KK approval).

## Read this in order (top of repo, top of context)

1. [`docs/current-state/README.md`](docs/current-state/README.md) — index; start with the newest `reports/morning-truth-*.md`
2. [`docs/current-state/CURRENT-STATE-2026-07-30.md`](docs/current-state/CURRENT-STATE-2026-07-30.md) — declared snapshot for drift/morning-truth (Makefile default)
3. [`docs/current-state/WORK-PLAN-2026-08-09.md`](docs/current-state/WORK-PLAN-2026-08-09.md) — **day runbook** (repo-integrity rescue → truth → deploy window; supersedes 2026-08-05)
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
- **`.github/workflows/agent-pr-generator.yml`** — parked on 2026-05-20. It is now a manual, read-only diagnostic stub and no longer auto-runs when `auto-implement` is labeled.
- **`.github/workflows/test-pr.yml`** — still active PR validation. Do not describe all workflows as dormant.
- **`docs/architecture.md`, `docs/automation-guide.md`** — reference docs for the dormant swarm.
- **`docs/cloudways-setup.md`, `docs/local-development-setup.md`, `.claude/context/wordpress-setup.md`** — Cloudways dev-server setup that was never used as planned. Relevant if/when Track B needs staging, otherwise ignore.
- **`docs/vision.md`, `docs/roadmap.md`** — early planning docs. Use `CURRENT-STATE-2026-07-30.md`, `WORK-PLAN-2026-07-30.md`, `MASTER-PLAN-2026-07-30.md`, and the newest committed morning-truth report for current truth. May–June handoffs live under `docs/current-state/archive/`.

Anything banner-tagged `STATUS: Historical` at the top is reference-only.

## How to publish a post (Track A)

See [`scripts/notion-to-wp/README.md`](scripts/notion-to-wp/README.md). Short version: dry-run first, slug-match second, publish third.

## How to file an issue

`issues-to-create/` holds markdown drafts. Filed issues live at [github.com/WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues).

## How to commit

- Commit messages: `<area>: <short imperative>` — e.g. `content: ...`, `docs: ...`, `feat: ...`, `fix: ...`.
- One concern per commit. Don't bundle content edits with doc edits with theme edits.
- Don't push to `main` without KK's go-ahead if the change touches prod-rendering code (schema, redirects, custom snippets).
- PRs start as drafts unless the lane is tiny and fully verified. Repo `allow_auto_merge` is `false`. Green checks mean ready for review, not automatic merge.
- **Theme / plugins / `inc/` / live deploy PRs:** merge only after KK approval (and pixel gate when required).
- **Content/docs-only PRs:** Cloud agents may approve+squash-merge when Cursor Cloud secret `GH_TOKEN` is a write-access PAT, or when label `agent-safe-merge` is applied (Actions secret `AGENT_MERGE_TOKEN`). See [`docs/current-state/AGENT-MERGE-PATH-2026-07-26.md`](docs/current-state/AGENT-MERGE-PATH-2026-07-26.md). The Cursor GitHub App token alone **cannot** satisfy required reviews.

## When in doubt

Read [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md). If that doesn't answer it, stop and ask the human.

## Morning truth command

Run `make morning-truth` at session start (or before execution) to emit a timestamped read-only report under `docs/current-state/reports/` with git/issue/worktree state, WP smoke, draft queue counts, and current-state drift flags.

If the task explicitly forbids file changes, run `make status-readonly` instead. It prints the same startup truth shape to stdout and does not write a report file.

**Keeping the cadence alive:** `make morning-truth` writes the `.md` but does *not* auto-commit it — the report only becomes the shared source of truth once someone commits it. The report others read stays current only if the session that runs `morning-truth` also commits the fresh `docs/current-state/reports/morning-truth-*.md` (these `.md` summaries are tracked; only `reports/` PNG/HTML/CSV captures are gitignored). If the newest committed report is more than a few days stale, that means recent sessions ran `status-readonly` (stdout-only) or skipped the commit — not that the target is broken. Regenerate and commit one.

## Cursor Cloud specific instructions

This repo is CLI tooling + a WordPress theme/plugins line — there is **no local web app or server to boot**. "Running" it means executing the Python CLIs (`scripts/notion-to-wp/`, `scripts/*.py`) and the PHP lint/smoke checks. Standard commands (`make test`, `make validate`, `make verify`, connector usage) are already documented in `CONTRIBUTING.md`, `Makefile`, and `scripts/notion-to-wp/README.md`; use those.

Non-obvious caveats for future agents (the update script already installs deps):

- The Python venv lives at `scripts/notion-to-wp/.venv` and **many `Makefile` targets call `scripts/notion-to-wp/.venv/bin/python` directly** (e.g. `seo-audit`, `seo-backfill`, `draft-queue-audit`). If that venv is missing those targets break, so it must exist — the update script (re)creates it.
- PHP is **8.3** here (CI pins 8.2). This does not affect linting: `phpcs.xml.dist` sets `testVersion 8.1-` as a static target, so `make validate` / `make plugin-smoke` run fine on 8.3.
- Pixel gate (`make visual-preflight` / `visual-baseline` / `visual-diff`): Chromium is **not** always at `/opt/pw-browsers` in every Cloud image. If preflight FATAL, install Playwright locally under `~/.local/pw` with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`, point `PLAYWRIGHT_BROWSERS_PATH=~/.local/pw-browsers`, and symlink Playwright's `chromium-1148` (+ headless shell) binaries to the system Chrome at `/opt/google/chrome/chrome`. Export `NODE_PATH=$HOME/.local/pw/node_modules` when invoking make targets. Official gate still compares **post-deploy live vs pre-deploy live** — a frozen baseline alone is not merge proof.
- Theme SFTP deploy (`scripts/deploy_theme_sftp.py`): accepts `WP_SFTP_PASSWORD` in process env (Cloud), else macOS Keychain service `pagely-sftp-kriskrug`. Needs `paramiko` installed. REST `WP_APP_PASSWORD` cannot upload themes via Appearance → Themes.
- Authenticated work needs process env `WP_USER` + `WP_APP_PASSWORD` (optional `NOTION_TOKEN`). Cursor Cloud secrets must use **those exact names**. Laptop Varlock/1Password does **not** inject into this VM. After secret entry, verify with a redacted presence check (`WP_USER` length only) before assuming auth works; a long-lived agent pod that started before secrets were saved may still see them as unset until a new session boots with the secrets attached.
- **GitHub merge from Cloud:** set Cursor Cloud secret `GH_TOKEN` to a classic PAT with `repo` scope owned by an account that has write access (same value as Actions secret `AGENT_MERGE_TOKEN`). Without it, `gh pr review --approve` / `gh pr merge` fail under branch protection even when CI is green. Details: [`docs/current-state/AGENT-MERGE-PATH-2026-07-26.md`](docs/current-state/AGENT-MERGE-PATH-2026-07-26.md).
- Without those env vars (and without a gitignored `scripts/notion-to-wp/.env` cache), connector/publisher paths stay unauthenticated: the live publisher and `create_local_wp_draft.py` **hard-exit requiring creds even in dry-run**. Use credential-free paths instead — `LOCAL_ONLY=1 make draft-queue-audit` and `make status-readonly`.
- Read [`.env.schema`](.env.schema) and [`docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md`](docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md) for the Varlock env contract. Do **not** read, print, or commit `.env` / `.env.local`. Use `make env-check` when `varlock` is on `PATH` (soft-OK if secrets are absent). Prefer `make varlock-run CMD='…'` / `varlock run --inject vars -- …` when secrets are resolved. Sibling-path `KKAI_ENV_PATH` fallbacks are **compat only**, not the secret source of truth.
- - `make morning-truth`, `make status-readonly`, and the audit targets make live HTTP calls to `https://kriskrug.co` when reachable; they degrade gracefully but expect outbound network for the WP smoke portions.
- Live Aurora and repo Aurora drift in **either** direction. As of 2026-08-11 they are **in sync at 1.6.4** (second deploy window executed). Historically the drift has gone both ways: on 2026-07-27 they were in sync at 1.5.0, and on 2026-08-01 live ran *ahead* of `main` because the 1.5.7 hero was SFTP-deployed before PR #618 merged. Do not treat `theme/kk-aurora/style.css` Version as proof of production without a public `style.css` readback, and do not assume the direction of any future drift. Readback, don't assume, in either direction.

---

**Last verified:** 2026-08-11 (live WP **7.0.3**; Aurora live and repo `main` **in sync at 1.6.4**; pixel gate repaired (#697) and ran clean on the 1.6.4 window — 33 small diffs all accounted for by intentional changes + same-day content drift; front door is CURRENT-STATE 2026-07-30 / WORK-PLAN 2026-08-09 / MASTER-PLAN 2026-07-30; Cloud secrets may still be unset in long-lived pods). If you're reading this much later and the repo has drifted, run `make morning-truth` (or `make status-readonly`) and treat the newest committed `docs/current-state/reports/morning-truth-*.md` as the source of truth.
