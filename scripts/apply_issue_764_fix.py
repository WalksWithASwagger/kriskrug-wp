#!/usr/bin/env python3
"""Issue #764: apply the prepared em-dash and dead-link fixes to kriskrug.co.

Dry-run by default. Every write is gated on three checks that satisfy the
2026-05-15 incident rules: the target ID resolves to the expected slug, the live
body still matches the baseline hash captured when the payload was written, and
a fresh `context=edit` snapshot lands on disk before the POST update. Every
update is then verified through an independent `context=edit` GET.

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
from dataclasses import dataclass
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


@dataclass(frozen=True)
class PreparedTarget:
    post_id: int
    spec: dict
    live: dict
    payload: str
    already_applied: bool


@dataclass(frozen=True)
class PreparedRestore:
    post_id: int
    spec: dict
    snapshot: dict
    live: dict
    already_restored: bool


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


def write_snapshot(post: dict, post_id: int, stamp: str, label: str) -> Path:
    SNAPSHOT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    SNAPSHOT_DIR.chmod(0o700)
    path = SNAPSHOT_DIR / f"rest-post-{post_id}-{label}-{stamp}.json"
    temporary = path.with_suffix(".json.tmp")
    serialized = json.dumps(post, indent=2, ensure_ascii=False)
    json.loads(serialized)
    temporary_created = False

    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
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


def validate_live_identity(live: dict, post_id: int, spec: dict) -> None:
    if live.get("id") != post_id:
        sys.exit(
            f"[ABORT] {post_id}: REST response id is {live.get('id')!r}, expected {post_id}."
        )
    if live.get("slug") != spec["slug"]:
        sys.exit(
            f"[ABORT] {post_id}: slug is {live.get('slug')!r}, expected {spec['slug']!r}."
        )


def response_matches(
    response: dict, post_id: int, spec: dict, expected_sha256: str
) -> bool:
    content = response.get("content")
    body = content.get("raw") if isinstance(content, dict) else None
    return (
        response.get("id") == post_id
        and response.get("slug") == spec["slug"]
        and isinstance(body, str)
        and sha256(body) == expected_sha256
    )


def preflight_target(post_id: int, spec: dict, header: str) -> PreparedTarget:
    payload = (spec["dir"] / f"{post_id}-content-payload.html").read_text(
        encoding="utf-8"
    )
    if sha256(payload) != spec["payload_sha256"]:
        sys.exit(f"[ABORT] {post_id}: payload file does not match its recorded sha256.")

    live = request(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit", header)
    validate_live_identity(live, post_id, spec)

    current = live["content"]["raw"]
    if sha256(current) == spec["payload_sha256"]:
        print(f"[SKIP] {post_id}: live body already equals the payload. Nothing to do.")
        return PreparedTarget(post_id, spec, live, payload, True)
    if sha256(current) != spec["baseline_sha256"]:
        sys.exit(
            f"[ABORT] {post_id}: live body drifted from the 2026-08-15 baseline "
            f"(modified {live['modified_gmt']}). Re-derive the payload before applying."
        )

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

    return PreparedTarget(post_id, spec, live, payload, False)


def apply_target(plan: PreparedTarget, header: str, snapshot: Path) -> bool:
    updated = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{plan.post_id}?context=edit",
        header,
        {"content": plan.payload},
    )
    response_ok = response_matches(
        updated, plan.post_id, plan.spec, plan.spec["payload_sha256"]
    )
    print(
        f"[WRITE] {plan.post_id}: POST response "
        f"{'matches' if response_ok else 'DOES NOT MATCH'} the target and payload."
    )

    readback = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{plan.post_id}?context=edit", header
    )
    validate_live_identity(readback, plan.post_id, plan.spec)
    readback_ok = response_matches(
        readback, plan.post_id, plan.spec, plan.spec["payload_sha256"]
    )
    print(
        f"[READBACK] {plan.post_id}: fresh context=edit GET "
        f"{'matches' if readback_ok else 'DOES NOT MATCH'} the payload."
    )
    print(
        "[ROLLBACK] python3 scripts/apply_issue_764_fix.py "
        f"--restore {snapshot} --apply"
    )
    return response_ok and readback_ok


def run_targets(
    post_ids: list[int], header: str, stamp: str, apply: bool
) -> bool:
    plans = [preflight_target(post_id, TARGETS[post_id], header) for post_id in post_ids]
    pending = [plan for plan in plans if not plan.already_applied]

    if not apply:
        for plan in pending:
            print(
                f"[DRY RUN] {plan.post_id}: no local or WordPress write. "
                "Pass --apply after KK approval."
            )
        return True

    snapshots = {
        plan.post_id: write_snapshot(plan.live, plan.post_id, stamp, "before")
        for plan in pending
    }
    return all(
        apply_target(plan, header, snapshots[plan.post_id]) for plan in pending
    )


def preflight_restore(path: Path, header: str) -> PreparedRestore:
    try:
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        post_id = snapshot["id"]
        snapshot_slug = snapshot["slug"]
        snapshot_body = snapshot["content"]["raw"]
    except (KeyError, OSError, TypeError, json.JSONDecodeError) as exc:
        sys.exit(f"[ABORT] Restore snapshot is not valid context=edit JSON: {exc}")

    if post_id not in TARGETS:
        sys.exit(f"[ABORT] Restore target {post_id!r} is outside the issue #764 allowlist.")
    spec = TARGETS[post_id]
    if snapshot_slug != spec["slug"]:
        sys.exit(
            f"[ABORT] {post_id}: snapshot slug is {snapshot_slug!r}, "
            f"expected {spec['slug']!r}."
        )
    if sha256(snapshot_body) != spec["baseline_sha256"]:
        sys.exit(
            f"[ABORT] {post_id}: snapshot body does not match the approved baseline hash."
        )

    live = request(f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?context=edit", header)
    validate_live_identity(live, post_id, spec)
    current_hash = sha256(live["content"]["raw"])
    if current_hash == spec["baseline_sha256"]:
        return PreparedRestore(post_id, spec, snapshot, live, True)
    if current_hash != spec["payload_sha256"]:
        sys.exit(
            f"[ABORT] {post_id}: current body matches neither the reviewed payload "
            "nor the approved baseline; refusing to overwrite live drift."
        )
    return PreparedRestore(post_id, spec, snapshot, live, False)


def restore(path: Path, header: str, stamp: str, apply: bool) -> bool:
    plan = preflight_restore(path, header)
    captured = plan.snapshot.get("modified_gmt", "unknown")
    print(f"[RESTORE] {plan.post_id} from {path} (captured {captured})")
    if plan.already_restored:
        print(f"[SKIP] {plan.post_id}: live body already equals the restore snapshot.")
        return True
    if not apply:
        print("[DRY RUN] restore validated; no local or WordPress write.")
        return True

    recovery = write_snapshot(
        plan.live, plan.post_id, stamp, "before-restore"
    )
    updated = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{plan.post_id}?context=edit",
        header,
        {"content": plan.snapshot["content"]["raw"]},
    )
    expected_hash = plan.spec["baseline_sha256"]
    response_ok = response_matches(updated, plan.post_id, plan.spec, expected_hash)
    print(
        f"[RESTORE] {plan.post_id}: POST response "
        f"{'matches' if response_ok else 'DOES NOT MATCH'} the target and snapshot."
    )

    readback = request(
        f"{BASE_URL}/wp-json/wp/v2/posts/{plan.post_id}?context=edit", header
    )
    validate_live_identity(readback, plan.post_id, plan.spec)
    readback_ok = response_matches(
        readback, plan.post_id, plan.spec, expected_hash
    )
    print(
        f"[READBACK] {plan.post_id}: fresh context=edit GET "
        f"{'matches' if readback_ok else 'DOES NOT MATCH'} the snapshot."
    )
    print(f"[RECOVERY] Pre-restore state: {recovery}")
    return response_ok and readback_ok


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
        return 0 if restore(args.restore, header, stamp, args.apply) else 1

    ids = [args.post_id] if args.post_id else sorted(TARGETS)
    return 0 if run_targets(ids, header, stamp, args.apply) else 1


if __name__ == "__main__":
    raise SystemExit(main())
