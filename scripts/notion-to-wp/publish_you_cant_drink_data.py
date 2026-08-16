#!/usr/bin/env python3
"""Convert the "You Can't Drink Data" march dispatch into a WordPress DRAFT on
kriskrug.co (and update it). Reuses WordPress/load_config from kk_notion_to_wp.
Links are hand-placed in post.md; the auto-linker is NOT run here.

Marker syntax in post.md:
  ## X               -> wp:heading
  ---                -> wp:separator
  >>> X              -> wp:pullquote
  ![alt](media:ID)   -> constrained in-body image reusing an AI-sign media id
  ![alt](photo:NNNN) -> constrained in-body image reusing an uploaded march photo
  [[GALLERY-BEST]]   -> gallery of the best signs (close crops, KK-voice captions)
  [[GALLERY-AI]]     -> gallery of the 14 AI protest signs
  [[GALLERY-PHOTOS]] -> gallery of the remaining unique real signs (not in BEST)
  everything else    -> wp:paragraph

Photos are uploaded idempotently (find-or-reuse by filename) so re-runs don't
duplicate media. Dry-run by default; --execute creates the draft; --update
refreshes the body of the existing draft. NEVER publishes.
"""
import re, sys, json, pathlib
from kk_notion_to_wp import WordPress, load_config
from wp_blocks import image, gallery
from publish_common import (
    build_seo_meta,
    category_id,
    exact,
    find_existing_post_by_slug,
    load_photos_from_dir,
    media_group_index,
    media_group_keys,
    media_id,
    parse_int_arg,
    parse_publish_argv,
    render_marker_blocks,
    resolve_category_ids,
    resolve_featured_media,
    standard_text_handlers,
    strip_frontmatter,
)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
STAGE = REPO_ROOT / "content" / "drafts" / "2026-05-23-you-cant-drink-data"
FLAGS = parse_publish_argv()
EXECUTE = FLAGS.execute
UPDATE = FLAGS.update
WRITE = FLAGS.write

TITLE = "You Can't Drink Data"
SLUG = "you-cant-drink-data"
DATE = "2026-05-23T15:00:00"
# Defaults are declared in publisher-ids.json and match the live draft;
# override with --category-id / --featured-media-id.
CATEGORY_ID = parse_int_arg(sys.argv[1:], "--category-id", category_id("ai-ethics-philosophy"))
FEATURED_ID = parse_int_arg(
    sys.argv[1:], "--featured-media-id", media_id("you-cant-drink-data-featured")
)
TAGS = ["ai-protest","data-centres","vancouver","clean-energy-ai",
        "indigenous-data-sovereignty","open-source-ai","both-hands-full"]
SEO_TITLE = "You Can't Drink Data | Notes From My First AI Protest"
META_DESC = ("Kris Krug marches in Vancouver's first anti-AI, anti-data-centre protest, "
             "and argues that 'shut it all down' and 'more compute, trust us' are the same "
             "dead end. A West Coast vision for building AI differently.")
SEO_META = build_seo_meta(SEO_TITLE, META_DESC)

# Already-uploaded AI protest signs (from the DC-signs draft), declared in
# publisher-ids.json. AI_SIGNS is id -> (url, alt); AI_GALLERY is the declared
# order used by the [[GALLERY-AI]] block.
AI_SIGNS, AI_GALLERY = media_group_index("ai-protest-signs-2026-05")
# short captions for the AI gallery (the slogan, lower-cased label)
AI_CAP = {mid: AI_SIGNS[mid][1].split(",")[0] for mid in AI_GALLERY}

