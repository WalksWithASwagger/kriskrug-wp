import io
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import wp_post_ia_rollout as rollout  # noqa: E402


PILOT_MEDIA_ALT = "Cover image for Make Culture, Not Content, highlighting Kris Krug's culture-first AI message."


class FakeWP:
    def __init__(self):
        self.posts = []

    def post(self, endpoint, payload):
        self.posts.append((endpoint, payload))
        return {"ok": True}


def audit(
    post_id=42,
    slug="make-culture-not-content",
    featured_media=11264,
    missing_excerpt=True,
    missing_featured=False,
    missing_featured_alt=True,
):
    return rollout.PostAudit(
        post_id=post_id,
        slug=slug,
        link=f"https://kriskrug.co/{slug}/",
        title="Make Culture, Not Content",
        featured_media=featured_media,
        featured_alt="",
        has_excerpt=not missing_excerpt,
        has_featured=featured_media > 0,
        has_featured_alt=not missing_featured_alt,
        missing_excerpt=missing_excerpt,
        missing_featured=missing_featured,
        missing_featured_alt=missing_featured_alt,
    )


class WpPostIaRolloutDryRunTests(unittest.TestCase):
    def test_dry_run_builds_plan_without_wordpress_writes_or_snapshot(self):
        fake_wp = FakeWP()
        before_audits = [audit()]
        after_audits = [
            audit(
                missing_excerpt=False,
                missing_featured=False,
                missing_featured_alt=False,
            )
        ]

        with mock.patch.object(sys, "argv", ["wp_post_ia_rollout.py", "--since", "2026-01-01"]), \
             mock.patch.object(rollout, "load_config", return_value=rollout.Config("https://example.com", "u", "p")), \
             mock.patch.object(rollout, "WordPressClient", return_value=fake_wp), \
             mock.patch.object(rollout, "fetch_posts", side_effect=[["before"], ["after"]]), \
             mock.patch.object(rollout, "audit_posts", side_effect=[before_audits, after_audits]), \
             mock.patch.object(rollout, "fetch_media", return_value={"alt_text": ""}), \
             mock.patch.object(
                 rollout,
                 "post_content",
                 return_value="<p>This is the first sentence. This second sentence makes a useful excerpt.</p>",
             ), \
             mock.patch.object(rollout, "public_page_probe", return_value={
                 "featured_alt": "alt",
                 "og_alt": "og alt",
                 "hierarchy_ok": True,
                 "hardcoded_field_note": False,
                 "schema_has_image": True,
             }), \
             mock.patch.object(rollout, "write_report") as write_report, \
             mock.patch.object(rollout, "snapshot_targets") as snapshot_targets, \
             mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
            rollout.main()

        self.assertEqual(fake_wp.posts, [])
        snapshot_targets.assert_not_called()
        write_report.assert_called_once()
        output = stdout.getvalue()
        self.assertIn("[dry-run] planned writes: media=1 excerpt=1", output)
        self.assertIn("media_updates=1 excerpt_updates=1", output)

    def test_execute_path_snapshots_before_wordpress_writes(self):
        fake_wp = FakeWP()
        before_audits = [audit()]
        after_audits = [
            audit(
                missing_excerpt=False,
                missing_featured=False,
                missing_featured_alt=False,
            )
        ]
        snapshot_path = Path("/tmp/pre-write-snapshot.json")

        with mock.patch.object(sys, "argv", ["wp_post_ia_rollout.py", "--execute", "--since", "2026-01-01"]), \
             mock.patch.object(rollout, "load_config", return_value=rollout.Config("https://example.com", "u", "p")), \
             mock.patch.object(rollout, "WordPressClient", return_value=fake_wp), \
             mock.patch.object(rollout, "fetch_posts", side_effect=[["before"], ["after"]]), \
             mock.patch.object(rollout, "audit_posts", side_effect=[before_audits, after_audits]), \
             mock.patch.object(rollout, "fetch_media", return_value={"alt_text": ""}), \
             mock.patch.object(
                 rollout,
                 "post_content",
                 return_value="<p>This is the first sentence. This second sentence makes a useful excerpt.</p>",
             ), \
             mock.patch.object(rollout, "public_page_probe", return_value={
                 "featured_alt": "alt",
                 "og_alt": "og alt",
                 "hierarchy_ok": True,
                 "hardcoded_field_note": False,
                 "schema_has_image": True,
             }), \
             mock.patch.object(rollout, "write_report"), \
             mock.patch.object(rollout, "snapshot_targets", return_value=snapshot_path) as snapshot_targets, \
             mock.patch("sys.stdout", new_callable=io.StringIO):
            rollout.main()

        snapshot_targets.assert_called_once()
        self.assertEqual(
            fake_wp.posts,
            [
                ("/wp-json/wp/v2/media/11264", {"alt_text": PILOT_MEDIA_ALT}),
                ("/wp-json/wp/v2/posts/42", {"excerpt": "This is the first sentence. This second sentence makes a useful excerpt."}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
