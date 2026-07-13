#!/usr/bin/env python3
"""Stage "The Great Canadian Proximity Game" as a DRAFT on kriskrug.co.

Text post with hand-placed links (the auto-linker is NOT run here). Models the
create-draft pattern of publish_you_cant_drink_data.py without the photo/gallery
machinery. WP-only: reads creds straight from .env, so no NOTION_TOKEN required.

Markers in post.md:
  # X    -> post title (first one is skipped; comes from frontmatter)
  ## X   -> wp:heading (h2)
  ### X  -> wp:heading (h3)
  ---    -> wp:separator
  else   -> wp:paragraph

Dry-run by default. --execute creates the draft (status=draft, NEVER publishes,
aborts if the slug already exists). --update refreshes the body of the existing
draft found by slug.
"""
import re, sys, json, pathlib
import yaml
from dotenv import dotenv_values
from kk_notion_to_wp import WordPress, WP_BASE_URL_DEFAULT, WP_DEFAULT_AUTHOR_ID
from publish_common import (
    build_seo_meta,
    ensure_term_id,
    parse_publish_argv,
    render_text_post,
)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
STAGE = REPO_ROOT / "content" / "drafts" / "2026-06-04-the-great-canadian-proximity-game"
ENV = SCRIPT_DIR / ".env"
FLAGS = parse_publish_argv()
EXECUTE = FLAGS.execute
UPDATE = FLAGS.update
WRITE = FLAGS.write


# ---- load draft ----
raw = (STAGE / "post.md").read_text()
fmatch = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", raw, flags=re.S)
fm = yaml.safe_load(fmatch.group(1))
body = fmatch.group(2).strip()
assert "—" not in body, "em-dash leaked into post.md body"

content = render_text_post(body)
(STAGE / "post.html").write_text(content)
assert "—" not in content, "em-dash leaked into content"
n_links = content.count("<a href=")
n_blocks = content.count("<!-- wp:")
print(f"[blocks] {n_blocks} blocks | {n_links} links | post.html staged ({len(content)} bytes)")

if not WRITE:
    print("\nDRY-RUN complete. --execute creates the draft; --update updates the existing one.")
    sys.exit(0)

# ---- WP client (WP-only creds; no NOTION_TOKEN needed) ----
env = dotenv_values(ENV)
user = env.get("WP_USER")
pw = (env.get("WP_APP_PASSWORD") or "").replace(" ", "")
author_id = int(env.get("WP_DEFAULT_AUTHOR_ID", WP_DEFAULT_AUTHOR_ID))
if not (user and pw):
    sys.exit(f"[ABORT] WP_USER / WP_APP_PASSWORD missing from {ENV}")
wp = WordPress(WP_BASE_URL_DEFAULT, user, pw)

TITLE = fm["title"]
SLUG = fm["slug"]
EXCERPT = fm.get("excerpt", "")
CATEGORIES = fm.get("categories", []) or []
TAGS = fm.get("tags", []) or []
SEO = fm.get("seo", {}) or {}
SEO_META = build_seo_meta(SEO.get("meta_title", ""), SEO.get("meta_description", ""))

existing = wp.find_post_by_slug(SLUG)

if UPDATE:
    if not existing:
        sys.exit(f"[ABORT] --update but no post with slug {SLUG}. Run --execute first.")
    post = wp.update_post(existing, {"content": content})
    pid = existing
    print(f"[post] UPDATED draft id={pid} status={post['status']}")
else:
    if existing:
        sys.exit(f"[ABORT] a post with slug {SLUG} already exists (id={existing}). Use --update.")
    cat_ids = [ensure_term_id(wp, "categories", c) for c in CATEGORIES]
    tag_ids = [ensure_term_id(wp, "tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft",
        "author": author_id, "content": content, "excerpt": EXCERPT,
        "categories": cat_ids, "tags": tag_ids,
        "meta": SEO_META,
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

# ---- verify (must remain a draft) ----
v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "is_draft_not_publish": v["status"] == "draft",
    "title_ok": v["title"]["raw"] == TITLE,
    "links_present": vc.count("<a href=") >= 12,
    "kriskrug_link": "kriskrug.co/2026/01/24/both-hands-full" in vc,
    "bcai_link": "bc-ai.ca/news/aligning-bc-ai" in vc,
    "gov_links": "pm.gc.ca" in vc and "ised-isde.canada.ca" in vc,
    "external_newtab": 'rel="noopener noreferrer"' in vc,
    "no_em_dash": "—" not in vc,
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"{'updated' if UPDATE else 'created'} draft id={pid} status={post['status']}\n"
    f"preview={preview}\nedit={edit}\n\nVERIFY:\n" + json.dumps(checks, indent=2)
)
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK ' if val else 'FAIL'} {k}")
print(f"\nPREVIEW: {preview}\nEDIT:    {edit}\nDONE — left as DRAFT.")
