import argparse
import unittest
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from public_image_audit import (
    ImageParser,
    audit_images,
    collect_urls,
    is_filename_style_alt,
    media_id_from_class,
    summarize,
)


class PublicImageAuditTests(unittest.TestCase):
    def test_parser_classifies_decorative_and_problem_alt_states(self):
        parser = ImageParser("https://kriskrug.co/example/")
        parser.feed(
            """
            <img class="aurora-brand-logo" src="/logo.png" alt="">
            <img class="wp-image-123" src="/wp-content/uploads/flickr-photographr-badge.jpg" alt="flickr-photographr-badge.jpg" srcset="x 1x" loading="lazy">
            <img src="/missing.jpg">
            """
        )

        self.assertEqual(len(parser.images), 3)
        self.assertEqual(media_id_from_class(parser.images[1]["class"]), 123)
        self.assertTrue(is_filename_style_alt(parser.images[1]["alt"], parser.images[1]["src"]))

    def test_summary_counts_alt_states(self):
        from public_image_audit import RenderedImage

        rows = [
            RenderedImage("u", "url", None, "home", "/logo.png", "", None, "", False, "aurora-brand-logo", "", "", ""),
            RenderedImage("u", "url", None, "home", "/flickr-photographr-badge.jpg", "flickr-photographr-badge.jpg", 123, "lazy", True, "", "", "", ""),
            RenderedImage("u", "url", None, "home", "/missing.jpg", None, None, "", False, "", "", "", ""),
        ]

        stats = summarize(rows)

        self.assertEqual(stats["decorative_empty"], 1)
        self.assertEqual(stats["filename_style"], 1)
        self.assertEqual(stats["missing_attr"], 1)

    def test_collect_urls_normalizes_explicit_relative_urls(self):
        args = argparse.Namespace(
            base_url="https://kriskrug.co",
            urls=["/about/", "https://example.com/custom/"],
            ids=[],
            default_urls=False,
            kind=["post", "page"],
            limit=50,
            since="2025-01-01",
        )

        items = collect_urls(args)

        self.assertEqual(items[0]["link"], "https://kriskrug.co/about/")
        self.assertEqual(items[0]["slug"], "about")
        self.assertEqual(items[1]["link"], "https://example.com/custom/")

    def test_audit_images_parses_public_html_and_probes_image_urls(self):
        class FakeResponse:
            status_code = 200
            encoding = "utf-8"
            headers = {"content-length": "1234"}

            def __init__(self, body=""):
                self.body = body.encode("utf-8")

            def raise_for_status(self):
                return None

            def iter_content(self, chunk_size=65536):
                yield self.body

        class FakeSession:
            def __init__(self):
                self.head_calls = []

            def get(self, url, stream=False, timeout=None, **kwargs):
                return FakeResponse(
                    """
                    <img class="wp-image-77" src="/wp-content/uploads/photo.jpg" alt="Useful alt" loading="lazy" srcset="a 1x">
                    <img class="tracking-pixel" src="/pixel.gif" alt="">
                    """
                )

            def head(self, src, allow_redirects=True, timeout=20):
                self.head_calls.append(src)
                return FakeResponse()

        fake_session = FakeSession()
        args = argparse.Namespace(
            base_url="https://kriskrug.co",
            urls=["/example/"],
            ids=[],
            default_urls=False,
            kind=["post", "page"],
            limit=50,
            since="2025-01-01",
            timeout=20,
            check_urls=True,
        )

        with mock.patch("public_image_audit.public_session", return_value=fake_session):
            rows = audit_images(args)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].src, "https://kriskrug.co/wp-content/uploads/photo.jpg")
        self.assertEqual(rows[0].media_id, 77)
        self.assertEqual(rows[0].alt_state, "ok")
        self.assertEqual(rows[0].status, 200)
        self.assertEqual(rows[0].content_length, 1234)
        self.assertEqual(rows[1].alt_state, "decorative-empty")
        self.assertEqual(fake_session.head_calls, [
            "https://kriskrug.co/wp-content/uploads/photo.jpg",
            "https://kriskrug.co/pixel.gif",
        ])


if __name__ == "__main__":
    unittest.main()
