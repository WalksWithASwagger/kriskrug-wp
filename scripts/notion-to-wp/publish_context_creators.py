#!/usr/bin/env python3
"""Convert the "Context Creators" field report (2026 Philadelphia Creators Summit /
Lenfest PMFE journalism+AI program) into a WordPress DRAFT on kriskrug.co.

Reuses WordPress/load_config from kk_notion_to_wp. Links are hand-placed in
post.md; the auto-linker is NOT run here. The five Aurora concept posters are
uploaded idempotently (find-or-reuse by filename) so re-runs don't duplicate
media. Dry-run by default; --execute creates the draft; --update refreshes the
body of the existing draft. NEVER publishes.

Marker syntax in post.md:
  ## X              -> wp:heading
  ---               -> wp:separator
  >>> X             -> wp:pullquote (deck / callout)
  ![alt](poster:N)  -> full-width in-body hero, N in 1..5 (staged poster file)
  everything else   -> wp:paragraph
"""
import re, sys, json, pathlib
from kk_notion_to_wp import WordPress, load_config, slugify
from connector_payload import normalize_seo_meta
from wp_blocks import inline, inline_image, hero_image, heading, separator, pullquote

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
STAGE = REPO_ROOT / "content" / "drafts" / "2026-06-28-context-creators"
IMAGES = STAGE / "images"
EXECUTE = "--execute" in sys.argv
UPDATE = "--update" in sys.argv
WRITE = EXECUTE or UPDATE

TITLE = "Context Creators"
SLUG = "context-creators"
DATE = "2026-06-28T09:00:00"
CATEGORY = "AI for Creatives"
TAGS = ["ai-for-journalists", "creator-economy", "philadelphia",
        "lenfest-institute", "context-creators", "the-upgrade-ai", "journalism"]
SEO_TITLE = "Context Creators | Four Months Inside Philadelphia's Journalism + AI Experiment"
META_DESC = ("Four months coaching eight Philadelphia journalists on building AI into their "
             "work for the Lenfest Institute's creator program, and what it proved about "
             "trust, specificity, and the future of local media.")

# Real screenshots from KK's "AI-Assisted Workflows" deck -> (filename, alt, caption).
# Placed as centered, captioned, medium-width receipts in "What I Actually Did".
SCREENSHOTS = {
    "persona": ("slide-persona-output-parameters.png",
                "Slide titled Persona, Output, Parameters, the recipe for briefing an AI assistant in plain language.",
                "The recipe behind every bot I built: Persona, Output, Parameters. Straight from my AI-Assisted Workflows deck."),
    "pipeline": ("slide-transcript-to-story.png",
                 "Slide titled Transcript to Story, showing Record, Extract, Draft, Publish and three to four hours saved per story.",
                 "One interview in, a full package out. Roughly three to four hours saved per story."),
    "rules": ("slide-five-rules.png",
              "Slide titled Five Rules: human in the loop, verify everything, protect sources, disclose when appropriate, bias is baked in.",
              "The five rules I kept coming back to in every session."),
}

# poster N -> (staged filename, alt). poster 1 is the featured/OG image (not placed in body).
POSTERS = {
    1: ("poster-1-context-creator.png",
        "Context Creator. Three braided strands of aurora light over a Philadelphia skyline."),
    2: ("poster-2-both-hands-full.png",
        "Both Hands Full. A figure holds an iron weight in one hand and a swirl of aurora light in the other."),
    3: ("poster-3-fellows-plants.png",
        "You cannot be what you cannot see. A Puerto Rican wildflower and a Haitian tropical bloom with roots braided together underground."),
    4: ("poster-4-loom.png",
        "Teaching the machine who you are. A wooden loom weaves ribbons of rainbow light into dark cloth."),
    5: ("poster-5-city-map.png",
        "The city got to me. A glowing map of Philadelphia, light running from the Science Center out to every neighborhood."),
}


# In-body block markup lives in wp_blocks.py (shared, kk-aurora-aware):
#   hero_image()   -> full-width section heroes (the posters)
#   inline_image() -> small, centered, click-to-zoom receipts (the deck screenshots)
#   inline/heading/separator/pullquote -> text + structural blocks

# ---------------------------------------------------------------------------
raw = (STAGE / "post.md").read_text()
fm_end = raw.index("\n---", raw.index("---") + 3)
body = raw[fm_end + 4:]
assert "—" not in body, "em-dash leaked into post.md body"

cfg = load_config()
wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)


def find_media(stem: str):
    """Reuse already-uploaded media whose basename matches stem (avoid dupes)."""
    if not WRITE:
        return None
    try:
        r = wp.s.get(f"{wp.base}/wp-json/wp/v2/media",
                     params={"search": stem, "per_page": 10, "context": "edit"}, timeout=30).json()
    except Exception:
        return None
    if isinstance(r, list):
        for m in r:
            base = m.get("source_url", "").rsplit("/", 1)[-1]
            if base == f"{stem}.png" or base.startswith(stem):
                return m["id"], m["source_url"]
    return None


media_log = []
poster_media = {}  # N -> (id, url, alt)
for n, (fn, alt) in POSTERS.items():
    p = IMAGES / fn
    assert p.exists(), f"missing staged poster: {p}"
    if WRITE:
        found = find_media(p.stem)
        if found:
            mid, url = found
            media_log.append(f"{fn} -> REUSE id={mid}")
        else:
            m = wp.upload_media(p, alt=alt, mime="image/png")
            mid, url = m["id"], m["source_url"]
            media_log.append(f"{fn} -> NEW id={mid} {url}")
        poster_media[n] = (mid, url, alt)
    else:
        poster_media[n] = (0, f"DRYRUN/{fn}", alt)

