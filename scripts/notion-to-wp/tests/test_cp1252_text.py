"""Text outside cp1252 reaches kriskrug.co as numeric references or not at all (#1225).

The database's "latin1" is MySQL's cp1252, so curly quotes and dashes are stored
as sent and anything else above U+00FF comes back as "?".
Offline only: fakes stand in for WordPress and Notion.
"""

import contextlib
import difflib
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

import yaml

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402
from cp1252_text import (  # noqa: E402
    UnstorableText,
    assert_storable,
    derived_meta_text,
    encode_html,
    plain_meta_text,
    storable_payload,
    to_ncr,
)
from test_run_order import (  # noqa: E402
    PAGE_ID,
    FakeNotion,
    FakeWordPress,
    notion_blocks,
)
from update_safety import readback_mismatches, update_title_guard  # noqa: E402
from wp_client import WordPress  # noqa: E402

ETHOS = "Eth\u1ecd\u0301s"  # o with dot below + combining acute accent
ETHOS_NCR = "Eth&#7885;&#769;s"
CP1252_PUNCTUATION = "KK’s “take” ‘yes’ – — … • € ™"


def unstorable(value) -> list[str]:
    if isinstance(value, str):
        out = []
        for ch in value:
            try:
                ch.encode("cp1252")
            except UnicodeEncodeError:
                out.append(ch)
        return out
    if isinstance(value, dict):
        return [ch for item in value.values() for ch in unstorable(item)]
    if isinstance(value, (list, tuple)):
        return [ch for item in value for ch in unstorable(item)]
    return []


def stored_as_cp1252(value):
    """What the database keeps: every character outside cp1252 becomes '?'."""
    if isinstance(value, str):
        return "".join("?" if unstorable(ch) else ch for ch in value)
    if isinstance(value, dict):
        return {key: stored_as_cp1252(item) for key, item in value.items()}
    if isinstance(value, list):
        return [stored_as_cp1252(item) for item in value]
    return value


class FakeResponse:
    status_code = 200

    def __init__(self, body):
        self.body = body

    def json(self):
        return self.body

    def raise_for_status(self):
        pass


class FakeCp1252Site:
    """The REST API over the cp1252 database, as a WordPress session stand-in."""

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
            json = stored_as_cp1252(json)
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


class WritesAllowed(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"DRY_RUN": ""})
        patcher.start()
        self.addCleanup(patcher.stop)


class ToNcrTests(unittest.TestCase):
    def test_characters_outside_cp1252_become_decimal_references(self):
        self.assertEqual(to_ncr(f"<p>{ETHOS} Lab</p>"), f"<p>{ETHOS_NCR} Lab</p>")
        self.assertEqual(to_ncr("draft → live 🙂"), "draft &#8594; live &#128578;")

    def test_cp1252_text_is_left_byte_for_byte(self):
        for text in ("Krüg", "café", "Kris Krüg × Café · ½ ©", CP1252_PUNCTUATION, "plain ASCII"):
            with self.subTest(text=text):
                self.assertEqual(to_ncr(text).encode("utf-8"), text.encode("utf-8"))

    def test_existing_entities_are_not_double_encoded(self):
        text = f"{ETHOS_NCR} &amp; &#x2192; &rarr; Kr&#252;g"
        self.assertEqual(to_ncr(text), text)
        self.assertEqual(to_ncr(to_ncr(f"{ETHOS} →")), to_ncr(f"{ETHOS} →"))

    def test_c1_control_characters_are_refused_not_encoded(self):
        # 0x81 is one of the five bytes cp1252 leaves undefined; 0x80 is the euro byte.
        for control in (chr(0x81), chr(0x80), chr(0x9D)):
            with self.subTest(control=hex(ord(control))):
                with self.assertRaisesRegex(UnstorableText, "C1 control"):
                    to_ncr(f"Kr{control}g")


