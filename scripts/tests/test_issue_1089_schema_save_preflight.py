import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPLOYED = ROOT / "fixes/schema-snippets-deployed.php"
PACKET = ROOT / "fixes/issue-1089-schema-save-preflight-2026-09-29.md"
MANIFEST = ROOT / "fixes/issue-1089-schema-save-preflight-2026-09-29.json"
HANDOFF_316 = ROOT / "fixes/issue-316-schema-identity-handoff-2026-07-13.md"
HANDOFF_641 = ROOT / "fixes/issue-641-speaking-video-schema-handoff-2026-08-27.md"
README = ROOT / "fixes/README.md"
RELEASE = ROOT / "docs/current-state/reports/schema-1089-verification-2026-10-25.json"

PERSON_ID = "https://kriskrug.co/#person"
ORG_ID = "https://bc-ai.ca/#organization"
APPROVED_SAME_AS = [
    "https://twitter.com/kriskrug",
    "https://x.com/kriskrug",
    "https://www.instagram.com/kriskrug/",
    "https://www.linkedin.com/in/kriskrug/",
    "https://www.youtube.com/kriskrug",
    "https://www.flickr.com/photos/kk/",
]
PREPARED_X = [
    "https://twitter.com/kriskrug",
    "https://x.com/kriskrug",
]
APPROVAL_COMMENT = (
    "https://github.com/WalksWithASwagger/kriskrug-wp/issues/1089"
    "#issuecomment-5877883436"
)
APPROVAL_TABLE_HEADING = "## Approval state (JSON must match)"
FORBIDDEN_WHEN_RECORDED_APPROVALS = (
    r"recommended, not approved",
    r"Default recommendation \(not approval\)",
    r"Pending KK\. Do not guess",
    r"Leave X out of the approved",
    r"X left pending",
    r"omits(?: the two)? X/Twitter",
    r"(?i)\bundecided\b",
)


def parse_markdown_approval_state(packet: str) -> dict[str, dict[str, object]]:
    heading_at = packet.find(APPROVAL_TABLE_HEADING)
    if heading_at < 0:
        raise AssertionError("Markdown is missing the Approval state table")
    table_block = packet[heading_at:]
    rows: dict[str, dict[str, object]] = {}
    for line in table_block.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"key", "---"} or set(cells[0]) == {"-"}:
            continue
        key, approved, source = cells
        if approved not in {"true", "false"}:
            raise AssertionError(f"approval table approved cell must be true/false: {line}")
        rows[key] = {"approved": approved == "true", "source": source}
    if not rows:
        raise AssertionError("Markdown Approval state table has no data rows")
    return rows


