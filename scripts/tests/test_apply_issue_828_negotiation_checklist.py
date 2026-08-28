"""Offline safety tests for the issue #828 negotiation checklist package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_828_negotiation_checklist.py"
SPEC = importlib.util.spec_from_file_location(
    "apply_issue_828_negotiation_checklist", SCRIPT
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()


def spec_by_id(item_id: int) -> dict:
    return next(row for row in TARGETS["items"] if row["id"] == item_id)


def before_body(item_id: int) -> str:
    return MODULE.load_before_body(spec_by_id(item_id))


def fake_item(spec: dict, *, raw: str | None = None, slug: str | None = None) -> dict:
    return {
        "id": spec["id"],
        "slug": slug or spec["slug"],
        "type": "page" if spec["kind"] == "pages" else "post",
        "status": "publish",
        "title": {"raw": spec.get("title", "")},
        "date": spec.get("date", "2007-04-10T14:54:00"),
        "categories": spec.get("categories", []),
        "tags": spec.get("tags", []),
        "content": {"raw": raw if raw is not None else before_body(spec["id"])},
    }


def run_main(*args: str) -> int:
    with (
        mock.patch.object(
            sys, "argv", ["apply_issue_828_negotiation_checklist.py", *args]
        ),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue828NegotiationChecklistTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_item(row) for row in TARGETS["items"]}

    def _patch_request(self, calls):
        def fake_request(url, _header, payload=None):
            calls.append((url, payload))
            kind = "pages" if "/pages/" in url else "posts"
            item_id = int(url.split(f"/{kind}/")[1].split("?")[0])
            live = json.loads(json.dumps(self.lives[item_id]))
            if payload is not None:
                live["content"] = {"raw": payload["content"]}
                self.lives[item_id] = live
            return live

        return fake_request

    def test_targets_own_rows_34_through_37_and_exact_identities(self):
        self.assertEqual(
            [row["id"] for row in TARGETS["items"]], [1210, 12013, 1222, 1056]
        )
        self.assertEqual(
            spec_by_id(1210)["slug"],
            "checklist-of-model-photographer-negotiation-items",
        )
        self.assertEqual(spec_by_id(12013)["slug"], "photography")
        self.assertEqual(
            spec_by_id(1222)["slug"], "to-all-you-wannabe-fashion-photographers"
        )
        self.assertEqual(spec_by_id(1056)["slug"], "kk-on-modelmayhemcom")
        anchors = [
            (anchor["row"], anchor["text"], anchor["href"])
            for spec in TARGETS["items"]
            for anchor in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (
                    37,
                    "twenty years of shooting since I wrote this",
                    "https://kriskrug.co/photography/",
                ),
                (
                    34,
                    "the negotiation checklist I wrote in 2007 and still stand behind",
                    "https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/",
                ),
                (
                    35,
                    "the checklist version of this rant",
                    "https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/",
                ),
                (
                    36,
                    "the one useful thing I posted over there",
                    "https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/",
                ),
            ],
        )

    def test_draft_is_substantive_grounded_and_covers_every_required_topic(self):
        draft = MODULE.load_draft_body()
        summary = MODULE.validate_draft_body(draft, TARGETS)
        self.assertGreaterEqual(summary["word_count"], 400)
        self.assertEqual(summary["covered_topics"], set(TARGETS["required_topics"]))
        self.assertIn("ModelMayhem forum thread", draft)
        self.assertIn("Wayback Machine has no copy", draft)
        self.assertNotIn(TARGETS["dead_href"], draft)
        self.assertNotIn("legal advice", draft.lower())
        self.assertNotIn("\u2014", draft)
        self.assertNotIn("\u2013", draft)
        self.assertNotIn("synergy", draft.lower())
        self.assertNotIn("thought leader", draft.lower())

    def test_rewrite_1210_replaces_dead_stub_and_preserves_footer(self):
        spec = spec_by_id(1210)
        before = before_body(1210)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(before.count(TARGETS["dead_href"]), 1)
        self.assertNotIn(TARGETS["dead_href"], after)
        self.assertEqual(
            MODULE.collection_footer(before), MODULE.collection_footer(after)
        )
        self.assertEqual(after.count("kk-collection-footer"), 2)
        self.assertEqual(after.count("twenty years of shooting since I wrote this"), 1)
        self.assertLess(
            after.find("twenty years of shooting since I wrote this"),
            after.find("kk-collection-footer"),
        )
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_three_spokes_is_exact_and_preserves_owned_surfaces(self):
        for item_id in (12013, 1222, 1056):
            with self.subTest(item_id=item_id):
                spec = spec_by_id(item_id)
                before = before_body(item_id)
                after = MODULE.rewrite_body(before, spec, TARGETS)
                self.assertIsNotNone(after)
                anchor = spec["anchors"][0]
                needle = f'<a href="{anchor["href"]}">{anchor["text"]}</a>'
                self.assertEqual(after.count(needle), 1)
                self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))
                if spec.get("preserve_footer"):
                    self.assertEqual(
                        before.count("kk-collection-footer"),
                        after.count("kk-collection-footer"),
                    )
                if spec.get("preserve_style"):
                    self.assertEqual(
                        MODULE.style_sha256(before), MODULE.style_sha256(after)
                    )

    def test_missing_or_duplicate_needle_aborts(self):
        spec = spec_by_id(1056)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>wrong body</p>", spec, TARGETS)
        duplicate = before_body(1056) + spec["find"]
        with self.assertRaises(ValueError):
            MODULE.rewrite_body(duplicate, spec, TARGETS)

    def test_from_files_validates_committed_after_payloads_without_network(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            self.assertEqual(0, run_main("--from-files"))
        self.assertEqual(calls, [])
        for spec in TARGETS["items"]:
            self.assertEqual(
                MODULE.load_after_body(spec),
                MODULE.rewrite_body(before_body(spec["id"]), spec, TARGETS),
            )

    def test_live_dry_run_performs_gets_only_and_creates_no_snapshot(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main())
        self.assertFalse(snapshot_dir.exists())
        self.assertEqual(len(calls), 4)
        self.assertTrue(all(payload is None for _, payload in calls))

    def test_apply_refuses_until_reviewed_body_hash_is_committed(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "1210")
        self.assertIn("reviewed_body_sha256", str(caught.exception))
        self.assertEqual(calls, [])
        self.assertFalse(snapshot_dir.exists())

    def test_slug_mismatch_aborts_before_any_write(self):
        self.lives[1056]["slug"] = "wrong-slug"
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--item-id", "1056")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(payload is None for _, payload in calls))

    def test_reviewed_single_item_apply_snapshots_writes_and_reads_back(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        approved = json.loads(json.dumps(TARGETS))
        approved["reviewed_body_sha256"] = hashlib.sha256(
            MODULE.load_draft_body().encode("utf-8")
        ).hexdigest()
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(MODULE, "load_targets", return_value=approved),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--item-id", "1056"))
        writes = [payload for _, payload in calls if payload is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn("the one useful thing I posted over there", writes[0]["content"])
        self.assertGreaterEqual(len(calls), 3)
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_runbook_keeps_review_and_live_approval_as_separate_gates(self):
        runbook = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("reviewed_body_sha256", runbook)
        self.assertIn("fresh explicit live approval", runbook)
        self.assertIn("--restore", runbook)
        self.assertIn("No live write has been made", runbook)
        self.assertNotIn("Fixes #828", runbook)


if __name__ == "__main__":
    unittest.main()