class EncodeHtmlTests(unittest.TestCase):
    def test_style_and_script_bodies_are_left_as_written(self):
        html = (
            '<style>.q::before{content:"“";}</style>'
            '<p>→</p><script>var t = "’";</script><p>“→”</p>'
        )
        self.assertEqual(
            encode_html(html),
            '<style>.q::before{content:"“";}</style>'
            '<p>&#8594;</p><script>var t = "’";</script><p>“&#8594;”</p>',
        )

    def test_character_outside_cp1252_inside_style_or_script_is_refused(self):
        cases = {
            '<STYLE media="all">.a::after{content:"→"}</STYLE>': r"<style> .*U\+2192.*CSS escape",
            "<script>var arrow = '→';</script>": r"<script> .*JavaScript escape",
            "<p>ok</p><style>.a::after{content:'→'}": r"<style>",  # unclosed: still raw text
        }
        for html, message in cases.items():
            with self.subTest(html=html):
                with self.assertRaisesRegex(UnstorableText, message):
                    encode_html(html)

    def test_inline_style_attributes_are_encoded_because_browsers_decode_them(self):
        self.assertEqual(
            encode_html('<span style="content:\'→\'">x</span>'),
            '<span style="content:\'&#8594;\'">x</span>',
        )


class PlainMetaTextTests(unittest.TestCase):
    def test_cp1252_text_is_left_byte_for_byte(self):
        for text in ("Kris Krüg", "Café Krüg", CP1252_PUNCTUATION, "Plain ASCII"):
            with self.subTest(text=text):
                self.assertEqual(plain_meta_text(text, "SEO title").encode("utf-8"), text.encode("utf-8"))

    def test_decomposed_accents_are_composed(self):
        self.assertEqual(plain_meta_text("Cafe\u0301 Kru\u0308g", "SEO title"), "Café Krüg")

    def test_combining_marks_raise(self):
        with self.assertRaisesRegex(UnstorableText, r"SEO title .*U\+0301 COMBINING ACUTE ACCENT.*HTTP 500"):
            plain_meta_text(f"{ETHOS} Lab", "SEO title")

    def test_other_characters_outside_cp1252_raise_without_blaming_combining_marks(self):
        with self.assertRaises(UnstorableText) as caught:
            plain_meta_text("draft → live 🙂", "Publicize message")
        message = str(caught.exception)
        self.assertIn("U+2192 RIGHTWARDS ARROW", message)
        self.assertIn("U+1F642 SLIGHTLY SMILING FACE", message)
        self.assertNotIn("HTTP 500", message)

    def test_c1_control_characters_raise(self):
        with self.assertRaises(UnstorableText):
            plain_meta_text(f"Kr{chr(0x81)}g", "SEO title")


class DerivedMetaTextTests(unittest.TestCase):
    """Meta a writer derives folds to plain letters instead of refusing (KK, 2026-11-12)."""

    def test_characters_outside_cp1252_fold_with_one_warning(self):
        cases = {
            f"{ETHOS} Lab": "Ethos Lab",
            "Read this → now": "Read this now",
            "Notes 🙂 from the lab": "Notes from the lab",
            "Łódź field notes": "Lódz field notes",
        }
        for text, folded in cases.items():
            with self.subTest(text=text):
                warnings = []

                self.assertEqual(
                    derived_meta_text(text, "advanced_seo_description", warnings.append), folded
                )
                self.assertEqual(
                    warnings, [f'seo: folded advanced_seo_description: "{text}" -> "{folded}"']
                )

    def test_cp1252_text_is_never_touched_or_warned_about(self):
        for text in ("Kris Krüg", "Café Krüg × ½", CP1252_PUNCTUATION, "Krüg’s “notes” – 2025–2026…"):
            with self.subTest(text=text):
                warnings = []

                folded = derived_meta_text(text, "jetpack_seo_html_title", warnings.append)

                self.assertEqual(folded.encode("utf-8"), text.encode("utf-8"))
                self.assertEqual(warnings, [])

    def test_only_the_characters_cp1252_cannot_store_change(self):
        warnings = []

        folded = derived_meta_text(
            f"KK’s {ETHOS} – Krüg → Łódź 🙂", "jetpack_publicize_message", warnings.append
        )

        self.assertEqual(folded, "KK’s Ethos – Krüg Lódz")
        self.assertEqual(unstorable(folded), [])
        self.assertEqual(len(warnings), 1)


