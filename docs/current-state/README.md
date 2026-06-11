# Current State of kriskrug.co — Baseline Snapshot

**Snapshot date:** 2026-05-14
**Purpose:** Document the live site, the repo, the access channels, and the rollback paths *before* we start making modifications. If we break something, this is what we return to.

This folder is the source of truth for "what was true on May 14, 2026" and for dated working addenda that came out of the May 2026 recovery/redesign push. Treat the baseline files as historical snapshots and the latest dated handoff/truth docs plus the newest committed `reports/morning-truth-*.md` artifact as the current front door.

## Current Front Door (verified 2026-06-11 via `make status-readonly`)

Read these first for current execution context:

1. [POST-SHIP-AUDIT-WORKPLAN-2026-06-04.md](POST-SHIP-AUDIT-WORKPLAN-2026-06-04.md), `reports/morning-truth-20260609-043246Z.md`, and the latest read-only startup truth from `make status-readonly`
2. [LOCAL-WP-QA-2026-06-04.md](LOCAL-WP-QA-2026-06-04.md)
3. [AURORA-ARTICLE-LUX-COMPOSITION-1.3.10-WORKPLAN-2026-06-03.md](AURORA-ARTICLE-LUX-COMPOSITION-1.3.10-WORKPLAN-2026-06-03.md)
4. [WORK-PAGE-METADATA-68-2026-06-04.md](WORK-PAGE-METADATA-68-2026-06-04.md)
5. [AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md](AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md)
6. [TRACK-A-RESTART-2026-05-31.md](TRACK-A-RESTART-2026-05-31.md)
7. [SHUTDOWN-2026-05-30.md](SHUTDOWN-2026-05-30.md)
8. [AURORA-CONTENT-RECOVERY-2026-05-25.md](AURORA-CONTENT-RECOVERY-2026-05-25.md)
9. [AURORA-LIVE-QA-2026-05-25.md](AURORA-LIVE-QA-2026-05-25.md)
10. [QUEUE-MERGE-CLEANUP-2026-05-26.md](QUEUE-MERGE-CLEANUP-2026-05-26.md)
11. [TRACK-A-SWARM-75-95-128-2026-05-29.md](TRACK-A-SWARM-75-95-128-2026-05-29.md)
12. [HANDOFF-2026-05-24.md](HANDOFF-2026-05-24.md)
13. [SESSION-HANDOFF-2026-05-24.md](SESSION-HANDOFF-2026-05-24.md)
14. [TRACK-A-MORNING-TRUTH-2026-05-24.md](TRACK-A-MORNING-TRUTH-2026-05-24.md)
15. [TWO-TRACK-MODEL.md](TWO-TRACK-MODEL.md)
16. [INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md)

Side-worktree safety refresh (2026-06-02): canonical new work should start from
`main` in a fresh lane-scoped branch. Do not edit
`/Users/kk/Code/kriskrug-wp-aurora-keynote`
(`codex/aurora-keynote-redesign`),
`/Users/kk/Code/kriskrug-wp-aurora-reconcile` (`aurora/v3-reconcile`), or the
locked `/Users/kk/Code/kriskrug-wp/.claude/worktrees/agent-aec50fddbd7207f80`
(`aurora/v2`) directly. Treat those side worktrees as evidence or historical
branches unless a maintainer explicitly resumes one.

Then use historical plans for context:

