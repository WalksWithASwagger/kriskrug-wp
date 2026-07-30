# Content Audit — kriskrug.co

**Audit date:** 2026-05-14
**Scope:** All 34 published pages + the **101 posts from 2024-01-01 onward** (per the chosen scope). The 840 older posts in the archive are out of scope for this pass.
**Method:** Public REST API + HTML inspection. No admin or SSH used.
**Companion docs:** [SEO_AUDIT.md](SEO_AUDIT.md), [FIX_QUEUE.md](FIX_QUEUE.md).

---

## Executive summary

The content layer has three big problems and a lot of upside.

**Problems:**
1. **Categorization is broken.** 98 of 101 recent posts are filed under a single "Misc" category (slug `uncategorized`, renamed). Crawlers, AI assistants, and your own internal navigation can't distinguish a Vancouver AI meetup recap from a manifesto from a journalism piece.
2. **Pages are flat.** All 34 pages are top-level (no parent/child). Marketing offers, multilingual welcomes, archive pages, and core navigation pages all live at the same hierarchy level.
3. **Multilingual welcome pages don't form a coherent set.** 7 language variants exist but they're not hreflang'd together and there's no visible language switcher pattern.

**Upside:**
- **Writing is good.** Posts have voice, clear theses, and quotable lines.
- **Cadence is healthy.** 101 posts in ~28 months = ~3.6/month average; ramping in 2024 (75 posts) and 2025 (20 posts so far in 2026).
- **Topics cluster cleanly** around Vancouver AI scene, AI for creatives, AI philosophy, and personal projects — clean clusters mean clean topical authority once categorization is fixed.
- **Strong personal brand pages** (About, AI Upgrade offers, Reconciliation page) — they read like KK, which is rare and valuable.

---

## 1. Pages — per-page review

All 34 published pages, audited at the URL/REST level. Status column uses 🟢 keep / 🟡 needs work / 🔴 broken-or-redundant.

### Core navigation pages

| Page | Slug | Status | Notes |
|---|---|---|---|
| Home (2315) | `/home/` | 🟡 | Title rendered as "Recent Posts & Updates:" — that's a section heading, not a page title. WordPress treats this as the static homepage; rendered title should be the brand or value prop. |
| About (1208) | `/about/` | 🟢 | 1935 words, strong KK voice. Title is colorful (109 chars — too long for SERP); meta description is excellent. **Reflects multiple H1s** (theme issue). |
| Contact (2418) | `/contact/` | 🟢 | 527 words. Adequate; could be richer (response time SLA, what NOT to email about, link to office hours). |
| Blog (2316) | `/blog/` | 🟡 | Blog index page. **No H1**, no twitter:card, no canonical — theme template gap. |
| News (2389) | `/news/` | 🟡 | Purpose unclear — is this different from Blog? Look at what gets posted here vs Blog. Possibly merge. |

### Marketing / offer pages (high commercial value)

| Page | Slug | Status | Notes |
|---|---|---|---|
| AI Upgrade for Modern Media Leaders (7610) | `/ai-upgrade-for-modern-media-leaders/` | 🟢 | 1758 words. Strong value prop. **Should have Service + FAQPage schema**. |
| AI Upgrade for Creative Professionals (6770) | `/ai-upgrade-for-creative-professionals/` | 🟢 | 1306 words. Same recommendation. |
| AI Upgrade Community Coaching (6755) | `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` | 🟡 | Co-branded with Peter Bittner; slug is unwieldy. Confirm co-marketing status. |
| Cinematic Podcasts (7764) | `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/` | 🟡 | Slug is 73 chars — unreadable. Confirm it's actively driving inquiries; if so, consider shortening to `/cinematic-podcasts/` with a 301 from current. |
| Generative AI Creative Services (2666) | `/generative-ai-services/` | 🟢 | 1686 words. Solid. |
| Workshop (2603) | `/generative-ai-workshop-for-artists-creatives/` | 🟡 | Confirm currency — is this offer still live? Older content. |
| Speaking (1887) | `/speaking/` | 🟡 | Thin — 520 words. Add: recent talks list, topics, speaker reel, booking CTA, Event schema. |
| Podcast Guesting / EPK (3609) | `/podcast-guesting-page-epk/` | 🟢 | Good niche page. Should have downloadable EPK link + Person schema. |
| Sponsor: Cyberpunk Chronicles (3969) | `/sponsor-cyberpunk-chronicles-newsletter/` | 🟢 | Sponsorship pitch page; ensure it has FAQPage schema and clear CTA. |

### Authority / portfolio pages

