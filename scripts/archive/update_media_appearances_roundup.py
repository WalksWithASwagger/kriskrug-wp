#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests


POST_ID = 11879
POST_SLUG = "ai-media-appearances-podcast-guesting"
POST_TITLE = "AI Media Appearances, Podcast Guesting, and Broadcast Commentary"
DEFAULT_SNAPSHOT_DIR = Path("backup/20260731-kris-youtube-press-roundup")
VIDEO_IDS = ("n_aGBFGnPzo", "Vbk2B7aqw8E", "TOk2YwViBKs")
SECTION_HEADING = "Recent Video Interviews and Talks"
ANCHOR_RE = re.compile(
    r"(?:<!--\s+wp:heading\s+-->\s*)?"
    r'<h2 class="wp-block-heading">Long-Form Podcast Conversations</h2>'
    r"(?:\s*<!--\s+/wp:heading\s*-->)?"
)

BLOCK = """<!-- wp:heading {\"level\":3} -->
<h3 class="wp-block-heading">Recent Video Interviews and Talks</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>These three videos hit the same live wire from different angles: who controls the infrastructure, what happens to creative work, and how we keep the human parts from getting optimized out while AI kicks down the door.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><strong><a href="https://youtu.be/n_aGBFGnPzo">Canada's AI Power Struggle: Energy, Data Centres &amp; Sovereignty | Kris Krüg</a>:</strong> <a href="https://www.youtube.com/watch?v=UzJfMJzkFwc">Power Struggle</a> host Stewart Muir pulls the conversation toward electricity, data centres, Indigenous leadership, national sovereignty, and who gets to shape Canada's AI future.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong><a href="https://youtu.be/Vbk2B7aqw8E">AI Is Kicking Down the Door: Creativity, Jobs &amp; BC's Future | Kris Krüg</a>:</strong> Recorded at <a href="https://www.youtube.com/watch?v=d8CvTTSWqj8">LLLSummit</a>, this talk moves from assistants, automations, and agents into AI literacy, creative disruption, environmental cost, and the choices British Columbia still gets to make.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong><a href="https://youtu.be/TOk2YwViBKs">Live With Curiosity: AI, Creativity &amp; Staying Human | Kris Krüg on Human Biography</a>:</strong> <a href="https://www.youtube.com/watch?v=fF1taMiIV8Q">Sharad Kharé</a> and I get into photography, creative practice, AI ethics, and the stubbornly human value of curiosity. <a href="https://kriskrug.co/2025/01/25/human-biography-podcast-w-sharad-khare/">Read the companion article</a>.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->"""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_bypass(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["cb"] = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def auth_session() -> tuple[requests.Session, str]:
    base_url = os.getenv("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = os.getenv("WP_USER") or os.getenv("WP_API_USERNAME")
    password = os.getenv("WP_APP_PASSWORD") or os.getenv("WP_API_PASSWORD")
    if not user or not password:
        raise SystemExit("[ABORT] WordPress credentials are unresolved. Run through Varlock.")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    session = requests.Session()
    session.headers.update({"Authorization": f"Basic {token}"})
    return session, base_url


def fetch_post(session: requests.Session, base_url: str) -> dict:
    response = session.get(
        f"{base_url}/wp-json/wp/v2/posts/{POST_ID}",
        params={"context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    post = response.json()
    title = post.get("title", {}).get("raw") or post.get("title", {}).get("rendered")
    if post.get("id") != POST_ID:
        raise SystemExit(f"[ABORT] expected post id {POST_ID}, got {post.get('id')!r}")
    if post.get("slug") != POST_SLUG:
        raise SystemExit(f"[ABORT] expected slug {POST_SLUG!r}, got {post.get('slug')!r}")
    if title != POST_TITLE:
        raise SystemExit(f"[ABORT] expected title {POST_TITLE!r}, got {title!r}")
    if post.get("status") != "publish":
        raise SystemExit(f"[ABORT] expected published status, got {post.get('status')!r}")
    if not post.get("content", {}).get("raw"):
        raise SystemExit("[ABORT] authenticated response did not include content.raw")
    return post


def build_updated(raw: str) -> tuple[str, bool]:
    counts = {video_id: raw.count(video_id) for video_id in VIDEO_IDS}
    present = [video_id for video_id, count in counts.items() if count]
    if present:
        if len(present) == len(VIDEO_IDS) and all(count == 1 for count in counts.values()):
            if raw.count(SECTION_HEADING) != 1:
                raise SystemExit("[ABORT] all video ids exist but the section heading is not unique")
            return raw, True
        raise SystemExit(f"[ABORT] partial or duplicate target state: {counts}")
    anchors = list(ANCHOR_RE.finditer(raw))
    if len(anchors) != 1:
        raise SystemExit(f"[ABORT] expected one Long-Form anchor, found {len(anchors)}")
    start = anchors[0].start()
    return f"{raw[:start]}{BLOCK}\n\n{raw[start:]}", False


def diff_text(before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="post-11879-before.html",
            tofile="post-11879-after.html",
        )
    )


def write_snapshot(post: dict, snapshot_dir: Path, label: str) -> tuple[Path, Path]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = snapshot_dir / f"post-{POST_ID}-{label}-{stamp}.json"
    html_path = snapshot_dir / f"post-{POST_ID}-{label}-{stamp}.html"
    json_path.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path.write_text(post["content"]["raw"], encoding="utf-8")
    json_path.chmod(0o600)
    html_path.chmod(0o600)
    return json_path, html_path


def update_content(session: requests.Session, base_url: str, content: str) -> dict:
    response = session.post(
        f"{base_url}/wp-json/wp/v2/posts/{POST_ID}",
        json={"content": content},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def verify_public(post_url: str) -> str:
    url = cache_bypass(post_url)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    missing = [video_id for video_id in VIDEO_IDS if video_id not in response.text]
    if missing or SECTION_HEADING not in response.text:
        raise SystemExit(f"[ABORT] public cache-bypass verification failed; missing={missing}")
    return url


def write_manifest(
    snapshot_dir: Path,
    before_json: Path,
    before_html: Path,
    before_sha: str,
    after_sha: str,
    public_url: str,
) -> Path:
    manifest_path = snapshot_dir / "rollback-manifest.json"
    restore_command = (
        "varlock run --inject vars -- python3 scripts/update_media_appearances_roundup.py "
        f"--restore {before_json} --apply"
    )
    manifest = {
        "post_id": POST_ID,
        "slug": POST_SLUG,
        "snapshot_json": str(before_json),
        "snapshot_html": str(before_html),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "public_verification_url": public_url,
        "restore_command": restore_command,
        "cache_note": "Cache-bypass verified. Purge Pagely PressCACHE manually if canonical HTML remains stale.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update KrisKrug.co media roundup post 11879")
    parser.add_argument("--apply", action="store_true", help="perform the WordPress write")
    parser.add_argument("--restore", type=Path, help="restore content.raw from a saved post snapshot")
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session, base_url = auth_session()
    current = fetch_post(session, base_url)
    current_raw = current["content"]["raw"]

    if args.restore:
        snapshot = json.loads(args.restore.read_text(encoding="utf-8"))
        if snapshot.get("id") != POST_ID:
            raise SystemExit(f"[ABORT] restore snapshot is not post {POST_ID}")
        desired = snapshot.get("content", {}).get("raw")
        if not desired:
            raise SystemExit("[ABORT] restore snapshot has no content.raw")
        print(diff_text(current_raw, desired))
        if not args.apply:
            print("[DRY RUN] restore diff only; pass --apply to write")
            return 0
        write_snapshot(current, args.snapshot_dir, "before-restore")
        update_content(session, base_url, desired)
        readback = fetch_post(session, base_url)["content"]["raw"]
        if sha256(readback) != sha256(desired):
            raise SystemExit("[ABORT] restore readback hash mismatch")
        print(f"[RESTORED] post={POST_ID} sha256={sha256(readback)}")
        return 0

    desired, already_applied = build_updated(current_raw)
    if already_applied:
        print(f"[NOOP] post={POST_ID} already contains the verified section")
        return 0

    print(f"target post={POST_ID} slug={POST_SLUG} status={current['status']}")
    print(f"before_sha256={sha256(current_raw)}")
    print(f"after_sha256={sha256(desired)}")
    print(diff_text(current_raw, desired))
    if not args.apply:
        print("[DRY RUN] no WordPress write; pass --apply to write")
        return 0

    before_json, before_html = write_snapshot(current, args.snapshot_dir, "before-youtube-roundup")
    result = update_content(session, base_url, desired)
    if result.get("id") != POST_ID:
        raise SystemExit("[ABORT] update response returned the wrong post id")
    readback = fetch_post(session, base_url)
    readback_raw = readback["content"]["raw"]
    if sha256(readback_raw) != sha256(desired):
        raise SystemExit("[ABORT] authenticated readback hash mismatch")
    public_url = verify_public(readback["link"])
    manifest = write_manifest(
        args.snapshot_dir,
        before_json,
        before_html,
        sha256(current_raw),
        sha256(readback_raw),
        public_url,
    )
    print(f"[APPLIED] post={POST_ID} modified={readback.get('modified_gmt')}")
    print(f"snapshot={before_json}")
    print(f"rollback={manifest}")
    print(f"verified={public_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
