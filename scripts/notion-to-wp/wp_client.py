from __future__ import annotations

import base64
from pathlib import Path

import requests

from notion_client import slugify


class WordPress:
    def __init__(self, base_url: str, user: str, app_password: str):
        self.base = base_url.rstrip("/")
        self.s = requests.Session()
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.s.headers.update({"Authorization": f"Basic {token}"})

    def upload_media_file(self, path: Path, mime: str = "image/jpeg") -> dict:
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
            return hits[0]["id"]
        return None

    def get_post(self, post_id: int) -> dict:
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/posts/{post_id}?context=edit",
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def create_post(self, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()

    def update_post(self, post_id: int, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts/{post_id}", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
