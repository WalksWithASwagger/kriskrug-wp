import copy
import json
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import body_h1_migration as migration  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-353-body-h1-migration-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-353-body-h1-migration-2026-07-13.md"


class FakeWP:
    def __init__(self, before, after):
        self.responses = [before, after]
        self.gets = []
        self.posts = []

    def get(self, path, *, params=None):
        self.gets.append((path, params))
        return self.responses.pop(0)

    def post(self, path, payload):
        self.posts.append((path, payload))
        return {"id": payload}


def target_for(raw, **overrides):
    expected_after = migration.rewrite_h1(
        raw,
        content_format="classic",
        expected_count=1,
    )
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
        "expected_after_sha256": migration.sha256_text(expected_after),
        "expected_after_length": len(expected_after),
        "body_h1_count": 1,
        "format": "classic",
        "heading_texts": ["Example heading"],
    }
    target.update(overrides)
    return target


def wp_item(target, raw, *, modified_gmt=None):
    return {
        "id": target["id"],
        "type": target["type"],
        "slug": target["slug"],
        "status": target["status"],
        "modified_gmt": modified_gmt or target["modified_gmt"],
        "link": target["url"],
        "content": {"raw": raw},
    }


class Issue353PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.handoff = HANDOFF.read_text(encoding="utf-8")

    def test_packet_locks_exact_scope_and_remains_repo_only(self):
        expected = {
            11358: (9, "gutenberg"),
            7927: (5, "gutenberg"),
            6453: (1, "gutenberg"),
            6435: (1, "gutenberg"),
            6344: (9, "gutenberg"),
            4826: (1, "gutenberg"),
            4174: (1, "gutenberg"),
            4372: (1, "gutenberg"),
            3908: (1, "gutenberg"),
            3567: (1, "gutenberg"),
            3151: (6, "gutenberg"),
            2857: (6, "gutenberg"),
            1547: (1, "classic"),
            12013: (1, "classic"),
        }
        targets = {target["id"]: target for target in self.data["targets"]}

        self.assertEqual(353, self.data["issue"])
        self.assertEqual("repo-only-migration-packet", self.data["status"])
        self.assertEqual(expected.keys(), targets.keys())
        self.assertEqual(44, sum(target["body_h1_count"] for target in targets.values()))
        self.assertEqual(1012, self.data["observed"]["published_posts_and_pages_scanned"])
        self.assertFalse(self.data["observed"]["wordpress_write_performed"])
        self.assertFalse(self.data["observed"]["search_console_write_performed"])
        self.assertFalse(self.data["claims"]["ranking_lift_claimed"])

        for target_id, (count, content_format) in expected.items():
            target = targets[target_id]
            self.assertEqual(count, target["body_h1_count"])
            self.assertEqual(content_format, target["format"])
            self.assertEqual(count, len(target["heading_texts"]))
            self.assertEqual(64, len(target["raw_sha256"]))
            self.assertEqual(64, len(target["expected_after_sha256"]))
            self.assertNotEqual(target["raw_sha256"], target["expected_after_sha256"])
            self.assertEqual(target["raw_length"], target["expected_after_length"])
            self.assertEqual("publish", target["status"])
            self.assertIn(target["endpoint"], {"posts", "pages"})

        self.assertIn("no live WordPress write", self.handoff)
        self.assertIn("one target at a time", self.handoff)
        self.assertIn("does not claim a ranking lift", self.handoff)

    def test_homepage_body_h1_is_explicitly_excluded(self):
        homepage = self.data["homepage_exclusion"]
        self.assertEqual(3930, homepage["id"])
        self.assertEqual("https://kriskrug.co/", homepage["url"])
        self.assertEqual(1, homepage["body_h1_count"])
        self.assertEqual("intentional-homepage-hero-h1", homepage["reason"])
        self.assertNotIn(3930, {target["id"] for target in self.data["targets"]})


