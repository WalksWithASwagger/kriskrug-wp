import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import prepare_review_draft  # noqa: E402


class PrepareReviewDraftTests(unittest.TestCase):
    def test_markdown_to_blocks_outputs_gutenberg_blocks(self):
        html = prepare_review_draft.markdown_to_blocks(
            "## Heading\n\nA paragraph with [a link](https://example.com).\n\n- one\n- two\n"
        )

        self.assertIn("<!-- wp:heading -->", html)
        self.assertIn("<!-- wp:paragraph -->", html)
        self.assertIn("<!-- wp:list -->", html)
        self.assertIn('<a href="https://example.com">a link</a>', html)

    def test_quality_gate_flags_private_markers(self):
        pkg = prepare_review_draft.DraftPackage(
            path=Path("post.md"),
            frontmatter={
                "title": "Draft",
                "slug": "draft",
                "featured_media_id": 1,
            },
            body="/Users/kk/private\n\n" + "word " * 950 + "[link](https://example.com)\n" * 4,
        )
        html = prepare_review_draft.markdown_to_blocks(pkg.body)

        issues = prepare_review_draft.quality_issues(pkg, html)

        self.assertTrue(any("/Users/" in issue for issue in issues))

    def test_quality_gate_flags_absolute_frontmatter_paths(self):
        pkg = prepare_review_draft.DraftPackage(
            path=Path("post.md"),
            frontmatter={
                "title": "Draft",
                "slug": "draft",
                "featured_media_id": 1,
                "source_pack": {"kb_recap": "/Users/kk/private.md"},
            },
            body="word " * 950 + "[one](https://example.com)\n" * 4,
        )
        html = prepare_review_draft.markdown_to_blocks(pkg.body)

        issues = prepare_review_draft.quality_issues(pkg, html)

        self.assertIn("frontmatter contains an absolute local path", issues)


class FakeWordPress:
    def __init__(self):
        self.writes = []

    def get_post(self, post_id):
        return {"id": post_id, "slug": "draft", "status": "draft", "title": {"raw": "Draft"}}

    def ensure_term(self, taxonomy, name):
        self.writes.append(("ensure_term", taxonomy, name))
        return 900

    def update_post(self, post_id, payload, *, expected_slug):
        self.writes.append(("update_post", post_id, payload))
        return {"id": post_id, "link": "https://wp.example.test/?p=123", "meta": payload.get("meta")}


class PrepareReviewDraftSeoMetaTests(unittest.TestCase):
    """SEO meta goes through the shared cp1252 rule before any write (#1225)."""

    def write_post(self, root: Path, seo_title: str) -> Path:
        post = root / "post.md"
        post.write_text(
            "---\n"
            "title: Draft\n"
            "slug: draft\n"
            "categories: [Vancouver AI Ecosystem]\n"
            "tags: [Ethos]\n"
            "seo:\n"
            f"  meta_title: {seo_title}\n"
            "  meta_description: About the lab\n"
            "---\n\n" + "word " * 50 + "\n",
            encoding="utf-8",
        )
        return post

    def run_main(self, post: Path, wp):
        argv = ["prepare_review_draft.py", str(post), "--wp-id", "123", "--no-write"]
        out = io.StringIO()
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(prepare_review_draft, "WordPress", lambda *a, **k: wp),
            mock.patch.object(prepare_review_draft, "load_config", mock.Mock()),
            contextlib.redirect_stdout(out),
        ):
            code = prepare_review_draft.main()
        return code, out.getvalue()

    def test_unstorable_seo_meta_exits_4_with_zero_writes(self):
        wp = FakeWordPress()
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_main(self.write_post(Path(tmp), "Eth\u1ecd\u0301s Lab"), wp)

        self.assertEqual(code, 4)
        self.assertIn("ERROR: SEO title has characters the database cannot store", out)
        self.assertEqual(wp.writes, [])

    def test_storable_seo_meta_is_sent_as_built(self):
        wp = FakeWordPress()
        with tempfile.TemporaryDirectory() as tmp:
            code, out = self.run_main(self.write_post(Path(tmp), "KK’s Lab"), wp)

        self.assertEqual(code, 0, out)
        update = wp.writes[-1]
        self.assertEqual(update[0], "update_post")
        self.assertEqual(
            update[2]["meta"],
            {"jetpack_seo_html_title": "KK’s Lab", "advanced_seo_description": "About the lab"},
        )


if __name__ == "__main__":
    unittest.main()
