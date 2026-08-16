#!/usr/bin/env python3
"""Safely sync the Futureproof v2 package to its existing private WP draft.

The command is authenticated and read-only by default. ``--apply`` snapshots
the complete edit-context post before uploading missing media or updating the
post. There is deliberately no publish, delete, or restore mode.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from create_local_wp_draft import (  # noqa: E402
    DraftPackage,
    WPConfig,
    load_package,
    load_wp_config,
    quality_issues,
)
from kk_notion_to_wp import REPO_ROOT, WordPress  # noqa: E402
from publish_common import build_seo_meta, select_media_match  # noqa: E402

TARGET_POST_ID = 12732
TARGET_SLUG = "futureproof-festival-announcement"
FEATURED_FILENAME = "futureproof-salmon-starfield-share-20260711.jpg"
DEFAULT_POST_MD = (
    REPO_ROOT
    / "content"
    / "drafts"
    / "2026-07-26-futureproof-festival-announcement"
    / "post.md"
)
KNOWN_MEDIA_IDS = {
    "vanai-meetup31-stage-kris-futureproof-slide.webp": 12725,
    "vanai-meetup31-audience-wide-shot.webp": 12726,
    "futureproof-honest-conversation-poster.png": 12727,
}
SEO_META_KEYS = ("jetpack_seo_html_title", "advanced_seo_description")
PRESERVED_FIELDS = (
    "status",
    "slug",
    "categories",
    "tags",
    "author",
    "date",
    "date_gmt",
)
IMAGE_BLOCK_RE = re.compile(
    r"<!-- wp:image(?: (?P<attrs>\{.*?\}))? -->"
    r"(?P<body>.*?)"
    r"<!-- /wp:image -->",
    flags=re.S,
)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", flags=re.I)
IMG_SRC_RE = re.compile(r'\bsrc="([^"]+)"', flags=re.I)
IMG_CLASS_RE = re.compile(r'\bclass="([^"]*)"', flags=re.I)


@dataclass(frozen=True)
class Asset:
    filename: str
    path: Path
    alt: str
    role: str
    source: str
    credit: str

    @property
    def title(self) -> str:
        label = self.role.replace("-", " ").strip() or self.path.stem.replace("-", " ")
        return f"Futureproof Festival: {label.title()}"

    @property
    def caption(self) -> str:
        parts = [part for part in (self.credit, f"Source: {self.source}" if self.source else "") if part]
        return " ".join(parts)

    @property
    def description(self) -> str:
        return " ".join(part for part in (self.alt, self.caption) if part)


def raw_field(value: object) -> str:
    if isinstance(value, dict):
        raw = value.get("raw")
        if raw is not None:
            return str(raw)
        rendered = value.get("rendered")
        if rendered is not None:
            return str(rendered)
    if value is None:
        return ""
    return str(value)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rendered_content_report(post: dict) -> dict:
    content = post.get("content") if isinstance(post.get("content"), dict) else {}
    raw = raw_field(content)
    rendered = str(content.get("rendered") or "")
    return {
        "raw_image_count": len(IMG_TAG_RE.findall(raw)),
        "raw_image_ids": [
            int(value)
            for value in re.findall(r'<!-- wp:image \{[^>]*"id":(\d+)', raw)
        ],
        "rendered_image_count": len(IMG_TAG_RE.findall(rendered)),
        "rendered_iframe_count": rendered.count("<iframe"),
        "youtube_present": "YitQ4fNEDW8" in rendered,
        "lazy_image_count": rendered.count('loading="lazy"'),
        "srcset_image_count": rendered.count(" srcset="),
        "sizes_image_count": rendered.count(" sizes="),
        "lightbox_trigger_count": rendered.count("data-wp-on--click"),
        "has_local_or_placeholder_markers": any(
            marker in raw + rendered
            for marker in ('src="images/', "wp-image-TBD", "content/drafts/", "/Users/")
        ),
    }


def package_assets(pkg: DraftPackage) -> dict[str, Asset]:
    assets: dict[str, Asset] = {}
    images_dir = (pkg.draft_dir / "images").resolve()
    for item in pkg.frontmatter.get("images") or []:
        relative = str(item.get("file", "")).strip()
        if not relative:
            raise RuntimeError("image frontmatter entry is missing file")
        relative_path = Path(relative)
        filename = relative_path.name
        if Path(relative).as_posix() != f"images/{filename}":
            raise RuntimeError(
                f"image path must use canonical images/<filename> form: {relative!r}"
            )
        path = (pkg.draft_dir / relative_path).resolve()
        if not path.is_relative_to(images_dir) or not path.is_file():
            raise RuntimeError(
                f"image must resolve to a regular file inside {images_dir}: {relative!r}"
            )
        if filename in assets:
            raise RuntimeError(f"duplicate image filename in frontmatter: {filename}")
        assets[filename] = Asset(
            filename=filename,
            path=path,
            alt=str(item.get("alt", "")).strip(),
            role=str(item.get("role", "")).strip(),
            source=str(item.get("source", "")).strip(),
            credit=str(item.get("credit", "")).strip(),
        )
    return assets


def local_image_filename(src: str) -> str | None:
    decoded = html.unescape(src)
    parsed = urlparse(decoded)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path).replace("\\", "/")
    if path.startswith("./"):
        path = path[2:]
    candidate = Path(path)
    if path != f"images/{candidate.name}" or candidate.name in ("", ".", ".."):
        return None
    return candidate.name


def referenced_image_filenames(body_html: str) -> list[str]:
    filenames: list[str] = []
    for tag in IMG_TAG_RE.findall(body_html):
        match = IMG_SRC_RE.search(tag)
        if not match:
            raise RuntimeError("image tag is missing src")
        filename = local_image_filename(match.group(1))
        if not filename:
            raise RuntimeError(
                f"canonical post.html contains a non-local or hotlinked image source: {match.group(1)!r}"
            )
        filenames.append(filename)
    return filenames


def assert_local_package(pkg: DraftPackage) -> dict[str, Asset]:
    issues = quality_issues(pkg)
    if issues:
        raise RuntimeError("quality gate failed: " + "; ".join(issues))
    if pkg.slug != TARGET_SLUG:
        raise RuntimeError(f"local slug mismatch: expected {TARGET_SLUG!r}, got {pkg.slug!r}")
    if str(pkg.frontmatter.get("status", "")).strip() != "draft":
        raise RuntimeError("local package must remain a draft")
    declared_featured_id = int(pkg.frontmatter.get("featured_media_id") or 0)
    if declared_featured_id < 0:
        raise RuntimeError("featured_media_id must be zero or a positive media id")

    assets = package_assets(pkg)
    for asset in assets.values():
        missing_metadata = [
            field
            for field, value in (
                ("alt", asset.alt),
                ("source", asset.source),
                ("credit", asset.credit),
            )
            if not value
        ]
        if missing_metadata:
            raise RuntimeError(
                f"image {asset.filename} is missing frontmatter metadata: "
                + ", ".join(missing_metadata)
            )
    referenced = referenced_image_filenames(pkg.body_html)
    if not referenced:
        raise RuntimeError("canonical post.html has no image blocks")
    missing_entries = sorted(set(referenced) - set(assets))
    if missing_entries:
        raise RuntimeError(
            "post.html images are missing from frontmatter: " + ", ".join(missing_entries)
        )
    if FEATURED_FILENAME not in assets:
        raise RuntimeError(f"frontmatter is missing featured asset {FEATURED_FILENAME}")
    return {
        name: assets[name]
        for name in dict.fromkeys([*referenced, FEATURED_FILENAME])
    }


def assert_target_post(post: dict, pkg: DraftPackage) -> None:
    if int(post.get("id") or 0) != TARGET_POST_ID:
        raise RuntimeError(
            f"target id mismatch: expected {TARGET_POST_ID}, got {post.get('id')!r}"
        )
    if post.get("slug") != TARGET_SLUG or post.get("slug") != pkg.slug:
        raise RuntimeError(
            f"target slug mismatch: WP={post.get('slug')!r}, local={pkg.slug!r}"
        )
    if post.get("status") != "draft":
        raise RuntimeError(
            f"refusing to update non-draft post {TARGET_POST_ID}: status={post.get('status')!r}"
        )


def seo_meta_supported(post: dict) -> bool:
    meta = post.get("meta")
    return isinstance(meta, dict) and all(key in meta for key in SEO_META_KEYS)


def media_record_matches(media: dict, path: Path) -> bool:
    try:
        match = select_media_match(
            [media], path.stem, extensions=(path.suffix.lower(),)
        )
    except SystemExit:
        return False
    return match is not None


def validate_known_media(wp: WordPress, asset: Asset, media_id: int) -> dict:
    media = wp.get_media(media_id, context="edit")
    if int(media.get("id") or 0) != media_id:
        raise RuntimeError(
            f"known media id mismatch for {asset.filename}: expected {media_id}, got {media.get('id')!r}"
        )
    if not media_record_matches(media, asset.path):
        raise RuntimeError(
            f"known media {media_id} does not match exact filename {asset.filename!r}"
        )
    source_url = str(media.get("source_url", "")).strip()
    if not source_url:
        raise RuntimeError(f"known media {media_id} has no source_url")
    return {"id": media_id, "source_url": source_url}


def search_media_exact(wp: WordPress, path: Path) -> dict | None:
    response = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/media",
        params={
            "search": path.stem,
            "per_page": 100,
            "context": "edit",
        },
        timeout=30,
    )
    response.raise_for_status()
    results = response.json()
    if not isinstance(results, list):
        raise RuntimeError(f"unexpected media search response for {path.name}")
    try:
        match = select_media_match(
            results, path.stem, extensions=(path.suffix.lower(),)
        )
    except SystemExit as exc:
        raise RuntimeError(str(exc)) from exc
    if not match:
        return None
    media_id, source_url = match
    return {"id": int(media_id), "source_url": str(source_url)}


def resolve_media_plan(
    wp: WordPress, assets: dict[str, Asset]
) -> tuple[dict[str, dict], list[Asset]]:
    resolved: dict[str, dict] = {}
    missing: list[Asset] = []
    for filename, asset in assets.items():
        known_id = KNOWN_MEDIA_IDS.get(filename)
        if known_id is not None:
            resolved[filename] = validate_known_media(wp, asset, known_id)
            continue
        found = search_media_exact(wp, asset.path)
        if found:
            resolved[filename] = found
        else:
            missing.append(asset)
    return resolved, missing


def set_image_class(tag: str, media_id: int) -> str:
    class_name = f"wp-image-{media_id}"
    match = IMG_CLASS_RE.search(tag)
    if match:
        classes = [
            value
            for value in match.group(1).split()
            if not re.fullmatch(r"wp-image-(?:TBD|\d+)", value)
        ]
        classes.append(class_name)
        return tag[: match.start(1)] + " ".join(classes) + tag[match.end(1) :]
    closing = "/>" if tag.endswith("/>") else ">"
    return f'{tag[: -len(closing)]} class="{class_name}"{closing}'


def rewrite_image_blocks(body_html: str, media: dict[str, dict]) -> str:
    used: set[str] = set()

    def replace_block(match: re.Match[str]) -> str:
        body = match.group("body")
        tags = IMG_TAG_RE.findall(body)
        if len(tags) != 1:
            raise RuntimeError("each Gutenberg image block must contain exactly one img tag")
        tag = tags[0]
        src_match = IMG_SRC_RE.search(tag)
        if not src_match:
            raise RuntimeError("image block is missing src")
        filename = local_image_filename(src_match.group(1))
        if not filename:
            raise RuntimeError(
                f"refusing to preserve hotlinked image source {src_match.group(1)!r}"
            )
        if filename not in media:
            raise RuntimeError(f"image has no resolved WordPress media: {filename}")
        record = media[filename]
        media_id = int(record["id"])
        source_url = str(record["source_url"])
        escaped_url = html.escape(source_url, quote=True)
        rewritten_tag = (
            tag[: src_match.start(1)]
            + escaped_url
            + tag[src_match.end(1) :]
        )
        rewritten_tag = set_image_class(rewritten_tag, media_id)
        rewritten_body = body.replace(tag, rewritten_tag, 1)

        attrs_raw = match.group("attrs")
        attrs = json.loads(attrs_raw) if attrs_raw else {}
        if not isinstance(attrs, dict):
            raise RuntimeError("Gutenberg image attributes must be a JSON object")
        attrs["id"] = media_id
        encoded_attrs = json.dumps(attrs, ensure_ascii=False, separators=(",", ":"))
        used.add(filename)
        return (
            f"<!-- wp:image {encoded_attrs} -->"
            f"{rewritten_body}"
            "<!-- /wp:image -->"
        )

    rewritten = IMAGE_BLOCK_RE.sub(replace_block, body_html)
    referenced = set(referenced_image_filenames(body_html))
    if used != referenced:
        missing = sorted(referenced - used)
        raise RuntimeError(
            "not every canonical image was inside a Gutenberg image block: "
            + ", ".join(missing)
        )
    validate_rewritten_content(rewritten, media)
    return rewritten


def validate_rewritten_content(body_html: str, media: dict[str, dict]) -> None:
    forbidden = ("wp-image-TBD", 'src="images/', "content/drafts/", "/Users/")
    present = [value for value in forbidden if value in body_html]
    if present:
        raise RuntimeError("rewritten content contains forbidden local markers: " + ", ".join(present))

    allowed_urls = {str(record["source_url"]) for record in media.values()}
    tags = IMG_TAG_RE.findall(body_html)
    sources: list[str] = []
    for tag in tags:
        src_match = IMG_SRC_RE.search(tag)
        if not src_match:
            raise RuntimeError("rewritten image is missing src")
        source = html.unescape(src_match.group(1))
        if source not in allowed_urls:
            raise RuntimeError(f"rewritten content retains an unowned image source: {source!r}")
        sources.append(source)

    blocks = list(IMAGE_BLOCK_RE.finditer(body_html))
    if len(blocks) != len(tags):
        raise RuntimeError("every rewritten image must remain in its own Gutenberg image block")
    for block in blocks:
        attrs = json.loads(block.group("attrs") or "{}")
        media_id = attrs.get("id")
        if not isinstance(media_id, int) or media_id <= 0:
            raise RuntimeError("every Gutenberg image block must carry a positive media id")
        tag = IMG_TAG_RE.search(block.group("body"))
        if not tag or f"wp-image-{media_id}" not in tag.group(0).split('class="', 1)[-1]:
            raise RuntimeError(f"image block {media_id} is missing its matching wp-image class")


def expected_seo_meta(pkg: DraftPackage) -> dict[str, str]:
    seo = pkg.frontmatter.get("seo") or {}
    return build_seo_meta(
        str(seo.get("meta_title", "")).strip(),
        str(seo.get("meta_description", "")).strip(),
    )


def build_post_payload(
    pkg: DraftPackage,
    content: str,
    *,
    featured_media_id: int,
    seo_meta_supported: bool,
) -> dict:
    payload = {
        "title": pkg.title,
        "content": content,
        "excerpt": pkg.excerpt,
        "featured_media": featured_media_id,
    }
    if seo_meta_supported:
        payload["meta"] = expected_seo_meta(pkg)
    return payload


def snapshot_post(pkg: DraftPackage, post: dict) -> Path:
    snapshot_dir = pkg.draft_dir / "wp-snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = snapshot_dir / f"rest-post-{TARGET_POST_ID}-before-polish-v2-{stamp}.json.tmp"
    payload = (json.dumps(post, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return path


def preserved_values(post: dict) -> dict:
    return {field: post[field] for field in PRESERVED_FIELDS if field in post}


def concurrency_values(post: dict) -> dict:
    return {
        "modified": post.get("modified"),
        "modified_gmt": post.get("modified_gmt"),
        "title": raw_field(post.get("title")),
        "content": raw_field(post.get("content")),
        "excerpt": raw_field(post.get("excerpt")),
        "featured_media": int(post.get("featured_media") or 0),
        "meta": post.get("meta"),
        **preserved_values(post),
    }


def assert_post_unchanged(before: dict, current: dict, pkg: DraftPackage) -> None:
    assert_target_post(current, pkg)
    expected = concurrency_values(before)
    actual = concurrency_values(current)
    changed = sorted(
        field for field in set(expected) | set(actual) if expected.get(field) != actual.get(field)
    )
    if changed:
        raise RuntimeError(
            "target post changed during sync; aborting before content write: "
            + ", ".join(changed)
        )


def verify_readback(
    before: dict,
    after: dict,
    pkg: DraftPackage,
    payload: dict,
    media: dict[str, dict],
    featured_media_id: int,
) -> dict:
    assert_target_post(after, pkg)
    expected_fields = {
        "title": pkg.title,
        "content": payload["content"],
        "excerpt": pkg.excerpt,
    }
    mismatches = [
        field
        for field, expected in expected_fields.items()
        if raw_field(after.get(field)) != expected
    ]
    if mismatches:
        raise RuntimeError("exact WordPress readback mismatch: " + ", ".join(mismatches))
    if int(after.get("featured_media") or 0) != featured_media_id:
        raise RuntimeError(
            f"featured media readback mismatch: {after.get('featured_media')!r}"
        )
    if "meta" in payload:
        after_meta = after.get("meta")
        if not isinstance(after_meta, dict):
            raise RuntimeError("SEO meta was sent but is absent from readback")
        seo_mismatches = [
            key for key, value in payload["meta"].items() if after_meta.get(key) != value
        ]
        if seo_mismatches:
            raise RuntimeError("SEO meta readback mismatch: " + ", ".join(seo_mismatches))

    before_preserved = preserved_values(before)
    after_preserved = preserved_values(after)
    if after_preserved != before_preserved:
        changed = sorted(
            field
            for field in set(before_preserved) | set(after_preserved)
            if before_preserved.get(field) != after_preserved.get(field)
        )
        raise RuntimeError("non-payload fields changed unexpectedly: " + ", ".join(changed))
    validate_rewritten_content(raw_field(after.get("content")), media)
    return after_preserved


def receipt_base(
    *,
    cfg: WPConfig,
    before: dict,
    payload_fields: list[str],
    supported_seo: bool,
) -> dict:
    base = cfg.base_url.rstrip("/")
    return {
        "post_id": TARGET_POST_ID,
        "slug": TARGET_SLUG,
        "status": "draft",
        "published": False,
        "seo_meta_supported": supported_seo,
        "payload_fields": payload_fields,
        "before_content_sha256": sha256_text(raw_field(before.get("content"))),
        "featured_media_id": None,
        "preview_url": f"{base}/?p={TARGET_POST_ID}",
        "edit_url": f"{base}/wp-admin/post.php?post={TARGET_POST_ID}&action=edit",
    }


def sync_futureproof(post_md: Path = DEFAULT_POST_MD, *, apply: bool = False) -> dict:
    pkg = load_package(post_md)
    assets = assert_local_package(pkg)
    cfg = load_wp_config()
    wp = WordPress(cfg.base_url, cfg.user, cfg.app_password)

    before = wp.get_post(TARGET_POST_ID)
    assert_target_post(before, pkg)
    supported_seo = seo_meta_supported(before)
    payload_fields = ["title", "content", "excerpt", "featured_media"]
    if supported_seo:
        payload_fields.append("meta")

    resolved, missing = resolve_media_plan(wp, assets)
    declared_featured_id = int(pkg.frontmatter.get("featured_media_id") or 0)
    resolved_featured = resolved.get(FEATURED_FILENAME)
    if declared_featured_id and resolved_featured:
        if int(resolved_featured["id"]) != declared_featured_id:
            raise RuntimeError(
                "frontmatter featured_media_id does not match the exact resolved "
                f"{FEATURED_FILENAME}: declared={declared_featured_id}, "
                f"resolved={resolved_featured['id']}"
            )
    elif declared_featured_id:
        raise RuntimeError(
            "frontmatter declares a featured_media_id, but the exact featured "
            "filename was not found in WordPress"
        )
    missing_names = [asset.filename for asset in missing]
    reused_ids = {name: int(record["id"]) for name, record in resolved.items()}
    result = receipt_base(
        cfg=cfg,
        before=before,
        payload_fields=payload_fields,
        supported_seo=supported_seo,
    )
    result.update(
        {
            "dry_run": not apply,
            "snapshot_path": None,
            "new_media_ids": {},
            "reused_media_ids": reused_ids,
            "missing_media": missing_names,
            "would_upload": missing_names,
            "preserved_fields": preserved_values(before),
            "after_content_sha256": None,
            "restore_command": None,
            "featured_media_id": (
                int(resolved_featured["id"]) if resolved_featured else None
            ),
            "rendered_content": rendered_content_report(before),
        }
    )

    if not apply:
        if not missing:
            content = rewrite_image_blocks(pkg.body_html, resolved)
            result["after_content_sha256"] = sha256_text(content)
        return result

    snapshot = snapshot_post(pkg, before)
    result["snapshot_path"] = str(snapshot)
    result["restore_command"] = (
        f"MANUAL ONLY: review {snapshot} and construct a separate minimal authenticated "
        "REST restore payload; no automated restore mode is provided by this guarded sync"
    )
    new_ids: dict[str, int] = {}
    for asset in missing:
        mime = mimetypes.guess_type(asset.filename)[0] or "application/octet-stream"
        media = wp.upload_media(
            asset.path,
            alt=asset.alt,
            mime=mime,
            title=asset.title,
            caption=asset.caption,
            description=asset.description,
        )
        media_id = int(media.get("id") or 0)
        source_url = str(media.get("source_url", "")).strip()
        if media_id <= 0 or not source_url:
            raise RuntimeError(f"upload returned incomplete media for {asset.filename}")
        resolved[asset.filename] = {"id": media_id, "source_url": source_url}
        new_ids[asset.filename] = media_id

    featured_media_id = int(resolved[FEATURED_FILENAME]["id"])
    if declared_featured_id and declared_featured_id != featured_media_id:
        raise RuntimeError(
            "uploaded featured media does not match declared featured_media_id: "
            f"declared={declared_featured_id}, resolved={featured_media_id}"
        )
    content = rewrite_image_blocks(pkg.body_html, resolved)
    payload = build_post_payload(
        pkg,
        content,
        featured_media_id=featured_media_id,
        seo_meta_supported=supported_seo,
    )
    prewrite = wp.get_post(TARGET_POST_ID)
    assert_post_unchanged(before, prewrite, pkg)
    updated = wp.update_post(TARGET_POST_ID, payload, expected_slug=pkg.slug)
    if int(updated.get("id") or 0) != TARGET_POST_ID:
        raise RuntimeError(f"unexpected update response id: {updated.get('id')!r}")
    after = wp.get_post(TARGET_POST_ID)
    preserved = verify_readback(
        before,
        after,
        pkg,
        payload,
        resolved,
        featured_media_id,
    )

    result.update(
        {
            "dry_run": False,
            "new_media_ids": new_ids,
            "reused_media_ids": {
                name: media_id
                for name, media_id in reused_ids.items()
                if name not in new_ids
            },
            "missing_media": [],
            "would_upload": [],
            "after_content_sha256": sha256_text(raw_field(after.get("content"))),
            "preserved_fields": preserved,
            "featured_media_id": featured_media_id,
            "rendered_content": rendered_content_report(after),
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_md", nargs="?", type=Path, default=DEFAULT_POST_MD)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Snapshot, upload only missing media, and update the existing private draft.",
    )
    args = parser.parse_args()
    try:
        result = sync_futureproof(args.post_md, apply=args.apply)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
