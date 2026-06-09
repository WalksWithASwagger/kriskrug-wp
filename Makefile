# kriskrug-wp Development Makefile
# Quick access to common development commands

.PHONY: help test plugin-smoke verify validate health issues pr dashboard stats agent-status backup-check draft-queue-audit jetpack-feedback-audit seo-audit wp7-smoke wp7-admin-readiness current-state-drift-check morning-truth status-readonly docs-truth-check clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "kriskrug-wp Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make health"
	@echo "  make issues FILE=test-data/issues.json"
	@echo "  make pr ISSUE=123"

test: ## Run test suite
	@echo "Running tests..."
	@bash skills/github-workflow-automation/scripts/run_tests.sh
	@$(MAKE) plugin-smoke

plugin-smoke: ## Run lightweight plugin smoke tests
	@if command -v php >/dev/null 2>&1; then \
		php plugins/kk-sidebar-promos/tests/smoke.php; \
	else \
		echo "Skipping plugin smoke: php not found"; \
	fi

verify: ## Run the standard local verification suite
	@$(MAKE) test
	@$(MAKE) docs-truth-check
	@$(MAKE) validate

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
	@echo "kriskrug-wp Repository Stats"
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

agent-status: ## Show parked agent automation state records
	@echo "🤖 Agent Automation Status"
	@echo ""
	@echo "  Agent PR Generator is parked; auto-implement labels do not start automation."
	@echo "  Historical state records:"
	@if [ -d ".github/agent-state" ]; then \
		find .github/agent-state -name "state.json" -exec sh -c 'jq -r "select(.status == \"in_progress\") | \"Issue #\" + (.issue_number | tostring) + \": \" + .current_stage" {} 2>/dev/null || true' \; | \
		while read line; do \
			if [ -n "$$line" ]; then \
				echo "  ⏳ $$line"; \
			fi; \
		done; \
	fi
	@echo "  (These records are not proof of active automation.)" 2>/dev/null || true

backup-check: ## Verify a backup set (use BACKUP_DIR=backup/YYYY-MM-DD; STRICT=1 requires restore proof)
	@if [ -z "$(BACKUP_DIR)" ]; then \
		echo "❌ Error: Please specify BACKUP_DIR=backup/YYYY-MM-DD"; \
		exit 1; \
	fi
	@if [ "$(STRICT)" = "1" ]; then \
		bash scripts/verify-backup-set.sh "$(BACKUP_DIR)"; \
	else \
		bash scripts/verify-backup-set.sh --allow-incomplete "$(BACKUP_DIR)"; \
	fi

draft-queue-audit: ## Run read-only draft queue audit (LOCAL_ONLY=1 FORMAT=json)
	@if [ "$${LOCAL_ONLY:-0}" = "1" ]; then \
		python3 scripts/notion-to-wp/draft_queue_audit.py --local-only --format "$${FORMAT:-markdown}"; \
	else \
		scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --format "$${FORMAT:-markdown}"; \
	fi

seo-audit: ## Run read-only Jetpack SEO metadata inventory (FORMAT=markdown|json|csv)
	@if [ "$${FORMAT:-markdown}" = "csv" ]; then \
		scripts/notion-to-wp/.venv/bin/python scripts/seo-audit/inventory.py --format csv --output "$${OUTPUT:-content/seo-audit-inventory.csv}"; \
	elif [ "$${FORMAT:-markdown}" = "json" ]; then \
		scripts/notion-to-wp/.venv/bin/python scripts/seo-audit/inventory.py --format json; \
	else \
		scripts/notion-to-wp/.venv/bin/python scripts/seo-audit/inventory.py --format markdown; \
	fi

jetpack-feedback-audit: ## Run PII-safe read-only Jetpack Forms feedback counts/routing audit (FORMAT=json)
	@if [ "$${FORMAT:-human}" = "json" ]; then \
		python3 scripts/jetpack_feedback_audit.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}" --json; \
	else \
		python3 scripts/jetpack_feedback_audit.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}"; \
	fi

wp7-smoke: ## Run read-only public WP 7 rollout smoke checks (BASE_URL=https://kriskrug.co EXPECT_VERSION=6.9.4)
	@python3 scripts/wp7-public-smoke.py --base-url "$${BASE_URL:-https://kriskrug.co}" --timeout "$${REQUEST_TIMEOUT:-20}" $${EXPECT_VERSION:+--expect-version "$$EXPECT_VERSION"}

wp7-admin-readiness: ## Run authenticated read-only WP 7 readiness snapshot (ENV_FILE=scripts/notion-to-wp/.env)
	@python3 scripts/wp7-admin-readiness.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}"

current-state-drift-check: ## Compare declared current-state snapshot values vs live read-only checks
	@python3 scripts/check_current_state_drift.py --work-plan "$${WORK_PLAN:-docs/current-state/WORK-PLAN-2026-05-23.md}" --base-url "$${BASE_URL:-https://kriskrug.co}"

morning-truth: ## Run startup truth checks and write a timestamped markdown report
	@python3 scripts/morning_truth_report.py --work-plan "$${WORK_PLAN:-docs/current-state/WORK-PLAN-2026-05-23.md}" --base-url "$${BASE_URL:-https://kriskrug.co}" --expect-version "$${EXPECT_VERSION:-6.9.4}" --request-timeout "$${REQUEST_TIMEOUT:-20}" --command-timeout "$${COMMAND_TIMEOUT:-120}"

status-readonly: ## Print startup truth checks without writing a report
	@python3 scripts/morning_truth_report.py --stdout --skip-fetch --work-plan "$${WORK_PLAN:-docs/current-state/WORK-PLAN-2026-05-23.md}" --base-url "$${BASE_URL:-https://kriskrug.co}" --expect-version "$${EXPECT_VERSION:-6.9.4}" --request-timeout "$${REQUEST_TIMEOUT:-20}" --command-timeout "$${COMMAND_TIMEOUT:-120}"

docs-truth-check: ## Scan non-evidence docs for known stale current-state claims
	@python3 scripts/docs_truth_check.py --exclude docs/current-state/reports --exclude docs/current-state/raw

clean: ## Clean up test artifacts and temporary files
	@echo "Cleaning up..."
	@rm -rf coverage/
	@rm -rf phpcs-report.*
	@rm -rf .phpunit.result.cache
	@echo "✓ Cleanup complete"

setup: ## Initial setup for new contributors
	@echo "Setting up kriskrug-wp development environment..."
	@echo ""
	@bash skills/github-workflow-automation/scripts/gh_health_check.sh
	@echo ""
	@echo "✅ Setup complete! Run 'make help' to see available commands."

quick-start: ## Quick start guide for new contributors
	@echo "Welcome to kriskrug-wp development!"
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
