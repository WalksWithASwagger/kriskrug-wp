# Publications KB gap report v2 — 2026-08-01

Status: Phase 1 research complete for Publications Showpiece plan. **Read-only** against live/payload/KB except this file. No deploy, no `publications.html` edits, no image capture.

Plan ref: `publications_showpiece_design_system_effdc5f9` (Heard-on shelf, In-print credits, The Wall, CBC broadcast, Tier 1 art).

Prior report: [`PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md`](./PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md) (v1 — Power 50 already shipped onto payload; CBC holiday + Bossier deferred; Sandboxing left on Media Appearances).

---

## Sources consulted

| # | Source | Finding for this pass |
|---|---|---|
| 1 | `content/source-packs/keynotes-2026/wp-payloads/publications.html` | Full inventory below |
| 2 | `kk-kb/meta/reports/press-clippings.json` | 47 logged rows; payload covers **all** with working URLs (Vancouver Sun is on Long trail; HTML `&amp;` false-negative only) |
| 3 | `kk-kb/content/people/kris-krug/sources/press.md` | Portfolio.YVR + Power 50 letter — both already on page |
| 4 | `kk-kb/meta/reports/appearances.json` | 47 rows; **every `press: []` empty** — no new URLs from press arrays. CBC Sandboxing series + Web Summit appearances present as appearance records only |
| 5 | `kk-kb/meta/reports/media-credits.json` + `…/media-credits/` | **15 credits** (11 dated + 4 spans) — **zero** on publications page today |
| 6 | `…/broadcast-interviews/` | Sandboxing AI series + Nov 2025 holiday shopping recap/transcript |
| 7 | `…/feature-articles/` | Own/partner authored copy — not third-party tear-sheet material |
| 8 | `…/press-clippings/` + assets + README “tracked elsewhere” / backfill | Holiday clipping `status: verify`; Bossier tracked elsewhere; open Hinton audio ID |
| 9 | Gap report v1 | Dispositions reconciled below |
| 10 | Web / iTunes Lookup (2026-08-01) | CBC player URLs for companions + inauguration; Medium/Top Boss (= Bossier Brand) publish; podcast artwork URLs |

---

## Current page inventory (`publications.html`)

Ledger claims **48 dated entries**. Structure:

### Right now (featured — 3)

| Date | Outlet | Title | Media key | Tier note |
|---|---|---|---|---|
| 2026-07-31 | BIV | Stronger AI ecosystem | `press-2026-07-31-biv-ecosystem-context.jpg` | Tier 2 clip — **recapture** (plan: ad-banner crop) |
| 2026-07-24 | The Tyee | Who Gets a Say in AI Adoption? | `press-2026-07-24-the-tyee-context.jpg` | Tier 2 — **recapture** |
| 2026-06-15 | BIV | Lawyers / AI shakeups | `press-2026-06-15-biv-context.jpg` | Tier 2 — **recapture** |

### Board 4-up (becomes The Wall)

| Stamp | URL | Media key |
|---|---|---|
| VanMag Power 50 | vanmag.com Power 50 2026 list | `press-2026-02-05-vanmag-power50-context.jpg` |
| Byte Club | youtube `uMTBoHIdhdA` | `press-2024-11-21-byte-club.jpg` (Tier 1 video thumb — keep pattern) |
| FOLIO.YVR | folioyvr.com 2024-06 profile | `press-2024-06-01-folio-yvr-context.jpg` |
| BC Studies | ojs.library.ubc.ca 199875 | `press-2025-04-14-bc-studies-context.jpg` |

### The recent run (20 feed rows)

