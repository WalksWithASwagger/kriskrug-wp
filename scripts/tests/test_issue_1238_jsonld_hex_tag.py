import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNIPPET_SOURCES = (
    ROOT / "fixes/schema-snippets-deployed.php",
    ROOT / "fixes/schema-snippets.php",
)
MARQUEE_SCHEMA = ROOT / "plugins/kk-marquee-board/includes/schema.php"
HOSTILE_TITLE = "</script><b>x</b>"
HOSTILE_EXCERPT = "Tom & Jerry <img src=x onerror=alert(1)>"
SCRIPT_BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def emit(source: Path) -> str:
    harness = f"""<?php
function add_action() {{}}
function wp_json_encode($data, $flags = 0) {{ return json_encode($data, $flags); }}
require {json.dumps(str(source))};
kk_schema_emit(array(
    '@context'    => 'https://schema.org',
    '@type'       => 'BlogPosting',
    'headline'    => {json.dumps(HOSTILE_TITLE)},
    'description' => {json.dumps(HOSTILE_EXCERPT)},
    'url'         => 'https://kriskrug.co/2026/11/12/example/',
));
"""
    result = subprocess.run(["php"], input=harness, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout


class Issue1238JsonLdHexTagTests(unittest.TestCase):
    def test_every_emitter_sets_hex_tag_and_hex_amp(self):
        for path in (*SNIPPET_SOURCES, MARQUEE_SCHEMA):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("JSON_UNESCAPED_UNICODE)", source)
                self.assertNotIn("JSON_UNESCAPED_UNICODE;", source)
                self.assertIn(
                    "JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP",
                    source,
                )

    def test_hostile_title_stays_inside_the_json_ld_block(self):
        for path in SNIPPET_SOURCES:
            with self.subTest(path=path.relative_to(ROOT)):
                out = emit(path)
                self.assertEqual(1, out.count("</script>"))
                self.assertTrue(out.rstrip().endswith("</script>"))
                self.assertNotIn("<b>", out)
                self.assertNotIn("<img", out)
                blocks = SCRIPT_BLOCK.findall(out)
                self.assertEqual(1, len(blocks))
                data = json.loads(blocks[0])
                self.assertEqual(HOSTILE_TITLE, data["headline"])
                self.assertEqual(HOSTILE_EXCERPT, data["description"])
                self.assertIn(
                    '"url":"https://kriskrug.co/2026/11/12/example/"', blocks[0]
                )


if __name__ == "__main__":
    unittest.main()
