"""WPClient refuses writes kriskrug.co's cp1252 database would store as "?" (#1225).

The page deploy tools compare their readback with the payload file exactly, so
the client refuses instead of sending numeric references. Offline only: urlopen
is a fake, and a call to it where none is allowed fails the test.
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import deploy_events_page  # noqa: E402
from common import UnstorableText, WPClient  # noqa: E402

ETHOS = "Eth\N{LATIN SMALL LETTER O WITH DOT BELOW}\N{COMBINING ACUTE ACCENT}s"
EMOJI = "\N{SLIGHTLY SMILING FACE}"
ARROW = "\N{RIGHTWARDS ARROW}"
EN_DASH, EM_DASH = "\N{EN DASH}", "\N{EM DASH}"
CP1252_TEXT = f"Kris Krüg’s “field” ‘notes’ {EN_DASH} 2025{EN_DASH}2026 {EM_DASH} €40 …"
PAGE_URL = "https://example.test/wp-json/wp/v2/pages/2250"


def _fake_response(body: str):
    resp = mock.MagicMock()
    resp.read.return_value = body.encode()
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


class RefusedWriteTests(unittest.TestCase):
    def setUp(self):
        self.client = WPClient("https://example.test", "u", "p")
        patcher = mock.patch(
            "urllib.request.urlopen", side_effect=AssertionError("network call")
        )
        self.urlopen = patcher.start()
        self.addCleanup(patcher.stop)

    def assert_refused(self, method, payload, field, character, params=None):
        with self.assertRaises(UnstorableText) as caught:
            self.client.request(method, "pages/2250", payload, params=params)
        message = str(caught.exception)
        self.assertIn(f"refused to send {method} {PAGE_URL}", message)
        self.assertIn(f"{field} has raw characters outside cp1252", message)
        self.assertIn(character, message)
        self.urlopen.assert_not_called()

    def test_combining_accent_in_a_post_is_refused_before_any_request(self):
        self.assert_refused(
            "POST",
            {"title": f"{ETHOS} Lab Block Party"},
            "payload.title",
            "U+0301 COMBINING ACUTE ACCENT",
        )

    def test_emoji_deep_in_a_payload_is_refused_naming_its_path(self):
        payload = {"meta": {"cards": [{"label": "ok"}, {"label": f"Live {EMOJI}"}]}}
        self.assert_refused(
            "POST",
            payload,
            "payload.meta.cards[1].label",
            "U+1F642 SLIGHTLY SMILING FACE",
        )

    def test_put_and_patch_are_guarded_too(self):
        for method in ("PUT", "PATCH"):
            with self.subTest(method=method):
                self.assert_refused(
                    method,
                    {"content": f"<p>draft {ARROW} live</p>"},
                    "payload.content",
                    "U+2192 RIGHTWARDS ARROW",
                )

    def test_query_params_on_a_write_are_checked(self):
        # WordPress reads write params from the query string as well as the body.
        self.assert_refused(
            "POST",
            None,
            "params.alt_text",
            "U+1ECD LATIN SMALL LETTER O WITH DOT BELOW",
            params={"alt_text": ETHOS},
        )

    def test_post_helper_is_refused(self):
        with self.assertRaisesRegex(UnstorableText, "payload.alt_text"):
            self.client.post("media/12", {"alt_text": f"{ETHOS} poster"})
        self.urlopen.assert_not_called()

    def test_cookie_login_is_not_attempted_for_a_refused_write(self):
        client = WPClient("https://example.test", "u", "p", auth_mode="login")
        with mock.patch("urllib.request.build_opener") as build_opener:
            with self.assertRaises(UnstorableText):
                client.post("pages/2250", {"content": f"<p>{EMOJI}</p>"})
        build_opener.assert_not_called()
        self.urlopen.assert_not_called()


class StorableWriteTests(unittest.TestCase):
    def test_cp1252_text_is_sent_untouched(self):
        payload = {
            "title": "Kris Krüg",
            "content": f"<p>{CP1252_TEXT}</p>",
            "meta": {"jetpack_seo_html_title": f"KK’s Notes {EN_DASH} Kris Krüg"},
        }
        original = json.loads(json.dumps(payload))
        bodies = []

        def fake_urlopen(req, timeout=0):
            bodies.append(req.data)
            return _fake_response('{"id": 2250}')

        client = WPClient("https://example.test", "u", "p")
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            self.assertEqual(client.post("pages/2250", payload), {"id": 2250})

        self.assertEqual(bodies, [json.dumps(original).encode()])
        self.assertEqual(json.loads(bodies[0]), original)
        self.assertNotIn(b"&#", bodies[0])
        self.assertEqual(payload, original)

    def test_reads_are_not_guarded(self):
        # Searching for text the database cannot store is still a valid read.
        client = WPClient("https://example.test", "u", "p")
        with mock.patch(
            "urllib.request.urlopen", return_value=_fake_response("[]")
        ) as urlopen:
            self.assertEqual(client.get("posts", params={"search": ETHOS}), [])
        urlopen.assert_called_once()


class EventsDeployTests(unittest.TestCase):
    """deploy_events_page sends its write through the guarded client."""

    ARTIFACT = (
        '<div data-events-grid="sheet"></div><div data-events-grid="upcoming"></div>'
        f'<div class="kk-ev-record-grid"></div><p>See the archive {ARROW}</p>'
    )

    def test_artifact_with_an_arrow_is_never_posted(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        artifact = Path(tmp.name) / "events.html"
        artifact.write_text(self.ARTIFACT, encoding="utf-8")
        page = {
            "id": 2250,
            "slug": "events",
            "type": "page",
            "status": "publish",
            "modified_gmt": "2026-11-12T00:00:00",
            "content": {"raw": "<p>live events page</p>"},
        }
        methods = []

        def fake_urlopen(req, timeout=0):
            methods.append(req.get_method())
            if req.get_method() != "GET":
                raise AssertionError(f"{req.get_method()} reached the network")
            return _fake_response(json.dumps(page))

        client = WPClient("https://example.test", "u", "p")
        with (
            mock.patch.object(deploy_events_page, "ARTIFACT", artifact),
            mock.patch.object(deploy_events_page, "BACKUP_DIR", Path(tmp.name)),
            mock.patch.object(
                deploy_events_page.WPClient, "from_env", return_value=client
            ),
            mock.patch.object(sys, "argv", ["deploy_events_page.py", "--execute"]),
            mock.patch("urllib.request.urlopen", side_effect=fake_urlopen),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            with self.assertRaises(deploy_events_page.DeployError) as caught:
                deploy_events_page.main()

        self.assertIn("payload.content", str(caught.exception))
        self.assertIn("U+2192 RIGHTWARDS ARROW", str(caught.exception))
        self.assertEqual(methods, ["GET"])


if __name__ == "__main__":
    unittest.main()
