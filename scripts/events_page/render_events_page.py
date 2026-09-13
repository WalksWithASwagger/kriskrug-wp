#!/usr/bin/env python3
"""Render WP page 2250 (/events/) HTML from events-catalog.yaml.

Dry-run default: writes scripts/events_page/out/events-2250.generated.html
Does NOT POST to WordPress.

Layout (2026-09-13 art direction):
  masthead -> Next up (big photo cards) -> rooms strip -> contact sheet
  (full-bleed square photo grid, dark ground) -> complete record (typographic
  index) -> CTA.

The contact sheet only ever shows real photographs. An event with no resolvable
image is not given generated art; it lives in the record index instead. The
index carries every public event, so nothing is lost by that exclusion.
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
    resolve_path_roots,
)

PT = ZoneInfo("America/Vancouver")

NEXT_UP_LIMIT = 4
SHEET_PREVIEW_ROWS = 4

# --preview-local only. Lets the dry-run artifact show heroes that are downloaded
# but not yet in the WP media library, so the layout can be reviewed at real
# density before any upload. Never set for the artifact that goes to page 2250:
# those paths are not public URLs. (#631)
PREVIEW_LOCAL = False


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
    if recap_url and (
        not isinstance(recap_url, str) or not recap_url.startswith("https://kriskrug.co/")
    ):
        raise ValueError("recap_url must be an absolute HTTPS link on kriskrug.co")
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


def render_next_card(event: dict[str, Any], roots: dict[str, Path]) -> str:
    """Big spotlight card for an upcoming event."""
    eid = html_escape(event.get("id") or "")
    end = html_escape(end_iso(event))
    title = html_escape(event.get("title") or "")
    label = html_escape(event.get("label") or edition_label(event))
    blurb = html_escape(event.get("blurb") or "")
    role = html_escape(role_line(event))
    url = event_url(event)
    cta = html_escape(event.get("cta_upcoming") or "Register")
    src, alt = image_src(event, roots)

    if src:
        art = f"""      <figure class="kk-ev-next-art">
        <img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />
      </figure>"""
    else:
        # No hero yet. The card carries its own weight typographically rather
        # than inventing art for it.
        dt = parse_end(event)
        art = f"""      <div class="kk-ev-next-art kk-ev-next-art--bare" aria-hidden="true">
        <span class="kk-ev-next-month">{html_escape(dt.strftime("%b").upper() if dt else "TBA")}</span>
        <span class="kk-ev-next-day">{html_escape(dt.strftime("%-d") if dt else "")}</span>
      </div>"""

    role_html = f'<p class="kk-ev-next-role">{role}</p>' if role else ""
    action = (
        f'<a class="kk-ev-btn kk-ev-btn--primary" href="{html_escape(url)}">{cta}</a>'
        if url
        else ""
    )
    return f"""    <article class="kk-ev-next" data-event-end="{end}" data-event-id="{eid}">
{art}
      <div class="kk-ev-next-body">
        <p class="kk-ev-next-when">{label}</p>
        <h3>{title}</h3>
        <p class="kk-ev-next-blurb">{blurb}</p>
        {role_html}
        {action}
      </div>
    </article>"""


def render_tile(event: dict[str, Any], roots: dict[str, Path], *, upcoming: bool) -> str:
    """One frame on the contact sheet. Photograph only, never generated art."""
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


def render_record_row(event: dict[str, Any]) -> str:
    """One line in the complete record. Every public event gets one of these."""
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
    return (
        f'        <li class="kk-ev-rec" data-event-end="{end}" data-event-id="{eid}">'
        f'<span class="kk-ev-rec-date">{day}</span>'
        f'<span class="kk-ev-rec-title">{name}</span>{role_html}</li>'
    )


def render_record(events: list[dict[str, Any]]) -> str:
    """Year-grouped index of everything, newest year first."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        groups.setdefault(year_of(event), []).append(event)

    def year_key(year: str) -> tuple[int, str]:
        return (0, year) if year == "Undated" else (1, year)

    blocks = []
    for year in sorted(groups, key=year_key, reverse=True):
        rows = "\n".join(render_record_row(e) for e in groups[year])
        blocks.append(
            f"""      <div class="kk-ev-rec-year">
        <h3>{html_escape(year)}</h3>
        <ul>
{rows}
        </ul>
      </div>"""
        )
    return "\n".join(blocks)


