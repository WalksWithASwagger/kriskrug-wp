# Acceptance checklist - #402 SEO authority hubs

Packet path: `content/drafts/2026-07-26-seo-authority-hubs/`  
Mode: Track A draft only. No live WordPress writes in this PR.

## Issue acceptance criteria

- [x] Each target query has an updated or proposed page action (`OPPORTUNITY.md` table).
- [x] At least 5 internal links connect old search-winning posts to current strategic pages (`hub-plan.md` cross-lane minimum; still draft until KK applies live).
- [x] No spammy keyword stuffing; hub outlines preserve Kris voice; no em dashes in drafted hub copy.
- [ ] Agent docs/rules encode KrisKrug.co content tone and SEO guardrails (`AGENTS.md` / `REVIEW.md` update deferred to a follow-up docs(#402) commit if KK wants it in this lane).

## Packet deliverables

- [x] `OPPORTUNITY.md` - keyword/entity list with known on-site URLs
- [x] `hub-plan.md` - proposed hubs + internal link map
- [x] Hub outlines for top opportunities under `hub-outlines/`
  - [x] `01-most-benevolent-outcomes.md`
  - [x] `02-clean-ai-you-cant-drink-data.md`
  - [x] `03-vancouver-ai-community-meetup.md`
  - [x] `04-photography-model-craft-archive.md`
  - [x] `05-cyber-love-garden-creative-ai.md`
- [x] `acceptance-checklist.md` (this file)

## Verification (repo / public only)

- [x] Public URL probes for ranking winners and strategic pages (2026-07-26)
- [x] Cross-check against #328 most-benevolent handoff + SEO crafted batches + pillar drafts
- [ ] `make status-readonly` or `make seo-publisher-smoke` run recorded in PR notes when CI/env allows (honest: this packet is markdown-only; smoke is optional evidence, not a blocker for draft merge)
- [ ] Live title/meta/H1/canonical/OG edits: **not done** (KK-gated)
- [ ] Schema Person/Article/FAQ/Breadcrumb live changes: **not done** (guidance only in `hub-plan.md`)
- [ ] Bidirectional internal links live: **not done**
- [ ] Search Console URL submit / validate: **not done** (human account)

## Live apply gate (separate session)

Before any production write:

1. Re-fetch each post by ID; confirm slug, status, modified.
2. Snapshot `content.raw` / rendered HTML.
3. Dry-run body-only diffs for link patches.
4. KK approval of exact checklist.
5. Pagely cache purge after write; cache-busted public readback.

## Done for this PR when

- [x] Packet committed on `cursor/402-seo-authority-hubs-f196`
- [x] Pushed for human review
- [ ] KK marks which hubs to build first (recommend: #328 links → Vancouver AI refresh → photography hub)
