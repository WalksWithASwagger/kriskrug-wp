"""run() must decide create, update or abort before any WordPress write.

Every case drives the real kk_notion_to_wp.run() against an in-memory
Notion page and a FakeWordPress that records calls. Nothing touches the
network, Notion, WordPress or the repo's content/drafts/ folder.
"""

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import requests

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402
from update_safety import readback_mismatches  # noqa: E402
from wp_client import SlugVerificationFailed  # noqa: E402

PAGE_ID = "0123456789abcdef0123456789abcdef"
TITLE = "Calling Us All In"
SLUG = "calling-us-all-in"
IMAGE_URL = "https://files.example.test/calling.jpg?X-Amz-Signature=abc"
WRITE_CALLS = {"upload_media", "ensure_term", "create_post", "update_post"}

# sent title -> (raw values WordPress may store for it faithfully,
#                texturized title.rendered, a raw value that is real drift)
TITLE_ROUND_TRIPS = {
    "Art & Code": (
        ["Art & Code", "Art &amp; Code"],
        "Art &#038; Code",
        "Art &amp;amp; Code",
    ),
    "KK's Field Notes": (
        ["KK's Field Notes", "KK&#039;s Field Notes"],
        "KK&#8217;s Field Notes",
        "KK\\'s Field Notes",
    ),
    "Café Krüg": (
        ["Café Krüg", "Caf&#233; Kr&#252;g"],
        "Café Krüg",
        "CafÃ© KrÃ¼g",
    ),
    # Non-latin1 text as the writers will send it once #1225 lands.
    "Eth&#7885;&#769;s": (
        ["Eth&#7885;&#769;s", "Ethọ́s"],
        "Eth&#7885;&#769;s",
        "Eth??s",
    ),
}


def notion_page() -> dict:
    return {
        "id": PAGE_ID,
        "properties": {
            "Name": {"type": "title", "title": [{"plain_text": TITLE}]},
            "Publication Date": {"type": "date", "date": {"start": "2026-05-15"}},
            "Tags": {
                "type": "multi_select",
                "multi_select": [{"name": "Vancouver AI"}],
            },
            "Type": {"type": "select", "select": {"name": "Report"}},
        },
    }


def notion_blocks() -> list[dict]:
    return [
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"plain_text": "We showed up and counted the room."}]
            },
        },
        {
            "type": "image",
            "image": {"type": "file", "file": {"url": IMAGE_URL}, "caption": []},
        },
    ]


class FakeNotion:
    def __init__(self, token):
        self.token = token

    def page(self, page_id):
        return notion_page()

    def block_children(self, page_id):
        return notion_blocks()


def wordpress_status(status: str, date: str) -> str:
    """wp_insert_post's date rule: a publish dated in the future is scheduled,
    and a scheduled post whose date has passed is published."""
    when = datetime.fromisoformat(date)
    now = datetime.now(timezone.utc) if when.tzinfo else datetime.now()
    if status == "publish" and when > now:
        return "future"
    if status == "future" and when <= now:
        return "publish"
    return status


def stored_post(post_id: int, payload: dict) -> dict:
    """What WordPress hands back for a post it stored as sent, after its date rule."""
    return {
        "id": post_id,
        "link": f"https://wp.example.test/?p={post_id}",
        "title": {"raw": payload["title"]},
        "slug": payload["slug"],
        "status": wordpress_status(payload["status"], payload["date"]),
        "date": payload["date"],
        "date_gmt": payload["date"],
        "meta": dict(payload["meta"]),
    }


class FakeWordPress:
    def __init__(self, *, existing=None, lookup_error=None, readback_overrides=None):
        self.existing = existing
        self.lookup_error = lookup_error
        self.readback_overrides = readback_overrides or {}
        self.stored = {}
        self.calls = []

    def writes(self):
        return [name for name, *_ in self.calls if name in WRITE_CALLS]

    def find_post_by_slug(self, slug):
        self.calls.append(("find_post_by_slug", slug))
        if self.lookup_error:
            raise self.lookup_error
        return self.existing["id"] if self.existing else None

    def get_post(self, post_id):
        self.calls.append(("get_post", post_id))
        if post_id in self.stored:
            return {**self.stored[post_id], **self.readback_overrides}
        return self.existing

    def upload_media(self, path, alt, **kwargs):
        self.calls.append(("upload_media", path.name))
        return {"id": 501, "source_url": f"https://wp.example.test/uploads/{path.name}"}

    def ensure_term(self, taxonomy, name):
        self.calls.append(("ensure_term", taxonomy, name))
        return 900 + len(self.calls)

    def create_post(self, payload):
        self.calls.append(("create_post", payload["slug"]))
        self.stored[701] = stored_post(701, payload)
        return self.stored[701]

    def update_post(self, post_id, payload, *, expected_slug):
        self.calls.append(("update_post", post_id, expected_slug))
        # Like WordPress, an update keeps the stored status and date it was not sent.
        kept = {"status": self.existing["status"], "date": self.existing["date"]}
        self.stored[post_id] = stored_post(post_id, {**kept, **payload})
        return self.stored[post_id]