| Date | Type | Title | Image? | Media key |
|---|---|---|---|---|
| 2026-05-20 | STORYHIVE broadcast | On Location: Victoria | yes | `press-2026-05-20-storyhive.jpg` |
| 2026-02-09 | Tela Viva | WAIFF AI audiovisual | yes | `press-2026-02-09-tela-viva-context.jpg` |
| 2026-02-05 | VanMag | Power 50 (2026) | yes | `press-2026-02-05-vanmag-power50-context.jpg` |
| 2025-07-09 | E-ChannelNews | ChannelNext interview | yes | `press-2025-07-09-e-channelnews-context.jpg` |
| 2025-05-01 | Portfolio.YVR | Future Proof Creatives | yes | `press-2025-05-01-portfolio-yvr-context.jpg` |
| 2025-04-14 | BC Studies | Grass Roots AI Community | yes | `press-2025-04-14-bc-studies-context.jpg` |
| 2025-02-11 | Compass Horizons | Exploring AI Models | yes | `press-2025-02-11-compass-horizons-context.jpg` |
| 2025-01-31 | Rachel Thexton Connects | Leading AI Voices | **no-image** | — |
| 2025-01-28 | Pique | Can’t abdicate this future | **no-image** | — |
| 2025-01-21 | CBC News | Meta / #Democrat hashtag | **no-image** | — |
| 2025-01-10 | Human Biography | Live With Curiosity | **no-image** | — |
| 2024-11-21 | Byte Club | Generative AI interview | yes | `press-2024-11-21-byte-club.jpg` |
| 2024-08-22 | Techcouver | AWS Community Day | yes | `press-2024-08-22-techcouver-context.jpg` |
| 2024-06-01 | FOLIO.YVR | Human & AI Compatibility | yes | `press-2024-06-01-folio-yvr-context.jpg` |
| 2024-05-06 | Teen2Life | CEO / Artist | **no-image** | — |
| 2024-02-12 | Jessica Grey | FPC workshop recap | yes | `press-2024-02-12-jessica-grey-context.jpg` |
| 2024-01-08 | AI-Volution | Are We Done Yet? | yes | `press-2024-01-08-ai-volution.jpg` |
| 2023-11-08 | Kurty D Show | Widen the Lens | **no-image** | — |
| 2023-09-08 | Olio by Marilyn | Interview | yes | `press-2023-09-08-olio-context.jpg` |
| 2023-09-07 | UNIQUEWAYS | Storyteller | **no-image** | — |

### The long trail (25 legacy rows)

Popular Science → Vancouver Sun / Kootenay Co-op Radio (2006), including TED Blog, TechCrunch, Next Web, YES!, Current TV, Lab with Leo ×2, etc. No dedicated graphics (text list — acceptable as Tier 3).

### CTA

EPK `/podcast-guesting-page-epk/` · Media Appearances `/2026/07/02/ai-media-appearances-podcast-guesting/`.

### Unique `data-media-key` files (16 unique; 20 attrs with reuse)

`press-2026-07-31-biv-ecosystem-context.jpg`, `press-2026-07-24-the-tyee-context.jpg`, `press-2026-06-15-biv-context.jpg`, `press-2026-02-05-vanmag-power50-context.jpg`, `press-2024-11-21-byte-club.jpg`, `press-2024-06-01-folio-yvr-context.jpg`, `press-2025-04-14-bc-studies-context.jpg`, `press-2026-05-20-storyhive.jpg`, `press-2026-02-09-tela-viva-context.jpg`, `press-2025-07-09-e-channelnews-context.jpg`, `press-2025-05-01-portfolio-yvr-context.jpg`, `press-2025-02-11-compass-horizons-context.jpg`, `press-2024-08-22-techcouver-context.jpg`, `press-2024-02-12-jessica-grey-context.jpg`, `press-2024-01-08-ai-volution.jpg`, `press-2023-09-08-olio-context.jpg`.

**Sections not present yet (plan):** Heard-on · In-print · The Wall (board is the stub).

---

## Verdict vs v1

