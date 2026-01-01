## Summary

<!-- Provide a brief description of what this PR does -->

## Related Issue

<!-- Link to the issue this PR addresses -->
Fixes #
Closes #
Relates to #

## Changes

<!-- List the main changes in this PR -->

-
-
-

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Performance improvement
- [ ] Accessibility improvement
- [ ] SEO improvement
- [ ] Content update
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)

## Testing

<!-- Describe how you tested this change -->

### Test Steps

1.
2.
3.

### Test Results

- [ ] All unit tests pass (`vendor/bin/phpunit`)
- [ ] WordPress Coding Standards pass (`phpcs --standard=WordPress-Extra`)
- [ ] No PHPCS errors or warnings
- [ ] Tested on multiple browsers
- [ ] Tested on mobile devices
- [ ] Tested with keyboard navigation
- [ ] Tested with screen reader (if applicable)

## Screenshots

<!-- Add screenshots or screen recordings for UI/UX changes -->

### Before

<!-- Screenshot or description of current state -->

### After

<!-- Screenshot or description of new state -->

## Performance Impact

<!-- Describe any performance implications -->

- [ ] No performance impact
- [ ] Improves performance
- [ ] May impact performance (explain below)

<!-- If there's a performance impact, explain: -->

## Accessibility Considerations

<!-- Describe accessibility testing and compliance -->

- [ ] No accessibility impact
- [ ] Improves accessibility
- [ ] Maintains WCAG 2.1 AA compliance
- [ ] Tested with keyboard navigation
- [ ] Tested with screen reader

<!-- Explain any accessibility changes: -->

## Deployment Notes

<!-- Any special considerations for deploying this change? -->

- [ ] No special deployment steps required
- [ ] Requires database migration
- [ ] Requires new environment variables
- [ ] Requires plugin updates
- [ ] Requires cache clearing

<!-- If special steps are needed, list them: -->

## Checklist

<!-- Check all items before requesting review -->

### Code Quality

- [ ] My code follows the WordPress Coding Standards
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have added/updated PHPDoc comments for all functions
- [ ] I have removed any debugging code or console.logs
- [ ] I have not introduced any new linting errors or warnings

### Security

- [ ] All inputs are properly sanitized
- [ ] All outputs are properly escaped
- [ ] Nonces are used for forms and AJAX requests
- [ ] Database queries use prepared statements
- [ ] No sensitive data is exposed in logs or errors

### Testing

- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested this change on multiple browsers
- [ ] I have tested this change on mobile devices

### Documentation

- [ ] I have updated the documentation accordingly
- [ ] I have updated the README if needed
- [ ] I have added inline code comments where necessary

### Review

- [ ] I have performed a self-review of my own code
- [ ] I have checked my code for typos and formatting issues
- [ ] I have ensured my commits have clear, descriptive messages

## Additional Notes

<!-- Any other information reviewers should know -->

---

## For Automated PRs

<!-- If this PR was created by an AI agent, fill this section -->

**Created by Agent**: <!-- e.g., Claude Implementer Agent -->
**Agent Task ID**: <!-- gh agent-task ID if applicable -->
**Automated Workflow Run**: <!-- Link to GitHub Actions run -->

### Automated Testing Results

<!-- Agent should fill this automatically -->

**PHPUnit Results**:
- Tests run:
- Assertions:
- Failures:
- Execution time:

**PHPCS Results**:
- Errors:
- Warnings:
- Standard: WordPress-Extra

**Code Review Agent Status**:
- [ ] Passed automated review
- [ ] Has review comments (see below)

---

**Note to Reviewers**: Even though this PR passed automated checks, please review thoroughly for edge cases, WordPress best practices, and code quality.
