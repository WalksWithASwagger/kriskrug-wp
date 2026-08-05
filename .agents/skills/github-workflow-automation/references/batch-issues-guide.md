# Batch Issues Guide

Complete guide to batch creating GitHub issues from JSON or CSV files.

## JSON Format

### Basic Structure

```json
{
  "issues": [
    {
      "title": "Issue title here",
      "body": "Detailed description of the issue",
      "labels": ["bug", "priority:high"],
      "assignees": ["username"],
      "milestone": "v1.0"
    }
  ]
}
```

### Alternative Structure (Direct Array)

```json
[
  {
    "title": "Issue title",
    "body": "Description",
    "labels": ["enhancement"]
  }
]
```

### Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | Yes | String | Issue title (non-empty) |
| `body` | Yes | String | Issue description (non-empty) |
| `labels` | No | Array of strings | Label names to apply |
| `assignees` | No | Array of strings | GitHub usernames to assign |
| `milestone` | No | String | Milestone name |

### Complete Example

```json
{
  "issues": [
    {
      "title": "Contact Form Not Working on Mobile",
      "body": "## Bug Description\n\nThe contact form doesn't submit on mobile Safari.\n\n## Steps to Reproduce\n1. Open site on iPhone\n2. Fill out form\n3. Click Submit\n\n## Expected\nForm submits\n\n## Actual\nNothing happens",
      "labels": ["bug", "priority:high", "mobile"],
      "assignees": ["maintainer"],
      "milestone": "Q1 2026"
    },
    {
      "title": "Add Dark Mode Support",
      "body": "Implement dark mode theme option for better accessibility and user preference.\n\n## Requirements\n- Toggle in settings\n- Remember user preference\n- Smooth transition",
      "labels": ["enhancement", "accessibility"],
      "assignees": []
    }
  ]
}
```

## CSV Format

### Basic Structure

```csv
title,body,labels,assignees,milestone
"Issue title","Issue description","bug,priority:high","username","v1.0"
```

### Field Reference

| Column | Required | Format | Description |
|--------|----------|--------|-------------|
| `title` | Yes | String | Issue title |
| `body` | Yes | String | Issue description |
| `labels` | No | Comma-separated | Label names |
| `assignees` | No | Comma-separated | GitHub usernames |
| `milestone` | No | String | Milestone name |

### Complete Example

```csv
title,body,labels,assignees,milestone
"Contact Form Not Working","Form doesn't submit on mobile Safari. Steps: 1. Open on iPhone 2. Fill form 3. Click Submit. Expected: submission. Actual: nothing.","bug,priority:high,mobile","maintainer","Q1 2026"
"Add Dark Mode","Implement dark mode with toggle in settings and user preference memory.","enhancement,accessibility","",""
"Improve Page Speed","Optimize images and lazy-load JavaScript for better performance.","performance,enhancement","",""
```

### CSV Best Practices

1. **Always include header row**
2. **Use quotes** for fields containing commas or newlines
3. **Escape quotes** by doubling them: `"She said ""Hello"""`
4. **Leave optional fields empty** but include the commas

## Usage Examples

### Validate Before Creating

```bash
# Validate JSON
python scripts/validate_input.py --input issues.json

# Validate CSV
python scripts/validate_input.py --input issues.csv
```

### Create Issues

```bash
# From JSON
python scripts/batch_create_issues.py --input issues.json

# From CSV
python scripts/batch_create_issues.py --input issues.csv

# Specify repository
python scripts/batch_create_issues.py --input issues.json --repo owner/repo

# Dry run (preview without creating)
python scripts/batch_create_issues.py --input issues.json --dry-run

# Save results
python scripts/batch_create_issues.py --input issues.json --output results.json
```

## Common Patterns

### Website Audit to Issues

1. Export audit findings to CSV/JSON
2. Include findings as issue descriptions
3. Tag with appropriate labels
4. Assign to team members

