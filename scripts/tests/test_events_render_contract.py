"""#631 render contract for scripts/events_page/render_events_page.py.

Offline. Synthetic catalogs pin the invariants the live /events/ page (WP 2250)
depends on: no local filesystem path ever reaches an ``src``, bucketing splits
on an explicit reference date, every card carries ``data-event-end`` for the
rolloff script, titles are escaped, and an event with no art is carried by the
record index rather than by invented artwork.

The local-path case guards a reachable-but-never-shipped defect: a hero existing
only on disk used to render as ``file:///Users/kk/...``. No such src has been
observed live, because ``sync_event_media.py`` has always run before ship and
the 2026-08-02 audit records no ``file://`` leaks. The guard keeps it that way,
and now also covers the ``--preview-local`` escape hatch.

Layout contract (2026-09-13 art direction): upcoming events render as spotlight
cards, every event with real art renders as a contact-sheet tile, and every
publishable event renders as a row in the complete record.
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

NEXT_RE = re.compile(r'<article class="kk-ev-next"')
TILE_RE = re.compile(r'<article class="kk-ev-tile"')
REC_RE = re.compile(r'<li class="kk-ev-rec"')
CARD_ID_RE = re.compile(r'data-event-id="([^"]*)"')
CARD_END_RE = re.compile(r'data-event-end="([^"]*)"')
H3_RE = re.compile(r"<h3>(.*?)</h3>", re.DOTALL)
REC_ID_RE = re.compile(r'<li class="kk-ev-rec" data-event-end="[^"]*" data-event-id="([^"]*)"')


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


def block(upcoming, past, everything=None, roots=None):
    return render.render_dynamic_block(
        upcoming,
        past,
        everything if everything is not None else list(upcoming) + list(past),
        roots or roots_for(Path(".")),
    )


class PreviewLocalIsOff(unittest.TestCase):
    """--preview-local is a review-only mode and must never be the default."""

    def test_module_default_is_off(self):
        self.assertFalse(render.PREVIEW_LOCAL)

    def tearDown(self):
        render.PREVIEW_LOCAL = False

    def test_preview_local_paths_are_relative_and_never_absolute(self):
        render.PREVIEW_LOCAL = True
        ev = event(image={"path": "repo:heroes/_pending/x.webp", "alt": "Night"})
        src, _ = render.image_src(ev, roots_for(Path("/Users/someone")))
        self.assertEqual(src, "heroes/x.webp")
        self.assertNotIn("/Users/", src)
        self.assertFalse(src.startswith("/"))


class RecapDestination(unittest.TestCase):
    def test_tile_prefers_recap_but_retains_source_record(self):
        ev = event(recap_url="https://kriskrug.co/a-recap/", image={"url": "https://kriskrug.co/x.jpg"})
        output = render.render_tile(ev, roots_for(ROOT), upcoming=False)
        self.assertIn('href="https://kriskrug.co/a-recap/"', output)
        self.assertNotIn('href="https://example.org/stage"', output)
        self.assertEqual("https://example.org/stage", ev["url"])

    def test_empty_recap_keeps_existing_fallback(self):
        for recap in (None, ""):
            output = render.render_record_row(event(recap_url=recap))
            self.assertIn('href="https://example.org/stage"', output)

    def test_recap_url_is_escaped(self):
        output = render.render_record_row(event(recap_url='https://kriskrug.co/?a="&b=2'))
        self.assertIn('href="https://kriskrug.co/?a=&quot;&amp;b=2"', output)

    def test_recap_rejects_unsafe_or_noncanonical_destinations(self):
        for url in ("javascript:alert(1)", "//example.org/", "/recap/", "https://kriskrug.co.evil.test/", True):
            with self.subTest(url=url), self.assertRaises(ValueError):
                render.render_record_row(event(recap_url=url))


class LocalPathsNeverShip(unittest.TestCase):
    """Guard: no file:// or /Users/ src ever reaches the shipped output."""

    def hero_on_disk(self, tmp: str) -> Path:
        path = Path(tmp) / "hero.jpg"
        path.write_bytes(b"jpeg-bytes")
        return path

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

    def test_local_only_hero_gets_no_tile_and_still_appears_in_the_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            ev = event(id="local-1", image={"path": "kk_kb:hero.jpg", "alt": "Night shot"})
            html = block([], [ev], roots=roots_for(Path(tmp)))
            self.assertNotIn("file://", html)
            self.assertNotIn("/Users/", html)
            self.assertEqual(len(TILE_RE.findall(html)), 0)
            self.assertIn('data-event-id="local-1"', html)

    def test_dynamic_block_with_local_heroes_ships_no_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.hero_on_disk(tmp)
            upcoming = [event(id="up-1", image={"path": "kk_kb:hero.jpg"})]
            past = [event(id="past-1", image={"path": "repo:hero.jpg"})]
            html = block(upcoming, past, roots=roots_for(Path(tmp)))
            self.assertNotIn("file://", html)
            self.assertNotIn("/Users/", html)

    def test_public_url_still_renders_an_img(self):
        ev = event(image={"url": "https://kriskrug.co/wp-content/x.jpg", "alt": "Hero"})
        html = render.render_tile(ev, roots_for(Path(".")), upcoming=False)
        self.assertIn('src="https://kriskrug.co/wp-content/x.jpg"', html)

    def test_media_id_without_url_is_not_art(self):
        """A bare media_id used to emit src="#media-NNNN", which the browser
        resolves as a broken image and paints as an empty frame on the sheet.
        Only a real URL counts as art now; sync_event_media.py fills in the URL."""
        ev = event(image={"media_id": 12660, "alt": "Pitch Night"})
        self.assertEqual(render.image_src(ev, roots_for(Path(".")))[0], "")
        self.assertFalse(render.has_art(ev, roots_for(Path("."))))
        html = block([], [ev])
        self.assertNotIn("#media-12660", html)
        self.assertEqual(len(TILE_RE.findall(html)), 0)


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
        stale = event(id="u3", bucket_hint="upcoming", end="2025-01-01T21:00:00-08:00")
        self.assertTrue(render.is_past(stale, self.NOW))

    def test_date_only_event_ends_at_2100_pacific(self):
        parsed = render.parse_end({"date": "2026-03-04"})
        self.assertEqual(parsed.hour, 21)
        self.assertEqual(parsed.tzinfo, render.PT)

    def test_unparseable_date_yields_an_empty_end(self):
        self.assertIsNone(render.parse_end({"date": "sometime in spring"}))
        self.assertEqual(render.end_iso({"date": "sometime in spring"}), "")

    def test_spotlight_precedes_the_sheet_which_precedes_the_record(self):
        art = {"url": "https://kriskrug.co/x.jpg"}
        upcoming = [event(id="up-1", image=art)]
        past = [event(id="past-1", image=art)]
        html = block(upcoming, past)
        self.assertLess(
            html.index('data-events-grid="upcoming">'),
            html.index('data-events-grid="sheet">'),
        )
        # Needles must be markup-unique; the class names also appear in the CSS.
        self.assertLess(
            html.index('data-events-grid="sheet">'),
            html.index('<div class="kk-ev-record-grid">'),
        )

    def test_upcoming_is_held_back_from_the_sheet_until_it_rolls_off(self):
        art = {"url": "https://kriskrug.co/x.jpg"}
        html = block([event(id="up-1", image=art)], [event(id="past-1", image=art)])
        self.assertIn('data-event-id="up-1" data-tile-upcoming="true"', html)
        self.assertNotIn('data-event-id="past-1" data-tile-upcoming="true"', html)

    def test_empty_upcoming_is_flagged_for_the_collapse_css(self):
        html = block([], [event(id="past-1")])
        self.assertIn('data-events-bucket="upcoming" data-events-empty="true"', html)


