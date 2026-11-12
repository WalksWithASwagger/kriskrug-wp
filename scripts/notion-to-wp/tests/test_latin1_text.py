"""Text above U+00FF reaches kriskrug.co as numeric references or not at all (#1225).

The database is latin1, so a raw character above U+00FF comes back as "?".
Offline only: fakes stand in for WordPress and Notion.
"""

import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from urllib.parse import urlsplit

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402
from latin1_text import (  # noqa: E402
    NonLatin1Text,
    assert_latin1,
    latin1_payload,
    plain_meta_text,
    to_ncr,
)
from test_run_order import (  # noqa: E402
    PAGE_ID,
    FakeNotion,
    FakeWordPress,
    notion_blocks,
)
from update_safety import readback_mismatches  # noqa: E402
from wp_client import WordPress  # noqa: E402

ETHOS = "Eth\u1ecd\u0301s"  # o with dot below + combining acute accent
ETHOS_NCR = "Eth&#7885;&#769;s"


def above_latin1(value) -> list[str]:
    if isinstance(value, str):
        return [ch for ch in value if ord(ch) > 0xFF]
    if isinstance(value, dict):
        return [ch for item in value.values() for ch in above_latin1(item)]
    if isinstance(value, (list, tuple)):
        return [ch for item in value for ch in above_latin1(item)]
    return []


def stored_as_latin1(value):
    """What the latin1 database keeps: every character above U+00FF becomes '?'."""
    if isinstance(value, str):
        return "".join(ch if ord(ch) <= 0xFF else "?" for ch in value)
    if isinstance(value, dict):
        return {key: stored_as_latin1(item) for key, item in value.items()}
    if isinstance(value, list):
        return [stored_as_latin1(item) for item in value]
    return value


class FakeResponse:
    status_code = 200

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body

    def raise_for_status(self):
        pass


class FakeLatin1Site:
    """The REST API over a latin1 database, as a WordPress session stand-in."""

    def __init__(self):
        self.json_bodies = []
        self.posts = {}
        self.media = {}

    def get(self, url, params=None, timeout=None):
        path = urlsplit(url).path
        if re.search(r"/posts/\d+$", path):
            return FakeResponse(self.posts[int(path.rsplit("/", 1)[1])])
        return FakeResponse([])  # slug lookups and term searches find nothing

    def post(self, url, json=None, data=None, headers=None, timeout=None):
        path = urlsplit(url).path
        if json is not None:
            self.json_bodies.append((path, json))
            json = stored_as_latin1(json)
        if path.endswith("/media"):
            self.media[501] = {"id": 501, "source_url": "https://wp.example.test/uploads/hero.jpg"}
            return FakeResponse(self.media[501])
        if "/media/" in path:
            media = self.media[int(path.rsplit("/", 1)[1])]
            media.update(json)
            return FakeResponse(media)
        if path.endswith(("/categories", "/tags")):
            return FakeResponse({"id": 900 + len(self.json_bodies), **json})
        post_id = 701 if path.endswith("/posts") else int(path.rsplit("/", 1)[1])
        self.posts[post_id] = {
            "id": post_id,
            "link": f"https://wp.example.test/?p={post_id}",
            "title": {"raw": json["title"]},
            "content": {"raw": json.get("content", "")},
            "slug": json["slug"],
            "status": json["status"],
            "date": json["date"],
            "date_gmt": json["date"],
            "meta": dict(json.get("meta") or {}),
        }
        return FakeResponse(self.posts[post_id])


def wordpress_over(site) -> WordPress:
    wp = WordPress("https://wp.example.test", "fake-user", "fake-app-password")
    wp.s = site
    return wp


class ToNcrTests(unittest.TestCase):
    def test_non_latin1_characters_become_decimal_references(self):
        self.assertEqual(to_ncr(f"<p>{ETHOS} Lab</p>"), f"<p>{ETHOS_NCR} Lab</p>")
        self.assertEqual(to_ncr("draft → live"), "draft &#8594; live")
        self.assertEqual(to_ncr("KK’s notes…"), "KK&#8217;s notes&#8230;")

    def test_latin1_text_is_left_byte_for_byte(self):
        for text in ("Krüg", "café", "Kris Krüg × Café · ½ ©", "plain ASCII"):
            with self.subTest(text=text):
                self.assertEqual(to_ncr(text).encode("utf-8"), text.encode("utf-8"))

    def test_existing_entities_are_not_double_encoded(self):
        text = f"{ETHOS_NCR} &amp; &#x2192; &rarr; Kr&#252;g"
        self.assertEqual(to_ncr(text), text)
        self.assertEqual(to_ncr(to_ncr(f"{ETHOS} →")), to_ncr(f"{ETHOS} →"))


