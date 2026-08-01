import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PAYLOAD_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "publications.html"
)
META_PATH = PAYLOAD_PATH.parent / "page-meta.json"
ASSETS_DIR = REPO_ROOT / "content" / "source-packs" / "keynotes-2026" / "assets"
MEDIA_MANIFEST_PATH = ASSETS_DIR / "publications-press-media.md"
PRESS_MEDIA_MANIFEST_JSON = ASSETS_DIR / "press-media-manifest.json"
DESIGN_SPEC_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "PUBLICATIONS-DESIGN-SPEC.md"
)
PRESS_IMAGE_NAME_RE = re.compile(
    r"^press-\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.jpg$",
    re.IGNORECASE,
)
PRESS_IMAGE_NAME_V2_RE = re.compile(
    r"^press-\d{4}-\d{2}-\d{2}-[a-z0-9-]+-v2\.jpg$",
    re.IGNORECASE,
)

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from capture_press_media import load_manifest  # noqa: E402

PUBLISH_GATE_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "verification"
    / "PUBLICATIONS-EDITORIAL-PUBLISH-GATE-2026-07-24.md"
)
GAP_REPORT_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "verification"
    / "PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md"
)

FORBIDDEN_SKIN_MARKERS = (
    "kk-publications",
    "#00e5ff",
    "#ff6a6a",
    "--press-night",
)


