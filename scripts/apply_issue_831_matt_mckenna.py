#!/usr/bin/env python3
"""Issue #831: add Matt McKenna to the /ai-conversations/ hub.

Dry-run by default. Writes are gated on ID->slug match, exact text-match
insertion, child-1 (#826) category proof, and a fresh context=edit snapshot.

    python3 scripts/apply_issue_831_matt_mckenna.py --from-files
    make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py'
    make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py --apply'
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
PACK = REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-831"
TARGETS_PATH = PACK / "targets.json"
BEFORE_DIR = PACK / "before"
AFTER_DIR = PACK / "after"
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-831-matt-mckenna"
BASE_URL = "https://kriskrug.co"
FOOTER_SENTINEL = "kk-collection-footer"


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
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-831"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def write_snapshot(item: dict, stamp: str) -> Path:
    SNAPSHOT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    SNAPSHOT_DIR.chmod(0o700)
    kind = "page" if item.get("type") == "page" else "post"
    path = SNAPSHOT_DIR / f"rest-{kind}-{item['id']}-before-{stamp}.json"
    temporary = path.with_suffix(".json.tmp")
    serialized = json.dumps(item, indent=2, ensure_ascii=False)
    json.loads(serialized)
    temporary_created = False
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        temporary_created = True
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
        sys.exit(f"[ABORT] Snapshot creation failed for {path}: {exc}")
    finally:
        if temporary_created:
            temporary.unlink(missing_ok=True)
    print(f"[SNAPSHOT] {path}")
    return path


def raw_body(item: dict) -> str:
    content = item.get("content")
    body = content.get("raw") if isinstance(content, dict) else None
    if not isinstance(body, str):
        sys.exit(f"[ABORT] {item.get('id')}: content.raw missing from context=edit.")
    return body


def anchor_needle(row: dict) -> str:
    return f'<a href="{row["href"]}">{row["text"]}</a>'


def row_is_present(body: str, row: dict) -> bool:
    if row.get("link_style") == "card":
        return row["href"] in body and row["text"] in body
    return anchor_needle(row) in body


def already_applied(body: str, spec: dict) -> bool:
    return all(row_is_present(body, row) for row in spec["anchors"])


def inserted_fragment(spec: dict) -> str:
    find = spec["find"]
    replace = spec["replace"]
    prefix = os.path.commonprefix([find, replace])
    find_rest = find[len(prefix) :]
    replace_rest = replace[len(prefix) :]
    while find_rest and replace_rest and find_rest[-1] == replace_rest[-1]:
        find_rest = find_rest[:-1]
        replace_rest = replace_rest[:-1]
    return replace_rest


def rewrite_body(body: str, spec: dict, targets: dict) -> str | None:
    if already_applied(body, spec):
        return None
    find = spec["find"]
    replace = spec["replace"]
    count = body.count(find)
    if count != 1:
        raise ValueError(
            f"{spec['id']}: find needle occurs {count} times; expected 1. "
            "Insert by text match, not a stale block index."
        )
    added = inserted_fragment(spec)
    if "\u2014" in added or "\u2013" in added:
        raise ValueError(f"{spec['id']}: inserted copy contains a dash codepoint")
    if any(ord(char) > 127 for char in added):
        raise ValueError(f"{spec['id']}: inserted copy is not ASCII; use NCR")
    rewritten = body.replace(find, replace, 1)
    if spec.get("preserve_existing_cards"):
        for href in targets["preserve_existing_hrefs"]:
            if rewritten.count(href) != body.count(href):
                raise ValueError(f"{spec['id']}: existing card href {href} changed")
        if rewritten.count("aurora-media-card") != body.count("aurora-media-card") + 1:
            raise ValueError(f"{spec['id']}: expected exactly one new media card")
    if spec.get("preserve_footer"):
        if body.count(FOOTER_SENTINEL) != rewritten.count(FOOTER_SENTINEL):
            raise ValueError(f"{spec['id']}: kk-collection-footer count changed")
    for forbidden in targets.get("forbidden_href_substrings") or []:
        if forbidden in rewritten and forbidden not in body:
            raise ValueError(f"{spec['id']}: forbidden href {forbidden} was added")
    for row in spec["anchors"]:
        if row.get("link_style") == "card":
            if rewritten.count(row["href"]) != 1 or rewritten.count(row["text"]) != 1:
                raise ValueError(f"{spec['id']}: expected one card {row['text']!r}")
            continue
        needle = anchor_needle(row)
        if rewritten.count(needle) != 1:
            raise ValueError(f"{spec['id']}: expected one {needle!r}")
    return rewritten


def validate_identity(live: dict, spec: dict) -> None:
    if live.get("id") != spec["id"]:
        sys.exit(f"[ABORT] {spec['id']}: REST id is {live.get('id')!r}.")
    if live.get("slug") != spec["slug"]:
        sys.exit(
            f"[ABORT] {spec['id']}: slug is {live.get('slug')!r}, "
            f"expected {spec['slug']!r}."
        )


def rest_url(spec: dict) -> str:
    return f"{BASE_URL}/wp-json/wp/v2/{spec['kind']}/{spec['id']}?context=edit"


def fetch_live(spec: dict, header: str) -> dict:
    return request(rest_url(spec), header)


def child1_is_live(header: str, targets: dict) -> tuple[bool, list[str]]:
    notes: list[str] = []
    ready = True
    for row in targets["child1_gate"]:
        live = request(
            f"{BASE_URL}/wp-json/wp/v2/posts/{row['id']}?_fields=id,slug,categories",
            header,
        )
        if live.get("slug") != row["slug"]:
            ready = False
            notes.append(f"{row['id']} slug {live.get('slug')!r}")
            continue
        cats = list(live.get("categories") or [])
        if row["to_category"] not in cats or row["from_category"] in cats:
            ready = False
            notes.append(f"{row['id']} categories {cats}")
        else:
            notes.append(f"{row['id']} ok {cats}")
    return ready, notes


def plan_item(spec: dict, body: str, targets: dict) -> dict | None:
    try:
        rewritten = rewrite_body(body, spec, targets)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc
    if rewritten is None:
        print(f"[SKIP] {spec['id']}: exact href+anchor already present.")
        return None
    return {"spec": spec, "before": body, "after": rewritten}


def print_plan(item: dict) -> None:
    spec = item["spec"]
    print(
        f"[PLAN] {spec['kind']}/{spec['id']} {spec['slug']}: "
        f"{len(item['before'])} chars -> {len(item['after'])} chars"
    )
    for row in spec["anchors"]:
        print(f"        row {row['row']}: {row['text']!r} -> {row['href']}")


def write_after_files(planned: list[dict]) -> None:
    AFTER_DIR.mkdir(parents=True, exist_ok=True)
    for item in planned:
        spec = item["spec"]
        path = AFTER_DIR / f"{spec['kind'][:-1]}-{spec['id']}-content.raw.html"
        path.write_text(item["after"], encoding="utf-8")
        print(f"[AFTER] {path}")


def apply_item(item: dict, header: str, stamp: str, do_apply: bool) -> None:
    print_plan(item)
    if not do_apply:
        return
    spec = item["spec"]
    live = fetch_live(spec, header)
    validate_identity(live, spec)
    replanned = plan_item(spec, raw_body(live), load_targets())
    if replanned is None:
        return
    write_snapshot(live, stamp)
    updated = request(rest_url(spec), header, {"content": replanned["after"]})
    validate_identity(updated, spec)
    print(f"[WROTE] {spec['id']}")


def restore_snapshot(path: Path, header: str, do_apply: bool) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    allowed = {row["id"] for row in load_targets()["items"]}
    post_id = snapshot.get("id")
    if post_id not in allowed:
        sys.exit(f"[ABORT] snapshot id {post_id} is not in the #831 set.")
    spec = next(row for row in load_targets()["items"] if row["id"] == post_id)
    validate_identity(snapshot, spec)
    payload = {"content": raw_body(snapshot)}
    print(f"[RESTORE] {post_id} from {path}")
    if not do_apply:
        return
    live = fetch_live(spec, header)
    validate_identity(live, spec)
    write_snapshot(live, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    request(rest_url(spec), header, payload)
    print(f"[WROTE] {post_id} restored")


def load_before_body(spec: dict) -> str:
    path = BEFORE_DIR / f"{spec['kind'][:-1]}-{spec['id']}-content.raw.html"
    if not path.is_file():
        sys.exit(f"[ABORT] missing before-file {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply issue #831 Matt McKenna hub links."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--from-files", action="store_true")
    parser.add_argument("--item-id", type=int)
    parser.add_argument("--restore", type=Path)
    parser.add_argument(
        "--allow-before-826",
        action="store_true",
        help="Unsafe. Bypass the child-1 category gate. Do not use on production.",
    )
    args = parser.parse_args()
    targets = load_targets()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.restore:
        restore_snapshot(args.restore, auth_header(), args.apply)
        return 0

    rows = targets["items"]
    if args.item_id:
        rows = [row for row in rows if row["id"] == args.item_id]
        if not rows:
            sys.exit(f"[ABORT] unknown --item-id {args.item_id}")
        forbidden = {row["id"] for row in targets["do_not_touch"]}
        if args.item_id in forbidden:
            sys.exit(f"[ABORT] {args.item_id} is do-not-touch for #831.")

    if args.from_files:
        planned = []
        for spec in rows:
            try:
                item = plan_item(spec, load_before_body(spec), targets)
            except ValueError as exc:
                sys.exit(f"[ABORT] {exc}")
            if item is not None:
                planned.append(item)
                print_plan(item)
        if not planned:
            print("[OK] nothing pending.")
            return 0
        write_after_files(planned)
        print("[FROM-FILES] wrote after/ payloads. No WordPress writes.")
        return 0

    header = auth_header()
    if args.apply and not args.allow_before_826:
        ready, notes = child1_is_live(header, targets)
        for note in notes:
            print(f"[826] {note}")
        if not ready:
            sys.exit(
                "[ABORT] #826 category fixes are not live. "
                "Need 3330 out of 1757 into 1676. Do not PATCH 12319/2833/2423 yet."
            )

    planned = []
    for spec in rows:
        live = fetch_live(spec, header)
        validate_identity(live, spec)
        try:
            item = plan_item(spec, raw_body(live), targets)
        except ValueError as exc:
            sys.exit(f"[ABORT] {exc}")
        if item is not None:
            item["live"] = live
            planned.append(item)

    if not planned:
        print("[OK] nothing pending.")
        return 0

    for item in planned:
        apply_item(item, header, stamp, args.apply)
    if not args.apply:
        print(
            "[DRY-RUN] no WordPress writes. Pass --apply after #826 is live and KK approves."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
