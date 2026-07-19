# kriskrug-wp Development Makefile
# Quick access to common development commands

.PHONY: help test python-test javascript-syntax php-syntax plugin-smoke theme-smoke verify validate health issues pr dashboard stats agent-status backup-check wp-package aurora-package sidebar-promos-package marquee-package draft-queue-audit jetpack-feedback-audit seo-audit public-image-audit performance-audit wp7-smoke wp7-admin-readiness current-state-drift-check morning-truth status-readonly docs-truth-check env-check varlock-run clean

PYTHON ?= python3
VARLOCK ?= varlock
WORK_PLAN_DEFAULT := docs/current-state/CURRENT-STATE-2026-07-16.md
EXPECT_VERSION_DEFAULT := 7.0.2
JAVASCRIPT_FILES := \
	plugins/kk-marquee-board/assets/marquee.js \
	scripts/marquee/render_og.cjs \
	theme/kk-aurora/assets/js/marquee.js \
	theme/kk-aurora/assets/js/micro-interactions.js \
	theme/kk-aurora/assets/js/theme.js

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
	@$(MAKE) python-test
	@$(MAKE) javascript-syntax
	@$(MAKE) plugin-smoke
	@$(MAKE) theme-smoke

python-test: ## Run all declared Python test suites
	@$(PYTHON) -c 'import dotenv, pytest, requests, yaml' || { \
		echo "ERROR: Python test dependencies are missing for $(PYTHON). Install requirements-test.txt."; \
		exit 1; \
	}
	@echo "Publisher unit tests"
	@$(PYTHON) -m unittest discover -s scripts/notion-to-wp/tests -v
	@echo "Operational unit tests"
	@$(PYTHON) -m unittest discover -s scripts/tests -v
	@echo "SEO inventory unit tests"
	@$(PYTHON) -m unittest discover -s scripts/seo-audit/tests -v
	@echo "SEO backfill and link-safety tests"
	@$(PYTHON) -m pytest scripts/seo-backfill/tests -q

javascript-syntax: ## Check committed JavaScript syntax
	@command -v node >/dev/null 2>&1 || { echo "ERROR: node is required for JavaScript syntax checks."; exit 1; }
	@for file in $(JAVASCRIPT_FILES); do node --check "$$file"; done

php-syntax: ## Run php -l across all tracked PHP in inc/, plugins/, theme/, fixes/
	@command -v php >/dev/null 2>&1 || { echo "ERROR: php is required for PHP syntax checks."; exit 1; }
	@status=0; count=0; \
	for file in $$(git ls-files 'inc/*.php' 'plugins/*.php' 'theme/*.php' 'fixes/*.php' | LC_ALL=C sort); do \
		count=$$((count + 1)); \
		out=$$(php -l "$$file" 2>&1) || { echo "$$out"; status=1; }; \
	done; \
	if [ "$$count" -eq 0 ]; then echo "ERROR: php-syntax found no tracked PHP files."; exit 1; fi; \
	if [ "$$status" -ne 0 ]; then echo "php-syntax: FAILED ($$count files checked)"; exit 1; fi; \
	echo "php-syntax: $$count files passed php -l"

plugin-smoke: ## Run lightweight plugin smoke tests
	@command -v php >/dev/null 2>&1 || { echo "ERROR: php is required for plugin smoke tests."; exit 1; }
	@php plugins/kk-sidebar-promos/tests/smoke.php
	@php plugins/kk-marquee-board/tests/smoke.php

theme-smoke: ## Run lightweight theme behavior smoke tests
	@command -v php >/dev/null 2>&1 || { echo "ERROR: php is required for theme smoke tests."; exit 1; }
	@php theme/kk-aurora/tests/seo-title-smoke.php

verify: ## Run the standard local verification suite
	@$(MAKE) test
	@$(MAKE) docs-truth-check
	@$(MAKE) validate

validate: ## Run PHP syntax gate plus WordPress coding standards check
	@$(MAKE) php-syntax
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

