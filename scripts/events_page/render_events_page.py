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
    # A hero that only exists on disk has no public URL. Emitting its local
    # path.as_uri() here would put a file:///Users/kk/... src on page 2250.
    # Never observed live: the 2026-08-02 audit records no file:// leaks and
    # sync_event_media.py has always run before ship. The path was reachable
    # though, so it is closed. Run sync first; degrade to empty until then.
    # (#631)
    return "", alt


POSTER_STOPWORDS = {"a", "an", "and", "at", "for", "of", "on", "the", "to", "with"}


def poster_mark(event: dict[str, Any]) -> str:
    words = [
        word
        for word in str(event.get("title") or "Event").replace("&", " ").split()
        if word.lower().strip(":,.") not in POSTER_STOPWORDS
    ]
    mark = "".join(word[0] for word in words if word and word[0].isalnum())[:3]
    return (mark or "KK").upper()


def poster_date(event: dict[str, Any]) -> str:
    dt = parse_end(event)
    if not dt:
        return "LIVE"
    return dt.strftime("%b %d").upper().replace(" 0", " ")


def artwork_html(
    event: dict[str, Any], roots: dict[str, Path], *, base_class: str
) -> str:
    src, alt = image_src(event, roots)
    if src:
        fit = event.get("image_fit") or (
            "contain" if event.get("image_layout") == "portrait" else "cover"
        )
        classes = (
            f"{base_class} aurora-event-art aurora-event-art--image "
            f"aurora-event-art--{html_escape(fit)}"
        )
        return f"""        <figure class="{classes}">
          <img src="{html_escape(src)}" alt="{html_escape(alt)}" loading="lazy" decoding="async" />
        </figure>"""

    eid = str(event.get("id") or event.get("title") or "event")
    palette = sum(ord(char) for char in eid) % 4
    title = event.get("title") or "Event"
    role = event.get("role") or event.get("kind") or "Appearance"
    return f"""        <figure class="{base_class} aurora-event-art aurora-event-art--generated aurora-event-art--palette-{palette}" role="img" aria-label="Graphic for {html_escape(title)}">
          <span class="aurora-event-art-date">{html_escape(poster_date(event))}</span>
          <strong class="aurora-event-art-mark">{html_escape(poster_mark(event))}</strong>
          <span class="aurora-event-art-role">{html_escape(role)}</span>
        </figure>"""


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
    media_block = artwork_html(event, roots, base_class="aurora-proof-media")
    return f"""      <article class="aurora-proof-module aurora-event-card aurora-event-card--rich" data-event-end="{end}" data-event-id="{eid}">
{media_block}
        <div class="aurora-proof-body">
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
    media = artwork_html(event, roots, base_class="aurora-event-compact-media")
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
  body.page-id-2250 .aurora-page-header {
    padding-bottom: 0;
  }
  body.page-id-2250 .wp-block-post-title {
    color: var(--wp--preset--color--signal, #c84b2f);
    font-family: "DM Sans", system-ui, sans-serif;
    font-size: 0.72rem !important;
    font-weight: 800;
    letter-spacing: 0.18em;
    line-height: 1.2;
    text-transform: uppercase;
  }
  .aurora-events-page {
    --events-paper: #eee6d2;
    --events-ink: #18140f;
    --events-signal: #c84b2f;
    --events-sky: #86a9c4;
    --events-sun: #e3bd4f;
    --events-plum: #57204d;
    --events-line: rgba(24, 20, 15, 0.18);
    --events-serif: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
    --events-sans: "DM Sans", system-ui, sans-serif;
    display: flex;
    flex-direction: column;
  }
  .aurora-events-page > .aurora-speaking-hero {
    order: 1;
    padding-top: clamp(1.25rem, 3vw, 2.5rem);
  }
  .aurora-events-page .aurora-speaking-hero h2 {
    color: var(--events-ink);
    font-size: clamp(2.4rem, 6.5vw, 5.8rem);
    font-weight: 700;
    letter-spacing: -0.035em;
    line-height: 0.92;
    margin: 0;
    max-width: 14ch;
    text-wrap: balance;
  }
  .aurora-events-page > [data-events-bucket="upcoming"] { order: 2; }
  .aurora-events-page > [aria-labelledby="aurora-events-host"] { order: 3; }
  .aurora-events-page > [aria-labelledby="aurora-events-stages"] { order: 4; }
  .aurora-events-page > [aria-labelledby="aurora-events-signature"] { order: 5; }
  .aurora-events-page > [data-events-bucket="past"] { order: 6; }
  .aurora-events-page > .aurora-final-cta { order: 7; }

  .aurora-events-page [data-events-bucket] {
    border-top: 1px solid var(--events-line);
    padding-top: clamp(2.5rem, 6vw, 5rem);
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

  .aurora-events-page [data-events-grid="upcoming"] {
    align-items: stretch;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .aurora-events-page .aurora-event-card--rich {
    background: rgba(255, 252, 244, 0.34);
    border-color: var(--events-line);
    box-shadow: 0 1rem 3rem rgba(41, 29, 18, 0.06);
    display: flex;
    flex-direction: column;
    min-height: 100%;
    transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
  }
  .aurora-events-page .aurora-event-card--rich:hover,
  .aurora-events-page .aurora-event-card--rich:focus-within {
    border-color: rgba(200, 75, 47, 0.62);
    box-shadow: 0 1.4rem 3.5rem rgba(41, 29, 18, 0.12);
    transform: translateY(-4px);
  }
  .aurora-events-page .aurora-event-card--rich .aurora-proof-body {
    flex: 1;
    grid-template-rows: auto auto auto auto 1fr;
    padding: clamp(1rem, 2.4vw, 1.4rem);
  }
  .aurora-events-page .aurora-event-card--rich .aurora-proof-body h3 {
    font-family: var(--events-serif);
    font-size: clamp(1.65rem, 3vw, 2.45rem);
    letter-spacing: -0.035em;
    line-height: 0.98;
    margin: 0;
    text-wrap: balance;
  }
  .aurora-events-page .aurora-event-card--rich .aurora-proof-actions {
    align-self: end;
    margin-top: auto;
  }

  .aurora-events-page .aurora-event-art {
    aspect-ratio: 16 / 10;
    border-bottom: 1px solid var(--events-line);
    box-sizing: border-box;
    display: block;
    margin: 0;
    overflow: hidden;
    position: relative;
    width: 100%;
  }
  .aurora-events-page .aurora-event-art img {
    box-sizing: border-box;
    display: block;
    height: 100%;
    object-fit: cover;
    transition: transform 280ms ease;
    width: 100%;
  }
  .aurora-events-page .aurora-event-card:hover .aurora-event-art--cover img,
  .aurora-events-page .aurora-event-card:focus-within .aurora-event-art--cover img {
    transform: scale(1.025);
  }
  .aurora-events-page .aurora-event-art--contain {
    background: #540016;
  }
  .aurora-events-page .aurora-event-art--contain img {
    object-fit: contain;
    padding: clamp(0.75rem, 2.5vw, 1.5rem);
  }
  .aurora-events-page .aurora-event-art--generated {
    align-content: space-between;
    background: var(--events-signal);
    color: var(--events-ink);
    display: grid;
    isolation: isolate;
    padding: clamp(0.8rem, 2.4vw, 1.25rem);
  }
  .aurora-events-page .aurora-event-art--generated::before {
    border: 1px solid currentColor;
    content: "";
    inset: clamp(0.8rem, 2.4vw, 1.25rem);
    opacity: 0.34;
    pointer-events: none;
    position: absolute;
    z-index: -1;
  }
  .aurora-events-page .aurora-event-art--generated::after {
    border: 1px solid currentColor;
    border-radius: 50%;
    content: "";
    height: 72%;
    opacity: 0.26;
    position: absolute;
    right: -11%;
    top: -28%;
    width: 45%;
    z-index: -1;
  }
  .aurora-events-page .aurora-event-art--palette-0 { background: var(--events-signal); }
  .aurora-events-page .aurora-event-art--palette-1 { background: var(--events-sky); }
  .aurora-events-page .aurora-event-art--palette-2 { background: var(--events-sun); }
  .aurora-events-page .aurora-event-art--palette-3 { background: var(--events-plum); color: var(--events-paper); }
  .aurora-events-page .aurora-event-art-date,
  .aurora-events-page .aurora-event-art-role {
    font-family: var(--events-sans);
    font-size: clamp(0.62rem, 1vw, 0.74rem);
    font-weight: 800;
    letter-spacing: 0.16em;
    position: relative;
    text-transform: uppercase;
  }
  .aurora-events-page .aurora-event-art-mark {
    align-self: center;
    font-family: var(--events-serif);
    font-size: clamp(3rem, 8vw, 6.6rem);
    font-weight: 400;
    letter-spacing: -0.08em;
    line-height: 0.7;
    position: relative;
  }
  .aurora-events-page .aurora-event-art-role {
    align-self: end;
    justify-self: end;
    max-width: 62%;
    text-align: right;
  }

  /* Past archive: newest six first, complete archive on demand. */
  .aurora-events-page [data-events-grid="past"] {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.25rem;
  }
  .aurora-events-page .aurora-event-card--compact {
    background: rgba(255, 252, 244, 0.3);
    border: 1px solid var(--events-line);
    border-radius: 2px;
    display: flex;
    flex-direction: column;
    gap: 0;
    margin: 0;
    overflow: hidden;
    transition: border-color 180ms ease, transform 180ms ease;
  }
  .aurora-events-page .aurora-event-card--compact:hover,
  .aurora-events-page .aurora-event-card--compact:focus-within {
    border-color: rgba(200, 75, 47, 0.62);
    transform: translateY(-3px);
  }
  .aurora-events-page .aurora-event-compact-body {
    padding: 0.9rem;
  }
  .aurora-events-page .aurora-event-compact-body h3 {
    font-family: var(--events-serif);
    font-size: clamp(1.05rem, 1.6vw, 1.3rem);
    letter-spacing: -0.025em;
    line-height: 1.08;
    margin: 0.25rem 0 0.65rem;
  }
  .aurora-events-page .aurora-event-compact-link {
    font-size: 0.82rem;
    font-weight: 700;
  }
  .aurora-events-page .aurora-event-card.is-archive-hidden {
    display: none;
  }
  .aurora-events-page .aurora-event-archive-actions {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
  }
  .aurora-events-page .aurora-event-archive-toggle {
    appearance: none;
    background: transparent;
    border: 1px solid var(--events-ink);
    color: var(--events-ink);
    cursor: pointer;
    font-family: var(--events-sans);
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.11em;
    padding: 0.85rem 1.1rem;
    text-transform: uppercase;
    transition: background-color 160ms ease, color 160ms ease;
  }
  .aurora-events-page .aurora-event-archive-toggle:hover,
  .aurora-events-page .aurora-event-archive-toggle:focus-visible {
    background: var(--events-ink);
    color: var(--events-paper);
    outline-offset: 4px;
  }

  .aurora-events-page .aurora-editorial-mark {
    align-content: space-between;
    aspect-ratio: 16 / 5;
    background: var(--events-sky);
    border-bottom: 1px solid var(--events-line);
    color: var(--events-ink);
    display: grid;
    overflow: hidden;
    padding: 0.8rem 1rem;
    position: relative;
  }
  .aurora-events-page .aurora-editorial-mark::after {
    border: 1px solid currentColor;
    content: "";
    inset: 0.55rem;
    opacity: 0.3;
    position: absolute;
  }
  .aurora-events-page .aurora-editorial-mark span {
    font-family: var(--events-serif);
    font-size: clamp(1.8rem, 4vw, 3.5rem);
    letter-spacing: -0.06em;
    line-height: 0.8;
    position: relative;
    z-index: 1;
  }
  .aurora-events-page .aurora-editorial-mark small {
    font-family: var(--events-sans);
    font-size: 0.62rem;
    font-weight: 800;
    justify-self: end;
    letter-spacing: 0.14em;
    position: relative;
    text-transform: uppercase;
    z-index: 1;
  }
  .aurora-events-page .aurora-proof-module-text:nth-child(4n + 2) .aurora-editorial-mark { background: var(--events-sun); }
  .aurora-events-page .aurora-proof-module-text:nth-child(4n + 3) .aurora-editorial-mark { background: var(--events-signal); }
  .aurora-events-page .aurora-proof-module-text:nth-child(4n) .aurora-editorial-mark { background: var(--events-plum); color: var(--events-paper); }

  @keyframes aurora-event-arrive {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .aurora-events-page [data-events-grid="upcoming"] .aurora-event-card {
    animation: aurora-event-arrive 420ms ease both;
  }
  @media (max-width: 900px) {
    .aurora-events-page [data-events-grid="upcoming"] {
      grid-template-columns: 1fr;
    }
    .aurora-events-page [data-events-grid="past"] {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }
  @media (max-width: 560px) {
    .aurora-events-page [data-events-grid="past"] {
      grid-template-columns: 1fr;
    }
    .aurora-events-page .aurora-event-card--compact {
      display: grid;
      grid-template-columns: minmax(7.25rem, 38vw) minmax(0, 1fr);
    }
    .aurora-events-page .aurora-event-card--compact .aurora-event-art {
      aspect-ratio: 1;
      border-bottom: 0;
      border-right: 1px solid var(--events-line);
      height: 100%;
    }
    .aurora-events-page .aurora-event-art-mark {
      font-size: clamp(2.4rem, 18vw, 4.2rem);
    }
    .aurora-events-page .aurora-event-art-role {
      display: none;
    }
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
  var archivePreviewCount = 6;
  var archiveExpanded = false;

  function syncArchive() {
    var pastGrid = page.querySelector('[data-events-grid="past"]');
    var toggle = page.querySelector('[data-events-archive-toggle]');
    if (!pastGrid || !toggle) return;
    var cards = Array.prototype.slice.call(pastGrid.children);
    cards.forEach(function (card, index) {
      card.classList.toggle('is-archive-hidden', !archiveExpanded && index >= archivePreviewCount);
    });
    toggle.hidden = cards.length <= archivePreviewCount;
    toggle.setAttribute('aria-expanded', archiveExpanded ? 'true' : 'false');
    toggle.textContent = archiveExpanded
      ? 'Show recent appearances'
      : 'Show complete archive (' + cards.length + ')';
  }

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
    syncArchive();
  }

  var archiveToggle = page.querySelector('[data-events-archive-toggle]');
  if (archiveToggle) {
    archiveToggle.addEventListener('click', function () {
      archiveExpanded = !archiveExpanded;
      syncArchive();
    });
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
      <p>Stages, festivals, and the next rooms. Register and come say hi.</p>
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
    <div class="aurora-event-archive-actions">
      <button class="aurora-event-archive-toggle" type="button" data-events-archive-toggle aria-expanded="false">Show complete archive ({len(past)})</button>
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
