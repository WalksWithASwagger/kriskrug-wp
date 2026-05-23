import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
