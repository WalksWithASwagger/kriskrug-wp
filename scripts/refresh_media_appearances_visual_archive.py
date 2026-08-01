#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

import update_media_appearances_roundup as original


SNAPSHOT_DIR = Path("backup/20260731-kris-youtube-press-roundup-v2")
VERSION_MARKER = "<!-- kk-media-roundup-v2-20260731 -->"
PRODUCED_HEADING = """<!-- wp:heading -->
<h2 class="wp-block-heading">Produced Video Interviews</h2>
<!-- /wp:heading -->"""
STALE_FOOTER = """<!-- wp:paragraph -->
<p>This page is based on public sources collected on May 19, 2026.</p>
<!-- /wp:paragraph -->"""
FRESH_FOOTER = """<!-- wp:paragraph -->
<p>This is a selected proof stack, not the whole archive. For the wider publication, citation, and interview trail, visit <a href="https://kriskrug.co/publications/">Press and Publications</a>.</p>
<!-- /wp:paragraph -->"""

PRESS_BLOCK = """<!-- wp:heading -->
<h2 class="wp-block-heading">Recent Press and Quoted Commentary</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The camera and mic are only half the trail. The work also shows up when reporters need somebody who can connect AI infrastructure, creative labour, public policy, and what people are actually feeling.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><a href="https://www.biv.com/news/technology/bc-groups-push-to-build-a-stronger-ai-ecosystem-12601298"><strong>Business in Vancouver: B.C. groups push to build a stronger AI ecosystem</strong></a> (2026): clean energy, Indigenous-owned data centres, and an AI economy that lands inside every profession.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://thetyee.ca/News/2026/07/24/Who-Gets-Say-AI-Adoption/"><strong>The Tyee: Who gets a say in AI adoption?</strong></a> (2026): data centres as heavy industry, public bargaining, and consultation that can still change the outcome.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.biv.com/news/economy-law-politics/bc-lawyers-face-ai-driven-shakeups-in-legal-work-12415161"><strong>Business in Vancouver: AI-driven shakeups in legal work</strong></a> (2026): how legal AI could democratize parts of practice, while training and culture decide what actually gets adopted.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.piquenewsmagazine.com/local-news/we-cant-abdicate-this-future-to-governments-or-tech-bros-says-ai-expert-10076883"><strong>Pique Newsmagazine: We can't abdicate this future</strong></a> (2025): public agency and refusing to leave the future to governments or tech bros.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.cbc.ca/news/instagram-1.7437667"><strong>CBC News and The Early Edition: Meta, Instagram, and platform power</strong></a> (2025): with Jovian Radheshwar and Stephen Quinn on how embedded tech has become in the economy and governance.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://ojs.library.ubc.ca/index.php/bcstudies/article/view/199875"><strong>BC Studies: Building a Grass Roots AI Community of Practice</strong></a> (2025): co-authored with Patrick Pennefather and David Gaertner, documenting the Vancouver AI Community as a grassroots use case.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>For the broader written trail, older interviews, citations, and photography history, see <a href="https://kriskrug.co/publications/"><strong>Press and Publications</strong></a>.</p>
<!-- /wp:paragraph -->"""

VISUAL_BLOCK = f"""{VERSION_MARKER}
<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Watch the Work</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Two rooms, two different versions of the same question: who gets power, and what do we do with it?</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns">
<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:embed {{"url":"https://youtu.be/n_aGBFGnPzo","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
https://youtu.be/n_aGBFGnPzo
</div><figcaption class="wp-element-caption">Power Struggle with Stewart Muir: AI infrastructure, energy, data centres, and sovereignty.</figcaption></figure>
<!-- /wp:embed -->
</div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column">
<!-- wp:embed {{"url":"https://youtu.be/zVy9zCQXPu0","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->
<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">
https://youtu.be/zVy9zCQXPu0
</div><figcaption class="wp-element-caption">STORYHIVE On Location with Jordan Dack: creativity, authorship, consent, community, and both hands full.</figcaption></figure>
<!-- /wp:embed -->
</div>
<!-- /wp:column -->
</div>
<!-- /wp:columns -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Recent Video Interviews and Talks</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The current work moves between public policy, creative survival, systems thinking, and the stubbornly human parts of living through an AI shift.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><strong><a href="https://youtu.be/Vbk2B7aqw8E">AI Is Kicking Down the Door: Creativity, Jobs &amp; BC's Future | Kris Krüg</a>:</strong> Recorded at <a href="https://www.youtube.com/watch?v=d8CvTTSWqj8">LLLSummit</a>, this talk moves from assistants and agents into creative disruption, environmental cost, and the choices British Columbia still gets to make.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><strong><a href="https://youtu.be/TOk2YwViBKs">Live With Curiosity: AI, Creativity &amp; Staying Human | Kris Krüg on Human Biography</a>:</strong> <a href="https://www.youtube.com/watch?v=fF1taMiIV8Q">Sharad Kharé</a> and I get into photography, creative practice, AI ethics, and the stubbornly human value of curiosity. <a href="https://kriskrug.co/2025/01/25/human-biography-podcast-w-sharad-khare/">Read the companion article</a>.</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Earlier Video Receipts</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>This did not start with the current AI cycle. The archive holds nearly two decades of interviews about open source, citizen media, photography, culture, and who gets to make the future.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li><a href="https://www.youtube.com/watch?v=uMTBoHIdhdA"><strong>Byte Club: What Is Generative AI?</strong></a> (2024), with Nessa Palmer.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.youtube.com/watch?v=pss7CfiiBxg"><strong>OHEY Podcasts: Are We Done Yet? Kris Krüg on AI-Volution</strong></a> (2024), with Rob Anthony.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.youtube.com/watch?v=9YubH5GqhnM"><strong>Citizen media and activism during the Vancouver Olympics</strong></a> (2010), with Justin Ruckman.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://vimeo.com/17794857"><strong>W2 Culture + Media House launch interview</strong></a> (2010), from Techvibes.</li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="https://www.youtube.com/watch?v=xuQp1mOiEps"><strong>The Lab with Leo Laporte: Drupal, Bryght, and Raincity Studios</strong></a> (2008).</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->"""


