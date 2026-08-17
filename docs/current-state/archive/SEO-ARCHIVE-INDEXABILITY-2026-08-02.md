# Archive Indexability Policy Proposal, 2026-08-02

**Issue:** [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331)
**Status:** PROPOSAL. Nothing live was changed. No snippet was created, activated, or deactivated. No cache was purged. No Search Console action was taken.
**Lane:** Track A (content / SEO ops)
**Repo state at write time:** `main` at `dd87d4a`, branch `docs/331-archive-indexability`
**Supersedes as the current measurement:** `reports/issue-331-archive-policy-20260712.md` (2026-07-12) and `reports/taxonomy-sitemap-plan-331-20260726.md` (2026-07-26). The policy shape in those two docs still holds. The numbers in them do not.

---

## 1. Short version

Three weeks of drift added 17 URLs to the sitemap. That is not the interesting part.

The interesting part is that the sitemap was never the whole problem. Counting only what WordPress submits, archives are 642 of 1,658 URLs. Counting what a crawler can actually reach by following on-page links, archives are roughly **1,529 URLs**, because paginated archives and date archives are indexable too and neither shows up in `wp-sitemap.xml`. Date archives alone are about 755 crawlable URLs, and the snippet already merged for this issue (`fixes/issue-331-archive-sitemap-policy.php`, PR #334) does not touch them at all.

So the proposal is: keep the exclusion shape that the 07-12 and 07-26 passes landed on, add `is_date()` to the robots filter, and stop describing this as a sitemap problem when it is an indexability problem that the sitemap only partly reveals.

---

## 2. Measured counts, today vs 2026-07-12

All figures below come from read-only `curl` against production on 2026-08-02, plus the public REST endpoints. No authentication was used.

### 2.1 Sitemap membership

| Child sitemap | 2026-07-12 | 2026-07-26 | 2026-08-02 | Change vs 07-12 |
|---|---:|---:|---:|---:|
| `wp-sitemap-posts-post-1.xml` | 967 | 968 | **970** | +3 |
| `wp-sitemap-posts-page-1.xml` | 45 | 46 | **46** | +1 |
| `wp-sitemap-taxonomies-category-1.xml` | 14 | 14 | **14** | 0 |
| `wp-sitemap-taxonomies-post_tag-1.xml` | 613 | 619 | **626** | +13 |
| `wp-sitemap-users-1.xml` | 2 | 2 | **2** | 0 |
| **Total** | **1,641** | **1,649** | **1,658** | **+17** |

Archive share of the sitemap: 642 of 1,658, or **38.7%**. On 07-12 it was 37.7%. The direction is wrong and the drift is entirely tag growth: tags are the only class adding URLs, at roughly 4 per week, because new posts keep minting new single-use tags.

`/sitemap.xml` still returns `301` to `/wp-sitemap.xml` with `x-redirect-by: WordPress`. That handoff is intact and this proposal does not touch it.

`robots.txt` still points at `/sitemap.xml`, still disallows only `/wp-admin/`, `/?s=`, and `/search/`, and still has no taxonomy disallow. That is correct and this proposal does not touch it either.

### 2.2 The surface the sitemap does not show

WordPress paginates archives at **19 posts per page** on this install. Verified two ways: `/category/web-early-blog/` (344 posts) serves `page/19/` as `200` and `page/20/` as `404`; `/tag/misc/` (690 posts) serves `page/37/` as `200` and `page/38/` as `404`. Both match `ceil(count / 19)`.

Date archives are also live. `/2003/`, `/2003/10/`, `/2003/10/14/`, `/2026/07/`, and `/2026/07/31/` all return `200`. `/1999/` returns `404`, so the range is bounded by real content. Post URLs use `/YYYY/MM/DD/slug/`, and the 970 post URLs in the sitemap resolve to 21 distinct years, 114 distinct months, and 554 distinct days.

| Archive class | In sitemap | Crawlable, including pagination | Not in sitemap |
|---|---:|---:|---:|
| Category | 14 | 58 | 44 |
| Tag | 626 | 665 | 39 |
| Author | 2 | 51 | 49 |
| Date (year / month / day) | 0 | 755 | 755 |
| **Total archives** | **642** | **1,529** | **887** |

Author depth was measured by binary search on the pagination boundary: `/author/kk/` serves through `page/41/`, `/author/wpadmin5102/` through `page/10/`.

Date archive pagination was computed as `ceil(posts_in_period / 19)` from the sitemap's own date-partitioned post URLs, giving 64 year URLs, 137 month URLs, and 554 day URLs. That is a derived number, not a crawl of all 755. The three eras spot-checked (2003, 2006, 2026) all returned `200` with an indexable robots meta.

The takeaway: **more archive URLs are indexable outside the sitemap than inside it.** Removing archives from the sitemap without also setting `noindex` would leave 887 crawlable, indexable, canonical-free archive URLs and simply make them harder to see.

---

## 3. Sample method and results

### 3.1 Method

Deterministic and reproducible, not hand-picked:

- **Categories:** all 14 from `wp-sitemap-taxonomies-category-1.xml`, in sitemap order.
- **Tags:** every 63rd entry from `wp-sitemap-taxonomies-post_tag-1.xml` starting at index 0, giving 10 tags. With 626 entries and a fixed stride, this samples across the whole file rather than the top of it.
- **Authors:** both.
- **Control:** first, middle, and last post from the post sitemap; first, middle, and last page from the page sitemap. Six URLs. The control exists so that "archives have no canonical" is a comparison, not an assertion.
- **Crawler view:** first category, first sampled tag, first author, and one control post re-fetched with the Googlebot user agent.
- **Cache view:** first category, first sampled tag, and first author re-fetched with a `?cb=` query string to defeat the Jetpack Boost / Pagely edge cache.

For every response the probe captured HTTP status, redirect count, `link rel=canonical`, `meta name=robots`, any `X-Robots-Tag` header, `title`, `meta name=description`, `og:url`, `og:description`, and H1 count.

32 URL fetches in the main pass, 7 more in the crawler and cache passes.

### 3.2 Results

| Signal | Categories (14/14) | Tags (10/10) | Authors (2/2) | Control posts and pages (6/6) |
|---|---|---|---|---|
| HTTP status | 200 | 200 | 200 | 200 |
| Redirects | 0 | 0 | 0 | 0 |
| `rel=canonical` | **absent** | **absent** | **absent** | present, self-referential |
| `meta robots` | `max-image-preview:large` only | same | same | same |
| `X-Robots-Tag` header | absent | absent | absent | absent |
| `meta description` | **absent** | **absent** | **absent** | present |
| `og:url` | **`https://kriskrug.co/`** | **`https://kriskrug.co/`** | **`https://kriskrug.co/`** | self-referential |
| H1 count | 1 | 1 | 1 | 1 |
| H1 text | `Category: {name}` | `Tag: {name}` | `Author: {name}` | post or page title |

Uniform across every sampled URL. No exceptions, no partial coverage, no class that behaves differently from the others.

Three things in that table are worth stating plainly.

**The missing canonical is core behavior, not a regression.** WordPress core's `rel_canonical()` only fires on `is_singular()`. Archives have never had one and nothing in `theme/kk-aurora/`, `inc/`, or `plugins/` adds one (grepped for `rel_canonical`, `wp_robots`, and `wp_sitemaps`; the only hits are in `fixes/issue-331-archive-sitemap-policy.php`, which is not deployed). Nobody should spend time hunting for what broke it.

**`og:url` on every archive points at the homepage.** This is worse than "no canonical." It is a positive, machine-readable signal that a category page is the homepage. Social scrapers and some link-preview crawlers read `og:url` as a canonical substitute. The 07-26 pass noted that `og:description` falls back to the site tagline. The `og:url` fallback was not caught, and it is the sharper problem.

**The archive HTML is identical to Googlebot and to a cache-busted request.** No cloaking, no cache-layer variance. Whatever policy gets deployed, the readback will be honest.

### 3.3 Paginated and feed variants

`/category/web-early-blog/page/2/`, `/category/vancouver-ai-ecosystem/feed/`, and `/author/kk/page/2/` all return `200` with zero canonical links and the same permissive robots meta as page 1. Deep pagination behaves correctly at the boundary: past the last real page WordPress returns a proper `404`, not a soft 200. Verified at `/tag/misc/page/38/` and `/tag/misc/page/40/`.

The `?cb=` probe also proves an incidental risk. Because archives emit no canonical, any archive URL with a tracking parameter appended is a distinct indexable duplicate. Posts and pages are protected from this by their self-canonical. Archives are not.

---

## 4. Taxonomy shape as of today

Public REST, `hide_empty=true`.

### 4.1 Tags: 626 terms

- **502** have exactly one post
- **67** have two
- **29** have three
- **598 of 626, or 95.5%, have three posts or fewer**
- Only **9** have ten or more
- **626 of 626 have an empty term description**

Largest tags: `misc` (690 posts), `creativity` (55), `vancouver-ai` (20), `vancouver` (18), `ai` (15), `bc-ai` (15), `kris-krug` (14), `generative-ai` (11), `photography` (10).

`misc` covers 690 of 970 posts. It is a legacy dumping ground, not a topic hub, and it generates 37 paginated URLs on its own.

A tag page with one post is, structurally, a worse copy of that post: same title text, no description, no canonical, an H1 that reads `Tag: {slug}`, and one link out. There is no version of that page that outranks the post it points to, and no reason to want it to.

### 4.2 Categories: 14 terms

| Posts | Slug | Term description |
|---:|---|---|
| 344 | `web-early-blog` | empty |
| 158 | `photography-visual-storytelling` | empty |
| 118 | `vancouver-ai-ecosystem` | empty |
| 101 | `events-reports` | empty |
| 91 | `ai-creatives` | empty |
| 37 | `ai-ethics-philosophy` | empty |
| 35 | `field-notes` | empty |
| 29 | `conversations-interviews` | empty |
| 18 | `ai-for-journalism-media` | empty |
| 13 | `creative-technology-making` | empty |
| 11 | `generative-ai-tools` | empty |
| 8 | `keynotes-speaking` | empty |
| 5 | `indigenous-reconciliation-in-tech` | empty |
| 4 | `responsible-ai-policy` | empty |

Every category has posts. Every category has an empty description. Volume moved slightly since 07-26 (`vancouver-ai-ecosystem` 116 to 118, `ai-creatives` 90 to 91, `responsible-ai-policy` 3 to 4), which is normal publishing, not a signal.

Categories are the only archive class with a plausible case for staying indexable, because they are editorially chosen, they have real depth, and their names read like topics a human might search. But none of the 14 currently has a description, a meta description, a canonical, or an H1 that reads as anything other than a WordPress default. Right now they are indexable in name only.

### 4.3 Authors: 2

`/author/kk/` (Kris Krüg, roughly 780 posts, 41 pages) and `/author/wpadmin5102/` (display name "Krüg", roughly 180 posts, 10 pages).

This is a single-author site with two author URLs because of an admin account, and the second one is a near-duplicate of the first with a truncated display name. There is no world in which two author archives on a personal site are the answer to a search query. `/about/` is.

---

## 5. Proposed policy

Definitions used below:

- **Remove from sitemap:** drop from the WordPress core sitemap provider. The URL still returns 200 for humans.
- **`noindex,follow`:** robots meta only. No `Disallow`, no redirect, no deletion. Links on the page still pass equity to posts.
- **Keep:** in the sitemap and indexable, which requires a self-canonical, a unique title, a meta description, and a single meaningful H1.

### 5.1 Per class

| Class | Sitemap | Robots | Count affected |
|---|---|---|---:|
| Posts | keep, unchanged | unchanged | 970 |
| Pages | keep, unchanged | unchanged | 46 |
| Tag archives | remove | `noindex,follow` | 626 in sitemap, 665 crawlable |
| Author archives | remove | `noindex,follow` | 2 in sitemap, 51 crawlable |
| Date archives | already absent | `noindex,follow` | 0 in sitemap, 755 crawlable |
| Category archives | see 5.2 | see 5.2 | 14 in sitemap, 58 crawlable |
| Paginated archives (`/page/N/`) | already absent | inherits class policy | 132 beyond page 1 |
| `/sitemap.xml` handoff | unchanged | n/a | 1 |

**Tags: exclude, no allowlist.** 95.5% have three or fewer posts. The largest is a legacy catch-all. None has a description. The reasoning is not "tags are bad," it is that these specific 626 tags were never curated for search and there is no subset that clears the bar. If KK wants a curated tag hub later, the right move is to build it as a page with real copy, not to un-noindex an auto-generated term listing.

**Authors: exclude, both.** Single-author site, `/about/` already does this job with real copy and a canonical, and `wpadmin5102` is an artifact of the admin account.

**Dates: exclude.** This class is new to the analysis and it is the largest one. 755 crawlable URLs, zero in the sitemap, zero canonical, all indexable. A day archive with one post is the same structural problem as a one-post tag. Nobody links to `/2006/09/07/` on purpose and nobody searches for it. This is the single highest-volume fix in the whole proposal, and the currently-merged snippet does not cover it.

**Paginated archives need no separate rule.** `is_category()`, `is_tag()`, `is_author()`, and `is_date()` are all true on their `/page/N/` variants, so a `wp_robots` filter keyed on those conditionals covers pagination automatically. Worth stating explicitly so nobody adds a redundant `is_paged()` branch.

### 5.2 The category fork, unchanged from 07-26 and still KK's call

The issue's acceptance criteria assume some categories get retained. The evidence available does not identify which ones. Three options, and the cost differs a lot:

| | Sitemap | Robots | Work required |
|---|---|---|---|
| **A. Exclude all 14** | 0 categories | all `noindex,follow` | none beyond the snippet already written |
| **B. Curated keep-list** | named slugs only | keep-list indexable, rest `noindex,follow` | per-term: self-canonical, meta description, term description, an H1 that is not `Category: {name}`, plus an allowlist filter in the sitemap provider |
| **C. Keep all 14** | 14 | all indexable | the same per-term work, times 14, including for `web-early-blog` |

Option A is what the 07-12 receipt decided and what the merged snippet implements. It is also the only option that is honest about the current state: a category page with no description, no canonical, and a default H1 is not a page that deserves to be indexed, so leaving it in the sitemap is a claim the page cannot back up.

Option B is the better long-term answer **if** someone does the copy work. The candidates worth arguing for, on editorial grounds and not on evidence: `vancouver-ai-ecosystem`, `ai-creatives`, `keynotes-speaking`, `ai-ethics-philosophy`. Those four match what KK actually does and what people actually ask him about. `web-early-blog` and `photography-visual-storytelling` should not be kept on volume alone; they are archive buckets, not topics.

Option C is not recommended. It commits to writing and maintaining 14 sets of archive copy for terms including a 344-post legacy bucket.

**Recommendation: A now, B later as a deliberate content project with its own issue.** Shipping A does not foreclose B. Un-noindexing a category later is a one-line allowlist change plus the copy work.

### 5.3 The forward-going rule

The tag count grows about 4 per week because publishing mints new single-use tags. A one-time cleanup that does not change the rule will be back to 626 within three years. The rule:

1. **A URL belongs in the sitemap only if it is indexable, and it is indexable only if it has a self-canonical, a unique title, and a description.** No exceptions by URL class. This is the whole policy in one sentence.
2. **Auto-generated listing pages are `noindex,follow` by default.** Tags, authors, dates, and paginated variants qualify. They stay publicly reachable and they stay linked.
3. **Promoting an archive out of `noindex` is a content decision, not a config decision.** It requires the copy to exist first and a named person to own it.
4. **New taxonomy terms inherit the class default automatically.** Because the policy is a `wp_robots` conditional and not a per-term list, a tag created next year is already `noindex` on creation. Nothing to maintain.
5. **`/sitemap.xml` keeps its 301 to `/wp-sitemap.xml`.** Do not add a second sitemap source.

---

## 6. Implementation path

### 6.1 Which lever

| Lever | Verdict | Why |
|---|---|---|
| **Code Snippets plus core `wp_sitemaps_*` and `wp_robots` filters** | **use this** | Core owns the sitemap providers and the robots meta, so core filters are the direct control. Matches the existing ops pattern on this site (snippets 5, 7, 8, 13). Reversible by deactivating one snippet. Testable in-repo. The snippet is already written and merged. |
| Theme PHP in `kk-aurora` | no | Couples a Track A SEO policy to a Track B theme release. Rollback becomes a theme redeploy instead of a checkbox. |
| Jetpack SEO settings | no | Jetpack does not own core sitemap providers. Its archive noindex coverage does not reach date archives or the sitemap membership question, and it cannot be unit-tested from this repo. |
| Yoast or Rank Math | no | Not installed. Yoast sitemap paths return 404, confirming absence. Installing an SEO plugin to solve a 30-line filter problem adds an ownership conflict with Jetpack and the theme. |
| `robots.txt` `Disallow` | no | Wrong tool. Disallow blocks crawling, which prevents Google from ever seeing the `noindex`, and it strands URLs that are still linked on-site. It also contradicts the deliberate AI-crawler-friendly stance in `fixes/robots.txt`. |

### 6.2 What the existing snippet covers and what it misses

`fixes/issue-331-archive-sitemap-policy.php` (merged in PR #334, not deployed) does three things:

1. `wp_sitemaps_add_provider` returns `false` for `users`
2. `wp_sitemaps_taxonomies` unsets `category` and `post_tag`
3. `wp_robots` sets `noindex,follow` on `is_author() || is_tag() || is_category()`, preserving unrelated directives

That is correct as far as it goes, and it matches Option A. Two gaps, both found by this pass:

- **`is_date()` is missing from the robots conditional.** 755 crawlable date archive URLs stay indexable after deploy. This is the largest single class in the whole inventory and fixing it is one added conditional.
- **The snippet does not add a self-canonical to anything.** That is fine under Option A, because everything it touches becomes `noindex`. It becomes a required addition under Option B or C, and it is the reason B is more work than it looks.

Neither gap is a reason to hold the deploy. Adding `is_date()` is a small, testable change to a file this lane does not own.

### 6.3 Files this proposal implies, none of which this lane touched

Flagged here rather than edited, per lane ownership:

- `fixes/issue-331-archive-sitemap-policy.php`: add `is_date()` to `kk_archive_policy_robots()`
- `scripts/tests/test_issue_331_archive_policy.py`: add a date-archive case to the robots harness
- `docs/current-state/SEO-INDEXING-RUNBOOK.md`: record the standing rule from section 5.3

### 6.4 Deploy sequence, human-gated, not this lane

1. KK picks the category fork (A, B, or C) and confirms the empty tag allowlist.
2. Add `is_date()` to the snippet, extend the test, run `make python-test` and `make validate`.
3. Re-count the live sitemap children immediately before deploy. Do not hard-code any total from this document. The count moves every week.
4. Snapshot the live Code Snippets inventory and the current sitemap index XML.
5. Create the snippet **inactive**, diff the saved body against the repo file, PHP lint.
6. Activate, then purge the approved Pagely and Jetpack Boost cache.
7. Readback, in section 7.
8. Rollback if any check fails: deactivate, purge, re-read.

---

## 7. Readback gate for whoever deploys

Record all of it. Do not call the change done without it.

1. `/sitemap.xml` still `301` to `/wp-sitemap.xml`.
2. The sitemap index contains the post and page children and no `taxonomies-category`, `taxonomies-post_tag`, or `users` child. Under Option B or C the category child stays and its contents are exactly the allowlist.
3. A full crawl of the remaining children matches the post and page counts taken in step 3 of the deploy sequence, with no redirect or deletion mixed in.
4. Representative category, tag, author, **and date** archives return `200`, do not redirect, and emit exactly one robots meta containing `noindex,follow`, under a normal request, a Googlebot user agent, and a cache-busted request. Include at least one `/page/2/` variant, because pagination coverage is an inherited behavior and inherited behavior is what breaks quietly.
5. Representative posts and pages still return `200`, still carry a self-canonical, and still appear in their sitemap provider.
6. Search Console sitemap status read at 24 hours and 72 hours, without resubmitting in between. Record the reported indexed count as reported. The API's indexed number is unreliable at low volumes and a zero there is not proof of anything.

---

## 8. The open question, and what would settle it

**Everything above about tags, authors, and dates is an argument from page structure, not from demand.** The structural case is strong: a page with one outbound link, no description, and no canonical cannot serve a query better than the post it links to. But "cannot serve a query well" is not the same measurement as "does not currently receive queries," and only Search Console has the second one.

What exists today is the 2026-07-12 Growth Mirror rehearsal recorded in `reports/issue-331-archive-policy-20260712.md`: across two 28-day windows, author archives drew 2 and 4 impressions, tag archives 4 and 2, and the only category rows were `/category/.../feed/` URLs rather than landing pages. Sixteen impressions and zero clicks in total.

That is a real number and it points the same direction as the structural argument. It is also **three weeks stale, it was a rehearsal rather than a standing report, and it cannot be refreshed from this lane** because no Search Console credential is available here and this lane is repo-only by instruction.

More honestly still: sixteen impressions across 642 archive URLs is close to the noise floor. It is consistent with "these pages have no demand." It is also consistent with "these pages are barely indexed, so of course they show no impressions." Those two readings have the same evidence and different implications, and no amount of `curl` distinguishes them.

**What would settle it.** One authenticated Search Console Search Analytics query, dimension `page`, last 90 days, no row limit, filtered to URLs containing `/category/`, `/tag/`, `/author/`, and the `/YYYY/` date pattern. Then:

- Any archive URL with **zero clicks and fewer than 10 impressions over 90 days**: exclude, no argument.
- Any archive URL with **clicks**: stop and look at it before excluding. Find out which query it wins and whether a post or page could win that query instead. If yes, exclude the archive and improve the post. If no, that URL is a legitimate keep and it needs the full canonical, title, description, and H1 treatment from section 5.2.
- Any archive URL with **impressions but no clicks**: this is the ambiguous band. Check the average position. Ranking at position 40 with impressions means Google found it and buried it, which argues for exclusion. Ranking at position 8 with no clicks means the title and description are failing, which argues for fixing the page or for accepting that the query belongs to a post instead.

That one query is the difference between a defensible policy and a confident guess. It is also the only acceptance criterion on #331 that this lane cannot satisfy.

**Second open question, smaller.** Nothing here checked whether the 887 archive URLs that are indexable but absent from the sitemap are actually in Google's index. Sitemap absence is not index absence. A `site:` operator sample, or better, the Search Console index coverage report, would show whether the date archives are already indexed and competing. If they are, the `is_date()` addition moves from "good hygiene" to "the most valuable single line in this change."

---

## 9. What this proposal explicitly does not do

- Delete any post, page, term, media item, or user
- Redirect any archive URL
- Change any permalink structure
- Add any `Disallow` to `robots.txt`
- Change the `/sitemap.xml` handoff
- Request indexing, submit a sitemap, or use temporary URL removals in Search Console
- Rewrite archive copy without editorial review
- Deploy, activate, or purge anything

---

## 10. Reproducing the measurements

Every number in this document came from these, on 2026-08-02:

```
curl -sS https://kriskrug.co/wp-sitemap.xml
curl -sS https://kriskrug.co/wp-sitemap-posts-post-1.xml
curl -sS https://kriskrug.co/wp-sitemap-posts-page-1.xml
curl -sS https://kriskrug.co/wp-sitemap-taxonomies-category-1.xml
curl -sS https://kriskrug.co/wp-sitemap-taxonomies-post_tag-1.xml
curl -sS https://kriskrug.co/wp-sitemap-users-1.xml
curl -sSI https://kriskrug.co/sitemap.xml
curl -sS https://kriskrug.co/robots.txt
curl -sS 'https://kriskrug.co/wp-json/wp/v2/tags?per_page=100&page=N&hide_empty=true&_fields=id,slug,count,description'
curl -sS 'https://kriskrug.co/wp-json/wp/v2/categories?per_page=100&hide_empty=true&_fields=id,slug,count,description'
curl -sS 'https://kriskrug.co/wp-json/wp/v2/users?per_page=100&_fields=id,slug,name'
```

Archive HTML probes used `curl -sS -D - -o -` against each sampled URL, with `-A` for the Googlebot pass and a `?cb=` suffix for the cache-busted pass. Pagination boundaries were found by binary search on `%{http_code}` over `/page/N/`. Posts-per-page was confirmed at 19 by matching `ceil(count / 19)` against the observed last-200 page for two independent terms.

---

## 11. Related

- Issue [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331)
- `docs/current-state/reports/issue-331-archive-policy-20260712.md`, the 07-12 decision and Growth Mirror evidence
- `docs/current-state/reports/taxonomy-sitemap-plan-331-20260726.md`, the 07-26 lever comparison and category fork
- `fixes/issue-331-archive-sitemap-policy.php`, merged in PR #334, not deployed
- `scripts/tests/test_issue_331_archive_policy.py`
- `docs/current-state/SEO-INDEXING-RUNBOOK.md`
- `docs/current-state/reports/gsc-sitemap-checklist-274-20260726.md` (#274)
