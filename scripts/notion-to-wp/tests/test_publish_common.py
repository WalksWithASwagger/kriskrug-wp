"""Unit tests for publish_common helpers (issue #254)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402


class PublishCommonTests(unittest.TestCase):
    def test_render_text_post_skips_title_and_uses_wp_blocks(self):
        body = "# Title\n\n## Section\n\n---\n\nA [link](https://example.com) here.\n\n### Sub"
        out = publish_common.render_text_post(body)
        self.assertNotIn("<h1", out)
        self.assertIn("<!-- wp:heading -->", out)
        self.assertIn("<!-- wp:separator -->", out)
        self.assertIn('target="_blank"', out)
        self.assertIn('{"level":3}', out)

    def test_parse_markdown_image_order(self):
        body = (
            "# T\n\n"
            "![alt one](images/01-a.png)\n\n"
            "para\n\n"
            "![alt two](images/02-b.png)\n"
        )
        order = publish_common.parse_markdown_image_order(body)
        self.assertEqual(order, [("01-a.png", "alt one"), ("02-b.png", "alt two")])

    def test_load_captions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "captions.txt").write_text("a.jpg|Alt A\nb.jpg|Alt B\n")
            self.assertEqual(
                publish_common.load_captions(path),
                {"a.jpg": "Alt A", "b.jpg": "Alt B"},
            )

    def test_upload_image_manifest_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            uploaded, log = publish_common.upload_image_manifest(
                None,
                [("a.png", "alt")],
                src,
                write=False,
            )
        self.assertEqual(uploaded["a.png"]["id"], 0)
        self.assertEqual(uploaded["a.png"]["url"], "DRYRUN/a.png")
        self.assertEqual(log, [])

    def test_find_media_by_stem(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 9, "source_url": "https://example.test/wp-content/uploads/stem.jpg"}
        ]
        found = publish_common.find_media_by_stem(wp, "stem")
        self.assertEqual(found, (9, "https://example.test/wp-content/uploads/stem.jpg"))

    def test_validate_term_ids_raises(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.status_code = 404
        with self.assertRaises(SystemExit):
            publish_common.validate_term_ids(wp, "categories", [1678])

    def test_validate_media_id_raises(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.status_code = 404
        with self.assertRaises(SystemExit):
            publish_common.validate_media_id(wp, 11976)

    def test_build_seo_meta_strips_combining_marks(self):
        meta = publish_common.build_seo_meta("Ethọ́s Lab", "desc")
        self.assertFalse(
            any(__import__("unicodedata").combining(c) for c in meta["jetpack_seo_html_title"])
        )

    def test_verify_seo_meta_landed_all_present(self):
        dropped = publish_common.verify_seo_meta_landed(
            {"jetpack_seo_html_title": "T", "advanced_seo_description": "D", "footnotes": ""},
            {"jetpack_seo_html_title": "T", "advanced_seo_description": "D"},
        )
        self.assertEqual(dropped, [])

    def test_verify_seo_meta_landed_detects_silent_drop(self):
        dropped = publish_common.verify_seo_meta_landed(
            {"footnotes": ""},
            {"jetpack_seo_html_title": "T", "advanced_seo_description": "D"},
        )
        self.assertEqual(
            sorted(dropped),
            ["advanced_seo_description", "jetpack_seo_html_title"],
        )

    def test_verify_seo_meta_landed_detects_value_mismatch(self):
        dropped = publish_common.verify_seo_meta_landed(
            {"jetpack_seo_html_title": "OLD", "advanced_seo_description": "D"},
            {"jetpack_seo_html_title": "NEW", "advanced_seo_description": "D"},
        )
        self.assertEqual(dropped, ["jetpack_seo_html_title"])

    def test_verify_seo_meta_landed_empty_expected_returns_empty(self):
        self.assertEqual(publish_common.verify_seo_meta_landed({"footnotes": ""}, {}), [])
        self.assertEqual(publish_common.verify_seo_meta_landed({"footnotes": ""}, None), [])

    def test_verify_seo_meta_landed_skips_empty_sent_values(self):
        dropped = publish_common.verify_seo_meta_landed(
            {"footnotes": ""},
            {"jetpack_seo_html_title": "", "advanced_seo_description": ""},
        )
        self.assertEqual(dropped, [])

    def test_verify_seo_meta_landed_handles_none_response_meta(self):
        dropped = publish_common.verify_seo_meta_landed(
            None,
            {"jetpack_seo_html_title": "T", "advanced_seo_description": "D"},
        )
        self.assertEqual(
            sorted(dropped),
            ["advanced_seo_description", "jetpack_seo_html_title"],
        )

    def test_parse_publish_argv(self):
        flags = publish_common.parse_publish_argv(["--execute", "--update"])
        self.assertTrue(flags.execute)
        self.assertTrue(flags.update)
        self.assertTrue(flags.write)


def _media(media_id: str | int, filename: str, *, original: str | None = None) -> dict:
    """A media REST record as WordPress returns it."""
    record: dict = {
        "id": media_id,
        "source_url": f"https://example.test/wp-content/uploads/2026/07/{filename}",
    }
    if original:
        record["media_details"] = {"original_image": original}
    return record


class SelectMediaMatchTests(unittest.TestCase):
    """Issue #483: prefix matching attached the wrong image and reported success."""

    def test_exact_filename_matches(self):
        self.assertEqual(
            publish_common.select_media_match([_media(9, "hero.png")], "hero"),
            (9, "https://example.test/wp-content/uploads/2026/07/hero.png"),
        )

    def test_scaled_variant_does_not_match_its_own_stem(self):
        """The reported collision: uploading hero.png must not reuse hero-scaled.png."""
        self.assertIsNone(
            publish_common.select_media_match([_media(9, "hero-scaled.png")], "hero")
        )

    def test_dimension_variant_does_not_match(self):
        """WordPress auto-generates -{width}x{height}; those are not the original."""
        for variant in ("hero-1024x768.png", "hero-150x150.png", "hero-thumbnail.png"):
            with self.subTest(variant=variant):
                self.assertIsNone(
                    publish_common.select_media_match([_media(9, variant)], "hero")
                )

    def test_re_export_suffix_does_not_match(self):
        """hero-2.png is an editor's re-export, a different image entirely."""
        self.assertIsNone(publish_common.select_media_match([_media(9, "hero-2.png")], "hero"))

    def test_longer_stem_does_not_match_shorter_request(self):
        self.assertIsNone(
            publish_common.select_media_match([_media(9, "hero-at-city-hall.jpg")], "hero")
        )

    def test_scaled_attachment_matches_via_wordpress_original_image(self):
        """A scaled attachment is still the same upload when WP says so itself."""
        record = _media(9, "hero-scaled.png", original="hero.png")
        self.assertEqual(
            publish_common.select_media_match([record], "hero"),
            (9, "https://example.test/wp-content/uploads/2026/07/hero-scaled.png"),
        )

    def test_original_image_still_requires_an_exact_stem(self):
        record = _media(9, "hero-2-scaled.png", original="hero-2.png")
        self.assertIsNone(publish_common.select_media_match([record], "hero"))

    def test_extension_allow_list_is_enforced(self):
        self.assertIsNone(
            publish_common.select_media_match([_media(9, "hero.tiff")], "hero")
        )
        self.assertIsNone(
            publish_common.select_media_match(
                [_media(9, "hero.png")], "hero", extensions=(".jpg",)
            )
        )

    def test_extension_match_is_case_insensitive(self):
        self.assertEqual(
            publish_common.select_media_match([_media(9, "hero.PNG")], "hero")[0], 9
        )

    def test_ambiguous_match_aborts_instead_of_picking_one(self):
        records = [_media(9, "hero.png"), _media(10, "hero.png")]
        with self.assertRaises(SystemExit) as ctx:
            publish_common.select_media_match(records, "hero")
        message = str(ctx.exception)
        self.assertIn("ambiguous media match", message)
        self.assertIn("9", message)
        self.assertIn("10", message)

    def test_ambiguity_counts_attachments_not_matching_names(self):
        """One attachment matching by both source_url and original_image is not ambiguous."""
        record = _media(9, "hero.png", original="hero.png")
        self.assertEqual(publish_common.select_media_match([record], "hero")[0], 9)

    def test_ambiguity_spans_the_extension_allow_list(self):
        """hero.png and hero.jpg are different files; the publisher cannot pick."""
        with self.assertRaises(SystemExit):
            publish_common.select_media_match(
                [_media(9, "hero.png"), _media(10, "hero.jpg")], "hero"
            )

    def test_malformed_records_are_skipped(self):
        records = ["nonsense", {"id": 9}, {"source_url": "https://example.test/u/hero.png"}]
        self.assertIsNone(publish_common.select_media_match(records, "hero"))

    def test_empty_results(self):
        self.assertIsNone(publish_common.select_media_match([], "hero"))
        self.assertIsNone(publish_common.select_media_match(None, "hero"))


