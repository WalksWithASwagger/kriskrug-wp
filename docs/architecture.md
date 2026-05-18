# Kris Krug Agent Swarm Architecture

> **STATUS: Historical.** This describes the dormant GitHub Actions agent swarm. Current sessions use `AGENTS.md` and `docs/current-state/TWO-TRACK-MODEL.md`.

Complete system architecture and how everything connects.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Kris Krug ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Production Site          GitHub Repository          Dev Server │
│  ┌──────────────┐        ┌────────────────┐        ┌──────────┐ │
│  │  kk.ca    │◄──────►│ Issue Tracking │◄──────►│ Cloudways│ │
│  │  (Live WP)   │        │  Automation    │        │ (WP 6.9) │ │
│  └──────────────┘        │  Agent Swarm   │        └──────────┘ │
│                          └────────────────┘                   │
│                                 ▲                             │
│                                 │                             │
│                          ┌──────▼───────┐                    │
│                          │  Claude AI   │                    │
│                          │    Agents    │                    │
│                          └──────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. GitHub Repository (Central Hub)

**Purpose:** Issue tracking, automation orchestration, version control

**Components:**
- **Issues:** Bug reports, feature requests, audits
- **Projects:** Kanban board for organization
- **Actions:** Automated workflows
- **Agents:** AI agent definitions
- **Skills:** Custom automation tools

**Workflows:**
```
Issue Created → Auto-Triage → Labels Applied
Issue Labeled (auto-implement) → Agent Swarm → PR Created
PR Created → Tests Run → Human Review → Merge
PR Merged → Deploy (manual for now)
```

### 2. Agent Swarm (AI Automation)

**Purpose:** Convert issues to pull requests automatically

**Architecture:** Hierarchical orchestration with 7 specialized agents

```
                    ┌─────────────────┐
                    │  Orchestrator   │
                    │   (Coordinator) │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
    │ Analyzer  │────►│Test Writer│────►│Implementer│
    │           │     │   (TDD)   │     │   (Code)  │
    └───────────┘     └───────────┘     └─────┬─────┘
                                              │
                      ┌───────────────────────┼────────────┐
                      │                       │            │
                ┌─────▼─────┐          ┌─────▼────┐  ┌────▼───┐
                │    QA     │─────────►│ Reviewer │─►│PR      │
                │ (Testing) │          │  (Review)│  │Creator │
                └───────────┘          └──────────┘  └────────┘
```

**Data Flow:**
```
Issue → Analysis JSON → Test Files → Code Changes → QA Results → Review Decision → Pull Request
```

**State Management:**
```
.github/agent-state/{issue-number}/
├── state.json              # Pipeline state
├── analysis.json           # Analyzer output
├── test-plan.json          # Test Writer output
├── implementation.json     # Implementer output
├── qa-results.json         # QA output
└── review-decision.json    # Reviewer output
```

### 3. GitHub Actions (Automation Engine)

**Purpose:** Trigger and execute workflows automatically

**Workflows:**

#### auto-triage.yml
```
Event: Issue opened/edited
Actions:
1. Analyze title and body for keywords
2. Add relevant labels (bug, accessibility, performance, etc.)
3. Determine priority (high/medium/low)
4. Comment with labels added
5. Suggest automation if well-defined
```

#### agent-pr-generator.yml
```
Event: Issue labeled with 'auto-implement'
Actions:
1. Acknowledge automation request
2. Initialize agent state directory
3. Create state.json tracking file
4. Invoke orchestrator agent (framework in place)
5. Monitor pipeline progress
6. Create PR when complete
7. Handle failures (retry or escalate)
```

#### test-pr.yml
```
Event: PR opened/updated
Actions:
1. Validate PR title format
2. Check issue linking (Fixes #123)
3. Run PHPCS (WordPress-Extra standard)
4. Run JavaScript linting
5. Run security scan (Trivy)
6. Comment results on PR
7. Fail if critical issues found
```

