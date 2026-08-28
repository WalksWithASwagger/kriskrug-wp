"""Offline safety tests for the issue #4 alt-text batch helper."""

from __future__ import annotations

import copy
import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).parents[2]
    / "content/drafts/alt-text-backfill-2026-08-02/apply_batches.py"
)
SPEC = importlib.util.spec_from_file_location("alt_text_apply_batches", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def content_row(
    media_id: str,
    image_file: str,
    proposed_alt: str,
) -> dict[str, str]:
    return {
        "batch": "batch-1",
        "fix_surface": "post-content-block",
        "tier": "2-page",
        "page_id": "3899",
        "page_slug": "about",
        "page_url": "https://kriskrug.co/about/",
        "media_id": media_id,
        "image_file": image_file,
        "image_src": f"https://kriskrug.co/wp-content/uploads/{image_file}",
        "proposed_alt": proposed_alt,
    }


def page_record(raw: str) -> dict:
    return {
        "id": 3899,
        "slug": "about",
        "link": "https://kriskrug.co/about/",
        "status": "publish",
        "content": {"raw": raw},
    }


def media_row(
    media_id: str,
    image_file: str,
    proposed_alt: str,
    *,
    classification: str = "empty-alt-VIOLATION",
    media_library_alt: str = "",
) -> dict[str, str]:
    return {
        "fix_surface": "media-library-alt_text",
        "classification": classification,
        "media_id": media_id,
        "image_file": image_file,
        "image_src": f"https://s5102.pcdn.co/wp-content/uploads/{image_file}",
        "media_library_alt": media_library_alt,
        "proposed_alt": proposed_alt,
    }


class FakeClient:
    def __init__(self, get_responses: list[dict]):
        self.get_responses = iter(copy.deepcopy(get_responses))
        self.gets: list[tuple[str, dict | None]] = []
        self.posts: list[tuple[str, dict]] = []

    def get(self, path: str, *, params: dict | None = None) -> dict:
        self.gets.append((path, params))
        return next(self.get_responses)

    def post(self, path: str, payload: dict) -> dict:
        self.posts.append((path, payload))
        return {}


class AltTextApplyBatchSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.snapshot_root = Path(self.tempdir.name) / "snapshots"
        snapshot_root_patch = mock.patch.object(
            MODULE, "SNAPSHOT_ROOT", self.snapshot_root
        )
        snapshot_root_patch.start()
        self.addCleanup(snapshot_root_patch.stop)
        self.run_dir = self.snapshot_root / "run"

    def test_apply_refuses_entire_page_when_any_row_is_blocked(self):
        rows = [
            content_row("100", "community.jpg", "Community members at an event"),
            content_row("200", "portrait.jpg", "Portrait of Kris Krug"),
        ]
        live = page_record(
            '<img class="wp-image-100" src="community.jpg" alt="">'
            '<img class="wp-image-200" src="portrait.jpg" alt="Existing alt">'
        )
        client = FakeClient([live, live])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_content(client, True, self.run_dir, None)

        self.assertEqual(client.posts, [])
        self.assertEqual(report["pages"][0]["status"], "REFUSED-blocked-rows")
        self.assertFalse(self.run_dir.exists())

    def test_content_readback_is_bound_to_the_matching_image(self):
        proposed = "Community members at an event"
        rows = [content_row("100", "community.jpg", proposed)]
        live = page_record(
            '<img class="wp-image-100" src="community.jpg" alt="">'
            f'<img class="wp-image-999" src="other.jpg" alt="{proposed}">'
        )
        client = FakeClient([live, live])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_content(client, True, self.run_dir, None)

        page = report["pages"][0]
        self.assertEqual(page["status"], "WRITTEN-READBACK-MISSING")
        self.assertEqual(page["readback_missing_media_ids"], ["100"])

    def test_main_returns_nonzero_for_lowercase_conflict(self):
        report = {
            "batch": "content (batch 1)",
            "pages": [{"status": "dry-run", "items": [{"status": "conflict"}]}],
        }
        with (
            mock.patch.object(sys, "argv", ["apply_batches.py", "--batch", "content"]),
            mock.patch.object(MODULE, "SNAPSHOT_ROOT", Path(self.tempdir.name)),
            mock.patch.object(MODULE, "make_client", return_value=None),
            mock.patch.object(MODULE, "run_content", return_value=report),
        ):
            result = MODULE.main()

        self.assertEqual(result, 1)

    def test_snapshot_is_private(self):
        path = MODULE.snapshot(self.run_dir, "page-3899-before", {"id": 3899})

        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_content_restore_dry_run_performs_no_write(self):
        rows = [content_row("100", "community.jpg", "New alt")]
        source = MODULE.snapshot(
            self.run_dir / "source",
            "page-3899-before",
            page_record('<img class="wp-image-100" src="community.jpg" alt="">'),
        )
        client = FakeClient(
            [page_record('<img class="wp-image-100" src="community.jpg" alt="New alt">')]
        )

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_restore(
                "content", source, client, False, self.run_dir / "restore"
            )

        self.assertEqual(report["items"][0]["status"], "would-restore")
        self.assertEqual(client.posts, [])
        self.assertFalse((self.run_dir / "restore").exists())

    def test_content_restore_snapshots_current_state_before_write(self):
        rows = [content_row("100", "community.jpg", "New alt")]
        original = page_record('<img class="wp-image-100" src="community.jpg" alt="">')
        current = page_record(
            '<img class="wp-image-100" src="community.jpg" alt="New alt">'
        )
        source = MODULE.snapshot(
            self.run_dir / "source", "page-3899-before", original
        )
        restore_dir = self.run_dir / "restore"
        client = FakeClient([current, original])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_restore("content", source, client, True, restore_dir)

        self.assertEqual(
            client.posts,
            [("pages/3899", {"content": original["content"]["raw"]})],
        )
        recovery = restore_dir / "page-3899-before-restore.json"
        self.assertTrue(recovery.is_file())
        self.assertEqual(stat.S_IMODE(recovery.stat().st_mode), 0o600)
        self.assertEqual(report["items"][0]["status"], "restored-verified")

    def test_media_restore_rejects_snapshot_outside_planned_ids(self):
        rows = [media_row("100", "community.jpg", "New alt")]
        source = MODULE.snapshot(
            self.run_dir / "source",
            "media-999-before",
            {
                "id": 999,
                "source_url": "https://kriskrug.co/wp-content/uploads/other.jpg",
                "alt_text": "Old alt",
            },
        )
        client = FakeClient([])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            with self.assertRaisesRegex(SystemExit, "not in the approved media batch"):
                MODULE.run_restore("media", source, client, True, self.run_dir / "restore")

        self.assertEqual(client.posts, [])

    def test_media_restore_snapshots_current_state_before_write(self):
        rows = [media_row("100", "community.jpg", "New alt")]
        original = {
            "id": 100,
            "source_url": "https://kriskrug.co/wp-content/uploads/community.jpg",
            "alt_text": "",
        }
        current = {**original, "alt_text": "New alt"}
        source = MODULE.snapshot(
            self.run_dir / "source", "media-100-before", original
        )
        restore_dir = self.run_dir / "restore"
        client = FakeClient([current, original])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_restore("media", source, client, True, restore_dir)

        self.assertEqual(client.posts, [("media/100", {"alt_text": ""})])
        recovery = restore_dir / "media-100-before-restore.json"
        self.assertTrue(recovery.is_file())
        self.assertEqual(stat.S_IMODE(recovery.stat().st_mode), 0o600)
        self.assertEqual(report["items"][0]["status"], "restored-verified")

    def test_media_restore_uses_apply_report_after_inventory_identity_correction(self):
        proposed = "Alt written to the wrong duplicate attachment"
        source_dir = self.run_dir / "source"
        original = {
            "id": 6729,
            "source_url": "https://kriskrug.co/wp-content/uploads/2024/08/shared.png",
            "alt_text": "",
        }
        source = MODULE.snapshot(source_dir, "media-6729-before", original)
        (source_dir / "report.json").write_text(
            json.dumps(
                {
                    "batch": "media (batch 0)",
                    "mode": "APPLY",
                    "items": [
                        {
                            "media_id": "6729",
                            "proposed_alt": proposed,
                            "status": "written-verified",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        current = {**original, "alt_text": proposed}
        client = FakeClient([current, original])
        corrected_rows = [media_row("6014", "shared.png", proposed)]

        with mock.patch.object(MODULE, "load_rows", return_value=corrected_rows):
            report = MODULE.run_restore(
                "media", source, client, True, self.run_dir / "restore"
            )

        self.assertEqual(client.posts, [("media/6729", {"alt_text": ""})])
        self.assertEqual(report["items"][0]["status"], "restored-verified")

    def test_media_apply_uses_authenticated_state_for_write_and_readback(self):
        proposed = "Community members at an event"
        rows = [media_row("100", "community.jpg", proposed)]
        original = {
            "id": 100,
            "source_url": "https://kriskrug.co/wp-content/uploads/community.jpg",
            "alt_text": "",
        }
        client = FakeClient([original, {**original, "alt_text": proposed}])

        with (
            mock.patch.object(MODULE, "load_rows", return_value=rows),
            mock.patch.object(MODULE, "public_get", return_value=original) as public_get,
        ):
            report = MODULE.run_media(client, True, self.run_dir, "100")

        self.assertEqual(report["items"][0]["status"], "written-verified")
        self.assertEqual(
            client.gets,
            [
                ("media/100", {"context": "edit"}),
                ("media/100", {"context": "edit"}),
            ],
        )
        public_get.assert_not_called()

    def test_unauthenticated_media_read_bypasses_public_cache(self):
        live = {"id": 100, "alt_text": ""}
        with (
            mock.patch.object(MODULE.time, "time_ns", return_value=123),
            mock.patch.object(MODULE, "public_get", return_value=live) as public_get,
        ):
            result = MODULE.get_media("100", None)

        self.assertEqual(result, live)
        public_get.assert_called_once_with("media/100?cb=123")

    def test_media_apply_replaces_exact_inventoried_filename_alt(self):
        current = "community_event_100.jpg"
        proposed = "Community members at an event"
        rows = [
            media_row(
                "100",
                "community.jpg",
                proposed,
                classification="filename-style-alt-VIOLATION",
                media_library_alt=current,
            )
        ]
        original = {
            "id": 100,
            "source_url": "https://kriskrug.co/wp-content/uploads/community.jpg",
            "alt_text": current,
        }
        client = FakeClient([original, {**original, "alt_text": proposed}])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_media(client, True, self.run_dir, "100")

        self.assertEqual(report["items"][0]["status"], "written-verified")
        self.assertEqual(report["items"][0]["replacement_basis"], "inventory-baseline")
        self.assertEqual(client.posts, [("media/100", {"alt_text": proposed})])

    def test_media_apply_preserves_non_filename_inventory_alt(self):
        current = "Existing contextual alt"
        rows = [
            media_row(
                "100",
                "community.jpg",
                "Different contextual alt",
                classification="empty-alt-content-VIOLATION",
                media_library_alt=current,
            )
        ]
        live = {
            "id": 100,
            "source_url": "https://kriskrug.co/wp-content/uploads/community.jpg",
            "alt_text": current,
        }
        client = FakeClient([live])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_media(client, True, self.run_dir, "100")

        self.assertEqual(
            report["items"][0]["status"], "CONFLICT-existing-different-alt"
        )
        self.assertEqual(client.posts, [])
        self.assertFalse(self.run_dir.exists())

    def test_content_restore_refuses_intervening_live_edits(self):
        rows = [content_row("100", "community.jpg", "New alt")]
        original = page_record('<img class="wp-image-100" src="community.jpg" alt="">')
        source = MODULE.snapshot(
            self.run_dir / "source", "page-3899-before", original
        )
        drifted = page_record(
            '<img class="wp-image-100" src="community.jpg" alt="New alt">'
            "<p>Intervening editor change</p>"
        )
        client = FakeClient([drifted])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            with self.assertRaisesRegex(SystemExit, "drifted from the expected applied state"):
                MODULE.run_restore("content", source, client, True, self.run_dir / "restore")

        self.assertEqual(client.posts, [])
        self.assertFalse((self.run_dir / "restore").exists())

    def test_media_restore_refuses_intervening_alt_change(self):
        rows = [media_row("100", "community.jpg", "New alt")]
        original = {
            "id": 100,
            "source_url": "https://kriskrug.co/wp-content/uploads/community.jpg",
            "alt_text": "",
        }
        source = MODULE.snapshot(
            self.run_dir / "source", "media-100-before", original
        )
        drifted = {**original, "alt_text": "Editor supplied alt"}
        client = FakeClient([drifted])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            with self.assertRaisesRegex(SystemExit, "drifted from the expected applied state"):
                MODULE.run_restore("media", source, client, True, self.run_dir / "restore")

        self.assertEqual(client.posts, [])

    def test_restore_rejects_snapshot_outside_private_generated_root(self):
        outside = Path(self.tempdir.name) / "page-3899-before.json"
        MODULE.snapshot(outside.parent, outside.stem, page_record("original"))
        client = FakeClient([])

        with self.assertRaisesRegex(SystemExit, "private generated snapshot directory"):
            MODULE.run_restore("content", outside, client, False, self.run_dir / "restore")

    def test_media_only_id_must_exist_in_the_approved_batch(self):
        rows = [media_row("100", "community.jpg", "New alt")]

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            with self.assertRaisesRegex(SystemExit, "not in the approved media batch"):
                MODULE.run_media(None, False, self.run_dir, "999")

    def test_media_dry_run_rejects_duplicate_filename_from_wrong_upload_month(self):
        rows = [media_row("6126", "shared-name.png", "Reviewed alt")]
        rows[0]["image_src"] = (
            "https://s5102.pcdn.co/wp-content/uploads/2024/06/shared-name.png"
        )
        wrong_upload = {
            "id": 6126,
            "source_url": "https://kriskrug.co/wp-content/uploads/2024/07/shared-name.png",
            "alt_text": "",
        }
        client = FakeClient([wrong_upload])

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            report = MODULE.run_media(client, False, self.run_dir, "6126")

        self.assertEqual(report["items"][0]["status"], "REFUSED-identity-mismatch")
        self.assertFalse(report["items"][0]["verified_file"])
        self.assertEqual(client.posts, [])

    def test_similarly_named_media_have_asset_specific_proposals(self):
        targets, _ = MODULE.media_targets(MODULE.load_rows())
        proposals = {
            row["media_id"]: row["proposed_alt"]
            for row in targets
            if row["media_id"] in {"6985", "7637"}
        }

        self.assertEqual(
            proposals,
            {
                "6985": (
                    "The Human Algorithm keynote graphic with Kris Kr&#252;g "
                    "speaking beside a group at Enya Liftoff"
                ),
                "7637": (
                    "Autolume: Post-Photographic Cybernetic Portraiture graphic "
                    "showing a white-haired figure in red glasses surrounded by "
                    "camera lenses"
                ),
            },
        )

    def test_content_only_page_must_exist_in_the_approved_batch(self):
        rows = [content_row("100", "community.jpg", "New alt")]

        with mock.patch.object(MODULE, "load_rows", return_value=rows):
            with self.assertRaisesRegex(SystemExit, "not in the approved content batch"):
                MODULE.run_content(None, False, self.run_dir, "999")

    def test_content_target_selects_exact_page_and_media_outside_batch_one(self):
        pages = MODULE.content_targets(MODULE.load_rows(), "6815", "6835")

        self.assertEqual(list(pages), ["6815"])
        self.assertEqual(len(pages["6815"]), 1)
        self.assertEqual(pages["6815"][0]["media_id"], "6835")
        self.assertEqual(
            pages["6815"][0]["proposed_alt"],
            "Vancouver AI meetup crowd standing shoulder to shoulder under magenta "
            "light, watching something off frame",
        )

    def test_content_target_changes_only_the_exact_selected_image(self):
        target = content_row("6835", "crowd-shot-vancovuer-ai-1024x683.jpeg", "Crowd alt")
        target.update(
            {
                "batch": "batch-2",
                "tier": "4-archive-sample",
                "page_id": "6815",
                "page_slug": "august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics",
                "page_url": (
                    "https://kriskrug.co/2024/09/01/"
                    "august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/"
                ),
            }
        )
        sibling = {**target, "batch": "batch-5", "media_id": "999", "image_file": "other.jpg"}
        sibling["image_src"] = "https://kriskrug.co/wp-content/uploads/other.jpg"
        original_html = (
            '<img class="wp-image-6835" src="crowd-shot-vancovuer-ai-1024x683.jpeg" alt="">'
            '<img class="wp-image-999" src="other.jpg" alt="">'
        )
        changed_html = original_html.replace(
            'src="crowd-shot-vancovuer-ai-1024x683.jpeg" alt=""',
            'src="crowd-shot-vancovuer-ai-1024x683.jpeg" alt="Crowd alt"',
        )

        def record(raw: str) -> dict:
            return {
                "id": 6815,
                "slug": target["page_slug"],
                "link": target["page_url"],
                "status": "publish",
                "content": {"raw": raw},
            }

        client = FakeClient([record(original_html), record(changed_html)])
        with mock.patch.object(MODULE, "load_rows", return_value=[target, sibling]):
            report = MODULE.run_content(
                client, True, self.run_dir, "6815", "6835"
            )

        self.assertEqual(
            client.posts,
            [("posts/6815", {"content": changed_html})],
        )
        self.assertEqual(report["pages"][0]["rows"], 1)
        self.assertEqual(report["pages"][0]["status"], "written-verified")

    def test_content_media_selector_requires_exactly_one_page_row(self):
        row = content_row("6835", "crowd.jpg", "Crowd alt")

        with self.assertRaisesRegex(SystemExit, "requires --only-page-id"):
            MODULE.content_targets([row], None, "6835")
        with self.assertRaisesRegex(SystemExit, "expected exactly one inventory row"):
            MODULE.content_targets([row, row.copy()], "3899", "6835")

    def test_exact_content_target_refuses_multiple_matching_tags(self):
        row = content_row("6835", "crowd.jpg", "Crowd alt")
        row.update(
            {
                "batch": "batch-2",
                "tier": "4-archive-sample",
                "page_id": "6815",
                "page_slug": "meetup-recap",
                "page_url": "https://kriskrug.co/2024/09/01/meetup-recap/",
            }
        )
        live = {
            "id": 6815,
            "slug": "meetup-recap",
            "link": row["page_url"],
            "status": "publish",
            "content": {
                "raw": (
                    '<img class="wp-image-6835" src="crowd.jpg" alt="">'
                    '<img class="wp-image-6835" src="crowd.jpg" alt="">'
                )
            },
        }
        client = FakeClient([live, live])

        with mock.patch.object(MODULE, "load_rows", return_value=[row]):
            report = MODULE.run_content(
                client, True, self.run_dir, "6815", "6835"
            )

        self.assertEqual(client.posts, [])
        self.assertEqual(
            report["pages"][0]["status"], "REFUSED-exact-target-match-count"
        )

    def test_targeted_post_restore_uses_the_post_endpoint(self):
        row = content_row("6835", "crowd.jpg", "Crowd alt")
        row.update(
            {
                "batch": "batch-2",
                "tier": "4-archive-sample",
                "page_id": "6815",
                "page_slug": "meetup-recap",
                "page_url": "https://kriskrug.co/2024/09/01/meetup-recap/",
            }
        )
        original = {
            "id": 6815,
            "slug": "meetup-recap",
            "link": row["page_url"],
            "status": "publish",
            "content": {"raw": '<img class="wp-image-6835" src="crowd.jpg" alt="">'},
        }
        applied = copy.deepcopy(original)
        applied["content"]["raw"] = (
            '<img class="wp-image-6835" src="crowd.jpg" alt="Crowd alt">'
        )
        source = MODULE.snapshot(
            self.run_dir / "source", "post-6815-before", original
        )
        client = FakeClient([applied, original])

        with mock.patch.object(MODULE, "load_rows", return_value=[row]):
            report = MODULE.run_restore(
                "content",
                source,
                client,
                True,
                self.run_dir / "restore",
                "6815",
                "6835",
            )

        self.assertEqual(
            client.posts,
            [("posts/6815", {"content": original["content"]["raw"]})],
        )
        self.assertEqual(report["items"][0]["status"], "restored-verified")

    def test_proposed_alt_rejects_html_markup(self):
        with self.assertRaisesRegex(SystemExit, "HTML markup"):
            MODULE.set_tag_alt(
                '<img src="community.jpg" alt="">', "<script>alert(1)</script>"
            )

    def test_main_rejects_selector_for_the_wrong_batch(self):
        cases = [
            (["--batch", "media", "--only-page-id", "3899"], "content selector"),
            (["--batch", "content", "--only-media-id", "100"], "media selector"),
            (
                ["--batch", "media", "--only-content-media-id", "100"],
                "content selector",
            ),
            (
                ["--batch", "content", "--only-content-media-id", "100"],
                "requires --only-page-id",
            ),
        ]
        for arguments, message in cases:
            with self.subTest(arguments=arguments):
                with (
                    mock.patch.object(sys, "argv", ["apply_batches.py", *arguments]),
                    mock.patch.object(MODULE, "make_client", return_value=None),
                ):
                    with self.assertRaisesRegex(SystemExit, message):
                        MODULE.main()


if __name__ == "__main__":
    unittest.main()
