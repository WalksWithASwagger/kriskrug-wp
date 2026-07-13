import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import create_local_wp_draft  # noqa: E402
import publish_common  # noqa: E402


class CreateLocalWPDraftTests(unittest.TestCase):
    def write_package(self, root: Path, seo_title: str = "SEO title") -> Path:
        draft_dir = root / "draft"
        draft_dir.mkdir()
        post_md = draft_dir / "post.md"
        post_md.write_text(
            "---\n"
            "title: Guarded Draft\n"
            "slug: guarded-draft\n"
            "status: draft\n"
            "excerpt: A guarded draft.\n"
            "seo:\n"
            f"  meta_title: {seo_title}\n"
            "  meta_description: About Ethọ́s Lab\n"
            "---\n"
            "Body\n",
            encoding="utf-8",
        )
        (draft_dir / "post.html").write_text(
            "<!-- wp:paragraph --><p>Body</p><!-- /wp:paragraph -->",
            encoding="utf-8",
        )
        return post_md

    def test_resolve_local_src_accepts_repo_relative_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft_dir = root / "content" / "drafts" / "example"
            image = draft_dir / "images" / "hero.jpg"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"fake")

            resolved = create_local_wp_draft.resolve_local_src(
                "content/drafts/example/images/hero.jpg",
                draft_dir,
                repo_root=root,
            )

        self.assertEqual(resolved, image.resolve())

    def test_resolve_local_src_accepts_draft_relative_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft_dir = root / "content" / "drafts" / "example"
            image = draft_dir / "images" / "hero.jpg"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"fake")

            resolved = create_local_wp_draft.resolve_local_src(
                "images/hero.jpg",
                draft_dir,
                repo_root=root,
            )

        self.assertEqual(resolved, image.resolve())

    def test_rewrite_uploaded_images_replaces_src_and_wp_image_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft_dir = root / "content" / "drafts" / "example"
            image = draft_dir / "images" / "hero.jpg"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"fake")
            body = (
                '<figure><img src="content/drafts/example/images/hero.jpg" '
                'alt="Hero" class="wp-image-TBD"/></figure>'
            )

            rewritten = create_local_wp_draft.rewrite_uploaded_images(
                body,
                draft_dir,
                {
                    image.resolve(): {
                        "id": 123,
                        "source_url": "https://kriskrug.co/wp-content/uploads/hero.jpg",
                    }
                },
                repo_root=root,
            )

        self.assertIn('src="https://kriskrug.co/wp-content/uploads/hero.jpg"', rewritten)
        self.assertIn('class="wp-image-123"', rewritten)
        self.assertNotIn("content/drafts/example/images/hero.jpg", rewritten)

    def test_rewrite_uploaded_images_adds_class_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft_dir = root / "content" / "drafts" / "example"
            image = draft_dir / "images" / "hero.jpg"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"fake")

            rewritten = create_local_wp_draft.rewrite_uploaded_images(
                '<img src="images/hero.jpg" alt="Hero"/>',
                draft_dir,
                {
                    image.resolve(): {
                        "id": 456,
                        "source_url": "https://kriskrug.co/wp-content/uploads/hero.jpg",
                    }
                },
                repo_root=root,
            )

        self.assertIn('class="wp-image-456"/>', rewritten)

    def test_slug_collision_aborts_before_uploads_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            cfg = create_local_wp_draft.WPConfig("https://example.test", "user", "pass", 1)
            with (
                mock.patch.object(create_local_wp_draft, "load_wp_config", return_value=cfg),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(
                    create_local_wp_draft,
                    "assert_slug_available",
                    side_effect=RuntimeError("slug collision"),
                ),
                mock.patch.object(create_local_wp_draft, "upload_images") as upload_images,
            ):
                with self.assertRaisesRegex(RuntimeError, "slug collision"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

        upload_images.assert_not_called()
        wp.create_post.assert_not_called()
        wp.update_post.assert_not_called()

    def test_bad_readback_fails_visibly_after_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            wp.create_post.return_value = {"id": 99}
            wp.get_post.return_value = {"id": 99, "status": "publish", "slug": "wrong"}
            cfg = create_local_wp_draft.WPConfig("https://example.test", "user", "pass", 1)
            with (
                mock.patch.object(create_local_wp_draft, "load_wp_config", return_value=cfg),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(create_local_wp_draft, "assert_slug_available"),
                mock.patch.object(create_local_wp_draft, "upload_images", return_value={}),
            ):
                with self.assertRaisesRegex(RuntimeError, "unexpected readback"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

        wp.create_post.assert_called_once()
        wp.get_post.assert_called_once_with(99)

    def test_payload_uses_canonical_seo_normalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp), seo_title="Ethọ́s Lab")
            pkg = create_local_wp_draft.load_package(post_md)
            cfg = create_local_wp_draft.WPConfig("https://example.test", "user", "pass", 1)
            payload = create_local_wp_draft.build_payload(pkg, cfg, pkg.body_html, {})

        self.assertEqual(
            payload["meta"],
            publish_common.build_seo_meta("Ethọ́s Lab", "About Ethọ́s Lab"),
        )
        self.assertFalse(
            any(
                __import__("unicodedata").combining(char)
                for value in payload["meta"].values()
                for char in value
            )
        )


if __name__ == "__main__":
    unittest.main()
