"""Issue #322 — live WordPress writer safety contract (mocked / offline).

Covers the shared safety shape across guarded writers without production
credentials or live WordPress mutation:

1. Snapshot before the first write
2. ID/slug identity mismatch aborts with zero writes
3. Write payloads stay on an explicit allowlist (content-only for body writers)
4. Failed readback fails visibly
5. Restoration from a captured snapshot is possible after a bad write
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import body_h1_migration as migration  # noqa: E402
import content_architecture_deploy as cad  # noqa: E402
import wp_post_ia_rollout as rollout  # noqa: E402


class RecordingWP:
    def __init__(self, responses):
        self.responses = list(responses)
        self.gets = []
        self.posts = []

    def get(self, path, *, params=None):
        self.gets.append((path, params))
        if not self.responses:
            raise AssertionError(f"unexpected GET {path}")
        return self.responses.pop(0)

    def post(self, path, payload):
        self.posts.append((path, payload))
        return {"ok": True, "id": payload}


class WriterSafetyContractTests(unittest.TestCase):
    def test_rollout_execute_snapshots_before_any_wordpress_write(self):
        class OrderedWP:
            def __init__(self):
                self.posts = []
                self.snapshot_seen = False
                self.write_after_snapshot = False

            def post(self, endpoint, payload):
                self.write_after_snapshot = self.snapshot_seen
                self.posts.append((endpoint, payload))
                return {"ok": True}

        fake = OrderedWP()
        before = [
            rollout.PostAudit(
                post_id=42,
                slug="make-culture-not-content",
                link="https://kriskrug.co/make-culture-not-content/",
                title="Make Culture, Not Content",
                featured_media=11264,
                featured_alt="",
                has_excerpt=False,
                has_featured=True,
                has_featured_alt=False,
                missing_excerpt=True,
                missing_featured=False,
                missing_featured_alt=True,
            )
        ]
        after = [
            rollout.PostAudit(
                post_id=42,
                slug="make-culture-not-content",
                link="https://kriskrug.co/make-culture-not-content/",
                title="Make Culture, Not Content",
                featured_media=11264,
                featured_alt="alt",
                has_excerpt=True,
                has_featured=True,
                has_featured_alt=True,
                missing_excerpt=False,
                missing_featured=False,
                missing_featured_alt=False,
            )
        ]

        def snapshot_targets(*_args, **_kwargs):
            fake.snapshot_seen = True
            self.assertEqual([], fake.posts)
            return Path("/tmp/pre-write-snapshot.json")

        with mock.patch.object(sys, "argv", ["wp_post_ia_rollout.py", "--execute", "--since", "2026-01-01"]), \
             mock.patch.object(rollout, "load_config", return_value=rollout.Config("https://example.com", "u", "p")), \
             mock.patch.object(rollout, "WordPressClient", return_value=fake), \
             mock.patch.object(rollout, "fetch_posts", side_effect=[["before"], ["after"]]), \
             mock.patch.object(rollout, "audit_posts", side_effect=[before, after]), \
             mock.patch.object(rollout, "fetch_media", return_value={"alt_text": ""}), \
             mock.patch.object(
                 rollout,
                 "post_content",
                 return_value="<p>First. Second.</p>",
             ), \
             mock.patch.object(
                 rollout,
                 "public_page_probe",
                 return_value={
                     "featured_alt": "alt",
                     "og_alt": "og",
                     "hierarchy_ok": True,
                     "hardcoded_field_note": False,
                     "schema_has_image": True,
                 },
             ), \
             mock.patch.object(rollout, "write_report"), \
             mock.patch.object(rollout, "snapshot_targets", side_effect=snapshot_targets), \
             mock.patch("sys.stdout"):
            rollout.main()

        self.assertTrue(fake.snapshot_seen)
        self.assertTrue(fake.write_after_snapshot)
        self.assertGreaterEqual(len(fake.posts), 1)

    def test_body_h1_identity_mismatch_and_content_allowlist(self):
        raw = "<h1>Example heading</h1><p>Body</p>"
        target = {
            "id": 42,
            "endpoint": "posts",
            "type": "post",
            "slug": "example-post",
            "status": "publish",
            "modified_gmt": "2026-07-13T12:00:00",
            "url": "https://kriskrug.co/2026/07/13/example-post/",
            "raw_sha256": migration.sha256_text(raw),
            "raw_length": len(raw),
            "expected_after_sha256": migration.sha256_text(
                migration.rewrite_h1(raw, content_format="classic", expected_count=1)
            ),
            "expected_after_length": len(
                migration.rewrite_h1(raw, content_format="classic", expected_count=1)
            ),
            "body_h1_count": 1,
            "format": "classic",
            "heading_texts": ["Example heading"],
        }
        mismatched = {
            "id": 42,
            "type": "post",
            "slug": "other-slug",
            "status": "publish",
            "modified_gmt": "2026-07-13T12:00:00",
            "link": "https://kriskrug.co/2026/07/13/example-post/",
            "content": {"raw": raw},
        }
        client = RecordingWP([mismatched])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(migration.MigrationError, "slug drift"):
                migration.apply_target(
                    client,
                    target,
                    confirmation=migration.confirmation_for(42),
                    snapshot_dir=Path(tmp),
                )
        self.assertEqual([], client.posts)

    def test_content_architecture_restore_from_snapshot_after_failed_readback(self):
        page = {
            "id": 100,
            "slug": "about",
            "url": "https://kriskrug.co/about/",
            "markers": ["marker-a"],
            "payload": "about.html",
        }
        before_raw = "<!-- before -->"
        bad_raw = "<p>broken</p>"
        snapshot = {
            "id": 100,
            "slug": "about",
            "status": "publish",
            "content": {"raw": before_raw},
        }
        readback_ok = {
            "id": 100,
            "slug": "about",
            "status": "publish",
            "content": {"raw": before_raw},
        }

        with tempfile.TemporaryDirectory() as tmp:
            snapshot_dir = Path(tmp)
            (snapshot_dir / "page-100-about-before.json").write_text(
                json.dumps(snapshot),
                encoding="utf-8",
            )
            wp = RecordingWP([readback_ok])
            # Simulate a bad write already happened, then restore.
            wp.posts.append((f"pages/{page['id']}", {"content": bad_raw}))
            cad.restore_page(wp, "about", page, snapshot_dir)

        self.assertEqual(
            ("pages/100", {"content": before_raw}),
            wp.posts[-1],
        )
        self.assertEqual({"content"}, set(wp.posts[-1][1]))

    def test_content_architecture_verify_target_rejects_id_slug_mismatch(self):
        expected = {"id": 7, "slug": "work"}
        with self.assertRaisesRegex(RuntimeError, "slug:"):
            cad.verify_target({"id": 7, "slug": "projects", "status": "publish"}, expected)
        with self.assertRaisesRegex(RuntimeError, "id:"):
            cad.verify_target({"id": 8, "slug": "work", "status": "publish"}, expected)

    def test_body_h1_failed_readback_is_visible_and_leaves_snapshot(self):
        raw = "<h1>Example heading</h1><p>Body</p>"
        after = migration.rewrite_h1(raw, content_format="classic", expected_count=1)
        target = {
            "id": 42,
            "endpoint": "posts",
            "type": "post",
            "slug": "example-post",
            "status": "publish",
            "modified_gmt": "2026-07-13T12:00:00",
            "url": "https://kriskrug.co/2026/07/13/example-post/",
            "raw_sha256": migration.sha256_text(raw),
            "raw_length": len(raw),
            "expected_after_sha256": migration.sha256_text(after),
            "expected_after_length": len(after),
            "body_h1_count": 1,
            "format": "classic",
            "heading_texts": ["Example heading"],
        }
        before_item = {
            "id": 42,
            "type": "post",
            "slug": "example-post",
            "status": "publish",
            "modified_gmt": "2026-07-13T12:00:00",
            "link": "https://kriskrug.co/2026/07/13/example-post/",
            "content": {"raw": raw},
        }
        bad_readback = dict(before_item)
        bad_readback["content"] = {"raw": "<h2>Not the reviewed patch</h2><p>Body</p>"}
        bad_readback["modified_gmt"] = "2026-07-13T12:01:00"
        client = RecordingWP([before_item, bad_readback])

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(migration.MigrationError, "readback SHA-256"):
                migration.apply_target(
                    client,
                    target,
                    confirmation=migration.confirmation_for(42),
                    snapshot_dir=Path(tmp),
                    now=datetime(2026, 7, 14, 3, 0, tzinfo=timezone.utc),
                )
            snapshots = list(Path(tmp).glob("kriskrug-issue-353-42-*.json"))
            self.assertEqual(1, len(snapshots))
            saved = json.loads(snapshots[0].read_text(encoding="utf-8"))
            self.assertEqual(raw, saved["content_raw"])

        self.assertEqual(1, len(client.posts))
        self.assertEqual({"content"}, set(client.posts[0][1]))


if __name__ == "__main__":
    unittest.main()