wp-package: ## Package a WP theme/plugin upload zip. Args: SOURCE KIND LABEL ROLLBACK_REF OUTPUT_DIR OPEN_ADMIN=1 COPY_PATH=1 REPORT=path
	@python3 scripts/package_wp_artifact.py \
		--source "$${SOURCE:-theme/kk-aurora}" \
		--kind "$${KIND:-theme}" \
		--label "$${LABEL:-release}" \
		--output-dir "$${OUTPUT_DIR:-$$HOME/Desktop}" \
		$${ROLLBACK_REF:+--rollback-ref "$${ROLLBACK_REF}"} \
		$${ROLLBACK_LABEL:+--rollback-label "$${ROLLBACK_LABEL}"} \
		$${OPEN_ADMIN:+--open-admin} \
		$${COPY_PATH:+--copy-path} \
		$${ALLOW_DIRTY:+--allow-dirty} \
		$${REPORT:+--report "$${REPORT}"}

aurora-package: ## Package KK Aurora for wp-admin upload. Args: LABEL ROLLBACK_REF OPEN_ADMIN=1 COPY_PATH=1
	@$(MAKE) wp-package SOURCE=theme/kk-aurora KIND=theme LABEL="$${LABEL:-aurora-release}" ROLLBACK_REF="$${ROLLBACK_REF:-}" ROLLBACK_LABEL="$${ROLLBACK_LABEL:-rollback}" OPEN_ADMIN="$${OPEN_ADMIN:-}" COPY_PATH="$${COPY_PATH:-}" REPORT="$${REPORT:-}"

sidebar-promos-package: ## Package KK Sidebar Promos plugin for wp-admin upload
	@$(MAKE) wp-package SOURCE=plugins/kk-sidebar-promos KIND=plugin LABEL="$${LABEL:-sidebar-promos}" ROLLBACK_REF="$${ROLLBACK_REF:-}" OPEN_ADMIN="$${OPEN_ADMIN:-}" COPY_PATH="$${COPY_PATH:-}" REPORT="$${REPORT:-}"

marquee-package: ## Package KK Marquee Board plugin for wp-admin upload
	@$(MAKE) wp-package SOURCE=plugins/kk-marquee-board KIND=plugin LABEL="$${LABEL:-marquee-board}" ROLLBACK_REF="$${ROLLBACK_REF:-}" OPEN_ADMIN="$${OPEN_ADMIN:-}" COPY_PATH="$${COPY_PATH:-}" REPORT="$${REPORT:-}"

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

seo-backfill: ## Additive-only SEO meta backfill (default DRY-RUN). Live: EXECUTE=1. Args: KIND LIMIT SINCE IDS ORDER FIELDS PROBE_ID BACKUP_DIR
	@scripts/notion-to-wp/.venv/bin/python scripts/seo-backfill/backfill_meta.py \
		$${EXECUTE:+--execute} \
		--kind "$${KIND:-post}" --order "$${ORDER:-recent}" --fields "$${FIELDS:-seo_title,meta_desc,social}" \
		$${LIMIT:+--limit $${LIMIT}} $${SINCE:+--since $${SINCE}} $${IDS:+--ids $${IDS}} \
		$${PROBE_ID:+--probe-id $${PROBE_ID}} $${BACKUP_DIR:+--backup-dir $${BACKUP_DIR}} \
		$${FROM_FILE:+--from-file $${FROM_FILE}}

public-image-audit: ## Audit public-rendered images (dry-run). Args: IDS URLS DEFAULT_URLS=1 CHECK_URLS=1 FORMAT OUTPUT
	@python3 scripts/public_image_audit.py \
		--kind "$${KIND:-post,page}" --limit "$${LIMIT:-50}" --since "$${SINCE:-2025-01-01}" \
		$${IDS:+--ids "$${IDS}"} $${URLS:+--urls "$${URLS}"} $${DEFAULT_URLS:+--default-urls} \
		$${CHECK_URLS:+--check-urls} --timeout "$${TIMEOUT:-20}" --format "$${FORMAT:-markdown}" $${OUTPUT:+--output "$${OUTPUT}"}

performance-audit: ## Run read-only public performance baseline. Args: ROUTES SAMPLES LONGFORM_URL FORMAT OUTPUT
	@python3 scripts/performance_audit.py \
		--base-url "$${BASE_URL:-https://kriskrug.co}" \
		--routes "$${ROUTES:-/,/about/,/blog/,/projects/,/work/}" \
		--samples "$${SAMPLES:-3}" --timeout "$${TIMEOUT:-30}" \
		$${LONGFORM_URL:+--longform-url "$${LONGFORM_URL}"} \
		--format "$${FORMAT:-markdown}" $${OUTPUT:+--output "$${OUTPUT}"}