def build_refresh(raw: str) -> tuple[str, bool]:
    if VERSION_MARKER in raw:
        required = (
            "n_aGBFGnPzo",
            "zVy9zCQXPu0",
            "uMTBoHIdhdA",
            "pss7CfiiBxg",
            "9YubH5GqhnM",
            "17794857",
            "xuQp1mOiEps",
            "Recent Press and Quoted Commentary",
            "12601298",
            "Who-Gets-Say-AI-Adoption",
            "12415161",
            "10076883",
            "instagram-1.7437667",
            "199875",
            "This is a selected proof stack",
        )
        missing = [item for item in required if item not in raw]
        if missing:
            raise SystemExit(f"[ABORT] visual marker exists but required items are missing: {missing}")
        return raw, True
    if raw.count(original.BLOCK) != 1:
        raise SystemExit(f"[ABORT] expected one v1 roundup block, found {raw.count(original.BLOCK)}")
    if raw.count(PRODUCED_HEADING) != 1:
        raise SystemExit(f"[ABORT] expected one Produced Video heading, found {raw.count(PRODUCED_HEADING)}")
    if raw.count(STALE_FOOTER) != 1:
        raise SystemExit(f"[ABORT] expected one stale source footer, found {raw.count(STALE_FOOTER)}")
    updated = raw.replace(original.BLOCK, VISUAL_BLOCK, 1)
    updated = updated.replace(PRODUCED_HEADING, f"{PRESS_BLOCK}\n\n{PRODUCED_HEADING}", 1)
    updated = updated.replace(STALE_FOOTER, FRESH_FOOTER, 1)
    return updated, False


def verify_public(url: str) -> str:
    public_url = original.cache_bypass(url)
    response = requests.get(public_url, timeout=30)
    response.raise_for_status()
    required = (
        "youtube.com/embed/n_aGBFGnPzo",
        "youtube.com/embed/zVy9zCQXPu0",
        "Earlier Video Receipts",
        "uMTBoHIdhdA",
        "pss7CfiiBxg",
        "9YubH5GqhnM",
        "17794857",
        "xuQp1mOiEps",
        "Recent Press and Quoted Commentary",
        "12601298",
        "Who-Gets-Say-AI-Adoption",
        "12415161",
        "10076883",
        "instagram-1.7437667",
        "199875",
        "This is a selected proof stack",
    )
    missing = [item for item in required if item not in response.text]
    if missing:
        raise SystemExit(f"[ABORT] public visual refresh verification failed: {missing}")
    return public_url


def write_manifest(snapshot: Path, snapshot_html: Path, before_sha: str, after_sha: str, verified: str) -> Path:
    path = SNAPSHOT_DIR / "rollback-manifest.json"
    payload = {
        "post_id": original.POST_ID,
        "slug": original.POST_SLUG,
        "snapshot_json": str(snapshot),
        "snapshot_html": str(snapshot_html),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "public_verification_url": verified,
        "restore_command": (
            "varlock run --inject vars -- python3 scripts/update_media_appearances_roundup.py "
            f"--restore {snapshot} --apply"
        ),
        "cache_note": "Cache-bypass verified. Check canonical HTML before requesting a Pagely purge.",
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add visual and KB archive proof to post 11879")
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session, base_url = original.auth_session()
    current = original.fetch_post(session, base_url)
    before = current["content"]["raw"]
    desired, already_applied = build_refresh(before)
    if already_applied:
        print(f"[NOOP] post={original.POST_ID} already contains the visual KB refresh")
        return 0
    print(f"target post={original.POST_ID} slug={original.POST_SLUG} status={current['status']}")
    print(f"before_sha256={original.sha256(before)}")
    print(f"after_sha256={original.sha256(desired)}")
    print(original.diff_text(before, desired))
    if not args.apply:
        print("[DRY RUN] no WordPress write; pass --apply to write")
        return 0
    snapshot, snapshot_html = original.write_snapshot(current, SNAPSHOT_DIR, "before-visual-kb-refresh")
    original.update_content(session, base_url, desired)
    readback = original.fetch_post(session, base_url)
    after = readback["content"]["raw"]
    if original.sha256(after) != original.sha256(desired):
        raise SystemExit("[ABORT] authenticated visual refresh readback hash mismatch")
    verified = verify_public(readback["link"])
    manifest = write_manifest(
        snapshot,
        snapshot_html,
        original.sha256(before),
        original.sha256(after),
        verified,
    )
    print(f"[APPLIED] post={original.POST_ID} modified_gmt={readback.get('modified_gmt')}")
    print(f"snapshot={snapshot}")
    print(f"rollback={manifest}")
    print(f"verified={verified}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
