# Issue #994: AI Second Brain search-decline diagnosis

**Captured:** 2026-09-08T04:50Z (UTC)
**Mode:** Track A, read-only. Public HTML (plain + cache-busted), public REST GET, sitemap/robots. Zero WordPress writes. Zero cache purges. Zero Search Console submits / Validate Fix.
**Refs:** #994 (this diagnosis), #339 (pending apply packet), #336 (closed prep handoff), #402 (parked growth umbrella). Do not start #996, #274, #995, or #997 from this file.
**Target:** https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/

## Ranked recommendation

**Retain the pending #339 package.** Do not revise named title, description, body, or link fields in this lane. Do not write a competing #994 apply packet.

| Rank | Choice | Verdict |
|---|---|---|
| 1 | Retain pending #339 package | **SELECTED.** Live title, description, and both inbound wraps still match the packet's "before" state. The Sep 6 click/impression drop happened while those fields were still unapplied, so the packet cannot have caused the decline. |
| 2 | Revise named fields | **Not selected.** No query-level GSC export exists in this session. Inventing a new title or description would be speculation. The approved strings still name the query more honestly than the live zombies excerpt. |
| 3 | No edit | **Not selected.** The pending overwrite and two wraps remain the smallest useful on-page move. "No edit" would freeze a title that still drops "for You" and two still-unlinked source phrases. |

Live publication remains out of scope. #339 still owns the apply. This report only says the #336/#339 copy is still the right payload after the decline, and that #339 must refresh the drifted post-12327 `modified` guard before any future write.

---

## 1. Identities, verified 2026-09-08

Public REST `GET /wp/v2/posts/{id}` plus public HTML. Slug, ID, and URL still match #336/#339.

| Role | ID | Slug | Status | `modified` now | Packet guard | Identity |
|---|---:|---|---|---|---|---|
| Target | 8802 | `how-to-build-an-ai-second-brain-that-actually-works-for-you` | publish | `2026-06-28T20:27:34` | `2026-06-28T20:27:34` | **match** |
| Source 1 | 9774 | `what-journalists-need-to-know-about-ai-right-now` | publish | `2026-06-14T20:05:53` | `2026-06-14T20:05:53` | **match** |
| Source 2 | 12327 | `storyhive-haus-of-owl-jordan-dack` | publish | `2026-09-07T13:07:06` | `2026-08-16T21:03:50` | **ID/slug/URL match; modified drifted** |

Post 12327's FIND needle `knowledge bases and named assistants` is still present once and still unlinked. The wrap copy is not superseded. The stale `modified` / raw-hash pair in `apply-336-ai-second-brain.md` and `manifest.json` is a **publisher precondition for #339**, not a reason to change the replacement HTML. Do not PATCH 12327 from this issue.

Several other posts were also `modified` on 2026-09-07 (12744, 12183, 11936). That batch is outside this lane. It does not change the target's own `modified` value.

---

## 2. Live vs #336 / #339 field status

Public HTML is authoritative. Plain and `?cb=<epoch>` fetches of the target both returned HTTP 200 from `Pagely-ARES/1.22.28`, `x-gateway-cache-status: MISS`, identical `<title>`, description, canonical, and robots. WordPress generator `7.0.4`. Site Kit `1.186.0`. Live and repo Aurora `style.css` Version **1.6.11**.

| Field | Live 2026-09-08 | #336 / #339 approved | Status |
|---|---|---|---|
| HTTP | 200 | 200 | applied (unchanged) |
| Canonical | self, one tag | self | applied |
| `robots` | `max-image-preview:large` | indexable | applied |
| `googlebot` meta | absent | n/a | no extra block |
| H1 | `How to Build an AI Second Brain That Actually Works for You` (1) | do not change post title | applied / out of package |
| `<title>` | `Build an AI Second Brain That Actually Works` (44) | `Build an AI Second Brain That Actually Works for You` (52) | **pending** |
| `jetpack_seo_html_title` (public REST) | `Build an AI Second Brain That Actually Works` | same approved string | **pending** |
| `<meta name="description">` | zombies excerpt, 146 chars | 150-char thought-patterns / creative-chaos / voice-memos string | **pending** |
| `advanced_seo_description` (public REST) | same zombies excerpt | same approved string | **pending** |
| og/twitter description | same as standard description | expected after overwrite | **pending** (will follow the standard field) |
| Post title / excerpt / slug / date / taxonomies | unchanged vs packet | do not change | applied / leave alone |
| 9774 wrap `AI as a second brain` | needle 1, target hrefs 0 | wrap existing words | **pending** |
| 12327 wrap `knowledge bases and named assistants` | needle 1, target hrefs 0 | wrap existing words | **pending** |
| Target in `wp-sitemap-posts-post-1.xml` | yes; lastmod `2026-06-28T20:27:34-08:00` | expected | applied |
| `?p=8802` | 200 at the pretty permalink | expected | applied |
| `robots.txt` | allows the URL; disallows only `/wp-admin/`, `/?s=`, `/search/` | expected | applied |
| Sitemap index | posts + pages only (no tag/category/user children) | #331 v2 live | applied; see §5 |