shot_media = {}  # key -> (id, url, alt, caption)
for key, (fn, alt, caption) in SCREENSHOTS.items():
    p = IMAGES / fn
    assert p.exists(), f"missing staged screenshot: {p}"
    if WRITE:
        found = find_media(p.stem)
        if found:
            mid, url = found
            media_log.append(f"{fn} -> REUSE id={mid}")
        else:
            m = wp.upload_media(p, alt=alt, mime="image/png")
            mid, url = m["id"], m["source_url"]
            media_log.append(f"{fn} -> NEW id={mid} {url}")
        shot_media[key] = (mid, url, alt, caption)
    else:
        shot_media[key] = (0, f"DRYRUN/{fn}", alt, caption)

print(f"[media] {'wrote' if WRITE else 'DRY'} {len(poster_media)} posters + {len(shot_media)} screenshots")
for l in media_log:
    print("   " + l)

FEATURED_ID = poster_media[1][0]

# ---- build blocks ----
out = []
seen_title = False
for b in [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]:
    if b.startswith("# ") and not seen_title:
        seen_title = True
        continue
    if b == "---":
        out.append(separator())
    elif b.startswith("## "):
        out.append(heading(inline(b[3:].strip())))
    elif b.startswith(">>> "):
        out.append(pullquote(inline(b[4:].strip())))
    else:
        mp = re.match(r"^!\[(.*?)\]\(poster:(\d+)\)$", b)
        ms = re.match(r"^!\[(.*?)\]\(screenshot:([a-z-]+)\)$", b)
        if mp:
            n = int(mp.group(2))
            mid, url, alt = poster_media[n]
            out.append(hero_image(mid, url, alt))
        elif ms:
            mid, url, alt, caption = shot_media[ms.group(2)]
            out.append(inline_image(mid, url, alt, caption=caption))
        else:
            para = "<br>".join(inline(line.strip()) for line in b.split("\n"))
            out.append(f"<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->")

content = "\n\n".join(out)
(STAGE / "post.html").write_text(content)

# ---- sanity ----
assert "—" not in content, "em-dash leaked into content"
assert "poster:" not in content, "unresolved poster marker"
assert "screenshot:" not in content, "unresolved screenshot marker"
n_img = content.count("<!-- wp:image ")
n_pq = content.count("wp:pullquote") // 2
n_h2 = content.count("<h2")
exp_img = 4 + len(SCREENSHOTS)  # 4 in-body posters + N deck screenshots
assert n_img == exp_img, f"expected {exp_img} in-body images, got {n_img}"
assert n_pq >= 4, f"expected >=4 pullquotes, got {n_pq}"
print(f"[blocks] {len(out)} blocks | {n_img} images ({exp_img} expected) | pullquotes={n_pq} | h2={n_h2} | post.html staged ({len(content)} bytes)")

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
    post = wp.update_post(pid, {"content": content, "featured_media": FEATURED_ID})
    print(f"[post] UPDATED draft id={pid} status={post['status']}")
else:
    if existing:
        sys.exit(f"[ABORT] a post with slug {SLUG} already exists (id={existing['id']}). Use --update.")
    cat_id = wp.ensure_term("categories", CATEGORY)
    tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
        "author": cfg.wp_author_id, "content": content, "excerpt": META_DESC,
        "categories": [cat_id], "tags": tag_ids, "featured_media": FEATURED_ID,
        "meta": {"advanced_seo_description": normalize_seo_meta(META_DESC),
                 "jetpack_seo_html_title": normalize_seo_meta(SEO_TITLE)},
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

# ---- verify ----
v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "is_draft": v["status"] == "draft",
    "not_published": v["status"] != "publish",
    "featured_set": v.get("featured_media") == FEATURED_ID,
    "all_images_present": vc.count("<!-- wp:image ") == 4 + len(SCREENSHOTS),
    "screenshots_captioned": all(s[1] in vc for s in shot_media.values()),
    "screenshots_small": vc.count('"width":"460px"') == len(SCREENSHOTS),
    "lightbox_on": vc.count('"lightbox":{"enabled":true}') == 4 + len(SCREENSHOTS),
    "no_820_no_anchor": "820" not in vc and not re.search(r'<a href="[^"]*"><img', vc),
    "pullquotes_ge4": vc.count("wp:pullquote") // 2 >= 4,
    "all_posters_in_or_featured": all(
        (poster_media[n][1] in vc) or n == 1 for n in POSTERS),
    "no_em_dash": "—" not in vc,
    "quote_terrill": "I create like a journalist." in vc,
    "quote_elena": "You cannot be what you cannot see." in vc,
    "number_160k": "$160,000" in vc and "$160K" in vc,
    "number_che": "565,000 followers" in vc,
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == normalize_seo_meta(META_DESC),
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == normalize_seo_meta(SEO_TITLE),
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"{'updated' if UPDATE else 'created'} draft id={pid} status={post['status']}\n"
    f"preview={preview}\nedit={edit}\nfeatured(poster1)={FEATURED_ID}\n\n"
    "MEDIA:\n" + ("\n".join(media_log) if media_log else "(none)")
    + "\n\nVERIFY:\n" + json.dumps(checks, indent=2))
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK ' if val else 'FAIL'} {k}")
print(f"\nPREVIEW: {preview}\nEDIT:    {edit}\nDONE - left as DRAFT.")