| v1 disposition | v2 update |
|---|---|
| Power 50 → Add text row | **Done on payload** (featured board + recent-run row) |
| CBC holiday → Defer | **Still SKIP** until CBC Listen/Player URL (transcript/recap exist; clipping `pending:…`) |
| CBC Sandboxing → Leave on Media Appearances | **Upgrade to ADD** — cornerstone broadcast; YouTube episode set + at least one CBC.ca player URL now verified |
| Bossier → Defer (no public URL) | **Upgrade to ADD** — published as Medium/Top Boss (Bossier Brand) 2026-02-09 |
| Web Summit CBC clip → Candidate | **Still SKIP** — no KK-credited Web Summit CBC clip found this pass |
| Clippings JSON complete vs page | Confirmed; holiday stays outside JSON projection until URL logged |

**Embarrassment-by-omission (highest):** ~18-month CBC *Sandboxing AI* residency absent from `/publications/` while the page hero-lists “CBC”; photography print credits (Rolling Stone cover-adjacent, NY Press front cover, Olympics/LA Times, NatGeo via Pop!Tech) entirely missing; podcasts listed as naked text while the showpiece plan depends on square covers.

---

## A. CBC broadcast — ready / blocked

| Item | Evidence | Source URL | Disposition | Suggested media key | Graphic |
|---|---|---|---|---|---|
| **Sandboxing AI** series (Early Edition / Stephen Quinn, ~2024–2025) | `broadcast-interviews/2024-07-03-cbc-early-edition-sandboxing-ai-series.md`; appearances series row; kk-kb “tracked elsewhere” | Series home: series md. Launch note: https://kriskrug.co/2024/07/03/new-segment-on-cbc-radio-early-edition-ai-sandbox-with-kris-krug/ · YT set e.g. https://www.youtube.com/watch?v=rLWbdKg_q0k (music), `5aI3aYNpWXo` (Running Wolf), `0R7Re-EnPwA` (2025-03-09), etc. | **ADD** to Recent run as a **series lead row** (one card, not 10 episode rows). Optional: one Wall tile. | `press-2024-07-03-cbc-sandboxing-ai-series.jpg` | **NEED graphic:** video thumb from best YT episode (Tier 1), not a CBC player chrome screenshot |
| **AI companions / chatbots** (Early Edition lineage) | CBC player, dated May 16, 2024 | https://www.cbc.ca/player/play/video/9.4228529 | **ADD** to Recent run (or fold as first concrete episode under series). Stronger public URL than most sandboxing cuts. | `press-2024-05-16-cbc-ai-companions.jpg` | **NEED graphic:** video thumb / CBC still (Tier 1) |
| **Tech CEOs at inauguration** (Jan 21, 2025) | CBC player; same day/theme as Meta article already on page | https://www.cbc.ca/player/play/video/9.6619320 | **ADD** as video sibling **or** attach thumb to existing 2025-01-21 Meta row (prefer one feed row + video link, avoid double-count). | `press-2025-01-21-cbc-tech-ceos-inauguration.jpg` | **NEED graphic:** video thumb (Tier 1) — upgrades the current **no-image** CBC row |
| **AI holiday shopping** (~2025-11-28 / air ~week of Dec 1) | Clipping + full transcript/recap; URL `pending:cbc-listen-or-player-url-not-yet-located` | — | **SKIP** (reason: no aired public URL as of 2026-07-31; do not invent). Revisit when Listen/Player lands. | `press-2025-11-28-cbc-ai-holiday-shopping.jpg` (reserved) | — |
| **Should AI be open sourced?** (~2024-09-12) | Series md cites CBC player `9.6508206`; bot-blocks | CBC player ID only | **SKIP** for page until air credit/URL stable; keep under series body | — | — |
| **Hinton Nobel reaction** | README backfill: `cbc.ca/player/play/audio/9.6530156`; air date unconfirmed | audio/9.6530156 | **SKIP** until air date pinned | — | — |
| Web Summit CBC clip | v1 candidate; web pass 2026-08-01 | — | **SKIP** — no dedicated clip found | — | — |

---

## B. Heard-on shelf (podcasts)

Plan shelf: Rachel Thexton, Human Biography, UNIQUEWAYS, Kurty D, Teen2Life, AI-Volution.

