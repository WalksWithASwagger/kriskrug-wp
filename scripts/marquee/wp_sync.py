"""WordPress REST sync for marquee boards (Tier 3).

Pushes boards from marquee.json into the `marquee_board` CPT. Mirrors the proven safety model
from scripts/notion-to-wp (post-2026-05-15 incident): app-password Basic auth, slug-based
idempotency, CREATE-by-default, a title-similarity guard on --update, and post-write readback.

Auth comes from scripts/notion-to-wp/.env (WP_BASE_URL / WP_USER / WP_APP_PASSWORD) or the
environment — no Notion token required. Live writes need credentials AND the caller passing
execute=True; everything else is a dry run.
"""
from __future__ import annotations
import base64
import json
import sys
from pathlib import Path

from marquee_lib import ROOT, slugify
from render import post_content

# Reuse the pure title-similarity guard from the Notion connector (difflib only, no heavy deps).
sys.path.insert(0, str(ROOT / "scripts" / "notion-to-wp"))
from update_safety import title_similarity, TITLE_SIMILARITY_UPDATE_THRESHOLD  # noqa: E402

POST_TYPE = "marquee_board"
ENV_PATH = ROOT / "scripts" / "notion-to-wp" / ".env"
DEFAULT_BASE = "https://kriskrug.co"

META = {
    "lines": "_kk_mb_lines", "week": "_kk_mb_week", "skin": "_kk_mb_skin",
    "after": "_kk_mb_after", "source": "_kk_mb_source", "tags": "_kk_mb_tags",
}


def load_wp_credentials() -> dict:
    """WP creds from .env (simple parser, no python-dotenv dependency) with os.environ fallback."""
    import os
    vals = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            vals[k.strip()] = v.strip().strip('"').strip("'")
    get = lambda k, d=None: vals.get(k) or os.environ.get(k) or d  # noqa: E731
    return {
        "base": (get("WP_BASE_URL", DEFAULT_BASE) or DEFAULT_BASE).rstrip("/"),
        "user": get("WP_USER"),
        "app_password": (get("WP_APP_PASSWORD") or "").replace(" ", "") or None,
    }


class MarqueeWP:
    """Minimal REST client scoped to the marquee_board CPT + media (same auth as wp_client.py)."""

    def __init__(self, base: str, user: str, app_password: str):
        import requests
        self.base = base.rstrip("/")
        self.s = requests.Session()
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.s.headers.update({"Authorization": f"Basic {token}"})

    def find_by_slug(self, slug: str):
        r = self.s.get(f"{self.base}/wp-json/wp/v2/{POST_TYPE}",
                       params={"slug": slug, "status": "any", "per_page": 5, "context": "edit"}, timeout=30)
        if r.status_code != 200:
            return None
        hits = r.json()
        return hits[0]["id"] if isinstance(hits, list) and len(hits) == 1 else None

    def get(self, post_id: int) -> dict:
        r = self.s.get(f"{self.base}/wp-json/wp/v2/{POST_TYPE}/{post_id}?context=edit", timeout=30)
        r.raise_for_status()
        return r.json()

    def create(self, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/{POST_TYPE}", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()

    def update(self, post_id: int, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/{POST_TYPE}/{post_id}", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()

    def upload_media(self, path: Path, alt: str, mime: str = "image/png") -> dict:
        data = Path(path).read_bytes()
        r = self.s.post(f"{self.base}/wp-json/wp/v2/media",
                        headers={"Content-Disposition": f'attachment; filename="{Path(path).name}"',
                                 "Content-Type": mime}, data=data, timeout=120)
        r.raise_for_status()
        media = r.json()
        if alt:
            self.s.post(f"{self.base}/wp-json/wp/v2/media/{media['id']}",
                        json={"alt_text": alt}, timeout=30).raise_for_status()
        return media


def build_payload(board: dict) -> dict:
    """Map a marquee.json board to a marquee_board REST payload."""
    phrase = " ".join(board["board"])
    seo = board.get("seo", {})
    return {
        "title": seo.get("title") or phrase,
        "slug": seo.get("slug") or slugify(phrase),
        "status": "publish" if board.get("status") == "live" else "publish",
        "excerpt": board.get("dek", ""),
        "content": post_content(board),
        "meta": {
            META["lines"]: json.dumps(board["board"], ensure_ascii=False),
            META["week"]: board.get("week", ""),
            META["skin"]: board.get("skin", "led"),
            META["after"]: board.get("after", ""),
            META["source"]: json.dumps(board.get("source", {}), ensure_ascii=False),
            META["tags"]: ", ".join(board.get("tags", [])),
        },
    }


def sync_board(wp, board: dict, og_png: Path | None, *, execute: bool, allow_update: bool, log=print) -> dict:
    """Create (default) or update one board. Returns an outcome dict. No writes unless execute."""
    payload = build_payload(board)
    slug = payload["slug"]
    out = {"slug": slug, "status": "planned"}

    if not execute:
        out["preview"] = {"title": payload["title"], "slug": slug,
                          "content_chars": len(payload["content"]), "og": bool(og_png)}
        log(f"  [dry-run] {payload['title']}  (slug={slug}, og={'yes' if og_png else 'no'})")
        return out

    existing = wp.find_by_slug(slug)
    if existing is None:
        # Featured image first so the create can reference it.
        if og_png and Path(og_png).exists():
            media = wp.upload_media(Path(og_png), alt=f'Marquee board: {" ".join(board["board"])}')
            payload["featured_media"] = media["id"]
        res = wp.create(payload)
        verify = wp.get(res["id"])
        ok = verify.get("slug") == slug
        out.update(status="created" if ok else "failed", id=res["id"], verified=ok)
        log(f"  CREATED {res['id']} — {slug} (verified={ok})")
        return out

    # Existing slug: never blind-overwrite.
    if not allow_update:
        out["status"] = "skipped-exists"
        log(f"  SKIP {slug}: exists (pass --update to modify)")
        return out
    cur = wp.get(existing)
    cur_title = (cur.get("title") or {}).get("raw", "")
    sim = title_similarity(payload["title"], cur_title)
    if sim < TITLE_SIMILARITY_UPDATE_THRESHOLD:
        out.update(status="aborted-title-drift", similarity=round(sim, 2))
        log(f"  ABORT {slug}: title drift {sim:.2f} < {TITLE_SIMILARITY_UPDATE_THRESHOLD}")
        return out
    if og_png and Path(og_png).exists():
        media = wp.upload_media(Path(og_png), alt=f'Marquee board: {" ".join(board["board"])}')
        payload["featured_media"] = media["id"]
    res = wp.update(existing, payload)
    verify = wp.get(res["id"])
    ok = verify.get("slug") == slug
    out.update(status="updated" if ok else "failed", id=res["id"], verified=ok)
    log(f"  UPDATED {res['id']} — {slug} (verified={ok})")
    return out
