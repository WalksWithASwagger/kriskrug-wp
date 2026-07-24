from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import requests

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import ingest_media_manifest as ingest  # noqa: E402


class IngestMediaManifestTests(unittest.TestCase):
    def manifest(self, root: Path, *, caption_credit: bool = True) -> Path:
        assets = root / "assets"
        assets.mkdir()
        image = assets / "portrait.jpg"
        image.write_bytes(b"jpeg fixture")
        credit = "Photo: Michelle Diamond."
        caption = f"Kris at an event. {credit}" if caption_credit else "Kris at an event."
        payload = {
            "schema_version": 1,
            "assets": [
                {
                    "file": "assets/portrait.jpg",
                    "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                    "credit": credit,
                    "wordpress": {
                        "title": "Kris portrait",
                        "alt_text": "Kris smiling",
                        "caption": caption,
                        "description": f"Event portrait. {credit}",
                    },
                }
            ],
        }
        path = root / "manifest.json"
        path.write_text(json.dumps(payload))
        return path

    def test_validate_manifest_checks_hash_credit_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.manifest(Path(tmp))
            _, assets = ingest.validate_manifest(path)
        self.assertEqual(assets[0]["mime"], "image/jpeg")
        self.assertEqual(assets[0]["wordpress"]["alt_text"], "Kris smiling")

    def test_validate_manifest_rejects_caption_without_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.manifest(Path(tmp), caption_credit=False)
            with self.assertRaisesRegex(ValueError, "preserve credit"):
                ingest.validate_manifest(path)

    def test_exact_media_matches_original_scaled_and_numbered_names(self):
        items = [
            {"id": 1, "source_url": "https://example.test/uploads/portrait.jpg"},
            {"id": 2, "source_url": "https://example.test/uploads/portrait-scaled.jpg"},
            {"id": 3, "source_url": "https://example.test/uploads/portrait-1.jpg"},
            {"id": 4, "source_url": "https://example.test/uploads/portrait-card.jpg"},
        ]
        matches = ingest.exact_media_matches(items, "portrait.jpg")
        self.assertEqual([item["id"] for item in matches], [1, 2, 3])

    def test_media_metadata_prefers_edit_context_raw_values(self):
        media = {
            "title": {"raw": "Title", "rendered": "Wrong"},
            "alt_text": "Alt",
            "caption": {"raw": "Caption"},
            "description": {"raw": "Description"},
        }
        self.assertEqual(
            ingest.media_metadata(media),
            {
                "title": "Title",
                "alt_text": "Alt",
                "caption": "Caption",
                "description": "Description",
            },
        )

    def test_build_result_accepts_manifest_outside_repo(self):
        path = Path("/tmp/external-media-manifest.json")
        result = ingest.build_result(path, "https://example.test", "dry-run")
        self.assertEqual(result["manifest"], str(path))

    def test_execute_records_partial_upload_in_failure_report(self):
        wp = mock.Mock()
        wp.upload_media_file.return_value = {
            "id": 77,
            "source_url": "https://example.test/uploads/portrait.jpg",
        }
        wp.update_media.side_effect = requests.HTTPError("metadata write rejected")
        asset = {
            "file": "assets/portrait.jpg",
            "path": Path("/tmp/portrait.jpg"),
            "mime": "image/jpeg",
            "wordpress": {
                "title": "Title",
                "alt_text": "Alt",
                "caption": "Caption",
                "description": "Description",
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "failure.json"
            with mock.patch.dict(
                os.environ,
                {"WP_USER": "user", "WP_APP_PASSWORD": "password"},
            ), mock.patch.object(ingest, "WordPress", return_value=wp), mock.patch.object(
                ingest, "search_media", return_value=[]
            ), redirect_stdout(io.StringIO()), self.assertRaisesRegex(
                SystemExit, "metadata write rejected"
            ):
                ingest.execute(
                    Path("/tmp/manifest.json"),
                    "https://example.test",
                    [asset],
                    report,
                )
            payload = json.loads(report.read_text())
        self.assertEqual(payload["rollback"]["created_media_ids"], [77])
        self.assertEqual(payload["assets"][0]["action"], "uploaded-pending-metadata")


if __name__ == "__main__":
    unittest.main()
