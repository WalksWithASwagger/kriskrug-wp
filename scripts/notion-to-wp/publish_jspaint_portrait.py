#!/usr/bin/env python3
"""Publish "I Made Claude Paint My Portrait in MS Paint. No Scripts."

Links are hand-placed in post.md; the auto-linker is NOT run. Staged media are
uploaded idempotently (find-or-reuse by filename stem) so re-runs never
duplicate. The timelapse MP4 is self-hosted, postered with the finished
portrait so the top of the post is not a black rectangle.

Category IDs are pinned, not resolved by name. The live "Creative Technology &
Making" term comes back from REST HTML-encoded ("&amp;"), so ensure_term's name
branch misses it and only the slug branch saves you. Pinning removes the chance
of silently creating a duplicate category on production.

Dry-run by default. --execute creates the DRAFT. --update refreshes the body.
--publish flips an existing draft to published (separate, deliberate step).

Marker syntax in post.md:
  ## X                      -> wp:heading
  >>> X                     -> wp:pullquote
  - item                    -> wp:list (consecutive lines in one block)
  [[VIDEO]]                 -> self-hosted wp:video, postered, controls, no autoplay
  [[GALLERY-BEFORE-AFTER]]  -> 2-up wp:gallery, the state the history ends on vs final
  everything else           -> wp:paragraph
"""

import json
import pathlib
import re
import sys

from create_local_wp_draft import load_wp_config
from kk_notion_to_wp import WordPress
from publish_common import (
    build_seo_meta,
    find_existing_post_by_slug,
    find_or_upload_media,
    parse_publish_argv,
    render_marker_blocks,
    standard_text_handlers,
    strip_frontmatter,
)
from wp_blocks import gallery, inline, video

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
STAGE = REPO_ROOT / "content" / "drafts" / "2026-09-27-claude-painted-my-portrait"
IMAGES = STAGE / "images"

VIDEO_RE = re.compile(r"^\[\[VIDEO\]\]$")
BEFORE_AFTER_RE = re.compile(r"^\[\[GALLERY-BEFORE-AFTER\]\]$")

FLAGS = parse_publish_argv()
EXECUTE = FLAGS.execute
UPDATE = FLAGS.update
PUBLISH = "--publish" in sys.argv
WRITE = EXECUTE or UPDATE

TITLE = "I Made Claude Paint My Portrait in MS Paint. No Scripts."
SLUG = "claude-painted-my-portrait-ms-paint"
DATE = "2026-09-27T09:00:00"

# Pinned live term IDs (verified 2026-09-27 against /wp-json/wp/v2/categories).
CATEGORY_IDS = {1665: "ai-creatives", 1755: "creative-technology-making"}
TAGS = ["claude", "jspaint", "portraiture", "ai-collaboration", "creative-process"]

# Hero: the painting is a 600x600 square, so it cannot be the featured image on
# its own. img/hero-c2-wash.png mats it onto a 1600x900 ground at 780px with
# 60px of vertical margin, because the 1.91:1 OG crop eats 31px top and bottom
# and the first cut (square at full 900 height) decapitated the beanie.
# featured-image-forge gates + all four crop previews checked 2026-09-27.
# Alternate candidate kept at img/hero-a2-blurfill.png. Swap is one line.
HERO = "hero-c2-wash.png"

SEO_TITLE = "I Made Claude Paint My Portrait in MS Paint. No Scripts. | Kris Krüg"
META_DESC = (
    "Four sessions, a hand mixed palette, and one rule: brushes and clicking only. "
    "No scripting the canvas. The failures taught me more than the finished picture did."
)
SEO_META = build_seo_meta(SEO_TITLE, META_DESC)

