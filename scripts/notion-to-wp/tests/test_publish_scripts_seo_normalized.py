import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402
from cp1252_text import UnstorableText  # noqa: E402


class PublishScriptsSeoNormalizedTests(unittest.TestCase):
    def test_shared_seo_meta_contract_keeps_cp1252_text_in_both_write_fields(self):
        meta = publish_common.build_seo_meta("KK’s Café Krüg", "About “Café Krüg” – more…")

        self.assertEqual(
            meta,
            {
                "jetpack_seo_html_title": "KK’s Café Krüg",
                "advanced_seo_description": "About “Café Krüg” – more…",
            },
        )

    def test_shared_seo_meta_contract_refuses_either_field(self):
        for title, description in (("Ethọ́s Lab", "About"), ("About", "Ethọ́s Lab")):
            with self.subTest(title=title, description=description):
                with self.assertRaises(UnstorableText):
                    publish_common.build_seo_meta(title, description)


if __name__ == "__main__":
    unittest.main()
