# Draft Queue Triage, 2026-09-03

Decision sheet for issue #745. **Read-only. No package was moved, renamed, or
deleted to produce this.** Execution waits on KK's ruling per group.

## What the audit actually found

The issue describes "the 28-post 2026-05-24 slop batch + dormant May/June
drafts" as an archive-import batch that fails every content quality standard
and sits "one careless publish run away" from going out. Two corrections:

1. **The batch is 27 packages, not 28.**
2. **21 of the 57 packages in scope are already published.** Five of the
   05-24 batch and sixteen of the May/June singles have a live post at a
   matching slug in `wp-sitemap-posts-post-1.xml`. They are not a publish
   risk, and culling them would delete the source of record for live posts.

The `LOCAL_ONLY=1 make draft-queue-audit` run reports "no WP slug match" for
every package, because in local-only mode it cannot reach WordPress. That
column is not evidence of being unpublished. Publication status below comes
from matching each package slug against the 973 live post URLs in the public
sitemap.

## Scope and method

- 27 packages under `content/drafts/2026-05-24-*`.
- 30 dormant May/June singles under `content/drafts/2026-0[56]-*`.
- Word, link, image, and quality-state figures come from
  `LOCAL_ONLY=1 make draft-queue-audit`.
- Publication status comes from the public post sitemap, fetched 2026-09-03.

## Recommended disposition

| Disposition | Count | Meaning |
|---|---:|---|
| Shipped | 21 | Already live. Keep the package as the source of record and mark it, so no future session mistakes it for an unpublished draft. |
| Rewrite | 6 | Enough substance to be worth showpiece treatment. Each needs its own scoped issue before any work starts. |
| Shelve | 11 | Real material, not a priority. Keep in place with an explicit status marker. |
| Cull | 19 | Thin, no images, no links, and no live post. Move to `content/drafts/archive/`, which is a move, not a delete. |

Rules applied, in order: already live wins over everything; then a strong
local candidate or 1,500-plus words means rewrite; then under 800 words with
no images means cull; everything else shelves. Where a package sits near a
boundary, the recommendation is the softer option.


### SHIPPED (21)

