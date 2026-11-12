#!/usr/bin/env python3
"""Publish the theBreaker.news 460 recap ("AI Is Already a Campaign Issue in Vancouver").

Links are hand-placed in post.md; the auto-linker is NOT run. Staged images are
uploaded idempotently (find-or-reuse by filename) so re-runs don't duplicate media.
Existing library media are referenced by ID and never re-uploaded.

Dry-run by default. --execute creates the DRAFT. --update refreshes the body.
--publish flips an existing draft to published (separate, deliberate step).

Marker syntax in post.md:
  ## X                    -> wp:heading
  ---                     -> wp:separator
  >>> X                   -> wp:pullquote
  ![alt](media:ID)             -> existing library image, inline
  ![alt](stage:file)           -> staged image from images/, uploaded then inline
  ![alt](stage:file|caption)   -> same, with a caption line
  [[AUDIO:url]]                -> wp:audio player (streams from the source host)
  [[YOUTUBE:url]]              -> wp:embed responsive 16:9 video
  - item                       -> wp:list (consecutive lines in one block)
  everything else         -> wp:paragraph
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
from wp_blocks import inline, inline_image

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
STAGE = REPO_ROOT / "content" / "drafts" / "2026-09-07-breaker-460-ai-election-issue"
IMAGES = STAGE / "images"

MEDIA_RE = re.compile(r"^!\[(.*?)\]\(media:(\d+)\)$")
STAGE_RE = re.compile(r"^!\[(.*?)\]\(stage:([A-Za-z0-9._-]+)(?:\|(.*?))?\)$")
AUDIO_RE = re.compile(r"^\[\[AUDIO:(\S+)\]\]$")
YOUTUBE_RE = re.compile(r"^\[\[YOUTUBE:(\S+)\]\]$")
LIST_RE = re.compile(r"^- ", re.M)


def audio_block(url: str) -> str:
    """Native player pointed at the publisher's own stream endpoint.

    Nothing is rehosted: the file is served (and its play counted) by
    theBreaker's Seriously Simple Podcasting route, exactly as on their page.
    """
    return ('<!-- wp:audio -->\n'
            f'<figure class="wp-block-audio"><audio controls src="{url}"></audio></figure>\n'
            '<!-- /wp:audio -->')


def youtube_block(url: str) -> str:
    return ('<!-- wp:embed {"url":"' + url + '","type":"video",'
            '"providerNameSlug":"youtube","responsive":true,'
            '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
            '<figure class="wp-block-embed is-type-video is-provider-youtube '
            'wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
            f'<div class="wp-block-embed__wrapper">\n{url}\n</div></figure>\n'
            '<!-- /wp:embed -->')


def list_block(block: str) -> str:
    items = "".join(
        f"<!-- wp:list-item -->\n<li>{inline(line[2:].strip())}</li>\n<!-- /wp:list-item -->\n"
        for line in block.splitlines() if line.startswith("- ")
    )
    return f'<!-- wp:list -->\n<ul class="wp-block-list">\n{items}</ul>\n<!-- /wp:list -->' 

FLAGS = parse_publish_argv()
EXECUTE = FLAGS.execute
UPDATE = FLAGS.update
PUBLISH = "--publish" in sys.argv

TITLE = "AI Is Already a Campaign Issue in Vancouver"
SLUG = "ai-already-campaign-issue-vancouver"
DATE = "2026-09-07T09:00:00"
CATEGORY = "AI Policy"
TAGS = ["vancouver-ai", "civic-election", "data-centres", "bc-ai-ecosystem",
        "dave-olson", "thebreaker-news", "bob-mackin", "media-appearances"]
FEATURED_ID = 12098  # Vancouver AI data centre protest crowd, KK in frame

SEO_TITLE = "AI Is Already a Campaign Issue in Vancouver | Kris Krüg"
META_DESC = ("Bob Mackin asked if AI would sway B.C.'s civic elections. Council had already "
             "answered by punting the data centre past the October 17 vote. Two days later, "
             "every party in town had a position.")
SEO_META = build_seo_meta(SEO_TITLE, META_DESC)

cfg = load_wp_config()
wp = WordPress(cfg.base_url, cfg.user, cfg.app_password)

body = strip_frontmatter((STAGE / "post.md").read_text(encoding="utf-8"))
media_log: list[str] = []


def _existing(block, match):
    alt, mid = match.group(1), int(match.group(2))
    if not (EXECUTE or UPDATE):
        media_log.append(f"reuse  {mid} (dry-run, not fetched)")
        return inline_image(mid, f"DRYRUN/media-{mid}", alt, width=560)
    item = wp.get_media(mid)
    url = item["source_url"]
    media_log.append(f"reuse  {mid} {url}")
    return inline_image(mid, url, alt, width=560)


def _staged(block, match):
    alt, filename, caption = match.group(1), match.group(2), match.group(3)
    path = IMAGES / filename
    if not path.exists():
        raise SystemExit(f"[ABORT] staged image missing: {path}")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    mid, url = find_or_upload_media(
        wp, path, alt, mime=mime, write=(EXECUTE or UPDATE), log=media_log)
    return inline_image(mid, url, alt, caption=inline(caption) if caption else None,
                        width=560)


handlers = [
    (MEDIA_RE, _existing),
    (STAGE_RE, _staged),
    (AUDIO_RE, lambda block, match: audio_block(match.group(1))),
    (YOUTUBE_RE, lambda block, match: youtube_block(match.group(1))),
] + standard_text_handlers(pullquote_marker=True) + [
    (lambda block: block.startswith("- "), lambda block, match: list_block(block)),
]
content = "\n\n".join(render_marker_blocks(body, handlers))

print(f"[body] {len(content)} chars | "
      f"images={content.count('<!-- wp:image ')} "
      f"pullquotes={content.count('wp:pullquote') // 2} "
      f"headings={content.count('<!-- wp:heading')}")
assert "—" not in content, "em dash found in body"

if not EXECUTE and not UPDATE and not PUBLISH:
    print("\n=== DRY RUN, nothing written ===")
    for line in media_log:
        print("  " + line)
    print(f"\ntitle:  {TITLE}\nslug:   {SLUG}\nfeatured: {FEATURED_ID}")
    print(f"seo:    {SEO_TITLE}")
    (STAGE / "dry-run-body.html").write_text(content, encoding="utf-8")
    print(f"body preview written to {STAGE / 'dry-run-body.html'}")
    sys.exit(0)

existing = find_existing_post_by_slug(wp, SLUG)

if PUBLISH:
    if not existing:
        raise SystemExit(f"[ABORT] no post with slug {SLUG}; create the draft first")
    pid = existing["id"]
    post = wp.update_post(pid, {"status": "publish"}, expected_slug=SLUG)
    print(f"[post] PUBLISHED id={pid} status={post['status']}")
elif existing:
    pid = existing["id"]
    payload = {"content": content, "excerpt": META_DESC,
               "featured_media": FEATURED_ID, "meta": SEO_META}
    post = wp.update_post(pid, payload, expected_slug=SLUG)
    print(f"[post] UPDATED id={pid} status={post['status']}")
else:
    cat_id = wp.ensure_term("categories", CATEGORY)
    tag_ids = [wp.ensure_term("tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
        "author": cfg.author_id, "content": content, "excerpt": META_DESC,
        "categories": [cat_id], "tags": tag_ids, "featured_media": FEATURED_ID,
        "meta": SEO_META,
    }
    post = wp.create_post(payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

v = wp.get_post(pid)
vc = v["content"]["raw"]
checks = {
    "featured_set": v.get("featured_media") == FEATURED_ID,
    "four_images": vc.count("<!-- wp:image ") == 4,
    "lightbox_on": vc.count('"lightbox":{"enabled":true}') == 4,
    "audio_embedded": "<!-- wp:audio -->" in vc and "podcast-player/15764" in vc,
    "audio_not_rehosted": "kriskrug.co/wp-content/uploads" not in vc.split(
        "<!-- wp:audio -->")[1].split("<!-- /wp:audio -->")[0],
    "youtube_embedded": '"providerNameSlug":"youtube"' in vc and "fSbIJO0K-8o" in vc,
    "mackin_credited": "Bob Mackin" in vc and "theBreaker.news" in vc,
    "bcai_links_ge5": vc.count("https://bc-ai.ca/news/") >= 5,
    "public_compute_hub_linked": vc.count("https://bc-ai.ca/public-compute") == 1,
    "no_public_compute_subpages": not re.search(
        r"bc-ai\.ca/public-compute/", vc),
    "kruug_spelled_right": "Kris Krug" not in vc,
    "no_bcai_net": "bc-ai.net" not in vc,
    "further_reading_lists": vc.count("<!-- wp:list -->") == 2,
    "pullquotes_ge5": vc.count("wp:pullquote") // 2 >= 5,
    "no_em_dash": "—" not in vc,
    "no_820_no_anchor": "820" not in vc and not re.search(r'<a href="[^"]*"><img', vc),
    "breaker_linked": "thebreaker.news/opinion/podcast-460/" in vc,
    "tyee_scorecard_linked": "Where-Vancouver-Parties-Stand-AI" in vc,
    "tyee_movement_linked": "Vancouver-Growing-Anti-AI-Movement" in vc,
    "dave_correct_domain": "daveostory.com" in vc and "daveolson.ca" not in vc,
    "oct_17_present": "October 17" in vc,
    "no_meetup_number": not re.search(r"[Mm]eetup #?3[12]", vc),
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == SEO_TITLE,
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == META_DESC,
}
preview = f"{wp.base}/?p={pid}&preview=true"
edit = f"{wp.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"id={pid} status={v['status']}\npreview={preview}\nedit={edit}\n"
    f"featured={FEATURED_ID}\n\nMEDIA:\n" + "\n".join(media_log)
    + "\n\nVERIFY:\n" + json.dumps(checks, indent=2), encoding="utf-8")
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK  ' if val else 'FAIL'} {k}")
print(f"\nSTATUS:  {v['status']}\nPREVIEW: {preview}\nEDIT:    {edit}")
