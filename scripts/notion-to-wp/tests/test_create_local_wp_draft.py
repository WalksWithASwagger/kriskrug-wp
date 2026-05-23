import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import create_local_wp_draft  # noqa: E402


class CreateLocalWPDraftTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
