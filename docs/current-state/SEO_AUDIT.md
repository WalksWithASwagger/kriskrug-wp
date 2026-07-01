# SEO Audit — kriskrug.co

> **STATUS: Historical / Superseded 2026-07-01.**
> This audit preserves May 2026 findings, including Jetpack-era sitemap notes.
> Current sitemap and Search Console instructions live in
> [`../../fixes/issue-37-xml-sitemap-setup.md`](../../fixes/issue-37-xml-sitemap-setup.md):
> submit only `https://kriskrug.co/sitemap.xml`; do not advertise or submit
> the former Jetpack news/image/video sitemap endpoints.

**Audit date:** 2026-05-14
**Scope:** Technical SEO + on-page + AI / generative search readiness.
**Method:** Public REST API + HTML inspection of 16 representative pages. No admin or SSH access used.
**Companion docs:** [CONTENT_AUDIT.md](CONTENT_AUDIT.md), [FIX_QUEUE.md](FIX_QUEUE.md).

---

## Executive summary

The site has the bones of solid SEO — sitemaps work, OG tags are present site-wide, meta descriptions are mostly thoughtful, page word counts are healthy. The big gaps are **zero structured data** (no JSON-LD on any page), **no AI-discoverability surface** (no `llms.txt`, no AI-crawler directives, no author/Person schema), **broken alt-text coverage** (most images have empty `alt`), and **a missing hreflang network** across the 7 multilingual welcome pages.

For generative / AI search, the most impactful single change is **adding `Article`, `Person`, and `WebSite` JSON-LD** — that alone changes whether LLMs cite KK by name and attribute claims to him versus pulling anonymized snippets.

**P0 fixes** (do first, high impact, low effort):
1. Add `llms.txt` at site root
2. Add JSON-LD `Person` + `WebSite` to homepage; `Article` to every post
3. Fix homepage H1 (currently empty + a second one says "Why Choose Me?")
4. Add `alt` text to at minimum the first 20 most-viewed images
5. Add hreflang network connecting the 7 language variants
6. Pick AI-crawler stance and write it explicitly into `robots.txt`

See [FIX_QUEUE.md](FIX_QUEUE.md) for the full P0→P3 backlog with effort and impact ranking.

---

## 1. Technical foundation

### 1.1 robots.txt

Current content:
```
Sitemap: https://kriskrug.co/sitemap.xml
Sitemap: https://kriskrug.co/news-sitemap.xml
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
```

**Findings:**
- ✅ Sitemap declared, and the URL is correct (Jetpack sitemap at `/sitemap.xml` resolves to a real index).
- ✅ wp-admin disallow is standard.
- ❌ **No explicit stance on AI crawlers.** GPTBot, ClaudeBot (Anthropic), PerplexityBot, CCBot (Common Crawl), Google-Extended (Gemini training), Applebot-Extended, anthropic-ai, FacebookBot, Bytespider, etc. all default to allowed because there's no `Disallow` directive.
- ❌ **No image sitemap reference** even though one exists (`/image-sitemap-index-1.xml`).

**This is a strategic choice, not a bug.** Two reasonable defaults:
- **"Be cited" stance** (recommended for KK): explicitly **allow** every legitimate AI crawler. This is what most public-facing thought-leaders want — to be quoted in ChatGPT, Claude, Perplexity, Gemini answers.
- **"No training" stance**: explicitly disallow training-purpose crawlers (`Google-Extended`, `anthropic-ai`, `CCBot`, `Applebot-Extended`) while keeping retrieval bots (`GPTBot`, `ClaudeBot`, `PerplexityBot`) allowed because those are user-initiated retrieval, not training.

See `fixes/robots-txt-update.txt` for both options ready to paste.

### 1.2 Sitemap

Jetpack generates a correct sitemap index at `/sitemap.xml`:
- `sitemap-1.xml` — **975 URLs** (pages + posts + jetpack-testimonial post type)
- `image-sitemap-index-1.xml` → 3 image sitemap files (paginated)
- `video-sitemap-1.xml` — videos (a few entries from 2023)
- `news-sitemap.xml` — Google News-format sitemap (works, separately declared in robots.txt)

