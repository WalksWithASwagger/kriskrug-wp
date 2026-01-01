# BC+AI Documentation Index

Complete navigation for all project documentation.

---

## 📖 Start Here

**New to the project?** Read these first:

1. **[PROJECT-SUMMARY.md](../PROJECT-SUMMARY.md)** - What this project is and how it works
2. **[QUICK-START.md](../QUICK-START.md)** - Get up and running in 5 minutes
3. **[README.md](../README.md)** - Project overview and features
4. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute

---

## 🏗️ Architecture & System Design

**Understanding how it all works:**

- **[architecture.md](architecture.md)** - Complete system architecture
- **[automation-guide.md](automation-guide.md)** - GitHub Actions workflows explained
- **[testing-results.md](testing-results.md)** - Validation and test results

**Agent swarm:**
- **[.github/agents/](../.github/agents/)** - All 7 agent definitions
  - `orchestrator.agent.md` - Pipeline coordinator
  - `analyzer.agent.md` - Issue analysis
  - `test-writer.agent.md` - TDD testing
  - `implementer.agent.md` - Code implementation
  - `qa.agent.md` - Quality assurance
  - `reviewer.agent.md` - Code review
  - `pr-creator.agent.md` - PR generation

---

## 🛠️ Development Setup

**Setting up your environment:**

- **[cloudways-setup.md](cloudways-setup.md)** - Cloudways server setup and SSH
- **[local-development-setup.md](local-development-setup.md)** - Local WordPress with Flywheel/Docker
- **[../.editorconfig](../.editorconfig)** - Code formatting standards
- **[../Makefile](../Makefile)** - Quick development commands

**WordPress-specific:**
- **[.claude/context/wordpress-setup.md](../.claude/context/wordpress-setup.md)** - Current WordPress configuration
- **[.claude/naming-conventions.md](../.claude/naming-conventions.md)** - Naming standards
- **[.claude/wordpress-patterns.md](../.claude/wordpress-patterns.md)** - Common code patterns (future)

---

## 🌲 BC+AI Context & Philosophy

**Understanding the mission:**

- **[.claude/context/project-context.md](../.claude/context/project-context.md)** - BC+AI mission, values, audience
- **[.claude/agents-vibe.md](../.claude/agents-vibe.md)** - Agent philosophy & community values
- **[vision.md](vision.md)** - Long-term vision (3-5 years)
- **[roadmap.md](roadmap.md)** - Development roadmap & priorities

---

## 🤖 Automation & Skills

**Custom automation tools:**

- **[skills/github-workflow-automation/SKILL.md](../skills/github-workflow-automation/SKILL.md)** - Skill documentation
- **[skills/github-workflow-automation/references/batch-issues-guide.md](../skills/github-workflow-automation/references/batch-issues-guide.md)** - JSON/CSV schemas

**Scripts:**
- `skills/github-workflow-automation/scripts/` - All 6 automation scripts
  - `batch_create_issues.py` - Batch issue creation
  - `create_pr_from_issue.py` - PR automation
  - `validate_wordpress.sh` - PHPCS validation
  - `run_tests.sh` - Test execution
  - `validate_input.py` - Input validation
  - `gh_health_check.sh` - System health

---

## 🔧 Configuration Files

**Project configuration:**

- **[.gitignore](../.gitignore)** - Git ignore rules (WordPress-specific)
- **[.editorconfig](../.editorconfig)** - Code formatting (tabs/spaces)
- **[Makefile](../Makefile)** - Development commands
- **[.github/agent-config/error-handling.yml](../.github/agent-config/error-handling.yml)** - Error handling & retries

**GitHub configuration:**
- **[.github/ISSUE_TEMPLATE/](../.github/ISSUE_TEMPLATE/)** - 5 issue templates
- **[.github/pull_request_template.md](../.github/pull_request_template.md)** - PR template
- **[.github/workflows/](../.github/workflows/)** - 5 GitHub Actions workflows

---

## 📚 Reference Documentation

**Learning & patterns:**

- **[.claude/common-failures.md](../.claude/common-failures.md)** - Common errors & solutions
- **[.claude/naming-conventions.md](../.claude/naming-conventions.md)** - Code naming standards
- **[.github/agent-state/README.md](../.github/agent-state/README.md)** - State management guide

