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
from kk_notion_to_wp import WordPress, load_config, slugify
from connector_payload import normalize_seo_meta
from wp_blocks import inline, image, gallery, heading, separator, pullquote

STAGE = pathlib.Path("/Users/kk/Code/kriskrug-wp/content/drafts/2026-05-23-you-cant-drink-data")
EXECUTE = "--execute" in sys.argv
UPDATE = "--update" in sys.argv
WRITE = EXECUTE or UPDATE

TITLE = "You Can't Drink Data"
SLUG = "you-cant-drink-data"
DATE = "2026-05-23T15:00:00"
CATEGORY_ID = 1678  # AI Ethics & Philosophy
TAGS = ["ai-protest","data-centres","vancouver","clean-energy-ai",
        "indigenous-data-sovereignty","open-source-ai","both-hands-full"]
FEATURED_ID = 11976  # hero/og: the FUCK AI! sign (KK's pick). Selfie moved to bottom.
SEO_TITLE = "You Can't Drink Data | Notes From My First AI Protest"
META_DESC = ("Kris Krug marches in Vancouver's first anti-AI, anti-data-centre protest, "
             "and argues that 'shut it all down' and 'more compute, trust us' are the same "
             "dead end. A West Coast vision for building AI differently.")

# Already-uploaded AI protest signs (from the DC-signs draft): id -> (url, alt)
AI_SIGNS = {
    11915: ("https://kriskrug.co/wp-content/uploads/2026/05/02-both-hands-full.png", "BOTH HANDS FULL, neon block-stack lettering over two hands overflowing with shapes"),
    11916: ("https://kriskrug.co/wp-content/uploads/2026/05/01-dumbest-timeline-the-keeper.png", "THIS IS THE DUMBEST TIMELINE & I WOULDN'T MISS IT, CMYK slab type"),
    11917: ("https://kriskrug.co/wp-content/uploads/2026/05/01-ruthlessly-optimistic-absolutely-terrified.png", "RUTHLESSLY OPTIMISTIC & ABSOLUTELY TERRIFIED, acid riso, sunny yellow into blood red"),
    11918: ("https://kriskrug.co/wp-content/uploads/2026/05/04-water-the-servers-last.png", "WATER THE SERVERS LAST, block-stack type with a watering can over a server rack"),
    11919: ("https://kriskrug.co/wp-content/uploads/2026/05/06-who-s-a-thirsty-little-data-center.png", "WHO'S A THIRSTY LITTLE DATA CENTER?, a googly-eyed building with its tongue out"),
    11920: ("https://kriskrug.co/wp-content/uploads/2026/05/02-we-are-the-training-data.jpg", "WE ARE THE TRAINING DATA, datamosh glitch type"),
    11921: ("https://kriskrug.co/wp-content/uploads/2026/05/09-ai-wrote-a-better-sign.jpg", "AI WROTE A BETTER SIGN THAN THIS ONE, neon block panels"),
    11922: ("https://kriskrug.co/wp-content/uploads/2026/05/03-my-position-yes-also-help.png", "MY POSITION: YES. ALSO: HELP., green YES over a panicked red HELP"),
    11923: ("https://kriskrug.co/wp-content/uploads/2026/05/03-it-s-complicated.png", "IT'S COMPLICATED, CMYK halftone"),
    11924: ("https://kriskrug.co/wp-content/uploads/2026/05/04-i-contain-multitudes.png", "I CONTAIN MULTITUDES, fractured tall glyphs in pink, teal, cream"),
    11925: ("https://kriskrug.co/wp-content/uploads/2026/05/07-error-404-side-not-found.png", "ERROR 404: SIDE NOT FOUND, RGB-split datamosh"),
    11926: ("https://kriskrug.co/wp-content/uploads/2026/05/09-stop-okay-go-no-stop.png", "STOP. okay GO. no, STOP., clashing panels with a strike-through"),
    11927: ("https://kriskrug.co/wp-content/uploads/2026/05/07-hush-now-little-supercluster.png", "HUSH NOW, LITTLE SUPERCLUSTER, server racks tucked in under a quilt, crescent moon"),
    11928: ("https://kriskrug.co/wp-content/uploads/2026/05/08-i-love-the-cloud-i-just-want-it-to-rain.png", "I LOVE THE CLOUD, I JUST WANT IT TO RAIN, riso clouds and rain"),
}
AI_GALLERY = [11915, 11919, 11920, 11918, 11922, 11923, 11924, 11916, 11917, 11925, 11926, 11921, 11927, 11928]
# short captions for the AI gallery (the slogan, lower-cased label)
AI_CAP = {mid: AI_SIGNS[mid][1].split(",")[0] for mid in AI_GALLERY}

