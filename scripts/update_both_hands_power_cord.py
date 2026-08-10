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


POST_ID = 12656
POST_SLUG = "both-hands-on-the-power-cord"
OLD_TITLE = "Both Hands on the Power Cord"
NEW_TITLE = "Both Hands on the Power Cord: AI, Energy and Who Gets Canada's Future"
MEDIA_SLUG = "kris-krug-jason-dsouza-cbc-vancouver-2026-08-03"
MEDIA_FILENAME = f"{MEDIA_SLUG}.jpg"
MEDIA_ALT = "Kris Krüg and CBC interviewer Jason D'Souza in the CBC Vancouver studio"
MEDIA_CAPTION = (
    "Kris Krüg with interviewer Jason D'Souza at CBC Vancouver after their BC Day "
    "conversation. Photo: Kris Krüg."
)
AUDIO_URL = "https://mp3.cbc.ca/radio/2026/08/03/dave-JlqWqynA-20260803.mp3"
HERO_PATH = (
    Path(__file__).resolve().parents[1]
    / "content/drafts/2026-07-31-both-hands-on-the-power-cord/img/hero.jpg"
)
DEFAULT_SNAPSHOT_DIR = Path("backup/20260810-both-hands-title-visual-refresh")

OLD_IMAGE_BLOCK = """<!-- wp:image {\"sizeSlug\":\"large\",\"linkDestination\":\"none\"} -->
<figure class=\"wp-block-image size-large\"><img src=\"https://kriskrug.co/wp-content/uploads/2026/08/cbc-the-early-edition-2026-08-03.jpg\" alt=\"CBC The Early Edition program artwork featuring host Stephen Quinn\" class=\"wp-image-12717\"/><figcaption class=\"wp-element-caption\">CBC/The Early Edition program artwork. Host: Stephen Quinn.</figcaption></figure>
<!-- /wp:image -->"""


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_bypass(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["cb"] = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def auth_session() -> tuple[requests.Session, str]:
    base_url = os.getenv("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = os.getenv("WP_API_USERNAME") or os.getenv("WP_USER")
    password = os.getenv("WP_API_PASSWORD") or os.getenv("WP_APP_PASSWORD")
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
    if post.get("status") != "publish":
        raise SystemExit(f"[ABORT] expected published status, got {post.get('status')!r}")
    if title not in {OLD_TITLE, NEW_TITLE}:
        raise SystemExit(f"[ABORT] unexpected live title {title!r}")
    if not post.get("content", {}).get("raw"):
        raise SystemExit("[ABORT] authenticated response did not include content.raw")
    return post


def image_block(media_id: int | str, source_url: str) -> str:
    return f"""<!-- wp:image {{\"id\":{media_id},\"sizeSlug\":\"large\",\"linkDestination\":\"none\"}} -->
<figure class=\"wp-block-image size-large\"><img src=\"{source_url}\" alt=\"{MEDIA_ALT}\" class=\"wp-image-{media_id}\"/><figcaption class=\"wp-element-caption\">{MEDIA_CAPTION}</figcaption></figure>
<!-- /wp:image -->"""


def build_updated(raw: str, media_id: int | str, source_url: str) -> tuple[str, bool]:
    desired_block = image_block(media_id, source_url)
    if OLD_IMAGE_BLOCK in raw:
        if raw.count(OLD_IMAGE_BLOCK) != 1:
            raise SystemExit("[ABORT] old CBC image block is not unique")
        return raw.replace(OLD_IMAGE_BLOCK, desired_block), False
    if MEDIA_SLUG in raw and MEDIA_ALT in raw and "Stephen Quinn" not in raw:
        return raw, True
    raise SystemExit("[ABORT] live CBC image block is neither the expected old nor new state")


def diff_text(before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="post-12656-before.html",
            tofile="post-12656-after.html",
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


def find_media(session: requests.Session, base_url: str) -> dict | None:
    response = session.get(
        f"{base_url}/wp-json/wp/v2/media",
        params={"slug": MEDIA_SLUG, "status": "inherit", "per_page": 10, "context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    matches = response.json()
    if len(matches) > 1:
        raise SystemExit(f"[ABORT] expected at most one media match, found {len(matches)}")
    return matches[0] if matches else None


def upload_media(session: requests.Session, base_url: str) -> dict:
    if not HERO_PATH.is_file():
        raise SystemExit(f"[ABORT] hero image is missing: {HERO_PATH}")
    response = session.post(
        f"{base_url}/wp-json/wp/v2/media",
        headers={
            "Content-Disposition": f'attachment; filename="{MEDIA_FILENAME}"',
            "Content-Type": "image/jpeg",
        },
        data=HERO_PATH.read_bytes(),
        timeout=120,
    )
    response.raise_for_status()
    media = response.json()
    metadata = session.post(
        f"{base_url}/wp-json/wp/v2/media/{media['id']}",
        json={
            "alt_text": MEDIA_ALT,
            "title": "Kris Krüg with Jason D'Souza at CBC Vancouver",
            "caption": MEDIA_CAPTION,
        },
        timeout=30,
    )
    metadata.raise_for_status()
    return metadata.json()


def update_post(
    session: requests.Session,
    base_url: str,
    *,
    title: str,
    content: str,
    featured_media: int,
) -> dict:
    response = session.post(
        f"{base_url}/wp-json/wp/v2/posts/{POST_ID}",
        json={"title": title, "content": content, "featured_media": featured_media},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def og_image(html: str) -> str:
    for tag in re.findall(r"<meta\b[^>]*>", html, flags=re.I):
        if not re.search(r"property=[\"']og:image[\"']", tag, flags=re.I):
            continue
        match = re.search(r"content=[\"']([^\"']+)", tag, flags=re.I)
        if match:
            return match.group(1)
    return ""


def verify_public(post_url: str) -> tuple[str, str]:
    url = cache_bypass(post_url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()
    html = response.text
    required = [
        "Both Hands on the Power Cord: AI, Energy and Who Gets Canada",
        MEDIA_SLUG,
        "Jason D",
        AUDIO_URL,
    ]
    missing = [item for item in required if item not in html]
    if missing or "Stephen Quinn" in html:
        raise SystemExit(f"[ABORT] public verification failed; missing={missing}")
    og_url = og_image(html)
    if MEDIA_SLUG not in og_url:
        raise SystemExit(f"[ABORT] og:image does not reference approved media: {og_url!r}")
    return url, og_url


def write_manifest(
    snapshot_dir: Path,
    before_json: Path,
    before_html: Path,
    before_post: dict,
    after_post: dict,
    media: dict,
    public_url: str,
    og_url: str,
) -> Path:
    manifest_path = snapshot_dir / "rollback-manifest.json"
    restore_command = (
        "pnpm exec varlock run --inject vars -- python3 "
        "scripts/update_both_hands_power_cord.py "
        f"--restore {before_json} --apply"
    )
    manifest = {
        "post_id": POST_ID,
        "slug": POST_SLUG,
        "snapshot_json": str(before_json),
        "snapshot_html": str(before_html),
        "before_content_sha256": sha256(before_post["content"]["raw"]),
        "after_content_sha256": sha256(after_post["content"]["raw"]),
        "before_title": before_post["title"]["raw"],
        "after_title": after_post["title"]["raw"],
        "before_featured_media": before_post["featured_media"],
        "after_featured_media": after_post["featured_media"],
        "new_media_id": media["id"],
        "new_media_url": media["source_url"],
        "public_verification_url": public_url,
        "og_image": og_url,
        "restore_command": restore_command,
        "rollback_note": "Restoring the post leaves the newly uploaded media attachment in the library.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update KrisKrug.co post 12656")
    parser.add_argument("--apply", action="store_true", help="perform WordPress writes")
    parser.add_argument("--restore", type=Path, help="restore title, content, and featured media")
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session, base_url = auth_session()
    current = fetch_post(session, base_url)
    current_raw = current["content"]["raw"]

    if args.restore:
        snapshot = json.loads(args.restore.read_text(encoding="utf-8"))
        if snapshot.get("id") != POST_ID or snapshot.get("slug") != POST_SLUG:
            raise SystemExit("[ABORT] restore snapshot is for the wrong post")
        desired_title = snapshot["title"]["raw"]
        desired_content = snapshot["content"]["raw"]
        desired_media = int(snapshot["featured_media"])
        print(f"title: {current['title']['raw']!r} -> {desired_title!r}")
        print(f"featured_media: {current['featured_media']} -> {desired_media}")
        print(diff_text(current_raw, desired_content))
        if not args.apply:
            print("[DRY RUN] restore diff only; pass --apply to write")
            return 0
        write_snapshot(current, args.snapshot_dir, "before-restore")
        update_post(
            session,
            base_url,
            title=desired_title,
            content=desired_content,
            featured_media=desired_media,
        )
        readback = fetch_post(session, base_url)
        if (
            readback["title"]["raw"] != desired_title
            or readback["featured_media"] != desired_media
            or sha256(readback["content"]["raw"]) != sha256(desired_content)
        ):
            raise SystemExit("[ABORT] restore readback mismatch")
        print(f"[RESTORED] post={POST_ID}")
        return 0

    media = find_media(session, base_url)
    preview_id: int | str = media["id"] if media else "TBD"
    preview_url = media["source_url"] if media else f"__WP_MEDIA_URL__/{MEDIA_FILENAME}"
    desired_preview, already_applied = build_updated(current_raw, preview_id, preview_url)
    title_ok = current["title"]["raw"] == NEW_TITLE
    featured_ok = bool(media and current["featured_media"] == media["id"])
    if already_applied and title_ok and featured_ok:
        print(f"[NOOP] post={POST_ID} already has the approved title and media")
        return 0

    print(f"target post={POST_ID} slug={POST_SLUG} status={current['status']}")
    print(f"title: {current['title']['raw']!r} -> {NEW_TITLE!r}")
    print(f"featured_media: {current['featured_media']} -> {preview_id}")
    print(diff_text(current_raw, desired_preview))
    if not args.apply:
        print("[DRY RUN] no WordPress or media-library write; pass --apply to write")
        return 0

    before_json, before_html = write_snapshot(current, args.snapshot_dir, "before-title-visual-refresh")
    if media is None:
        media = upload_media(session, base_url)
        print(f"[UPLOADED] media={media['id']} url={media['source_url']}")
    desired, _ = build_updated(current_raw, media["id"], media["source_url"])
    result = update_post(
        session,
        base_url,
        title=NEW_TITLE,
        content=desired,
        featured_media=media["id"],
    )
    if result.get("id") != POST_ID:
        raise SystemExit("[ABORT] update response returned the wrong post id")
    readback = fetch_post(session, base_url)
    if (
        readback["title"]["raw"] != NEW_TITLE
        or readback["featured_media"] != media["id"]
        or sha256(readback["content"]["raw"]) != sha256(desired)
        or "Stephen Quinn" in readback["content"]["raw"]
        or AUDIO_URL not in readback["content"]["raw"]
    ):
        raise SystemExit("[ABORT] authenticated readback mismatch")
    public_url, og_url = verify_public(readback["link"])
    manifest = write_manifest(
        args.snapshot_dir,
        before_json,
        before_html,
        current,
        readback,
        media,
        public_url,
        og_url,
    )
    print(f"[APPLIED] post={POST_ID} modified={readback.get('modified_gmt')}")
    print(f"snapshot={before_json}")
    print(f"rollback={manifest}")
    print(f"verified={public_url}")
    print(f"og_image={og_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
