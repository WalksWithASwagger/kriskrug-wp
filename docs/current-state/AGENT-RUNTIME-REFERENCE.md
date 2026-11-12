# Agent Runtime Reference

Environment-specific operating notes for agents working in `kriskrug-wp`.
This is a reference, not a source of live production truth. Start with
`AGENTS.md`, then use `make doctor` and `make status-readonly` before acting.

## Runtime model

This repository is CLI tooling plus a WordPress theme and plugin line. It has
no local web application to boot. Local work means running the documented
Python CLIs and PHP validation gates. Live WordPress runs on Pagely and is not
file-synced with this checkout.

CI pins PHP 8.2 and Python 3.12. JavaScript syntax checks use Node 20;
the WordPress Playground browser job uses Node 24. Playground 3.1.62
requires Node >=24.18.0 and npm >=11.16.0. Local versions may differ. Check
`php --version` before explaining a local PHP result; `phpcs.xml.dist` targets
PHP 8.1 and later independently of the local minor version.

## Python environments

The root `requirements-test.txt` is the canonical test environment. It is the
only requirements file that supports `make python-test` and
`make ruff-changed`.

`scripts/notion-to-wp/.venv` is a separate runtime environment used directly
by several Make targets, including `seo-audit`, `seo-backfill`, and
`draft-queue-audit`. Its `requirements.txt` is runtime-only; include the root
test requirements when running that package's tests.

## Authentication and secrets

Use either `WP_USER` plus `WP_APP_PASSWORD`, or `WP_API_USERNAME` plus
`WP_API_PASSWORD`; `scripts/common.py` maps the latter pair to the former.
Do not infer that credentials are missing from an unset `WP_USER`. Run
`make doctor` and use redacted presence checks only.

Varlock is the source of truth. Read `.env.schema` and
`VARLOCK-ROLLOUT-2026-07-16.md`; never read, print, or commit `.env` or
`.env.local`. The project values file is
`~/.agents/env/values/.env.kriskrug-wp.local`. Prefer `make varlock-run CMD='…'`
or `varlock run --inject vars -- …`. `make draft-queue-audit` injects through
Varlock; if credentials are unavailable, use credential-free paths such as
`LOCAL_ONLY=1 make draft-queue-audit` and `make status-readonly`.

Use normal `gh` authentication. A scoped `GH_TOKEN` can authenticate the CLI,
but does not bypass branch protection.

## Validation and production boundaries

The pixel gate uses `make visual-preflight`, `make visual-baseline`, and
`make visual-diff`. Browser locations vary by environment. Follow
`AURORA-VISUAL-BASELINE-RUNBOOK.md` when preflight fails. A frozen baseline is
not deploy proof: the official comparison is post-deploy live against
pre-deploy live.

`scripts/deploy_theme_sftp.py` uses `WP_SFTP_PASSWORD` from the process or the
macOS Keychain service `pagely-sftp-kriskrug`, and requires `paramiko`. REST
application passwords cannot upload themes. A live theme deploy always needs
explicit KK approval and an explicit rollback path.

`make morning-truth`, `make status-readonly`, and audit targets may call
`https://kriskrug.co`. They degrade when the network is unavailable. Never use
the checked-in Aurora version as production proof: read public `style.css`.

`make payload-parity` (`scripts/check_page_payload_parity.py`, #1222) compares
live `content.raw` for every page in `wp-payloads/page-map.json` and
`wp-payloads/topic-hubs/page-map.json` with its tracked payload, using the
deploy's own normalization and SHA-256. It sends authenticated GETs only and
prints IDs, slugs, dates, hashes and `match` or `DRIFT`, never page content.
It needs credentials, so run it as `make varlock-run CMD='make payload-parity'`.
Exit 0 means every page matches, 1 means drift, 2 means it could not verify.
It never checks the superseded `issue-480-retire-inline-css/` pack, which
`content_architecture_deploy.py` also refuses as a `--map`, and it does
not cover Publications (1895) or Events (2250). A dry run of
`scripts/content_architecture_deploy.py` prints the same per-page verdict
before its `[dry-run]` line. File any drift it finds as its own issue; the
check does not fix it.

## GitHub Actions: files present vs enabled

A workflow YAML file in `.github/workflows/` is not proof it is enabled or
scheduled. Read the Actions API before treating a workflow as live:

```bash
gh api repos/WalksWithASwagger/kriskrug-wp/actions/workflows --jq '[.workflows[] | {name,state,path}]'
```

Dated API readback **2026-09-30**:

| Name | Path | State |
|---|---|---|
| Test PR | `.github/workflows/test-pr.yml` | `active` |
| backlog-reconcile | `.github/workflows/backlog-reconcile.yml` | `active` |
| Dependabot Updates | `dynamic/dependabot/dependabot-updates` | `active` |
| Dependency Graph | `dynamic/dependabot/update-graph` | `active` |
| Auto-Triage Issues | `.github/workflows/auto-triage.yml` | `disabled_manually` |
| Marquee Weekly Scan | `.github/workflows/marquee-weekly.yml` | `disabled_manually` |

Auto-Triage Issues and Marquee Weekly Scan sat disabled for an unknown reason
until KK ruled on 2026-11-12 (#1220) to delete both YAML files. Without a file
on `main` neither can run, though the Actions API may keep listing them by name.
Do not recreate them or edit repository settings to restore them. Historical
swarm docs (`docs/architecture.md`,
`docs/automation-guide.md`) describe files, not current Actions state.

`practice-preview` is a local-only Make target. CI's `practice-browser` job
runs `make practice-browser-test` (which runs `practice-test` first) and
`make events-browser-test` on every pull request. Setup, Node/npm split, and
the fixture-vs-production boundary live in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md). Playground 3.1.62 still requires
Node >=24.18.0 and npm >=11.16.0; JavaScript syntax checks still use Node 20.
