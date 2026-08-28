#!/usr/bin/env python3
"""Prepare or apply the six issue #833 MBO links.

Dry-run by default. Live writes are single-item only and use exact identity,
dependency, snapshot, content-only payload, and authenticated readback gates.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-833"
TARGETS_PATH = PACK / "targets.json"
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-833-mbo-links"
BASE_URL = "https://kriskrug.co"
FOOTER_OPEN = '<!-- wp:paragraph {"className":"kk-collection-footer"} -->'


def load_targets() -> dict:
    return json.loads(TARGETS_PATH.read_text(encoding="utf-8"))


def auth_header() -> str:
    user = os.getenv("WP_API_USERNAME") or os.getenv("WP_USER")
    password = os.getenv("WP_API_PASSWORD") or os.getenv("WP_APP_PASSWORD")
    if not user or not password:
        sys.exit("[ABORT] WordPress credentials unresolved. Run through Varlock.")
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def request(url: str, header: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-833"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)


def anchor_html(operation: dict) -> str:
    return f'<a href="{operation["href"]}">{operation["text"]}</a>'


def inserted_fragment(operation: dict) -> str:
    if operation.get("kind") == "append_to_paragraph":
        return operation["append_html"]
    find = operation["find"]
    replace = operation["replace"]
    prefix_length = 0
    for before, after in zip(find, replace):
        if before != after:
            break
        prefix_length += 1
    find_rest = find[prefix_length:]
    replace_rest = replace[prefix_length:]
    while find_rest and replace_rest and find_rest[-1] == replace_rest[-1]:
        find_rest = find_rest[:-1]
        replace_rest = replace_rest[:-1]
    return replace_rest


def fixture_body(spec: dict) -> str:
    parts = []
    if spec.get("preserve_href_counts"):
        parts.append('<p><a href="https://kriskrug.co/glossary/">Glossary</a></p>')
    for operation in spec["operations"]:
        if operation.get("kind") == "append_to_paragraph":
            parts.append(f"<p>Before <strong>{operation['find']}</strong> after.</p>")
        else:
            parts.append(operation["find"])
    if spec["id"] == 3948:
        parts.append(" in a much larger story.</p>")
    if spec["id"] == 3814:
        parts.append('<h3 class="wp-block-heading">How To Practice MBOs</h3>')
    if spec.get("preserve_footer"):
        if FOOTER_OPEN not in "\n".join(parts):
            parts.append(FOOTER_OPEN)
        parts.extend(
            [
                '<p class="kk-collection-footer">Footer</p>',
                "<!-- /wp:paragraph -->",
            ]
        )
    return "\n".join(parts)


def rewrite_operation(body: str, operation: dict, item_id: int) -> str:
    find = operation["find"]
    count = body.count(find)
    if count != 1:
        raise ValueError(
            f"{item_id}: row {operation['row']} marker occurs {count} times; expected 1"
        )
    if operation.get("kind") != "append_to_paragraph":
        return body.replace(find, operation["replace"], 1)
    marker_at = body.index(find)
    paragraph_at = body.rfind("<p", 0, marker_at)
    paragraph_end = body.find("</p>", marker_at)
    if paragraph_at < 0 or paragraph_end < 0:
        raise ValueError(
            f"{item_id}: row {operation['row']} paragraph boundary missing"
        )
    return body[:paragraph_end] + operation["append_html"] + body[paragraph_end:]


def rewrite_body(body: str, spec: dict) -> str | None:
    original = body
    rewritten = body
    changed = False
    for operation in spec["operations"]:
        anchor = anchor_html(operation)
        anchor_count = rewritten.count(anchor)
        if anchor_count == 1:
            continue
        if anchor_count != 0:
            raise ValueError(
                f"{spec['id']}: row {operation['row']} anchor occurs {anchor_count} times"
            )
        added = inserted_fragment(operation)
        if "\u2014" in added or "\u2013" in added:
            raise ValueError(
                f"{spec['id']}: row {operation['row']} adds a dash codepoint"
            )
        rewritten = rewrite_operation(rewritten, operation, spec["id"])
        if rewritten.count(anchor) != 1:
            raise ValueError(
                f"{spec['id']}: row {operation['row']} anchor count is not 1"
            )
        changed = True
    if not changed:
        return None
    if spec.get("preserve_footer"):
        if original.count(FOOTER_OPEN) != 1 or rewritten.count(FOOTER_OPEN) != 1:
            raise ValueError(f"{spec['id']}: collection footer structure drifted")
        original_footer = original[original.index(FOOTER_OPEN) :]
        rewritten_footer = rewritten[rewritten.index(FOOTER_OPEN) :]
        if original_footer != rewritten_footer:
            raise ValueError(f"{spec['id']}: collection footer content changed")
        footer_at = rewritten.find(FOOTER_OPEN)
        for operation in spec["operations"]:
            if rewritten.find(anchor_html(operation)) > footer_at:
                raise ValueError(
                    f"{spec['id']}: row {operation['row']} landed after footer"
                )
    for href in spec.get("preserve_href_counts") or []:
        if original.count(href) != rewritten.count(href):
            raise ValueError(f"{spec['id']}: {href} href count changed")
    if spec["id"] == 3814:
        ethics_at = rewritten.find(spec["operations"][1]["text"])
        heading_at = rewritten.find("How To Practice MBOs")
        if heading_at >= 0 and ethics_at > heading_at:
            raise ValueError("3814: AI ethics link landed after How To Practice MBOs")
    return rewritten


def raw_body(item: dict) -> str:
    content = item.get("content")
    body = content.get("raw") if isinstance(content, dict) else None
    if not isinstance(body, str):
        sys.exit(f"[ABORT] {item.get('id')}: content.raw missing from context=edit")
    return body


def validate_identity(live: dict, spec: dict) -> None:
    for field in ("id", "slug", "status", "date"):
        if live.get(field) != spec[field]:
            sys.exit(
                f"[ABORT] {spec['id']}: {field} is {live.get(field)!r}, "
                f"expected {spec[field]!r}."
            )
    title = live.get("title") or {}
    observed_title = title.get("raw") or title.get("rendered")
    if observed_title != spec["title"]:
        sys.exit(
            f"[ABORT] {spec['id']}: title is {observed_title!r}, expected {spec['title']!r}."
        )
    if "categories" in spec and live.get("categories") != spec["categories"]:
        sys.exit(
            f"[ABORT] {spec['id']}: categories is {live.get('categories')!r}, "
            f"expected {spec['categories']!r}."
        )


def rest_url(spec: dict) -> str:
    return f"{BASE_URL}/wp-json/wp/v2/{spec['kind']}/{spec['id']}?context=edit"


def fetch_live(spec: dict, header: str) -> dict:
    return request(rest_url(spec), header)


def assert_dependency_live(header: str, targets: dict) -> None:
    gate = targets["dependency_gate"]
    live = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{gate['id']}"
        "?_fields=id,slug,status,categories",
        header,
    )
    categories = list(live.get("categories") or [])
    if (
        live.get("id") != gate["id"]
        or live.get("slug") != gate["slug"]
        or live.get("status") != gate["status"]
        or gate["required_category"] not in categories
        or gate["forbidden_category"] in categories
    ):
        sys.exit(f"[ABORT] #826 dependency is not live: observed {live!r}")


def write_snapshot(item: dict, stamp: str) -> Path:
    SNAPSHOT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    SNAPSHOT_DIR.chmod(0o700)
    kind = "page" if item.get("type") == "page" else "post"
    path = SNAPSHOT_DIR / f"rest-{kind}-{item['id']}-before-{stamp}.json"
    temporary = path.with_suffix(".json.tmp")
    serialized = json.dumps(item, indent=2, ensure_ascii=False)
    json.loads(serialized)
    created = False
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        created = True
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        if json.loads(temporary.read_text(encoding="utf-8")) != item:
            raise ValueError("snapshot readback differs from source")
        temporary.chmod(0o600)
        os.link(temporary, path)
    except (OSError, ValueError) as exc:
        sys.exit(f"[ABORT] snapshot creation failed for {path}: {exc}")
    finally:
        if created:
            temporary.unlink(missing_ok=True)
    print(f"[SNAPSHOT] {path}")
    return path


def plan_item(spec: dict, body: str) -> dict | None:
    try:
        after = rewrite_body(body, spec)
    except ValueError as exc:
        sys.exit(f"[ABORT] {exc}")
    if after is None:
        print(f"[SKIP] {spec['id']}: all exact #833 anchors already present")
        return None
    return {"spec": spec, "before": body, "after": after}


def print_plan(item: dict) -> None:
    spec = item["spec"]
    print(
        f"[PLAN] {spec['kind']}/{spec['id']} {spec['slug']}: "
        f"{len(item['before'])} chars -> {len(item['after'])} chars"
    )
    for operation in spec["operations"]:
        print(
            f"        row {operation['row']}: {operation['text']!r} -> "
            f"{operation['href']}"
        )


def apply_item(item: dict, header: str, stamp: str) -> None:
    spec = item["spec"]
    fresh = fetch_live(spec, header)
    validate_identity(fresh, spec)
    replanned = plan_item(spec, raw_body(fresh))
    if replanned is None:
        return
    write_snapshot(fresh, stamp)
    updated = request(rest_url(spec), header, {"content": replanned["after"]})
    validate_identity(updated, spec)
    readback = fetch_live(spec, header)
    validate_identity(readback, spec)
    if raw_body(readback) != replanned["after"]:
        sys.exit(f"[ABORT] {spec['id']}: authenticated readback differs from payload")
    print(f"[WROTE] {spec['id']} and verified content.raw readback")


def restore_snapshot(path: Path, header: str, do_apply: bool, targets: dict) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    item_id = snapshot.get("id")
    rows = [row for row in targets["items"] if row["id"] == item_id]
    if not rows:
        sys.exit(f"[ABORT] snapshot id {item_id} is not in the #833 write set")
    spec = rows[0]
    validate_identity(snapshot, spec)
    print(f"[RESTORE] {item_id} from {path}")
    if not do_apply:
        print("[DRY-RUN] no WordPress restore write")
        return
    fresh = fetch_live(spec, header)
    validate_identity(fresh, spec)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_snapshot(fresh, stamp)
    request(rest_url(spec), header, {"content": raw_body(snapshot)})
    readback = fetch_live(spec, header)
    validate_identity(readback, spec)
    if raw_body(readback) != raw_body(snapshot):
        sys.exit(f"[ABORT] {item_id}: restore readback differs from snapshot")
    print(f"[WROTE] {item_id} restored and verified")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply issue #833 MBO links safely.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--from-spec", action="store_true")
    parser.add_argument("--item-id", type=int)
    parser.add_argument("--restore", type=Path)
    args = parser.parse_args()
    targets = load_targets()

    if args.apply and args.item_id is None and args.restore is None:
        sys.exit("[ABORT] --apply requires one exact --item-id")

    if args.from_spec:
        for spec in targets["items"]:
            planned = plan_item(spec, fixture_body(spec))
            if planned is None:
                sys.exit(f"[ABORT] {spec['id']}: fixture unexpectedly already applied")
            print_plan(planned)
        print("[FROM-SPEC] all five transforms valid. No network or WordPress writes.")
        return 0

    header = auth_header()
    assert_dependency_live(header, targets)

    if args.restore:
        restore_snapshot(args.restore, header, args.apply, targets)
        return 0

    rows = targets["items"]
    if args.item_id is not None:
        rows = [row for row in rows if row["id"] == args.item_id]
        if not rows:
            sys.exit(f"[ABORT] unknown --item-id {args.item_id}")

    planned = []
    for spec in rows:
        live = fetch_live(spec, header)
        validate_identity(live, spec)
        item = plan_item(spec, raw_body(live))
        if item is not None:
            planned.append(item)
            print_plan(item)

    if not planned:
        print("[OK] nothing pending")
        return 0

    if not args.apply:
        print(
            "[DRY-RUN] no WordPress writes. Fresh explicit live approval is required."
        )
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    apply_item(planned[0], header, stamp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
