# Documentation Index

Navigation for everything in this repo. Entries are grouped by what they're for, not by file path.

> **Agents start here:** [`/AGENTS.md`](../AGENTS.md) — then come back to this index.

---

## 🟢 Current State And Dated Evidence

The canonical baseline snapshot and current handoffs live in [`docs/current-state/`](current-state/). The May 14 files are frozen evidence; use the newest dated closeout plus the latest `make status-readonly` or `make morning-truth` output as the startup front door.

| File | What it covers |
|---|---|
| [`current-state/README.md`](current-state/README.md) | Index of the baseline snapshot |
| [`current-state/TWO-TRACK-MODEL.md`](current-state/TWO-TRACK-MODEL.md) | Active Track A / Track B decision rule, with the 2026-05-29 branch-model update marking `aurora/v2` as historical and `aurora/v3-reconcile` as evidence only |
| [`current-state/REPO_STATE.md`](current-state/REPO_STATE.md) | What's actually checked in vs. just documented |
| [`current-state/SITE_INVENTORY.md`](current-state/SITE_INVENTORY.md) | Live-site fingerprint: host, theme, plugins, content shape |
| [`current-state/ACCESS_CHANNELS.md`](current-state/ACCESS_CHANNELS.md) | MCP / REST / Chrome / SSH — what works today |
| [`current-state/BACKUP_PLAN.md`](current-state/BACKUP_PLAN.md) | The four pieces of a real WP backup and how to get them |
| [`current-state/ROLLBACK_PLAYBOOK.md`](current-state/ROLLBACK_PLAYBOOK.md) | Order of operations if a prod change breaks |
| [`current-state/SEO_AUDIT.md`](current-state/SEO_AUDIT.md) | Technical SEO + AI search readiness |
| [`current-state/CONTENT_AUDIT.md`](current-state/CONTENT_AUDIT.md) | Per-page review + post inventory + IA proposal |
| [`current-state/FIX_QUEUE.md`](current-state/FIX_QUEUE.md) | P0 → P3 backlog |
| [`current-state/ROADMAP.md`](current-state/ROADMAP.md) | Six-phase, 3-month plan; use as longer-range reference after the latest work plan |
| [`current-state/WORK-PLAN-2026-07-01.md`](current-state/WORK-PLAN-2026-07-01.md) | **Active weekly plan** (rest of week). Live PR/issue readback + execution lanes; supersedes `WORK-PLAN-2026-05-23.md` |
| [`current-state/CONTENT-ARCHITECTURE-RESET-2026-07-01.md`](current-state/CONTENT-ARCHITECTURE-RESET-2026-07-01.md) | Trust + Offers and Topic Hubs content architecture waves: fifteen live page migrations, snapshots, verification, and next-wave boundaries |
| [`current-state/AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md`](current-state/AURORA-READABILITY-RESET-CLOSEOUT-2026-07-01.md) | Aurora 1.3.27 readability reset live closeout, test evidence, blockers, and next Track B roadmap |
| [`current-state/FULL-AUDIT-ROADMAP-2026-05-18.md`](current-state/FULL-AUDIT-ROADMAP-2026-05-18.md) | May 18 post-closeout audit, roadmap, and human decision list |
| [`current-state/HANDOFF-2026-05-24.md`](current-state/HANDOFF-2026-05-24.md) | Current cross-track state (Aurora/theme/content truth, deployment mechanics, open work) |
| [`current-state/AURORA-V3-QA-ROADMAP-2026-05-24.md`](current-state/AURORA-V3-QA-ROADMAP-2026-05-24.md) | Current Aurora v1.3.0 QA and rollout truth for Track B |
| [`current-state/TRACK-A-MORNING-TRUTH-2026-05-24.md`](current-state/TRACK-A-MORNING-TRUTH-2026-05-24.md) | Current Track A startup truth and verification command surface, last normalized against `reports/morning-truth-20260525-021945Z.md` |
| [`current-state/reports/morning-truth-20260703-175742Z.md`](current-state/reports/morning-truth-20260703-175742Z.md) | Newest packaged `make morning-truth` artifact: `0` open PRs, `27` open issues, WP `6.9.4`, and draft queue/drift readback |
| [`current-state/reports/`](current-state/reports/) | Timestamped `make morning-truth` outputs; newest packaged file is the most recent immutable truth artifact |
| [`current-state/WORK-PLAN-2026-05-23.md`](current-state/WORK-PLAN-2026-05-23.md) | Historical baseline plan; keep for context only |
| [`current-state/DIAGNOSTIC-POLISH-2026-05-20.md`](current-state/DIAGNOSTIC-POLISH-2026-05-20.md) | Repo-truth, technical-debt, SOTA, live-fix, and workflow diagnostic |
| [`current-state/FIXES-LIVE-RECONCILIATION-2026-05-20.md`](current-state/FIXES-LIVE-RECONCILIATION-2026-05-20.md) | Current disposition of `fixes/` artifacts against live evidence |
| [`current-state/AURORA-MOTION-GOVERNANCE-2026-05-20.md`](current-state/AURORA-MOTION-GOVERNANCE-2026-05-20.md) | Motion budget and QA rules for Aurora |
| [`current-state/TOMORROW-ROADMAP-2026-05-20.md`](current-state/TOMORROW-ROADMAP-2026-05-20.md) | Historical next-session roadmap after rewrite recovery and branch/worktree cleanup |
| [`current-state/WORK-PLAN-2026-05-20.md`](current-state/WORK-PLAN-2026-05-20.md) | Historical execution plan after Wave 3 completion and Track B QA setup |
| [`current-state/NEXT-ROUND-WORK-2026-05-19.md`](current-state/NEXT-ROUND-WORK-2026-05-19.md) | Historical command sheet from 2026-05-19 (superseded by 2026-05-20 roadmap/work-plan docs) |
| [`current-state/ISSUE-SWARM-ROADMAP-2026-05-19.md`](current-state/ISSUE-SWARM-ROADMAP-2026-05-19.md) | 72-hour swarm roadmap with bounded parallel lanes, wave labels, and stop rules |
| [`current-state/AURORA-ISSUE-SWARM-2026-05-19.md`](current-state/AURORA-ISSUE-SWARM-2026-05-19.md) | Filed Aurora epics and routed stale design issues into the Track B lane |
| [`current-state/CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md`](current-state/CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md) | Redacted history-scan findings and safe rewrite/force-push preflight |
| [`current-state/CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md`](current-state/CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md) | Execution log of the rewrite, force-updated branches, and post-rewrite recovery steps |
| [`current-state/GITHUB-QUEUE-RECOVERY-2026-05-19.md`](current-state/GITHUB-QUEUE-RECOVERY-2026-05-19.md) | Queue recovery after rewrite: replacement PRs, CI gate fix, merges, and cleanup |
| [`current-state/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md`](current-state/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md) | Current agent-swarm lanes and execution order |
| [`current-state/SWARM-STATUS-2026-05-18.md`](current-state/SWARM-STATUS-2026-05-18.md) | Current command-desk status after the first bounded swarm |
| [`current-state/DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md`](current-state/DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md) | Next-batch Notion inventory and local dry-run packs |
| [`current-state/NEXT-PUBLISHING-PLAN-2026-05-18.md`](current-state/NEXT-PUBLISHING-PLAN-2026-05-18.md) | Security gate, live-post verification, and ranked next publishing plan |
| [`current-state/POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md`](current-state/POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md) | Read-only audit of public posts, local draft packs, and issue lanes after the overwrite incident |
| [`current-state/TRACK-A-QUICK-FIX-PACK-2026-05-18.md`](current-state/TRACK-A-QUICK-FIX-PACK-2026-05-18.md) | Production-safe current-site quick-fix pack |
| [`current-state/NAV-IA-DECISION-PACK-2026-05-18.md`](current-state/NAV-IA-DECISION-PACK-2026-05-18.md) | Navigation and IA decision pack |
| [`current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`](current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md) | Aurora visual redesign audit, benchmark frame, and Track B issue rollout map |
| [`current-state/AURORA-STAGING-REPORT-2026-05-18.md`](current-state/AURORA-STAGING-REPORT-2026-05-18.md) | Local Aurora smoke results and current redesign blocker |
| [`current-state/SITE-AUDIT-2026-05-16.md`](current-state/SITE-AUDIT-2026-05-16.md) | Reader-facing site audit (Track A punch-list) |
| [`current-state/POST-ENRICHMENT-2026-05-16.md`](current-state/POST-ENRICHMENT-2026-05-16.md) | Post-enrichment pass + connector rules |
| [`current-state/TRAFFIC-DIAGNOSTIC-2026-05-15.md`](current-state/TRAFFIC-DIAGNOSTIC-2026-05-15.md) | GSC / traffic dive |
| [`current-state/AURORA-MIGRATION-PLAN.md`](current-state/AURORA-MIGRATION-PLAN.md) | Track B migration plan |
| [`current-state/INCIDENT-2026-05-15-overwritten-post.md`](current-state/INCIDENT-2026-05-15-overwritten-post.md) | Postmortem + safety rules every agent follows |

## 🟢 Current — content & code references

| File | What it covers |
|---|---|
| [`../scripts/notion-to-wp/README.md`](../scripts/notion-to-wp/README.md) | Notion → WP publisher: setup, dry-run, safety guards |
| [`../content/source-packs/content-architecture-2026/README.md`](../content/source-packs/content-architecture-2026/README.md) | Content architecture source pack and body-only WordPress payloads for Trust + Offers and Topic Hubs |
| [`kris-krug-roles-module.md`](kris-krug-roles-module.md) | KK's role-switching framework (voice / tone reference) |
| [`archive-content-mine.md`](archive-content-mine.md) | 20-year blog-archive content mine (2003–2026): bio/credential threads + "from the archives" content backlog, with source links |
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

**Last updated:** 2026-07-03. Added the latest morning-truth artifact. Note: this index does not exhaustively list every dated file under `docs/current-state/` - the June/July 2026 snapshots and closeouts are newer than some entries here, so treat `docs/current-state/` itself as the source of truth for the latest dated evidence. Update this index whenever you add or remove documentation, or whenever a doc's "Current vs Historical" status changes.