class CardContract(unittest.TestCase):
    """Class names and data attributes the CSS and rolloff script select on."""

    def test_spotlight_card_classes(self):
        html = render.render_next_card(event(), roots_for(Path(".")))
        self.assertIn('<article class="kk-ev-next"', html)
        self.assertIn('data-event-id="ev-1"', html)

    def test_tile_classes(self):
        ev = event(image={"url": "https://kriskrug.co/x.jpg"})
        html = render.render_tile(ev, roots_for(Path(".")), upcoming=False)
        self.assertIn('<article class="kk-ev-tile"', html)
        self.assertIn("kk-ev-tile-info", html)

    def test_every_rendered_element_carries_data_event_end(self):
        art = {"url": "https://kriskrug.co/x.jpg"}
        upcoming = [event(id="up-1", image=art)]
        past = [event(id="past-1", end="2025-01-15T21:00:00-08:00", image=art)]
        html = block(upcoming, past)
        # one spotlight + two tiles + two record rows
        self.assertEqual(len(NEXT_RE.findall(html)), 1)
        self.assertEqual(len(TILE_RE.findall(html)), 2)
        self.assertEqual(len(REC_RE.findall(html)), 2)
        self.assertEqual(len(CARD_END_RE.findall(html)), 5)

    def test_data_event_end_is_tz_aware_iso(self):
        html = render.render_next_card(
            event(end="2026-05-05T18:00:00-07:00"), roots_for(Path("."))
        )
        value = CARD_END_RE.search(html).group(1)
        self.assertEqual(datetime.fromisoformat(value).utcoffset(), timedelta(hours=-7))

    def test_undated_row_still_emits_the_attribute(self):
        self.assertIn('data-event-end=""', render.render_record_row({"id": "u1"}))

    def test_spotlight_carries_its_registration_cta(self):
        html = render.render_next_card(event(), roots_for(Path(".")))
        self.assertIn(">Register<", html)
        self.assertIn('href="https://example.org/stage"', html)


