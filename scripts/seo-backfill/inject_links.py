#!/usr/bin/env python3
"""Spoke-injection: add contextual internal links + footer collection block to posts.

SAFETY MODEL (mirrors backfill_meta.py):
- Default is dry-run. Live writes require --execute.
- Per-post: assert_minimal_diff runs in BOTH dry-run and execute modes.
  Any unexplained body change (the 2026-05-15 incident class) raises before
  a write is ever attempted.
- Live write payload = {"content": <new_content>} — only one key, only
  "content". No title, slug, date, status, or meta is ever included.
- Post-write readback verifies footer sentinel + expected anchors present,
  slug and title unchanged.
- Prior content is saved to a rollback sidecar JSON before every live write.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "notion-to-wp"))

from kk_notion_to_wp import WordPress, load_config, title_similarity  # noqa: E402
from linkinject_lib import (  # noqa: E402
    FOOTER_SENTINEL,
    PILLAR_BY_CATEGORY,
    assert_minimal_diff,
    build_content_payload,
    has_footer,
    plan_links_for_post,
    rank_siblings,
)

LIST_FIELDS = "id,slug,title,link,date,status,categories,content"
READBACK_FIELDS = "id,slug,title,content"
TITLE_DRIFT_THRESHOLD = 0.9

REPORTS_DIR = REPO_ROOT / "docs" / "current-state" / "reports"


def log(msg: str) -> None:
    print(msg, flush=True)


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def fetch_candidates(
    wp: WordPress,
    kind: str,
    since: str | None,
    category: int | None,
) -> list[dict]:
    endpoint = "posts" if kind == "post" else "pages"
    page, items = 1, []
    while True:
        params: dict = {
            "status": "publish",
            "per_page": 100,
            "page": page,
            "context": "edit",
            "_fields": LIST_FIELDS,
            "orderby": "date",
            "order": "desc",
        }
        if since:
            params["after"] = f"{since}T00:00:00"
        if category:
            params["categories"] = category
        r = wp.s.get(
            f"{wp.base}/wp-json/wp/v2/{endpoint}", params=params, timeout=60
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        if page >= int(r.headers.get("X-WP-TotalPages", "1")):
            break
        page += 1
    return items


def fetch_post(wp: WordPress, post_id: int) -> dict:
    r = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit", "_fields": LIST_FIELDS},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def readback(wp: WordPress, post_id: int) -> dict:
    r = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit", "_fields": READBACK_FIELDS},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def get_url_200(wp: WordPress, url: str) -> bool:
    try:
        r = wp.s.get(url, timeout=20, allow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Sibling cache
# ---------------------------------------------------------------------------

_sibling_cache: dict[int, list[dict]] = {}


def get_siblings(wp: WordPress, cat_id: int, limit: int = 50) -> list[dict]:
    if cat_id in _sibling_cache:
        return _sibling_cache[cat_id]
    params = {
        "status": "publish",
        "per_page": limit,
        "context": "edit",
        "_fields": LIST_FIELDS,
        "categories": cat_id,
        "orderby": "date",
        "order": "desc",
    }
    r = wp.s.get(f"{wp.base}/wp-json/wp/v2/posts", params=params, timeout=60)
    r.raise_for_status()
    result = r.json()
    _sibling_cache[cat_id] = result
    return result


# ---------------------------------------------------------------------------
# Per-post processing
# ---------------------------------------------------------------------------

def _raw_content(item: dict) -> str:
    """Extract raw (pre-render) content string from a context=edit WP item."""
    c = item.get("content") or {}
    if isinstance(c, dict):
        return c.get("raw") or c.get("rendered") or ""
    return str(c or "")


def _item_title(item: dict) -> str:
    t = item.get("title") or {}
    if isinstance(t, dict):
        return t.get("raw") or t.get("rendered") or ""
    return str(t or "")


def _primary_cat(item: dict) -> int | None:
    cats = item.get("categories") or []
    if cats:
        return int(cats[0])
    return None


def apply_one(
    wp: WordPress,
    item: dict,
    wave: str,
    *,
    live: bool,
    rollback_path: Path,
) -> dict:
    """Plan and optionally apply link injection for one post.

    Returns an outcome dict suitable for the report writer."""
    pid = int(item["id"])
    slug = item.get("slug", "")
    link = item.get("link", "")
    out: dict = {
        "id": pid,
        "slug": slug,
        "status": "skipped",
        "flags": [],
        "reason": "",
        "anchors": [],
        "footer": None,
        "total_internal_after": 0,
    }

    content_raw = _raw_content(item)
    if not content_raw.strip():
        out["reason"] = "empty content"
        return out

    # Pillar lookup
    primary_cat = _primary_cat(item)
    pillar = PILLAR_BY_CATEGORY.get(primary_cat) if primary_cat else None

    # Sibling fetch + rank
    sibling_candidates: list[dict] = []
    if pillar and primary_cat:
        sibling_candidates = get_siblings(wp, primary_cat)
    ranked_siblings = rank_siblings(item, sibling_candidates, n=5)

    # Plan
    try:
        new_content, applied, footer_block, flags = plan_links_for_post(
            content_raw, link, pillar, ranked_siblings, wave
        )
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"plan_links_for_post: {exc}"
        return out

    out["flags"] = flags

    if "already-done" in flags:
        out["reason"] = "already-done (footer present)"
        return out

    if new_content == content_raw and not applied and footer_block is None:
        out["reason"] = "no changes planned"
        return out

    # Minimal-diff assertion — runs in BOTH dry-run and execute.
    try:
        assert_minimal_diff(content_raw, new_content, applied, footer_block)
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"assert_minimal_diff: {exc}"
        return out

    # Count internal links in new content.
    import re as _re
    total_internal = len(_re.findall(r'href="https://kriskrug\.co/', new_content, _re.IGNORECASE))
    out["total_internal_after"] = total_internal
    out["anchors"] = [{"text": a["text"], "url": a["url"]} for a in applied]
    out["footer"] = footer_block

    if not live:
        out["status"] = "planned"
        return out

    # --- live path ---

    # Identity readback before write.
    try:
        fresh = readback(wp, pid)
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"pre-write readback failed: {exc}"
        return out

    if int(fresh.get("id", -1)) != pid:
        out["status"] = "failed"
        out["reason"] = "id mismatch on pre-write readback"
        return out

    fresh_title = _item_title(fresh)
    list_title = _item_title(item)
    sim = title_similarity(list_title, fresh_title)
    if sim < TITLE_DRIFT_THRESHOLD:
        out["status"] = "failed"
        out["reason"] = f"title drift sim={sim:.2f} (<{TITLE_DRIFT_THRESHOLD})"
        return out

    # TOCTOU: re-derive against a fresh content.raw.
    fresh_content_raw = _raw_content(fresh)
    try:
        new_content2, applied2, footer_block2, flags2 = plan_links_for_post(
            fresh_content_raw, link, pillar, ranked_siblings, wave
        )
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"TOCTOU re-plan: {exc}"
        return out

    if "already-done" in flags2:
        out["status"] = "skipped"
        out["reason"] = "already-done (footer appeared between enumeration and write)"
        return out

    # Minimal-diff on the fresh content too.
    try:
        assert_minimal_diff(fresh_content_raw, new_content2, applied2, footer_block2)
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"TOCTOU assert_minimal_diff: {exc}"
        return out

    # Save prior content to rollback sidecar.
    _append_rollback(rollback_path, pid, slug, fresh_content_raw)

    # Build payload — single key guard.
    try:
        payload = build_content_payload(new_content2)
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"build_content_payload: {exc}"
        return out

    # Write.
    try:
        wp.s.post(
            f"{wp.base}/wp-json/wp/v2/posts/{pid}", json=payload, timeout=60
        ).raise_for_status()
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"POST failed: {exc}"
        return out

    # Post-write readback verification.
    try:
        verify = readback(wp, pid)
    except Exception as exc:
        out["status"] = "failed"
        out["reason"] = f"post-write readback failed: {exc}"
        return out

    verify_content = _raw_content(verify)
    verify_slug = verify.get("slug")
    verify_title = _item_title(verify)

    issues = []
    if footer_block2 and FOOTER_SENTINEL not in verify_content:
        issues.append("footer-sentinel-missing")
    for anchor in applied2:
        if anchor["url"] not in verify_content:
            issues.append(f"anchor-url-missing:{anchor['url'][:40]}")
    if verify_slug != fresh.get("slug"):
        issues.append(f"slug-changed:{verify_slug}")
    if title_similarity(verify_title, fresh_title) < TITLE_DRIFT_THRESHOLD:
        issues.append(f"title-drifted")

    if issues:
        out["status"] = "failed"
        out["reason"] = f"post-write verify: {'; '.join(issues)}"
        return out

    # GET link 200.
    if link and not get_url_200(wp, link):
        out["flags"] = list(out["flags"]) + ["url-get-non-200"]

    out["status"] = "written"
    out["anchors"] = [{"text": a["text"], "url": a["url"]} for a in applied2]
    out["footer"] = footer_block2
    return out


# ---------------------------------------------------------------------------
# Rollback sidecar
# ---------------------------------------------------------------------------

def _append_rollback(path: Path, pid: int, slug: str, prior_content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"items": []}
    data["items"].append({
        "id": pid,
        "slug": slug,
        "prior_content": prior_content,
        "saved_at": _utcnow().isoformat(timespec="seconds"),
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(
    path: Path,
    *,
    mode: str,
    wave: str,
    filters: str,
    outcomes: list[dict],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = {s: sum(1 for o in outcomes if o["status"] == s)
         for s in ("written", "planned", "skipped", "failed")}

    lines = [
        f"# Internal-link injection report — {mode}",
        "",
        f"- Generated: {_utcnow().isoformat(timespec='seconds').replace('+00:00', '')}Z",
        f"- Mode: **{mode}** · wave: {wave}",
        f"- Filters: {filters}",
        "",
        "## Counts",
        f"- candidates: {len(outcomes)}",
        f"- **written: {n['written']}**"
        + ("  (dry-run — nothing written)" if mode == "dry-run" else ""),
        f"- planned (dry-run): {n['planned']}",
        f"- skipped: {n['skipped']}",
        f"- **failed: {n['failed']}**",
        "",
        "## Per-post",
        "",
        "| id | slug | status | anchors | internal-links-after | flags | reason |",
        "|---|---|---|---|---|---|---|",
    ]
    for o in outcomes:
        if o["status"] == "skipped" and not o.get("flags"):
            continue
        anchor_summary = "; ".join(
            f"{a['text']} -> {a['url'][:30]}" for a in (o.get("anchors") or [])
        )
        lines.append(
            f"| {o['id']} | {o['slug'][:40]} | {o['status']} | "
            f"{anchor_summary[:60]} | {o.get('total_internal_after', '')} | "
            f"{','.join(o.get('flags') or [])} | {o.get('reason', '')} |"
        )

    # Footer previews for review
    with_footer = [o for o in outcomes if o.get("footer") and o["status"] in ("written", "planned")]
    if with_footer:
        lines += ["", "## Footer blocks (review)", ""]
        for o in with_footer:
            lines.append(f"### {o['id']} — {o['slug']}")
            lines.append("")
            lines.append("```")
            lines.append(o["footer"])
            lines.append("```")
            lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Inject internal spoke links into posts (default: dry-run)"
    )
    p.add_argument(
        "--execute", action="store_true",
        help="perform live writes (default is dry-run)"
    )
    p.add_argument("--kind", choices=("post", "page"), default="post")
    p.add_argument("--since", help="only items published after YYYY-MM-DD")
    p.add_argument("--ids", help="comma-separated post IDs")
    p.add_argument("--category", type=int, help="filter by category term ID")
    p.add_argument("--limit", type=int, default=0, help="max items (0 = all)")
    p.add_argument("--wave", choices=("A", "B"), default="A")
    p.add_argument("--from-file", help="JSON file with {items:[{id,slug}]} (apply to listed posts)")
    p.add_argument("--report-dir", default="docs/current-state/reports")
    args = p.parse_args()

    mode = "live" if args.execute else "dry-run"

    cfg = load_config()
    if not cfg.has_wp_credentials:
        log("WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env")
        return 1
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

    ts = _utcnow().strftime("%Y%m%d-%H%M%SZ")
    report_path = REPO_ROOT / args.report_dir / f"link-inject-{ts}.md"
    rollback_path = REPO_ROOT / args.report_dir / f"link-inject-rollback-{ts}.json"

    # Build candidate list.
    if args.from_file:
        data = json.loads(Path(args.from_file).read_text(encoding="utf-8"))
        entries = data["items"] if isinstance(data, dict) and "items" in data else data
        candidates = []
        for entry in entries:
            pid = int(entry["id"])
            try:
                candidates.append(fetch_post(wp, pid))
            except Exception as exc:
                log(f"  WARN: id {pid} not fetchable: {exc}")
    elif args.ids:
        want = [int(x) for x in args.ids.split(",") if x.strip()]
        candidates = []
        for pid in want:
            try:
                candidates.append(fetch_post(wp, pid))
            except Exception as exc:
                log(f"  WARN: id {pid} not fetchable: {exc}")
    else:
        candidates = fetch_candidates(wp, args.kind, args.since, args.category)

    if args.limit:
        candidates = candidates[: args.limit]

    log(f"{mode} (wave={args.wave}): {len(candidates)} candidate {args.kind}s")

    outcomes: list[dict] = []
    for item in candidates:
        out = apply_one(wp, item, args.wave, live=args.execute, rollback_path=rollback_path)
        outcomes.append(out)
        if out["status"] in ("written", "planned"):
            flag_str = f"  [{','.join(out['flags'])}]" if out.get("flags") else ""
            log(f"  {out['status']:8} {out['id']} {out['slug'][:45]}{flag_str}")
        elif out["status"] == "failed":
            log(f"  FAILED   {out['id']} {out['slug'][:45]} -- {out['reason']}")

    filters = (
        f"wave={args.wave} limit={args.limit or 'all'} "
        f"since={args.since or '-'} "
        f"category={args.category or '-'} "
        f"ids={'yes' if args.ids else 'no'}"
    )
    write_report(report_path, mode=mode, wave=args.wave, filters=filters, outcomes=outcomes)

    n = {s: sum(1 for o in outcomes if o["status"] == s)
         for s in ("written", "planned", "skipped", "failed")}
    log("")
    log(
        f"SUMMARY [{mode}]: written={n['written']} planned={n['planned']} "
        f"skipped={n['skipped']} failed={n['failed']}"
    )
    log(f"report: {report_path.relative_to(REPO_ROOT)}")
    return 1 if n["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
