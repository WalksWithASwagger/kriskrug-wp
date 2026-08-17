"""Offline safety tests for the issue #827 photography hub apply helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_827_photography_hub.py"
SPEC = importlib.util.spec_from_file_location(
    "apply_issue_827_photography_hub", SCRIPT
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()
FIX_DIR = (
    MODULE.REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-827"
)


def spec_by_id(item_id: int) -> dict:
    return next(row for row in TARGETS["targets"] if row["id"] == item_id)


def exact(row: dict) -> str:
    return MODULE.exact_link(row["href"], row["anchor"])


def coda_fixture(*, figures: int = 16, already: str = "") -> str:
    shots = "\n".join(f"<figure>shot {i}</figure>" for i in range(figures))
    return (
        "<style>.kkx{color:#171310}</style>\n"
        "<div class=\"kkx\">\n"
        "  <p class=\"kkx-intro\">The full archive lives on "
        f"<a href=\"{TARGETS['flickr_href']}\">Flickr</a>.</p>\n"
        f"  <div>{shots}</div>\n"
        "  <section class=\"kkx-coda\">\n"
        "    <h2>This is a fraction of it.</h2>\n"
        "    <p>Twenty years of frames. The deep archive, including the "
        "cross-processed portraits and the work that isn't here, lives on Flickr."
        f"{already}</p>\n"
        f"    <a class=\"kkx-btn\" href=\"{TARGETS['flickr_href']}\">"
        "See 144,000+ frames on Flickr</a>\n"
        "  </section>\n"
        "</div>\n"
    )


def footer_block() -> str:
    return (
        '<!-- wp:paragraph {"className":"kk-collection-footer"} -->\n'
        '<p class="kk-collection-footer wp-block-paragraph">Part of the '
        '<a href="https://kriskrug.co/category/photography-visual-storytelling/">'
        "Photography and Visual Storytelling</a> collection. See also: "
        '<a href="https://kriskrug.co/example/">Sibling</a>.</p>\n'
        "<!-- /wp:paragraph -->"
    )


def fake_item(spec: dict, *, raw: str | None = None) -> dict:
    if raw is not None:
        body = raw
    elif spec["kind"] == "coda_page":
        body = coda_fixture()
    elif spec["kind"] == "before_footer":
        body = "<p>Fashion rant body.</p>\n\n" + footer_block()
    else:
        body = (
            '<p class="extended">I joined Model Mayhem. '
            "I've met a couple cool peeps already.</p>\n\n" + footer_block()
        )
    return {
        "id": spec["id"],
        "slug": spec["slug"],
        "content": {"raw": body},
    }


def run_main(*args: str) -> int:
    with (
        mock.patch.object(sys, "argv", ["apply_issue_827_photography_hub.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue827PhotographyHubTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_item(row) for row in TARGETS["targets"]}

    def _patch_request(self, calls):
        def fake_request(url, _header, body=None):
            calls.append((url, body))
            if "/pages/" in url:
                item_id = int(url.split("/pages/")[1].split("?")[0])
            else:
                item_id = int(url.split("/posts/")[1].split("?")[0])
            live = json.loads(json.dumps(self.lives[item_id]))
            if body is not None:
                if "content" in body:
                    live["content"] = {"raw": body["content"]}
                self.lives[item_id] = live
            return live

        return fake_request

    def test_targets_match_issue_rows_11_to_14(self):
        ids = [row["id"] for row in TARGETS["targets"]]
        self.assertEqual(ids, [12013, 1222, 1056])
        self.assertEqual(spec_by_id(12013)["rest"], "pages")
        self.assertEqual(spec_by_id(12013)["slug"], "photography")
        rows = {
            item["row"]: item
            for spec in TARGETS["targets"]
            for item in spec["rows"]
        }
        self.assertEqual(
            rows[11]["anchor"], "the whole archive, twenty years of it"
        )
        self.assertEqual(
            rows[11]["href"],
            "https://kriskrug.co/category/photography-visual-storytelling/",
        )
        self.assertEqual(
            rows[12]["anchor"], "the fashion and model years, 2006 to 2008"
        )
        self.assertEqual(
            rows[12]["href"],
            "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/",
        )
        self.assertEqual(
            rows[13]["anchor"], "how I found those people in the first place"
        )
        self.assertEqual(rows[14]["anchor"], "where all of that ended up")
        self.assertEqual(rows[14]["href"], "https://kriskrug.co/photography/")
        self.assertNotIn(1210, ids)
        self.assertTrue(
            set(TARGETS["out_of_payload_ids"]).isdisjoint(ids)
        )

    def test_payload_snippets_match_targets(self):
        coda = (FIX_DIR / "12013-coda-inserts.html").read_text(encoding="utf-8")
        self.assertIn(exact(spec_by_id(12013)["rows"][0]), coda)
        self.assertIn(exact(spec_by_id(12013)["rows"][1]), coda)
        self.assertNotIn("checklist-of-model-photographer-negotiation-items", coda)
        para = (FIX_DIR / "1222-sentence.html").read_text(encoding="utf-8").strip()
        self.assertEqual(para, spec_by_id(1222)["rows"][0]["paragraph"])
        peeps = (FIX_DIR / "1056-sentence.html").read_text(encoding="utf-8")
        self.assertIn(exact(spec_by_id(1056)["rows"][0]), peeps)

    def test_coda_insert_is_text_match_not_stale_block_index(self):
        spec = spec_by_id(12013)
        for figure_count in (0, 3, 16, 40):
            raw = coda_fixture(figures=figure_count)
            rewritten, notes = MODULE.rewrite_coda_page(raw, spec, TARGETS)
            self.assertIsNotNone(rewritten)
            self.assertIn("row 11 insert", notes)
            self.assertIn("row 12 insert", notes)
            self.assertIn(exact(spec["rows"][0]), rewritten)
            self.assertIn(exact(spec["rows"][1]), rewritten)
            self.assertEqual(
                MODULE.style_blocks(raw), MODULE.style_blocks(rewritten)
            )
            self.assertEqual(
                rewritten.count(TARGETS["flickr_href"]),
                raw.count(TARGETS["flickr_href"]),
            )
            self.assertNotIn(
                "checklist-of-model-photographer-negotiation-items", rewritten
            )

    def test_coda_skips_a_row_when_exact_href_and_anchor_exist(self):
        spec = spec_by_id(12013)
        row11 = exact(spec["rows"][0])
        raw = coda_fixture(already=f" The on-site version is {row11}.")
        rewritten, notes = MODULE.rewrite_coda_page(raw, spec, TARGETS)
        self.assertIsNotNone(rewritten)
        self.assertIn("row 11 already present", notes)
        self.assertIn("row 12 insert", notes)
        self.assertEqual(rewritten.count(row11), 1)
        self.assertIn(exact(spec["rows"][1]), rewritten)

    def test_coda_aborts_if_locate_text_missing_or_duplicated(self):
        spec = spec_by_id(12013)
        with self.assertRaises(ValueError):
            MODULE.rewrite_coda_page("<p>no coda</p>", spec, TARGETS)
        with self.assertRaises(ValueError):
            MODULE.rewrite_coda_page(
                coda_fixture() + "<h2>This is a fraction of it.</h2>",
                spec,
                TARGETS,
            )

    def test_coda_aborts_if_paragraph_resolves_inside_style(self):
        spec = spec_by_id(12013)
        poisoned = (
            "<style>This is a fraction of it. <p>lives on Flickr</p></style>"
            "<p>body</p>"
        )
        with self.assertRaises(ValueError):
            MODULE.rewrite_coda_page(poisoned, spec, TARGETS)

    def test_1222_inserts_before_footer_and_keeps_count(self):
        spec = spec_by_id(1222)
        raw = fake_item(spec)["content"]["raw"]
        rewritten, _notes = MODULE.rewrite_before_footer(raw, spec, TARGETS)
        self.assertIsNotNone(rewritten)
        self.assertIn(exact(spec["rows"][0]), rewritten)
        self.assertLess(
            rewritten.find(exact(spec["rows"][0])),
            rewritten.find(MODULE.FOOTER_SENTINEL),
        )
        self.assertEqual(MODULE.footer_count(raw), MODULE.footer_count(rewritten))
        self.assertIn("Sibling", rewritten)

    def test_1056_inserts_after_entity_encoded_peeps_line(self):
        spec = spec_by_id(1056)
        raw = (
            '<p class="extended">I joined. I&#8217;ve met a couple cool peeps '
            "already.</p>\n\n" + footer_block()
        )
        rewritten, _notes = MODULE.rewrite_after_peeps(raw, spec, TARGETS)
        self.assertIsNotNone(rewritten)
        self.assertIn("I&#8217;ve met a couple cool peeps already. Here is ", rewritten)
        self.assertIn(exact(spec["rows"][0]), rewritten)
        self.assertEqual(MODULE.footer_count(raw), MODULE.footer_count(rewritten))

    def test_dry_run_performs_no_local_or_wordpress_writes(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main())
        self.assertFalse(snapshot_dir.exists())
        self.assertTrue(calls)
        self.assertTrue(all(body is None for _, body in calls))
        self.assertTrue(any("/pages/12013" in url for url, _ in calls))
        self.assertTrue(any("/posts/1222" in url for url, _ in calls))
        self.assertTrue(any("/posts/1056" in url for url, _ in calls))

    def test_slug_mismatch_aborts_before_any_write(self):
        self.lives[12013]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--id", "12013")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_snapshots_then_posts_content_only(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--id", "12013"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn(exact(spec_by_id(12013)["rows"][0]), writes[0]["content"])
        self.assertIn(exact(spec_by_id(12013)["rows"][1]), writes[0]["content"])
        self.assertEqual(
            MODULE.style_blocks(self.lives[12013]["content"]["raw"]),
            MODULE.style_blocks(coda_fixture()),
        )
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)
        self.assertIn("pages-12013", snapshots[0].name)

    def test_apply_all_three_targets_is_content_only(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(3, len(writes))
        for body in writes:
            self.assertEqual(set(body), {"content"})
            self.assertNotIn("categories", body)

    def test_skip_when_already_applied(self):
        spec = spec_by_id(1222)
        applied, _notes = MODULE.rewrite_before_footer(
            fake_item(spec)["content"]["raw"], spec, TARGETS
        )
        self.lives[1222] = fake_item(spec, raw=applied)
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            self.assertEqual(0, run_main("--apply", "--id", "1222"))
        self.assertTrue(all(body is None for _, body in calls))

    def test_restore_refuses_ids_outside_the_allowlist(self):
        snapshot = self.tmp_path / "rest-posts-1067-before.json"
        snapshot.write_text(
            json.dumps(
                {
                    "id": 1067,
                    "slug": "hardcore-superstar-photoshoot",
                    "content": {"raw": "<p>nope</p>"},
                }
            ),
            encoding="utf-8",
        )
        with mock.patch.object(MODULE, "request", side_effect=self._patch_request([])):
            with self.assertRaises(SystemExit) as caught:
                run_main("--restore", str(snapshot))
        self.assertIn("not in the #827 set", str(caught.exception))

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (FIX_DIR / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("follow #826", apply_md)
        self.assertIn("zero", apply_md.lower())
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #402", apply_md)
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("inject_links", source)


if __name__ == "__main__":
    unittest.main()