| Page | Slug | Status | Notes |
|---|---|---|---|
| Recent Projects (2672) | `/recent-projects-include/` | 🟡 | Slug is awkward ("/recent-projects-include/"). Rename to `/projects/` or `/portfolio/` with 301. 872 words. |
| Publications (1895) | `/publications/` | 🟡 | 613 words. Confirm currency, add structured list with publication dates. |
| Testimonials (2409) | `/testimonials/` | 🟢 | 817 words. Add `ItemList` schema with `Review` items for rich snippets. |
| Events (2250) | `/events/` | 🟡 | 1684 words. Currency check: events change fast. Add Event schema. |
| Art Island (2543) | `/art-island-perspectives-from-a-creative-community/` | 🟡 | Specific essay-page. Confirm purpose — is this an evergreen page or a one-off? |
| MØTLEYKRÜG Podcast (2828) | `/motleykrug-podcast/` | 🟢 | 1259 words. Should have `PodcastSeries` schema + each episode as `PodcastEpisode`. |
| The KK Worldview (3948) | `/the-kk-worldview/` | 🟢 | Manifesto-style; great for entity reinforcement. Likely a top citation target for LLMs once schema is added. |
| Reconciliation & Indigenous Land Ack (3899) | `/reconciliation-indigenous-land-acknowledgement/` | 🟢 | 488 words. Important; could be slightly longer with specifics on KK's commitments. |
| Privacy Policy (2985) | `/privacy-policy/` | 🟢 | "KK Pledge to Privacy" — nice rebranding. |
| Product Review Policy (3974) | `/product-review-policy-instructions/` | 🟢 | Useful for press / PR. |

### Multilingual welcome pages — 7 variants

| Page | Slug | Word count |
|---|---|---|
| Japanese (3595) | `/japanese-introduction-page-kaykaysan/` | 551 |
| Chinese (3598) | `/chinese-introduction-kang-jia/` | — |
| Farsi (3601) | `/farsi-introduction-khalil-khalifa/` | — |
| Russian (3600) | `/russian-introduction-kristofor-kruglov/` | — |
| Hindi (3606) | `/hindi-introduction-krishna-vishwanathapriyadhanvanshi/` | — |
| Urdu (3696) | `/urdu-language-introduction-kris-krug/` | — |
| Swahili (3603 + duplicate 3623) | `/swahili-introduction-…/` + `/karibu-kwenye-…/` | — |

**Status: 🔴 unfinished as a set.** Findings:
- **No hreflang** linking the variants together. Google can't connect them; LLMs can't route to them based on user language.
- **Two Swahili pages** with overlapping content (IDs 3603 and 3623). One is redundant — pick canonical, 301 the other.
- **Slugs use creative pseudonyms** (Kintu Krowfeather, Krishna Vishwanathapriyadhanvanshi, etc.) — fun, but bad for discoverability. Search-language users won't search for "Krishna Vishwanathapriyadhanvanshi"; they'll search "Kris Krug हिन्दी" or "Kris Krug Hindi".
- **No language switcher** visible on the main site.

Three options:
1. **Make them work** — install Polylang or WPML, build a proper hreflang network, add a language switcher in the header, canonical to one master "international" entry page. Real work; do it if a multilingual audience matters.
2. **Position as art** — these are clearly playful (Kintu Krowfeather is a character). Keep them, mark them as Easter eggs in the page itself, but `noindex` them. Removes them from SEO confusion but preserves the work.
3. **Remove from sitemap** — same as (2) but lighter touch.

🔵 Recommend (1) if KK's audience genuinely includes non-English speakers; (2) if they're personal/creative pieces.

### Likely-stale or low-value pages

| Page | Slug | Notes |
|---|---|---|
| Empowering Events & Organizations (3930) | `/empowering-events-organizations-for-the-ai-age/` | **Empty rendered title** in REST API. Either fix or `noindex`. |
| Subscribe (2808) | `/subscribe/` | **Empty rendered title** in REST API. Confirm purpose. |
| Karibu kwenye… Swahili Welcome (3623) | (Swahili duplicate) | See above. |
| Russian/Hindi/Chinese/etc. intros | (multilingual) | See above. |

---

## 2. Posts — 2024-onwards inventory

### 2.1 By year

| Year | Posts | Note |
|---|---|---|
| 2026 (Jan-May) | 6 | On pace for ~14/year. |
| 2025 | 20 | Down from 2024. |
| 2024 | 75 | **Most prolific year.** |
| 2023 | 64 | Strong. |
| 2022 | — | Gap visible in older posts. |
| 2021 | 1 | Effectively dormant. |
| 2020 | 1 | — |
| 2019 | 5 | — |
| pre-2018 | ~28 | Old archive. |

**Cadence pattern:** 2023-2024 was the most active period (139 posts in 24 months); 2025 slowed sharply (20 in 12 months); 2026 has 6 in 4 months (back to ~1.5/month). Worth understanding what changed in 2025 — was it BC + AI organizational work eating writing time?