Example CSV:
```csv
title,body,labels,assignees,milestone
"Accessibility: Color Contrast","Audit found color contrast ratios below WCAG AA standards on navigation elements.","accessibility,priority:high","a11y-team",""
"Performance: Large Images","Homepage images are not optimized. Total page weight: 8MB.","performance,priority:medium","",""
"SEO: Missing Meta Tags","Several pages missing meta descriptions and Open Graph tags.","seo,priority:low","",""
```

### Feature Request Backlog

1. Collect feature requests
2. Organize by priority and type
3. Batch create with milestones

Example JSON:
```json
{
  "issues": [
    {
      "title": "User Dashboard",
      "body": "Create personalized dashboard for logged-in users",
      "labels": ["feature", "priority:high"],
      "milestone": "v2.0"
    },
    {
      "title": "Email Notifications",
      "body": "Send email notifications for important events",
      "labels": ["feature", "priority:medium"],
      "milestone": "v2.1"
    }
  ]
}
```

### Bug Triage Import

1. Export bugs from tracking system
2. Convert to JSON/CSV
3. Import with proper labels and assignments

## Error Handling

### Validation Errors

```bash
$ python scripts/validate_input.py --input issues.json

Errors:
  ✗ Issue 1: Missing 'title'
  ✗ Issue 3: 'body' must be non-empty string

✗ Validation failed
```

**Fix**: Ensure all required fields are present and non-empty.

### Creation Errors

```bash
$ python scripts/batch_create_issues.py --input issues.json

[1/3] Creating issue: Contact Form Bug
  ✓ Created: https://github.com/owner/repo/issues/1

[2/3] Creating issue: Invalid Issue
  ✗ Failed: Label 'nonexistent-label' not found

[3/3] Creating issue: Another Issue
  ✓ Created: https://github.com/owner/repo/issues/2

Summary:
  Total: 3
  Successful: 2
  Failed: 1
```

**Fix**: Verify labels exist before batch creation, or create labels first.

## Advanced Usage

### Template Variables

Create issue templates with placeholders:

```json
{
  "issues": [
    {
      "title": "Update ${component} Documentation",
      "body": "Documentation for ${component} needs to be updated.\n\nSections to update:\n${sections}",
      "labels": ["documentation"]
    }
  ]
}
```

Then replace variables programmatically before creating issues.

### Conditional Fields

Skip optional fields by using empty values:

```json
{
  "title": "Issue with no labels",
  "body": "Description",
  "labels": []
}
```

### Large Batch Operations

For 100+ issues:
1. Split into smaller batches (20-50 issues)
2. Add delays between batches to avoid rate limiting
3. Use `--output` to track progress
4. Resume from last successful issue if interrupted

## Tips

1. **Start with dry-run** to preview changes
2. **Validate first** to catch errors early
3. **Use descriptive titles** for better searchability
4. **Include context in body** - links, screenshots, code samples
5. **Tag appropriately** for easier filtering and workflows
6. **Assign strategically** - don't over-assign
7. **Group by milestone** for release planning
8. **Save results** for audit trail and retry logic

## Troubleshooting

**Issue: CSV parsing fails**
- Check for unescaped quotes
- Verify all rows have same number of columns
- Ensure UTF-8 encoding

**Issue: JSON parsing fails**
- Validate JSON syntax with JSON linter
- Check for trailing commas
- Ensure proper escaping of special characters

**Issue: Rate limiting**
- GitHub API limits: 5000 requests/hour
- Add delays between batches
- Authenticate with gh CLI for higher limits

**Issue: Labels don't exist**
- Create labels first with `gh label create`
- Or remove non-existent labels from input
- Use standard GitHub labels (bug, enhancement, etc.)

## Schema Validation

### JSON Schema (for advanced users)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "body"],
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1
          },
          "body": {
            "type": "string",
            "minLength": 1
          },
          "labels": {
            "type": "array",
            "items": {"type": "string"}
          },
          "assignees": {
            "type": "array",
            "items": {"type": "string"}
          },
          "milestone": {
            "type": "string"
          }
        }
      }
    }
  },
  "required": ["issues"]
}
```