#336 closed on 2026-07-13 after PR #337 merged the **prep** handoff. That close is not a live-apply receipt. #339 still owns the unpublished packet at `content/drafts/339-july-publisher-batch-2026-08-16/apply-336-ai-second-brain.md`.

July 13 public state said "no standard meta description." That is **superseded as a live fact**: Aurora now emits one `<meta name="description">` from the stored `advanced_seo_description`. The stored value is still the unapproved zombies excerpt, so the #339 overwrite is still required. Public REST now exposes `jetpack_seo_html_title` and `advanced_seo_description` (theme `inc/seo-meta-rest.php`). The July "fields unregistered" warning is historical; overwrite mode is still required because both keys are non-empty.

---

## 3. Search Console: what is dated evidence vs what is blocked

### 3a. Precise blocker for this session

I could not retrieve exact-date, page-filtered, query-level GSC rows.

| Needed | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, or Search Console env names. `.env.schema` does not define a GSC secret. |
| Signed-in GSC UI | **Not available** to this agent. |
| Committed page+query export for this URL | **Absent** from the repo. |
| WP credentials for Site Kit REST | **Absent.** `WP_USER` / `WP_APP_PASSWORD` and `WP_API_*` are unset. Site Kit is visible in public HTML (`1.186.0`) but its Search Console reports were not readable. |
| Context.dev MCP | `needsAuth`. Not used. |
| Ryze MCP | HTTP 402, subscription inactive. Not a GSC property client in any case. |
| Profound MCP | AI-visibility product, not `sc-domain:kriskrug.co` Search Console. |

Do not invent query names, positions, device splits, country splits, or branded/non-branded click counts.

### 3b. Dated page-level aggregates that do exist

Two human-recorded page totals, both for property `sc-domain:kriskrug.co`. Neither is a query table.

| Source | Window | Page impressions | Page clicks | Implied CTR | Avg position |
|---|---|---:|---:|---:|---:|
| #336 / #279 digest-safe copy | 2026-06-12 to 2026-07-09 (exact dates) | 1,053 | 10 | 0.95% | 11.27 |
| #336 query `ai second brain` | same window | 46 | 2 | n/a | 17.52 |
| #994 issue body, signed-in UI displayed **2026-09-06** | GSC "last 28 days" vs previous period (`num_of_days=28&compare_date=PREV`) | 1,146 → 602 | 14 → 3 | 1.22% → 0.50% | **not recorded** |
| Same display, sitewide clicks | same compare | n/a | 172 → 168 | n/a | n/a |

Exact inclusive calendar dates for the Sep 6 compare were **not independently retrieved**. Typical GSC "last 28 days" vs previous, viewed 2026-09-06, is two adjacent 28-day windows ending on the last complete data day (often 2026-08-09–2026-09-05 vs 2026-07-12–2026-08-08). Treat that pair as **inferred UI convention**, not as a pulled export. KK should save the report with the date chips visible.

Longer history beyond those two windows: **not available here.**

Device, country, branded/non-branded, and query-mix: **not available here.**

### 3c. At most five query-level losses

**Cannot name five query-level losses.** That requires the Queries tab with the Page filter set to the exact target URL, for two complete 28-day windows. Inventing `ai second brain` variants as "the" losses would recycle the June query and pretend it is a Sep 6 delta.

What the **page** totals can and cannot distinguish:

