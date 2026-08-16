from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402
from wp_client import (  # noqa: E402
    DryRunWriteBlocked,
    SlugVerificationFailed,
    WordPress,
)


def offline_client() -> WordPress:
    wp = WordPress.__new__(WordPress)
    wp.base = "https://example.test"
    wp.s = mock.Mock()
    return wp


class WordPressMediaTests(unittest.TestCase):
    def test_upload_media_sets_full_metadata(self):
        uploaded = mock.Mock()
        uploaded.json.return_value = {"id": 42, "source_url": "https://example.test/portrait.jpg"}
        updated = mock.Mock()
        updated.json.return_value = {"id": 42, "source_url": "https://example.test/portrait.jpg"}

        wp = WordPress.__new__(WordPress)
        wp.base = "https://example.test"
        wp.s = mock.Mock()
        wp.s.post.side_effect = [uploaded, updated]

        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "portrait.jpg"
            image.write_bytes(b"jpeg fixture")
            result = wp.upload_media(
                image,
                "Alt",
                title="Title",
                caption="Caption",
                description="Description",
            )

        self.assertEqual(result["id"], 42)
        self.assertEqual(wp.s.post.call_count, 2)
        self.assertEqual(
            wp.s.post.call_args_list[1].kwargs["json"],
            {
                "alt_text": "Alt",
                "title": "Title",
                "caption": "Caption",
                "description": "Description",
            },
        )


class WordPressDryRunGuardTests(unittest.TestCase):
    def test_direct_session_post_refuses_under_dry_run_at_http_boundary(self):
        wp = WordPress("https://example.test", "user", "password")

        with mock.patch("requests.sessions.Session.request") as request:
            with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
                with self.assertRaises(DryRunWriteBlocked) as caught:
                    wp.s.post(
                        "https://example.test/wp-json/wp/v2/tags",
                        json={"name": "ai"},
                    )

        self.assertIn("HTTP POST", str(caught.exception))
        request.assert_not_called()

    def test_publish_common_direct_session_write_is_blocked(self):
        wp = WordPress("https://example.test", "user", "password")
        not_found = mock.Mock(status_code=200)
        not_found.json.return_value = []

        with mock.patch(
            "requests.sessions.Session.request", return_value=not_found
        ) as request:
            with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
                with self.assertRaises(DryRunWriteBlocked):
                    publish_common.ensure_term_id(wp, "tags", "ai")

        request.assert_called_once()

    def test_create_post_refuses_under_dry_run_without_touching_http(self):
        wp = offline_client()

        with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
            with self.assertRaises(DryRunWriteBlocked) as caught:
                wp.create_post(
                    {"title": "Calling Us All In", "slug": "calling-us-all-in"}
                )

        self.assertIn("create_post", str(caught.exception))
        self.assertIn("DRY_RUN", str(caught.exception))
        self.assertEqual(wp.s.mock_calls, [])

    def test_update_post_refuses_under_dry_run_without_touching_http(self):
        wp = offline_client()

        with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
            with self.assertRaises(DryRunWriteBlocked) as caught:
                wp.update_post(
                    11765,
                    {"title": "Calling Us All In"},
                    expected_slug="calling-us-all-in",
                )

        self.assertIn("update_post", str(caught.exception))
        self.assertIn("DRY_RUN", str(caught.exception))
        self.assertEqual(wp.s.mock_calls, [])

    def test_every_write_method_refuses_under_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "portrait.jpg"
            image.write_bytes(b"jpeg fixture")
            writes = {
                "upload_media_file": lambda wp: wp.upload_media_file(image),
                "upload_media": lambda wp: wp.upload_media(image, "Alt"),
                "update_media": lambda wp: wp.update_media(42, {"alt_text": "Alt"}),
                "ensure_term": lambda wp: wp.ensure_term("tags", "ai"),
                "create_post": lambda wp: wp.create_post({"title": "T"}),
                "update_post": lambda wp: wp.update_post(
                    11765, {"title": "T"}, expected_slug="t"
                ),
            }
            for name, write in writes.items():
                with self.subTest(method=name):
                    wp = offline_client()
                    with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
                        with self.assertRaises(DryRunWriteBlocked):
                            write(wp)
                    self.assertEqual(wp.s.mock_calls, [])

    def test_dry_run_blocks_writes_without_blocking_reads(self):
        found = mock.Mock(status_code=200)
        found.json.return_value = [
            {"id": 11765, "slug": "web-summit-vancouver-2026"}
        ]
        wp = offline_client()
        wp.s.get.return_value = found

        with mock.patch.dict(os.environ, {"DRY_RUN": "1"}):
            post_id = wp.find_post_by_slug("web-summit-vancouver-2026")

        self.assertEqual(post_id, 11765)
        wp.s.post.assert_not_called()

    def test_falsey_dry_run_values_leave_writes_enabled(self):
        for value in ("", "0", "false", "FALSE", "no", "off", " 0 "):
            with self.subTest(value=value):
                created = mock.Mock()
                created.json.return_value = {"id": 12}
                wp = offline_client()
                wp.s.post.return_value = created

                with mock.patch.dict(os.environ, {"DRY_RUN": value}):
                    self.assertEqual(wp.create_post({"title": "T"})["id"], 12)

                wp.s.post.assert_called_once()

    def test_unset_dry_run_leaves_write_requests_unchanged(self):
        created = mock.Mock()
        created.json.return_value = {"id": 12}
        updated = mock.Mock()
        updated.json.return_value = {"id": 11765}
        wp = offline_client()
        wp.s.post.side_effect = [created, updated]

        with mock.patch.dict(os.environ, {}, clear=True):
            wp.create_post({"title": "T", "slug": "t"})
            with mock.patch.object(
                wp, "find_post_by_slug", return_value=11765
            ) as find_post:
                wp.update_post(
                    11765,
                    {"content": "<p>Body</p>"},
                    expected_slug="calling-us-all-in",
                )

        find_post.assert_called_once_with("calling-us-all-in")

        create_call, update_call = wp.s.post.call_args_list
        self.assertEqual(
            create_call.args[0], "https://example.test/wp-json/wp/v2/posts"
        )
        self.assertEqual(create_call.kwargs["json"], {"title": "T", "slug": "t"})
        self.assertEqual(create_call.kwargs["timeout"], 60)
        self.assertEqual(
            update_call.args[0],
            "https://example.test/wp-json/wp/v2/posts/11765",
        )
        self.assertEqual(update_call.kwargs["json"], {"content": "<p>Body</p>"})
        self.assertEqual(update_call.kwargs["timeout"], 60)


