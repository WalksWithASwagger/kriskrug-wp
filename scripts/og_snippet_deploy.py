#!/usr/bin/env python3
"""Safely create, inspect, activate, or deactivate the temporary OG snippet."""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from common import WPClient


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / "scripts" / "notion-to-wp" / ".env"
MIRROR_PATH = REPO_ROOT / "fixes" / "og-restore-snippet.php"
SNIPPET_NAME = "Open Graph + Twitter Card meta (social link previews)"


def snippet_api(client: WPClient, path: str) -> str:
    return f"{client.base}/wp-json/code-snippets/v1{path}"


def snippet_code() -> str:
    return MIRROR_PATH.read_text(encoding="utf-8").removeprefix("<?php\n").lstrip("\n")


def list_snippets(client: WPClient) -> tuple[Any, list[dict[str, Any]]]:
    response = client.get(snippet_api(client, "/snippets"))
    if isinstance(response, list):
        return response, response
    if isinstance(response, dict):
        for key in ("items", "snippets", "data"):
            items = response.get(key)
            if isinstance(items, list):
                return response, items
    raise RuntimeError("Code Snippets inventory returned an unexpected shape")


def write_snapshot(raw_inventory: Any) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = Path("/private/tmp") / f"kriskrug-code-snippets-{timestamp}.json"
    path.write_text(json.dumps(raw_inventory, indent=2), encoding="utf-8")
    path.chmod(0o600)
    return path


def create(client: WPClient) -> None:
    raw_inventory, snippets = list_snippets(client)
    snapshot = write_snapshot(raw_inventory)
    matches = [item for item in snippets if item.get("name") == SNIPPET_NAME]
    if len(matches) > 1:
        raise RuntimeError(f"Refusing to continue: {len(matches)} snippets share the target name")
    if matches:
        existing = matches[0]
        if existing.get("active"):
            raise RuntimeError(f"Refusing to replace active snippet id={existing.get('id')}")
        if existing.get("code") != snippet_code():
            raise RuntimeError(f"Inactive snippet id={existing.get('id')} has different code")
        print(f"snapshot={snapshot} mode=0600")
        print(f"reusing id={existing.get('id')} active=false code_round_trip=ok")
        return

    payload = {
        "name": SNIPPET_NAME,
        "desc": "Temporary direct OG/Twitter metadata bridge. Retire after Aurora 1.3.37 is live.",
        "code": snippet_code(),
        "scope": "front-end",
        "priority": 5,
        "active": False,
    }
    created = client.post(snippet_api(client, "/snippets"), payload)
    snippet_id = int(created["id"])
    readback = client.get(snippet_api(client, f"/snippets/{snippet_id}"))
    if readback.get("code") != payload["code"]:
        raise RuntimeError("Created snippet code did not round-trip")
    if readback.get("active") is not False:
        raise RuntimeError("Created snippet was unexpectedly active")
    if readback.get("scope") != payload["scope"]:
        raise RuntimeError("Created snippet scope did not round-trip")
    print(f"snapshot={snapshot} mode=0600")
    print(f"created id={snippet_id} active=false scope=front-end code_round_trip=ok")


def set_active(client: WPClient, snippet_id: int, active: bool) -> None:
    action = "activate" if active else "deactivate"
    try:
        client.request(
            "PATCH",
            snippet_api(client, f"/snippets/{snippet_id}"),
            {"active": active},
        )
    except Exception as error:
        print(f"PATCH failed ({error}); trying POST /{action}")
        client.post(snippet_api(client, f"/snippets/{snippet_id}/{action}"))
    readback = client.get(snippet_api(client, f"/snippets/{snippet_id}"))
    if bool(readback.get("active")) is not active:
        raise RuntimeError(f"Snippet id={snippet_id} did not become active={active}")
    print(f"id={snippet_id} active={str(active).lower()} name={readback.get('name')!r}")


def status(client: WPClient, snippet_id: int) -> None:
    readback = client.get(snippet_api(client, f"/snippets/{snippet_id}"))
    print(
        f"id={snippet_id} active={str(bool(readback.get('active'))).lower()} "
        f"scope={readback.get('scope')} name={readback.get('name')!r}"
    )


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: og_snippet_deploy.py create|status|activate|deactivate [id]")
    os.environ["WP_AUTH_MODE"] = "login"
    client = WPClient.from_env(ENV_PATH)
    command = sys.argv[1]
    if command == "create" and len(sys.argv) == 2:
        create(client)
        return
    if command in {"status", "activate", "deactivate"} and len(sys.argv) == 3:
        snippet_id = int(sys.argv[2])
        if command == "status":
            status(client, snippet_id)
        else:
            set_active(client, snippet_id, command == "activate")
        return
    raise SystemExit("usage: og_snippet_deploy.py create|status|activate|deactivate [id]")


if __name__ == "__main__":
    main()
