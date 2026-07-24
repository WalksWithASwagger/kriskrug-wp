import io
import json
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

import catalog_album


class CatalogAlbumTests(unittest.TestCase):
    def test_media_kind_is_case_insensitive(self):
        self.assertEqual(catalog_album.media_kind("portrait.JPEG"), "image")
        self.assertEqual(catalog_album.media_kind("clip.MOV"), "video")
        self.assertIsNone(catalog_album.media_kind("metadata.json"))

    def test_sha256_stream_is_stable(self):
        self.assertEqual(
            catalog_album.sha256_stream(io.BytesIO(b"kris")),
            "d999056550fd648de6de0537f389c3da467f846a4fd6117a62cb54ba1c23cf3c",
        )

    def test_captured_at_prefers_original_date(self):
        captured, source = catalog_album.captured_at(
            {"DateTimeOriginal": "2026:05:01 10:44:56", "CreateDate": "2025:01:01 00:00:00"},
            datetime(2024, 1, 1),
        )
        self.assertEqual(captured, "2026-05-01T10:44:56")
        self.assertEqual(source, "exif:DateTimeOriginal")

    def test_review_record_removes_exact_gps(self):
        review = catalog_album.review_record(
            {
                "asset_id": "abc",
                "filename": "portrait.jpg",
                "media_kind": "image",
                "size_bytes": 42,
                "metadata": {"GPSLatitude": 49.2, "GPSLongitude": -123.1, "Creator": "Michelle"},
            }
        )
        self.assertNotIn("GPSLatitude", review["metadata"])
        self.assertNotIn("GPSLongitude", review["metadata"])
        self.assertEqual(review["metadata"]["Creator"], "Michelle")

    def test_google_sidecar_date_precedes_archive_mtime(self):
        captured, source = catalog_album.captured_at(
            {},
            datetime(2024, 1, 1),
            {"photoTakenTime": {"timestamp": "1777628696"}},
        )
        self.assertEqual(captured, "2026-05-01T09:44:56Z")
        self.assertEqual(source, "google-sidecar")

    def test_google_sidecar_reads_exact_media_companion(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "album.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("portrait.jpg", b"image")
                archive.writestr("portrait.jpg.json", json.dumps({"description": "CreativeMornings"}))
            with zipfile.ZipFile(archive_path) as archive:
                sidecar = catalog_album.google_sidecar(archive, "portrait.jpg")
        self.assertEqual(sidecar["description"], "CreativeMornings")

    def test_tesseract_parser_drops_low_confidence_noise(self):
        tsv = (
            "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
            "5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t91.5\tVANCOUVER\n"
            "5\t1\t1\t1\t1\t2\t0\t0\t10\t10\t88.0\tMAGAZINE\n"
            "5\t1\t2\t1\t1\t1\t0\t0\t10\t10\t12.0\txqz\n"
        )
        self.assertEqual(catalog_album.parse_tesseract_tsv(tsv), "VANCOUVER MAGAZINE")

    def test_iter_zip_media_skips_sidecars_and_macos_entries(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "album.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("portrait.jpg", b"image")
                archive.writestr("portrait.jpg.json", "{}")
                archive.writestr("__MACOSX/portrait.jpg", b"resource fork")
                archive.writestr("talk.mp4", b"video")
            with zipfile.ZipFile(archive_path) as archive:
                names = [info.filename for info in catalog_album.iter_zip_media(archive)]
        self.assertEqual(names, ["portrait.jpg", "talk.mp4"])

    def test_load_jsonl_indexes_by_asset_id(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "catalog.jsonl"
            path.write_text(json.dumps({"asset_id": "abc", "filename": "one.jpg"}) + "\n", encoding="utf-8")
            records = catalog_album.load_jsonl(path)
        self.assertEqual(records["abc"]["filename"], "one.jpg")

    def test_review_html_marks_catalog_private(self):
        rendered = catalog_album.render_review_html(
            [
                {
                    "asset_id": "a" * 64,
                    "filename": "<portrait>.jpg",
                    "captured_at": "2026-05-01T10:44:56",
                    "event_group": "2026-05-01",
                    "ocr_text": "CreativeMornings",
                    "thumbnail": "thumbnails/a.jpg",
                }
            ],
            "KK PHotos",
        )
        self.assertIn("Private working catalog", rendered)
        self.assertIn("&lt;portrait&gt;.jpg", rendered)
        self.assertNotIn("GPSLatitude", rendered)
        self.assertIn('data-search="&lt;portrait&gt;.jpg', rendered)
        self.assertNotIn('data-search="<portrait>.jpg', rendered)

    def test_catalog_rerender_preserves_review_annotations(self):
        records = {
            "abc": {
                "asset_id": "abc",
                "filename": "portrait.jpg",
                "media_kind": "image",
                "size_bytes": 42,
                "metadata": {},
                "event_group": "2026-05-01",
            }
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            catalog_album.write_catalog_outputs(root, records, {}, "KK PHotos")
            annotation_path = root / "review/annotations.jsonl"
            annotation_path.write_text(
                json.dumps(
                    {
                        "asset_id": "abc",
                        "caption_draft": "Kris at CreativeMornings Vancouver.",
                        "event_name": "CreativeMornings Vancouver",
                        "identity_clues": [{"name": "Kris Krug", "evidence": "album scope"}],
                        "site_uses": ["speaking"],
                        "review_status": "review_candidate",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            catalog_album.write_catalog_outputs(root, records, {}, "KK PHotos")
            preserved = json.loads(annotation_path.read_text(encoding="utf-8"))
            review = json.loads((root / "review/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(preserved["event_name"], "CreativeMornings Vancouver")
        self.assertEqual(preserved["review_status"], "review_candidate")
        self.assertEqual(review[0]["event_group"], "CreativeMornings Vancouver")


if __name__ == "__main__":
    unittest.main()