- [WORK-PLAN-2026-05-23.md](WORK-PLAN-2026-05-23.md)
- [WORK-PLAN-2026-05-21.md](WORK-PLAN-2026-05-21.md)
- [WORK-PLAN-2026-05-20.md](WORK-PLAN-2026-05-20.md)

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
| [ROADMAP.md](ROADMAP.md) | Six-phase, 3-month plan that synthesizes FIX_QUEUE + postmortem follow-ups + content pipeline next steps. Use as longer-range reference after the latest work plan. |
| [FULL-AUDIT-ROADMAP-2026-05-18.md](FULL-AUDIT-ROADMAP-2026-05-18.md) | May 18 post-closeout audit of repo, GitHub queue, Track A, Track B, and human decisions. |
| [POST-SHIP-AUDIT-WORKPLAN-2026-06-04.md](POST-SHIP-AUDIT-WORKPLAN-2026-06-04.md) | Current post-ship audit and workplan after Aurora 1.3.10, Work metadata #68, open queue, draft audit, and ready/agent/block buckets. |
| [LOCAL-WP-QA-2026-06-04.md](LOCAL-WP-QA-2026-06-04.md) | Local WP QA path for Track B: `kriskrug-local.local:10003`, GraphQL startup, Local theme sync, and proof that `/blog/` plus a real article load with Aurora 1.3.11. |
| [HANDOFF-2026-05-24.md](HANDOFF-2026-05-24.md) | Authoritative cross-track state as of 2026-05-24 (Aurora live, branch divergence warning, deploy mechanics). |
| [AURORA-ARTICLE-LUX-COMPOSITION-1.3.10-WORKPLAN-2026-06-03.md](AURORA-ARTICLE-LUX-COMPOSITION-1.3.10-WORKPLAN-2026-06-03.md) | Aurora 1.3.10 article/blog composition closeout and next QA path. |
| [WORK-PAGE-METADATA-68-2026-06-04.md](WORK-PAGE-METADATA-68-2026-06-04.md) | Work page metadata and OG image closeout for issue #68, with remaining #126 social-debugger follow-up. |
| [AURORA-CONTENT-RECOVERY-2026-05-25.md](AURORA-CONTENT-RECOVERY-2026-05-25.md) | Recovery note for stale Aurora 1.3.0 production templates masking rich page content, plus the 1.3.3/1.3.4 deploy artifacts and verification markers. |
| [AURORA-LIVE-QA-2026-05-25.md](AURORA-LIVE-QA-2026-05-25.md) | Live QA closeout for the 1.3.3 recovery deploy and 1.3.4 polish pass, including desktop/mobile screenshot artifact paths and residual CDN notes. |
| [QUEUE-MERGE-CLEANUP-2026-05-26.md](QUEUE-MERGE-CLEANUP-2026-05-26.md) | GitHub PR, branch, worktree, and issue-comment closeout after merging the Aurora recovery, Cotton draft, modernization guardrails, and v3 IA rollout salvage lanes. |
| [AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md](AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md) | Aurora header wordmark closeout, 1.3.9 deploy package path, production readback, Jetpack Boost Critical CSS caveat, and preserved dirty-work inventory. |
| [TRACK-A-RESTART-2026-05-31.md](TRACK-A-RESTART-2026-05-31.md) | Read-only restart pass after shutdown: verification, May 31 morning truth, Jetpack feedback counts, and human-gated queue disposition. |
| [SHUTDOWN-2026-05-30.md](SHUTDOWN-2026-05-30.md) | End-of-day closeout for Cursor WordPress MCP helpers, verification results, open risks, and restart commands. |
| [TRACK-A-SWARM-75-95-128-2026-05-29.md](TRACK-A-SWARM-75-95-128-2026-05-29.md) | Public-safe closeout for issues #75, #95, and #128, including dependency-aware Notion tests, draft `11879` readback, and PII-safe Jetpack feedback audit guidance. |
| [SESSION-HANDOFF-2026-05-24.md](SESSION-HANDOFF-2026-05-24.md) | Track A/Track B lane handoff with ownership boundaries and public-surface updates. |
| [AURORA-V3-QA-ROADMAP-2026-05-24.md](AURORA-V3-QA-ROADMAP-2026-05-24.md) | Reconciled Aurora v1.3.0 line, local QA evidence, and post-merge rollout priorities. |
| [TRACK-A-MORNING-TRUTH-2026-05-24.md](TRACK-A-MORNING-TRUTH-2026-05-24.md) | Read-only truth memo with live evidence, drift flags, and verification matrix for safe next-session startup. |
| `reports/` | Timestamped outputs from `make morning-truth` (read-only startup truth reports). Newest committed artifact as of 2026-06-09: `morning-truth-20260609-043246Z.md`; refresh live counts with `make status-readonly` before acting. |
| [WORK-PLAN-2026-05-23.md](WORK-PLAN-2026-05-23.md) | Historical Track A baseline after the Sovereign AI draft pipeline closeout. Live-count declarations were refreshed from the 2026-06-11 `make status-readonly` truth pass; branch assumptions remain historical. |
| [WORK-PLAN-2026-05-21.md](WORK-PLAN-2026-05-21.md) | Historical next-session front door after the diagnostic/polish branch, docs tidy pass, and sidebar promo hardening. Superseded by `WORK-PLAN-2026-05-23.md`. |
| [DRAFT-QUALITY-RESET-2026-05-22.md](DRAFT-QUALITY-RESET-2026-05-22.md) | Active Track A publishing correction: live draft counts, why the May 21-22 drafts are not schedule-ready, and the required editorial/link/image/block QA gate. |
| [DRAFT-QUEUE-AUDIT-2026-05-22.md](DRAFT-QUEUE-AUDIT-2026-05-22.md) | Historical draft queue routing snapshot plus the Sovereign AI addendum (`11905`); re-run `make draft-queue-audit` for live counts. |
| [STORYHIVE-DRAFT-AUDIT-2026-05-22.md](STORYHIVE-DRAFT-AUDIT-2026-05-22.md) | Fine-toothed audit of the rebuilt StoryHive drafts, live WP readback, review-gate verification, and release roadmap. |
| [WP-7-UPGRADE-2026-05-22.md](WP-7-UPGRADE-2026-05-22.md) | Track A WordPress 7.0 staging-first upgrade runbook, smoke command, Pagely gate, rollback plan, and "AI connectors stay empty" rule. |
| [ISSUE-QUEUE-AUDIT-2026-05-22.md](ISSUE-QUEUE-AUDIT-2026-05-22.md) | Historical issue-routing snapshot from the 63-issue queue hygiene pass; re-run `gh issue list` for live counts. |
| [TOMORROW-ROADMAP-2026-05-20.md](TOMORROW-ROADMAP-2026-05-20.md) | Historical next-session roadmap after rewrite recovery, branch hygiene follow-through, and worktree reconciliation. Superseded by `WORK-PLAN-2026-05-21.md`. |
| [WORK-PLAN-2026-05-20.md](WORK-PLAN-2026-05-20.md) | Historical execution plan after Wave 3 implementation completion and final Track B QA gate (`#86`). Superseded by `WORK-PLAN-2026-05-21.md`. |
| [DIAGNOSTIC-POLISH-2026-05-20.md](DIAGNOSTIC-POLISH-2026-05-20.md) | Repository truth-refresh, technical-debt audit, SOTA direction, and polish/action checklist from the 2026-05-20 diagnostic pass. |
| [FIXES-LIVE-RECONCILIATION-2026-05-20.md](FIXES-LIVE-RECONCILIATION-2026-05-20.md) | Current disposition of every `fixes/` artifact against live-site evidence after schema/page updates. |
| [AURORA-MOTION-GOVERNANCE-2026-05-20.md](AURORA-MOTION-GOVERNANCE-2026-05-20.md) | Motion budget and QA rules for Aurora so visual polish does not degrade accessibility or Core Web Vitals. |
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
| `fixes/llms.txt` | Deployment-ready curated `llms.txt` content for site root (P0.2). |
| `fixes/llms-txt-template.md` | Deployment and rollback guide for `llms.txt` (P0.2). |
| `fixes/robots-txt-update.txt` | Two robots.txt options with explicit AI-crawler stances (P0.4). |
| `fixes/schema-snippets.php` | Mu-plugin: `Person`, `WebSite`, `Article`, `BreadcrumbList`, `Service` JSON-LD (P0.3). Supersedes the older `issue-39-schema-markup.php`. |
| `fixes/schema-snippets-deployed.php` | Production Code Snippets version. Public HTML appears to include this schema path as of 2026-05-20; verify in wp-admin before editing. |

