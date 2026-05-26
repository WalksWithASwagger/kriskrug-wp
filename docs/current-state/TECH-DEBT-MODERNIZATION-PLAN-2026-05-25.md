# Technical Debt Modernization Plan - 2026-05-25

**Scope:** `kriskrug-wp` as the operations, content, and Aurora theme hub for kriskrug.co.
**Initial evidence pass:** `make morning-truth` wrote `reports/morning-truth-20260525-045528Z.md`; `make test` passed 21 Notion publisher tests; `php plugins/kk-sidebar-promos/tests/smoke.php` passed; `make docs-truth-check` passed; `make validate` initially failed because PHPCS/WPCS was not repo-provisioned.
**Assumptions:** production currently works; no rewrite is justified; live WordPress writes remain gated by dry-runs, exact target checks, snapshots/rollback notes, and explicit approval for risky mutations.

## Phase 0 Kickoff - Completed 2026-05-25

- `make test` now includes the `kk-sidebar-promos` lightweight PHP smoke test.
- `make verify` now runs the default local test suite, docs truth checks, and PHP validation.
- `make wp7-smoke` and `make morning-truth` accept request timeout controls; `morning_truth_report.py` now returns a timeout result for long-running subprocesses instead of waiting silently.
- `auto-triage.yml` no longer tells users that `auto-implement` starts the parked agent swarm.
- `sync-projects.yml` is now manual/read-only diagnostic output instead of a placeholder workflow with write permissions and issue/PR triggers.

## Phase 1 Kickoff - Completed 2026-05-25

- Added repo-owned PHP validation through `composer.json`, `composer.lock`, and `phpcs.xml.dist`.
- Scoped the default PHPCS ruleset to high-signal WordPress security checks instead of full formatting cleanup.
- Updated `validate_wordpress.sh` to prefer `vendor/bin/phpcs`/`vendor/bin/phpcbf` and give clear install instructions.
- Aligned active GitHub PHP validation with `composer install` plus `make validate`.
- Fixed the new security gate findings: sanitized the sidebar promo nonce before verification and sanitized/unslashed request server values in the Aurora `/projects/` redirect.
- Updated contributor docs to remove stale global PHPCS and "no composer.json" guidance.

## Executive Summary

The repo is healthier than a typical rushed AI-assisted recovery project because it has strong incident memory, current-state reports, lane boundaries, and working guardrails around the highest-risk publishing path. The core debt is not "bad code everywhere"; it is operational sprawl around a repo that is both a documentation hub, content package archive, WordPress connector, theme source, plugin staging area, issue factory, and agent-workflow fossil bed.

Highest-priority risks:

- The active WordPress surface depends on a mix of repo theme files, live database page content, Code Snippets, Jetpack, Redirection, Pagely cache, and manual wp-admin upload steps. That is workable, but easy for agents to misunderstand.
- CI and local validation were mismatched at audit time. Phase 0/1 aligned the local PHP/test gate and active PHP CI, but JavaScript/theme checks are still mostly absent.
- Deployment remains partly manual and fragile: SFTP/SSH is blocked, theme upload requires a human to choose "Replace current with uploaded", and REST edits require explicit Pagely cache purge.
- At audit time, active workflows and issue labels still implied inactive automation. The Phase 0 kickoff corrected the workflow language, but `auto-implement` remains attached to 44 open issues and still needs queue hygiene.
- Theme complexity is high relative to the repo's tooling: multiple CSS/JS layers, CDN GSAP/ScrollTrigger, external hotlinked media, and several legacy templates that conflict with the new content-as-DB rule.

Immediate recommendation: stabilize the command surface first, then prune stale operational affordances, then standardize deploy and QA gates around the two real lanes: Track A content/SEO and Track B Aurora theme.

## Key Findings

### Architecture and Repo Structure

- `main` is canonical and synced with `origin/main`, but the tree holds several roles at once: docs, backups/manifests, content drafts, issue batches, WP scripts, a plugin, an FSE theme, and historical agent scaffolding.
- The two-track model is the right boundary. The newer 2026-05-24 decision is even sharper: global surfaces belong in `theme/kk-aurora/`; individual content pages should be REST-authored database content unless they are intentionally global templates.
- Worktree drift is material. The morning truth report shows the locked local `aurora/v2` worktree is ahead 38 and behind 50 with a modified zip, while `origin/aurora/v2...origin/main` is 18/129. Treat old Aurora branches as evidence, not deploy candidates.
- `theme/kk-aurora/` contains duplicate or legacy page templates (`page-work.html`, `page-2672.html`, `page-recent-projects-include.html`, `page-services.html`, `page-generative-ai-services.html`) that encode historical confusion about template ownership.

