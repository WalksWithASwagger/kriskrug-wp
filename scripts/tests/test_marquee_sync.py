"""Marquee Tier 3 REST sync — offline guarantees (no live WordPress).

A FakeWP records calls. Locks: payload shape, dry-run writes nothing, create path + readback,
slug-exists is skipped without --update, and the title-drift guard aborts a bad update.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/marquee"))

import wp_sync  # noqa: E402

BOARD = {
    "id": "2026-w26-x", "status": "live", "week": "2026-W26", "date": "2026-06-26",
    "after": "Marshall McLuhan", "skin": "led", "board": ["THE MODEL", "IS THE", "MESSAGE"],
    "kicker": "now showing", "dek": "why it matters",
    "source": {"title": "Understanding Media", "author": "Marshall McLuhan, 1964"},
    "tags": ["mcluhan", "ai"],
    "seo": {"title": "The Model Is the Message", "slug": "the-model-is-the-message"},
}


class FakeWP:
    def __init__(self, existing_id=None, existing_title=""):
        self.existing_id, self.existing_title = existing_id, existing_title
        self.calls = []

    def find_by_slug(self, slug):
        self.calls.append(("find", slug)); return self.existing_id

    def get(self, pid):
        self.calls.append(("get", pid))
        return {"id": pid, "slug": BOARD["seo"]["slug"], "title": {"raw": self.existing_title}}

    def create(self, payload):
        self.calls.append(("create", payload)); return {"id": 999, "slug": payload["slug"]}

    def update(self, pid, payload):
        self.calls.append(("update", pid)); return {"id": pid, "slug": payload["slug"]}

    def upload_media(self, path, alt, mime="image/png"):
        self.calls.append(("upload", str(path))); return {"id": 42}


class PayloadTests(unittest.TestCase):
    def test_payload_shape(self):
        p = wp_sync.build_payload(BOARD)
        self.assertEqual(p["slug"], "the-model-is-the-message")
        self.assertEqual(p["title"], "The Model Is the Message")
        self.assertEqual(p["excerpt"], "why it matters")
        self.assertIn("kkm-board", p["content"])              # board rendered into content
        self.assertEqual(p["meta"]["_kk_mb_skin"], "led")
        self.assertIn("MESSAGE", p["meta"]["_kk_mb_lines"])   # lines preserved as JSON
        self.assertIn("mcluhan", p["meta"]["_kk_mb_tags"])


class SyncTests(unittest.TestCase):
    def test_dry_run_writes_nothing(self):
        wp = FakeWP()
        out = wp_sync.sync_board(wp, BOARD, None, execute=False, allow_update=False, log=lambda *a: None)
        self.assertEqual(out["status"], "planned")
        self.assertEqual(wp.calls, [])                        # no REST calls at all

    def test_create_path_uploads_and_verifies(self):
        wp = FakeWP(existing_id=None)
        out = wp_sync.sync_board(wp, BOARD, Path(__file__), execute=True, allow_update=False, log=lambda *a: None)
        self.assertEqual(out["status"], "created")
        self.assertTrue(out["verified"])
        kinds = [c[0] for c in wp.calls]
        self.assertIn("upload", kinds)                        # og uploaded as featured image
        self.assertIn("create", kinds)
        self.assertIn("get", kinds)                           # post-write readback

    def test_existing_slug_skipped_without_update(self):
        wp = FakeWP(existing_id=7, existing_title="The Model Is the Message")
        out = wp_sync.sync_board(wp, BOARD, None, execute=True, allow_update=False, log=lambda *a: None)
        self.assertEqual(out["status"], "skipped-exists")
        self.assertNotIn("update", [c[0] for c in wp.calls])  # never wrote

    def test_title_drift_aborts_update(self):
        wp = FakeWP(existing_id=7, existing_title="Completely Unrelated Headline About Something Else")
        out = wp_sync.sync_board(wp, BOARD, None, execute=True, allow_update=True, log=lambda *a: None)
        self.assertEqual(out["status"], "aborted-title-drift")
        self.assertNotIn("update", [c[0] for c in wp.calls])  # guard blocked the write


if __name__ == "__main__":
    unittest.main()