class PlainMetaTextTests(unittest.TestCase):
    def test_latin1_text_is_left_byte_for_byte(self):
        for text in ("Kris Krüg", "Café Krüg", "Plain ASCII"):
            with self.subTest(text=text):
                self.assertEqual(plain_meta_text(text, "SEO title").encode("utf-8"), text.encode("utf-8"))

    def test_decomposed_accents_are_composed_into_latin1(self):
        self.assertEqual(plain_meta_text("Cafe\u0301 Kru\u0308g", "SEO title"), "Café Krüg")

    def test_typographic_punctuation_folds_to_ascii(self):
        self.assertEqual(
            plain_meta_text("KK’s “take” – 2024–2026…", "SEO description"),
            "KK's \"take\" - 2024-2026...",
        )

    def test_combining_marks_raise(self):
        with self.assertRaisesRegex(NonLatin1Text, r"SEO title .*U\+0301 COMBINING ACUTE ACCENT.*HTTP 500"):
            plain_meta_text(f"{ETHOS} Lab", "SEO title")

    def test_other_characters_above_latin1_raise_without_blaming_combining_marks(self):
        with self.assertRaises(NonLatin1Text) as caught:
            plain_meta_text("draft → live — now", "Publicize message")
        message = str(caught.exception)
        self.assertIn("U+2192 RIGHTWARDS ARROW", message)
        self.assertIn("U+2014 EM DASH", message)
        self.assertNotIn("HTTP 500", message)


class Latin1PayloadTests(unittest.TestCase):
    def test_html_fields_are_encoded_and_the_rest_left_alone(self):
        payload = {
            "title": f"{ETHOS} Lab",
            "content": "<p>draft → live, Krüg</p>",
            "excerpt": "KK’s notes",
            "alt_text": f"{ETHOS} stage",
            "caption": "→",
            "description": "→",
            "name": "KK’s tag",
            "slug": "ethos-lab",
            "status": "draft",
            "meta": {"jetpack_seo_html_title": "Ethos Lab | Kris Krüg"},
        }

        body = latin1_payload(payload)

        self.assertEqual(body["title"], f"{ETHOS_NCR} Lab")
        self.assertEqual(body["content"], "<p>draft &#8594; live, Krüg</p>")
        self.assertEqual(body["excerpt"], "KK&#8217;s notes")
        self.assertEqual(body["alt_text"], f"{ETHOS_NCR} stage")
        self.assertEqual(body["caption"], "&#8594;")
        self.assertEqual(body["description"], "&#8594;")
        self.assertEqual(body["name"], "KK&#8217;s tag")
        self.assertEqual(body["meta"], payload["meta"])
        self.assertEqual(payload["title"], f"{ETHOS} Lab", "the caller's payload is not mutated")

    def test_raw_text_left_in_any_other_field_is_refused(self):
        with self.assertRaisesRegex(NonLatin1Text, r"payload\.meta\.jetpack_seo_html_title"):
            latin1_payload({"title": "ok", "meta": {"jetpack_seo_html_title": f"{ETHOS} Lab"}})
        with self.assertRaisesRegex(NonLatin1Text, r"payload\.tags\[1\]"):
            assert_latin1({"tags": ["ok", "→"]})


class ClientWireTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"DRY_RUN": ""})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_create_post_sends_references_for_post_text_fields(self):
        site = FakeLatin1Site()
        payload = {
            "title": f"{ETHOS} Lab",
            "slug": "ethos-lab",
            "status": "draft",
            "date": "2026-06-23T12:00:00",
            "excerpt": f"About {ETHOS} → Krüg",
            "content": f"<p>{ETHOS} → café</p>",
            "meta": {"jetpack_seo_html_title": "Ethos Lab | Kris Krüg"},
        }

        wordpress_over(site).create_post(payload)

        [(path, body)] = site.json_bodies
        self.assertTrue(path.endswith("/posts"))
        self.assertEqual(above_latin1(body), [])
        self.assertEqual(body["title"], f"{ETHOS_NCR} Lab")
        self.assertEqual(body["excerpt"], f"About {ETHOS_NCR} &#8594; Krüg")
        self.assertEqual(body["content"], f"<p>{ETHOS_NCR} &#8594; café</p>")
        self.assertEqual(body["meta"], payload["meta"])

    def test_raw_meta_is_refused_before_any_request(self):
        site = mock.Mock()
        wp = wordpress_over(site)
        payload = {"title": "Ok", "slug": "ok", "meta": {"advanced_seo_description": f"{ETHOS}"}}

        with self.assertRaises(NonLatin1Text):
            wp.create_post(payload)
        with self.assertRaises(NonLatin1Text):
            wp.update_post(1, payload, expected_slug="ok")

        site.get.assert_not_called()
        site.post.assert_not_called()

    def test_media_alt_text_and_term_names_are_sent_as_references(self):
        site = FakeLatin1Site()
        wp = wordpress_over(site)

        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "hero.jpg"
            image.write_bytes(b"jpeg fixture")
            wp.upload_media(image, alt=f"{ETHOS} on stage", caption="Krüg → café")
        wp.ensure_term("tags", "KK’s Picks")

        bodies = dict(site.json_bodies)
        self.assertEqual(bodies["/wp-json/wp/v2/media/501"]["alt_text"], f"{ETHOS_NCR} on stage")
        self.assertEqual(bodies["/wp-json/wp/v2/media/501"]["caption"], "Krüg &#8594; café")
        self.assertEqual(bodies["/wp-json/wp/v2/tags"], {"name": "KK&#8217;s Picks", "slug": "kks-picks"})


