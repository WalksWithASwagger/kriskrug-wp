#!/usr/bin/env python3
"""
Create GitHub pull request from issue(s) with automatic linking.
Uses gh CLI for all GitHub operations.
"""

import argparse
import json
import subprocess
import sys
from typing import List


def get_issue_details(issue_number: int, repo: str = None) -> dict:
    """Fetch issue details using gh CLI."""
    cmd = ['gh', 'issue', 'view', str(issue_number), '--json', 'number,title,body,labels']

    if repo:
        cmd.extend(['--repo', repo])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching issue #{issue_number}: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def generate_pr_body(issues: List[dict], custom_body: str = None) -> str:
    """Generate PR body with issue references."""
    body_parts = []

    # Add custom body if provided
    if custom_body:
        body_parts.append(custom_body)
        body_parts.append("")

    # Add issue references
    if len(issues) == 1:
        body_parts.append(f"Fixes #{issues[0]['number']}")
    else:
        body_parts.append("This PR addresses multiple issues:")
        for issue in issues:
            body_parts.append(f"- Fixes #{issue['number']}")

    body_parts.append("")

    # Add issue summaries
    if len(issues) == 1:
        body_parts.append("## Issue Summary")
        body_parts.append("")
        body_parts.append(issues[0].get('body', 'No description'))
    else:
        body_parts.append("## Issues Summary")
        for issue in issues:
            body_parts.append("")
            body_parts.append(f"### #{issue['number']}: {issue['title']}")
            body_parts.append("")
            # First 200 chars of body
            issue_body = issue.get('body', 'No description')
            if len(issue_body) > 200:
                issue_body = issue_body[:200] + "..."
            body_parts.append(issue_body)

    return "\n".join(body_parts)


def create_pr(
    issues: List[dict],
    title: str = None,
    body: str = None,
    base: str = 'main',
    draft: bool = False,
    repo: str = None
) -> dict:
    """Create pull request using gh CLI."""

    # Generate title if not provided
    if not title:
        if len(issues) == 1:
            title = f"Fix: {issues[0]['title']}"
        else:
            title = f"Fix multiple issues ({len(issues)} issues)"

    # Generate body
    pr_body = generate_pr_body(issues, body)

    # Build gh pr create command
    cmd = ['gh', 'pr', 'create', '--title', title, '--body', pr_body, '--base', base]

    if repo:
        cmd.extend(['--repo', repo])

    if draft:
        cmd.append('--draft')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        url = result.stdout.strip()

        # Extract PR number from URL
        pr_number = url.split('/')[-1]

        return {
            'number': int(pr_number),
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
        description='Create GitHub PR from issue(s) with automatic linking'
    )
    parser.add_argument('--issue', required=True, help='Issue number(s), comma-separated for multiple')
    parser.add_argument('--title', help='PR title (auto-generated if not provided)')
    parser.add_argument('--body', help='Custom PR body text')
    parser.add_argument('--base', default='main', help='Base branch (default: main)')
    parser.add_argument('--draft', action='store_true', help='Create as draft PR')
    parser.add_argument('--repo', help='Repository (owner/name) - uses current repo if not specified')

    args = parser.parse_args()

    # Parse issue numbers
    try:
        issue_numbers = [int(n.strip()) for n in args.issue.split(',')]
    except ValueError:
        print("Error: --issue must be number(s), e.g., 123 or 123,124,125", file=sys.stderr)
        sys.exit(1)

    # Fetch issue details
    print(f"Fetching details for {len(issue_numbers)} issue(s)...")
    issues = []
    for issue_num in issue_numbers:
        print(f"  - Issue #{issue_num}")
        issue_details = get_issue_details(issue_num, args.repo)
        issues.append(issue_details)

    print()

    # Create PR
    print(f"Creating pull request...")
    result = create_pr(
        issues=issues,
        title=args.title,
        body=args.body,
        base=args.base,
        draft=args.draft,
        repo=args.repo
    )

    if result.get('success'):
        print(f"✓ PR created successfully!")
        print(f"  URL: {result['url']}")
        print(f"  Number: #{result['number']}")
        print(f"  Title: {result['title']}")

        if args.draft:
            print(f"  Status: Draft")

        print(f"\nLinked issues:")
        for issue in issues:
            print(f"  - #{issue['number']}: {issue['title']}")

        sys.exit(0)
    else:
        print(f"✗ Failed to create PR: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
