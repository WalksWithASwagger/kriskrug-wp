import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import draft_queue_audit  # noqa: E402


class DraftQueueAuditTests(unittest.TestCase):
    def test_local_draft_metrics_reads_package_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft_dir = Path(tmp) / "content" / "drafts" / "example"
            images_dir = draft_dir / "images"
            images_dir.mkdir(parents=True)
            (images_dir / "hero.jpg").write_bytes(b"fake")
            (draft_dir / "post.md").write_text(
                "---\n"
                "title: Example Draft\n"
                "slug: example-draft\n"
                "status: draft\n"
                "---\n"
                "Opening paragraph with [one](https://example.com).\n\n"
                "TODO: choose final image.\n",
                encoding="utf-8",
            )
            (draft_dir / "post.html").write_text(
                "<!-- wp:paragraph -->\n"
                '<p>Opening paragraph with <a href="https://example.com">one</a>.</p>\n'
                "<!-- /wp:paragraph -->\n",
                encoding="utf-8",
            )

            metric = draft_queue_audit.local_draft_metrics(draft_dir)

        self.assertEqual(metric.title, "Example Draft")
        self.assertEqual(metric.slug, "example-draft")
        self.assertEqual(metric.markdown_links, 1)
        self.assertEqual(metric.html_links, 1)
        self.assertEqual(metric.image_files, 1)
        self.assertEqual(metric.blocks, 1)
        self.assertEqual(metric.todos, 1)

    def test_render_markdown_includes_counts_and_gate(self):
        local = draft_queue_audit.LocalDraft(
            path="content/drafts/example",
            title="Example Draft",
            slug="example-draft",
            status="draft",
            words=1200,
            markdown_links=4,
            html_links=4,
            markdown_images=0,
            html_images=1,
            image_files=1,
            blocks=80,
            todos=0,
            files=["post.md", "post.html"],
        )
        wp = draft_queue_audit.WPDraft(
            kind="post",
            wp_id=123,
            status="draft",
            slug="example-draft",
            title="Example Draft",
            date="2026-05-22T12:00:00",
            modified="2026-05-22T12:00:00",
            words=1200,
            links=4,
            images=1,
            blocks=80,
            featured_media=456,
            categories=[1665],
            tags=[],
        )
        match = draft_queue_audit.WPMatch(
            kind="post",
            wp_id=123,
            status="draft",
            title="Example Draft",
            link="https://kriskrug.co/?p=123",
        )

        markdown = draft_queue_audit.render_markdown(
            [local],
            [
                {"kind": "posts", "status": "future", "count": 0},
                {"kind": "posts", "status": "draft", "count": 1},
                {"kind": "posts", "status": "pending", "count": 0},
                {"kind": "posts", "status": "private", "count": 0},
                {"kind": "pages", "status": "future", "count": 0},
                {"kind": "pages", "status": "draft", "count": 0},
                {"kind": "pages", "status": "pending", "count": 0},
                {"kind": "pages", "status": "private", "count": 0},
            ],
            [wp],
            {"example-draft": [match]},
        )

        self.assertIn("| Posts | 0 | 1 | 0 | 0 |", markdown)
        self.assertIn("post 123 (draft)", markdown)
        self.assertIn("Required Promotion Gate", markdown)

    def test_frontmatter_falls_back_when_yaml_is_loose(self):
        frontmatter, body = draft_queue_audit.split_frontmatter(
            "---\n"
            "title: Loose Draft\n"
            "slug: loose-draft\n"
            "excerpt: This has a colon: and is not quoted\n"
            "---\n"
            "Body copy.\n"
        )

        self.assertEqual(frontmatter["title"], "Loose Draft")
        self.assertEqual(frontmatter["slug"], "loose-draft")
        self.assertEqual(body, "Body copy.\n")


if __name__ == "__main__":
    unittest.main()
