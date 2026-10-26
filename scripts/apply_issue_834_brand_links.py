#!/usr/bin/env python3
"""Apply the three reviewed #834 links, one post at a time; dry-run by default."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WPClient  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TARGETS = json.loads((ROOT / "fixes/issue-834-brand-navigation.json").read_text())


def digest(body: str) -> str:
    return hashlib.sha256(body.encode()).hexdigest()


def validate(item: dict, spec: dict) -> str:
    for field in ("id", "slug", "type", "status", "date"):
        if item.get(field) != spec[field]:
            raise ValueError(f"{spec['id']}: {field} identity mismatch")
    if item.get("title", {}).get("raw") != spec["title"]:
        raise ValueError(f"{spec['id']}: title identity mismatch")
    body = item.get("content", {}).get("raw")
    if not isinstance(body, str):
        raise ValueError(f"{spec['id']}: authenticated content.raw missing")
    return body


def candidate(body: str, spec: dict) -> str:
    if digest(body) == spec["after_sha256"]:
        return body
    if digest(body) != spec["before_sha256"]:
        raise ValueError(f"{spec['id']}: content changed since review; re-snapshot")
    if spec["dependency"] and body.count(spec["dependency"]) != 1:
        raise ValueError(f"{spec['id']}: earlier issue anchor missing or duplicated")
    anchor = f'<a href="{spec["href"]}">{spec["anchor"]}</a>'
    if body.count(spec["find"]) != 1 or anchor in body:
        raise ValueError(f"{spec['id']}: insertion marker missing or duplicated")
    result = body.replace(spec["find"], spec["replace"], 1)
    if result.count(anchor) != 1 or digest(result) != spec["after_sha256"]:
        raise ValueError(f"{spec['id']}: candidate differs from reviewed content")
    return result


def save_private(folder: Path, label: str, item: dict) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = folder / f"{item['id']}-{label}-{stamp}.json"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(item, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return path


def update(
    client: WPClient,
    spec: dict,
    folder: Path,
    *,
    apply: bool,
    restore: dict | None = None,
) -> dict:
    route = f"posts/{spec['id']}"
    live = client.get(route, params={"context": "edit"})
    before = validate(live, spec)
    if restore is None:
        after = candidate(before, spec)
    else:
        after = validate(restore, spec)
        if digest(after) != spec["before_sha256"]:
            raise ValueError("Restore snapshot is not the reviewed original")
        if before != after and digest(before) != spec["after_sha256"]:
            raise ValueError("Refusing to restore over a newer or unreviewed edit")
    if before == after:
        return {"id": spec["id"], "status": "unchanged", "sha256": digest(before)}
    print(
        "".join(
            difflib.unified_diff(
                before.splitlines(True),
                after.splitlines(True),
                fromfile=f"{spec['id']}-live",
                tofile=f"{spec['id']}-candidate",
            )
        )
    )
    if not apply:
        return {"id": spec["id"], "status": "dry-run", "sha256": digest(after)}
    snapshot = save_private(folder, "before-restore" if restore else "before", live)
    fresh = client.get(route, params={"context": "edit"})
    if validate(fresh, spec) != before or fresh.get("modified") != live.get("modified"):
        raise ValueError("Post changed during snapshot; no write attempted")
    # The shared client never replays an ambiguous POST; inspect live before retrying.
    client.post(route, {"content": after})
    observed = client.get(route, params={"context": "edit"})
    readback = save_private(folder, "readback", observed)
    if validate(observed, spec) != after:
        raise ValueError(f"Readback differs; inspect {readback} and {snapshot}")
    for field in ("categories", "tags", "featured_media", "excerpt", "meta"):
        if observed.get(field) != live.get(field):
            raise ValueError(f"{field} drifted; inspect {readback} and {snapshot}")
    return {
        "id": spec["id"],
        "status": "restored" if restore else "applied",
        "sha256": digest(after),
        "snapshot": str(snapshot),
        "readback": str(readback),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--id", type=int, choices=[row["id"] for row in TARGETS], required=True
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--restore", type=Path)
    parser.add_argument(
        "--snapshot-dir", type=Path, default=ROOT / "backup/issue-834-brand-links"
    )
    args = parser.parse_args()
    user = os.environ.get("WP_API_USERNAME") or os.environ.get("WP_USER")
    password = os.environ.get("WP_API_PASSWORD") or os.environ.get("WP_APP_PASSWORD")
    if not user or not password:
        parser.error("WordPress credentials unresolved; run through Varlock")
    client = WPClient("https://kriskrug.co", user, password)
    spec = next(row for row in TARGETS if row["id"] == args.id)
    restore = json.loads(args.restore.read_text()) if args.restore else None
    result = update(client, spec, args.snapshot_dir, apply=args.apply, restore=restore)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
