"""#1028 FAQ magnet packet: locked answers, no Event, gated FAQPage."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/drafts/issue-1028-all-in-faq-aeo"
EM_DASH = "\u2014"

POSTS = (
    {
        "faq": PACK / "blocks/all-in-01-faq.html",
        "faqpage": PACK / "blocks/all-in-01-faqpage.html",
        "questions": (
            "What is ALL IN Montréal?",
            "Who wrote this?",
            "Where and when?",
            "Why does this matter for British Columbia?",
        ),
        "answer_needles": (
            "September 16-17, 2026",
            "accredited media",
            "September 15 travel and setup-day dispatch",
            "Mila-scale institutional anchor",
        ),
    },
    {
        "faq": PACK / "blocks/all-in-02-faq.html",
        "faqpage": PACK / "blocks/all-in-02-faqpage.html",
        "questions": (
            "What happened on day one at ALL IN Montréal?",
            "Who is this for?",
            "Where and when?",
            "Why do BC + AI and Futureproof care?",
        ),
        "answer_needles": (
            "Cohere and Aleph Alpha",
            "LawZero funding",
            "Palais des congrès",
            "September 16, 2026",
        ),
    },
)


def _jsonld(html: str) -> dict:
    match = re.search(
        r"<script type=\"application/ld\+json\">(.*?)</script>",
        html,
        re.S,
    )
    assert match, "FAQPage file is missing JSON-LD"
    return json.loads(match.group(1))


class TestIssue1028AllInFaq(unittest.TestCase):
    def test_packet_files_exist(self):
        for name in (
            "README.md",
            "STATUS.md",
            "APPLY.md",
            "copy.md",
            "seo-lgtm.md",
            "targets.json",
        ):
            self.assertTrue((PACK / name).is_file(), name)

    def test_targets_are_the_two_live_posts(self):
        targets = json.loads((PACK / "targets.json").read_text(encoding="utf-8"))
        items = {item["id"]: item for item in targets["items"]}
        self.assertEqual(set(items), {12783, 12788})
        self.assertEqual(items[12783]["slug"], "headed-east-for-all-in-montreal")
        self.assertEqual(items[12788]["slug"], "all-in-montreal-robot-mirror")
        self.assertEqual(targets["status"], "paste_ready_not_live")
        for item in items.values():
            self.assertEqual(item["insert_before"], '<section id="owned-network-links-2026"')
            self.assertFalse(item["live_faq_heading"])

    def test_recommended_faq_has_locked_qas_and_no_related_line(self):
        for post in POSTS:
            html = post["faq"].read_text(encoding="utf-8")
            self.assertIn('id="faq"', html)
            self.assertNotIn(EM_DASH, html)
            self.assertNotIn('"Event"', html)
            self.assertNotIn("Related:", html)
            self.assertNotIn('href="https://bc-ai.ca/"', html)
            self.assertNotIn('href="https://www.futureproof.website/"', html)
            for question in post["questions"]:
                self.assertIn(question, html)
            for needle in post["answer_needles"]:
                self.assertIn(needle, html)

    def test_faqpage_mirrors_visible_questions_only(self):
        for post in POSTS:
            html = post["faqpage"].read_text(encoding="utf-8")
            self.assertIn("GATED", html)
            payload = _jsonld(html)
            self.assertEqual(payload["@type"], "FAQPage")
            names = [entity["name"] for entity in payload["mainEntity"]]
            self.assertEqual(tuple(names), post["questions"])
            dumped = json.dumps(payload)
            self.assertNotIn("Event", dumped)
            self.assertNotIn(EM_DASH, dumped)

    def test_apply_path_stays_off_live_wp(self):
        apply_text = (PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("prep-only", apply_text)
        self.assertIn("Do not invent a WP login", apply_text)
        self.assertIn("Do not send email or Buffer", apply_text)


if __name__ == "__main__":
    unittest.main()
