import csv
import json
import sys
import tempfile
import unittest
import unittest.mock
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

    def test_issue_exists_matches_exact_title_only(self):
        listing = json.dumps([{"title": "One extra"}, {"title": "One"}])
        completed = unittest.mock.Mock(stdout=listing)

        with patch("batch_create_issues.subprocess.run", return_value=completed):
            self.assertTrue(batch_create_issues.issue_exists("One"))
            self.assertFalse(batch_create_issues.issue_exists("On"))

    def test_main_skips_existing_title_and_creates_new_one(self):
        issues = [
            {"title": "Filed", "body": "Body"},
            {"title": "Fresh", "body": "Body"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issues.json"
            path.write_text(json.dumps(issues))

            def fake_run(cmd, **kwargs):
                if cmd[:3] == ["gh", "issue", "list"]:
                    search = cmd[cmd.index("--search") + 1]
                    titles = [{"title": "Filed"}] if search.startswith("Filed") else []
                    return unittest.mock.Mock(stdout=json.dumps(titles))
                return unittest.mock.Mock(stdout="https://github.com/o/r/issues/9\n")

            with patch(
                "batch_create_issues.subprocess.run", side_effect=fake_run
            ) as run:
                with patch.object(sys, "argv", ["x", "--input", str(path)]):
                    with self.assertRaises(SystemExit) as exit_info:
                        batch_create_issues.main()

        created = [
            c.args[0][c.args[0].index("--title") + 1]
            for c in run.call_args_list
            if c.args[0][:3] == ["gh", "issue", "create"]
        ]
        self.assertEqual(0, exit_info.exception.code)
        self.assertEqual(["Fresh"], created)

    def test_dry_run_never_queries_or_creates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issues.json"
            path.write_text(json.dumps([{"title": "One", "body": "Body"}]))

            with patch("batch_create_issues.subprocess.run") as run:
                with patch.object(
                    sys, "argv", ["x", "--input", str(path), "--dry-run"]
                ):
                    with self.assertRaises(SystemExit):
                        batch_create_issues.main()

        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
