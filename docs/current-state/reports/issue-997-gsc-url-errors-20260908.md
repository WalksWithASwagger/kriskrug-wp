# Issue #997: GSC 404 / canonical / 5xx triage against live URLs

**Captured:** 2026-09-08T06:35Z–06:42Z (UTC)
**Mode:** Track A, read-only. Public GET (not HEAD-only), public REST GET, sitemap/robots. Zero WordPress writes. Zero cache purges. Zero Search Console submits, removals, Validate Fix, or indexing requests.
**Refs:** [#997](https://github.com/WalksWithASwagger/kriskrug-wp/issues/997) (this triage). Cross-link only: [#274](https://github.com/WalksWithASwagger/kriskrug-wp/issues/274) sitemap follow-through, [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331) archive policy (live snippet 26), [#996](https://github.com/WalksWithASwagger/kriskrug-wp/issues/996) unindexed-primary batch (handed `/page/2/` here). Do not start or edit #339 / #402 / #994 / #995 from this file.
**Property (dated, not re-read):** `sc-domain:kriskrug.co`

This is a reviewable Track A triage. It is **not** closeout. Closeout still needs the current GSC example lists.

---

## Ranked recommendation

**One exact repair class.** Homepage `/page/{n}/` (n ≥ 2) is a same-document alias of `https://kriskrug.co/`. It currently emits a user-canonical of `https://kriskrug.co/{n}/`, and that numeric path then 301s via WordPress slug-guess onto an unrelated published post. Collapse the alias to the homepage. Do not invent a homepage catch-all for unrelated 404s.

| Rank | Choice | Verdict |
|---|---|---|
| 1 | 301 `/page/{n}/` → `https://kriskrug.co/` and force that canonical when a 200 still renders | **SELECTED.** `/page/2/`, `/page/3/`, and `/page/100/` all 200 the same four homepage post cards and the same H1 as `/`. Semantic equivalence is proven. The current canonical (`/{n}/`) is not equivalent. |
| 2 | Self-canonical `/page/{n}/` | **Not selected.** That would ask Google to index many copies of the same static front page. |
| 3 | No change / wait for GSC Validate Fix | **Not selected.** The collision is live on public GET, independent of the missing example export. |
| 4 | Redirect `/3/`, `/]`, `/*`, or other hard 404s to `/` | **Forbidden.** Unrelated missing content. Leave as 404. |

Live publication remains out of scope. The paste-ready snippet is `fixes/issue-997-homepage-paged-canonical.php` (**not live**). Activate it only after KK approval and a stated rollback. Do not also ship a theme copy of the same filter.

A second, optional decision — stop WordPress from slug-guessing `/2/` → post 4002, `/4/` → post 1171, and the other numeric first-segments — is **not** in that snippet. Those 301s currently land on real articles. Changing them is a different blast radius. Do not send those paths to the homepage.

---

## 1. Snapshot dates, coverage, and the GSC hole

### 1a. Precise blocker for this session

I have no Google Search Console access from this machine. I did not invent the current 125 / 33 / 1 / 10 example lists, crawl dates per row, or URL Inspection states.

| Needed | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, or Search Console names in `.env.schema`. |
| Signed-in GSC UI | **Not available.** |
| Current Pages export for Not found (404), Duplicate without user-selected canonical, Soft 404, Server error (5xx) | **Absent** from the repo and this VM. |
| Per-URL last-crawl / reported date for those four buckets | **Missing.** |
| URL Inspection (Google-selected vs user canonical, last crawl, referring sitemap) | **Missing for every URL.** |
| WP credentials for Site Kit REST | **Absent.** `make doctor` FAIL: credentials unresolved; `scripts/notion-to-wp/.venv` missing. Site Kit `1.186.0` is visible in public HTML only. |
| Ryze / Context.dev GSC | Ryze subscription inactive (HTTP 402). Context.dev not used. |

### 1b. Dated GSC evidence copied from issue #997 (not re-measured)

Quoted from the 2026-09-06 signed-in audit in the issue body. These are historical reports, not confirmed current defects.

| Bucket | 2026-09-06 display | What the issue already said |
|---|---:|---|
| Not found (404) | 125 examples | Historical; not confirmed current |
| Duplicate without user-selected canonical | 33 examples | Historical |
| Soft 404 | 1 example | Historical; URL not named |
| Server error (5xx) | 10 examples | All legacy share variants crawled March–July |
| Sitemap GET (posts + pages) | 974 posts + 46 pages = 1,020, all 200, exact self-canonicals | **Refreshed:** 975 posts + 46 pages = **1,021**. #274's same-day retained crawl already recorded 1,021 / 1,021. This session did not repeat that full crawl. |
| Sampled sharing URL | 301 → article → 200 | **Refreshed:** `x-redirect-by: KK GSC404` |
| Intentional noindex inventory | 901 share variants, 46 login URLs, 6 embeds, 11 tag archives; zero primary articles | Class reps rechecked; not a new inventory |

Do not treat 125 as the count of live 404s. Do not treat 10 as current 5xx.

---

## 2. Verification run this session

| Check | Result |
|---|---|
| `make doctor` | **FAIL** (expected here): WP credentials unresolved; venv missing; Varlock not on PATH. `gh` authenticated. Live `style.css` reachable |
| `make status-readonly` | WP smoke 0 failures / 0 warnings. WordPress `7.0.4`. Aurora live and repo `main` **1.6.11**. Draft-queue unavailable |
| `make seo-publisher-smoke` | **PASS**: `/wp-sitemap.xml` 200, `/feed/` 200, `/news-sitemap.xml` 200; three recent `BlogPosting` checks |
| `robots.txt` | Allows public content. Disallows `/wp-admin/` (except admin-ajax), `/?s=`, `/search/`. `Sitemap: https://kriskrug.co/sitemap.xml` |
| `/sitemap.xml` | **301** → `/wp-sitemap.xml` (`x-redirect-by: WordPress`). Intentional. Owned by #274 / #331. Do not "fix." |
| Sitemap children | **2**: posts (975) + pages (46). No category / tag / users children |
| Bounded GET | 57 documented or named URLs, 2 workers, GET not HEAD. First-hop headers recaptured with `curl` `--max-redirs 0` because Python `urlopen` follows 301s silently |
| `git diff --check` | clean (this packet) |

Public HTML is authoritative. `make seo-audit` was not used (false 1016/1016 missing after Jetpack deactivation; see `SEO-STRIKING-DISTANCE-2026-08-02.md`).

Front page identity, public REST: page **3930**, slug `empowering-events-organizations-for-the-ai-age`, `link` `https://kriskrug.co/`, `modified` `2026-09-07T12:58:30`. Page 2315 (`/home/`) is a different published page and is not this collision.

---

## 3. URL classes (public evidence, not a forged GSC export)

Join rule: classify from a documented source (issue body, June 2026 GSC-404 artifacts, #996 handoff, #331 deploy receipt) plus a live GET. I did not add URLs "that GSC probably has."

| Class | Representative (documented) | Live 2026-09-08 | Intended target | Disposition |
|---|---|---|---|---|
| Static-front-page `/page/{n}/` | `/page/2/` named by #996 | **200**, title `… \| Page 2`, H1 `The model is the message.`, robots indexable, **canonical `https://kriskrug.co/2/`**, `og:url` homepage. Same four post cards as `/` | `https://kriskrug.co/` | **Repair.** Proposal 1 |
| Numeric first-segment | `/2/` named by #996 | **301** `x-redirect-by: WordPress` → `/2023/11/05/20-ways-to-resist-ais-mind-enslavement/` (post **4002**) → 200 self-canonical | Pretty permalink of that post is a *guess*, not a declared alias. REST: no post/page/media id or slug `2` | **Parked.** Do not 301 to `/`. Optional later: stop slug-guess |
| Numeric first-segment, no guess | `/3/` | **404**, no Location, no canonical, title `Page not found` | none | **Keep 404.** Not a homepage candidate |
| Writing pagination | `/blog/page/2/` | **200**, self-canonical `https://kriskrug.co/blog/page/2/` | self | **No change.** Theme `writing_archive_canonical_url()` already owns this |
| Share / `amp` / `nb` variant | June 2026 + #996 photography `?share=twitter` | **301** `KK GSC404` → clean permalink → **200**, self-canonical. Not 5xx | clean permalink | **No change.** Owned by snippet 8 / `fixes/gsc-404-query-param-canonicalize.php` |
| June 2026 mapped 404 | deleted categories, Drupal subpaths, dead `?p=` / `?page_id=`, `/quote-request/`, `/shrine`, FiR slug, `/spark/wordpress/`, `/node/216`, field-notes `/page/3/` | **301** `x-redirect-by: redirection` → documented target → 200 | mapped target (not `/` except where the 2026-06-18 rule already said `/blog/`) | **No change.** Redirection IDs 21–38 |
| Archive (category / tag / author / date) | `/category/ai-ethics-philosophy/`, `/tag/sxsw-sxswi/`, `/author/kk/`, `/2026/08/` | **200**, robots `noindex, follow`, **zero user-canonical** | none; stay out of the sitemap | **No change here.** #331 v2 / snippet 26. Explains the *shape* of "duplicate without user-selected canonical." Do not add archive canonicals or sitemap rows in this lane |
| Embed | photography `/embed/` | **200**, `noindex, follow`, canonical to parent | parent article | **Keep** intentional exclusion |
| Login | `/wp-login.php` | **200**, `noindex, noarchive` | none | **Keep** |
| Pretty `?p=` of a live post | `?p=11936` | **301** WordPress → `/2026/05/23/you-cant-drink-data/` → 200 | pretty permalink | **No change** |
| Junk probe | `/]`, `/*` (June skip list) | **404**, no redirect | none | **Keep 404** |
| Tag overflow | `/tag/misc/page/38/`, `/page/40/` (August last-page notes) | **404** | none | **Keep 404.** Do not redirect to `/` or page 1 |
| Sitemap primaries | posts + pages | #274 already crawled 1,021 / 1,021 | self | **#274.** Not duplicated here |

Tech-village leftover: `/…/system/files?file=techvilliage.pdf` **301s** to the parent post **with `?file=` still attached**. The parent user-canonical is the clean permalink. Cosmetic. Not a homepage issue. Not in the top-ten list.

---

## 4. The material defect (proposal 1)

### 4a. What `/page/2/` is

`/page/2/` is not a second page of the Writing archive and it is not post 4002.

| Field | `https://kriskrug.co/` | `https://kriskrug.co/page/2/` | `https://kriskrug.co/2/` |
|---|---|---|---|
| First hop | 200 | 200 | **301** WordPress → post 4002 |
| Title | `Kris Krüg \| AI Keynote Speaker & Creative Technologist` | same + ` \| Page 2` | `20 Ways to Resist AI's Mind Enslavement \| Kris Krüg` |
| H1 | `The model is the message.` | `The model is the message.` | `20 Ways to Resist AI’s Mind Enslavement` |
| User-canonical | self `/` | **`https://kriskrug.co/2/`** | pretty permalink of 4002 |
| `og:url` | `/` | `/` | 4002 pretty permalink |
| Robots | `max-image-preview:large` | same, indexable | same, indexable |
| Unique dated post hrefs | 4 (Web Summit / campaign / founders / Futureproof) | **identical 4** | article body |
| Homepage pagination links | **none** in the rendered HTML | none | n/a |
| Cache-busted | same title / canonical | same title / canonical ` /2/` | same 301 → 4002 |

`/page/3/` and `/page/100/` repeat the homepage card set. `/page/4/`, `/page/5/`, `/page/20/`, `/page/50/`, `/page/80/` are the same pattern: 200 + ` | Page N` + canonical `/{n}/`.

`/page/1/` already **301s** to `/` (`x-redirect-by: WordPress`). Core got page 1 right and left page ≥ 2 as a 200 alias.

Mechanism, from live behaviour plus theme source:

1. Page 3930 is a **static front page**. WordPress still accepts `/page/{n}/` and stamps ` | Page N` on the title.
2. Core `rel_canonical` on that singular appends the page number as `/{n}/` (single-paged form), not `/page/{n}/`.
3. Aurora `writing_archive_canonical_url()` correctly self-canonicalizes `/blog/page/{n}/` and **explicitly returns empty on `is_front_page()`**, so it does not correct this.
4. Requesting `/{n}/` does not resolve a post/page/media with that slug. WordPress `redirect_canonical` **guesses** the first `post_name LIKE '{n}%'` and 301s to it.

Guesses verified this session (`x-redirect-by: WordPress`):

| Request | Destination | Post ID | In sitemap? |
|---|---|---:|---|
| `/2/` | `/2023/11/05/20-ways-to-resist-ais-mind-enslavement/` | 4002 | yes |
| `/4/` | `/2007/02/15/4-tips-regarding-converging-lines/` | 1171 | yes |
| `/5/` | `/2007/02/21/5-black-and-white-photography-tips/` | 1161 | yes |
| `/20/` | same 4002 article as `/2/` (`20-ways-…`) | 4002 | yes |
| `/50/` | `/2005/11/11/50-flavorful-affordable-wines/` | 746 | yes |
| `/80/` | `/2006/01/04/802/` | (404 after the hop) | n/a |
| `/3/` | hard 404 | — | — |
| `/100/` | hard 404 | — | — |

So `/page/2/` tells Google "the canonical of this homepage alias is `/2/`," and `/2/` then claims a 2023 ethics article. That is a user-selected canonical pointing at the wrong primary.

### 4b. Why the target is the homepage, not `/page/2/` and not `/2/`

The issue forbids homepage catch-alls for **unrelated missing** content. This is the opposite: `/page/{n}/` **is** the homepage. Same H1, same four cards, no distinct listing. The proven equivalent URL is `https://kriskrug.co/`.

`/blog/page/2/` is a different, real listing and already self-canonicalizes. Leave it alone.

### 4c. Current owner and implementation handoff

| Piece | Current owner | Change? |
|---|---|---|
| `/page/{n}/` 200 + ` | Page N` title | WordPress core, static front page 3930 | 301 to `/` |
| User-canonical `/{n}/` | WordPress core `rel_canonical` on that singular | Filter to `https://kriskrug.co/` if a 200 still renders |
| `/blog/page/{n}/` self-canonical | Aurora `theme/kk-aurora/functions.php` `writing_archive_canonical_url()` | **Do not touch** |
| `/{n}/` slug-guess 301 | WordPress `redirect_canonical` | **Not in this snippet** |
| Share variants | Snippet 8 (`KK GSC404`) | **Do not touch** |
| June mapped 404s | Redirection rules 21–38 | **Do not touch** |
| Archive noindex / sitemap drop | Snippet 26 (#331 v2) | **Do not touch** |

**Track A apply vehicle (this PR, prep only):** `fixes/issue-997-homepage-paged-canonical.php`. Code Snippet, front-end, not live. Rollback: deactivate. No database write. No Redirection import. No homepage rules for `/3/`, `/]`, `/*`, or dead post IDs.

**Live approval boundary:** KK must approve activation as a separate act from merging this PR. Pagely cache may still serve a HIT of `/page/2/` after activate; that purge is also KK. Do not click Validate Fix from this lane. Do not deploy theme files from this lane.

**Track B handoff (do not mix into this PR):** if KK wants the durable owner in Aurora instead of a snippet, add the same `is_front_page() && paged ≥ 2` redirect/canonical next to `writing_archive_canonical_url()`. Use `home_url('/')`, **not** `get_pagenum_link()`, which is the function that yields `/{n}/` on this front page. Rollback: revert the theme release and purge. **Do not run the snippet and a theme copy at the same time.** Pixel gate applies to a theme deploy; it does not apply to a snippet-only activate unless KK asks.

### 4d. Post-approval readback (after a future write, not now)

```bash
curl -sS -D - -o /dev/null --max-redirs 0 --max-time 30 'https://kriskrug.co/page/2/'
# expect: HTTP 301, location: https://kriskrug.co/, x-redirect-by: KK 997

curl -sS -D - -o /dev/null --max-redirs 0 --max-time 30 'https://kriskrug.co/blog/page/2/'
# expect: HTTP 200, unchanged

curl -sS -D - -o /dev/null --max-redirs 0 --max-time 30 'https://kriskrug.co/3/'
# expect: HTTP 404, no Location
```

Then GET the 301 target and confirm one self-canonical `https://kriskrug.co/`. Cache-bust `/page/2/` if the edge still HITs a 200.

---

## 5. Compact manifest

Only documented or named URLs. `reported_crawl_date` is the source document's date, not a fresh GSC last-crawl.

| source | original_bucket | reported_crawl_date | current_chain | intended_target | evidence | disposition |
|---|---|---|---|---|---|---|
| `https://kriskrug.co/page/2/` | #996 pagination collision; likely duplicate/canonical | 2026-09-06 named; not a GSC export row | 200 → canonical `/2/` | `https://kriskrug.co/` | same 4 cards + H1 as `/`; GET + cache-bust | **repair** (proposal 1) |
| `https://kriskrug.co/page/3/` | same class | this session, public | 200 → canonical `/3/` | `https://kriskrug.co/` | same cards as `/`; `/3/` is 404 | **repair** (same class) |
| `https://kriskrug.co/page/100/` | same class | this session, public | 200 → canonical `/100/` | `https://kriskrug.co/` | same cards as `/` | **repair** (same class) |
| `https://kriskrug.co/2/` | #996 numeric alias | 2026-09-06 named | 301 WP → post 4002 → 200 | pretty permalink of 4002 *or* 404 if guess is retired | REST: no slug/id `2` | **parked** (do not send to `/`) |
| `https://kriskrug.co/3/` | numeric, no guess | this session | 404 | none | hard 404, no Location | **keep 404** |
| `https://kriskrug.co/blog/page/2/` | writing pagination | theme / #347 history | 200 self-canonical | self | theme owner | **no change** |
| `https://kriskrug.co/page/1/` | front-page page 1 | this session | 301 WP → `/` → 200 | `/` | already correct | **no change** |
| `…/barcampearth-…/?share=twitter&nb=1` | June 2026 share / dated 5xx class | 2026-06-09 | 301 `KK GSC404` → 200 | clean permalink | snippet 8 | **no change** |
| `…/photography-and-generative-ai/?share=twitter` | #996 share class | 2026-09-08 #996 | 301 `KK GSC404` → 200 | clean permalink | snippet 8 | **no change** |
| `…/you-cant-drink-data/?amp=1` | amp tracking | this session | 301 `KK GSC404` → 200 | clean permalink | snippet 8 | **no change** |
| `/category/art/` and `?amp=1` | June deleted category | 2026-06-08 | 301 redirection → `/blog/` | `/blog/` | rule 21 | **no change** |
| `/2007/08/07/bryght-world-tour-2007/events/barcamp-vancouver-2007` | June Drupal subpath | 2026-06-08 | 301 redirection → parent | parent post | rule 22 | **no change** |
| `/?p=87` | June dead post id | 2026-06-08 | 301 redirection → `/blog/` | `/blog/` | rule 27 | **no change** |
| `/quote-request/` | June dead page | 2026-06-08 | 301 redirection → `/contact/` | `/contact/` | rule 34 | **no change** |
| `/2023/09/28/future-in-review-podcast/` | June dead slug | 2026-06-08 | 301 redirection → FiR post | FiR pretty permalink | rule 35 | **no change** |
| `/shrine` | June short path | 2026-06-08 | 301 redirection → shrine post | shrine pretty permalink | rule 36 | **no change** |
| `/category/field-notes/page/3/` | June overflow | 2026-06-08 | 301 redirection → `/page/2/` of that category | category page 2 | rule 38; destination is `noindex,follow` | **no change** |
| `/spark/wordpress/`, `/node/216` | June legacy | 2026-06-08 | 301 redirection → `/blog/` | `/blog/` | rules 37 / 26 | **no change** |
| `/category/ai-ethics-philosophy/` | #331 archive | 2026-09-03 deploy | 200, noindex,follow, no canonical | none | snippet 26 | **#331, not #997** |
| `/tag/sxsw-sxswi/`, `/author/kk/`, `/2026/08/` | #331 archive | 2026-09-03 | same robots, no canonical | none | snippet 26 | **#331, not #997** |
| photography `/embed/` | Sep 6 embed class | 2026-09-06 inventory | 200 noindex,follow, parent canonical | parent | intentional | **keep** |
| `/wp-login.php` | Sep 6 login class | 2026-09-06 inventory | 200 noindex,noarchive | none | intentional | **keep** |
| `/]`, `/*` | June junk skip | 2026-06-14 | 404, no redirect | none | intentional skip | **keep 404** |
| `/tag/misc/page/38/` | August last-page note | 2026-08-02 archive doc | 404 | none | overflow | **keep 404** |
| sitemap primaries | Sep 6 + #274 | 2026-09-06 / 2026-09-08 | 1,021 URLs, 2 children | self | #274 receipt | **#274** |

---

## 6. Four GSC buckets, what I can and cannot say

| Bucket | 2026-09-06 count | Public 2026-09-08 | Missing | Action |
|---|---:|---|---|---|
| Not found (404) | 125 | Documented June sources now **301**. Public 404s I hit: `/3/`, `/100/`, `/]`, `/*`, `/tag/misc/page/38` and `/40/`. That is not the 125-row list | Current example export + last-crawl dates | Do not bulk-redirect. Do not Validate Fix from here |
| Duplicate without user-selected canonical | 33 | Archives still emit **no** `rel=canonical` and `noindex,follow` (#331). Homepage `/page/{n}/` *has* a user-canonical, so it may sit in a *different* GSC duplicate bucket if Google still lists it | Which 33 URLs | Do not add archive canonicals here. Cross-link #331 / #274 |
| Soft 404 | 1 | URL **not named** in the issue. `/page/{n}/` 200s the homepage and *could* be a soft-404 shape; I will not claim it is the GSC row | The one example URL | After proposal 1, KK can inspect that one row |
| Server error (5xx) | 10 | Dated as share variants. Four live share/amp GETs were **301 `KK GSC404` → 200**, not 5xx | The ten exact URLs + March–July crawl stamps | No server/security overhaul. No snippet change |

---

## 7. Cross-links (do not duplicate)

| Lane | What they own | What this file does |
|---|---|---|
| #274 | Sitemap submit/readback, robots handoff, retained-primary crawl | Quotes the 1,021 receipt. Does not resubmit |
| #331 | Archive sitemap drop + `noindex,follow` | Rechecked class reps. Does not reopen allowlists or add archive canonicals |
| #996 | Five unindexed primaries; handed `/page/2/` here | Does not edit `content/drafts/issue-996-indexing-recovery/` |
| #994 / #339 | AI Second Brain packet | Untouched |
| #995 | `/events/` title + description snippet | Untouched |
| #402 | Growth / authority hubs | Untouched |
| June GSC-404 (snippet 8 + Redirection 21–38) | Share params and mapped legacy 404s | Rechecked; left live |

---

## 8. Acceptance criteria

| #997 criterion | Status |
|---|---|
| Read current examples for the four named GSC buckets; record dates/coverage; classify | **Partial.** Classes from public GET + dated issue text + June artifacts + #996. Current four-bucket exports are **missing** |
| Bounded low-concurrency GET; chains; canonical/robots; not HEAD-only | **Met** for every documented/named URL in the manifest |
| Cross-reference sitemap, internal links, available traffic | **Partial.** Sitemap refreshed. Homepage HTML has **zero** `/page/{n}/` hrefs. Traffic/backlink GSC rows missing |
| Report + compact manifest | **Met** by this file |
| ≤10 exact repairs where replacement/canonical is proven; no homepage catch-all; or no-change receipt | **Met.** One repair class. Unrelated 404s stay 404 |
| Owner + bounded handoff with rollback and live approval; no Track A+B mix | **Met.** Snippet prep in this PR. Theme notes only |
| Keep sitemap/archive with #274/#331; cross-link #996 | **Met.** Other-lane files not edited |

Use `Refs #997`, not `Closes`. Keep the issue open until KK has the current example lists and, if he wants, activates the snippet.

### Exact GSC pull KK can run later

Search Console → Indexing → Pages, property `sc-domain:kriskrug.co`. For each of **Not found (404)**, **Duplicate without user-selected canonical**, **Soft 404**, **Server error (5xx)**: record report last-updated date, example count, and whether the export is the full set or the UI sample. Confirm whether `/page/2/` still appears (and in which bucket). Do not invent those rows in a later comment if the export is still missing. Do not click Validate Fix from an agent session.

---

## 9. Scope and safety

Read-only session. No POST / PATCH / PUT / DELETE against kriskrug.co. No theme deploy, no SFTP, no snippet activate, no Redirection edit, no Pagely purge, no GSC write.

No `.env` file was read or printed. Authenticated WordPress REST was not available.

`fixes/issue-997-homepage-paged-canonical.php` is prep only. It is not a live apply.

THINGS THIS PACKET DID NOT TOUCH: `content/drafts/issue-996-indexing-recovery/`, `fixes/issue-995-events-search-snippet.php`, #339 apply packet, #274 / #331 / #994 report files, theme PHP, production snippets.