**WordPress resources:**
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [WordPress Plugin Handbook](https://developer.wordpress.org/plugins/)
- [WP-CLI Commands](https://developer.wordpress.org/cli/commands/)

---

## 🎯 By Task

### I Want To...

**...understand the project**
→ Read: `PROJECT-SUMMARY.md`, then `README.md`

**...contribute code**
→ Read: `CONTRIBUTING.md`, then `QUICK-START.md`

**...understand the automation**
→ Read: `docs/automation-guide.md`, then `docs/architecture.md`

**...set up development environment**
→ Read: `docs/cloudways-setup.md` or `docs/local-development-setup.md`

**...understand BC+AI's mission**
→ Read: `.claude/context/project-context.md`, then `docs/vision.md`

**...create issues**
→ Use templates: `.github/ISSUE_TEMPLATE/`

**...understand the agents**
→ Browse: `.github/agents/` (start with `orchestrator.agent.md`)

**...deploy code**
→ Read: `docs/cloudways-setup.md` (deployment workflow section)

**...troubleshoot**
→ Read: `.claude/common-failures.md`, then `docs/automation-guide.md` (troubleshooting section)

---

## 📂 File Directory

### Root Level
```
PROJECT-SUMMARY.md      - Master project overview
QUICK-START.md          - This file (fast onboarding)
README.md               - Project description
CONTRIBUTING.md         - Contribution guidelines
Makefile                - Development commands
.editorconfig           - Code formatting
.gitignore              - Git ignore rules
```

### Documentation (`docs/`)
```
INDEX.md                - This file (documentation navigation)
architecture.md         - System architecture
automation-guide.md     - Workflow documentation (400+ lines)
cloudways-setup.md      - Server setup guide
local-development-setup.md - Local WordPress setup
vision.md               - 3-5 year vision
roadmap.md              - Development roadmap
testing-results.md      - Test validation results
```

### GitHub (`.github/`)
```
agents/                 - 7 AI agent definitions
workflows/              - 5 GitHub Actions workflows
ISSUE_TEMPLATE/         - 5 issue templates
agent-state/            - Agent pipeline state tracking
agent-config/           - Error handling configuration
pull_request_template.md - PR template
```

### Claude Context (`.claude/`)
```
context/
  project-context.md    - BC+AI mission & values (270 lines)
  wordpress-setup.md    - WordPress configuration
agents-vibe.md          - Agent philosophy (360 lines)
naming-conventions.md   - Code standards (240 lines)
common-failures.md      - Failure patterns (280 lines)
```

### Automation (`skills/`)
```
github-workflow-automation/
  SKILL.md              - Skill documentation
  scripts/              - 6 Python/Bash scripts
  references/           - Guides and templates
```

---

## 🔍 Documentation by Role

### For Contributors (Human)
1. QUICK-START.md
2. CONTRIBUTING.md
3. docs/automation-guide.md
4. .claude/naming-conventions.md

### For Maintainers
1. docs/cloudways-setup.md
2. docs/automation-guide.md
3. docs/architecture.md
4. .github/agent-config/error-handling.yml

### For Agents (AI)
1. .claude/context/project-context.md (mission)
2. .claude/agents-vibe.md (philosophy)
3. .claude/naming-conventions.md (standards)
4. .claude/common-failures.md (learn from mistakes)
5. .github/agents/{agent-name}.agent.md (specific role)

### For Leadership
1. docs/vision.md
2. docs/roadmap.md
3. PROJECT-SUMMARY.md

---

## 📊 Documentation Stats

- **Total Files:** 14 markdown documents
- **Total Lines:** ~4,500 lines of documentation
- **Coverage:** All major aspects documented
- **Status:** Complete and comprehensive

---

## 🚀 Next Steps

1. Read `PROJECT-SUMMARY.md` for overview
2. Follow `QUICK-START.md` to get started
3. Explore `docs/architecture.md` to understand system
4. Dive into specific docs as needed

**Welcome to BC+AI Agent Swarm!** 🌲🤖

---

**Last Updated:** 2026-01-01
