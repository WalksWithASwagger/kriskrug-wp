import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import batch_create_issues


class BatchCreateIssuesTests(unittest.TestCase):
    def test_load_json_accepts_wrapped_issue_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issues.json"
            path.write_text(json.dumps({"issues": [{"title": "One", "body": "Body"}]}))

            self.assertEqual(
                "One", batch_create_issues.load_json(str(path))[0]["title"]
            )

    def test_load_csv_normalizes_labels_and_assignees(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issues.csv"
            with path.open("w", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["title", "body", "labels", "assignees"]
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "title": "One",
                        "body": "Body",
                        "labels": "bug, content",
                        "assignees": "octocat",
                    }
                )

            issue = batch_create_issues.load_csv(str(path))[0]

            self.assertEqual(["bug", "content"], issue["labels"])
            self.assertEqual(["octocat"], issue["assignees"])

    def test_validate_issue_rejects_invalid_boundary_types(self):
        errors = batch_create_issues.validate_issue(
            {"title": "", "body": "Body", "labels": "bug", "milestone": 1}
        )

        self.assertEqual(
            [
                "'title' must be a non-empty string",
                "'labels' must be an array of strings",
                "'milestone' must be a string",
            ],
            errors,
        )

    def test_dry_run_does_not_call_github(self):
        issue = {"title": "One", "body": "Body", "labels": [], "assignees": []}

        with patch("batch_create_issues.subprocess.run") as run:
            result = batch_create_issues.create_issue(issue, dry_run=True)

        run.assert_not_called()
        self.assertEqual("dry-run", result["url"])


if __name__ == "__main__":
    unittest.main()
