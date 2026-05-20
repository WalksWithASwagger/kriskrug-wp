# Current State of kriskrug.co — Baseline Snapshot

**Snapshot date:** 2026-05-14
**Purpose:** Document the live site, the repo, the access channels, and the rollback paths *before* we start making modifications. If we break something, this is what we return to.

This folder is the source of truth for "what was true on May 14, 2026" and for dated working addenda that came out of the May 2026 recovery/redesign push. Treat the baseline files as historical snapshots and the dated `2026-05-*` files as current handoff material.

## Files in this folder

| File | What it covers |
|---|---|
| [SITE_INVENTORY.md](SITE_INVENTORY.md) | Live site fingerprint: host, WP version, theme, plugins, content shape, users, integrations. |
| [REPO_STATE.md](REPO_STATE.md) | What's actually in this repo (vs. what's planned). Cleanly separates "checked in" from "documented but not built." |
| [ACCESS_CHANNELS.md](ACCESS_CHANNELS.md) | Every way we can reach the site today (MCP, REST, browser, SSH-when-ready) and what's blocked. |
| [BACKUP_PLAN.md](BACKUP_PLAN.md) | The four pieces of a full WP backup, which we have, which we don't, and the staged plan to get them. |
| [ROLLBACK_PLAYBOOK.md](ROLLBACK_PLAYBOOK.md) | If a change breaks production, here's the order of operations to undo it. |
| [SEO_AUDIT.md](SEO_AUDIT.md) | Technical SEO + on-page + AI/generative-search readiness, with specific findings. |
| [CONTENT_AUDIT.md](CONTENT_AUDIT.md) | Per-page review of all 34 pages, posts inventory (101 recent), taxonomy, multilingual, IA proposal. |
| [FIX_QUEUE.md](FIX_QUEUE.md) | Prioritized P0→P3 backlog from both audits. |
| [ROADMAP.md](ROADMAP.md) | Six-phase, 3-month plan that synthesizes FIX_QUEUE + postmortem follow-ups + content pipeline next steps. **Start here.** |
| [FULL-AUDIT-ROADMAP-2026-05-18.md](FULL-AUDIT-ROADMAP-2026-05-18.md) | Current post-closeout audit of repo, GitHub queue, Track A, Track B, and human decisions. |
| [TOMORROW-ROADMAP-2026-05-20.md](TOMORROW-ROADMAP-2026-05-20.md) | Refreshed next-session roadmap after rewrite recovery, branch hygiene follow-through, and worktree reconciliation. |
| [WORK-PLAN-2026-05-20.md](WORK-PLAN-2026-05-20.md) | Current execution plan after Wave 3 implementation completion and final Track B QA gate (`#86`). |
| [NEXT-ROUND-WORK-2026-05-19.md](NEXT-ROUND-WORK-2026-05-19.md) | Historical 2026-05-19 handoff sheet (superseded by the 2026-05-20 roadmap/work-plan docs). |
| [ISSUE-SWARM-ROADMAP-2026-05-19.md](ISSUE-SWARM-ROADMAP-2026-05-19.md) | 72-hour swarm-ready issue roadmap with parallel lanes, stop rules, and wave labels. |
| [AURORA-ISSUE-SWARM-2026-05-19.md](AURORA-ISSUE-SWARM-2026-05-19.md) | Filed Aurora epics #80-#86 and routed old design issues #24-#35. |
| [AURORA-SOTA-ROADMAP-2026-05-20.md](AURORA-SOTA-ROADMAP-2026-05-20.md) | Summer-2026 state-of-the-art benchmark and feature roadmap for Aurora Track B. |
| [CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md](CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md) | Redacted history-scan findings and safe force-push preflight; no rewrite performed. |
| [CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md](CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md) | Execution log for the credential history rewrite, affected branch force-updates, and post-rewrite follow-ups. |
| [GITHUB-QUEUE-RECOVERY-2026-05-19.md](GITHUB-QUEUE-RECOVERY-2026-05-19.md) | Queue recovery log for replacement PRs #87/#88, CI fix, and post-rewrite branch cleanup. |
| [GITHUB-QUEUE-SWEEP-2026-05-18.md](GITHUB-QUEUE-SWEEP-2026-05-18.md) | PR, branch, and issue classification after the GitHub queue sweep. |
| [AGENT-SWARM-OPERATING-PLAN-2026-05-18.md](AGENT-SWARM-OPERATING-PLAN-2026-05-18.md) | Current swarm lanes across GitHub issues, draft publishing, Aurora, and content/nav structure. |
| [SWARM-STATUS-2026-05-18.md](SWARM-STATUS-2026-05-18.md) | Current command-desk status after the first bounded issue/content/Aurora swarm. |
| [DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md](DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md) | Next-batch Notion inventory and local dry-run packs. |
| [NEXT-PUBLISHING-PLAN-2026-05-18.md](NEXT-PUBLISHING-PLAN-2026-05-18.md) | Security gate, live-post verification, and ranked next publishing plan. |
| [POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md](POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md) | Read-only audit of public posts, local draft packs, and issue lanes after the overwrite incident. |
| [TRACK-A-QUICK-FIX-PACK-2026-05-18.md](TRACK-A-QUICK-FIX-PACK-2026-05-18.md) | Production-safe snippets, commands, checks, and rollback notes for current-site fixes. |
| [TRACK-A-SEO-SOCIAL-PREP-2026-05-18.md](TRACK-A-SEO-SOCIAL-PREP-2026-05-18.md) | Prep notes for issues #36 and #43 covering Jetpack-owned SEO/social metadata, verification, and deployment cautions. |
| [INTERNAL-LINKING-STRATEGY-2026-05-18.md](INTERNAL-LINKING-STRATEGY-2026-05-18.md) | Report-only strategy artifact for issue #38. |
| [NAV-IA-DECISION-PACK-2026-05-18.md](NAV-IA-DECISION-PACK-2026-05-18.md) | Navigation and IA decisions for current theme and Aurora. |
| [OWNED-SITES-LINKING-RECOMMENDATION-2026-05-18.md](OWNED-SITES-LINKING-RECOMMENDATION-2026-05-18.md) | Where to place KK's related AI sites across About, Work, Speaking, sidebar/footer, and nav. |
| [AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md](AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md) | Track B visual redesign audit, 2026 benchmark frame, media/motion direction, and issue rollout map. |
| [AURORA-STAGING-REPORT-2026-05-18.md](AURORA-STAGING-REPORT-2026-05-18.md) | Local Aurora smoke results and the current redesign blocker. |
| [INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md) | Postmortem for the connector overwrite incident on 2026-05-15. Lessons + safety guards. |
| `raw/` | Raw API snapshots + HTML fetches: `wp-json/`, `pages.json`, `posts-page1.json`, fingerprint HTML for 16 pages, sitemaps, robots — the underlying evidence behind the other files. |

