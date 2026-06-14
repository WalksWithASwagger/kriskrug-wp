# Rafiki image selection — image-blocked draft queue (2026-06-14)

Gate for KK: pick one image per draft (or request a regen / supply a real asset). Nothing is uploaded to WordPress until you select. Rejected media `12264`–`12270` remain detached and must not be reused.

All candidates are 16:9, generated against each draft's `image-brief.md`, honoring its style lane and refusal lines (no robots, no fake UI, no glowing brains, no fake people unless noted).

## Ready to pick (4 drafts)

| Draft | WP ID | Style | Candidates | My pick | Notes |
|---|---|---|---|---|---|
| The Great Canadian Proximity Game | 12190 | hopecode | `images/rafiki-v1.png`, `rafiki-v2.png` | **v2** | v2 has the clean "THE PROXIMITY GAME" title; v1 headline misreads "PROXIIITY". v2 side-label slightly garbled but minor. |
| AI Won't Fix Your Broken Permit Process | 12035 | aefl | `images/rafiki-v1.png`, `rafiki-v2.png` | **v1** | v1 whiteboard audit is cleaner; v2 bottleneck label garbles to "BOTTLENOTECK". |
| Canada Doesn't Need a Bigger AI Machine | 12030 | aefl | `images/rafiki-v1.png`, `rafiki-v2.png` | **either** | Both clean + legible. v1 = column ledger; v2 = balance-scale metaphor (BETTER vs BIGGER). |
| What Would Chat Do? | 12032 | hopecode | `images/rafiki-v1.png`, `rafiki-v2.png` | **either** | Both clean. v1 = wider mirror map w/ hand; v2 = tight PERSON↔MODEL loop under HUMAN AGENCY. |

## Needs your input (3 drafts)

| Draft | WP ID | Issue | Recommendation |
|---|---|---|---|
| How We Did It: SFU SIAT Microcredential | 12038 | Rafiki repeatedly misspells "MICROCREDENTIAL" (both v1/v2 say "MICROCREDENIAL"); v2 also inserted a face. | Brief's preferred source was a **real project artifact / screenshot** anyway — supply one, or accept v1 with a title fix/overlay. Candidates staged at `images/rafiki-v1.png`, `rafiki-v2.png`. |
| Zero to One: From Meetup to Movement | 12034 | Brief: "the stronger path is real BC + AI meetup photography. Rafiki generation is backup only." Refusal: no fake people/crowd. | **Supply a real meetup/event photo.** I did not generate fake community imagery. |
| AI Media Appearances / Podcast Guesting | 11879 | Brief: real media still / press image / headshot preferred; Rafiki backup only. Refusal: no fake broadcasters. | **Supply a real press still or headshot,** or approve a proof-stack collage built from real sources. I did not fabricate media imagery. |

## After you pick
For each selected image I will: upload via `kk_notion_to_wp.py` media flow (with alt text), set it as the draft's featured media, and record the new media ID here — then the draft moves to preview QA (#207). All of that stops again at your approval before any schedule/publish.
