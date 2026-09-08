# Issue #274: sitemap follow-through after #331 (dated verification receipt)

**Captured:** 2026-09-08T06:03Z–06:10Z (UTC)
**Mode:** Track A, read-only. Public HTTP/XML/HTML only. Zero WordPress writes. Zero cache purges. Zero Search Console submits, removals, resubmits, indexing requests, or Validate Fix.
**Refs:** [#274](https://github.com/WalksWithASwagger/kriskrug-wp/issues/274) (this receipt). Cross-link only: [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331) deployed archive policy ([receipt](DEPLOY-767-331-2026-09-03.md), snippet 26). Do not start #994 / #995 / #996 / #997 / #402 / #339 from this file.
**Property (dated, not re-read):** `sc-domain:kriskrug.co`
**Submitted URL (dated, not re-read):** `https://kriskrug.co/sitemap.xml`

Success for this issue is a reviewable public receipt plus a precise GSC wait. It is **not** closeout. Closeout still needs a post-deploy Google last-read.

---

## Verdict

Public discovery after the 2026-09-03 #331 v2 deploy is healthy and consistent.

| Check | 2026-09-08 observation |
|---|---|
| `robots.txt` Sitemap: | only `https://kriskrug.co/sitemap.xml` |
| `/sitemap.xml` handoff | **301** → `https://kriskrug.co/wp-sitemap.xml` (`x-redirect-by: WordPress`). Intentional. Do not "fix." |
| Core index children | **2**: posts + pages. No category / tag / users children |
| Normal vs cache-busted index | **identical** children and SHA-256 |
| Live inventory | **975 posts + 46 pages = 1,021** unique URLs |
| Retained-URL crawl (this session) | **1,021 / 1,021** direct 200, exact self-canonical, description present, zero robots/googlebot-meta or `X-Robots-Tag` noindex |
| Archive robots | category / tag / author / date still `noindex, follow`. Approved exclusions preserved |
| Primary robots | home, `/about/`, `/blog/`, `/work/`, `/contact/`, and sampled posts still indexable (`max-image-preview:large` only) |
| GSC last-read / status / counts | **external-wait / blocker.** Not readable in this session. Not a public failure |

Do **not** resubmit the sitemap because Google's discovered count still lags. Do **not** close #274 from this PR.

---

## 1. Session snapshot

| Signal | Observation | Source |
|---|---|---|
| Observation window | 2026-09-08T06:03:52Z–06:09:49Z | this session |
| `make doctor` | **FAIL** (expected here): WP credentials unresolved; `scripts/notion-to-wp/.venv` missing; Varlock not on PATH. `gh` authenticated. Live `style.css` reachable | local |
| `make status-readonly` | WP smoke 0 failures / 0 warnings. WordPress `7.0.4`. Aurora live and repo `main` **1.6.11**. Draft-queue counts unavailable (no WP creds). Open issues 49 / open PRs 5 vs the 2026-07-30 declared snapshot | local + public |
| Live `style.css` Version | `1.6.11` | `GET https://kriskrug.co/wp-content/themes/kk-aurora/style.css` |
| `make seo-publisher-smoke` | **PASS**: `/wp-sitemap.xml` 200, `/feed/` 200, `/news-sitemap.xml` 200; three recent posts emit `BlogPosting` with required fields | public |
| News sitemap | 200, 169 bytes, **0** `<loc>` (empty urlset; trailing-slash final URL). Not advertised in `robots.txt`. Do not submit | public |
| #331 deploy | 2026-09-03, snippet 26 (`fixes/issue-331-archive-sitemap-policy-v2.php`) | [DEPLOY-767-331-2026-09-03.md](DEPLOY-767-331-2026-09-03.md) |

Public state wins over dated docs. The 2026-07-26 checklist still expected ~1.6k submitted URLs and five index children; that is **pre-#331**. Live index is posts + pages only.

---

## 2. Public sitemap index and child counts

Refreshed 2026-09-08T06:04:24Z. `GET` each discovered child, then the same children with `?cb=1788847464`.

### 2a. Index

| Request | HTTP | Cache | Children | SHA-256 |
|---|---:|---|---:|---|
| `GET /wp-sitemap.xml` | 200 | HIT | 2 | `14043769ac93b6416aadaae99084a525aa7cded0099a0978e948a8f3c3d74edd` |
| `GET /wp-sitemap.xml?cb=1788847464` | 200 | MISS | 2 | same |
| `GET /sitemap.xml` (follow) | 200 at `/wp-sitemap.xml` | HIT | 2 | same |

Children, both copies:

1. `https://kriskrug.co/wp-sitemap-posts-post-1.xml`
2. `https://kriskrug.co/wp-sitemap-posts-page-1.xml`

No `taxonomies-category`, `taxonomies-post_tag`, or `users` child. That matches the #331 v2 deploy target (five children → two). The 2026-09-03 receipt still warned that a **bare** index might serve a stale five-child copy from Pagely ARES. On 2026-09-08 the bare HIT and the cache-busted MISS are the same two-child document. The stale five-child edge copy is gone.

### 2b. Child counts

| Child | HTTP | Cache | URLs | Cache-busted URLs | SHA match |
|---|---:|---|---:|---:|---|
| `wp-sitemap-posts-post-1.xml` | 200 | HIT | **975** | 975 (MISS) | yes |
| `wp-sitemap-posts-page-1.xml` | 200 | HIT | **46** | 46 (MISS) | yes |
| **Total unique** | | | **1,021** | **1,021** | |

Newest post loc: `https://kriskrug.co/2026/09/07/ai-already-campaign-issue-vancouver/` (`lastmod` `2026-09-07T11:51:46-08:00`). That URL is the documented +1 versus the September 6 inventory of 974 posts.

Page locs still start at `/about/`, `/speaking/`, `/publications/` and still end at `/ai-tools/`, `/indigenous-ai/`, `/sponsor-deck/`.

### 2c. Side / leftover paths (not in the index)

| URL | HTTP | Notes |
|---|---:|---|
| `/wp-sitemap-taxonomies-category-1.xml` | 404 | removed from the index; URL itself 404s |
| `/wp-sitemap-taxonomies-post_tag-1.xml` | 404 | same |
| `/wp-sitemap-users-1.xml` | 200 **HTML** | not XML; 0 `<loc>`. Title `Kris Krüg`, homepage H1. Canonical `https://kriskrug.co/wp-sitemap-users-1.xml/`. Robots `max-image-preview:large` (indexable). **Not in the submitted index.** Out of scope to change. Duplicate-content recovery is #402 / #997, not this receipt |
| `/sitemap_index.xml` | 404 | do not submit |
| `/sitemap-1.xml` | 404 | obsolete row already removed in GSC on 2026-07-12 (dated comment) |
| `/news-sitemap.xml` | 200 | empty urlset; not in `robots.txt`; do not submit |

---

## 3. robots.txt and `/sitemap.xml` handoff

`GET https://kriskrug.co/robots.txt` → 200. One sitemap declaration:

```text
Sitemap: https://kriskrug.co/sitemap.xml
```

Disallows (repeated once under `User-agent: *` and once under the AI-crawler group): `/wp-admin/` (with `Allow: /wp-admin/admin-ajax.php`), `/?s=`, `/search/`. Source comment still `fixes/robots.txt`, last reviewed 2026-06-07.

Required header probe, `curl -sSI https://kriskrug.co/sitemap.xml` at 2026-09-08T06:04:42Z:

| Field | Value |
|---|---|
| Status | `HTTP/2 301` |
| `location` | `https://kriskrug.co/wp-sitemap.xml` |
| `x-redirect-by` | `WordPress` |
| `x-gateway-cache-status` | `BYPASS` |
| `x-gateway-skip-cache` | `1` |

Followed GET returns the same two-child index as a direct `/wp-sitemap.xml` GET. Do not change `robots.txt` merely to remove this handoff.

---

## 4. Representative primary vs archive robots

HTML `robots` meta, not headers. `wp_robots` still emits a meta tag. No `X-Robots-Tag` on these rows. Captured 2026-09-08T06:04:58Z.

| Class | URL | HTTP | robots | Canonical | Keep? |
|---|---|---:|---|---|---|
| Home | `/` | 200 | `max-image-preview:large` | self | yes, indexable |
| Page | `/about/` | 200 | same | self | yes |
| Page | `/blog/` | 200 | same | self | yes |
| Page | `/work/` | 200 | same | self | yes |
| Page | `/contact/` | 200 | same | self | yes |
| New post | `/2026/09/07/ai-already-campaign-issue-vancouver/` | 200 | same | self | yes |
| Sep 3 post | `/2026/09/03/what-i-showed-founders-about-ai-workflows/` | 200 | same | self | yes |
| #996 named primary | `/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` | 200 | same | self | yes; recovery belongs to #996 |
| Category | `/category/ai-ethics-philosophy/` | 200 | `max-image-preview:large, noindex, follow` | none | **approved #331** |
| Tag | `/tag/sxsw-sxswi/` | 200 | same noindex,follow | none | **approved #331** |
| Tag | `/tag/ai/` | 200 | same | none | **approved #331** |
| Author | `/author/kk/` | 200 | same | none | **approved #331** |
| Date | `/2026/08/` | 200 | same | none | **approved #331** |
| Share variant | same photography URL + `?share=twitter` | 301 → 200 | indexable on the clean permalink | parent article | intentional canonicalize; do not index the variant |
| Login | `/wp-login.php` | 200 | `max-image-preview:large, noindex, noarchive` | none | intentional |
| Embed | `…/embed/` | 200 | `noindex, follow, max-image-preview:large` | parent article | intentional |
| Search | `/?s=photography` | 200 | `noindex, follow, max-image-preview:large` | none | intentional; also disallowed in `robots.txt` |

`follow` is present on every archive row. Primaries were not noindexed by #331. Approved exclusions stay.

---

## 5. Live versus Google (GSC)

### 5a. Precise blocker for this session

I could not read the submitted-sitemap report.

| Needed | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, or Search Console names. `.env.schema` does not define a GSC secret |
| Signed-in GSC UI | **Not available** |
| Site Kit Search Console REST | **Not available.** WP credentials unset (`WP_USER` / `WP_APP_PASSWORD` and `WP_API_*`). Site Kit chrome is visible in public HTML (`1.186.0` in the 2026-09-08 #994 receipt); that is not a sitemap last-read |
| Committed post-deploy GSC export | **Absent** from the repo |

Missing GSC fields (do not invent):

| Field | This session |
|---|---|
| Property confirmation from a live UI/API read | **missing** |
| Submitted sitemap row last-read date | **missing** |
| Status (`Success` / `Couldn't fetch` / other) | **missing** |
| Discovered pages | **missing** |
| Discovered videos | **missing** |
| Child-level inventory Google currently lists | **missing** |
| Fetch-error detail | **missing** |
| Indexed totals / coverage deltas | **missing** (and out of scope to scrape from Performance) |

This is an **external-wait / blocker**, not a public-check failure.

### 5b. Dated GSC evidence that already exists (not re-measured)

Copied from issue #274's September 6, 2026 refresh. Treat as a snapshot, not as this session's read.

| Item | Dated claim | This session |
|---|---|---|
| Property | `sc-domain:kriskrug.co` | not re-read |
| Submitted URL | `https://kriskrug.co/sitemap.xml` | public handoff re-verified; GSC row not re-read |
| Status | Success | not re-read |
| Last read | **September 2, 2026** (pre-#331 deploy on September 3) | not re-read |
| Discovered pages in the observed UI | 1,666 | not re-read. Live inventory is now **1,021**. The gap is expected until Google re-reads and drops archive URLs |
| Submission already exists | yes; do not recreate | held |

Earlier dated comments remain historical records, not instructions to repeat the clicks: Jul 2 Success after submit; Jul 12 last-read Jul 2 / 1,637 pages and obsolete `/sitemap-1.xml` removed; Jul 16 `/indigenous-ai/` inspection; Aug 28 signed-out queue audit.

### 5c. Live-versus-Google comparison (what can be said without inventing)

| Inventory | Count | What it is |
|---|---:|---|
| Live submitted sitemap (this session) | **1,021** | posts + pages only |
| Sep 6 retained crawl (issue body) | **1,020** | 974 + 46; see §7 |
| #331 deploy expected | **1,019** | 973 + 46 on 2026-09-03 |
| Last GSC discovered (Sep 6 UI, last read Sep 2) | **1,666** | pre-deploy Google inventory. Includes archives Google had already discovered |

A reduced Google discovered count after the next post-deploy read is **expected**. It is not traffic loss by itself. Indexed totals were not available here and are not invented.

### 5d. Next manual GSC check (closeout criterion)

KK, in a signed-in session, open the [submitted sitemap report](https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Akriskrug.co) for `sc-domain:kriskrug.co`. Record, without resubmitting:

1. Observation timestamp (real clock, not backdated).
2. Property id.
3. Canonical row URL (`https://kriskrug.co/sitemap.xml`).
4. **Last read** date.
5. **Status**.
6. Discovered pages (and videos if shown).
7. Child-level list if the UI still expands one.
8. Any fetch error text.

**Close #274 only when** last-read is **after 2026-09-03**, status is Success with **no fetch error**, and the discovered count is explained against live **1,021** (allow the documented Sep 7 publication and ordinary reporting lag). If last-read is still September 2 or any pre-deploy date, keep waiting. Do not resubmit, delete rows, or request mass indexing to satisfy the old checklist.

---

## 6. Noindex classification (issue body + public re-check)

September 6 issue text classified **964** noindex examples: **901** share variants, **46** login URLs, **6** embeds, **11** tag archives, **zero** primary article or landing-page URLs. New tag examples fit the approved policy. Old share classifications do not prove current noindex on the original articles.

This session did **not** re-fetch a GSC example export (none is in the repo; GSC is blocked). Public class representatives in §4 still match that grouping:

| Class | Public 2026-09-08 | Disposition |
|---|---|---|
| Primary posts / pages | 1,021 sitemap URLs; sampled and then fully crawled, all indexable | retain |
| Tag / category / author / date archives | noindex,follow; absent from the sitemap | **keep** (#331) |
| Share variants | 301 to the clean permalink | **keep** canonicalize |
| Login | noindex,noarchive | **keep** |
| Embeds | noindex,follow; canonical to the parent | **keep** |
| Search | noindex,follow + robots.txt Disallow | **keep** |

Do not remove intentional noindex. Duplicate-content recovery and article growth stay with #996 / #402 / #997.

---

## 7. Retained-crawl receipt

### 7a. September 6 complete crawl (reused with provenance)

**Provenance:** issue #274 body, refreshed 2026-09-06. Raw GET logs are **not** in this repo (no committed or uncommitted local report in this session). The issue text is the dated receipt:

- 974 posts + 46 pages = **1,020**
- all direct 200
- all exact self-canonicals and descriptions
- zero robots / googlebot-meta or `X-Robots-Tag` noindex

Counts are a dated baseline, not an immutable acceptance value.

### 7b. Why this session recrawled

Two reasons the issue allows a bounded-concurrency full crawl:

1. Raw Sep 6 evidence is unavailable here; the issue says reproduce checks if the uncommitted report is missing.
2. Live inventory **changed**: 974 → **975** posts. The new URL is `/2026/09/07/ai-already-campaign-issue-vancouver/` (`lastmod` 2026-09-07T11:51:46-08:00), after the Sep 6 crawl.

Same-day independent public count in [issue-996-unindexed-primary-triage-20260908.md](issue-996-unindexed-primary-triage-20260908.md): 975 + 46. That file was not edited.

### 7c. 2026-09-08 bounded crawl

| Field | Value |
|---|---|
| Start | 2026-09-08T06:05:31Z |
| Finish | 2026-09-08T06:09:49Z |
| Elapsed | 258 s |
| Concurrency | 4 |
| Population | every `<loc>` from the two live child sitemaps (1,021 unique) |
| Method | direct GET, no redirect follow; fail on any hop, noindex, missing/mismatched canonical, missing description, googlebot meta, or `X-Robots-Tag` noindex |
| Result | **1,021 ok / 0 fail** |
| Status | 200 × 1,021 |
| noindex | 0 |
| not self-canonical | 0 |
| missing description | 0 |
| googlebot meta | 0 |
| `X-Robots-Tag` present | 0 |

The Sep 7 post is in the 1,021 and passed the same checks as the Sep 6 population.

---

## 8. Original 24h / 72h checkpoints

Never backdated. No observation in this session is labeled as a July or September T+24h / T+72h read.

| Planned checkpoint | Evidence in repo / issue | This receipt |
|---|---|---|
| Original July submit-monitor T+24h (checklist 2026-07-26) | No committed file or comment titled as that checkpoint | **missed / unavailable** |
| Original July submit-monitor T+72h | Same. Dated Jul 2 / Jul 12 / Jul 16 GSC comments exist; they are not a completed 24h/72h packet | **missed / unavailable** as labeled checkpoints |
| Post-#331 T+24h (calendar 2026-09-04) | None | **missed / unavailable** |
| Post-#331 ~T+72h (calendar 2026-09-06) | Issue #274 body records a Sep 6 public + GSC audit. Last Google read in that text is still **September 2** | dated issue text only; **not** this session; **not** a post-deploy Google read |
| This session (2026-09-08T06:03Z) | Public matrix, robots, 1,021-URL crawl | establishes live inventory and policy; **does not** establish Google's last-read |

Suggested July 29–August 2 coverage window from the old checklist also has **no** committed 24h/72h packet.

---

## 9. Acceptance criteria status

| #274 criterion | Status |
|---|---|
| Existing sitemap submission observed as Success on September 6; do not recreate | **Met** by dated issue text. Not re-clicked |
| Post-deploy retained crawl September 6: 1,020 primaries passed | **Met** by dated issue text (provenance §7a) |
| Refresh public index + child counts; robots.txt; `/sitemap.xml` handoff; normal vs cache-bust; representative robots; preserve exclusions | **Met** this session (§2–§4) |
| Inspect GSC last-read / status / child inventory; say whether Google read after September 3 | **Blocked.** Last dated read remains September 2. This session cannot refresh |
| Record original 24h/72h as missed/unavailable if no evidence; never backdate | **Met** (§8) |
| Deliver this dated report, cross-referenced to #331, with live-versus-Google, noindex classification, retained-crawl receipt | **Met** by this file |
| If Google's read remains pre-deploy, finish public evidence and return external-wait + next manual check; do not close or resubmit | **Met** (§5). Draft PR uses `Refs #274`, not `Closes` |
| Final closeout: post-deploy GSC read, no fetch error, explained inventory | **Not met.** External wait |

---

## 10. Out of scope (held)

No repeated submission. No mass or manual indexing requests. No deleting old GSC rows. No temporary removals. No archive-policy edit. No `robots.txt` edit to remove the 301 handoff. No #996 recovery writes. No #402 growth. No edits to #994 / #995 / #996 / #997 / #402 / #339 proposal files.

The leftover `/wp-sitemap-users-1.xml` HTML 200 is recorded, not fixed.

---

## 11. What KK does next

1. Review this receipt. Public half is done.
2. When convenient, open the GSC sitemaps report and write last-read / status / counts onto #274 (or a short follow-up receipt). Use a real timestamp.
3. Close #274 only after §5d. If last-read is still pre-2026-09-03, leave it open and wait.
4. Do not purge, deploy, or resubmit from this lane.
