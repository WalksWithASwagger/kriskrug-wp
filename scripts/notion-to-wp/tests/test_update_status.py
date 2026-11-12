"""--update changes a post's status only when --publish asks for it.

The connector used to send status=draft on every update without --publish, so
an update unpublished a live post, and the readback passed because it saw the
draft it had sent. It also sent the Notion date (or today), and WordPress
publishes a scheduled post whose date has passed. Same family as the
2026-05-15 overwrite (docs/current-state/INCIDENT-2026-05-15-overwritten-post.md).

Drives the real kk_notion_to_wp.run() with the in-memory Notion page and the
recording FakeWordPress from test_run_order, which applies WordPress's date
rule. Nothing touches the network.
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
    wordpress_status,
)
from update_safety import readback_mismatches, update_diff, update_payload  # noqa: E402

PAST = "2026-05-07T11:37:33"
FUTURE = "2099-01-01T09:00:00"


class RecordingWordPress(FakeWordPress):
    def update_post(self, post_id, payload, *, expected_slug):
        self.update_body = dict(payload)
        return super().update_post(post_id, payload, expected_slug=expected_slug)


def existing(status: str, date: str = PAST) -> dict:
    return {**existing_post(TITLE), "status": status, "date": date}


class FakeDateRuleTests(unittest.TestCase):
    def test_fake_applies_wordpress_date_rule(self):
        # The Notion page's own date (2026-05-15) is in the past.
        self.assertEqual(wordpress_status("future", "2026-05-15T12:00:00"), "publish")
        self.assertEqual(wordpress_status("publish", FUTURE), "future")
        self.assertEqual(wordpress_status("draft", FUTURE), "draft")


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

    def test_update_without_publish_sends_no_status_or_date_and_the_post_keeps_both(self):
        for status, date in (("publish", PAST), ("draft", PAST), ("future", FUTURE), ("private", PAST)):
            with self.subTest(status=status):
                wp = RecordingWordPress(existing=existing(status, date))

                code, logs = self.run_connector(wp, allow_update=True)

                self.assertEqual(code, 0, logs)
                self.assertNotIn("status", wp.update_body)
                self.assertNotIn("date", wp.update_body)
                self.assertEqual(wp.stored[123]["status"], status)
                self.assertEqual(wp.stored[123]["date"], date)
                self.assertIn(f"existing status:     {status!r} (left unchanged)", logs)

    def test_scheduled_post_is_not_published_by_the_older_notion_date(self):
        wp = RecordingWordPress(existing=existing("future", FUTURE))

        code, logs = self.run_connector(wp, allow_update=True)

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.stored[123]["status"], "future")
        self.assertEqual(wp.stored[123]["date"], FUTURE)

    def test_date_is_sent_on_update_only_with_the_date_flag(self):
        wp = RecordingWordPress(existing=existing("draft"))

        code, logs = self.run_connector(wp, allow_update=True, date_override="2026-06-01T08:00:00")

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.update_body["date"], "2026-06-01T08:00:00")
        self.assertEqual(wp.stored[123]["date"], "2026-06-01T08:00:00")
        self.assertIn("(replaced by --date)", logs)

    def test_update_with_publish_publishes_a_draft(self):
        wp = RecordingWordPress(existing=existing("draft"))

        code, logs = self.run_connector(wp, allow_update=True, force_publish=True)

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.update_body["status"], "publish")
        self.assertEqual(wp.stored[123]["status"], "publish")

    def test_update_with_publish_may_schedule_a_draft(self):
        wp = RecordingWordPress(existing=existing("draft"))

        code, logs = self.run_connector(
            wp, allow_update=True, force_publish=True, date_override=FUTURE
        )

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.stored[123]["status"], "future")

    def test_update_with_publish_that_schedules_a_live_post_exits_7(self):
        wp = RecordingWordPress(existing=existing("publish"))

        code, logs = self.run_connector(
            wp, allow_update=True, force_publish=True, date_override=FUTURE
        )

        self.assertEqual(code, 7)
        self.assertEqual(wp.stored[123]["status"], "future")
        self.assertIn("status: sent 'publish', WordPress stored 'future'", logs)

    def test_explicit_date_that_publishes_a_scheduled_post_exits_7(self):
        wp = RecordingWordPress(existing=existing("future", FUTURE))

        code, logs = self.run_connector(wp, allow_update=True, date_override=PAST)

        self.assertEqual(code, 7)
        self.assertIn("status: sent 'future', WordPress stored 'publish'", logs)

    def test_create_still_sends_draft_unless_publish(self):
        for force_publish, status in ((False, "draft"), (True, "publish")):
            with self.subTest(force_publish=force_publish):
                wp = RecordingWordPress()

                code, logs = self.run_connector(wp, force_publish=force_publish)

                self.assertEqual(code, 0, logs)
                self.assertEqual(wp.stored[701]["status"], status)
                self.assertEqual(wp.stored[701]["date"], "2026-05-15T12:00:00")

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
                changed = [
                    line for line in logs.splitlines()
                    if re.match(r'^[-+]\s+"(status|date)"', line)
                ]
                self.assertEqual(changed, expected)


class UpdateStatusHelperTests(unittest.TestCase):
    def test_update_payload_drops_status_and_date_unless_asked_and_copies(self):
        payload = sent_payload()

        body = update_payload(payload, force_publish=False, send_date=False)
        self.assertNotIn("status", body)
        self.assertNotIn("date", body)
        self.assertEqual(payload["status"], "draft")
        self.assertEqual(payload["date"], "2026-05-15T12:00:00")

        body = update_payload(payload, force_publish=True, send_date=True)
        self.assertEqual(body, payload)
        self.assertIsNot(body, payload)

    def test_readback_without_a_sent_status_expects_the_previous_one_exactly(self):
        sent = update_payload(sent_payload(), force_publish=False, send_date=False)
        before = {"status": "publish", "date": PAST}

        self.assertEqual(
            readback_mismatches(sent, readback(status="publish", date="2026-11-12T10:00:00"), before=before),
            {},
        )
        for stored in ("draft", "future", "private"):
            with self.subTest(stored=stored):
                self.assertEqual(
                    readback_mismatches(sent, readback(status=stored), before=before),
                    {"status": ("publish", stored)},
                )

    def test_sent_publish_reads_back_as_future_only_when_the_post_was_not_live(self):
        sent = sent_payload(status="publish")

        self.assertEqual(readback_mismatches(sent, readback(status="future")), {})
        self.assertEqual(
            readback_mismatches(sent, readback(status="future"), before={"status": "draft"}), {}
        )
        self.assertEqual(
            readback_mismatches(sent, readback(status="future"), before={"status": "publish"}),
            {"status": ("publish", "future")},
        )

    def test_diff_without_a_sent_status_or_date_proposes_the_existing_ones(self):
        diff = update_diff(
            {"title": {"raw": TITLE}, "status": "future", "date": FUTURE},
            update_payload(sent_payload(), force_publish=False, send_date=False),
        )

        changed = [line for line in diff.splitlines() if re.match(r'^[-+]\s+"(status|date)"', line)]
        self.assertEqual(changed, [])


if __name__ == "__main__":
    unittest.main()
