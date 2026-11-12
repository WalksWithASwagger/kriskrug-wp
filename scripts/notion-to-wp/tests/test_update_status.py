"""--update never changes a post's status unless --publish asks for it.

The connector used to send status=draft on every update without --publish, so
an update unpublished a live post, and the readback passed because it saw the
draft it had sent. Same family as the 2026-05-15 overwrite
(docs/current-state/INCIDENT-2026-05-15-overwritten-post.md).

Drives the real kk_notion_to_wp.run() with the in-memory Notion page and
recording FakeWordPress from test_run_order. Nothing touches the network.
"""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402
import test_run_order  # noqa: E402
from test_run_order import (  # noqa: E402
    PAGE_ID,
    TITLE,
    FakeWordPress,
    existing_post,
    readback,
    sent_payload,
)
from update_safety import readback_mismatches, update_diff, update_payload  # noqa: E402


class RecordingWordPress(FakeWordPress):
    def update_post(self, post_id, payload, *, expected_slug):
        self.update_body = dict(payload)
        return super().update_post(post_id, payload, expected_slug=expected_slug)


def existing(status: str) -> dict:
    return {**existing_post(TITLE), "status": status}


class ConnectorUpdateStatusTests(unittest.TestCase):
    setUp = test_run_order.RunOrderTests.setUp

    def run_connector(self, wp, *, force_publish=False, **kwargs):
        logs = io.StringIO()
        with mock.patch.object(kk_notion_to_wp, "WordPress", lambda *a, **k: wp):
            with contextlib.redirect_stdout(logs):
                code = kk_notion_to_wp.run(
                    f"https://www.notion.so/Calling-{PAGE_ID}",
                    dry_run=False,
                    force_publish=force_publish,
                    **kwargs,
                )
        return code, logs.getvalue()

    def test_update_without_publish_sends_no_status_and_the_post_keeps_its_own(self):
        for status in ("publish", "draft", "future", "private"):
            with self.subTest(status=status):
                wp = RecordingWordPress(existing=existing(status))

                code, logs = self.run_connector(wp, allow_update=True)

                self.assertEqual(code, 0, logs)
                self.assertNotIn("status", wp.update_body)
                self.assertEqual(wp.stored[123]["status"], status)
                self.assertIn(f"existing status:     {status!r} (left unchanged)", logs)

    def test_update_with_publish_publishes_a_draft(self):
        wp = RecordingWordPress(existing=existing("draft"))

        code, logs = self.run_connector(wp, allow_update=True, force_publish=True)

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.update_body["status"], "publish")
        self.assertEqual(wp.stored[123]["status"], "publish")

    def test_create_still_sends_draft_unless_publish(self):
        for force_publish, status in ((False, "draft"), (True, "publish")):
            with self.subTest(force_publish=force_publish):
                wp = RecordingWordPress()

                code, logs = self.run_connector(wp, force_publish=force_publish)

                self.assertEqual(code, 0, logs)
                self.assertEqual(wp.stored[701]["status"], status)

    def test_readback_fails_when_an_update_moved_the_status_anyway(self):
        wp = RecordingWordPress(
            existing=existing("publish"), readback_overrides={"status": "draft"}
        )

        code, logs = self.run_connector(wp, allow_update=True)

        self.assertEqual(code, 7)
        self.assertIn("status: sent 'publish', WordPress stored 'draft'", logs)

    def test_diff_shows_a_status_change_only_with_publish(self):
        published = ['-  "status": "draft",', '+  "status": "publish",']
        for force_publish, expected in ((False, []), (True, published)):
            with self.subTest(force_publish=force_publish):
                wp = RecordingWordPress(existing=existing("draft"))

                code, logs = self.run_connector(wp, diff_update=True, force_publish=force_publish)

                self.assertEqual(code, 0, logs)
                self.assertEqual(wp.writes(), [])
                changed = [line for line in logs.splitlines() if re.match(r'^[-+]\s+"status"', line)]
                self.assertEqual(changed, expected)


class UpdateStatusHelperTests(unittest.TestCase):
    def test_update_payload_drops_status_without_publish_and_leaves_the_input_alone(self):
        payload = sent_payload()

        self.assertNotIn("status", update_payload(payload, force_publish=False))
        self.assertEqual(payload["status"], "draft")
        self.assertIs(update_payload(payload, force_publish=True), payload)

    def test_readback_without_a_sent_status_expects_the_kept_status_exactly(self):
        sent = update_payload(sent_payload(), force_publish=False)

        self.assertEqual(
            readback_mismatches(sent, readback(status="publish"), kept_status="publish"), {}
        )
        for stored in ("draft", "future", "private"):
            with self.subTest(stored=stored):
                self.assertEqual(
                    readback_mismatches(sent, readback(status=stored), kept_status="publish"),
                    {"status": ("publish", stored)},
                )

    def test_diff_without_a_sent_status_proposes_the_existing_one(self):
        diff = update_diff(
            {"title": {"raw": TITLE}, "status": "future"},
            update_payload(sent_payload(), force_publish=False),
        )

        changed = [line for line in diff.splitlines() if re.match(r'^[-+]\s+"status"', line)]
        self.assertEqual(changed, [])


if __name__ == "__main__":
    unittest.main()
