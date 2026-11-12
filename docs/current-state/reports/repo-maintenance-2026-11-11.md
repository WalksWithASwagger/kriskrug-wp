# Repo Status

Observed on November 11, 2026, America/Vancouver (tool timestamps cross into
November 12 UTC). Startup was `main` at `936f29c`, eight commits behind
`origin/main`, with zero local-only commits and no stashes. The primary checkout
was fast-forwarded to `81036bf` before focused feature work.

There were no tracked edits at startup. Four untracked directory groups
contained 107 files: `.generated/`, the October 4 Downtown Eastside draft,
the October 4 Work-card package, and `design-proofs/`. A SHA-256 preservation
manifest was recorded before synchronization; the final comparison verified
all 107 files unchanged. These files are outside this maintenance's
commit/deletion scope.

Git listed only the primary checkout. No extra worktree needed removal and no
disk-space recovery is claimed. Twelve local branches and eight remote branches
were removed after matching their tips, or an ancestor of their tips, to merged
PRs or main. Six already-deleted remote branches had stale tracking refs pruned.
All 26 selected local/remote tips were verified against their recovery refs,
including the six already-absent remote branches. Recovery refs are under:

```text
refs/archive/cleanup-20261111/local/<former-branch-name>
refs/archive/cleanup-20261111/remote/<former-branch-name>
```

Removed local branches: `codex/4819-host-hardening-package`,
`codex/appearances-events-20261106`, `codex/canada-now-source-record`,
`codex/events-archive-2021-galiano`, `codex/events-archive-2023`,
`codex/events-overhaul`, `codex/gardener-1168-refresh`,
`codex/qs-security-after-playground`, `codex/testimonials-redesign`,
`codex/ubc-header-layout-20261102`, `codex/wp7-smoke-recovery`, and
`codex/wp7-smoke-transport`.

Removed remote branches: `codex/4819-host-hardening-package`,
`codex/canada-now-intake-20261109`, `codex/futureproof-events-links-20261109`,
`codex/qs-security-after-playground`, `codex/ubc-header-layout-20261102`,
`codex/wp7-smoke-recovery`, `dependabot/npm_and_yarn/npm-minor-patch-29cd64fc33`,
and `dependabot/pip/pytest-gte-9.2.0`.

Preserved pre-existing branches: `codex/local-checkpoint-2026-10-02` and
`codex/qs-security-patch` retain explicit checkpoint/superseded-patch history;
`codex/showpiece-review` retains the prior release source; `codex/publications-1191`
retains its existing task pointer. No force deletion, history rewrite, raw
worktree removal or default-branch deletion was used.

# What This Project Is

The operations/content hub for Kris Krüg's personal WordPress site on Pagely.
It holds the Aurora theme, helper plugins, page payloads, publishing tools and
release evidence. The repository is adjacent to production, not an automatic
deployment mirror. A merged commit does not prove a WordPress release.

# How To Run It

These commands come from the Makefile, README, CONTRIBUTING and CI configuration.
There is no local application server.

| Purpose | Evidence-backed command |
|---|---|
| Install Python test dependencies | `python3 -m venv .venv && source .venv/bin/activate`, then `pip install -r requirements-test.txt` |
| Install PHP validation dependencies | `composer install` |
| Install browser-test dependencies | `npm ci --ignore-scripts`; CI also runs `node node_modules/playwright/cli.js install --with-deps chromium` |
| Startup/run | `make doctor`, then `make status-readonly` |
| Redacted environment check | `varlock load --agent --show-all` |
| Authenticated read-only startup | `make varlock-run CMD='make status-readonly'` |
| Full local gate | `make verify` |
| Python test suites | `make python-test` |
| Python lint | `make ruff-changed BASE_REF=origin/main` |
| PHP lint/standards | `make validate` |
| JavaScript syntax/harnesses | `make javascript-syntax` |
| Browser behavior | `make practice-browser-test` and `make events-browser-test` |
| Typecheck | No dedicated typecheck target found |

This pass used the existing `scripts/notion-to-wp/.venv/bin/python` via the
`PYTHON` override; no dependency installation was needed. CI uses Python 3.12,
PHP 8.2, Node 20 for syntax and Node 24 for browser tests. Local verification
used Python 3.14.6, PHP 8.5.12, Node 24.22.1 and npm 11.19.1. The lockfile's
Playground 3.1.62 packages require Node >=24.18.0 and npm >=11.16.0.

# Project Map

| Path | Purpose |
|---|---|
| `content/drafts/`, `content/source-packs/` | Cleared editorial packages and approved page payloads |
| `scripts/notion-to-wp/`, `scripts/common.py` | Publisher and shared authenticated WordPress client |
| `scripts/events_page/` | Events catalog, fragments, renderer and rollover contract |
| `theme/kk-aurora/`, `plugins/`, `inc/` | Theme and packaged/custom WordPress code |
| `scripts/tests/`, `scripts/seo-backfill/tests/` | Operational, publishing, SEO and regression tests |
| `docs/current-state/` | Runbooks, roadmap and dated receipts |
| `.github/workflows/` | CI configuration; inspect the API for actual enabled state |

