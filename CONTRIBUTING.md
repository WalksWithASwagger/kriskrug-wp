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

By participating in this project, you agree to maintain a respectful, inclusive, and collaborative environment that aligns with Kris Krug's mission of building a responsible and inclusive AI future.

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Respect privacy and confidentiality
- Follow WordPress and open-source best practices

## How to Contribute

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
2. **Create a branch**: `feature/issue-123-short-description` or `fix/issue-456-bug-name`
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
- **auto-implement** - Ready for AI agent automation
- **needs-human-review** - Requires human attention
- **priority:high** - Urgent issue
- **priority:medium** - Important but not urgent
- **priority:low** - Nice to have

## Pull Request Process

### Before Submitting

- [ ] PHP/JS in `fixes/` and `inc/` follows WordPress Coding Standards (`phpcs --standard=WordPress` if you have it installed locally — no CI gate enforces this currently)
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

> The older GitHub Actions agent swarm (`.github/workflows/`) included automated PHPCS / test / reviewer steps. Those workflows are dormant in current sessions; PRs are reviewed manually.

## Coding Standards

### WordPress PHP Standards

We follow [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/):

```bash
# Install PHPCS and WordPress standards
composer global require wp-coding-standards/wpcs
phpcs --config-set installed_paths ~/.composer/vendor/wp-coding-standards/wpcs

# Check your code
phpcs --standard=WordPress-Extra path/to/file.php

# Auto-fix issues
phpcbf --standard=WordPress-Extra path/to/file.php
```

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
- **Architect mode (Track B):** Aurora v2 theme migration. Operates on `aurora/v2`.

See [`docs/current-state/TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md) for the decision rule.

**Safety rules every agent must follow** (post 2026-05-15 incident):
- Backup before destructive operations
- Slug-based idempotency for the Notion → WP connector (never PATCH without verified target)
- No theme file changes on `main` — that's Track B's branch only

## Development Workflow

### Local Setup

```bash
# Clone repository
git clone https://github.com/WalksWithASwagger/kriskrug-wp.git
cd kriskrug-wp

# Notion → WP publisher (Python)
cd scripts/notion-to-wp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Then see scripts/notion-to-wp/README.md for env vars + dry-run usage

# WordPress coding standards (optional, if you have PHPCS installed)
phpcs --standard=WordPress-Extra fixes/ inc/
```

> There is no `composer.json` or `vendor/` in this repo. There are no PHPUnit tests checked in. Anything in earlier docs that references `vendor/bin/phpunit` is a leftover from the original era-1 plan and should be ignored.

### Branch Naming

- Feature: `feature/issue-123-description`
- Bug Fix: `fix/issue-456-bug-name`
- Enhancement: `enhancement/issue-789-improvement`
- Documentation: `docs/issue-101-update-readme`

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

This repo does not currently have automated tests checked in. Validation is manual:

- **Content publishing:** dry-run the connector first (`--dry-run`), eyeball the rendered post on staging or with the WP REST API, then publish for real.
- **PHP snippets in `fixes/`:** paste into Code Snippets on prod, save as inactive, toggle on, watch Query Monitor / front-end behavior.
- **Aurora theme (Track B):** stand up on Cloudways or Local by Flywheel, render every post type (Make Culture and Your Taste are the stress tests per [`TWO-TRACK-MODEL.md`](docs/current-state/TWO-TRACK-MODEL.md)).

If/when a PHPUnit suite is added, this section will get updated.

## Getting Help

- **Questions?** Open an issue with the `question` label
- **Stuck?** Check existing issues and PRs for similar problems
- **General inquiries?** Visit [kriskrug.co](https://kriskrug.co/)

## Recognition

Contributors will be:
- Listed in release notes
- Credited in PR descriptions
- Recognized in the Kris Krug community

Thank you for helping build a better AI future for British Columbia!

---

**Remember**: Quality over quantity. Well-tested, accessible, secure code is more valuable than rushing features.