### Dependency Quality and Sprawl

- Python dependency footprint is small (`requests`, `python-dotenv`, `pyyaml`), but it is not locked. Runs depend on whichever interpreter/venv is available.
- There is no Node package surface despite theme JavaScript being production-relevant. That means no lint, formatting, or unit-level checks for `assets/js/`.
- PHP validation is now repo-provisioned through Composer and a focused PHPCS ruleset. Full WPCS formatting cleanup remains intentionally out of scope for the default gate.
- Theme runtime depends on external Google Fonts and jsDelivr GSAP/ScrollTrigger. That is acceptable as a temporary polish path but not a great long-term reliability posture.

### Security and Secrets Handling

- Secrets are gitignored (`scripts/notion-to-wp/.env` is ignored and not tracked), and prior credential-history rewrite docs exist. This is good.
- The operational risk is local-secret sprawl: multiple scripts read the same application password from local env files, and some docs name exact credential paths. Future agents must avoid printing those values.
- Authenticated WordPress writes are properly guarded in the main connector and local-draft creator, but one-off publisher scripts still exist and should be retired or clearly marked single-use.

### CI/CD and Deployment

- `test-pr.yml` runs useful checks, and PHP validation now uses the repo-owned Composer/PHPCS path. Remaining CI debt: JS lint/tests are skipped without `package.json`, and Trivy still uses `@master`.
- At audit time, `sync-projects.yml` was a placeholder workflow with write permissions and issue/PR triggers. The Phase 0 kickoff parked it as a manual read-only diagnostic stub.
- At audit time, `auto-triage.yml` told users that `auto-implement` would start the parked agent swarm. The Phase 0 kickoff changed that message to focused routing guidance.
- Theme deployment is manual and cache-sensitive; there is no package manifest/checksum/release checklist that ties a zip to a git commit.

### Testing and Reliability

- `make test` now covers the Notion publisher tests and the sidebar plugin smoke test.
- The most important live safety checks are report-style scripts (`morning_truth_report.py`, `check_current_state_drift.py`, `wp7-public-smoke.py`). They are valuable but can run long because nested smoke checks multiply endpoint timeouts.
- There is no automated browser/mobile/a11y/performance gate for Aurora, despite open issues depending on those properties.

### Type Safety and Validation

- Python scripts use dataclasses and explicit boundaries in newer places, but the main connector is a 980-line CLI doing config, Notion IO, image download, conversion, WP media upload, taxonomy resolution, write safety, and artifact writing.
- PHP plugin code validates admin settings and escapes output reasonably, but no Composer/WPCS baseline exists in-repo.
- JavaScript is vanilla and readable, but untyped and unlinted; failures in animation loading can directly affect visibility.

### Observability and Operations

- `make morning-truth` is the strongest operational primitive. It captures GitHub queue truth, live WP smoke, draft counts, drift checks, and worktree risk.
- Observability is mostly manual/read-only. There is no scheduled report artifact in this repo for Core Web Vitals, uptime, contact-form delivery, broken image scans, or cache purge verification.
- Pagely cache behavior is a repeated source of ambiguity. REST edits do not auto-purge, and verification must use cache-busted reads.

### Documentation Quality

- Documentation is unusually rich and helpful, but volume is now a debt vector. There are 126 non-backup top-level docs/current-state-adjacent files and 362 tracked markdown files overall.
- The current front door is good (`AGENTS.md`, current-state README, handoffs, morning-truth reports), but older docs and issue templates still contain stale domain examples and automation claims.
- The root cause of doc debt is rapid agent iteration: every session wrote a handoff or audit, but fewer sessions retired or consolidated the preceding surfaces.

### Maintainability Hotspots