#### sync-projects.yml
```
Event: Issue/PR state changes
Actions:
1. Sync to project board
2. Update status based on activity
3. Add metadata (priority, type)
```

#### reusable-wordpress-validation.yml
```
Callable workflow for PHPCS validation
Inputs: standard, php-version, files
Outputs: Error count, warnings, report
```

### 4. Custom Skill (Automation Tools)

**Purpose:** Reusable automation scripts for GitHub operations

**Scripts:**

```python
# batch_create_issues.py
Input: JSON/CSV file with issues
Output: Created GitHub issues
Features: Validation, error handling, dry-run

# create_pr_from_issue.py
Input: Issue number(s)
Output: Pull request with "Fixes #N" linking
Features: Multiple issue linking, draft PRs

# validate_input.py
Input: JSON/CSV file
Output: Validation report
Features: Schema validation, duplicate detection
```

```bash
# validate_wordpress.sh
Input: PHP files
Output: PHPCS results
Features: Auto-fix, multiple standards

# run_tests.sh
Input: Project directory
Output: Test results
Features: Auto-detect frameworks (PHPUnit, pytest, npm)

# gh_health_check.sh
Input: None
Output: System health report
Features: gh CLI, auth, permissions check
```

### 5. Development Environment (Cloudways)

**Purpose:** Safe WordPress testing environment

**Specifications:**
- **Server:** Cloudways VPS (24.144.80.107)
- **WordPress:** 6.9 (latest)
- **PHP:** 8.2.29
- **Tools:** WP-CLI 2.12.0, Git 2.39.5
- **Storage:** 50GB (39GB available)
- **Caching:** Redis (Object Cache Pro) + Breeze

**Access:**
```bash
# SSH (key-based authentication)
ssh cloudways-bcai-dev

# WordPress
URL: https://wordpress-1569695-6109303.cloudwaysapps.com
Admin: {credentials in Cloudways dashboard}

# File paths
WordPress root: ~/applications/fkgwevabgu/public_html
Custom plugin: ~/applications/fkgwevabgu/public_html/wp-content/plugins/kk-custom
Custom theme: ~/applications/fkgwevabgu/public_html/wp-content/themes/kk-theme
```

---

## Data Flow

### Issue-to-PR Pipeline

**1. Issue Creation**
```
User creates issue
  ↓
GitHub Issue #123
  ↓
auto-triage.yml triggers
  ↓
Labels added (bug, accessibility, priority:high)
  ↓
Comment posted with automation suggestion
```

**2. Automation Activation**
```
User/maintainer adds 'auto-implement' label
  ↓
agent-pr-generator.yml triggers
  ↓
Initialize agent state
  ↓
Comment: "Agent swarm activated"
```

**3. Agent Pipeline** (when fully integrated)
```
Orchestrator starts
  ↓
Analyzer: Issue → analysis.json
  ↓
Test Writer: analysis.json → test files (failing tests)
  ↓
Implementer: tests + analysis → code changes (tests pass)
  ↓
QA: code → qa-results.json (PHPCS, tests, security)
  ↓
Reviewer: all outputs → review-decision.json (approve/reject)
  ↓
PR Creator: approved → GitHub pull request
  ↓
test-pr.yml validates PR
  ↓
Human review and merge
```

**4. State Tracking**
```
.github/agent-state/123/state.json updated at each stage:
- current_stage: "implementation"
- status: "in_progress"
- timestamps for each stage
- retry_counts if failures
- errors array if issues
- metadata (branch name, etc.)
```

---

## Technology Stack

### Languages & Frameworks
- **PHP 8.2** - WordPress backend
- **Python 3** - Automation scripts
- **Bash** - Shell scripts
- **JavaScript** - WordPress frontend (when needed)
- **YAML** - GitHub Actions workflows
- **Markdown** - Documentation & agent definitions

