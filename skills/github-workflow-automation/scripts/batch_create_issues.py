#!/usr/bin/env python3
"""
Batch create GitHub issues from JSON or CSV files.
Uses gh CLI for all GitHub operations.
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Load issues from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Support both {"issues": [...]} and direct array
    if isinstance(data, dict) and 'issues' in data:
        return data['issues']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("JSON must be array or object with 'issues' key")


def load_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load issues from CSV file."""
    issues = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Split comma-separated labels
            if 'labels' in row and row['labels']:
                row['labels'] = [l.strip() for l in row['labels'].split(',')]
            else:
                row['labels'] = []

            # Split comma-separated assignees
            if 'assignees' in row and row['assignees']:
                row['assignees'] = [a.strip() for a in row['assignees'].split(',')]
            else:
                row['assignees'] = []

            issues.append(row)

    return issues


def validate_issue(issue: Dict[str, Any]) -> List[str]:
    """Validate issue has required fields. Returns list of errors."""
    errors = []

    if 'title' not in issue or not issue['title']:
        errors.append("Missing required field: title")

    if 'body' not in issue or not issue['body']:
        errors.append("Missing required field: body")

    return errors


def create_issue(issue: Dict[str, Any], repo: str = None, dry_run: bool = False) -> Dict[str, Any]:
    """Create a single GitHub issue using gh CLI."""
    title = issue['title']
    body = issue['body']
    labels = issue.get('labels', [])
    assignees = issue.get('assignees', [])
    milestone = issue.get('milestone')

    # Build gh issue create command
    cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]

    if repo:
        cmd.extend(['--repo', repo])

    if labels:
        for label in labels:
            cmd.extend(['--label', label])

    if assignees:
        for assignee in assignees:
            cmd.extend(['--assignee', assignee])

    if milestone:
        cmd.extend(['--milestone', milestone])

    if dry_run:
        print(f"[DRY RUN] Would create issue: {title}")
        print(f"  Labels: {', '.join(labels)}")
        print(f"  Assignees: {', '.join(assignees)}")
        if milestone:
            print(f"  Milestone: {milestone}")
        return {'number': 0, 'url': 'dry-run', 'title': title}

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        url = result.stdout.strip()

        # Extract issue number from URL
        issue_number = url.split('/')[-1]

        return {
            'number': int(issue_number),
            'url': url,
            'title': title,
            'success': True
        }
    except subprocess.CalledProcessError as e:
        return {
            'title': title,
            'success': False,
            'error': e.stderr
        }


def main():
    parser = argparse.ArgumentParser(
        description='Batch create GitHub issues from JSON or CSV'
    )
    parser.add_argument('--input', required=True, help='Input file (JSON or CSV)')
    parser.add_argument('--format', choices=['json', 'csv'], help='File format (auto-detected if not specified)')
    parser.add_argument('--repo', help='Repository (owner/name) - uses current repo if not specified')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating issues')
    parser.add_argument('--output', help='Output file for results (JSON)')

    args = parser.parse_args()

    # Auto-detect format from file extension
    file_path = Path(args.input)
    if not file_path.exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    format_type = args.format
    if not format_type:
        if file_path.suffix.lower() == '.json':
            format_type = 'json'
        elif file_path.suffix.lower() == '.csv':
            format_type = 'csv'
        else:
            print(f"Error: Cannot auto-detect format. Use --format", file=sys.stderr)
            sys.exit(1)

    # Load issues
    print(f"Loading issues from {args.input} ({format_type})...")
    try:
        if format_type == 'json':
            issues = load_json(args.input)
        else:
            issues = load_csv(args.input)
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(issues)} issue(s)")

    # Validate all issues first
    validation_errors = []
    for i, issue in enumerate(issues, 1):
        errors = validate_issue(issue)
        if errors:
            validation_errors.append(f"Issue {i}: {', '.join(errors)}")

    if validation_errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in validation_errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    # Create issues
    results = []
    successful = 0
    failed = 0

    for i, issue in enumerate(issues, 1):
        print(f"\n[{i}/{len(issues)}] Creating issue: {issue['title']}")
        result = create_issue(issue, args.repo, args.dry_run)
        results.append(result)

        if result.get('success', True):  # dry-run doesn't set success key
            successful += 1
            if not args.dry_run:
                print(f"  ✓ Created: {result['url']}")
        else:
            failed += 1
            print(f"  ✗ Failed: {result.get('error', 'Unknown error')}", file=sys.stderr)

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total: {len(issues)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")

    # Save results to file if requested
    if args.output:
        output_data = {
            'total': len(issues),
            'successful': successful,
            'failed': failed,
            'results': results
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    # Exit with error code if any failed
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