jetpack-feedback-audit: ## Run PII-safe read-only Jetpack Forms feedback counts/routing audit (FORMAT=json)
	@if [ "$${FORMAT:-human}" = "json" ]; then \
		python3 scripts/jetpack_feedback_audit.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}" --json; \
	else \
		python3 scripts/jetpack_feedback_audit.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}"; \
	fi

wp7-smoke: ## Run read-only public WP rollout smoke checks (BASE_URL=https://kriskrug.co EXPECT_VERSION=7.0.2)
	@python3 scripts/wp7-public-smoke.py --base-url "$${BASE_URL:-https://kriskrug.co}" --timeout "$${REQUEST_TIMEOUT:-20}" $${EXPECT_VERSION:+--expect-version "$$EXPECT_VERSION"}

wp7-admin-readiness: ## Run authenticated read-only WP 7 readiness snapshot (ENV_FILE=scripts/notion-to-wp/.env)
	@python3 scripts/wp7-admin-readiness.py --env-file "$${ENV_FILE:-scripts/notion-to-wp/.env}"

current-state-drift-check: ## Compare declared current-state snapshot values vs live read-only checks
	@python3 scripts/check_current_state_drift.py --work-plan "$${WORK_PLAN:-$(WORK_PLAN_DEFAULT)}" --base-url "$${BASE_URL:-https://kriskrug.co}"

morning-truth: ## Run startup truth checks and write a timestamped markdown report
	@python3 scripts/morning_truth_report.py --work-plan "$${WORK_PLAN:-$(WORK_PLAN_DEFAULT)}" --base-url "$${BASE_URL:-https://kriskrug.co}" --expect-version "$${EXPECT_VERSION:-$(EXPECT_VERSION_DEFAULT)}" --request-timeout "$${REQUEST_TIMEOUT:-20}" --command-timeout "$${COMMAND_TIMEOUT:-120}"

status-readonly: ## Print startup truth checks without writing a report
	@python3 scripts/morning_truth_report.py --stdout --skip-fetch --work-plan "$${WORK_PLAN:-$(WORK_PLAN_DEFAULT)}" --base-url "$${BASE_URL:-https://kriskrug.co}" --expect-version "$${EXPECT_VERSION:-$(EXPECT_VERSION_DEFAULT)}" --request-timeout "$${REQUEST_TIMEOUT:-20}" --command-timeout "$${COMMAND_TIMEOUT:-120}"

env-check: ## Validate .env.schema via Varlock (soft-OK when secrets are absent)
	@if command -v "$(VARLOCK)" >/dev/null 2>&1; then \
		if $(VARLOCK) load --agent --show-all; then \
			echo "env-check: schema + resolved values OK"; \
		else \
			echo "env-check: schema is readable; one or more values are missing/unresolved."; \
			echo "This is expected in Cursor Cloud without secrets, or before local vault wiring."; \
			echo "Wire WP_USER / WP_APP_PASSWORD (and optional NOTION_TOKEN) via:"; \
			echo "  - gitignored .env.local with op(op://kk-dev/...) after enabling the 1Password plugin"; \
			echo "  - Cursor Cloud secrets / process env"; \
			echo "  - temporary scripts/notion-to-wp/.env cache (compat only)"; \
			echo "Then: $(VARLOCK) run --inject vars -- make status-readonly"; \
			exit 0; \
		fi; \
	else \
		echo "varlock not on PATH. Install: curl -sSfL https://varlock.dev/install.sh | sh -s"; \
		echo "Then: export PATH=\"\$${XDG_CONFIG_HOME:-\$$HOME/.config}/varlock/bin:\$$PATH\""; \
		echo "Schema contract is committed at .env.schema (readable without secrets)."; \
		exit 0; \
	fi

# Usage: make varlock-run CMD='make status-readonly'
# Prefer complex one-liners via the CLI directly:
#   varlock run --inject vars -- python3 -c '...'
varlock-run: ## Run CMD with Varlock-injected env (requires varlock + resolved secrets)
	@if ! command -v "$(VARLOCK)" >/dev/null 2>&1; then \
		echo "varlock not on PATH — see docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md"; \
		exit 1; \
	fi
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make varlock-run CMD='make status-readonly'"; \
		echo "Or:    varlock run --inject vars -- <command>"; \
		exit 1; \
	fi
	@$(VARLOCK) run --inject vars -- $(CMD)

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
	@echo "Secrets: see docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md (do not paste secrets into chat/git)."

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
