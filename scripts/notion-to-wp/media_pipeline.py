from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

import requests

from content_derivation import _plain_text


def collect_image_blocks(blocks: list[dict]) -> list[dict]:
    out: list[dict] = []
    for b in blocks:
        if b.get("type") == "image":
            out.append(b)
        children = b.get("_children")
        if children:
            out.extend(collect_image_blocks(children))
    return out


def flatten_blocks(blocks: list[dict]) -> list[dict]:
    out: list[dict] = []
    for b in blocks:
        out.append(b)
        children = b.get("_children")
        if children:
            out.extend(flatten_blocks(children))
    return out


def auto_alt(blocks: list[dict], image_block: dict, fallback_topic: str) -> str:
    try:
        idx = blocks.index(image_block)
    except ValueError:
        return fallback_topic

    nearest_heading = ""
    for i in range(idx - 1, -1, -1):
        if blocks[i].get("type", "").startswith("heading_"):
            nearest_heading = _plain_text(blocks[i]).strip()
            break

    def first_sentence(txt: str) -> str:
        return re.split(r"(?<=[.!?])\s+", txt.strip())[0][:140].strip() if txt.strip() else ""

    context = ""
    for i in range(idx - 1, max(-1, idx - 4), -1):
        if blocks[i].get("type") == "paragraph":
            t = _plain_text(blocks[i])
            if t.strip():
                context = first_sentence(t)
                break
    if not context:
        for i in range(idx + 1, min(len(blocks), idx + 4)):
            if blocks[i].get("type") == "paragraph":
                t = _plain_text(blocks[i])
                if t.strip():
                    context = first_sentence(t)
                    break

    parts = [p for p in [nearest_heading, context] if p]
    if not parts:
        return fallback_topic
    return " — ".join(parts)[:200]


def image_filename(block: dict, idx: int, slug_hint: str) -> str:
    src_obj = block["image"].get("file") or block["image"].get("external") or {}
    url = src_obj.get("url", "")
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    return f"{idx:02d}-{slug_hint}{ext}"


def download_image(url: str, dest: Path) -> int:
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(dest, "wb") as f:
        for chunk in r.iter_content(64 * 1024):
            f.write(chunk)
            total += len(chunk)
    return total
