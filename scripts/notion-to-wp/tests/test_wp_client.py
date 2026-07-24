from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from wp_client import WordPress  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
