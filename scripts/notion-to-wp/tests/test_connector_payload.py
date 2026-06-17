import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import connector_payload  # noqa: E402
import kk_notion_to_wp  # noqa: E402


class ConnectorPayloadTests(unittest.TestCase):
    def test_build_wp_payload_preserves_dry_run_rest_shape(self):
        payload = connector_payload.build_wp_payload(
            title="Your Taste Is Your Moat",
            slug="your-taste-is-your-moat",
            force_publish=False,
            pub_datetime="2026-06-17T12:00:00",
            author_id=1,
            excerpt="A short KK-voice excerpt.",
            body_html="<p>Body</p>",
            page_id="12345678-1234-1234-1234-123456789abc",
            featured=True,
            seo_title="Your Taste Is Your Moat | Kris Krüg",
            meta_desc="A short KK-voice excerpt.",
        )

        self.assertEqual(
            payload,
            {
                "title": "Your Taste Is Your Moat",
                "slug": "your-taste-is-your-moat",
                "status": "draft",
                "date": "2026-06-17T12:00:00",
                "author": 1,
                "excerpt": "A short KK-voice excerpt.",
                "content": "<p>Body</p>",
                "meta": {
                    "kk_notion_source_id": "12345678-1234-1234-1234-123456789abc",
                    "kk_featured": "1",
                    "jetpack_seo_html_title": "Your Taste Is Your Moat | Kris Krüg",
                    "advanced_seo_description": "A short KK-voice excerpt.",
                    "jetpack_publicize_message": "A short KK-voice excerpt.",
                },
            },
        )

    def test_wrapper_reexports_payload_builder_for_connector_callers(self):
        self.assertIs(kk_notion_to_wp.build_wp_payload, connector_payload.build_wp_payload)


if __name__ == "__main__":
    unittest.main()
