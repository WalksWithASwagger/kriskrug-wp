# BC+AI Development Makefile
# Quick access to common development commands

.PHONY: help test validate health issues pr dashboard stats clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "🌲 BC+AI Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make health"
	@echo "  make issues FILE=test-data/issues.json"
	@echo "  make pr ISSUE=123"

test: ## Run test suite
	@echo "Running tests..."
	@bash skills/github-workflow-automation/scripts/run_tests.sh

validate: ## Run WordPress coding standards check
	@echo "Validating WordPress coding standards..."
	@bash skills/github-workflow-automation/scripts/validate_wordpress.sh

validate-fix: ## Auto-fix WordPress coding standard violations
	@echo "Auto-fixing WordPress coding standards..."
	@bash skills/github-workflow-automation/scripts/validate_wordpress.sh --fix

health: ## Check gh CLI and system health
	@bash skills/github-workflow-automation/scripts/gh_health_check.sh

issues: ## Create issues from JSON/CSV file (use FILE=path.json)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: Please specify FILE=path.json"; \
		echo "Example: make issues FILE=test-data/issues.json"; \
		exit 1; \
	fi
	@python3 skills/github-workflow-automation/scripts/validate_input.py --input $(FILE)
	@python3 skills/github-workflow-automation/scripts/batch_create_issues.py --input $(FILE)

issues-dry-run: ## Preview issues without creating (use FILE=path.json)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: Please specify FILE=path.json"; \
		exit 1; \
	fi
	@python3 skills/github-workflow-automation/scripts/batch_create_issues.py --input $(FILE) --dry-run

pr: ## Create PR from issue (use ISSUE=123)
	@if [ -z "$(ISSUE)" ]; then \
		echo "❌ Error: Please specify ISSUE=number"; \
		echo "Example: make pr ISSUE=123"; \
		exit 1; \
	fi
	@python3 skills/github-workflow-automation/scripts/create_pr_from_issue.py --issue $(ISSUE)

pr-draft: ## Create draft PR from issue (use ISSUE=123)
	@if [ -z "$(ISSUE)" ]; then \
		echo "❌ Error: Please specify ISSUE=number"; \
		exit 1; \
	fi
	@python3 skills/github-workflow-automation/scripts/create_pr_from_issue.py --issue $(ISSUE) --draft

dashboard: ## Open gh-dash monitoring dashboard
	@gh dash

list-issues: ## List open issues
	@gh issue list

list-prs: ## List open pull requests
	@gh pr list

list-workflows: ## List recent workflow runs
	@gh run list --limit 10

stats: ## Show repository statistics
	@echo "📊 BC+AI Repository Stats"
	@echo ""
	@echo "Issues:"
	@gh issue list --state all --json number --jq '. | length' | xargs -I {} echo "  Total: {}"
	@gh issue list --state open --json number --jq '. | length' | xargs -I {} echo "  Open: {}"
	@gh issue list --state closed --json number --jq '. | length' | xargs -I {} echo "  Closed: {}"
	@echo ""
	@echo "Pull Requests:"
	@gh pr list --state all --json number --jq '. | length' | xargs -I {} echo "  Total: {}"
	@gh pr list --state open --json number --jq '. | length' | xargs -I {} echo "  Open: {}"
	@gh pr list --state merged --json number --jq '. | length' | xargs -I {} echo "  Merged: {}"
	@echo ""
	@echo "Labels:"
	@gh label list --json name --jq '. | length' | xargs -I {} echo "  Total: {}"
	@echo ""
	@echo "Recent Activity:"
	@gh run list --limit 5

agent-status: ## Show active agent automations
	@echo "🤖 Agent Automation Status"
	@echo ""
	@if [ -d ".github/agent-state" ]; then \
		find .github/agent-state -name "state.json" -exec sh -c 'jq -r "select(.status == \"in_progress\") | \"Issue #\" + (.issue_number | tostring) + \": \" + .current_stage" {} 2>/dev/null || true' \; | \
		while read line; do \
			if [ -n "$$line" ]; then \
				echo "  ⏳ $$line"; \
			fi; \
		done; \
	fi
	@echo "  (No active automations)" 2>/dev/null || true

clean: ## Clean up test artifacts and temporary files
	@echo "Cleaning up..."
	@rm -rf coverage/
	@rm -rf phpcs-report.*
	@rm -rf .phpunit.result.cache
	@echo "✓ Cleanup complete"

setup: ## Initial setup for new contributors
	@echo "🌲 Setting up BC+AI development environment..."
	@echo ""
	@bash skills/github-workflow-automation/scripts/gh_health_check.sh
	@echo ""
	@echo "✅ Setup complete! Run 'make help' to see available commands."

quick-start: ## Quick start guide for new contributors
	@echo "🌲 Welcome to BC+AI Development!"
	@echo ""
	@echo "Quick commands to get you started:"
	@echo "  make health       - Check system health"
	@echo "  make list-issues  - See open issues"
	@echo "  make dashboard    - Open monitoring dashboard"
	@echo "  make stats        - View repository statistics"
	@echo ""
	@echo "For full command list, run: make help"
	@echo ""
	@echo "Read CONTRIBUTING.md for contribution guidelines!"
