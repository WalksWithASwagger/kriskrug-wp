#!/usr/bin/env python3
"""Issue #828: prepare and safely apply the model-photographer checklist.

Dry-run by default. Live writes require a committed review hash, an exact
``--item-id``, a fresh context=edit snapshot, and independent readback.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-828"
TARGETS_PATH = PACK / "targets.json"
DRAFT_BODY_PATH = PACK / "post-body.html"
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-828-negotiation-checklist"
BASE_URL = "https://kriskrug.co"
FOOTER_OPEN = '<!-- wp:paragraph {"className":"kk-collection-footer"} -->'
FOOTER_SENTINEL = "kk-collection-footer"
STYLE_OPEN = "<style>"
STYLE_CLOSE = "</style>"


def load_targets() -> dict:
    return json.loads(TARGETS_PATH.read_text(encoding="utf-8"))


def load_draft_body() -> str:
    return DRAFT_BODY_PATH.read_text(encoding="utf-8").strip()


def load_before_body(spec: dict) -> str:
    path = REPO_ROOT / spec["before_path"]
    if not path.is_file():
        sys.exit(f"[ABORT] missing baseline {path}")
    return path.read_text(encoding="utf-8").rstrip("\n")


def load_after_body(spec: dict) -> str:
    rewritten = rewrite_body(load_before_body(spec), spec, load_targets())
    if rewritten is None:
        raise ValueError(f"{spec['id']}: baseline already contains the #828 change")
    return rewritten


def auth_header() -> str:
    user = os.getenv("WP_API_USERNAME") or os.getenv("WP_USER")
    password = os.getenv("WP_API_PASSWORD") or os.getenv("WP_APP_PASSWORD")
    if not user or not password:
        sys.exit("[ABORT] WordPress credentials unresolved. Run through Varlock.")
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def request(url: str, header: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-828"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)


def raw_body(item: dict) -> str:
    content = item.get("content")
    body = content.get("raw") if isinstance(content, dict) else None
    if not isinstance(body, str):
        sys.exit(f"[ABORT] {item.get('id')}: content.raw missing from context=edit.")
    return body


def collection_footer(body: str) -> str:
    if body.count(FOOTER_OPEN) != 1:
        raise ValueError(
            f"collection footer opener occurs {body.count(FOOTER_OPEN)} times; expected 1"
        )
    footer = body[body.index(FOOTER_OPEN) :]
    if footer.count(FOOTER_SENTINEL) != 2:
        raise ValueError("collection footer structure drifted")
    return footer


def style_block(body: str) -> str:
    start = body.find(STYLE_OPEN)
    end = body.find(STYLE_CLOSE)
    if start < 0 or end < 0 or end < start:
        raise ValueError("inline <style> block missing")
    return body[start : end + len(STYLE_CLOSE)]


def style_sha256(body: str) -> str:
    return hashlib.sha256(style_block(body).encode("utf-8")).hexdigest()


def visible_text(body: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()


def validate_draft_body(body: str, targets: dict) -> dict:
    if targets["dead_href"] in body:
        raise ValueError("draft still contains the dead ModelMayhem href")
    if FOOTER_SENTINEL in body:
        raise ValueError("draft must not bake the generated collection footer")
    if "\u2014" in body or "\u2013" in body:
        raise ValueError("draft contains an em dash or en dash")
    if (
        "ModelMayhem forum thread" not in body
        or "Wayback Machine has no copy" not in body
    ):
        raise ValueError("draft must preserve the honest lost-source note")
    text = visible_text(body)
    word_count = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'+-]*", text))
    if word_count < 400:
        raise ValueError(f"draft has {word_count} words; expected at least 400")
    lower = text.lower()
    covered = {
        topic
        for topic, needles in targets["required_topics"].items()
        if all(needle.lower() in lower for needle in needles)
    }
    missing = sorted(set(targets["required_topics"]) - covered)
    if missing:
        raise ValueError(f"draft misses required topics: {', '.join(missing)}")
    for forbidden in ("synergy", "thought leader", "excited to announce"):
        if forbidden in lower:
            raise ValueError(f"draft contains forbidden voice phrase {forbidden!r}")
    closing = spec_anchor(targets["items"][0])
    if body.count(closing) != 1:
        raise ValueError("draft must contain the exact row-37 photography link once")
    return {"word_count": word_count, "covered_topics": covered}


def spec_anchor(spec: dict, index: int = 0) -> str:
    anchor = spec["anchors"][index]
    return f'<a href="{anchor["href"]}">{anchor["text"]}</a>'


def already_applied(body: str, spec: dict, targets: dict) -> bool:
    anchors_present = all(
        spec_anchor(spec, index) in body for index in range(len(spec["anchors"]))
    )
    if spec.get("replace_body"):
        return anchors_present and targets["dead_href"] not in body
    return anchors_present


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
    if already_applied(body, spec, targets):
        return None

    if spec.get("replace_body"):
        if body.count(targets["dead_href"]) != 1:
            raise ValueError(
                f"{spec['id']}: dead href occurs {body.count(targets['dead_href'])} times; expected 1"
            )
        footer = collection_footer(body)
        draft = load_draft_body()
        validate_draft_body(draft, targets)
        rewritten = f"{draft}\n\n{footer}"
        if collection_footer(rewritten) != footer:
            raise ValueError(f"{spec['id']}: collection footer changed")
    else:
        find = spec["find"]
        count = body.count(find)
        if count != 1:
            raise ValueError(
                f"{spec['id']}: find needle occurs {count} times; expected 1. "
                "Insert by text match, not a stale block index."
            )
        added = inserted_fragment(spec)
        if "\u2014" in added or "\u2013" in added:
            raise ValueError(f"{spec['id']}: inserted copy contains a dash codepoint")
        rewritten = body.replace(find, spec["replace"], 1)

    if spec.get("preserve_footer"):
        if body.count(FOOTER_SENTINEL) != rewritten.count(FOOTER_SENTINEL):
            raise ValueError(f"{spec['id']}: collection footer count changed")
        anchor_at = rewritten.find(spec["anchors"][0]["text"])
        footer_at = rewritten.find(FOOTER_SENTINEL)
        if anchor_at < 0 or footer_at < 0 or anchor_at > footer_at:
            raise ValueError(f"{spec['id']}: new link is not before the footer")
    if spec.get("preserve_style"):
        if style_sha256(body) != targets["style_sha256_12013"]:
            raise ValueError(f"{spec['id']}: live style hash drifted")
        if style_sha256(rewritten) != style_sha256(body):
            raise ValueError(f"{spec['id']}: rewrite touched the style block")
    for index in range(len(spec["anchors"])):
        needle = spec_anchor(spec, index)
        if rewritten.count(needle) != 1:
            raise ValueError(f"{spec['id']}: expected one {needle!r}")
    if targets["dead_href"] in rewritten:
        raise ValueError(f"{spec['id']}: dead ModelMayhem href remains")
    return rewritten


def validate_identity(live: dict, spec: dict) -> None:
    if live.get("id") != spec["id"]:
        sys.exit(f"[ABORT] {spec['id']}: REST id is {live.get('id')!r}.")
    if live.get("slug") != spec["slug"]:
        sys.exit(
            f"[ABORT] {spec['id']}: slug is {live.get('slug')!r}, expected {spec['slug']!r}."
        )
    if "title" in spec:
        title = live.get("title") or {}
        observed = title.get("raw") or title.get("rendered")
        if observed != spec["title"]:
            sys.exit(
                f"[ABORT] {spec['id']}: title is {observed!r}, expected {spec['title']!r}."
            )
    for field in ("date", "categories", "tags"):
        if field in spec and live.get(field) != spec[field]:
            sys.exit(
                f"[ABORT] {spec['id']}: {field} is {live.get(field)!r}, expected {spec[field]!r}."
            )


def rest_url(spec: dict) -> str:
    return f"{BASE_URL}/wp-json/wp/v2/{spec['kind']}/{spec['id']}?context=edit"


def fetch_live(spec: dict, header: str) -> dict:
    return request(rest_url(spec), header)


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


def plan_item(spec: dict, body: str, targets: dict) -> dict | None:
    rewritten = rewrite_body(body, spec, targets)
    if rewritten is None:
        print(f"[SKIP] {spec['id']}: exact #828 change already present.")
        return None
    return {"spec": spec, "before": body, "after": rewritten}


def print_plan(item: dict) -> None:
    spec = item["spec"]
    print(
        f"[PLAN] {spec['kind']}/{spec['id']} {spec['slug']}: "
        f"{len(item['before'])} chars -> {len(item['after'])} chars"
    )
    for anchor in spec["anchors"]:
        print(f"        row {anchor['row']}: {anchor['text']!r} -> {anchor['href']}")


def apply_item(item: dict, header: str, stamp: str, targets: dict) -> None:
    spec = item["spec"]
    fresh = fetch_live(spec, header)
    validate_identity(fresh, spec)
    replanned = plan_item(spec, raw_body(fresh), targets)
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
    allowed = {row["id"] for row in targets["items"]}
    item_id = snapshot.get("id")
    if item_id not in allowed:
        sys.exit(f"[ABORT] snapshot id {item_id} is not in the #828 set")
    spec = next(row for row in targets["items"] if row["id"] == item_id)
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


def assert_review_gate(targets: dict) -> None:
    approved = targets.get("reviewed_body_sha256")
    if not approved:
        sys.exit(
            "[ABORT] reviewed_body_sha256 is unset. Kris must review the draft before any apply."
        )
    observed = hashlib.sha256(load_draft_body().encode("utf-8")).hexdigest()
    if observed != approved:
        sys.exit(
            f"[ABORT] reviewed_body_sha256 mismatch: observed {observed}, expected {approved}."
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare or apply issue #828 negotiation checklist content."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--from-files",
        action="store_true",
        help="Validate committed baselines and transformations without network access.",
    )
    parser.add_argument("--item-id", type=int)
    parser.add_argument("--restore", type=Path)
    args = parser.parse_args()
    targets = load_targets()

    if args.restore:
        restore_snapshot(args.restore, auth_header(), args.apply, targets)
        return 0

    if args.apply:
        if args.item_id is None:
            sys.exit("[ABORT] --apply requires one exact --item-id")
        assert_review_gate(targets)

    rows = targets["items"]
    if args.item_id is not None:
        rows = [row for row in rows if row["id"] == args.item_id]
        if not rows:
            sys.exit(f"[ABORT] unknown --item-id {args.item_id}")

    if args.from_files:
        for spec in rows:
            try:
                planned = plan_item(spec, load_before_body(spec), targets)
            except ValueError as exc:
                sys.exit(f"[ABORT] {exc}")
            if planned is None:
                sys.exit(f"[ABORT] {spec['id']}: baseline unexpectedly already applied")
            if load_after_body(spec) != planned["after"]:
                sys.exit(f"[ABORT] {spec['id']}: computed after payload is unstable")
            print_plan(planned)
        print("[FROM-FILES] all four transforms valid. No network or WordPress writes.")
        return 0

    header = auth_header()
    planned = []
    for spec in rows:
        live = fetch_live(spec, header)
        validate_identity(live, spec)
        try:
            item = plan_item(spec, raw_body(live), targets)
        except ValueError as exc:
            sys.exit(f"[ABORT] {exc}")
        if item is not None:
            planned.append(item)
            print_plan(item)

    if not planned:
        print("[OK] nothing pending")
        return 0

    if not args.apply:
        print(
            "[DRY-RUN] no WordPress writes. Kris review, a committed review hash, "
            "and fresh explicit live approval are still required."
        )
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for item in planned:
        apply_item(item, header, stamp, targets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
