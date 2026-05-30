#!/usr/bin/env python3
"""Smoke-test WordPress REST + MCP adapter for WordCamp demo readiness."""

from __future__ import annotations

import base64
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ENV_FILE = Path(__file__).resolve().parent / "notion-to-wp" / ".env"
BASE = "https://kriskrug.co"


def load_env(path: Path) -> tuple[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    user = values.get("WP_USER", "")
    password = (values.get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not password:
        raise SystemExit(f"Missing WP_USER/WP_APP_PASSWORD in {path}")
    return user, password


def probe(label: str, url: str, user: str, password: str, method: str = "GET", body: bytes | None = None) -> bool:
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, headers=headers, method=method, data=body)
    try:
        with urlopen(request, timeout=20) as response:
            print(f"PASS {label}: HTTP {response.status}")
            return True
    except HTTPError as exc:
        snippet = exc.read(300).decode("utf-8", "replace")
        if label == "mcp" and exc.code in (400, 405):
            # 400 = JSON-RPC validation after auth; 405 on GET is expected
            print(f"PASS {label}: HTTP {exc.code} (auth OK, adapter responding)")
            return True
        print(f"FAIL {label}: HTTP {exc.code} {snippet[:120]}")
        return False


def main() -> int:
    if not ENV_FILE.is_file():
        print(f"FAIL: missing {ENV_FILE}")
        return 1

    user, password = load_env(ENV_FILE)
    ok = True
    ok &= probe("posts", f"{BASE}/wp-json/wp/v2/posts?per_page=1", user, password)
    ok &= probe("abilities", f"{BASE}/wp-json/wp-abilities/v1/abilities", user, password)
    ok &= probe(
        "mcp",
        f"{BASE}/wp-json/mcp/mcp-adapter-default-server",
        user,
        password,
        method="POST",
        body=b"{}",
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
