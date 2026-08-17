#!/usr/bin/env python3
"""Issue #826: recategorize five posts and repair the dead contact href on 2819.

Dry-run by default. Writes are gated on ID→slug match, live category (or href)
still matching the recorded defect, and a fresh context=edit snapshot before
each POST.

    make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py'
    make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --apply'
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
TARGETS_PATH = (
    REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-826/targets.json"
)
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-826-taxonomy"
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
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-826"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def write_snapshot(post: dict, post_id: int, stamp: str) -> Path:
    SNAPSHOT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    SNAPSHOT_DIR.chmod(0o700)
    path = SNAPSHOT_DIR / f"rest-post-{post_id}-before-{stamp}.json"
    temporary = path.with_suffix(".json.tmp")
    serialized = json.dumps(post, indent=2, ensure_ascii=False)
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
        if json.loads(temporary.read_text(encoding="utf-8")) != post:
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


def raw_body(post: dict) -> str:
    content = post.get("content")
    body = content.get("raw") if isinstance(content, dict) else None
    if not isinstance(body, str):
        sys.exit(f"[ABORT] {post.get('id')}: content.raw missing from context=edit.")
    return body


def validate_identity(live: dict, spec: dict) -> None:
    post_id = spec["id"]
    if live.get("id") != post_id:
        sys.exit(f"[ABORT] {post_id}: REST id is {live.get('id')!r}.")
    if live.get("slug") != spec["slug"]:
        sys.exit(
            f"[ABORT] {post_id}: slug is {live.get('slug')!r}, expected {spec['slug']!r}."
        )


def swap_primary_category(
    live_categories: list[int], from_id: int, to_id: int
) -> list[int] | None:
    if from_id not in live_categories:
        if to_id in live_categories:
            return None
        raise ValueError(
            f"live categories {live_categories} do not contain from_id {from_id}"
        )
    if to_id in live_categories:
        raise ValueError(
            f"live categories {live_categories} already contain to_id {to_id} "
            f"and still contain from_id {from_id}"
        )
    return [to_id if cat == from_id else cat for cat in live_categories]


def rewrite_footer_pillar(
    raw: str, old_href: str, old_label: str, new_href: str, new_label: str
) -> str | None:
    if FOOTER_SENTINEL not in raw:
        return None
    needle = f'<a href="{old_href}">{old_label}</a>'
    already = f'<a href="{new_href}">{new_label}</a>'
    count = raw.count(needle)
    if count == 0:
        if already in raw:
            return None
        raise ValueError(
            "baked footer present but neither the old nor the new pillar <a> was found"
        )
    if count != 1:
        raise ValueError(f"old pillar <a> occurs {count} times; expected 1")
    return raw.replace(needle, already, 1)


def plan_post(spec: dict, live: dict, targets: dict) -> dict | None:
    post_id = spec["id"]
    term_ids = targets["term_ids"]
    payload: dict = {}
    notes: list[str] = []

    if spec.get("href_repair"):
        body = raw_body(live)
        find = targets["contact_find"]
        replace = targets["contact_replace"]
        count = body.count(find)
        if count == 0 and replace in body:
            notes.append("contact href already repaired")
        elif count != 1:
            raise ValueError(
                f"{post_id}: {find!r} occurs {count} times in content.raw; expected 1"
            )
        else:
            payload["content"] = body.replace(find, replace, 1)
            notes.append("href repair")
    else:
        from_id = term_ids[spec["from_category"]]
        to_id = term_ids[spec["to_category"]]
        live_cats = list(live.get("categories") or [])
        new_cats = swap_primary_category(live_cats, from_id, to_id)
        if new_cats is None:
            notes.append("category already swapped")
        else:
            payload["categories"] = new_cats
            notes.append(f"categories {live_cats} -> {new_cats}")

        old_href = spec.get("old_pillar_href")
        old_label = spec.get("old_pillar_label")
        if old_href and old_label:
            pillar = targets["pillars"][str(to_id)]
            body = raw_body(live)
            try:
                rewritten = rewrite_footer_pillar(
                    body, old_href, old_label, pillar["url"], pillar["label"]
                )
            except ValueError as exc:
                raise ValueError(f"{post_id}: {exc}") from exc
            if rewritten is None:
                notes.append("no footer rewrite needed")
            else:
                payload["content"] = rewritten
                notes.append("footer pillar swap")

    if not payload:
        print(f"[SKIP] {post_id}: {'; '.join(notes) or 'nothing to do'}.")
        return None
    return {"spec": spec, "live": live, "payload": payload, "notes": notes}


def fetch_live(post_id: int, header: str) -> dict:
    return request(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit", header)


def print_plan(item: dict) -> None:
    spec = item["spec"]
    payload = item["payload"]
    print(f"[PLAN] {spec['id']} {spec['slug']}: {'; '.join(item['notes'])}")
    if "categories" in payload:
        print(f"        categories -> {payload['categories']}")
    if "content" in payload:
        old = raw_body(item["live"])
        new = payload["content"]
        print(f"        content.raw {len(old)} chars -> {len(new)} chars")


def apply_item(item: dict, header: str, stamp: str, do_apply: bool) -> None:
    spec = item["spec"]
    post_id = spec["id"]
    print_plan(item)
    if not do_apply:
        return
    live = fetch_live(post_id, header)
    validate_identity(live, spec)
    replanned = plan_post(spec, live, load_targets())
    if replanned is None:
        return
    write_snapshot(live, post_id, stamp)
    updated = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit",
        header,
        replanned["payload"],
    )
    validate_identity(updated, spec)
    print(f"[WROTE] {post_id}")


def restore_snapshot(path: Path, header: str, do_apply: bool) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    post_id = snapshot.get("id")
    allowed = {row["id"] for row in load_targets()["posts"]}
    if post_id not in allowed:
        sys.exit(f"[ABORT] snapshot id {post_id} is not in the #826 set.")
    spec = next(row for row in load_targets()["posts"] if row["id"] == post_id)
    validate_identity(snapshot, spec)
    payload = {
        "categories": snapshot.get("categories"),
        "content": raw_body(snapshot),
    }
    print(f"[RESTORE] {post_id} from {path}")
    if not do_apply:
        return
    live = fetch_live(post_id, header)
    validate_identity(live, spec)
    write_snapshot(live, post_id, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    request(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit", header, payload)
    print(f"[WROTE] {post_id} restored")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply issue #826 taxonomy repair.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--post-id", type=int)
    parser.add_argument("--restore", type=Path)
    args = parser.parse_args()
    header = auth_header()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.restore:
        restore_snapshot(args.restore, header, args.apply)
        return 0

    targets = load_targets()
    rows = targets["posts"]
    if args.post_id:
        rows = [row for row in rows if row["id"] == args.post_id]
        if not rows:
            sys.exit(f"[ABORT] unknown --post-id {args.post_id}")

    planned = []
    for spec in rows:
        live = fetch_live(spec["id"], header)
        validate_identity(live, spec)
        try:
            item = plan_post(spec, live, targets)
        except ValueError as exc:
            sys.exit(f"[ABORT] {exc}")
        if item is not None:
            planned.append(item)

    if not planned:
        print("[OK] nothing pending.")
        return 0

    for item in planned:
        apply_item(item, header, stamp, args.apply)
    if not args.apply:
        print("[DRY-RUN] no WordPress writes. Pass --apply after KK approves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