MEDIA = {
    "timelapse": (
        "jspaint-portrait-timelapse.mp4",
        "video/mp4",
        "Timelapse of a portrait of Kris Krüg being painted stroke by stroke in JSPaint",
    ),
    "final": (
        "jspaint-portrait-final.png",
        "image/png",
        "Finished JSPaint portrait of Kris Krüg in a black beanie with a large auburn beard, "
        "warm orange rim light on the left and cyan rim light on the right",
    ),
    "before": (
        "jspaint-portrait-before-last-rounds.png",
        "image/png",
        "The same JSPaint portrait at the state the recorded undo history ends on, "
        "with a flatter beard and hard edged background glows",
    ),
    "hero": (
        HERO,
        "image/png",
        "Finished JSPaint portrait of Kris Kr\u00fcg on a dark ground, warm glow "
        "to the left and cool cyan glow to the right",
    ),
}
HERO_DIR = STAGE / "img"

cfg = load_wp_config()
wp = WordPress(cfg.base_url, cfg.user, cfg.app_password)

body = strip_frontmatter((STAGE / "post.md").read_text(encoding="utf-8"))
media_log: list[str] = []
resolved: dict[str, tuple[int, str]] = {}


def _resolve(key: str) -> tuple[int, str]:
    """Upload-or-reuse one staged file, memoised so markers can share results."""
    if key in resolved:
        return resolved[key]
    filename, mime, alt = MEDIA[key]
    path = (HERO_DIR if key == "hero" else IMAGES) / filename
    if not path.exists():
        raise SystemExit(f"[ABORT] staged media missing: {path}")
    mid, url = find_or_upload_media(
        wp,
        path,
        alt,
        mime=mime,
        write=WRITE,
        log=media_log,
        extensions=(path.suffix.lower(),),
    )
    resolved[key] = (mid, url)
    return mid, url


def _video_block(block, match) -> str:
    vid, vurl = _resolve("timelapse")
    _, poster_url = _resolve("final")
    return video(
        vid or None,
        vurl,
        poster=poster_url,
        controls=True,
        autoplay=False,
        caption=inline(
            "834 frames of real brush strokes out of JSPaint's own undo history, "
            "then a dissolve into the finished portrait. The two sessions in between "
            "were lost with the tab."
        ),
    )


def _before_after(block, match) -> str:
    bid, burl = _resolve("before")
    fid, furl = _resolve("final")
    return gallery(
        [
            (
                bid or None,
                burl,
                MEDIA["before"][2],
                "Where the recorded history stops.",
            ),
            (fid or None, furl, MEDIA["final"][2], "Where it actually ended up."),
        ],
        columns=2,
    )


def list_block(block: str) -> str:
    items = "".join(
        f"<!-- wp:list-item -->\n<li>{inline(line[2:].strip())}</li>\n<!-- /wp:list-item -->\n"
        for line in block.splitlines()
        if line.startswith("- ")
    )
    return (
        f'<!-- wp:list -->\n<ul class="wp-block-list">\n{items}</ul>\n<!-- /wp:list -->'
    )


handlers = (
    [
        (VIDEO_RE, _video_block),
        (BEFORE_AFTER_RE, _before_after),
    ]
    + standard_text_handlers(pullquote_marker=True)
    + [
        (lambda block: block.startswith("- "), lambda block, match: list_block(block)),
    ]
)
content = "\n\n".join(render_marker_blocks(body, handlers))

print(
    f"[body] {len(content)} chars | "
    f"video={content.count('<!-- wp:video ')} "
    f"images={content.count('<!-- wp:image ')} "
    f"pullquotes={content.count('wp:pullquote') // 2} "
    f"headings={content.count('<!-- wp:heading')} "
    f"lists={content.count('<!-- wp:list -->')}"
)
assert "—" not in content, "em dash found in body"

if not WRITE and not PUBLISH:
    print("\n=== DRY RUN, nothing written ===")
    for line in media_log:
        print("  " + line)
    print(f"\ntitle:    {TITLE}\nslug:     {SLUG}")
    print(f"cats:     {sorted(CATEGORY_IDS)}  {list(CATEGORY_IDS.values())}")
    print(f"tags:     {TAGS}")
    print(f"featured: {HERO} (featured-image-forge gates + 4 crops checked)")
    print(f"seo:      {SEO_TITLE}")
    (STAGE / "dry-run-body.html").write_text(content, encoding="utf-8")
    print(f"\nbody preview written to {STAGE / 'dry-run-body.html'}")
    sys.exit(0)

