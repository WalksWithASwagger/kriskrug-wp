# Press kit asset review

This directory is the rights gate for Press Kit v2. Public visibility is not permission to redistribute. `manifest.json` therefore exposes **zero approved downloads**: the best files have documented KrisKrug.co site use, but the creator-approved scope needed for a public press download is not on file.

The `Decision` column is KK's proposed curation choice after the named gate closes. It does not override `status`. Integration must use `status`, and must not render a download control unless the entry is `approved` and carries `public_download_url`.

## Review board

| Asset | Status | Decision | Why | Gate before integration |
|---|---|---:|---|---|
| Current Aurora raster wordmark | `candidate` | **replace** | Official visual reference, but only 468 × 229 and Canva-derived | Supply the vector master; confirm ownership and editorial reuse rules |
| Current EPK portrait, media 5113 | `blocked-rights` | **replace** | No creator, credit, or reuse metadata | Replace with the 2026 close portrait after creator permission |
| Current EPK meetup image, media 6847 | `blocked-rights` | **omit** | The audited frame does not contain Kris; no press-download permission | Remove it from Kris speaking/hosting use |
| CreativeMornings close portrait, media 12627 | `blocked-rights` | **approve** | Strong all-purpose headshot with embedded Michelle Diamond provenance | Confirm public press-download and editorial republication scope with Michelle |
| CreativeMornings staircase portrait, media 12628 | `blocked-rights` | **approve** | Distinctive full-length editorial/personality image | Confirm public press-download and editorial republication scope with Michelle |
| Power 50 portrait, media 12626 | `blocked-rights` | **omit** | Useful on-site recognition image; event-photo scope and resolution are narrow | Keep in recognition context unless Mark Kinskofer / Vision grants broader use |
| VAN-AI portrait, media 12629 | `blocked-rights` | **omit** | Strong community image, but too context-specific for the general kit | Keep for BC + AI / Vancouver AI context unless a later kit needs it |
| Vancouver AI Meetup 30 stage frame | `blocked-rights` | **approve** | Best verified image of Kris hosting an engaged room | Confirm Michelle's press-download scope and request the high-resolution original |
| Vector wordmark master | `missing` | **replace** | Required for print and durable export | Supply authorized SVG or vector PDF with provenance |
| Light-background logo variant | `missing` | **replace** | No dedicated variant exists | Supply an authorized source asset; do not derive silently |
| Dark-background logo variant | `missing` | **replace** | No dedicated variant exists | Supply an authorized source asset; do not derive silently |
| High-resolution stage original | `missing` | **replace** | Only a 1600 × 1066 site copy is tracked | Supply an owned original with explicit download scope |

## Hard separation: coverage is not a brand library

The publication screenshots, article clips, YouTube thumbnails, podcast covers, and publisher photographs under `content/source-packs/keynotes-2026/assets/` remain **press-coverage context**. Their source notes explicitly say they contain copyrighted third-party material. They must not be copied into the downloadable Kris brand set, even when they already appear on the Publications page.

The manifest records that collection under `excluded_collections` so an integrator cannot mistake a `ready` clipping-manifest state for brand-download clearance.

## Approval path

1. KK confirms the `approve / replace / omit` shortlist.
2. Obtain written creator confirmation for public press download and editorial republication, including the required credit line and any crop or alteration limits.
3. Supply missing original/vector files without overwriting the tracked evidence sources.
4. Update the relevant record to `approved`, record the confirmation in `rights_evidence`, state the exact `reuse_terms`, and add the already-public `public_download_url`.
5. Run the rights, download, accessibility, and leak gates before the EPK integration issue consumes the manifest.

No contact sheet is included. The review table and specific alt text are enough for this selection pass, while avoiding a second public-facing artifact before reuse scope is settled.

## Evidence used

- `theme/kk-aurora/assets/img/kriskrug-wordmark.png` and commit `8530a10`
- `content/source-packs/content-architecture-2026/wp-payloads/podcast-guesting-page-epk.html`
- `content/source-packs/site-photography-2026/media-manifest.json`
- `content/source-packs/site-photography-2026/speaking-stage-manifest.json`
- `content/drafts/2026-07-26-speaking-page/photography-inventory.md`
- `content/drafts/alt-text-backfill-2026-08-02/inventory.csv`
- public, read-only WordPress media records for IDs 5113, 6847, and 12626–12629
- `content/source-packs/keynotes-2026/assets/publications-press-media.md`
- `content/source-packs/keynotes-2026/assets/press-media-manifest.json`

No binary was copied, transformed, uploaded, or generated for this inventory.
