import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "content/drafts/339-july-publisher-batch-2026-08-16"
MANIFEST = PACKET / "manifest.json"
SEO = PACKET / "seo-meta-overwrite.json"
README = PACKET / "README.md"
GUARD_REFRESH = PACKET / "authenticated-guard-refresh-20260828.json"

EM_DASH = "\u2014"
EN_DASH = "\u2013"
ALLOWED_META = {
    "jetpack_seo_html_title",
    "advanced_seo_description",
    "jetpack_publicize_message",
}


class Issue339PublisherRefreshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.seo = json.loads(SEO.read_text(encoding="utf-8"))
        cls.guard_refresh = json.loads(GUARD_REFRESH.read_text(encoding="utf-8"))

    def test_packet_claims_no_live_write(self):
        self.assertFalse(self.manifest["live_wordpress_write_performed"])
        self.assertFalse(self.seo["live_wordpress_write_performed"])
        self.assertEqual(339, self.manifest["issue"])

    def test_theme_zip_is_marked_obsolete(self):
        aurora = self.manifest["aurora"]
        self.assertEqual("obsolete", aurora["verdict"])
        self.assertEqual("1.3.39", aurora["issue_body_zip"])
        self.assertEqual("1.6.9", aurora["live_style_css"])
        self.assertEqual("1.6.9", aurora["repo_style_css"])
        theme_item = next(
            i for i in self.manifest["items"] if i["issue"] == "theme-zip"
        )
        self.assertEqual("DONE / DEAD", theme_item["verdict"])

    def test_content_items_are_still_open_with_payloads(self):
        by_issue = {
            i["issue"]: i for i in self.manifest["items"] if isinstance(i["issue"], int)
        }
        for number in (249, 328, 335, 336, 342):
            item = by_issue[number]
            self.assertEqual("STILL OPEN", item["verdict"], msg=f"#{number}")
            payload = PACKET / item["payload"]
            self.assertTrue(payload.is_file(), msg=item["payload"])
            text = payload.read_text(encoding="utf-8")
            self.assertIn("**Verdict:** STILL OPEN", text)
            self.assertIn("Snapshot-first apply", text)
            self.assertIn("Rollback", text)

    def test_seo_overwrite_file_is_strict_and_ascii_new_copy(self):
        self.assertEqual("overwrite", self.seo["mode"])
        items = self.seo["items"]
        self.assertEqual([35, 8802], [row["id"] for row in items])
        self.assertEqual(
            "the-lord-of-the-rings-drinking-game",
            items[0]["slug"],
        )
        self.assertEqual(
            "how-to-build-an-ai-second-brain-that-actually-works-for-you",
            items[1]["slug"],
        )
        for row in items:
            meta = row["meta"]
            self.assertTrue(set(meta) <= ALLOWED_META)
            self.assertEqual(
                {"jetpack_seo_html_title", "advanced_seo_description"},
                set(meta),
            )
            for value in meta.values():
                self.assertIsInstance(value, str)
                self.assertTrue(value.strip())
                self.assertNotIn(EM_DASH, value)
                self.assertNotIn(EN_DASH, value)
                value.encode("latin-1")

        self.assertEqual(
            "The Lord of the Rings Drinking Game: 4 Original Rules",
            items[0]["meta"]["jetpack_seo_html_title"],
        )
        self.assertEqual(
            "Build an AI Second Brain That Actually Works for You",
            items[1]["meta"]["jetpack_seo_html_title"],
        )

    def test_refreshed_modified_guards_are_locked(self):
        by_issue = {
            i["issue"]: i for i in self.manifest["items"] if isinstance(i["issue"], int)
        }
        self.assertEqual(
            "2026-08-16T21:29:03",
            by_issue[249]["target"]["modified"],
        )
        self.assertEqual(1208, by_issue[249]["target"]["id"])
        self.assertEqual("about", by_issue[249]["target"]["slug"])
        self.assertEqual(
            "2026-08-10T18:24:39",
            by_issue[342]["target"]["modified"],
        )
        self.assertEqual(11171, by_issue[342]["target"]["id"])
        self.assertEqual(
            "2026-08-16T21:03:50",
            by_issue[336]["sources"][1]["modified"],
        )

    def test_authenticated_guard_refresh_locks_raw_and_planned_hashes(self):
        self.assertEqual("authenticated-read-only", self.guard_refresh["mode"])
        self.assertFalse(self.guard_refresh["live_wordpress_write_performed"])
        guards = {row["id"]: row for row in self.guard_refresh["objects"]}
        self.assertEqual({1208, 12327}, set(guards))
        by_issue = {
            row["issue"]: row
            for row in self.manifest["items"]
            if isinstance(row["issue"], int)
        }
        manifest_guards = {
            1208: by_issue[249]["target"],
            12327: by_issue[336]["sources"][1],
        }

        expected = {
            1208: {
                "modified": "2026-08-16T21:29:03",
                "raw": "3171b2f41bfc919aba40640200cb2bafe76e75329ba736efec1713cd29135783",
                "desired": "857ea7af53db7dd2b5007123b0ac8efa86b0397c1e4baea5572c38c26b565b5b",
                "changed": 218,
            },
            12327: {
                "modified": "2026-08-16T21:03:50",
                "raw": "045c697906260becae376d39fcf0987911ac9c94e5d3b25def8a4f1b4a69981d",
                "desired": "32a77f548f700cde5edd77e8c6959dda04d9aa229e852b8f860c8ce87f09b4bd",
                "changed": 106,
            },
        }
        for post_id, values in expected.items():
            guard = guards[post_id]
            self.assertEqual(values["modified"], guard["modified"])
            self.assertEqual(values["raw"], guard["content_raw_sha256"])
            self.assertEqual(values["desired"], guard["desired_content_sha256"])
            self.assertEqual(values["changed"], guard["changed_chars"])
            self.assertEqual(1, guard["find_count"])
            self.assertEqual(0, guard["target_href_count"])
            self.assertEqual(
                guard["desired_content_chars"] - guard["content_raw_chars"],
                guard["changed_chars"],
            )
            self.assertNotEqual(
                guard["content_raw_sha256"], guard["desired_content_sha256"]
            )
            for key in (
                "modified",
                "modified_gmt",
                "content_raw_chars",
                "content_raw_sha256",
                "desired_content_chars",
                "desired_content_sha256",
                "find_count",
                "target_href_count",
            ):
                self.assertEqual(guard[key], manifest_guards[post_id][key])

    def test_readme_strikes_the_zip_and_points_at_the_report(self):
        readme = README.read_text(encoding="utf-8")
        self.assertIn("STILL OPEN", readme)
        self.assertIn("1.3.39", readme)
        self.assertIn("1.6.9", readme)
        self.assertIn("Do not upload", readme)
        self.assertIn("authenticated-guard-refresh-20260828.json", readme)
        self.assertIn("publisher-batch-refresh-339-20260816.md", readme)


if __name__ == "__main__":
    unittest.main()
