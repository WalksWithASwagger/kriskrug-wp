# Repo State — `kriskrug-wp/`

**Baseline date:** 2026-05-14.
**Latest reconciliation:** 2026-05-20. Read dated addenda in this folder for current handoffs, especially `DIAGNOSTIC-POLISH-2026-05-20.md`.

This repo was set up earlier in 2026 as an **issue tracking + automation hub** for kriskrug.co, not as a code mirror of the WordPress install. As of today the repo and the live site share almost no files.

## What's actually checked in (built, not just documented)

### Repo-side WordPress code

| Path | What it is | Status |
|---|---|---|
| `inc/digital-composting.php` | Custom Post Type + Taxonomy module for ingesting transcripts ("digital composting") | Merged via PR #71 + #72 on 2026-05-07. **Not yet deployed to production.** |
| `plugins/kk-sidebar-promos/` | Packaged helper plugin for auto-expiring sidebar promos, evergreen pillar cards, and Luma iCal import | Built in May 2026. **Do not deploy until backup/rollback proof is current.** |

### Prepared fixes and live-state reconciliation (`fixes/`)

`fixes/` is a staging area for ready-to-paste snippets, content packs, and migration notes tied to GitHub issues. It is no longer accurate to say that none have reached production: `owned-sites-network-rollout.md` documents applied page/widget/menu content, and public HTML on key pages now appears to include the schema path represented by `schema-snippets-deployed.php`.

Use `FIXES-LIVE-RECONCILIATION-2026-05-20.md` before deploying anything from `fixes/`. Several January files are now historical or superseded.

| File | Tied to | Type |
|---|---|---|
| `issue-5-color-contrast.css` | #5 | CSS |
| `issue-9-button-hover-states.css` | #9 | CSS |
| `issue-12-new-homepage-hero.md` | #12 | Content |
| `issue-13-14-15-project-sections.md` | #13/14/15 | Content |
| `issue-22-land-acknowledgment.md` | #22 | Content |
| `issue-36-meta-descriptions.md` | #36 | SEO content |
| `issue-37-xml-sitemap-setup.md` | #37 | SEO config |
| `issue-39-schema-markup.php` | #39 | PHP snippet |
| `issue-43-twitter-cards.php` | #43 | PHP snippet |
| `issue-67-services-page-expanded.md` | #67 | Content |
| `issue-68-work-page-complete.md` | #68 | Content |
| `UPDATED-ABOUT-PAGE-COMPLETE.md` | About | Content |
| `README-FIXES-BATCH-1.md` | — | Index |
| `llms-txt-template.md` | P0.2 | AI search |
| `robots-txt-update.txt` | P0.4 | Robots / AI crawler policy |
| `schema-snippets.php` | P0.3 | Future mu-plugin schema path |
| `schema-snippets-deployed.php` | P0.3 | Code Snippets production schema source |
| `owned-sites-network-rollout.md` | Owned-sites IA | Applied production record |

### Agent swarm and workflows (`.github/agents/` + `.github/workflows/`)

A historical 10-agent hierarchical automation system for converting GitHub issues into PRs:
- **Workflow agents:** orchestrator, analyzer, test-writer, implementer, qa, reviewer, pr-creator
- **Doc swarm:** content-analyzer, readme-writer, link-validator
- **Workflows:** `test-pr` remains active PR validation. `agent-pr-generator` is parked as a manual, read-only diagnostic stub as of 2026-05-20. Older swarm docs remain for reference.
- **Per-issue state:** `.github/agent-state/<issue>/state.json` exists for 12 historical issues (2, 4, 5, 12, 22, 34, 41, 57, 60, 66, 70, 99). Treat these as evidence records, not live automation state.

> The old system produced PRs #71 and #72, but it is not the current implementation path. Do not add `auto-implement` expecting autonomous PR creation unless the swarm is rebuilt intentionally.

### Skills (`skills/`)

| Skill | Purpose |
|---|---|
| `github-workflow-automation/` | Helpers for batch-creating issues, generating PRs from issues, validating WordPress code. Includes `validate_wordpress.sh`, `gh_health_check.sh`, `run_tests.sh`. |

### Documentation (`docs/`)

Substantial documentation, written before the modification work begins:

| File | Topic |
|---|---|
| `architecture.md` | 17K — full agent swarm architecture |
| `automation-guide.md` | 10K — how to use the automation |
| `cloudways-setup.md` | 11K — dev server setup (the dev server, not Pagely production) |
| `local-development-setup.md` | 17K — Local by Flywheel or Docker workflow |
| `vision.md` | 7K — what the site is for |
| `roadmap.md` | 10K — planned work |
| `INDEX.md` | 8K — docs index |
| `FIRST-AGENT-SUCCESS.md` | 8K — agent debut report |
| `testing-results.md` | 10K — test outputs |
| `kris-krug-roles-module.md` | 7K — KK roles module guide (newest, May 8) |

### Issue batches queued for filing (`issues-to-create/`)

| File | Batch |
|---|---|
| `batch-1-critical-bugs.json` | Critical bugs |
| `batch-2-content-positioning.json` | Content/positioning |
| `batch-3-4-all-remaining.json` | Everything else |
| `batch-marketing-archives-portal.json` | Marketing archives portal |
| `content-extraction-updates.json` | Content extraction updates |

## What is **NOT** in this repo

Everything that would constitute a backup of the live site:

- ❌ The active **theme** (`catch-responsive`) source files
- ❌ Any **child theme** customizations
- ❌ Installed **plugins** (Jetpack, Popup Maker, Zero BS CRM, Site Kit, Akismet…)
- ❌ The **database** (posts, pages, options, users, comments, plugin data)
- ❌ The **uploads/** media library
- ❌ `wp-config.php`
- ❌ Any `.htaccess` / Pagely config overrides
- ❌ mu-plugins, drop-ins

> **Implication:** if a modification to production goes wrong and we don't have an off-site Pagely backup, this repo cannot restore the site. That's what `BACKUP_PLAN.md` exists to solve.

## Recent commit activity

```
fc339da  docs: add Kris Krug roles module guide                 (2026-05-08)
9cb65dc  chore: simplify .gitignore                              (2026-05-08)
56e3aab  Merge PR #72  (transcript composting)                    (2026-05-07)
df77d7f  feat: implement enhanced digital composting module       (2026-05-07)
99618db  Merge PR #71                                              (~2026-05-07)
5a4930e  feat: implement digital composting transcript module
1e2c3fb  Add Batch 2 fixes: Services and Work pages complete
7995db6  Complete Batch 1: 12 kriskrug.co fixes ready for deployment
0f10b77  Add Batch 1 fixes: 12 issues solved
9672d86  Initial commit                                            (2026-01)
```

Cadence: heavy setup work in January, dormant Feb-April, picked back up in early May. Since 2026-05-18, commit activity has been mostly documentation and content-pack work, with smaller code hardening passes.

## How to interpret older docs

Older docs may describe the agent swarm as "infrastructure complete" or mention `kk.ca`. Treat that as historical. The production URL is `kriskrug.co`, the old autonomous swarm is parked, and current work should follow the two-track model plus the dated handoff docs in `docs/current-state/`.
