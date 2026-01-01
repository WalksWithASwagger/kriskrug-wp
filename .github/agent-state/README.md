# Agent State Directory

This directory stores state files for the agent swarm automation pipeline.

## Structure

```
agent-state/
├── README.md (this file)
├── {issue-number}/
│   ├── state.json (main state file)
│   ├── analysis.json (analyzer output)
│   ├── test-plan.json (test writer output)
│   ├── implementation.json (implementer output)
│   ├── qa-results.json (QA output)
│   └── review-decision.json (reviewer output)
└── agent-orchestration.log (global log)
```

## State File Schema

### Main State File (`state.json`)

```json
{
  "issue_number": 123,
  "workflow_id": "github-actions-run-id",
  "current_stage": "implementation",
  "status": "in_progress",
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T10:15:00Z",
  "stages": {
    "analysis": {
      "status": "completed",
      "started_at": "2026-01-01T10:00:00Z",
      "completed_at": "2026-01-01T10:05:00Z",
      "output_file": ".github/agent-state/123/analysis.json",
      "agent_task_id": "task-abc123"
    },
    "test_writing": {
      "status": "completed",
      "started_at": "2026-01-01T10:05:00Z",
      "completed_at": "2026-01-01T10:10:00Z",
      "output_file": ".github/agent-state/123/test-plan.json",
      "agent_task_id": "task-def456"
    },
    "implementation": {
      "status": "in_progress",
      "started_at": "2026-01-01T10:10:00Z",
      "agent_task_id": "task-ghi789"
    },
    "testing": {
      "status": "pending"
    },
    "review": {
      "status": "pending"
    },
    "pr_creation": {
      "status": "pending"
    }
  },
  "retry_counts": {
    "implementation": 1
  },
  "errors": [],
  "metadata": {
    "branch_name": "feature/issue-123-auto-fix",
    "base_branch": "main",
    "pr_url": null
  }
}
```

## Status Values

- `pending` - Stage not yet started
- `in_progress` - Stage currently running
- `completed` - Stage finished successfully
- `failed` - Stage failed (may retry)
- `skipped` - Stage skipped (not needed)

## Usage

### Read State

```bash
# Get current state
cat .github/agent-state/123/state.json

# Get specific stage status
jq '.stages.implementation.status' .github/agent-state/123/state.json

# Get all errors
jq '.errors' .github/agent-state/123/state.json
```

### Update State

```bash
# Update stage status
jq '.stages.analysis.status = "completed"' state.json > temp.json
mv temp.json state.json

# Add timestamp
jq '.updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' state.json > temp.json
mv temp.json state.json

# Increment retry count
jq '.retry_counts.implementation = (.retry_counts.implementation // 0) + 1' state.json > temp.json
mv temp.json state.json

# Add error
jq '.errors += ["Error message"]' state.json > temp.json
mv temp.json state.json
```

### Clean Up

```bash
# Remove old completed states (30+ days)
find .github/agent-state -name "state-completed.json" -mtime +30 -delete

# Archive completed state
mv .github/agent-state/123/state.json .github/agent-state/123/state-completed.json
```

## Agent Outputs

### analysis.json
Output from Analyzer agent containing technical specification.

### test-plan.json
Output from Test Writer agent listing tests created.

### implementation.json
Output from Implementer agent summarizing code changes.

### qa-results.json
Output from QA agent with comprehensive test results.

### review-decision.json
Output from Reviewer agent with approval decision.

## Monitoring

### Check Active Workflows

```bash
# Find all in-progress workflows
find .github/agent-state -name "state.json" -exec jq -r 'select(.status == "in_progress") | .issue_number' {} \;

# Find failed workflows
find .github/agent-state -name "state.json" -exec jq -r 'select(.status == "failed") | .issue_number' {} \;
```

### View Logs

```bash
# Tail orchestration log
tail -f .github/agent-state/agent-orchestration.log

# Search for errors
grep "ERROR" .github/agent-state/agent-orchestration.log
```

## Troubleshooting

### Stuck Workflow

If a workflow appears stuck:

1. Check state file for current stage
2. View workflow logs in GitHub Actions
3. Check agent-task status with `gh agent-task view {task-id}`
4. Manually advance or retry if needed

### State File Corruption

If state file is corrupted:

1. Check git history: `git log .github/agent-state/123/state.json`
2. Restore from previous commit if needed
3. Manually fix JSON syntax
4. Restart workflow from last good state

### Missing Outputs

If agent output files are missing:

1. Check if stage actually completed
2. Review agent task logs
3. Manually run agent if needed
4. Verify file permissions

## Best Practices

1. **Always commit state changes** - State should be in git
2. **Never edit state manually** unless troubleshooting
3. **Clean up old states** - Run cleanup script monthly
4. **Monitor for stuck workflows** - Check daily
5. **Archive completed states** - Keep for audit trail

## Security

⚠️ **Important:** State files may contain sensitive information from issues.

- Never commit API keys or secrets
- Be careful with issue descriptions containing private data
- Clean up test data after completion
- Review before making repository public

## Git Ignore

This directory is tracked in git to preserve state across workflow runs.

Individual state files are committed to enable:
- Resume after failures
- Audit trail of agent decisions
- Debugging and troubleshooting

Large output files (> 1MB) should be stored as artifacts instead.