def array_constant(source: str, key: str) -> list[str]:
    match = re.search(
        rf"'{re.escape(key)}'\s*=>\s*array\((.*?)\),",
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing array schema constant: {key}")
    return re.findall(r"'([^']*)'", match.group(1))


def walk_types(node, found: list[str]) -> None:
    if isinstance(node, dict):
        type_value = node.get("@type")
        if isinstance(type_value, str):
            found.append(type_value)
        elif isinstance(type_value, list):
            found.extend(str(item) for item in type_value)
        for value in node.values():
            walk_types(value, found)
    elif isinstance(node, list):
        for item in node:
            walk_types(item, found)


class Issue1089SchemaSavePreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.packet = PACKET.read_text(encoding="utf-8")
        cls.deployed = DEPLOYED.read_text(encoding="utf-8")

    def test_manifest_json_is_valid_and_secret_free(self):
        self.assertEqual(1, self.manifest["schema_version"])
        self.assertEqual(1104, self.manifest["issue"])
        self.assertEqual(1089, self.manifest["parent_issue"])
        self.assertFalse(self.manifest["live_wordpress_write_performed"])
        self.assertFalse(self.manifest["live_code_snippet_write_performed"])
        serialized = json.dumps(self.manifest).lower()
        for marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "oauth",
        ):
            self.assertNotIn(marker, serialized)

    def test_historical_candidate_and_current_runtime_match_release(self):
        release = json.loads(RELEASE.read_text(encoding="utf-8"))
        self.assertEqual(
            self.manifest["candidate"]["sha256"], release["approved_file_sha256"]
        )
        self.assertEqual(
            self.manifest["candidate"]["byte_length"],
            release["approved_file_bytes"],
        )
        runtime = self.deployed[self.deployed.index("function kk_schema_constants()"):]
        self.assertEqual(
            release["runtime_sha256"], hashlib.sha256(runtime.encode()).hexdigest()
        )
        self.assertTrue(self.manifest["candidate"]["prepared_not_live"])
        self.assertEqual(5, self.manifest["candidate"]["expected_snippet_id"])

    def test_option_a_is_approved_2026_09_28(self):
        option_a = self.manifest["option_a"]
        self.assertTrue(option_a["recommended"])
        self.assertTrue(option_a["approved"])
        self.assertFalse(option_a["awaits_approval"])
        self.assertEqual("2026-09-28", option_a["approved_on"])
        self.assertEqual(APPROVAL_COMMENT, option_a["source"])
        self.assertIn("Option A — approved 2026-09-28", self.packet)
        self.assertIn(APPROVAL_COMMENT, self.packet)
        self.assertNotIn("recommended, not approved", self.packet)

    def test_one_person_id_and_live_bc_ai_organization_id(self):
        self.assertEqual(PERSON_ID, self.manifest["identity"]["person_id"])
        self.assertEqual(ORG_ID, self.manifest["bc_ai_organization"]["id"])
        self.assertIn(f"'id' => '{ORG_ID}'", self.deployed)
        self.assertIn("$c['site_url'] . '/#person'", self.deployed)
        self.assertIn(ORG_ID, self.packet)
        self.assertIn(PERSON_ID, self.packet)
        person = self.manifest["review_person"]
        self.assertEqual(PERSON_ID, person["@id"])
        self.assertEqual(ORG_ID, person["worksFor"][0]["@id"])
        self.assertEqual(
            "BC + AI Ecosystem Association",
            person["worksFor"][0]["name"],
        )

    def test_approved_same_as_includes_prepared_x(self):
        self.assertEqual(APPROVED_SAME_AS, self.manifest["same_as"]["approved"])
        self.assertEqual(PREPARED_X, self.manifest["same_as"]["prepared_x"])
        self.assertTrue(self.manifest["same_as"]["prepared_x_approved"])
        self.assertEqual(APPROVAL_COMMENT, self.manifest["same_as"]["prepared_x_source"])
        self.assertTrue(self.manifest["same_as"]["candidate_file_still_contains_prepared_x"])
        self.assertFalse(self.manifest["same_as"]["packet_changed_php_payload"])
        self.assertEqual(APPROVED_SAME_AS, self.manifest["review_person"]["sameAs"])
        for page in ("homepage", "speaking", "about", "article"):
            person = next(
                node
                for node in self.manifest["review_jsonld"][page]
                if node["@type"] == "Person"
            )
            self.assertEqual(APPROVED_SAME_AS, person["sameAs"])
        for url in PREPARED_X:
            self.assertIn(url, self.manifest["review_person"]["sameAs"])
            self.assertIn(url, array_constant(self.deployed, "same_as"))
        for url in APPROVED_SAME_AS:
            self.assertIn(url, array_constant(self.deployed, "same_as"))
        self.assertIn("Approved as prepared: keep `https://x.com/kriskrug`", self.packet)
        self.assertIn("twitter.com/feelmoreplants", self.packet)
        youtube = self.manifest["same_as"]["pending_youtube"]
        self.assertEqual("keep, swap, or both", youtube["decision"])
        self.assertTrue(youtube["pending_kk"])
        self.assertTrue(youtube["approved_set_unchanged"])
        self.assertTrue(youtube["adding_alternate_is_new_profile"])
        self.assertEqual("https://www.youtube.com/kriskrug", youtube["keep"])
        self.assertEqual("@kriskrugdotcom", youtube["keep_resolves_to"])
        self.assertEqual(
            "https://www.youtube.com/kriskrug10000",
            youtube["swap_or_add"],
        )
        self.assertEqual("@feelmoreplants", youtube["swap_or_add_resolves_to"])
        self.assertEqual("-c7mgY2aSgM", youtube["swap_or_add_hosts_speaking_video"])
        self.assertNotIn(
            "https://www.youtube.com/kriskrug10000",
            self.manifest["same_as"]["approved"],
        )
        self.assertNotIn(
            "https://www.youtube.com/kriskrug10000",
            self.manifest["review_person"]["sameAs"],
        )
        self.assertIn("## Decision 3 — YouTube `sameAs` (TODO)", self.packet)
        self.assertIn("Keep, swap, or both", self.packet)
        self.assertIn("https://www.youtube.com/kriskrug10000", self.packet)
        self.assertIn("@kriskrugdotcom", self.packet)
        self.assertIn("is a **new** `sameAs`", self.packet)
        self.assertIn("not treat this later YouTube choice as covered", self.packet)

    def test_markdown_and_json_approval_states_agree(self):
        markdown_state = parse_markdown_approval_state(self.packet)
        json_state = {
            key: {"approved": value["approved"], "source": value["source"]}
            for key, value in self.manifest["approval_state"].items()
        }
        self.assertEqual(set(markdown_state), set(json_state))
        self.assertEqual(markdown_state, json_state)

        approval = self.manifest["approval_state"]
        self.assertEqual(
            approval["option_a_person_plus_videoobjects"]["approved"],
            self.manifest["option_a"]["approved"],
        )
        self.assertEqual(
            approval["prepared_x_identity"]["approved"],
            self.manifest["same_as"]["prepared_x_approved"],
        )
        self.assertEqual(
            approval["youtube_same_as_keep_swap_both"]["approved"],
            not self.manifest["same_as"]["pending_youtube"]["pending_kk"],
        )
        self.assertEqual(
            approval["live_wordpress_save"]["approved"],
            self.manifest["live_wordpress_write_performed"],
        )
        self.assertTrue(approval["option_a_person_plus_videoobjects"]["approved"])
        self.assertTrue(approval["prepared_x_identity"]["approved"])
        self.assertFalse(approval["youtube_same_as_keep_swap_both"]["approved"])
        self.assertFalse(approval["live_wordpress_save"]["approved"])
        self.assertEqual(
            APPROVAL_COMMENT,
            approval["option_a_person_plus_videoobjects"]["source"],
        )
        self.assertEqual(APPROVAL_COMMENT, approval["prepared_x_identity"]["source"])

        for pattern in FORBIDDEN_WHEN_RECORDED_APPROVALS:
            self.assertNotRegex(self.packet, pattern)
        self.assertNotIn("pending_x_twitter", self.manifest["same_as"])
        self.assertIn("x.com/kriskrug", json.dumps(self.manifest["review_jsonld"]))

    def test_website_homepage_only_and_name_preserved(self):
        self.assertEqual("Kris Krug", self.manifest["identity"]["website_name"])
        self.assertIn("'site_name'            => 'Kris Krug'", self.deployed)
        self.assertIn("if (!is_front_page() && !is_home()) return;", self.deployed)
        homepage_types = [node["@type"] for node in self.manifest["review_jsonld"]["homepage"]]
        self.assertEqual(["Person", "WebSite"], homepage_types)
        self.assertEqual(
            "Kris Krug",
            self.manifest["review_jsonld"]["homepage"][1]["name"],
        )
        for page in ("speaking", "about", "article"):
            types = [node["@type"] for node in self.manifest["review_jsonld"][page]]
            self.assertNotIn("WebSite", types)

    def test_video_objects_only_on_speaking_and_have_required_fields(self):
        speaking = self.manifest["review_jsonld"]["speaking"]
        videos = [node for node in speaking if node["@type"] == "VideoObject"]
        self.assertEqual(2, len(videos))
        required = {"name", "thumbnailUrl", "uploadDate"}
        for video in videos:
            self.assertTrue(required.issubset(video))
            self.assertTrue("embedUrl" in video or "contentUrl" in video)
            self.assertEqual({"@id": PERSON_ID}, video["about"])
            self.assertNotIn("Event", json.dumps(video))
        for page in ("homepage", "about", "article"):
            types = [node["@type"] for node in self.manifest["review_jsonld"][page]]
            self.assertNotIn("VideoObject", types)
        self.assertIn("if (!is_page(1887)) return;", self.deployed)

    def test_no_event_nodes_and_no_futureproof_festival_id(self):
        self.assertFalse(self.manifest["exclusions"]["event_nodes"])
        self.assertIsNone(self.manifest["exclusions"]["futureproof_festival_id"])
        self.assertFalse(self.manifest["exclusions"]["futureproof_works_for_has_id"])
        self.assertEqual(
            "https://www.futureproof.website/",
            self.manifest["exclusions"]["futureproof_works_for_url"],
        )
        self.assertNotIn("'@type'         => 'Event'", self.deployed)
        self.assertNotIn("futureproof.website/#", self.deployed)
        self.assertNotIn("#festival", self.deployed)
        types: list[str] = []
        walk_types(self.manifest["review_jsonld"], types)
        self.assertNotIn("Event", types)
        festival = self.manifest["review_person"]["worksFor"][2]
        self.assertNotIn("@id", festival)
        self.assertEqual("https://www.futureproof.website/", festival["url"])

    def test_article_references_person_id_instead_of_inlining(self):
        article = next(
            node
            for node in self.manifest["review_jsonld"]["article"]
            if node["@type"] == "BlogPosting"
        )
        self.assertEqual({"@id": PERSON_ID}, article["author"])
        self.assertEqual({"@id": PERSON_ID}, article["publisher"])
        self.assertNotEqual("Person", article["author"].get("@type"))
        live_article = self.manifest["live_readback"]["routes"][2]
        self.assertEqual({"@id": PERSON_ID}, live_article["author"])
        self.assertEqual({"@id": PERSON_ID}, live_article["publisher"])

    def test_packet_records_readbacks_decisions_and_pending_snapshot(self):
        self.assertIn("2026-09-30T05:30:50.196067-07:00", self.packet)
        self.assertIn("Authenticated snippet 5 body/scope snapshot", self.packet)
        self.assertIn("Pending KK", self.packet)
        self.assertIn("https://validator.schema.org/", self.packet)
        self.assertIn("Do **not** treat Google Rich Results Test", self.packet)
        self.assertIn("Detect unexpected concurrent snippet 5 edits", self.packet)
        self.assertIn("concurrent snippet-5 hash drift", " ".join(self.manifest["rollback"]))
        self.assertEqual(
            "pending-kk",
            self.manifest["live_readback"]["authenticated_snippet_snapshot"],
        )
        self.assertEqual("pending", self.manifest["validator"]["receipts"])
        self.assertEqual(404, self.manifest["live_readback"]["footer_twitter_http_status"])
        self.assertIn("#1024", self.packet)
        self.assertIn("Decisions 1 and 2 are already approved", self.packet)

    def test_existing_handoffs_and_index_point_here(self):
        pointer = "issue-1089-schema-save-preflight-2026-09-29.md"
        self.assertIn(pointer, HANDOFF_316.read_text(encoding="utf-8"))
        self.assertIn(pointer, HANDOFF_641.read_text(encoding="utf-8"))
        self.assertIn(pointer, README.read_text(encoding="utf-8"))
        self.assertIn("No live WordPress write", self.packet)


if __name__ == "__main__":
    unittest.main()
