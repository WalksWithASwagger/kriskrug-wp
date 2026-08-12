#!/usr/bin/env python3
"""Verify the Futureproof v2 article package without changing WordPress."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

EXPECTED_TITLE = "Futureproof Festival of AI: A Bat Signal from Vancouver"
EXPECTED_SEO_TITLE = "Futureproof Festival of AI in Vancouver | Kris Krüg"
EXPECTED_SLUG = "futureproof-festival-announcement"
EXPECTED_POST_DATE = "2026-08-11"

CRITICAL_CONTENT = {
    "https://bc-ai.ca/events/vancouver-ai-meetup-2026-07": "Vancouver AI Meetup",
    "https://bc-ai.ca/news/futureproof-festival-regional-story-national-invitation": "Futureproof Festival",
    "https://kriskrug.co/vancouver-ai/": "Vancouver AI Ecosystem",
    "https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/": "Zero to One",
    "https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/": "DENT the Future",
    "https://kriskrug.co/ai-events/": "AI Events",
    "https://mediashift.org/2010/02/true-north-media-house-w2-provide-citizen-media-hub-at-olympics053/": "True North Media House",
    "https://blog.ted.com/what-does-tedx-mean-to-me-answering-tedxsummit-photographer-kris-krug/": "TEDxSummit photographer",
    "https://www.spacecentre.ca/": "H.R. MacMillan Space Centre",
    "https://www.futureproof.website/": "Futureproof Festival of AI",
    "https://www.futureproof.website/tickets/": "Festival Pass",
    "https://www.futureproof.website/call-for-talks/": "Call for Talks",
    "https://www.futureproof.website/startup-exhibitors/": "Startup Exhibitor",
    "https://www.futureproof.website/sponsors/": "Partner with",
    "https://www.futureproof.website/speakers/": "Speakers",
    "https://www.futureproof.website/venues/": "H.R. MacMillan Space Centre",
}

EXPECTED_IMAGE_SIZES = {
    "futureproof-salmon-starfield-share-20260711.jpg": (1200, 630),
    "vanai-meetup31-stage-kris-futureproof-slide.webp": (2400, 1600),
    "vanai-meetup31-community-group-photo.webp": (2400, 1600),
    "receipt-true-north-media-house.png": (1440, 900),
    "receipt-tedx-summit-kris-krug.png": (1440, 900),
    "receipt-dent-kris-krug.png": (1440, 900),
    "vanai-space-centre-courtyard-community.webp": (1800, 1200),
    "space-centre-community-night.webp": (1800, 1200),
    "futureproof-honest-conversation-poster.png": (1024, 1536),
}
EXPECTED_MEDIA_IDS = {
    "futureproof-salmon-starfield-share-20260711.jpg": 12739,
    "vanai-meetup31-stage-kris-futureproof-slide.webp": 12725,
    "vanai-meetup31-community-group-photo.webp": 12733,
    "receipt-true-north-media-house.png": 12734,
    "receipt-tedx-summit-kris-krug.png": 12735,
    "receipt-dent-kris-krug.png": 12736,
    "vanai-space-centre-courtyard-community.webp": 12737,
    "space-centre-community-night.webp": 12738,
    "futureproof-honest-conversation-poster.png": 12727,
}
EXPECTED_IMAGE_HASHES = {
    "futureproof-salmon-starfield-share-20260711.jpg": "68ecc3c42b32857916e5d62c7ac30efe5bfc387bb2614045abb42791121dfc08",
    "vanai-meetup31-stage-kris-futureproof-slide.webp": "4f2c77c776e54174b08b69a3e41cca4d954ffdb17149c59928ff04ab497e0647",
    "vanai-meetup31-community-group-photo.webp": "e3d58e4b17ebcd8e20d673ea5b21a0f2abc3afdeb202000f4c3617bb916a6360",
    "receipt-true-north-media-house.png": "bd630687fd16a0d4ef4507f1087c8be7f5abcadfe803f20926ae4b40a152390b",
    "receipt-tedx-summit-kris-krug.png": "a7c864d3b2f5369261abd320ed3c00eb1db9e3b7bfbf8024d07bf558d12969a6",
    "receipt-dent-kris-krug.png": "7d02497cfd2a4dc3ed82e6c2d5b04c5cc18fd1fd6b517bf9feb6945dedbe27c8",
    "vanai-space-centre-courtyard-community.webp": "1bfe958b5ed5ad29a9f159032f5456fb1db18607d1d2e3a1e8252432bc9e7015",
    "space-centre-community-night.webp": "b611a54de56815613bee5823413b67a39a620c1217e74e6c9e0be1ba3049dc26",
    "futureproof-honest-conversation-poster.png": "01fdaa144ff92bfa7a7cbd4155714c91a12c550194b3771438f790ef27258a7f",
}


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        raise ValueError("post.md has no YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def editorial_urls(body: str) -> list[str]:
    urls: list[str] = []
    for url in re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", body):
        if url not in urls:
            urls.append(url)
    return urls


def check_url(session: requests.Session, url: str) -> dict:
    response = session.get(url, timeout=30, allow_redirects=True)
    response.raise_for_status()
    text = response.text
    expected = CRITICAL_CONTENT.get(url)
    if expected and expected.casefold() not in text.casefold():
        raise AssertionError(f"{url} returned 200 but did not contain {expected!r}")
    lowered = text.casefold()
    if "domain for sale" in lowered or "buy this domain" in lowered:
        raise AssertionError(f"{url} resolves to a parked-domain page")
    return {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "expected_content": expected,
        "content_verified": bool(expected),
    }


def image_artifact_report(draft_dir: Path) -> dict:
    manifest_path = draft_dir / "asset-manifest.md"
    manifest = manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else ""
    current_manifest = manifest.split("## #500 WordPress receipt", 1)[0]
    manifest_receipts = all(
        f"`{name}`" in current_manifest
        and f"{width}×{height}" in current_manifest
        and f"| `{name}` | {EXPECTED_MEDIA_IDS[name]} |" in current_manifest
        and EXPECTED_IMAGE_HASHES[name] in current_manifest
        for name, (width, height) in EXPECTED_IMAGE_SIZES.items()
    )

    paths = {name: draft_dir / "images" / name for name in EXPECTED_IMAGE_SIZES}
    present = {name: path for name, path in paths.items() if path.exists()}
    expected_count = len(paths)
    present_count = len(present)
    hashes_match = all(
        hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED_IMAGE_HASHES[name]
        for name, path in present.items()
    )
    local_state_valid = present_count in (0, expected_count) and hashes_match
    return {
        "manifest_receipts": manifest_receipts,
        "local_files_present": present_count,
        "local_files_expected": expected_count,
        "local_hashes_match": hashes_match,
        "local_state_valid": local_state_valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_md", type=Path)
    parser.add_argument("--skip-network", action="store_true")
    args = parser.parse_args()

    post_md = args.post_md.resolve()
    draft_dir = post_md.parent
    html_path = draft_dir / "post.html"
    frontmatter, body = split_frontmatter(post_md.read_text(encoding="utf-8"))
    html = html_path.read_text(encoding="utf-8")
    urls = editorial_urls(body)
    image_report = image_artifact_report(draft_dir)
    declared_images = {
        Path(str(item.get("file", ""))).as_posix()
        for item in (frontmatter.get("images") or [])
    }

    checks = {
        "title": frontmatter.get("title") == EXPECTED_TITLE,
        "slug": frontmatter.get("slug") == EXPECTED_SLUG,
        "post_date": frontmatter.get("post_date") == EXPECTED_POST_DATE,
        "status_publish": frontmatter.get("status") == "publish",
        "featured_media_declared": frontmatter.get("featured_media_id")
        == EXPECTED_MEDIA_IDS["futureproof-salmon-starfield-share-20260711.jpg"],
        "approved_featured_asset": any(
            str(item.get("file", "")).endswith(
                "futureproof-salmon-starfield-share-20260711.jpg"
            )
            and item.get("role") == "featured-graphic"
            for item in (frontmatter.get("images") or [])
        ),
        "seo_title": (frontmatter.get("seo") or {}).get("meta_title") == EXPECTED_SEO_TITLE,
        "seo_title_length": len((frontmatter.get("seo") or {}).get("meta_title", "")) <= 60,
        "meta_description_length": 140 <= len((frontmatter.get("seo") or {}).get("meta_description", "")) <= 160,
        "word_count": len(re.findall(r"\b[\w'-]+\b", body)) >= 1800,
        "editorial_links": len(urls) >= 25,
        "internal_links": len([u for u in urls if urlparse(u).netloc == "kriskrug.co"]) >= 5,
        "html_images": html.count("<img ") == 9,
        "image_declarations": declared_images
        == {f"images/{name}" for name in EXPECTED_IMAGE_SIZES},
        "html_image_sources": all(
            f'src="images/{name}"' in html for name in EXPECTED_IMAGE_SIZES
        ),
        "image_dimensions": html.count(' width="') == 9 and html.count(' height="') == 9,
        "video_embed": html.count("<!-- wp:embed ") == 1 and "YitQ4fNEDW8" in html,
        "no_unresolved_markers": "[[" not in html and "]]" not in html,
        "no_old_venue_domain": "hrmacmillanspacecentre.com" not in body + html,
        "no_morocco_error": "Morocco" not in body + html,
        "no_disputed_counts": not re.search(
            r"(?:\b300 members\b|\b3,000\+|\b94\+)", body
        ),
        "no_em_dash": "—" not in post_md.read_text(encoding="utf-8") + html,
        "no_absolute_paths": "/Users/" not in body + html,
        "image_manifest_receipts": image_report["manifest_receipts"],
        "local_image_artifacts_consistent": image_report["local_state_valid"],
    }

    failures = [name for name, passed in checks.items() if not passed]
    network: list[dict] = []
    network_errors: list[str] = []
    if not args.skip_network:
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (compatible; KrisKrug editorial verifier/1.0)"
        for url in urls:
            try:
                network.append(check_url(session, url))
            except Exception as exc:
                network_errors.append(f"{url}: {exc}")

    report = {
        "package": str(post_md),
        "checks": checks,
        "failures": failures,
        "counts": {
            "words": len(re.findall(r"\b[\w'-]+\b", body)),
            "editorial_urls": len(urls),
            "internal_urls": len([u for u in urls if urlparse(u).netloc == "kriskrug.co"]),
            "html_images": html.count("<img "),
            "video_embeds": html.count("<!-- wp:embed "),
        },
        "network": network,
        "network_errors": network_errors,
        "image_artifacts": image_report,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if failures or network_errors else 0


if __name__ == "__main__":
    sys.exit(main())
