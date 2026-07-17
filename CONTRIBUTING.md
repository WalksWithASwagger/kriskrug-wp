# Contributing to kriskrug-wp

Thank you for your interest in contributing to the [kriskrug.co](https://kriskrug.co/) operations repo. We welcome both human contributors and AI-assisted contributions.

**If you're an AI agent, read [`AGENTS.md`](AGENTS.md) and [`docs/current-state/README.md`](docs/current-state/README.md) first to understand the two-track operating model.**

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Agent Automation](#agent-automation)

## Code of Conduct

By participating in this project, you agree to keep this a respectful, inclusive, and collaborative place to work. This is the operations repo for Kris Krug's personal site; treat it and the people around it with care.

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Respect privacy and confidentiality
- Follow WordPress and open-source best practices

## How to Contribute

### Secrets / Varlock (local + Cloud)

Do **not** commit plaintext secrets. Canonical store is your vault (1Password `kk-dev`); this repo’s contract is [`.env.schema`](.env.schema).

1. Install Varlock: `curl -sSfL https://varlock.dev/install.sh | sh -s` and put `~/.config/varlock/bin` on `PATH`
2. Read [`docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md`](docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md)
3. `make env-check` (soft-OK without secrets)
4. Prefer `make varlock-run CMD='make status-readonly'` over maintaining plaintext `scripts/notion-to-wp/.env`
5. Cursor Cloud needs the **same** values injected as Cloud secrets — laptop Varlock does not reach remote agents

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** for bugs, features, or accessibility concerns
3. **Provide details**: Clear description, steps to reproduce, expected vs actual behavior
4. **Add labels**: Help us categorize your issue appropriately

### Suggesting Enhancements

- Open a feature request using the feature template
- Describe the problem you're solving
- Explain your proposed solution
- Consider accessibility, performance, and SEO implications

### Code Contributions

1. **Fork the repository**
2. **Create a lane-scoped branch from `main`**: `fix/issue-456-bug-name`, `docs/issue-101-update-readme`, or an agent-lane branch like `codex/...` or `cursor/...` (see [Branch Naming](#branch-naming))
3. **Make your changes** following our coding standards
4. **Test thoroughly** - all tests must pass
5. **Submit a pull request** using our PR template

## Issue Guidelines

### Creating Quality Issues

**Good Issue:**
```
Title: Contact form submission fails on mobile devices

Description:
The contact form does not submit on mobile Safari.

Steps to Reproduce:
1. Visit kriskrug.co on iPhone (iOS 16)
2. Navigate to contact form
3. Fill out all fields
4. Tap Submit button
5. Nothing happens

Expected: Form submits and shows confirmation
Actual: No response, no error message

Environment:
- Browser: Mobile Safari 16.3
- Device: iPhone 13
- URL: https://kriskrug.co/#contact

Labels: bug, priority:high, mobile
```

### Issue Labels

- **bug** - Something is broken
- **enhancement** - New feature or improvement
- **accessibility** - A11y and WCAG compliance
- **performance** - Speed and optimization
- **seo** - Search engine optimization
- **content** - Content or UX improvements
- **documentation** - Docs need updates
- **auto-implement** - Historical automation-intent label; does not trigger the parked `agent-pr-generator` workflow
- **needs-human-review** - Requires human attention
- **priority:high** - Urgent issue
- **priority:medium** - Important but not urgent
- **priority:low** - Nice to have

## Pull Request Process

### Before Submitting

- [ ] Run `composer install` once, then `make verify` before opening a PR with code changes
- [ ] Changes are documented in PR description
- [ ] Issue is linked (use `Fixes #123` or `Closes #456`)
- [ ] Commit messages are clear and descriptive
- [ ] If you changed content via the Notion → WP publisher, you ran with `--dry-run` first and confirmed the slug-based idempotency match (see [`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`](docs/current-state/INCIDENT-2026-05-15-overwritten-post.md))

### PR Template

Your PR should include:

1. **Summary** - What does this PR do?
2. **Issue Reference** - `Fixes #123`
3. **Changes** - List of modifications
4. **Testing** - How to test your changes
5. **Screenshots** - For UI/UX changes
6. **Checklist** - Tests, linting, docs completed

### Review Process

1. **Human maintainer** (KK) reviews and approves
2. **Merge** once approved

> The older GitHub Actions agent swarm is parked (`agent-pr-generator.yml` is read-only and no longer label-triggered). `test-pr.yml` still runs as active PR validation; maintainers still do human review/approval.

## Coding Standards

### WordPress PHP Standards

We follow [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/):

Use the repo-owned PHPCS/WPCS setup rather than global standards:

```bash
composer install
make validate
```

The default ruleset is intentionally focused on high-signal WordPress security checks for production PHP. Do not broaden it to full formatting cleanup without a dedicated refactor PR.

### Key Requirements

**Security:**
- Sanitize all inputs (`sanitize_text_field()`, `esc_url()`, etc.)
- Escape all outputs (`esc_html()`, `esc_attr()`, etc.)
- Use nonces for forms (`wp_nonce_field()`, `wp_verify_nonce()`)
- Use prepared statements for database queries

**Documentation:**
- All functions must have PHPDoc comments
- Include `@param`, `@return`, `@since` tags
- Document complex logic with inline comments

**Naming Conventions:**
- Functions: `prefix_function_name()`
- Classes: `Prefix_Class_Name`
- Variables: `$variable_name`
- Constants: `PREFIX_CONSTANT_NAME`

### JavaScript Standards

- Use ES6+ syntax where supported
- Follow WordPress JavaScript Coding Standards
- Include JSDoc comments for functions
- Use meaningful variable and function names

### Accessibility Standards

- Meet WCAG 2.1 AA compliance
- Test with keyboard navigation
- Verify screen reader compatibility
- Ensure proper color contrast (4.5:1 minimum)
- Use semantic HTML5 elements
- Include alt text for images

## Agent Sessions (current model)

Day-to-day work happens through Claude Code / Cursor agent sessions, not via the dormant GitHub Actions agent swarm. Two modes:

- **Publisher mode (Track A):** Notion → kriskrug.co publishing, content enrichment, schema/SEO tweaks. Operates on `main`.
- **Architect mode (Track B):** Aurora theme maintenance. Start from `main` on a lane-scoped `codex/...` branch; use `aurora/v3-reconcile` and `aurora/v2` only as historical/evidence branches unless a dated handoff explicitly revives one.

See [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) for the decision rule.

**Safety rules every agent must follow** (post 2026-05-15 incident):
- Backup before destructive operations
- Slug-based idempotency for the Notion → WP connector (never PATCH without verified target)
- Theme file changes happen in focused Track B PR branches from `main`; do not mix them with Track A content publishing changes.

## Development Workflow

### Local Setup

There is no local app server to boot. The live site runs on Pagely and is not file-synced here. Local work means running the CLI tools and the validation gates below.

CI runs the gates on PHP 8.2, Python 3.12, and Node 20 (pinned in [`.github/workflows/test-pr.yml`](.github/workflows/test-pr.yml)). The Aurora theme declares a minimum of PHP 8.0 in [`theme/kk-aurora/style.css`](theme/kk-aurora/style.css). You don't need exact version matches locally, but if a gate behaves differently than CI, check your runtime versions first.

```bash
# Clone repository
git clone https://github.com/WalksWithASwagger/kriskrug-wp.git
cd kriskrug-wp

# Full Python test gate (repo root)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-test.txt
make python-test PYTHON=python

# Notion → WP publisher (its own venv; several Makefile targets call it directly)
cd scripts/notion-to-wp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd ../..
# Then see scripts/notion-to-wp/README.md for env vars + dry-run usage

# WordPress PHP validation
composer install
make verify
```

> `vendor/` is local-only and ignored. The repo owns `composer.json`, `composer.lock`, and `phpcs.xml.dist` so local and CI validation use the same PHPCS/WPCS baseline.

### Branch Naming

All work branches from current `main`, one lane per branch. Agent sessions use their lane prefix so it is obvious which tool owns the branch:

- Agent lanes: `codex/short-description`, `cursor/short-description`, `claude/issue-123-short-description`
- Bug fix: `fix/issue-456-bug-name`
- Documentation: `docs/issue-101-update-readme`
- Feature: `feature/issue-123-description`

Keep one issue per branch and don't mix Track A content changes with Track B theme changes in the same branch.

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Fix contact form validation on mobile devices"
- "Add caching for API responses using transients"
- "Improve accessibility of navigation menu"

Bad:
- "fix bug"
- "updates"
- "changes"
```

## Testing

This repo has focused automated tests for the Notion publisher safety guards, plus manual validation for production-adjacent WordPress changes.

Automated tests:

- `scripts/notion-to-wp/.venv/bin/python -m unittest discover -s scripts/notion-to-wp/tests -v`
- `make test` (runs the Notion publisher tests plus the sidebar promo smoke test)
- `make validate` (runs the focused WordPress PHP security ruleset)
- `make verify` (runs the standard local gate)

Manual validation:

- **Content publishing:** dry-run the connector first (`--dry-run`), eyeball the rendered post on staging or with the WP REST API, then publish for real.
- **PHP snippets in `fixes/`:** paste into Code Snippets on prod, save as inactive, toggle on, watch Query Monitor / front-end behavior.
- **Aurora theme (Track B):** production is Pagely-hosted; Cloudways staging was planned and never used as the default path (see AGENTS.md historical notes). Prefer Local by Flywheel / public smoke / package-then-upload when rendered proof is needed, then render every post type (Make Culture and Your Taste are the stress tests per [`TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md)).

If broader automated coverage is added (for example PHPUnit, Playwright, or end-to-end staging checks), extend this section with exact run commands.

## Getting Help

- **Questions?** Open an issue with the `question` label
- **Stuck?** Check existing issues and PRs for similar problems
- **General inquiries?** Visit [kriskrug.co](https://kriskrug.co/)

## Recognition

Contributors will be:
- Listed in release notes
- Credited in PR descriptions

Thanks for helping keep kriskrug.co healthy.

---

**Remember**: Quality over quantity. Well-tested, accessible, secure code is more valuable than rushing features.
