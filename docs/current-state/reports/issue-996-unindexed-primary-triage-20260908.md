# Issue #996: Unindexed primary-article triage and five-URL recovery batch

**Captured:** 2026-09-08T05:54Z (UTC)
**Mode:** Track A, read-only. Public HTML (plain + cache-busted), public REST GET, sitemap/robots/feed. Zero WordPress writes. Zero cache purges. Zero Search Console submits / Validate Fix / sitemap submit / removal.
**Refs:** #996 (this batch). Cross-link only: #274 (sitemap follow-through), #331 (archive policy, already deployed), #402 (growth umbrella), #994/#339 (Second Brain; not touched), #995 (Events; not touched), #997 (404/canonical buckets; one pagination collision handed off), #830 (Cyber Love Garden / `/ai-for-creatives/` write surface; not edited).
**Draft pack:** [`content/drafts/issue-996-indexing-recovery/`](../../../content/drafts/issue-996-indexing-recovery/)

Success for this issue is a ranked, reviewable draft-PR batch. It is not a promise of Google inclusion.

---

## Ranked recommendation

Prepare a five-URL recovery batch around the Future Proof / photography / generative-AI residency cluster. Do not try to index the 892-example report. Do not remove intentional noindex.

| Rank | URL | ID | Manifest action | Why this rank |
|---:|---|---:|---|---|
| 1 | `/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` | 4539 | content improvement + internal-link repair + manual indexing recommendation | Only URL the 2026-09-06 GSC audit named as a crawled-not-indexed primary. Still 200, self-canonical, no noindex. Dated present-tense February invite. Two footer inbound only. Hub `/ai-for-creatives/` does not link it. **Not excluded.** |
| 2 | `/2023/09/06/exploring-the-world-of-ai-image-generation-with-artist-frank-yu/` | 3082 | content improvement + internal-link repair | Same artist, original conversation, empty `jetpack_seo_html_title` so the live title is a 75-character fallback. No href to 4539. GSC membership **unconfirmed**. |
| 3 | `/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/` | 4372 | internal-link repair | Inaugural residency sibling that 4539 already names, but 4539 points at Notion instead of this permalink. Footer is the unrelated early-blog archive. GSC membership **unconfirmed**. |
| 4 | `/2023/12/28/generative-ai-future-proof-creatives-online-training-workshops-2024/` | 4359 | internal-link repair | Practical-AI / community workshop record. Public REST search found **zero** inbound hrefs to this slug. GSC membership **unconfirmed**. |
| 5 | `/2024/03/05/join-the-future-proof-creatives-community/` | 4826 | internal-link repair | Community-series landing. Public REST search found **zero** inbound hrefs to this slug. Mentions workshops 20 times and photography/residencies zero times. GSC membership **unconfirmed**. |

**Photography/generative-AI candidate (must-include rule):** still in the batch. Fresh public evidence does **not** exclude it. It remains HTTP 200, one self-canonical, robots `max-image-preview:large`, no `googlebot` noindex, in `wp-sitemap-posts-post-1.xml`, `?p=4539` 301s to the pretty permalink. A generic web search also surfaced the URL; that is not a GSC URL Inspection result and does not override the 2026-09-06 listing.

Reviewed and not selected (still eligible primaries; do not spend this batch on them):

| URL | Why not in the five |
|---|---|
| Autolume `/2024/06/18/the-cyborg-art-of-autolume-when-ai-meets-the-human-lens/` (5833) and `/2024/12/02/autolume-post-photographic-cybernetic-portraiture/` (7631) | Photography + AI flagship. Already have contextual inbound from meetup recaps. A public web search surfaced both. More likely already indexed; confirm in GSC before opening a later wave. |
| Vancouver AI meetup posts 4495 / 4348 | #402 already treats `vancouver ai community meetup` as a surprising winner. Wrong report for an unindexed-recovery batch. |
| Cyber Love Garden 2650 | #402 winner and #830 destination. Do not duplicate. |
| AI Second Brain 8802 | #994 / #339. |
| `/events/` | #995. |
| Hardcore photoshoot 1067 / photographer-negotiation 1210 | #402 / #828. Indexed-winner or rewrite lanes, not this report. |

---

## 1. Snapshot dates, coverage, and the GSC hole

