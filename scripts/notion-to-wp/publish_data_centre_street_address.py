#!/usr/bin/env python3
"""Stage "The Data Centre Has a Street Address" (SFU Bridging the Political
Divide dialogue, 2026-11-26) as a WordPress post on kriskrug.co.

Dry-run by default. --execute creates the DRAFT; --update refreshes the
existing draft's body, terms, excerpt and featured image. --publish flips the
slug-verified post to publish (KK's explicit go only).

Marker syntax in post.md (an image or video caption is the block's 2nd line,
wrapped in *...*):
  ## X / >>> X / ---                 -> heading / pullquote / separator
  ![alt](media:ID)                   -> reuse existing kriskrug.co media
  ![alt](file:NAME)                  -> upload images/NAME (idempotent by stem)
  https://www.youtube.com/watch?v=ID -> core YouTube embed
  - item lines                       -> wp:list
  <!-- ... -->                       -> dropped (editor notes)
"""

import json
import pathlib
import re
import sys

from kk_notion_to_wp import WordPress, load_config
from wp_blocks import image, inline
from publish_common import (
    build_seo_meta,
    find_existing_post_by_slug,
    find_or_upload_media,
    parse_publish_argv,
    render_marker_blocks,
    standard_text_handlers,
    strip_frontmatter,
)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
STAGE = (
    SCRIPT_DIR.parents[1]
    / "content"
    / "drafts"
    / "2026-11-26-the-data-centre-has-a-street-address"
)
IMAGES = STAGE / "images"
FLAGS = parse_publish_argv()
PUBLISH = "--publish" in sys.argv[1:]
WRITE = FLAGS.write or PUBLISH

TITLE = "The Data Centre Has a Street Address"
SLUG = "the-data-centre-has-a-street-address"
CATEGORY_IDS = [1754]  # Responsible AI & Policy
EXISTING_TAG_IDS = [
    1683,
    1704,
    289,
    1843,
    1810,
]  # both-hands-full, data-centres, vancouver, bc-politics, civic-election
NEW_TAGS = ["Democracy"]
EXCERPT = (
    "A day at SFU's Bridging the Political Divide dialogue, a month after BC voted in two "
    "directions at once. My own snark, why the data centre fight is really about agency, "
    "and what it would take to build a table people trust."
)
SEO_META = build_seo_meta(
    "The Data Centre Has a Street Address | Kris Krüg",
    "Notes from SFU's Bridging the Political Divide dialogue: anger as a map to your values, "
    "why the data centre fight is about agency, and how to build a table people trust.",
)
HERO = (
    "data-centre-street-address-hero.jpg",
    "The words The data centre has a street address above a protest banner reading "
    "Let's demand more transparency around LLMs, AI and tech.",
)

MEDIA_RE = re.compile(r"^!\[(.+?)\]\(media:(\d+)\)(?:\n\*(.+)\*)?$", re.S)
FILE_RE = re.compile(r"^!\[(.+?)\]\(file:([\w.-]+)\)(?:\n\*(.+)\*)?$", re.S)
YT_RE = re.compile(
    r"^(https://www\.youtube\.com/watch\?v=[\w-]+)(?:&t=\d+s)?(?:\n\*(.+)\*)?$", re.S
)

raw = (STAGE / "post.md").read_text()
body = strip_frontmatter(raw)
assert "—" not in raw, "em dash in post.md"

cfg = load_config()
wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)
media_log = []


