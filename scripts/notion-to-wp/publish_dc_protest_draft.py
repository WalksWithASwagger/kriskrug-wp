#!/usr/bin/env python3
"""One-off: convert the 'Data Center Protest Signs' article package into a
WordPress DRAFT on kriskrug.co. Reuses WordPress (upload_media/ensure_term/
create_post), slugify, load_config, and text_polish.purge_em_dashes.

Dry-run by default (writes staged post.html + prints plan). --execute uploads
the 14 images and creates the DRAFT post. NEVER publishes.
"""
import re, sys, json, shutil, pathlib, datetime
from kk_notion_to_wp import WordPress, load_config, slugify
from text_polish import purge_em_dashes

SRC = pathlib.Path("/Users/kk/Code/notion-local/kk-ai-ecosystem/content/articles/kris-krug-thought-leadership/25-data-center-protest-signs")
STAGE = pathlib.Path("/Users/kk/Code/kriskrug-wp/content/drafts/2026-05-23-data-center-protest-signs")
EXECUTE = "--execute" in sys.argv

TITLE = "Both Hands Full at the Data Center: Protest Signs for People Who Refuse to Pick a Side"
SLUG = "data-center-protest-signs"
DATE = "2026-05-23T12:00:00"
CATEGORY_ID = 1678  # AI Ethics & Philosophy
TAGS = ["data-centers","ai-infrastructure","sovereign-ai","protest","vancouver","both-hands-full","generative-art","bc-ai"]
# KK's call (2026-05-23): Jetpack ties og:image to the featured image, so to get
# the "thirsty data center" share card, it IS the featured image. both-hands-full
# stays as the first in-body image.
FEATURED_FILE = "06-who-s-a-thirsty-little-data-center.png"
OG_FILE = "06-who-s-a-thirsty-little-data-center.png"
BHF_URL = "https://kriskrug.co/2026/01/24/both-hands-full/"
LINK39_OLD = "[critique and curiosity in the same two hands](https://kriskrug.co)"
LINK39_NEW = "[critique and curiosity in the same two hands](" + BHF_URL + ")"
SEO_TITLE = "Both Hands Full at the Data Center: Protest Signs for the Middle"
META_DESC = purge_em_dashes("I made AI protest signs for a Vancouver data-center fight — signs that refuse to pick a side. On water, compute, sovereignty, and holding both hands full.")

raw = (SRC / "draft.md").read_text()
fm_end = raw.index("\n---", raw.index("---") + 3)
body = raw[fm_end + 4:]
# fixes + house em-dash purge (site-wide)
body = body.replace(LINK39_OLD, LINK39_NEW)
assert LINK39_NEW in body, "line-39 link fix did not apply"
body = purge_em_dashes(body)

def inline(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

IMG_RE = re.compile(r"^!\[(.+?)\]\(images/(.+?)\)$")
blocks_src = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]

# ordered list of (filename, alt) for images, in body order
image_order = []
for b in blocks_src:
    m = IMG_RE.match(b)
    if m:
        image_order.append((m.group(2), m.group(1)))
assert len(image_order) == 14, f"expected 14 images, found {len(image_order)}"

cfg = load_config()
wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

# ---- stage a copy into content/drafts/ (repo record) ----
STAGE.mkdir(parents=True, exist_ok=True)
shutil.copy2(SRC / "draft.md", STAGE / "post.md")
shutil.copy2(SRC / "seo.md", STAGE / "seo.md")
(STAGE / "images").mkdir(exist_ok=True)
for fn, _ in image_order:
    shutil.copy2(SRC / "images" / fn, STAGE / "images" / fn)

# ---- upload images (execute) or stub (dry-run) ----
uploaded = {}  # filename -> {id, url}
log = []
for fn, alt in image_order:
    if EXECUTE:
        media = wp.upload_media(SRC / "images" / fn, alt=alt, mime="image/png")
        uploaded[fn] = {"id": media["id"], "url": media["source_url"]}
        log.append(f"{fn} -> id={media['id']} {media['source_url']}")
    else:
        uploaded[fn] = {"id": 0, "url": f"DRYRUN/{fn}"}
