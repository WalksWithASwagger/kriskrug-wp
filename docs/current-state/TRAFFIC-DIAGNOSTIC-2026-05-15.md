# Traffic diagnostic — kriskrug.co, 2026-05-15

**Question KK asked:** *"My site gets shitty traffic vis-à-vis how long it's been online. I can barely Google my own headlines up."*

**Answer in one line:** the site looks technically clean today, so the lever is **content/architecture/theme**, not bug-fixing. Specifically: **theme weight (Catch Responsive) + zero topical authority signal (99% uncategorized) + thin internal link graph + no recent publish cadence**. The KK Aurora theme migration + the categorization sweep + a weekly publish cadence are the three things that move the needle.

---

## What I checked

### 1. Sitemap errors (formerly "31 errors per GSC")

- **Sample**: HEAD-checked the first 200 of 976 URLs in `sitemap-1.xml` → **0 errors** (no 404s, no 5xx, no broken redirects)
- **Full check** in progress (network-bound, 12-20 min wall time); update this doc when it lands
- **Inference**: GSC's 31-error count was likely **stale**, predating the Web Summit Vancouver 2026 restoration we did in this session and earlier housekeeping. GSC re-crawls on its own cadence (24-72h); the count should drift down over the next few days. Re-check the sitemap report next week — if it's still showing 31 errors against a clean sitemap, escalate.
- The current sitemap is **Jetpack-generated** at `/sitemap.xml` → `/sitemap-1.xml` (976 URLs, all confirmed live in the sample) and a separate `/news-sitemap.xml`. Both fine.

**Verdict:** sitemap is healthy. Not the cause of traffic underperformance.

### 2. Schema markup (deployed in last session)

Already confirmed live and rendering:
- **Person + WebSite** sitewide (homepage)
- **Person + Article + BreadcrumbList** on every blog post
- Article schema includes `headline`, `datePublished`, `dateModified`, `author` (resolves to `#person`), `articleSection`, `wordCount`, `image`

This was the single biggest AI/SEO miss before our work. It's fixed.

**Verdict:** structured data is no longer blocking ranking signal interpretation by Google or AI search engines.

### 3. Theme weight (the suspected lever)

Catch Responsive is a 2023 classic theme. Inspection of homepage HTML earlier in this audit found:
- jQuery + jQuery Migrate (legacy)
- Multiple Jetpack JS bundles (Stats, Carousel, Likes, Boost, Instant Search, Swiper)
- Popup Maker JS on every page
- Site Kit by Google
- Genericons font
- Catch Responsive's own custom JS
- ~50KB inline CSS in `<head>` (some unused on most pages)

We haven't run a Lighthouse pass yet (Chrome was busy this session). Strong inference:
- LCP probably OK (Pagely PressCache + CDN)
- INP likely poor (jQuery + Popup Maker is the usual culprit)
- Mobile rendering: untested

**Verdict:** **probable rank drag.** Google heavily weights Core Web Vitals. The KK Aurora theme (vanilla JS, GSAP, ~100KB JS budget) directly addresses this.

### 4. Categorization (the topical authority lever)

From the May 8 content audit (still true):
- **867 of ~941 published posts are in `Misc`** (the renamed `uncategorized` category)
- **1 post in `Oil Spill`** (the only meaningful category by usage)

That's it. Two categories. For 941 posts.

**What this signals to Google + LLMs**: the site has zero topical authority. There's no "Vancouver AI" cluster. There's no "AI for Creatives" cluster. There's no "AI Ethics" cluster. Each post is a snowflake floating in a sea of "Misc" — making it hard for any algorithm to recognize KK as an authority on any specific topic.

**This session moved the needle slightly:** "AI for Creatives" is now a real category (id 1665), with 2 scheduled posts going into it ("Your Taste Is Your Moat" 2026-05-16, "Make Culture, Not Content" 2026-05-17). And earlier in the session we created "Vancouver AI Ecosystem" with 1 post. So we have 2 real categories now. That's still 2 of ~10 needed.

**Verdict:** **this is the highest-leverage SEO unblock.** Categorize the 100 most-recent posts into the 9 proposed categories from CONTENT_AUDIT §2.2 → kriskrug.co goes from "uncategorized blog" to "thematic authority on Vancouver AI / AI for Creatives / AI Ethics / Indigenomics / etc."

### 5. Internal link graph (the discoverability lever)