All six **already appear** in Recent run; five are `no-image`. Disposition = **ADD to Heard-on** (new section) + **NEED graphic** (podcast cover). Keep Recent-run text rows or promote thumbs per design spec.

| Show | Apple collection ID | Episode ID | Episode / show URL | Artwork URL (iTunes 600) | Disposition | Suggested media key |
|---|---|---|---|---|---|---|
| Rachel Thexton Connects | `1663438596` | `1000687318552` | https://podcasts.apple.com/us/podcast/id1663438596?i=1000687318552 | https://is1-ssl.mzstatic.com/image/thumb/Podcasts221/v4/dc/ee/43/dcee4302-e5a0-64d3-c020-092aef77da85/mza_10802915206242894076.jpg/600x600bb.jpg | **ADD** Heard-on · **NEED graphic:** podcast cover | `press-2025-01-31-rachel-thexton-cover.jpg` |
| Human Biography | `1668006539` | `1000683484337` | https://podcasts.apple.com/us/podcast/id1668006539?i=1000683484337 | https://is1-ssl.mzstatic.com/image/thumb/Podcasts123/v4/8b/a9/f8/8ba9f888-29b0-2d97-9760-4c9655ac4b3b/mza_11071470160806735958.jpg/600x600bb.jpg | **ADD** Heard-on · **NEED graphic:** podcast cover | `press-2025-01-10-human-biography-cover.jpg` |
| UNIQUEWAYS | `1632267449` | `1000627111776` | https://podcasts.apple.com/us/podcast/113-kris-krüg-storyteller/id1632267449?i=1000627111776 | Show: `…/mza_14011119410296919288.jpg/600x600bb.jpg` · Episode art also available | **ADD** Heard-on · **NEED graphic:** podcast cover | `press-2023-09-07-uniqueways-cover.jpg` |
| Kurty D Show | `1575595225` | `1000634160006` | https://podcasts.apple.com/us/podcast/id1575595225?i=1000634160006 | https://is1-ssl.mzstatic.com/image/thumb/Podcasts115/v4/e3/ba/64/e3ba648b-2345-262d-f2be-64bac0ff2522/mza_6926379317233300605.jpg/600x600bb.jpg | **ADD** Heard-on · **NEED graphic:** podcast cover | `press-2023-11-08-kurty-d-cover.jpg` |
| Teen2Life Experience | `1666427209` | `1000654718269` | https://podcasts.apple.com/us/podcast/id1666427209?i=1000654718269 (also iHeart URL on page) | https://is1-ssl.mzstatic.com/image/thumb/Podcasts113/v4/4c/ad/03/4cad03bf-4b5b-f772-4602-8ca1f19dbcec/mza_13821386149566638488.jpeg/600x600bb.jpg | **ADD** Heard-on · **NEED graphic:** podcast cover · prefer Apple deep link alongside iHeart | `press-2024-05-06-teen2life-cover.jpg` |
| AI-Volution (OHEY) | *(no clean Apple show match this pass)* | — | https://www.youtube.com/watch?v=pss7CfiiBxg | YT thumb already on page: `press-2024-01-08-ai-volution.jpg` / oembed `hqdefault.jpg` | **ADD** Heard-on using **existing video thumb** as Tier 1 · SKIP Apple-cover hunt | `press-2024-01-08-ai-volution.jpg` (reuse) |

### Podcast / audio SKIP (not on plan shelf)

| Item | Why |
|---|---|
| Vancouver AI Pods ×3 (2023-09–12 Tub Time / AI Mindset / AEC) | Own-community podcast; not in plan’s six; optional later Heard-on overflow |
| Compass Horizons | Already in Recent run with page clip; video series not podcast shelf |
| On the Line / Lift / Kootenay / Lab with Leo | Long trail / legacy — leave text |

---

## C. In-print photography credits (15)

None on page. Visual leads = **KK-owned photos** (Flickr / kriskrug.co / TED-published credit), captioned with where they ran. Cover scans only where saved-HTML/Wayback already identified.

