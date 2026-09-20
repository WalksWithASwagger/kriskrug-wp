# Issue #994: AI Second Brain search-decline — in-repo closeout

**Captured:** 2026-09-20 (UTC)
**Mode:** Track A, **in-repo only**. No outbound HTTP. No live GSC pull. No WordPress admin, REST write, cache purge, indexing request, or Validate Fix.
**Closes:** [#994](https://github.com/WalksWithASwagger/kriskrug-wp/issues/994) as a preparation issue. Live apply of the pending packet is a later KK-gated act and is not this PR.
**Prior live-readback:** [`issue-994-second-brain-diagnosis-20260908.md`](issue-994-second-brain-diagnosis-20260908.md) (merged PR #1000, `Refs #994`). That file remains the last public-HTML / public-REST snapshot. This file does not re-fetch it.
**Refreshed proposal:** [`content/drafts/issue-994-second-brain/proposal.md`](../../../content/drafts/issue-994-second-brain/proposal.md). Confirmation only. It does **not** overwrite [`content/drafts/339-july-publisher-batch-2026-08-16/apply-336-ai-second-brain.md`](../../../content/drafts/339-july-publisher-batch-2026-08-16/apply-336-ai-second-brain.md).
**Refs:** #339 (pending apply owner), #336 (closed prep handoff), #402 (parked growth umbrella). Do not start #274, #995, #996, #997, #1025, or #1030 from this file.

**Target:** `https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/` (WordPress post **8802**, slug `how-to-build-an-ai-second-brain-that-actually-works-for-you`)

---

## Ranked recommendation

**Retain the pending #339 package.** Do not revise named title, description, body, or link fields in this lane. Do not write a competing apply packet.

| Rank | Choice | Verdict |
|---|---|---|
| 1 | Retain pending #339 package | **SELECTED.** Last live title, description, and both inbound wraps (2026-09-08) still match the packet's "before" state. The Sep 6 click/impression drop happened while those fields were still unapplied, so the packet cannot have caused the decline. No later in-repo receipt shows the overwrite landed. |
| 2 | Revise named fields | **Not selected.** No query-level GSC export exists in this repo. Inventing a new title or description would be speculation. The approved strings still name the query more honestly than the last-live zombies excerpt. |
| 3 | No edit | **Not selected.** "No edit" would freeze a title that still drops "for You" and two still-unlinked source phrases. The pending overwrite and two wraps remain the smallest useful on-page move. |

PR #1000 delivered the same recommendation on 2026-09-08 and deliberately did **not** close #994, because query-level GSC was missing. That gap is still missing (no committed export). #994's own close rule is a defensible diagnosis plus a retain / revise-named-fields / no-edit recommendation; live publication is outside completion. This file plus the retain proposal are that packet.

Live publication remains out of scope. #339 still owns the apply. #339 must refresh the drifted post-12327 `modified` / raw-hash guard immediately before any future write.

---

## 0. Hard gates for this session

| Gate | This session |
|---|---|
| Outbound HTTP (`curl`, `make status-readonly`, `make seo-publisher-smoke`, live `style.css` readback) | **Not run.** Hard-gated. |
| Signed-in or API Search Console | **Absent.** `.env.schema` still defines no GSC secret. No committed page+query export for this URL exists. |
| WordPress admin / REST write / Code Snippets activate | **Not done.** |
| Invented query names, positions, device/country splits, or branded CTR | **Forbidden.** Not invented. |
| #339 packet / #336 fixtures / #1030 matrix edits | **Not done.** Other lanes. |

Everything below is dated in-repo evidence plus the issue body's Sep 6 page totals. This session does not claim a 2026-09-20 live title.

---

## 1. Identities (repo + last live snapshot)

Slug, ID, and URL still match #336 / #339 in every committed capture. #1030's 2026-09-18 identity table reconfirmed the same 8802 row without a new title/description readback.

| Role | ID | Slug | Last `modified` in-repo | Packet guard | Identity |
|---|---:|---|---|---|---|
| Target | 8802 | `how-to-build-an-ai-second-brain-that-actually-works-for-you` | `2026-06-28T20:27:34` (2026-09-08 live = packet) | `2026-06-28T20:27:34` | **match** through 2026-09-08; ID/slug/URL reconfirmed 2026-09-18 |
| Source 1 | 9774 | `what-journalists-need-to-know-about-ai-right-now` | `2026-06-14T20:05:53` (2026-09-08 live = packet) | `2026-06-14T20:05:53` | **match** through 2026-09-08 |
| Source 2 | 12327 | `storyhive-haus-of-owl-jordan-dack` | `2026-09-07T13:07:06` (2026-09-08 live) | `2026-08-16T21:03:50` | **ID/slug/URL match; modified drifted** |

Post 12327's FIND needle `knowledge bases and named assistants` was still present once and still unlinked on 2026-09-08. The wrap copy is not superseded. The stale `modified` / raw-hash pair in `apply-336-ai-second-brain.md` and `manifest.json` is a **publisher precondition for #339**, not a reason to change the replacement HTML. Do not PATCH 12327 from this issue.

Do not treat repo Aurora `theme/kk-aurora/style.css` Version **1.6.12** as production proof. The 2026-09-08 live/repo pair was `1.6.11`.

---

## 2. Last live vs #336 / #339 field status

Public HTML was authoritative on 2026-09-08. This session did not re-fetch. #336 closed 2026-07-13 after PR #337 merged the **prep** handoff. That close is not a live-apply receipt. No later `*applied*` receipt in `docs/current-state/reports/` names post 8802.

| Field | Last live 2026-09-08 | #336 / #339 approved | Status |
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
| Target in `wp-sitemap-posts-post-1.xml` | yes; lastmod `2026-06-28T20:27:34-08:00` | expected | applied as of 2026-09-08 |
| `?p=8802` | 200 at the pretty permalink | expected | applied as of 2026-09-08 |
| `robots.txt` | allows the URL; disallows only `/wp-admin/`, `/?s=`, `/search/` | expected | applied as of 2026-09-08 |

July 13 public state said "no standard meta description." That is **superseded as a live fact** by the 2026-08-16 compact capture and the 2026-09-08 readback: Aurora emits one `<meta name="description">` from the stored `advanced_seo_description`. The stored value is still the unapproved zombies excerpt, so the #339 overwrite is still required. Public REST exposes `jetpack_seo_html_title` and `advanced_seo_description` for posts (`theme/kk-aurora/inc/seo-meta-rest.php`). The July "fields unregistered" warning is historical; overwrite mode is still required because both keys are non-empty.

`make seo-audit` remains a false-negative instrument after Jetpack deactivation ([SEO-STRIKING-DISTANCE-2026-08-02.md](../SEO-STRIKING-DISTANCE-2026-08-02.md)). Not used as evidence.

---

## 3. Search Console: dated page totals only

### 3a. Still missing (do not invent)

No GSC query / device / country export has been committed since PR #1000. This session did not open Search Console.

| Needed | Status |
|---|---|
| Exact-date page-filtered Queries for two complete 28-day windows | **Missing.** Pull A–D remain in §8. |
| Device / country / branded / non-branded split | **Missing.** |
| Average position for either Sep 6 window | **Not recorded** on that screen. |
| Named query-level losses | **Not available.** |

### 3b. Dated page-level aggregates that do exist

Two human-recorded page totals, both for property `sc-domain:kriskrug.co`. Neither is a query table.

| Source | Window | Page impressions | Page clicks | Implied CTR | Avg position |
|---|---|---:|---:|---:|---:|
| #336 / #279 digest-safe copy | 2026-06-12 to 2026-07-09 (exact dates) | 1,053 | 10 | 0.95% | 11.27 |
| #336 query `ai second brain` | same window | 46 | 2 | n/a | 17.52 |
| #994 issue body, signed-in UI displayed **2026-09-06** | GSC "last 28 days" vs previous period (`num_of_days=28&compare_date=PREV`) | 1,146 → 602 | 14 → 3 | 1.22% → 0.50% | **not recorded** |
| Same display, sitewide clicks | same compare | n/a | 172 → 168 | n/a | n/a |

Exact inclusive calendar dates for the Sep 6 compare were **not independently retrieved**. Typical GSC "last 28 days" vs previous, viewed 2026-09-06, is two adjacent 28-day windows ending on the last complete data day (often 2026-08-09–2026-09-05 vs 2026-07-12–2026-08-08). Treat that pair as **inferred UI convention**, not as a pulled export.

Longer history beyond those two windows: **not available here.**

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

**Do not blame #331 / #767 archive cleanup.** Those snippets deployed 2026-09-03 ([receipt](DEPLOY-767-331-2026-09-03.md)). A 28-day window displayed 2026-09-06 is almost entirely pre-deploy. GSC itself lags one to three days, so the latest window contains at most a few days after activation, and those days are incomplete. The issue already says the drop is not proof of noindex or of any deployment. Last public checks (2026-09-08) agree: the target was 200, self-canonical, indexable, and present in the post sitemap.

If a later Pull A shows the lost impressions are branded or off-intent, KK can reopen a **named-field** revision then. Until those rows exist, retain.

---

## 4. On-page and link-graph notes (not a rewrite brief)

From the 2026-09-08 live notes and later in-repo packets. Not re-fetched.

- Body ~1,250–1,350 words depending on chrome; JSON-LD `wordCount` 1255 on 2026-09-08. Eight topical H2s plus the About block. Answer-first lead is already the zombies excerpt.
- JSON-LD: BlogPosting + BreadcrumbList + Person/Organization. `BlogPosting.description` uses the excerpt, not the SEO description. Cosmetic, same pattern as other posts.
- Category `/category/generative-ai-tools/` is a listing link, not a contextual inbound.
- Hub `/ai-tools/` already contained one href to the target on 2026-09-08. #1030 (live-checked 2026-09-18) still records that card; the proposed retitle is **#1030**, not this lane.
- Contextual hrefs to the target already existed on posts 11878, 12183, 5823, 5590, 4948, and 4773. The #339 wraps on 9774 and 12327 are **additional** and were still absent on 2026-09-08. They are not duplicates of those existing hrefs.
- Post 12744 (`what-i-showed-founders-about-ai-workflows`) mentioned "second brain" once with zero hrefs to 8802 as of 2026-09-08. #1030 later drafted that wrap. Parked. Do not add a third source here. #402 stays parked.

None of that is a noindex, canonical, or "the article disappeared" defect.

---

## 5. Compact evidence table

| Check | Result | Bearing on the decline |
|---|---|---|
| Target identity 8802 / slug / URL | match through 2026-09-08; ID/slug/URL reconfirmed 2026-09-18 | same URL Google already has |
| Last live `<title>` vs approved | missing "for You" | pending CTR/intent tweak, not a live regression from #339 |
| Last live description vs approved | still zombies excerpt | pending; not applied |
| Canonical / robots / sitemap (2026-09-08) | clean, indexable | rules out noindex / wrong-canonical as the cause |
| 9774 / 12327 proposed wraps | still unlinked on 2026-09-08; needles once each | pending; 12327 `modified` drifted |
| Sitewide clicks Sep 6 compare | 172 → 168 | page-specific, not sitewide |
| Page clicks / impressions Sep 6 compare | 14 → 3 / 1,146 → 602 | dated human GSC UI; query rows missing |
| June 12–Jul 9 page | 10 / 1,053 / pos 11.27 | older baseline; previous-28 on Sep 6 was actually higher |
| #331 deploy 2026-09-03 | archives noindex; posts still indexed | window is largely pre-deploy; do not assign cause |
| Query-level losses | **blocked** | see §3 |
| Later #1030 extra inbounds / outbounds | drafted 2026-09-18; not this packet | do not expand the #339 source set here |

---

## 6. Why retain, not revise

The approved title restores the article's own promise ("for You") in the SERP title. The approved description names second-brain outcomes that the body already claims (thought patterns, creative chaos, notes, voice memos, finished work). Both are still better query-aligned than the last-live strings, and both are still unshipped as of the last live readback plus the absence of an apply receipt.

Revising them now would create a second publishing packet for the same post while #339 is still waiting on KK ticks. That is the duplication #994 forbids.

The issue-specific proposal at `content/drafts/issue-994-second-brain/proposal.md` records that decision as a **zero named-field delta** against the existing package. It is a refresh, not a competing overwrite.

---

## 7. Measurement protocol (after an eventual approved publish)

Do not start the clock on this diagnosis. Start it only after KK approves and a publisher session applies the #339 8802 / 9774 / 12327 fields, public HTML confirms the approved title/description and the two hrefs, and Google has had time to recrawl.

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

## 8. Exact GSC pull for KK (unblocks §3c; does not block this close)

Search Console → Performance → Search results. Property `sc-domain:kriskrug.co`. All four metric toggles on.

**Pull A.** Filter Page = exact `https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/`. Custom dates, two complete 28-day windows that match the Sep 6 compare (read the date chips; do not assume). Export Queries for each window. Note device and country only if a single slice is material.

**Pull B.** Same page filter, Queries contains `second brain` (and a second pass for `second mind` if rows appear).

**Pull C.** Cannibalisation: keep the query filter, switch to Pages. If another URL is taking the impressions, say so. Candidates to look at, not to assume: `/ai-tools/`, `/2026/06/13/speak-it-into-existence-ai-voice-first-workflows/`, `/2026/09/03/what-i-showed-founders-about-ai-workflows/`.

**Pull D.** Sitewide Search results for the same two windows (already 172 vs 168 clicks on Sep 6) so the page drop stays in context.

Paste digest-safe aggregates onto #339 or a later apply note. No raw export in git.

---

## 9. Cross-links and ownership

| Issue | Role after this report |
|---|---|
| #994 | Diagnosis + retain proposal. This PR closes the preparation issue. |
| #339 | Still the apply owner. Refresh 12327 `modified` / raw hash immediately before any dry-run. Do not apply from this PR. |
| #336 | Closed prep. Historical evidence + locked test fixtures. Not a live-apply receipt. |
| #402 | Parked. Surprising-winner hub work. Do not expand here. |
| #1030 | Later cross-link matrix. Extra Second Brain inbounds/outbounds stay there. |
| #331 / #767 | Deployed 2026-09-03. Not assigned as the cause of this page drop. |
| #274 / #995 / #996 / #997 / #1025 | Independent lanes. Not started from this file. |

---

## 10. Acceptance criteria

| #994 criterion | Status |
|---|---|
| Verify target identity, last title/description/body/canonical/robots, and the two proposed inbound links vs #336/#339 | **MET** from the 2026-09-08 live snapshot + later identity reconfirm. This session did not re-fetch; §1 states the drift risk. |
| Retrieve exact-date page-filtered GSC query comparisons | **NOT MET** (access still missing). Gap recorded in §3a. Pull spec in §8. Not a live-write blocker. |
| At most five query-level losses; distinguish ranking / demand / CTR / mix; do not blame archive cleanup | **MET** as "cannot name five" plus the effect table. #331 not assigned as cause. |
| Deliver `docs/current-state/reports/issue-<n>-second-brain-diagnosis-YYYYMMDD.md` with evidence table + ranked retain / revise / no-edit | **MET** (this file) |
| If change warranted: exact before/after delta vs existing package, this article + ≤2 sources, issue-specific proposal | **MET** as retain. Proposal records a **zero named-field delta**. #339 packet not overwritten. |
| Measurement protocol after ≥14 full days following approved publication/recrawl | **MET** in §7 |
| Cross-link #339 and #402; live publication outside completion | **MET** |

This packet **closes #994**. Apply / reject of the #339 8802 / 9774 / 12327 fields is a separate publisher decision.

---

## 11. Scope and safety

No POST, PATCH, PUT, or DELETE against kriskrug.co. No theme deploy, SFTP, snippet edit, cache purge, indexing request, or Validate Fix. No secrets printed. The #336 unit-test fixtures and the #339 packet were **not** modified. Other-lane proposal files (#274 / #331 / #339 / #402 / #995 / #996 / #997 / #1025 / #1030) were not edited.

### Session verification (2026-09-20)

| Check | Result |
|---|---|
| Outbound live verification | **Skipped** (hard gate). |
| `make doctor` / `make status-readonly` / `make seo-publisher-smoke` | **Skipped** (those targets make live HTTP). |
| Packet / fixture review | #339 `apply-336-ai-second-brain.md`, `seo-meta-overwrite.json`, `manifest.json`; #336 handoff md/json; 2026-09-08 diagnosis; #1030 identity table |
| Theme ownership review | `theme/kk-aurora/inc/seo-title.php`, `inc/seo-meta-rest.php` (post keys only) |
| `python3 -m unittest scripts.tests.test_issue_336_ai_second_brain_seo_handoff -v` | fixtures unchanged; run after these docs |
| `git diff --check` | clean after these files |

### Follow-ups that are not this PR

1. KK Pull A–D in §8 so query-level losses can be named (optional; can confirm or reopen a named-field revision).
2. #339 publisher session: snapshot 8802 / 9774 / 12327, refresh 12327 guards, apply only after ticks.
3. Optional later: extra wraps from #1030 (12744 / 12263 / 11878 retitle). Not now. Not a third source in the #339 packet.
