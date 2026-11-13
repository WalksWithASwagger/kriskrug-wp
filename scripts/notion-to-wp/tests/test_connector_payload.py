import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import connector_payload  # noqa: E402
from cp1252_text import UnstorableText  # noqa: E402


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

    def test_seo_meta_passed_in_unfolded_is_refused(self):
        # run() folds the SEO title and description it derives before this
        # point, so an unfolded value here did not come from it: fail closed.
        combining_title = "Ethọ́s Lab Block Party | Kris Krüg"
        with self.assertRaisesRegex(UnstorableText, "SEO title .*Combining marks"):
            connector_payload.build_wp_payload(
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
                meta_desc="A description.",
            )

    def test_publicize_message_derived_from_the_excerpt_is_folded_with_a_warning(self):
        excerpt = "Ethọ́s Lab → Łódź 🙂 opened the night."
        warnings = []

        payload = connector_payload.build_wp_payload(
            title="Ethọ́s Lab",
            slug="ethos-lab",
            force_publish=False,
            pub_datetime="2026-06-23T12:00:00",
            author_id=1,
            excerpt=excerpt,
            body_html="<p>Body</p>",
            page_id="12345678-1234-1234-1234-123456789abc",
            featured=False,
            seo_title="Ethos Lab | Kris Krüg",
            meta_desc="Ethos Lab Lódz opened the night.",
            warn=warnings.append,
        )

        self.assertEqual(
            payload["meta"]["jetpack_publicize_message"], "Ethos Lab Lódz opened the night."
        )
        self.assertEqual(
            warnings,
            [
                f'seo: folded jetpack_publicize_message: "{excerpt}" -> '
                '"Ethos Lab Lódz opened the night."'
            ],
        )
        # The client sends these as numeric references; only plain-text meta folds.
        self.assertEqual(payload["title"], "Ethọ́s Lab")
        self.assertEqual(payload["excerpt"], excerpt)

    def test_plain_text_meta_keeps_cp1252_punctuation_as_written(self):
        long_excerpt = "Kris Krüg’s café notes. " + "x" * 260
        warnings = []
        payload = connector_payload.build_wp_payload(
            title="KK’s Field Notes",
            slug="kks-field-notes",
            force_publish=False,
            pub_datetime="2026-06-23T12:00:00",
            author_id=1,
            excerpt=long_excerpt,
            body_html="<p>Body</p>",
            page_id="12345678-1234-1234-1234-123456789abc",
            featured=False,
            seo_title="KK’s Field Notes | Kris Krüg",
            meta_desc="“Café Krüg” – the notes…",
            warn=warnings.append,
        )

        self.assertEqual(warnings, [])
        meta = payload["meta"]
        self.assertEqual(meta["jetpack_seo_html_title"], "KK’s Field Notes | Kris Krüg")
        self.assertEqual(meta["advanced_seo_description"], "“Café Krüg” – the notes…")
        # derive_social_message ends a cut message with an ellipsis of its own.
        self.assertTrue(meta["jetpack_publicize_message"].endswith("…"))
        self.assertEqual(payload["title"], "KK’s Field Notes")
        self.assertEqual(payload["excerpt"], long_excerpt)


if __name__ == "__main__":
    unittest.main()
