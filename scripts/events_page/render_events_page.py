#!/usr/bin/env python3
"""Render WP page 2250 (/events/) HTML from events-catalog.yaml.

Dry-run default: writes scripts/events_page/out/events-2250.generated.html
Does NOT POST to WordPress.

The masthead uses an existing catalog photograph. Upcoming dates lead into
the contact sheet and year-by-year archive. Future rows and frames wait hidden
until rollover.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from catalog_contract import documentation_url, normalize_docs, normalize_status, public_status

from lib import (
    CATALOG_PATH,
    DYNAMIC_END,
    DYNAMIC_START,
    OUT_DIR,
    SHELL_PATH,
    html_escape,
    load_catalog,
    resolve_path_roots,
)

PT = ZoneInfo("America/Vancouver")

FEATURED_FRAME_ID = "2026-07-09-bc-ai-film-club-july-idea-lab"
NEXT_UP_LIMIT = 4
SHEET_PREVIEW_ROWS = 4

# --preview-local only. Lets the dry-run artifact show heroes that are downloaded
# but not yet in the WP media library, so the layout can be reviewed at real
# density before any upload. Never set for the artifact that goes to page 2250:
# those paths are not public URLs. (#631)
PREVIEW_LOCAL = False


def parse_end(event: dict[str, Any]) -> datetime | None:
    """Parse an event's end instant for display stamps.

    Date-only values use midnight solely for sorting/date formatting. No
    event time is inferred or displayed; rolloff uses ``rolloff_datetime``.
    """
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
            hour=0, minute=0, second=0, tzinfo=PT
        )
        return dt
    except ValueError:
        return None


def event_end_date(event: dict[str, Any]) -> date | None:
    """America/Vancouver calendar date the event ends. No invented clock time."""
    for raw in (event.get("end"), event.get("date")):
        if not raw:
            continue
        text = str(raw)
        try:
            if "T" in text:
                dt = datetime.fromisoformat(text)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=PT)
                return dt.astimezone(PT).date()
            return date.fromisoformat(text)
        except ValueError:
            continue
    return None


def rolloff_datetime(event: dict[str, Any]) -> datetime | None:
    """America/Vancouver midnight of the calendar day after the event ends.

    Issue #1100: date-only, timed, and multi-day events share this cutoff.
    Do not invent a clock time on the event day; the card stays current
    until the morning after.
    """
    ended = event_end_date(event)
    if ended is None:
        return None
    return datetime.combine(ended + timedelta(days=1), time.min, tzinfo=PT)


def end_iso(event: dict[str, Any]) -> str:
    dt = rolloff_datetime(event)
    if not dt:
        return ""
    return dt.isoformat()


def is_past(event: dict[str, Any], now: datetime) -> bool:
    cutoff = rolloff_datetime(event)
    if cutoff is not None:
        return cutoff <= now
    hint = (event.get("bucket_hint") or "").lower()
    return hint == "past"


def image_src(event: dict[str, Any], roots: dict[str, Path]) -> tuple[str, str]:
    """Public URL + alt for an event hero, or ("", alt) when there is none.

    A media_id with no source_url used to return "#media-NNNN", which reaches the
    browser as a broken <img src> and paints an empty tile. Only a real URL counts
    as art now; run sync_event_media.py to resolve ids into urls. (#631)
    """
    image = event.get("image") or {}
    alt = image.get("alt") or event.get("title") or "Event"
    photographer = image.get("photographer") or event.get("photographer")
    if photographer:
        alt = f"{alt} (photo: {photographer})"
    url = image.get("url")
    if url:
        return str(url), alt
    if PREVIEW_LOCAL:
        local = image.get("path")
        if local:
            return f"heroes/{str(local).split('/')[-1]}", alt
    # A hero that only exists on disk has no public URL. Emitting its local
    # path.as_uri() here would put a file:///Users/kk/... src on page 2250.
    return "", alt


def has_art(event: dict[str, Any], roots: dict[str, Path]) -> bool:
    return bool(image_src(event, roots)[0])


def credit_line(event: dict[str, Any]) -> str:
    image = event.get("image") or {}
    return str(image.get("photographer") or event.get("photographer") or "")


def role_line(event: dict[str, Any]) -> str:
    return str(event.get("role") or event.get("kind") or "").strip()


def short_date(event: dict[str, Any]) -> str:
    dt = parse_end(event)
    if not dt:
        return ""
    return dt.strftime("%b %-d").upper()


def year_of(event: dict[str, Any]) -> str:
    dt = parse_end(event)
    return dt.strftime("%Y") if dt else "Undated"


def event_url(event: dict[str, Any]) -> str:
    recap_url = event.get("recap_url")
    if recap_url:
        documentation_url(recap_url, canonical_recap=True)
    return str(recap_url or event.get("url") or "")


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


def render_next_card(event: dict[str, Any], roots: dict[str, Path], *, hidden: bool = False) -> str:
    """Compact calendar entry for an upcoming event."""
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    label = html_escape(event.get("label") or edition_label(event))
    blurb = html_escape(event.get("blurb") or "")
    role = html_escape(role_line(event))
    url = str(event.get("url") or "")
    cta = html_escape(event.get("cta_upcoming") or "Register")
    src, alt = image_src(event, roots)

    start_date = date.fromisoformat(str(event["date"]))
    art = (
        f'<img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />'
        if src else ""
    )
    blurb_html = f'<p class="kk-ev-next-blurb">{blurb}</p>' if blurb else ""

    role_html = f'<p class="kk-ev-next-role">{role}</p>' if role else ""
    action = (
        f'<a class="kk-ev-next-link" href="{html_escape(url)}">{cta}</a>'
        if url
        else ""
    )
    state = " hidden" if hidden else ""
    return f"""    <article class="kk-ev-next" data-event-end="{end}" data-event-id="{eid}"{state}>
      <time class="kk-ev-next-date" datetime="{start_date.isoformat()}">
        <span>{start_date:%b}</span>
        <b>{start_date:%-d}</b>
      </time>
      <div class="kk-ev-next-body">
        <p class="kk-ev-next-when">{label}</p>
        <h3>{title}</h3>
        {role_html}
        {action}
        {blurb_html}
      </div>
      {art}
    </article>"""


def render_tile(event: dict[str, Any], roots: dict[str, Path], *, upcoming: bool) -> str:
    """One frame with existing catalog artwork."""
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    url = event_url(event)
    src, alt = image_src(event, roots)
    credit = credit_line(event)
    role = role_line(event)
    meta = " · ".join(part for part in (short_date(event), role) if part)

    link = (
        f'<a class="kk-ev-tile-link" href="{html_escape(url)}"><span class="screen-reader-text">{title}</span></a>'
        if url
        else ""
    )
    credit_html = (
        f'<span class="kk-ev-tile-credit">{html_escape(credit)}</span>' if credit else ""
    )
    state = ' data-tile-upcoming="true"' if upcoming else ""
    return f"""      <article class="kk-ev-tile" data-event-end="{end}" data-event-id="{eid}"{state}>
        <img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />
        <span class="kk-ev-tile-stamp">{html_escape(short_date(event))}</span>
        <span class="kk-ev-tile-info">
          <span class="kk-ev-tile-title">{title}</span>
          <span class="kk-ev-tile-meta">{html_escape(meta)}</span>
          {credit_html}
        </span>
        {link}
      </article>"""


def render_documentation(event: dict[str, Any]) -> str:
    links = []
    for kind, urls in normalize_docs(event).items():
        for index, url in enumerate(urls, start=1):
            label = kind.capitalize() + (f" {index}" if index > 1 else "")
            links.append(f'<a href="{html_escape(url)}">{label}</a>')
    return f'<span class="kk-ev-rec-docs">{" · ".join(links)}</span>' if links else ""


def render_record_row(event: dict[str, Any], *, upcoming: bool = False) -> str:
    """Keep a future row hidden until the same cutoff that retires its card."""
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    role = html_escape(role_line(event))
    url = event_url(event)
    dt = parse_end(event)
    day = html_escape(dt.strftime("%b %-d") if dt else "")
    name = (
        f'<a href="{html_escape(url)}">{title}</a>' if url else f"<span>{title}</span>"
    )
    role_html = f'<span class="kk-ev-rec-role">{role}</span>' if role else ""
    edition = event.get("edition")
    edition_attr = f' data-event-edition="{edition}"' if edition is not None else ""
    state = " hidden" if upcoming else ""
    return (
        f'        <li class="kk-ev-rec" data-event-end="{end}" data-event-id="{eid}"{edition_attr}{state}>'
        f'<span class="kk-ev-rec-date">{day}</span>'
        f'<span class="kk-ev-rec-title">{name}</span>{role_html}{render_documentation(event)}</li>'
    )


def render_record(events: list[dict[str, Any]], *, upcoming_ids: set | None = None) -> str:
    """Year-grouped past index with hidden future rows for browser rollover."""
    upcoming_ids = upcoming_ids or set()
    groups: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        groups.setdefault(year_of(event), []).append(event)

    def year_key(year: str) -> tuple[int, str]:
        return (0, year) if year == "Undated" else (1, year)

    blocks = []
    for year in sorted(groups, key=year_key, reverse=True):
        rows = "\n".join(
            render_record_row(e, upcoming=e.get("id") in upcoming_ids) for e in groups[year]
        )
        state = " hidden" if all(e.get("id") in upcoming_ids for e in groups[year]) else ""
        blocks.append(
            f"""      <div class="kk-ev-rec-year"{state}>
        <h3>{html_escape(year)}</h3>
        <ul>
{rows}
        </ul>
      </div>"""
        )
    return "\n".join(blocks)

def render_masthead(past: list[dict[str, Any]], roots: dict[str, Path]) -> str:
    frame = next((event for event in past if event["id"] == FEATURED_FRAME_ID), {})
    src, alt = image_src(frame, roots)
    caption = " · ".join(part for part in (frame.get("title"), credit_line(frame)) if part)
    photo = (
        f"""    <figure class="kk-ev-feature">
      <img src="{html_escape(src)}" alt="{html_escape(alt)}" fetchpriority="high" decoding="async" />
      <figcaption>{html_escape(caption)}</figcaption>
    </figure>"""
        if src else ""
    )
    return f"""  <section class="kk-ev-masthead kk-ev-wide" aria-labelledby="aurora-events-title">
    <div class="kk-ev-intro">
      <div class="kk-ev-kicker">Kris Krüg / Events</div>
      <h2 id="aurora-events-title"><span>Come through.</span></h2>
      <p class="kk-ev-lede"><span>I host AI meetups in Vancouver, screen films with BC + AI, and take the work on the road. Bring a demo, a question, or just yourself.</span></p>
      <div class="kk-ev-actions">
        <a class="kk-ev-btn kk-ev-btn--primary" href="#aurora-events-upcoming">Next events</a>
        <a class="kk-ev-btn kk-ev-btn--ghost" href="#aurora-events-sheet">Photos &amp; recaps</a>
      </div>
    </div>
{photo}
  </section>"""


PAGE_SCOPED_CSS = """
<style>
  body.page-id-2250 #aurora-main {
    margin-block-start: 0;
    padding-top: clamp(0.75rem, 2vw, 1.65rem);
  }
  body.page-id-2250 #aurora-main > .aurora-page-header {
    clip-path: inset(50%);
    height: 1px;
    margin: 0;
    padding: 0;
    overflow: hidden;
    position: absolute;
    width: 1px;
  }
  body.page-id-2250 #aurora-main > .aurora-page-content { margin-block-start: 0; }

  .aurora-events-page {
    --ev-paper: #eee6d2;
    --ev-ink: #18140f;
    --ev-ink-soft: rgba(24, 20, 15, 0.66);
    --ev-signal: #a23820;
    --ev-green: #153d35;
    --ev-lime: #e0e9a8;
    --ev-dark: #14110d;
    --ev-line: rgba(24, 20, 15, 0.16);
    --ev-serif: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    --ev-sans: "DM Sans", system-ui, sans-serif;
    --ev-gutter: clamp(1rem, 4vw, 2.5rem);

    color: var(--ev-ink);
    font-family: var(--ev-sans);
  }
  /* The full-bleed band sets an explicit width and carries its own padding, so
     a content-box fallback pushes it 2x padding past the viewport. */
  .aurora-events-page,
  .aurora-events-page *,
  .aurora-events-page *::before,
  .aurora-events-page *::after { box-sizing: border-box; }

  .aurora-events-page :is(h2, h3) { color: var(--ev-ink); }
  .aurora-events-page :is(h2, h3)::before { content: none !important; }
  .aurora-events-page :is(h2, #events-series) { scroll-margin-top: 6rem; }
  .aurora-events-page :is(a, button):focus-visible {
    outline: 2px solid currentColor;
    outline-offset: 4px;
  }

  /* The theme styles bare ul/li; every list here is a custom component. It also
     hangs an absolutely positioned 6px red ::before bullet off each li, which
     lands outside these grid rows. */
  .aurora-events-page ul,
  .aurora-events-page ol,
  .aurora-events-page li {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .aurora-events-page li::before,
  .aurora-events-page li::after { content: none; }

  .kk-ev-kicker {
    color: var(--ev-signal);
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.26em;
    margin: 0 0 0.9rem;
    text-transform: uppercase;
  }

  .kk-ev-btn {
    border: 1px solid var(--ev-signal);
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    padding: 0.7rem 1.15rem;
    text-decoration: none;
    text-transform: uppercase;
    transition: background-color 0.18s ease, color 0.18s ease;
  }
  .kk-ev-btn--primary { background: var(--ev-signal); color: var(--ev-paper); }
  .kk-ev-btn--primary:hover { background: var(--ev-ink); border-color: var(--ev-ink); }
  .kk-ev-btn--ghost { background: transparent; color: var(--ev-signal); }
  .kk-ev-btn--ghost:hover { background: var(--ev-signal); color: var(--ev-paper); }
  .kk-ev-actions { display: flex; flex-wrap: wrap; gap: 0.6rem; }

  /* ---- masthead ------------------------------------------------------- */
  .kk-ev-masthead {
    align-items: stretch;
    background: var(--ev-green);
    color: var(--ev-paper);
    display: grid;
    gap: clamp(1.3rem, 4vw, 3.5rem);
    grid-template-columns: repeat(2, minmax(0, 1fr));
    padding: clamp(1.25rem, 3vw, 2.4rem);
  }
  .kk-ev-intro { align-self: center; }
  .kk-ev-intro:only-child { grid-column: 1 / -1; }
  .kk-ev-masthead .kk-ev-kicker { color: var(--ev-lime); }
  #aurora-main .kk-ev-masthead h2,
  .kk-ev-masthead h2 {
    border: 0;
    font-family: var(--ev-serif);
    font-size: clamp(2.55rem, 5.4vw, 5.25rem);
    font-weight: 400;
    letter-spacing: -0.055em;
    line-height: 0.96;
    margin: 0 0 0.9rem;
    max-width: none;
    padding: 0;
  }
  .kk-ev-masthead h2 span,
  .kk-ev-lede span,
  .kk-ev-ondark {
    color: var(--ev-paper);
    -webkit-text-fill-color: currentColor;
  }
  #aurora-main .kk-ev-masthead .kk-ev-lede,
  .kk-ev-lede {
    font-size: clamp(0.95rem, 1.5vw, 1.12rem);
    line-height: 1.5;
    margin: 0 0 1.25rem;
    max-width: 39ch;
  }
  #aurora-main .kk-ev-masthead a.kk-ev-btn,
  .kk-ev-masthead a.kk-ev-btn {
    border-color: var(--ev-lime);
    color: var(--ev-lime) !important;
    text-decoration: none;
  }
  #aurora-main .kk-ev-masthead a.kk-ev-btn--primary,
  #aurora-main .kk-ev-masthead a.kk-ev-btn:hover,
  .kk-ev-masthead a.kk-ev-btn--primary,
  .kk-ev-masthead a.kk-ev-btn:hover {
    background: var(--ev-lime);
    color: var(--ev-green) !important;
  }
  .kk-ev-feature {
    align-self: center;
    background: var(--ev-dark);
    margin: 0;
    min-width: 0;
    padding: 0.45rem;
  }
  .kk-ev-feature img {
    aspect-ratio: 16 / 9;
    display: block;
    object-fit: cover;
    width: 100%;
  }
  .kk-ev-feature figcaption {
    color: var(--ev-paper);
    font-size: 0.72rem;
    line-height: 1.35;
    padding: 0.5rem 0.15rem 0.15rem;
  }

  /* ---- upcoming dates ------------------------------------------------ */
  .kk-ev-head { align-items: baseline; display: flex; flex-wrap: wrap; gap: 0.35rem 1.5rem; }
  #aurora-main .aurora-events-page .kk-ev-head h2,
  .aurora-events-page .kk-ev-head h2 {
    font-size: clamp(1.6rem, 3vw, 2.45rem);
    letter-spacing: -0.035em;
    line-height: 1.12;
    margin: 0;
    padding: 0;
  }
  .kk-ev-head-note {
    color: var(--ev-ink-soft);
    font-size: 0.85rem;
    margin: 0;
  }
  .kk-ev-upcoming { padding-top: clamp(1.15rem, 2.5vw, 1.85rem); }
  .kk-ev-upcoming .kk-ev-head { justify-content: space-between; }
  .kk-ev-upcoming .kk-ev-head a { text-underline-offset: 0.2em; }
  .kk-ev-next-grid {
    display: grid;
    gap: 0.85rem 1.35rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    margin-top: 0.7rem;
  }
  .kk-ev-next {
    align-content: start;
    border-top: 1px solid var(--ev-line);
    display: grid;
    gap: 0.75rem;
    grid-template-columns: 3.5rem minmax(0, 1fr) auto;
    padding-top: 0.8rem;
  }
  .kk-ev-next[hidden] { display: none; }
  .kk-ev-next-date {
    align-self: start;
    background: var(--ev-green);
    color: var(--ev-paper);
    display: grid;
    justify-items: center;
    line-height: 1;
    padding: 0.5rem 0.25rem;
  }
  .kk-ev-next-date span {
    color: var(--ev-lime);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .kk-ev-next-date b {
    font-family: var(--ev-serif);
    font-size: 1.95rem;
    font-weight: 400;
    margin-top: 0.15rem;
  }
  .kk-ev-next > img {
    aspect-ratio: 1;
    object-fit: cover;
    width: clamp(2.75rem, 6vw, 4.5rem);
  }
  #aurora-main .aurora-events-page .kk-ev-next h3,
  .kk-ev-next h3 {
    font-family: var(--ev-serif);
    font-size: clamp(1.2rem, 2.15vw, 1.7rem);
    font-weight: 400;
    line-height: 1.1;
    margin: 0.2rem 0 0.3rem;
  }
  .kk-ev-next .kk-ev-next-when,
  .kk-ev-next .kk-ev-next-role {
    color: var(--ev-ink-soft);
    font-size: 0.7rem;
    font-weight: 700;
    line-height: 1.35;
    margin: 0;
  }
  .kk-ev-next .kk-ev-next-blurb {
    color: var(--ev-ink-soft);
    font-size: 0.88rem;
    line-height: 1.48;
    margin: 0.6rem 0 0;
  }
  #aurora-main .aurora-events-page .kk-ev-next-link,
  .kk-ev-next-link {
    color: var(--ev-signal) !important;
    display: inline-block;
    font-size: 0.82rem;
    font-weight: 700;
    margin-top: 0.4rem;
    padding-block: 0.35rem;
    text-decoration: underline;
    text-underline-offset: 0.2em;
  }
  .kk-ev-next-link:hover { text-decoration-thickness: 2px; }
  .kk-ev-empty,
  [data-events-empty="true"] .kk-ev-next-grid { display: none; }
  [data-events-empty="true"] .kk-ev-empty { display: block; }

  /* ---- rooms strip ---------------------------------------------------- */
  .kk-ev-rooms {
    border-top: 1px solid var(--ev-line);
    margin-top: 2.75rem;
    padding-top: 1.6rem;
  }
  .kk-ev-rooms-head h2 {
    font-size: clamp(1.4rem, 2.4vw, 1.85rem);
    letter-spacing: -0.015em;
    margin: 0 0 1.4rem;
  }
  .kk-ev-rooms-list {
    display: grid;
    gap: 1.4rem 1.6rem;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .kk-ev-room { margin: 0; }
  .kk-ev-room-when {
    color: var(--ev-signal);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    margin: 0 0 0.35rem;
    text-transform: uppercase;
  }
  .kk-ev-room h3 {
    font-family: var(--ev-serif);
    font-size: 1.08rem;
    font-weight: 400;
    margin: 0 0 0.4rem;
  }
  .kk-ev-room h3 a { color: inherit; text-decoration: none; }
  .kk-ev-room h3 a:hover { color: var(--ev-signal); }
  .kk-ev-room p:last-child {
    color: var(--ev-ink-soft);
    font-size: 0.82rem;
    line-height: 1.45;
    margin: 0;
  }

  /* ---- contact sheet --------------------------------------------------- */
  /* Full-bleed out of the theme's 980px column. --ev-vw is set from
     documentElement.clientWidth because 100vw counts the scrollbar (and, under
     browser zoom, can resolve wider than the actual viewport), which bleeds the
     band past the edge and eats its padding. 100vw is the pre-script fallback. */
  /* The theme constrains the page body to a text column. */
  .kk-ev-wide {
    margin-inline: calc(50% - min(var(--ev-vw, 100vw) - 2 * var(--ev-gutter), 1240px) / 2);
    width: min(calc(var(--ev-vw, 100vw) - 2 * var(--ev-gutter)), 1240px);
  }

  .kk-ev-sheet {
    background: var(--ev-dark);
    color: var(--ev-paper);
    margin-block: clamp(1.7rem, 4vw, 3rem) 0;
    margin-inline: calc(50% - var(--ev-vw, 100vw) / 2);
    padding: 2.5rem var(--ev-gutter) 2.75rem;
    width: var(--ev-vw, 100vw);
  }
  /* Text on the dark band is wrapped in these spans rather than coloured on the
     h2/p itself. The theme colours headings and kickers with !important from
     rules carrying an id (body.aurora-theme #aurora-main :where(...)), so no
     selector this stylesheet can write wins on the element. Those rules do not
     match a span with a class of our own, so the span simply takes our colour.
     Without this the heading computed to near-black on the near-black band and
     was invisible while still reporting opacity 1. Verified live 2026-09-13. */

  .kk-ev-sheet-inner { margin-inline: auto; max-width: 1240px; }
  .kk-ev-sheet .kk-ev-head { justify-content: space-between; }
  .kk-ev-sheet .kk-ev-head a { text-underline-offset: 0.2em; }
  .aurora-events-page .kk-ev-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.15rem;
    margin: 0.75rem 0 0;
  }
  .kk-ev-stats li { font-size: 0.78rem; }
  .kk-ev-stats span { color: var(--ev-paper); }
  .kk-ev-stats b { color: var(--ev-lime); margin-right: 0.25rem; }

  .kk-ev-sheet-grid {
    display: grid;
    gap: 4px;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    margin-top: 1.5rem;
  }
  .kk-ev-tile {
    aspect-ratio: 1;
    background: #221d16;
    overflow: hidden;
    position: relative;
  }
  .kk-ev-tile img {
    display: block;
    filter: saturate(0.92);
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease, filter 0.3s ease;
    width: 100%;
  }
  .kk-ev-tile-stamp {
    background: rgba(20, 17, 13, 0.72);
    color: var(--ev-paper);
    font-size: 0.54rem;
    font-weight: 700;
    inset: auto auto 0 0;
    letter-spacing: 0.14em;
    padding: 0.3rem 0.45rem;
    position: absolute;
    transition: opacity 0.2s ease;
  }
  /* Frames range from night photos to high-contrast poster art, so the caption
     needs a floor of its own rather than a gradient tuned to one kind of image. */
  .kk-ev-tile-info {
    background:
      linear-gradient(to top, rgba(20, 17, 13, 0.96) 30%, rgba(20, 17, 13, 0.12) 75%, rgba(20, 17, 13, 0)),
      rgba(20, 17, 13, 0.45);
    display: flex;
    flex-direction: column;
    gap: 0.18rem;
    inset: 0;
    justify-content: flex-end;
    opacity: 0;
    padding: 0.7rem 0.65rem;
    position: absolute;
    transition: opacity 0.22s ease;
  }
  .kk-ev-tile-title {
    font-family: var(--ev-serif);
    font-size: 0.9rem;
    line-height: 1.18;
  }
  .kk-ev-tile-meta {
    color: rgba(238, 230, 210, 0.72);
    font-size: 0.56rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }
  .kk-ev-tile-credit {
    color: var(--ev-paper);
    font-size: 0.54rem;
    font-style: italic;
  }
  .kk-ev-tile-link { inset: 0; position: absolute; }
  .kk-ev-tile:hover img,
  .kk-ev-tile:focus-within img { filter: saturate(1); transform: scale(1.06); }
  .kk-ev-tile:hover .kk-ev-tile-info,
  .kk-ev-tile:focus-within .kk-ev-tile-info { opacity: 1; }
  .kk-ev-tile:hover .kk-ev-tile-stamp,
  .kk-ev-tile:focus-within .kk-ev-tile-stamp { opacity: 0; }
  /* An upcoming event is spotlighted above; it rejoins the sheet on rolloff. */
  .kk-ev-tile[data-tile-upcoming="true"] { display: none; }
  .kk-ev-tile.is-sheet-hidden { display: none; }

  .kk-ev-sheet-actions { margin-top: 1.4rem; }
  .kk-ev-sheet-toggle {
    background: transparent;
    border: 1px solid rgba(238, 230, 210, 0.4);
    color: var(--ev-paper);
    cursor: pointer;
    font-family: var(--ev-sans);
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 0.65rem 1.1rem;
    text-transform: uppercase;
    transition: background-color 0.18s ease, color 0.18s ease;
  }
  .kk-ev-sheet-toggle:hover { background: var(--ev-paper); color: var(--ev-dark); }
  .kk-ev-sheet-toggle[hidden] { display: none; }

  /* ---- complete record ------------------------------------------------- */
  .kk-ev-record { padding-top: 2.5rem; }
  .kk-ev-record-grid {
    display: grid;
    /* start, not stretch: 2023 holds one event and was being handed a cell as
       tall as the 26-row years beside it. */
    align-items: start;
    gap: 1.75rem 2rem;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    margin-top: 1.5rem;
  }
  .kk-ev-rec-year h3 {
    border-bottom: 1px solid var(--ev-line);
    font-family: var(--ev-serif);
    font-size: 1.15rem;
    font-weight: 400;
    margin: 0 0 0.6rem;
    padding-bottom: 0.35rem;
  }
  .kk-ev-rec-year ul { list-style: none; margin: 0; padding: 0; }
  .kk-ev-rec {
    display: grid;
    font-size: 0.85rem;
    line-height: 1.35;
    gap: 0 0.6rem;
    grid-template-columns: 3.6rem 1fr;
    padding: 0.3rem 0;
  }
  .kk-ev-rec[hidden], .kk-ev-rec-year[hidden] { display: none; }
  .kk-ev-rec-docs { grid-column: 2; font-size: 0.72rem; padding-top: 0.3rem; }
  .kk-ev-rec-docs a { color: var(--ev-ink); text-decoration: underline; }
  .kk-ev-rec-date {
    color: var(--ev-ink-soft);
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    padding-top: 0.22rem;
    text-transform: uppercase;
  }
  .kk-ev-rec-title { font-size: 0.85rem; line-height: 1.35; }
  .kk-ev-rec-title a { color: inherit; text-decoration: none; }
  .kk-ev-rec-title a:hover { color: var(--ev-signal); text-decoration: underline; }
  .kk-ev-rec-role {
    color: var(--ev-ink-soft);
    font-size: 0.56rem;
    grid-column: 2;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  /* ---- cta ------------------------------------------------------------- */
  .kk-ev-cta {
    border-top: 1px solid var(--ev-line);
    margin-top: 2.75rem;
    padding-top: 1.9rem;
  }
  .kk-ev-cta h2 {
    font-size: clamp(1.5rem, 2.8vw, 2.1rem);
    letter-spacing: -0.015em;
    margin: 0 0 1.1rem;
  }

  /* ---- responsive ------------------------------------------------------ */
  @media (max-width: 1080px) {
    .kk-ev-sheet-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  }
  @media (max-width: 720px) {
    /* Keep the offscreen link labels inside the scrolling navigation. */
    body.page-id-2250 .aurora-primary-nav { position: relative; }
    .kk-ev-sheet-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .kk-ev-masthead,
    .kk-ev-next-grid { grid-template-columns: minmax(0, 1fr); }
    .kk-ev-masthead { gap: 0.95rem; }
    .kk-ev-feature img { aspect-ratio: 2.25 / 1; }
  }
  @media (max-width: 420px) {
    .kk-ev-sheet-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .kk-ev-masthead { padding: 1rem; }
    #aurora-main .kk-ev-masthead h2,
    .kk-ev-masthead h2 { font-size: clamp(2.1rem, 10.45vw, 2.55rem); }
    .kk-ev-masthead .kk-ev-btn { font-size: 0.63rem; padding-inline: 0.65rem; }
  }
  /* Touch: there is no hover, so the caption has to be standing information. */
  @media (hover: none) {
    .kk-ev-tile-info { opacity: 1; }
    .kk-ev-tile-stamp { opacity: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .aurora-events-page *,
    .aurora-events-page *::before,
    .aurora-events-page *::after {
      animation-duration: 0.01ms !important;
      scroll-behavior: auto !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>
"""


ROLLOFF_SCRIPT = """
<script>
(function () {
  var page = document.querySelector('.aurora-events-page');
  if (!page) return;

  var PREVIEW_ROWS = %(preview_rows)d;
  var NEXT_UP_LIMIT = %(next_up_limit)d;
  var sheetGrid = page.querySelector('[data-events-grid="sheet"]');
  var sheetToggle = page.querySelector('[data-events-sheet-toggle]');
  var upcomingGrid = page.querySelector('[data-events-grid="upcoming"]');
  var upcomingBucket = page.querySelector('[data-events-bucket="upcoming"]');
  var sheetExpanded = false;
  var rolloffTimer;

  function parseEnd(iso) {
    var t = Date.parse(iso);
    return Number.isFinite(t) ? t : NaN;
  }

  function syncBleed() {
    page.style.setProperty('--ev-vw', document.documentElement.clientWidth + 'px');
  }

  function columnCount() {
    if (!sheetGrid) return 6;
    var cols = window.getComputedStyle(sheetGrid).gridTemplateColumns;
    if (!cols) return 6;
    return cols.split(' ').filter(Boolean).length || 6;
  }

  function syncSheet() {
    if (!sheetGrid || !sheetToggle) return;
    // Only tiles actually in play. A tile still held back as upcoming is not
    // part of the sheet and must not consume a preview slot.
    var tiles = Array.prototype.slice.call(sheetGrid.children).filter(function (tile) {
      return tile.getAttribute('data-tile-upcoming') !== 'true';
    });
    var limit = columnCount() * PREVIEW_ROWS;
    tiles.forEach(function (tile, index) {
      var hide = sheetExpanded ? false : index >= limit;
      tile.classList.toggle('is-sheet-hidden', hide);
    });
    sheetToggle.hidden = tiles.length <= limit;
    sheetToggle.setAttribute('aria-expanded', sheetExpanded ? 'true' : 'false');
    sheetToggle.textContent = sheetExpanded
      ? 'Show fewer frames'
      : 'Show all ' + tiles.length + ' frames';
  }

  function setCount(name, value) {
    Array.prototype.slice.call(page.querySelectorAll('[data-events-count="' + name + '"]')).forEach(function (node) {
      node.textContent = String(value);
    });
  }

  function syncRolloff() {
    var now = Date.now();
    var liveCards = 0;
    Array.prototype.slice.call(page.querySelectorAll('.kk-ev-next[data-event-end]')).forEach(function (card) {
      var end = parseEnd(card.getAttribute('data-event-end'));
      card.hidden = true;
      if (Number.isFinite(end)) {
        if (end > now) {
          card.hidden = liveCards >= NEXT_UP_LIMIT;
          liveCards += 1;
        }
      }
    });
    var frames = 0;
    Array.prototype.slice.call(page.querySelectorAll('.kk-ev-tile[data-event-end]')).forEach(function (tile) {
      var end = parseEnd(tile.getAttribute('data-event-end'));
      var future = Number.isFinite(end) ? end > now : false;
      if (future) tile.setAttribute('data-tile-upcoming', 'true');
      else {
        tile.removeAttribute('data-tile-upcoming');
        frames += 1;
      }
    });
    var rooms = 0;
    var editions = 0;
    Array.prototype.slice.call(page.querySelectorAll('.kk-ev-rec[data-event-end]')).forEach(function (row) {
      var end = parseEnd(row.getAttribute('data-event-end'));
      row.hidden = Number.isFinite(end) ? end > now : false;
      if (!row.hidden) {
        rooms += 1;
        if (row.getAttribute('data-event-edition') !== null) editions += 1;
      }
    });
    Array.prototype.slice.call(page.querySelectorAll('.kk-ev-rec-year')).forEach(function (year) {
      year.hidden = !Array.prototype.slice.call(year.querySelectorAll('.kk-ev-rec')).some(function (row) {
        return !row.hidden;
      });
    });
    setCount('rooms', rooms);
    setCount('editions', editions);
    setCount('frames', frames);
    if (upcomingBucket) upcomingBucket.setAttribute('data-events-empty', liveCards ? 'false' : 'true');
  }

  function scheduleRolloff() {
    window.clearTimeout(rolloffTimer);
    var now = Date.now();
    var soonest = Infinity;
    Array.prototype.slice.call(page.querySelectorAll('[data-event-end]')).forEach(
      function (el) {
        var end = parseEnd(el.getAttribute('data-event-end'));
        if (Number.isFinite(end)) {
          if (end > now) {
            if (end < soonest) soonest = end;
          }
        }
      }
    );
    if (soonest < Infinity) {
      var wait = soonest - now;
      if (wait < 0) wait = 0;
      if (wait > 86400000) wait = 86400000;
      rolloffTimer = window.setTimeout(function () {
        syncRolloff();
        syncSheet();
        scheduleRolloff();
      }, wait);
    }
  }

  if (sheetToggle) {
    sheetToggle.addEventListener('click', function () {
      sheetExpanded = !sheetExpanded;
      syncSheet();
    });
  }

  var resizeTimer;
  window.addEventListener('resize', function () {
    syncBleed();
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(syncSheet, 150);
  });

  function init() {
    syncBleed();
    syncRolloff();
    syncSheet();
    scheduleRolloff();
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') {
      init();
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
""" % {"preview_rows": SHEET_PREVIEW_ROWS, "next_up_limit": NEXT_UP_LIMIT}


def render_dynamic_block(
    upcoming: list[dict[str, Any]],
    past: list[dict[str, Any]],
    everything: list[dict[str, Any]],
    roots: dict[str, Path],
) -> str:
    next_cards = "\n".join(
        render_next_card(e, roots, hidden=index >= NEXT_UP_LIMIT)
        for index, e in enumerate(upcoming)
    )
    up_empty = "false" if upcoming else "true"

    # Contact sheet: photographs only, newest first, upcoming held back until
    # its spotlight card retires.
    upcoming_ids = {e.get("id") for e in upcoming}
    sheet_events = [e for e in everything if has_art(e, roots)]
    tiles = "\n".join(
        render_tile(e, roots, upcoming=e.get("id") in upcoming_ids) for e in sheet_events
    )
    sheet_count = sum(1 for e in sheet_events if e.get("id") not in upcoming_ids)

    editions = sum(1 for e in past if e.get("edition") is not None)
    stats = [
        ("rooms", len(past), "past events"),
        ("editions", editions, "meetup editions"),
        ("frames", sheet_count, "frames"),
    ]
    stats_html = "\n".join(
        f'      <li><b data-events-count="{key}">{value}</b><span>{label}</span></li>' for key, value, label in stats
    )

    return f"""{PAGE_SCOPED_CSS}

{render_masthead(past, roots)}

  <section class="kk-ev-upcoming kk-ev-wide" aria-labelledby="aurora-events-upcoming" data-events-bucket="upcoming" data-events-empty="{up_empty}">
    <div class="kk-ev-head">
      <h2 id="aurora-events-upcoming">Where I’ll be next</h2>
      <a class="kk-ev-head-note" href="#events-series">Meetups, screenings &amp; office hours</a>
    </div>
    <div class="kk-ev-next-grid" data-events-grid="upcoming">
{next_cards}
    </div>
    <p class="kk-ev-empty">I’m between dates. <a href="https://lu.ma/vancouver-ai">Follow Vancouver AI on Luma</a> for the next meetup.</p>
  </section>

  <section class="kk-ev-sheet" aria-labelledby="aurora-events-sheet">
    <div class="kk-ev-sheet-inner">
      <div class="kk-ev-head">
        <h2 id="aurora-events-sheet"><span class="kk-ev-ondark">The contact sheet</span></h2>
        <a class="kk-ev-head-note" href="#aurora-events-record"><span class="kk-ev-ondark">Find recaps, photos &amp; recordings</span></a>
      </div>
      <ul class="kk-ev-stats">
{stats_html}
      </ul>
      <div id="events-contact-sheet-grid" class="kk-ev-sheet-grid" data-events-grid="sheet">
{tiles}
      </div>
      <div class="kk-ev-sheet-actions">
        <button class="kk-ev-sheet-toggle" type="button" data-events-sheet-toggle aria-expanded="false" aria-controls="events-contact-sheet-grid" hidden>Show all {sheet_count} frames</button>
      </div>
    </div>
  </section>

  <section class="kk-ev-record kk-ev-wide" aria-labelledby="aurora-events-record">
    <div class="kk-ev-head">
      <h2 id="aurora-events-record">Past events by year</h2>
      <p class="kk-ev-head-note"><span data-events-count="rooms">{len(past)}</span> rooms so far. Recaps, photos and recordings where I have them.</p>
    </div>
    <div class="kk-ev-record-grid">
{render_record(everything, upcoming_ids=upcoming_ids)}
    </div>
  </section>
{ROLLOFF_SCRIPT}"""


def partition_events(events: list[dict[str, Any]], now: datetime) -> tuple[list, list, list]:
    eligible = [e for e in events if public_status(e)]
    # Scaffold rows document past archive gaps, never tentative future appearances.
    eligible = [e for e in eligible if normalize_status(e.get("status")) != "scaffold" or is_past(e, now)]
    everything = sorted(
        eligible, key=lambda e: parse_end(e) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    past = [e for e in everything if is_past(e, now)]
    upcoming = [e for e in everything if not is_past(e, now)]
    upcoming.sort(key=lambda e: datetime.fromisoformat(str(e["date"])).replace(tzinfo=PT)
                  if e.get("date") else parse_end(e))
    return upcoming, past, everything


def inject_into_shell(shell: str, dynamic: str) -> str:
    if DYNAMIC_START in shell and DYNAMIC_END in shell:
        pre, rest = shell.split(DYNAMIC_START, 1)
        _, post = rest.split(DYNAMIC_END, 1)
        return f"{pre}{DYNAMIC_START}\n{dynamic}\n{DYNAMIC_END}{post}"
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
    parser.add_argument(
        "--preview-local",
        action="store_true",
        help="Render not-yet-uploaded heroes from heroes/_pending for local review. "
        "Produces a preview artifact only; never POST this output.",
    )
    parser.add_argument(
        "--now",
        default=None,
        help="ISO timestamp for the upcoming/past split (default: now). "
        "Used by tests to pin the America/Vancouver morning-after cutoff.",
    )
    args = parser.parse_args()

    global PREVIEW_LOCAL
    PREVIEW_LOCAL = args.preview_local

    catalog = load_catalog(args.catalog)
    roots = resolve_path_roots(catalog)
    if args.now:
        now = datetime.fromisoformat(args.now)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
    else:
        now = datetime.now(tz=timezone.utc)

    upcoming, past, everything = partition_events(catalog["events"], now)

    shell = args.shell.read_text(encoding="utf-8")
    dynamic = render_dynamic_block(upcoming, past, everything, roots)
    html_out = inject_into_shell(shell, dynamic)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html_out, encoding="utf-8")

    with_art = sum(1 for e in everything if has_art(e, roots))
    harvest = (
        "merged"
        if catalog.get("_harvest_merged")
        else "not present (scaffold past only)"
    )
    print(f"Wrote {args.out}")
    print(f"Upcoming: {len(upcoming)}  Past: {len(past)}  Harvest index: {harvest}")
    print(f"Contact sheet: {with_art} of {len(everything)} events have art")
    if PREVIEW_LOCAL:
        print("PREVIEW-LOCAL artifact: contains non-public paths. Do not POST.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
