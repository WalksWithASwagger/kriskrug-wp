import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import create_local_wp_draft  # noqa: E402


class CreateLocalWPDraftTests(unittest.TestCase):
    def write_package(
        self,
        root: Path,
        seo_title: str = "SEO title",
        seo_description: str = "About Café Krüg",
    ) -> Path:
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
            f"  meta_description: {seo_description}\n"
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

        self.assertIn(
            'src="https://kriskrug.co/wp-content/uploads/hero.jpg"', rewritten
        )
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

    def test_dry_run_succeeds_without_wp_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            with (
                mock.patch.dict(
                    "os.environ",
                    {
                        "WP_USER": "",
                        "WP_APP_PASSWORD": "",
                        "WP_API_USERNAME": "",
                        "WP_API_PASSWORD": "",
                    },
                    clear=False,
                ),
                mock.patch.object(create_local_wp_draft, "LOCAL_ENV_PATH") as local_env,
                mock.patch.object(create_local_wp_draft, "KKAI_ENV_PATH") as kkai_env,
                mock.patch.object(create_local_wp_draft, "WordPress") as wp_cls,
                mock.patch.object(create_local_wp_draft, "load_wp_config") as load_cfg,
            ):
                local_env.exists.return_value = False
                kkai_env.exists.return_value = False
                result = create_local_wp_draft.create_local_draft(post_md, dry_run=True)

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["slug"], "guarded-draft")
        self.assertEqual(result["slug_check"], "skipped_offline")
        load_cfg.assert_not_called()
        wp_cls.assert_not_called()

    def test_execute_still_requires_wp_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            with (
                mock.patch.dict(
                    "os.environ",
                    {
                        "WP_USER": "",
                        "WP_APP_PASSWORD": "",
                        "WP_API_USERNAME": "",
                        "WP_API_PASSWORD": "",
                    },
                    clear=False,
                ),
                mock.patch.object(create_local_wp_draft, "LOCAL_ENV_PATH") as local_env,
                mock.patch.object(create_local_wp_draft, "KKAI_ENV_PATH") as kkai_env,
            ):
                local_env.exists.return_value = False
                kkai_env.exists.return_value = False
                with self.assertRaisesRegex(RuntimeError, "WP credentials not found"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

    def test_slug_collision_aborts_before_uploads_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            cfg = create_local_wp_draft.WPConfig(
                "https://example.test", "user", "pass", 1
            )
            with (
                mock.patch.object(
                    create_local_wp_draft, "load_wp_config", return_value=cfg
                ),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(
                    create_local_wp_draft,
                    "assert_slug_available",
                    side_effect=RuntimeError("slug collision"),
                ),
                mock.patch.object(
                    create_local_wp_draft, "upload_images"
                ) as upload_images,
            ):
                with self.assertRaisesRegex(RuntimeError, "slug collision"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

        upload_images.assert_not_called()
        wp.create_post.assert_not_called()
        wp.update_post.assert_not_called()

    def test_ambiguous_slug_lookup_aborts_before_uploads_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            wp.base = "https://example.test"
            wp.s.get.return_value.status_code = 200
            wp.s.get.return_value.json.return_value = [
                {"id": 11, "slug": "guarded-draft", "status": "draft"},
                {"id": 12, "slug": "guarded-draft", "status": "draft"},
            ]
            cfg = create_local_wp_draft.WPConfig(
                "https://example.test", "user", "pass", 1
            )
            with (
                mock.patch.object(
                    create_local_wp_draft, "load_wp_config", return_value=cfg
                ),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(
                    create_local_wp_draft, "upload_images"
                ) as upload_images,
            ):
                with self.assertRaisesRegex(RuntimeError, "post 11 .*post 12"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

        upload_images.assert_not_called()
        wp.create_post.assert_not_called()
        wp.update_post.assert_not_called()

    def test_non_canonical_slug_owned_by_another_post_aborts_before_writes(self):
        # WordPress sanitize_title()s the slug query, so "Guarded-Dräft" finds the
        # existing "guarded-draft" post. That must abort, not read as absent.
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            post_md.write_text(
                post_md.read_text(encoding="utf-8").replace(
                    "slug: guarded-draft", "slug: Guarded-Dräft"
                ),
                encoding="utf-8",
            )
            wp = mock.Mock()
            wp.base = "https://example.test"
            wp.s.get.return_value.status_code = 200
            wp.s.get.return_value.json.return_value = [
                {"id": 77, "slug": "guarded-draft", "status": "publish"}
            ]
            cfg = create_local_wp_draft.WPConfig(
                "https://example.test", "user", "pass", 1
            )
            with (
                mock.patch.object(
                    create_local_wp_draft, "load_wp_config", return_value=cfg
                ),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(
                    create_local_wp_draft, "upload_images"
                ) as upload_images,
            ):
                with self.assertRaisesRegex(RuntimeError, "guarded-draft"):
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
            cfg = create_local_wp_draft.WPConfig(
                "https://example.test", "user", "pass", 1
            )
            with (
                mock.patch.object(
                    create_local_wp_draft, "load_wp_config", return_value=cfg
                ),
                mock.patch.object(create_local_wp_draft, "WordPress", return_value=wp),
                mock.patch.object(create_local_wp_draft, "assert_slug_available"),
                mock.patch.object(
                    create_local_wp_draft, "upload_images", return_value={}
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "unexpected readback"):
                    create_local_wp_draft.create_local_draft(post_md, dry_run=False)

        wp.create_post.assert_called_once()
        wp.get_post.assert_called_once_with(99)

    def test_payload_seo_meta_keeps_cp1252_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp), seo_title="KK’s Lab")
            pkg = create_local_wp_draft.load_package(post_md)
            cfg = create_local_wp_draft.WPConfig(
                "https://example.test", "user", "pass", 1
            )
            payload = create_local_wp_draft.build_payload(pkg, cfg, pkg.body_html, {})

        self.assertEqual(
            payload["meta"],
            {
                "jetpack_seo_html_title": "KK’s Lab",
                "advanced_seo_description": "About Café Krüg",
            },
        )

    def test_quality_gate_refuses_seo_meta_before_any_write(self):
        for field in ("seo_title", "seo_description"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                post_md = self.write_package(Path(tmp), **{field: "Ethọ́s Lab"})
                with mock.patch.object(create_local_wp_draft, "WordPress") as wordpress:
                    with self.assertRaisesRegex(RuntimeError, "quality gate failed: SEO"):
                        create_local_wp_draft.create_local_draft(post_md, dry_run=False)
                wordpress.assert_not_called()

    def test_hand_written_seo_meta_is_refused_not_folded(self):
        # Frontmatter SEO meta is the operator's own copy, so the fold that
        # the connector applies to the meta it derives never applies here.
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp), seo_title="Ethọ́s Lab")
            argv = ["create_local_wp_draft.py", str(post_md), "--execute"]
            stdout, stderr = io.StringIO(), io.StringIO()
            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(create_local_wp_draft, "load_wp_config") as load_wp_config,
                mock.patch.object(create_local_wp_draft, "WordPress") as wordpress,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                code = create_local_wp_draft.main()

        self.assertEqual(code, 2)
        self.assertIn("SEO title has characters the database cannot store", stderr.getvalue())
        self.assertIn("U+0301 COMBINING ACUTE ACCENT", stderr.getvalue())
        self.assertNotIn("seo: folded", stdout.getvalue() + stderr.getvalue())
        load_wp_config.assert_not_called()
        wordpress.assert_not_called()

    def test_quality_gate_refuses_a_body_it_cannot_send_before_any_write(self):
        bodies = {
            "C1 control": "<!-- wp:paragraph --><p>it\x92s</p><!-- /wp:paragraph -->",
            "style": '<!-- wp:html --><style>.a::after{content:"→"}</style><!-- /wp:html -->',
        }
        for label, body in bodies.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                post_md = self.write_package(Path(tmp))
                (post_md.parent / "post.html").write_text(body, encoding="utf-8")
                with mock.patch.object(create_local_wp_draft, "WordPress") as wordpress:
                    with self.assertRaisesRegex(RuntimeError, "quality gate failed: content: "):
                        create_local_wp_draft.create_local_draft(post_md, dry_run=False)
                wordpress.assert_not_called()


if __name__ == "__main__":
    unittest.main()