## TL;DR

- **Site is on Pagely** (managed WP host), publicly reporting **WordPress 6.9.4** with **`kk-aurora` 1.3.10 active** as of the 2026-06-04 post-ship audit.
- **Jetpack is on the Free plan**, which is why WordPress.com MCP write access is currently blocked.
- **Baseline note:** the May 14 snapshot started before later page-level snapshots, source packs, and Aurora theme work were added. Read the dated addenda above for current operating state.
- **Current addendum:** start with the post-ship audit/workplan and newest morning-truth report, then use the Local WP QA note, Aurora 1.3.10 workplan, Work metadata closeout, Aurora logo closeout, and the 2026-05-24 handoff set ([`HANDOFF-2026-05-24.md`](HANDOFF-2026-05-24.md), [`AURORA-V3-QA-ROADMAP-2026-05-24.md`](AURORA-V3-QA-ROADMAP-2026-05-24.md), [`SESSION-HANDOFF-2026-05-24.md`](SESSION-HANDOFF-2026-05-24.md), [`TRACK-A-MORNING-TRUTH-2026-05-24.md`](TRACK-A-MORNING-TRUTH-2026-05-24.md)).
- **June 11 addendum:** PRs #205, #210, and #212 are merged, open PRs are `0`, open issues are `63` including #206-#208, production still reports WordPress `6.9.4`, and the draft queue is `0` future posts, `74` draft posts, and `5` draft pages via `make status-readonly`.
- **Follow-up addendum:** GSAP/CDN production drift remains tracked by #189/#204; Rafiki/content queue closeout is split across #206, #207, and #208; docs drift refresh #209 is closed.
- **WordPress 7.0 addendum:** production still publicly reports WordPress 6.9.4 as of 2026-06-11 20:09 UTC (`make status-readonly` / `make wp7-smoke EXPECT_VERSION=6.9.4`). Use [`WP-7-UPGRADE-2026-05-22.md`](WP-7-UPGRADE-2026-05-22.md), `make wp7-smoke`, and `make wp7-admin-readiness` before any staging or production upgrade.
- **Draft queue addendum:** `make status-readonly` reported `0` future posts, `74` draft posts, and `5` draft pages on 2026-06-11 20:09 UTC; `sovereign-ai-for-whom` is already WP draft `11905`.
- **Issue queue addendum:** `gh pr list --state open --limit 200` returned `0` open PRs after PR #212 merged, and `gh issue list --state open --limit 200` returned `63` open issues on 2026-06-11 20:40 UTC.
- **Read-only fingerprinting works** through the public WP REST API; that's how this snapshot was built.
- **Path to "safe to modify":** the strict backup/restore proof gate was retired on 2026-05-22. Use dry-runs, exact slug/ID/status checks, page/post snapshots or reversible diffs, and explicit rollback notes. Keep improving backup coverage as resilience, not as a blanket blocker.