def existing_post(title: str) -> dict:
    return {
        "id": 123,
        "title": {"raw": title},
        "slug": SLUG,
        "status": "publish",
        "date": "2026-05-07T11:37:33",
    }


class RunOrderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        cfg = SimpleNamespace(
            notion_token="fake-notion-token",
            wp_base_url="https://wp.example.test",
            wp_user="fake-user",
            wp_app_password="fake-app-password",
            wp_author_id=1,
            has_wp_credentials=True,
        )

        def fake_download(url, dest):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(b"not really a jpeg")
            return dest.stat().st_size

        for name, value in {
            "load_config": lambda: cfg,
            "Notion": FakeNotion,
            "download_image": fake_download,
            "DRAFTS_DIR": self.tmp / "drafts",
            "REPO_ROOT": self.tmp,
        }.items():
            patcher = mock.patch.object(kk_notion_to_wp, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_connector(self, wp, **kwargs):
        logs = io.StringIO()
        with mock.patch.object(kk_notion_to_wp, "WordPress", lambda *a, **k: wp):
            with contextlib.redirect_stdout(logs):
                code = kk_notion_to_wp.run(
                    f"https://www.notion.so/Calling-{PAGE_ID}",
                    dry_run=False,
                    force_publish=False,
                    **kwargs,
                )
        return code, logs.getvalue()

    def test_existing_slug_without_update_makes_zero_writes(self):
        wp = FakeWordPress(existing=existing_post(TITLE))

        code, logs = self.run_connector(wp)

        self.assertEqual(code, 2)
        self.assertEqual(wp.writes(), [])
        self.assertIn("--update was not passed", logs)

    def test_ambiguous_or_failed_slug_lookup_makes_zero_writes(self):
        for message in (
            f"slug {SLUG!r} matches 2 records (ids [123, 456])",
            f"slug lookup for {SLUG!r} got HTTP 503",
        ):
            with self.subTest(message=message):
                wp = FakeWordPress(lookup_error=SlugVerificationFailed(message))

                code, logs = self.run_connector(wp)

                self.assertEqual(code, 8)
                self.assertEqual(wp.writes(), [])
                self.assertIn(message, logs)

    def test_unreachable_slug_lookup_raises_before_any_write(self):
        wp = FakeWordPress(lookup_error=requests.ConnectionError("connection refused"))

        with self.assertRaises(requests.ConnectionError):
            self.run_connector(wp)

        self.assertEqual(wp.writes(), [])

    def test_diff_lookup_refusal_exits_8_without_a_traceback(self):
        message = f"slug {SLUG!r} matches 2 records (ids [123, 456])"
        wp = FakeWordPress(lookup_error=SlugVerificationFailed(message))

        code, logs = self.run_connector(wp, diff_update=True)

        self.assertEqual(code, 8)
        self.assertEqual(wp.writes(), [])
        self.assertIn(message, logs)
        self.assertIn("No diff was emitted", logs)

    def test_title_guard_abort_makes_zero_writes(self):
        wp = FakeWordPress(existing=existing_post("Web Summit Vancouver 2026"))

        code, logs = self.run_connector(wp, allow_update=True)

        self.assertEqual(code, 3)
        self.assertEqual(wp.writes(), [])
        self.assertIn("too different", logs)

    def test_readback_slug_mismatch_exits_non_zero(self):
        wp = FakeWordPress(readback_overrides={"slug": f"{SLUG}-2"})

        code, logs = self.run_connector(wp)

        self.assertEqual(code, 7)
        self.assertEqual(wp.writes()[-1], "create_post")
        self.assertIn(f"slug: sent {SLUG!r}, WordPress stored '{SLUG}-2'", logs)

    def test_title_round_trip_exits_0_and_title_drift_exits_7(self):
        for sent, (faithful, rendered, drifted) in TITLE_ROUND_TRIPS.items():
            for stored, expected_code in [
                *((raw, 0) for raw in faithful),
                (drifted, 7),
            ]:
                with self.subTest(sent=sent, stored=stored):
                    wp = FakeWordPress(
                        readback_overrides={
                            "title": {"raw": stored, "rendered": rendered}
                        }
                    )

                    code, logs = self.run_connector(
                        wp, title_override=sent, slug_override=SLUG
                    )

                    self.assertEqual(code, expected_code)
                    self.assertEqual(wp.writes()[-1], "create_post")
                    self.assertEqual("title: sent" in logs, expected_code == 7, logs)

    def test_readback_mismatch_is_a_non_zero_process_exit(self):
        wp = FakeWordPress(readback_overrides={"status": "publish"})
        argv = ["kk_notion_to_wp.py", f"https://www.notion.so/Calling-{PAGE_ID}"]

        with (
            mock.patch.object(kk_notion_to_wp, "WordPress", lambda *a, **k: wp),
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(SystemExit) as exit_info,
        ):
            kk_notion_to_wp.main()

        self.assertEqual(exit_info.exception.code, 7)

    def test_happy_path_looks_up_then_uploads_media_then_creates(self):
        wp = FakeWordPress()

        code, _ = self.run_connector(wp)

        self.assertEqual(code, 0)
        names = [name for name, *_ in wp.calls]
        self.assertEqual(names[0], "find_post_by_slug")
        self.assertEqual(
            wp.writes(), ["upload_media", "ensure_term", "ensure_term", "create_post"]
        )
        self.assertEqual(names[-1], "get_post")
        self.assertEqual(wp.stored[701]["slug"], SLUG)

    def test_guarded_update_checks_title_before_any_write(self):
        wp = FakeWordPress(existing=existing_post(TITLE))

        code, _ = self.run_connector(wp, allow_update=True)

        self.assertEqual(code, 0)
        names = [name for name, *_ in wp.calls]
        self.assertEqual(names[:2], ["find_post_by_slug", "get_post"])
        self.assertEqual(
            wp.writes(), ["upload_media", "ensure_term", "ensure_term", "update_post"]
        )
        self.assertIn(("update_post", 123, SLUG), wp.calls)


def sent_payload(**overrides) -> dict:
    payload = {
        "title": TITLE,
        "slug": SLUG,
        "status": "draft",
        "date": "2026-05-15T12:00:00",
    }
    payload.update(overrides)
    return payload


def readback(**overrides) -> dict:
    post = {
        "title": {"raw": TITLE},
        "slug": SLUG,
        "status": "draft",
        "date": "2026-05-15T12:00:00",
        "date_gmt": "2026-05-15T19:00:00",
    }
    post.update(overrides)
    return post


class ReadbackMismatchTests(unittest.TestCase):
    def test_exact_readback_matches(self):
        self.assertEqual(readback_mismatches(sent_payload(), readback()), {})

    def test_rendered_title_is_never_the_stored_value(self):
        mismatches = readback_mismatches(
            sent_payload(), readback(title={"rendered": TITLE})
        )

        self.assertEqual(mismatches, {"title": (TITLE, None)})

    def test_each_identity_field_is_compared(self):
        mismatches = readback_mismatches(
            sent_payload(),
            readback(
                title={"raw": "Calling Us All In?"},
                slug=f"{SLUG}-2",
                status="publish",
                date="2026-05-16T12:00:00",
            ),
        )

        self.assertEqual(
            mismatches,
            {
                "title": (TITLE, "Calling Us All In?"),
                "slug": (SLUG, f"{SLUG}-2"),
                "status": ("draft", "publish"),
                "date": ("2026-05-15T12:00:00", "2026-05-16T12:00:00"),
            },
        )

    def test_scheduled_publish_reads_back_as_future(self):
        self.assertEqual(
            readback_mismatches(
                sent_payload(status="publish"), readback(status="future")
            ),
            {},
        )

    def test_draft_never_reads_back_as_future(self):
        self.assertIn(
            "status", readback_mismatches(sent_payload(), readback(status="future"))
        )

    def test_offset_date_is_compared_in_utc(self):
        sent = sent_payload(date="2026-05-15T12:00:00.000-07:00")

        self.assertEqual(readback_mismatches(sent, readback()), {})
        self.assertIn(
            "date",
            readback_mismatches(sent, readback(date_gmt="2026-05-15T12:00:00")),
        )

    def test_title_whitespace_trimmed_by_wordpress_is_not_drift(self):
        self.assertEqual(
            readback_mismatches(sent_payload(title=f" {TITLE} "), readback()), {}
        )


if __name__ == "__main__":
    unittest.main()
