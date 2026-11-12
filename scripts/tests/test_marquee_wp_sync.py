"""Marquee board sync uses the shared fail-closed slug lookup (#1217).

A failed or ambiguous lookup used to return None, and sync_board then uploaded
media and created a duplicate board. Offline fakes only; nothing calls WordPress.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/marquee"))

import wp_sync  # noqa: E402
from cp1252_text import UnstorableText  # noqa: E402
from wp_client import SlugVerificationFailed  # noqa: E402

BOARD = {
    "id": "2026-w26-the-model-is-the-message",
    "status": "live",
    "week": "2026-W26",
    "board": ["THE MODEL", "IS THE", "MESSAGE"],
    "dek": "A test board.",
    "source": {"title": "Understanding Media", "author": "Marshall McLuhan"},
}
SLUG = wp_sync.build_payload(BOARD)["slug"]
ENDPOINT = f"https://example.test/wp-json/wp/v2/{wp_sync.POST_TYPE}"


def response(status_code, body):
    r = mock.Mock(status_code=status_code)
    r.json.return_value = body
    return r


def offline_client(*responses) -> wp_sync.MarqueeWP:
    wp = wp_sync.MarqueeWP.__new__(wp_sync.MarqueeWP)
    wp.base = "https://example.test"
    wp.s = mock.Mock()
    wp.s.get.side_effect = list(responses)
    return wp


def sync(wp):
    return wp_sync.sync_board(
        wp, BOARD, None, execute=True, allow_update=False, log=lambda _: None
    )


class MarqueeSlugLookupTests(unittest.TestCase):
    def test_lookup_error_aborts_with_zero_writes(self):
        wp = offline_client(response(503, "<html>busy</html>"))

        with self.assertRaisesRegex(SlugVerificationFailed, "HTTP 503"):
            sync(wp)

        wp.s.post.assert_not_called()

    def test_two_boards_sharing_the_slug_abort_with_zero_writes(self):
        hits = [{"id": 1, "slug": SLUG}, {"id": 2, "slug": SLUG}]
        wp = offline_client(response(200, hits))

        with self.assertRaisesRegex(SlugVerificationFailed, "1, 2"):
            sync(wp)

        wp.s.post.assert_not_called()

    def test_absent_slug_still_creates_once(self):
        created = response(201, {"id": 42, "slug": SLUG})
        created.raise_for_status = mock.Mock()
        readback = response(200, {"id": 42, "slug": SLUG})
        readback.raise_for_status = mock.Mock()
        wp = offline_client(response(200, []), readback)
        wp.s.post.return_value = created

        out = sync(wp)

        self.assertEqual(out["status"], "created")
        lookup = wp.s.get.call_args_list[0]
        self.assertEqual(lookup.args[0], ENDPOINT)
        self.assertEqual(lookup.kwargs["params"]["slug"], SLUG)
        wp.s.post.assert_called_once()
        self.assertEqual(wp.s.post.call_args.args[0], ENDPOINT)


class MarqueeStorableTextTests(unittest.TestCase):
    """The database is cp1252; text outside it would be stored as "?" (#1225)."""

    def test_board_text_outside_cp1252_goes_out_as_references(self):
        board = {
            **BOARD,
            "dek": "Medium → message — McLuhan",
            "source": {"title": "Understanding Media", "remixed_from": "environments — not tools"},
        }
        created = response(201, {"id": 42, "slug": SLUG})
        created.raise_for_status = mock.Mock()
        readback = response(200, {"id": 42, "slug": SLUG})
        readback.raise_for_status = mock.Mock()
        wp = offline_client(response(200, []), readback)
        wp.s.post.return_value = created

        wp_sync.sync_board(wp, board, None, execute=True, allow_update=False, log=lambda _: None)

        body = wp.s.post.call_args.kwargs["json"]
        self.assertEqual(body["excerpt"], "Medium &#8594; message — McLuhan")
        self.assertEqual(json.loads(body["meta"]["_kk_mb_source"]), board["source"])
        self.assertIn("—", body["meta"]["_kk_mb_source"])

    def test_plain_meta_it_cannot_store_is_refused_before_the_image_upload(self):
        board = {**BOARD, "after": "Marshall McLuhan →"}
        wp = offline_client(response(200, []))

        with tempfile.TemporaryDirectory() as tmp:
            og_png = Path(tmp) / "og.png"
            og_png.write_bytes(b"png fixture")
            with self.assertRaisesRegex(UnstorableText, "_kk_mb_after"):
                wp_sync.sync_board(wp, board, og_png, execute=True, allow_update=False, log=lambda _: None)

        wp.s.get.assert_not_called()
        wp.s.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