## Verification Matrix (2026-06-11 20:09 UTC)

| Surface | Proof command / URL | Expected truth signal |
|---|---|---|
| Startup repo state | `make morning-truth` | Timestamped report under `docs/current-state/reports/` with git/issue/worktree snapshot. |
| `/projects/` route health (`#3`) | `curl -sI https://kriskrug.co/projects/` | Status line now returns `301` redirecting to the Work surface (`/recent-projects-include/`). |
| Work OG image (`#68`, `#126`) | `curl -sL "https://kriskrug.co/recent-projects-include/?cachebust=<ts>" \| rg -n "og:image"` | Cache-busted readback shows a non-blank OG image (latest truth pass resolved to the BC+AI ecosystem image). |
| Homepage reveal resilience (`#116` follow-through) | `curl -sL https://kriskrug.co/ \| rg -n "Aurora reveal safety net|gsap.min.js|ScrollTrigger.min.js"` | Safety-net marker is absent; GSAP/ScrollTrigger scripts are still CDN-loaded. |
| Queue truth | `gh pr list --state open --limit 100` and `gh issue list --state open --limit 200` | Snapshot values: `0` open PRs, `63` open issues including #206-#208. |
| Draft queue truth | `make status-readonly` or `make draft-queue-audit` | Snapshot values: `0` future posts, `74` draft posts, `5` draft pages. |
| WP version gate | `make wp7-smoke EXPECT_VERSION=6.9.4` | Public version check + key endpoint smoke pass. |
| Declared-vs-live drift | `make current-state-drift-check` | Flags mismatches between `WORK-PLAN-2026-05-23.md` declarations and live counts/version. |
| Aurora branch-model risk (read-only) | `git branch -r \| rg 'aurora/v[23]'` plus `git rev-list --left-right --count origin/main...origin/aurora/v3-reconcile` when a specific salvage is proposed | Confirms that `main` is the canonical Track B base and that `aurora/v2` / `aurora/v3-reconcile` are evidence branches, not wholesale merge targets. |