class FindMediaByStemTests(unittest.TestCase):
    def _wp(self, payload):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = payload
        return wp

    def test_scaled_collision_does_not_reuse(self):
        wp = self._wp([_media(9, "hero-scaled.png")])
        self.assertIsNone(publish_common.find_media_by_stem(wp, "hero"))

    def test_ambiguity_propagates_out_of_the_lookup(self):
        wp = self._wp([_media(9, "hero.png"), _media(10, "hero.png")])
        with self.assertRaises(SystemExit):
            publish_common.find_media_by_stem(wp, "hero")

    def test_network_failure_returns_none(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.side_effect = RuntimeError("connection reset")
        self.assertIsNone(publish_common.find_media_by_stem(wp, "hero"))

    def test_non_list_payload_returns_none(self):
        wp = self._wp({"code": "rest_forbidden"})
        self.assertIsNone(publish_common.find_media_by_stem(wp, "hero"))


class PrefixMatchRegressionGuardTests(unittest.TestCase):
    """Both publishers must route media matching through the one shared rule (#483)."""

    def test_keep_the_machine_strange_delegates_to_select_media_match(self):
        source = (SCRIPT_DIR.parent / "archive" / "publish_keep_the_machine_strange.py").read_text()
        self.assertIn("select_media_match", source)
        self.assertNotIn("base.startswith(stem)", source)

    def test_publish_common_has_no_stem_prefix_match(self):
        source = (SCRIPT_DIR / "publish_common.py").read_text()
        self.assertNotIn("startswith(stem)", source)


class FindOrUploadMediaTests(unittest.TestCase):
    """Extracted from the copy-pasted resolve-or-upload loops (issue #254)."""

    def test_dry_run_never_touches_wordpress(self):
        wp = mock.Mock()
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/poster-1.png"), "alt", mime="image/png", write=False
        )
        self.assertEqual((media_id, url), (0, "DRYRUN/poster-1.png"))
        wp.s.get.assert_not_called()
        wp.upload_media.assert_not_called()

    def test_reuse_logs_and_does_not_upload(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 42, "source_url": "https://example.test/u/poster-1.png"}
        ]
        log: list[str] = []
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/poster-1.png"), "alt", mime="image/png", write=True, log=log
        )
        self.assertEqual((media_id, url), (42, "https://example.test/u/poster-1.png"))
        self.assertEqual(log, ["poster-1.png -> REUSE id=42"])
        wp.upload_media.assert_not_called()

    def test_new_upload_logs_id_and_url(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        wp.upload_media.return_value = {"id": 43, "source_url": "https://example.test/u/new.png"}
        log: list[str] = []
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/new.png"), "alt", mime="image/png", write=True, log=log
        )
        self.assertEqual((media_id, url), (43, "https://example.test/u/new.png"))
        self.assertEqual(log, ["new.png -> NEW id=43 https://example.test/u/new.png"])

    def test_label_prefixes_the_log_line(self):
        """load_photos_from_dir logs `subdir/filename`; the shape must not change."""
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 7, "source_url": "https://example.test/u/01-a.jpg"}
        ]
        log: list[str] = []
        publish_common.find_or_upload_media(
            wp, Path("/tmp/01-a.jpg"), "alt", mime="image/jpeg", write=True,
            label="photos/best/01-a.jpg", log=log,
        )
        self.assertEqual(log, ["photos/best/01-a.jpg -> REUSE id=7"])