### Tools & Platforms
- **GitHub** - Version control, issues, automation
- **GitHub Actions** - CI/CD workflows
- **Claude AI** - Agent intelligence
- **Cloudways** - WordPress hosting
- **WP-CLI** - WordPress command-line
- **gh CLI** - GitHub command-line + extensions

### WordPress Stack
- **WordPress 6.9** - CMS platform
- **PHPUnit** - PHP testing
- **PHPCS + WPCS** - Code standards
- **Breeze** - Page caching
- **Object Cache Pro** - Redis object caching

---

## Security Architecture

### Multi-Layer Security

**Layer 1: Input Validation**
- All issue inputs validated before processing
- JSON/CSV schema validation
- Sanitization of user data

**Layer 2: Code Generation**
- Agents programmed to sanitize inputs
- Escape all outputs
- Verify nonces
- Check capabilities

**Layer 3: Automated Testing**
- PHPCS catches security violations
- Security scans (Trivy) on PRs
- Test coverage requirements

**Layer 4: Human Review**
- All agent PRs require human approval
- Code review checklist
- Manual testing before merge

**Layer 5: Production Separation**
- Development on Cloudways (separate server)
- Never deploy untested code
- Git-based deployment (controlled)

### Credential Management

**Never in Git:**
- ❌ wp-config.php (database credentials)
- ❌ API keys
- ❌ Passwords
- ❌ Production data

**Stored Securely:**
- GitHub Secrets for Actions
- Cloudways dashboard for WordPress admin
- Password manager for sensitive data
- Encrypted .cloudways-credentials (local only)

---

## Scalability & Performance

### Current Capacity
- **Concurrent workflows:** 5 simultaneous
- **Agent retries:** Max 3 per stage
- **Issue processing:** Unlimited (rate-limited by GitHub API)
- **Storage:** 50GB on Cloudways

### Performance Optimizations
- **Caching:** Redis object cache + Breeze page cache
- **CDN:** Cloudways built-in (if enabled)
- **OPcache:** PHP opcode caching enabled
- **Context caching:** Claude AI prompt caching

### Bottlenecks & Mitigation
- **GitHub API limits:** 5000 req/hour (authenticated)
- **Agent execution time:** Timeout limits per stage
- **Workflow concurrency:** Max 3 simultaneous (configured)

---

## Error Handling & Reliability

### Retry Strategy

**Error Categories:**
1. **Transient** (network, rate limits) → Immediate retry
2. **Recoverable** (test failures) → Retry with context
3. **Fatal** (permissions, conflicts) → Human intervention

**Retry Policy:**
- Max 3 retries per stage
- Exponential backoff: 1min, 2min, 4min
- State preserved for resume

### Failure Recovery

```
Error detected
  ↓
Categorize error type
  ↓
Check retry count
  ↓
If < 3: Retry with context
If ≥ 3: Label 'needs-human-review' + notify
```

### Monitoring

- GitHub Actions logs (all workflow runs)
- Agent state files (progress tracking)
- Workflow run history
- Error logs in state.json

---

## Integration Points

### GitHub API
- Issue creation/management
- PR creation/management
- Label operations
- Workflow triggers
- Project board sync

### WordPress APIs
- WP-CLI for management
- WordPress REST API (potential)
- Database access via wp-config
- Plugin/theme APIs

### External Services
- Cloudways API (potential)
- Notion API (via MCP server)
- Future integrations as needed

---

## Development Workflow

### Local Development
```
1. Clone repo → 2. Make changes → 3. Validate → 4. Test → 5. Commit → 6. Push → 7. PR → 8. Review → 9. Merge
```

### Agent Automation
```
1. Issue created → 2. Auto-triaged → 3. Label added → 4. Agent swarm → 5. PR generated → 6. Human review → 7. Merge → 8. Deploy
```

### Deployment
```
Git repo (main branch) → Review → Deploy to Cloudways dev → Test → Deploy to production (manual)
```

---

## Future Architecture Enhancements

### Planned Improvements

**Q1 2026:**
- Full gh agent-task integration
- End-to-end automation testing
- Performance monitoring

