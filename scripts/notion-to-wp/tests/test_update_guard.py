import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402


class UpdateTitleGuardTests(unittest.TestCase):
    def test_guard_allows_matching_title_case_insensitive(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Your Taste Is Your Moat",
            "your taste is your moat",
        )

        self.assertTrue(allowed)
        self.assertEqual(similarity, 1.0)

    def test_guard_allows_close_title_variation(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Web Summit Vancouver 2026",
            "Web Summit Vancouver 2026: Field Notes",
        )

        self.assertTrue(allowed)
        self.assertGreaterEqual(
            similarity,
            kk_notion_to_wp.TITLE_SIMILARITY_UPDATE_THRESHOLD,
        )

    def test_guard_blocks_incident_style_wrong_post_collision(self):
        allowed, similarity = kk_notion_to_wp.update_title_guard(
            "Calling Us All In",
            "Web Summit Vancouver 2026",
        )

        self.assertFalse(allowed)
        self.assertLess(
            similarity,
            kk_notion_to_wp.TITLE_SIMILARITY_UPDATE_THRESHOLD,
        )


if __name__ == "__main__":
    unittest.main()
