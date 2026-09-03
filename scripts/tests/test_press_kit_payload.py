"""Source-chain contract tests for the Press Kit v2 payload (#881).

The press kit joins three reviewed sources to one WordPress payload:

    copy-deck.md          producer copy            (#877)
    assets/manifest.json  rights-aware asset list  (#878)
    brand-reference.json  Aurora-derived tokens    (#879)

These tests guard the joins that could publish a wrong or unauthorized
asset. Each contract is a function over in-memory data so the mutation
checks in #881 can feed it a deliberately broken copy and prove the
contract rejects it, rather than only proving the current files pass.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/source-packs/content-architecture-2026"
PRESS_KIT = PACK / "press-kit"
PAYLOAD = PACK / "wp-payloads/podcast-guesting-page-epk.html"
PAGE_MAP = PACK / "wp-payloads/page-map.json"

OWNED_DOWNLOAD_HOST = "https://kriskrug.co/wp-content"

# A download must never point at anything but a cleared, owned file.
UNSAFE_URL_MARKERS = (
    "file://",
    "localhost",
    "127.0.0.1",
    "notion.so",
    "notionusercontent",
    ".local/",
    "/Users/",
    "staging.",
    "tmp.",
)

RETIRED_CLASS_PREFIXES = ("kk-", "kkp-", "kkx-")


def download_links(html):
    """Every asset download the payload offers."""
    return set(re.findall(r'href="(https?://[^"]*/wp-content/[^"]+)"', html))


def approved_assets(manifest):
    return {
        asset["public_download_url"]: asset
        for asset in manifest["assets"]
        if asset["status"] == "approved" and asset.get("public_download_url")
    }


def unapproved_urls(manifest):
    urls = set()
    for asset in manifest["assets"]:
        if asset["status"] == "approved":
            continue
        for key in ("public_download_url", "public_source_url"):
            if asset.get(key):
                urls.add(asset[key])
    return urls


def check_downloads_are_approved(html, manifest):
    """Every download maps to one approved entry; nothing else is linked."""
    problems = []
    approved = approved_assets(manifest)
    blocked = unapproved_urls(manifest)
    for link in sorted(download_links(html)):
        if link in blocked:
            problems.append(f"links a non-approved asset: {link}")
        elif link not in approved:
            problems.append(f"download is not in the approved manifest: {link}")
    return problems


def check_approved_records_are_complete(manifest):
    """An approved record must carry enough to publish it safely."""
    problems = []
    for asset in manifest["assets"]:
        if asset["status"] != "approved":
            continue
        key = asset.get("key", "<unkeyed>")
        for field in ("credit", "reuse_terms", "rights_evidence", "alt"):
            if not asset.get(field):
                problems.append(f"{key} approved without {field}")
        if not asset.get("public_download_url"):
            problems.append(f"{key} approved without a public download URL")
        if not (asset.get("width") and asset.get("height")):
            problems.append(f"{key} approved without dimensions")
    return problems


def check_credits_are_published(html, manifest):
    """A cleared photo may not appear without its creator credit."""
    problems = []
    for asset in approved_assets(manifest).values():
        credit = asset["credit"].rstrip(".")
        if credit not in html:
            problems.append(f"{asset['key']} download published without: {credit}")
    return problems


def brand_values(brand):
    """Every token value that carries provenance, by value."""
    found = {}

    def walk(node):
        if isinstance(node, dict):
            value = node.get("value")
            if isinstance(value, str) and node.get("provenance"):
                found.setdefault(value.lower(), node)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(brand)
    return found


def check_brand_roles_traceable(html, brand):
    """No colour or type role may be invented in the payload."""
    problems = []
    known = brand_values(brand)
    for colour in sorted(set(re.findall(r"#[0-9a-fA-F]{6}", html))):
        if colour.lower() not in known:
            problems.append(f"colour not traceable to the brand reference: {colour}")
    for family in ("Space Grotesk", "DM Sans", "JetBrains Mono"):
        # `known` is keyed by the lowercased token value.
        if family in html and not any(family.lower() in value for value in known):
            problems.append(f"type family not traceable: {family}")
    return problems


def check_body_safety(html):
    """Body-only payload rules that keep the page publishable."""
    problems = []
    for fragment in ("<h1", "</h1>", "<style", "<script", "javascript:"):
        if fragment in html:
            problems.append(f"forbidden fragment: {fragment}")
    if re.search(r"\sstyle=", html):
        problems.append("inline style attribute")
    for marker in UNSAFE_URL_MARKERS:
        if marker in html:
            problems.append(f"private, temporary, or local URL: {marker}")
    for class_attr in re.findall(r'class="([^"]+)"', html):
        bad = [t for t in class_attr.split() if t.startswith(RETIRED_CLASS_PREFIXES)]
        if bad:
            problems.append(f"retired page classes: {bad}")
    for link in download_links(html):
        if not link.startswith(OWNED_DOWNLOAD_HOST):
            problems.append(f"third-party hotlinked download: {link}")
    return problems


def check_markers(html, page):
    return [m for m in page["markers"] if m not in html]


def check_booking_ctas(html):
    """The booking path must survive ahead of, and after, the brand material."""
    problems = []
    contact_ctas = [
        m.start() for m in re.finditer(r'class="aurora-button" href="/contact/"', html)
    ]
    if len(contact_ctas) < 2:
        problems.append("expected a primary and a final booking CTA")
        return problems
    brand_at = html.find("Brand at a glance")
    if brand_at != -1:
        if contact_ctas[0] > brand_at:
            problems.append("primary booking CTA falls after the brand section")
        if contact_ctas[-1] < brand_at:
            problems.append("no booking CTA after the brand section")
    return problems


def check_copy_deck(text):
    """Required sections, and #735 still visibly unresolved."""
    problems = []
    for heading in (
        "## Identity, pronunciation, location, and availability",
        "## Formats",
        "## Topics and interview angles",
        "## Voice and mood",
        "## Public booking route and canonical links",
        "## Sources",
    ):
        if heading not in text:
            problems.append(f"copy deck missing section: {heading}")
    if "PENDING" not in text:
        problems.append("copy deck no longer marks any PENDING item")
    if "Still open" not in text:
        problems.append("copy deck no longer marks the open #735 choices")
    return problems


