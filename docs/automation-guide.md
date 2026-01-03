# Kris Krug Automation Guide

Complete guide to the AI-powered automation workflows for the Kris Krug WordPress site.

## Overview

This repository uses GitHub Actions and AI agents to automate the development workflow from issue creation to pull request merging.

## Workflows

### 1. Auto-Triage (`auto-triage.yml`)

**Triggers:** When issues are opened or edited

**What it does:**
- Automatically adds labels based on issue title and body
- Detects: bugs, enhancements, accessibility, performance, SEO, content, documentation, security, mobile
- Determines priority (high, medium, low)
- Suggests automation for well-defined issues

**Keywords for auto-labeling:**
- **Bug**: "bug", "error", "broken", "not working", "fix"
- **Enhancement**: "feature", "add", "new", "enhancement"
- **Accessibility**: "accessibility", "a11y", "wcag", "screen reader", "keyboard"
- **Performance**: "performance", "slow", "speed", "optimize", "page load"
- **SEO**: "seo", "meta", "schema", "search engine"
- **Security**: "security", "vulnerability", "auth", "password", "xss"
- **Mobile**: "mobile", "responsive", "iphone", "android"

**Example:**
```
Title: Contact form not working on mobile Safari
→ Labels: bug, mobile, priority:high
```

### 2. Agent PR Generator (`agent-pr-generator.yml`)

**Triggers:** When `auto-implement` label is added to an issue

**What it does:**
- Initializes agent state tracking
- Creates agent-state directory for the issue
- Prepares for agent orchestration
- Currently in development mode (placeholder for full agent swarm)

**Agent Pipeline (when fully implemented):**
1. **Analyzer** - Parse issue, create technical spec
2. **Test Writer** - Write tests (TDD approach)
3. **Implementer** - Write code to pass tests
4. **QA** - Run all tests and validations
5. **Reviewer** - Code review with best practices
6. **PR Creator** - Generate comprehensive PR

**State Management:**
- State file: `.github/agent-state/{issue-number}/state.json`
- Tracks: current stage, timestamps, outputs, errors
- Enables: resume from failures, progress monitoring

**To fully enable:**
1. Create custom agents in `.github/agents/`
2. Configure `gh agent-task` integration
3. Implement orchestration logic in workflow

### 3. Test PR (`test-pr.yml`)

**Triggers:** When PRs are opened, updated, or reopened

**What it does:**

