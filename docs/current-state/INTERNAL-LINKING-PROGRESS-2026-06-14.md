# Internal linking (#38) — progress

Branch: `codex/internal-linking-38`. Builds on the merged SEO overhaul (PR #224) + the 14-category taxonomy.

## Done

- **8 topic-cluster pillar pages live**, art-directed v2 design (image card grid, scoped `.kkp` style, tight type, KK voice, zero em dashes, Jetpack Photon CDN thumbnails). See `PILLAR-PAGES-2026-06-14.md` for IDs/URLs. Source drafts: `content/drafts/pillars/*.v2.html`. Rollback: `reports/pillar-v2-rollback-2026-06-14.json`.
- **Em dashes purged site-wide** from all SEO meta (97 fixed, 0 remain). Tool: `scripts/seo-backfill/purge_meta_emdashes.py`. Rollback: `reports/emdash-purge-rollback-*.json`. Per [[kk-no-em-dashes-no-ai-voice]].

## Next — Phase 3 spoke-injection engine (plan: ~/.claude/plans)

Give every post 2-5 contextual internal links (up to its pillar + sibling cross-links), safely:
- `text_polish.py LINK_MAP`: fix stale URLs (Punk Rock AI) + add 8 pillar pages. Flag for KK: `Both Hands Full` target ambiguity.
- New `scripts/seo-backfill/linkinject_lib.py` (pure) + `inject_links.py` (CLI): contextual `auto_link_first_occurrence` + append-only `kk-collection-footer` block (pillar up-link + siblings), with a **minimal-diff safety assertion** (proves new body == old + only recorded anchors + one footer; refuses full-overwrite). Dry-run review → waves A (2024+) then B (legacy), cluster by cluster.

## Human-gated
Nav-menu inclusion of pillars; `Both Hands Full` canonical URL; whether bare `Vancouver AI` contextual anchor stays site-wide.
