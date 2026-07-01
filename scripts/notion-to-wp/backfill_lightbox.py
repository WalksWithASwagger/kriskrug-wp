#!/usr/bin/env python3
"""Backfill the native WordPress lightbox onto already-published kriskrug.co posts.

In-place transform of LIVE post content (safe even when a post's source markdown
has drifted from what's live, because it never rebuilds from source). For every
core image block it:
  - enables the native WP 6.4+ lightbox  ("linkDestination": none|media -> "lightbox":{"enabled":true})
  - unwraps click-to-open  <a href="..."><img></a>  anchors
  - drops gallery  "linkTo":"media"
  - normalizes the caption class  (wp-block-image__caption -> wp-element-caption)
Images with a CUSTOM outbound link ("linkDestination":"custom") are left untouched.

Safety: every write is guarded so the Gutenberg block STRUCTURE must be identical
before/after (only image markup changes), else the post is skipped and logged.
The original content of each post is appended to a rollback manifest BEFORE its
write, so a mid-run stop still leaves an accurate manifest.

  python backfill_lightbox.py                      # dry-run: report what would change
  python backfill_lightbox.py --execute            # apply; writes backfill-rollback.jsonl
  python backfill_lightbox.py --rollback FILE.jsonl # restore original content for every post in FILE

NOTE: updating content via REST bumps each post's modified date (sitemap lastmod).
"""
import sys, re, json, argparse
from collections import Counter

from kk_notion_to_wp import WordPress, load_config

_ANCHOR = re.compile(r'<a href="[^"]*"\s*>\s*(<img\b[^>]*?/?>)\s*</a>')


def transform(c: str) -> str:
    for a, b in (('"linkDestination":"none"', '"lightbox":{"enabled":true}'),
                 ('"linkDestination":"media"', '"lightbox":{"enabled":true}')):
        c = c.replace(a, b)
    c = c.replace('"linkTo":"media",', '').replace(',"linkTo":"media"', '').replace('"linkTo":"media"', '')
    c = _ANCHOR.sub(r'\1', c)
    c = c.replace('wp-block-image__caption', 'wp-element-caption')
    return c


def _struct(s: str) -> Counter:
    return Counter(re.findall(r'<!-- /?wp:[a-z]+', s))


def _iter_published(wp):
    page = 1
    while True:
        r = wp.s.get(f"{wp.base}/wp-json/wp/v2/posts",
                     params={"status": "publish", "per_page": 100, "page": page,
                             "context": "edit", "_fields": "id,slug,content"}, timeout=60).json()
        if not r:
            break
        for p in r:
            yield p
        if len(r) < 100:
            break
        page += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="apply the transform (default: dry-run)")
    ap.add_argument("--rollback", metavar="MANIFEST", help="restore original content from a manifest")
    ap.add_argument("--manifest", default="backfill-rollback.jsonl", help="rollback manifest path for --execute")
    args = ap.parse_args()

    cfg = load_config()
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

    if args.rollback:
        seen = {}
        for line in open(args.rollback):
            rec = json.loads(line)
            seen.setdefault(rec["id"], rec["before"])  # earliest = true original
        for pid, before in seen.items():
            wp.update_post(pid, {"content": before})
            print(f"restored {pid}")
        print(f"rollback complete: {len(seen)} posts")
        return

    cands = [(p["id"], p["slug"], p["content"]["raw"]) for p in _iter_published(wp)
             if "<!-- wp:image " in p["content"]["raw"]
             and transform(p["content"]["raw"]) != p["content"]["raw"]]
    print(f"posts needing transform: {len(cands)}")

    if not args.execute:
        for pid, slug, c in cands[:25]:
            t = transform(c)
            tag = "OK  " if _struct(t) == _struct(c) else "SKIP"
            print(f"  {tag} {pid} {slug} (+{t.count('lightbox') - c.count('lightbox')} lightbox)")
        if len(cands) > 25:
            print(f"  ... and {len(cands) - 25} more")
        print(f"\nDRY-RUN. --execute applies the transform to {len(cands)} posts.")
        return

    updated = skipped = 0
    errors = []
    for pid, slug, before in cands:
        after = transform(before)
        if _struct(after) != _struct(before):
            skipped += 1
            errors.append((pid, slug, "struct-changed"))
            continue
        with open(args.manifest, "a") as f:  # record original BEFORE writing (crash-safe)
            f.write(json.dumps({"id": pid, "slug": slug, "before": before}) + "\n")
        try:
            wp.update_post(pid, {"content": after})
            updated += 1
        except Exception as e:
            errors.append((pid, slug, str(e)[:60]))
    print(f"DONE updated={updated} skipped={skipped} errors={len(errors)} manifest={args.manifest}")
    for e in errors[:15]:
        print("  ", e)


if __name__ == "__main__":
    main()