class StorablePayloadTests(unittest.TestCase):
    def test_html_fields_are_encoded_and_the_rest_left_alone(self):
        payload = {
            "title": f"{ETHOS} Lab",
            "content": "<p>draft → live, KK’s Krüg</p>",
            "excerpt": "KK’s notes →",
            "alt_text": f"{ETHOS} stage",
            "caption": "→",
            "description": "→",
            "name": f"{ETHOS} picks",
            "slug": "ethos-lab",
            "status": "draft",
            "meta": {"jetpack_seo_html_title": "Ethos Lab – KK’s | Kris Krüg"},
        }

        body = storable_payload(payload)

        self.assertEqual(body["title"], f"{ETHOS_NCR} Lab")
        self.assertEqual(body["content"], "<p>draft &#8594; live, KK’s Krüg</p>")
        self.assertEqual(body["excerpt"], "KK’s notes &#8594;")
        self.assertEqual(body["alt_text"], f"{ETHOS_NCR} stage")
        self.assertEqual(body["caption"], "&#8594;")
        self.assertEqual(body["description"], "&#8594;")
        self.assertEqual(body["name"], f"{ETHOS_NCR} picks")
        self.assertEqual(body["meta"], payload["meta"])
        self.assertEqual(payload["title"], f"{ETHOS} Lab", "the caller's payload is not mutated")

    def test_raw_text_left_in_any_other_field_is_refused(self):
        with self.assertRaisesRegex(UnstorableText, r"payload\.meta\.jetpack_seo_html_title"):
            storable_payload({"title": "ok", "meta": {"jetpack_seo_html_title": f"{ETHOS} Lab"}})
        with self.assertRaisesRegex(UnstorableText, r"payload\.tags\[1\]"):
            assert_storable({"tags": ["ok", "→"]})


