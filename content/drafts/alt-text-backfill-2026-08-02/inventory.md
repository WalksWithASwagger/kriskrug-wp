# Alt text inventory, kriskrug.co (issue #4)

**Date of crawl:** 2026-08-02 (all HTTP was read-only GET; zero writes were made to the live site)
**Scope:** rendered `<img>` alt attributes in delivered public HTML, plus the public media library
**Machine-readable companion:** [`inventory.csv`](inventory.csv), 2,140 rows, one row per rendered image occurrence
**Out of scope:** the broader WCAG 2.1 AA audit, which is issue #46 and owns `docs/current-state/A11Y-*`. This file is images only.

---

## Headline

**1,185 rendered content images across the 216 audited routes have no usable alt text right now.**

| Class | Count | What it is |
|---|---:|---|
| `empty-alt-content-VIOLATION` | 1,060 | Content image rendered with `alt=""` |
| `filename-style-alt-VIOLATION` | 107 | `alt` is the filename or a Flickr photo ID, useless to a screen reader |
| `missing-alt-attr-VIOLATION` | 18 | No `alt` attribute at all, excluding the tracking pixel |
| **Subtotal needing alt** | **1,185** | Spread across **129 of the 216 routes** |
| `has-alt` | 736 | Real descriptive alt already in place |
| `decorative-tracking-pixel` | 216 | Meta noscript pixel, one per route, needs `alt=""` not a description |
| `decorative-empty-correct` | 3 | Correctly decorative, leave alone |
| **Total rendered images observed** | **2,140** | |

Media library side: **2,879 image attachments enumerated, 494 of them (17.2%) have `alt_text` set.** So 2,385 attachments carry no alt text in the library. Not all of those render publicly, which is why the rendered number above is the one that matters for #4.

Extrapolated to the whole site (see the sampling method below): roughly **1,760 empty content images sitewide**. That number is soft. The 2005 to 2007 photoblog years hold 665 of the 970 published posts and were sampled at only four posts per year, so that slice is the least certain part of the estimate.

---

## What is already clean

The high-traffic routes are in good shape, which matches the earlier narrowing work on this issue (issue #4 comment, 2026-06-18, and child issue #287, closed 2026-07-02).

`/`, `/about/`, `/blog/`, `/speaking/`, `/contact/`, `/work/`, `/photography/`, `/generative-ai-services/`, `/glossary/`, `/events/` returned **zero empty-alt content images**. 96 images across those ten routes, all with descriptive alt, plus one Meta pixel each.

Verification: `make public-image-audit DEFAULT_URLS=1 FORMAT=json` on the eight-route default set returned `missing_attr: 8, empty_alt: 3, filename_style: 0` on 87 images. The three empties were the two `/home/` images and the one on `/flickr-photographr-badge/`. The full 216-route crawl reproduces that and then finds the rest.

**So the violations are not on the front door. They are in page bodies and in the post archive.**

---

## Method

Everything here builds on the existing `scripts/public_image_audit.py`. The crawler in this pass imports that module's `ImageParser`, `RenderedImage`, `is_filename_style_alt`, and `row_dict` rather than re-implementing the classification, and only adds the route-selection and media-library join.

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

## The two fix surfaces, and why this matters before anyone writes

This is the single most decision-relevant thing in the audit.

**Featured images pull alt from the media library at render time.** One `alt_text` write on the attachment fixes every place that image renders. 76 posts in the crawl render their hero featured image with `alt=""` purely because the attachment has no `alt_text`. Cheap, safe, high leverage.

**In-content image blocks bake the alt into `post_content`.** The core image block stores `alt=""` in the block markup, and that literal wins over the media library. Writing `alt_text` on the attachment will not change the rendered page.

Proof, from the crawl: seven images render with `alt=""` on a page even though their media library `alt_text` is populated. Examples:

| Media ID | Library `alt_text` | Renders as | On |
|---:|---|---|---|
| 2596 | `On location in the studio of Gordon Payne on Hornby Island` | `alt=""` | `/art-island-perspectives-from-a-creative-community/` |
| 6657 | `Young Kris Krug standing in front of the Form Media Technologies sign in 2000.` | `alt=""` | `/2026/05/24/ai-mindset-creative-paradigm/` |
| 11630 | `Responsible AI Professional Certification` | `alt=""` | `/2026/04/17/applied-ethical-ai-responsible-ai-professional-certification-rap/` |
| 8549 | `Second Brain AI` | `alt=""` | `/2025/03/09/transcending-techs-darker-impulses/` |

The `fix_surface` column in `inventory.csv` marks every row as `media-library-alt_text`, `post-content-block`, `post-content-html-or-theme`, `tracking-pixel-snippet`, or `leave-as-is`. Anyone shipping a batch should read that column first. A media-library-only script will silently no-op on 1,000+ of these.

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

## Acceptance criteria on issue #4, honestly marked

- [ ] All images have descriptive alt text. **No.** 1,185 rendered images still need it. This pass inventories them and writes 36 exact strings covering 43 rendered instances.
- [x] Alt text keyword-optimized where appropriate. Batch 1 and 2 strings name the people, the courses, the brands, and the events.
- [x] Profile and headshots labeled with context. Media 7529 (Peter Bittner), 7530 (Kris Krüg), 7523 (both), and 2592 (Michelle Nyberg) all name the person and their role.
- [x] Project images describe content and purpose. Course cards, logo walls, testimonial cards and podcast covers all carry their actual content.
- [ ] Decorative images have empty `alt=""`. **Partly.** 3 are correctly decorative. The 216 Meta pixels still have no `alt` attribute at all and should get `alt=""`, which is batch 0.
- [ ] Tested with screen readers. **Not done.** No screen reader was run in this pass.
- [ ] WCAG 2.1 AA compliance verified. **Not done here.** That is issue #46.

## What needs KK

1. **`/home/`:** redirect, unpublish, or keep and fix? It is a live 200 that nothing links to.
2. **Approval to apply batch 0 and batch 1.** Batch 1 is 34 in-content block edits across seven pages, which means `post_content` writes on live pages, not media library writes. Those need snapshots and slug and ID checks per the incident rules in `docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`.
3. **Volume call on batches 4 to 6.** 1,070 images across 106 posts, mostly meetup recap galleries from 2023 and 2024. Options: do them all, do only posts that still get traffic, or accept the archive as-is and gate alt discipline on new posts only. This is a scope decision, not an engineering one.
4. **The em dash and NCR question.** 51 media items currently hold raw em dashes and curly quotes in `alt_text` and read back clean. Either the latin1 substitution model is narrower than the memory note says, or those were written through a path other than a plain REST write. Worth one deliberate test write on a throwaway attachment before batch 3 runs, since batch 3 is media library writes.

---

## Files

- `content/drafts/alt-text-backfill-2026-08-02/inventory.md`, this file
- `content/drafts/alt-text-backfill-2026-08-02/inventory.csv`, 2,140 rows, columns: `batch, page_url, page_id, page_slug, page_title, tier, media_id, image_file, image_src, rendered_alt, alt_state, classification, fix_surface, media_library_alt, media_library_title, proposed_alt, needs_ncr, confidence, notes`

Rows with `confidence` starting `TODO` are the ones still needing a human to look at the image. Rows with `confidence` starting `high` are apply-ready.