| Package | Group | Words | Links | Images | Audit state |
|---|---|---:|---:|---:|---|
| `2026-05-13-sovereign-ai-for-whom` | May/June single | 4109 | 80 | 6 | strong local candidate |
| `2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | 05-24 batch | 4051 | 5 | 0 | needs media/taxonomy pass |
| `2026-05-24-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey` | 05-24 batch | 3610 | 7 | 0 | needs media/taxonomy pass |
| `2026-06-04-ai-keynote-slides-visual-workflow` | May/June single | 3539 | 14 | 7 | strong local candidate |
| `2026-06-04-canada-ai-for-all-strategy-skeptical-guide` | May/June single | 3429 | 44 | 0 | needs media/taxonomy pass |
| `2026-06-28-keep-the-machine-strange` | May/June single | 2675 | 26 | 2 | strong local candidate |
| `2026-06-07-god-skills-agentic-loop-workflows` | May/June single | 2165 | 5 | 5 | needs media/taxonomy pass |
| `2026-05-07-web-summit-vancouver-2026` | May/June single | 2149 | 23 | 10 | needs media/taxonomy pass |
| `2026-05-24-agent-orchestrators-creative-insurgents-the-new-stack` | 05-24 batch | 2005 | 2 | 0 | needs media/taxonomy pass |
| `2026-05-14-calling-us-all-in` | May/June single | 2002 | 52 | 6 | needs media/taxonomy pass |
| `2026-05-24-ai-wont-fix-your-broken-permit-process` | 05-24 batch | 1966 | 5 | 0 | needs media/taxonomy pass |
| `2026-06-16-storyhive-haus-of-owl-jordan-dack` | May/June single | 1776 | 42 | 6 | needs media/taxonomy pass |
| `2026-05-21-speak-it-into-existence-ai-voice-first-workflows` | May/June single | 1611 | 7 | 1 | needs media/taxonomy pass |
| `2026-05-23-data-center-protest-signs` | May/June single | 1422 | 5 | 14 | needs media/taxonomy pass |
| `2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question` | 05-24 batch | 1419 | 6 | 0 | needs media/taxonomy pass |
| `2026-05-16-why-we-built-the-responsible-ai-professional-certification` | May/June single | 1278 | 11 | 3 | needs media/taxonomy pass |
| `2026-06-23-ethos-lab-block-party` | May/June single | 1097 | 13 | 7 | thin source draft |
| `2026-06-04-the-great-canadian-proximity-game` | May/June single | 972 | 15 | 0 | thin source draft |
| `2026-06-23-vancouver-made-world-cup` | May/June single | 879 | 17 | 11 | thin source draft |
| `2026-05-19-ai-media-appearances-podcast-guesting` | May/June single | 759 | 19 | 0 | thin source draft |
| `2026-05-23-you-cant-drink-data` | May/June single | 0 | 0 | 0 | unknown |

### REWRITE (6)

| Package | Group | Words | Links | Images | Audit state |
|---|---|---:|---:|---:|---|
| `2026-05-24-keynote-music-elevation-series-haus-of-owl` | 05-24 batch | 5215 | 0 | 0 | needs media/taxonomy pass |
| `2026-05-24-gender-balance-email-post-vancouver-ai` | 05-24 batch | 4061 | 0 | 0 | needs media/taxonomy pass |
| `2026-05-06-comox-valley-ai-is-becoming-its-own-thing` | May/June single | 3014 | 10 | 0 | needs media/taxonomy pass |
| `2026-06-28-context-creators` | May/June single | 2309 | 25 | 7 | needs media/taxonomy pass |
| `2026-05-25-cotton-underwear-paradox` | May/June single | 1997 | 12 | 4 | needs media/taxonomy pass |
| `2026-05-21-the-75-percent-rule-ai-art-adjacent-work` | May/June single | 1793 | 9 | 1 | needs media/taxonomy pass |

### SHELVE (11)

| Package | Group | Words | Links | Images | Audit state |
|---|---|---:|---:|---:|---|
| `2026-05-24-transmuting-words-into-gold-in-the-age-of-ai` | 05-24 batch | 1463 | 0 | 0 | needs media/taxonomy pass |
| `2026-05-21-i-wont-fake-the-people-who-showed-up` | May/June single | 1462 | 6 | 1 | needs media/taxonomy pass |
| `2026-05-24-kris-krugs-laws-of-digital-nomadism` | 05-24 batch | 1366 | 0 | 0 | needs media/taxonomy pass |
| `2026-06-18-creative-ai-human-lab-network` | May/June single | 1365 | 20 | 0 | needs media/taxonomy pass |
| `2026-05-24-guide-to-hacking-language-and-dismantling-colonialism` | 05-24 batch | 1263 | 0 | 0 | needs media/taxonomy pass |
| `2026-05-24-how-a-late-night-brain-dump-became-a-multimedia-thought-leadership-machine` | 05-24 batch | 1125 | 0 | 0 | thin source draft |
| `2026-05-24-finding-harmony-in-the-age-of-ai-a-digital-alchemists-guide-to-the-future` | 05-24 batch | 1112 | 0 | 0 | thin source draft |
| `2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | 05-24 batch | 1104 | 5 | 2 | thin source draft |
| `2026-05-24-how-to-build-an-ungovernable-life-and-why-youd-want-to` | 05-24 batch | 1047 | 3 | 0 | thin source draft |
| `2026-05-24-why-100-young-canadians-are-writing-canadas-ai-future-and-why-bc-needs-to-show-up` | 05-24 batch | 929 | 8 | 0 | thin source draft |
| `2026-05-24-human-element-shane-loki-talk` | 05-24 batch | 875 | 0 | 7 | thin source draft |

