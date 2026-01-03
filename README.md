# Kris Krug WordPress Site - Issue Tracking & Automation

> Building a Responsible & Inclusive AI Future for British Columbia

[![Infrastructure](https://img.shields.io/badge/Infrastructure-Complete-success)](https://github.com/WalksWithASwagger/kk-wp)
[![Agent Swarm](https://img.shields.io/badge/Agent%20Swarm-Validated-success)](https://github.com/WalksWithASwagger/kk-wp/tree/main/.github/agents)
[![Status](https://img.shields.io/badge/Status-Awaiting%20Production-blue)](https://kk.ca)

**Status:** Infrastructure complete and validated. Agent swarm proven operational. Awaiting production kk.ca import to begin real issue resolution.

This repository serves as the issue tracking, project management, and automation hub for the **Kris Krug** WordPress website at [kk.ca](https://kk.ca/).

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

1. **Issue Tracking** - Bugs, feature requests, enhancements for kk.ca
2. **Project Management** - Organizing development tasks and priorities
3. **AI Agent Automation** - Automated issue-to-PR workflows powered by Claude agents
4. **Documentation** - Technical documentation and development guidelines

### Why a Separate Repo?

The live WordPress site is not currently synced with version control. This repository allows us to:

- Track issues and feature requests systematically
- Build AI-powered automation for website improvements
- Document development processes
- Test agent-driven development workflows
- Eventually sync with WordPress custom themes/plugins

## 🤖 Agent Swarm - Infrastructure Complete ✅

**Validation Status:** Proven operational through proof-of-concept testing

**What was validated:**
- ✅ Complete agent pipeline (7 specialized agents)
- ✅ Autonomous code generation (944 lines generated during testing)
- ✅ GitHub Actions workflows functional
- ✅ Cloudways development environment configured
- ✅ Ready for production kk.ca issues

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

- **Live Site**: [kk.ca](https://kk.ca/)
- **Events**: [Luma Calendar](https://lu.ma/kk)
- **News**: Updates via Notion
- **GitHub**: [WalksWithASwagger/kk-wp](https://github.com/WalksWithASwagger/kk-wp)

## Contact

For questions about this repository or Kris Krug:

- Create an issue in this repository
- Visit [kk.ca](https://kk.ca/) for general inquiries
- Join our community events

## License

This repository is for project management and automation purposes. WordPress core and third-party plugins/themes maintain their respective licenses.

---

**Powered by AI Agent Automation** - This repository uses Claude AI agents to automatically convert issues into pull requests with full test coverage.
