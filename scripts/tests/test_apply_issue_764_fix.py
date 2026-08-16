"""Offline safety tests for the issue #764 WordPress apply helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_764_fix.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_764_fix", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def baseline(post_id: int) -> dict:
    path = MODULE.TARGETS[post_id]["dir"] / f"{post_id}-baseline-20260815.json"
    return json.loads(path.read_text(encoding="utf-8"))


def payload(post_id: int) -> str:
    path = MODULE.TARGETS[post_id]["dir"] / f"{post_id}-content-payload.html"
    return path.read_text(encoding="utf-8")


def run_main(*args: str) -> int:
    with mock.patch.object(sys, "argv", ["apply_issue_764_fix.py", *args]), mock.patch.object(
        MODULE, "auth_header", return_value="Basic offline-test"
    ):
        return MODULE.main()


class ApplyIssue764FixTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)

    def test_default_dry_run_performs_no_local_or_wordpress_writes(self):
        calls = []

        def fake_request(url, _header, body=None):
            calls.append((url, body))
            post_id = int(url.split("/posts/")[1].split("?")[0])
            return baseline(post_id)

        snapshot_dir = self.tmp_path / "snapshots"
        with mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir), mock.patch.object(
            MODULE, "request", side_effect=fake_request
        ):
            self.assertEqual(0, run_main())

        self.assertFalse(snapshot_dir.exists())
        self.assertTrue(calls)
        self.assertTrue(all(body is None for _, body in calls))

    def test_apply_preflights_every_target_before_first_write(self):
        calls = []
        ordered_ids = sorted(MODULE.TARGETS)

        def fake_request(url, _header, body=None):
            calls.append((url, body))
            post_id = int(url.split("/posts/")[1].split("?")[0])
            live = baseline(post_id)
            if post_id == ordered_ids[1]:
                live["content"]["raw"] += "<!-- concurrent edit -->"
            if body is not None:
                return {**live, "content": {"raw": body["content"]}}
            return live

        snapshot_dir = self.tmp_path / "snapshots"
        with mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir), mock.patch.object(
            MODULE, "request", side_effect=fake_request
        ), mock.patch.object(
            sys, "argv", ["apply_issue_764_fix.py", "--apply"]
        ), mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"):
            with self.assertRaisesRegex(SystemExit, "drifted"):
                MODULE.main()

        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_snapshots_every_target_before_first_wordpress_write(self):
        snapshot_dir = self.tmp_path / "snapshots"
        writes = []
        saved = {}
        calls = []
        get_urls = []

        def fake_request(url, _header, body=None):
            post_id = int(url.split("/posts/")[1].split("?")[0])
            live = baseline(post_id)
            if body is None:
                calls.append(("GET", post_id))
                get_urls.append(url)
                if post_id in saved:
                    live["content"]["raw"] = saved[post_id]
                return live

            snapshots = list(snapshot_dir.glob("*.json"))
            self.assertEqual(len(MODULE.TARGETS), len(snapshots))
            self.assertTrue(
                all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in snapshots)
            )
            writes.append(post_id)
            calls.append(("POST", post_id))
            saved[post_id] = body["content"]
            return {**live, "content": {"raw": body["content"]}}

        with mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir), mock.patch.object(
            MODULE, "request", side_effect=fake_request
        ):
            self.assertEqual(0, run_main("--apply"))

        self.assertEqual(sorted(MODULE.TARGETS), writes)
        ordered_ids = sorted(MODULE.TARGETS)
        self.assertEqual(
            [("GET", post_id) for post_id in ordered_ids]
            + [
                item
                for post_id in ordered_ids
                for item in (("POST", post_id), ("GET", post_id))
            ],
            calls,
        )
        self.assertTrue(all(url.endswith("?context=edit") for url in get_urls))

    def test_apply_fails_when_post_claims_success_but_fresh_get_disagrees(self):
        post_id = sorted(MODULE.TARGETS)[0]
        calls = []

        def fake_request(url, _header, body=None):
            calls.append(("POST" if body else "GET", url))
            live = baseline(post_id)
            if body is not None:
                return {**live, "content": {"raw": body["content"]}}
            return live

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request", side_effect=fake_request):
            self.assertEqual(1, run_main("--post-id", str(post_id), "--apply"))

        self.assertEqual(["GET", "POST", "GET"], [method for method, _ in calls])
        self.assertTrue(calls[-1][1].endswith("?context=edit"))

    def test_apply_fails_on_mismatched_post_response_even_if_fresh_get_matches(self):
        post_id = sorted(MODULE.TARGETS)[0]
        saved = False
        calls = []

        def fake_request(url, _header, body=None):
            nonlocal saved
            calls.append(("POST" if body else "GET", url))
            live = baseline(post_id)
            if body is not None:
                saved = True
                return live
            if saved:
                live["content"]["raw"] = payload(post_id)
            return live

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request", side_effect=fake_request):
            self.assertEqual(1, run_main("--post-id", str(post_id), "--apply"))

        self.assertEqual(["GET", "POST", "GET"], [method for method, _ in calls])
        self.assertTrue(calls[-1][1].endswith("?context=edit"))

    def test_apply_refuses_fresh_readback_slug_mismatch(self):
        post_id = sorted(MODULE.TARGETS)[0]
        wrote = False

        def fake_request(_url, _header, body=None):
            nonlocal wrote
            live = baseline(post_id)
            if body is not None:
                wrote = True
                return {**live, "content": {"raw": body["content"]}}
            if wrote:
                live["slug"] = "wrong-post"
                live["content"]["raw"] = payload(post_id)
            return live

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request", side_effect=fake_request):
            with self.assertRaisesRegex(SystemExit, "slug"):
                run_main("--post-id", str(post_id), "--apply")

    def test_restore_refuses_post_outside_allowlist_without_network_or_disk_write(self):
        restore_file = self.tmp_path / "untrusted.json"
        restore_file.write_text(
            json.dumps(
                {
                    "id": 99999,
                    "slug": "not-an-issue-764-target",
                    "modified_gmt": "2026-08-15T00:00:00",
                    "content": {"raw": "untrusted"},
                }
            ),
            encoding="utf-8",
        )
        snapshot_dir = self.tmp_path / "snapshots"

        with mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir), mock.patch.object(
            MODULE, "request"
        ) as request_mock, mock.patch.object(
            sys,
            "argv",
            ["apply_issue_764_fix.py", "--restore", str(restore_file), "--apply"],
        ), mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"):
            with self.assertRaisesRegex(SystemExit, "allowlist"):
                MODULE.main()

        request_mock.assert_not_called()
        self.assertFalse(snapshot_dir.exists())

    def test_restore_refuses_snapshot_slug_mismatch(self):
        post_id = sorted(MODULE.TARGETS)[0]
        snapshot = baseline(post_id)
        snapshot["slug"] = "wrong-post"
        restore_file = self.tmp_path / "wrong-slug.json"
        restore_file.write_text(json.dumps(snapshot), encoding="utf-8")

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request") as request_mock, mock.patch.object(
            sys,
            "argv",
            ["apply_issue_764_fix.py", "--restore", str(restore_file), "--apply"],
        ), mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"):
            with self.assertRaisesRegex(SystemExit, "slug"):
                MODULE.main()

        request_mock.assert_not_called()

    def test_restore_refuses_live_slug_or_hash_drift_before_write(self):
        post_id = sorted(MODULE.TARGETS)[0]
        restore_file = self.tmp_path / "baseline.json"
        restore_file.write_text(json.dumps(baseline(post_id)), encoding="utf-8")

        for live_mutation, expected in (
            (lambda live: live.update(slug="wrong-post"), "slug"),
            (
                lambda live: live["content"].update(
                    raw=payload(post_id) + "<!-- drift -->"
                ),
                "current body",
            ),
        ):
            calls = []

            def fake_request(url, _header, body=None):
                calls.append((url, body))
                live = baseline(post_id)
                live["content"]["raw"] = payload(post_id)
                live_mutation(live)
                return live

            snapshot_dir = self.tmp_path / expected.replace(" ", "-")
            with mock.patch.object(
                MODULE, "SNAPSHOT_DIR", snapshot_dir
            ), mock.patch.object(MODULE, "request", side_effect=fake_request), mock.patch.object(
                sys,
                "argv",
                ["apply_issue_764_fix.py", "--restore", str(restore_file), "--apply"],
            ), mock.patch.object(
                MODULE, "auth_header", return_value="Basic offline-test"
            ):
                with self.assertRaisesRegex(SystemExit, expected):
                    MODULE.main()

            self.assertTrue(all(body is None for _, body in calls))
            self.assertFalse(snapshot_dir.exists())

    def test_restore_takes_mode_0600_backup_of_current_body_before_write(self):
        post_id = sorted(MODULE.TARGETS)[0]
        original = baseline(post_id)
        restore_file = self.tmp_path / "baseline.json"
        restore_file.write_text(json.dumps(original), encoding="utf-8")
        current = {**original, "content": {"raw": payload(post_id)}}
        snapshot_dir = self.tmp_path / "snapshots"
        writes = []
        restored = False
        calls = []

        def fake_request(_url, _header, body=None):
            nonlocal restored
            if body is None:
                calls.append("GET")
                return original if restored else current
            backups = list(snapshot_dir.glob("*.json"))
            self.assertEqual(1, len(backups))
            self.assertEqual(
                current, json.loads(backups[0].read_text(encoding="utf-8"))
            )
            self.assertEqual(0o600, stat.S_IMODE(backups[0].stat().st_mode))
            writes.append(body)
            calls.append("POST")
            restored = True
            return {**original, "content": {"raw": body["content"]}}

        with mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir), mock.patch.object(
            MODULE, "request", side_effect=fake_request
        ):
            self.assertEqual(
                0, run_main("--restore", str(restore_file), "--apply")
            )

        self.assertEqual([{"content": original["content"]["raw"]}], writes)
        self.assertEqual(["GET", "POST", "GET"], calls)

    def test_restore_fails_when_post_claims_success_but_fresh_get_disagrees(self):
        post_id = sorted(MODULE.TARGETS)[0]
        original = baseline(post_id)
        restore_file = self.tmp_path / "baseline.json"
        restore_file.write_text(json.dumps(original), encoding="utf-8")
        current = {**original, "content": {"raw": payload(post_id)}}
        calls = []

        def fake_request(_url, _header, body=None):
            calls.append("POST" if body else "GET")
            if body is not None:
                return {**original, "content": {"raw": body["content"]}}
            return current

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request", side_effect=fake_request):
            self.assertEqual(
                1, run_main("--restore", str(restore_file), "--apply")
            )

        self.assertEqual(["GET", "POST", "GET"], calls)

    def test_restore_fails_on_mismatched_post_response_even_if_fresh_get_matches(self):
        post_id = sorted(MODULE.TARGETS)[0]
        original = baseline(post_id)
        restore_file = self.tmp_path / "baseline.json"
        restore_file.write_text(json.dumps(original), encoding="utf-8")
        current = {**original, "content": {"raw": payload(post_id)}}
        restored = False
        calls = []

        def fake_request(url, _header, body=None):
            nonlocal restored
            calls.append(("POST" if body else "GET", url))
            if body is not None:
                restored = True
                return current
            return original if restored else current

        with mock.patch.object(
            MODULE, "SNAPSHOT_DIR", self.tmp_path / "snapshots"
        ), mock.patch.object(MODULE, "request", side_effect=fake_request):
            self.assertEqual(
                1, run_main("--restore", str(restore_file), "--apply")
            )

        self.assertEqual(["GET", "POST", "GET"], [method for method, _ in calls])
        self.assertTrue(calls[-1][1].endswith("?context=edit"))


if __name__ == "__main__":
    unittest.main()