- `scripts/notion-to-wp/kk_notion_to_wp.py` is the main god module. It is critical, tested around high-risk guards, and should not be rewritten, but should be split along stable boundaries.
- `theme/kk-aurora/style.css` is 2,543 lines and `theme.json` is 839 lines. That is not automatically bad for a WP theme, but without linting, component ownership, and visual regression checks it becomes fragile.
- `theme/kk-aurora/assets/js/aurora-animations.js` and `micro-interactions.js` overlap in interaction responsibility.
- Single-use publishing scripts (`publish_dc_protest_draft.py`, `publish_you_cant_drink_data.py`) are operational liabilities once their posts are done.

## Prioritized Work Plan

### Phase 0 — Immediate Containment

**Goals**

- Make the repo safer for the next agent without touching production.
- Remove misleading automation signals.
- Ensure every default command tells the truth.

**High-impact tasks**

- Keep the sidebar promo smoke test wired into `make test`.
- Keep bounded timeout/fail-fast behavior in `make morning-truth` and its nested smoke calls.
- Keep `auto-triage.yml` aligned with the current reality: labels are triage hints only.
- Keep `sync-projects.yml` parked until it actually syncs Projects.
- Expand `make verify` when the next stable gate is ready; today it runs local tests and docs truth.
- Mark one-off publish scripts as archived or move them under `scripts/notion-to-wp/archive/`.
- Record the current untracked startup artifacts and decide what should be tracked vs local-only.

**Expected outcomes**

- Agents stop trusting labels/workflows that no longer do real work.
- Local validation matches the repo's actual risk profile.
- Morning startup remains useful but stops surprising operators with long silent runs.

### Phase 1 — Stabilization

**Goals**

- Standardize tooling and reduce environment-specific failures.
- Harden the live-write and deploy paths.
- Establish minimum confidence for theme/content/plugin changes.

**High-impact tasks**

- Maintain the repo-owned PHP tooling (`composer.json`, `composer.lock`, and focused `phpcs.xml.dist`) and broaden only with intentional cleanup PRs.
- Pin Python dependencies with a lock or constraints file and document one setup path.
- Add a small Node toolchain only if it earns its keep: eslint/prettier for `theme/kk-aurora/assets/js` and optional stylelint for theme CSS.
- Create a theme release checklist: version, zip path, checksum, git commit, upload step, cache purge step, cache-busted verification URLs, rollback zip.
- Create a REST content change checklist: snapshot path, page ID/slug, dry-run/diff, POST, cache purge, readback.
- Add direct tests for `wp7-public-smoke.py` and `check_current_state_drift.py` parsing behavior so the truth tools are not trusted only by convention.
- Add a secret-scan command that outputs findings without printing values.

**Expected outcomes**

- Validation failures become actionable instead of machine-specific.
- Theme and REST deployment stop relying on memory of prior incidents.
- The repo has a single "green enough to proceed" command.

### Phase 2 — Standardization

**Goals**

- Reduce architectural drift in Aurora and content operations.
- Make docs and issues reflect the current operating model.
- Keep useful evidence while deleting stale affordances.

**High-impact tasks**

- Consolidate Aurora template ownership: preserve global templates, convert Services-style legacy templates to DB content when editability matters, and document exceptions.
- Build a page-content component contract for Aurora classes so REST-authored pages reuse known classes without inventing new inline CSS every time.
- Queue-hygiene pass: remove or re-label stale `auto-implement` issues, close superseded design issues only with evidence, and split broad platform/archive issues into scoped deliverables.
- Consolidate current-state docs into a small front door plus dated archive. Do not delete incident reports, raw evidence, rollback snapshots, or morning-truth reports.
- Replace external proof-image hotlinks with media-library assets and record ownership/alt text.
- Decide whether `kk-sidebar-promos` is a real productized plugin or a parked experiment; if real, give it install/deploy docs and CI coverage.

**Expected outcomes**

- Future agents can see what is deployable, what is evidence, and what is history.
- Aurora work becomes less template-by-template improvisation.
- The GitHub queue becomes an execution queue, not an archaeological layer.

### Phase 3 — Refactoring & Optimization

**Goals**

- Simplify critical modules without breaking working flows.
- Improve performance, accessibility, and operational confidence.
- Retire complexity that does not justify its cost.

**High-impact tasks**