### 2.2 Categorization — **critical issue**

Of 101 posts since 2024:
- **98 are filed only in "Misc"** (the renamed `uncategorized` category)
- **3 have no category at all** (also reads as Misc by default)

Categories that exist: only `Misc` (867 posts total) and `Oil Spill` (1 post). That's it.

**This means:** when Google or an LLM tries to understand topical authority on kriskrug.co, every post looks topically unstructured. There's no signal saying "this site has authority on Vancouver AI community, on AI ethics, on creative AI workflows."

**Proposed category structure** (based on inspecting the recent 101 titles):

| Category | Slug | Approx count in recent 101 | Topical authority value |
|---|---|---|---|
| Vancouver AI Ecosystem | `vancouver-ai` | ~25 | Meetup recaps, BC + AI association, community pieces |
| AI for Creatives | `ai-creatives` | ~15 | Workflow, tools, working with artists |
| AI for Journalism & Media | `ai-journalism` | ~10 | What journalists need to know, training pieces |
| AI Ethics & Philosophy | `ai-ethics` | ~12 | Bias, manifestos, "AI Ate the Future" |
| Generative AI Tools | `ai-tools` | ~10 | Hands-on tool reviews, comparisons |
| Conversations & Interviews | `conversations` | ~15 | Podcast recaps, guest spots, human biography |
| Events & Reports | `events` | ~10 | Web Summit, AI Summit, hackathons |
| Field Notes | `field-notes` | ~10 | Personal observations, "Spa at the End of Time" |
| Indigenous & Reconciliation in Tech | `indigenous-tech` | ~5 | Indigenomics.ai, Indigenous AI work |

Most posts will fit ≥1 category, sometimes 2. Don't go past 9 categories — fewer is better.

### 2.3 Tags

**124 unique tags** used across the 101 recent posts — good. Tagging is happening. Without admin access I can't see tag names, but the spread is reasonable.

🔵 Once category structure is fixed, **audit the 124 tags** in wp-admin: consolidate near-duplicates, merge low-volume tags (<3 uses) into categories or delete.

### 2.4 Topic clusters spotted in recent titles

Without keyword research data, here are themes that show up repeatedly. These are KK's **emerging topical authorities** and the natural targets for AI/SEO consolidation:

| Cluster | Sample titles | Why it matters |
|---|---|---|
| **"Vancouver AI" / BC AI scene** | "Vancouver AI Meetup #16", "BC + AI Is Live", "Vancouver AI January 2025 Recap", "BC's AI Ecosystem: A Mycelial Network" | Geographic + topical authority. Almost unique in the world. KK + BC + AI = a brand. |
| **"AI for journalists / media"** | "What Journalists Need to Know About AI", "AI Training for Media, PR…", "Vancouver Tech Journal Isn't Journalism" | High commercial intent ties to AI Upgrade for Media Leaders offer. |
| **"AI for creatives"** | "A Creative Technologist's AI Age Manifesto", "We Don't Do Panels, We Do Portals" | Ties to Creative Professionals offer and the Workshop. |
| **"AI second brain" / personal workflow** | "How to Build an AI Second Brain That Actually Works", "Punk Rock AI" | High-traffic potential SEO topic. People search for this. |
| **AI ethics / bias / philosophy** | "Name the Bias", "Both Hands Full", "Transcending Tech's Darker Impulses", "AI Ate the Future" | Identity-defining content; perfect for `FAQPage`/`AnalysisNewsArticle` schema. |
| **Conversation / podcast** | "Human Biography Podcast w/ Sharad Khare", "Shane Gibson's AI Sales Dojo" | Belongs in MØTLEYKRÜG umbrella; should be linked structurally to the podcast page. |

### 2.5 Top opportunity posts for AI/generative search

These are posts that, with the right markup and structure, would be the highest-leverage citation targets for LLMs answering questions about Vancouver AI, AI ethics, or creative AI work. They are also evergreen.

Recommendations: add Article schema (P0, blocked by schema work), tighten alt text on all images, ensure each has a clean Person/author byline rendered, and link them from a topical category landing page once categories exist.