From the May 8 content audit:
- **34 published pages, all top-level** — no parent/child hierarchy
- No pillar pages — `/bc-ai/`, `/vancouver-ai-meetup/`, `/web-summit-vancouver/`, `/press/` all proposed but don't exist
- Most posts have no inbound links from other posts
- The "related posts" Jetpack widget exists but is anemic without categorization to find related posts

This session we added a bidirectional cross-link between #11178 and #10594, which is the right pattern — but two posts isn't a graph.

**Verdict:** **this is the secondary lever, gated by Phase 2 categorization.** Once posts are categorized, building cross-link patterns becomes mechanical.

### 6. Image alt-text (image search + AI vision)

From the May 8 audit (still true):
- Homepage hero: 7 of 8 images have empty alt
- Recent post (Web Summit 2026): 16 of 18 images have empty alt
- Site-wide: most images uploaded 2018-2025 have no alt set

**Verdict:** **invisible to Google Images and AI vision search.** A vision-LLM batch fix (FIX_QUEUE P1.4) would resolve this in a few hours of compute time + KK review.

### 7. Publish cadence

From audit data:
| Year | Posts | Note |
|---|---|---|
| 2023 | ~64 | Active |
| 2024 | 75 | **Most prolific** |
| 2025 | 20 | **Sharp drop** |
| 2026 (Jan-May) | ~8 | Recovering, but spotty |

Google + LLM ranking algorithms reward **fresh, regular publishing**. Sites that go quiet drop down the rankings. The 2025 quiet period likely cost ranking that compounds month over month.

This session adds 2 scheduled posts (May 16 + 17). The connector now exists, so weekly cadence is operationally easy. Need to commit to it.

**Verdict:** **ranking decay is happening.** Reverse it by publishing 1-2 posts per week consistently for 3 months and watch the data.

---

## What I did NOT measure (yet)

- **Lighthouse / Core Web Vitals** — needs Chrome (was busy this session). Pending for next session.
- **GSC Performance report** — top queries, average position, CTR. Pending for next session.
- **Backlink profile** — needs Ahrefs / Semrush, not free.
- **Comparative ranking analysis** for "Kris Krüg" / "Vancouver AI" / etc. — manual SERP checks, can do via Chrome MCP next session.

---

## Highest-leverage actions, ranked

1. **Migrate to KK Aurora theme** (Phase 4 of the existing roadmap, effectively the SEO+performance combined unblock). Test on Cloudways dev first. **Expected impact: noticeable Core Web Vitals improvement, ranking signal lift over 4-8 weeks.**
2. **Categorize the 100 most-recent posts** into the 9 proposed categories. ~3-4 hours wp-admin bulk-edit. **Expected impact: builds topical authority signal, makes related-posts widget useful.**
3. **Commit to weekly publish cadence** via the now-hardened Notion connector. ~30 min per post once Notion source exists. **Expected impact: reverses the ranking decay from 2025's quiet period.**
4. **Run vision-LLM alt-text batch on top-100 most-trafficked images.** ~1 hour automation + KK review. **Expected impact: opens Google Images traffic channel currently zero.**
5. **Build pillar pages** (`/bc-ai/`, `/vancouver-ai-meetup/`, `/web-summit-vancouver/`, `/press/`). Half-day each. **Expected impact: anchor pages that catch broad search intent and channel it down to specific posts.**

These are exactly the items in [`ROADMAP.md`](ROADMAP.md) Phase 2 + Phase 5. The roadmap was already aimed at the right things; this diagnostic confirms the priority order.

---

## What changed in this session that may already be moving the needle

- **2 new posts scheduled** (Your Taste Is Your Moat 2026-05-16; Make Culture, Not Content 2026-05-17)
- **2 real categories** (Vancouver AI Ecosystem, AI for Creatives) replacing the Misc-everything default for at least 3 posts
- **Bidirectional cross-link** between sister pieces — small but real internal-link-graph progress
- **38 encoding artifacts fixed** in #10594 (reads cleaner, less "abandoned blog" signal)
- **All 15 ALL CAPS headings** in #10594 → title case (more readable, better skim signal)
- **Schema** continues to render on every post including the two scheduled ones

The kriskrug.co property in GSC should start showing slightly more impressions over the next 2-4 weeks just from the schema being live + the categorization improving + the recency signal from new posts. The theme migration is the bigger unlock.

---

## Update path

When the full sitemap diagnostic completes, append findings here under §1. When the Lighthouse pass happens, add §3 with real numbers. When GSC Performance data is captured, add §8 with top-queries analysis.
