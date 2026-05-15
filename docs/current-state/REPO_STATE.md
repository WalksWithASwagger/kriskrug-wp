# Repo State — `kriskrug-wp/` as of 2026-05-14

This repo was set up earlier in 2026 as an **issue tracking + automation hub** for kriskrug.co, not as a code mirror of the WordPress install. As of today the repo and the live site share almost no files.

## What's actually checked in (built, not just documented)

### PHP modules — exactly one

| Path | What it is | Status |
|---|---|---|
| `inc/digital-composting.php` | Custom Post Type + Taxonomy module for ingesting transcripts ("digital composting") | Merged via PR #71 + #72 on 2026-05-07. **Not yet deployed to production.** |

### Prepared but undeployed fixes (`fixes/`)

A staging area of 12 ready-to-paste solutions tied to specific GitHub issues. **None of these have been applied to production.**

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

### Agent swarm (`.github/agents/` + `.github/workflows/`)

A 10-agent hierarchical automation system for converting GitHub issues into PRs:
- **Workflow agents:** orchestrator, analyzer, test-writer, implementer, qa, reviewer, pr-creator
- **Doc swarm:** content-analyzer, readme-writer, link-validator
- **Workflows:** `auto-triage`, `agent-pr-generator`, `sync-projects`, `test-pr`, `reusable-wordpress-validation`
- **Per-issue state:** `.github/agent-state/<issue>/state.json` exists for 11 issues (2, 4, 5, 12, 22, 34, 41, 57, 60, 66, 70)

> The system is described as "Infrastructure complete, Agent swarm validated, awaiting production import" in the README. It has produced PRs (#71, #72 most recently) but the bulk of issues haven't been processed.

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

Cadence: heavy setup work in January, dormant Feb–April, picked back up in early May.

## How to interpret the README

The repo's `README.md` says: *"Status: Infrastructure complete and validated. Agent swarm proven operational. Awaiting production kk.ca import to begin real issue resolution."*

That status is accurate. **"Production import"** = importing the live site into a local dev environment so the agent swarm has something to operate against. That hasn't happened yet, which is why everything in `fixes/` is staged but undeployed.

The README also references the site as **`kk.ca`** in several places. The actual production URL is **`kriskrug.co`**. Likely a historical naming the docs haven't caught up to — flag for a sweep later.