PAGE_SCOPED_CSS = """
<style>
  body.page-id-2250 .aurora-page-header { padding-bottom: 0; }
  body.page-id-2250 .wp-block-post-title {
    color: var(--wp--preset--color--signal, #c84b2f);
    font-family: "DM Sans", system-ui, sans-serif;
    font-size: 0.72rem !important;
    font-weight: 700;
    letter-spacing: 0.26em;
    text-transform: uppercase;
  }

  .aurora-events-page {
    --ev-paper: #eee6d2;
    --ev-paper-2: #e5dcc4;
    --ev-ink: #18140f;
    --ev-ink-soft: rgba(24, 20, 15, 0.66);
    --ev-signal: #c84b2f;
    --ev-dark: #14110d;
    --ev-line: rgba(24, 20, 15, 0.16);
    --ev-serif: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    --ev-sans: "DM Sans", system-ui, sans-serif;
    --ev-gutter: clamp(1rem, 4vw, 2.5rem);

    display: flex;
    flex-direction: column;
    color: var(--ev-ink);
    font-family: var(--ev-sans);
  }
  /* The full-bleed band sets an explicit width and carries its own padding, so
     a content-box fallback pushes it 2x padding past the viewport. */
  .aurora-events-page,
  .aurora-events-page *,
  .aurora-events-page *::before,
  .aurora-events-page *::after { box-sizing: border-box; }

  .aurora-events-page > .kk-ev-masthead { order: 1; }
  .aurora-events-page > [data-events-bucket="upcoming"] { order: 2; }
  .aurora-events-page > .kk-ev-rooms { order: 3; }
  .aurora-events-page > .kk-ev-sheet { order: 4; }
  .aurora-events-page > .kk-ev-record { order: 5; }
  .aurora-events-page > .kk-ev-cta { order: 6; }

  .aurora-events-page h2,
  .aurora-events-page h3 { color: var(--ev-ink); }

  /* The theme styles bare ul/li; every list here is a custom component. */
  .aurora-events-page ul,
  .aurora-events-page ol,
  .aurora-events-page li {
    list-style: none;
    margin: 0;
    padding: 0;
  }

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
  .kk-ev-masthead { padding: 0.5rem 0 2.25rem; max-width: 46ch; }
  .kk-ev-masthead h2 {
    font-size: clamp(2rem, 4.4vw, 3.1rem);
    letter-spacing: -0.02em;
    line-height: 1.04;
    margin: 0 0 1rem;
  }
  .kk-ev-lede {
    color: var(--ev-ink-soft);
    font-size: 1rem;
    line-height: 1.6;
    margin: 0 0 1.4rem;
  }

  /* ---- next up -------------------------------------------------------- */
  .kk-ev-head { align-items: baseline; display: flex; flex-wrap: wrap; gap: 0 1.5rem; }
  .kk-ev-head h2 {
    font-size: clamp(1.4rem, 2.4vw, 1.85rem);
    letter-spacing: -0.015em;
    margin: 0;
  }
  .kk-ev-head-note {
    color: var(--ev-ink-soft);
    font-size: 0.8rem;
    margin: 0;
  }

  .kk-ev-upcoming {
    border-top: 1px solid var(--ev-line);
    padding-top: 1.6rem;
  }
  .kk-ev-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0 2.4rem;
    list-style: none;
    margin: 0 0 1.8rem;
    padding: 0;
  }
  .kk-ev-stats li { margin: 0; }
  .kk-ev-stats b {
    display: block;
    font-family: var(--ev-serif);
    font-size: 1.9rem;
    font-weight: 400;
    line-height: 1;
  }
  .kk-ev-stats span {
    color: var(--ev-ink-soft);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }

  .kk-ev-next-grid {
    display: grid;
    gap: 1.5rem 1.25rem;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    margin-top: 1.4rem;
  }
  .kk-ev-next { display: flex; flex-direction: column; }
  .kk-ev-next-art {
    aspect-ratio: 4 / 3;
    background: var(--ev-paper-2);
    margin: 0 0 0.9rem;
    overflow: hidden;
  }
  .kk-ev-next-art img {
    display: block;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
    width: 100%;
  }
  .kk-ev-next:hover .kk-ev-next-art img { transform: scale(1.03); }
  /* No hero yet, so the date becomes the art rather than an empty frame. */
  .kk-ev-next-art--bare {
    align-items: center;
    background: var(--ev-paper-2);
    border-top: 3px solid var(--ev-signal);
    display: flex;
    flex-direction: column;
    justify-content: center;
    line-height: 1;
  }
  .kk-ev-next-month {
    color: var(--ev-signal);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-indent: 0.3em;
  }
  .kk-ev-next-day {
    font-family: var(--ev-serif);
    font-size: 3.4rem;
    margin-top: 0.2rem;
  }
  .kk-ev-next-when {
    color: var(--ev-signal);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    margin: 0 0 0.4rem;
    text-transform: uppercase;
  }
  .kk-ev-next h3 {
    font-family: var(--ev-serif);
    font-size: 1.3rem;
    font-weight: 400;
    letter-spacing: -0.01em;
    line-height: 1.15;
    margin: 0 0 0.5rem;
  }
  .kk-ev-next-blurb {
    color: var(--ev-ink-soft);
    font-size: 0.86rem;
    line-height: 1.5;
    margin: 0 0 0.7rem;
  }
  .kk-ev-next-role {
    color: var(--ev-ink-soft);
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    margin: 0 0 0.9rem;
    text-transform: uppercase;
  }
  .kk-ev-next .kk-ev-btn { align-self: flex-start; margin-top: auto; }
  [data-events-bucket="upcoming"][data-events-empty="true"] { display: none; }

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
  /* Grids get a capped bleed out of the theme's ~860px text column. Prose
     (masthead, rooms, CTA) deliberately keeps the narrow measure. */
  .kk-ev-wide {
    margin-inline: calc(50% - min(var(--ev-vw, 100vw) - 2 * var(--ev-gutter), 1240px) / 2);
    width: min(calc(var(--ev-vw, 100vw) - 2 * var(--ev-gutter)), 1240px);
  }

  .kk-ev-sheet {
    background: var(--ev-dark);
    color: var(--ev-paper);
    margin-block: 3rem 0;
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
  .kk-ev-ondark { color: var(--ev-paper); }
  .kk-ev-ondark-kicker { color: #d98a6f; }
  .kk-ev-ondark-soft { color: rgba(238, 230, 210, 0.6); }

  .kk-ev-sheet h2 {
    font-size: clamp(1.4rem, 2.4vw, 1.85rem);
    letter-spacing: -0.015em;
    margin: 0;
  }
  .kk-ev-sheet-toggle { color: var(--ev-paper); }

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
    color: rgba(238, 230, 210, 0.45);
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
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
    .kk-ev-sheet-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    /* Flex wrapping drops the third stat onto a ragged second row. */
    .kk-ev-stats {
      display: grid;
      gap: 0 1rem;
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .kk-ev-stats b { font-size: 1.5rem; }
  }
  @media (max-width: 420px) {
    .kk-ev-sheet-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
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
  var sheetGrid = page.querySelector('[data-events-grid="sheet"]');
  var sheetToggle = page.querySelector('[data-events-sheet-toggle]');
  var upcomingGrid = page.querySelector('[data-events-grid="upcoming"]');
  var upcomingBucket = page.querySelector('[data-events-bucket="upcoming"]');
  var sheetExpanded = false;

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

  function syncRolloff() {
    var now = Date.now();
    // A spotlight card whose date has passed retires, and the matching sheet
    // tile that was held back takes its place. No DOM is moved between grids.
    Array.prototype.slice.call(page.querySelectorAll('.kk-ev-next[data-event-end]')).forEach(
      function (card) {
        var end = parseEnd(card.getAttribute('data-event-end'));
        // Deliberately nested rather than a logical-and operator. WordPress
        // rewrites a literal ampersand pair in post content into HTML entities,
        // which is a SyntaxError that kills this whole script silently. Keep
        // every ampersand out of this block; the render contract enforces it.
        if (Number.isFinite(end)) {
          if (end <= now) card.hidden = true;
        }
      }
    );
    Array.prototype.slice.call(
      page.querySelectorAll('.kk-ev-tile[data-tile-upcoming="true"]')
    ).forEach(function (tile) {
      var end = parseEnd(tile.getAttribute('data-event-end'));
      if (Number.isFinite(end)) {
        if (end <= now) tile.removeAttribute('data-tile-upcoming');
      }
    });

    if (upcomingGrid) {
      if (!upcomingBucket) return;
      var live = Array.prototype.slice.call(upcomingGrid.children).some(function (card) {
        return !card.hidden;
      });
      upcomingBucket.setAttribute('data-events-empty', live ? 'false' : 'true');
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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
""" % {"preview_rows": SHEET_PREVIEW_ROWS}