| Credit | Date / span | Rights-clean visual lead | Disposition | Suggested media key | Graphic |
|---|---|---|---|---|---|
| Rolling Stone — Raconteurs @ Commodore | 2008-04-19 | Flickr album `72157604689120729`; 2008 recap HTML in media-credits assets | **ADD** In-print (hero of section) | `press-2008-04-19-rolling-stone-raconteurs.jpg` | **NEED graphic:** KK photo from album (not RS masthead scrape) |
| New York Press front cover — R.E.M. / Stipe SXSW | ~2008-03-01 | Recap claim in `2009-01-02-kriskrug-photography-recap-2008.html`; no cover scan yet | **ADD** In-print | `press-2008-03-01-nypress-rem-cover.jpg` | **NEED graphic:** KK Stipe frame if in archive; **cover scan** TBD (Wayback/print) |
| Beijing Olympics / LA Times essays | ~2008-08-01 | Recap HTML; essay titles unconfirmed independently | **ADD** In-print (caption carefully) | `press-2008-08-beijing-olympics.jpg` | **NEED graphic:** KK photo from Games set |
| NY Fashion Week F/W 2009 | 2009-02-19 | Flickr `72157614644950989` | **ADD** In-print | `press-2009-02-19-nyfw.jpg` | **NEED graphic:** KK runway photo |
| COP15 / Granville Magazine | ~2009-12-14 | kriskrug.co Granville essays; Current TV clip already Long trail | **ADD** In-print | `press-2009-12-14-cop15-granville.jpg` | **NEED graphic:** KK Copenhagen photo |
| TEDxOilSpill lead photographer | 2010-06-14 | YES! Magazine essay already Long trail; YT CBC oil-spill photos | **ADD** In-print | `press-2010-06-14-tedxoilspill.jpg` | **NEED graphic:** KK Gulf / expedition photo |
| Eco Fashion Week inaugural | 2010-09-27 | Wayback `2010-eco-fashion-week-canadatalent.html` credit block | **ADD** In-print | `press-2010-09-27-eco-fashion-week.jpg` | **NEED graphic:** KK EFW photo |
| TEDxSummit Doha official photographer | ~2012-04-16 | TED Blog clipping already Long trail | **ADD** In-print | `press-2012-04-16-tedxsummit-doha.jpg` | **NEED graphic:** KK TEDxSummit photo |
| TEDActive 2013 TEDx Workshop | 2013-02-24 | TED Blog “All photos by Kris Krug”; saved `2013-02-25-ted-blog-tedx-workshop.html` | **ADD** In-print | `press-2013-02-24-tedactive-tedx-workshop.jpg` | **NEED graphic:** KK workshop photo (or TED-published still KK owns) |
| Dent:Space SF | 2016-09-21 | Flickr set; Popular Science Long trail | **ADD** In-print (secondary) | `press-2016-09-21-dent-space.jpg` | **NEED graphic:** KK Dent:Space photo |
| Dent 2019 Sun Valley | ~2019-03-30 | https://kriskrug.co/2019/03/30/dent-2019-photo-recap-gallery/ | **ADD** In-print (secondary) | `press-2019-03-30-dent-sun-valley.jpg` | **NEED graphic:** KK Dent photo |
| Pop!Tech official photographer (+ NatGeo Feb 2008 Zinhle portrait) | 2007–2010 | Recap HTML NatGeo note; Flickr PopTech albums | **ADD** In-print (span card; NatGeo line is the brag) | `press-2007-2010-poptech.jpg` | **NEED graphic:** KK Pop!Tech / NatGeo-published portrait if rights-clean to show |
| True North Media House / W2 Olympics hub | 2009–2010 | Tyee + CLT already Long trail | **ADD** In-print span (or SKIP if section budget tight — role was media-team-manager) | `press-2009-2010-true-north-media-house.jpg` | **NEED graphic:** KK / hub photo |
| Vancouver + BC Fashion Week DoP | 2008 | Recap HTML | **ADD** In-print span | `press-2008-fashion-weeks-dop.jpg` | **NEED graphic:** KK fashion-week photo |
| Future in Review (FiRe) photographer | 2015–2024 | Entry delivered; no single cover story | **ADD** In-print span (small) **or SKIP** if 12-slot budget — lower “tear sheet” punch than Rolling Stone / NY Press / Olympics | `press-2015-2024-fire.jpg` | **NEED graphic:** KK FiRe photo if kept |

