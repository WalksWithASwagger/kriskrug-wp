# Alt text inventory, kriskrug.co (issue #4)

**Date of crawl:** 2026-08-02 (all HTTP was read-only GET; zero writes were made to the live site)
**Scope:** rendered `<img>` alt attributes in delivered public HTML, plus the public media library
**Machine-readable companion:** [`inventory.csv`](inventory.csv), 2,140 rows. **One row per unique (page URL, image src) pair, not per rendered occurrence.** See the counting rule below before you quote any number from it.
**Re-run it:** [`recount_live.py`](recount_live.py), read-only, re-fetches all 216 routes and re-derives every total in this file.
**Out of scope:** the broader WCAG 2.1 AA audit, which is issue #46 and owns `docs/current-state/A11Y-*`. This file is images only.

> ### Before you write a backfill script, read [the two fix surfaces](#read-this-first-there-are-two-fix-surfaces-and-a-library-only-backfill-silently-fixes-almost-nothing).
> A script that only writes media library `alt_text` reaches **80 of the 1,185 findings**. It no-ops on the other 1,105 and exits clean while doing it.

---

## Counting rule (read this before quoting a number)

An earlier version of this file mixed two different units and got three figures wrong. There are two, and they are not the same:

- **Occurrence.** Every `<img>` element in the delivered HTML. If a page renders the same file twice, that is two occurrences.
- **Row.** One unique `(page_url, image_src)` pair. `inventory.csv` stores rows. When a page renders the same `src` more than once, the crawler kept one row.

Across the 216 audited routes on 2026-08-02: **2,161 occurrences, 2,140 rows.** 21 occurrences collapse into rows they share, spread over six routes (`/publications/` 14, `/2026/05/23/you-cant-drink-data/` 3, and one each on `/work/`, `/photography/`, `/sponsor-deck/`, `/2024/08/22/web-summit-vancouver-2025-and-how-you-can-shape-it/`).

Almost all of that collapse lands on images that already have alt. Counted as violations: **1,185 rows, 1,186 occurrences.** So the 1,185 headline undercounts real screen-reader exposure by exactly one, and every other class in the table below is a row count.

Verified by re-fetching all 216 routes on 2026-08-02: `python3 recount_live.py` returned `occurrences_total: 2161`, `unique_page_src_total: 2140`, `csv_rows_for_these_routes: 2140`, `violation_occurrences: 1186`, `violation_unique: 1185`, `routes_fetched: 216`, `fetch_errors: []`. Every per-class row total below reproduced exactly.

---

## Headline

**1,185 rendered content images across the 216 audited routes have no usable alt text right now.**

| Class | Rows | Occurrences | What it is |
|---|---:|---:|---|
| `empty-alt-content-VIOLATION` | 1,060 | 1,061 | Content image rendered with `alt=""` |
| `filename-style-alt-VIOLATION` | 107 | 107 | `alt` is the filename or a Flickr photo ID, useless to a screen reader |
| `missing-alt-attr-VIOLATION` | 18 | 18 | No `alt` attribute at all, excluding the tracking pixel |
| **Subtotal needing alt** | **1,185** | **1,186** | Spread across **129 of the 216 routes** |
| `has-alt` | 736 | 756 | Real descriptive alt already in place |
| `decorative-tracking-pixel` | 216 | 216 | Meta noscript pixel, one per route, needs `alt=""` not a description |
| `decorative-empty-correct` | 3 | 3 | Correctly decorative, leave alone |
| **Total** | **2,140** | **2,161** | |

Media library side: **2,879 image attachments enumerated, 494 of them (17.2%) have `alt_text` set.** So 2,385 attachments carry no alt text in the library. Not all of those render publicly, which is why the rendered number above is the one that matters for #4.

Extrapolated to the whole site (see the sampling method below): roughly **1,760 empty content images sitewide**. That number is soft. The 2005 to 2007 photoblog years hold 665 of the 970 published posts and were sampled at only four posts per year, so that slice is the least certain part of the estimate.

---

## What is already clean

