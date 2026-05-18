# Documentation Index

Navigation for everything in this repo. Entries are grouped by what they're for, not by file path.

> **Agents start here:** [`/AGENTS.md`](../AGENTS.md) — then come back to this index.

---

## 🟢 Current — read these first

The canonical "what's true right now" snapshot lives in [`docs/current-state/`](current-state/). Written May 14–17, 2026.

| File | What it covers |
|---|---|
| [`current-state/README.md`](current-state/README.md) | Index of the baseline snapshot |
| [`current-state/TWO-TRACK-MODEL.md`](current-state/TWO-TRACK-MODEL.md) | Active operating model — Track A (content/SEO) vs Track B (Aurora theme) |
| [`current-state/REPO_STATE.md`](current-state/REPO_STATE.md) | What's actually checked in vs. just documented |
| [`current-state/SITE_INVENTORY.md`](current-state/SITE_INVENTORY.md) | Live-site fingerprint: host, theme, plugins, content shape |
| [`current-state/ACCESS_CHANNELS.md`](current-state/ACCESS_CHANNELS.md) | MCP / REST / Chrome / SSH — what works today |
| [`current-state/BACKUP_PLAN.md`](current-state/BACKUP_PLAN.md) | The four pieces of a real WP backup and how to get them |
| [`current-state/ROLLBACK_PLAYBOOK.md`](current-state/ROLLBACK_PLAYBOOK.md) | Order of operations if a prod change breaks |
| [`current-state/SEO_AUDIT.md`](current-state/SEO_AUDIT.md) | Technical SEO + AI search readiness |
| [`current-state/CONTENT_AUDIT.md`](current-state/CONTENT_AUDIT.md) | Per-page review + post inventory + IA proposal |
| [`current-state/FIX_QUEUE.md`](current-state/FIX_QUEUE.md) | P0 → P3 backlog |
| [`current-state/ROADMAP.md`](current-state/ROADMAP.md) | Six-phase, 3-month plan |
| [`current-state/SITE-AUDIT-2026-05-16.md`](current-state/SITE-AUDIT-2026-05-16.md) | Reader-facing site audit (Track A punch-list) |
| [`current-state/POST-ENRICHMENT-2026-05-16.md`](current-state/POST-ENRICHMENT-2026-05-16.md) | Post-enrichment pass + connector rules |
| [`current-state/TRAFFIC-DIAGNOSTIC-2026-05-15.md`](current-state/TRAFFIC-DIAGNOSTIC-2026-05-15.md) | GSC / traffic dive |
| [`current-state/AURORA-MIGRATION-PLAN.md`](current-state/AURORA-MIGRATION-PLAN.md) | Track B migration plan |
| [`current-state/INCIDENT-2026-05-15-overwritten-post.md`](current-state/INCIDENT-2026-05-15-overwritten-post.md) | Postmortem + safety rules every agent follows |

## 🟢 Current — content & code references

| File | What it covers |
|---|---|
| [`../scripts/notion-to-wp/README.md`](../scripts/notion-to-wp/README.md) | Notion → WP publisher: setup, dry-run, safety guards |
| [`kris-krug-roles-module.md`](kris-krug-roles-module.md) | KK's role-switching framework (voice / tone reference) |
| [`../.claude/context/project-context.md`](../.claude/context/project-context.md) | Mission, values, audience, voice |
| [`../.claude/agents-vibe.md`](../.claude/agents-vibe.md) | Agent philosophy & community values |
| [`../.claude/naming-conventions.md`](../.claude/naming-conventions.md) | Code naming standards |
| [`../.claude/common-failures.md`](../.claude/common-failures.md) | Known failure patterns to avoid |
| [`../skills/github-workflow-automation/SKILL.md`](../skills/github-workflow-automation/SKILL.md) | Batch issue creation + PR helpers |

## 🟢 Current — entry points & contribution

| File | What it covers |
|---|---|
| [`../README.md`](../README.md) | Project overview |
| [`../AGENTS.md`](../AGENTS.md) | Agent orientation — read first if you're an LLM |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute (human + agent) |

---

## 🟡 Historical — reference only, may drift

These were written in the era-1 push (Jan–early May 2026) when the plan was "GitHub Actions agent swarm runs against a Cloudways-imported clone of production". That plan was superseded by the two-track model in May 2026. These docs still have architectural and reference value but **do not describe how work happens today**.

| File | What it was for |
|---|---|
| [`architecture.md`](architecture.md) | Architecture of the dormant GitHub Actions agent swarm |
| [`automation-guide.md`](automation-guide.md) | How to operate the dormant swarm |
| [`vision.md`](vision.md) | Long-term vision (3–5 years) from era 1 |
| [`roadmap.md`](roadmap.md) | Superseded by [`current-state/ROADMAP.md`](current-state/ROADMAP.md) |
| [`cloudways-setup.md`](cloudways-setup.md) | Cloudways dev-server setup. Relevant if/when Track B needs staging |
| [`local-development-setup.md`](local-development-setup.md) | Local WordPress with Flywheel/Docker. Relevant if/when Track B needs local |
| [`../.claude/context/wordpress-setup.md`](../.claude/context/wordpress-setup.md) | Cloudways WP config; **not** the prod config |
| [`../fixes/README-FIXES-BATCH-1.md`](../fixes/README-FIXES-BATCH-1.md) | Index of the original Batch 1 fixes |
| [`../.github/agents/`](../.github/agents/) | 10 agent definitions (orchestrator + workflow + doc-swarm) for the dormant pipeline |

Each historical doc carries a `STATUS: Historical` banner at the top pointing at its current replacement (if one exists).

---

## 📂 Other directories worth knowing

| Path | What's there |
|---|---|
| [`../content/drafts/`](../content/drafts/) | Notion-derived post drafts before publication |
| [`../fixes/`](../fixes/) | Production-ready code snippets + per-issue fix proposals |
| [`../inc/`](../inc/) | Custom WordPress modules (currently: `digital-composting.php`) |
| [`../issues-to-create/`](../issues-to-create/) | Markdown drafts of GitHub issues waiting to be filed |
| [`../backup/`](../backup/) | Backup manifests (archives themselves are gitignored) |
| [`../skills/`](../skills/) | Claude Code skills used by this repo |
| [`../.github/`](../.github/) | Workflows, agent definitions, issue templates |

---

**Last updated:** 2026-05-17. Update this index whenever you add or remove documentation, or whenever a doc's "Current vs Historical" status changes.
