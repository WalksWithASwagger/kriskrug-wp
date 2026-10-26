"""Offline regression checks for the #834 content-only publisher."""

from __future__ import annotations

import copy
import importlib.util
import json
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

SCRIPT = Path(__file__).parents[1] / "apply_issue_834_brand_links.py"
SPEC = importlib.util.spec_from_file_location("issue834", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def fixture(index=0):
    spec = copy.deepcopy(MODULE.TARGETS[index])
    body = (
        '<!-- wp:image --><img src="unchanged.jpg"><!-- /wp:image -->\n'
        + spec["find"]
        + f"\n<p>{spec['dependency'] or 'Earlier text'}</p>\n"
        + '<p class="kk-collection-footer">Original footer and sources</p>'
    )
    spec["before_sha256"] = MODULE.digest(body)
    spec["after_sha256"] = MODULE.digest(body.replace(spec["find"], spec["replace"]))
    item = {key: spec[key] for key in ("id", "slug", "type", "status", "date")}
    item.update(
        title={"raw": spec["title"]},
        content={"raw": body},
        modified="before",
        categories=[7],
        tags=[8],
        featured_media=42,
        excerpt={"raw": "fixed"},
        meta={},
    )
    return spec, item


class Issue834Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.spec, self.item = fixture()
        self.client = Mock()
        self.client.get.side_effect = lambda *_a, **_k: copy.deepcopy(self.item)

    def test_exact_scope_and_surgical_idempotent_rewrites(self):
        self.assertEqual([row["id"] for row in MODULE.TARGETS], [12653, 12030, 11700])
        for index in range(3):
            spec, item = fixture(index)
            before = item["content"]["raw"]
            after = MODULE.candidate(before, spec)
            self.assertEqual(after.replace(spec["replace"], spec["find"]), before)
            self.assertEqual(MODULE.candidate(after, spec), after)
            self.assertEqual(after.count('class="kk-collection-footer"'), 1)
            addition = spec["replace"].removeprefix(spec["find"][:-4])
            self.assertNotIn("\u2014", addition)
            self.assertNotIn("\u2013", addition)

    def test_wrong_identity_or_missing_raw_refuses(self):
        for key in ("id", "slug", "type", "status", "date", "title", "content"):
            item = copy.deepcopy(self.item)
            item.pop(key)
            with self.subTest(key=key), self.assertRaises(ValueError):
                MODULE.validate(item, self.spec)

    def test_newer_body_is_never_overwritten(self):
        self.item["content"]["raw"] += "new edit"
        with self.assertRaisesRegex(ValueError, "changed since review"):
            MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.client.post.assert_not_called()
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_missing_or_duplicate_markers_refuse_even_if_hash_was_recut(self):
        for body in ("missing", self.spec["find"] * 2):
            spec = dict(self.spec, before_sha256=MODULE.digest(body))
            with self.assertRaisesRegex(ValueError, "insertion marker"):
                MODULE.candidate(body, spec)

    def test_prior_issue_dependency_is_required(self):
        spec, item = fixture(1)
        body = item["content"]["raw"].replace(spec["dependency"], "absent")
        spec["before_sha256"] = MODULE.digest(body)
        with self.assertRaisesRegex(ValueError, "earlier issue"):
            MODULE.candidate(body, spec)

    def test_dry_run_has_no_write_or_snapshot(self):
        result = MODULE.update(self.client, self.spec, self.folder, apply=False)
        self.assertEqual(result["status"], "dry-run")
        self.client.post.assert_not_called()
        self.assertEqual(list(self.folder.iterdir()), [])

    def test_apply_snapshots_before_content_only_write_then_reads_back(self):
        original = copy.deepcopy(self.item)

        def write(route, payload):
            files = list(self.folder.glob("*-before-*.json"))
            self.assertEqual(len(files), 1)
            self.assertEqual(json.loads(files[0].read_text()), original)
            self.assertEqual(stat.S_IMODE(files[0].stat().st_mode), 0o600)
            self.assertEqual(route, f"posts/{self.spec['id']}")
            self.assertEqual(set(payload), {"content"})
            self.item["content"]["raw"] = payload["content"]

        self.client.post.side_effect = write
        result = MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.assertEqual(result["status"], "applied")
        self.assertEqual(self.client.get.call_count, 3)
        self.assertEqual(json.loads(Path(result["readback"]).read_text()), self.item)
        MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.assertEqual(self.client.post.call_count, 1)

    def test_edit_between_snapshot_and_write_aborts(self):
        fresh = copy.deepcopy(self.item)
        fresh["modified"] = "newer"
        self.client.get.side_effect = [self.item, fresh]
        with self.assertRaisesRegex(ValueError, "during snapshot"):
            MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.client.post.assert_not_called()

    def test_failed_readback_is_not_success(self):
        with self.assertRaisesRegex(ValueError, "Readback differs"):
            MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.assertEqual(self.client.post.call_count, 1)

    def test_ambiguous_write_is_not_replayed(self):
        self.client.post.side_effect = TimeoutError("ambiguous outcome")
        with self.assertRaises(TimeoutError):
            MODULE.update(self.client, self.spec, self.folder, apply=True)
        self.assertEqual(self.client.post.call_count, 1)
        self.assertEqual(len(list(self.folder.glob("*-before-*.json"))), 1)

    def test_restore_dry_run_apply_and_newer_edit_guard(self):
        original = copy.deepcopy(self.item)
        self.item["content"]["raw"] = MODULE.candidate(
            self.item["content"]["raw"], self.spec
        )
        result = MODULE.update(
            self.client, self.spec, self.folder, apply=False, restore=original
        )
        self.assertEqual(result["status"], "dry-run")
        self.client.post.assert_not_called()
        self.client.post.side_effect = lambda _route, payload: self.item[
            "content"
        ].update(raw=payload["content"])
        result = MODULE.update(
            self.client, self.spec, self.folder, apply=True, restore=original
        )
        self.assertEqual(result["status"], "restored")
        self.assertEqual(self.item, original)
        self.item["content"]["raw"] += "newer edit"
        with self.assertRaisesRegex(ValueError, "newer or unreviewed"):
            MODULE.update(
                self.client, self.spec, self.folder, apply=True, restore=original
            )
        self.assertEqual(self.client.post.call_count, 1)

    def test_restore_rejects_wrong_snapshot(self):
        altered = copy.deepcopy(self.item)
        altered["content"]["raw"] += "wrong original"
        with self.assertRaisesRegex(ValueError, "not the reviewed original"):
            MODULE.update(
                self.client, self.spec, self.folder, apply=True, restore=altered
            )
        self.client.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
