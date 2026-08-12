from __future__ import annotations

import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import sync_futureproof_polish_v2 as sync  # noqa: E402
import verify_futureproof_polish_v2 as verify  # noqa: E402


class Response:
    def __init__(self, payload: object, status_code: int = 200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> object:
        return self.payload


class FutureproofSyncTests(unittest.TestCase):
    def write_package(
        self,
        root: Path,
        *,
        slug: str = sync.TARGET_SLUG,
        status: str = "draft",
    ) -> Path:
        draft_dir = root / "futureproof"
        images = draft_dir / "images"
        images.mkdir(parents=True)
        featured = images / sync.FEATURED_FILENAME
        known = images / "vanai-meetup31-stage-kris-futureproof-slide.webp"
        new = images / "receipt-dent-kris-krug.png"
        featured.write_bytes(b"approved featured image")
        known.write_bytes(b"known image")
        new.write_bytes(b"new image")
        (draft_dir / "post.md").write_text(
            "---\n"
            "title: 'Futureproof Festival of AI: A Bat Signal from Vancouver'\n"
            f"slug: {slug}\n"
            f"status: {status}\n"
            "featured_media_id: 0\n"
            "excerpt: A deeper invitation to Futureproof Festival of AI.\n"
            "seo:\n"
            "  meta_title: Futureproof Festival of AI in Vancouver | Kris Krüg\n"
            "  meta_description: A clear Futureproof Festival description.\n"
            "images:\n"
            f"- file: images/{sync.FEATURED_FILENAME}\n"
            "  alt: Approved Futureproof salmon key art.\n"
            "  role: featured-graphic\n"
            "  source: https://futureproof.example/approved-key-art.jpg\n"
            "  credit: Futureproof Festival art layer.\n"
            "- file: images/vanai-meetup31-stage-kris-futureproof-slide.webp\n"
            "  alt: Kris presents Futureproof at Vancouver AI.\n"
            "  role: opening-proof\n"
            "  source: https://bc-ai.example/stage.webp\n"
            "  credit: 'Photo: Michael Caswell.'\n"
            "- file: images/receipt-dent-kris-krug.png\n"
            "  alt: DENT article receipt.\n"
            "  role: archival-receipt\n"
            "  source: https://kriskrug.co/dent/\n"
            "  credit: Screenshot captured for editorial reference.\n"
            "---\n"
            "Body\n",
            encoding="utf-8",
        )
        (draft_dir / "post.html").write_text(
            '<!-- wp:image {"sizeSlug":"large"} -->\n'
            f'<figure><img src="images/{sync.FEATURED_FILENAME}" '
            'alt="Key art" class="wp-image-TBD"/></figure>\n'
            '<!-- /wp:image -->\n'
            '<!-- wp:image {"sizeSlug":"large"} -->\n'
            '<figure><img src="images/vanai-meetup31-stage-kris-futureproof-slide.webp" '
            'alt="Stage" class="wp-image-TBD"/></figure>\n'
            '<!-- /wp:image -->\n'
            '<!-- wp:image {"lightbox":{"enabled":true}} -->\n'
            '<figure><img src="images/receipt-dent-kris-krug.png" '
            'alt="Receipt" class="visual wp-image-TBD"/></figure>\n'
            '<!-- /wp:image -->',
            encoding="utf-8",
        )
        return draft_dir / "post.md"

    @staticmethod
    def before_post(*, status: str = "draft", slug: str = sync.TARGET_SLUG) -> dict:
        return {
            "id": sync.TARGET_POST_ID,
            "status": status,
            "slug": slug,
            "title": {"raw": "Old title"},
            "content": {"raw": "<!-- wp:paragraph --><p>Old</p><!-- /wp:paragraph -->"},
            "excerpt": {"raw": "Old excerpt"},
            "featured_media": 12725,
            "meta": {
                "jetpack_seo_html_title": "Old SEO title",
                "advanced_seo_description": "Old SEO description",
            },
            "categories": [4],
            "tags": [8, 9],
            "author": 1,
            "date": "2026-07-26T12:00:00",
            "modified": "2026-08-12T14:40:00",
            "modified_gmt": "2026-08-12T22:40:00",
        }

    @staticmethod
    def known_media() -> dict:
        return {
            "id": 12725,
            "source_url": (
                "https://kriskrug.co/wp-content/uploads/2026/08/"
                "vanai-meetup31-stage-kris-futureproof-slide.webp"
            ),
            "media_details": {},
        }

    def config(self):
        return sync.WPConfig("https://kriskrug.co", "user", "password", 1)

    def test_verifier_accepts_manifest_receipts_when_ignored_images_are_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft_dir = Path(tmp)
            lines = ["## V2 visual package"]
            for name, (width, height) in verify.EXPECTED_IMAGE_SIZES.items():
                lines.append(
                    f"| `{name}` | {width}×{height} | "
                    f"{verify.EXPECTED_IMAGE_HASHES[name]} |"
                )
            for name, media_id in verify.EXPECTED_MEDIA_IDS.items():
                lines.append(f"| `{name}` | {media_id} | uploaded |")
            (draft_dir / "asset-manifest.md").write_text(
                "\n".join(lines), encoding="utf-8"
            )

            report = verify.image_artifact_report(draft_dir)

        self.assertTrue(report["manifest_receipts"])
        self.assertEqual(report["local_files_present"], 0)
        self.assertTrue(report["local_hashes_match"])
        self.assertTrue(report["local_state_valid"])

    def test_verifier_rejects_complete_local_set_with_hash_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft_dir = Path(tmp)
            images_dir = draft_dir / "images"
            images_dir.mkdir()
            for name in verify.EXPECTED_IMAGE_SIZES:
                (images_dir / name).write_bytes(b"wrong artifact")

            report = verify.image_artifact_report(draft_dir)

        self.assertEqual(
            report["local_files_present"], len(verify.EXPECTED_IMAGE_SIZES)
        )
        self.assertFalse(report["local_hashes_match"])
        self.assertFalse(report["local_state_valid"])

    def test_verifier_expected_featured_media_is_exact(self):
        self.assertEqual(
            verify.EXPECTED_MEDIA_IDS[
                "futureproof-salmon-starfield-share-20260711.jpg"
            ],
            12739,
        )

    def test_target_guard_rejects_non_draft_before_media_or_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            wp.get_post.return_value = self.before_post(status="publish")
            with (
                mock.patch.object(sync, "load_wp_config", return_value=self.config()),
                mock.patch.object(sync, "WordPress", return_value=wp),
                self.assertRaisesRegex(RuntimeError, "non-draft"),
            ):
                sync.sync_futureproof(post_md)

        wp.get_media.assert_not_called()
        wp.upload_media.assert_not_called()
        wp.update_post.assert_not_called()

    def test_package_rejects_image_path_escape_before_wordpress_access(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            post_md = self.write_package(root)
            outside = post_md.parent / "outside.jpg"
            outside.write_bytes(b"private bytes")
            text = post_md.read_text(encoding="utf-8")
            text = text.replace(
                f"images/{sync.FEATURED_FILENAME}", "images/../outside.jpg", 1
            )
            post_md.write_text(text, encoding="utf-8")
            with (
                mock.patch.object(sync, "load_wp_config") as load_config,
                self.assertRaisesRegex(RuntimeError, "canonical images/<filename>"),
            ):
                sync.sync_futureproof(post_md)

        load_config.assert_not_called()

    def test_package_rejects_symlink_escape_before_wordpress_access(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            post_md = self.write_package(root)
            outside = root / "outside.jpg"
            outside.write_bytes(b"private bytes")
            featured = post_md.parent / "images" / sync.FEATURED_FILENAME
            featured.unlink()
            featured.symlink_to(outside)
            with (
                mock.patch.object(sync, "load_wp_config") as load_config,
                self.assertRaisesRegex(RuntimeError, "regular file inside"),
            ):
                sync.sync_futureproof(post_md)

        load_config.assert_not_called()

    def test_dry_run_is_authenticated_but_never_uploads_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            wp = mock.Mock()
            wp.get_post.return_value = self.before_post()
            wp.get_media.return_value = self.known_media()
            wp.s.get.return_value = Response([])
            with (
                mock.patch.object(sync, "load_wp_config", return_value=self.config()),
                mock.patch.object(sync, "WordPress", return_value=wp),
            ):
                result = sync.sync_futureproof(post_md)

        self.assertTrue(result["dry_run"])
        self.assertEqual(
            result["missing_media"],
            [sync.FEATURED_FILENAME, "receipt-dent-kris-krug.png"],
        )
        self.assertEqual(
            result["would_upload"],
            [sync.FEATURED_FILENAME, "receipt-dent-kris-krug.png"],
        )
        self.assertIsNone(result["snapshot_path"])
        wp.get_post.assert_called_once_with(sync.TARGET_POST_ID)
        wp.upload_media.assert_not_called()
        wp.update_post.assert_not_called()

    def test_rewrite_adds_block_ids_and_replaces_src_and_classes(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            package = sync.load_package(post_md)
            media = {
                sync.FEATURED_FILENAME: {
                    "id": 13001,
                    "source_url": "https://kriskrug.co/uploads/key-art.jpg",
                },
                "vanai-meetup31-stage-kris-futureproof-slide.webp": {
                    "id": 12725,
                    "source_url": "https://kriskrug.co/uploads/stage.webp",
                },
                "receipt-dent-kris-krug.png": {
                    "id": 13002,
                    "source_url": "https://kriskrug.co/uploads/receipt.png",
                },
            }

            rewritten = sync.rewrite_image_blocks(package.body_html, media)

        self.assertIn('<!-- wp:image {"sizeSlug":"large","id":13001} -->', rewritten)
        self.assertIn('<!-- wp:image {"sizeSlug":"large","id":12725} -->', rewritten)
        self.assertIn('<!-- wp:image {"lightbox":{"enabled":true},"id":13002} -->', rewritten)
        self.assertIn('src="https://kriskrug.co/uploads/key-art.jpg"', rewritten)
        self.assertIn('class="visual wp-image-13002"', rewritten)
        self.assertNotIn("wp-image-TBD", rewritten)
        self.assertNotIn('src="images/', rewritten)

    def test_minimal_payload_omits_unsupported_seo_meta(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = sync.load_package(self.write_package(Path(tmp)))
            payload = sync.build_post_payload(
                package,
                "<!-- wp:paragraph --><p>Ready</p><!-- /wp:paragraph -->",
                featured_media_id=13001,
                seo_meta_supported=False,
            )

        self.assertEqual(
            set(payload), {"title", "content", "excerpt", "featured_media"}
        )
        self.assertNotIn("status", payload)
        self.assertNotIn("slug", payload)
        self.assertNotIn("date", payload)
        self.assertNotIn("meta", payload)

    def test_exact_media_search_aborts_when_filename_is_ambiguous(self):
        wp = mock.Mock()
        wp.s.get.return_value = Response(
            [
                {
                    "id": 41,
                    "source_url": "https://kriskrug.co/uploads/receipt.png",
                },
                {
                    "id": 42,
                    "source_url": "https://kriskrug.co/uploads/receipt.png",
                },
            ]
        )

        with self.assertRaisesRegex(RuntimeError, "ambiguous media match"):
            sync.search_media_exact(wp, Path("receipt.png"))

        wp.upload_media.assert_not_called()
        wp.update_post.assert_not_called()

    def test_apply_rechecks_draft_state_immediately_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            before = self.before_post()
            published = dict(before, status="publish")
            wp = mock.Mock()
            wp.get_post.side_effect = [before, published]
            wp.get_media.return_value = self.known_media()
            wp.s.get.return_value = Response([])
            wp.upload_media.side_effect = [
                {
                    "id": 13001,
                    "source_url": f"https://kriskrug.co/uploads/{sync.FEATURED_FILENAME}",
                },
                {
                    "id": 13002,
                    "source_url": "https://kriskrug.co/uploads/receipt-dent-kris-krug.png",
                },
            ]
            with (
                mock.patch.object(sync, "load_wp_config", return_value=self.config()),
                mock.patch.object(sync, "WordPress", return_value=wp),
                self.assertRaisesRegex(RuntimeError, "non-draft"),
            ):
                sync.sync_futureproof(post_md, apply=True)

        wp.update_post.assert_not_called()

    def test_apply_aborts_when_editor_changes_content_during_uploads(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            before = self.before_post()
            changed = dict(before)
            changed["content"] = {"raw": "<p>Concurrent editor change</p>"}
            changed["modified_gmt"] = "2026-08-12T22:45:00"
            wp = mock.Mock()
            wp.get_post.side_effect = [before, changed]
            wp.get_media.return_value = self.known_media()
            wp.s.get.return_value = Response([])
            wp.upload_media.side_effect = [
                {
                    "id": 13001,
                    "source_url": f"https://kriskrug.co/uploads/{sync.FEATURED_FILENAME}",
                },
                {
                    "id": 13002,
                    "source_url": "https://kriskrug.co/uploads/receipt-dent-kris-krug.png",
                },
            ]
            with (
                mock.patch.object(sync, "load_wp_config", return_value=self.config()),
                mock.patch.object(sync, "WordPress", return_value=wp),
                self.assertRaisesRegex(RuntimeError, "changed during sync"),
            ):
                sync.sync_futureproof(post_md, apply=True)

        wp.update_post.assert_not_called()

    def test_apply_snapshots_uploads_missing_and_verifies_exact_readback(self):
        with tempfile.TemporaryDirectory() as tmp:
            post_md = self.write_package(Path(tmp))
            before = self.before_post()
            wp = mock.Mock()
            wp.s.get.return_value = Response([])
            wp.get_media.return_value = self.known_media()
            wp.upload_media.side_effect = [
                {
                    "id": 13001,
                    "source_url": f"https://kriskrug.co/uploads/{sync.FEATURED_FILENAME}",
                },
                {
                    "id": 13002,
                    "source_url": "https://kriskrug.co/uploads/receipt-dent-kris-krug.png",
                },
            ]

            def read_post(_post_id: int) -> dict:
                if not wp.update_post.called:
                    return before
                payload = wp.update_post.call_args.args[1]
                after = dict(before)
                after.update(
                    {
                        "title": {"raw": payload["title"]},
                        "content": {"raw": payload["content"]},
                        "excerpt": {"raw": payload["excerpt"]},
                        "featured_media": payload["featured_media"],
                        "meta": payload["meta"],
                    }
                )
                return after

            wp.get_post.side_effect = read_post
            wp.update_post.return_value = {"id": sync.TARGET_POST_ID}
            with (
                mock.patch.object(sync, "load_wp_config", return_value=self.config()),
                mock.patch.object(sync, "WordPress", return_value=wp),
            ):
                result = sync.sync_futureproof(post_md, apply=True)

            snapshot = Path(result["snapshot_path"])
            snapshot_payload = json.loads(snapshot.read_text(encoding="utf-8"))
            snapshot_mode = stat.S_IMODE(snapshot.stat().st_mode)

        self.assertFalse(result["dry_run"])
        self.assertFalse(result["published"])
        self.assertEqual(
            result["new_media_ids"],
            {sync.FEATURED_FILENAME: 13001, "receipt-dent-kris-krug.png": 13002},
        )
        self.assertEqual(result["featured_media_id"], 13001)
        self.assertEqual(result["would_upload"], [])
        self.assertEqual(snapshot_payload, before)
        self.assertEqual(snapshot_mode, 0o600)
        self.assertEqual(
            result["payload_fields"],
            ["title", "content", "excerpt", "featured_media", "meta"],
        )
        self.assertNotEqual(result["before_content_sha256"], result["after_content_sha256"])
        self.assertEqual(result["rendered_content"]["raw_image_count"], 3)
        self.assertFalse(
            result["rendered_content"]["has_local_or_placeholder_markers"]
        )
        self.assertIn(str(snapshot), result["restore_command"])
        self.assertIn("no automated restore mode", result["restore_command"])
        upload_kwargs = wp.upload_media.call_args_list[1].kwargs
        self.assertEqual(upload_kwargs["alt"], "DENT article receipt.")
        self.assertIn("Screenshot captured", upload_kwargs["caption"])
        self.assertIn("https://kriskrug.co/dent/", upload_kwargs["caption"])
        payload = wp.update_post.call_args.args[1]
        self.assertEqual(
            set(payload),
            {"title", "content", "excerpt", "featured_media", "meta"},
        )
        self.assertEqual(payload["featured_media"], 13001)
        self.assertNotIn("wp-image-TBD", payload["content"])
        self.assertNotIn('src="images/', payload["content"])


if __name__ == "__main__":
    unittest.main()
