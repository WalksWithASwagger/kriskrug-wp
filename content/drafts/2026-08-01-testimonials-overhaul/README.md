# Testimonials page overhaul: 2026-08-01 (v1 shipped) / v2 built

**Track:** A (content) + B (theme) · **Live target:** WP page **2409** · `/testimonials/`
**Epic:** [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593) · **Narrative:** career arc, AI era first, photography/community archive second.

## Goal

Replace the legacy flat `user-infos` stack with an Aurora body: hero → featured → talks → programs → rooms → archive → CTA. Real names, linked sources, receipts. No invented quotes, no invented attributions, no anonymous filler. Named people link to LinkedIn only when the URL is verified.

---

# v2 (showpiece): built, not deployed

## Packet files, and who owns what

| File | Issue | What it is |
|---|---|---|
| [`quote-inventory.md`](./quote-inventory.md) | [#594](https://github.com/WalksWithASwagger/kriskrug-wp/issues/594) | 148 rows harvested from Notion, RAP, kk-kb, WhatsApp, press. Raw pool, not curated. |
| [`linkedin-gaps.md`](./linkedin-gaps.md) | [#595](https://github.com/WalksWithASwagger/kriskrug-wp/issues/595) | Per-person resolution: 36 FOUND, 8 MISSING, 1 SKIP. Zero guessed slugs. |
| [`copy-v2.md`](./copy-v2.md) | [#597](https://github.com/WalksWithASwagger/kriskrug-wp/issues/597) | Hero, six footnoted stat chips, press band, section intros, CTA. |
| [`curated-set-v2.md`](./curated-set-v2.md) | [#598](https://github.com/WalksWithASwagger/kriskrug-wp/issues/598) | The ~40 quotes that actually ship, mapped to the locked sections. |
| [`consent-log.md`](./consent-log.md) | [#598](https://github.com/WalksWithASwagger/kriskrug-wp/issues/598) | One row per shipped quote: source, consent basis, status. Plus hard blocks. |
| [`consent-outreach.md`](./consent-outreach.md) | [#600](https://github.com/WalksWithASwagger/kriskrug-wp/issues/600) | The 8 T2 people to contact, channels, draft messages. **Nothing sent.** |

Payload lives at [`../../source-packs/content-architecture-2026/wp-payloads/testimonials.html`](../../source-packs/content-architecture-2026/wp-payloads/testimonials.html) ([#599](https://github.com/WalksWithASwagger/kriskrug-wp/issues/599)); CSS is `aurora-tstm` in the theme ([#596](https://github.com/WalksWithASwagger/kriskrug-wp/issues/596), Aurora 1.5.8). v1 files (`curated-set.md`, `copy.md`) are kept for history.

## Hard blocks: never publish

Full table in [`consent-log.md`](./consent-log.md).

- **William Jordan**, **Stephanie McKay**: RAP Cohort 1 consent tracker says no. Internal feedback only.
- **Any tilde or unresolved WhatsApp name**: no legal name on file.
- **The "camera in hand" quote attributed to Stewart Butterfield**: that is Rob Cottingham's line. Butterfield's only publishable quote is his 2006 photography recommendation, Archive only.
- **Invented paraphrases, unverified LinkedIn slugs, private coaching material.**

**Do not publish decliners.** Anyone from `consent-outreach.md` who asks to be pulled moves to `pulled` in the consent log and comes off the page the same day. That promise is what makes the T2 ship-and-log ruling defensible.

## Wave status (2026-08-02)

| Wave | Issues | State |
|---|---|---|
| 1 | #594 inventory · #595 LinkedIn · #597 copy · #596 CSS | Merged, closed |
| 2 | #598 curate + consent log | Merged, closed |
| 3 | #599 payload rebuild · #600 outreach packet | Merged, closed |
| Gate | [#601](https://github.com/WalksWithASwagger/kriskrug-wp/issues/601) pixel-gate theme deploy | **Open, human-gated** |
| Gate | [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602) snapshot-gate page deploy | **Open, human-gated** |

Everything is on `main`. **Nothing new is live:** Aurora 1.5.8 sits in the repo while production runs 1.5.7, and page 2409 still shows the v1 body. Both gates are KK's to open.

## Notes for whoever picks this up next

- **Notion auth:** the direct API token is invalid. Use the workspace plugin/connector. Do not burn time re-trying the raw token.
- **Simon Haworth's LinkedIn slug changed.** Old `linkedin.com/in/simon-haworth` 404s; the live page was hotfixed 2026-08-01 to `ca.linkedin.com/in/simon-haworth-uk-us-prc`. Use the new one everywhere.
- **Two stat chips rest on KK's word,** not a document: RAP 9.5/10 and ~2,400 attendees in 2024, both footnoted as such in `copy-v2.md`. Swap the footnote to a file path if an export ever lands.
- **Membership is 300 at $340/year** per KK's 2026-08-01 ruling. `bc-ai.ca/about` still says 250+ and needs its own fix in that repo.
- **Voicecheck flags here are expected.** The ones that fire sit inside verbatim third-party quotes, preserved unedited on purpose. Do not "fix" someone else's words to satisfy the checker.
- **Five editorial judgment calls** are flagged inline in `curated-set-v2.md` for KK: the Featured three, Peter Bowles's profanity quote, Rob Cottingham appearing twice, two v1 Featured picks moved to Rooms, and two people held out for identity ambiguity.

---

# v1: shipped 2026-08-01 (history)

| Item | Status |
|---|---|
| Inventory + curated set | Done, 19 enriched quotes |
| Payload + page-map | Done (markers include Simon/Suzy/Landon/Josh) |
| Dry-run / live execute | Merged via [PR #582](https://github.com/WalksWithASwagger/kriskrug-wp/pull/582) (`f066693`); enrichment via [#584](https://github.com/WalksWithASwagger/kriskrug-wp/pull/584) |
| Cache-bypass verify | PASS |
| Rollback manifest | `backup/20260801-testimonials/rollback-testimonials-2409.json` |

**v1 clearance rules** (superseded by `consent-log.md`, kept for context): ship freely = public LinkedIn captures, quotes already live, keynote-bank named lines. KK-decide = Luma named survey quotes, aggressive shortening, optional archive extras.

## Exact deploy commands

These are what [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602) runs. Dry-run first, always. For v2 use a fresh snapshot dir (e.g. `backup/20260802-testimonials-v2/page-snapshots`) so the v1 rollback baseline stays intact.

```bash
# Dry-run
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots

# Execute
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots \
  --execute

# Rollback
varlock run --inject vars -- \
  scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir backup/20260801-testimonials/page-snapshots \
  --restore
```

Public verify: `https://kriskrug.co/testimonials/?cb=<timestamp>`

## Open follow-ups for KK

1. Open the [#601](https://github.com/WalksWithASwagger/kriskrug-wp/issues/601) pixel gate to deploy Aurora 1.5.8, then the [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602) snapshot gate to publish the v2 body.
2. Rule on the five editorial calls in `curated-set-v2.md`.
3. Send (or hand back) the 8 outreach messages in `consent-outreach.md`.
4. Supply contacts for Harrison Reed, Becky Pallack, Sev Geraskin, who have no resolved public channel.
