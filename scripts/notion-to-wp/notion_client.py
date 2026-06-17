from __future__ import annotations

import re
import sys
import time

import requests

from connector_config import NOTION_API, NOTION_VERSION


class Notion:
    def __init__(self, token: str):
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Accept": "application/json",
        })

    def get(self, path: str) -> dict:
        for attempt in range(4):
            r = self.s.get(f"{NOTION_API}{path}", timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
        r.raise_for_status()

    def page(self, page_id: str) -> dict:
        return self.get(f"/pages/{page_id}")

    def block_children(self, block_id: str, depth: int = 0, max_depth: int = 3) -> list[dict]:
        """Fetch direct children, then attach nested children under `_children`."""
        all_blocks: list[dict] = []
        cursor = None
        while True:
            qs = f"?start_cursor={cursor}&page_size=100" if cursor else "?page_size=100"
            data = self.get(f"/blocks/{block_id}/children{qs}")
            all_blocks.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        if depth < max_depth:
            for b in all_blocks:
                if b.get("has_children"):
                    b["_children"] = self.block_children(b["id"], depth=depth + 1, max_depth=max_depth)
        return all_blocks


def parse_page_id(url_or_id: str) -> str:
    """Accept https://notion.so/Title-<32hex> or bare UUID or 32hex; return UUID with dashes."""
    s = url_or_id.strip()
    m = re.search(r"([0-9a-fA-F]{32})", s.replace("-", ""))
    if not m:
        m2 = re.search(r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", s)
        if not m2:
            sys.exit(f"Could not parse Notion page ID from: {url_or_id}")
        return m2.group(1)
    h = m.group(1)
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def read_prop_title(page: dict) -> str:
    props = page.get("properties", {})
    for v in props.values():
        if v.get("type") == "title":
            return "".join(rt.get("plain_text", "") for rt in v.get("title", []))
    return ""


def read_prop(page: dict, name: str, default=None):
    p = page.get("properties", {}).get(name)
    if not p:
        return default
    t = p.get("type")
    if t == "rich_text":
        return "".join(rt.get("plain_text", "") for rt in p.get("rich_text", []))
    if t == "select":
        sel = p.get("select")
        return sel.get("name") if sel else default
    if t == "multi_select":
        return [s.get("name") for s in p.get("multi_select", [])]
    if t == "date":
        d = p.get("date") or {}
        return d.get("start")
    if t == "checkbox":
        return p.get("checkbox", False)
    if t == "status":
        st = p.get("status") or {}
        return st.get("name")
    if t == "people":
        return [u.get("id") for u in p.get("people", [])]
    if t == "url":
        return p.get("url")
    if t == "number":
        return p.get("number")
    return default


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")
