#!/usr/bin/env python3
"""Audit and prepare the issue #353 legacy body-H1 migration.

The default command is a read-only full inventory. Live writes require the
explicit ``apply`` command, one target ID, and a target-specific confirmation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from common import WPClient


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "fixes/issue-353-body-h1-migration-2026-07-13.json"
DEFAULT_ENV_PATH = REPO_ROOT / "scripts/notion-to-wp/.env"
DEFAULT_SNAPSHOT_DIR = Path("/private/tmp")
REST_FIELDS = "id,type,slug,status,modified_gmt,link,content"

H1_OPEN_RE = re.compile(r"<h1(?=[\s>])", flags=re.IGNORECASE)
H1_CLOSE_RE = re.compile(r"</h1\s*>", flags=re.IGNORECASE)
H1_ELEMENT_RE = re.compile(
    r"(?P<open><h1(?=[\s>])[^>]*>)(?P<body>.*?)(?P<close></h1\s*>)",
    flags=re.IGNORECASE | re.DOTALL,
)
GUTENBERG_HEADING_RE = re.compile(
    r"(?P<prefix><!--\s+wp:heading\s+)"
    r"(?P<attrs>\{.*?\})"
    r"(?P<suffix>\s+-->)"
    r"(?P<body>.*?)"
    r"(?P<close><!--\s+/wp:heading\s+-->)",
    flags=re.DOTALL,
)
LEVEL_ONE_ATTR_RE = re.compile(r'("level"\s*:\s*)1(?=\s*[,}])')


class MigrationError(RuntimeError):
    pass


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def count_h1(value: str) -> int:
    return len(H1_OPEN_RE.findall(value))


def confirmation_for(target_id: int) -> str:
    return f"APPLY-ISSUE-353-TARGET-{target_id}"


def _rewrite_gutenberg_h1(raw: str, expected_count: int) -> str:
    converted = 0

    def patch_block(match: re.Match[str]) -> str:
        nonlocal converted
        attrs_text = match.group("attrs")
        try:
            attrs = json.loads(attrs_text)
        except json.JSONDecodeError as exc:
            raise MigrationError("invalid Gutenberg heading attributes") from exc
        if attrs.get("level") != 1:
            return match.group(0)

        body = match.group("body")
        if count_h1(body) != 1 or len(H1_CLOSE_RE.findall(body)) != 1:
            raise MigrationError(
                "a reviewed Gutenberg level-1 block does not contain exactly one H1"
            )
        new_attrs, attr_count = LEVEL_ONE_ATTR_RE.subn(
            r"\g<1>2",
            attrs_text,
            count=1,
        )
        if attr_count != 1:
            raise MigrationError("could not change the reviewed Gutenberg level attribute")
        new_body, open_count = H1_OPEN_RE.subn("<h2", body, count=1)
        new_body, close_count = H1_CLOSE_RE.subn("</h2>", new_body, count=1)
        if open_count != 1 or close_count != 1:
            raise MigrationError("could not change the reviewed Gutenberg H1 tags")

        converted += 1
        return (
            match.group("prefix")
            + new_attrs
            + match.group("suffix")
            + new_body
            + match.group("close")
        )

    rewritten = GUTENBERG_HEADING_RE.sub(patch_block, raw)
    if converted != expected_count or count_h1(rewritten) != 0:
        raise MigrationError(
            "body H1s are not fully contained in the reviewed Gutenberg level-1 blocks"
        )
    return rewritten


def _rewrite_classic_h1(raw: str, expected_count: int) -> str:
    def patch_element(match: re.Match[str]) -> str:
        opening = H1_OPEN_RE.sub("<h2", match.group("open"), count=1)
        return opening + match.group("body") + "</h2>"

    rewritten, converted = H1_ELEMENT_RE.subn(patch_element, raw)
    if converted != expected_count or count_h1(rewritten) != 0:
        raise MigrationError("classic body H1 elements do not match the reviewed count")
    return rewritten


def rewrite_h1(raw: str, *, content_format: str, expected_count: int) -> str:
    actual_count = count_h1(raw)
    if actual_count != expected_count:
        raise MigrationError(
            f"expected {expected_count} body H1 elements, found {actual_count}"
        )
    if content_format == "gutenberg":
        return _rewrite_gutenberg_h1(raw, expected_count)
    if content_format == "classic":
        return _rewrite_classic_h1(raw, expected_count)
    raise MigrationError(f"unsupported content format: {content_format}")


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("issue") != 353:
        raise MigrationError("manifest is not for issue #353")
    if not isinstance(data.get("targets"), list) or not data["targets"]:
        raise MigrationError("manifest has no migration targets")
    return data


def targets_by_id(manifest: dict[str, Any]) -> dict[int, dict[str, Any]]:
    targets = {int(target["id"]): target for target in manifest["targets"]}
    if len(targets) != len(manifest["targets"]):
        raise MigrationError("manifest contains duplicate target IDs")
    return targets


def _raw_content(item: dict[str, Any]) -> str:
    content = item.get("content")
    raw = content.get("raw") if isinstance(content, dict) else None
    if not isinstance(raw, str):
        raise MigrationError("authenticated WordPress response did not include content.raw")
    return raw


def _validate_identity(
    item: dict[str, Any],
    target: dict[str, Any],
    *,
    include_modified: bool,
) -> None:
    checks = {
        "id": target["id"],
        "type": target["type"],
        "slug": target["slug"],
        "status": target["status"],
        "link": target["url"],
    }
    if include_modified:
        checks["modified_gmt"] = target["modified_gmt"]
    for field, expected in checks.items():
        if item.get(field) != expected:
            raise MigrationError(
                f"target {target['id']} {field} drift: expected {expected!r}, "
                f"found {item.get(field)!r}"
            )


def plan_target(item: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    _validate_identity(item, target, include_modified=True)
    raw = _raw_content(item)
    if len(raw) != target["raw_length"]:
        raise MigrationError(
            f"target {target['id']} raw length drift: expected {target['raw_length']}, "
            f"found {len(raw)}"
        )
    before_sha = sha256_text(raw)
    if before_sha != target["raw_sha256"]:
        raise MigrationError(
            f"target {target['id']} raw SHA-256 drift: expected "
            f"{target['raw_sha256']}, found {before_sha}"
        )
    after = rewrite_h1(
        raw,
        content_format=target["format"],
        expected_count=target["body_h1_count"],
    )
    after_sha = sha256_text(after)
    if after_sha != target["expected_after_sha256"]:
        raise MigrationError(
            f"target {target['id']} planned SHA-256 does not match the reviewed patch"
        )
    if len(after) != target["expected_after_length"]:
        raise MigrationError(
            f"target {target['id']} planned length does not match the reviewed patch"
        )
    return {
        "target_id": target["id"],
        "content_after": after,
        "before_raw_sha256": before_sha,
        "after_raw_sha256": after_sha,
        "body_h1_count_before": target["body_h1_count"],
        "body_h1_count_after": 0,
    }


def fetch_target(client: WPClient, target: dict[str, Any]) -> dict[str, Any]:
    return client.get(
        f"{target['endpoint']}/{target['id']}",
        params={"context": "edit", "_fields": REST_FIELDS},
    )


def fetch_inventory(client: WPClient) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for endpoint in ("posts", "pages"):
        items.extend(
            client.get_all(
                endpoint,
                params={
                    "status": "publish",
                    "context": "edit",
                    "_fields": REST_FIELDS,
                },
                per_page=100,
            )
        )
    return items


def _target_state(item: dict[str, Any], target: dict[str, Any]) -> str:
    raw = _raw_content(item)
    current_sha = sha256_text(raw)
    if current_sha == target["raw_sha256"]:
        plan_target(item, target)
        return "pending"
    if current_sha == target["expected_after_sha256"]:
        _validate_identity(item, target, include_modified=False)
        if len(raw) != target["expected_after_length"] or count_h1(raw) != 0:
            raise MigrationError(f"target {target['id']} migrated content failed validation")
        return "migrated"
    raise MigrationError(
        f"target {target['id']} raw SHA-256 matches neither reviewed state"
    )


def audit_inventory(
    items: list[dict[str, Any]],
    targets: dict[int, dict[str, Any]],
    homepage: dict[str, Any],
) -> dict[str, Any]:
    found_ids = {int(item["id"]) for item in items}
    required_ids = set(targets) | {int(homepage["id"])}
    missing = sorted(required_ids - found_ids)
    if missing:
        raise MigrationError(f"published inventory is missing reviewed IDs: {missing}")

    states: dict[int, str] = {}
    unknown_h1: list[tuple[int, int]] = []
    for item in items:
        item_id = int(item["id"])
        raw = _raw_content(item)
        body_h1_count = count_h1(raw)
        if item_id in targets:
            states[item_id] = _target_state(item, targets[item_id])
        elif item_id == int(homepage["id"]):
            _validate_identity(item, homepage, include_modified=True)
            if sha256_text(raw) != homepage["raw_sha256"]:
                raise MigrationError("homepage raw SHA-256 drifted from the reviewed exclusion")
            if len(raw) != homepage["raw_length"]:
                raise MigrationError("homepage raw length drifted from the reviewed exclusion")
            if body_h1_count != homepage["body_h1_count"]:
                raise MigrationError("homepage body H1 count drifted from the reviewed exclusion")
        elif body_h1_count:
            unknown_h1.append((item_id, body_h1_count))

    if unknown_h1:
        raise MigrationError(f"unreviewed non-homepage body H1s found: {unknown_h1}")
    return {
        "published_posts_and_pages_scanned": len(items),
        "pending_targets": sorted(
            target_id for target_id, state in states.items() if state == "pending"
        ),
        "migrated_targets": sorted(
            target_id for target_id, state in states.items() if state == "migrated"
        ),
        "homepage_exclusion_id": homepage["id"],
        "unreviewed_body_h1_sources": [],
    }


def _snapshot_target(
    item: dict[str, Any],
    target: dict[str, Any],
    plan: dict[str, Any],
    *,
    snapshot_dir: Path,
    now: dt.datetime,
) -> Path:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.astimezone(dt.timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    path = snapshot_dir / f"kriskrug-issue-353-{target['id']}-{stamp}.json"
    payload = {
        "issue": 353,
        "captured_at": now.astimezone(dt.timezone.utc).isoformat(),
        "target_id": target["id"],
        "endpoint": target["endpoint"],
        "slug": item["slug"],
        "status": item["status"],
        "modified_gmt": item["modified_gmt"],
        "url": item["link"],
        "raw_sha256": plan["before_raw_sha256"],
        "expected_after_sha256": plan["after_raw_sha256"],
        "content_raw": _raw_content(item),
    }
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def _verify_readback(item: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    _validate_identity(item, target, include_modified=False)
    raw = _raw_content(item)
    current_sha = sha256_text(raw)
    if current_sha != target["expected_after_sha256"]:
        raise MigrationError(
            f"target {target['id']} readback SHA-256 does not match the reviewed patch"
        )
    if len(raw) != target["expected_after_length"]:
        raise MigrationError(f"target {target['id']} readback length mismatch")
    body_h1_count = count_h1(raw)
    if body_h1_count != 0:
        raise MigrationError(f"target {target['id']} readback still contains body H1s")
    return {
        "readback_raw_sha256": current_sha,
        "readback_body_h1_count": body_h1_count,
        "readback_modified_gmt": item.get("modified_gmt"),
    }


def apply_target(
    client: WPClient,
    target: dict[str, Any],
    *,
    confirmation: str,
    snapshot_dir: Path = DEFAULT_SNAPSHOT_DIR,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    expected_confirmation = confirmation_for(int(target["id"]))
    if confirmation != expected_confirmation:
        raise MigrationError(
            f"exact confirmation required: {expected_confirmation}"
        )

    before = fetch_target(client, target)
    plan = plan_target(before, target)
    captured_at = now or dt.datetime.now(dt.timezone.utc)
    snapshot_path = _snapshot_target(
        before,
        target,
        plan,
        snapshot_dir=snapshot_dir,
        now=captured_at,
    )
    print(f"pre-write snapshot={snapshot_path}", flush=True)
    client.post(
        f"{target['endpoint']}/{target['id']}",
        {"content": plan["content_after"]},
    )
    readback = fetch_target(client, target)
    result = _verify_readback(readback, target)
    result.update(
        {
            "target_id": target["id"],
            "snapshot_path": str(snapshot_path),
        }
    )
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        nargs="?",
        default="audit",
        choices=("audit", "plan", "apply"),
    )
    parser.add_argument("--target-id", type=int)
    parser.add_argument("--confirm", default="")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--env-path", type=Path, default=DEFAULT_ENV_PATH)
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    manifest = load_manifest(args.manifest)
    targets = targets_by_id(manifest)
    client = WPClient.from_env(args.env_path, timeout=30)

    if args.command == "audit":
        if args.target_id is not None:
            raise MigrationError("audit is a full inventory; omit --target-id")
        result = audit_inventory(
            fetch_inventory(client),
            targets,
            manifest["homepage_exclusion"],
        )
        print(json.dumps(result, indent=2))
        return

    if args.target_id is None:
        raise MigrationError(f"{args.command} requires --target-id")
    if args.target_id not in targets:
        raise MigrationError(f"target ID {args.target_id} is not in the reviewed manifest")
    target = targets[args.target_id]

    if args.command == "plan":
        plan = plan_target(fetch_target(client, target), target)
        plan.pop("content_after")
        print(json.dumps(plan, indent=2))
        return

    result = apply_target(
        client,
        target,
        confirmation=args.confirm,
        snapshot_dir=args.snapshot_dir,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
