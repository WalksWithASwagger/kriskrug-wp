"""#631 render contract for scripts/events_page/render_events_page.py.

Offline. Synthetic catalogs pin the invariants the live /events/ page (WP 2250)
depends on: no local filesystem path ever reaches an ``src``, bucketing splits
on an explicit reference date, every card carries ``data-event-end`` for the
rolloff script, titles are escaped, and empty media degrades to the ``--empty``
variant. One smoke case renders the real merged catalog through ``main()``.

The local-path case guards a reachable-but-never-shipped defect: a hero existing
only on disk used to render as ``file:///Users/kk/...``. No such src has been
observed live, because ``sync_event_media.py`` has always run before ship and
the 2026-08-02 audit records no ``file://`` leaks. The guard keeps it that way.
"""

import contextlib
import io
import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/events_page"))

import lib  # noqa: E402
import render_events_page as render  # noqa: E402

CARD_RE = re.compile(r'<article class="([^"]*aurora-event-card[^"]*)"')
CARD_ID_RE = re.compile(r'data-event-id="([^"]*)"')
CARD_END_RE = re.compile(r'data-event-end="([^"]*)"')
ART_RE = re.compile(r'<figure class="[^"]*\baurora-event-art(?:\s|")')
H3_RE = re.compile(r"<h3>(.*?)</h3>", re.DOTALL)


def roots_for(base: Path) -> dict[str, Path]:
    return {"kk_kb": base, "repo": base}


def event(**overrides):
    base = {
        "id": "ev-1",
        "title": "Example Stage",
        "date": "2026-03-04",
        "end": "2026-03-04T21:00:00-08:00",
        "url": "https://example.org/stage",
        "blurb": "One sentence.",
        "label": "Mar 4 · Venue",
        "tags": [],
        "image": {},
        "status": "confirmed",
        "bucket_hint": "upcoming",
    }
    base.update(overrides)
    return base