# in-body AI signs: media id -> (caption, align, width). Small + floated so text wraps around them
# (KK: "reduce the size and integrate them into the text"). Click to enlarge.
INBODY_AI = {
    11920: ("WE ARE THE TRAINING DATA. One of mine. The uncomfortable part is that it's just true.", "right", 300),
    11918: ("WATER THE SERVERS LAST. Also mine. The watershed should outrank the GPU.", "left", 300),
    11928: ("I LOVE THE CLOUD, I JUST WANT IT TO RAIN. Mine. Both-hands-full in eight words.", "right", 300),
}
# in-body documentary photos: key (leading IMG#) -> (align, width). Editorial = centered, larger.
INBODY_PHOTO = {
    "7674": ("center", 680), "7735": ("center", 720), "7719": ("center", 720),
    "7750": ("center", 600), "7790": ("center", 680), "7717": ("center", 460),
}
# which gallery/ files to KEEP in GALLERY-PHOTOS (the rest are duplicated in BEST, or held back)
PHOTOS_KEEP_PREFIX = {"05","07","10","13","14","15","16","17","18","21","23","24","25","26"}


# in-body image / gallery / heading / separator / pullquote markup now lives in wp_blocks.py


# ---------------------------------------------------------------------------
raw = (STAGE / "post.md").read_text()
fm_end = raw.index("\n---", raw.index("---") + 3)
body = raw[fm_end + 4:]
assert "—" not in body, "em-dash leaked into post.md body"

cfg = load_config()
wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp"}
photo_log = []

def load_captions(d: pathlib.Path) -> dict:
    caps = {}
    f = d / "captions.txt"
    if f.exists():
        for line in f.read_text().splitlines():
            if "|" in line:
                fn, alt = line.split("|", 1)
                caps[fn.strip()] = alt.strip()
    return caps

def find_media(stem: str):
    """Find already-uploaded media whose file basename starts with stem. Reuse to avoid dupes."""
    try:
        r = wp.s.get(f"{wp.base}/wp-json/wp/v2/media",
                     params={"search": stem, "per_page": 10, "context": "edit"}, timeout=30).json()
    except Exception:
        return None
    if isinstance(r, list):
        for m in r:
            base = m.get("source_url", "").rsplit("/", 1)[-1]
            if base == f"{stem}.jpg" or base.startswith(stem):
                return m["id"], m["source_url"]
    return None

def load_photos(subdir: str, alt_from_slug=False) -> list:
    """Return [(id, url, alt, caption, filename)] for STAGE/subdir.
    caption = captions.txt text. alt = slug-derived (if alt_from_slug) else caption."""
    d = STAGE / subdir
    files = sorted(p for p in d.glob("*.jpg") if not p.name.startswith("_"))
    caps = load_captions(d)
    items = []
    for p in files:
        caption = caps.get(p.name, "")
        alt = (re.sub(r"^\d+-", "", p.stem).replace("-", " ") + " protest sign") if alt_from_slug else (caption or p.stem)
        if WRITE:
            found = find_media(p.stem)
            if found:
                mid, url = found
                photo_log.append(f"{subdir}/{p.name} -> REUSE id={mid}")
            else:
                media = wp.upload_media(p, alt=alt, mime="image/jpeg")
                mid, url = media["id"], media["source_url"]
                photo_log.append(f"{subdir}/{p.name} -> NEW id={mid} {url}")
            items.append((mid, url, alt, caption, p.name))
        else:
            items.append((0, f"DRYRUN/{p.name}", alt, caption, p.name))
    return items

