# START HERE — Testimonials showpiece v2

**Status:** Waves 1–3 and #601 are done. Page body is **not** live. Snapshot-gate apply is [`APPLY-RUNBOOK.md`](./APPLY-RUNBOOK.md) (#602). Do not PATCH without KK's comment.  
**Epic:** [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593)  
**Board:** [`issues-to-create/testimonials-showpiece-v2-swarm-2026-08-01.md`](../../../issues-to-create/testimonials-showpiece-v2-swarm-2026-08-01.md)

This packet already has **v1** artifacts (live enrichment shipped via #582/#584). Showpiece v2 **extends** them — do not delete v1 files; add `*-v2` / `consent-log` / expand inventory per exclusive ownership.

## When you come back — kickoff in order

### 0. Hygiene (30 seconds)
```bash
cd /Users/kk/Code/kriskrug-wp
git fetch origin main
git checkout -B codex/593-tstm-<lane> origin/main   # one branch per issue
curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i '^Version:'
# Expect live ≥ 1.5.3 as of 2026-08-01; TSTM-3 bumps NEXT patch (not 1.6.0 — #478)
```

Do **not** start from `cursor/publications-aurora-tearsheet` or any dirty pubs/theme WIP branch.

### 1. Wave 1 — four parallel agents (exclusive files)

| Issue | Branch suggestion | Writes only |
|-------|-------------------|-------------|
| [#594](https://github.com/WalksWithASwagger/kriskrug-wp/issues/594) TSTM-1 | `codex/593-tstm-1-quote-inventory` | `quote-inventory.md` (expand in place or clearly section as v2) |
| [#595](https://github.com/WalksWithASwagger/kriskrug-wp/issues/595) TSTM-2 | `codex/593-tstm-2-linkedin-gaps` | `linkedin-gaps.md` |
| [#596](https://github.com/WalksWithASwagger/kriskrug-wp/issues/596) TSTM-3 | `codex/593-tstm-3-aurora-tstm-css` | `theme/kk-aurora/style.css` only |
| [#597](https://github.com/WalksWithASwagger/kriskrug-wp/issues/597) TSTM-4 | `codex/593-tstm-4-copy-v2` | `copy-v2.md` (new) |

### 2. Then Wave 2 → 3 → 4
- #598 curate + consent-log → #599 payload + #600 outreach → #601 theme deploy → #602 body deploy  
- #601 closed. #602 is the remaining human gate: [`APPLY-RUNBOOK.md`](./APPLY-RUNBOOK.md).

## Hard blocks (every lane)
William Jordan · Stephanie McKay · tilde/unresolved names · Butterfield **conference/camera** mis-quote.  
Butterfield **2006 photography LinkedIn rec** OK in Archive only.

## Class contract (do not rename)
See epic #593 / board. Payload dual-classes `aurora-tstm-*` + existing `aurora-quote-card` fallbacks.

## Consume — do not re-mine from scratch
- Notion Master Directory + RAP consent (links on #593)
- v1 packet files in this directory + live payload `…/wp-payloads/testimonials.html`
- Harvest notes in Cursor plan + agent transcripts (Power 50, LinkedIn recs, meetup T1, WhatsApp T2)
- Backups: `backup/20260801-testimonials/` and `backup/20260801-testimonials-enrichment/`

## KK judgment parked for Wave 2
Peter Bowles “Don't fucking stop…” — include/exclude called out in #598.

## Out of scope
Homepage #415 · Jetpack CPT · Review schema · headshots · auto-sync · starting Wave 4 without KK.
