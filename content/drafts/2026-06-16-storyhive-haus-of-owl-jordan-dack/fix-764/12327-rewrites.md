# Post 12327: the 21 em-dash rewrites

Scan the right column. Every dash got its own decision: comma, colon, period, or a
reworked sentence. Nothing was find-and-replaced.

Source: live `content.raw` readback 2026-08-15 (`12327-baseline-20260815.json`).
Result: `12327-content-payload.html`, 0 × U+2014, 0 × `&mdash;`.

| # | Fix | Before | After |
|---|---|---|---|
| 1 | comma | in downtown Victoria **—** unceded Lekwungen territories, acknowledged on air | in downtown Victoria**, on** unceded Lekwungen territories, acknowledged on air |
| 2 | colon | This post is the cited companion **—** names, links, and the ideas in one place. | This post is the cited companion**:** names, links, and the ideas in one place. |
| 3 | new sentence | …dancers, and poets **—** studio access, mentorship, the Garden as communal core, and a downtown Victoria address… | …dancers, and poets**. It runs on** studio access, mentorship, the Garden as communal core, and a downtown Victoria address… |
| 4 | new sentence | produces and hosts **Creative or Die** **—** poet, songwriter, and the kind of interviewer who… | produces and hosts **Creative or Die**. **He is a** poet, **a** songwriter, and the kind of interviewer who… |
| 5, 6 | paired commas | part of **STORYHIVE On Location** **—** TELUS's documentary and creator funding lane **—** produced here… | part of **STORYHIVE On Location****,** TELUS's documentary and creator funding lane**,** produced here… |
| 7 | colon | framed the middle as **Both Hands Full** **—** skepticism in one hand, curiosity in the other. | framed the middle as **Both Hands Full****:** skepticism in one hand, curiosity in the other. |
| 8 | colon | It was coming for the **orbit** **—** briefs, budgets, contact sheets… | It was coming for the **orbit****:** briefs, budgets, contact sheets… |
| 9, 10 | three short sentences | …already out in the world **—** blog posts, talks, photos, half-finished ideas **—** so I can ask better questions… | …already out in the world**. Blog** posts, talks, photos, half-finished ideas**. It lets me** ask better questions… |
| 11 | period | Art is weirder **—** process, embodiment, relationship, the thing that does not compress… | Art is weirder**. It runs on** process, embodiment, relationship, the thing that does not compress… |
| 12 | colon (alt text) | Vancouver AI March 2026 community talk **—** real room, real people | Vancouver AI March 2026 community talk**:** real room, real people |
| 13 | period + colon | format**:** roughly four hours **—** networking, two-hour program, networking again. | format**.** Roughly four hours**:** networking, two-hour program, networking again. |
| 14 | reworded, no punctuation | **BC + AI** as the front door **—** membership, events, and the wider ecosystem map. | **BC + AI** **is** the front door **for** membership, events, and the wider ecosystem map. |
| 15 | colon | tracked my pipeline epochs **—** Midjourney jams, knowledge bases and named assistants, then **agentic workflows**… | tracked my pipeline epochs **in order:** Midjourney jams, **then** knowledge bases and named assistants, then **agentic workflows**… |
| 16 | comma | slang, self-correction **—** the mess typing often strips out. | slang, self-correction**, all** the mess typing often strips out. |
| 17 | reworded | certification we built with **BC + AI** **—** trust, disclosure, and human relationships as curriculum, not slide-deck garnish. | certification we built with **BC + AI****, where** trust, disclosure, and human relationships **are the** curriculum, not slide-deck garnish. |
| 18 | reworded (alt text) | Responsible AI Professional certification **—** BC plus AI | Responsible AI Professional certification **from** BC plus AI |
| 19, 20 | restructured | build a **public-interest AI identity** **—** green where possible, Indigenous-led data governance where required, culture reserved a seat at the compute table **—** instead of photocopying Palo Alto. | build a **public-interest AI identity** instead of photocopying Palo Alto**. Green** where possible, Indigenous-led data governance where required, culture reserved a seat at the compute table. |
| 21 | period | the life raft is not faster dashboards **—** it is trusted rooms, honest witness… | the life raft is not faster dashboards**. It is** trusted rooms, honest witness… |

Punctuation mix across the 21: 3 commas, 5 colons, 6 periods or sentence splits,
2 paired commas, 5 rewordings that need no punctuation at all.

## Two more dashes outside `content` (KK decides)

Not in the 21, not in the issue's acceptance criteria, and **not** in the apply
script. Same rule, different fields, so they are here rather than lost.

| Field | Before | Proposed |
|---|---|---|
| `excerpt` | …at Haus of Owl in Victoria **—** territory acknowledged, facts-or-fiction warm-up… | …at Haus of Owl in Victoria**. Territory** acknowledged, facts-or-fiction warm-up… |
| `meta.advanced_seo_description` | …with Jordan Dack at Haus of Owl **—** both hands full, AI as mirror… | …with Jordan Dack at Haus of Owl**:** both hands full, AI as mirror… |

Both are already fixed in `post.md`'s front matter, so a re-emit will carry them.
Pushing them live is a separate, one-field PATCH each. Jetpack SEO meta has a
history of silently no-op'ing on this site, so verify `advanced_seo_description`
with a readback rather than trusting the 200.