**Q2 2026:**
- Automated deployment to production
- Staging environment automation
- Advanced caching strategies

**Q3 2026:**
- MCP server for GitHub API
- Custom WordPress APIs
- Real-time monitoring

**Q4 2026:**
- Multi-environment support
- A/B testing infrastructure
- Analytics integration

---

## Key Design Decisions

### Why Hierarchical Agent Orchestration?
- Clear accountability
- Easier debugging
- State management
- Resume from failures

### Why Test-Driven Development?
- Quality assurance
- Specification through tests
- Regression prevention
- Confidence in automation

### Why WordPress Coding Standards?
- Community consistency
- Security best practices
- Maintainability
- Plugin compatibility

### Why Cloudways?
- Managed WordPress hosting
- Easy staging/cloning
- Built-in caching
- Good developer tools

### Why GitHub Actions?
- Native GitHub integration
- Free for public repos
- Powerful workflow engine
- Large ecosystem

---

## System Boundaries

### What's Automated
- ✅ Issue labeling
- ✅ Technical specification creation
- ✅ Test generation (TDD)
- ✅ Code implementation
- ✅ Code quality validation
- ✅ PR generation

### What Requires Humans
- ❌ Final PR approval
- ❌ Production deployment
- ❌ Architectural decisions
- ❌ Community strategy
- ❌ Security-critical changes

---

## Documentation Architecture

### Four Levels of Documentation

**Level 1: Overview** (for everyone)
- PROJECT-SUMMARY.md
- README.md
- QUICK-START.md

**Level 2: Guides** (for contributors)
- CONTRIBUTING.md
- docs/automation-guide.md
- docs/cloudways-setup.md

**Level 3: Technical** (for maintainers)
- docs/architecture.md (this file)
- .github/agents/*.md
- skills/github-workflow-automation/

**Level 4: Context** (for agents)
- .claude/context/project-context.md
- .claude/agents-vibe.md
- .claude/naming-conventions.md
- .claude/common-failures.md

---

## Agent Architecture Deep Dive

### Agent Communication Pattern

**Sequential pipeline with shared state:**

```
Each agent:
1. Reads: Previous agent outputs + issue details
2. Processes: Executes specific task
3. Writes: Output JSON to agent-state/
4. Updates: state.json with completion status
5. Commits: State changes to git
6. Signals: Orchestrator to proceed
```

**State Schema (state.json):**
```json
{
  "issue_number": 123,
  "workflow_id": "run-id",
  "current_stage": "implementation",
  "status": "in_progress",
  "stages": {
    "analysis": {
      "status": "completed",
      "started_at": "timestamp",
      "completed_at": "timestamp",
      "output_file": "path",
      "agent_task_id": "gh-agent-task-id"
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

### Agent Responsibilities Matrix

| Agent | Input | Output | Tools | Validation |
|-------|-------|--------|-------|------------|
| Orchestrator | Issue | State file | All | Coordinates pipeline |
| Analyzer | Issue | analysis.json | read, search | Spec completeness |
| Test Writer | analysis.json | Test files | write, read | Tests fail initially |
| Implementer | Tests + analysis | Code | write, edit, execute | Tests pass, PHPCS clean |
| QA | Code | qa-results.json | execute, read | All checks pass |
| Reviewer | All outputs | review-decision.json | read | Checklist complete |
| PR Creator | Approved | PR URL | github API | PR created |

---

## This Architecture Enables

✅ **Autonomous Operation** - Minimal human intervention
✅ **Quality Assurance** - TDD + automated testing
✅ **Transparency** - Full audit trail in state files
✅ **Reliability** - Retry logic and error handling
✅ **Scalability** - Handle multiple issues in parallel
✅ **Learning** - Agents improve from documented failures
✅ **Values Alignment** - Context engineering ensures mission focus

---

**The architecture serves the mission: Building responsible, inclusive AI for British Columbia through automated, high-quality WordPress development.** 🌲🤖
