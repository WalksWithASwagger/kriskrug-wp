# Issue #274: sitemap follow-through after #331 (dated verification receipt)

**Captured:** 2026-09-21T00:39:34Z–00:40:16Z (UTC)
**Mode:** Track A, read-only. Public HTTP/XML/HTML only. Zero WordPress writes. Zero cache purges. Zero Search Console submits, removals, resubmits, indexing requests, or Validate Fix.
**Refs:** [#274](https://github.com/WalksWithASwagger/kriskrug-wp/issues/274) (this receipt). Cross-link only: [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331) deployed archive policy ([receipt](DEPLOY-767-331-2026-09-03.md), snippet 26). Prior public receipt: [issue-274-sitemap-followthrough-20260908.md](issue-274-sitemap-followthrough-20260908.md). Do not start #994 / #995 / #996 / #997 / #402 / #339 / #1025 from this file.
**Property (dated, not re-read):** `sc-domain:kriskrug.co`
**Submitted URL (dated, not re-read):** `https://kriskrug.co/sitemap.xml`
**Repro:** `make sitemap-followthrough` → `scripts/sitemap_followthrough.py` (public dry-run; never calls GSC)

Success for this issue is a reviewable public receipt plus a precise GSC wait. It is **not** closeout. Closeout still needs a post-deploy Google last-read. This PR uses **Refs #274**, not `Closes #274`.

---

## Verdict

Public discovery after the 2026-09-03 #331 v2 deploy is still healthy. Live inventory grew by four ALL IN Montreal posts since the 2026-09-08 receipt.

| Check | 2026-09-21 observation |
|---|---|
| `robots.txt` Sitemap: | only `https://kriskrug.co/sitemap.xml` |
| `/sitemap.xml` handoff | **301** → `https://kriskrug.co/wp-sitemap.xml` (`x-redirect-by: WordPress`). Intentional. Do not "fix." |
| Core index children | **2**: posts + pages. No category / tag / users children |
| Normal vs cache-busted index | **identical** children and SHA-256 |
| Live inventory | **979 posts + 46 pages = 1,025** unique URLs |
| New primaries since 2026-09-08 | **4 / 4** direct 200, exact self-canonical, description present, indexable robots |
| Sep 8 retained crawl (1,021 URLs) | reused with provenance; inventory change did not warrant a second 1,025-URL GET sweep |
| Archive robots | category / tag / author / date still `noindex, follow`. Approved exclusions preserved |
| Primary robots | home, `/about/`, `/blog/`, `/work/`, `/contact/`, sampled posts still indexable (`max-image-preview:large` only) |
| GSC last-read / status / counts | **external-wait / blocker.** Not readable in this session. Not a public failure |

**Do not resubmit** the sitemap because Google's discovered count still lags. Do **not** close #274 from this PR.

---

## 1. Session snapshot

| Signal | Observation | Source |
|---|---|---|
| Observation window | 2026-09-21T00:39:34Z–00:40:16Z | this session |
| `make doctor` | **FAIL** (expected here): WP credentials unresolved; `scripts/notion-to-wp/.venv` missing; Varlock not on PATH. `gh` authenticated. Live `style.css` reachable | local |
| `make status-readonly` | Public WP7 smoke degraded only because the Makefile still expects WordPress `7.0.4` and live is `7.0.5`. Aurora live and repo `main` both **1.6.12**. Draft-queue counts unavailable (no WP creds). Open issues 57 vs the 2026-07-30 declared snapshot | local + public |
| Live `style.css` Version | `1.6.12` | `make status-readonly` / `check-live-parity` |
| `make seo-publisher-smoke` | **PASS**: `/wp-sitemap.xml` 200, `/feed/` 200, `/news-sitemap.xml` 200; three recent posts emit `BlogPosting` with required fields | public |
| News sitemap | 301 → `/news-sitemap.xml/` then 200, 169 bytes, **0** `<loc>` (empty urlset). Not advertised in `robots.txt`. Do not submit | public |
| #331 deploy | 2026-09-03, snippet 26 (`fixes/issue-331-archive-sitemap-policy-v2.php`) | [DEPLOY-767-331-2026-09-03.md](DEPLOY-767-331-2026-09-03.md) |
| GSC / WP admin creds | **Absent.** `WP_USER` / `WP_APP_PASSWORD` / `WP_API_*` unset. No `GOOGLE_APPLICATION_CREDENTIALS` or other GSC names. `.env.schema` still does not define a GSC secret | this session |

Public state wins over dated docs. The 2026-07-26 checklist still expected ~1.6k submitted URLs and five index children; that is **pre-#331**.

---

## 2. Public sitemap index and child counts

Refreshed 2026-09-21T00:39:35Z. `GET` each discovered child, then the same children with `?cb=1789951216`.

### 2a. Index

| Request | HTTP | Cache | Children | SHA-256 |
|---|---:|---|---:|---|
| `GET /wp-sitemap.xml` | 200 | MISS | 2 | `14043769ac93b6416aadaae99084a525aa7cded0099a0978e948a8f3c3d74edd` |
| `GET /wp-sitemap.xml?cb=1789951174` | 200 | MISS | 2 | same |
| `GET /sitemap.xml` (follow) | 200 at `/wp-sitemap.xml` | — | 2 | same |

Children, both copies:

1. `https://kriskrug.co/wp-sitemap-posts-post-1.xml`
2. `https://kriskrug.co/wp-sitemap-posts-page-1.xml`

No `taxonomies-category`, `taxonomies-post_tag`, or `users` child. That still matches the #331 v2 deploy target. The 2026-09-03 receipt warned that a **bare** index might serve a stale five-child copy from Pagely ARES. On 2026-09-08 and again today the bare and cache-busted documents are the same two-child index (same SHA as 2026-09-08). The stale five-child edge copy remains gone.

### 2b. Child counts

| Child | HTTP | Cache | URLs | Cache-busted URLs | SHA match |
|---|---:|---|---:|---:|---|
| `wp-sitemap-posts-post-1.xml` | 200 | MISS | **979** | 979 (MISS) | yes (`8a61094c171e9f4eede61a9a36e46ec1b140a37dc47b136204c6c56be4d4b50b`) |
| `wp-sitemap-posts-page-1.xml` | 200 | MISS | **46** | 46 (MISS) | yes (`86852fc122a415e42e7f0d14e53b8d887eebf0c8af877d436f50bea966f6a596`) |
| **Total unique** | | | **1,025** | **1,025** | |

Newest post loc: `https://kriskrug.co/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/`. Newest `lastmod` on the posts child is `2026-09-18T20:46:51-08:00` on `/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/`.

Page locs still start at `/about/` and still end at `/sponsor-deck/`. `/work/` carries `lastmod` `2026-09-20T10:05:25-08:00`.

Delta versus 2026-09-08 (975 + 46 = 1,021): **+4 posts**, pages unchanged.

| New since 2026-09-08 | `lastmod` |
|---|---|
| `/2026/09/15/headed-east-for-all-in-montreal/` | `2026-09-18T15:09:01-08:00` |
| `/2026/09/16/all-in-montreal-robot-mirror/` | `2026-09-18T15:09:21-08:00` |
| `/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/` | `2026-09-18T20:46:51-08:00` |
| `/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/` | `2026-09-18T15:08:00-08:00` |

### 2c. Side / leftover paths (not in the index)

| URL | HTTP | Notes |
|---|---:|---|
| `/wp-sitemap-taxonomies-category-1.xml` | 404 | removed from the index; URL itself 404s |
| `/wp-sitemap-taxonomies-post_tag-1.xml` | 404 | same |
| `/wp-sitemap-users-1.xml` | 200 **HTML** | not XML; 0 `<loc>`. Title `Kris Krüg`, H1 `Writing for the age of generative AI.`. Canonical `https://kriskrug.co/wp-sitemap-users-1.xml/`. Robots `max-image-preview:large` (indexable). **Not in the submitted index.** Out of scope to change |
| `/sitemap_index.xml` | 404 | do not submit |
| `/sitemap-1.xml` | 404 | obsolete row already removed in GSC on 2026-07-12 (dated comment) |
| `/news-sitemap.xml` | 301 → 200 | empty urlset; not in `robots.txt`; do not submit |

---

## 3. robots.txt and `/sitemap.xml` handoff

`GET https://kriskrug.co/robots.txt` → 200. One sitemap declaration:

```text
Sitemap: https://kriskrug.co/sitemap.xml
```

Disallows (repeated once under `User-agent: *` and once under the AI-crawler group): `/wp-admin/` (with `Allow: /wp-admin/admin-ajax.php`), `/?s=`, `/search/`. Source comment still `fixes/robots.txt`.

Required header probe, `curl -sSI https://kriskrug.co/sitemap.xml` at 2026-09-21T00:39:35Z:

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

HTML `robots` meta, not headers. `wp_robots` still emits a meta tag. No `X-Robots-Tag` on these rows. Captured 2026-09-21T00:39:53Z.

| Class | URL | HTTP | robots | Canonical | Keep? |
|---|---|---:|---|---|---|
| Home | `/` | 200 | `max-image-preview:large` | self | yes, indexable |
| Page | `/about/` | 200 | same | self | yes |
| Page | `/blog/` | 200 | same | self | yes |
| Page | `/work/` | 200 | same | self | yes |
| Page | `/contact/` | 200 | same | self | yes |
| New post | `/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/` | 200 | same | self | yes |
| Sep 17 post | `/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/` | 200 | same | self | yes |
| Sep 7 post | `/2026/09/07/ai-already-campaign-issue-vancouver/` | 200 | same | self | yes |
| #996 named primary | `/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` | 200 | same | self | yes; recovery belongs to #996 |
| Category | `/category/ai-ethics-philosophy/` | 200 | `max-image-preview:large, noindex, follow` | none | **approved #331** |
| Tag | `/tag/sxsw-sxswi/` | 200 | same noindex,follow | none | **approved #331** |
| Tag | `/tag/ai/` | 200 | same | none | **approved #331** |
| Author | `/author/kk/` | 200 | same | none | **approved #331** |
| Date | `/2026/08/` | 200 | same | none | **approved #331** |
| Share variant | same photography URL + `?share=twitter` | 301 → clean permalink | (not followed) | parent article | intentional canonicalize |
| Login | `/wp-login.php` | 200 | `max-image-preview:large, noindex, noarchive` | none | intentional |
| Embed | `…/embed/` | 200 | `noindex, follow, max-image-preview:large` | parent article | intentional |
| Search | `/?s=photography` | 200 | `noindex, follow, max-image-preview:large` | none | intentional; also disallowed in `robots.txt` |

`follow` is present on every archive row. Primaries were not noindexed by #331. Approved exclusions stay.

---

## 5. Live versus Google (GSC)

### 5a. Precise blocker for this session

I could not read the submitted-sitemap report. GSC API credentials and a signed-in Search Console UI are unavailable. Missing GSC access is a **precise blocker**, not evidence that the public sitemap failed.

| Needed | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, `GSC_CLIENT_SECRET`, `SEARCH_CONSOLE_CREDENTIALS`, or `GOOGLE_GSC_CREDENTIALS`. `.env.schema` does not define a GSC secret |
| Signed-in GSC UI | **Not available** |
| WP admin / Site Kit Search Console REST | **Not available.** `WP_USER` / `WP_APP_PASSWORD` and `WP_API_*` unset |
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
| Discovered pages in the observed UI | 1,666 | not re-read. Live inventory is now **1,025**. The gap is expected until Google re-reads and drops archive URLs |
| Submission already exists | yes; do not recreate | held |

Earlier dated comments remain historical records, not instructions to repeat the clicks: Jul 2 Success after submit; Jul 12 last-read Jul 2 / 1,637 pages and obsolete `/sitemap-1.xml` removed; Jul 16 `/indigenous-ai/` inspection; Aug 28 signed-out queue audit.

### 5c. Live-versus-Google comparison (what can be said without inventing)

| Inventory | Count | What it is |
|---|---:|---|
| Live submitted sitemap (this session) | **1,025** | posts + pages only |
| Sep 8 public receipt | **1,021** | 975 + 46 |
| Sep 6 retained crawl (issue body) | **1,020** | 974 + 46; see §7 |
| #331 deploy expected | **1,019** | 973 + 46 on 2026-09-03 |
| Last GSC discovered (Sep 6 UI, last read Sep 2) | **1,666** | pre-deploy Google inventory. Includes archives Google had already discovered |

A reduced Google discovered count after the next post-deploy read is **expected**. It is not traffic loss by itself. Indexed totals were not available here and are not invented.

### 5d. Exact manual GSC click path (closeout criterion)

KK, in a signed-in session as the owner of `sc-domain:kriskrug.co` (dated comments used `kk@bc-ai.ca`):

1. Open [Google Search Console → Sitemaps](https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Akriskrug.co).
2. Confirm the property selector is **`sc-domain:kriskrug.co`** (domain property, not a stray URL-prefix duplicate).
3. Find the existing row **`https://kriskrug.co/sitemap.xml`**.
4. **Do not resubmit. Do not Submit a new URL. Do not remove rows. Do not Request indexing.**
5. Record, with a real clock timestamp (never backdated):
   1. Observation timestamp.
   2. Property id.
   3. Canonical row URL (`https://kriskrug.co/sitemap.xml`).
   4. **Last read** date.
   5. **Status**.
   6. Discovered pages (and videos if shown).
   7. Child-level list if the UI still expands one.
   8. Any fetch error text.
6. Paste those eight fields onto #274 or a short follow-up receipt.

**Close #274 only when** last-read is **after 2026-09-03**, status is Success with **no fetch error**, and the discovered count is explained against live **1,025** (allow the four ALL IN Montreal publications and ordinary reporting lag). If last-read is still September 2 or any pre-deploy date, keep waiting.

---

## 6. Noindex classification (issue body + public re-check)

September 6 issue text classified **964** noindex examples: **901** share variants, **46** login URLs, **6** embeds, **11** tag archives, **zero** primary article or landing-page URLs. New tag examples fit the approved policy. Old share classifications do not prove current noindex on the original articles.

This session did **not** re-fetch a GSC example export (none is in the repo; GSC is blocked). Public class representatives in §4 still match that grouping:

| Class | Public 2026-09-21 | Disposition |
|---|---|---|
| Primary posts / pages | 1,025 sitemap URLs; sampled primaries plus the four new posts all indexable | retain |
| Tag / category / author / date archives | noindex,follow; absent from the sitemap | **keep** (#331) |
| Share variants | 301 to the clean permalink | **keep** canonicalize |
| Login | noindex,noarchive | **keep** |
| Embeds | noindex,follow; canonical to the parent | **keep** |
| Search | noindex,follow + robots.txt Disallow | **keep** |

Do not remove intentional noindex. Duplicate-content recovery and article growth stay with #996 / #402 / #997.

---

## 7. Retained-crawl receipt

### 7a. September 6 complete crawl (reused with provenance)

**Provenance:** issue #274 body, refreshed 2026-09-06. Raw GET logs are **not** in this repo.

- 974 posts + 46 pages = **1,020**
- all direct 200
- all exact self-canonicals and descriptions
- zero robots / googlebot-meta or `X-Robots-Tag` noindex

Counts are a dated baseline, not an immutable acceptance value.

### 7b. September 8 complete crawl (reused with provenance)

**Provenance:** [issue-274-sitemap-followthrough-20260908.md](issue-274-sitemap-followthrough-20260908.md), 2026-09-08T06:05:31Z–06:09:49Z, concurrency 4.

- Population: every `<loc>` from the two live child sitemaps (**1,021** unique)
- Result: **1,021 ok / 0 fail**
- The Sep 7 post `/2026/09/07/ai-already-campaign-issue-vancouver/` was in that 1,021

### 7c. Why this session did not recrawl all 1,025 URLs

The issue says reuse a complete crawl when provenance exists, and repeat a bounded-concurrency full crawl only if changes or missing evidence warrant it. Sep 8 raw counts live in the committed receipt. The only inventory change is **+4** posts. A second 1,025-URL GET sweep would be outbound noise, not new proof of the 1,021 already crawled.

`make sitemap-followthrough` therefore defaults to index + children + leftover paths + representative robots. `--full-crawl` exists as an opt-in and is capped at 4 workers.

### 7d. 2026-09-21 crawl of the four new retained URLs

| Field | Value |
|---|---|
| Window | 2026-09-21T00:40:00Z |
| Population | the four post locs that were not in the Sep 8 1,021 |
| Method | direct GET, no redirect follow; fail on any hop, noindex, missing/mismatched canonical, missing description, googlebot meta, or `X-Robots-Tag` noindex |
| Result | **4 ok / 0 fail** |

| URL | HTTP | robots | Canonical | Description |
|---|---:|---|---|---|
| `/2026/09/15/headed-east-for-all-in-montreal/` | 200 | `max-image-preview:large` | self | 177 chars |
| `/2026/09/16/all-in-montreal-robot-mirror/` | 200 | same | self | 143 chars |
| `/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/` | 200 | same | self | 213 chars |
| `/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/` | 200 | same | self | 300 chars |

No `X-Robots-Tag`. No googlebot meta.

---

## 8. Original 24h / 72h checkpoints

Never backdated. No observation in this session is labeled as a July or September T+24h / T+72h read.

| Planned checkpoint | Evidence in repo / issue | This receipt |
|---|---|---|
| Original July submit-monitor T+24h (checklist 2026-07-26) | No committed file or comment titled as that checkpoint | **missed / unavailable** |
| Original July submit-monitor T+72h | Same. Dated Jul 2 / Jul 12 / Jul 16 GSC comments exist; they are not a completed 24h/72h packet | **missed / unavailable** as labeled checkpoints |
| Post-#331 T+24h (calendar 2026-09-04) | None | **missed / unavailable** |
| Post-#331 ~T+72h (calendar 2026-09-06) | Issue #274 body records a Sep 6 public + GSC audit. Last Google read in that text is still **September 2** | dated issue text only; **not** this session; **not** a post-deploy Google read |
| 2026-09-08 public receipt | Public matrix, robots, 1,021-URL crawl | establishes then-current inventory; **does not** establish Google's last-read |
| This session (2026-09-21T00:39Z) | Public matrix, robots, 1,025 inventory, four new-URL checks | establishes live inventory and policy; **does not** establish Google's last-read |

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

No repeated submission. No mass or manual indexing requests. No deleting old GSC rows. No temporary removals. No archive-policy edit. No `robots.txt` edit to remove the 301 handoff. No #996 recovery writes. No #402 growth. No edits to #994 / #995 / #996 / #997 / #402 / #339 / #1025 proposal files.

The leftover `/wp-sitemap-users-1.xml` HTML 200 is recorded, not fixed.

---

## 11. What KK does next

1. Review this receipt. Public half is done again, with inventory **1,025**.
2. When convenient, walk the §5d click path and write last-read / status / counts onto #274 (or a short follow-up receipt). Use a real timestamp.
3. Close #274 only after §5d. If last-read is still pre-2026-09-03, leave it open and wait.
4. Do not purge, deploy, or resubmit from this lane.

Reproduce the public half later with `make sitemap-followthrough`. Add `--full-crawl` only if the child counts change again and a complete recrawl is actually needed.
