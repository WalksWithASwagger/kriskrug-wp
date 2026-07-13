import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402


class PublishScriptsSeoNormalizedTests(unittest.TestCase):
    def test_shared_seo_meta_contract_normalizes_both_write_fields(self):
        meta = publish_common.build_seo_meta("Ethọ́s Lab", "About Ethọ́s Lab")

        self.assertEqual(
            set(meta),
            {"jetpack_seo_html_title", "advanced_seo_description"},
        )
        self.assertFalse(
            any(
                __import__("unicodedata").combining(char)
                for value in meta.values()
                for char in value
            )
        )


if __name__ == "__main__":
    unittest.main()
