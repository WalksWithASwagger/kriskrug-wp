#!/usr/bin/env python3
"""Shared env loading + WordPress REST client for kriskrug.co ops scripts.

Stdlib-only (urllib) so the standalone audit/publish scripts gain one consistent
client with zero new dependencies. The notion-to-wp package keeps its own
requests-based WordPress client (it does media upload and other package-specific
work); this module is for the urllib-based scripts under scripts/ that currently
hand-roll env loading and Basic-auth requests.
"""
from __future__ import annotations

import base64
import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

try:  # optional; falls back to the simple parser when absent
    from dotenv import dotenv_values
except Exception:  # pragma: no cover - local fallback
    dotenv_values = None

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATHS = (
    REPO_ROOT / "scripts" / "notion-to-wp" / ".env",
    Path("/Users/kk/Code/notion-local/kk-ai-ecosystem/.env"),
)
DEFAULT_BASE_URL = "https://kriskrug.co"
_OVERRIDE_KEYS = ("WP_USER", "WP_APP_PASSWORD", "WP_BASE_URL")


def parse_simple_env(path: Path) -> dict[str, str]:
    """Parse a KEY=VALUE .env file, skipping comments/blanks and stripping quotes."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_env(path: Path | str | None = None, *, overlay_os: bool = True) -> dict[str, str]:
    """Load .env values, preferring python-dotenv when installed.

    With no path, searches DEFAULT_ENV_PATHS and uses the first that exists.
    When overlay_os is True, matching process env vars win over file values.
    """
    candidates = [Path(path)] if path else list(DEFAULT_ENV_PATHS)
    values: dict[str, str] = {}
    for candidate in candidates:
        if not candidate.exists():
            continue
        if dotenv_values is not None:
            values = {
                str(k): str(v)
                for k, v in dotenv_values(candidate).items()
                if k and v is not None
            }
        else:
            values = parse_simple_env(candidate)
        break
    if overlay_os:
        for key in _OVERRIDE_KEYS:
            if os.environ.get(key):
                values[key] = os.environ[key]
    return values


def wp_credentials(env: dict[str, str] | None = None) -> tuple[str, str, str]:
    """Return (base_url, user, app_password). Raises if credentials are missing."""
    env = env if env is not None else load_env()
    user = env.get("WP_USER", "")
    app_password = env.get("WP_APP_PASSWORD", "")
    base_url = env.get("WP_BASE_URL", DEFAULT_BASE_URL)
    if not user or not app_password:
        raise RuntimeError(
            "WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env"
        )
    return base_url.rstrip("/"), user, app_password


class WPClient:
    """Minimal stdlib WordPress REST client with Basic auth and 5xx retry."""

    def __init__(
        self,
        base_url: str,
        user: str,
        app_password: str,
        *,
        timeout: int = 40,
        retries: int = 2,
    ):
        self.base = base_url.rstrip("/")
        self.api = f"{self.base}/wp-json/wp/v2"
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self._auth = f"Basic {token}"
        self.timeout = timeout
        self.retries = retries

    @classmethod
    def from_env(cls, path: Path | str | None = None, **kwargs) -> "WPClient":
        base_url, user, app_password = wp_credentials(load_env(path))
        return cls(base_url, user, app_password, **kwargs)

    def _url(self, path: str, params: dict | None) -> str:
        url = path if path.startswith("http") else f"{self.api}/{path.lstrip('/')}"
        if params:
            url = f"{url}{'&' if '?' in url else '?'}{urlencode(params)}"
        return url

    def request(
        self,
        method: str,
        path: str,
        payload: Any | None = None,
        *,
        params: dict | None = None,
    ) -> Any:
        """Issue a REST call; returns parsed JSON (or None for an empty body).

        4xx errors raise immediately (deterministic); 5xx and transient network
        errors are retried up to ``retries`` times before re-raising.
        """
        url = self._url(path, params)
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {"Authorization": self._auth}
        if data is not None:
            headers["Content-Type"] = "application/json"
        last_err: Exception | None = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read().decode()
                    return json.loads(body) if body else None
            except HTTPError as err:
                if err.code < 500:
                    raise
                last_err = err
            except URLError as err:
                last_err = err
            if attempt < self.retries:
                time.sleep(0.5 * (attempt + 1))
        assert last_err is not None
        raise last_err

    def get(self, path: str, *, params: dict | None = None) -> Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, payload: Any | None = None, *, params: dict | None = None) -> Any:
        return self.request("POST", path, payload=payload, params=params)

    def delete(self, path: str, *, params: dict | None = None) -> Any:
        return self.request("DELETE", path, params=params)

    def get_all(
        self,
        path: str,
        *,
        params: dict | None = None,
        per_page: int = 100,
        max_pages: int = 100,
    ) -> list:
        """Paginate a list endpoint, returning all items concatenated."""
        merged = dict(params or {})
        merged["per_page"] = per_page
        items: list = []
        for page in range(1, max_pages + 1):
            merged["page"] = page
            batch = self.request("GET", path, params=merged)
            if not isinstance(batch, list) or not batch:
                break
            items.extend(batch)
            if len(batch) < per_page:
                break
        return items
