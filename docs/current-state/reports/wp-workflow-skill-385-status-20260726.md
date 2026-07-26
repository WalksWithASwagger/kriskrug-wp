# #385 Status — Normalize WordPress workflow skill (2026-07-26)

**Mode:** docs / tooling hygiene only. No package move. No Makefile mutation. No production writes.  
**Branch:** `cursor/385-wp-skill-status-f196`  
**Issue:** [#385](https://github.com/WalksWithASwagger/kriskrug-wp/issues/385) — *Normalize the WordPress workflow skill without breaking automation*  
**Declared blocker:** [kk-agents#2](https://github.com/WalksWithASwagger/kk-agents/issues/2) — *Dynamic read-only skills doctor*  
**Work-plan note:** parked / low urgency in `WORK-PLAN-2026-07-25.md`

## Verdict

**Blocked on external tooling.** The in-repo package and hardcoded callers are fully inventoriable and an atomic move is feasible, but acceptance criteria require `skills-doctor --repo` (from kk-agents#2) to pass with no duplicate or broken-path findings. That binary and repo contract are **not available in this Cloud agent environment**, and `WalksWithASwagger/kk-agents` is **not readable** with the current GitHub token (404). Do **not** start the move PR until KK confirms kk-agents#2 is merged/available and skills-doctor is installable here.

## What the issue asks for

| Acceptance criterion | Local status |
|---|---|
| Move `github-workflow-automation` → `.agents/skills` (history preserved) | **Not started** — package still under legacy `skills/` |
| Relative Claude symlink adapter | **Not started** — no `.agents/` tree; no Claude skills symlink |
| Update every active Makefile + docs path | **Not started** — inventory below |
| No physical body left in legacy `skills/` or client mirrors | **N/A until move** — only one skill package exists under `skills/` |
| Validate frontmatter | **Present** — `SKILL.md` has `name` + `description` YAML |
| `skills-doctor --repo` passes | **Blocked** — tool absent; kk-agents#2 unreachable |
| Preserve workflow behavior | **Current paths still work** for `make validate` / `health` / `issues` / `pr` |

## In-repo vs external

### In-repo (kriskrug-wp)

Canonical package today:

```
skills/github-workflow-automation/
  SKILL.md
  references/batch-issues-guide.md
  scripts/
    batch_create_issues.py
    create_pr_from_issue.py
    gh_health_check.sh
    run_tests.sh
    validate_input.py
    validate_wordpress.sh   ← WordPress/PHPCS gate used by `make validate`
```

Notes:

- Issue title says “WordPress workflow skill”; the package name is **`github-workflow-automation`**. WordPress validation is one capability inside it (`validate_wordpress.sh`), also wired into `make verify` → `make validate`.
- `SKILL.md` references additional docs under `references/` (`wordpress-standards.md`, `pr-workflow-guide.md`, etc.) that are **not present** in-tree — only `batch-issues-guide.md` exists. Harmless for Makefile automation; frontmatter/doc completeness is a follow-up when the move lands.
- There is **no** `.agents/skills/` directory yet.
- There is **no** second physical copy / client mirror of this skill in-repo (`.claude/` holds context docs only, not a skill body).

### External (kk-agents + host tooling)

| Item | Observation (2026-07-26 Cloud probe) |
|---|---|
| `WalksWithASwagger/kk-agents` | API + HTML → **404 / Not Found** (private or outside token scope) |
| kk-agents#2 status | **Unknown** — cannot read issue body/state from this agent |
| `~/.agents/bin/skills-doctor` | **Absent** on this host |
| `skills-doctor` on `PATH` | **Absent** |
| Repo contract for discovery | Issue #385: “Do not mark ready without a repo contract” — contract lives outside this repo |

Issue #385 explicitly: *Dependency: Dynamic read-only skills doctor must be merged and available.*

## Hardcoded path inventory (must move atomically)

### Active automation (do not half-update)

| Location | Paths |
|---|---|
| `Makefile` | `validate`, `validate-fix`, `health`, `issues`, `issues-dry-run`, `pr`, `pr-draft`, `setup` — **9** invocations of `skills/github-workflow-automation/scripts/...` |
| `make verify` | Depends on `validate` → `validate_wordpress.sh` |

### Docs / indexes (update in same PR)

| Location | Role |
|---|---|
| `README.md` | Tree comment for `skills/` |
| `docs/INDEX.md` | Link to `SKILL.md` |
| `docs/architecture.md` | Path mention |
| `docs/automation-guide.md` | Example `validate_wordpress.sh --fix` |
| `docs/testing-results.md` | Historical command examples |
| `docs/local-development-setup.md` | Tree comment for `skills/` |
| `docs/current-state/REPO_STATE.md` | Skills table (banner may mark historical) |

### Dormant swarm (still hardcoded; update or leave intentionally stale)

| Location | Note |
|---|---|
| `.github/agents/qa.agent.md` | `validate_wordpress.sh` |
| `.github/agents/implementer.agent.md` | `validate_wordpress.sh --fix` |
| `.github/agent-config/error-handling.yml` | same |

AGENTS.md marks `.github/agents/` as historical / not used by current sessions — still update in the move PR to avoid broken-path findings from skills-doctor, unless the doctor excludes that tree by contract.

### Not skill-path blockers

- `scripts/notion-to-wp/README.md` mentions a *future* graduation to `skills/notion-to-wp/SKILL.md` — aspirational; different package.
- Content draft alt-text referring to “AI workflow skills” — editorial, unrelated.

## What can be done here vs blocked

| Action | Do now? |
|---|---|
| Document status + path inventory (this report) | **Yes** |
| Draft move checklist for a future PR | **Yes** (below) |
| Premature `git mv` to `.agents/skills` | **No** — fails AC without skills-doctor; risk breaking `make validate` if docs/Makefile lag |
| Install / run `skills-doctor --repo` | **Blocked** — external |
| Confirm kk-agents#2 merged | **Blocked** — repo not readable here |
| WP content / production / secrets / MCP | Out of scope per #385 |

### Future atomic PR checklist (when unblocked)

1. Confirm `~/.agents/bin/skills-doctor` (or contracted path) exists and understands `.agents/skills`.
2. Fresh worktree from `origin/main`.
3. `git mv skills/github-workflow-automation .agents/skills/github-workflow-automation` (history-preserving).
4. Add relative Claude symlink adapter per kk-agents contract (exact layout TBD from kk-agents#2).
5. Rewrite every active Makefile + docs + dormant agent path in the **same** commit/PR.
6. Ensure legacy `skills/` has no leftover body.
7. Gate: `skills-doctor --repo "$PWD"`, `make verify`, `git diff --check`.
8. Open **draft** PR; do not mark ready without the repo contract.

## Local impact if left alone

- **Day path unchanged.** `make validate` / `make verify` keep working via `skills/...`.
- **Hygiene debt only.** Canonical skills home is drifting toward `.agents/skills` elsewhere in KK’s agent stack; this repo stays on legacy `skills/` until the doctor lands.
- **No production / publisher impact.** Track A connector and Aurora theme are untouched.

## Recommended next step for KK

1. **Unblock externally:** merge (or confirm) [kk-agents#2](https://github.com/WalksWithASwagger/kk-agents/issues/2), publish the read-only `skills-doctor`, and note the install path for Cloud/laptop agents.
2. **Access:** if `kk-agents` is private, grant the Cloud agent / automation token read access so future lanes can verify the dependency instead of reporting 404.
3. **Then** authorize a single Track-B/tooling draft PR for #385 that moves the package + all hardcoded references together and runs the doctor + `make verify`.
4. Until then: keep #385 parked (low urgency). Prefer other swarm lanes; do not partial-path-rewrite Makefile.

## Verification performed this lane

- Read #385 body (open; dependency stated).
- Repo search for `github-workflow-automation`, `skills/`, `.agents/skills`, `skills-doctor`.
- Confirmed package tree under `skills/`; confirmed **no** `.agents/skills`.
- Confirmed `skills-doctor` binary absent on host.
- Confirmed `WalksWithASwagger/kk-agents` → 404 with current `gh` auth.
- No `make` target mutations; no skill move; no live WP calls required for this status doc.