def render_dynamic_block(
    upcoming: list[dict[str, Any]],
    past: list[dict[str, Any]],
    everything: list[dict[str, Any]],
    roots: dict[str, Path],
) -> str:
    next_up = upcoming[:NEXT_UP_LIMIT]
    next_cards = "\n".join(render_next_card(e, roots) for e in next_up)
    up_empty = "false" if next_up else "true"

    # Contact sheet: photographs only, newest first, upcoming held back until
    # its spotlight card retires.
    upcoming_ids = {e.get("id") for e in upcoming}
    sheet_events = [e for e in everything if has_art(e, roots)]
    tiles = "\n".join(
        render_tile(e, roots, upcoming=e.get("id") in upcoming_ids) for e in sheet_events
    )
    sheet_count = sum(1 for e in sheet_events if e.get("id") not in upcoming_ids)

    editions = sum(1 for e in everything if e.get("edition") is not None)
    stats = [
        (len(everything), "rooms on record"),
        (editions, "meetup editions"),
        (sheet_count, "frames on the sheet"),
    ]
    stats_html = "\n".join(
        f"      <li><b>{value}</b><span>{label}</span></li>" for value, label in stats
    )

    return f"""{PAGE_SCOPED_CSS}

  <section class="kk-ev-upcoming" aria-labelledby="aurora-events-upcoming" data-events-bucket="upcoming" data-events-empty="{up_empty}">
    <div class="kk-ev-head">
      <p class="kk-ev-kicker">Next up</p>
    </div>
    <h2 id="aurora-events-upcoming">On the calendar.</h2>
    <ul class="kk-ev-stats">
{stats_html}
    </ul>
    <div class="kk-ev-next-grid kk-ev-wide" data-events-grid="upcoming">
{next_cards}
    </div>
  </section>

  <section class="kk-ev-sheet" aria-labelledby="aurora-events-sheet">
    <div class="kk-ev-head">
      <p class="kk-ev-kicker"><span class="kk-ev-ondark-kicker">The contact sheet</span></p>
    </div>
    <div class="kk-ev-head">
      <h2 id="aurora-events-sheet"><span class="kk-ev-ondark">Every room I have a frame of.</span></h2>
      <p class="kk-ev-head-note"><span class="kk-ev-ondark-soft">Hover any frame for the night, the room, and the photographer.</span></p>
    </div>
    <div class="kk-ev-sheet-grid" data-events-grid="sheet">
{tiles}
    </div>
    <div class="kk-ev-sheet-actions">
      <button class="kk-ev-sheet-toggle" type="button" data-events-sheet-toggle aria-expanded="false">Show all {sheet_count} frames</button>
    </div>
  </section>

  <section class="kk-ev-record" aria-labelledby="aurora-events-record">
    <div class="kk-ev-head">
      <p class="kk-ev-kicker">The complete record</p>
    </div>
    <div class="kk-ev-head">
      <h2 id="aurora-events-record">Everything, by year.</h2>
      <p class="kk-ev-head-note">{len(everything)} rooms hosted, spoken at, or built.</p>
    </div>
    <div class="kk-ev-record-grid kk-ev-wide">
{render_record(everything)}
    </div>
  </section>
{ROLLOFF_SCRIPT}"""


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
    args = parser.parse_args()

    global PREVIEW_LOCAL
    PREVIEW_LOCAL = args.preview_local

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
    everything = sorted(
        events,
        key=lambda e: parse_end(e) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

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
