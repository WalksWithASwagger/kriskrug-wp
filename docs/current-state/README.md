# Current State of kriskrug.co — Baseline Snapshot

**Snapshot date:** 2026-05-14
**Purpose:** Document the live site, the repo, the access channels, and the rollback paths *before* we start making modifications. If we break something, this is what we return to.

This folder is the source of truth for "what was true on May 14, 2026" — not a living document. Future changes go elsewhere; this stays frozen for reference.

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
| [INCIDENT-2026-05-15-overwritten-post.md](INCIDENT-2026-05-15-overwritten-post.md) | Postmortem for the connector overwrite incident on 2026-05-15. Lessons + safety guards. |
| `raw/` | Raw API snapshots + HTML fetches: `wp-json/`, `pages.json`, `posts-page1.json`, fingerprint HTML for 16 pages, sitemaps, robots — the underlying evidence behind the other files. |

## Ready-to-paste fix snippets (in `../../../fixes/`)

| File | Fix item |
|---|---|
| `fixes/llms-txt-template.md` | Curated `llms.txt` content for site root (P0.2). |
| `fixes/robots-txt-update.txt` | Two robots.txt options with explicit AI-crawler stances (P0.4). |
| `fixes/schema-snippets.php` | Mu-plugin: `Person`, `WebSite`, `Article`, `BreadcrumbList`, `Service` JSON-LD (P0.3). Supersedes the older `issue-39-schema-markup.php`. |

## TL;DR

- **Site is on Pagely** (managed WP host), running **WordPress 6.9.4** with the **Catch Responsive** classic theme.
- **Jetpack is on the Free plan**, which is why WordPress.com MCP write access is currently blocked.
- **We have no local backup yet.** The repo contains planning, automation tooling, and 12 prepared fixes — but zero theme code, plugin code, database, or media.
- **Read-only fingerprinting works** through the public WP REST API; that's how this snapshot was built.
- **Path to "safe to modify":** get SSH on Pagely → take a `wp db export` + `wp-content/` archive → commit a `backup/` reference set → then start modifying.