### 1a. What this session could not retrieve

I have no Google Search Console access from this machine. I did not invent indexing states, last-crawl dates, Google-selected canonicals, referring sitemaps, or query demand.

| Needed for #996 | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, or Search Console names in `.env.schema`. |
| Signed-in GSC UI | **Not available.** |
| Current "Crawled — currently not indexed" example export | **Absent** from the repo. The issue says the local audit report is uncommitted on purpose. |
| Report update date / pagination / export completeness for the 892 rows | **Unknown.** Cannot refresh the 2026-09-06 example list. |
| URL Inspection (indexing state, last crawl, Google-selected vs user canonical, discovery/referring sitemap, crawl permission) | **Missing for every URL.** |
| Performance → Search results page/query rows | **Missing.** Not invented from Profound, Site Kit chrome, or web search. |
| WP credentials for Site Kit REST | **Absent.** `make doctor` FAIL: no `WP_USER` / `WP_APP_PASSWORD` and no `WP_API_*`. Site Kit `1.186.0` is visible in public HTML only. |

### 1b. Dated GSC evidence copied from issue #996 (not re-measured)

These are KK's 2026-09-06 signed-in observations for property `sc-domain:kriskrug.co`. Treat them as a dated snapshot, not current counts.

| Item | 2026-09-06 claim | This session |
|---|---|---|
| Crawled — currently not indexed examples | 892, mixed classes; not 892 missing articles | **Not re-fetched** |
| Named primary still listed | `https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` | Public eligibility **refreshed** 2026-09-08; still include |
| Sitemap GET of all posts + pages | 974 posts + 46 pages, all 200, self-canonical, descriptions, no noindex | **Refreshed:** 975 posts + 46 pages = 1021. Sampled targets still 200 / self-canonical / description / no noindex |
| Excluded noindex inventory | 964 examples: 901 share variants, 46 login, 6 embeds, 11 tag archives; no primary articles | Public class reps **refreshed**; see §2. Intentional exclusions kept |

### 1c. Public session snapshot

| Signal | 2026-09-08 observation |
|---|---|
| WordPress generator | `7.0.4` |
| Aurora live `style.css` Version | `1.6.11` (repo `main` agrees; `make status-readonly`) |
| `make seo-publisher-smoke` | PASS: `/wp-sitemap.xml` 200, `/feed/` 200, `/news-sitemap.xml` 200, three recent posts emit `BlogPosting` with required fields |
| `make doctor` | FAIL (expected here): no WP creds, no `scripts/notion-to-wp/.venv` |
| Draft-queue counts | unavailable without creds |
| `robots.txt` Sitemap: | `https://kriskrug.co/sitemap.xml` → **301** to `/wp-sitemap.xml` (same sloppy declaration as earlier SEO notes; owned by the root-files snippet, not this batch) |
| News sitemap | 200, 169 bytes, does not contain 4539 (expected; not a 48h NewsArticle) |
| `make seo-audit` | **Not used as evidence.** Public HTML is authoritative; the legacy inventory can still lie about Jetpack fields |

---

## 2. URL classes, grouped before ranking

The current submitted sitemap is **primary posts and pages only**. That matches the #331 v2 deploy receipt. The 892-example report is therefore mostly URLs that are **not** in the sitemap, plus a minority of genuine articles.

