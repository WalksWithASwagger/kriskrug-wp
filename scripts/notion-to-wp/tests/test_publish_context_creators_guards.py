"""Mocked runs of publish_context_creators.py (#1219).

The script does its work at import time, so each test runs a copy of it with
runpy inside a throwaway repo layout. That keeps post.html and publish.log in
the temp dir instead of content/drafts/, and no WordPress client is real.
"""

from __future__ import annotations

import io
import re
import runpy
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402
import publish_common  # noqa: E402

SCRIPT = SCRIPT_DIR / "publish_context_creators.py"
STAGE_REL = Path("content/drafts/2026-06-28-context-creators")
STAGED_IMAGES = sorted(
    set(re.findall(r'"([a-z0-9-]+\.png)"', SCRIPT.read_text(encoding="utf-8")))
)


class FakeWordPress:
    base = "https://example.test"

    def __init__(self, existing=None, tamper=None):
        self.existing = existing
        self.tamper = tamper or (lambda post: post)
        self.writes = []
        self.stored = None

    def ensure_term(self, taxonomy, name):
        self.writes.append(("ensure_term", taxonomy, name))
        return 7

    def create_post(self, payload):
        self.writes.append(("create_post", payload["slug"]))
        self.stored = {
            "id": 501,
            "status": payload["status"],
            "content": {"raw": payload["content"]},
            "featured_media": payload["featured_media"],
            "meta": dict(payload["meta"]),
        }
        return self.stored

    def update_post(self, post_id, payload, *, expected_slug):
        self.writes.append(("update_post", post_id, expected_slug))
        raise AssertionError("these tests never take the --update path")

    def get_post(self, post_id):
        return self.tamper(dict(self.stored))


def fake_media(wp, path, alt, **kwargs):
    media_id = 9000 + STAGED_IMAGES.index(path.name)
    return media_id, f"https://example.test/wp-content/uploads/{path.name}"


def run_publisher(wp, *argv):
    """Run a temp copy of the script; return (exit code, stdout, stderr)."""
    config = SimpleNamespace(
        wp_base_url=wp.base,
        wp_user="fake-user",
        wp_app_password="fake-secret",
        wp_author_id=1,
    )
    stdout, stderr = io.StringIO(), io.StringIO()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        script = root / "scripts" / "notion-to-wp" / SCRIPT.name
        script.parent.mkdir(parents=True)
        shutil.copy(SCRIPT, script)
        stage = root / STAGE_REL
        (stage / "images").mkdir(parents=True)
        shutil.copy(REPO_ROOT / STAGE_REL / "post.md", stage / "post.md")
        for name in STAGED_IMAGES:
            (stage / "images" / name).write_bytes(b"")
        patches = (
            mock.patch.object(sys, "argv", [str(script), *argv]),
            mock.patch.object(kk_notion_to_wp, "load_config", return_value=config),
            mock.patch.object(kk_notion_to_wp, "WordPress", return_value=wp),
            mock.patch.object(
                publish_common, "find_or_upload_media", side_effect=fake_media
            ),
            mock.patch.object(
                publish_common,
                "find_existing_post_by_slug",
                side_effect=lambda client, slug: client.existing,
            ),
        )
        code = 0
        with redirect_stdout(stdout), redirect_stderr(stderr):
            for patch in patches:
                patch.start()
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                code = exc.code
            finally:
                mock.patch.stopall()
    return code, stdout.getvalue(), stderr.getvalue()


class ContextCreatorsGuardTests(unittest.TestCase):
    def test_clean_execute_exits_zero(self):
        wp = FakeWordPress()
        code, out, _ = run_publisher(wp, "--execute")
        self.assertEqual(code, 0, out)
        self.assertNotIn("FAIL", out)
        self.assertIn("DONE - left as DRAFT.", out)

    def test_failed_verification_check_exits_1(self):
        wp = FakeWordPress(tamper=lambda post: {**post, "featured_media": 0})
        code, out, err = run_publisher(wp, "--execute")
        self.assertEqual(code, 1)
        self.assertIn("FAIL featured_set", out)
        self.assertIn("featured_set", err)
        self.assertNotIn("DONE - left as DRAFT.", out)

    def test_execute_with_existing_slug_aborts_before_any_post_or_term_write(self):
        wp = FakeWordPress(existing={"id": 12404, "slug": "context-creators"})
        code, _, _ = run_publisher(wp, "--execute")
        self.assertIsInstance(code, str)
        self.assertIn("Use --update", code)
        self.assertEqual(wp.writes, [])


if __name__ == "__main__":
    unittest.main()
