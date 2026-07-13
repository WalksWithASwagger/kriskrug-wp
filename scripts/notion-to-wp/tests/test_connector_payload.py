import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import connector_payload  # noqa: E402


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

    def test_seo_meta_strips_combining_diacritics_but_keeps_visible_title(self):
        # "Ethọ́s" = E t h o + U+0323 (combining dot below) + U+0301 (combining acute) + s
        combining_title = "Ethọ́s Lab Block Party | Kris Krüg"
        payload = connector_payload.build_wp_payload(
            title=combining_title,
            slug="ethos-lab-block-party",
            force_publish=False,
            pub_datetime="2026-06-23T12:00:00",
            author_id=1,
            excerpt="An excerpt.",
            body_html="<p>Body</p>",
            page_id="12345678-1234-1234-1234-123456789abc",
            featured=False,
            seo_title=combining_title,
            meta_desc="A description about Ethọ́s Lab.",
        )

        seo_title = payload["meta"]["jetpack_seo_html_title"]
        seo_desc = payload["meta"]["advanced_seo_description"]

        # The REST-breaking combining marks (category Mn) are gone from SEO meta.
        self.assertFalse(any(__import__("unicodedata").combining(c) for c in seo_title))
        self.assertFalse(any(__import__("unicodedata").combining(c) for c in seo_desc))
        # Precomposed accents survive (ü is a single NFC codepoint, not combining).
        self.assertIn("Kris Krüg", seo_title)
        # The visible post title keeps its original diacritics untouched.
        self.assertEqual(payload["title"], combining_title)

    def test_normalize_seo_meta_leaves_plain_and_precomposed_text_unchanged(self):
        self.assertEqual(connector_payload.normalize_seo_meta("Kris Krüg"), "Kris Krüg")
        self.assertEqual(connector_payload.normalize_seo_meta("Plain ASCII"), "Plain ASCII")


if __name__ == "__main__":
    unittest.main()
