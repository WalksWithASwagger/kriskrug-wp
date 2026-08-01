#!/usr/bin/env python3
"""Render WP page 2250 (/events/) HTML from events-catalog.yaml.

Dry-run default: writes scripts/events_page/out/events-2250.generated.html
Does NOT POST to WordPress.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from lib import (
    CATALOG_PATH,
    DYNAMIC_END,
    DYNAMIC_START,
    OUT_DIR,
    SHELL_PATH,
    html_escape,
    load_catalog,
    resolve_image_path,
    resolve_path_roots,
)

PT = ZoneInfo("America/Vancouver")


def parse_end(event: dict[str, Any]) -> datetime | None:
    raw = event.get("end") or event.get("date")
    if not raw:
        return None
    text = str(raw)
    try:
        if "T" in text:
            dt = datetime.fromisoformat(text)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=PT)
            return dt
        dt = datetime.fromisoformat(text).replace(
            hour=21, minute=0, second=0, tzinfo=PT
        )
        return dt
    except ValueError:
        return None


def end_iso(event: dict[str, Any]) -> str:
    dt = parse_end(event)
    if not dt:
        return ""
    return dt.isoformat()


def is_past(event: dict[str, Any], now: datetime) -> bool:
    hint = (event.get("bucket_hint") or "").lower()
    dt = parse_end(event)
    if dt is not None:
        return dt <= now
    return hint == "past"


def public_status(event: dict[str, Any]) -> bool:
    """Whether the event should appear on the public page."""
    status = (event.get("status") or "confirmed").lower()
    # proposed / unverified / placeholder stay in catalog for ops but never ship live
    if status in {"draft", "hidden", "omit", "proposed", "unverified", "placeholder"}:
        return False
    return True


def image_src(event: dict[str, Any], roots: dict[str, Path]) -> tuple[str, str]:
    image = event.get("image") or {}
    alt = image.get("alt") or event.get("title") or "Event"
    photographer = image.get("photographer") or event.get("photographer")
    if photographer:
        alt = f"{alt} (photo: {photographer})"
    url = image.get("url")
    if url:
        return str(url), alt
    media_id = image.get("media_id")
    if media_id and not url:
        # Placeholder until sync writes source_url; still emit a stable attr.
        return f"#media-{media_id}", alt
    path = resolve_image_path(image, roots)
    if path and path.exists():
        return path.as_uri(), alt
    return "", alt


def tags_html(tags: list[Any]) -> str:
    if not tags:
        return ""
    spans = "".join(f"<span>{html_escape(t)}</span>" for t in tags)
    return f'<div class="aurora-proof-tags">{spans}</div>'


def cta_label(event: dict[str, Any], *, past: bool) -> str:
    if past:
        return event.get("cta_past") or "Event details"
    return event.get("cta_upcoming") or "Register"


def render_rich_card(event: dict[str, Any], roots: dict[str, Path]) -> str:
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    label = html_escape(event.get("label") or "")
    blurb = html_escape(event.get("blurb") or "")
    url = event.get("url") or "#"
    src, alt = image_src(event, roots)
    portrait = event.get("image_layout") != "landscape"
    media_class = (
        "aurora-proof-media aurora-proof-media--portrait"
        if portrait
        else "aurora-proof-media"
    )
    media_block = ""
    if src:
        media_block = f"""        <figure class="{media_class}">
          <img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />
        </figure>