# Guard the pinned IDs against term drift before writing anything.
for cid, want_slug in CATEGORY_IDS.items():
    got = wp.s.get(f"{wp.base}/wp-json/wp/v2/categories/{cid}", timeout=30)
    got.raise_for_status()
    got_slug = got.json().get("slug")
    if got_slug != want_slug:
        raise SystemExit(
            f"[ABORT] category {cid} is '{got_slug}', expected '{want_slug}'"
        )

hero_id, _ = _resolve("hero")

existing = find_existing_post_by_slug(wp, SLUG)

if PUBLISH:
    if not existing:
        raise SystemExit(f"[ABORT] no post with slug {SLUG}; create the draft first")
    pid = existing["id"]
    post = wp.update_post(pid, {"status": "publish"}, expected_slug=SLUG)
    print(f"[post] PUBLISHED id={pid} status={post['status']}")
elif existing:
    pid = existing["id"]
    payload = {"content": content, "excerpt": META_DESC, "meta": SEO_META,
               "featured_media": hero_id}
    post = wp.update_post(pid, payload, expected_slug=SLUG)
    print(f"[post] UPDATED id={pid} status={post['status']}")
else:
    tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
    payload = {
        "title": TITLE,
        "slug": SLUG,
        "status": "draft",
        "date": DATE,
        "author": cfg.author_id,
        "content": content,
        "excerpt": META_DESC,
        "categories": sorted(CATEGORY_IDS),
        "tags": tag_ids,
        "meta": SEO_META,
        "featured_media": hero_id,
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

v = wp.get_post(pid)
vc = v["content"]["raw"]
vid_id, vid_url = resolved.get("timelapse", (0, ""))
checks = {
    "is_draft": v["status"] == "draft",
    "one_video": vc.count("<!-- wp:video ") == 1,
    "video_self_hosted": "/wp-content/uploads/" in vid_url,
    "video_postered": 'poster="' in vc and ".png" in vc.split('poster="')[1][:200],
    # The block attrs always carry "autoplay":false, so assert on the element.
    "video_no_autoplay": "autoplay" not in re.search(r"<video[^>]*>", vc).group(0),
    "two_gallery_images": vc.count("<!-- wp:image ") == 2,
    "lightbox_on": vc.count('"lightbox":{"enabled":true}') == 2,
    "pullquotes_eq3": vc.count("wp:pullquote") // 2 == 3,
    "headings_ge5": vc.count("<!-- wp:heading") >= 5,
    "jspaint_credited": "isaiahodhner.io" in vc and "Isaiah Odhner" in vc,
    "jspaint_linked": "https://jspaint.app" in vc,
    "claude_linked": "claude.com/claude-code" in vc,
    "autolume_crosslink": "autolume-post-photographic-cybernetic-portraiture" in vc,
    "montreal_crosslink": "all-in-montreal-robot-mirror" in vc,
    "kruug_spelled_right": "Kris Krug" not in vc,
    "no_em_dash": "—" not in vc,
    "cats_pinned": sorted(v.get("categories", [])) == sorted(CATEGORY_IDS),
    "featured_is_hero": v.get("featured_media") == hero_id,
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == SEO_TITLE,
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == META_DESC,
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"id={pid} status={v['status']}\npreview={preview}\nedit={edit}\n"
    f"featured={v.get('featured_media')}\n\nMEDIA:\n"
    + "\n".join(media_log)
    + "\n\nVERIFY:\n"
    + json.dumps(checks, indent=2),
    encoding="utf-8",
)
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK  ' if val else 'FAIL'} {k}")
print(f"\nSTATUS:  {v['status']}\nPREVIEW: {preview}\nEDIT:    {edit}")