- Split `kk_notion_to_wp.py` into stable modules: config, Notion client, WP client, image pipeline, artifact writers, CLI orchestration. Keep behavior and tests intact.
- Add a `--diff` mode before update writes, as already identified after the overwrite incident.
- Prune Aurora motion: keep visibility-safe, reduced-motion-safe interactions; remove or self-host GSAP/ScrollTrigger only if the measured benefit beats vanilla IntersectionObserver/CSS alternatives.
- Introduce targeted browser/a11y/performance verification for Aurora: homepage, blog archive, single post, Work, Speaking, mobile nav, and one generic content page.
- Convert plugin smoke tests to PHPUnit only if the plugin is moving toward deployment; otherwise keep the lightweight smoke but wire it into default tests.
- Add recurring read-only operational reports for contact-form delivery, broken images/media hotlinks, WP version/plugin fingerprint, and Core Web Vitals/Lighthouse snapshots.

**Expected outcomes**

- The highest-risk code becomes easier to change.
- Visual polish no longer threatens page visibility or performance.
- Operations become boring, inspectable, and repeatable.

## Quick Wins

- Keep `php plugins/kk-sidebar-promos/tests/smoke.php` wired into `make test`.
- Keep timeout controls around slow public smoke commands.
- Keep `auto-triage.yml` from promising parked swarm behavior.
- Keep `sync-projects.yml` as manual/read-only until real project sync is implemented.
- Keep the root Composer/PHPCS setup green.
- Add `scripts/notion-to-wp/archive/` for completed one-off publishers.
- Add a `make verify` command with local-only, read-only defaults.
- Add a theme zip release note template with commit, checksum, and rollback.
- Update issue templates still showing `kk.ca` placeholders to `kriskrug.co`.
- Add a short "current deploy paths" table to the root README that points to the two-track model and handoff.

## Anti-Rewrite Guidance

Leave untouched unless there is a direct task:

- The current two-track model and current-state front door.
- The hardened connector safety semantics: create-first, slug lookup, explicit `--update`, title similarity guard, post-write readback.
- Incident reports, raw evidence, rollback snapshots, and morning-truth reports.
- Working Aurora production source on `main`; do not merge old `aurora/v2` broadly.
- Pagely/Jetpack/Redirection production behavior unless a task has rollback and verification.

Incrementally improve:

- `kk_notion_to_wp.py`: split by responsibility only after tests lock behavior.
- Aurora CSS/JS: prune and standardize component by component, measured against real pages.
- Current-state docs: consolidate indexes and mark historical surfaces rather than deleting evidence.
- GitHub issue labels: normalize gradually while preserving useful routing history.

Prefer simplification over expansion:

- Do not rebuild the old agent swarm until there is a real operator need.
- Do not add a headless frontend or new framework just to escape WordPress complexity.
- Do not turn every page into a theme template; content pages should stay editable DB content by default.
- Do not add dependencies for formatting/linting unless they become part of default verification.

## Monday Morning Checklist

1. Run the startup truth set:
   - `git fetch --prune`
   - `git status --short --branch`
   - `make morning-truth`
   - `make test`
   - `php plugins/kk-sidebar-promos/tests/smoke.php`
   - `make docs-truth-check`
   - `make validate`
2. Commit or deliberately ignore generated morning-truth reports and known local-only scripts; do not leave mystery untracked files.
3. Confirm `make test` includes the plugin smoke test.
4. Confirm `auto-triage.yml` and `sync-projects.yml` still do not imply inactive automation.
5. Run `composer install` if `vendor/bin/phpcs` is missing, then run `make validate`.
6. Add fail-fast timeouts to morning-truth nested public smoke checks.
7. Move completed one-off publishing scripts into an archive folder or add a clear "single-use, do not run" header.
8. Open a small queue-hygiene PR: stale `auto-implement` label language, issue templates using `kk.ca`, and README deploy-path pointers.
9. For Aurora, do not start with visual redesign. Start with ownership cleanup: identify templates that should remain global vs content pages that should be REST-managed.
10. For production changes, always attach the rollback path, cache-purge step, and cache-busted verification URL before touching live WordPress.

## Final Guidance

The long-term engineering philosophy for this repo should be: make the boring path the default path. Keep WordPress as the production system of record, keep `main` as the canonical theme/content-ops truth, and use this repo to make risky operations reversible, observable, and repeatable. Stabilize by deleting misleading automation, standardizing verification, and narrowing ownership boundaries. Refactor only where repeated work proves the abstraction has earned its cost.
