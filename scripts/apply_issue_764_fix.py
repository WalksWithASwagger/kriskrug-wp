#!/usr/bin/env python3
"""Issue #764: apply the prepared em-dash and dead-link fixes to kriskrug.co.

Dry-run by default. Every write is gated on three checks that satisfy the
2026-05-15 incident rules: the target ID resolves to the expected slug, the live
body still matches the baseline hash captured when the payload was written, and
a fresh `context=edit` snapshot lands on disk before the PATCH.

    make varlock-run CMD='python3 scripts/apply_issue_764_fix.py'
    make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --apply'
"""

from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = REPO_ROOT / "backup" / "issue-764-em-dash-404"

TARGETS = {
    12327: {
        "slug": "storyhive-haus-of-owl-jordan-dack",
        "url": "https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/",
        "dir": REPO_ROOT
        / "content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764",
        "baseline_sha256": "e29a7e8e0f7c47d8ffe157c09003b3c5ff71832341b3956dfa1b662daee5773a",
        "payload_sha256": "045c697906260becae376d39fcf0987911ac9c94e5d3b25def8a4f1b4a69981d",
    },
    12032: {
        "slug": "what-would-chat-do-and-why-thats-the-wrong-question",
        "url": "https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/",
        "dir": REPO_ROOT
        / "content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764",
        "baseline_sha256": "f2b4374560746f10d8c5e1c7eb1b347ff73745f9032a5931691c523536036ddb",
        "payload_sha256": "28d87a5d2817579e18bedc67fd4914cf70bbb1c3d8ed4e59e073aaa70da26b9d",
    },
}

EM_DASH = "—"
BASE_URL = "https://kriskrug.co"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def auth_header() -> str:
    user = os.getenv("WP_API_USERNAME") or os.getenv("WP_USER")
    password = os.getenv("WP_API_PASSWORD") or os.getenv("WP_APP_PASSWORD")
    if not user or not password:
        sys.exit("[ABORT] WordPress credentials unresolved. Run through Varlock.")
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def request(url: str, header: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": header, "User-Agent": "kriskrug-ops/issue-764"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if data else "GET"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def run_target(post_id: int, spec: dict, header: str, stamp: str, apply: bool) -> bool:
    payload = (spec["dir"] / f"{post_id}-content-payload.html").read_text(
        encoding="utf-8"
    )
    if sha256(payload) != spec["payload_sha256"]:
        sys.exit(f"[ABORT] {post_id}: payload file does not match its recorded sha256.")

    live = request(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit", header)
    if live["slug"] != spec["slug"]:
        sys.exit(
            f"[ABORT] {post_id}: slug is {live['slug']!r}, expected {spec['slug']!r}."
        )

    current = live["content"]["raw"]
    if sha256(current) == spec["payload_sha256"]:
        print(f"[SKIP] {post_id}: live body already equals the payload. Nothing to do.")
        return True
    if sha256(current) != spec["baseline_sha256"]:
        sys.exit(
            f"[ABORT] {post_id}: live body drifted from the 2026-08-15 baseline "
            f"(modified {live['modified_gmt']}). Re-derive the payload before applying."
        )

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = SNAPSHOT_DIR / f"rest-post-{post_id}-before-{stamp}.json"
    snapshot.write_text(
        json.dumps(live, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[SNAPSHOT] {snapshot}")

    diff = list(
        difflib.unified_diff(
            current.splitlines(),
            payload.splitlines(),
            "live",
            "payload",
            lineterm="",
            n=0,
        )
    )
    print(
        f"[DIFF] {post_id}: {len(diff)} unified-diff lines, "
        f"em dashes {current.count(EM_DASH)} -> {payload.count(EM_DASH)}"
    )
    for line in diff:
        print("   " + line)

    if not apply:
        print(f"[DRY RUN] {post_id}: no write. Pass --apply after KK approval.")
        return True

    updated = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}", header, {"content": payload}
    )
    written = updated["content"]["raw"]
    ok = sha256(written) == spec["payload_sha256"]
    print(
        f"[WRITE] {post_id}: readback {'matches' if ok else 'DOES NOT MATCH'} the payload."
    )
    print(
        f"[ROLLBACK] python3 scripts/apply_issue_764_fix.py --restore {snapshot} --apply"
    )
    return ok


def restore(path: Path, header: str, apply: bool) -> bool:
    snap = json.loads(path.read_text(encoding="utf-8"))
    post_id = snap["id"]
    print(f"[RESTORE] {post_id} from {path} (captured {snap['modified_gmt']})")
    if not apply:
        print("[DRY RUN] restore prepared; pass --apply to write.")
        return True
    updated = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}",
        header,
        {"content": snap["content"]["raw"]},
    )
    ok = updated["content"]["raw"] == snap["content"]["raw"]
    print(
        f"[RESTORE] {post_id}: readback {'matches' if ok else 'DOES NOT MATCH'} the snapshot."
    )
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply the issue #764 content fixes")
    parser.add_argument("--apply", action="store_true", help="perform WordPress writes")
    parser.add_argument(
        "--post-id", type=int, choices=sorted(TARGETS), help="limit to one post"
    )
    parser.add_argument(
        "--restore", type=Path, help="restore a post from a snapshot JSON"
    )
    args = parser.parse_args()

    header = auth_header()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.restore:
        return 0 if restore(args.restore, header, args.apply) else 1

    ids = [args.post_id] if args.post_id else sorted(TARGETS)
    return (
        0
        if all(run_target(i, TARGETS[i], header, stamp, args.apply) for i in ids)
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
