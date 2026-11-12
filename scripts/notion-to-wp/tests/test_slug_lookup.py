"""One fail-closed slug lookup behind every publisher (#1217).

The 2026-05-15 incident PATCHed the wrong post because a lookup trusted the
wrong record. These cases pin the same answer from all three public names, so a
lookup error, a shared slug or a hit with a different slug can never read as
"absent" or hand back a post.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import create_local_wp_draft  # noqa: E402
import publish_common  # noqa: E402
from notion_client import slugify  # noqa: E402
from update_safety import emit_update_diff_review  # noqa: E402
from wp_client import SlugVerificationFailed, WordPress, lookup_slug  # noqa: E402

SLUG = "web-summit-vancouver-2026"
POSTS = "https://example.test/wp-json/wp/v2/posts"
ONE = [{"id": 11765, "slug": SLUG, "status": "publish"}]
TWO = [
    {"id": 11765, "slug": SLUG, "status": "publish"},
    {"id": 11766, "slug": SLUG, "status": "draft"},
]
WRONG = [{"id": 999, "slug": "calling-us-all-in", "status": "publish"}]

# name -> (status code, body). Every scenario the issue lists.
SCENARIOS = {
    "200-empty": (200, []),
    "200-one": (200, ONE),
    "200-two": (200, TWO),
    "200-one-wrong-slug": (200, WRONG),
    "429": (429, {"code": "rest_too_many_requests"}),
    "500": (500, {"code": "internal_server_error"}),
}
FAILS_CLOSED = {"200-two", "200-one-wrong-slug", "429", "500"}


def response(status_code, body):
    r = mock.Mock(status_code=status_code)
    r.json.return_value = body
    return r


def offline_client(*responses) -> WordPress:
    wp = WordPress.__new__(WordPress)
    wp.base = "https://example.test"
    wp.s = mock.Mock()
    wp.s.get.side_effect = list(responses)
    return wp


class LookupSlugTests(unittest.TestCase):
    def test_queries_every_status_in_edit_context(self):
        wp = offline_client(response(200, []))

        lookup_slug(wp, SLUG)

        wp.s.get.assert_called_once_with(
            POSTS,
            params={"slug": SLUG, "status": "any", "per_page": 100, "context": "edit"},
            timeout=30,
        )

    def test_kind_selects_the_endpoint(self):
        wp = offline_client(response(200, []))

        lookup_slug(wp, SLUG, "pages")

        self.assertEqual(
            wp.s.get.call_args.args[0], "https://example.test/wp-json/wp/v2/pages"
        )

    def test_states(self):
        expected = {
            "200-empty": ("absent", ()),
            "200-one": ("unique", (11765,)),
            "200-two": ("ambiguous", (11765, 11766)),
        }
        for name, (state, ids) in expected.items():
            with self.subTest(scenario=name):
                match = lookup_slug(offline_client(response(*SCENARIOS[name])), SLUG)
                self.assertEqual((match.state, match.ids), (state, ids))

    def test_ambiguous_never_returns_a_record(self):
        match = lookup_slug(offline_client(response(200, TWO)), SLUG)

        with self.assertRaisesRegex(SlugVerificationFailed, "11765, 11766"):
            match.unique_or_none()

    def test_any_hit_with_a_different_slug_raises(self):
        for body in (WRONG, WRONG + ONE, ONE + WRONG):
            with self.subTest(body=body):
                with self.assertRaisesRegex(
                    SlugVerificationFailed, "999 \\('calling-us-all-in'\\)"
                ):
                    lookup_slug(offline_client(response(200, body)), SLUG)

    def test_non_canonical_slug_is_never_absent(self):
        # WordPress sanitize_title()s the query, so asking for an accented slug
        # returns the existing ASCII post. Main used to call that "already owned".
        hit = [{"id": 77, "slug": "kris-krug-notes", "status": "publish"}]

        with self.assertRaisesRegex(SlugVerificationFailed, "kris-krug-notes"):
            lookup_slug(offline_client(response(200, hit)), "Kris-Krüg-Notes")

    def test_non_200_raises_with_status_and_endpoint(self):
        for status in (401, 404, 429, 500, 503):
            with self.subTest(status=status):
                with self.assertRaises(SlugVerificationFailed) as caught:
                    lookup_slug(offline_client(response(status, ONE)), SLUG)
                self.assertIn(f"HTTP {status}", str(caught.exception))
                self.assertIn(POSTS, str(caught.exception))

    def test_unexpected_200_body_raises(self):
        for body in (
            {"code": "rest_no_route"},
            None,
            "<html>blocked</html>",
            ONE + ["x"],
        ):
            with self.subTest(body=body):
                with self.assertRaises(SlugVerificationFailed):
                    lookup_slug(offline_client(response(200, body)), SLUG)

    def test_non_json_200_body_raises(self):
        waf_page = mock.Mock(status_code=200)
        waf_page.json.side_effect = ValueError("Expecting value")

        with self.assertRaises(SlugVerificationFailed):
            lookup_slug(offline_client(waf_page), SLUG)

    def test_error_message_never_carries_credentials(self):
        wp = WordPress("https://example.test", "fixture-user", "fixture-app-password")
        auth_header = wp.s.headers["Authorization"]

        with mock.patch.object(wp.s, "get", return_value=response(429, {})):
            with self.assertRaises(SlugVerificationFailed) as caught:
                wp.find_post_by_slug(SLUG)

        message = str(caught.exception)
        for secret in (
            "fixture-user",
            "fixture-app-password",
            auth_header,
            auth_header.split()[-1],
        ):
            self.assertNotIn(secret, message)


class PublicNamesAgreeTests(unittest.TestCase):
    """The three old names delegate to lookup_slug and fail closed the same way."""

    def test_find_post_by_slug(self):
        expected = {"200-empty": None, "200-one": 11765}
        for name, scenario in SCENARIOS.items():
            with self.subTest(scenario=name):
                wp = offline_client(response(*scenario))
                if name in FAILS_CLOSED:
                    with self.assertRaises(SlugVerificationFailed):
                        wp.find_post_by_slug(SLUG)
                else:
                    self.assertEqual(wp.find_post_by_slug(SLUG), expected[name])

    def test_find_existing_post_by_slug(self):
        expected = {"200-empty": None, "200-one": ONE[0]}
        for name, scenario in SCENARIOS.items():
            with self.subTest(scenario=name):
                wp = offline_client(response(*scenario))
                if name in FAILS_CLOSED:
                    with self.assertRaises(SlugVerificationFailed):
                        publish_common.find_existing_post_by_slug(wp, SLUG)
                else:
                    self.assertEqual(
                        publish_common.find_existing_post_by_slug(wp, SLUG),
                        expected[name],
                    )

    def test_assert_slug_available(self):
        for name, scenario in SCENARIOS.items():
            with self.subTest(scenario=name):
                wp = offline_client(response(*scenario), response(200, []))
                if name == "200-empty":
                    create_local_wp_draft.assert_slug_available(wp, SLUG)
                elif name in {"200-one-wrong-slug", "429", "500"}:
                    with self.assertRaises(SlugVerificationFailed):
                        create_local_wp_draft.assert_slug_available(wp, SLUG)
                else:
                    with self.assertRaisesRegex(RuntimeError, "post 11765"):
                        create_local_wp_draft.assert_slug_available(wp, SLUG)

    def test_assert_slug_available_checks_pages_too(self):
        page = [{"id": 2672, "slug": SLUG, "status": "publish"}]
        wp = offline_client(response(200, []), response(200, page))

        with self.assertRaisesRegex(RuntimeError, "page 2672"):
            create_local_wp_draft.assert_slug_available(wp, SLUG)

    def test_diff_review_aborts_on_ambiguous_slug_before_reading_a_post(self):
        wp = offline_client(response(200, TWO))
        logs = []

        code = emit_update_diff_review(wp, SLUG, "Web Summit", {}, log=logs.append)

        self.assertEqual(code, 8)
        self.assertTrue(any("Refusing to pick one" in line for line in logs), logs)
        wp.s.get.assert_called_once()


class SlugifyMatchesWordPressTests(unittest.TestCase):
    """slugify must produce the slug WordPress stores, or exact matching fails closed."""

    def test_folds_accented_latin_to_ascii(self):
        cases = {
            "Kris Krüg Live": "kris-krug-live",
            "MØTLEYKRÜG": "motleykrug",
            "Ethọ́s": "ethos",
            "Ethọ́s": "ethos",
            "Æsir Œuvre Straße Łódź Þór Đorđe": "aesir-oeuvre-strasse-lodz-thor-dorde",
        }
        for title, slug in cases.items():
            with self.subTest(title=title):
                self.assertEqual(slugify(title), slug)

    def test_ascii_titles_are_unchanged(self):
        cases = {
            "Web Summit Vancouver 2026": "web-summit-vancouver-2026",
            "AI's Future: Now & Then": "ais-future-now-then",
            "  Keep the Machine Strange  ": "keep-the-machine-strange",
            "snake_case stays": "snake_case-stays",
        }
        for title, slug in cases.items():
            with self.subTest(title=title):
                self.assertEqual(slugify(title), slug)


if __name__ == "__main__":
    unittest.main()
