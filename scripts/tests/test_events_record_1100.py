"""#1100 past-only record/counter semantics and independent documentation links."""

import re
import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "events_page"))
import render_events_page as render  # noqa: E402
from scripts.tests.test_events_render_contract import block, event  # noqa: E402


def visible_rows(html):
    return [
        tag
        for tag in re.findall(r'<li class="kk-ev-rec"[^>]*>', html)
        if " hidden" not in tag
    ]


class EventsRecordTests(unittest.TestCase):
    def test_record_and_counters_include_only_past_with_and_without_art(self):
        art = {"url": "https://kriskrug.co/frame.jpg"}
        html = block(
            [event(id="future", edition=34, image=art)],
            [event(id="past", edition=33, image=art), event(id="bare")],
        )
        rows = visible_rows(html)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all('data-event-id="future"' not in row for row in rows))
        self.assertIn('<b data-events-count="rooms">2</b>', html)
        self.assertIn('<b data-events-count="editions">1</b>', html)
        self.assertIn('<b data-events-count="frames">1</b>', html)
        self.assertIn('<span data-events-count="rooms">2</span> rooms', html)

    def test_future_only_year_is_hidden_and_empty_stats_are_zero(self):
        html = block([event(id="future")], [])
        self.assertEqual(visible_rows(html), [])
        self.assertIn('<div class="kk-ev-rec-year" hidden>', html)
        for key in ("rooms", "editions", "frames"):
            self.assertIn(f'<b data-events-count="{key}">0</b>', html)
        empty = block([], [])
        self.assertIn('data-events-empty="true"', empty)
        self.assertIn(":not(.kk-ev-stats)", empty)

    def test_more_than_four_upcoming_cards_are_retained_hidden_for_later(self):
        html = block([event(id=f"future-{i}") for i in range(6)], [])
        cards = re.findall(r'<article class="kk-ev-next"[^>]*>', html)
        self.assertEqual(len(cards), 6)
        self.assertEqual(sum(" hidden" not in card for card in cards), 4)

    def test_documentation_links_are_independent_and_do_not_replace_registration(self):
        row = event(
            recap_url="https://kriskrug.co/recap/",
            docs={
                "recap": "https://bc-ai.ca/report/",
                "photos": "https://example.com/photos?a=1&b=2",
                "video": "https://youtu.be/example",
            },
        )
        html = render.render_record_row(row)
        for label in ("Recap", "Recap 2", "Photos", "Video"):
            self.assertIn(f">{label}</a>", html)
        self.assertIn('href="https://example.com/photos?a=1&amp;b=2"', html)
        self.assertIn(
            'href="https://example.org/stage"', render.render_next_card(row, {})
        )
        self.assertEqual(row["url"], "https://example.org/stage")
        self.assertNotIn('class="kk-ev-rec-docs"', render.render_record_row(event()))

    def test_unsafe_documentation_never_reaches_markup(self):
        for kind in ("recap", "photos", "video"):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                render.render_record_row(event(docs={kind: "javascript:alert(1)"}))

    def test_partition_keeps_unconfirmed_and_future_scaffolds_out(self):
        now = datetime.fromisoformat("2026-10-25T20:00:00-07:00")
        rows = [
            event(id="past", status="scaffold"),
            event(id="future-scaffold", status="scaffold", date="2026-11-01", end=None),
            event(id="unknown", status="not-confirmed"),
            event(id="unconfirmed", status="unconfirmed"),
        ]
        upcoming, past, everything = render.partition_events(rows, now)
        self.assertEqual(upcoming, [])
        self.assertEqual([e["id"] for e in past], ["past"])
        self.assertEqual(past, everything)

    def test_upcoming_sorts_by_start_date_including_multiday_festival(self):
        rows = [
            event(id="meeting", date="2026-10-29", end="2026-10-29T18:00:00-07:00"),
            event(id="festival", date="2026-10-28", end="2026-10-30T23:00:00-07:00"),
        ]
        upcoming, _, _ = render.partition_events(
            rows, datetime.fromisoformat("2026-10-25T20:00:00-07:00")
        )
        self.assertEqual([e["id"] for e in upcoming], ["festival", "meeting"])

    def test_before_at_after_cutoff_agrees_with_rendered_record(self):
        row = event(
            id="festival",
            date="2026-10-28",
            end="2026-10-30T23:00:00-07:00",
            edition=34,
        )
        for instant, expected_past in [
            ("2026-10-30T23:59:59-07:00", 0),
            ("2026-10-31T00:00:00-07:00", 1),
            ("2026-10-31T00:01:00-07:00", 1),
        ]:
            with self.subTest(instant=instant):
                up, past, all_rows = render.partition_events(
                    [row], datetime.fromisoformat(instant)
                )
                html = block(up, past, all_rows)
                self.assertEqual(len(visible_rows(html)), expected_past)
                self.assertIn(f'<b data-events-count="rooms">{expected_past}</b>', html)


if __name__ == "__main__":
    unittest.main()
