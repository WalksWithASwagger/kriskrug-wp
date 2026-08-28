import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEAKING_DIR = (
    ROOT / "content" / "drafts" / "2026-07-26-speaking-page"
)
PAYLOAD = SPEAKING_DIR / "payload-body.html"
PLAN = SPEAKING_DIR / "payload-plan.md"
CANONICAL_TALKS = (
    "Both Hands Full",
    "Punk Rock AI / Creative Rebellion",
    "Developing an AI Mindset",
    "Compost AI",
    "Leadership After the AI Point of No Return",
    "Power, Taste, and Trust",
)
FORMAT_FAMILIES = (
    "Keynotes",
    "Workshops",
    "Executive briefings",
    "Hosting and moderation",
)


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"}:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth and data.strip():
            self.parts.append(data.strip())

    def text(self):
        return " ".join(self.parts)


def section_with_id(html, section_id):
    match = re.search(
        rf'<section\b(?=[^>]*\bid="{re.escape(section_id)}")[^>]*>(.*?)</section>',
        html,
        re.DOTALL,
    )
    if not match:
        return ""
    return match.group(1)


def visible_text(html):
    parser = VisibleTextParser()
    parser.feed(html)
    return parser.text()


class SpeakingBookingFactsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAYLOAD.read_text(encoding="utf-8")
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.booking_facts = section_with_id(cls.html, "booking-facts")
        cls.booking_text = visible_text(cls.booking_facts)

    def test_answer_first_block_precedes_keynote_grid_and_names_the_offer(self):
        self.assertTrue(self.booking_facts, "booking-facts section is missing")
        self.assertLess(
            self.html.index('id="booking-facts"'),
            self.html.index('id="signature-keynotes"'),
        )
        self.assertIn(
            "Kris Krüg is an AI keynote speaker based in Vancouver, "
            "British Columbia, Canada.",
            self.booking_text,
        )
        for format_family in FORMAT_FAMILIES:
            self.assertIn(format_family.lower(), self.booking_text.lower())

    def test_five_planning_facts_cover_the_booking_path(self):
        self.assertEqual(5, len(re.findall(r"<article\b", self.booking_facts)))
        for heading in (
            "Location",
            "Formats",
            "Audiences and topics",
            "What to send",
            "Next step",
        ):
            self.assertRegex(
                self.booking_facts,
                rf"<h3>{re.escape(heading)}</h3>",
            )
        for field in ("audience", "date", "location", "format", "question"):
            self.assertIn(field, self.booking_text.lower())
        self.assertIn('href="/contact/"', self.booking_facts)

    def test_existing_six_talk_video_and_format_contracts_remain_intact(self):
        keynotes = section_with_id(self.html, "signature-keynotes")
        watch = section_with_id(self.html, "watch")

        talk_titles = re.findall(r"<h3>(.*?)</h3>", keynotes, re.DOTALL)
        self.assertEqual(list(CANONICAL_TALKS), talk_titles)
        self.assertEqual(2, len(re.findall(r"<iframe\b", watch)))
        for format_family in FORMAT_FAMILIES:
            self.assertIn(f"<h3>{format_family}</h3>", self.html)

    def test_booking_facts_do_not_add_unsupported_claims_or_old_location(self):
        self.assertTrue(self.booking_facts, "booking-facts section is missing")
        lowered = self.booking_text.lower()
        for unsupported in (
            "galiano",
            "travel",
            "nationwide",
            "virtual",
            "bilingual",
            "fee",
            "lead time",
            "availability",
        ):
            self.assertNotIn(unsupported, lowered)
        self.assertNotIn("$", self.booking_text)
        self.assertNotIn("galiano", self.plan.lower())

    def test_claim_to_source_matrix_covers_each_new_fact_family(self):
        self.assertIn("## Booking claim-to-source matrix (#904)", self.plan)
        for claim_family in (
            "Identity and location",
            "Formats",
            "Audiences and topics",
            "Booking inputs",
            "Next step",
        ):
            self.assertRegex(
                self.plan,
                rf"(?m)^\| {re.escape(claim_family)} \|",
            )


if __name__ == "__main__":
    unittest.main()