Tracked assets total roughly 409 MB; `all-in-2026/` accounts for about 298 MB
and `content/` for 76 MB. No additional checkout or asset archive copy was
created. Those figures are tracked blob sizes, not a disk-usage measurement.

# GitHub Workflow

Startup had zero open PRs and 33 open issues. Six completed issues were closed,
leaving 27 open after the Publications merge. Recent commits include the
approved page redesigns and dependency patches; there was no pending PR queue
to merge blindly.

- Closed #1194, #1195, #1196 and #1197 after approved-release/browser evidence
  and fresh authenticated/public verification. About, Photography, MØTLEYKRÜG
  and Contact match canonical source byte for byte, with all expected markers
  and public HTTP 200. About's retained portrait credit remains unverified.
- Closed the delivered Events implementation epic #1098. Current cadence
  verification and stronger-intake decisions remain explicitly in #1102.
- Reconciled #767, #1165, #1176 and #1102 to their actual remaining work;
  corrected #771's source-package path and preserved its distinction from #1016.
- Publications reconciliation [#1207](https://github.com/WalksWithASwagger/kriskrug-wp/pull/1207)
  merged through the normal protected path and closed #1191. Required CI,
  including the browser suites, passed. Its live source hash is
  `bcf7cd4cf9971ebe5a660848b20437cf631ff769c9905787f83c31904c085c0b`.
  Independent review confirmed all 51 dated archive records and their
  destinations are preserved. The later polish preview is excluded.

The Actions API reports Test PR, backlog-reconcile, Dependabot Updates and
Dependency Graph active. Auto-Triage Issues and Marquee Weekly Scan remain
`disabled_manually`. Branch protection requires `summary`, strict freshness
against main, and zero approving reviews. No settings or workflow states changed.

# Engineering Health

- `make doctor` passed with warnings for the original untracked work and
  credentials not directly present in the shell. Varlock resolved the schema
  and the authenticated readbacks succeeded through the existing alias pair.
- Startup observed WordPress 7.0.8, 69 draft posts, four draft pages and no
  scheduled posts. Public Aurora and `origin/main` both report 1.7.1.
  The October baseline's 68 drafts/28 issues are dated counters, not defects.
- The initial public smoke had one Speaking TLS timeout. A targeted retry
  returned 200 with no route failures. Supplying only Speaking to the version
  gate cannot detect the homepage generator; no clean full-smoke rerun is claimed.
- The full Python suites passed 1,145 tests after the Publications sync.
  JavaScript, plugin/theme smoke, PHP syntax (56 files), WPCS and scoped Ruff
  passed. The docs gate caught an undated heading during editing; it was fixed
  and rerun. Browser suites passed in required CI on #1207, not as local runs.
- Publications exposed a real source-drift gap: the approved page was live
  while tracked HTML was older. Exact live-body reconciliation, four new media
  records, explicit published-URL mappings and the lead-video regression
  check repair that gap. The source synchronization performs no live write.
- GitHub returned zero open Dependabot alerts. This is not a new exhaustive
  vulnerability audit. No secret values, old credential bodies or browser
  cookies were inspected; the environment schema is the contract.
- The redacted enumeration check reports REST 401, no users sitemap child,
  and author probe 404 without a username redirect. HSTS remains absent:
  three checks pass, one fails. The keep-admin decision is already recorded.
- TODO/FIXME/HACK search found mostly test fixtures and draft-quality scanners;
  it is not proof of no debt. No dedicated coverage percentage was measured.
  This is not an LLM application requiring a separate model-evaluation suite.

The current Events heartbeat and signup monitor were not independently
reverified. They remain explicit evidence tasks; no duplicate automation was
created and no scheduler state was changed.

# Highest-Leverage Next Steps

- **Quick wins:** retain the reconciled Publications source and new
  documentation entry points; verify the existing Events cadence.
- **Important fixes:** complete the Canada Now KB/quote-bank work, prepare the
  exact remaining HSTS decision, and resolve Futureproof's conditional BC + AI link.
- **Bigger refactors:** take one interaction gap at a time under #424; prove
  Open Studio with real participants before expanding it. Reuse the Events system.
- **Questions for KK:** exact HSTS proposal, practice copy/participants,
  interaction treatment, favicon assets and which Gorgeous Ghost draft to advance.
  These decisions do not block independent knowledge or maintenance work.

# Suggested First Work Session

One hour on Canada Now: 10 minutes to confirm the verified source record,
35 minutes to complete transcript/index and quote-bank gaps, then 15 minutes
to check retrieval and citations. If those sources are unavailable, perform a
bounded Events sweep and return one exact proposal or a dated no-change result.
The [roadmap](../ROADMAP-2026-11-11.md) gives owners, sequence and completion gates.