### CULL (19)

| Package | Group | Words | Links | Images | Audit state |
|---|---|---:|---:|---:|---|
| `2026-05-24-nobel-chemistry-foldit` | 05-24 batch | 764 | 0 | 0 | thin source draft |
| `2026-05-24-smudging-the-lines-humanity-embodiment-and-ai-in-the-creative-process` | 05-24 batch | 760 | 0 | 0 | thin source draft |
| `2026-05-19-both-hands-full-ai-creatives-lasalle-college` | May/June single | 749 | 4 | 0 | thin source draft |
| `2026-05-24-outline-for-droid-army-post` | 05-24 batch | 662 | 2 | 0 | thin source draft |
| `2026-05-19-inside-vancouvers-ai-boom-whistler-institute` | May/June single | 644 | 4 | 0 | thin source draft |
| `2026-05-24-canada-media-fund-prototyping-spektorai` | 05-24 batch | 626 | 0 | 0 | thin source draft |
| `2026-05-24-community-washed-capitalism-when-volunteering-becomes-unpaid-labor-at-scale` | 05-24 batch | 597 | 0 | 0 | thin source draft |
| `2026-05-24-funding-for-journalism-startups-and-media-companies-in-2023` | 05-24 batch | 556 | 0 | 0 | thin source draft |
| `2026-05-19-both-hands-full-vancouver-ai-march-2026` | May/June single | 554 | 4 | 0 | thin source draft |
| `2026-05-19-horizons-ai-models-future-machine-learning` | May/June single | 488 | 4 | 0 | thin source draft |
| `2026-05-19-ai-keynote-chaos-creativity-channelnext` | May/June single | 486 | 4 | 0 | thin source draft |
| `2026-05-24-the-inside-out-evolution-how-ai-turned-this-old-dogs-brain-inside-out-and-why-youre-next` | 05-24 batch | 427 | 0 | 0 | thin source draft |
| `2026-05-19-dear-ai-bass-coast-brain-stage` | May/June single | 424 | 4 | 0 | thin source draft |
| `2026-05-24-the-synthetic-renaissance-beyond-prompts-parameters` | 05-24 batch | 398 | 0 | 0 | thin source draft |
| `2026-05-24-rewiring-education-hacking-the-system-for-an-ai-powered-future` | 05-24 batch | 391 | 0 | 0 | thin source draft |
| `2026-05-24-future-proof-chaos-building-the-creative-tech-utopia` | 05-24 batch | 388 | 0 | 0 | thin source draft |
| `2026-06-12-vancouver-world-cup-2026-becker-kk-robots` | May/June single | 249 | 0 | 0 | thin source draft |
| `2026-05-24-born-for-this-co-creative-age` | 05-24 batch | 219 | 0 | 0 | thin source draft |
| `2026-06-11-vancouver-ai-community-page` | May/June single | 0 | 0 | 0 | unknown |

## What happens after KK rules

Nothing in this list is acted on until KK rules per group. Then, per #745:

1. Culled packages **move** to `content/drafts/archive/`. They are not deleted.
2. Shelved packages get a `STATUS: shelved` line in their folder.
3. Shipped packages get a `STATUS: shipped` line naming the live URL.
4. Rewrite candidates each get their own scoped issue.
5. Re-run `LOCAL_ONLY=1 make draft-queue-audit` and confirm the queue reads
   truthfully, with no `2026-05-24-*` package left unmarked.

## Open question for KK

The "shipped" group is the one worth a decision beyond cull/rewrite/shelve.
These 21 packages are the local source for posts already on the site. Options:
keep them in `content/drafts/` with a status marker, or move them to a
`content/drafts/published/` directory so the active queue only ever contains
genuinely unpublished work. The second is tidier but touches 21 packages, so
it is KK's call rather than a default.
