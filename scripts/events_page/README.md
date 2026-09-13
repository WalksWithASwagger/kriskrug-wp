# Events page pipeline (`/events/` · WP 2250)

Catalog → (optional media sync) → HTML render. The WordPress page HTML is **generated output**; edit `events-catalog.yaml`, not the live block, when adding dated cards.

Preserved evergreen sections (not regenerated from the catalog): masthead, **Series I produce & host**, final CTA. Those live in `shell-events-2250.html`. *Stages I speak on* and *Signature moments* were folded away on 2026-09-13: every event they listed already exists as a catalog row, so they were duplicate surface.

## Layout (2026-09-13 art direction)

Masthead → **Next up** (up to 4 spotlight cards) → rooms strip → **contact sheet** → **complete record** → CTA. Section order is CSS `order` on the flex page wrapper, so the shell and the generated block can interleave.

The contact sheet is a full-bleed square photo grid on a dark ground, 6 columns at desktop down to 2 on a phone, and it shows **only events with real art**. There is no generated fallback tile: the old monogram poster (`WTD`, `VAC`, initials on a colour block) was the dominant visual on a photographer's page and is gone. An event with no art is carried by the complete record instead, so nothing is lost by the exclusion.

The complete record is a year-grouped typographic index carrying **every** publishable event, art or not. It is the page's completeness guarantee; the sheet is the page's art.

Upcoming events render twice: as a spotlight card, and as a sheet tile held back with `data-tile-upcoming`. When the date passes, the page-scoped script hides the spotlight and releases the tile. No DOM moves between grids.

## Layout

| File | Role |
|---|---|
| `events-catalog.yaml` | SSOT for dated Upcoming + Past cards |
| `meetup-editions.yaml` | Optional harvest index (`#1`–`#31`); merged at render time when present |
| `shell-events-2250.html` | Page shell with `EVENTS_DYNAMIC_*` markers |
| `render_events_page.py` | Builds spotlight cards + contact sheet + complete record + rolloff |
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

5. **Apply to live** (separate approval): snapshot and verify page **2250** first. #635's [runbook](../../content/drafts/2026-08-16-events-hero-backfill/APPLY-RUNBOOK.md) is historical deployment evidence, not reusable approval. The North House proof uses its [bounded runbook](../../content/drafts/2026-09-05-north-house-journey/README.md). Do not treat a merged PR as permission for a live write.

Past records may set `recap_url` to an absolute HTTPS link to a published recap
on `kriskrug.co`; other destinations are rejected. Compact cards then show
"Read the recap"; otherwise they retain "Recap / details" and `url`. Keep `url`
as the host/event source because the hero-fetch engine consumes it. Upcoming
cards retain their registration destination. This proof configures only the
already-past North House record; no media sync or other record change is needed.

## Harvest merge

If `meetup-editions.yaml` exists (harvest agent output: editions `#1`–`#31` with `hero_image_kk_kb` / `luma_url`), `load_catalog()` converts those rows into catalog events and merges them into Past (harvest wins on date/url/hero). Scaffold rows in `events-catalog.yaml` remain as fallback when harvest is absent. `sync_event_media.py --execute` materializes harvest-only rows into the catalog when writing media IDs back.

## Rolloff

Each rendered element has `data-event-end`. Page-scoped JS retires a spotlight card whose date has passed and releases its held-back sheet tile; empty Upcoming collapses via `data-events-empty`. The sheet previews 4 rows and expands via `data-events-sheet-toggle`.

The same script sets `--ev-vw` from `documentElement.clientWidth` for the full-bleed band. `100vw` is only the pre-script fallback: it counts the scrollbar and, under browser zoom, can resolve wider than the viewport, which pushes the band past the edge and eats its padding.

## Reviewing before upload (`--preview-local`)

A hero that is downloaded but not yet in the WP media library has no public URL, so it renders as nothing. To review the layout at real density first:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/events_page/render_events_page.py \
  --preview-local --out scripts/events_page/out/events-2250.preview.html
