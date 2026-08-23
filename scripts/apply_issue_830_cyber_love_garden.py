#!/usr/bin/env python3
"""Issue #830: add Cyber Love Garden to /ai-for-creatives/ and three spokes.

Dry-run by default. Writes are gated on ID->slug match, exact text-match
insertion, child-1 (#826) 2819 contact-href proof, and a fresh context=edit
snapshot.

    python3 scripts/apply_issue_830_cyber_love_garden.py --from-files
    make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py'
    make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py --apply'
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
PACK = REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-830"
TARGETS_PATH = PACK / "targets.json"
BEFORE_DIR = PACK / "before"
AFTER_DIR = PACK / "after"
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-830-cyber-love-garden"
BASE_URL = "https://kriskrug.co"
FOOTER_SENTINEL = "kk-collection-footer"
APOS_FORMS = ("&#8217;", "\u2019", "'")


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
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-830"}
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


def apos_variants(text: str) -> list[str]:
    variants = {text}
    for src in APOS_FORMS:
        if src in text:
            for dst in APOS_FORMS:
                variants.add(text.replace(src, dst))
    return list(variants)


def find_candidates(spec: dict) -> list[str]:
    needles = [spec["find"], *spec.get("find_variants", [])]
    expanded: list[str] = []
    seen: set[str] = set()
    for needle in needles:
        for variant in apos_variants(needle):
            if variant not in seen:
                seen.add(variant)
                expanded.append(variant)
    return expanded


def pick_find(body: str, spec: dict) -> str:
    ones = [needle for needle in find_candidates(spec) if body.count(needle) == 1]
    if spec["find"] in ones:
        return spec["find"]
    if len(ones) == 1:
        return ones[0]
    if len(ones) > 1:
        ones.sort(key=len, reverse=True)
        return ones[0]
    counts = {needle: body.count(needle) for needle in find_candidates(spec)}
    observed = max(counts.values()) if counts else 0
    raise ValueError(
        f"{spec['id']}: find needle occurs {observed} times; expected 1. "
        "Insert by text match, not a stale block index."
    )


def already_applied(body: str, spec: dict) -> bool:
    return all(anchor_present(body, row) for row in spec["anchors"])


def anchor_present(body: str, row: dict) -> bool:
    if row.get("match") == "card":
        return row["href"] in body and f"<h3>{row['text']}</h3>" in body
    return f'<a href="{row["href"]}">{row["text"]}</a>' in body


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


def build_replace(find: str, spec: dict) -> str:
    if find == spec["find"]:
        return spec["replace"]
    added = inserted_fragment(spec)
    if find.endswith("</p>") and spec["find"].endswith("</p>"):
        return find[: -len("</p>")] + added + "</p>"
    raise ValueError(f"{spec['id']}: cannot map replace onto find variant")


def rewrite_body(body: str, spec: dict, targets: dict) -> str | None:
    if already_applied(body, spec):
        return None
    find = pick_find(body, spec)
    replace = build_replace(find, spec)
    added = inserted_fragment(spec)
    if "\u2014" in added or "\u2013" in added:
        raise ValueError(f"{spec['id']}: inserted copy contains a dash codepoint")
    if any(ord(char) > 127 for char in added):
        raise ValueError(f"{spec['id']}: inserted copy is not ASCII; use NCR")
    rewritten = body.replace(find, replace, 1)
    if spec.get("preserve_cards"):
        for card in targets["keep_cards"]:
            if body.count(card["href"]) != rewritten.count(card["href"]):
                raise ValueError(f"{spec['id']}: existing card href {card['href']} changed")
            title = f"<h3>{card['title']}</h3>"
            if body.count(title) != rewritten.count(title):
                raise ValueError(f"{spec['id']}: existing card title {card['title']!r} changed")
        archive = targets["keep_archive_href"]
        if body.count(archive) != rewritten.count(archive):
            raise ValueError(f"{spec['id']}: archive card href changed")
    if spec.get("preserve_footer"):
        if body.count(FOOTER_SENTINEL) != rewritten.count(FOOTER_SENTINEL):
            raise ValueError(f"{spec['id']}: kk-collection-footer count changed")
    if spec.get("preserve_contact"):
        for needle in (
            targets["child1_gate"]["forbidden_href_substring"],
            targets["child1_gate"]["required_href_substring"],
        ):
            if body.count(needle) != rewritten.count(needle):
                raise ValueError(f"{spec['id']}: contact href {needle} count changed")
    for forbidden in targets["forbidden_href_substrings"]:
        if forbidden in rewritten and forbidden not in body:
            raise ValueError(f"{spec['id']}: forbidden href {forbidden} was added")
    for row in spec["anchors"]:
        if row.get("match") == "card":
            if rewritten.count(row["href"]) != 1:
                raise ValueError(f"{spec['id']}: expected one garden card href")
            if rewritten.count(f"<h3>{row['text']}</h3>") != 1:
                raise ValueError(f"{spec['id']}: expected one {row['text']!r} card title")
            if targets["garden_blurb"] not in rewritten:
                raise ValueError(f"{spec['id']}: garden card blurb missing")
        else:
            needle = f'<a href="{row["href"]}">{row["text"]}</a>'
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


def extract_body(live: dict) -> str:
    content = live.get("content")
    if isinstance(content, dict):
        if isinstance(content.get("raw"), str):
            return content["raw"]
        if isinstance(content.get("rendered"), str):
            return content["rendered"]
    sys.exit(f"[ABORT] {live.get('id')}: no content.raw or content.rendered.")


def child1_is_live(header: str, targets: dict) -> tuple[bool, list[str]]:
    gate = targets["child1_gate"]
    live = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{gate['id']}?context=edit",
        header,
    )
    notes: list[str] = []
    if live.get("slug") != gate["slug"]:
        notes.append(f"{gate['id']} slug {live.get('slug')!r}")
        return False, notes
    body = extract_body(live)
    if gate["forbidden_href_substring"] in body:
        notes.append(f"{gate['id']} still has {gate['forbidden_href_substring']}")
        return False, notes
    if gate["required_href_substring"] not in body:
        notes.append(f"{gate['id']} missing {gate['required_href_substring']}")
        return False, notes
    notes.append(f"{gate['id']} contact repair live")
    return True, notes


def plan_item(spec: dict, body: str, targets: dict) -> dict | None:
    rewritten = rewrite_body(body, spec, targets)
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
        sys.exit(f"[ABORT] snapshot id {post_id} is not in the #830 set.")
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
        description="Apply issue #830 Cyber Love Garden hub links."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--from-files", action="store_true")
    parser.add_argument("--item-id", type=int)
    parser.add_argument("--restore", type=Path)
    parser.add_argument(
        "--allow-before-826",
        action="store_true",
        help="Unsafe. Bypass the child-1 2819 contact-href gate. Do not use on production.",
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
                "[ABORT] #826 2819 contact-href repair is not live. "
                "Do not PATCH 12316/2819/2661/3567 yet."
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
            "[DRY-RUN] no WordPress writes. Pass --apply after #826 2819 "
            "contact repair is live and KK approves."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
