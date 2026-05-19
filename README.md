# kriskrug-wp — Operations Hub for kriskrug.co

> Building a Responsible & Inclusive AI Future for British Columbia

**Live site:** [kriskrug.co](https://kriskrug.co/) (Pagely-hosted WordPress, Catch Responsive theme)
**Repo:** [WalksWithASwagger/kriskrug-wp](https://github.com/WalksWithASwagger/kriskrug-wp)
**Operating model:** Two tracks — see [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md)

This repository is the **operations + content hub** for [kriskrug.co](https://kriskrug.co/). The live WordPress install is not file-synced here (it runs on Pagely). This repo holds everything *adjacent* to the site: audit snapshots, draft content before publication, deployment-ready code snippets, and the Notion → WordPress publisher.

**If you're an AI agent landing in this repo cold, start at [`AGENTS.md`](AGENTS.md).**

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

1. **Site audits + state snapshots** of the live kriskrug.co WordPress install (see [`docs/current-state/`](docs/current-state/))
2. **Content pipeline** — Notion → kriskrug.co publisher with safety guards (see [`scripts/notion-to-wp/`](scripts/notion-to-wp/))
3. **Custom WordPress code** — schema markup, theme tweaks, helper plugins (see [`fixes/`](fixes/) and [`inc/`](inc/))
4. **Aurora v2 theme work** — separate `aurora/v2` branch, paced sprints (see [`docs/current-state/AURORA-MIGRATION-PLAN.md`](docs/current-state/AURORA-MIGRATION-PLAN.md))
5. **Issue tracking + project management** for fixes, content, and theme work

### Why a Separate Repo?

The live WordPress site is not file-synced with this repo (it runs on Pagely). This repo holds everything *adjacent* to the site: audit data, draft content before publication, deployment-ready code snippets, and runbooks. See [Project Structure](#project-structure) for the layout.

## Project Structure

```
content/drafts/                  # Notion-derived post drafts before publication
  └── YYYY-MM-DD-<slug>/         # post.md, post.html, images/, seo-meta.md, etc.

content/source-packs/            # Curated source packs for page/content overhauls
  └── keynotes-2026/             # Speaking/Work/About payloads and source notes for issue #76

backup/                          # Manifests and page-level rollback snapshots; archives are ignored
  └── YYYYMMDD-HHMMSS/           # Small REST/HTML snapshots used for targeted rollback

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
  ├── FULL-AUDIT-ROADMAP-2026-05-18.md # Current queue audit + next roadmap
  ├── INCIDENT-2026-05-15-overwritten-post.md   # Postmortem for the connector overwrite
  └── raw/                       # Underlying API/HTML evidence behind the audit

issues-to-create/                # Markdown drafts of GitHub issues waiting to be filed

inc/                             # Custom WordPress modules (e.g., digital-composting CPT)

skills/                          # Claude Code skills used in this repo
.github/                         # Agent swarm definitions + workflows (older pipeline)
```

### Where to start

- **Reading the site state:** `docs/current-state/README.md`
- **Planning next work:** `docs/current-state/FULL-AUDIT-ROADMAP-2026-05-18.md`, then `docs/current-state/ROADMAP.md` and `FIX_QUEUE.md`
- **Publishing a Notion post:** `scripts/notion-to-wp/README.md`
- **Reviewing staged drafts:** `content/drafts/README.md`
- **Filing an issue:** `issues-to-create/` for drafts; existing ones at [WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues)

## How work happens here

Two parallel tracks. Pick one per session — don't mix.

### Track A — Content + SEO (on `main`, weekly cadence)

Notion → kriskrug.co publishing, post-publish enrichment, schema maintenance, alt-text batches, category sweeps, GSC + sitemap health.

- Publish a post: [`scripts/notion-to-wp/README.md`](scripts/notion-to-wp/README.md)
- Enrichment + link-graph helper: [`scripts/notion-to-wp/text_polish.py`](scripts/notion-to-wp/text_polish.py)
- Active backlog: [`docs/current-state/FIX_QUEUE.md`](docs/current-state/FIX_QUEUE.md), [`docs/current-state/SITE-AUDIT-2026-05-16.md`](docs/current-state/SITE-AUDIT-2026-05-16.md)
- Deployed schema: [`fixes/schema-snippets-deployed.php`](fixes/schema-snippets-deployed.php)

### Track B — Aurora v2 theme migration (on `aurora/v2`, paced sprints)

FSE theme rebuild on a separate branch. Touches `theme/`, FSE templates, theme.json. Never touches post content.

- Migration plan: [`docs/current-state/AURORA-MIGRATION-PLAN.md`](docs/current-state/AURORA-MIGRATION-PLAN.md)

### Which track am I in?

See the decision rule in [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md#how-to-know-which-track-youre-in). If you're editing a post, page, schema, redirect, or category → Track A. If you're editing theme files or FSE templates → Track B.

## Getting Started

### For agents
Start at [`AGENTS.md`](AGENTS.md), then read [`docs/current-state/README.md`](docs/current-state/README.md).

### For human contributors
1. Browse [open issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues)
2. Read [`CONTRIBUTING.md`](CONTRIBUTING.md)
3. Use issue templates when filing new issues
4. Follow WordPress coding standards for PHP/JS in `fixes/` and `inc/`

### Dormant: GitHub Actions agent swarm
`.github/agents/` and `.github/workflows/` define an older issue-to-PR pipeline (orchestrator → analyzer → test-writer → implementer → QA → reviewer → PR creator). It produced PRs #71 and #72 in May 2026 and is not used by current sessions. See [`docs/architecture.md`](docs/architecture.md) and [`docs/automation-guide.md`](docs/automation-guide.md) for reference if/when it's revived.

## Technology Stack

- **Platform:** WordPress 6.9+ on Pagely (production), Catch Responsive theme
- **Content pipeline:** Python (Notion API → WordPress REST API)
- **Custom code:** PHP snippets (Code Snippets plugin on prod), one custom module (`inc/digital-composting.php`)
- **CLI Tools:** GitHub CLI (`gh`), Claude Code / Cursor agents
- **Languages:** PHP, JavaScript, Python, Bash

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

- **Live Site:** [kriskrug.co](https://kriskrug.co/)
- **Events:** [Luma Calendar](https://lu.ma/kk)
- **GitHub:** [WalksWithASwagger/kriskrug-wp](https://github.com/WalksWithASwagger/kriskrug-wp)
- **Issues:** [github.com/WalksWithASwagger/kriskrug-wp/issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues)

## Contact

For questions about this repository or Kris Krug:

- Create an issue in this repository
- Visit [kriskrug.co](https://kriskrug.co/) for general inquiries
- Join our community events

## License

This repository is for project management, content publishing, and theme development. WordPress core and third-party plugins/themes maintain their respective licenses.
