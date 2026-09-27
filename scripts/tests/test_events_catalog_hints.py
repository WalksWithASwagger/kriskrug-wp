"""Guard against bucket_hint drift in events-catalog.yaml.

Four past events sat at `bucket_hint: upcoming` for weeks before anyone noticed
(2026-09-27). Nothing caught it because nothing reads the field on those rows:
render_events_page.is_past() only consults the hint when an event has no
parseable end date, and every event currently has one. Dead data does not
misbehave, so it never surfaces. These tests make it surface.

Deliberately NOT asserting "hint always agrees with the date". Every upcoming
event becomes past the day after it happens, so that assertion would turn red
overnight on unrelated PRs and get muted within a month. STALE_AFTER_DAYS gives
a week of slack: no surprise failure the morning after an event, but drift
cannot quietly accumulate either.
"""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "events_page"))

from render_events_page import parse_end  # noqa: E402

CATALOG = REPO_ROOT / "scripts" / "events_page" / "events-catalog.yaml"
STALE_AFTER_DAYS = 7


def load_events() -> list[dict]:
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))["events"]


def hint_of(event: dict) -> str:
    return (event.get("bucket_hint") or "").strip().lower()


def stale_upcoming(events: list[dict], now: datetime, grace_days: int) -> list[str]:
    """Events that ended more than `grace_days` ago and still claim upcoming."""
    cutoff = now - timedelta(days=grace_days)
    out = []
    for e in events:
        end = parse_end(e)
        if end is not None and end < cutoff and hint_of(e) == "upcoming":
            out.append(f"{e['id']} (ended {end.date()}, still bucket_hint: upcoming)")
    return out


class BucketHintDriftTests(unittest.TestCase):
    def test_no_long_past_event_still_marked_upcoming(self):
        stale = stale_upcoming(
            load_events(), datetime.now(timezone.utc), STALE_AFTER_DAYS
        )
        self.assertEqual(
            stale,
            [],
            "Past events still flagged upcoming in events-catalog.yaml. "
            "Set bucket_hint: past on:\n  " + "\n  ".join(stale),
        )

    def test_events_without_an_end_date_carry_an_explicit_hint(self):
        """The only rows where the hint actually drives bucketing.

        Vacuous while every event has an end date. It exists so that adding a
        dateless event without a hint fails loudly instead of silently
        defaulting to past in lib.py and landing in the wrong section.
        """
        missing = [
            e["id"]
            for e in load_events()
            if parse_end(e) is None and hint_of(e) not in {"past", "upcoming"}
        ]
        self.assertEqual(
            missing,
            [],
            "Events with no parseable end date must set bucket_hint explicitly "
            "(past or upcoming), because that is the only case the renderer "
            "reads it:\n  " + "\n  ".join(missing),
        )


class DriftDetectorTests(unittest.TestCase):
    """The guard above is only worth having if it can actually fail."""

    def setUp(self):
        self.now = datetime(2026, 9, 27, tzinfo=timezone.utc)

    def test_detects_a_long_past_event_marked_upcoming(self):
        drifted = [
            {"id": "x", "end": "2026-08-01T12:00:00-07:00", "bucket_hint": "upcoming"}
        ]
        self.assertEqual(len(stale_upcoming(drifted, self.now, STALE_AFTER_DAYS)), 1)

    def test_ignores_an_event_that_only_just_ended(self):
        """No red the morning after. This is what STALE_AFTER_DAYS buys."""
        yesterday = (self.now - timedelta(days=1)).isoformat()
        fresh = [{"id": "x", "end": yesterday, "bucket_hint": "upcoming"}]
        self.assertEqual(stale_upcoming(fresh, self.now, STALE_AFTER_DAYS), [])

    def test_ignores_a_genuinely_upcoming_event(self):
        later = (self.now + timedelta(days=30)).isoformat()
        future = [{"id": "x", "end": later, "bucket_hint": "upcoming"}]
        self.assertEqual(stale_upcoming(future, self.now, STALE_AFTER_DAYS), [])

    def test_ignores_a_past_event_correctly_marked(self):
        done = [{"id": "x", "end": "2026-08-01T12:00:00-07:00", "bucket_hint": "past"}]
        self.assertEqual(stale_upcoming(done, self.now, STALE_AFTER_DAYS), [])


if __name__ == "__main__":
    unittest.main()
