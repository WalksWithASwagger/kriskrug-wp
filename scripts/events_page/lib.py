"""Shared helpers for the /events page catalog → render → media pipeline."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
DEFAULT_KK_KB = Path("/Users/kk/Code/kk-kb")
CATALOG_PATH = HERE / "events-catalog.yaml"
MEETUP_EDITIONS_PATH = HERE / "meetup-editions.yaml"
SHELL_PATH = HERE / "shell-events-2250.html"
OUT_DIR = HERE / "out"
ENV_PATH = REPO_ROOT / "scripts" / "notion-to-wp" / ".env"
DEFAULT_WP_BASE = "https://kriskrug.co"

DYNAMIC_START = "<!-- EVENTS_DYNAMIC_START -->"
DYNAMIC_END = "<!-- EVENTS_DYNAMIC_END -->"


def load_dotenv_vals(path: Path = ENV_PATH) -> dict[str, str]:
    vals: dict[str, str] = {}
    if not path.exists():
        return vals
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        vals[key.strip()] = value.strip().strip('"').strip("'")
    return vals


def load_wp_credentials() -> dict[str, str | None]:
    file_vals = load_dotenv_vals()

    def get(key: str, default: str | None = None) -> str | None:
        return os.environ.get(key) or file_vals.get(key) or default

    password = get("WP_APP_PASSWORD") or get("WP_API_PASSWORD")
    if password:
        password = password.replace(" ", "")
    return {
        "base": (get("WP_BASE_URL", DEFAULT_WP_BASE) or DEFAULT_WP_BASE).rstrip("/"),
        "user": get("WP_USER") or get("WP_API_USERNAME"),
        "app_password": password,
    }


def resolve_path_roots(catalog: dict[str, Any]) -> dict[str, Path]:
    roots = catalog.get("path_roots") or {}
    kk_kb = Path(os.environ.get("KK_KB_ROOT") or roots.get("kk_kb") or DEFAULT_KK_KB)
    repo = Path(roots.get("repo") or REPO_ROOT)
    return {"kk_kb": kk_kb.expanduser().resolve(), "repo": repo.expanduser().resolve()}


def resolve_image_path(
    image: dict[str, Any] | None, roots: dict[str, Path]
) -> Path | None:
    if not image:
        return None
    raw = image.get("path")
    if not raw:
        return None
    text = str(raw)
    if text.startswith("kk_kb:"):
        return (roots["kk_kb"] / text[len("kk_kb:") :]).resolve()
    if text.startswith("repo:"):
        return (roots["repo"] / text[len("repo:") :]).resolve()
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = (HERE / path).resolve()
    return path


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_yaml(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def _norm_event(raw: dict[str, Any]) -> dict[str, Any]:
    event = dict(raw)
    event.setdefault("status", "confirmed")
    event.setdefault("kind", "one-off")
    event.setdefault("bucket_hint", "past")
    event.setdefault("tags", [])
    image = event.get("image") or {}
    if not isinstance(image, dict):
        image = {"path": image}
    event["image"] = image
    return event


def _edition_to_event(raw: dict[str, Any]) -> dict[str, Any] | None:
    """Normalize a harvest meetup-editions.yaml row (or catalog-shaped meetup)."""
    if raw.get("id") and (raw.get("kind") or raw.get("end") or raw.get("image")):
        return _norm_event(raw)

    edition = raw.get("edition")
    if edition is None:
        return None
    try:
        edition_i = int(edition)
    except (TypeError, ValueError):
        return None

    date = raw.get("date")
    end = raw.get("end")
    if not end and date:
        end = f"{date}T22:00:00-07:00"

    image: dict[str, Any] = {}
    if isinstance(raw.get("image"), dict):
        image = dict(raw["image"])
    else:
        hero = raw.get("hero_image_kk_kb") or raw.get("hero_image")
        if hero:
            path = str(hero)
            if not path.startswith(("kk_kb:", "repo:", "/")):
                path = f"kk_kb:{path}"
            image = {"path": path}

    photographer = raw.get("photographer_credit") or raw.get("photographer")
    if photographer:
        image["photographer"] = photographer
    if image and not image.get("alt"):
        image["alt"] = raw.get("title") or f"Vancouver AI Community Meetup #{edition_i}"

    url = raw.get("url") or raw.get("luma_url") or "https://lu.ma/vancouver-ai"
    confidence = (raw.get("date_confidence") or "").lower()
    status = raw.get("status") or (
        "scaffold" if confidence in {"approximate", "soft"} else "confirmed"
    )

    return _norm_event(
        {
            "id": raw.get("id") or f"van-ai-meetup-{edition_i:02d}",
            "title": raw.get("title") or f"Vancouver AI Community Meetup #{edition_i}",
            "date": date,
            "end": end,
            "bucket_hint": raw.get("bucket_hint") or "past",
            "kind": "meetup",
            "edition": edition_i,
            "role": raw.get("role") or "Host & curator",
            "url": url,
            "image": image,
            "blurb": raw.get("blurb") or raw.get("notes") or "",
            "label": raw.get("label") or raw.get("notes") or "",
            "tags": raw.get("tags") or ["Meetup", "Vancouver"],
            "status": status,
            "cta_past": raw.get("cta_past") or "Recap / Luma",
            "date_confidence": raw.get("date_confidence"),
        }
    )


def merge_meetup_editions(
    catalog_events: list[dict[str, Any]], editions_doc: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Import harvest meetup-editions.yaml into the catalog (by id / edition)."""
    if not editions_doc:
        return catalog_events

    editions = editions_doc.get("editions") or editions_doc.get("events") or []
    by_id = {e["id"]: _norm_event(e) for e in catalog_events if e.get("id")}

    for raw in editions:
        if not isinstance(raw, dict):
            continue
        event = _edition_to_event(raw)
        if not event:
            continue
        eid = event["id"]
        if eid in by_id:
            merged = dict(by_id[eid])
            for key, value in event.items():
                if value in (None, "", [], {}):
                    continue
                if key == "image":
                    img = dict(merged.get("image") or {})
                    for k, v in value.items():
                        if v not in (None, ""):
                            img[k] = v
                    merged["image"] = img
                else:
                    merged[key] = value
            by_id[eid] = merged
        else:
            by_id[eid] = event

    return list(by_id.values())


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    doc = load_yaml(path)
    if not doc or not isinstance(doc, dict):
        raise SystemExit(f"Catalog missing or invalid: {path}")
    events = [_norm_event(e) for e in (doc.get("events") or [])]
    harvest = load_yaml(MEETUP_EDITIONS_PATH)
    if harvest:
        events = merge_meetup_editions(events, harvest)
        doc["_harvest_merged"] = True
    else:
        doc["_harvest_merged"] = False
    doc["events"] = events
    return doc


def html_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def slugish(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "event"


def guess_mime(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")