class WordPressSlugLookupTests(unittest.TestCase):
    """2026-05-15: a lookup that silently returned every post handed back the
    newest one, and the connector PATCHed it."""

    def lookup(self, status_code: int, payload):
        response = mock.Mock(status_code=status_code)
        response.json.return_value = payload
        wp = offline_client()
        wp.s.get.return_value = response
        return wp, wp.find_post_by_slug("web-summit-vancouver-2026")

    def test_exactly_one_slug_match_is_the_update_target(self):
        wp, post_id = self.lookup(
            200, [{"id": 11765, "slug": "web-summit-vancouver-2026"}]
        )

        self.assertEqual(post_id, 11765)
        self.assertEqual(
            wp.s.get.call_args.kwargs["params"],
            {
                "slug": "web-summit-vancouver-2026",
                "status": "any",
                "per_page": 5,
                "context": "edit",
            },
        )

    def test_multiple_slug_matches_refuse_to_pick_the_first(self):
        _, post_id = self.lookup(200, [{"id": 11765}, {"id": 11766}])

        self.assertIsNone(post_id)

    def test_no_slug_match_returns_none(self):
        _, post_id = self.lookup(200, [])

        self.assertIsNone(post_id)

    def test_failed_lookup_returns_none_rather_than_a_guess(self):
        _, post_id = self.lookup(500, [{"id": 11765}])

        self.assertIsNone(post_id)

    def test_singleton_with_different_slug_is_rejected(self):
        _, post_id = self.lookup(
            200, [{"id": 999, "slug": "calling-us-all-in"}]
        )

        self.assertIsNone(post_id)

    def test_update_verifies_expected_slug_when_payload_omits_slug(self):
        found = mock.Mock(status_code=200)
        found.json.return_value = [
            {"id": 11765, "slug": "web-summit-vancouver-2026"}
        ]
        updated = mock.Mock()
        updated.json.return_value = {
            "id": 11765,
            "slug": "web-summit-vancouver-2026",
        }
        wp = offline_client()
        wp.s.get.return_value = found
        wp.s.post.return_value = updated

        result = wp.update_post(
            11765,
            {"title": "Web Summit Vancouver 2026"},
            expected_slug="web-summit-vancouver-2026",
        )

        self.assertEqual(result["id"], 11765)
        wp.s.get.assert_called_once()
        wp.s.post.assert_called_once_with(
            "https://example.test/wp-json/wp/v2/posts/11765",
            json={"title": "Web Summit Vancouver 2026"},
            timeout=60,
        )

    def test_update_requires_expected_slug(self):
        wp = offline_client()

        with self.assertRaises(TypeError):
            wp.update_post(11765, {"content": "<p>Body</p>"})

        self.assertEqual(wp.s.mock_calls, [])

    def test_update_rejects_mismatched_singleton_without_posting(self):
        found = mock.Mock(status_code=200)
        found.json.return_value = [{"id": 999, "slug": "calling-us-all-in"}]
        wp = offline_client()
        wp.s.get.return_value = found

        with self.assertRaises(SlugVerificationFailed):
            wp.update_post(
                11765,
                {
                    "title": "Web Summit Vancouver 2026",
                    "slug": "web-summit-vancouver-2026",
                },
                expected_slug="web-summit-vancouver-2026",
            )

        wp.s.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
