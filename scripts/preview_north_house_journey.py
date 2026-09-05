#!/usr/bin/env python3
"""Build private baseline/candidate browser pages from public shells; never writes WP."""

import argparse
import re
import urllib.request
from pathlib import Path

import apply_north_house_journey as journey

ROUTES = {
    "services": "/generative-ai-services/",
    "recap": "/2026/09/03/what-i-showed-founders-about-ai-workflows/",
    "events": "/events/",
    "contact": "/contact/",
}


def candidate_html(name: str, public: str) -> str:
    if name == "services":
        fragment = (journey.PACK / "services-insert.html").read_text().rstrip()
        return journey.replace_once(public, journey.SERVICES_ANCHOR, fragment + "\n\n" + journey.SERVICES_ANCHOR)
    if name == "recap":
        anchor = f'<p class="wp-block-paragraph">{journey.TAKEAWAY}</p>'
        fragment = (journey.PACK / "recap-link.html").read_text().strip()
        return journey.replace_once(public, anchor, anchor + "\n\n" + fragment)
    if name == "events":
        cards = re.findall(r'<article\b[^>]*data-event-id="' + re.escape(journey.EVENT_ID) + r'"[^>]*>.*?</article>', public, re.S)
        if len(cards) != 1:
            raise journey.JourneyError("Public North House card is missing or ambiguous")
        old, new = journey.event_cards()
        link = r'<a class="aurora-event-compact-link"[^>]*>.*?</a>'
        old_link, new_link = re.search(link, old).group(), re.search(link, new).group()
        card = journey.replace_once(cards[0], old_link, new_link)
        return journey.replace_once(public, cards[0], card)
    return public


def local_links(public: str) -> str:
    for path in ROUTES.values():
        public = public.replace(journey.BASE + path, path)
    return public


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--captured-public", type=Path, help="Optional existing <id>-public.html captures")
    args = parser.parse_args()
    for name, path in ROUTES.items():
        captured = args.captured_public / f'{journey.TARGETS[name]["id"]}-public.html' if args.captured_public and name in journey.TARGETS else None
        if captured:
            public = captured.read_text()
        else:
            request = urllib.request.Request(journey.BASE + path, headers={"User-Agent": "kriskrug-proof-readonly/1.0"})
            with urllib.request.urlopen(request, timeout=40) as response:
                public = response.read().decode()
        for state, html in (("baseline", public), ("candidate", candidate_html(name, public))):
            journey.private_write(args.output / state / path.strip("/") / "index.html", local_links(html))
    print(f"Private preview: {args.output}. Public shells with local content overrides; not a WordPress render.")


if __name__ == "__main__":
    main()
