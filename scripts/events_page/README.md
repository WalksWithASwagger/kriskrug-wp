# Events page pipeline (`/events/` · WP 2250)

Catalog → (optional media sync) → HTML render. The WordPress page HTML is **generated output**; edit `events-catalog.yaml`, not the live block, when adding dated cards.

Preserved evergreen sections (not regenerated from the catalog): hero, **Series I produce & host**, **Stages I speak on**, **Signature moments**, final CTA. Those live in `shell-events-2250.html`.

## Layout

| File | Role |
|---|---|
| `events-catalog.yaml` | SSOT for dated Upcoming + Past cards |
| `meetup-editions.yaml` | Optional harvest index (`#1`–`#31`); merged at render time when present |
| `shell-events-2250.html` | Page shell with `EVENTS_DYNAMIC_*` markers |
| `render_events_page.py` | Builds Upcoming rich cards + Past compact grid + rolloff |
| `sync_event_media.py` | Uploads local heroes → WP media IDs (dry-run default) |
| `out/events-2250.generated.html` | Dry-run artifact for KK eyeball |
| `lib.py` | Shared load/merge/path helpers |

## Add an event

1. Add a row under `events:` in `events-catalog.yaml`:

```yaml
- id: my-event-2026
  title: "Example Stage"
  date: "2026-11-01"
  end: "2026-11-01T21:00:00-07:00"   # ISO with TZ — drives client rolloff
  bucket_hint: upcoming               # upcoming | past
  kind: one-off                       # meetup | festival | external | one-off
  role: Speaker
  url: "https://…"
  image:
    path: repo:content/drafts/…/hero.jpg   # or kk_kb:… or media_id + url
    alt: "…"
    photographer: "Michelle Diamond"       # optional — folded into alt
  blurb: "One or two sentences."
  label: "Nov 1 · Venue"
  tags: [Speaker, Vancouver]
  status: confirmed                   # confirmed | proposed | unverified | placeholder | scaffold
  edition: null                       # integer for Van AI meetups
```

`proposed`, `unverified`, and `placeholder` are kept in the catalog for ops but **skipped** by the renderer (never land on the live page). Use `confirmed` (or `scaffold` for past archive gaps) for public cards.

2. Put a hero on disk (prefer night photo > promo). Paths use roots from the catalog:

   - `kk_kb:relative/path` → `$KK_KB_ROOT` or `path_roots.kk_kb`
   - `repo:relative/path` → this repo

3. Dry-run media sync, then execute when ready:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/events_page/sync_event_media.py
scripts/notion-to-wp/.venv/bin/python scripts/events_page/sync_event_media.py --execute
```

4. Re-render:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/events_page/render_events_page.py
# → scripts/events_page/out/events-2250.generated.html
```

5. **Apply to live** (separate phase — snapshot page 2250 first, KK approval): POST the generated HTML to WP page **2250**. Do not skip rollback snapshot.

## Harvest merge

If `meetup-editions.yaml` exists (harvest agent output: editions `#1`–`#31` with `hero_image_kk_kb` / `luma_url`), `load_catalog()` converts those rows into catalog events and merges them into Past (harvest wins on date/url/hero). Scaffold rows in `events-catalog.yaml` remain as fallback when harvest is absent. `sync_event_media.py --execute` materializes harvest-only rows into the catalog when writing media IDs back.

## Rolloff

Each dated card has `data-event-end`. Page-scoped JS moves cards between Upcoming and Past; empty Upcoming collapses via `data-events-empty`. Past uses a dense 3/2/1 grid; Upcoming keeps rich proof modules.

## Safety

- Default sync is dry-run (no uploads).
- This folder does **not** POST page content.
- Creds from `scripts/notion-to-wp/.env` (`WP_USER`, `WP_APP_PASSWORD`) — never commit or print them.
- Pitch Night graphic is already WP media **12660**; leave that `media_id` alone.