**Findings:**
- ✅ Sitemaps exist, validate, and are referenced in robots.txt.
- ✅ Image sitemap exists — important for AI image search and Google Images.
- ⚠️ `video-sitemap-1.xml` last modified 2025-03-02 — newer videos missing.
- ⚠️ Yoast and Rank Math sitemap URLs both 404 (confirms **no dedicated SEO plugin installed** — only Jetpack).
- ⚠️ **The image sitemap isn't directly named in robots.txt.** Some crawlers won't discover it from the index.

### 1.3 Canonicals, redirects, and URL structure

| Page type | URL pattern | Canonical | Redirects |
|---|---|---|---|
| Pages | `/slug/` | ✅ Self-referential canonical present | None |
| Posts | `/YYYY/MM/DD/slug/` | ✅ Self-referential canonical | `/slug/` 301s to `/YYYY/MM/DD/slug/` (good) |
| Tags | (untested) | (likely OK) | — |

**Findings:**
- ✅ Canonicals are present on every audited page.
- ⚠️ The `YYYY/MM/DD/slug/` permalink structure is **legacy WordPress default**. It's not bad per se, but it dates content visibly in the URL and creates messy slugs. Many modern thought-leader blogs use `/slug/` for posts (more evergreen-feeling). Switching now would require a comprehensive 301 redirect map — significant work for a 941-post archive.
- 🔵 Recommendation: keep current structure (don't gamble a working redirect map), but ensure new posts use descriptive, evergreen slugs that don't fight the date prefix.

### 1.4 HTTPS / TLS / mixed content

- ✅ Site is HTTPS-only (verified — homepage redirects http→https, HSTS headers handled by Pagely).
- ✅ All assets load over HTTPS (no mixed-content warnings in HTML inspection).

### 1.5 Page speed & caching signals

From response headers:
- ✅ `x-gateway-cache-status: HIT` — Pagely PressCache is working on the homepage (cached at edge).
- ✅ Static assets served from `s5102.pcdn.co` (Pagely CDN).
- ✅ Jetpack Boost is loaded — critical CSS inlined on the homepage.
- ⚠️ The Catch Responsive theme inlines a substantial chunk of CSS in the head (~50K visible in the raw HTML). I didn't run coverage to verify how much is actually unused on a given page — flagged for verification with a Lighthouse / Coverage tab run.
- ⚠️ jQuery, jQuery Migrate, multiple Jetpack JS bundles, Site Kit, Popup Maker, instant-search, swiper all loaded — heavy JS payload for a content site.

Speed isn't directly measured here (no Lighthouse run), but inferring from the HTML the homepage will likely score:
- LCP: probably OK (cached + CDN)
- CLS: likely fine
- INP / TBT: probably *not* great because of jQuery + Popup Maker + Jetpack Search all loading on every page

🔵 Run Lighthouse in Chrome (when ready) to confirm. If INP is the bottleneck, the win is in dequeuing Jetpack Search assets on pages that don't need them.

### 1.6 Mobile

Catch Responsive is, by name, responsive. Viewport meta is present (`width=device-width, initial-scale=1`). Visual mobile testing wasn't done in this audit — recommend a manual or Chrome DevTools mobile pass.

---

## 2. On-page SEO

### 2.1 Titles

Title structure across 17 inspected pages:

| Page | Length | Title |
|---|---|---|
| Homepage | 103 | `Kris Krüg \| Generative AI Tools & Techniques - Empowering Events & Organizations for the AI Age` |
| About | 109 | `Techartist, quasi-sage, cyberpunk anti-hero from the future. Kris Krüg \| Generative AI Tools & Techniques` |
| Services | 95 | `Generative AI Creative Services & Strategy Kris Krüg \| Generative AI Tools & Techniques` |
| AI Upgrade (Creative) | 86 | `AI Upgrade for Creative Professionals Kris Krüg \| Generative AI Tools & Techniques` |
| AI Upgrade (Media) | 84 | `AI Upgrade for Modern Media Leaders Kris Krüg \| Generative AI Tools & Techniques` |
| Contact | 66 | `Contact Kris Krüg - Kris Krüg \| Generative AI Tools & Techniques` |
| Speaking | 57 | `Speaking - Kris Krüg \| Generative AI Tools & Techniques` |
| Blog | 61 | `Blog - Kris Krüg \| Generative AI Tools & Techniques` |
| Publications | 61 | `Publications - Kris Krüg \| Generative AI Tools & Techniques` |
| Testimonials | 61 | `Testimonials - Kris Krüg \| Generative AI Tools & Techniques` |
| Post: Web Summit | 76 | `Web Summit Vancouver 2026 - Kris Krüg \| Generative AI Tools & Techniques` |

**Findings:**
- ✅ Titles include the brand consistently.
- ⚠️ **5 of 17 titles exceed Google's typical SERP truncation point of ~60 characters.** "Generative AI Tools & Techniques" eats 32 chars before any page-specific content.
- ⚠️ Inconsistent separator: some use ` - `, some use ` | `, some have no separator before the brand at all (the Services page reads `Generative AI Creative Services & Strategy Kris Krüg | …`).
- ⚠️ The About page title burns 70 characters on flavor before the brand even starts (`Techartist, quasi-sage, cyberpunk anti-hero from the future.`).
- 🔵 Recommendation: standardize to `{Page} | Kris Krüg` (drop the descriptor in the title; keep it in the meta description). Cuts ~32 chars from every title, makes them more SERP-friendly, and is what generative search engines tend to use as citation text.

### 2.2 Meta descriptions

All inspected pages have meta descriptions. Quality is mixed:

**Good:**
- Homepage: `Explore Kris Krug's professional journey in the dynamic world of AI…` — coherent.
- About: `My name is Kris Krug – a boundary-pushing Creative Explorer…` — KK's voice, strong.
- AI Upgrade (Media): `Discover how to seamlessly integrate cutting-edge AI strategies…` — clear value prop.

**Less good:**
- Several look like first paragraphs auto-pulled — fine, but generic.
- Some are >155 chars and will get truncated in SERPs.

**Where these are coming from:** Almost certainly **Jetpack's SEO Tools module** (wp-admin → Jetpack → Settings → Traffic → "Search Engine Optimization"). Jetpack on the Free plan offers per-page meta description editing, and the `<!-- Jetpack Open Graph Tags -->` marker in the HTML confirms Jetpack is owning the meta-tag layer. There is no dedicated SEO plugin (Yoast / Rank Math / AIOSEO sitemap responses all 404) — Jetpack is the SEO surface today.

🔵 Recommendation: **install Rank Math** (free, lightweight, good schema support) or **SEOPress** to gain per-page control over meta + structured data. Yoast is fine but bloated for this scale of site.
**Important:** before activating Rank Math, **disable Jetpack's SEO Tools module** (same screen). Running both will produce duplicate / conflicting meta tags. The same applies for OG/Twitter — pick one source.

### 2.3 Open Graph / Twitter Cards

- ✅ `og:title`, `og:description`, `og:image` present on all audited pages (Jetpack Open Graph module is enabled — comment marker `<!-- Jetpack Open Graph Tags -->` confirms).
- ✅ `twitter:card` present on most pages.
- ⚠️ **Blog index page is missing twitter:card and canonical.**
- ⚠️ `og:image` defaults to the post's featured image; on pages without one, Jetpack uses a site-wide fallback. Several pages may share the same image — visually weak when shared.

### 2.4 H1 / heading hierarchy

| Page | H1 count | Notes |
|---|---|---|
| Homepage | **2** | One is empty, second is "Why Choose Me?" — neither matches the page title. |
| About | **4** | Multiple H1s is bad for SEO and AI parsing. |
| Blog | **0** | No H1 — bad. |
| Most other pages | 1 | OK. |

**Findings:**
- 🔴 Homepage's H1 situation is a meaningful issue. The current empty H1 is likely a logo wrapper. Modern best practice: the logo should be in a `<p class="site-title">` or similar, and the page-level H1 should be the actual content heading. "Why Choose Me?" being H1 misframes the page for crawlers — Google and LLMs may treat that as the page's main topic.
- 🔴 About page with 4 H1s likely comes from the Catch Responsive theme's section blocks. Should be H1 → H2 → H3.
- 🔴 Blog index page (`/blog/`) has 0 H1s — the page literally has no top-level heading. Theme-level fix.

These are theme-template issues. Fixing them right means editing `header.php` / template parts in a child theme.

### 2.5 Image alt text — critical for AI search

Sample coverage:

| Page | Total images | With real alt | Empty alt | Missing alt attr |
|---|---|---|---|---|
| Homepage | 8 | 0 | 7 | 1 |
| Post (Web Summit 2026) | 18 | 1 | 16 | 1 |

**This is the biggest invisible problem on the site.**

Modern image search (Google Images, Bing, Pinterest) and AI search (ChatGPT image understanding, Claude vision, Perplexity) both rely heavily on alt text to understand what an image is about *in context*. Empty alt = the image is decoration only. Missing alt = accessibility failure.

For KK specifically — a *photographer and creative whose images are often the message* — empty alt is leaving a huge surface unclaimed. An image of you presenting at a conference, with no alt text, is invisible to AI search. An image with alt="Kris Krug speaking at Web Summit Vancouver 2026 about AI's impact on creative work" is a citable answer.

🔵 Recommendation:
- **Pass 1 (manual):** Write real alt for the ~20 most prominent images (homepage hero, About page portrait, the headers of the 5 most-trafficked posts). Half-day of work.
- **Pass 2 (programmatic, if budget allows):** Use a vision LLM to draft alt text for every image in the Media Library, KK reviews & approves in batches. The fixes/ directory already has a relevant prep — see `fixes/issue-43-twitter-cards.php` for the schema-snippet pattern; the alt-batch script would follow the same approach.

### 2.6 Internal linking & navigation

Not directly inspected in depth (would need wp-admin or full HTML parsing), but headline observations:
- ⚠️ The site has 34 top-level pages, **no parent/child hierarchy**. This signals to crawlers that everything is equally important — flat, not curated.
- ⚠️ The 12 "fixes" prepared in the repo include `issue-13-14-15-project-sections.md` — looks like a planned restructure of project sections. Implementing it would create a clearer information architecture.

---

## 3. Structured data (JSON-LD)

**Result of audit:** ZERO `<script type="application/ld+json">` blocks on every page tested — homepage, about, services, posts, multilingual pages, blog index.

This is the single highest-leverage gap.

### Why this matters more than ever (2026)

| Search surface | What schema unlocks |
|---|---|
| Google SERP (traditional) | Rich results: stars, author photo, FAQ accordion, breadcrumb chips, video markup, event date |
| Google AI Overviews | Higher citation rate; explicit author attribution; entity disambiguation ("Kris Krüg" vs other Krügs) |
| ChatGPT browsing / search | Author/source attribution in citations; clean entity extraction |
| Claude search (web context) | Same as above; structured Article markup helps clean extraction |
| Perplexity | Source ranking favours canonical, structured content |
| Bing / Copilot | Strong response to BreadcrumbList, FAQPage, HowTo schema |

**The schemas KK should have:**

| Schema type | Where | Priority |
|---|---|---|
| `WebSite` (with `SearchAction`) | Sitewide (homepage) | **P0** |
| `Person` (you) | Sitewide author markup, plus homepage / about | **P0** |
| `Article` (or `BlogPosting`) | Every post — author, headline, date, image, body | **P0** |
| `BreadcrumbList` | All pages | P1 |
| `Service` | The 4 marketing offer pages (AI Upgrade for X, Workshops, Coaching) | P1 |
| `Event` | Events page (if events are listed) and each event post | P1 |
| `FAQPage` | Service pages, sponsor pitch page | P2 |
| `VideoObject` | The MØTLEYKRÜG podcast page + posts with video | P2 |
| `PodcastSeries` / `PodcastEpisode` | Podcast page | P2 |
| `ItemList` for testimonials | Testimonials page | P3 |

**Ready-to-paste snippets** for the P0 items live in `fixes/schema-snippets.php` (created as part of this audit). The implementation pattern: inject via a small mu-plugin OR via a Code Snippets plugin, so they're not theme-bound.

### Sample — what `Person` schema does

Without it, an LLM asked "Who is Kris Krüg?" pulls noisy text from your site (or worse, gets you confused with someone else). With this on every page:

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Kris Krüg",
  "alternateName": "Kris Krug",
  "url": "https://kriskrug.co",
  "image": "https://kriskrug.co/wp-content/uploads/kris-krug-headshot.jpg",
  "jobTitle": "Generative AI Strategist, Photographer, Community Builder",
  "worksFor": {
    "@type": "Organization",
    "name": "BC + AI Ecosystem Industry Association"
  },
  "sameAs": [
    "https://www.linkedin.com/in/kriskrug/",
    "https://twitter.com/kk",
    "https://www.youtube.com/@kriskrug",
    "https://en.wikipedia.org/wiki/Kris_Krug"
  ],
  "knowsAbout": ["Generative AI", "AI for Creative Professionals", "AI Ethics", "Vancouver Tech Community", "Photography"]
}
```

The `sameAs` array is what disambiguates entities for LLMs. Every URL in there reinforces "this Kris is that Kris."

---

## 4. AI / generative search readiness

### 4.1 `llms.txt`

**Status: ❌ Not present.**

`llms.txt` is the emerging convention (proposed by Jeremy Howard, gaining adoption across docs sites, SaaS, and creator sites in 2025–2026) for offering LLMs a structured, curated map of the site. It's a single Markdown file at `/llms.txt` that says: *"Here are my most important pages, in priority order, with one-line summaries."*

It's not yet a hard ranking signal, but Anthropic's Claude (when browsing), Perplexity, and many smaller agents read it. ChatGPT does not officially read it yet but treats it as bonus context when fetched.

**For KK, this is a low-effort, high-leverage win** because:
- He has a small, curated set of 34 pages — perfect for the format.
- The 7 multilingual welcome pages can be flagged as "language variants" so LLMs route correctly.
- The MØTLEYKRÜG podcast, BC + AI work, AI Upgrade offers, and Reconciliation page each have a clean one-liner.

Template prepared at `fixes/llms-txt-template.md`.

### 4.2 Author / E-E-A-T signals for AI

LLMs increasingly weight "experience + expertise + authoritativeness + trustworthiness" signals because they're trained to attribute and reduce hallucination. Current state for KK:

| Signal | Status | Fix |
|---|---|---|
| Clear `Person` schema (you) | ❌ Missing | Add via mu-plugin (P0) |
| `rel="author"` on posts | ❌ Missing | Theme template fix |
| Author byline visible on every post | ⚠️ Inconsistent (Catch Responsive sometimes hides it) | Theme fix or move to FSE theme later |
| Bio block at end of posts | ❌ Not present | Plugin or theme template |
| External profile cross-links (`sameAs`) | ⚠️ Some present in About page body, but not in structured form | Add to `Person` schema |
| Wikipedia entry | unverified | If KK has one, link in `sameAs` — huge weight signal |
| Verified social accounts (LinkedIn `verified`, X blue, etc.) | unverified | Worth confirming and listing |

### 4.3 AI crawler stance

See section 1.1. Three crawlers worth thinking about explicitly:

| Crawler | What it does | Recommendation for KK |
|---|---|---|
| **GPTBot** | OpenAI's crawler; powers ChatGPT search and training | Allow |
| **ClaudeBot** / **anthropic-ai** | Anthropic; powers Claude's web tools | Allow |
| **PerplexityBot** | Perplexity AI; user-initiated retrieval, attributed | Allow |
| **Google-Extended** | Google; training Gemini and AI Overviews | Allow (KK wants to be cited in AI Overviews) |
| **Applebot-Extended** | Apple Intelligence | Allow |
| **CCBot** | Common Crawl; bulk dataset used by many model trainers | Personal call — if KK wants his work in foundation-model training, allow. If concerned about uncompensated training, block. |
| **Bytespider** | ByteDance / TikTok | Allow or block based on personal stance |

For a public-facing thought-leader on AI specifically, **the strongest argument is allow everything**. Hiding from AI search is a strategic disadvantage in 2026.

### 4.4 Content suitability for LLM extraction

Spot checks on two recent posts:

**`Punk Rock AI` (2026-05-04, 3427 words):**
- ✅ Clear thesis in first paragraph.
- ✅ Strong section breaks.
- ✅ Quotable lines suitable for citation.
- ❌ No JSON-LD `Article`.
- ❌ Most embedded images have empty alt.

**`Web Summit Vancouver 2026` (2026-05-07, 2489 words):**
- ✅ Strong opening hook (LLMs love a clear premise).
- ✅ Author voice consistent (good for entity association).
- ❌ No author markup.
- ❌ 16 of 18 images have empty alt.
- ❌ Multiple `<section>` blocks but no headings inside them — sections without H2/H3 are essentially invisible to summarizers.

🔵 Content style is already LLM-friendly. The problem is the *envelope* (markup), not the content.

---

## 5. Specific bugs found

| Bug | Where | Impact |
|---|---|---|
| Duplicate Pinterest verification meta tags (`c0975…` and `f8bbe…`) | Sitewide head | Low; Pinterest may use the first only. Pick one and remove the other. |
| Empty H1 on homepage | Theme `front-page.php` | Medium — confuses crawlers about the page's main topic. |
| 2 published pages with empty rendered titles (IDs 3930 `empowering-events-…`, 2808 `subscribe`) | Page editor | Medium — these pages exist in the sitemap with blank titles. Either fix titles or `noindex`. |
| `wpadmin5102` user exposed in REST API | `/wp-json/wp/v2/users` | Low; not a vulnerability but unnecessary exposure. Consider setting user role properly or hiding via REST filter. |
| GA4 ID + Site Kit tag visible in HTML | Sitewide | None (this is normal). |
| Blog index page missing twitter:card and canonical | `/blog/` | Low; doesn't affect ranking but worth tidying. |
| Video sitemap stale (last entry 2025-03) | `/video-sitemap-1.xml` | Low — newer videos won't be indexed via video sitemap. |
| 7 multilingual pages without hreflang | Multilingual variant pages | Medium — Google can't connect them; user-language detection may serve wrong version. |

---

## 6. What's already addressed in `fixes/`

The repo already contains relevant work-in-progress for several of these gaps:

| Existing fix | Addresses | Status |
|---|---|---|
| `fixes/issue-36-meta-descriptions.md` | Meta descriptions | Likely overlaps — already partially solved |
| `fixes/issue-37-xml-sitemap-setup.md` | Sitemap | Mostly redundant (Jetpack sitemap is fine) |
| `fixes/issue-39-schema-markup.php` | Schema | **Direct overlap — check this file first before writing new schema** |
| `fixes/issue-43-twitter-cards.php` | Twitter Cards | Mostly redundant (Jetpack handles it) |
| `fixes/issue-9-button-hover-states.css` | UX, not SEO | — |
| `fixes/issue-5-color-contrast.css` | Accessibility, indirect SEO | — |

🔵 **Action:** before writing fresh schema snippets in this audit's `fixes/`, **review `fixes/issue-39-schema-markup.php`** to see if there's already a starting point we can extend.

---

## 7. What this audit did **not** cover

Honest about limits:

- **Lighthouse / Core Web Vitals** — needs browser run, not done here.
- **Backlink profile** — needs Ahrefs / Semrush; not run.
- **Keyword rank tracking** — same.
- **Page-level search console data** — needs Search Console access.
- **Plugin SEO settings** — needs wp-admin to see what Jetpack SEO module is actually configured to do.
- **Database-side SEO data** (e.g. whether per-page meta descriptions are stored as custom fields, and which post types have them) — needs SSH / wp-cli.
- **Mobile UX** — quick HTML inspection only, not on-device.
- **Old-post quality at scale** — covered in CONTENT_AUDIT.md, but per scope only recent ~100 posts.

These are real gaps the next iteration should fill once we have admin access and a backup.