class LocalPathsNeverShip(unittest.TestCase):
    """Guard: no file:// or /Users/ src ever reaches the output."""

    def hero_on_disk(self, tmp: str) -> Path:
        path = Path(tmp) / "hero.jpg"
        path.write_bytes(b"jpeg-bytes")
        return path

    def test_prefixed_local_path_emits_no_src_on_compact_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            ev = event(image={"path": "kk_kb:hero.jpg", "alt": "Night shot"})
            html = render.render_compact_card(ev, roots_for(Path(tmp)))
            self.assertNotIn("file://", html)
            self.assertNotIn("/Users/", html)
            self.assertNotIn("<img", html)
            self.assertIn("aurora-event-art--generated", html)

    def test_prefixed_local_path_emits_no_src_on_rich_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            ev = event(image={"path": "repo:hero.jpg", "alt": "Night shot"})
            html = render.render_rich_card(ev, roots_for(Path(tmp)))
            self.assertNotIn("file://", html)
            self.assertNotIn("/Users/", html)
            self.assertNotIn("<img", html)
            self.assertIn("aurora-event-art--generated", html)

    def test_absolute_local_path_emits_no_src(self):
        with tempfile.TemporaryDirectory() as tmp:
            hero = self.hero_on_disk(tmp)
            ev = event(image={"path": str(hero), "alt": "Night shot"})
            self.assertEqual(render.image_src(ev, roots_for(Path(tmp)))[0], "")

    def test_image_src_never_returns_a_local_uri(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            for path in ("kk_kb:hero.jpg", "repo:hero.jpg", "hero.jpg"):
                with self.subTest(path=path):
                    ev = event(image={"path": path})
                    src, _ = render.image_src(ev, roots_for(Path(tmp)))
                    self.assertFalse(src.startswith("file:"))
                    self.assertFalse(src.startswith("/"))

    def test_dynamic_block_with_local_heroes_ships_no_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            upcoming = [event(id="up-1", image={"path": "kk_kb:hero.jpg"})]
            past = [event(id="past-1", image={"path": "repo:hero.jpg"})]
            html = render.render_dynamic_block(upcoming, past, roots_for(Path(tmp)))
            self.assertNotIn("file://", html)
            self.assertNotIn("/Users/", html)

    def test_public_url_still_renders_an_img(self):
        ev = event(image={"url": "https://kriskrug.co/wp-content/x.jpg", "alt": "Hero"})
        html = render.render_compact_card(ev, roots_for(Path(".")))
        self.assertIn('src="https://kriskrug.co/wp-content/x.jpg"', html)
        self.assertNotIn("aurora-event-compact-media--empty", html)

    def test_media_id_without_url_still_emits_the_placeholder_src(self):
        ev = event(image={"media_id": 12660, "alt": "Pitch Night"})
        html = render.render_compact_card(ev, roots_for(Path(".")))
        self.assertIn('src="#media-12660"', html)


class Bucketing(unittest.TestCase):
    """Upcoming/past splits on the reference date, never on list order."""

    NOW = datetime(2026, 6, 1, 12, 0, tzinfo=timezone.utc)

    def test_split_ignores_list_order(self):
        events = [
            event(id="future-1", end="2026-09-01T21:00:00-07:00"),
            event(id="past-1", end="2025-01-15T21:00:00-08:00"),
            event(id="future-2", end="2026-07-04T21:00:00-07:00"),
            event(id="past-2", end="2026-02-02T21:00:00-08:00"),
        ]
        past = [e["id"] for e in events if render.is_past(e, self.NOW)]
        upcoming = [e["id"] for e in events if not render.is_past(e, self.NOW)]
        self.assertEqual(sorted(past), ["past-1", "past-2"])
        self.assertEqual(sorted(upcoming), ["future-1", "future-2"])

    def test_reference_date_moves_the_split(self):
        ev = event(id="ev", end="2026-07-04T21:00:00-07:00")
        self.assertFalse(render.is_past(ev, self.NOW))
        self.assertTrue(render.is_past(ev, self.NOW + timedelta(days=90)))

    def test_end_exactly_at_now_is_past(self):
        ev = event(id="ev", end="2026-06-01T12:00:00+00:00")
        self.assertTrue(render.is_past(ev, self.NOW))

    def test_bucket_hint_decides_only_when_there_is_no_date(self):
        undated_past = {"id": "u1", "bucket_hint": "past"}
        undated_upcoming = {"id": "u2", "bucket_hint": "upcoming"}
        self.assertTrue(render.is_past(undated_past, self.NOW))
        self.assertFalse(render.is_past(undated_upcoming, self.NOW))
        # A real end date wins over a stale hint.
        stale = event(id="u3", bucket_hint="upcoming", end="2025-01-01T21:00:00-08:00")
        self.assertTrue(render.is_past(stale, self.NOW))

    def test_date_only_event_ends_at_2100_pacific(self):
        parsed = render.parse_end({"date": "2026-03-04"})
        self.assertEqual(parsed.hour, 21)
        self.assertEqual(parsed.tzinfo, render.PT)

    def test_unparseable_date_yields_an_empty_end(self):
        self.assertIsNone(render.parse_end({"date": "sometime in spring"}))
        self.assertEqual(render.end_iso({"date": "sometime in spring"}), "")

    def test_cards_land_in_their_declared_grid(self):
        upcoming = [event(id="up-1")]
        past = [event(id="past-1")]
        html = render.render_dynamic_block(upcoming, past, roots_for(Path(".")))
        up_grid = html.index('data-events-grid="upcoming">')
        past_grid = html.index('data-events-grid="past">')
        self.assertLess(up_grid, html.index('data-event-id="up-1"'))
        self.assertLess(html.index('data-event-id="up-1"'), past_grid)
        self.assertLess(past_grid, html.index('data-event-id="past-1"'))

    def test_empty_buckets_are_flagged_for_the_collapse_css(self):
        html = render.render_dynamic_block(
            [], [event(id="past-1")], roots_for(Path("."))
        )
        self.assertIn('data-events-bucket="upcoming" data-events-empty="true"', html)
        self.assertIn('data-events-bucket="past" data-events-empty="false"', html)


class CardContract(unittest.TestCase):
    """Class names and data attributes the CSS and rolloff script select on."""

    def test_rich_card_classes(self):
        html = render.render_rich_card(event(), roots_for(Path(".")))
        classes = CARD_RE.search(html).group(1).split()
        self.assertIn("aurora-event-card", classes)
        self.assertIn("aurora-event-card--rich", classes)
        self.assertIn("aurora-proof-module", classes)
        self.assertNotIn("aurora-event-card--compact", classes)

    def test_compact_card_classes(self):
        html = render.render_compact_card(event(), roots_for(Path(".")))
        classes = CARD_RE.search(html).group(1).split()
        self.assertIn("aurora-event-card", classes)
        self.assertIn("aurora-event-card--compact", classes)
        self.assertNotIn("aurora-event-card--rich", classes)

    def test_every_card_carries_data_event_end(self):
        upcoming = [event(id="up-1"), event(id="up-2", end="2026-05-05T18:00:00-07:00")]
        past = [event(id="past-1", end="2025-01-15T21:00:00-08:00"), {"id": "past-2"}]
        html = render.render_dynamic_block(upcoming, past, roots_for(Path(".")))
        self.assertEqual(len(CARD_RE.findall(html)), 4)
        self.assertEqual(len(CARD_END_RE.findall(html)), 4)

    def test_data_event_end_is_tz_aware_iso(self):
        html = render.render_rich_card(
            event(end="2026-05-05T18:00:00-07:00"), roots_for(Path("."))
        )
        value = CARD_END_RE.search(html).group(1)
        self.assertEqual(datetime.fromisoformat(value).utcoffset(), timedelta(hours=-7))

    def test_undated_card_still_emits_the_attribute(self):
        html = render.render_compact_card({"id": "u1"}, roots_for(Path(".")))
        self.assertIn('data-event-end=""', html)

    def test_cta_labels_swap_between_buckets(self):
        html = render.render_rich_card(event(), roots_for(Path(".")))
        self.assertIn("aurora-event-cta-upcoming", html)
        self.assertIn("aurora-event-cta-past", html)
        self.assertIn(">Register<", html)
        self.assertIn(">Event details<", html)


class Escaping(unittest.TestCase):
    def test_title_with_markup_characters_is_escaped(self):
        ev = event(title='Rooms & <Stages> "2026"')
        for html in (
            render.render_rich_card(ev, roots_for(Path("."))),
            render.render_compact_card(ev, roots_for(Path("."))),
        ):
            heading = H3_RE.search(html).group(1)
            self.assertEqual(heading, "Rooms &amp; &lt;Stages&gt; &quot;2026&quot;")

    def test_alt_text_cannot_break_out_of_the_attribute(self):
        ev = event(image={"url": "https://kriskrug.co/x.jpg", "alt": 'A "quoted" hero'})
        html = render.render_compact_card(ev, roots_for(Path(".")))
        self.assertIn('alt="A &quot;quoted&quot; hero"', html)

    def test_url_and_tags_are_escaped(self):
        ev = event(url='https://example.org/?a=1&b="2"', tags=["Keynote & Panel"])
        html = render.render_rich_card(ev, roots_for(Path(".")))
        self.assertIn('href="https://example.org/?a=1&amp;b=&quot;2&quot;"', html)
        self.assertIn("<span>Keynote &amp; Panel</span>", html)

    def test_photographer_credit_folds_into_alt(self):
        ev = event(
            image={
                "url": "https://kriskrug.co/x.jpg",
                "alt": "Meetup floor",
                "photographer": "Michelle Diamond",
            }
        )
        _, alt = render.image_src(ev, roots_for(Path(".")))
        self.assertEqual(alt, "Meetup floor (photo: Michelle Diamond)")


class ArtworkFallback(unittest.TestCase):
    def test_compact_card_without_media_uses_a_generated_poster(self):
        html = render.render_compact_card(event(image={}), roots_for(Path(".")))
        self.assertIn("aurora-event-art--generated", html)
        self.assertIn('role="img"', html)
        self.assertNotIn("<img", html)
        self.assertIn("<figure", html)

    def test_rich_card_without_media_uses_a_generated_poster(self):
        html = render.render_rich_card(event(image={}), roots_for(Path(".")))
        self.assertNotIn("<img", html)
        self.assertIn("aurora-event-art--generated", html)
        self.assertIn("<figure", html)
        self.assertIn("aurora-proof-body", html)

    def test_contain_fit_is_explicit_on_real_artwork(self):
        ev = event(
            image={"url": "https://kriskrug.co/logo.webp", "alt": "Logo"},
            image_fit="contain",
        )
        html = render.render_rich_card(ev, roots_for(Path(".")))
        self.assertIn("aurora-event-art--contain", html)
        self.assertIn('src="https://kriskrug.co/logo.webp"', html)

    def test_compact_card_without_a_url_emits_no_link(self):
        html = render.render_compact_card(event(url=""), roots_for(Path(".")))
        self.assertNotIn("aurora-event-compact-link", html)


class RealCatalogSmoke(unittest.TestCase):
    """Real merged catalog renders one card per publishable event."""

    def render_main(self, out: Path) -> str:
        argv = sys.argv
        sys.argv = ["render_events_page.py", "--out", str(out)]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                code = render.main()
        finally:
            sys.argv = argv
        self.assertEqual(code, 0)
        return out.read_text(encoding="utf-8")

    def test_real_catalog_renders_every_publishable_event_once(self):
        doc = lib.load_catalog()
        publishable = [e for e in doc["events"] if render.public_status(e)]
        self.assertTrue(publishable, "catalog should have publishable events")
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")

        self.assertEqual(len(CARD_RE.findall(html)), len(publishable))
        self.assertEqual(
            sorted(CARD_ID_RE.findall(html)),
            sorted(e["id"] for e in publishable),
        )
        # Non-publishable statuses stay in the catalog but never ship.
        withheld = {e["id"] for e in doc["events"]} - {e["id"] for e in publishable}
        for eid in withheld:
            self.assertNotIn(f'data-event-id="{eid}"', html)

    def test_real_render_gives_every_dated_card_an_artboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertEqual(len(ART_RE.findall(html)), len(CARD_RE.findall(html)))

    def test_real_render_includes_the_accessible_archive_toggle(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertIn('data-events-archive-toggle', html)
        self.assertIn('aria-expanded="false"', html)

    def test_real_render_carries_no_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertNotIn("file://", html)
        self.assertNotIn("/Users/", html)
        self.assertNotIn('src=""', html)

    def test_real_render_gives_every_card_a_usable_rolloff_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        ends = CARD_END_RE.findall(html)
        self.assertEqual(len(ends), len(CARD_RE.findall(html)))
        for value in ends:
            if not value:
                continue
            with self.subTest(end=value):
                self.assertIsNotNone(datetime.fromisoformat(value).tzinfo)

    def test_real_render_keeps_the_shell_markers_and_evergreen_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertIn(lib.DYNAMIC_START, html)
        self.assertIn(lib.DYNAMIC_END, html)
        self.assertIn('data-events-grid="upcoming">', html)
        self.assertIn('data-events-grid="past">', html)


if __name__ == "__main__":
    unittest.main()
