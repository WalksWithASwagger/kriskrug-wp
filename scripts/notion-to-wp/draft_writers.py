from __future__ import annotations

import re
from pathlib import Path


def html_to_md_preview(html: str) -> str:
    s = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    s = re.sub(r"</?p>", "\n\n", s)
    s = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n", s, flags=re.S)
    s = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n", s, flags=re.S)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def write_seo_meta(draft_dir: Path, fm: dict, seo_title: str, meta_desc: str):
    body = f"""# SEO snapshot — {fm['title']}

| Field | Value |
|---|---|
| Visible title (H1) | {fm['title']} |
| SEO title (`<title>`) | {seo_title} |
| Slug | `{fm['slug']}` (permalink `/{fm['post_date'][:4]}/{fm['post_date'][5:7]}/{fm['post_date'][8:10]}/{fm['slug']}/`) |
| Meta description | {meta_desc} |
| Category | {fm['categories'][0]} |
| Tags | {", ".join(fm['tags']) or "(none)"} |
| Excerpt | {fm['excerpt'][:200]} |
| Featured | {"YES" if fm.get('featured') else "no"} |
| Schema | Article (auto via kk-schema mu-plugin if deployed) |
| OG image | featured image |
| Twitter Card | summary_large_image (Jetpack default) |

## Next-step checks after publish

- View source on the live URL → confirm `<meta name="description">` matches above
- https://search.google.com/test/rich-results → confirm Article + Person schema if mu-plugin live
- https://cards-dev.twitter.com/validator → preview card
- Submit URL in Google Search Console for instant indexing
"""
    (draft_dir / "seo-meta.md").write_text(body, encoding="utf-8")


def write_alt_text(draft_dir: Path, image_map: dict, locals_: list[Path]):
    rows = []
    seen = set()
    for nurl, meta in image_map.items():
        lp = meta.get("_local_path")
        if not lp or lp in seen:
            continue
        seen.add(lp)
        rows.append(f"- **{Path(lp).name}** — alt: \"{meta['alt'] or '(empty — needs human-written alt)'}\"")
    body = "# Image alt text\n\n" + ("\n".join(rows) if rows else "(no images)") + """

Replace any "(empty — needs human-written alt)" lines with descriptive sentences. Good alt text:
- Describes what's in the image, not what you want it to mean
- Includes context the reader can't get from surrounding prose
- Is under 125 characters where possible
- Uses natural language, not keyword stuffing
"""
    (draft_dir / "alt-text.md").write_text(body, encoding="utf-8")


def write_internal_links(draft_dir: Path, html: str):
    urls = re.findall(r'href="([^"]+)"', html)
    internal = sorted({u for u in urls if "kriskrug.co" in u or u.startswith("/")})
    external = sorted({u for u in urls if u not in internal and u.startswith("http")})
    body = f"""# Link audit

## Internal links ({len(internal)})

""" + "\n".join(f"- {u}" for u in internal) + f"""

## External links ({len(external)})

""" + "\n".join(f"- {u}" for u in external) + """

After publish, click-check every internal link in the live post. External links should open in a new tab with rel="noopener noreferrer" (the connector sets these automatically).
"""
    (draft_dir / "internal-links.md").write_text(body, encoding="utf-8")
