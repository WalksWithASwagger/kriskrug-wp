#!/usr/bin/env python3
"""Create a guarded WordPress draft from a local draft package.

This is for recovered/rebuilt packages where `post.html` is already the
reviewed canonical Gutenberg body. It does not fetch Notion and it never
publishes. It defaults to a dry-run and creates a new WP draft only when
`--execute` is passed and no post or page already owns the slug.
"""

from __future__ import annotations

import argparse
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

import yaml
from dotenv import dotenv_values

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from kk_notion_to_wp import (  # noqa: E402
    KKAI_ENV_PATH,
    LOCAL_ENV_PATH,
    REPO_ROOT,
    WP_BASE_URL_DEFAULT,
    WP_DEFAULT_AUTHOR_ID,
    WordPress,
    slugify,
)


@dataclass(frozen=True)
class WPConfig:
    base_url: str
    user: str
    app_password: str
    author_id: int


@dataclass(frozen=True)
class DraftPackage:
    post_md: Path
    draft_dir: Path
    frontmatter: dict
    body_markdown: str
    body_html: str

    @property
    def title(self) -> str:
        return str(self.frontmatter.get("title", "")).strip()

    @property
    def slug(self) -> str:
        return str(self.frontmatter.get("slug", "")).strip()

    @property
    def excerpt(self) -> str:
        return str(self.frontmatter.get("excerpt", "")).strip()