class ClientWireTests(WritesAllowed):
    def test_create_post_sends_references_only_for_text_outside_cp1252(self):
        site = FakeCp1252Site()
        payload = {
            "title": f"{ETHOS} Lab – KK’s",
            "slug": "ethos-lab",
            "status": "draft",
            "date": "2026-06-23T12:00:00",
            "excerpt": f"About {ETHOS} → Krüg",
            "content": f'<style>.q::before{{content:"“"}}</style><p>{ETHOS} → café</p>',
            "meta": {"jetpack_seo_html_title": "Ethos Lab – KK’s | Kris Krüg"},
        }

        wordpress_over(site).create_post(payload)

        [(path, body)] = site.json_bodies
        self.assertTrue(path.endswith("/posts"))
        self.assertEqual(unstorable(body), [])
        self.assertEqual(body["title"], f"{ETHOS_NCR} Lab – KK’s")
        self.assertEqual(body["excerpt"], f"About {ETHOS_NCR} &#8594; Krüg")
        self.assertEqual(
            body["content"], f'<style>.q::before{{content:"“"}}</style><p>{ETHOS_NCR} &#8594; café</p>'
        )
        self.assertEqual(body["meta"], payload["meta"])

    def test_unstorable_meta_or_style_is_refused_before_any_request(self):
        site = mock.Mock()
        wp = wordpress_over(site)
        for payload in (
            {"title": "Ok", "slug": "ok", "meta": {"advanced_seo_description": ETHOS}},
            {"title": "Ok", "slug": "ok", "content": '<style>a::after{content:"→"}</style>'},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(UnstorableText):
                    wp.create_post(payload)
                with self.assertRaises(UnstorableText):
                    wp.update_post(1, payload, expected_slug="ok")

        site.get.assert_not_called()
        site.post.assert_not_called()

    def test_media_alt_text_and_term_names_are_sent_as_references(self):
        site = FakeCp1252Site()
        wp = wordpress_over(site)

        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "hero.jpg"
            image.write_bytes(b"jpeg fixture")
            wp.upload_media(image, alt=f"{ETHOS} on stage", caption="KK’s → café")
        wp.ensure_term("tags", f"{ETHOS} Picks")

        bodies = dict(site.json_bodies)
        self.assertEqual(bodies["/wp-json/wp/v2/media/501"]["alt_text"], f"{ETHOS_NCR} on stage")
        self.assertEqual(bodies["/wp-json/wp/v2/media/501"]["caption"], "KK’s &#8594; café")
        self.assertEqual(bodies["/wp-json/wp/v2/tags"], {"name": f"{ETHOS_NCR} Picks", "slug": "ethos-picks"})


class TermLookupTests(WritesAllowed):
    """A stored name holds references, so it never equals the raw name (#1225 review)."""

    def wordpress_answering(self, by_slug, by_search):
        site = mock.Mock()

        def get(url, params=None, timeout=None):
            return FakeResponse(by_slug if "slug" in params else by_search)

        site.get.side_effect = get
        return wordpress_over(site), site

    def test_existing_term_is_found_by_slug_without_a_create(self):
        stored = [{"id": 55, "name": f"{ETHOS_NCR} Picks", "slug": "ethos-picks"}]
        wp, site = self.wordpress_answering(by_slug=stored, by_search=[])

        self.assertEqual(wp.ensure_term("tags", f"{ETHOS} Picks"), 55)

        self.assertEqual(site.get.call_args_list[0].kwargs["params"]["slug"], "ethos-picks")
        site.post.assert_not_called()

    def test_stored_name_is_compared_unescaped(self):
        stored = [{"id": 56, "name": f"{ETHOS_NCR} Picks", "slug": "ethos-picks-2"}]
        wp, site = self.wordpress_answering(by_slug=[], by_search=stored)

        self.assertEqual(wp.ensure_term("tags", f"{ETHOS} Picks"), 56)

        site.post.assert_not_called()


class TitleGuardTests(unittest.TestCase):
    def test_a_title_stored_as_references_is_still_the_same_title(self):
        raw = "Đặng Thị Ngọc Thịnh → Hà Nội"
        stored = to_ncr(raw)
        self.assertLess(difflib.SequenceMatcher(None, raw.lower(), stored.lower()).ratio(), 0.5)

        self.assertEqual(update_title_guard(raw, stored), (True, 1.0))


class ReadbackTests(WritesAllowed):
    """update_safety compares the sent title with title.raw after html.unescape (#1218)."""

    def payload(self, title):
        return {"title": title, "slug": "ethos-lab", "status": "draft", "date": "2026-06-23T12:00:00"}

    def test_title_sent_as_references_reads_back_as_a_match(self):
        site = FakeCp1252Site()
        wp = wordpress_over(site)
        payload = self.payload(f"{ETHOS} Lab → KK’s")

        created = wp.create_post(payload)
        readback = wp.get_post(created["id"])

        self.assertEqual(readback["title"]["raw"], f"{ETHOS_NCR} Lab &#8594; KK’s")
        self.assertEqual(readback_mismatches(payload, readback), {})

    def test_title_corrupted_to_question_marks_is_still_a_mismatch(self):
        site = FakeCp1252Site()
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


UNSTORABLE_TITLE = f"{ETHOS} Lab → Łódź 🙂"
FOLDED_SEO_TITLE = "Ethos Lab Lódz | Kris Krüg"
OPENING = f"{ETHOS} Lab → Łódź 🙂 opened the night with forty people in the room."
FOLDED_OPENING = "Ethos Lab Lódz opened the night with forty people in the room."
FOLD_WARNINGS = (
    f'seo: folded advanced_seo_description: "{OPENING}" -> "{FOLDED_OPENING}"',
    f'seo: folded jetpack_seo_html_title: "{UNSTORABLE_TITLE} | Kris Krüg" -> "{FOLDED_SEO_TITLE}"',
    f'seo: folded jetpack_publicize_message: "{OPENING}" -> "{FOLDED_OPENING}"',
)


class UnstorableOpeningNotion(CaptionedNotion):
    def block_children(self, page_id):
        blocks = super().block_children(page_id)
        blocks[0]["paragraph"]["rich_text"] = [{"plain_text": OPENING}]
        return blocks


class MisdecodedNotion(FakeNotion):
    def block_children(self, page_id):
        blocks = notion_blocks()
        # U+0092 is what cp1252's apostrophe byte becomes when read as latin-1.
        blocks.insert(1, {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "it\x92s"}]}})
        return blocks


