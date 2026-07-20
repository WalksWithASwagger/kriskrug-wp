import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
PHOTO = ROOT / "theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg"
PHOTO_PATH = "/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg"
PHOTO_SHA256 = "86934e9268e7cb6e1ecc7df95bd502006cafb73e038676f9aacba59f3aef0714"


class ApprovedCommunityPhotoTests(unittest.TestCase):
    def test_homepage_uses_the_canonical_approved_photo(self):
        source = FRONT_PAGE.read_text(encoding="utf-8")

        self.assertIn(PHOTO_PATH, source)
        self.assertIn(
            "Kris Krüg raises one hand onstage while rows of attendees raise their hands "
            "at the H.R. MacMillan Space Centre",
            source,
        )
        self.assertEqual(PHOTO_SHA256, hashlib.sha256(PHOTO.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
