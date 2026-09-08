import copy
import contextlib
import io
import json
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import apply_north_house_journey as journey  # noqa: E402


def fixture(name="services"):
    bodies = {
        "services": '<style>.keep {color: red}</style>\n<p>Keep this.</p>\n' + journey.SERVICES_ANCHOR + "\n</section>",
        "recap": "<p>Keep this.</p>\n" + journey.RECAP_ANCHOR + "\n<footer>Keep author</footer>",
        "events": "<p>Keep the shell.</p>\n" + journey.event_cards()[0] + "\n<script>keep()</script>",
    }
    item = {k: v for k, v in journey.TARGETS[name].items() if k != "endpoint"}
    item.update(status="publish", modified_gmt="2026-09-05T00:00:00", title={"raw": "Keep title"},
                featured_media=12742, meta={"keep": "metadata"}, content={"raw": bodies[name]})
    after = journey.rewrite(bodies[name], name)
    manifest = {name: {"modified_gmt": item["modified_gmt"], "before_sha256": journey.sha(bodies[name]),
                       "after_sha256": journey.sha(after)}}
    return item, after, manifest


class FakeWP:
    def __init__(self, item):
        self.item = copy.deepcopy(item)
        self.posts = []
        self.corrupt = False
        self.uncertain = False

    def get(self, *_args, **_kwargs):
        return copy.deepcopy(self.item)

    def post(self, endpoint, payload):
        self.posts.append((endpoint, payload))
        self.item["content"]["raw"] = "bad readback" if self.corrupt else payload["content"]
        self.item["modified_gmt"] = "2026-09-05T00:01:00"
        if self.uncertain:
            raise ConnectionError("lost response after write")