class Escaping(unittest.TestCase):
    def test_title_with_markup_characters_is_escaped(self):
        ev = event(title='Rooms & <Stages> "2026"')
        heading = H3_RE.search(render.render_next_card(ev, roots_for(Path(".")))).group(1)
        self.assertEqual(heading, "Rooms &amp; &lt;Stages&gt; &quot;2026&quot;")

    def test_tile_title_is_escaped(self):
        ev = event(title="Rooms & <Stages>", image={"url": "https://kriskrug.co/x.jpg"})
        html = render.render_tile(ev, roots_for(Path(".")), upcoming=False)
        self.assertIn("Rooms &amp; &lt;Stages&gt;", html)
        self.assertNotIn("<Stages>", html)

    def test_record_row_title_is_escaped(self):
        html = render.render_record_row(event(title='Rooms & <Stages>'))
        self.assertIn("Rooms &amp; &lt;Stages&gt;", html)

    def test_alt_text_cannot_break_out_of_the_attribute(self):
        ev = event(image={"url": "https://kriskrug.co/x.jpg", "alt": 'A "quoted" hero'})
        html = render.render_tile(ev, roots_for(Path(".")), upcoming=False)
        self.assertIn('alt="A &quot;quoted&quot; hero"', html)

    def test_url_is_escaped(self):
        ev = event(url='https://example.org/?a=1&b="2"')
        html = render.render_next_card(ev, roots_for(Path(".")))
        self.assertIn('href="https://example.org/?a=1&amp;b=&quot;2&quot;"', html)

    def test_photographer_credit_folds_into_alt_and_shows_on_the_tile(self):
        ev = event(
            image={
                "url": "https://kriskrug.co/x.jpg",
                "alt": "Meetup floor",
                "photographer": "Michelle Diamond",
            }
        )
        _, alt = render.image_src(ev, roots_for(Path(".")))
        self.assertEqual(alt, "Meetup floor (photo: Michelle Diamond)")
        html = render.render_tile(ev, roots_for(Path(".")), upcoming=False)
        self.assertIn('<span class="kk-ev-tile-credit">Michelle Diamond</span>', html)


