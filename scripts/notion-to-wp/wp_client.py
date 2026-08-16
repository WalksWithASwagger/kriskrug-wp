from __future__ import annotations

import base64
import os
from pathlib import Path

import requests

from notion_client import slugify


DRY_RUN_ENV = "DRY_RUN"
DRY_RUN_FALSEY = {"", "0", "false", "no", "off"}
WRITE_HTTP_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class DryRunWriteBlocked(RuntimeError):
    pass


class SlugVerificationFailed(RuntimeError):
    pass


def dry_run_active() -> bool:
    return os.environ.get(DRY_RUN_ENV, "").strip().lower() not in DRY_RUN_FALSEY


def _refuse_write_under_dry_run(method: str) -> None:
    """Choke-point backstop for the 2026-05-15 overwrite: callers own their own
    dry-run gate, and this catches the caller that forgets it."""
    if dry_run_active():
        raise DryRunWriteBlocked(
            f"WordPress.{method} refused: {DRY_RUN_ENV}="
            f"{os.environ.get(DRY_RUN_ENV, '')!r} blocks every WordPress write. "
            f"Unset {DRY_RUN_ENV} to allow live writes."
        )


class _DryRunSession(requests.Session):
    def request(self, method, url, *args, **kwargs):
        if method.upper() in WRITE_HTTP_METHODS:
            _refuse_write_under_dry_run(f"HTTP {method.upper()}")
        return super().request(method, url, *args, **kwargs)


class WordPress:
    def __init__(self, base_url: str, user: str, app_password: str):
        self.base = base_url.rstrip("/")
        self.s = _DryRunSession()
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.s.headers.update({"Authorization": f"Basic {token}"})

    def upload_media_file(self, path: Path, mime: str = "image/jpeg") -> dict:
        _refuse_write_under_dry_run("upload_media_file")
        with open(path, "rb") as f:
            data = f.read()
        r = self.s.post(
            f"{self.base}/wp-json/wp/v2/media",
            headers={
                "Content-Disposition": f'attachment; filename="{path.name}"',
                "Content-Type": mime,
            },
            data=data,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def update_media(self, media_id: int, payload: dict) -> dict:
        _refuse_write_under_dry_run("update_media")
        r = self.s.post(
            f"{self.base}/wp-json/wp/v2/media/{media_id}",
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def get_media(self, media_id: int, *, context: str = "view") -> dict:
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/media/{media_id}",
            params={"context": context},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def upload_media(
        self,
        path: Path,
        alt: str,
        mime: str = "image/jpeg",
        *,
        title: str = "",
        caption: str = "",
        description: str = "",
    ) -> dict:
        media = self.upload_media_file(path, mime=mime)
        metadata = {
            key: value
            for key, value in {
                "alt_text": alt,
                "title": title,
                "caption": caption,
                "description": description,
            }.items()
            if value
        }
        if metadata:
            return self.update_media(media["id"], metadata)
        return media

    def ensure_term(self, taxonomy: str, name: str) -> int:
        _refuse_write_under_dry_run("ensure_term")
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/{taxonomy}",
            params={"search": name, "per_page": 50},
            timeout=30,
        )
        r.raise_for_status()
        for t in r.json():
            if t.get("name", "").lower() == name.lower() or t.get("slug", "") == slugify(name):
                return t["id"]
        r2 = self.s.post(
            f"{self.base}/wp-json/wp/v2/{taxonomy}",
            json={"name": name, "slug": slugify(name)},
            timeout=30,
        )
        r2.raise_for_status()
        return r2.json()["id"]

    def find_post_by_slug(self, slug: str) -> int | None:
        """Idempotency by slug; returns an ID only for exactly one post match."""
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/posts",
            params={"slug": slug, "status": "any", "per_page": 5, "context": "edit"},
            timeout=30,
        )
        if r.status_code != 200:
            return None
        hits = r.json()
        if isinstance(hits, list) and len(hits) == 1:
            hit = hits[0]
            if isinstance(hit, dict) and hit.get("slug") == slug:
                return hit.get("id")
        return None

    def get_post(self, post_id: int) -> dict:
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/posts/{post_id}?context=edit",
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def create_post(self, payload: dict) -> dict:
        _refuse_write_under_dry_run("create_post")
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()

    def update_post(
        self, post_id: int, payload: dict, *, expected_slug: str
    ) -> dict:
        _refuse_write_under_dry_run("update_post")
        if self.find_post_by_slug(expected_slug) != post_id:
            raise SlugVerificationFailed(
                f"WordPress.update_post refused: slug {expected_slug!r} did not "
                f"resolve uniquely to post id {post_id}."
            )
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts/{post_id}", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
