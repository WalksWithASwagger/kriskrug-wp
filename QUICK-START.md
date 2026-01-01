# Quick Start Guide

Get up and running with BC+AI Agent Swarm in 5 minutes.

---

## For New Contributors

### 1. Clone & Setup (2 min)

```bash
# Clone repository
git clone https://github.com/WalksWithASwagger/bc-ai-wp.git
cd bc-ai-wp

# Check health
make health
```

**Output should show:**
- ✓ gh CLI installed
- ✓ Authenticated
- ✓ Repository detected
- ✓ Write permissions

### 2. Explore (1 min)

```bash
# See available commands
make help

# View open issues
make list-issues

# Check repository stats
make stats
```

### 3. Read Documentation (2 min)

**Essential reading:**
1. `README.md` - Overview
2. `CONTRIBUTING.md` - How to contribute
3. `docs/automation-guide.md` - How automation works

**Browse all docs:**
```bash
cat docs/INDEX.md
```

### 4. Start Contributing

**Pick an issue:**
```bash
make list-issues
# Or browse: https://github.com/WalksWithASwagger/bc-ai-wp/issues
```

**Or let the agent swarm handle it:**
- Find a well-defined issue
- Add `auto-implement` label
- Watch the magic happen!

---

## For Maintainers

### 1. Connect to Cloudways Dev Server

```bash
# SSH access (if you have the key)
ssh cloudways-bcai-dev

# Or check docs
cat docs/cloudways-setup.md
```

### 2. Common Tasks

```bash
# Validate WordPress code
make validate

# Run tests
make test

# Create issues from file
make issues FILE=issues.json

# Create PR from issue
make pr ISSUE=123

# Monitor everything
make dashboard
```

### 3. Agent Automation

**Enable for an issue:**
```bash
gh issue edit 123 --add-label "auto-implement"
```

**Monitor progress:**
```bash
make agent-status
# Or check: https://github.com/WalksWithASwagger/bc-ai-wp/actions
```

---

## Quick Reference

### Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all commands |
| `make health` | System health check |
| `make test` | Run test suite |
| `make validate` | Check WordPress coding standards |
| `make stats` | Repository statistics |
| `make dashboard` | Open monitoring dashboard |
| `make list-issues` | Show open issues |
| `make agent-status` | Active agent automations |

### Links

| Resource | URL |
|----------|-----|
| Repository | https://github.com/WalksWithASwagger/bc-ai-wp |
| Issues | https://github.com/WalksWithASwagger/bc-ai-wp/issues |
| Actions | https://github.com/WalksWithASwagger/bc-ai-wp/actions |
| Live Site | https://bc-ai.ca/ |
| Dev Server | https://wordpress-1569695-6109303.cloudwaysapps.com |

### Files

| File | Purpose |
|------|---------|
| `PROJECT-SUMMARY.md` | This project overview |
| `README.md` | Project description |
| `CONTRIBUTING.md` | Contribution guidelines |
| `docs/INDEX.md` | Documentation navigation |
| `docs/automation-guide.md` | Workflow details |
| `.claude/context/project-context.md` | BC+AI mission & values |

---

## First Time Setup

### 1. Install Prerequisites

```bash
# GitHub CLI (if not installed)
brew install gh

# Authenticate
gh auth login

# Verify
gh auth status
```

### 2. Install Extensions (Optional)

```bash
# Monitoring dashboard
gh extension install dlvhdr/gh-dash

# SQL queries
gh extension install KOBA789/gh-sql

# Interactive selection
gh extension install benelan/gh-fzf

# Issue-to-PR workflows
gh extension install InditexTech/gh-sherpa
```

### 3. Configure Git (Optional)

```bash
# Set up commit template
git config commit.template .gitmessage

# Configure user
git config user.name "Your Name"
git config user.email "your@email.com"
```

---

## Common Workflows

### Create Issues from Audit

```bash
# 1. Create JSON file with issues
cat > my-issues.json <<'EOF'
{
  "issues": [
    {
      "title": "Fix navigation bug",
      "body": "Navigation fails on mobile...",
      "labels": ["bug", "mobile"]
    }
  ]
}
EOF

# 2. Validate
python3 skills/github-workflow-automation/scripts/validate_input.py --input my-issues.json

# 3. Create issues
make issues FILE=my-issues.json
```

### Enable Agent Automation

```bash
# Find issue number
make list-issues

# Add auto-implement label
gh issue edit 123 --add-label "auto-implement"

# Monitor progress
make agent-status
# Or watch Actions tab on GitHub
```

### Manual Development

```bash
# 1. Create branch
git checkout -b feature/issue-123-description

# 2. Make changes (on Cloudways or locally)

# 3. Validate
make validate
make test

# 4. Commit
git add .
git commit -m "Fix: Description"

# 5. Push and create PR
git push -u origin feature/issue-123
gh pr create
```

---

## Troubleshooting

### Can't connect to GitHub?

```bash
# Check authentication
make health

# Re-authenticate
gh auth login
```

### Validation failing?

```bash
# Check specific errors
make validate

# Auto-fix issues
bash skills/github-workflow-automation/scripts/validate_wordpress.sh --fix
```

### Agent automation not working?

```bash
# Check workflow status
gh run list --limit 5

# View specific run
gh run view <run-id>

# Check agent state
cat .github/agent-state/{issue-number}/state.json
```

---

## Getting Help

### Documentation
- See `docs/INDEX.md` for all documentation
- Check `docs/automation-guide.md` for workflow details
- Read `.claude/common-failures.md` for known issues

### Community
- Create an issue: https://github.com/WalksWithASwagger/bc-ai-wp/issues
- Visit BC+AI: https://bc-ai.ca/

### Debugging
- Check workflow logs in Actions tab
- Review agent state files in `.github/agent-state/`
- Run `make health` for system check

---

## 🌲 Remember

You're building for BC's AI community. Every line of code serves the mission of responsible, inclusive AI.

**Welcome to the team!** 🤖✨

---

**Read Next:** `docs/INDEX.md` for complete documentation navigation
