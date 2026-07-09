import re
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import connector_payload  # noqa: E402

# One-off publish scripts that write Jetpack SEO post-meta directly (not via
# build_wp_payload). They MUST route those two fields through normalize_seo_meta
# so combining-diacritic titles (e.g. "Ethọ́s") don't 500 — see #248/#252.
ONE_OFF_PUBLISH_SCRIPTS = [
    "publish_dc_protest_draft.py",
    "publish_you_cant_drink_data.py",
    "publish_proximity_game.py",
    "publish_context_creators.py",
    "publish_keep_the_machine_strange.py",
]

SEO_META_FIELDS = ("jetpack_seo_html_title", "advanced_seo_description")


class PublishScriptsSeoNormalizedTests(unittest.TestCase):
    def test_normalize_seo_meta_neutralizes_combining_diacritics(self):
        out = connector_payload.normalize_seo_meta("Ethọ́s Lab")
        self.assertFalse(any(__import__("unicodedata").combining(c) for c in out))

    def test_one_off_scripts_route_seo_meta_through_normalizer(self):
        for name in ONE_OFF_PUBLISH_SCRIPTS:
            src = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            self.assertIn(
                "normalize_seo_meta",
                src,
                f"{name} must import/use normalize_seo_meta",
            )
            for field in SEO_META_FIELDS:
                # Every line that assigns an SEO meta field must wrap its value
                # in normalize_seo_meta(...). Catches a future re-hardcode.
                for line in src.splitlines():
                    if f'"{field}":' in line and "get(" not in line.split(f'"{field}":')[0]:
                        self.assertIn(
                            "normalize_seo_meta",
                            line,
                            f"{name}: '{field}' assignment is not normalized: {line.strip()}",
                        )


if __name__ == "__main__":
    unittest.main()