#### PR Validation
- Checks PR title format (Fix:, Add:, Update:, etc.)
- Verifies PR links to an issue (Fixes #123)
- Warns if missing issue link

#### PHP/WordPress Validation
- Runs PHPCS with WordPress Coding Standards
- Checks for errors and warnings
- Comments results on PR
- Fails if errors found (warnings are acceptable)

#### JavaScript Validation
- Runs linting if package.json has lint script
- Runs tests if package.json has test script
- Reports results

#### Security Scanning
- Uses Trivy to scan for vulnerabilities
- Uploads results to GitHub Security tab
- SARIF format for code scanning

#### Summary
- Aggregates all check results
- Comments success or failure on PR
- Lists failed checks if any

**Standards checked:**
- WordPress: `WordPress` (default)
- WordPress-Core: Stricter subset
- WordPress-Extra: Includes all WordPress standards

### 4. Sync Projects (`sync-projects.yml`)

**Triggers:** Issue/PR opened, closed, labeled, etc.

**What it does:**
- Syncs issues and PRs to project boards (placeholder)
- Updates status based on activity
- Adds metadata (priority, type, labels)

**Status mapping:**
- Opened → Triage
- `auto-implement` label → In Progress (Automated)
- Ready for review → In Review
- Closed (completed) → Done

**Note:** Full GitHub Projects v2 integration requires additional configuration.

### 5. Reusable WordPress Validation (`reusable-wordpress-validation.yml`)

**Type:** Reusable workflow (called by other workflows)

**Inputs:**
- `standard`: WordPress coding standard (default: WordPress)
- `php-version`: PHP version to use (default: 8.2)
- `files`: Files/directories to check (default: .)

**Usage example:**
```yaml
jobs:
  validate:
    uses: ./.github/workflows/reusable-wordpress-validation.yml
    with:
      standard: WordPress-Extra
      php-version: '8.1'
      files: 'wp-content/themes/custom'
```

## Using the Automation

### For Contributors

#### Creating Issues
1. Use issue templates (bug, feature, accessibility, etc.)
2. Provide clear title and description
3. Auto-triage will add appropriate labels
4. If well-defined, automation will be suggested

#### Enabling Automation
1. Create a detailed issue with clear requirements
2. Wait for auto-triage labels
3. Add `auto-implement` label when ready
4. Monitor progress in Actions tab
5. Review and approve the generated PR

#### Creating PRs
1. Link to an issue using `Fixes #123`
2. Use proper title format (`Fix:`, `Add:`, etc.)
3. Automated tests will run
4. Fix any PHPCS violations
5. Wait for all checks to pass

### For Maintainers

#### Configuring Workflows

**Required secrets:** None (uses GITHUB_TOKEN)

**Required permissions:**
- issues: write
- pull-requests: write
- contents: write
- repository-projects: write (for project sync)

**Branch protection:**
- Require status checks to pass
- Require review before merging
- Include administrators: Optional

#### Monitoring

**Check workflow runs:**
```bash
gh run list
gh run view <run-id>
gh run watch <run-id>
```

**View agent state:**
```bash
cat .github/agent-state/{issue-number}/state.json
```

**Manually trigger:**
```bash
gh workflow run auto-triage.yml
```

## Agent Swarm Setup (Phase 4)

### Prerequisites
1. Custom agents defined in `.github/agents/`
2. `gh agent-task` configured
3. Orchestration logic implemented

### Agent Definitions

Each agent needs a `.agent.md` file:

```markdown
# Agent Name

You are the [Role] Agent for WordPress development.

Your role is to:
1. [Responsibility 1]
2. [Responsibility 2]

## Tools Available
- read, edit, write, search, execute

## Output Format
Generate a JSON file with:
{
  "stage": "analysis",
  "status": "completed",
  "output": "..."
}

## WordPress Best Practices
- Follow WPCS
- Sanitize inputs, escape outputs
- Use prepared statements
```

### Required Agents
1. `orchestrator.agent.md` - Main coordinator
2. `analyzer.agent.md` - Issue analysis
3. `test-writer.agent.md` - TDD test creation
4. `implementer.agent.md` - Code implementation
5. `qa.agent.md` - Testing and validation
6. `reviewer.agent.md` - Code review
7. `pr-creator.agent.md` - PR generation

### State Schema

```json
{
  "issue_number": 123,
  "workflow_id": "abc123",
  "current_stage": "implementation",
  "status": "in_progress",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:05:00Z",
  "stages": {
    "analysis": {
      "status": "completed",
      "started_at": "2026-01-01T00:00:00Z",
      "completed_at": "2026-01-01T00:01:00Z",
      "output_file": ".github/agent-state/123/analysis.json",
      "agent_task_id": "task-xyz"
    },
    "implementation": {
      "status": "in_progress",
      "started_at": "2026-01-01T00:03:00Z",
      "agent_task_id": "task-abc"
    }
  },
  "retry_counts": {},
  "errors": [],
  "metadata": {
    "branch_name": "feature/issue-123",
    "base_branch": "main"
  }
}
```

## Troubleshooting

### Workflow not triggering
- Check trigger conditions (labels, events)
- Verify permissions in workflow file
- Check branch protection rules

### PHPCS errors
```bash
# Run locally
bash skills/github-workflow-automation/scripts/validate_wordpress.sh --fix

# Or use composer
composer global require wp-coding-standards/wpcs
phpcs --standard=WordPress-Extra . --fix
```

### PR checks failing
1. Check Actions tab for details
2. Read error messages in PR comments
3. Fix locally and push again
4. Re-run failed checks if needed

### Agent state not updating
- Check workflow run logs
- Verify state file exists
- Check file permissions
- Ensure git push succeeded

## Best Practices

### Issue Creation
- Use templates for consistency
- Provide reproduction steps for bugs
- Include acceptance criteria for features
- Link to related issues
- Add relevant labels

### PR Creation
- Always link to an issue
- Keep PRs focused and small
- Write clear commit messages
- Add tests for new features
- Update documentation

### Automation
- Start with simple, well-defined issues
- Review agent-generated code carefully
- Test locally before pushing
- Monitor agent progress
- Provide feedback for improvements

## Advanced Topics

### Custom Workflows

Create `.github/workflows/custom.yml`:

```yaml
name: Custom Workflow

on:
  workflow_dispatch:
    inputs:
      issue_number:
        description: 'Issue number'
        required: true

jobs:
  custom-task:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom logic
        run: echo "Issue ${{ inputs.issue_number }}"
```

### Calling Reusable Workflows

```yaml
jobs:
  wordpress-check:
    uses: ./.github/workflows/reusable-wordpress-validation.yml
    with:
      standard: WordPress-Extra
```

### Matrix Testing

```yaml
jobs:
  test:
    strategy:
      matrix:
        php: ['8.0', '8.1', '8.2']
        wordpress: ['6.4', '6.5']
    steps:
      - name: Test on PHP ${{ matrix.php }} with WP ${{ matrix.wordpress }}
        run: echo "Testing..."
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [GitHub CLI](https://cli.github.com/)
- [Anthropic Skills](https://github.com/anthropics/skills)

## Support

- **Issues**: Create an issue in this repository
- **Discussions**: Use GitHub Discussions
- **Documentation**: See `/docs` directory
- **Examples**: Check existing workflows in `.github/workflows/`
