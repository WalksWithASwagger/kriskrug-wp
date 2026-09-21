# Agent Runtime Reference

Environment-specific operating notes for agents working in `kriskrug-wp`.
This is a reference, not a source of live production truth. Start with
`AGENTS.md`, then use `make doctor` and `make status-readonly` before acting.

## Runtime model

This repository is CLI tooling plus a WordPress theme and plugin line. It has
no local web application to boot. Local work means running the documented
Python CLIs and PHP validation gates. Live WordPress runs on Pagely and is not
file-synced with this checkout.

CI pins PHP 8.2, Python 3.12, and Node 20. Local versions may differ. Check
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
`.env.local`. Prefer `make varlock-run CMD='…'` or
`varlock run --inject vars -- …`. If credentials are unavailable, use
credential-free paths such as `LOCAL_ONLY=1 make draft-queue-audit` and
`make status-readonly`.

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