class ArtworkPolicy(unittest.TestCase):
    """The sheet shows real art only. Nothing is generated to fill a gap."""

    def test_no_art_means_no_tile(self):
        html = block([], [event(id="bare-1", image={})])
        self.assertEqual(len(TILE_RE.findall(html)), 0)
        self.assertNotIn("<img", html)

    def test_no_art_event_is_still_in_the_record(self):
        html = block([], [event(id="bare-1", image={})])
        self.assertIn('data-event-id="bare-1"', html)
        self.assertEqual(len(REC_RE.findall(html)), 1)

    def test_no_generated_poster_markup_survives_anywhere(self):
        html = block([event(id="up-1")], [event(id="past-1")])
        for gone in ("aurora-event-art--generated", "aurora-event-art-mark", "palette-"):
            self.assertNotIn(gone, html)

    def test_spotlight_without_art_uses_the_date_not_an_empty_frame(self):
        html = render.render_next_card(event(image={}), roots_for(Path(".")))
        self.assertNotIn("<img", html)
        self.assertIn("kk-ev-next-art--bare", html)
        self.assertIn("kk-ev-next-day", html)

    def test_record_row_without_a_url_emits_no_link(self):
        html = render.render_record_row(event(url=""))
        self.assertNotIn("<a ", html)
        self.assertIn("Example Stage", html)


class RealCatalogSmoke(unittest.TestCase):
    """Real merged catalog renders one record row per publishable event."""

    def render_main(self, out: Path) -> str:
        argv = sys.argv
        sys.argv = ["render_events_page.py", "--out", str(out)]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                code = render.main()
        finally:
            sys.argv = argv
            render.PREVIEW_LOCAL = False
        self.assertEqual(code, 0)
        return out.read_text(encoding="utf-8")

    def test_real_catalog_records_every_publishable_event_once(self):
        doc = lib.load_catalog()
        publishable = [e for e in doc["events"] if render.public_status(e)]
        self.assertTrue(publishable, "catalog should have publishable events")
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")

        self.assertEqual(
            sorted(REC_ID_RE.findall(html)), sorted(e["id"] for e in publishable)
        )
        withheld = {e["id"] for e in doc["events"]} - {e["id"] for e in publishable}
        for eid in withheld:
            self.assertNotIn(f'data-event-id="{eid}"', html)

    def test_every_sheet_tile_has_a_real_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        tiles = re.findall(r'<article class="kk-ev-tile".*?</article>', html, re.S)
        self.assertTrue(tiles, "catalog should have at least one event with art")
        for tile in tiles:
            src = re.search(r'<img src="([^"]*)"', tile)
            self.assertIsNotNone(src, "a tile must carry an img")
            self.assertTrue(src.group(1).startswith("http"), src.group(1))

    def test_real_render_includes_the_accessible_sheet_toggle(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertIn("data-events-sheet-toggle", html)
        self.assertIn('aria-expanded="false"', html)

    def test_real_render_carries_no_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        self.assertNotIn("file://", html)
        self.assertNotIn("/Users/", html)
        self.assertNotIn('src=""', html)
        self.assertNotIn('src="heroes/', html)

    def test_real_render_gives_every_element_a_usable_rolloff_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = self.render_main(Path(tmp) / "events-2250.generated.html")
        for value in CARD_END_RE.findall(html):
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
        self.assertIn('data-events-grid="sheet">', html)
        self.assertIn("kk-ev-rooms", html)
        self.assertIn("kk-ev-cta", html)


if __name__ == "__main__":
    unittest.main()