```

That resolves `image.path` to a relative `heroes/<file>` src. **Never POST a `--preview-local` artifact**: those paths are not public URLs. The default render has the flag off, the contract test pins that default, and `test_real_render_carries_no_local_paths` fails if a local src ever reaches the shipped artifact.

## Hero candidate fields

Rows sourced from the `heroes/LEDGER-*.md` research carry, alongside `path` and `alt`:

- `source_url` — the verified upstream candidate, so the file can be re-fetched
- `rights_basis` — the ledger's vocabulary (`kk-own-asset`, `own-channel`, `luma-own-event`, `bcai-pipeline-credited`)
- `photographer` — required for `bcai-pipeline-credited`; folded into alt text and shown on the tile

Only `url` renders. `source_url` is a pointer for `sync_event_media.py`, never a hotlink: the ledgers are explicit that approved candidates get downloaded and uploaded to the media library rather than served from someone else's CDN.

## Safety

- Default sync is dry-run (no uploads).
- This folder does **not** POST page content.
- Resolve credentials through the root Varlock schema (`varlock run --inject vars -- …`); both supported WP name pairs are accepted. Never read or print value files. The old `.env` loader remains a compatibility fallback.
- Pitch Night graphic is already WP media **12660**; leave that `media_id` alone.

## Hero fetch engine (#587)

`fetch_event_heroes.py` resolves candidate card art for catalog events without touching WordPress. It stages downloads under `heroes/_engine_cache/` (gitignored) and prints a JSON report to stdout. It never uploads media and never writes media IDs into the catalog; Wave 3 ship owns that sync via `sync_event_media.py`.

Resolution order per event:

1. Tracked asset already on the record: `image.path` with `repo:`, `kk_kb:`, or absolute prefix that exists on disk (`source: repo-asset`)
2. YouTube `maxresdefault` thumbnail when `youtube_id` is present, or when `url` / `event_url` is a YouTube link (`source: youtube`)
3. `og:image` from a local HTML snapshot (`og_html_path` on the event, prefix-aware) or from the live `event_url` / `url` page (`source: og-image`; page fetch happens only on `--execute`)
4. `--allow-rafiki` (off by default) marks any remaining gap as `source: rafiki`. The script never generates tiles; Rafiki generation happens in its own toolchain.

Rows whose `image.media_id` is already set report `source: wp-media` and are skipped, so existing uploads (like Pitch Night 12660) are never re-fetched. Events with no usable field report `source: none` with a `MISSING hero_hint` note.

Usage:

```bash
# plan only (default; zero network)
python3 scripts/events_page/fetch_event_heroes.py --dry-run

# limit to specific ids (comma or space separated)
python3 scripts/events_page/fetch_event_heroes.py --ids channelnext-2025,whistler-institute-2025

# feed raw event dicts instead of the catalog
python3 scripts/events_page/fetch_event_heroes.py --events-json my-events.json

# actually download candidates into heroes/_engine_cache/ (GET-only)
python3 scripts/events_page/fetch_event_heroes.py --execute

# mark leftover gaps as Rafiki-tile eligible in the report
python3 scripts/events_page/fetch_event_heroes.py --execute --allow-rafiki

# also write the report to a file
python3 scripts/events_page/fetch_event_heroes.py --dry-run --report /tmp/heroes.json
```

Report rows always carry `id`, `source`, `local_path`, plus `remote_url`, `fetched`, and `note` where useful. Sources: `wp-media`, `repo-asset`, `youtube`, `og-image`, `rafiki`, `none`. Summary counts go to stderr so stdout stays pipeable JSON.

Engine safety:

- Dry-run is the default and does zero network. `--execute` performs plain GET downloads only; there is no WP client in this script at all.
- `maxresdefault` 404s on some older videos; the engine falls back to `hqdefault` and says so in the row note.
- Cache files are disposable and re-runs reuse an existing cache file instead of re-downloading. Fetch errors land in the row note and the run keeps going.
- Tests: `scripts/tests/test_fetch_event_heroes.py` (runs under `make python-test`).