class H1RewriteTests(unittest.TestCase):
    def test_gutenberg_rewrite_preserves_non_heading_bytes(self):
        raw = (
            '<p data-note="keep">Before</p>'
            '<!-- wp:heading {"level":1} -->\n'
            '<h1 class="wp-block-heading">Example heading</h1>\n'
            '<!-- /wp:heading -->'
            '<p>After</p>'
        )

        actual = migration.rewrite_h1(raw, content_format="gutenberg", expected_count=1)

        self.assertEqual(
            (
                '<p data-note="keep">Before</p>'
                '<!-- wp:heading {"level":2} -->\n'
                '<h2 class="wp-block-heading">Example heading</h2>\n'
                '<!-- /wp:heading -->'
                '<p>After</p>'
            ),
            actual,
        )
        self.assertEqual(0, migration.count_h1(actual))

    def test_gutenberg_rewrite_changes_every_reviewed_h1_block(self):
        block = '<!-- wp:heading {"level":1} --><h1>%s</h1><!-- /wp:heading -->'
        raw = f"<p>Before</p>{block % 'One'}{block % 'Two'}<p>After</p>"

        actual = migration.rewrite_h1(raw, content_format="gutenberg", expected_count=2)

        self.assertEqual(0, migration.count_h1(actual))
        self.assertEqual(2, actual.count('{"level":2}'))
        self.assertEqual(2, actual.count("<h2>"))
        self.assertTrue(actual.startswith("<p>Before</p>"))
        self.assertTrue(actual.endswith("<p>After</p>"))

    def test_classic_rewrite_changes_only_h1_tag_names(self):
        raw = '<section><h1 class="legacy">Example heading</h1><p>Keep me</p></section>'

        actual = migration.rewrite_h1(raw, content_format="classic", expected_count=1)

        self.assertEqual(
            '<section><h2 class="legacy">Example heading</h2><p>Keep me</p></section>',
            actual,
        )

    def test_gutenberg_rewrite_rejects_unmodeled_classic_h1(self):
        raw = '<!-- wp:paragraph --><p>Text</p><!-- /wp:paragraph --><h1>Loose heading</h1>'

        with self.assertRaisesRegex(migration.MigrationError, "reviewed Gutenberg"):
            migration.rewrite_h1(raw, content_format="gutenberg", expected_count=1)

    def test_rewrite_rejects_h1_count_drift(self):
        with self.assertRaisesRegex(migration.MigrationError, "expected 1 body H1"):
            migration.rewrite_h1(
                "<h2>Already changed</h2>",
                content_format="classic",
                expected_count=1,
            )


class MigrationGuardTests(unittest.TestCase):
    def setUp(self):
        self.raw = "<h1>Example heading</h1><p>Body</p>"
        self.target = target_for(self.raw)

    def test_plan_rejects_modified_timestamp_or_raw_hash_drift(self):
        stale_time = wp_item(self.target, self.raw, modified_gmt="2026-07-13T12:00:01")
        stale_body = wp_item(self.target, self.raw.replace("Body", "B0dy"))

        with self.assertRaisesRegex(migration.MigrationError, "modified_gmt"):
            migration.plan_target(stale_time, self.target)
        with self.assertRaisesRegex(migration.MigrationError, "raw SHA-256"):
            migration.plan_target(stale_body, self.target)

    def test_apply_requires_exact_per_target_confirmation_before_any_api_call(self):
        client = FakeWP(wp_item(self.target, self.raw), wp_item(self.target, self.raw))

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(migration.MigrationError, "exact confirmation"):
                migration.apply_target(
                    client,
                    self.target,
                    confirmation="issue-353",
                    snapshot_dir=Path(tmp),
                )

        self.assertEqual([], client.gets)
        self.assertEqual([], client.posts)

    def test_apply_snapshots_before_one_content_write_and_verifies_readback(self):
        after_raw = "<h2>Example heading</h2><p>Body</p>"
        before = wp_item(self.target, self.raw)
        after = wp_item(self.target, after_raw, modified_gmt="2026-07-13T12:01:00")
        client = FakeWP(before, after)

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("builtins.print") as output:
                result = migration.apply_target(
                    client,
                    self.target,
                    confirmation=migration.confirmation_for(self.target["id"]),
                    snapshot_dir=Path(tmp),
                    now=datetime(2026, 7, 14, 3, 0, tzinfo=timezone.utc),
                )
            snapshot_path = Path(result["snapshot_path"])
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            mode = stat.S_IMODE(snapshot_path.stat().st_mode)

        self.assertEqual(0o600, mode)
        self.assertEqual(self.raw, snapshot["content_raw"])
        self.assertEqual(self.target["raw_sha256"], snapshot["raw_sha256"])
        self.assertEqual(
            [("posts/42", {"content": after_raw})],
            client.posts,
        )
        self.assertEqual(2, len(client.gets))
        output.assert_called_once_with(
            f"pre-write snapshot={snapshot_path}",
            flush=True,
        )
        self.assertEqual(0, result["readback_body_h1_count"])
        self.assertEqual(migration.sha256_text(after_raw), result["readback_raw_sha256"])

    def test_default_cli_mode_is_read_only_audit(self):
        args = migration.parse_args([])

        self.assertEqual("audit", args.command)
        self.assertIsNone(args.target_id)