**In-print priority order for first ship:** Rolling Stone → NY Press cover → Beijing/LA Times → TEDActive/TEDxSummit → COP15/Granville → NYFW → Pop!Tech/NatGeo → TEDxOilSpill → EFW → Dent ×2 → spans as overflow.

---

## D. The Wall — high-value missing / upgrade tiles

Target 8–12 curated best images (covers, video thumbs, clean clips). Board today is 4 weak/mixed crops.

| Candidate | Why | Disposition | Media key | Graphic |
|---|---|---|---|---|
| STORYHIVE On Location | Best existing Tier 1 art on page | **ADD** Wall (keep) | `press-2026-05-20-storyhive.jpg` | Have (video thumb) |
| Byte Club | Designed YT thumb | **ADD** Wall (keep) | `press-2024-11-21-byte-club.jpg` | Have |
| CBC Sandboxing / companions | Broadcast cornerstone | **ADD** Wall | `press-2024-05-16-cbc-ai-companions.jpg` or series key | **NEED** video thumb |
| Rolling Stone Raconteurs | Name recognition | **ADD** Wall | `press-2008-04-19-rolling-stone-raconteurs.jpg` | **NEED** KK photo |
| NY Press cover | Front-cover claim | **ADD** Wall if cover scan or hero frame exists | `press-2008-03-01-nypress-rem-cover.jpg` | **NEED** cover scan or KK photo |
| TED / TEDxSummit | Institutional | **ADD** Wall | `press-2012-04-15-ted-blog.jpg` or Doha photo key | **NEED** KK photo or Tier 2 TED Blog clip |
| Power 50 | Civic recognition 2026 | **ADD** Wall after **recapture** Tier 2 (or magazine cover if available) | `press-2026-02-05-vanmag-power50-context-v2.jpg` | **NEED** Tier 2 recrop / cover |
| BIV or Tyee (one only) | Current AI policy signal | **ADD** Wall after Tier 2 recapture | `press-2026-07-*-…-v2.jpg` | **NEED** Tier 2 clip (masthead+headline) |
| AI-Volution / Rachel cover | Podcast shelf crossover | Optional Wall | cover keys above | Tier 1 cover |
| BC Studies herring cover | Journal already has designed cover art in saved HTML (`cover_issue_183200_en_US.png`) | Optional Wall (Tier 1 journal cover — better than page crop) | `press-2025-04-14-bc-studies-cover.jpg` | **NEED** journal cover fetch (not full-page screenshot) |

**Wall SKIP:** Techcouver mention, Jessica Grey blog, Olio — fine for feed, not Wall.

---

## E. Other candidates (2025–26 + embarrassment)