1. **`bc-ai-is-live-and-were-building-the-future-we-actually-want`** (2025-05-18) — Founding statement for BC + AI; perfect for AI summaries of "what is BC + AI Industry Association."
2. **`bcs-ai-ecosystem-a-mycelial-network-of-creation`** (2025-02-16) — The mycelial framing is sticky and quotable.
3. **`a-creative-technologists-ai-age-manifesto`** (2025-03-30) — Manifesto-shaped content is LLM gold.
4. **`how-to-build-an-ai-second-brain-that-actually-works-for-you`** (2025-04-01) — Strong SEO target; people search for "AI second brain."
5. **`how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada`** (2025-04-08) — Indigenomics.ai exposure; ties KK to Indigenous-tech entity.
6. **`web-summit-vancouver-2025-survival-guide`** (2025-04-13) and **`web-summit-vancouver-2026`** (2026-05-07) — Annual recurring entity. Worth linking together and giving a permanent landing page (e.g. `/web-summit-vancouver/` as a parent collection).
7. **`what-journalists-need-to-know-about-ai-right-now`** (2025-06-24) — Direct funnel into AI Upgrade for Media offer.
8. **`ai-training-for-media-pr-and-creative-professionals`** (2025-07-08) — Same.
9. **`fears-hopes-and-dreams-for-our-relationship-with-ai`** (2024-12-20) — Philosophy piece; quotable.
10. **`punk-rock-ai`** (2026-05-04) — Recent, 3427 words, strong voice. With schema + alt text, this is a citation magnet for "punk rock approach to AI" queries.

### 2.6 Recent posts with missing categorization → quick wins

The 3 fully uncategorized posts in the recent 101 (no categories at all) should be triaged first when category restructuring lands. Need wp-admin to identify; the REST data shows `categories: []` on these.

---

## 3. Content gaps

Topics that come up in posts but have no anchor page:

| Gap | Why it matters | Proposed |
|---|---|---|
| **"BC + AI Industry Association"** | KK is exec director; mentioned across many posts; no canonical page on kriskrug.co | A `/bc-ai/` page summarizing the association, linking out to its own site, with `Organization` schema |
| **"Indigenomics.ai"** | Same situation | A `/indigenomics/` page or section on the Recent Projects page |
| **"MØTLEYKRÜG Podcast"** | Has a page (2828), but episodes aren't linked from there as `PodcastEpisode` items | Restructure podcast page as a series listing |
| **"AI second brain / personal workflow"** | One blog post; lots of search demand | Promote to a pillar page; link in nav |
| **"Vancouver AI Meetup" landing** | Many recap posts, no parent page | `/vancouver-ai-meetup/` collecting all recaps |
| **"Web Summit Vancouver"** | Annual coverage; should be a perma-page that updates | `/web-summit-vancouver/` collecting all years |
| **Press / Media Kit** | EPK exists for podcasts but not general press | `/press/` page with headshots, bios, links |

---

## 4. Recommended information architecture

Current: 34 flat top-level pages, 941 posts in 2 categories.

Proposed:

```
/                           (home)
├── about/                  (about)
├── projects/               (renamed from recent-projects-include)
│   ├── motleykrug-podcast/
│   ├── bc-ai/             (NEW — landing page for BC + AI association)
│   ├── indigenomics/      (NEW)
│   └── art-island/        (renamed from art-island-perspectives-…)
├── services/              (parent page summarizing all offers)
│   ├── ai-upgrade-media/
│   ├── ai-upgrade-creative/
│   ├── ai-upgrade-coaching/
│   ├── workshops/         (renamed from generative-ai-workshop-…)
│   └── creative-services/ (renamed from generative-ai-services)
├── speaking/
│   └── podcast-guesting/  (renamed from podcast-guesting-page-epk)
├── publications/
├── testimonials/
├── events/
│   └── web-summit-vancouver/  (NEW pillar page)
├── blog/                  (post archive)
├── press/                 (NEW)
├── worldview/             (renamed from the-kk-worldview)
├── reconciliation/        (renamed from reconciliation-indigenous-land-acknowledgement)
├── contact/
├── privacy/
├── international/         (NEW parent for multilingual welcomes — OR noindex variants)
│   ├── japanese/
│   ├── chinese/
│   ├── etc.
└── sponsor/               (renamed from sponsor-cyberpunk-chronicles-newsletter)
```

Every renamed slug becomes a 301 from the old URL — no link rot.

This is a 1-2 day project once we have admin access. The win is significant: clear hierarchy, descriptive slugs, every cluster has a topical anchor for SEO + AI.

---

## 5. What this audit did **not** cover

- **Per-page word count for the 11 pages I didn't fetch HTML for** (would need 11 more curls; easy to do).
- **Quality assessment of individual older posts (pre-2024).** Out of scope per user direction.
- **Comment moderation / quality** (Akismet is enabled but disabled in MCP; can't read comments).
- **Internal link graph** (would need to scrape every page; doable but time-consuming).
- **Most-trafficked posts** — requires Jetpack Stats or GA4 access. Without that, the "top opportunities" list above is based on title quality and topical fit, not actual traffic.
- **Form conversion rates** — Jetpack Forms data isn't accessible via current MCP.

🔵 When admin access is available: pull GA4 + Jetpack Stats top-20 pages by traffic, then re-rank opportunities by `traffic × topical fit`.
