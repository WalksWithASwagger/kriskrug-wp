"""#592 fragment loader: merge-by-id override, append, duplicate-id error.

Offline. Unit tests drive load_fragments/merge_fragments with temp fixtures;
the integration test loads the real repo catalog + fragments with the harvest
index and asserts the 2026 hero-override rows merged instead of appending.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/events_page"))

import lib  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class LoadFragments(unittest.TestCase):
    def test_missing_dir_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(lib.load_fragments(Path(tmp) / "nope"), [])

    def test_sorted_by_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            frag_dir = Path(tmp)
            write(frag_dir / "b-later.yaml", "events:\n- id: b1\n")
            write(frag_dir / "a-earlier.yaml", "events:\n- id: a1\n")
            names = [name for name, _ in lib.load_fragments(frag_dir)]
            self.assertEqual(names, ["a-earlier.yaml", "b-later.yaml"])

    def test_non_dict_doc_and_missing_events_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            frag_dir = Path(tmp)
            write(frag_dir / "list.yaml", "- not\n- a-dict-doc\n")
            write(frag_dir / "noevents.yaml", "fragment: x\n")
            fragments = lib.load_fragments(frag_dir)
            self.assertEqual(fragments, [("noevents.yaml", [])])


class MergeById(unittest.TestCase):
    def core(self):
        return [
            {
                "id": "channelnext-2025",
                "title": "ChannelNext",
                "date": "2025-06-03",
                "end": "2025-06-03T18:00:00-07:00",
                "kind": "one-off",
                "role": "Keynote",
                "url": "https://www.youtube.com/watch?v=1OcC-0X6Nb8",
                "blurb": "Core blurb stays.",
                "status": "confirmed",
                "bucket_hint": "past",
                "image": {},
                "tags": ["Keynote"],
            }
        ]

    def test_image_only_fragment_overrides_core_record_not_append(self):
        fragments = [
            (
                "one-offs-2026.yaml",
                [
                    {
                        "id": "channelnext-2025",
                        "image": {
                            "path": "repo:thumbs/channel-next.jpg",
                            "alt": "ChannelNext keynote thumb",
                        },
                    }
                ],
            )
        ]
        merged = lib.merge_fragments(self.core(), fragments)
        self.assertEqual(len(merged), 1)
        event = merged[0]
        self.assertEqual(event["image"]["path"], "repo:thumbs/channel-next.jpg")
        self.assertEqual(event["image"]["alt"], "ChannelNext keynote thumb")
        # Non-image core fields survive the image-only patch.
        self.assertEqual(event["title"], "ChannelNext")
        self.assertEqual(event["blurb"], "Core blurb stays.")
        self.assertEqual(event["end"], "2025-06-03T18:00:00-07:00")

    def test_empty_fragment_values_never_clobber_core(self):
        fragments = [
            (
                "f.yaml",
                [
                    {
                        "id": "channelnext-2025",
                        "title": "",
                        "url": None,
                        "tags": [],
                        "image": {},
                        "blurb": "Fragment blurb wins.",
                    }
                ],
            )
        ]
        merged = lib.merge_fragments(self.core(), fragments)
        event = merged[0]
        self.assertEqual(event["title"], "ChannelNext")
        self.assertEqual(event["url"], "https://www.youtube.com/watch?v=1OcC-0X6Nb8")
        self.assertEqual(event["tags"], ["Keynote"])
        self.assertEqual(event["blurb"], "Fragment blurb wins.")

    def test_image_dict_merges_key_by_key(self):
        core = self.core()
        core[0]["image"] = {"media_id": 12660, "alt": "Core alt"}
        fragments = [
            ("f.yaml", [{"id": "channelnext-2025", "image": {"path": "repo:x.jpg"}}])
        ]
        merged = lib.merge_fragments(core, fragments)
        self.assertEqual(
            merged[0]["image"],
            {"media_id": 12660, "alt": "Core alt", "path": "repo:x.jpg"},
        )

    def test_new_ids_append_in_fragment_file_order(self):
        fragments = [
            (
                "one-offs-2024.yaml",
                [
                    {
                        "id": "innovate-west-keynote-2024",
                        "title": "Innovate West",
                        "date": "2024-04-20",
                        "bucket_hint": "past",
                        "kind": "one-off",
                        "status": "confirmed",
                    }
                ],
            ),
            (
                "one-offs-2025.yaml",
                [{"id": "2025-10-24-munda-mennuie-residency", "date": "2025-10-24"}],
            ),
        ]
        merged = lib.merge_fragments(self.core(), fragments)
        self.assertEqual(
            [e["id"] for e in merged],
            [
                "channelnext-2025",
                "innovate-west-keynote-2024",
                "2025-10-24-munda-mennuie-residency",
            ],
        )
        appended = merged[2]
        # Appended rows are normalized with the catalog defaults.
        self.assertEqual(appended["status"], "confirmed")
        self.assertEqual(appended["bucket_hint"], "past")
        self.assertEqual(appended["image"], {})

    def test_duplicate_id_across_fragments_is_an_error(self):
        fragments = [
            ("a.yaml", [{"id": "dup-1", "title": "First"}]),
            ("b.yaml", [{"id": "dup-1", "title": "Second"}]),
        ]
        with self.assertRaises(SystemExit) as ctx:
            lib.merge_fragments([], fragments)
        message = str(ctx.exception)
        self.assertIn("dup-1", message)
        self.assertIn("a.yaml", message)
        self.assertIn("b.yaml", message)

    def test_duplicate_id_within_one_fragment_is_an_error(self):
        fragments = [
            ("a.yaml", [{"id": "dup-2"}, {"id": "dup-2"}]),
        ]
        with self.assertRaises(SystemExit):
            lib.merge_fragments([], fragments)

    def test_fragment_event_without_id_is_an_error(self):
        with self.assertRaises(SystemExit):
            lib.merge_fragments([], [("a.yaml", [{"title": "No id"}])])


class LoadCatalogWiring(unittest.TestCase):
    def setUp(self):
        self._editions_path = lib.MEETUP_EDITIONS_PATH
        # Keep the temp-catalog tests hermetic from the repo harvest index.
        lib.MEETUP_EDITIONS_PATH = Path(tempfile.gettempdir()) / "no-such-editions.yaml"
        self.addCleanup(setattr, lib, "MEETUP_EDITIONS_PATH", self._editions_path)

    def test_fragments_merge_into_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            catalog = base / "catalog.yaml"
            write(
                catalog,
                "events:\n"
                "- id: core-1\n"
                "  title: Core One\n"
                "  date: '2026-01-01'\n"
                "  image: {}\n",
            )
            frag_dir = base / "fragments"
            write(
                frag_dir / "one.yaml",
                "events:\n"
                "- id: core-1\n"
                "  image:\n"
                "    path: repo:hero.jpg\n"
                "- id: frag-1\n"
                "  title: Fragment One\n"
                "  date: '2026-02-02'\n",
            )
            doc = lib.load_catalog(catalog, fragments_dir=frag_dir)
            self.assertEqual(doc["_fragments_merged"], ["one.yaml"])
            self.assertEqual([e["id"] for e in doc["events"]], ["core-1", "frag-1"])
            self.assertEqual(doc["events"][0]["image"]["path"], "repo:hero.jpg")
            self.assertEqual(doc["events"][0]["title"], "Core One")

    def test_no_fragments_dir_keeps_catalog_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            catalog = base / "catalog.yaml"
            write(catalog, "events:\n- id: core-1\n  title: Core One\n")
            doc = lib.load_catalog(catalog, fragments_dir=base / "missing")
            self.assertEqual(doc["_fragments_merged"], [])
            self.assertEqual([e["id"] for e in doc["events"]], ["core-1"])


HERO_OVERRIDE_IDS = [
    "creativemornings-perils-parallels-2026",
    "waiff-sao-paulo-2026",
    "lasalle-college-keynote-2026",
    "channelnext-2025",
    "whistler-institute-2025",
]


class RealCatalogIntegration(unittest.TestCase):
    """Real repo data: fragments must enrich, never duplicate."""

    def test_real_catalog_merges_fragments_without_duplicates(self):
        doc = lib.load_catalog()
        ids = [e["id"] for e in doc["events"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate event ids after merge")
        self.assertEqual(
            doc["_fragments_merged"],
            sorted(doc["_fragments_merged"]),
        )
        self.assertIn("one-offs-2026.yaml", doc["_fragments_merged"])
        by_id = {e["id"]: e for e in doc["events"]}
        for eid in HERO_OVERRIDE_IDS:
            self.assertEqual(ids.count(eid), 1)
            event = by_id[eid]
            image = event.get("image") or {}
            self.assertTrue(
                image.get("path") or image.get("media_id"),
                f"{eid} should carry a hero after the fragment merge",
            )
            # Override rows are image patches: the core title/blurb survive.
            self.assertTrue(event.get("title"))
            self.assertTrue(event.get("blurb"))


if __name__ == "__main__":
    unittest.main()
