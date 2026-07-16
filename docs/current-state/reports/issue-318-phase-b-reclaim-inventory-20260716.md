# Issue #318 Phase B — draft image reclaim inventory

**Captured:** `2026-07-16T01:46:00Z` (public REST slug probes only; **no deletions**; no auth).
**Parent:** #318 / #369

## Scope

- Draft dirs with images totaling ≥0.5MB: **19** (~**222 MB**)
- Published-candidate (public `status=publish` slug match): **16**
- Not found publicly / likely unpublished: **3**

## Published candidates (KK-gated: delete `images/` only after auth confirm)

| MB | Images | Dir | Live ID | Slug |
|---:|---:|---|---:|---|
| 42.1 | 14 | `2026-05-23-data-center-protest-signs` | 11929 | `data-center-protest-signs` |
| 34.9 | 13 | `2026-05-16-why-we-built-the-responsible-ai-professional-certification` | 12257 | `why-we-built-the-responsible-ai-professional-certification` |
| 29.5 | 10 | `2026-05-07-web-summit-vancouver-2026` | 11826 | `web-summit-vancouver-2026` |
| 23.9 | 6 | `2026-05-13-sovereign-ai-for-whom` | 11905 | `sovereign-ai-for-whom` |
| 22.7 | 6 | `2026-06-07-god-skills-agentic-loop-workflows` | 12263 | `god-skills-agentic-loop-workflows` |
| 8.2 | 4 | `2026-06-04-ai-keynote-slides-visual-workflow` | 12183 | `ai-keynote-slides-visual-workflow` |
| 7.5 | 11 | `2026-06-23-vancouver-made-world-cup` | 12363 | `vancouver-made-world-cup` |
| 4.1 | 2 | `2026-06-04-the-great-canadian-proximity-game` | 12190 | `the-great-canadian-proximity-game` |
| 4.0 | 8 | `2026-06-16-storyhive-haus-of-owl-jordan-dack` | 12327 | `storyhive-haus-of-owl-jordan-dack` |
| 4.0 | 2 | `2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question` | 12032 | `what-would-chat-do-and-why-thats-the-wrong-question` |
| 3.4 | 7 | `2026-06-23-ethos-lab-block-party` | 12357 | `ethos-lab-block-party` |
| 3.2 | 2 | `2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` |
| 3.2 | 2 | `2026-05-24-ai-wont-fix-your-broken-permit-process` | 12035 | `ai-wont-fix-your-broken-permit-process` |
| 3.0 | 2 | `2026-07-07-the-cheer-is-a-cap-table` | 12479 | `the-cheer-is-a-cap-table` |
| 2.5 | 6 | `2026-05-14-calling-us-all-in` | 11765 | `calling-us-all-in` |
| 1.4 | 2 | `2026-07-05-artists-learn-machines-extract` | 12473 | `artists-learn-machines-extract` |

## Not reclaimable yet

| MB | Images | Dir | Slug guess | Disposition |
|---:|---:|---|---|---|
| 19.2 | 7 | `2026-05-24-human-element-shane-loki-talk` | `human-element-shane-loki-talk` | not-found-public-or-unpublished |
| 2.9 | 2 | `2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | `how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | not-found-public-or-unpublished |
| 2.3 | 4 | `2026-05-25-cotton-underwear-paradox` | `cotton-underwear-paradox` | not-found-public-or-unpublished |

## Rules before any delete PR

1. Authenticated confirm of slug/ID + `publish` status (Cloud secrets) — public miss ≠ safe to delete.
2. One `content:`-lane PR; keep markdown/html; remove only `images/*` for published drafts.
3. Stub: assets live in WP media; originals in git history.
4. No Phase C `filter-repo` until A/B done and KK coordinates a mirror backup.

JSON twin: `issue-318-phase-b-reclaim-inventory-20260716.json`
