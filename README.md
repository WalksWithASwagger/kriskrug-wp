# Kris Krug WordPress Site - Issue Tracking & Automation

> Building a Responsible & Inclusive AI Future for British Columbia

[![Infrastructure](https://img.shields.io/badge/Infrastructure-Complete-success)](https://github.com/WalksWithASwagger/kk-wp)
[![Agent Swarm](https://img.shields.io/badge/Agent%20Swarm-Validated-success)](https://github.com/WalksWithASwagger/kk-wp/tree/main/.github/agents)
[![Status](https://img.shields.io/badge/Status-Awaiting%20Production-blue)](https://kriskrug.co)

**Status:** Infrastructure complete and validated. Agent swarm proven operational. Awaiting production kriskrug.co import to begin real issue resolution.

This repository serves as the issue tracking, project management, and automation hub for the **Kris Krug** WordPress website at [kriskrug.co](https://kriskrug.co/).

## About Kris Krug

Kris Krug is a grassroots AI ecosystem initiative focused on building a responsible and inclusive AI future for British Columbia. Our community brings together:

- AI enthusiasts and professionals
- Policy makers and educators
- Artists and creative technologists
- Local community organizers
- Technology innovators

### Key Initiatives

- **Regional Hubs** - Hyperlocal AI community building
- **AI Film Club** - Exploring AI through cinema
- **Mind/AI/Consciousness** - Philosophical discussions
- **Events & Workshops** - Community learning opportunities
- **Resource Directory** - Funding, hackathons, and tools

## Repository Purpose

This repository is used for:

1. **Site audits + state snapshots** of the live kriskrug.co WordPress install
2. **Content pipeline** — Notion → kriskrug.co publisher with safety guards
3. **Custom WordPress code** — schema markup, theme tweaks, helper plugins
4. **Issue tracking + project management** for fixes, content, and automation
5. **AI agent automation** — automated issue-to-PR workflows (older — not used in current sessions)

### Why a Separate Repo?

The live WordPress site is not file-synced with this repo (it runs on Pagely). This repo holds everything *adjacent* to the site: audit data, draft content before publication, deployment-ready code snippets, and runbooks. See [Project Structure](#project-structure) for the layout.

## Project Structure

```
content/drafts/                  # Notion-derived post drafts before publication
  └── YYYY-MM-DD-<slug>/         # post.md, post.html, images/, seo-meta.md, etc.

scripts/notion-to-wp/            # Notion → kriskrug.co publisher
  ├── kk_notion_to_wp.py         # Single-file CLI: fetch, convert, upload, publish
  ├── block_rules.py             # Notion block → Gutenberg block mapping
  └── README.md                  # Setup + safety notes

fixes/                           # Production-ready code snippets / migrations
  ├── schema-snippets.php        # JSON-LD (Person + WebSite + Article + Breadcrumb + Service)
  ├── schema-snippets-deployed.php  # The version actually running on prod
  ├── llms-txt-template.md       # Curated llms.txt for AI search
  ├── robots-txt-update.txt      # Two AI-crawler stance options
  └── issue-*.{css,php,md}       # Older queued fixes from earlier batches

docs/current-state/              # Frozen baseline snapshot — what was true on 2026-05-14
  ├── README.md                  # Index of the snapshot
  ├── SITE_INVENTORY.md          # Live-site fingerprint: host, theme, plugins, content shape
  ├── REPO_STATE.md              # What's actually built vs. just documented
  ├── ACCESS_CHANNELS.md         # MCP / REST / Chrome / SSH — what works today
  ├── BACKUP_PLAN.md             # The four pieces of a real WP backup + paths to get them
  ├── ROLLBACK_PLAYBOOK.md       # If a change breaks prod, here's the order of operations
  ├── SEO_AUDIT.md               # Technical SEO + on-page + AI/generative-search readiness
  ├── CONTENT_AUDIT.md           # Per-page review of all 34 pages + recent post inventory
  ├── FIX_QUEUE.md               # P0 → P3 backlog
  ├── ROADMAP.md                 # Where this is heading next
  ├── INCIDENT-2026-05-15-overwritten-post.md   # Postmortem for the connector overwrite
  └── raw/                       # Underlying API/HTML evidence behind the audit

issues-to-create/                # Markdown drafts of GitHub issues waiting to be filed

inc/                             # Custom WordPress modules (e.g., digital-composting CPT)

skills/                          # Claude Code skills used in this repo
.github/                         # Agent swarm definitions + workflows (older pipeline)
```

### Where to start

- **Reading the site state:** `docs/current-state/README.md`
- **Planning next work:** `docs/current-state/ROADMAP.md` and `FIX_QUEUE.md`
- **Publishing a Notion post:** `scripts/notion-to-wp/README.md`
- **Filing an issue:** `issues-to-create/` for drafts; existing ones at [WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues)

## 🤖 Agent Swarm - Infrastructure Complete ✅

**Validation Status:** Proven operational through proof-of-concept testing

**What was validated:**
- ✅ Complete agent pipeline (7 specialized agents)
- ✅ Autonomous code generation (944 lines generated during testing)
- ✅ GitHub Actions workflows functional
- ✅ Cloudways development environment configured
- ✅ Ready for production kriskrug.co issues

**Current Phase:** Awaiting production WordPress import

This repository includes production-ready AI agent automation:

### Agent Swarm Pipeline

```
GitHub Issue → Analyzer → Test Writer → Implementer → QA → Reviewer → PR Creator
```

**7 Specialized Agents:**
1. **Orchestrator** - Coordinates the entire pipeline
2. **Analyzer** - Parses issues and creates technical specifications
3. **Test Writer** - Writes tests before implementation (TDD)
4. **Implementer** - Writes WordPress-compliant code
5. **QA** - Runs automated tests and validation
6. **Reviewer** - Code review with best practices checks
7. **PR Creator** - Generates comprehensive pull requests

### Automated Workflows

- **Auto-triage** - Automatically labels and categorizes issues
- **Agent PR Generator** - Converts issues to pull requests automatically
- **Test Validation** - Runs WordPress coding standards and tests
- **Project Sync** - Keeps project boards updated

## Getting Started

### For Contributors

1. Browse [open issues](https://github.com/WalksWithASwagger/kk-wp/issues)
2. Read our [Contributing Guidelines](CONTRIBUTING.md)
3. Use issue templates when creating new issues
4. Follow WordPress coding standards for code contributions

### For Maintainers

See our [automation documentation](docs/automation-guide.md) for:
- Setting up the agent swarm
- Using gh CLI extensions
- Configuring workflows
- Managing the pipeline

## Technology Stack

- **Platform**: WordPress
- **Automation**: GitHub Actions + Claude AI Agents
- **CLI Tools**: GitHub CLI (gh), Claude Code
- **Testing**: PHPUnit, WordPress Coding Standards (PHPCS)
- **Language**: PHP, JavaScript, Bash, Python

## Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `accessibility` - WCAG compliance and a11y improvements
- `performance` - Speed and optimization
- `seo` - Search engine optimization
- `content` - Content updates and UX
- `documentation` - Documentation improvements
- `auto-implement` - Ready for agent automation
- `needs-human-review` - Requires manual review

## Project Links

- **Live Site**: [kriskrug.co](https://kriskrug.co/)
- **Events**: [Luma Calendar](https://lu.ma/kk)
- **News**: Updates via Notion
- **GitHub**: [WalksWithASwagger/kk-wp](https://github.com/WalksWithASwagger/kk-wp)

## Contact

For questions about this repository or Kris Krug:

- Create an issue in this repository
- Visit [kriskrug.co](https://kriskrug.co/) for general inquiries
- Join our community events

## License

This repository is for project management and automation purposes. WordPress core and third-party plugins/themes maintain their respective licenses.

---

**Powered by AI Agent Automation** - This repository uses Claude AI agents to automatically convert issues into pull requests with full test coverage.