class LoadPhotosFromDirTests(unittest.TestCase):
    def test_dry_run_shape_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            directory = stage / "photos" / "best"
            directory.mkdir(parents=True)
            (directory / "01-water.jpg").write_bytes(b"x")
            (directory / "_skipped.jpg").write_bytes(b"x")
            (directory / "captions.txt").write_text("01-water.jpg|A caption\n")
            items = publish_common.load_photos_from_dir(
                mock.Mock(), stage, "photos/best", write=False
            )
        self.assertEqual(
            items, [(0, "DRYRUN/01-water.jpg", "A caption", "A caption", "01-water.jpg")]
        )

    def test_alt_from_slug_appends_protest_sign(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            directory = stage / "photos" / "best"
            directory.mkdir(parents=True)
            (directory / "01-water-the-servers.jpg").write_bytes(b"x")
            items = publish_common.load_photos_from_dir(
                mock.Mock(), stage, "photos/best", write=False, alt_from_slug=True
            )
        self.assertEqual(items[0][2], "water the servers protest sign")


class FindExistingPostBySlugTests(unittest.TestCase):
    def test_returns_first_hit(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [{"id": 11}, {"id": 12}]
        self.assertEqual(publish_common.find_existing_post_by_slug(wp, "a-slug"), {"id": 11})

    def test_queries_any_status_in_edit_context(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        publish_common.find_existing_post_by_slug(wp, "a-slug")
        _, kwargs = wp.s.get.call_args
        self.assertEqual(
            kwargs["params"], {"slug": "a-slug", "status": "any", "context": "edit"}
        )

    def test_returns_none_when_absent_or_malformed(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        self.assertIsNone(publish_common.find_existing_post_by_slug(wp, "a-slug"))
        wp.s.get.return_value.json.return_value = {"code": "rest_no_route"}
        self.assertIsNone(publish_common.find_existing_post_by_slug(wp, "a-slug"))


class RawParagraphTests(unittest.TestCase):
    def test_differs_from_br_joined_paragraph_on_multiline_blocks(self):
        block = "line one\nline two"
        self.assertIn("line one\nline two", publish_common.raw_paragraph(block))
        self.assertIn(
            "line one<br>line two", publish_common.render_paragraph_from_markdown(block)
        )

    def test_agrees_on_single_line_blocks(self):
        block = "just one line with a [link](https://example.com)"
        self.assertEqual(
            publish_common.raw_paragraph(block),
            publish_common.render_paragraph_from_markdown(block),
        )


if __name__ == "__main__":
    unittest.main()