| Class | What I checked 2026-09-08 | Live behaviour | Disposition |
|---|---|---|---|
| Primary post | 975 URLs in `wp-sitemap-posts-post-1.xml` | Sitemap-only class. Sampled five are 200, one self-canonical, `max-image-preview:large`, description present | Rank and recover a subset. Do not bulk-index 975 |
| Primary page / hub | 46 URLs in `wp-sitemap-posts-page-1.xml` | Same eligibility shape | Out of this batch unless a hub is an inbound source. `/ai-for-creatives/` (12316) is a #830 write surface; **not used** |
| Category archive | `/category/ai-ethics-philosophy/` | 200, robots `max-image-preview:large, noindex, follow`, no canonical | Intentional #331. Keep |
| Tag archive | `/tag/ai/` | 200, same noindex,follow | Intentional. Matches the 11-tag-archive exclusion class |
| Author archive | `/author/kk/` | 200, same noindex,follow | Intentional #331 |
| Date archive | `/2024/01/` | 200, same noindex,follow | Intentional |
| Share / tracking variant | `…/exploring-the-intersection-of-photography-and-generative-ai/?share=twitter` | **301** to the clean permalink, then 200 / self-canonical | Intentional (`fixes/gsc-404-query-param-canonicalize.php`). Matches the 901-share-variant class. Do not index the variant |
| Login / utility | `/wp-login.php` | 200, robots `max-image-preview:large, noindex, noarchive` | Intentional. Matches the 46-login class |
| Embed | `…/exploring-the-intersection-of-photography-and-generative-ai/embed/` | 200, robots `noindex, follow`, canonical to the parent article | Intentional. Matches the 6-embed class |
| Search | `/?s=photography` | 200, robots `noindex, follow`, disallowed in `robots.txt` | Intentional |
| Feed | `/feed/` | 200, no robots/canonical in the RSS document | Discovery surface, not a primary article |
| Pagination / malformed | `/page/2/` is 200, robots indexable (`max-image-preview:large` only), canonical **`https://kriskrug.co/2/`**. Fetching `/2/` 200s a **different** primary (`/2023/11/05/20-ways-to-resist-ais-mind-enslavement/`) | Canonical collision, not an unindexed-article fix | Hand off to **#997**. Do not add `/page/2/` to this batch |

**Join rule used here:** a recovery candidate must be a current sitemap primary (post or page), resolve 200 without a hop, carry exactly one self-canonical, and not emit noindex. Retired aliases, archives, feeds, pagination, share variants, embeds, and login URLs are separated first. Distinct slugs were not merged.

I could not join the live 892-row example list to the sitemap because that export is not in this session. The class table above is the public stand-in. Ranks 2–5 are **theme-matched eligible primaries**, not confirmed members of the current GSC example list. KK should tick those four against the current Crawled-not-indexed examples before any write.

---

## 3. Public eligibility for the five (HTML is authoritative)

All five: HTTP 200 from `Pagely-ARES/1.22.28`, `?p={id}` 301 to the pretty permalink (one hop), exactly one self-canonical, no `googlebot` meta, robots `max-image-preview:large` (indexable), standard description present, in the post sitemap, **not** in `/feed/` (expected; none are recent). `curl -sSIL` recorded 2026-09-08T05:53Z.

| ID | `<title>` (chars) | description (chars) | H1 | Featured | `modified` / `modified_gmt` | Article words (approx.) |
|---:|---|---|---|---:|---|---:|
| 4539 | `Photography Meets Generative AI: Frank Yu Residency` (51) | present-tense February invite (157) | Exploring the Intersection of Photography and Generative AI | 4546 | `2026-06-28T20:36:28` / `2026-06-29T04:36:28` | 853 |
| 3082 | `Exploring the World of AI Image Generation with Artist Frank Yu \| Kris Krüg` (75) | 15-year craft line (148) | same as post title | 3108 | `2026-06-28T20:38:45` / `2026-06-29T04:38:45` | 801 |
| 4372 | `Building AI Companions w/ John Anthony Hartman` (46) | residency one-liner (152) | full post title | 4380 | `2026-07-24T14:39:51` / `2026-07-24T22:39:51` | 731 |
| 4359 | `Generative AI: Future Proof Creatives Workshops 2024` (52) | unveil line (155) | full post title | 4361 | `2026-07-01T16:24:12` / `2026-07-02T00:24:12` | 693 |
| 4826 | `Future Proof Creatives Community & Event Series \| Kris Krüg` (59) | community skills line | full post title | 4543 | `2026-07-24T14:39:53` / `2026-07-24T22:39:53` | long FAQ/series page |

REST `meta` (public, theme-registered; do not treat `make seo-audit` counts as truth):

| ID | `jetpack_seo_html_title` | `advanced_seo_description` |
|---:|---|---|
| 4539 | set; matches live `<title>` | set; matches live description |
| 3082 | **empty** | set; live description is this fallback |
| 4372 | set; matches live `<title>` | set |
| 4359 | set; matches live `<title>` | set |
| 4826 | set; live `<title>` appends sitename | set |

No competing canonical. No on-page noindex. Technical eligibility is not the missing piece for 4539; discovery and dated present-tense copy are.

---

## 4. Inbound internal links (public REST `content.rendered` href count)

