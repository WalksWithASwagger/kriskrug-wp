#!/usr/bin/env python3
"""Additive-only backfill of the three Jetpack SEO meta keys on kriskrug.co.

SAFETY MODEL (see docs/current-state/INCIDENT-2026-05-15-overwritten-post.md):
every live write is ONLY `{"meta": {<=3 allowlisted keys>}}` — no title, slug,
date, content, status, or taxonomy key is ever in the payload, so a write
cannot 404 a URL or blank a body. We only ever SET fields that are currently
EMPTY; we never overwrite. Default is dry-run; live requires --execute.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "notion-to-wp"))

from backfill_lib import (  # noqa: E402
    ALLOWED_META_KEYS,
    FIELD_TO_KEY,
    build_meta_payload,
    meta_value,
    meta_values_match,
    parse_approved_entry,
    plan_meta_for_item,
    reconcile_with_fresh_meta,
    title_text,
)
from kk_notion_to_wp import WordPress, load_config, title_similarity  # noqa: E402

LIST_FIELDS = "id,slug,title,link,date,status,meta,excerpt,content"
READBACK_FIELDS = "id,slug,title,meta"
TITLE_DRIFT_THRESHOLD = 0.9


def log(msg: str) -> None:
    print(msg, flush=True)


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def fetch_candidates(wp: WordPress, kind: str, since: str | None) -> list[dict]:
    endpoint = "posts" if kind == "post" else "pages"
    page, items = 1, []
    while True:
        params = {
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
        r = wp.s.get(f"{wp.base}/wp-json/wp/v2/{endpoint}", params=params, timeout=60)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        if page >= int(r.headers.get("X-WP-TotalPages", "1")):
            break
        page += 1
    return items


def readback(wp: WordPress, post_id: int) -> dict:
    r = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit", "_fields": READBACK_FIELDS},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def probe(wp: WordPress, probe_id: int) -> bool:
    """Non-mutating writability probe: write each currently-SET meta value back
    to itself and confirm readback equality. Proves Jetpack accepts the keys
    without changing any content. Skips keys that are empty on the probe post."""
    post = readback(wp, probe_id)
    meta = post.get("meta") or {}
    present = {k: meta[k] for k in ALLOWED_META_KEYS if isinstance(meta.get(k), str) and meta[k].strip()}
    if not present:
        log(f"  PROBE WARN: post {probe_id} has none of the 3 keys set — cannot prove writability here.")
        return False
    wp.s.post(
        f"{wp.base}/wp-json/wp/v2/posts/{probe_id}",
        json={"meta": present},
        timeout=60,
    ).raise_for_status()
    after = (readback(wp, probe_id).get("meta") or {})
    ok = all(after.get(k) == v for k, v in present.items())
    log(f"  PROBE {'PASS' if ok else 'FAIL'} on post {probe_id}: re-wrote+verified {list(present)} (no content changed)")
    return ok


def auto_probe_id(candidates: list[dict]) -> int | None:
    for item in candidates:
        meta = item.get("meta") or {}
        if all(isinstance(meta.get(k), str) and meta[k].strip() for k in ALLOWED_META_KEYS):
            return int(item["id"])
    return None


def apply_one(wp: WordPress, item: dict, kind: str, fields, *, live: bool) -> dict:
    """Returns an outcome dict. Live path is fully guarded (identity readback,
    title-drift check, re-check emptiness on fresh GET, meta-only write,
    post-write verification)."""
    pid = int(item["id"])
    out = {"id": pid, "slug": item.get("slug", ""), "status": "skipped", "written": [], "flags": [], "reason": ""}

    plan = plan_meta_for_item(item, kind, fields)
    out["flags"] = plan.flags
    if plan.is_empty:
        out["reason"] = plan.note or "nothing to fill"
        return out

    if not live:
        out["status"] = "planned"
        out["written"] = sorted(plan.planned)
        out["preview"] = {k: v for k, v in plan.planned.items()}
        return out

    # --- live path: re-verify identity on a fresh GET before writing ---
    fresh = readback(wp, pid)
    if int(fresh.get("id", -1)) != pid:
        out["status"] = "failed"; out["reason"] = "id mismatch on readback"; return out
    list_title = title_text(item)
    fresh_title = title_text(fresh)
    sim = title_similarity(list_title, fresh_title)
    if sim < TITLE_DRIFT_THRESHOLD:
        out["status"] = "failed"; out["reason"] = f"title drift sim={sim:.2f} (<{TITLE_DRIFT_THRESHOLD})"; return out

    # Re-gate emptiness against the FRESH meta (closes TOCTOU), but keep the
    # values derived from the ORIGINAL item — the readback omits excerpt/content,
    # so re-deriving from it would silently drop meta_desc/social. The post body
    # is stable between enumeration and write; only the meta emptiness can change.
    fresh_meta = fresh.get("meta") or {}
    planned = reconcile_with_fresh_meta(plan.planned, fresh_meta)
    if not planned:
        out["reason"] = "fields filled since enumeration"; return out

    payload = build_meta_payload(planned)  # raises if any key not allowlisted
    wp.s.post(f"{wp.base}/wp-json/wp/v2/posts/{pid}", json=payload, timeout=60).raise_for_status()

    # --- post-write verification ---
    verify = readback(wp, pid)
    vmeta = verify.get("meta") or {}
    mismatched = [k for k, v in planned.items() if not meta_values_match(v, vmeta.get(k))]
    slug_changed = verify.get("slug") != fresh.get("slug")
    title_changed = title_text(verify) != fresh_title
    if mismatched or slug_changed or title_changed:
        out["status"] = "failed"
        out["reason"] = f"readback mismatch keys={mismatched} slug_changed={slug_changed} title_changed={title_changed}"
        return out
    out["status"] = "written"
    out["written"] = sorted(planned)
    out["preview"] = planned
    return out


def apply_from_file_one(wp: WordPress, entry: dict, *, live: bool) -> dict:
    """Write KK-approved OVERWRITE values for one post. Unlike the additive path
    this MAY overwrite non-empty fields — but only the 3 allowlisted meta keys,
    only the exact approved values, and only after a slug-identity guard. Records
    prior values for rollback."""
    pid, slug, meta = parse_approved_entry(entry)  # raises on bad shape
    out = {"id": pid, "slug": slug, "status": "skipped", "written": [], "flags": [], "reason": "", "old": {}}

    fresh = readback(wp, pid)
    if int(fresh.get("id", -1)) != pid:
        out["status"] = "failed"; out["reason"] = "id mismatch on readback"; return out
    if fresh.get("slug") != slug:
        out["status"] = "failed"; out["reason"] = f"slug guard: file={slug!r} live={fresh.get('slug')!r}"; return out

    fresh_meta = fresh.get("meta") or {}
    out["old"] = {k: fresh_meta.get(k, "") for k in meta}  # capture prior values for rollback

    if not live:
        out["status"] = "planned"; out["written"] = sorted(meta); out["preview"] = meta; return out

    payload = build_meta_payload(meta)  # allowlist assert
    wp.s.post(f"{wp.base}/wp-json/wp/v2/posts/{pid}", json=payload, timeout=60).raise_for_status()

    verify = readback(wp, pid)
    vmeta = verify.get("meta") or {}
    mismatched = [k for k, v in meta.items() if not meta_values_match(v, vmeta.get(k))]
    if mismatched or verify.get("slug") != slug or title_text(verify) != title_text(fresh):
        out["status"] = "failed"; out["reason"] = f"readback mismatch keys={mismatched}"; return out
    out["status"] = "written"; out["written"] = sorted(meta); out["preview"] = meta
    return out


def run_from_file(wp: WordPress, path: Path, *, live: bool) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data["items"] if isinstance(data, dict) and "items" in data else data
    if isinstance(entries, dict):  # {"123": {...}} form
        entries = [{"id": int(k), **v} for k, v in entries.items()]
    outcomes = []
    for entry in entries:
        try:
            out = apply_from_file_one(wp, entry, live=live)
        except ValueError as e:
            out = {"id": entry.get("id"), "slug": entry.get("slug", ""), "status": "failed",
                   "written": [], "flags": [], "reason": f"validation: {e}", "old": {}}
        outcomes.append(out)
        if out["status"] in ("written", "planned"):
            log(f"  {out['status']:8} {out['id']} {out['slug'][:45]} -> {','.join(out['written'])}")
        elif out["status"] == "failed":
            log(f"  FAILED   {out.get('id')} {out.get('slug','')[:45]} -- {out['reason']}")
    return outcomes


def write_report(path: Path, *, mode, kind, fields, filters, probe_result, backup_note, outcomes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = {s: sum(1 for o in outcomes if o["status"] == s) for s in ("written", "planned", "skipped", "failed")}
    lines = [
        f"# SEO metadata backfill report — {mode}",
        "",
        f"- Generated: {_utcnow().isoformat(timespec='seconds').replace('+00:00','')}Z",
        f"- Mode: **{mode}** · kind: {kind} · fields: {','.join(fields)}",
        f"- Filters: {filters}",
        f"- Probe: {probe_result}",
        f"- Backup: {backup_note}",
        "",
        "## Counts",
        f"- candidates: {len(outcomes)}",
        f"- **written: {n['written']}**" + ("  (dry-run — nothing written)" if mode == "dry-run" else ""),
        f"- planned (dry-run): {n['planned']}",
        f"- skipped: {n['skipped']}",
        f"- **failed: {n['failed']}**",
        "",
        "## Per-item",
        "",
        "| id | slug | status | fields | flags | reason |",
        "|---|---|---|---|---|---|",
    ]
    for o in outcomes:
        if o["status"] == "skipped" and not o["flags"]:
            continue  # keep the table focused on actionable rows
        lines.append(
            f"| {o['id']} | {o['slug'][:40]} | {o['status']} | "
            f"{','.join(o.get('written') or [])} | {','.join(o.get('flags') or [])} | {o.get('reason','')} |"
        )
    low_conf = [o for o in outcomes if o.get("flags") and o["status"] in ("planned", "written")]
    if low_conf:
        lines += ["", "## Low-confidence / flagged (review or hand-edit)", ""]
        for o in low_conf:
            prev = o.get("preview", {})
            desc = prev.get("advanced_seo_description", "")
            lines.append(f"- **{o['id']}** {o['slug']} — flags: {', '.join(o['flags'])}" + (f" — desc: “{desc[:120]}”" if desc else ""))
    rollback = [o for o in outcomes if o.get("old") and o["status"] == "written"]
    if rollback:
        lines += ["", "## Prior values (rollback record — overwrite mode)", ""]
        for o in rollback:
            lines.append(f"- **{o['id']}** {o['slug']}:")
            for k, oldv in o["old"].items():
                lines.append(f"    - `{k}`: was “{(oldv or '∅empty')[:100]}”")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Additive-only SEO meta backfill (default: dry-run)")
    p.add_argument("--execute", action="store_true", help="perform live writes (default is dry-run)")
    p.add_argument("--kind", choices=("post", "page"), default="post")
    p.add_argument("--limit", type=int, default=0, help="max items to process (0 = all)")
    p.add_argument("--since", help="only items published after YYYY-MM-DD")
    p.add_argument("--ids", help="comma-separated post IDs (overrides ordering/filters)")
    p.add_argument("--order", choices=("recent", "oldest", "idlist"), default="recent")
    p.add_argument("--fields", default="seo_title,meta_desc,social",
                   help="which fields to backfill (subset of seo_title,meta_desc,social)")
    p.add_argument("--probe-id", type=int, help="post to probe writability on (auto-picked if omitted)")
    p.add_argument("--backup-dir", help="backup/YYYY-MM-DD set; checked for live runs")
    p.add_argument("--from-file", help="apply KK-approved OVERWRITE values from a JSON file (overwrite mode)")
    p.add_argument("--report-dir", default="docs/current-state/reports")
    args = p.parse_args()

    fields = tuple(f.strip() for f in args.fields.split(",") if f.strip() in FIELD_TO_KEY)
    if not fields:
        log("no valid --fields"); return 2
    mode = "live" if args.execute else "dry-run"

    cfg = load_config()
    if not cfg.has_wp_credentials:
        log("WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env"); return 1
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

    # --- OVERWRITE mode: apply KK-approved values from a reviewed file ---
    if args.from_file:
        path = Path(args.from_file)
        log(f"{mode} (from-file overwrite): {path}")
        outcomes = run_from_file(wp, path, live=args.execute)
        ts = _utcnow().strftime("%Y%m%d-%H%M%SZ")
        report = REPO_ROOT / args.report_dir / f"seo-overwrite-{ts}.md"
        write_report(report, mode=f"{mode} (overwrite from {path.name})", kind="post",
                     fields=("approved",), filters=f"from-file={path.name}",
                     probe_result="n/a", backup_note="overwrite — prior values recorded per-item for rollback",
                     outcomes=outcomes)
        n = {s: sum(1 for o in outcomes if o["status"] == s) for s in ("written", "planned", "skipped", "failed")}
        log("")
        log(f"SUMMARY [{mode} overwrite]: written={n['written']} planned={n['planned']} failed={n['failed']}")
        log(f"report: {report.relative_to(REPO_ROOT)}")
        return 1 if n["failed"] else 0

    # Build candidate list.
    if args.ids:
        want = [int(x) for x in args.ids.split(",") if x.strip()]
        candidates = []
        for pid in want:
            r = wp.s.get(f"{wp.base}/wp-json/wp/v2/posts/{pid}",
                         params={"context": "edit", "_fields": LIST_FIELDS}, timeout=30)
            if r.status_code == 200:
                candidates.append(r.json())
            else:
                log(f"  WARN: id {pid} not fetchable ({r.status_code})")
    else:
        candidates = fetch_candidates(wp, args.kind, args.since)
        if args.order == "oldest":
            candidates = list(reversed(candidates))
    if args.limit:
        candidates = candidates[: args.limit]
    log(f"{mode}: {len(candidates)} candidate {args.kind}s · fields={fields}")

    # Live preconditions: backup note + writability probe.
    probe_result = "n/a (dry-run)"
    backup_note = "n/a (dry-run)"
    if args.execute:
        if args.backup_dir and (REPO_ROOT / args.backup_dir).exists():
            backup_note = f"{args.backup_dir} present (additive meta-only; report is the revert artifact)"
        else:
            backup_note = ("NONE — additive meta-only write; every change recorded below for trivial "
                           "revert (set field back to empty). KK acknowledged pilot-without-backup.")
        pid = args.probe_id or auto_probe_id(candidates) or auto_probe_id(fetch_candidates(wp, "post", None))
        if not pid:
            log("ABORT: could not find a probe post with all 3 keys set."); return 3
        if not probe(wp, pid):
            log("ABORT: writability probe failed — keys not accepted. No batch writes attempted."); return 3
        probe_result = f"PASS on post {pid}"

    # Process.
    outcomes = []
    for item in candidates:
        out = apply_one(wp, item, args.kind, fields, live=args.execute)
        outcomes.append(out)
        if out["status"] in ("written", "planned"):
            log(f"  {out['status']:8} {out['id']} {out['slug'][:45]} -> {','.join(out.get('written') or [])}"
                + (f"  [{','.join(out['flags'])}]" if out["flags"] else ""))
        elif out["status"] == "failed":
            log(f"  FAILED   {out['id']} {out['slug'][:45]} -- {out['reason']}")

    ts = _utcnow().strftime("%Y%m%d-%H%M%SZ")
    report = REPO_ROOT / args.report_dir / f"seo-backfill-{ts}.md"
    filters = f"order={args.order} limit={args.limit or 'all'} since={args.since or '-'} ids={'yes' if args.ids else 'no'}"
    write_report(report, mode=mode, kind=args.kind, fields=fields, filters=filters,
                 probe_result=probe_result, backup_note=backup_note, outcomes=outcomes)

    n = {s: sum(1 for o in outcomes if o["status"] == s) for s in ("written", "planned", "skipped", "failed")}
    log("")
    log(f"SUMMARY [{mode}]: written={n['written']} planned={n['planned']} skipped={n['skipped']} failed={n['failed']}")
    log(f"report: {report.relative_to(REPO_ROOT)}")
    return 1 if n["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
