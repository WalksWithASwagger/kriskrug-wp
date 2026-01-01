# Contributing to BC+AI WordPress Site

Thank you for your interest in contributing to the BC+AI WordPress site! This repository uses AI agent automation to streamline development, but we welcome both human and AI-assisted contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Agent Automation](#agent-automation)

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and collaborative environment that aligns with BC+AI's mission of building a responsible and inclusive AI future.

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
The Gravity Forms contact form (#3) does not submit on mobile Safari.

Steps to Reproduce:
1. Visit bc-ai.ca on iPhone (iOS 16)
2. Navigate to contact form
3. Fill out all fields
4. Tap Submit button
5. Nothing happens

Expected: Form submits and shows confirmation
Actual: No response, no error message

Environment:
- Browser: Mobile Safari 16.3
- Device: iPhone 13
- URL: https://bc-ai.ca/#contact

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

- [ ] All tests pass (`vendor/bin/phpunit`)
- [ ] Code follows WordPress Coding Standards (`phpcs --standard=WordPress`)
- [ ] No PHPCS errors or warnings
- [ ] Changes are documented in PR description
- [ ] Issue is linked (use `Fixes #123` or `Closes #456`)
- [ ] Commit messages are clear and descriptive

### PR Template

Your PR should include:

1. **Summary** - What does this PR do?
2. **Issue Reference** - `Fixes #123`
3. **Changes** - List of modifications
4. **Testing** - How to test your changes
5. **Screenshots** - For UI/UX changes
6. **Checklist** - Tests, linting, docs completed

### Review Process

1. **Automated checks** run (PHPCS, PHPUnit, security scans)
2. **AI reviewer** may provide initial feedback
3. **Human maintainer** reviews and approves
4. **Merge** once all checks pass and approved

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

## Agent Automation

### How It Works

This repository uses AI agents to automate issue-to-PR workflows:

1. **Create an issue** with clear requirements
2. **Add label** `auto-implement` when ready
3. **Agent swarm activates**:
   - Analyzes issue
   - Writes tests (TDD)
   - Implements solution
   - Runs all tests
   - Creates PR if tests pass
4. **Review and merge** the generated PR

### When to Use Automation

**Good candidates:**
- Bug fixes with clear reproduction steps
- Feature additions with detailed specs
- Code refactoring with specific goals
- Performance optimizations
- Accessibility improvements

**Not suitable:**
- Vague or unclear requirements
- Major architectural changes
- Security-critical modifications (needs human review)
- Content changes requiring editorial judgment

### Working with Agent-Generated PRs

- Review thoroughly even though tests pass
- Check for edge cases the agent might have missed
- Verify WordPress best practices are followed
- Ensure documentation is complete
- Test manually on staging if possible

## Development Workflow

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/WalksWithASwagger/bc-ai-wp.git
cd bc-ai-wp

# Install dependencies
composer install

# Run tests
vendor/bin/phpunit

# Check coding standards
phpcs --standard=WordPress-Extra
```

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

### Running Tests

```bash
# All tests
vendor/bin/phpunit

# Specific test file
vendor/bin/phpunit tests/test-api-cache.php

# With coverage
vendor/bin/phpunit --coverage-html coverage/
```

### Writing Tests

- Extend `WP_UnitTestCase` for WordPress tests
- Use factory methods for test data
- Clean up after each test
- Test both success and failure cases
- Mock external API calls

## Getting Help

- **Questions?** Open an issue with the `question` label
- **Stuck?** Check existing issues and PRs for similar problems
- **Bug in automation?** Label it `automation-bug`
- **General inquiries?** Visit [bc-ai.ca](https://bc-ai.ca/)

## Recognition

Contributors will be:
- Listed in release notes
- Credited in PR descriptions
- Recognized in the BC+AI community

Thank you for helping build a better AI future for British Columbia!

---

**Remember**: Quality over quantity. Well-tested, accessible, secure code is more valuable than rushing features.