Counting rule: `GET /wp/v2/posts?search={slug}` then keep only `<a href>` values that contain the slug. Pages searched the same way.

| Target | Posts with a real href | Notes |
|---|---:|---|
| 4539 | **2** | 3820 footer "See also"; 3219 footer "See also". **0 pages.** Hub 12316: 0 |
| 3082 | **2** | 2930 and 1401, both collection-footer style |
| 4372 | many footers | REST `search=` over-matches; the href hits are baked "Web and Early Blog archive" footers on old posts, not contextual residency links |
| 4359 | **0** | Isolated |
| 4826 | **0** | Isolated |

Already-good inbound that this pack must **not** duplicate: 3820 and 3219 → 4539.

`/ai-for-creatives/` (12316, `modified` `2026-09-03T09:52:49`) currently links Both Hands Full, Taste Is Your Moat, Cyber Love Garden, the AI-creatives archive, services, and speaking. It does not mention Frank Yu, Autolume, or 4539. A hub card would help 4539, but 12316 is the #830 write surface. This pack does not edit it.

---

## 5. Compact URL manifest

| Rank | ID | Canonical URL | Class | GSC 2026-09-06 | Public 2026-09-08 | Action | Rationale |
|---:|---:|---|---|---|---|---|---|
| 1 | 4539 | `https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` | primary_post | named crawled-not-indexed | eligible; weak inbound; present-tense event copy | **content improvement + internal-link repair + manual indexing recommendation** | Only confirmed named primary. Keep the February 2024 session facts. Add an answer-first line, retarget the Hartman Notion href to 4372, and add two contextual inbound wraps. After an approved write + Pagely purge, KK submits this exact URL in URL Inspection. Do not click Validate Fix from an agent session |
| 2 | 3082 | `https://kriskrug.co/2023/09/06/exploring-the-world-of-ai-image-generation-with-artist-frank-yu/` | primary_post | unknown | eligible; empty SEO title; no href to 4539 | **content improvement + internal-link repair** | Same artist, original notes. Set a short SEO title. Close with one 4539 wrap. Confirm GSC membership before apply |
| 3 | 4372 | `https://kriskrug.co/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/` | primary_post | unknown | eligible; no contextual href to 4539 | **internal-link repair** | Series sibling. One closing wrap to 4539. Do not recategorize the early-blog footer in this lane |
| 4 | 4359 | `https://kriskrug.co/2023/12/28/generative-ai-future-proof-creatives-online-training-workshops-2024/` | primary_post | unknown | eligible; 0 inbound hrefs | **internal-link repair** | Isolated workshop record. One paragraph pointing at 4539 and 4826. Confirm GSC membership before apply |
| 5 | 4826 | `https://kriskrug.co/2024/03/05/join-the-future-proof-creatives-community/` | primary_post | unknown | eligible; 0 inbound hrefs | **internal-link repair** | Community landing that never names the residency. One sentence in the opening pointing at 4539 and 4359 |

