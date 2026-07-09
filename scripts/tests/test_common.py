import io
import sys
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import common  # noqa: E402
from common import WPClient, load_env, parse_simple_env, wp_credentials  # noqa: E402


def _fake_response(body: str):
    """Return an object usable as a urlopen context manager yielding body."""
    resp = mock.MagicMock()
    resp.read.return_value = body.encode()
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


def _http_error(code: int) -> HTTPError:
    err = HTTPError("http://x", code, f"err{code}", hdrs=None, fp=io.BytesIO(b""))
    err.close()  # client only reads err.code; avoids a GC ResourceWarning
    return err


class _EnvFileMixin:
    def write_env(self, text: str) -> str:
        import os
        import tempfile

        fd = tempfile.NamedTemporaryFile("w", suffix=".env", delete=False, encoding="utf-8")
        fd.write(text)
        fd.close()
        self.addCleanup(lambda: os.path.exists(fd.name) and os.unlink(fd.name))
        return fd.name


class ParseSimpleEnvTests(_EnvFileMixin, unittest.TestCase):
    def test_skips_comments_blanks_and_strips_quotes(self):
        path = Path(self.write_env("# comment\n\nWP_USER=alice\nWP_APP_PASSWORD=\"p a s s\"\nBAD LINE\n"))
        values = parse_simple_env(path)
        self.assertEqual(values, {"WP_USER": "alice", "WP_APP_PASSWORD": "p a s s"})

    def test_missing_file_returns_empty(self):
        self.assertEqual(parse_simple_env(Path("/no/such/.env")), {})


class LoadEnvTests(_EnvFileMixin, unittest.TestCase):
    def test_explicit_path_loads_and_os_overlay_wins(self):
        path = self.write_env("WP_USER=fileuser\nWP_APP_PASSWORD=filepass\n")
        with mock.patch.dict("os.environ", {"WP_USER": "envuser"}, clear=False):
            values = load_env(path)
        self.assertEqual(values["WP_USER"], "envuser")  # os overrides file
        self.assertEqual(values["WP_APP_PASSWORD"], "filepass")

    def test_overlay_disabled_keeps_file_value(self):
        path = self.write_env("WP_USER=fileuser\nWP_APP_PASSWORD=filepass\n")
        with mock.patch.dict("os.environ", {"WP_USER": "envuser"}, clear=False):
            values = load_env(path, overlay_os=False)
        self.assertEqual(values["WP_USER"], "fileuser")

    def test_auth_mode_os_overlay_wins(self):
        path = self.write_env("WP_USER=fileuser\nWP_APP_PASSWORD=filepass\nWP_AUTH_MODE=basic\n")
        with mock.patch.dict("os.environ", {"WP_AUTH_MODE": "login"}, clear=False):
            values = load_env(path)
        self.assertEqual(values["WP_AUTH_MODE"], "login")

    def test_from_env_uses_auth_mode(self):
        path = self.write_env("WP_USER=fileuser\nWP_APP_PASSWORD=filepass\nWP_AUTH_MODE=login\n")
        client = WPClient.from_env(path)
        self.assertEqual(client.auth_mode, "login")


class WpCredentialsTests(unittest.TestCase):
    def test_returns_tuple_and_strips_base_slash(self):
        env = {"WP_USER": "u", "WP_APP_PASSWORD": "p", "WP_BASE_URL": "https://example.com/"}
        self.assertEqual(wp_credentials(env), ("https://example.com", "u", "p"))

    def test_defaults_base_url(self):
        base, _, _ = wp_credentials({"WP_USER": "u", "WP_APP_PASSWORD": "p"})
        self.assertEqual(base, common.DEFAULT_BASE_URL)

    def test_raises_when_missing(self):
        with self.assertRaises(RuntimeError):
            wp_credentials({"WP_USER": "u"})


