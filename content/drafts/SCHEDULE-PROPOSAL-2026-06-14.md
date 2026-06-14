# Proposed 2-day publish schedule — 2026-06-14 (#208)

Gate for KK: approve this date table (and which drafts are in it) before any live scheduling run. Cadence per `PUBLISH-QUEUE-2026-06-11.md`: 9:00 AM Pacific, every two days, first slot ≥12h after approval. Already-scheduled `11876` (2026-06-11) and `11878` (2026-06-13) are excluded — they're handled. `you-cant-drink-data` stays held (coordinated 3-post drop).

## Tier 1 — ready now (no image blocker; pending KK source/preview approval)
First open slot is **2026-06-16 09:00 PT** (≥12h after a 2026-06-14 approval), then every 2 days.

| Slot | Date (09:00 PT) | Draft | WP ID | Outstanding gate |
|---|---|---|---|---|
| 1 | 2026-06-16 | Sovereign AI for Whom? | 11905 | KK source/fact review + BC+AI claims |
| 2 | 2026-06-18 | Why We Built the Responsible AI Professional Certification | 12257 | confirm current cohort language |
| 3 | 2026-06-20 | Ask the Right Skill First (Agentic Workflows) | 12263 | "God Skills" naming + generated-image text approval |
| 4 | 2026-06-22 | I Won't Fake the People Who Showed Up | 11877 | documentary-ethics framing + portrait choice |

## Tier 2 — image-blocked, slot in after image selection (see IMAGE-SELECTION-2026-06-14.md)
Append to the cadence in this order once each has an approved featured image. Dates assume they follow Tier 1; they shift earlier if any Tier 1 draft is skipped.

| Order | Date (09:00 PT) | Draft | WP ID | Image status |
|---|---|---|---|---|
| 5 | 2026-06-24 | The Great Canadian Proximity Game | 12190 | Rafiki v2 staged — pick |
| 6 | 2026-06-26 | AI Won't Fix Your Broken Permit Process | 12035 | Rafiki v1 staged — pick |
| 7 | 2026-06-28 | Canada Doesn't Need a Bigger AI Machine | 12030 | Rafiki v1/v2 staged — pick |
| 8 | 2026-06-30 | What Would Chat Do? | 12032 | Rafiki v1/v2 staged — pick |
| 9 | TBD | How We Did It: SFU SIAT Microcredential | 12038 | needs real artifact or title fix |
| 10 | TBD | Zero to One: From Meetup to Movement | 12034 | needs real meetup photo |
| 11 | TBD | AI Media Appearances | 11879 | needs real press still/headshot |

## Execution (after KK approves a row)
Per draft, with KK present (live write): `make status-readonly` → publisher dry-run → confirm slug/ID identity → set WP status `future` with the slot datetime via `kk_notion_to_wp.py` (slug-idempotent, `--update` only with title-similarity guard) → verify in WP → record run notes. Public render checked logged-out after each goes live.

## Notes
- Dates are proposals; first date keys off the actual approval timestamp (≥12h rule).
- Tier 2 dates are placeholders that compress upward if Tier 1 items are skipped or if you want image drafts interleaved sooner.