No row is **no change**. No row is **canonical/redirect investigation** (those collisions belong to #997). Manual indexing is recommended only for 4539 unless KK confirms ranks 2–5 in the current GSC example list.

---

## 6. Overlap and surfaces this pack will not touch

| Lane | Why it stays untouched |
|---|---|
| #339 / #994 / post 8802 / sources 9774 and 12327 | Second Brain diagnosis and pending apply packet |
| #995 / `/events/` | Events CTR |
| #274 / #331 snippet 26 | Sitemap children and archive robots. Already doing the right thing for archives |
| #402 parent + #830 pack | `/ai-for-creatives/` page 12316, posts 2819 / 2661 / 3567 / 2650 |
| #828 / #834 / #249 About 1208 | Other SEO writes |
| Share-variant snippet | Already 301s; keep |

---

## 7. Proposed writes (local only)

Exact FIND/REPLACE, identity guards, rollback, and the post-approval checklist live in [`content/drafts/issue-996-indexing-recovery/`](../../../content/drafts/issue-996-indexing-recovery/). Summary:

| Object | Fields that would change after KK approval | Fields that must not change |
|---|---|---|
| 4539 | `content` (answer-first paragraph + Hartman permalink retarget); `advanced_seo_description` | slug, status, date, categories, tags, featured_media, post title, `jetpack_seo_html_title` |
| 3082 | `content` (one closing wrap); `jetpack_seo_html_title` (currently empty) | slug, status, date, taxonomies, featured_media, post title, existing description unless KK also takes the optional tighten |
| 4372 | `content` (one closing wrap) | meta, slug, taxonomies, footer collection line |
| 4359 | `content` (one paragraph before the hashtag line) | meta, slug, luma URLs (do not claim they still sell seats) |
| 4826 | `content` (one opening sentence) | meta, FAQ body, luma CTAs |

Inbound sources are **only other members of this five**. That keeps the write set at five posts and satisfies "≤2 inbound source pages per target":

| Target | Source 1 | Source 2 |
|---|---|---|
| 4539 | 3082 wrap | 4372 wrap |
| 3082 | 4539 Frank Yu href (target-body outbound) | none further; a second wrap would be speculative |
| 4372 | 4539 Hartman href retarget (target-body outbound) | none further |
| 4359 | 4826 opening sentence | none further |
| 4826 | 4359 new paragraph | none further |

Two sources per target are used only where a real unsupported href already exists or a same-cluster sentence is already on the page. 3820 and 3219 already link 4539; they are not edited.

---

## 8. Future apply, rollback, readback

Not authorized by this report. When KK approves a write:

1. Authenticated snapshot first (`context=edit` JSON + public HTML + SHA-256) under `backup/<UTC>-issue-996/`.
2. Abort unless live `id` + `slug` + `status=publish` + `modified` match the guards in `manifest.json`. Never PATCH on ID alone.
3. Body writes: top-level `content` only. Meta writes: allowlisted `jetpack_seo_html_title` / `advanced_seo_description` only.
4. FIND must match exactly once in `content.raw`. Abort on 0 or >1.
5. One object, then authenticated + cache-busted public readback, then the next. Pagely does not auto-purge.
6. Rollback is re-POST of the snapshotted `content.raw` / prior meta. Do not rely on Pagely revisions.
7. After purge, KK (not an agent) may request indexing for 4539 in URL Inspection. Do not submit sitemaps, remove sitemaps, or click Validate Fix from an agent session.

Measurement (after at least 14 full days, then a 28-day compare): URL Inspection on each applied URL; Performance → Search results filtered to that exact page. Record clicks / impressions / CTR / position. Do not treat a recrawl-without-index as a failed content edit.

---

## 9. Acceptance criteria, marked honestly

| #996 criterion | Status |
|---|---|
| Retrieve current report examples; record snapshot / update / pagination / export limits; group URL classes | **Partial.** Classes grouped from public crawl + the dated 2026-09-06 issue text. Current 892-row export, report update date, and pagination coverage are **missing** (no GSC) |
| Join clean candidates to the current sitemap; separate primaries from aliases / archives / feeds / pagination / utility | **Met for public surfaces.** Sitemap is 975 posts + 46 pages. Class reps checked. No 892-row join |
| Rank ≤5 valuable primaries; include the photography/generative-AI candidate unless excluded | **Met.** 4539 included. Ranks 2–5 are GSC-unconfirmed |
| URL Inspection plus live HTTP/meta plus real inbound | **Partial.** Live HTTP/meta/inbound done. URL Inspection **missing** for every URL |
| Report + compact URL manifest with an action + rationale | **Met** by this file and the draft pack |
| Exact local proposals for ≤5 targets and ≤2 inbound sources; avoid #339 / Second Brain | **Met.** Pack under `content/drafts/issue-996-indexing-recovery/`. Other-lane files not edited |
| Identity / modified / hash guards, proposed fields, rollback, readback/measurement | **Met** in the pack. Public `content.rendered` hashes are session evidence; apply must re-GET `content.raw` |

Keep #996 open. Use `Refs #996`, not `Closes`.

### Exact GSC pull KK can run later

Search Console → Indexing → Pages → **Crawled — currently not indexed**, property `sc-domain:kriskrug.co`. Record report last-updated date, example count, and whether export covers all rows or the UI sample. Confirm whether these five pretty permalinks are still in the example list. Then URL Inspection on 4539 (required) and on 3082 / 4372 / 4359 / 4826 before apply.

Do not invent those rows in a later comment if the export is still missing.