| Effect | What the dated totals show | What they do not show |
|---|---|---|
| Ranking | Possible. Impressions halved. CTR also halved, which often tracks a worse average position. | No average position for either Sep 6 window. |
| Demand | Possible. A 47% impression drop can be fewer searches. | No query impression series. Sitewide clicks were almost flat (172 → 168), so this is **not** a sitewide demand collapse. |
| CTR | Supported at page level: 1.22% → 0.50%. Clicks fell harder (−79%) than impressions (−47%). | Cannot split snippet CTR from position-driven CTR or from a mix shift toward low-CTR queries. |
| Query-mix | Possible hypothesis only. | No query rows. |

The June window (1,053 / 10 / 0.95% / pos 11.27) is **not** the "previous 28 days" on the Sep 6 compare. The previous displayed period (1,146 / 14 / 1.22%) was stronger than June. The drop is latest-vs-previous on that Sep 6 screen, not a straight fade from the #336 baseline.

**Do not blame #331 / #767 archive cleanup.** Those snippets deployed 2026-09-03 ([receipt](DEPLOY-767-331-2026-09-03.md)). A 28-day window displayed 2026-09-06 is almost entirely pre-deploy. GSC itself lags one to three days, so the latest window contains at most a few days after activation, and those days are incomplete. The issue already says the drop is not proof of noindex or of any deployment. Public checks agree: the target is 200, self-canonical, indexable, and present in the post sitemap.

---

## 4. On-page and link-graph notes (not a rewrite brief)

- Body ~1,250–1,350 words depending on chrome; JSON-LD `wordCount` 1255. Eight topical H2s plus the About block. Answer-first lead is already the zombies excerpt.
- JSON-LD: BlogPosting + BreadcrumbList + Person/Organization. `BlogPosting.description` uses the excerpt, not the SEO description. Cosmetic, same pattern as other posts.
- Category `/category/generative-ai-tools/` is a listing link, not a contextual inbound.
- Hub `/ai-tools/` already contains one href to the target.
- Contextual hrefs to the target already exist on posts 11878, 12183, 5823, 5590, 4948, and 4773. The #339 wraps on 9774 and 12327 are **additional** and still absent. They are not duplicates of those existing hrefs.
- Post 12744 (`what-i-showed-founders-about-ai-workflows`, modified 2026-09-07) mentions "second brain" once and has zero hrefs to 8802. Parked. Do not add a third source in this PR. #402 stays parked.

None of that is a noindex, canonical, or "the article disappeared" defect.

---

## 5. Compact evidence table

| Check | Result | Bearing on the decline |
|---|---|---|
| Target identity 8802 / slug / URL | match | same URL Google already has |
| Live `<title>` vs approved | missing "for You" | pending CTR/intent tweak, not a live regression from #339 |
| Live description vs approved | still zombies excerpt | pending; not applied |
| Canonical / robots / sitemap | clean, indexable | rules out noindex / wrong-canonical as the cause |
| 9774 / 12327 proposed wraps | still unlinked; needles once each | pending; 12327 `modified` drifted |
| Sitewide clicks Sep 6 compare | 172 → 168 | page-specific, not sitewide |
| Page clicks / impressions Sep 6 compare | 14 → 3 / 1,146 → 602 | dated human GSC UI; query rows missing |
| June 12–Jul 9 page | 10 / 1,053 / pos 11.27 | older baseline; previous-28 on Sep 6 was actually higher |
| #331 deploy 2026-09-03 | archives noindex; posts still indexed | window is largely pre-deploy; do not assign cause |
| Query-level losses | **blocked** | see §3 |

---

## 6. Why retain, not revise

The approved title restores the article's own promise ("for You") in the SERP title. The approved description names second-brain outcomes that the body already claims (thought patterns, creative chaos, notes, voice memos, finished work). Both are still better query-aligned than the live strings, and both are still unshipped.

Revising them now would create a second publishing packet for the same post while #339 is still waiting on KK ticks. That is the duplication #994 forbids.

A future query export could still change this. If Pull A below shows the lost impressions are branded or off-intent, KK can reopen a **named-field** revision then. Until those rows exist, retain.

---

## 7. Measurement protocol (after an eventual approved publish)

Do not start the clock on this diagnosis. Start it only after KK approves and a publisher session applies the #339 8802/9774/12327 fields, public HTML confirms the approved title/description and the two hrefs, and Google has had time to recrawl.