class WPClientRequestTests(unittest.TestCase):
    def setUp(self):
        self.client = WPClient("https://example.com", "u", "p", retries=2)

    def test_builds_relative_path_under_api(self):
        self.assertEqual(
            self.client._url("posts", {"per_page": 5}),
            "https://example.com/wp-json/wp/v2/posts?per_page=5",
        )

    def test_absolute_path_passes_through(self):
        self.assertEqual(self.client._url("https://other/x", None), "https://other/x")

    def test_get_sets_auth_and_parses_json(self):
        captured = {}

        def fake_urlopen(req, timeout=0):
            captured["auth"] = req.headers.get("Authorization")
            captured["method"] = req.get_method()
            captured["data"] = req.data
            return _fake_response('[{"id": 1}]')

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            out = self.client.get("posts")
        self.assertEqual(out, [{"id": 1}])
        self.assertTrue(captured["auth"].startswith("Basic "))
        self.assertEqual(captured["method"], "GET")
        self.assertIsNone(captured["data"])

    def test_login_auth_uses_rest_nonce_and_cookie_opener(self):
        client = WPClient("https://example.com", "u", "p", auth_mode="login")
        opener = mock.MagicMock()
        opener.open.return_value = _fake_response('{"ok": true}')
        client._cookie_opener = opener
        client._rest_nonce = "nonce123"

        out = client.get("posts")

        self.assertEqual(out, {"ok": True})
        req = opener.open.call_args.args[0]
        self.assertEqual(req.get_header("X-wp-nonce"), "nonce123")
        self.assertIsNone(req.get_header("Authorization"))

    def test_login_auth_parses_wp_api_settings_nonce(self):
        client = WPClient("https://example.com", "u", "p", auth_mode="login")
        login = _fake_response("")
        profile = _fake_response(
            'wp-login.php?action=logout<script id="wp-api-request-js-extra">'
            'var wpApiSettings = {"root":"https://example.com/wp-json/","nonce":"abc123","versionString":"wp/v2/"};'
            "</script>"
        )
        opener = mock.MagicMock()
        opener.open.side_effect = [login, profile]

        with mock.patch("urllib.request.build_opener", return_value=opener):
            nonce = client._ensure_cookie_auth()

        self.assertEqual(nonce, "abc123")
        self.assertIs(client._cookie_opener, opener)

    def test_invalid_auth_mode_raises(self):
        with self.assertRaises(ValueError):
            WPClient("https://example.com", "u", "p", auth_mode="cookie")

    def test_post_sends_json_body(self):
        captured = {}

        def fake_urlopen(req, timeout=0):
            captured["data"] = req.data
            captured["method"] = req.get_method()
            return _fake_response('{"ok": true}')

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            out = self.client.post("posts/1", {"categories": [2]})
        self.assertEqual(out, {"ok": True})
        self.assertEqual(captured["method"], "POST")
        self.assertEqual(captured["data"], b'{"categories": [2]}')

    def test_empty_body_returns_none(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response("")):
            self.assertIsNone(self.client.get("posts"))

    def test_4xx_raises_immediately_without_retry(self):
        calls = {"n": 0}

        def fake_urlopen(req, timeout=0):
            calls["n"] += 1
            raise _http_error(404)

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            with self.assertRaises(HTTPError):
                self.client.get("posts/999")
        self.assertEqual(calls["n"], 1)

    def test_5xx_retried_then_succeeds(self):
        seq = [_http_error(503), _fake_response('{"ok": 1}')]

        def fake_urlopen(req, timeout=0):
            item = seq.pop(0)
            if isinstance(item, HTTPError):
                raise item
            return item

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen), \
             mock.patch("time.sleep"):
            out = self.client.get("posts")
        self.assertEqual(out, {"ok": 1})


class WPClientPaginationTests(unittest.TestCase):
    def test_get_all_stops_on_short_page(self):
        client = WPClient("https://example.com", "u", "p")
        pages = [[{"id": i} for i in range(100)], [{"id": 100}, {"id": 101}]]

        with mock.patch.object(client, "request", side_effect=lambda *a, **k: pages.pop(0)):
            items = client.get_all("posts", per_page=100)
        self.assertEqual(len(items), 102)

    def test_get_all_stops_on_empty(self):
        client = WPClient("https://example.com", "u", "p")
        with mock.patch.object(client, "request", return_value=[]):
            self.assertEqual(client.get_all("posts"), [])


if __name__ == "__main__":
    unittest.main()