"""
    return f"""      <article class="aurora-proof-module aurora-event-card aurora-event-card--rich" data-event-end="{end}" data-event-id="{eid}">
{media_block}        <div class="aurora-proof-body">
          <p class="aurora-card-label">{label}</p>
          <h3>{title}</h3>
          <p>{blurb}</p>
          {tags_html(event.get("tags") or [])}
          <div class="aurora-proof-actions aurora-event-cta-upcoming">
            <a class="aurora-button aurora-button-primary" href="{html_escape(url)}">{html_escape(cta_label(event, past=False))}</a>
          </div>
          <div class="aurora-proof-actions aurora-event-cta-past">
            <a class="aurora-button aurora-button-secondary" href="{html_escape(url)}">{html_escape(cta_label(event, past=True))}</a>
          </div>
        </div>
      </article>"""


def edition_label(event: dict[str, Any]) -> str:
    if event.get("edition_label"):
        return str(event["edition_label"])
    edition = event.get("edition")
    dt = parse_end(event)
    month = dt.strftime("%b %Y") if dt else ""
    if edition is not None and month:
        return f"Meetup #{edition} · {month}"
    if edition is not None:
        return f"Meetup #{edition}"
    return event.get("label") or month or ""


def render_compact_card(event: dict[str, Any], roots: dict[str, Path]) -> str:
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    label = html_escape(edition_label(event))
    url = event.get("url") or ""
    src, alt = image_src(event, roots)
    media = '<div class="aurora-event-compact-media aurora-event-compact-media--empty" aria-hidden="true"></div>'
    if src:
        media = f"""        <figure class="aurora-event-compact-media">
          <img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />
        </figure>"""
    link = ""
    if url:
        link = f'<a class="aurora-event-compact-link" href="{html_escape(url)}">Recap / details</a>'
    return f"""      <article class="aurora-event-card aurora-event-card--compact" data-event-end="{end}" data-event-id="{eid}">
{media}
        <div class="aurora-event-compact-body">
          <p class="aurora-card-label">{label}</p>
          <h3>{title}</h3>
          {link}
        </div>
      </article>"""


PAGE_SCOPED_CSS = """
<style>
  /* Dated event cards on /events/ — rich Upcoming + dense Past archive */
  .aurora-events-page .aurora-proof-media--portrait img {
    aspect-ratio: 4 / 5;
    object-fit: cover;
    object-position: center top;
  }
  .aurora-events-page [data-events-bucket][data-events-empty="true"] {
    display: none;
  }
  .aurora-events-page .aurora-event-cta-past {
    display: none;
  }
  .aurora-events-page [data-events-grid="past"] .aurora-event-cta-upcoming {
    display: none;
  }
  .aurora-events-page [data-events-grid="past"] .aurora-event-cta-past {
    display: flex;
  }
  .aurora-events-page .aurora-event-status-note {
    font-size: 0.9em;
    opacity: 0.8;
  }

  /* Past archive: dense 3 / 2 / 1 grid */
  .aurora-events-page [data-events-grid="past"] {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.25rem 1rem;
  }
  @media (max-width: 900px) {
    .aurora-events-page [data-events-grid="past"] {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }
  @media (max-width: 560px) {
    .aurora-events-page [data-events-grid="past"] {
      grid-template-columns: 1fr;
    }
  }
  .aurora-events-page .aurora-event-card--compact {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    margin: 0;
  }
  .aurora-events-page .aurora-event-compact-media {
    margin: 0;
    overflow: hidden;
    border-radius: 2px;
    background: rgba(0, 0, 0, 0.04);
  }
  .aurora-events-page .aurora-event-compact-media img {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 10;
    object-fit: cover;
    object-position: center;
  }
  .aurora-events-page .aurora-event-compact-media--empty {
    aspect-ratio: 16 / 10;
    background: linear-gradient(135deg, rgba(0,0,0,0.06), rgba(0,0,0,0.02));
  }
  .aurora-events-page .aurora-event-compact-body h3 {
    font-size: 1.05rem;
    margin: 0.15rem 0 0.35rem;
    line-height: 1.25;
  }
  .aurora-events-page .aurora-event-compact-link {
    font-size: 0.9rem;
  }

  /* Upcoming stays on the existing proof-grid / rich module rhythm */
  .aurora-events-page [data-events-grid="upcoming"] .aurora-event-card--rich {
    /* inherits .aurora-proof-module */
  }
</style>
"""

ROLLOFF_SCRIPT = """
<script>
(function () {
  var page = document.querySelector('.aurora-events-page');
  if (!page) return;

  function parseEnd(iso) {
    var t = Date.parse(iso);
    return Number.isFinite(t) ? t : NaN;
  }

  function syncBuckets() {
    var now = Date.now();
    var upcomingGrid = page.querySelector('[data-events-grid="upcoming"]');
    var pastGrid = page.querySelector('[data-events-grid="past"]');
    var upcomingBucket = page.querySelector('[data-events-bucket="upcoming"]');
    var pastBucket = page.querySelector('[data-events-bucket="past"]');
    if (!upcomingGrid || !pastGrid || !upcomingBucket || !pastBucket) return;

    var cards = Array.prototype.slice.call(page.querySelectorAll('[data-event-end]'));
    cards.sort(function (a, b) {
      return parseEnd(b.getAttribute('data-event-end')) - parseEnd(a.getAttribute('data-event-end'));
    });

    cards.forEach(function (card) {
      var end = parseEnd(card.getAttribute('data-event-end'));
      if (!Number.isFinite(end)) return;
      var target = end <= now ? pastGrid : upcomingGrid;
      if (card.parentElement !== target) target.appendChild(card);
    });

    upcomingBucket.setAttribute('data-events-empty', upcomingGrid.children.length ? 'false' : 'true');
    pastBucket.setAttribute('data-events-empty', pastGrid.children.length ? 'false' : 'true');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncBuckets);
  } else {
    syncBuckets();
  }
})();
</script>
"""


def render_dynamic_block(
    upcoming: list[dict[str, Any]], past: list[dict[str, Any]], roots: dict[str, Path]
) -> str:
    up_cards = "\n".join(render_rich_card(e, roots) for e in upcoming)
    past_cards = "\n".join(render_compact_card(e, roots) for e in past)
    up_empty = "false" if upcoming else "true"
    past_empty = "false" if past else "true"
    return f"""{PAGE_SCOPED_CSS}

  <section class="aurora-proof-section" aria-labelledby="aurora-events-upcoming" data-events-bucket="upcoming" data-events-empty="{up_empty}">
    <div class="aurora-section-heading">
      <p class="aurora-kicker">Upcoming</p>
      <h2 id="aurora-events-upcoming">On the calendar.</h2>
      <p>Stages, festivals, and the next rooms — register and come say hi.</p>
    </div>
    <div class="aurora-proof-grid" data-events-grid="upcoming">
{up_cards}
    </div>
  </section>

  <section class="aurora-proof-section" aria-labelledby="aurora-events-past" data-events-bucket="past" data-events-empty="{past_empty}">
    <div class="aurora-section-heading">
      <p class="aurora-kicker">Archive</p>
      <h2 id="aurora-events-past">Past rooms.</h2>
      <p>Every Vancouver AI meetup edition plus dated stages that have rolled off Upcoming.</p>
    </div>
    <div class="aurora-proof-grid" data-events-grid="past">
{past_cards}
    </div>
  </section>
{ROLLOFF_SCRIPT}"""


def inject_into_shell(shell: str, dynamic: str) -> str:
    if DYNAMIC_START in shell and DYNAMIC_END in shell:
        pre, rest = shell.split(DYNAMIC_START, 1)
        _, post = rest.split(DYNAMIC_END, 1)
        return f"{pre}{DYNAMIC_START}\n{dynamic}\n{DYNAMIC_END}{post}"
    # Fallback: replace first upcoming section through rolloff script if markers absent
    raise SystemExit("Shell missing EVENTS_DYNAMIC_START/END markers")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--shell", type=Path, default=SHELL_PATH)
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_DIR / "events-2250.generated.html",
        help="Output HTML path (dry-run artifact)",
    )
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    roots = resolve_path_roots(catalog)
    now = datetime.now(tz=timezone.utc)

    events = [e for e in catalog["events"] if public_status(e)]
    upcoming = sorted(
        [e for e in events if not is_past(e, now)],
        key=lambda e: parse_end(e) or datetime.max.replace(tzinfo=timezone.utc),
    )
    past = sorted(
        [e for e in events if is_past(e, now)],
        key=lambda e: parse_end(e) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    shell = args.shell.read_text(encoding="utf-8")
    dynamic = render_dynamic_block(upcoming, past, roots)
    html_out = inject_into_shell(shell, dynamic)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")

    harvest = (
        "merged"
        if catalog.get("_harvest_merged")
        else "not present (scaffold past only)"
    )
    print(f"Wrote {args.out}")
    print(f"Upcoming: {len(upcoming)}  Past: {len(past)}  Harvest index: {harvest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
