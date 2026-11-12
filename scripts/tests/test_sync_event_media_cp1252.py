"""Event hero alt text outside cp1252 reaches the database as numeric references (#1225).

Offline: a mock session stands in for WordPress.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/events_page"))

import sync_event_media  # noqa: E402


class EventMediaAltTextTests(unittest.TestCase):
    def test_alt_text_above_latin1_is_sent_as_references(self):
        uploaded = mock.Mock()
        uploaded.json.return_value = {"id": 77, "source_url": "https://example.test/hero.jpg"}
        wp = sync_event_media.WPMedia.__new__(sync_event_media.WPMedia)
        wp.base = "https://example.test"
        wp.s = mock.Mock()
        wp.s.post.return_value = uploaded

        with tempfile.TemporaryDirectory() as tmp:
            hero = Path(tmp) / "hero.jpg"
            hero.write_bytes(b"jpeg fixture")
            wp.upload(hero, alt="Eth\u1ecd\u0301s Lab → Krüg (photo: Café)", mime="image/jpeg")

        alt_call = wp.s.post.call_args_list[1]
        self.assertEqual(
            alt_call.kwargs["json"],
            {"alt_text": "Eth&#7885;&#769;s Lab &#8594; Krüg (photo: Café)"},
        )


if __name__ == "__main__":
    unittest.main()
