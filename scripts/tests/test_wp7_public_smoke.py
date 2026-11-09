import argparse
import importlib.util
import io
import sys
from email.message import Message
from http.client import RemoteDisconnected
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


path = Path(__file__).parents[1] / "wp7-public-smoke.py"
spec = importlib.util.spec_from_file_location("wp7_public_smoke", path)
smoke = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = smoke
spec.loader.exec_module(smoke)


def test_disconnected_request_is_reported_for_pages_and_rest():
    args = argparse.Namespace(base_url="https://example.com", path=["/", "/wp-json/"], timeout=1, expect_version=None)
    with patch.object(smoke, "urlopen", side_effect=RemoteDisconnected("connection closed")):
        report = smoke.run(args)

    assert [check["status"] for check in report["checks"]] == ["fail", "fail"]
    assert all("connection closed" in check["failures"][0] for check in report["checks"])


def test_http_error_preserves_status_and_body():
    headers = Message()
    error = HTTPError("https://example.com/", 503, "unavailable", headers, io.BytesIO(b"maintenance"))
    with patch.object(smoke, "urlopen", side_effect=error):
        result = smoke.fetch("https://example.com/", 1)

    assert result.status == 503
    assert result.body == "maintenance"
    assert smoke.check_page("/", result)[0] == ["HTTP 503"]


def test_disconnected_http_error_body_reports_status_and_transport_failure():
    headers = Message()
    error = HTTPError("https://example.com/", 503, "unavailable", headers, io.BytesIO())
    with patch.object(error, "read", side_effect=RemoteDisconnected("body interrupted")):
        with patch.object(smoke, "urlopen", side_effect=error):
            result = smoke.fetch("https://example.com/", 1)

    assert result.status == 503
    assert smoke.check_page("/", result)[0] == ["HTTP 503", "response body read failed: body interrupted"]
    assert smoke.check_rest_root(result)[0] == ["response body read failed: body interrupted"]