def existing_media(mid):
    r = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/media/{mid}",
        params={"_fields": "id,source_url"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["source_url"]


def upload(name, alt):
    return find_or_upload_media(
        wp,
        IMAGES / name,
        alt,
        mime="image/jpeg",
        write=WRITE,
        label=name,
        log=media_log,
    )


def image_block(_block, m, url_for):
    alt, ref, cap = m.group(1), m.group(2), m.group(3)
    mid, url = url_for(ref, alt)
    return image(mid, url, alt, caption=inline(cap) if cap else None)


def yt_block(_block, m):
    url, cap = m.group(1), m.group(2)
    figcap = (
        f'<figcaption class="wp-element-caption">{inline(cap)}</figcaption>'
        if cap
        else ""
    )
    attrs = json.dumps(
        {
            "url": url,
            "type": "video",
            "providerNameSlug": "youtube",
            "responsive": True,
            "className": "wp-embed-aspect-16-9 wp-has-aspect-ratio",
        }
    )
    return (
        f"<!-- wp:embed {attrs} -->\n"
        '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
        'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n'
        f"{url}\n</div>{figcap}</figure>\n<!-- /wp:embed -->"
    )


def list_block(block, _m):
    items = "".join(
        f"<!-- wp:list-item -->\n<li>{inline(line[2:].strip())}</li>\n<!-- /wp:list-item -->"
        for line in block.split("\n")
    )
    return (
        f'<!-- wp:list -->\n<ul class="wp-block-list">{items}</ul>\n<!-- /wp:list -->'
    )


hero_id, hero_url = upload(*HERO)
out = render_marker_blocks(
    body,
    standard_text_handlers(h3=False, pullquote_marker=True)
    + [
        (lambda b: b.startswith("<!--"), lambda b, m: None),
        (
            MEDIA_RE,
            lambda b, m: image_block(
                b, m, lambda ref, alt: (int(ref), existing_media(ref))
            ),
        ),
        (FILE_RE, lambda b, m: image_block(b, m, lambda ref, alt: upload(ref, alt))),
        (YT_RE, yt_block),
        (lambda b: all(line.startswith("- ") for line in b.split("\n")), list_block),
    ],
)
content = "\n\n".join(out)
(STAGE / "post.html").write_text(content)

n_img = content.count("<!-- wp:image ")
n_vid = content.count("<!-- wp:embed ")
assert (
    "—" not in content
    and "media:" not in content
    and "file:" not in content
    and "<!-- PHOTO" not in content
)
assert "HERO" not in content and "Title and slug locked" not in content, (
    "editor note leaked"
)
assert n_img == 9, f"expected 9 in-body images, got {n_img}"
assert n_vid == 2, f"expected 2 videos, got {n_vid}"
print(
    f"[blocks] {len(out)} blocks | images={n_img} videos={n_vid} "
    f"pullquotes={content.count('wp:pullquote') // 2} h2={content.count('<h2')} lists={content.count('<!-- wp:list -->')}"
)
for line in media_log:
    print("   " + line)

if not WRITE:
    print(
        "\nDRY-RUN complete. --execute creates the draft; --update refreshes it; --publish goes live."
    )
    sys.exit(0)

existing = find_existing_post_by_slug(wp, SLUG)
if PUBLISH:
    if not existing:
        sys.exit(f"[ABORT] --publish but no post with slug {SLUG}.")
    post = wp.update_post(existing["id"], {"status": "publish"}, expected_slug=SLUG)
    pid = post["id"]
    print(f"[post] PUBLISHED id={pid} link={post['link']}")
else:
    tag_ids = EXISTING_TAG_IDS + [wp.ensure_term("tags", t) for t in NEW_TAGS]
    fields = {
        "content": content,
        "excerpt": EXCERPT,
        "categories": CATEGORY_IDS,
        "tags": tag_ids,
        "featured_media": hero_id,
        "meta": SEO_META,
    }
    if FLAGS.update:
        if not existing:
            sys.exit(
                f"[ABORT] --update but no post with slug {SLUG}. Run --execute first."
            )
        post = wp.update_post(existing["id"], fields, expected_slug=SLUG)
        print(f"[post] UPDATED id={post['id']} status={post['status']}")
    else:
        if existing:
            sys.exit(
                f"[ABORT] slug {SLUG} already exists (id={existing['id']}). Use --update."
            )
        post = wp.create_post(
            {
                "title": TITLE,
                "slug": SLUG,
                "status": "draft",
                "author": cfg.wp_author_id,
                **fields,
            }
        )
        print(f"[post] CREATED draft id={post['id']}")
    pid = post["id"]

v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "slug": v["slug"] == SLUG,
    "status": v["status"] == ("publish" if PUBLISH else "draft"),
    "featured": v.get("featured_media") == hero_id,
    "images": vc.count("<!-- wp:image ") == 9,
    "videos": vc.count("<!-- wp:embed ") == 2,
    "no_em_dash": "—" not in vc,
    "seo_title": v.get("meta", {}).get("jetpack_seo_html_title")
    == SEO_META["jetpack_seo_html_title"],
    "seo_desc": v.get("meta", {}).get("advanced_seo_description")
    == SEO_META["advanced_seo_description"],
}
(STAGE / "publish.log").write_text(
    f"id={pid} status={v['status']} link={v.get('link')}\nfeatured={hero_id} {hero_url}\n\nMEDIA:\n"
    + "\n".join(media_log)
    + "\n\nVERIFY:\n"
    + json.dumps(checks, indent=2)
)
for k, ok in checks.items():
    print(f"  {'OK ' if ok else 'FAIL'} {k}")
print(
    f"\nPREVIEW: {wp.base}/?p={pid}&preview=true\nEDIT:    {wp.base}/wp-admin/post.php?post={pid}&action=edit"
)
if not all(checks.values()):
    sys.exit(1)
