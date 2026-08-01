# Testimonials page overhaul — 2026-08-01

> **Showpiece v2 kickoff:** see [`START-HERE.md`](./START-HERE.md) and epic [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593). v1 below shipped; v2 swarm extends it.

**Track:** A (content) · **Live target:** WP page **2409** · `/testimonials/`  
**Plan:** Cursor plan `testimonials_page_overhaul_bb42a748` (v1); showpiece v2 = epic #593  
**Narrative:** Career arc — AI era first, photography/community archive second.

## Goal

Replace the legacy flat `user-infos` stack with an Aurora body: hero → featured → talks → programs → rooms → archive → CTA. Named people link to LinkedIn profiles when verified.

## Packet files

| File | Role |
|---|---|
| [`quote-inventory.md`](./quote-inventory.md) | Master harvest table (22 rows) |
| [`curated-set.md`](./curated-set.md) | Proposed ship set + KK clearance checkboxes |
| [`linkedin-gaps.md`](./linkedin-gaps.md) | People still needing a verified profile URL |
| [`copy.md`](./copy.md) | Hero + section intros |
| Payload | [`../../source-packs/content-architecture-2026/wp-payloads/testimonials.html`](../../source-packs/content-architecture-2026/wp-payloads/testimonials.html) |
| Page map | key `testimonials` in `page-map.json` (id 2409) |
| Backup / rollback | [`../../../backup/20260801-testimonials/`](../../../backup/20260801-testimonials/) |

## Clearance rules

**Ship freely (default clearance):** public LinkedIn captures in kk-kb; quotes already live on `/testimonials/`; keynote bank named lines (Jai, Ed) + labeled audience lines.

**KK decide before using:** Luma named survey quotes (Simon, Suzy, Lucas); any aggressive shortening of long LinkedIn posts; optional archive extras (Corey, Claudine, Stephanie, Danie).

**Hard block:** Stewart Butterfield attribution on the Cottingham quote; private coaching; invented paraphrases; unverified LinkedIn slugs.

## Ship status — LIVE (2026-08-01)

| Item | Status |
|---|---|
| Inventory + curated set | Done — **19** enriched quotes |
| Payload + page-map | Done (enrichment markers include Simon/Suzy/Landon/Josh) |
| Before snapshot | `backup/20260801-testimonials/` (v1) + enrichment backup when executed |
| Dry-run / live execute | v1 merged via [PR #582](https://github.com/WalksWithASwagger/kriskrug-wp/pull/582); enrichment on `cursor/testimonials-enrichment` |
| Cache-bypass verify | v1 PASS; re-verify after enrichment PATCH |
| Rollback manifest | `backup/20260801-testimonials/rollback-testimonials-2409.json` (pre-enrichment baseline) |
| Commit / PR | Squash-merged `#582` → `main` (`f066693`); enrichment follow-up on this branch |
| Homepage #415 | Out of scope |

**Enriched set:** F1–F3, T1–T3, P1–P3, R1–R3 (incl. Luma Simon/Suzy), A1–A7.  
**LinkedIn coverage:** 14 linked / 16 named (~88%). Plain text: Benjamin, Corey, Claudine, Danie — see [`linkedin-gaps.md`](./linkedin-gaps.md).

## Exact commands

```bash
# Dry-run (already passed)
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots

# Re-execute after payload edits
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots \
  --execute

# Rollback to pre-overhaul body
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots \
  --restore
```

Public verify: `https://kriskrug.co/testimonials/?cb=<timestamp>`

## Follow-ups for KK

1. Confirm comfort with default set (or name swaps).
2. Clear Luma Simon/Suzy if they should join Rooms.
3. Supply LinkedIn profile URLs for Landon Steele + Steve Jones (highest-value gaps).
4. Commit/PR when ready (Track A only — do not mix theme work).
