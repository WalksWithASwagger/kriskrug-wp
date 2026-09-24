"""Offline apply/restore safety tests for scripts/deploy_events_page.py (#1035).

WPClient is replaced by an in-memory fake; no network or credentials.
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.error import URLError

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import deploy_events_page as dep  # noqa: E402

ARTIFACT_HTML = (
    '<div data-events-grid="sheet"></div><div data-events-grid="upcoming"></div>'
    '<div class="kk-ev-record-grid"></div>'
)
OLD = "<p>old events page</p>"
CURRENT = "<p>current live events page</p>"


def _page(raw, **over):
    page = {
        "id": 2250,
        "slug": "events",
        "type": "page",
        "status": "publish",
        "modified_gmt": "2026-09-20T00:00:00",
        "content": {"raw": raw},
    }
    page.update(over)
    return page


class FakeWP:
    """Stores one page; `on_post` can simulate filtering or concurrent edits."""

    def __init__(self, page, *, on_post=None, get_errors=None, post_error=None):
        self.page = page
        self.on_post = on_post
        self.get_errors = list(get_errors or [])
        self.post_error = post_error
        self.gets = 0
        self.posts = []

    def get(self, path, **_):
        self.gets += 1
        if self.get_errors:
            err = self.get_errors.pop(0)
            if err:
                raise err
        return json.loads(json.dumps(self.page))

    def post(self, path, payload=None, **_):
        self.posts.append(payload)
        if self.post_error:
            raise self.post_error
        stored = payload["content"]
        if self.on_post:
            stored = self.on_post(stored, len(self.posts))
        self.page["content"]["raw"] = stored
        return {"id": 2250, "content": {"raw": stored}}


class EventsDeployTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.backup = root / "snapshots"
        self.artifact = root / "events.html"
        self.artifact.write_text(ARTIFACT_HTML, encoding="utf-8")
        for target, value in (
            ("BACKUP_DIR", self.backup),
            ("ARTIFACT", self.artifact),
        ):
            patcher = mock.patch.object(dep, target, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write_snapshot(self, raw=OLD, **over):
        path = Path(self.tmp.name) / "snap.json"
        path.write_text(json.dumps(_page(raw, **over)), encoding="utf-8")
        return path

    def run_main(self, wp, *argv):
        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["deploy_events_page.py", *argv]),
            mock.patch.object(dep.WPClient, "from_env", return_value=wp),
            redirect_stdout(out),
            redirect_stderr(err),
        ):
            try:
                code = dep.main()
            except dep.DeployError as exc:
                code = exc
        return code, out.getvalue(), err.getvalue()


class RestoreTests(EventsDeployTestBase):
    def test_snapshot_with_wrong_slug_rejected_before_any_request(self):
        wp = FakeWP(_page(CURRENT))
        snap = self.write_snapshot(slug="about")
        code, _, _ = self.run_main(wp, "--restore", str(snap), "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual((wp.gets, len(wp.posts)), (0, 0))

    def test_snapshot_without_content_rejected(self):
        wp = FakeWP(_page(CURRENT))
        snap = self.write_snapshot(content={})
        code, _, _ = self.run_main(wp, "--restore", str(snap))
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual(wp.posts, [])

    def test_wrong_live_identity_rejected(self):
        wp = FakeWP(_page(CURRENT, slug="events-old", status="draft"))
        snap = self.write_snapshot()
        code, _, _ = self.run_main(
            wp,
            "--restore",
            str(snap),
            "--execute",
            "--expect-current-sha256",
            dep.sha256(CURRENT),
        )
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual(wp.posts, [])

    def test_preview_sends_no_post_and_prints_hash(self):
        wp = FakeWP(_page(CURRENT))
        snap = self.write_snapshot()
        code, out, _ = self.run_main(wp, "--restore", str(snap))
        self.assertEqual(code, 0)
        self.assertEqual(wp.posts, [])
        self.assertIn(dep.sha256(CURRENT), out)
        self.assertIn("RESTORE PREVIEW", out)

    def test_execute_without_expected_hash_refused(self):
        wp = FakeWP(_page(CURRENT))
        snap = self.write_snapshot()
        code, _, _ = self.run_main(wp, "--restore", str(snap), "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual(wp.posts, [])

    def test_stale_hash_after_intervening_edit_refused(self):
        wp = FakeWP(_page("<p>edited by someone after the preview</p>"))
        snap = self.write_snapshot()
        code, _, _ = self.run_main(
            wp,
            "--restore",
            str(snap),
            "--execute",
            "--expect-current-sha256",
            dep.sha256(CURRENT),
        )
        self.assertIsInstance(code, dep.DeployError)
        self.assertIn("changed since the preview", str(code))
        self.assertEqual(wp.posts, [])

    def test_successful_restore_snapshots_current_and_verifies(self):
        wp = FakeWP(_page(CURRENT))
        snap = self.write_snapshot()
        code, _, _ = self.run_main(
            wp,
            "--restore",
            str(snap),
            "--execute",
            "--expect-current-sha256",
            dep.sha256(CURRENT),
        )
        self.assertEqual(code, 0)
        self.assertEqual(wp.posts, [{"content": OLD}])
        self.assertEqual(wp.page["content"]["raw"], OLD)
        pre = list(self.backup.glob("*pre-restore.json"))
        self.assertEqual(len(pre), 1)
        self.assertEqual(json.loads(pre[0].read_text())["content"]["raw"], CURRENT)

    def test_restore_readback_mismatch_raises_without_second_write(self):
        wp = FakeWP(_page(CURRENT), on_post=lambda raw, n: raw + "<!-- filtered -->")
        snap = self.write_snapshot()
        code, _, _ = self.run_main(
            wp,
            "--restore",
            str(snap),
            "--execute",
            "--expect-current-sha256",
            dep.sha256(CURRENT),
        )
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual(len(wp.posts), 1)


class ApplyTests(EventsDeployTestBase):
    def test_dry_run_sends_no_post(self):
        wp = FakeWP(_page(OLD))
        code, _, _ = self.run_main(wp)
        self.assertEqual(code, 0)
        self.assertEqual(wp.posts, [])

    def test_execute_success(self):
        wp = FakeWP(_page(OLD))
        code, _, _ = self.run_main(wp, "--execute")
        self.assertEqual(code, 0)
        self.assertEqual(wp.posts, [{"content": ARTIFACT_HTML}])

    def test_filtered_write_restores_previous_content(self):
        wp = FakeWP(
            _page(OLD),
            on_post=lambda raw, n: raw.replace("sheet", "") if n == 1 else raw,
        )
        code, _, _ = self.run_main(wp, "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertIn("filtered", str(code))
        self.assertEqual(len(wp.posts), 2)
        self.assertEqual(wp.page["content"]["raw"], OLD)

    def test_concurrent_edit_after_write_is_not_clobbered(self):
        wp = FakeWP(_page(OLD))
        real_get = wp.get

        def get_with_concurrent_edit(path, **kw):
            if wp.posts:  # someone edits between our write and our readback
                wp.page["content"]["raw"] = "<p>editor change</p>"
            return real_get(path, **kw)

        wp.get = get_with_concurrent_edit
        code, _, _ = self.run_main(wp, "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertIn("concurrent edit", str(code))
        self.assertEqual(len(wp.posts), 1)
        self.assertEqual(wp.page["content"]["raw"], "<p>editor change</p>")

    def test_readback_failure_sends_no_restore(self):
        wp = FakeWP(_page(OLD), get_errors=[None, URLError("reset")])
        code, _, _ = self.run_main(wp, "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertIn("readback failed", str(code))
        self.assertEqual(len(wp.posts), 1)

    def test_ambiguous_write_is_not_retried(self):
        wp = FakeWP(_page(OLD), post_error=URLError("lost response"))
        code, _, _ = self.run_main(wp, "--execute")
        self.assertIsInstance(code, dep.DeployError)
        self.assertEqual(len(wp.posts), 1)
        self.assertEqual(wp.gets, 1)


if __name__ == "__main__":
    unittest.main()
