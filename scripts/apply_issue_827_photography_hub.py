#!/usr/bin/env python3
"""Issue #827: wire internal links on /photography/ (page 12013) plus posts 1222 and 1056.

Dry-run by default. Writes are gated on ID→slug match, a text-match insert
(not a stale block index), skip-if-exact-href+anchor, and a fresh
context=edit snapshot before each POST.

    make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py'
    make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --apply'
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = (
    REPO_ROOT / "content/drafts/2026-08-02-seo-authority-hubs/fix-827/targets.json"
)
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-827-photography-hub"
BASE_URL = "https://kriskrug.co"
FOOTER_SENTINEL = "kk-collection-footer"
STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
PEEPS_RE = re.compile(
    r"I(?:'|&#8217;|&rsquo;|&apos;|&#x2019;|\u2019)ve met a couple cool peeps already\."
)
FOOTER_MARKERS = (
    '<!-- wp:paragraph {"className":"kk-collection-footer"} -->',
    "<p class=\"kk-collection-footer",
)


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
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-827"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def rest_url(spec: dict, item_id: int | None = None) -> str:
    collection = spec["rest"]
    target_id = spec["id"] if item_id is None else item_id
    return f"{BASE_URL}/wp-json/wp/v2/{collection}/{target_id}?context=edit"


def write_snapshot(item: dict, spec: dict, stamp: str) -> Path:
    SNAPSHOT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    SNAPSHOT_DIR.chmod(0o700)
    path = SNAPSHOT_DIR / f"rest-{spec['rest']}-{spec['id']}-before-{stamp}.json"
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


def validate_identity(live: dict, spec: dict) -> None:
    item_id = spec["id"]
    if live.get("id") != item_id:
        sys.exit(f"[ABORT] {item_id}: REST id is {live.get('id')!r}.")
    if live.get("slug") != spec["slug"]:
        sys.exit(
            f"[ABORT] {item_id}: slug is {live.get('slug')!r}, expected {spec['slug']!r}."
        )


def exact_link(href: str, anchor: str) -> str:
    return f'<a href="{href}">{anchor}</a>'


def style_blocks(raw: str) -> list[str]:
    return STYLE_RE.findall(raw)


def footer_count(raw: str) -> int:
    return raw.count(FOOTER_SENTINEL)


def assert_payload_safe(raw: str, spec: dict, targets: dict, original: str) -> None:
    for needle in targets["forbidden_href_needles"]:
        if needle in raw:
            raise ValueError(f"{spec['id']}: forbidden href {needle!r} present")
    if spec.get("keep_style") and style_blocks(raw) != style_blocks(original):
        raise ValueError(f"{spec['id']}: inline <style> block changed")
    if spec.get("keep_flickr"):
        flickr = targets["flickr_href"]
        if raw.count(flickr) < original.count(flickr):
            raise ValueError(f"{spec['id']}: Flickr href count dropped")
    if spec["kind"] in {"before_footer", "after_peeps"}:
        if footer_count(raw) != footer_count(original):
            raise ValueError(f"{spec['id']}: kk-collection-footer count changed")


def coda_paragraph_close(raw: str, locate: str, must_contain: str) -> int:
    if raw.count(locate) != 1:
        raise ValueError(
            f"locate {locate!r} occurs {raw.count(locate)} times; expected 1"
        )
    loc = raw.find(locate)
    p_start = raw.find("<p", loc)
    if p_start < 0:
        raise ValueError("no <p> after locate text")
    p_close = raw.find("</p>", p_start)
    if p_close < 0:
        raise ValueError("coda <p> is unclosed")
    styles = list(STYLE_RE.finditer(raw))
    if styles and p_start < styles[-1].end():
        raise ValueError("coda paragraph resolved inside the style block")
    paragraph = raw[p_start:p_close]
    if must_contain not in paragraph:
        raise ValueError(f"coda <p> does not contain {must_contain!r}")
    return p_close


def rewrite_coda_page(raw: str, spec: dict, targets: dict) -> tuple[str | None, list[str]]:
    notes: list[str] = []
    close_at = coda_paragraph_close(
        raw, targets["locate_12013"], targets["coda_must_contain"]
    )
    new = raw
    offset = 0
    for row in spec["rows"]:
        link = exact_link(row["href"], row["anchor"])
        if link in new:
            notes.append(f"row {row['row']} already present")
            continue
        insert = f"{row['prefix']}{link}{row['suffix']}"
        at = close_at + offset
        new = new[:at] + insert + new[at:]
        offset += len(insert)
        notes.append(f"row {row['row']} insert")
    if new == raw:
        return None, notes
    assert_payload_safe(new, spec, targets, raw)
    return new, notes


def footer_insert_index(raw: str) -> int:
    found = [raw.find(marker) for marker in FOOTER_MARKERS if marker in raw]
    if not found:
        raise ValueError("kk-collection-footer marker not found")
    return min(found)


def rewrite_before_footer(raw: str, spec: dict, targets: dict) -> tuple[str | None, list[str]]:
    notes: list[str] = []
    if footer_count(raw) < 1:
        raise ValueError("kk-collection-footer is missing")
    row = spec["rows"][0]
    link = exact_link(row["href"], row["anchor"])
    if link in raw:
        notes.append(f"row {row['row']} already present")
        return None, notes
    paragraph = row["paragraph"]
    if link not in paragraph or not paragraph.startswith("<p>") or not paragraph.endswith("</p>"):
        raise ValueError("before_footer paragraph payload is malformed")
    idx = footer_insert_index(raw)
    prefix = raw[:idx]
    if not prefix.endswith("\n"):
        prefix += "\n"
    if not prefix.endswith("\n\n"):
        prefix += "\n"
    new = prefix + paragraph + "\n\n" + raw[idx:]
    notes.append(f"row {row['row']} insert")
    assert_payload_safe(new, spec, targets, raw)
    return new, notes


def rewrite_after_peeps(raw: str, spec: dict, targets: dict) -> tuple[str | None, list[str]]:
    notes: list[str] = []
    matches = list(PEEPS_RE.finditer(raw))
    if len(matches) != 1:
        raise ValueError(f"peeps line occurs {len(matches)} times; expected 1")
    row = spec["rows"][0]
    link = exact_link(row["href"], row["anchor"])
    if link in raw:
        notes.append(f"row {row['row']} already present")
        return None, notes
    insert = f"{row['prefix']}{link}{row['suffix']}"
    at = matches[0].end()
    new = raw[:at] + insert + raw[at:]
    notes.append(f"row {row['row']} insert")
    assert_payload_safe(new, spec, targets, raw)
    return new, notes


REWRITERS = {
    "coda_page": rewrite_coda_page,
    "before_footer": rewrite_before_footer,
    "after_peeps": rewrite_after_peeps,
}


def plan_target(spec: dict, live: dict, targets: dict) -> dict | None:
    body = raw_body(live)
    rewriter = REWRITERS.get(spec["kind"])
    if rewriter is None:
        raise ValueError(f"{spec['id']}: unknown kind {spec['kind']!r}")
    rewritten, notes = rewriter(body, spec, targets)
    if rewritten is None:
        print(f"[SKIP] {spec['id']}: {'; '.join(notes) or 'nothing to do'}.")
        return None
    return {
        "spec": spec,
        "live": live,
        "payload": {"content": rewritten},
        "notes": notes,
    }


def fetch_live(spec: dict, header: str) -> dict:
    return request(rest_url(spec), header)


def print_plan(item: dict) -> None:
    spec = item["spec"]
    payload = item["payload"]
    print(f"[PLAN] {spec['rest']}/{spec['id']} {spec['slug']}: {'; '.join(item['notes'])}")
    old = raw_body(item["live"])
    new = payload["content"]
    print(f"        content.raw {len(old)} chars -> {len(new)} chars")


def apply_item(item: dict, header: str, stamp: str, do_apply: bool) -> None:
    spec = item["spec"]
    print_plan(item)
    if not do_apply:
        return
    live = fetch_live(spec, header)
    validate_identity(live, spec)
    replanned = plan_target(spec, live, load_targets())
    if replanned is None:
        return
    if set(replanned["payload"]) != {"content"}:
        sys.exit(f"[ABORT] {spec['id']}: payload is not content-only.")
    write_snapshot(live, spec, stamp)
    updated = request(rest_url(spec), header, replanned["payload"])
    validate_identity(updated, spec)
    print(f"[WROTE] {spec['id']}")


def restore_snapshot(path: Path, header: str, do_apply: bool) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    item_id = snapshot.get("id")
    targets = load_targets()
    allowed = {row["id"]: row for row in targets["targets"]}
    if item_id not in allowed:
        sys.exit(f"[ABORT] snapshot id {item_id} is not in the #827 set.")
    spec = allowed[item_id]
    validate_identity(snapshot, spec)
    payload = {"content": raw_body(snapshot)}
    print(f"[RESTORE] {item_id} from {path}")
    if not do_apply:
        return
    live = fetch_live(spec, header)
    validate_identity(live, spec)
    write_snapshot(
        live, spec, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    request(rest_url(spec), header, payload)
    print(f"[WROTE] {item_id} restored")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply issue #827 photography hub internal links."
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--id", type=int, dest="target_id")
    parser.add_argument("--restore", type=Path)
    args = parser.parse_args()
    header = auth_header()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.restore:
        restore_snapshot(args.restore, header, args.apply)
        return 0

    targets = load_targets()
    rows = targets["targets"]
    if args.target_id:
        rows = [row for row in rows if row["id"] == args.target_id]
        if not rows:
            sys.exit(f"[ABORT] unknown --id {args.target_id}")

    planned = []
    for spec in rows:
        live = fetch_live(spec, header)
        validate_identity(live, spec)
        try:
            item = plan_target(spec, live, targets)
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
