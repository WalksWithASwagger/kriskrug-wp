#!/usr/bin/env python3
"""Publish "Keep the Machine Strange" as a WordPress DRAFT on kriskrug.co.

Stdlib-only on top of scripts/common.py's verified WPClient (Basic auth + retry).
Reads content/drafts/2026-06-28-keep-the-machine-strange/post.md, converts the
marker syntax to Gutenberg blocks, uploads licensing-clean images (idempotent by
filename), and creates the draft. Dry-run by default; --execute creates; --update
refreshes the body of the existing draft. NEVER publishes (status stays draft).

Marker syntax in post.md (each marker is its own blank-line-delimited block):
  ## X / ### X            -> wp:heading (h2/h3)
  ---                     -> wp:separator
  >>> X [|| cite]         -> wp:pullquote (KK's punchy lines)
  QUOTE: X || cite        -> wp:quote with <cite> (verbatim, attributed source)
  YT: VIDEO_ID || caption -> wp:embed (YouTube, 16:9 responsive)
  ![alt](img:KEY)         -> wp:image resolved from IMAGES (downloaded + uploaded)
  - item / - item         -> wp:list (consecutive "- " lines)
  everything else         -> wp:paragraph
Inline: [text](url) (external gets target=_blank), **bold**, *italic*.

Images are downloaded from their source (Wikimedia) with attribution baked into
the figcaption, then uploaded once and reused on re-runs. The hero/featured image
is content/drafts/.../img/hero.png if present, else it falls back to the McLuhan
public-domain image so the OG/social card is never empty.
"""
import json
import pathlib
import re
import sys
import unicodedata
import urllib.request

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from common import WPClient, load_env, wp_credentials  # noqa: E402

ENV_PATH = "/Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.env"
STAGE = REPO_ROOT / "content/drafts/2026-06-28-keep-the-machine-strange"
EXECUTE = "--execute" in sys.argv
UPDATE = "--update" in sys.argv
WRITE = EXECUTE or UPDATE

TITLE = "Keep the Machine Strange: Technological Resistance in the Age of AI"
SLUG = "keep-the-machine-strange"
DATE = "2026-06-28T09:00:00"
CATEGORY_IDS = [1678, 1754]  # AI Ethics & Philosophy; Responsible AI & Policy
TAGS = ["Neil Postman", "Marshall McLuhan", "Technopoly", "Media Ecology",
        "Responsible AI", "AI Governance", "AI for All", "Both Hands Full",
        "Technological Resistance"]
SEO_TITLE = "Keep the Machine Strange: Neil Postman, AI, and Technological Resistance | Kris Krüg"
META_DESC = ("Neil Postman gave us a discipline for refusing technological inevitability. "
             "In the age of AI, technological resistance is not rejection. It is civic attention.")
EXCERPT = ("Neil Postman did not predict AI. He left us something more useful: a discipline for "
           "refusing to treat any technology as the weather. Here is what technological "
           "resistance looks like in 2026.")

# Licensing-clean images, downloaded from source then uploaded once. Attribution
# lives in the figcaption so CC BY terms are satisfied on the page itself.
IMAGES = {
    "mcluhan": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/Marshall_McLuhan_with_and_on_television_%28cropped%29.jpg",
        "file": "mcluhan-1967.jpg",
        "mime": "image/jpeg",
        "alt": "Marshall McLuhan leaning against a television set that displays his own face, 1967",
        "caption": "Marshall McLuhan, 1967. Photo by Bernard Gotfryd, Library of Congress (public domain).",
        "align": "center", "width": 620,
    },
    "gutenberg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Gutenberg%27s_vintage_printing_press_in_the_Gutenberg_Museum_in_Mainz%2C_Germany_%2848988497077%29.jpg",
        "file": "gutenberg-press.jpg",
        "mime": "image/jpeg",
        "alt": "A working replica of an early Gutenberg-style printing press at the Gutenberg Museum in Mainz",
        "caption": ('Gutenberg press replica, Gutenberg Museum, Mainz. Photo by dronepicr, '
                    '<a href="https://creativecommons.org/licenses/by/2.0/" target="_blank" '
                    'rel="noopener noreferrer">CC BY 2.0</a>.'),
        "align": "center", "width": 720,
    },
}
HERO_FILE = STAGE / "img" / "hero.png"  # optional Rafiki hero; falls back to mcluhan


