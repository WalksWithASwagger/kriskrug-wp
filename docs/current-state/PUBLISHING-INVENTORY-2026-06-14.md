# Publishing Inventory — local draft packs ⇄ live WordPress

**Generated:** 2026-06-14 (read-only reconciliation for issue #75, acceptance criterion 5)
**Method:** every `content/drafts/*` pack matched to live kriskrug.co by slug (ID-keyed `wp-draft-NNNNN` folders matched by ID), all statuses, via authenticated WP REST `context=edit`.

## Why this exists

The 2026-05-15 overwrite happened because nobody had a definitive map of which local pack corresponded to which live WP post — the connector updated post 11765 (a live "Web Summit" post) believing it was a fresh draft. This inventory is that map. **Before any connector run, confirm the target draft's row here.**

## Summary

- **10 live** (`publish`)
- **9 scheduled** (`future`)
- **1 private**
- **32 WP drafts** (exist on WP, not yet live)
- **5 local-only** (no WP post — safe to CREATE; no slug collision)
- **Total: 57 local packs**

## Safety property (current connector)

Under the CREATE-only default, running the connector on any of the **52 slugs that already exist on WP** will find the slug and **abort** (no `--update` passed) — so a repeat of the incident is structurally blocked for every mapped pack. The 5 local-only packs are the only ones a plain run would CREATE.

## Live (`publish`) — never `--update` without explicit, verified intent

| WP ID | Status | Date | Slug | Local pack |
|---|---|---|---|---|
| 11826 | publish | 2026-05-07 | `web-summit-vancouver-2026` | 2026-05-07-web-summit-vancouver-2026 |
| 11765 | publish | 2026-05-14 | `calling-us-all-in` | 2026-05-14-calling-us-all-in |
| 11178 | publish | 2026-05-15 | `your-taste-is-your-moat` | wp-draft-11178-post-11178 |
| 10594 | publish | 2026-05-16 | `make-culture-not-content` | wp-draft-10594-post-10594 |
| 11936 | publish | 2026-05-23 | `you-cant-drink-data` | 2026-05-23-you-cant-drink-data |
| 12033 | publish | 2026-06-03 | `agent-orchestrators-creative-insurgents-the-new-stack` | 2026-05-24-agent-orchestrators-creative-insurgents-the-new-stack |
| 12183 | publish | 2026-06-04 | `ai-keynote-slides-visual-workflow` | 2026-06-04-ai-keynote-slides-visual-workflow |
| 12184 | publish | 2026-06-04 | `canada-ai-for-all-strategy-skeptical-guide` | 2026-06-04-canada-ai-for-all-strategy-skeptical-guide |
| 11877 | publish | 2026-06-13 | `i-wont-fake-the-people-who-showed-up` | 2026-05-21-i-wont-fake-the-people-who-showed-up |
| 11878 | publish | 2026-06-13 | `speak-it-into-existence-ai-voice-first-workflows` | 2026-05-21-speak-it-into-existence-ai-voice-first-workflows |

## Scheduled (`future`) — the approved cadence queue

| WP ID | Status | Date | Slug | Local pack |
|---|---|---|---|---|
| 11905 | future | 2026-06-16 | `sovereign-ai-for-whom` | 2026-05-13-sovereign-ai-for-whom |
| 12257 | future | 2026-06-18 | `why-we-built-the-responsible-ai-professional-certification` | 2026-05-16-why-we-built-the-responsible-ai-professional-certification |
| 12263 | future | 2026-06-20 | `god-skills-agentic-loop-workflows` | 2026-06-07-god-skills-agentic-loop-workflows |
| 12190 | future | 2026-06-22 | `the-great-canadian-proximity-game` | 2026-06-04-the-great-canadian-proximity-game |
| 12035 | future | 2026-06-24 | `ai-wont-fix-your-broken-permit-process` | 2026-05-24-ai-wont-fix-your-broken-permit-process |
| 12030 | future | 2026-06-26 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | 2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one |
| 12032 | future | 2026-06-28 | `what-would-chat-do-and-why-thats-the-wrong-question` | 2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question |
| 12034 | future | 2026-06-30 | `zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey` | 2026-05-24-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey |
| 11879 | future | 2026-07-02 | `ai-media-appearances-podcast-guesting` | 2026-05-19-ai-media-appearances-podcast-guesting |

## Private

| WP ID | Status | Date | Slug | Local pack |
|---|---|---|---|---|
| 11876 | private | 2026-06-11 | `the-75-percent-rule-ai-art-adjacent-work` | 2026-05-21-the-75-percent-rule-ai-art-adjacent-work |

## WP drafts — exist on WP; a CREATE run aborts on slug match (safe)

| WP ID | Status | Date | Slug | Local pack |
|---|---|---|---|---|
| 12274 | draft | 2026-05-06 | `comox-valley-ai-is-becoming-its-own-thing` | 2026-05-06-comox-valley-ai-is-becoming-its-own-thing |
| 11880 | draft | 2026-05-19 | `ai-keynote-chaos-creativity-channelnext` | 2026-05-19-ai-keynote-chaos-creativity-channelnext |
| 11881 | draft | 2026-05-19 | `both-hands-full-ai-creatives-lasalle-college` | 2026-05-19-both-hands-full-ai-creatives-lasalle-college |
| 11882 | draft | 2026-05-19 | `both-hands-full-vancouver-ai-march-2026` | 2026-05-19-both-hands-full-vancouver-ai-march-2026 |
| 11883 | draft | 2026-05-19 | `dear-ai-bass-coast-brain-stage` | 2026-05-19-dear-ai-bass-coast-brain-stage |
| 11884 | draft | 2026-05-19 | `horizons-ai-models-future-machine-learning` | 2026-05-19-horizons-ai-models-future-machine-learning |
| 11885 | draft | 2026-05-19 | `inside-vancouvers-ai-boom-whistler-institute` | 2026-05-19-inside-vancouvers-ai-boom-whistler-institute |
| 11929 | draft | 2026-05-23 | `data-center-protest-signs` | 2026-05-23-data-center-protest-signs |
| 12057 | draft | 2026-05-24 | `born-for-this-co-creative-age` | 2026-05-24-born-for-this-co-creative-age |
| 12058 | draft | 2026-05-24 | `canada-media-fund-prototyping-spektorai` | 2026-05-24-canada-media-fund-prototyping-spektorai |
| 12054 | draft | 2026-05-24 | `community-washed-capitalism-when-volunteering-becomes-unpaid-labor-at-scale` | 2026-05-24-community-washed-capitalism-when-volunteering-becomes-unpaid-labor-at-scale |
| 12049 | draft | 2026-05-24 | `finding-harmony-in-the-age-of-ai-a-digital-alchemists-guide-to-the-future` | 2026-05-24-finding-harmony-in-the-age-of-ai-a-digital-alchemists-guide-to-the-future |
| 12059 | draft | 2026-05-24 | `funding-for-journalism-startups-and-media-companies-in-2023` | 2026-05-24-funding-for-journalism-startups-and-media-companies-in-2023 |
| 12055 | draft | 2026-05-24 | `future-proof-chaos-building-the-creative-tech-utopia` | 2026-05-24-future-proof-chaos-building-the-creative-tech-utopia |
| 12029 | draft | 2026-05-24 | `gender-balance-email-post-vancouver-ai` | 2026-05-24-gender-balance-email-post-vancouver-ai |
| 12050 | draft | 2026-05-24 | `guide-to-hacking-language-and-dismantling-colonialism` | 2026-05-24-guide-to-hacking-language-and-dismantling-colonialism |
| 12031 | draft | 2026-05-24 | `how-a-late-night-brain-dump-became-a-multimedia-thought-leadership-machine` | 2026-05-24-how-a-late-night-brain-dump-became-a-multimedia-thought-leadership-machine |
| 12039 | draft | 2026-05-24 | `how-to-build-an-ungovernable-life-and-why-youd-want-to` | 2026-05-24-how-to-build-an-ungovernable-life-and-why-youd-want-to |
| 12038 | draft | 2026-05-24 | `how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | 2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project |
| 12048 | draft | 2026-05-24 | `human-element-shane-loki-talk` | 2026-05-24-human-element-shane-loki-talk |
| 12053 | draft | 2026-05-24 | `keynote-music-elevation-series-haus-of-owl` | 2026-05-24-keynote-music-elevation-series-haus-of-owl |
| 12040 | draft | 2026-05-24 | `kris-krugs-laws-of-digital-nomadism` | 2026-05-24-kris-krugs-laws-of-digital-nomadism |
| 12036 | draft | 2026-05-24 | `nik-badminton-a-sassy-critique-setting-the-ai-record-straight` | 2026-05-24-nik-badminton-a-sassy-critique-setting-the-ai-record-straight |
| 12060 | draft | 2026-05-24 | `nobel-chemistry-foldit` | 2026-05-24-nobel-chemistry-foldit |
| 12064 | draft | 2026-05-24 | `outline-for-droid-army-post` | 2026-05-24-outline-for-droid-army-post |
| 12061 | draft | 2026-05-24 | `rewiring-education-hacking-the-system-for-an-ai-powered-future` | 2026-05-24-rewiring-education-hacking-the-system-for-an-ai-powered-future |
| 12062 | draft | 2026-05-24 | `smudging-the-lines-humanity-embodiment-and-ai-in-the-creative-process` | 2026-05-24-smudging-the-lines-humanity-embodiment-and-ai-in-the-creative-process |
| 12063 | draft | 2026-05-24 | `the-inside-out-evolution-how-ai-turned-this-old-dogs-brain-inside-out-and-why-youre-next` | 2026-05-24-the-inside-out-evolution-how-ai-turned-this-old-dogs-brain-inside-out-and-why-youre-next |
| 12056 | draft | 2026-05-24 | `the-synthetic-renaissance-beyond-prompts-parameters` | 2026-05-24-the-synthetic-renaissance-beyond-prompts-parameters |
| 12051 | draft | 2026-05-24 | `transmuting-words-into-gold-in-the-age-of-ai` | 2026-05-24-transmuting-words-into-gold-in-the-age-of-ai |
| 12037 | draft | 2026-05-24 | `why-100-young-canadians-are-writing-canadas-ai-future-and-why-bc-needs-to-show-up` | 2026-05-24-why-100-young-canadians-are-writing-canadas-ai-future-and-why-bc-needs-to-show-up |
| 12081 | draft | 2026-05-25 | `cotton-underwear-paradox` | 2026-05-25-cotton-underwear-paradox |

## Local-only — no WP post; these are the CREATE-safe candidates

| WP ID | Status | Date | Slug | Local pack |
|---|---|---|---|---|
| — | local-only | — | `long-road-to-future-proof` | 2026-06-01-long-road-to-future-proof |
| — | local-only | — | `vancouver-ai-community-page` | 2026-06-11-vancouver-ai-community-page |
| — | local-only | — | `vancouver-world-cup-2026-becker-kk-robots` | 2026-06-12-vancouver-world-cup-2026-becker-kk-robots |
| — | local-only | — | `accessibility-statement-2026-05` | accessibility-statement-2026-05 |
| — | local-only | — | `ai-glossary-2026-05` | ai-glossary-2026-05 |
