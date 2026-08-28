import json
import re
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_SOURCE = ROOT / "fixes/schema-snippets-deployed.php"
MANIFEST = ROOT / "fixes/issue-641-speaking-video-schema-handoff-2026-08-27.json"
HANDOFF = ROOT / "fixes/issue-641-speaking-video-schema-handoff-2026-08-27.md"
PAYLOAD = ROOT / "content/drafts/2026-07-26-speaking-page/payload-body.html"
EVENTS_PLAN = ROOT / "content/drafts/events-internal-links/PLAN.md"
TESTIMONIALS_LIVE = (
    ROOT
    / "content/drafts/2026-08-01-testimonials-overhaul/live-content-rendered-2026-08-16.html"
)
SCRIPT_PATTERN = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL,
)
VIDEO_KEYS = {
    "@context",
    "@type",
    "@id",
    "name",
    "description",
    "thumbnailUrl",
    "uploadDate",
    "duration",
    "embedUrl",
    "about",
}


def render_speaking_schema(page_id: int) -> dict:
    schema_path = json.dumps(str(SCHEMA_SOURCE))
    harness = textwrap.dedent(
        f"""
        <?php
        $GLOBALS['kk_test_hooks'] = array();
        $GLOBALS['kk_test_page_id'] = {page_id};

        function add_action($hook, $callback, $priority = 10, $accepted_args = 1) {{
            $GLOBALS['kk_test_hooks'][] = compact('hook', 'callback', 'priority', 'accepted_args');
        }}
        function is_page($page = '') {{
            return (int) $page === $GLOBALS['kk_test_page_id'];
        }}
        function wp_json_encode($value, $flags = 0) {{
            return json_encode($value, $flags | JSON_THROW_ON_ERROR);
        }}

        require {schema_path};

        $hooks = array_values(array_filter(
            $GLOBALS['kk_test_hooks'],
            fn($row) => $row['hook'] === 'wp_head'
                && $row['callback'] === 'kk_schema_speaking_videos'
        ));

        ob_start();
        foreach ($hooks as $hook) {{
            call_user_func($hook['callback']);
        }}
        $output = ob_get_clean();

        echo json_encode(array('hooks' => $hooks, 'output' => $output), JSON_THROW_ON_ERROR);
        """
    ).lstrip()
    result = subprocess.run(
        ["php"],
        input=harness,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def json_ld_blocks(output: str) -> list[dict]:
    return [json.loads(block) for block in SCRIPT_PATTERN.findall(output)]


class Issue641SpeakingSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.schema_source = SCHEMA_SOURCE.read_text(encoding="utf-8")
        cls.payload = PAYLOAD.read_text(encoding="utf-8")

    def test_schema_hook_is_page_scoped_at_priority_ten(self):
        off_page = render_speaking_schema(1886)

        self.assertEqual("", off_page["output"])
        self.assertEqual(1, len(off_page["hooks"]))
        self.assertEqual(10, off_page["hooks"][0]["priority"])

    def test_speaking_page_emits_exactly_the_manifest_records(self):
        result = render_speaking_schema(1887)
        records = json_ld_blocks(result["output"])

        self.assertEqual(2, len(records))
        self.assertEqual(self.manifest["proposed_video_objects"], records)

    def test_each_video_object_is_minimal_and_valid(self):
        records = json_ld_blocks(render_speaking_schema(1887)["output"])

        for record in records:
            with self.subTest(video=record["@id"]):
                self.assertEqual(VIDEO_KEYS, set(record))
                self.assertEqual("https://schema.org", record["@context"])
                self.assertEqual("VideoObject", record["@type"])
                self.assertRegex(record["uploadDate"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertRegex(record["duration"], r"^PT(?:\d+H)?\d+M\d+S$")
                self.assertTrue(record["thumbnailUrl"].startswith("https://i.ytimg.com/"))
                self.assertTrue(
                    record["embedUrl"].startswith("https://www.youtube-nocookie.com/embed/")
                )

        validator = self.manifest["public_evidence"]["schema_markup_validator"]
        self.assertEqual(200, validator["http_status"])
        self.assertEqual(2, validator["num_objects"])
        self.assertEqual("VideoObject", validator["type"])
        self.assertEqual(0, validator["total_num_errors"])
        self.assertEqual(0, validator["total_num_warnings"])

    def test_records_only_reference_the_canonical_person(self):
        records = json_ld_blocks(render_speaking_schema(1887)["output"])
        function_source = self.schema_source.split(
            "function kk_schema_speaking_videos()", 1
        )[1].split("add_action('wp_head', 'kk_schema_speaking_videos'", 1)[0]

        for record in records:
            self.assertEqual({"@id": "https://kriskrug.co/#person"}, record["about"])
            for forbidden in ("creator", "publisher"):
                self.assertNotIn(forbidden, record)

        self.assertNotIn("'@type'         => 'Event'", function_source)
        self.assertNotIn("'@type'         => 'Service'", function_source)
        self.assertNotIn("'@type'         => 'Person'", function_source)

    def test_final_booking_card_links_to_both_proof_pages(self):
        final_booking = self.payload.split(
            "<h2>Book Kris Krüg for a keynote</h2>", 1
        )[1].split("</section>", 1)[0]

        for link in self.manifest["proof_triangle"]["speaking_outbound_links"]:
            expected = f'<a href="{link["path"]}">{link["anchor"]}</a>'
            self.assertIn(expected, final_booking)

        self.assertIn(
            "/events/ links to /speaking/ three times",
            EVENTS_PLAN.read_text(encoding="utf-8"),
        )
        self.assertIn(
            'href="/speaking/"',
            TESTIMONIALS_LIVE.read_text(encoding="utf-8"),
        )

    def test_handoff_keeps_production_changes_separately_gated(self):
        deployment = self.manifest["future_code_snippets_update_if_separately_approved"]
        handoff = HANDOFF.read_text(encoding="utf-8")

        self.assertFalse(self.manifest["live_wordpress_write_performed"])
        self.assertFalse(self.manifest["live_code_snippet_write_performed"])
        self.assertEqual(5, deployment["expected_snippet_id"])
        self.assertIn("exact snippet diff", deployment["requires"][3])
        self.assertIn("deploy and verify the Speaking page body", deployment["ordering"])
        self.assertIn("Do not apply this handoff from the worker lane.", handoff)
        self.assertIn(
            "Restore the complete captured snippet ID 5 body",
            self.manifest["post_deploy_evaluation"]["rollback"],
        )


if __name__ == "__main__":
    unittest.main()