class InventoryRegressionTests(unittest.TestCase):
    def setUp(self):
        self.raw = "<h1>Example heading</h1><p>Body</p>"
        self.target = target_for(self.raw)
        self.home_raw = "<h1>Intentional homepage heading</h1><p>Home</p>"
        self.homepage = {
            "id": 3930,
            "endpoint": "pages",
            "type": "page",
            "slug": "home-source",
            "status": "publish",
            "modified_gmt": "2026-07-13T11:00:00",
            "url": "https://kriskrug.co/",
            "raw_sha256": migration.sha256_text(self.home_raw),
            "raw_length": len(self.home_raw),
            "body_h1_count": 1,
        }

    def test_inventory_accepts_pending_target_homepage_and_h2_h3_only_content(self):
        ordinary = {
            "id": 99,
            "type": "post",
            "slug": "ordinary",
            "status": "publish",
            "modified_gmt": "2026-07-13T13:00:00",
            "link": "https://kriskrug.co/ordinary/",
            "content": {"raw": "<h2>Section</h2><h3>Detail</h3>"},
        }
        result = migration.audit_inventory(
            [
                wp_item(self.target, self.raw),
                wp_item(self.homepage, self.home_raw),
                ordinary,
            ],
            {self.target["id"]: self.target},
            self.homepage,
        )

        self.assertEqual([42], result["pending_targets"])
        self.assertEqual([], result["migrated_targets"])
        self.assertEqual([], result["unreviewed_body_h1_sources"])

    def test_inventory_accepts_exact_migrated_target_state(self):
        after_raw = "<h2>Example heading</h2><p>Body</p>"
        result = migration.audit_inventory(
            [
                wp_item(
                    self.target,
                    after_raw,
                    modified_gmt="2026-07-14T03:01:00",
                ),
                wp_item(self.homepage, self.home_raw),
            ],
            {self.target["id"]: self.target},
            self.homepage,
        )

        self.assertEqual([], result["pending_targets"])
        self.assertEqual([42], result["migrated_targets"])

    def test_inventory_rejects_new_non_homepage_body_h1(self):
        unexpected = {
            "id": 99,
            "type": "post",
            "slug": "unexpected",
            "status": "publish",
            "modified_gmt": "2026-07-13T13:00:00",
            "link": "https://kriskrug.co/unexpected/",
            "content": {"raw": "<h1>Unexpected heading</h1>"},
        }

        with self.assertRaisesRegex(migration.MigrationError, "unreviewed"):
            migration.audit_inventory(
                [
                    wp_item(self.target, self.raw),
                    wp_item(self.homepage, self.home_raw),
                    unexpected,
                ],
                {self.target["id"]: self.target},
                self.homepage,
            )


if __name__ == "__main__":
    unittest.main()