| Item | Evidence | Disposition | Notes |
|---|---|---|---|
| **Top Boss / Bossier Brand** — “Kris Krug: Technology Game Changer” | Medium 2026-02-09; footer points to Bossier Brand; Q&A matches `bossier-magazine-interview-2026.md`. Issuu *Bossier Magazine Issue 19–Spring 2026* exists but KK page presence unverified this pass | **ADD** Recent run | URL: https://medium.com/@topbosstalk/kris-krug-technology-game-changer-172059b9b28c · key `press-2026-02-09-top-boss-bossier.jpg` · **NEED graphic:** Tier 2 clip of Medium (or print page if Issuu confirmed later) |
| Bossier print Issuu only | https://issuu.com/bossiermag/docs/bossier_magazine_issue_19-spring_2026 | **SKIP** until KK page/spread confirmed | Don’t double-count with Medium |
| Pique 2025-01-28 | On page, no-image | Stay Recent run · **NEED graphic** optional Tier 2 **or** Tier 3 text | key `press-2025-01-28-pique-context.jpg` if clipped |
| CBC Meta article | On page, no-image | Upgrade via inauguration **video thumb** (above) | — |
| Feature articles (Creative Mornings, Ethos Lab drafts) | `feature-articles/` = own/partner copy | **SKIP** | Not third-party press |
| Issuu Folio.YVR Issue 26 | press.md related media | **SKIP** | FOLIO/Portfolio profiles already on page |
| Own-site STORYHIVE recap | companion URL in clipping JSON | **SKIP** | Tear sheet links YouTube primary |
| Portfolio.YVR Web Summit name-check | v1 | **SKIP** | Passim mention |
| Unverified EPK “as seen in BBC/WIRED/Forbes…” | legacy-archive warning | **SKIP** | Embarrassment risk if claimed without URLs |
| Legacy digest unpromoted (PBS MediaShift, Midway CBC, etc.) | `legacy-archive.md` | **SKIP** for this wave | Date/URL incomplete |

---

## Graphics debt for items already on page

| Slot | Current | Action |
|---|---|---|
| Right-now ×3 | Bad Tier 2 screenshots | Recapture 1200×750 `-v2` keys (plan) |
| Board ×3 page crops | Noise at small size | Replace via Wall Tier 1 rules |
| Podcasts ×5 | no-image | iTunes covers (table B) |
| CBC Meta | no-image | Player video thumb |
| Pique | no-image | Tier 2 or text-only |

---

## Disposition count summary

Counts are **candidate decisions for the showpiece rebuild** (not “missing from clippings JSON”). An item can count in multiple sections if it is both a feed ADD and a Wall/Heard-on graphic.

| Section | ADD | SKIP | NEED graphic (subset of ADD / upgrades) |
|---|---:|---:|---:|
| **A. CBC / broadcast → Recent run** | 3 | 4 | 3 |
| **B. Heard-on shelf** | 6 | 3+ | 5 new covers (+1 reuse YT) |
| **C. In-print credits** | 14 | 1 (optional FiRe) | 14 |
| **D. The Wall** | 8–10 | ~3 feed-only | ~6 new / recapture |
| **E. Other 2025–26 / misc** | 1 (Top Boss/Bossier) | 7 | 1 |
| **Page inventory already covered** | — | — | Recapture wave for featured/board Tier 2 |

### Compact ADD vs SKIP (unique content decisions)

| Bucket | ADD | SKIP |
|---|---:|---:|
| New Recent-run content rows | **4** (Sandboxing series lead, CBC companions player, Top Boss/Bossier, optional inauguration video link) | **4** CBC blocked (holiday, open-source player, Hinton, Web Summit) |
| Heard-on (section create) | **6** | community pods / legacy audio |
| In-print (section create) | **14–15** | 0 hard skips (FiRe optional) |
| Wall curation | **8–10** tiles | weak feed mentions |
| Feature-articles / own posts / unverified EPK | 0 | **all** |

---

## Recommended build order (research → capture)

1. **Pull Tier 1 podcast covers** (five mzstatic URLs above) + confirm AI-Volution YT thumb reuse.
2. **CBC companions + inauguration** video thumbs; Sandboxing series lead using strongest YT still.
3. **In-print** KK photo selection from Flickr/recap (Rolling Stone, NYFW, TEDx, COP15 first).
4. **Top Boss Medium** Tier 2 clip for Recent run.
5. Recapture featured BIV/Tyee Tier 2 `-v2`.
6. Hold holiday shopping + Issuu print Bossier + Hinton until URLs harden.

---

## Reciprocal links (unchanged)

- EPK: `/podcast-guesting-page-epk/`
- Media Appearances: `/2026/07/02/ai-media-appearances-podcast-guesting/`

---

*Phase 1 only. Next plan todos: design spec + manifest, `capture_press_media.py`, gather art, payload rework.*
