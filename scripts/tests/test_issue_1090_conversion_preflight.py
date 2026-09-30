"""Offline contract for the #1103 conversion-preflight packet."""

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "docs/current-state/reports/issue-1090-conversion-preflight-2026-09-29.md"
HANDOFF = ROOT / "fixes/issue-1090-conversion-handoff-2026-09-30.md"
HELPER = ROOT / "fixes/issue-1090-success-event.js"
HARNESS = ROOT / "scripts/tests/issue_1090_success_event_harness.cjs"
HEADER = ROOT / "theme/kk-aurora/parts/header.html"
FOOTER = ROOT / "theme/kk-aurora/parts/footer.html"
SINGLE = ROOT / "theme/kk-aurora/templates/single.html"
FRONT = ROOT / "theme/kk-aurora/templates/front-page.html"
HOME = ROOT / "theme/kk-aurora/templates/home.html"


class Issue1090ConversionPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = PACKET.read_text(encoding="utf-8")
        cls.handoff = HANDOFF.read_text(encoding="utf-8")
        cls.helper = HELPER.read_text(encoding="utf-8")

    def test_required_paths_exist(self):
        for path in (PACKET, HANDOFF, HELPER, HARNESS):
            self.assertTrue(path.is_file(), path)

    def test_packet_inventories_both_candidates_and_organic_surfaces(self):
        for needle in (
            "newsletter_submit",
            "speaking_inquiry_submit",
            "/speaking/",
            "article footer",
            "embeds.beehiiv.com",
            "cross-origin",
            "mailto:feelmoreplants@gmail.com",
            "#277",
        ):
            self.assertIn(needle, self.packet)

    def test_packet_rejects_click_and_postmessage(self):
        self.assertIn("never on a click", self.packet.lower())
        self.assertIn("Do not implement postMessage", self.packet)
        self.assertIn("newsletter_click", self.packet)
        self.assertIn("not a conversion", self.packet.lower())

    def test_packet_does_not_close_issues_or_refresh_ga4(self):
        self.assertNotIn("Closes #1103", self.packet)
        self.assertNotIn("Closes #1090", self.packet)
        self.assertIn("Keep #1090 open", self.packet)
        self.assertIn("dated provenance", self.packet.lower())
        self.assertNotIn("op://", self.packet)
        self.assertNotIn("op://", self.handoff)

    def test_handoff_is_prep_only(self):
        self.assertIn("NOT LIVE", self.handoff)
        self.assertIn("rollback", self.handoff.lower())
        self.assertIn("KK", self.handoff)
        self.assertIn("do not mark a ga4 key event", self.handoff.lower())

    def test_helper_is_success_only_and_unwired(self):
        executable = re.sub(r"/\*[\s\S]*?\*/", "", self.helper)
        executable = re.sub(r"//.*$", "", executable, flags=re.M)
        self.assertIn("newsletter_submit", self.helper)
        self.assertIn("speaking_inquiry_submit", self.helper)
        self.assertNotIn("postMessage", executable)
        self.assertNotIn("addEventListener", executable)
        self.assertNotRegex(executable, r"beehiiv")
        self.assertIn("NOT LIVE", self.helper)
        self.assertIn("submission_id", self.helper)

    def test_packet_documents_event_param_allowlist(self):
        lowered = self.packet.lower()
        self.assertIn("Event-param allowlist", self.packet)
        self.assertIn("never", lowered)
        self.assertIn("email", lowered)
        self.assertIn("form field", lowered)
        self.assertIn("allowlist", lowered)
        self.assertIn("email, name, and form field values are dropped", lowered)

    def test_theme_chrome_matches_inventory(self):
        header = HEADER.read_text(encoding="utf-8")
        footer = FOOTER.read_text(encoding="utf-8")
        single = SINGLE.read_text(encoding="utf-8")
        front = FRONT.read_text(encoding="utf-8")
        home = HOME.read_text(encoding="utf-8")
        self.assertIn("https://kriskrug.beehiiv.com/", header)
        self.assertIn("Newsletter", header)
        self.assertIn("https://kriskrug.beehiiv.com/", footer)
        self.assertIn("Subscribe free", footer)
        self.assertIn('href="/speaking/"', single)
        self.assertIn("Book Kris", single)
        self.assertIn("aurora-author-panel", single)
        self.assertNotIn("embeds.beehiiv.com", header + footer + single + front + home)
        self.assertIn("Get the weekly email", front)
        self.assertIn("Get the weekly email", home)

    def test_harness_passes(self):
        result = subprocess.run(
            ["node", str(HARNESS)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("issue_1090_success_event_harness: ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
