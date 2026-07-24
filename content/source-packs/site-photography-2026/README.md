# Site Photography 2025–2026

Four user-supplied photographs prepared for the `kriskrug.co` media library and future Track A page work.

## What is in this pack

| Asset | Photographer | Best role | Important limit |
|---|---|---|---|
| `kris-krug-vancouver-magazine-power-50-2026.jpg` | Mark Kinskofer / Vision Event Photography | Recognition, press, About credibility | Not a Michelle Diamond photograph |
| `kris-krug-creativemornings-portrait-close-2026.jpg` | Michelle Diamond | Contact, About, speaker profile | Posed portrait, not stage action |
| `kris-krug-creativemornings-portrait-staircase-2026.jpg` | Michelle Diamond | About, editorial profile, personality-led layout | Posed portrait, not stage action |
| `kris-krug-van-ai-portrait-2025.jpg` | Michelle Diamond | BC + AI / Vancouver AI organizer context | Taken at CreativeMornings; does not depict hosting |

The renamed JPEGs are byte-for-byte copies of the supplied files. No recompression, generative edit, colour change, or crop was applied. Embedded creator/copyright metadata remains intact.

## Metadata decisions

- Alt text describes visible content and does not repeat the photographer credit.
- Captions identify the real event context and carry the photographer credit.
- WordPress descriptions preserve provenance and distinguish portraits from action documentation.
- The Power 50 file embeds `Mark Kinskofer` as Artist and IPTC By-line. Vancouver Magazine credits Vision Event Photography for the event, so the manifest uses `Mark Kinskofer / Vision Event Photography` rather than Michelle Diamond.
- The October 2025 photograph was made at CreativeMornings Vancouver, where BC + AI was presenting sponsor. It is useful for Vancouver AI organizer context, but the image itself does not show Kris hosting.

## Page fit

The close CreativeMornings portrait is the strongest immediate candidate for the Contact-page portrait in issue #421. The full staircase portrait gives issue #418 a more expressive About-page option. The Power 50 image belongs in recognition or press context.

These four files do not close the stage-photography requirement in issues #419 or #414. Those surfaces still need wide action images showing a microphone, projected slides, audience context, or workshop interaction.

## Ingestion

Dry-run is the default and performs a hash check plus a public exact-filename search:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/ingest_media_manifest.py \
  --report content/source-packs/site-photography-2026/ingestion-dry-run.json
```

The live write requires Varlock-injected `WP_USER` and `WP_APP_PASSWORD`:

```bash
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/ingest_media_manifest.py \
  --execute \
  --report content/source-packs/site-photography-2026/ingestion-live.json
```

The execute path uploads only when there is no exact filename match. A matching item is reused only when all four WordPress metadata fields already match. Metadata drift or duplicate exact matches abort without changing an existing item.

The live report records created media IDs and their admin URLs. Rollback is deliberately manual: confirm that an uploaded item is not referenced by a page, then remove only that item through the WordPress Media Library.