def normalize_seo_meta(text: str) -> str:
    """NFC then drop combining marks (Jetpack SEO REST 500s on combining diacritics)."""
    nfc = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in nfc if not unicodedata.combining(ch))


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def inline(s: str) -> str:
    def link(m):
        text, url = m.group(1), m.group(2)
        extra = "" if url.startswith(("https://kriskrug.co", "/", "#")) else ' target="_blank" rel="noopener noreferrer"'
        return f'<a href="{url}"{extra}>{text}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def http_get(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kriskrug.co editorial bot)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def yt_ok(vid: str) -> bool:
    try:
        http_get(f"https://www.youtube.com/oembed?url=https://youtu.be/{vid}&format=json", timeout=20)
        return True
    except Exception:
        return False


# ---- blocks -----------------------------------------------------------------
def b_heading(text, level):
    attr = "" if level == 2 else ' {"level":3}'
    return f"<!-- wp:heading{attr} -->\n<h{level}>{inline(text)}</h{level}>\n<!-- /wp:heading -->"


def b_separator():
    return '<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->'


def b_list(items):
    lis = "".join(f"<!-- wp:list-item -->\n<li>{it}</li>\n<!-- /wp:list-item -->\n" for it in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">\n{lis}</ul>\n<!-- /wp:list -->'


def b_pullquote(text, cite=None):
    body = f"<p>{inline(text)}</p>" + (f"<cite>{inline(cite)}</cite>" if cite else "")
    return f'<!-- wp:pullquote -->\n<figure class="wp-block-pullquote"><blockquote>{body}</blockquote></figure>\n<!-- /wp:pullquote -->'


def b_quote(text, cite=None):
    body = f"<p>{inline(text)}</p>" + (f"<cite>{inline(cite)}</cite>" if cite else "")
    return f'<!-- wp:quote -->\n<blockquote class="wp-block-quote">{body}</blockquote>\n<!-- /wp:quote -->'


def b_youtube(vid, caption=None):
    url = f"https://www.youtube.com/watch?v={vid}"
    cap = f'<figcaption class="wp-element-caption">{inline(caption)}</figcaption>' if caption else ""
    return (
        '<!-- wp:embed {"url":"%s","type":"video","providerNameSlug":"youtube","responsive":true,'
        '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
        '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
        'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n%s\n'
        "</div>%s</figure>\n<!-- /wp:embed -->" % (url, url, cap)
    )


def b_image(media_id, url, alt, caption=None, width=None, align="center"):
    attrs = f'"id":{media_id},"sizeSlug":"large","linkDestination":"media","align":"{align}"'
    figcls = f"wp-block-image align{align} size-large"
    style = ""
    if width:
        attrs += f',"width":"{width}px"'
        figcls += " is-resized"
        style = f' style="width:{width}px"'
    img = f'<a href="{url}"><img src="{url}" alt="{alt}" class="wp-image-{media_id}"{style}/></a>'
    cap = f'<figcaption class="wp-block-image__caption">{caption}</figcaption>' if caption else ""
    return f'<!-- wp:image {{{attrs}}} -->\n<figure class="{figcls}">{img}{cap}</figure>\n<!-- /wp:image -->'


# ---- media upload (idempotent) ----------------------------------------------
def find_media(c, stem):
    try:
        r = c.get("media", params={"search": stem, "per_page": 10, "context": "edit"})
    except Exception:
        return None
    for m in r or []:
        base = m.get("source_url", "").rsplit("/", 1)[-1]
        if base.startswith(stem):
            return m["id"], m["source_url"]
    return None


def upload_media(c, path, alt, mime):
    found = find_media(c, path.stem)
    if found:
        print(f"   [media] REUSE {path.name} -> id={found[0]}")
        if alt:
            c.post(f"media/{found[0]}", {"alt_text": alt})
        return found
    data = path.read_bytes()
    req = urllib.request.Request(
        f"{c.base}/wp-json/wp/v2/media", data=data, method="POST",
        headers={"Authorization": c._auth,
                 "Content-Disposition": f'attachment; filename="{path.name}"',
                 "Content-Type": mime},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        media = json.loads(resp.read().decode())
    if alt:
        c.post(f"media/{media['id']}", {"alt_text": alt})
    print(f"   [media] NEW   {path.name} -> id={media['id']} {media['source_url']}")
    return media["id"], media["source_url"]


def ensure_term(c, taxonomy, name):
    hits = c.get(taxonomy, params={"search": name, "per_page": 50, "context": "edit"})
    for t in hits or []:
        if t.get("name", "").lower() == name.lower() or t.get("slug", "") == slugify(name):
            return t["id"]
    return c.post(taxonomy, {"name": name, "slug": slugify(name)})["id"]


# ---- load + verify post.md --------------------------------------------------
raw = (STAGE / "post.md").read_text(encoding="utf-8")
fm_end = raw.index("\n---", raw.index("---") + 3)
body = raw[fm_end + 4:]
assert "—" not in body, "em-dash leaked into post.md body"

base, user, pw = wp_credentials(load_env(ENV_PATH))
c = WPClient(base, user, pw)

# ---- verify YouTube embeds resolve ------------------------------------------
yt_ids = re.findall(r"^YT:\s*([A-Za-z0-9_-]{6,})", body, re.M)
print(f"[youtube] checking {len(yt_ids)} embeds")
for vid in yt_ids:
    print(f"   {'OK ' if yt_ok(vid) else 'FAIL'} {vid}")

# ---- download + (optionally) upload images ----------------------------------
(STAGE / "img").mkdir(parents=True, exist_ok=True)
resolved = {}
for key, meta in IMAGES.items():
    dest = STAGE / "img" / meta["file"]
    if not (dest.exists() and dest.stat().st_size > 0):
        dest.write_bytes(http_get(meta["url"]))
        print(f"[img] downloaded {key} -> {dest.name} ({dest.stat().st_size}b)")
    else:
        print(f"[img] cached     {key} -> {dest.name} ({dest.stat().st_size}b)")
    if WRITE:
        resolved[key] = upload_media(c, dest, meta["alt"], meta["mime"])
    else:
        resolved[key] = (0, f"DRYRUN/{meta['file']}")

# hero / featured
if HERO_FILE.exists() and HERO_FILE.stat().st_size > 0:
    FEATURED_ID = upload_media(c, HERO_FILE, "Keep the machine strange: technological resistance in the age of AI", "image/png")[0] if WRITE else 0
    print(f"[hero] using Rafiki hero {HERO_FILE.name} -> featured id={FEATURED_ID}")
else:
    FEATURED_ID = resolved["mcluhan"][0]
    print(f"[hero] no hero.png; falling back to McLuhan image as featured (id={FEATURED_ID})")

# ---- build blocks -----------------------------------------------------------
out = []
for blk in [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]:
    if blk == "---":
        out.append(b_separator())
    elif blk.startswith("### "):
        out.append(b_heading(blk[4:].strip(), 3))
    elif blk.startswith("## "):
        out.append(b_heading(blk[3:].strip(), 2))
    elif blk.startswith(">>> "):
        text, _, cite = blk[4:].partition(" || ")
        out.append(b_pullquote(text.strip(), cite.strip() or None))
    elif blk.startswith("QUOTE: "):
        text, _, cite = blk[7:].partition(" || ")
        out.append(b_quote(text.strip(), cite.strip() or None))
    elif blk.startswith("YT: "):
        vid, _, cap = blk[4:].partition(" || ")
        out.append(b_youtube(vid.strip(), cap.strip() or None))
    else:
        m = re.match(r"^!\[(.*?)\]\(img:([a-z0-9_-]+)\)$", blk)
        blk_lines = [ln.strip() for ln in blk.split("\n") if ln.strip()]
        if m:
            alt, key = m.group(1), m.group(2)
            mid, url = resolved[key]
            meta = IMAGES[key]
            out.append(b_image(mid, url, alt or meta["alt"], caption=meta.get("caption"),
                               width=meta.get("width"), align=meta.get("align", "center")))
        elif blk_lines and all(ln.startswith("- ") for ln in blk_lines):
            out.append(b_list([inline(ln[2:].strip()) for ln in blk_lines]))
        else:
            para = "<br>".join(inline(line.strip()) for line in blk.split("\n"))
            out.append(f"<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->")

content = "\n\n".join(out)
(STAGE / "post.html").write_text(content, encoding="utf-8")

# ---- sanity -----------------------------------------------------------------
assert "—" not in content, "em-dash leaked into content"
assert "](img:" not in content, "unresolved image marker"
assert "QUOTE:" not in content, "unresolved QUOTE marker"
n_h = content.count("<!-- wp:heading")
n_pq = content.count("<!-- wp:pullquote")
n_q = content.count("<!-- wp:quote")
n_em = content.count("<!-- wp:embed")
n_img = content.count("<!-- wp:image")
n_li = content.count("<!-- wp:list ")
print(f"[blocks] {len(out)} blocks | headings={n_h} pullquotes={n_pq} quotes={n_q} embeds={n_em} images={n_img} lists={n_li} | {len(content)}b staged")

if not WRITE:
    print("\nDRY-RUN complete. --execute creates the draft; --update refreshes the body.")
    sys.exit(0)

# ---- create / update draft (idempotent by slug, never publishes) -------------
hits = c.get("posts", params={"slug": SLUG, "status": "any", "context": "edit", "per_page": 5})
existing = hits[0] if isinstance(hits, list) and hits else None
author_id = int(load_env(ENV_PATH).get("WP_DEFAULT_AUTHOR_ID") or 18)

if UPDATE:
    if not existing:
        sys.exit(f"[ABORT] --update but no post with slug {SLUG}. Run --execute first.")
    pid = existing["id"]
    c.post(f"posts/{pid}", {"content": content, "featured_media": FEATURED_ID})
    print(f"[post] UPDATED draft id={pid}")
else:
    if existing:
        sys.exit(f"[ABORT] slug {SLUG} already exists (id={existing['id']}). Use --update.")
    tag_ids = [ensure_term(c, "tags", t) for t in TAGS]
    payload = {
        "title": TITLE, "slug": SLUG, "status": "draft", "date": DATE,
        "author": author_id, "content": content, "excerpt": EXCERPT,
        "categories": CATEGORY_IDS, "tags": tag_ids, "featured_media": FEATURED_ID,
        "meta": {"advanced_seo_description": normalize_seo_meta(META_DESC),
                 "jetpack_seo_html_title": normalize_seo_meta(SEO_TITLE)},
    }
    post = c.post("posts", payload)
    pid = post["id"]
    print(f"[post] CREATED draft id={pid} status={post['status']}")

# ---- readback ---------------------------------------------------------------
v = c.get(f"posts/{pid}", params={"context": "edit"})
vc = v["content"]["raw"]
checks = {
    "status_is_draft": v["status"] == "draft",
    "not_published": v["status"] != "publish",
    "featured_set": bool(v.get("featured_media")) and v.get("featured_media") == FEATURED_ID,
    "embeds_1": vc.count("wp:embed") == 2,            # one McLuhan embed; open+close
    "quotes_4": vc.count("<!-- wp:quote") == 4,
    "pullquotes_5plus": vc.count("<!-- wp:pullquote") >= 5,
    "images_2": vc.count("<!-- wp:image") == 2,
    "no_em_dash": "—" not in vc,
    "seo_title_meta": v.get("meta", {}).get("jetpack_seo_html_title") == normalize_seo_meta(SEO_TITLE),
    "seo_desc_meta": v.get("meta", {}).get("advanced_seo_description") == normalize_seo_meta(META_DESC),
    "links_canada": "canada-doesnt-need-a-bigger-ai-machine" in vc,
    "links_sovereign": "sovereign-ai-for-whom" in vc,
    "links_chat": "what-would-chat-do" in vc,
    "links_bothhands": "/2026/01/24/both-hands-full/" in vc,
    "cites_five_things": "neil-postman--five-things" in vc,
}
preview = f"{c.base}/?p={pid}&preview=true"
edit = f"{c.base}/wp-admin/post.php?post={pid}&action=edit"
(STAGE / "publish.log").write_text(
    f"{'updated' if UPDATE else 'created'} draft id={pid} status={v['status']}\n"
    f"preview={preview}\nedit={edit}\nfeatured={FEATURED_ID}\n\n" + json.dumps(checks, indent=2),
    encoding="utf-8")
print("\n=== VERIFY ===")
for k, val in checks.items():
    print(f"  {'OK  ' if val else 'FAIL'} {k}")
print(f"\nPREVIEW: {preview}\nEDIT:    {edit}\nDONE — left as DRAFT.")
