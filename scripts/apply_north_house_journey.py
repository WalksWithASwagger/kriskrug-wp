#!/usr/bin/env python3
"""Issue #978: prepare, check, or explicitly apply three reviewed content patches."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

from common import REPO_ROOT, WPClient, wp_process_credentials

sys.path.insert(0, str(REPO_ROOT / "scripts/events_page"))
import lib as events_lib  # noqa: E402
import render_events_page as events_render  # noqa: E402

BASE = "https://kriskrug.co"
PACK = REPO_ROOT / "content/drafts/2026-09-05-north-house-journey"
MANIFEST = PACK / "manifest.json"
EVENT_ID = "league-innovators-north-house-ai-show-tell-2026"
TARGETS = {
    "services": {"id": 2666, "type": "page", "slug": "generative-ai-services", "endpoint": "pages"},
    "recap": {"id": 12744, "type": "post", "slug": "what-i-showed-founders-about-ai-workflows", "endpoint": "posts"},
    "events": {"id": 2250, "type": "page", "slug": "events", "endpoint": "pages"},
}
PRESERVED = ("id", "type", "slug", "status", "title", "date", "date_gmt", "excerpt",
             "featured_media", "categories", "tags", "author", "template", "meta", "link")
FIELDS = ",".join((*PRESERVED, "modified_gmt", "content"))
SERVICES_ANCHOR = '  <section class="kk-services-section">\n    <p class="kk-services-kicker">Proof in motion</p>'
TAKEAWAY = "That is the whole talk, really. Not a tool list. One habit, applied until it compounds."
RECAP_ANCHOR = f"<p>{TAKEAWAY}</p>\n<!-- /wp:paragraph -->"


class JourneyError(RuntimeError):
    pass


def sha(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def replace_once(raw: str, needle: str, replacement: str) -> str:
    if raw.count(needle) != 1:
        raise JourneyError("Missing or ambiguous insertion anchor")
    return raw.replace(needle, replacement, 1)


def event_cards() -> tuple[str, str]:
    catalog = events_lib.load_catalog()
    matches = [e for e in catalog["events"] if e["id"] == EVENT_ID]
    if len(matches) != 1 or not matches[0].get("recap_url"):
        raise JourneyError("Expected one North House record with a recap URL")
    event = matches[0]
    roots = events_lib.resolve_path_roots(catalog)
    before = {k: v for k, v in event.items() if k != "recap_url"}
    return (events_render.render_compact_card(before, roots),
            events_render.render_compact_card(event, roots))


def rewrite(raw: str, name: str) -> str:
    if name == "events":
        before, after = event_cards()
        return replace_once(raw, before, after)
    if name == "services":
        fragment = (PACK / "services-insert.html").read_text().rstrip()
        return replace_once(raw, SERVICES_ANCHOR, fragment + "\n\n" + SERVICES_ANCHOR)
    fragment = (PACK / "recap-link.html").read_text().strip()
    return replace_once(raw, RECAP_ANCHOR, RECAP_ANCHOR + "\n\n" + fragment)


def identity(item: dict, name: str) -> None:
    expected = {k: v for k, v in TARGETS[name].items() if k != "endpoint"}
    expected["status"] = "publish"
    if any(item.get(k) != v for k, v in expected.items()):
        raise JourneyError(f"{name}: ID/type/slug/status mismatch")
    if not isinstance(item.get("content", {}).get("raw"), str):
        raise JourneyError(f"{name}: authenticated content.raw required")


def load_manifest(path: Path = MANIFEST) -> dict:
    manifest = json.loads(path.read_text())
    if set(manifest) != set(TARGETS):
        raise JourneyError("Manifest must contain exactly services, recap and events")
    for entry in manifest.values():
        for key in ("before_sha256", "after_sha256"):
            if not re.fullmatch(r"[a-f0-9]{64}", entry.get(key, "")):
                raise JourneyError("Manifest requires reviewed SHA-256 values")
        if not entry.get("modified_gmt") or entry["before_sha256"] == entry["after_sha256"]:
            raise JourneyError("Manifest requires a dated, nonempty patch")
    return manifest


def plan(item: dict, name: str, manifest: dict) -> tuple[str, str]:
    identity(item, name)
    raw = item["content"]["raw"]
    entry = manifest[name]
    if sha(raw) == entry["after_sha256"]:
        return "already-applied", raw
    if sha(raw) != entry["before_sha256"] or item.get("modified_gmt") != entry["modified_gmt"]:
        raise JourneyError(f"{name}: live content or modified timestamp drift; re-review required")
    after = rewrite(raw, name)
    if sha(after) != entry["after_sha256"]:
        raise JourneyError(f"{name}: generated patch differs from reviewed after hash")
    return "pending", after


def fetch(wp: WPClient, name: str) -> dict:
    target = TARGETS[name]
    return wp.get(f"{target['endpoint']}/{target['id']}", params={"context": "edit", "_fields": FIELDS})


def private_write(path: Path, text: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write(text)


def preserved(item: dict) -> dict:
    return {k: item.get(k) for k in PRESERVED}


def write_content(wp: WPClient, name: str, before: dict, after: str, snapshot_dir: Path) -> Path:
    snapshot = snapshot_dir / f"{name}-{time.time_ns()}.json"
    private_write(snapshot, json.dumps({"target": name, "before": before, "after_sha256": sha(after)},
                                       ensure_ascii=False, indent=2))
    current = fetch(wp, name)
    identity(current, name)
    if (current["content"]["raw"] != before["content"]["raw"]
            or current.get("modified_gmt") != before.get("modified_gmt")
            or preserved(current) != preserved(before)):
        raise JourneyError(f"{name}: changed after snapshot; no write sent")
    target = TARGETS[name]
    try:
        wp.post(f"{target['endpoint']}/{target['id']}", {"content": after})
    except Exception as exc:
        raise JourneyError(f"{name}: uncertain write ({type(exc).__name__}); inspect readback before retry; snapshot {snapshot}") from None
    readback = fetch(wp, name)
    identity(readback, name)
    if readback["content"]["raw"] != after or preserved(readback) != preserved(before):
        raise JourneyError(f"{name}: exact readback failed; inspect before restoring; snapshot {snapshot}")
    return snapshot


def apply(wp: WPClient, name: str, manifest: dict, snapshot_dir: Path, *, execute: bool = False) -> str:
    before = fetch(wp, name)
    state, after = plan(before, name, manifest)
    if state == "already-applied" or not execute:
        return state
    for dependency in list(TARGETS)[:list(TARGETS).index(name)]:
        if plan(fetch(wp, dependency), dependency, manifest)[0] != "already-applied":
            raise JourneyError(f"Apply {dependency} before {name}")
    snapshot = write_content(wp, name, before, after, snapshot_dir)
    return f"applied; snapshot {snapshot}"


def restore(wp: WPClient, snapshot: Path, manifest: dict, snapshot_dir: Path, *, execute: bool = False) -> str:
    receipt = json.loads(snapshot.read_text())
    name = receipt.get("target")
    if name not in TARGETS:
        raise JourneyError("Snapshot target is outside this slice")
    before = receipt["before"]
    identity(before, name)
    entry = manifest[name]
    if (sha(before["content"]["raw"]) != entry["before_sha256"]
            or receipt.get("after_sha256") != entry["after_sha256"]):
        raise JourneyError("Snapshot does not match this reviewed patch")
    current = fetch(wp, name)
    identity(current, name)
    digest = sha(current["content"]["raw"])
    if digest == entry["before_sha256"]:
        return "already-restored"
    if digest != entry["after_sha256"] or preserved(current) != preserved(before):
        raise JourneyError("Restore refuses changed content or metadata; review the conflict")
    if not execute:
        return "restore-pending"
    saved = write_content(wp, name, current, before["content"]["raw"], snapshot_dir)
    return f"restored; snapshot {saved}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "prepare", "apply", "restore"))
    parser.add_argument("--target", choices=TARGETS)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--snapshot-dir", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    if args.execute and (args.mode not in {"apply", "restore"} or not args.snapshot_dir):
        parser.error("--execute is only valid for apply/restore with --snapshot-dir")
    if args.mode == "apply" and not args.target:
        parser.error("apply requires --target")
    if args.mode == "restore" and not args.snapshot:
        parser.error("restore requires --snapshot")
    if args.mode == "prepare" and not args.output:
        parser.error("prepare requires --output (a private artifact directory)")
    manifest = load_manifest(args.manifest)
    user, password = wp_process_credentials()
    wp = WPClient(BASE, user, password, auth_mode="basic", retries=0)
    if args.mode == "restore":
        print(restore(wp, args.snapshot, manifest, args.snapshot_dir, execute=args.execute))
    elif args.mode == "apply":
        print(apply(wp, args.target, manifest, args.snapshot_dir, execute=args.execute))
    else:
        planned = []
        for name in ([args.target] if args.target else TARGETS):
            item = fetch(wp, name)
            state, after = plan(item, name, manifest)
            planned.append((name, item, after))
            print(f"{name}: {state}; after_sha256={sha(after)}")
        if args.mode == "prepare":
            for name, item, after in planned:
                private_write(args.output / f"{name}-before.json", json.dumps(item, ensure_ascii=False, indent=2))
                private_write(args.output / f"{name}-after.html", after)
            print(f"Prepared private artifacts in {args.output}; no WordPress writes")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except JourneyError as error:
        raise SystemExit(str(error)) from None