def load_wp_config() -> WPConfig:
    local = dotenv_values(LOCAL_ENV_PATH) if LOCAL_ENV_PATH.exists() else {}
    fallback = dotenv_values(KKAI_ENV_PATH) if KKAI_ENV_PATH.exists() else {}

    def get(key: str, default: str | None = None) -> str | None:
        return local.get(key) or fallback.get(key) or os.environ.get(key) or default

    user = get("WP_USER")
    app_password = (get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not app_password:
        raise RuntimeError(f"WP credentials not found in {LOCAL_ENV_PATH} or environment")
    return WPConfig(
        base_url=get("WP_BASE_URL", WP_BASE_URL_DEFAULT) or WP_BASE_URL_DEFAULT,
        user=user,
        app_password=app_password,
        author_id=int(get("WP_DEFAULT_AUTHOR_ID", str(WP_DEFAULT_AUTHOR_ID)) or WP_DEFAULT_AUTHOR_ID),
    )


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()


def load_package(post_md: Path) -> DraftPackage:
    post_md = post_md.resolve()
    draft_dir = post_md.parent
    frontmatter, body = split_frontmatter(post_md.read_text(encoding="utf-8"))
    post_html = draft_dir / "post.html"
    if not post_html.exists():
        raise RuntimeError(f"missing canonical HTML body: {post_html}")
    return DraftPackage(
        post_md=post_md,
        draft_dir=draft_dir,
        frontmatter=frontmatter,
        body_markdown=body,
        body_html=post_html.read_text(encoding="utf-8"),
    )


def image_entries(pkg: DraftPackage) -> list[tuple[Path, str]]:
    entries: list[tuple[Path, str]] = []
    for item in pkg.frontmatter.get("images") or []:
        rel = str(item.get("file", "")).strip()
        if not rel:
            continue
        path = (pkg.draft_dir / rel).resolve()
        entries.append((path, str(item.get("alt", "")).strip()))
    return entries


def quality_issues(pkg: DraftPackage) -> list[str]:
    issues: list[str] = []
    if not pkg.title:
        issues.append("missing frontmatter title")
    if not pkg.slug:
        issues.append("missing frontmatter slug")
    if not pkg.excerpt:
        issues.append("missing excerpt")
    if str(pkg.frontmatter.get("status", "")).strip() != "draft":
        issues.append("frontmatter status must be draft")
    if "<!-- wp:" not in pkg.body_html:
        issues.append("post.html has no Gutenberg block comments")
    if "/Users/" in pkg.body_html or "/Users/" in pkg.body_markdown:
        issues.append("public body contains an absolute local path")
    for path, _alt in image_entries(pkg):
        if not path.exists():
            issues.append(f"missing image file: {path}")
    return issues


def log_line(pkg: DraftPackage, message: str) -> None:
    line = f"[{datetime.now(timezone.utc).isoformat()}] {message}"
    print(line)
    with (pkg.draft_dir / "publish.log").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def wp_hits_by_slug(wp: WordPress, slug: str, kind: str) -> list[dict]:
    response = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/{kind}",
        params={"slug": slug, "status": "any", "per_page": 100, "context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def assert_slug_available(wp: WordPress, slug: str) -> None:
    collisions: list[str] = []
    for kind in ("posts", "pages"):
        hits = wp_hits_by_slug(wp, slug, kind)
        for hit in hits:
            collisions.append(f"{kind[:-1]} {hit.get('id')} ({hit.get('status')})")
    if collisions:
        raise RuntimeError(f"slug {slug!r} is already owned by: {', '.join(collisions)}")


def resolve_local_src(src: str, draft_dir: Path, repo_root: Path = REPO_ROOT) -> Path | None:
    parsed = urlparse(src)
    if parsed.scheme in {"http", "https", "data"}:
        return None
    raw = unquote(parsed.path)
    candidates = []
    path = Path(raw)
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.extend([repo_root / raw, draft_dir / raw])
    for candidate in candidates:
        try:
            return candidate.resolve(strict=True)
        except FileNotFoundError:
            continue
    return None


def _set_img_class(attrs: str, media_id: int) -> str:
    class_name = f"wp-image-{media_id}"
    if "wp-image-TBD" in attrs:
        return attrs.replace("wp-image-TBD", class_name)
    class_match = re.search(r'\bclass="([^"]*)"', attrs)
    if class_match:
        classes = class_match.group(1).split()
        if class_name not in classes:
            classes.append(class_name)
        return attrs[:class_match.start(1)] + " ".join(classes) + attrs[class_match.end(1):]
    stripped = attrs.rstrip()
    closing = "/>" if stripped.endswith("/>") else ">"
    body = stripped[:-2] if closing == "/>" else stripped[:-1]
    return f'{body} class="{class_name}"{closing}'


def rewrite_uploaded_images(
    html_body: str,
    draft_dir: Path,
    uploaded: dict[Path, dict],
    repo_root: Path = REPO_ROOT,
) -> str:
    by_path = {path.resolve(): meta for path, meta in uploaded.items()}

    def replace(match: re.Match[str]) -> str:
        prefix, src, suffix, tail = match.groups()
        local_path = resolve_local_src(html.unescape(src), draft_dir, repo_root=repo_root)
        if not local_path or local_path not in by_path:
            return match.group(0)
        meta = by_path[local_path]
        media_id = int(meta["id"])
        rewritten_tail = _set_img_class(tail, media_id)
        return f'{prefix}{html.escape(str(meta["source_url"]), quote=True)}{suffix}{rewritten_tail}'

    return re.sub(r'(<img\b[^>]*\bsrc=")([^"]+)(")([^>]*>)', replace, html_body)


def ensure_term(wp: WordPress, taxonomy: str, name: str) -> int:
    slug = slugify(name)
    for params in ({"slug": slug, "per_page": 100}, {"search": name, "per_page": 100}):
        response = wp.s.get(f"{wp.base}/wp-json/wp/v2/{taxonomy}", params=params, timeout=30)
        response.raise_for_status()
        for term in response.json():
            if term.get("slug") == slug or term.get("name", "").lower() == name.lower():
                return int(term["id"])

    response = wp.s.post(
        f"{wp.base}/wp-json/wp/v2/{taxonomy}",
        json={"name": name, "slug": slug},
        timeout=30,
    )
    if response.status_code == 400:
        try:
            data = response.json()
        except ValueError:
            data = {}
        term_id = (data.get("data") or {}).get("term_id")
        if data.get("code") == "term_exists" and term_id:
            return int(term_id)
    response.raise_for_status()
    return int(response.json()["id"])


def ensure_terms(wp: WordPress, taxonomy: str, values: list[str]) -> list[int]:
    return [ensure_term(wp, taxonomy, value) for value in values if str(value).strip()]


def logged_media(pkg: DraftPackage) -> dict[str, dict]:
    log_path = pkg.draft_dir / "publish.log"
    if not log_path.exists():
        return {}
    media: dict[str, dict] = {}
    pattern = re.compile(r"media (?P<name>[^ ]+) -> id=(?P<id>\d+) url=(?P<url>\S+)")
    for line in log_path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if match:
            media[match.group("name")] = {
                "id": int(match.group("id")),
                "source_url": match.group("url"),
            }
    return media


def build_payload(pkg: DraftPackage, cfg: WPConfig, content: str, uploaded: dict[Path, dict]) -> dict:
    categories = [str(value).strip() for value in (pkg.frontmatter.get("categories") or []) if str(value).strip()]
    tags = [str(value).strip() for value in (pkg.frontmatter.get("tags") or []) if str(value).strip()]
    post_date = str(pkg.frontmatter.get("post_date", "")).strip()
    payload: dict = {
        "title": pkg.title,
        "slug": pkg.slug,
        "status": "draft",
        "author": int(pkg.frontmatter.get("author_wp_id") or cfg.author_id),
        "excerpt": pkg.excerpt,
        "content": content,
    }
    if post_date:
        payload["date"] = post_date if "T" in post_date else f"{post_date}T12:00:00"
    if uploaded:
        first_media = next(iter(uploaded.values()))
        payload["featured_media"] = int(first_media["id"])
    seo = pkg.frontmatter.get("seo") or {}
    if seo:
        payload["meta"] = {
            "jetpack_seo_html_title": str(seo.get("meta_title", "")).strip(),
            "advanced_seo_description": str(seo.get("meta_description", "")).strip(),
        }
    payload["_local_categories"] = categories
    payload["_local_tags"] = tags
    return payload


def upload_images(wp: WordPress, pkg: DraftPackage) -> dict[Path, dict]:
    uploaded: dict[Path, dict] = {}
    reusable = logged_media(pkg)
    for path, alt in image_entries(pkg):
        if path.name in reusable:
            media = reusable[path.name]
            uploaded[path.resolve()] = media
            log_line(pkg, f"reusing logged media {path.name} -> id={media.get('id')}")
            continue
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        log_line(pkg, f"uploading media {path.name}")
        media = wp.upload_media(path, alt=alt, mime=mime)
        uploaded[path.resolve()] = media
        log_line(pkg, f"media {path.name} -> id={media.get('id')} url={media.get('source_url')}")
    return uploaded


def create_local_draft(post_md: Path, dry_run: bool = True) -> dict:
    pkg = load_package(post_md)
    issues = quality_issues(pkg)
    if issues:
        raise RuntimeError("quality gate failed: " + "; ".join(issues))
    cfg = load_wp_config()
    wp = WordPress(cfg.base_url, cfg.user, cfg.app_password)
    assert_slug_available(wp, pkg.slug)
    if dry_run:
        payload = build_payload(pkg, cfg, pkg.body_html, {})
        return {
            "dry_run": True,
            "slug": pkg.slug,
            "title": pkg.title,
            "categories": payload.pop("_local_categories", []),
            "tags": payload.pop("_local_tags", []),
            "images": [str(path) for path, _alt in image_entries(pkg)],
        }

    uploaded = upload_images(wp, pkg)
    content = rewrite_uploaded_images(pkg.body_html, pkg.draft_dir, uploaded)
    if re.search(r'src="(?:/Users/|content/drafts/|images/)', content):
        raise RuntimeError("rewritten HTML still contains local image paths")

    payload = build_payload(pkg, cfg, content, uploaded)
    categories = payload.pop("_local_categories", [])
    tags = payload.pop("_local_tags", [])
    if categories:
        payload["categories"] = ensure_terms(wp, "categories", categories)
    if tags:
        payload["tags"] = ensure_terms(wp, "tags", tags)

    result = wp.create_post(payload)
    readback = wp.get_post(int(result["id"]))
    if readback.get("status") != "draft" or readback.get("slug") != pkg.slug:
        raise RuntimeError(
            f"unexpected readback: id={readback.get('id')} "
            f"status={readback.get('status')!r} slug={readback.get('slug')!r}"
        )
    log_line(
        pkg,
        "created guarded WP draft "
        f"id={readback.get('id')} status={readback.get('status')} slug={readback.get('slug')} "
        f"link={readback.get('link')}",
    )
    log_line(pkg, f"edit URL: {cfg.base_url}/wp-admin/post.php?post={readback.get('id')}&action=edit")
    return {
        "id": readback.get("id"),
        "status": readback.get("status"),
        "slug": readback.get("slug"),
        "link": readback.get("link"),
        "edit_url": f"{cfg.base_url}/wp-admin/post.php?post={readback.get('id')}&action=edit",
        "featured_media": readback.get("featured_media"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_md", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate slug availability and payload shape without WordPress writes (default).",
    )
    mode.add_argument(
        "--execute",
        action="store_true",
        help="Upload media and create a new WordPress draft after slug checks.",
    )
    args = parser.parse_args()
    try:
        result = create_local_draft(args.post_md, dry_run=not args.execute)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