class ConnectorTests(WritesAllowed):
    def setUp(self):
        super().setUp()
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

        for name, value in {
            "load_config": lambda: cfg,
            "Notion": CaptionedNotion,
            "download_image": fake_download,
            "DRAFTS_DIR": self.tmp / "drafts",
            "REPO_ROOT": self.tmp,
        }.items():
            patcher = mock.patch.object(kk_notion_to_wp, name, value)
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

    def test_derived_meta_folds_with_one_warning_per_field_in_a_dry_run(self):
        wp = FakeWordPress()

        with mock.patch.object(kk_notion_to_wp, "Notion", UnstorableOpeningNotion):
            code, logs = self.run_connector(wp, dry_run=True, title_override=UNSTORABLE_TITLE)

        self.assertEqual(code, 0, logs)
        self.assertEqual(wp.calls, [])
        for line in FOLD_WARNINGS:
            self.assertEqual(logs.count(line), 1, line)
        # The package holds what WordPress will store, so the local-draft
        # scripts accept its SEO frontmatter.
        [post_md] = (self.tmp / "drafts").glob("*/post.md")
        frontmatter = yaml.safe_load(post_md.read_text(encoding="utf-8").split("---\n")[1])
        self.assertEqual(
            frontmatter["seo"],
            {"meta_title": FOLDED_SEO_TITLE, "meta_description": FOLDED_OPENING},
        )
        self.assertEqual(frontmatter["title"], UNSTORABLE_TITLE)
        self.assertEqual(frontmatter["excerpt"], OPENING)

    def test_derived_meta_folds_and_the_publish_continues(self):
        site = FakeCp1252Site()

        with mock.patch.object(kk_notion_to_wp, "Notion", UnstorableOpeningNotion):
            code, logs = self.run_connector(
                wordpress_over(site), dry_run=False, title_override=UNSTORABLE_TITLE
            )

        self.assertEqual(code, 0, logs)
        for line in FOLD_WARNINGS:
            self.assertEqual(logs.count(line), 1, line)
        self.assertEqual([ch for _, body in site.json_bodies for ch in unstorable(body)], [])
        post = site.posts[701]
        seo_keys = ("jetpack_seo_html_title", "advanced_seo_description", "jetpack_publicize_message")
        self.assertEqual(
            {key: post["meta"][key] for key in seo_keys},
            {
                "jetpack_seo_html_title": FOLDED_SEO_TITLE,
                "advanced_seo_description": FOLDED_OPENING,
                "jetpack_publicize_message": FOLDED_OPENING,
            },
        )
        # Title, excerpt and body keep every character, as numeric references.
        self.assertEqual(post["title"]["raw"], to_ncr(UNSTORABLE_TITLE))
        self.assertIn(to_ncr(OPENING), post["content"]["raw"])
        [(_, body)] = [(path, body) for path, body in site.json_bodies if path.endswith("/posts")]
        self.assertEqual(body["excerpt"], to_ncr(OPENING))

    def test_create_sends_nothing_outside_cp1252_and_reads_back_clean(self):
        site = FakeCp1252Site()

        code, logs = self.run_connector(
            wordpress_over(site), dry_run=False, title_override="KK’s “Field” Notes"
        )

        self.assertEqual(code, 0, logs)
        self.assertNotIn("seo: folded", logs)
        self.assertEqual([ch for _, body in site.json_bodies for ch in unstorable(body)], [])
        post = site.posts[701]
        self.assertEqual(post["title"]["raw"], "KK’s “Field” Notes")
        self.assertIn(f"{ETHOS_NCR} Lab &#8594; main stage", post["content"]["raw"])
        self.assertEqual(post["meta"]["jetpack_seo_html_title"], "KK’s “Field” Notes | Kris Krüg")
        self.assertEqual(site.media[501]["alt_text"], f"{ETHOS_NCR} Lab &#8594; main stage")

    def test_body_that_cannot_be_sent_exits_9_before_any_upload_or_term_write(self):
        style_body = '<!-- wp:html --><style>.a::after{content:"→"}</style><!-- /wp:html -->'
        cases = {
            "C1 control in the body": (
                mock.patch.object(kk_notion_to_wp, "Notion", MisdecodedNotion),
                "content: text has C1 control characters",
            ),
            "character outside cp1252 inside <style>": (
                mock.patch.object(
                    kk_notion_to_wp.block_rules, "render_blocks", lambda blocks, ctx=None: style_body
                ),
                "content: <style> holds characters",
            ),
        }
        for label, (patcher, message) in cases.items():
            for dry_run in (True, False):
                with self.subTest(label=label, dry_run=dry_run), patcher:
                    wp = FakeWordPress()

                    code, logs = self.run_connector(wp, dry_run=dry_run)

                    self.assertEqual(code, 9, logs)
                    self.assertIn(message, logs)
                    self.assertEqual(wp.calls, [])
                    self.assertEqual(wp.writes(), [])


if __name__ == "__main__":
    unittest.main()