# in-body AI signs: media id -> (caption, align, width). Small + floated so text wraps around them
# (KK: "reduce the size and integrate them into the text"). Click to enlarge.
# Signs are named via their declared key, so the production media IDs stay in
# publisher-ids.json rather than being retyped here.
SIGN = media_group_keys("ai-protest-signs-2026-05")
INBODY_AI = {
    SIGN["we-are-the-training-data"]: ("WE ARE THE TRAINING DATA. One of mine. The uncomfortable part is that it's just true.", "right", 300),
    SIGN["water-the-servers-last"]: ("WATER THE SERVERS LAST. Also mine. The watershed should outrank the GPU.", "left", 300),
    SIGN["i-love-the-cloud-i-just-want-it-to-rain"]: ("I LOVE THE CLOUD, I JUST WANT IT TO RAIN. Mine. Both-hands-full in eight words.", "right", 300),
}
# in-body documentary photos: key (leading IMG#) -> (align, width). Editorial = centered, larger.
INBODY_PHOTO = {
    "7674": ("center", 680), "7735": ("center", 720), "7719": ("center", 720),
    "7750": ("center", 600), "7790": ("center", 680), "7717": ("center", 460),
}
# which gallery/ files to KEEP in GALLERY-PHOTOS (the rest are duplicated in BEST, or held back)
PHOTOS_KEEP_PREFIX = {"05","07","10","13","14","15","16","17","18","21","23","24","25","26"}


# in-body image / gallery / heading / separator / pullquote markup now lives in
# wp_blocks.py; the marker -> block dispatch lives in publish_common.py.
MEDIA_RE = re.compile(r"^!\[(.*?)\]\(media:(\d+)\)$")
PHOTO_RE = re.compile(r"^!\[(.*?)\]\(photo:(\d+)\)$")


# ---------------------------------------------------------------------------
raw = (STAGE / "post.md").read_text()
body = strip_frontmatter(raw)
assert "—" not in body, "em-dash leaked into post.md body"

cfg = load_config()
wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

photo_log = []
best_photos = load_photos_from_dir(
    wp, STAGE, "photos/best", write=WRITE, alt_from_slug=True, photo_log=photo_log
)
gallery_all = load_photos_from_dir(
    wp, STAGE, "photos/gallery", write=WRITE, photo_log=photo_log
)
inbody_list = load_photos_from_dir(
    wp, STAGE, "photos/inbody", write=WRITE, photo_log=photo_log
)
photos_rest = [it for it in gallery_all if it[4][:2] in PHOTOS_KEEP_PREFIX]

inbody_photos = {}
for mid, url, alt, cap, fn in inbody_list:
    inbody_photos[fn.split("-", 1)[0]] = (mid, url, alt, cap)

print(f"[photos] {'wrote' if WRITE else 'DRY'} best={len(best_photos)} gallery_rest={len(photos_rest)} inbody={len(inbody_list)}")
for l in photo_log: print("   " + l)

# ---- build blocks ----
def ai_sign(block, match):
    """`![alt](media:ID)` -> small floated sign reusing an already-uploaded media id."""
    mid = int(match.group(2))
    url, alt = AI_SIGNS[mid]
    cap, align, width = INBODY_AI.get(mid, (None, "center", 320))
    return image(mid, url, alt, caption=cap, width=width, align=align)


def march_photo(block, match):
    """`![alt](photo:NNNN)` -> in-body march photo. An unknown key aborts.

    This used to emit nothing, which published a quietly shorter post than the one
    in post.md: the author asked for a photo, the photo was missing from
    photos/inbody/, and nothing said so (issue #483). Aborting surfaces it in the
    dry-run, before any WordPress write, because the inbody/ directory is globbed
    on both dry-run and execute.
    """
    key = match.group(2)
    if key not in inbody_photos:
        raise SystemExit(
            f"[ABORT] post.md references photo:{key} but no file in "
            f"{STAGE / 'photos/inbody'} starts with '{key}-'. "
            f"Known keys: {sorted(inbody_photos)}. "
            f"Add the photo or remove the marker; do not publish a shorter post silently."
        )
    mid, url, alt, cap = inbody_photos[key]
    align, width = INBODY_PHOTO.get(key, ("center", 660))
    return image(mid, url, alt, caption=cap, width=width, align=align)


out = render_marker_blocks(
    body,
    standard_text_handlers(h3=False, pullquote_marker=True)
    + [
        (exact("[[GALLERY-BEST]]"),
         lambda b, m: gallery([(i, u, a, c) for i, u, a, c, _ in best_photos], columns=3)),
        (exact("[[GALLERY-AI]]"),
         lambda b, m: gallery(
             [(mid, AI_SIGNS[mid][0], AI_SIGNS[mid][1], AI_CAP[mid]) for mid in AI_GALLERY],
             columns=3,
         )),
        # emits nothing when every gallery/ photo is already shown in BEST
        (exact("[[GALLERY-PHOTOS]]"),
         lambda b, m: gallery([(i, u, a, c) for i, u, a, c, _ in photos_rest], columns=3)
         if photos_rest else None),
        (MEDIA_RE, ai_sign),
        (PHOTO_RE, march_photo),
    ],
)

