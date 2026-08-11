import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
# KK-approved community photo (#631): served as right-sized WebP derivatives
# since #702; the source JPG stays in-repo for draft payloads that reference it.
PHOTO_600 = ROOT / "theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-600.webp"
PHOTO_1200 = ROOT / "theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-1200.webp"
PHOTO_600_PATH = "/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-600.webp"
PHOTO_1200_PATH = "/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-1200.webp"
PHOTO_600_SHA256 = "68576f636143ce3ca1e6ccce059c0790db9dbed1ec18371bc93515d1389677d4"
PHOTO_1200_SHA256 = "5dcb05f0ffc911cdca1d7c371daea365d49c0dbce133e85058df3e9dab3520f8"


class ApprovedCommunityPhotoTests(unittest.TestCase):
    def test_homepage_uses_the_canonical_approved_photo(self):
        source = FRONT_PAGE.read_text(encoding="utf-8")

        self.assertIn(PHOTO_600_PATH, source)
        self.assertIn(PHOTO_1200_PATH, source)
        self.assertIn(
            "Kris Krüg raises one hand onstage while rows of attendees raise their hands "
            "at the H.R. MacMillan Space Centre",
            source,
        )
        self.assertEqual(PHOTO_600_SHA256, hashlib.sha256(PHOTO_600.read_bytes()).hexdigest())
        self.assertEqual(PHOTO_1200_SHA256, hashlib.sha256(PHOTO_1200.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