The high-traffic routes are in good shape, which matches the earlier narrowing work on this issue (issue #4 comment, 2026-06-18, and child issue #287, closed 2026-07-02).

`/`, `/about/`, `/blog/`, `/speaking/`, `/contact/`, `/work/`, `/photography/`, `/generative-ai-services/`, `/glossary/`, `/events/` returned **zero empty-alt content images, zero missing-alt, zero filename-style**.

The exact numbers, because an earlier version of this file got them tangled:

| | Occurrences | Rows in `inventory.csv` |
|---|---:|---:|
| Content images, all with descriptive alt | 96 | 94 |
| Meta noscript pixel, one per route | 10 | 10 |
| **Total** | **106** | **104** |

96 is the true count of rendered content images on those ten routes. The CSV holds 94 rows for them because two pages render one `src` twice: `/photography/` renders the Iggy Pop archive frame twice, `/work/` renders `kk-laSalle-both-hands-full-25-scaled.jpg` twice. Both collapse to one row each. Nothing on those ten routes is a violation either way.

Verification, 2026-08-02: `python3 recount_live.py --top-routes-only` returned `occurrences_total: 106`, `unique_page_src_total: 104`, `csv_rows_for_these_routes: 104`, `violation_occurrences: 0`, `by_classification_occurrences: {has-alt: 96, decorative-tracking-pixel: 10}`, and named both collapsed duplicates.

Earlier corroboration: `make public-image-audit DEFAULT_URLS=1 FORMAT=json` on the eight-route default set returned `missing_attr: 8, empty_alt: 3, filename_style: 0` on 87 images. The three empties were the two `/home/` images and the one on `/flickr-photographr-badge/`. `/home/` and `/flickr-photographr-badge/` are in that default set but are not in the clean ten above.

**So the violations are not on the front door. They are in page bodies and in the post archive.**

---

## Method

Everything here builds on the existing `scripts/public_image_audit.py`. The crawler in this pass imports that module's `RenderedImage` (line 46), `ImageParser` (line 96), `is_filename_style_alt` (line 154), and `row_dict` (line 340) rather than re-implementing the classification, and only adds the route-selection and media-library join.

**Reproducibility, stated plainly.** The one-shot wrapper that did the 216-route selection and the media-library join was never committed and is gone. That is a real gap and it is only half closed. What is committed is [`recount_live.py`](recount_live.py), which takes the route list straight out of the delivered `inventory.csv`, re-fetches all 216 routes over read-only GET, re-classifies every rendered `<img>` through the same `public_image_audit.py` helpers, and prints occurrence and row totals per class. Run on 2026-08-02 it reproduced the CSV row count and every per-class row total exactly (`routes_fetched: 216`, `fetch_errors: []`, `unique_page_src_total: 2140`). So the classification half of the headline is now independently checkable by anyone with the repo.

What `recount_live.py` does **not** rebuild: the original route selection (it reads the routes back out of the CSV instead of re-deriving them from the REST API) and the media-library join. Anyone wanting to re-derive the route list or refresh the `media_library_alt` column has to write that part again.

Routes crawled (216 unique after dedupe):

| Tier | Routes | How selected |
|---|---:|---|
| 1, top routes | 10 | Hand-picked highest-value: `/`, `/about/`, `/blog/`, `/speaking/`, `/contact/`, `/work/`, `/photography/`, `/generative-ai-services/`, `/glossary/`, `/events/` |
| 2, pages | 46 | Every published page, `GET /wp-json/wp/v2/pages?status=publish` (`X-WP-Total: 46`) |
| 3, recent posts | 55 | Every post published since 2025-01-01 (`X-WP-Total: 55`) |
| 4, 2024 block | 60 | The 60 most recent pre-2025 posts, i.e. most of the 75 posts from 2024 |
| 5, stratified archive | 59 | Four posts per year, 2003 to 2024, evenly spaced within each year |

Media library: walked `GET /wp-json/wp/v2/media?per_page=100&page=N` for all 30 pages. `X-WP-Total: 2960`, 2,916 items came back across the walk, 2,879 of them `media_type: image`.

Post and page totals from the same headers: **970 published posts, 46 published pages**.

Per-year post distribution, from `X-WP-Total` on year-bounded queries:

`2003:1  2004:30  2005:242  2006:304  2007:119  2008:12  2009:21  2010:19  2011:6  2012:1  2013:3  2015:7  2016:3  2017:1  2019:5  2020:1  2021:1  2023:64  2024:75` (2014, 2018, 2022 are empty; 2025 to 2026 is the 55-post recent block).

---

## READ THIS FIRST: there are two fix surfaces and a library-only backfill silently fixes almost nothing

> **A script that only writes `alt_text` on media library attachments will no-op on 1,105 of the 1,185 findings.** It will exit clean, report 1,185 attachments touched, and change 80 rendered images. If you ship one thing out of this document, ship this sentence.

Two surfaces, and they are not interchangeable:

**1. Featured images pull alt from the media library at render time.** One `alt_text` write on the attachment fixes every place that image renders. 76 post heroes in the crawl render `alt=""` purely because the attachment has no `alt_text`. Cheap, safe, high leverage. This is the surface a library script actually reaches.

**2. In-content image blocks bake the alt into `post_content`.** The core image block stores `alt=""` in the block markup, and that literal wins over the media library. Writing `alt_text` on the attachment does not change the rendered page. This surface needs a `post_content` edit per post.

Split of the 1,185 by `fix_surface`, straight from `inventory.csv`:

| `fix_surface` | Violation rows | Reachable by a media library write? |
|---|---:|---|
| `post-content-block` | 1,094 | **No** |
| `post-content-html-or-theme` | 11 | **No** |
| `media-library-alt_text` | 80 | Yes |
| **Total** | **1,185** | **80 of 1,185** |

### The proof, re-fetched live on 2026-08-02

12 rendered images carry a populated media library `alt_text` and still render `alt=""` on the page. That is 12 rows across 11 unique media IDs. (An earlier version of this file said seven. That was wrong and it understated: no cut of `inventory.csv` yields seven.) All 12 were re-confirmed by fetching the live page and the live REST record on 2026-08-02:

| Media ID | Library `alt_text` | Renders as | On | `fix_surface` |
|---:|---|---|---|---|
| 2596 | `On location in the studio of Gordon Payne on Hornby Island` | `alt=""` | `/art-island-perspectives-from-a-creative-community/` | `post-content-block` |
| 6481 | `Small File Media Festival - Our Networks 2024` | `alt=""` | `/2024/06/26/blog-ai-the-revolution-of-governance-and-cybersecurity-a-night-with-anthony-green/` | `media-library-alt_text` |
| 8211 | `Featured image for "Vancouver AI January 2025 Recap..."` | `alt=""` | `/2024/09/11/the-human-algorithm-enya-learning-keynote/` | `media-library-alt_text` |
| 8211 | same attachment, second route | `alt=""` | `/2024/12/02/autolume-post-photographic-cybernetic-portraiture/` | `media-library-alt_text` |
| 8549 | `Second Brain AI` | `alt=""` | `/2025/03/09/transcending-techs-darker-impulses/` | `post-content-block` |
| 8675 | `Featured image for "Is A Hotdog A Sandwich?..."` | `alt=""` | `/2025/03/20/is-a-hotdog-a-sandwich-vancouver-aidata-storytelling-hackathon-w-andrew-reid/` | `post-content-block` |
| 11264 | `Cover image for Make Culture, Not Content...` | `alt=""` | `/2026/02/03/name-the-bias/` | `post-content-block` |
| 11630 | `Responsible AI Professional Certification` | `alt=""` | `/2026/04/17/applied-ethical-ai-responsible-ai-professional-certification-rap/` | `post-content-block` |
| 6657 | `Young Kris Krug standing in front of the Form Media Technologies sign in 2000.` | `alt=""` | `/2026/05/24/ai-mindset-creative-paradigm/` | `post-content-block` |
| 2456 | `Gulf Island Pirate Regatta` | `alt=""` | `/2019/04/02/upcoming-galiano-island-events/` | `post-content-block` |
| 2464 | `Galiano Relief Retreat - Boathouse Studio` | `alt=""` | `/2019/04/10/small-art-printmaking-press-on-whaler-bay-galiano-island/` | `post-content-block` |
| 6048 | `Psychedelic Vancouver skyline with floating orbs and a large green face reflected in water.` | `alt=""` | `/2024/06/19/blog-rise-of-the-vancouver-technopunks-hosting-the-web-summit-on-our-terms/` | `post-content-block` |

**The cleanest demonstration is the two pages where the same attachment renders twice, one render per surface.** On `/2025/03/20/is-a-hotdog-a-sandwich-vancouver-aidata-storytelling-hackathon-w-andrew-reid/`, media 8675 renders once as `alt="Featured image for "“Is A Hotdog A Sandwich?”: Vancouver AI Data Storytelling Hackathon w/ Andrew Reid""` (the hero, reading the library) and once as `alt=""` (the in-content block, ignoring it). Same page, same file, same library record, two different rendered alts. Media 2456 does the identical thing on `/2019/04/02/upcoming-galiano-island-events/`. Any doubt about which surface wins is settled by those two pages.

The `fix_surface` column in `inventory.csv` marks every row as `media-library-alt_text`, `post-content-block`, `post-content-html-or-theme`, `tracking-pixel-snippet`, or `leave-as-is`. Read that column before shipping any batch.

---

## Encoding rule for proposed alt strings

The kriskrug.co DB layer is latin1. Per repo memory and the Ethọ́s mojibake fix tracked in issue #606, codepoints outside latin1 can get `?`-substituted on REST write.

What I could verify live on 2026-08-02:

- **Latin-1 characters round-trip as literals.** 50 media items carry a literal `ü` in `alt_text`. `curl -s https://kriskrug.co/photography/` returns `alt="Iggy Pop performing at South by Southwest, 2007, photographed by Kris Krüg"` as raw UTF-8, rendering correctly.
- **The combining-diacritic case is stored as NCRs.** Media 12350 holds `Block Party 2026 album cover, Eth&#7885;&#769;s Lab, ...` and `curl -s https://kriskrug.co/blog/` returns `alt="The Eth&#7885;&#769;s Lab Block Party Album"`. That is the only NCR-escaped alt string in the entire 2,879-image library.
- **UNVERIFIED:** 51 media items currently hold raw non-latin1 characters in `alt_text` (U+2014 em dash, U+201C/U+201D curly quotes) and they read back clean over REST. That does not match a strict "all non-latin1 gets substituted" model. I did not test a write, so I cannot say whether those were written through a different path or whether the substitution is narrower than the memory note describes. Do not treat raw em dashes in alt as proven safe.

**Working rule for this backfill:** ASCII is always safe. Write anything outside ASCII as a numeric character reference. `ü` becomes `&#252;`, `Ø` becomes `&#216;`, `Ü` becomes `&#220;`, `ọ́` becomes `&#7885;&#769;`. Nine rows in `inventory.csv` are flagged `needs_ncr=yes`; they are the Kris Krüg name strings and the MØTLEYKRÜG podcast covers.

`inventory.csv` also escapes em dashes in the quoted-evidence columns (`rendered_alt`, `media_library_alt`, `media_library_title`, `page_title`) as `&#8212;` so the file contains no literal em dash. None of the `proposed_alt` values contain one.

---

## Backfill order, by traffic value

| Batch | Rows | Surface | What | Status |
|---|---:|---|---|---|
| 0 | 216 | Snippet or plugin | Meta noscript tracking pixel, one per route, add `alt=""` | Ready, one-line fix, kills 216 findings |
| 1 | 34 | `post-content-block` | Seven site pages, all alt strings written below | Ready to apply |
| 2 | 5 | Mixed | `/home/` plus two media items reused as post heroes | Ready to apply, but see the `/home/` question |
| 3 | 76 | `media-library-alt_text` | Post hero featured images with empty alt, one library write each | Needs per-image review, cheapest per fix |
| 4 | 266 | `post-content-block` | In-body images on 23 posts published 2025 to 2026 | Needs per-image review |
| 5 | 698 | `post-content-block` | In-body images on 69 archive posts, mostly 2024 meetup recap galleries | Needs per-image review, biggest block |
| 6 | 106 | `post-content-block` | 14 photoblog gallery posts where alt is a Flickr photo ID | Needs per-image review |

Batch 0 first because it is one edit and clears 216 of the 1,401 total alt findings. Batch 1 and 2 next because they are already written. Batch 3 next because it is the highest fixes-per-effort ratio and it fixes hero images that appear on both the post and any card that renders the thumbnail.

Batches 4 to 6 are volume work. They cannot be automated honestly, because the correct alt depends on what is in the photo. What can be automated is the harness: pull each image, show it, capture a proposed string, stage it as a diff against `post_content`, and gate the apply on review. Do not let a script invent alt text from a filename.

---

## Batch 1, exact proposed alt strings

Every string below was written after fetching and looking at the image at 520px on 2026-08-02. They are apply-ready. Copy them verbatim, including the NCRs.

**What the strings actually cover, counted properly.** 36 media IDs. **35 distinct strings**, not 36: media 7539 and 7617 are the same Isaac Shamam testimonial card used on two different course pages and carry byte-identical alt. 43 rows in `inventory.csv` carry a `proposed_alt` value, but only **39 of those rows are violations that need a fix** (34 in batch 1, 5 in batch 2). The other 4 rows are `has-alt` / `fix_surface=leave-as-is`: they are places where media 12646 and 6835 already render with real alt (the post-card renders on `/` and `/blog/` fall back to the post title, and 12646 has a real in-body alt on its own post). Those 4 are carried in the CSV for context and are not part of the 1,185.

So the honest line is: **35 distinct strings, 36 attachments, closing 39 of the 1,185 findings.** Not "36 strings covering 43 instances".

### `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/` (page 7764)

| Media | Proposed alt |
|---:|---|
| 7766 | `Two YouTube video cards side by side: Carrie Cassel on transforming education for the age of AI, and Rajith on mastering Kubernetes at AWS Community Day` |
| 7765 | `A speaker in a blazer and sneakers presenting under magenta and cyan LED tubes in a warehouse gallery hung with collage paintings` |

### `/ai-upgrade-for-modern-media-leaders/` (page 7610)

| Media | Proposed alt |
|---:|---|
| 7615 | `Course card: AI for PR and Media Professionals, six weeks, live sessions Tuesdays, two one-on-one coaching sessions and a capstone project, with a bearded man in a grey checked jacket standing outdoors in autumn` |
| 7616 | `Logo wall headed Our clients and students have come from, showing The New York Times, CNN, NASA, National Geographic, Bloomberg, Reuters, Apple, Adobe, Accenture, Vice, Vox, CNBC, Hearst, Paramount, Salesforce, Berkeley and others` |
| 7612 | `February and March calendars with session dates circled, beside text reading Starts February 4th at 12pm ET, six-week program with weekly one-hour live sessions, two flexible one-on-one coaching sessions and a final capstone presentation` |
| 7617 | `Five-star testimonial from Isaac Shamam, Communications Strategist: Extremely valuable. Peter and Kris gave me customized guidance on building chatbots and streamlining my workflows for organizing my information faster and more efficiently` |
| 7619 | `Five-star testimonial from Denise Wolf: Hearing how communicators across PR, journalism and media applied the course to real-world challenges gave me a clear sense of what is possible with these tools` |
| 7618 | `Five-star testimonial from Tobias Stanley: As a PR consultant I was skeptical of AI's impact until Kris and Peter's course. The tailored coaching developed an AI integration plan customized for my workflows` |
| 7620 | `Five-star testimonial from Jennifer Wanderer: I really enjoyed collaborating with classmates in a virtual setting. It was inspiring to see the creativity and talent showcased in everyone's final projects` |

### `/ai-upgrade-for-creative-professionals/` (page 6770)

| Media | Proposed alt |
|---:|---|
| 7523 | `Instructor card: Peter Bittner, Founder and CEO of The Upgrade, multimedia journalist and UC Berkeley lecturer, beside Kris Kr&#252;g, Founder and CEO of Future Proof Creatives, artist, educator and consultant` |
| 7524 | `Logo wall headed Our students and clients have come from, showing UCLA, Apple, IBM, Berkeley, Adobe, NASA, Amazon, Columbia Business School, National Geographic, Accenture, UC Davis, Emily Carr, United Nations, RBC, Vancouver Film School, BCIT, Salesforce, Fleishman Hillard, Saatchi and Saatchi and News Product Alliance` |
| 7525 | `January and February calendars with session dates circled, beside text reading Starts January 14th at 6pm ET, six two-hour sessions split between lecture and hands-on activities on AI's role in online communications, marketing and narrative design` |
| 7529 | `Black and white portrait of Peter Bittner labelled Founder and CEO, The Upgrade, new media journalist and lecturer at UC Berkeley Graduate School of Journalism` |
| 7530 | `Portrait of Kris Kr&#252;g in a black beanie against a teal and orange backdrop, labelled Founder and CEO, Future Proof Creatives, artist, educator, consultant` |
| 7535 | `Five-star testimonial from Denise Wolf: It was beneficial to hear how people of different backgrounds and disciplines were able to adapt the course for their own work. It opened up a lot of possibilities for me` |
| 7536 | `Five-star testimonial from Jules Bernstein: Very encouraging cohort that made me feel not so alone in my ignorance of AI. I made a bot version of myself that I am excited to apply to my work every day` |
| 7539 | `Five-star testimonial from Isaac Shamam, Communications Strategist: Extremely valuable. Peter and Kris gave me customized guidance on building chatbots and streamlining my workflows for organizing my information faster and more efficiently` |
| 7540 | `Five-star testimonial from Daria Yaschenko, CEO of TerminalFX: The hands-on skills I've acquired from Kris have completely transformed my content creation process. His guidance on the ethical use of AI in visual storytelling was eye-opening` |
| 7541 | `Five-star testimonial from Andrew Sheridan, Digital Marketer: Peter did a great job. His course provided an excellent introduction to AI concepts and applications, packed with tangible takeaways` |
| 7542 | `Five-star testimonial from Jessica Liang: The course with Kris exceeded all my expectations. It was enlightening to learn not just about AI tools but how to apply them ethically and creatively in my work` |

### `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` (page 6755)

| Media | Proposed alt |
|---:|---|
| 6760 | `AI Upgrade Community Coaching card listing personalized coaching, collaborative coworking and a strong community, with Kris Kr&#252;g and Peter Bittner laughing, above The Upgrade and Future Proof Creatives logos` |
| 6761 | `Five-star testimonial from Isaac Shamam, Communications Strategist: Extremely valuable. Peter and Kris gave me customized guidance on building chatbots and streamlining my workflows` |
| 6762 | `Logo wall headed Our students and clients have come from, showing UCLA, Apple, Berkeley, NASA, Adobe, Amazon, National Geographic, Accenture, United Nations, RBC, Emily Carr, UC Davis, Columbia Business School, BCIT, Vancouver Film School, Fleishman Hillard, Saatchi and Saatchi and News Product Alliance` |

### `/reconciliation-indigenous-land-acknowledgement/` (page 3899)

| Media | Proposed alt |
|---:|---|
| 3901 | `Round white vinyl sticker with a hand-drawn LAND BACK logo, two arrows circling the words` |

### `/motleykrug-podcast/` (page 2828)

| Media | Proposed alt |
|---:|---|
| 2872 | `M&#216;TLEYKR&#220;G podcast cover: an AI-generated portrait of Kris Kr&#252;g with a braided mohawk and long beard standing in neon rain, the word KR&#220;G in green glitch type` |
| 3003 | `M&#216;TLEYKR&#220;G episode 8 cover, Learning Out Loud: The Osmotic Power of Community, with Kris Kr&#252;g holding a microphone under purple stage light` |
| 2873 | `M&#216;TLEYKR&#220;G episode 7 cover, Burning Man Art Projects, with an AI portrait of Kris Kr&#252;g in front of a burning wooden temple` |
| 2874 | `M&#216;TLEYKR&#220;G episode 5 cover, Artistic Evolution: AI's Creative Revolution, red and black wave-pattern collage behind an AI portrait of Kris Kr&#252;g` |
| 2877 | `M&#216;TLEYKR&#220;G episode 4 cover, Artistic Evolution: AI's Creative Revolution, multicolour graffiti-pattern backdrop behind an AI portrait of Kris Kr&#252;g` |
| 3010 | `M&#216;TLEYKR&#220;G episode cover, Audio Deep Fakes, AI Chatbots and New Web Development Tools, recorded on Hornby Island 27 July 2023` |

### `/art-island-perspectives-from-a-creative-community/` (page 2543)

| Media | Proposed alt |
|---:|---|
| 2592 | `Art Island episode 4 cover, Sea Changes: painter Michelle Nyberg in black-framed glasses beside one of her floral abstracts on an easel, Hornby Arts logo below` |
| 2596 | `Painter Gordon Payne at his easel in his Hornby Island studio while a camera operator frames the shot on a gimbal` |
| 2597 | `A photographer crouched behind a tripod on a wide empty tidal flat, mountains and low cloud on the horizon` |
| 2595 | `Behind the scenes on Art Island: an interview subject seated beside a woodstove under a round LED softbox while Alina Milek operates the camera` |

---

## Batch 2, `/home/` and two reused images

| Media | Proposed alt | Where it renders |
|---:|---|---|
| 12646 | `Attendees packed into a courtyard at Vancouver AI Meetup 30, shot from a balcony above the crowd` | `/home/`, and as the hero of `/2026/07/31/ai-lands-inside-every-profession/` |
| 6835 | `Vancouver AI meetup crowd standing shoulder to shoulder under magenta light, watching something off frame` | `/home/`, the hero of `/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/`, and in the body of `/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/` |

Both attachments currently have empty `alt_text`. Two media library writes fix four of the five rendered instances. The fifth, the in-body use on the August 2024 recap, is a `post-content-block` and needs a content edit.

This supersedes the medium-confidence guess in the 2026-07-02 comment on this issue (`Vancouver AI community meetup crowd gathered for a local AI ecosystem event`). That guess was written without looking at the file. The image is a crowd under magenta light watching a stage, so the string above is closer.

**Question for KK:** `/home/` returns HTTP 200 but is not linked from `/`. It looks like a legacy duplicate of the homepage. If it should be redirected or unpublished, then the `/home/` half of this batch is wasted work and the redirect is the better fix.

---

## Alt strings that exist but are weak

These are classified `has-alt` in the CSV because they are not empty, so they are not in the 1,185. Flagging them anyway.

- **`Kris Krug home`, 216 occurrences.** The header wordmark, once per route. It sits inside the link to `/`, so it is the accessible name for that link. Defensible as is. The alternative, `alt=""` plus an `aria-label` on the link, is a theme change and belongs in Track B, not here. Child issue #287 already landed on "leave it decorative if the link has a good name". It currently is not decorative, it has a name. Either shape passes. Low priority.
- **Event card thumbnails on `/events/` that are only a meetup number:** `Vancouver AI Meetup #4`, `#11`, `#14`, `#17 (#WebSummit special edition)`, `#18`, `#28`, `#30`, `#31 (photo: Michelle Diamond / Diamond's Edge Photography)`. Eight cards. The alt tells you which event but nothing about the photo. If these get rewritten, use the pattern from [`content/drafts/2026-07-26-speaking-stages/VISUALS.md`](../2026-07-26-speaking-stages/VISUALS.md) lines 37 to 42: `Kris Krug [action] at [event], [context].`, with photographer credit in the caption rather than stuffed into alt. Note that #31 currently violates that rule by carrying the credit inside the alt.
- **`Archive photograph from Kris Krug photography practice`**, on `/` and `/about/`. Generic. Says nothing about the photo.
- **Old photoblog one-word alts** carried over from Flickr: `KGOODPHOTO`, `path`, `Pickup`, `Smile!`, `thailand boat`, `photo by penmachine`. Real strings, not filenames, so the classifier passes them, but they are near-useless. They sit inside batch 5 and 6 territory anyway.

---

## Individually notable findings

- **Testimonial cards are images of text.** Fourteen of the batch 1 images are five-star review cards where the entire quote is baked into a PNG. Alt is the only path to that content today. That is also a WCAG 1.4.5 "images of text" question, which belongs to issue #46, not here. The alt strings above carry the full quote and the attributed name so the content is at least reachable.
- **Two non-pixel images with no `alt` attribute at all** in the recent and 2024 sets:
  - `/2024/12/02/autolume-post-photographic-cybernetic-portraiture/`, hotlinked from `lh7-rt.googleusercontent.com/docsz/AD_4nXf...`, a Google Docs paste artifact
  - `/2024/04/19/not-all-white-guys-unpacking-the-wealth-tax-debate-in-canada/`, hotlinked from `cdn.midjourney.com/16e020d2-b069-4613-827a-f13233d3a392/0_3.webp`

  Both are external hotlinks, not media library items, so they also break the no-hotlinks rule in `VISUALS.md`. Fixing alt on these should probably be folded into ingesting them into the media library.
- **16 more missing-attr images** in the stratified archive sample, concentrated on `/2017/01/20/sharon-anderson-morris/` and three 2004 posts that still point at `kriskrug.co/images/` and `kriskrug.blogspot.com` paths.
- **The 107 filename-style alts cluster on 14 photoblog gallery posts.** The alt is the Flickr photo ID, for example `alt="3154868160_6d2974fa86_o"` next to `src=".../3154868160_6d2974fa86_o1-e1429044947708.jpg"`. Mechanically identifiable, but each one still needs a human to look at the photo.
- **The single filename-style alt found in the 2024 block** is on `/2024/04/19/not-all-white-guys-unpacking-the-wealth-tax-debate-in-canada/`: `alt="kriskrug_tech_tycoon_playing_Monopoly_with_actual_buildings_w_73b7662d-3859-42e7-b994-e5a72a601040_1.png"`, a raw Midjourney filename.

---

## Acceptance criteria on issue #4: 0 of 7 met

Every criterion on #4 is about the state of images **on the live site**. This pass made zero writes. Nothing here has been applied. So the count is 0 of 7, and it stays 0 of 7 until a batch actually runs.

An earlier version of this file marked three of them `[x]` because a proposed string existed in this markdown file. That was wrong. A string in a draft is not alt text on a website. Re-checked live on 2026-08-02, `GET /wp-json/wp/v2/media/<id>?_fields=id,alt_text`: media 7529, 7530, 7523, 2592, 2872, 12646, 6835, 7615 and 7616 all return `alt_text=""`. Not one of them has moved.

- [ ] All images have descriptive alt text. **No.** 1,185 findings, 0 fixed. This pass inventories them and drafts 35 distinct strings for 36 attachments, which would close 39 of them once applied.
- [ ] Alt text keyword-optimized where appropriate. **No.** The drafted strings name the people, courses, brands and events, but none of them are on the site. Live `alt_text` on 7615 and 7616 is `""`.
- [ ] Profile and headshots labeled with context. **No.** Strings are drafted for 7529 (Peter Bittner), 7530 (Kris Krüg), 7523 (both) and 2592 (Michelle Nyberg). All four attachments return `alt_text=""` live right now.
- [ ] Project images describe content and purpose. **No.** Strings are drafted for the course cards, logo walls, testimonial cards and podcast covers. Media 2872 (the MØTLEYKRÜG cover) returns `alt_text=""` live.
- [ ] Decorative images have empty `alt=""`. **No.** 3 are already correctly decorative, which predates this pass. The 216 Meta pixels still have no `alt` attribute at all. Batch 0 is the fix and it has not run.
- [ ] Tested with screen readers. **No.** No screen reader was run in this pass.
- [ ] WCAG 2.1 AA compliance verified. **No.** That is issue #46.

### What this PR does close

It is not zero work, it is just not site state. What is genuinely done:

1. **The scope question on #4 is answered with a number.** The issue has sat open since January partly because "all images" was never bounded. It is 1,185 findings across 129 of 216 audited routes, with a per-row CSV. The 2026-06-17 and 2026-06-18 comments on #4 could only say "the recent lane is clean, the archive is unknown". The archive is no longer unknown.
2. **The fix path is now known to be two paths, not one.** See the section above. That finding would have burned a whole backfill run.
3. **35 strings are written and apply-ready**, which converts batch 1 and 2 from "look at every image" into "paste and verify".
4. **The work is ordered into six batches with effort and blast radius per batch**, so KK can approve a slice instead of the whole thing.
5. **The headline is now re-runnable** via `recount_live.py`.

None of that is an acceptance criterion on #4. #4 closes when images on kriskrug.co have alt text.

## What needs KK

1. **`/home/`:** redirect, unpublish, or keep and fix? It is a live 200 that nothing links to.
2. **Approval to apply batch 0 and batch 1.** Batch 1 is 34 in-content block edits across seven pages, which means `post_content` writes on live pages, not media library writes. Those need snapshots and slug and ID checks per the incident rules in `docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`.
3. **Volume call on batches 4 to 6.** 1,070 images across 106 posts, mostly meetup recap galleries from 2023 and 2024. Options: do them all, do only posts that still get traffic, or accept the archive as-is and gate alt discipline on new posts only. This is a scope decision, not an engineering one.
4. **The em dash and NCR question.** 51 media items currently hold raw em dashes and curly quotes in `alt_text` and read back clean. Either the latin1 substitution model is narrower than the memory note says, or those were written through a path other than a plain REST write. Worth one deliberate test write on a throwaway attachment before batch 3 runs, since batch 3 is media library writes.

---

## Files

- `content/drafts/alt-text-backfill-2026-08-02/inventory.md`, this file
- `content/drafts/alt-text-backfill-2026-08-02/inventory.csv`, 2,140 rows, one per unique `(page_url, image_src)` pair. Columns: `batch, page_url, page_id, page_slug, page_title, tier, media_id, image_file, image_src, rendered_alt, alt_state, classification, fix_surface, media_library_alt, media_library_title, proposed_alt, needs_ncr, confidence, notes`
- `content/drafts/alt-text-backfill-2026-08-02/recount_live.py`, read-only re-verification of every total in this file. GET only, never writes to the site. `python3 recount_live.py` for all 216 routes, `--top-routes-only` for the fast ten-route check, `--json out.json` for machine-readable totals.

Rows with `confidence` starting `TODO` are the ones still needing a human to look at the image. Rows with `confidence` starting `high` are apply-ready.
