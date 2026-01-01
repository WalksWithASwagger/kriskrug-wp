#!/usr/bin/env python3
"""
Validate JSON/CSV input files before processing.
Checks format, required fields, and data types.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


def validate_json_structure(data: Any) -> Tuple[bool, List[str]]:
    """Validate JSON structure. Returns (is_valid, errors)."""
    errors = []

    # Must be list or dict with 'issues' key
    if isinstance(data, list):
        issues = data
    elif isinstance(data, dict) and 'issues' in data:
        issues = data['issues']
    else:
        return False, ["JSON must be array or object with 'issues' key"]

    if not isinstance(issues, list):
        return False, ["'issues' must be an array"]

    if len(issues) == 0:
        errors.append("No issues found in file")

    return True, errors


def validate_issue_fields(issue: Dict[str, Any], index: int) -> List[str]:
    """Validate individual issue fields. Returns list of errors."""
    errors = []
    prefix = f"Issue {index}"

    # Required fields
    if 'title' not in issue:
        errors.append(f"{prefix}: Missing 'title'")
    elif not isinstance(issue['title'], str) or not issue['title'].strip():
        errors.append(f"{prefix}: 'title' must be non-empty string")

    if 'body' not in issue:
        errors.append(f"{prefix}: Missing 'body'")
    elif not isinstance(issue['body'], str) or not issue['body'].strip():
        errors.append(f"{prefix}: 'body' must be non-empty string")

    # Optional but validated if present
    if 'labels' in issue:
        if not isinstance(issue['labels'], list):
            errors.append(f"{prefix}: 'labels' must be array")
        elif not all(isinstance(l, str) for l in issue['labels']):
            errors.append(f"{prefix}: All labels must be strings")

    if 'assignees' in issue:
        if not isinstance(issue['assignees'], list):
            errors.append(f"{prefix}: 'assignees' must be array")
        elif not all(isinstance(a, str) for a in issue['assignees']):
            errors.append(f"{prefix}: All assignees must be strings")

    if 'milestone' in issue:
        if not isinstance(issue['milestone'], str):
            errors.append(f"{prefix}: 'milestone' must be string")

    return errors


def validate_json(file_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate JSON file. Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"], []
    except Exception as e:
        return False, [f"Error reading file: {e}"], []

    # Validate structure
    valid, struct_errors = validate_json_structure(data)
    if not valid:
        return False, struct_errors, []

    errors.extend(struct_errors)

    # Get issues array
    if isinstance(data, list):
        issues = data
    else:
        issues = data['issues']

    # Validate each issue
    for i, issue in enumerate(issues, 1):
        issue_errors = validate_issue_fields(issue, i)
        errors.extend(issue_errors)

    # Check for duplicate titles (warning only)
    titles = [issue.get('title', '') for issue in issues]
    duplicates = set([t for t in titles if titles.count(t) > 1 and t])
    if duplicates:
        warnings.append(f"Duplicate titles found: {', '.join(duplicates)}")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def validate_csv(file_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate CSV file. Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)

            # Check required columns
            if not reader.fieldnames:
                return False, ["CSV file is empty or has no header"], []

            required_cols = {'title', 'body'}
            missing_cols = required_cols - set(reader.fieldnames)
            if missing_cols:
                return False, [f"Missing required columns: {', '.join(missing_cols)}"], []

            # Validate each row
            issues = list(reader)
            if len(issues) == 0:
                warnings.append("No data rows found in CSV")

            for i, issue in enumerate(issues, 1):
                if not issue.get('title', '').strip():
                    errors.append(f"Row {i}: Empty title")
                if not issue.get('body', '').strip():
                    errors.append(f"Row {i}: Empty body")

    except Exception as e:
        return False, [f"Error reading CSV: {e}"], []

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description='Validate JSON/CSV input files for batch issue creation'
    )
    parser.add_argument('--input', required=True, help='Input file to validate')
    parser.add_argument('--format', choices=['json', 'csv'], help='File format (auto-detected if not specified)')

    args = parser.parse_args()

    # Auto-detect format
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
            print(f"Error: Cannot auto-detect format from {file_path.suffix}. Use --format", file=sys.stderr)
            sys.exit(1)

    print(f"Validating {args.input} ({format_type})...")
    print()

    # Validate based on format
    if format_type == 'json':
        is_valid, errors, warnings = validate_json(args.input)
    else:
        is_valid, errors, warnings = validate_csv(args.input)

    # Print results
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  ✗ {error}")
        print()

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()

    if is_valid:
        print("✓ Validation passed")
        sys.exit(0)
    else:
        print("✗ Validation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