## Active source packs outside this folder

| Path | What it covers |
|---|---|
| [`../../content/source-packs/keynotes-2026/README.md`](../../content/source-packs/keynotes-2026/README.md) | Curated source pack and publish-ready payloads for issue #76, the Speaking/Work/About page overhaul. |
| [`../../backup/20260518-111546/page-snapshots/`](../../backup/20260518-111546/page-snapshots/) | Page-level REST/HTML rollback snapshots for the issue #76 target pages. |
| [`../../backup/20260518-113350/page-snapshots/`](../../backup/20260518-113350/page-snapshots/) | Verified post-deploy rollback snapshots and Redirection export for issue #76. |
| [`../../backup/20260518-215912/page-snapshots/`](../../backup/20260518-215912/page-snapshots/) | Speaking page rollback snapshot before the Horizons proof update. |
| [`../../backup/20260518-223014/page-snapshots/`](../../backup/20260518-223014/page-snapshots/) | Page-level rollback snapshots before the IA-polish continuation. |
| [`../../backup/20260518-224340/page-snapshots/`](../../backup/20260518-224340/page-snapshots/) | About page rollback snapshot before the final proof-list/interlink pass. |

## Ready-to-paste fix snippets (in `../../../fixes/`)

| File | Fix item |
|---|---|
| `fixes/llms-txt-template.md` | Curated `llms.txt` content for site root (P0.2). |
| `fixes/robots-txt-update.txt` | Two robots.txt options with explicit AI-crawler stances (P0.4). |
| `fixes/schema-snippets.php` | Mu-plugin: `Person`, `WebSite`, `Article`, `BreadcrumbList`, `Service` JSON-LD (P0.3). Supersedes the older `issue-39-schema-markup.php`. |

## TL;DR

- **Site is on Pagely** (managed WP host), running **WordPress 6.9.4** with the **Catch Responsive** classic theme.
- **Jetpack is on the Free plan**, which is why WordPress.com MCP write access is currently blocked.
- **Baseline note:** the May 14 snapshot started before later page-level snapshots, source packs, and Aurora theme work were added. Read the dated addenda above for current operating state.
- **Read-only fingerprinting works** through the public WP REST API; that's how this snapshot was built.
- **Path to "safe to modify":** get SSH on Pagely → take a `wp db export` + `wp-content/` archive → commit a `backup/` reference set → then start modifying.