best_photos = load_photos("photos/best", alt_from_slug=True)     # close crops, KK captions
gallery_all = load_photos("photos/gallery")                       # the 26 uploaded signs
inbody_list = load_photos("photos/inbody")                        # narrative-beat photos
photos_rest = [it for it in gallery_all if it[4][:2] in PHOTOS_KEEP_PREFIX]  # the 14 not in BEST

inbody_photos = {}
for mid, url, alt, cap, fn in inbody_list:
    inbody_photos[fn.split("-", 1)[0]] = (mid, url, alt, cap)

print(f"[photos] {'wrote' if WRITE else 'DRY'} best={len(best_photos)} gallery_rest={len(photos_rest)} inbody={len(inbody_list)}")
for l in photo_log: print("   " + l)

# ---- build blocks ----
out = []
seen_title = False
blocks_src = [b.rstrip() for b in re.split(r"\n\s*\n", body) if b.strip()]
for b in blocks_src:
    b = b.strip()
    if b.startswith("# ") and not seen_title:
        seen_title = True
        continue
    if b == "---":
        out.append(separator())
    elif b.startswith("## "):
        out.append(heading(inline(b[3:].strip())))
    elif b.startswith(">>> "):
        out.append(pullquote(inline(b[4:].strip())))
    elif b == "[[GALLERY-BEST]]":
        out.append(gallery([(i, u, a, c) for i, u, a, c, _ in best_photos], columns=3))
    elif b == "[[GALLERY-AI]]":
        out.append(gallery([(mid, AI_SIGNS[mid][0], AI_SIGNS[mid][1], AI_CAP[mid]) for mid in AI_GALLERY], columns=3))
    elif b == "[[GALLERY-PHOTOS]]":
        if photos_rest:
            out.append(gallery([(i, u, a, c) for i, u, a, c, _ in photos_rest], columns=3))
    else:
        m = re.match(r"^!\[(.*?)\]\(media:(\d+)\)$", b)
        mp = re.match(r"^!\[(.*?)\]\(photo:(\d+)\)$", b)
        if m:
            mid = int(m.group(2))
            url, alt = AI_SIGNS[mid]
            cap, align, width = INBODY_AI.get(mid, (None, "center", 320))
            out.append(image(mid, url, alt, caption=cap, width=width, align=align))
        elif mp:
            key = mp.group(2)
            if key in inbody_photos:
                mid, url, alt, cap = inbody_photos[key]
                align, width = INBODY_PHOTO.get(key, ("center", 660))
                out.append(image(mid, url, alt, caption=cap, width=width, align=align))
        else:
            para = "<br>".join(inline(line.strip()) for line in b.split("\n"))
            out.append(f"<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->")

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
hits = wp.s.get(f"{wp.base}/wp-json/wp/v2/posts",
                params={"slug": SLUG, "status": "any", "context": "edit"}, timeout=30).json()
existing = hits[0] if isinstance(hits, list) and hits else None

if UPDATE:
    if not existing:
        sys.exit(f"[ABORT] --update but no post with slug {SLUG} found. Run --execute first.")
    pid = existing["id"]
    payload = {"content": content, "featured_media": FEATURED_ID}
    post = wp.update_post(pid, payload)
    print(f"[post] UPDATED draft id={pid} status={post['status']}")
else:
    if existing:
        sys.exit(f"[ABORT] a post with slug {SLUG} already exists (id={existing['id']}). Use --update.")
    tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
        "author": cfg.wp_author_id, "content": content, "excerpt": META_DESC,
        "categories": [CATEGORY_ID], "tags": tag_ids, "featured_media": FEATURED_ID,
        "meta": {"advanced_seo_description": normalize_seo_meta(META_DESC), "jetpack_seo_html_title": normalize_seo_meta(SEO_TITLE)},
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "published": v["status"] == "publish",
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
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == normalize_seo_meta(META_DESC),
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == normalize_seo_meta(SEO_TITLE),
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