print("[media] " + ("uploaded" if EXECUTE else "DRY-RUN") + f" {len(uploaded)} images")
for line in log: print("   " + line)

# ---- build Gutenberg blocks ----
out = []
seen_title = False
for b in blocks_src:
    if b.startswith("# ") and not seen_title:
        seen_title = True; continue  # drop duplicate H1 (post title field)
    m = IMG_RE.match(b)
    if m:
        fn, alt = m.group(2), m.group(1)
        u = uploaded[fn]
        out.append(
            f'<!-- wp:image {{"id":{u["id"]},"sizeSlug":"large","linkDestination":"none"}} -->\n'
            f'<figure class="wp-block-image size-large"><img src="{u["url"]}" alt="{alt}" class="wp-image-{u["id"]}"/>'
            f'<figcaption class="wp-block-image__caption">{alt}</figcaption></figure>\n'
            f'<!-- /wp:image -->')
    elif b.startswith("## "):
        out.append(f"<!-- wp:heading -->\n<h2>{inline(b[3:].strip())}</h2>\n<!-- /wp:heading -->")
    elif b == "---":
        out.append('<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->')
    else:
        out.append(f"<!-- wp:paragraph -->\n<p>{inline(b)}</p>\n<!-- /wp:paragraph -->")
content = "\n\n".join(out)
(STAGE / "post.html").write_text(content)

# sanity
assert content.count("<!-- wp:image ") == 14, "expected 14 image blocks"
assert "images/" not in content, "local image path leaked into content"
assert "—" not in content, "em-dash leaked into content"
assert BHF_URL in content, "both-hands-full link missing"
print(f"[blocks] {len(out)} blocks | 14 images | post.html staged ({len(content)} bytes)")

if not EXECUTE:
    print("\nDRY-RUN complete. Re-run with --execute to upload + create the draft.")
    sys.exit(0)

# ---- create-only slug guard ----
hits = wp.s.get(f"{wp.base}/wp-json/wp/v2/posts", params={"slug": SLUG, "status": "any", "context": "edit"}, timeout=30).json()
if isinstance(hits, list) and hits:
    sys.exit(f"[ABORT] a post with slug {SLUG} already exists (id={hits[0]['id']}). Not creating a duplicate.")

# ---- terms ----
tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
print(f"[terms] category={CATEGORY_ID} tags={tag_ids}")

payload = {
    "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
    "author": cfg.wp_author_id, "content": content, "excerpt": META_DESC,
    "categories": [CATEGORY_ID], "tags": tag_ids,
    "featured_media": uploaded[FEATURED_FILE]["id"],
    "meta": {"advanced_seo_description": META_DESC, "jetpack_seo_html_title": SEO_TITLE},
}
post = wp.create_post(payload)
pid = post["id"]
print(f"[post] CREATED draft id={pid} status={post['status']}")

# verify
v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "status_draft": v["status"] == "draft",
    "slug": v["slug"] == SLUG,
    "category": CATEGORY_ID in v.get("categories", []),
    "tags": len(v.get("tags", [])) == len(TAGS),
    "featured_set": v.get("featured_media") == uploaded[FEATURED_FILE]["id"],
    "14_images": vc.count("<!-- wp:image ") == 14,
    "no_local_paths": "images/" not in vc or "wp-content/uploads" in vc,
    "bhf_link": BHF_URL in vc,
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == META_DESC,
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == SEO_TITLE,
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"created draft id={pid} status={post['status']}\npreview={preview}\nedit={edit}\n"
    f"featured(both-hands-full)={uploaded[FEATURED_FILE]['url']}\n"
    f"og-intended(thirsty-data-center)={uploaded[OG_FILE]['url']}\n\nMEDIA:\n" + "\n".join(log) +
    "\n\nVERIFY:\n" + json.dumps(checks, indent=2))
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK ' if val else 'FAIL'} {k}")
print(f"\nPREVIEW: {preview}\nEDIT:    {edit}")
print(f"FEATURED (both-hands-full): {uploaded[FEATURED_FILE]['url']}")
print(f"OG intended (thirsty-data-center): {uploaded[OG_FILE]['url']}")
print("\nMEDIA URLS:")
for line in log: print("  " + line)
print("\nDONE — left as DRAFT.")