class ReadbackTests(unittest.TestCase):
    """update_safety compares the sent title with title.raw after html.unescape (#1218)."""

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"DRY_RUN": ""})
        patcher.start()
        self.addCleanup(patcher.stop)

    def payload(self, title):
        return {"title": title, "slug": "ethos-lab", "status": "draft", "date": "2026-06-23T12:00:00"}

    def test_title_sent_as_references_reads_back_as_a_match(self):
        site = FakeLatin1Site()
        wp = wordpress_over(site)
        payload = self.payload(f"{ETHOS} Lab → KK’s")

        created = wp.create_post(payload)
        readback = wp.get_post(created["id"])

        self.assertEqual(readback["title"]["raw"], f"{ETHOS_NCR} Lab &#8594; KK&#8217;s")
        self.assertEqual(readback_mismatches(payload, readback), {})

    def test_title_corrupted_to_question_marks_is_still_a_mismatch(self):
        site = FakeLatin1Site()
        payload = self.payload(f"{ETHOS} Lab")
        # The pre-#1225 behaviour: the raw title goes straight onto the wire.
        site.post("https://wp.example.test/wp-json/wp/v2/posts", json=payload)
        readback = wordpress_over(site).get_post(701)

        self.assertEqual(readback["title"]["raw"], "Eth??s Lab")
        self.assertEqual(
            readback_mismatches(payload, readback),
            {"title": (f"{ETHOS} Lab", "Eth??s Lab")},
        )


class CaptionedNotion(FakeNotion):
    def block_children(self, page_id):
        blocks = notion_blocks()
        blocks[1]["image"]["caption"] = [{"plain_text": f"{ETHOS} Lab → main stage"}]
        return blocks


class ConnectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        cfg = SimpleNamespace(
            notion_token="fake-notion-token",
            wp_base_url="https://wp.example.test",
            wp_user="fake-user",
            wp_app_password="fake-app-password",
            wp_author_id=1,
            has_wp_credentials=True,
        )

        def fake_download(url, dest):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(b"not really a jpeg")
            return dest.stat().st_size

        for target, name, value in [
            (kk_notion_to_wp, "load_config", lambda: cfg),
            (kk_notion_to_wp, "Notion", CaptionedNotion),
            (kk_notion_to_wp, "download_image", fake_download),
            (kk_notion_to_wp, "DRAFTS_DIR", self.tmp / "drafts"),
            (kk_notion_to_wp, "REPO_ROOT", self.tmp),
        ]:
            patcher = mock.patch.object(target, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(os.environ, {"DRY_RUN": ""})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_connector(self, wp, **kwargs):
        logs = io.StringIO()
        with mock.patch.object(kk_notion_to_wp, "WordPress", lambda *a, **k: wp):
            with contextlib.redirect_stdout(logs):
                code = kk_notion_to_wp.run(
                    f"https://www.notion.so/Calling-{PAGE_ID}",
                    force_publish=False,
                    **kwargs,
                )
        return code, logs.getvalue()

    def test_title_the_seo_meta_cannot_carry_exits_9_before_any_request(self):
        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run):
                wp = FakeWordPress()

                code, logs = self.run_connector(
                    wp, dry_run=dry_run, title_override=f"{ETHOS} Lab Block Party"
                )

                self.assertEqual(code, 9)
                self.assertEqual(wp.calls, [])
                self.assertIn("SEO title has characters the latin1 database cannot store", logs)
                self.assertIn("No WP write was attempted.", logs)

    def test_create_sends_no_raw_character_above_latin1_and_reads_back_clean(self):
        site = FakeLatin1Site()

        code, logs = self.run_connector(
            wordpress_over(site), dry_run=False, title_override="KK’s Field Notes"
        )

        self.assertEqual(code, 0, logs)
        self.assertEqual([ch for _, body in site.json_bodies for ch in above_latin1(body)], [])
        post = site.posts[701]
        self.assertEqual(post["title"]["raw"], "KK&#8217;s Field Notes")
        self.assertIn(f"{ETHOS_NCR} Lab &#8594; main stage", post["content"]["raw"])
        self.assertEqual(post["meta"]["jetpack_seo_html_title"], "KK's Field Notes | Kris Krüg")
        self.assertEqual(site.media[501]["alt_text"], f"{ETHOS_NCR} Lab &#8594; main stage")


if __name__ == "__main__":
    unittest.main()
