"""Tests for the declared publisher ID map (issue #254).

publisher-ids.json replaces the WordPress IDs that used to be typed straight into
the one-off publish_*.py scripts. The equivalence tests below pin the manifest to
the exact literals those scripts carried before the refactor, so "de-hardcoded"
provably means "same numbers, one declaration" and not "new numbers".
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402

MANIFEST_PATH = SCRIPT_DIR / "publisher-ids.json"

# --- pre-#254 literals, transcribed verbatim from the scripts -----------------
LEGACY_DC_PROTEST_CATEGORY_ID = 1678
LEGACY_YOU_CANT_DRINK_CATEGORY_ID = 1678
LEGACY_YOU_CANT_DRINK_FEATURED_ID = 11976
LEGACY_KEEP_THE_MACHINE_CATEGORY_IDS = [1678, 1754]

LEGACY_AI_SIGNS = {
    11915: ("https://kriskrug.co/wp-content/uploads/2026/05/02-both-hands-full.png", "BOTH HANDS FULL, neon block-stack lettering over two hands overflowing with shapes"),
    11916: ("https://kriskrug.co/wp-content/uploads/2026/05/01-dumbest-timeline-the-keeper.png", "THIS IS THE DUMBEST TIMELINE & I WOULDN'T MISS IT, CMYK slab type"),
    11917: ("https://kriskrug.co/wp-content/uploads/2026/05/01-ruthlessly-optimistic-absolutely-terrified.png", "RUTHLESSLY OPTIMISTIC & ABSOLUTELY TERRIFIED, acid riso, sunny yellow into blood red"),
    11918: ("https://kriskrug.co/wp-content/uploads/2026/05/04-water-the-servers-last.png", "WATER THE SERVERS LAST, block-stack type with a watering can over a server rack"),
    11919: ("https://kriskrug.co/wp-content/uploads/2026/05/06-who-s-a-thirsty-little-data-center.png", "WHO'S A THIRSTY LITTLE DATA CENTER?, a googly-eyed building with its tongue out"),
    11920: ("https://kriskrug.co/wp-content/uploads/2026/05/02-we-are-the-training-data.jpg", "WE ARE THE TRAINING DATA, datamosh glitch type"),
    11921: ("https://kriskrug.co/wp-content/uploads/2026/05/09-ai-wrote-a-better-sign.jpg", "AI WROTE A BETTER SIGN THAN THIS ONE, neon block panels"),
    11922: ("https://kriskrug.co/wp-content/uploads/2026/05/03-my-position-yes-also-help.png", "MY POSITION: YES. ALSO: HELP., green YES over a panicked red HELP"),
    11923: ("https://kriskrug.co/wp-content/uploads/2026/05/03-it-s-complicated.png", "IT'S COMPLICATED, CMYK halftone"),
    11924: ("https://kriskrug.co/wp-content/uploads/2026/05/04-i-contain-multitudes.png", "I CONTAIN MULTITUDES, fractured tall glyphs in pink, teal, cream"),
    11925: ("https://kriskrug.co/wp-content/uploads/2026/05/07-error-404-side-not-found.png", "ERROR 404: SIDE NOT FOUND, RGB-split datamosh"),
    11926: ("https://kriskrug.co/wp-content/uploads/2026/05/09-stop-okay-go-no-stop.png", "STOP. okay GO. no, STOP., clashing panels with a strike-through"),
    11927: ("https://kriskrug.co/wp-content/uploads/2026/05/07-hush-now-little-supercluster.png", "HUSH NOW, LITTLE SUPERCLUSTER, server racks tucked in under a quilt, crescent moon"),
    11928: ("https://kriskrug.co/wp-content/uploads/2026/05/08-i-love-the-cloud-i-just-want-it-to-rain.png", "I LOVE THE CLOUD, I JUST WANT IT TO RAIN, riso clouds and rain"),
}
LEGACY_AI_GALLERY = [11915, 11919, 11920, 11918, 11922, 11923, 11924, 11916, 11917, 11925, 11926, 11921, 11927, 11928]


class ManifestShapeTests(unittest.TestCase):
    def test_manifest_is_valid_json_with_a_schema_version(self):
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["wordpress_base_url"], "https://kriskrug.co")

    def test_every_declared_id_is_a_positive_int(self):
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for section in ("categories", "media"):
            for key, entry in data[section].items():
                with self.subTest(section=section, key=key):
                    self.assertIsInstance(entry["id"], int)
                    self.assertGreater(entry["id"], 0)
        for key, group in data["media_groups"].items():
            for item in group["items"]:
                with self.subTest(group=key, item=item.get("id")):
                    self.assertIsInstance(item["id"], int)
                    self.assertGreater(item["id"], 0)
                    self.assertTrue(item["url"].startswith("https://kriskrug.co/"))
                    self.assertTrue(item["alt"].strip())

    def test_media_group_ids_are_unique(self):
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for key, group in data["media_groups"].items():
            ids = [item["id"] for item in group["items"]]
            with self.subTest(group=key):
                self.assertEqual(len(ids), len(set(ids)))


class DeclaredIdEquivalenceTests(unittest.TestCase):
    """The manifest must resolve to the exact pre-refactor literals."""

    def test_category_ids_match_the_literals_they_replaced(self):
        self.assertEqual(
            publish_common.category_id("ai-ethics-philosophy"), LEGACY_DC_PROTEST_CATEGORY_ID
        )
        self.assertEqual(
            publish_common.category_id("ai-ethics-philosophy"), LEGACY_YOU_CANT_DRINK_CATEGORY_ID
        )
        self.assertEqual(
            [
                publish_common.category_id("ai-ethics-philosophy"),
                publish_common.category_id("responsible-ai-policy"),
            ],
            LEGACY_KEEP_THE_MACHINE_CATEGORY_IDS,
        )

    def test_featured_media_id_matches_the_literal_it_replaced(self):
        self.assertEqual(
            publish_common.media_id("you-cant-drink-data-featured"),
            LEGACY_YOU_CANT_DRINK_FEATURED_ID,
        )

    def test_ai_protest_signs_group_reproduces_AI_SIGNS_and_AI_GALLERY(self):
        signs, order = publish_common.media_group_index("ai-protest-signs-2026-05")
        self.assertEqual(signs, LEGACY_AI_SIGNS)
        self.assertEqual(order, LEGACY_AI_GALLERY)

    def test_inbody_sign_keys_resolve_to_the_legacy_ids(self):
        """publish_you_cant_drink_data.py's INBODY_AI used to key on these raw IDs."""
        sign = publish_common.media_group_keys("ai-protest-signs-2026-05")
        self.assertEqual(
            [
                sign["we-are-the-training-data"],
                sign["water-the-servers-last"],
                sign["i-love-the-cloud-i-just-want-it-to-rain"],
            ],
            [11920, 11918, 11928],
        )

    def test_every_declared_key_matches_its_upload_filename_stem(self):
        """The key is the uploaded filename minus its ordering prefix; keep them in sync."""
        for item in publish_common.media_group("ai-protest-signs-2026-05"):
            stem = item["url"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
            with self.subTest(id=item["id"]):
                self.assertEqual(item["key"], stem.split("-", 1)[1])

    def test_derived_gallery_captions_are_unchanged(self):
        """AI_CAP is built off the declared alt text; pin the derivation."""
        signs, order = publish_common.media_group_index("ai-protest-signs-2026-05")
        self.assertEqual(
            {mid: signs[mid][1].split(",")[0] for mid in order},
            {mid: LEGACY_AI_SIGNS[mid][1].split(",")[0] for mid in LEGACY_AI_GALLERY},
        )


class LookupValidationTests(unittest.TestCase):
    def test_unknown_category_key_aborts_with_known_keys_listed(self):
        with self.assertRaises(SystemExit) as ctx:
            publish_common.category_id("no-such-category")
        self.assertIn("ai-ethics-philosophy", str(ctx.exception))

    def test_unknown_media_key_aborts(self):
        with self.assertRaises(SystemExit):
            publish_common.media_id("no-such-media")

    def test_unknown_media_group_aborts(self):
        with self.assertRaises(SystemExit):
            publish_common.media_group("no-such-group")

    def test_non_positive_id_aborts(self):
        bad = {"categories": {"broken": {"id": 0}}}
        with self.assertRaises(SystemExit):
            publish_common.category_id("broken", ids=bad)

    def test_media_group_entry_without_url_or_alt_aborts(self):
        bad = {"media_groups": {"g": {"items": [{"id": 5, "url": "", "alt": "a"}]}}}
        with self.assertRaises(SystemExit):
            publish_common.media_group("g", ids=bad)

    def test_media_group_keys_rejects_a_missing_or_duplicate_key(self):
        missing = {"media_groups": {"g": {"items": [{"id": 5, "url": "u", "alt": "a"}]}}}
        with self.assertRaises(SystemExit):
            publish_common.media_group_keys("g", ids=missing)
        dupe = {
            "media_groups": {
                "g": {
                    "items": [
                        {"key": "k", "id": 5, "url": "u", "alt": "a"},
                        {"key": "k", "id": 6, "url": "u", "alt": "a"},
                    ]
                }
            }
        }
        with self.assertRaises(SystemExit):
            publish_common.media_group_keys("g", ids=dupe)

    def test_loader_reads_an_explicit_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ids.json"
            path.write_text(json.dumps({"categories": {"x": {"id": 7}}}), encoding="utf-8")
            data = publish_common.load_publisher_ids(path)
        self.assertEqual(publish_common.category_id("x", ids=data), 7)


class ScriptsCarryNoBareIdsTests(unittest.TestCase):
    """Acceptance criterion: the prod IDs no longer live in the script sources."""

    SCRIPTS = (
        "publish_dc_protest_draft.py",
        "publish_you_cant_drink_data.py",
        "publish_keep_the_machine_strange.py",
        "publish_context_creators.py",
        "publish_proximity_game.py",
    )
    RETIRED_LITERALS = ("1678", "1754", "11976") + tuple(str(i) for i in LEGACY_AI_GALLERY)

    def test_no_publisher_script_hardcodes_a_declared_id(self):
        for name in self.SCRIPTS:
            source = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            for literal in self.RETIRED_LITERALS:
                with self.subTest(script=name, literal=literal):
                    self.assertNotIn(literal, source)


if __name__ == "__main__":
    unittest.main()
