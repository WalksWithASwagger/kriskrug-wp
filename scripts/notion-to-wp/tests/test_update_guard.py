import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402


class FakeWordPress:
    def __init__(self, existing_post=None, existing_id=123):
        self.existing_post = existing_post
        self.existing_id = existing_id
        self.write_calls = []

    def find_post_by_slug(self, slug):
        return self.existing_id

    def get_post(self, post_id):
        return self.existing_post

    def upload_media(self, *args, **kwargs):
        self.write_calls.append("upload_media")
        raise AssertionError("diff review must not upload media")

    def ensure_term(self, *args, **kwargs):
        self.write_calls.append("ensure_term")
        raise AssertionError("diff review must not create or resolve terms")

    def create_post(self, *args, **kwargs):
        self.write_calls.append("create_post")
        raise AssertionError("diff review must not create posts")

    def update_post(self, *args, **kwargs):
        self.write_calls.append("update_post")
        raise AssertionError("diff review must not update posts")


def existing_post(title="Web Summit Vancouver 2026", content="<p>Old body</p>"):
    return {
        "id": 123,
        "title": {"raw": title},
        "slug": "web-summit-vancouver-2026",
        "status": "draft",
        "date": "2026-05-07T12:00:00",
        "excerpt": {"raw": "Old excerpt"},
        "content": {"raw": content},
        "meta": {"advanced_seo_description": "Old excerpt"},
    }


def proposed_payload(title="Web Summit Vancouver 2026", content="<p>New body</p>"):
    return {
        "title": title,
        "slug": "web-summit-vancouver-2026",
        "status": "draft",
        "date": "2026-05-07T12:00:00",
        "excerpt": "New excerpt",
        "content": content,
        "meta": {"advanced_seo_description": "New excerpt"},
    }


class UpdateTitleGuardTests(unittest.TestCase):
    def test_guard_allows_matching_title_case_insensitive(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Your Taste Is Your Moat",
            "your taste is your moat",
        )

        self.assertTrue(allowed)
        self.assertEqual(similarity, 1.0)

    def test_guard_allows_close_title_variation(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Web Summit Vancouver 2026",
            "Web Summit Vancouver 2026: Field Notes",
        )

        self.assertTrue(allowed)
        self.assertGreaterEqual(
            similarity,
            kk_notion_to_wp.TITLE_SIMILARITY_UPDATE_THRESHOLD,
        )

    def test_guard_blocks_incident_style_wrong_post_collision(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Calling Us All In",
            "Web Summit Vancouver 2026",
        )

        self.assertFalse(allowed)
        self.assertLess(
            similarity,
            kk_notion_to_wp.TITLE_SIMILARITY_UPDATE_THRESHOLD,
        )

    def test_update_diff_is_deterministic(self):
        diff = kk_notion_to_wp.update_diff(existing_post(), proposed_payload())

        self.assertIn("--- existing-wp-post", diff)
        self.assertIn("+++ proposed-notion-payload", diff)
        self.assertIn('-  "excerpt": "Old excerpt"', diff)
        self.assertIn('+  "excerpt": "New excerpt"', diff)
        self.assertIn('-  "content": "<p>Old body</p>"', diff)
        self.assertIn('+  "content": "<p>New body</p>"', diff)

    def test_diff_review_emits_diff_without_wp_write_calls(self):
        wp = FakeWordPress(existing_post=existing_post())
        logs = []
        emitted = []

        code = kk_notion_to_wp.emit_update_diff_review(
            wp,
            "web-summit-vancouver-2026",
            "Web Summit Vancouver 2026",
            proposed_payload(),
            logs.append,
            emitted.append,
        )

        self.assertEqual(code, 0)
        self.assertEqual(wp.write_calls, [])
        self.assertEqual(len(emitted), 1)
        self.assertIn("proposed-notion-payload", emitted[0])
        self.assertTrue(any("no WP create, update, taxonomy, or media write" in msg for msg in logs))

    def test_diff_review_blocks_incident_style_wrong_post_collision(self):
        wp = FakeWordPress(existing_post=existing_post(title="Web Summit Vancouver 2026"))
        logs = []
        emitted = []

        code = kk_notion_to_wp.emit_update_diff_review(
            wp,
            "web-summit-vancouver-2026",
            "Calling Us All In",
            proposed_payload(title="Calling Us All In"),
            logs.append,
            emitted.append,
        )

        self.assertEqual(code, 3)
        self.assertEqual(wp.write_calls, [])
        self.assertEqual(emitted, [])
        self.assertTrue(any("too different" in msg for msg in logs))

    def test_diff_review_requires_existing_slug_target(self):
        wp = FakeWordPress(existing_post=None, existing_id=None)
        logs = []
        emitted = []

        code = kk_notion_to_wp.emit_update_diff_review(
            wp,
            "missing-slug",
            "Missing Slug",
            proposed_payload(title="Missing Slug"),
            logs.append,
            emitted.append,
        )

        self.assertEqual(code, 6)
        self.assertEqual(wp.write_calls, [])
        self.assertEqual(emitted, [])
        self.assertTrue(any("needs an existing post" in msg for msg in logs))


if __name__ == "__main__":
    unittest.main()
