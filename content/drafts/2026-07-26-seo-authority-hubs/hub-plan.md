# Hub plan - surprising search wins → authority hubs (#402)

**Goal:** Turn isolated ranking posts into linked authority hubs that also route traffic toward BC + AI, Futureproof, Punk Rock AI, and speaking/profile pages.

**Constraint:** This packet proposes hubs and link maps only. No live WordPress writes.

## Proposed hubs (5)

| # | Hub working title | Proposed slug / URL | Primary queries served | Build posture |
|---|---|---|---|---|
| 1 | Most Benevolent Outcomes | `/most-benevolent-outcomes/` (new page) or Field Notes hub section | `most benevolent outcome`, `most benevolent outcome prayer` | **New thin hub page** consolidating the 2023 prayer post + related voice posts |
| 2 | Clean AI Infrastructure (You Can't Drink Data) | Section on `/ai-ethics/` + optional `/you-cant-drink-data/` redirect stays on post | `you cant drink data` | **Extend existing** `/ai-ethics/` hub; do not fork a second ethics home |
| 3 | Vancouver AI Community Meetup | `/vancouver-ai/` (existing) | `vancouver ai community meetup` | **Refresh existing** hub: meetup FAQ, Luma CTA, Futureproof bridge |
| 4 | Photography & Model Craft Archive | `/photography/` or `/model-craft/` (new page) | `modelmayhem.com`, `hardcore photoshoot`, `negotiation equipment for photographers` | **New hub page**; category archive alone is not enough |
| 5 | Cyber Love Garden / Creative AI Experiences | Section on `/ai-for-creatives/` (existing) | `cyber love garden` (+ creative AI spillover) | **Extend existing** creatives hub; optional short companion outline |

**Person authority (not a separate hub outline):** `krug ai` and `matt mckenna miami` resolve through About/Speaking + interview links rather than new topical hubs.

## Internal link map

Direction legend: `→` = add link from source to target (draft proposal). Prefer natural anchors already in copy when possible (#328 pattern).

### Hub 1 - Most Benevolent Outcomes

```
community-weaving (2950) → most-benevolent post (3814)     [#328 ready]
embracing-the-future (2665) → most-benevolent post (3814)  [#328 ready]
most-benevolent post → /most-benevolent-outcomes/ hub (new)
most-benevolent post → /speaking/
most-benevolent post → /about/
most-benevolent post → /ai-ethics/   (optimistic AI voice ↔ ethics lane)
hub → Punk Rock AI post
hub → /vancouver-ai/
```

### Hub 2 - Clean AI / You Can't Drink Data

```
you-cant-drink-data → /ai-ethics/
you-cant-drink-data → BC + AI launch post (/bc-ai/ redirect)
you-cant-drink-data → long-road-to-futureproof
you-cant-drink-data → punk-rock-ai
you-cant-drink-data → /speaking/
/ai-ethics/ → you-cant-drink-data   (already in pillar draft)
canada-ai-for-all-strategy-skeptical-guide → you-cant-drink-data
cotton-underwear-paradox (if live) → you-cant-drink-data
```

### Hub 3 - Vancouver AI Community Meetup

```
legacy meetup posts → /vancouver-ai/
/vancouver-ai/ → https://lu.ma/vancouver-ai
/vancouver-ai/ → https://bc-ai.ca/ + /events/ + /membership/
/vancouver-ai/ → long-road-to-futureproof + https://www.futureproof.website/
/vancouver-ai/ → punk-rock-ai + /speaking/
lunch-meetup-2023-10-20 → /vancouver-ai/ + inaugural meetup + BC + AI live
```

### Hub 4 - Photography & Model Craft Archive

```
kk-on-modelmayhemcom → /photography/ hub (new)
checklist-of-model-photographer-negotiation-items → /photography/ hub
hardcore-superstar-photoshoot → /photography/ hub
hub → category/photography-visual-storytelling/
hub → wannabe-fashion-photographers (1222)
hub → /about/ + /speaking/ (career through-line: photographer → AI community builder)
modelmayhem post ↔ negotiation checklist (bidirectional)
```

### Hub 5 - Cyber Love Garden / Creative AI

```
cyber-love-garden → /ai-for-creatives/
cyber-love-garden → punk-rock-ai
cyber-love-garden → /vancouver-ai/
cyber-love-garden → long-road-to-futureproof / Futureproof site
/ai-for-creatives/ → cyber-love-garden (featured card)
```

### Cross-lane minimum (issue acceptance: ≥5 old→strategic links)

These five alone satisfy the "old search winners → current strategic pages" bar once applied live (KK-gated):

1. you-cant-drink-data → BC + AI launch / Futureproof / Punk Rock AI / speaking (pick ≥2)
2. most-benevolent post → speaking or about
3. modelmayhem → photography hub → about/speaking
4. cyber-love-garden → ai-for-creatives + Futureproof
5. vancouver lunch meetup (2023) → /vancouver-ai/ + bc-ai.ca

## Schema guidance (draft for later live apply)

| Surface | Suggested schema | Notes |
|---|---|---|
| Hub pages (new/refresh) | `WebPage` + `BreadcrumbList` + optional `FAQPage` | FAQ only when answers are real, not stuffed |
| Ranking posts | `Article` / `BlogPosting` (publisher rules per #425) | Keep existing Article-family once #425 is live |
| About / Speaking | `Person` (+ `Organization` for BC + AI mentions where accurate) | Do not invent Organization claims |
| Meetup hub | optional `Event` only for a specific dated meetup, not the hub itself | Prefer linking out to Luma events |

## Voice / SEO guardrails for hub copy

- Kris voice: concrete, local, both-hands-full. No booster/doomer binary.
- No em dashes in drafted hub copy.
- No keyword stuffing; one primary query per hub, secondary queries as natural aliases.
- Prefer consolidating existing posts over writing full new essays in this packet.
- Live publish, Search Console submit, and Pagely purge remain KK-gated (`SEO-INDEXING-RUNBOOK.md`).

## Sequencing recommendation

1. Apply #328 most-benevolent contextual links (smallest, already specified).
2. Refresh `/vancouver-ai/` meetup FAQ + external CTAs (existing page).
3. Add ethics reciprocal links around you-cant-drink-data.
4. Ship new photography hub page (largest net-new).
5. Ship most-benevolent hub page (or Field Notes landing) after prayer-post meta trim.
6. Fold cyber-love-garden into `/ai-for-creatives/` card row.

## Out of scope for this PR

- Live REST body/meta edits
- Search Console validation clicks
- Analytics property setup (Mission Control #71/#72/#76 if needed)
- AGENTS.md / REVIEW.md tone encoding (separate follow-up commit if KK wants agent-infra slice split)