1. Wait **at least 14 full days** after that public readback.
2. Then pull two **complete** 28-day windows that do not straddle the apply day.
3. Property: `sc-domain:kriskrug.co`. Report: Search results. Page filter = exact target URL.
4. Record page clicks, impressions, CTR, average position.
5. Queries tab, same page filter: every row for `ai second brain` and the top losses/gains by impression delta (cap discussion at five queries).
6. Count **non-branded clicks** only from those query rows (queries that are not `kris krug` / `kriskrug` variants). Do not invent a branded split if the export is not opened.
7. Qualified enquiries / conversions: record only if a real measurement exists. This repo has no enquiry counter for this URL. Do not fabricate one.
8. Compare against:
   - June 12–July 9: 1,053 / 10 / 0.95% / 11.27 and query `ai second brain` 46 / 2 / 17.52
   - The Sep 6 displayed latest window: 602 / 3 / 0.50%
9. Success for #994 is a defensible diagnosis (this file) plus, later, a defensible before/after. Success is **not** a promised rank increase. The old #336 signals (page position below 10, page CTR above 1.2%, query position below 15) remain useful watch points, not guarantees.

---

## 8. Exact GSC pull for KK (unblocks §3c)

Search Console → Performance → Search results. Property `sc-domain:kriskrug.co`. All four metric toggles on.

**Pull A.** Filter Page = exact `https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/`. Custom dates, two complete 28-day windows that match the Sep 6 compare (read the date chips; do not assume). Export Queries for each window. Note device and country only if a single slice is material.

**Pull B.** Same page filter, Queries contains `second brain` (and a second pass for `second mind` if rows appear).

**Pull C.** Cannibalisation: keep the query filter, switch to Pages. If another URL is taking the impressions, say so. Candidates to look at, not to assume: `/ai-tools/`, `/2026/06/13/speak-it-into-existence-ai-voice-first-workflows/`.

**Pull D.** Sitewide Search results for the same two windows (already 172 vs 168 clicks on Sep 6) so the page drop stays in context.

Paste digest-safe aggregates onto #994 / #339. No raw export in git.

---

## 9. Cross-links and ownership

| Issue | Role after this report |
|---|---|
| #994 | Diagnosis + retain recommendation. Draft PR only. |
| #339 | Still the apply owner. Refresh 12327 `modified` / raw hash immediately before any dry-run. Do not apply from this PR. |
| #336 | Closed prep. Historical evidence + locked test fixtures. Not a live-apply receipt. |
| #402 | Parked. Surprising-winner hub work. Do not expand here. |
| #331 / #767 | Deployed 2026-09-03. Not assigned as the cause of this page drop. |
| #274 / #995 / #996 / #997 | Independent lanes. Not started. |

---

## 10. Scope and safety

No POST, PATCH, PUT, or DELETE against kriskrug.co. No theme deploy, SFTP, snippet edit, cache purge, indexing request, or Validate Fix. No secrets printed. The #336 unit test file and the #339 packet were **not** modified. No issue-specific proposal file was added because the ranked recommendation is retain, not revise.

### Session verification (2026-09-08)

| Command | Result |
|---|---|
| `make doctor` | **FAIL**, expected. WP credentials unresolved; `scripts/notion-to-wp/.venv` missing; `gh` authenticated as `cursor`; live `style.css` reachable. No authenticated write path. |
| `make status-readonly` | Ran. WP 7.0.4; Aurora live and repo `1.6.11`; draft-queue counts unavailable without creds. |
| `make seo-publisher-smoke` | **PASS** (sitemap, feed, news sitemap, three recent BlogPosting pages). |
| `python3 -m unittest scripts.tests.test_issue_336_ai_second_brain_seo_handoff -v` | 7/7 OK. Handoff fixtures unchanged. |
| `curl -sSIL` target | HTTP/2 200; robots `max-image-preview:large`; self-canonical; live title still missing "for You". |
| `git diff --check` | clean after this file |

### Follow-ups that are not this PR

1. KK Pull A–D in §8 so query-level losses can be named.
2. #339 publisher session: snapshot 8802 / 9774 / 12327, refresh 12327 guards, apply only after ticks.
3. Optional later: one wrap from 12744 if Pull C shows it is a real source page. Not now.