content = "\n\n".join(out)
(STAGE / "post.html").write_text(content)

# ---- sanity ----
assert "—" not in content, "em-dash leaked into content"
assert "media:" not in content and "photo:" not in content, "unresolved image marker"
assert "[[GALLERY" not in content, "unresolved gallery marker"
assert content.count("wp:pullquote") == 2 * 4, "expected 4 pullquotes"
n_gal = content.count("wp:gallery") // 2
n_img = content.count("<!-- wp:image ")
print(f"[blocks] {len(out)} blocks | {n_img} image blocks | galleries={n_gal} | pullquotes=4 | post.html staged ({len(content)} bytes)")

if not WRITE:
    print("\nDRY-RUN complete. --execute creates the draft; --update updates the existing one.")
    sys.exit(0)

# ---- find existing post by slug ----
existing = find_existing_post_by_slug(wp, SLUG)

if UPDATE:
    if not existing:
        sys.exit(f"[ABORT] --update but no post with slug {SLUG} found. Run --execute first.")
    pid = existing["id"]
    featured_id = resolve_featured_media(wp, media_id=FEATURED_ID, write=True)
    payload = {"content": content, "featured_media": featured_id}
    post = wp.update_post(pid, payload, expected_slug=SLUG)
    print(f"[post] UPDATED draft id={pid} status={post['status']}")
else:
    if existing:
        sys.exit(f"[ABORT] a post with slug {SLUG} already exists (id={existing['id']}). Use --update.")
    category_ids = resolve_category_ids(wp, ids=[CATEGORY_ID])
    featured_id = resolve_featured_media(wp, media_id=FEATURED_ID, write=True)
    tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
        "author": cfg.wp_author_id, "content": content, "excerpt": META_DESC,
        "categories": category_ids, "tags": tag_ids, "featured_media": featured_id,
        "meta": SEO_META,
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    # This script NEVER publishes (see the module docstring), so the safe outcome
    # is status=draft. The check used to assert status=="publish", which printed
    # "FAIL published" on every correct run and trained readers to skim past FAIL
    # lines in a safety readback (issue #483).
    "stays_draft": v["status"] == "draft",
    "featured_set": v.get("featured_media") == FEATURED_ID,
    "pullquotes_4": vc.count("wp:pullquote") == 8,
    "two_galleries": vc.count("wp:gallery") == 4,  # consolidated signs + AI (open+close each)
    "best_gallery_21": sum(1 for _, u, _, _, _ in best_photos if u in vc) == len(best_photos),
    "selfie_at_bottom": any(u in vc for i, u, _, _, fn in inbody_list if fn.startswith("7717")),
    "captions_present": vc.count("wp-element-caption") >= 30,
    "constrained_widths": "is-resized" in vc,
    "no_em_dash": "—" not in vc,
    "new_links": "sovereign-ai-for-whom" in vc and "punk-rock-ai" in vc and "your-taste-is-your-moat" in vc,
    "bhf_link_live": "/2026/01/24/both-hands-full/" in vc,
    "no_dead_companion_links": "/2026/05/23/data-center-protest-signs/" not in vc and "/2026/05/19/both-hands-full-vancouver" not in vc,
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == SEO_META["advanced_seo_description"],
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == SEO_META["jetpack_seo_html_title"],
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"{'updated' if UPDATE else 'created'} draft id={pid} status={post['status']}\npreview={preview}\nedit={edit}\n"
    f"featured(selfie)={FEATURED_ID}\nbest={len(best_photos)} ai_gallery={len(AI_GALLERY)} photos_rest={len(photos_rest)} inbody={len(inbody_list)}\n\n"
    "PHOTO MEDIA:\n" + ("\n".join(photo_log) if photo_log else "(none)")
    + "\n\nVERIFY:\n" + json.dumps(checks, indent=2))
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK ' if val else 'FAIL'} {k}")
print(f"\nPREVIEW: {preview}\nEDIT:    {edit}\nDONE — left as DRAFT.")
