import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
REVIVE = ROOT / "theme/kk-aurora/assets/css/revive-port.css"

REQUIRED_HREFS = (
    "https://www.youtube.com/watch?v=-c7mgY2aSgM",
    "https://www.youtube.com/watch?v=T5ANAthZewE",
    "https://www.punkrockai.com/",
    "https://www.youtube.com/watch?v=1OcC-0X6Nb8",
    "https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/",
    "https://www.youtube.com/watch?v=-XEsqsEbpoo",
    "https://www.youtube.com/watch?v=owtSPcpRinI",
    "https://www.futureproof.website/",
    "/speaking/",
)

BANNED_WALLPAPER = (
    "TED",
    "SXSW",
    "Adobe MAX",
    "FITC",
    "MIT Media Lab",
)

APPROVED_PHOTOS = (
    "kk-laSalle-both-hands-full-25-scaled.jpg",
    "/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-600.webp",
    "/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community-1200.webp",
)


def _stages_block(source: str) -> str:
    match = re.search(
        r'<section class="aurora-stages-band".*?</section>',
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing #stages aurora-stages-band")
    return match.group(0)


class Issue414HomepageStagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = FRONT_PAGE.read_text(encoding="utf-8")
        cls.css = REVIVE.read_text(encoding="utf-8")
        cls.stages = _stages_block(cls.front)

    def test_section_is_image_led_and_linked(self):
        self.assertIn('id="stages"', self.stages)
        self.assertIn('id="aurora-stages-title"', self.stages)
        self.assertIn("Stages with receipts", self.stages)
        self.assertIn("Rooms where the work got said out loud.", self.stages)
        for href in REQUIRED_HREFS:
            self.assertIn(f'href="{href}"', self.stages)
        for photo in APPROVED_PHOTOS:
            self.assertIn(photo, self.stages)

    def test_no_prestige_wallpaper_or_uncleared_hotlinks(self):
        self.assertNotIn("aurora-proof-outlets", self.front)
        self.assertNotIn("punkrockai.com/public/photos", self.stages)
        self.assertNotIn("www.punkrockai.com/public", self.stages)
        for name in BANNED_WALLPAPER:
            self.assertNotIn(f">{name}<", self.stages)
            self.assertNotIn(f">{name}</span>", self.front)

    def test_only_two_stage_photos_in_the_band(self):
        images = re.findall(r"<img\b", self.stages)
        self.assertEqual(2, len(images))

    def test_hover_and_focus_states_exist(self):
        self.assertIn(".aurora-stages-feature:hover", self.css)
        self.assertIn(".aurora-stages-feature:focus-visible", self.css)
        self.assertIn(".aurora-stages-list a:hover", self.css)
        self.assertIn(".aurora-stages-list a:focus-visible", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)

    def test_copy_has_no_em_dash_or_newsletter_cliche(self):
        self.assertNotIn("\u2014", self.stages)
        self.assertNotRegex(self.stages, re.compile(r"field notes", re.I))
        self.assertNotRegex(self.stages, re.compile(r"dispatch", re.I))


if __name__ == "__main__":
    unittest.main()