class NorthHouseJourneyTests(unittest.TestCase):
    def test_cli_rejects_incomplete_execute_before_resolving_credentials(self):
        for argv in (["check", "--execute"], ["apply", "--execute"], ["apply"], ["restore"], ["prepare"]):
            with self.subTest(argv=argv), patch.object(journey, "wp_process_credentials") as credentials:
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                    journey.main(argv)
                self.assertEqual(2, error.exception.code)
                credentials.assert_not_called()

    def test_private_artifacts_never_overwrite_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "snapshot.json"
            journey.private_write(target, "keep")
            with self.assertRaises(FileExistsError):
                journey.private_write(target, "overwrite")
            self.assertEqual("keep", target.read_text())
            self.assertEqual(0o600, stat.S_IMODE(target.stat().st_mode))

    def test_public_preview_preserves_server_added_content(self):
        import preview_north_house_journey as preview
        suffix = '<aside>Keep server-rendered author</aside><script>keepTheme()</script>'
        originals = {
            "services": journey.SERVICES_ANCHOR + suffix,
            "recap": f'<p class="wp-block-paragraph">{journey.TAKEAWAY}</p>' + suffix,
            "events": journey.event_cards()[0] + suffix,
        }
        for name, public in originals.items():
            after = preview.candidate_html(name, public)
            self.assertTrue(after.endswith(suffix))
            self.assertGreater(len(after), len(public))
        self.assertEqual("/events/", preview.local_links(journey.BASE + "/events/"))
        self.assertEqual(suffix, preview.candidate_html("contact", suffix))

    def test_patches_preserve_everything_outside_the_insert_or_card(self):
        for name in journey.TARGETS:
            with self.subTest(name=name):
                before, after, manifest = fixture(name)
                self.assertEqual(("pending", after), journey.plan(before, name, manifest))
                if name == "events":
                    old, new = journey.event_cards()
                    self.assertEqual(before["content"]["raw"], after.replace(new, old))
                else:
                    fragment = (journey.PACK / f'{"services-insert" if name == "services" else "recap-link"}.html').read_text().rstrip()
                    separator = fragment + "\n\n" if name == "services" else "\n\n" + fragment
                    self.assertEqual(before["content"]["raw"], after.replace(separator, "", 1))

    def test_missing_or_duplicate_anchor_refuses(self):
        for name in journey.TARGETS:
            before, _, _ = fixture(name)
            for raw in ("", before["content"]["raw"] * 2):
                with self.subTest(name=name, raw_length=len(raw)), self.assertRaises(journey.JourneyError):
                    journey.rewrite(raw, name)

    def test_wrong_identity_or_drift_sends_zero_writes(self):
        for field, value in [("id", 999), ("slug", "other"), ("type", "post"), ("status", "draft"),
                             ("modified_gmt", "changed"), ("content", {"raw": "changed"})]:
            item, _, manifest = fixture()
            item[field] = value
            wp = FakeWP(item)
            with self.subTest(field=field), self.assertRaises(journey.JourneyError):
                journey.apply(wp, "services", manifest, Path("unused"), execute=True)
            self.assertEqual([], wp.posts)

    def test_default_apply_is_read_only(self):
        item, _, manifest = fixture()
        wp = FakeWP(item)
        with patch.object(journey, "private_write") as save:
            self.assertEqual("pending", journey.apply(wp, "services", manifest, Path("unused")))
            save.assert_not_called()
        self.assertEqual([], wp.posts)

    def test_snapshot_precedes_content_only_write_and_reapply_is_noop(self):
        item, after, manifest = fixture()
        wp = FakeWP(item)
        with tempfile.TemporaryDirectory() as tmp:
            original = wp.post

            def post(endpoint, payload):
                snapshots = list(Path(tmp).glob("*.json"))
                self.assertEqual(1, len(snapshots))
                self.assertEqual(0o600, stat.S_IMODE(snapshots[0].stat().st_mode))
                self.assertEqual(item, json.loads(snapshots[0].read_text())["before"])
                original(endpoint, payload)

            wp.post = post
            journey.apply(wp, "services", manifest, Path(tmp), execute=True)
            self.assertEqual([("pages/2666", {"content": after})], wp.posts)
            self.assertEqual("already-applied", journey.apply(wp, "services", manifest, Path(tmp), execute=True))
            self.assertEqual(1, len(wp.posts))

    def test_missing_snapshot_or_changed_after_snapshot_sends_zero_writes(self):
        item, _, manifest = fixture()
        wp = FakeWP(item)
        with patch.object(journey, "private_write", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                journey.apply(wp, "services", manifest, Path("unused"), execute=True)
        self.assertEqual([], wp.posts)
        changed = copy.deepcopy(item)
        changed["title"]["raw"] = "Another editor"
        with tempfile.TemporaryDirectory() as tmp, patch.object(journey, "fetch", side_effect=[item, changed]):
            with self.assertRaisesRegex(journey.JourneyError, "changed after snapshot"):
                journey.apply(wp, "services", manifest, Path(tmp), execute=True)
        self.assertEqual([], wp.posts)

    def test_readback_failure_stops_without_automatic_restore(self):
        item, _, manifest = fixture()
        wp = FakeWP(item)
        wp.corrupt = True
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(journey.JourneyError, "exact readback"):
                journey.apply(wp, "services", manifest, Path(tmp), execute=True)
            self.assertEqual(1, len(list(Path(tmp).glob("*.json"))))
        self.assertEqual(1, len(wp.posts))

    def test_uncertain_write_is_not_retried(self):
        item, _, manifest = fixture()
        wp = FakeWP(item)
        wp.uncertain = True
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(journey.JourneyError, "uncertain write"):
                journey.apply(wp, "services", manifest, Path(tmp), execute=True)
            self.assertEqual("already-applied", journey.apply(wp, "services", manifest, Path(tmp)))
        self.assertEqual(1, len(wp.posts))

    def test_reviewed_after_hash_cannot_be_bypassed(self):
        item, _, manifest = fixture()
        manifest["services"]["after_sha256"] = "0" * 64
        with self.assertRaisesRegex(journey.JourneyError, "reviewed after hash"):
            journey.plan(item, "services", manifest)

    def test_restore_is_dry_by_default_exact_and_conflict_safe(self):
        item, after, manifest = fixture()
        wp = FakeWP(item)
        with tempfile.TemporaryDirectory() as tmp:
            journey.apply(wp, "services", manifest, Path(tmp), execute=True)
            snapshot = next(Path(tmp).glob("*.json"))
            self.assertEqual("restore-pending", journey.restore(wp, snapshot, manifest, Path(tmp)))
            self.assertEqual(1, len(wp.posts))
            wp.item["content"]["raw"] = after + "Other editor"
            with self.assertRaisesRegex(journey.JourneyError, "conflict"):
                journey.restore(wp, snapshot, manifest, Path(tmp), execute=True)
            wp.item["content"]["raw"] = after
            journey.restore(wp, snapshot, manifest, Path(tmp), execute=True)
            self.assertEqual(item["content"]["raw"], wp.item["content"]["raw"])
            self.assertEqual("already-restored", journey.restore(wp, snapshot, manifest, Path(tmp), execute=True))
            self.assertEqual(2, len(wp.posts))

    def test_recap_waits_for_services(self):
        item, _, manifest = fixture("recap")
        services, _, other = fixture("services")
        wp = FakeWP(item)
        with patch.object(journey, "fetch", side_effect=[item, services]):
            with self.assertRaisesRegex(journey.JourneyError, "Apply services"):
                journey.apply(wp, "recap", manifest | other, Path("unused"), execute=True)
        self.assertEqual([], wp.posts)

    def test_committed_recap_matches_reviewed_patch(self):
        manifest = journey.load_manifest()
        source = journey.REPO_ROOT / "content/drafts/2026-09-02-north-house-show-and-tell/post.html"
        after = source.read_text()
        fragment = (journey.PACK / "recap-link.html").read_text().strip()
        self.assertEqual(1, after.count(fragment))
        before = after.replace("\n\n" + fragment, "", 1)
        self.assertEqual(manifest["recap"]["before_sha256"], journey.sha(before))
        self.assertEqual(manifest["recap"]["after_sha256"], journey.sha(after))
        self.assertEqual(after, journey.rewrite(before, "recap"))

    def test_full_events_generation_changes_only_the_north_house_card(self):
        catalog = journey.events_lib.load_catalog()
        render = journey.events_render
        now = datetime(2026, 9, 5, tzinfo=timezone.utc)
        events = [e for e in catalog["events"] if render.public_status(e)]
        upcoming = sorted([e for e in events if not render.is_past(e, now)], key=render.parse_end)
        past = sorted([e for e in events if render.is_past(e, now)], key=render.parse_end, reverse=True)
        dynamic = render.render_dynamic_block(upcoming, past, journey.events_lib.resolve_path_roots(catalog))
        after = render.inject_into_shell(journey.events_lib.SHELL_PATH.read_text(), dynamic)
        for event in events:
            if event["id"] == journey.EVENT_ID:
                del event["recap_url"]
        before_dynamic = render.render_dynamic_block(upcoming, past, journey.events_lib.resolve_path_roots(catalog))
        before = render.inject_into_shell(journey.events_lib.SHELL_PATH.read_text(), before_dynamic)
        old_card, new_card = journey.event_cards()
        self.assertEqual(1, before.count(old_card))
        self.assertEqual(after, before.replace(old_card, new_card, 1))

    def test_new_fragments_pass_voice_and_public_safety(self):
        import voice_check
        for name in ("services-insert.html", "recap-link.html"):
            raw = (journey.PACK / name).read_text()
            self.assertEqual([], voice_check.scan_text(raw, ".html"))
            for forbidden in ("<style", "<script", "<h1", "/Users/", "notion.so", "wp-json", "target=", "object-fit"):
                self.assertNotIn(forbidden, raw)


if __name__ == "__main__":
    unittest.main()