def manifest_lookups(manifest: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    """Return (by_key, by_legacy_file) maps for manifest entries."""
    by_key: dict[str, dict] = {}
    by_legacy: dict[str, dict] = {}
    for entry in manifest["entries"]:
        by_key[entry["key"]] = entry
        legacy = entry.get("legacy_file")
        if legacy:
            by_legacy[legacy] = entry
    return by_key, by_legacy


def ratio_matches(
    width: str | int, height: str | int, ratio: str, tolerance: float = 0.02
) -> bool:
    w, h = int(width), int(height)
    if ratio == "16:10":
        expected = 16 / 10
    elif ratio == "16:9":
        expected = 16 / 9
    elif ratio == "1:1":
        expected = 1.0
    else:
        return True
    actual = w / h
    return abs(actual - expected) <= tolerance


class LinkAndImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.external_links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href", "").startswith("http"):
            self.external_links.append(values)
        if tag == "img":
            self.images.append(values)


class PublicationsEditorialPayloadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = PAYLOAD_PATH.read_text(encoding="utf-8")
        cls.parser = LinkAndImageParser()
        cls.parser.feed(cls.payload)

    def test_complete_reverse_chronological_inventory(self):
        self.assertEqual(3, self.payload.count('<a class="kk-press-feature'))
        self.assertEqual(20, self.payload.count('<article class="kk-press-entry'))
        self.assertEqual(25, self.payload.count("<li><time"))

        dates = re.findall(r'datetime="(\d{4}-\d{2}-\d{2})"', self.payload)
        self.assertEqual(48, len(dates))
        self.assertEqual(sorted(dates, reverse=True), dates)

    def test_structure_and_reciprocal_links(self):
        self.assertIn('class="kk-press-featured"', self.payload)
        self.assertIn('class="kk-press-feed"', self.payload)
        self.assertIn('class="kk-press-legacy"', self.payload)
        self.assertIn('class="kk-press-board"', self.payload)
        self.assertIn('class="kk-press-outlets"', self.payload)
        self.assertIn('class="kk-press-pull"', self.payload)
        self.assertIn("/podcast-guesting-page-epk/", self.payload)
        self.assertIn(
            "/2026/07/02/ai-media-appearances-podcast-guesting/", self.payload
        )
        self.assertIn("Media Appearances", self.payload)
        self.assertIn("vanmag.com/city/power-50/", self.payload)

    def test_forbids_dark_neon_ghost_skin(self):
        lowered = self.payload.lower()
        for marker in FORBIDDEN_SKIN_MARKERS:
            self.assertNotIn(marker.lower(), lowered)
        self.assertNotRegex(self.payload, r"--press-night\s*:")
        self.assertNotIn("background:var(--press-night)", self.payload)
        self.assertNotIn("background:#0d1014", self.payload)

    def test_markup_and_voice_guards(self):
        self.assertNotRegex(self.payload, r"<h1\b")
        self.assertNotIn("—", self.payload)
        self.assertRegex(self.payload, r"@media\s*\(max-width:\s*620px\)")
        self.assertRegex(self.payload, r"@media\s*\(prefers-reduced-motion:\s*reduce\)")
        self.assertIn("Space Grotesk", self.payload)
        self.assertIn("DM Sans", self.payload)
        self.assertIn("--aurora-paper", self.payload)
        self.assertIn("--aurora-ink", self.payload)
        self.assertIn("--aurora-signal", self.payload)

    def test_images_have_dimensions_and_alt_text(self):
        keys = [img.get("data-media-key") for img in self.parser.images]
        self.assertGreaterEqual(len(self.parser.images), 16)
        self.assertGreaterEqual(len(set(keys)), 16)
        for image in self.parser.images:
            self.assertTrue(image.get("alt"))
            self.assertTrue(image.get("width"))
            self.assertTrue(image.get("height"))
            self.assertTrue(image.get("src", "").startswith("../assets/"))
            self.assertEqual(Path(image["src"]).name, image.get("data-media-key"))
            self.assertTrue((PAYLOAD_PATH.parent / image["src"]).resolve().exists())

    def test_external_links_open_safely(self):
        self.assertGreaterEqual(len(self.parser.external_links), 47)
        for link in self.parser.external_links:
            self.assertEqual("_blank", link.get("target"))
            self.assertEqual("noopener noreferrer", link.get("rel"))

    def test_seo_metadata_and_media_manifest(self):
        page_meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        publications = next(
            page for page in page_meta["pages"] if page["slug"] == "publications"
        )
        self.assertEqual(
            "Press, Interviews & Media Coverage | Kris Krüg",
            publications["meta"]["jetpack_seo_html_title"],
        )
        self.assertTrue(MEDIA_MANIFEST_PATH.exists())
        manifest = MEDIA_MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn("Excluded from the publication set", manifest)
        self.assertIn("explicit media approval", manifest)
        self.assertIn("superseded", manifest.lower())
        gate = PUBLISH_GATE_PATH.read_text(encoding="utf-8")
        self.assertIn("WordPress page ID: `1895`", gate)
        self.assertRegex(gate, r"authenticated\s+`context=edit` snapshot")
        self.assertIn("Do not delete uploaded media during emergency rollback", gate)
        self.assertIn("superseded", gate.lower())
        self.assertIn("Aurora paper", gate)
        self.assertTrue(GAP_REPORT_PATH.exists())
        gap = GAP_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Power 50", gap)
        self.assertIn("cyan", gap.lower())

    def test_design_spec_and_json_manifest_exist(self):
        self.assertTrue(DESIGN_SPEC_PATH.exists())
        spec = DESIGN_SPEC_PATH.read_text(encoding="utf-8")
        self.assertIn("## Image tiers", spec)
        self.assertIn("1200 × 750", spec)
        self.assertIn("contact-sheet.html", spec)
        self.assertTrue(PRESS_MEDIA_MANIFEST_JSON.exists())
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        self.assertGreaterEqual(len(manifest["entries"]), 16)
        self.assertIn("feature-lead", manifest["slots"])
        self.assertIn("podcast", manifest["slots"])

    def test_manifest_covers_all_legacy_press_assets(self):
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        legacy_files = sorted(
            p.name
            for p in ASSETS_DIR.glob("press-*.jpg")
            if not p.name.endswith("-v2.jpg")
        )
        manifest_legacy = {
            e["legacy_file"] for e in manifest["entries"] if e.get("legacy_file")
        }
        self.assertGreaterEqual(len(legacy_files), 16)
        self.assertEqual(set(legacy_files), manifest_legacy)

    def test_manifest_target_keys_use_v2_naming(self):
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        for entry in manifest["entries"]:
            self.assertRegex(
                entry["key"],
                PRESS_IMAGE_NAME_V2_RE,
                msg=f"manifest key must be -v2 target: {entry['key']}",
            )
            self.assertNotEqual(entry["key"], entry.get("legacy_file"))

    def test_manifest_slot_dimensions_are_internally_consistent(self):
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        slots = manifest["slots"]
        for entry in manifest["entries"]:
            slot_def = slots[entry["slot"]]
            self.assertEqual(entry["width"], slot_def["width"])
            self.assertEqual(entry["height"], slot_def["height"])
            self.assertEqual(entry["ratio"], slot_def["ratio"])
            self.assertTrue(
                ratio_matches(entry["width"], entry["height"], entry["ratio"])
            )

    def test_payload_images_have_manifest_entries(self):
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        _, by_legacy = manifest_lookups(manifest)
        for image in self.parser.images:
            media_key = image.get("data-media-key")
            self.assertTrue(media_key, "every img must have data-media-key")
            self.assertIn(
                media_key,
                by_legacy,
                msg=f"payload img {media_key!r} must map to manifest legacy_file",
            )

    def test_payload_image_dimensions_match_manifest_targets(self):
        """Spec gate: width/height attrs must match manifest target dimensions."""
        manifest = load_manifest(PRESS_MEDIA_MANIFEST_JSON)
        _, by_legacy = manifest_lookups(manifest)
        for image in self.parser.images:
            media_key = image["data-media-key"]
            entry = by_legacy[media_key]
            self.assertEqual(
                str(entry["width"]),
                str(image.get("width")),
                msg=f"{media_key}: width must be {entry['width']} per manifest",
            )
            self.assertEqual(
                str(entry["height"]),
                str(image.get("height")),
                msg=f"{media_key}: height must be {entry['height']} per manifest",
            )
            self.assertTrue(
                ratio_matches(image["width"], image["height"], entry["ratio"]),
                msg=f"{media_key}: attrs must match ratio {entry['ratio']}",
            )

    def test_payload_press_image_naming_convention(self):
        for image in self.parser.images:
            media_key = image.get("data-media-key", "")
            if not media_key.startswith("press-"):
                continue
            self.assertRegex(
                media_key,
                PRESS_IMAGE_NAME_RE,
                msg=f"press image naming must be press-YYYY-MM-DD-*: {media_key}",
            )
            date_part = media_key.split("-")[1:4]
            self.assertEqual(
                len(date_part), 3, msg=f"date segment missing in {media_key}"
            )
            year, month, day = date_part
            self.assertEqual(len(year), 4)
            self.assertEqual(len(month), 2)
            self.assertEqual(len(day), 2)


if __name__ == "__main__":
    unittest.main()