def check_payload_marks_open_735(html):
    """The payload must say which #735 choices it did not settle."""
    problems = []
    if "#735" not in html:
        problems.append("payload does not mark the unresolved #735 choices")
    if "PROPOSED" not in html:
        problems.append("payload does not record which copy is still PROPOSED")
    return problems


class PressKitSourceChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAYLOAD.read_text(encoding="utf-8")
        cls.manifest = json.loads(
            (PRESS_KIT / "assets/manifest.json").read_text(encoding="utf-8")
        )
        cls.brand = json.loads(
            (PRESS_KIT / "brand-reference.json").read_text(encoding="utf-8")
        )
        cls.copy_deck = (PRESS_KIT / "copy-deck.md").read_text(encoding="utf-8")
        cls.page = json.loads(PAGE_MAP.read_text(encoding="utf-8"))["podcast_epk"]

    # ---- the integrated source pack must satisfy every contract ----

    def test_every_download_maps_to_an_approved_asset(self):
        self.assertEqual([], check_downloads_are_approved(self.html, self.manifest))

    def test_approved_records_carry_rights_credit_alt_and_dimensions(self):
        self.assertEqual([], check_approved_records_are_complete(self.manifest))

    def test_every_published_download_carries_its_credit(self):
        self.assertEqual([], check_credits_are_published(self.html, self.manifest))

    def test_brand_roles_trace_to_the_generated_reference(self):
        self.assertEqual([], check_brand_roles_traceable(self.html, self.brand))

    def test_payload_is_body_only_and_public_safe(self):
        self.assertEqual([], check_body_safety(self.html))

    def test_payload_contains_required_page_map_markers(self):
        self.assertEqual([], check_markers(self.html, self.page))

    def test_booking_ctas_bracket_the_brand_material(self):
        self.assertEqual([], check_booking_ctas(self.html))

    def test_copy_deck_sections_exist_and_735_stays_marked(self):
        self.assertEqual([], check_copy_deck(self.copy_deck))

    def test_payload_marks_the_unresolved_735_choices(self):
        self.assertEqual([], check_payload_marks_open_735(self.html))

    def test_page_identity_is_unchanged(self):
        self.assertEqual(3609, self.page["id"])
        self.assertEqual("podcast-guesting-page-epk", self.page["slug"])

    # ---- and each contract must reject a broken source pack ----

    def test_demoting_an_approved_asset_rejects_its_download(self):
        broken = json.loads(json.dumps(self.manifest))
        demoted = next(a for a in broken["assets"] if a["status"] == "approved")
        demoted["status"] = "blocked-rights"
        problems = check_downloads_are_approved(self.html, broken)
        self.assertTrue(problems, "demoting an approved asset was not caught")
        self.assertIn(demoted["public_download_url"], " ".join(problems))

    def test_approved_asset_missing_its_credit_is_rejected(self):
        broken = json.loads(json.dumps(self.manifest))
        next(a for a in broken["assets"] if a["status"] == "approved")["credit"] = ""
        self.assertTrue(check_approved_records_are_complete(broken))

    def test_uncredited_download_is_rejected(self):
        asset = next(iter(approved_assets(self.manifest).values()))
        stripped = self.html.replace(asset["credit"].rstrip("."), "")
        self.assertTrue(check_credits_are_published(stripped, self.manifest))

    def test_renaming_a_generated_token_rejects_the_payload_role(self):
        drifted = json.loads(json.dumps(self.brand))

        def rename(node):
            if isinstance(node, dict):
                value = node.get("value")
                if isinstance(value, str) and value.lower() == "#9a2f14":
                    node["value"] = "#000001"
                for child in node.values():
                    rename(child)
            elif isinstance(node, list):
                for child in node:
                    rename(child)

        rename(drifted)
        problems = check_brand_roles_traceable(self.html, drifted)
        self.assertTrue(problems, "brand token drift was not caught")
        self.assertIn("#9a2f14", " ".join(problems))

    def test_token_without_provenance_does_not_satisfy_a_payload_role(self):
        unsourced = {"colors": [{"id": "x", "name": "X", "value": "#9a2f14"}]}
        self.assertTrue(check_brand_roles_traceable(self.html, unsourced))

    def test_inline_style_is_rejected(self):
        self.assertTrue(check_body_safety('<p style="color:red">x</p>'))

    def test_local_filesystem_url_is_rejected(self):
        self.assertTrue(check_body_safety('<a href="file:///Users/kk/x.jpg">x</a>'))

    def test_third_party_hotlinked_download_is_rejected(self):
        html = '<a href="https://example.com/wp-content/uploads/x.jpg">x</a>'
        self.assertTrue(check_body_safety(html))

    def test_heading_and_script_are_rejected(self):
        self.assertTrue(check_body_safety("<h1>no</h1>"))
        self.assertTrue(check_body_safety("<script>alert(1)</script>"))

    def test_retired_class_prefix_is_rejected(self):
        self.assertTrue(check_body_safety('<div class="kk-hero">x</div>'))

    def test_missing_marker_is_rejected(self):
        self.assertTrue(check_markers("nothing here", self.page))

    def test_dropping_the_final_cta_is_rejected(self):
        primary_only = self.html[: self.html.find("Brand at a glance")]
        self.assertTrue(check_booking_ctas(primary_only))

    def test_copy_deck_losing_its_735_markers_is_rejected(self):
        laundered = self.copy_deck.replace("PENDING", "DONE").replace(
            "Still open", "Settled"
        )
        self.assertTrue(check_copy_deck(laundered))

    def test_payload_dropping_its_735_note_is_rejected(self):
        self.assertTrue(check_payload_marks_open_735("<p>no note</p>"))


if __name__ == "__main__":
    unittest.main()
