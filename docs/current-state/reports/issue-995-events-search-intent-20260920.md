# Issue #995: Events search click-through — in-repo closeout

**Captured:** 2026-09-20 (UTC)
**Mode:** Track A, **in-repo only**. No outbound HTTP. No live GSC pull. No WordPress admin, REST write, cache purge, indexing request, or Validate Fix.
**Closes:** [#995](https://github.com/WalksWithASwagger/kriskrug-wp/issues/995) as a preparation issue. Live snippet activate is a later KK-gated act and is not this PR.
**Prior live-readback:** [`issue-995-events-search-intent-20260908.md`](issue-995-events-search-intent-20260908.md) (merged PR #1010, `Refs #995`). That file remains the last public-HTML / public-REST snapshot. This file does not re-fetch it.
**Refs:** #832 (closed meetup → `/events/` routing), #331 / #767 (archive policy live 2026-09-03), #635 (exclusive events-catalog / page-2250 **body** owner). Do not start #274, #339, #402, #994, #996, #997, or #1025 from this file.

**Target:** `https://kriskrug.co/events/` (WordPress page **2250**, slug `events`)

---

## Ranked recommendation

**Prepare one page-2250 title + description overwrite.** Do not add internal links. Do not edit event artboards, dates, registration destinations, or page design. Do not write live WordPress from this PR.

| Rank | Choice | Verdict |
|---|---|---|
| 1 | Scoped title + description for page 2250 | **SELECTED.** Last live `<title>` (2026-09-08) is the theme fallback `Events \| Kris Krüg` (18). Last live description is a 200-character mash of kicker + H2 + lede, truncated mid-word. Dated GSC page totals from the issue body (displayed 2026-09-06) show impressions 188 → 423 and clicks 6 → 5. That is a snippet / mix problem on a crawl-healthy URL, not a noindex or canonical defect. |
| 2 | Add contextual internal links | **Not selected.** #832 already staged and closed the recap → `/events/` routing. In-repo payloads and the 2026-09-08 live check both show those wraps. Extra inbound will not repair a 5-vs-6 click sample. |
| 3 | No edit | **Not selected.** Leaving the generic fallback title wastes the impression gain. The proposed strings only name rooms the 2026-09-13 repo shell already lists. They do not invent dates or availability. |

The paste-ready apply vehicle is already in-repo: [`fixes/issue-995-events-search-snippet.php`](../../../fixes/issue-995-events-search-snippet.php) (**not live**). The markdown proposal is §7 below. Activate only after KK approval, a fresh page-2250 snapshot, and a stated rollback.

PR #1010 delivered the same recommendation on 2026-09-08 and deliberately did **not** close #995, because query-level GSC was missing. That gap is still missing (no committed export). #995's own close rule is a reviewable Track A packet or a supported no-change verdict; no live write is required. This file is that packet.

---

## 0. Hard gates for this session

| Gate | This session |
|---|---|
| Outbound HTTP (`curl`, `make status-readonly`, `make seo-publisher-smoke`, live `style.css` readback) | **Not run.** Hard-gated. |
| Signed-in or API Search Console | **Absent.** `.env.schema` still defines no GSC secret. No committed `/events/` query export exists. |
| WordPress admin / REST write / Code Snippets activate | **Not done.** |
| Invented query names, positions, device/country splits, or branded CTR | **Forbidden.** Not invented. |
| Theme / catalog / page-2250 body edits | **Not done.** #635 owns the body. |

Everything below is dated in-repo evidence plus the issue body's Sep 6 page totals. Where the 2026-09-08 live snapshot and the current repo shell disagree, this file says so and does not pick a live winner.

---

## 1. Identity (repo + last live snapshot)

| Field | In-repo evidence | Last live (2026-09-08, not re-fetched) |
|---|---|---|
| ID | `scripts/events_page/events-catalog.yaml` `page_id: 2250`; #832 snapshot `content/drafts/2026-08-02-seo-authority-hubs/fix-832/before/page-2250-identity.json` | **2250** |
| Slug | catalog `page_slug: events`; #832 snapshot `events` | `events` |
| Status | #832 snapshot `publish` | `publish` |
| URL | catalog + snapshots | `https://kriskrug.co/events/` |
| Page title | #832 snapshot `title_rendered: Events`; shell H2 is not the WP title | `Events` (H1) |
| `modified` | #832 snapshot `2026-08-10T10:38:46` (older fixture) | `2026-09-07T12:58:41` (`modified_gmt` `2026-09-07T20:58:41`) |
| Public REST `meta` | not re-read | `{"footnotes":""}` only |
| Public HTML SHA-256 | not re-hashed | `16b1426ed14735d4114c372992a4ae975f6a8a631925551950620aaee2a17e0e` (136,885 bytes) |
| `?p=2250` | not re-fetched | **301** → `/events/` |

The Sep 6 GSC display is **before** the 2026-09-07 save recorded on 2026-09-08. The repo events pipeline then moved again on **2026-09-13** (`scripts/events_page/README.md`: masthead / rooms / contact-sheet layout; *Stages I speak on* and *Signature moments* folded into the catalog). This session cannot say whether that body is live. **Before any activate:** abort unless authenticated GET page 2250 still has `id=2250` and `slug=events`. Treat the then-current `modified` as the snapshot guard, not the 2026-09-07 stamp.

#635 remains the only issue allowed to mutate the events catalog, event media, or page 2250 **body**. This lane proposes metadata only.

Repo Aurora `theme/kk-aurora/style.css` Version is now **1.6.12**. The 2026-09-08 live/repo pair was `1.6.11`. Do not treat the repo Version as production proof.

---

## 2. Metadata ownership (theme source, not Jetpack)

Public HTML is authoritative when a live session can fetch it. This session uses the theme and snippet sources.

| Output | Owner in repo | What that means for page 2250 |
|---|---|---|
| Fallback `<title>` | `KK_Aurora\filter_document_title_parts` + `filter_document_title_separator` in `theme/kk-aurora/functions.php` | Inner pages get `{page title} \| Kris Krüg`. For title `Events` that is `Events \| Kris Krüg`. Matches the 2026-09-08 live title. |
| Approved-title override | `KK_Aurora\filter_pre_get_document_title` in `theme/kk-aurora/inc/seo-title.php` | Replaces the **whole** document title when `jetpack_seo_html_title` is a non-empty string. The 2026-09-08 live title was exactly the fallback, so that meta was empty or unused. |
| `<meta name="description">` | `KK_Aurora\public_meta_description()` in `functions.php` | Singular path: `advanced_seo_description` → excerpt → `wp_trim_words(content, 40)`, then `mb_substr(..., 0, 300)`. The 2026-09-08 200-character mash with a trailing ellipsis is the excerpt/content-trim path, not a curated SEO string. |
| `og:title` | `KK_Aurora\social_meta_tags()` | Singulars overwrite `og:title` with `get_the_title()`. Stays `Events` unless the WP page title changes. This lane does not change the page title. |
| `og:description` / Twitter | same `public_meta_description()` | Follows the standard description. |
| REST read/write of those keys on **pages** | `theme/kk-aurora/inc/seo-meta-rest.php` | Registers `jetpack_seo_html_title` and `advanced_seo_description` for `post` **only**. A REST PATCH of page 2250 `meta` would silently drop those keys. |
| Jetpack SEO plugin | not the render path | `SEO-STRIKING-DISTANCE-2026-08-02.md` records Jetpack inactive and `GET /wp-json/jetpack/v4/settings` 404. Do not assume Jetpack owns titles. |
| Code Snippet 12 (`fixes/og-restore-snippet.php`) | **must stay inactive** | Activating it defines `KK_OG_SNIPPET_ACTIVE` and makes the theme stand down. Do not pair with the #995 snippet. |
| `make seo-audit` | false-negative instrument | Still reports missing Jetpack fields after deactivation. Not used as evidence. |

**Apply implication:** do not invent a second `<meta name="description">`. Feed the two keys Aurora already reads. Because page meta is not REST-registered, the prep vehicle is a page-2250-only Code Snippet (`get_post_metadata` short-circuit), not a page PATCH.

---

## 3. What the snippet may honestly name (repo shell, 2026-09-13)

Evergreen copy lives in `scripts/events_page/shell-events-2250.html`. Dated cards live in `scripts/events_page/events-catalog.yaml` and are **out of the snippet**.

**Masthead (shell):**

- Kicker: `Events I build, host & speak at`
- H2: `I don't just attend the AI conversation. I host the room.`
- Lede: monthly Vancouver meetup, film-club screenings, weekly office hours, keynote stages from São Paulo to Whistler. Most of it runs on Luma.
- CTAs: `https://lu.ma/vancouver-ai`, `/speaking/`

**Series I produce & host (shell):**

| Room | Cadence on page | Destination in shell |
|---|---|---|
| Vancouver AI Community Meetup | Monthly · Vancouver | `https://lu.ma/vancouver-ai` |
| BC + AI Office Hours | Weekly · Online; body says every Friday | `https://lu.ma/bcai` |
| AI Film Club | Monthly · Multimodal Media Lab | `https://lu.ma/film` |
| Special-interest groups | Ongoing · BC + AI | `https://bc-ai.ca/` |

The proposed description names meetup / film club / Friday office hours / stages. That set is on this shell. It does **not** name SIGs, Luma, or `/speaking/` as search promises.

**Catalog rows the snippet must not freeze** (confirmed or proposed, still `bucket_hint: upcoming` in the YAML as of this write; several are already past today's date and are #635 rolloff work, not this lane):

| Catalog id | Why it stays out of metadata |
|---|---|
| `how-can-we-help-pitch-night-2026` (Sep 8) | Dated one-off; already past as of 2026-09-20 |
| `trecsa-world-tourism-day-2026` (Sep 25) | Dated keynote; do not promise tickets |
| `vancouver-ai-meetup-2026-09-30` | Dated edition of a series the snippet already names generically |
| `futureproof-festival-2026` (Oct 28–30) | Dated festival |
| `2026-11-23-ampa-magazines-webinar` | Dated external webinar |
| `trunorth-ai-leadership-summit-2026` | `status: proposed`; role TBD — **do not publish a claim** |

Registration destinations stay on the page. The snippet only says registration links live there.

JSON-LD: the 2026-09-08 live head had Person + Organization + BreadcrumbList and **no** `Event` schema. Adding Event schema is out of scope.

---

## 4. Search Console: dated page totals only

### 4a. Still missing (do not invent)

No GSC query / device / country export has been committed since PR #1010. This session did not open Search Console.

| Needed | Status |
|---|---|
| Exact-date page-filtered Queries for both 28-day windows | **Missing.** Pull A–D remain in §8. |
| Device / country / branded split | **Missing.** |
| Average position | **Not recorded** on the Sep 6 screen. |
| Named top-opportunity queries | **Not available.** |

### 4b. Dated page-level aggregates that do exist

Human-recorded on issue #995 from signed-in property `sc-domain:kriskrug.co`, displayed **2026-09-06**, Performance → Search results, page breakdown, `num_of_days=28&compare_date=PREV`.

| Source | Window | Page impressions | Page clicks | Implied CTR | Avg position |
|---|---|---:|---:|---:|---:|
| #995 issue body | GSC "last 28 days" vs previous period | 188 → **423** | 6 → **5** | 3.19% → **1.18%** | **not recorded** |

Exact inclusive calendar dates were not independently retrieved. Typical GSC "last 28 days" vs previous, viewed 2026-09-06, is two adjacent 28-day windows ending on the last complete data day (often 2026-08-09–2026-09-05 vs 2026-07-12–2026-08-08). Treat that pair as **inferred UI convention**, not as a pulled export.

This is **not** the homepage seven-day impression-drop alert. Do not mix those windows.

### 4c. What the page totals can and cannot distinguish

| Effect | What the dated totals show | What they do not show |
|---|---|---|
| Exposure | Impressions more than doubled (+125%). | Whether new impressions are event/booking, branded navigational, or low-relevance leftovers. |
| Clicks | 6 → 5. Absolute change is noise on a single-digit sample. | Whether any named query gained or lost a click. |
| CTR | Supported at page level: 3.19% → 1.18%. Clicks did not rise with impressions. | Cannot split snippet CTR from position-driven CTR or from a mix shift. |
| Crawl / index | 2026-09-08 public checks: 200, self-canonical, `robots` `max-image-preview:large`, in the page sitemap. | Not re-verified 2026-09-20. |

**Do not blame #331 / #767.** Those snippets deployed 2026-09-03 ([receipt](DEPLOY-767-331-2026-09-03.md)). A 28-day window displayed 2026-09-06 is almost entirely pre-deploy. `/category/events-reports/` is an intentional noindex archive, not a competing indexable Events URL.

If a later Pull A shows the new impressions are branded navigational with healthy CTR, KK can reject the snippet. If they are `vancouver ai meetup` / booking-shaped with impressions and no clicks, ship it. If they are off-intent junk, stand the proposal down. Absence of that pull is not a reason to keep the generic fallback title.

---

## 5. Nearby URLs (cannibalisation candidates)

From the 2026-09-08 live table and in-repo hub drafts. Not re-fetched.

| URL | ID | Last recorded title | Role vs `/events/` |
|---|---:|---|---|
| `/events/` | 2250 | `Events \| Kris Krüg` | Live calendar + hosted-series page |
| `/ai-events/` | 12317 | `AI Events & Recaps: Web Summit, Hackathons, Meetups` | Recap / survival-guide hub. Last live body had **nav only** to `/events/`. |
| `/vancouver-ai/` | 12315 | `Vancouver AI Ecosystem: BC's Grassroots AI Hub \| Kris Krüg` | Ecosystem hub. #832 wrap: `the calendar` → `/events/`. Also `Browse AI events` → `/ai-events/`. |
| `/speaking/` | 1887 | `AI Keynote Speaker Kris Krüg \| Humanizing AI, Creativity & Community` | Booking page. Last live wrap: `Kris Krüg’s event archive` → `/events/`. |
| `/category/events-reports/` | n/a | `Events & Reports \| Kris Krüg` | Archive. 2026-09-08 cache-busted robots: `noindex, follow`. Keep the exclusion. |

`/ai-events/` is the honest cannibalisation check for Pull C. Its title already names "AI Events". That is a reason to make the `/events/` title say **host / calendar**, not a reason to retitle `/ai-events/` in this lane.

---

## 6. Internal links: no discovery-gap write

#832 is closed in [`WORK-PLAN-2026-09-09.md`](../WORK-PLAN-2026-09-09.md). In-repo after-payloads still carry the matrix anchors:

| Source | Contextual `/events/` anchor in `fix-832/after/` |
|---|---|
| 4495 inaugural meetup | `we still do this every month, and the next one is on the calendar` |
| 9197 meetup 16 | `the next one` |
| 8418 February recap | `come to the next one` |
| 6815 August recap | `the current calendar` |
| 6251 June 2024 highlights | `where the next one lands` |
| 5768 June recap | `still monthly, still free, still worth the trip` |
| 4348 2024 directory | `the live calendar, which is the version that stays current` |
| `/vancouver-ai/` (12315) | `the calendar` |

The 2026-09-08 live HTML still had those wraps plus `/speaking/`. Homepage / About / Contact were nav-only. `/ai-events/` was nav-only. A calendar sentence on `/ai-events/` remains a #402-shaped extras pass, not a demonstrated #995 discovery defect. `/events/` already had 423 impressions.

---

## 7. Scoped snippet proposal (markdown)

H1, page title, slug, body, artboards, `data-event-end` cards, and registration hrefs stay untouched.

### 7a. Fields

| Field | Current (last live HTML, 2026-09-08) | Proposed | Chars |
|---|---|---|---:|
| `<title>` / `jetpack_seo_html_title` | `Events \| Kris Krüg` | `Vancouver AI Events I Host \| Kris Krüg` | 18 → 38 |
| `<meta name="description">` / `advanced_seo_description` | 200-char kicker+H2+lede mash, ends `São Pau…` | `Monthly Vancouver AI meetups, film-club screenings, Friday office hours, and keynote stages I host or speak at. Registration links live on this page.` | 200 → 149 |
| `og:description` / Twitter | follows current description | will follow the new description through the theme | 149 |
| `og:title` | `Events` | **leave.** Theme uses `get_the_title()`. | 6 |
| H1 | `Events` | leave | 6 |
| Body / catalog | last live 2026-09-07 save; repo shell 2026-09-13 | leave. #635 owns it. | n/a |

Why these strings:

- They name rooms the 2026-09-13 shell still lists (monthly Vancouver meetup, film club, Friday office hours, stages).
- They do not name Pitch Night, Sep 25, Sep 30, Futureproof, AMPA, TruNorth, or "tickets still available".
- They distinguish the page from `/ai-events/` recaps without attacking that URL.
- They stay inside normal SERP truncation. No em dashes.

The 2026-09-13 lede says "weekly office hours"; the rooms list says "Every Friday". "Friday office hours" is the more specific honest phrase and still matches the shell.

### 7b. Ownership of the future write

| Step | Owner |
|---|---|
| Review + approve strings | KK |
| Snapshot page 2250 (`id`, `slug`, `modified`, `content.raw`) | Publisher session |
| Paste / activate snippet | KK in Code Snippets. Run everywhere (front-end). Strip the opening `<?php` on paste. |
| Render after activation | Aurora, via the existing `get_post_meta` reads |
| Pagely purge | KK, if edge HTML stays stale |
| Persist into post meta later | Optional follow-up. Requires registering the two keys for `page` or WP-CLI. Not this PR. |

### 7c. Snapshot / readback / rollback

1. Before activate: authenticated GET page 2250. Abort if `id` ≠ 2250 or `slug` ≠ `events`. Record the **then-current** `modified` (do not reuse 2026-09-07 if the 2026-09-13 body landed). Keep the snapshot until the measurement window ends.
2. Confirm public HTML SHA or at least title + description + canonical.
3. Activate [`fixes/issue-995-events-search-snippet.php`](../../../fixes/issue-995-events-search-snippet.php). Do not PATCH `content`.
4. Logged-out readback, plain and `?cb=<ts>`: title and standard description must match the proposed strings; H1 still `Events`; registration hrefs unchanged; canonical still self; robots still indexable.
5. Rollback: deactivate the snippet. Title/description return to the theme fallback / content-trim path. No database restore required unless a later session also wrote post meta.

### 7d. Snippet contract (already in PHP; do not rewrite)

The existing prep file is the apply vehicle. Behaviour, unchanged:

- Filter `get_post_metadata` at priority 10.
- No-op unless `(int) $object_id === 2250`.
- Only short-circuit `jetpack_seo_html_title` and `advanced_seo_description`.
- Return a string when `$single` is true, or a one-item array when false.
- Do not print a second meta tag. Do not change `og:title`. Do not hard-code dates.

Conflict: snippet 12 (`og-restore-snippet.php`) must remain inactive.

---

## 8. Exact GSC pull for KK (names queries; does not block this close)

Search Console → Performance → Search results. Property `sc-domain:kriskrug.co`. All four metric toggles on.

**Pull A.** Filter Page = exact `https://kriskrug.co/events/`. Custom dates matching the Sep 6 compare (read the date chips; do not assume). Export Queries for each 28-day window. Note device and country only if one slice dominates.

**Pull B.** Same page filter, Queries contains `event` / `meetup` / `vancouver ai` (separate passes). Mark zero-click rows.

**Pull C.** Cannibalisation: keep a query filter, switch to Pages. Candidates to look at, not to assume: `/ai-events/`, `/vancouver-ai/`, `/speaking/`, individual recap posts.

**Pull D.** Sitewide Search results for the same two windows so the page movement stays in context. Keep the homepage seven-day alert on a different ticket.

Paste digest-safe aggregates onto a later note or a new apply issue. No raw export in git.

---

## 9. Measurement protocol (after an approved activate)

Do not start the clock on this diagnosis. Start it only after KK approves, the snippet is active, public HTML confirms the proposed title and description, and Google has had time to recrawl.

1. Wait **at least 14 full days** after that public readback. Prefer two **complete** 28-day windows that do not straddle the activate day.
2. Property: `sc-domain:kriskrug.co`. Report: Search results. Page filter = exact `https://kriskrug.co/events/`.
3. Record page clicks, impressions, CTR, average position.
4. Queries tab, same page filter: every matched row for `vancouver ai meetup`, `vancouver ai events`, and the top losses/gains by impression delta (cap discussion at five queries). Compare like-for-like query groups, not only page totals.
5. Count **non-branded clicks** only from those query rows (queries that are not `kris krug` / `kriskrug` variants). Do not invent a branded split if the export is not opened.
6. Registration / enquiry outcomes: Luma and Eventbrite are off-site. This repo has no registration counter for `/events/`. Record Luma/Eventbrite registrations or speaking enquiries **only if KK already has that measurement**. Do not install analytics from this issue. Do not attribute a registration to the snippet without a matching date and a named landing URL.
7. Event timing: single-digit clicks will move when a meetup or festival is close. Compare the same query set, and say when a window contains a listed room. Do not treat 5 vs 6 as a win or a loss.
8. Baseline to beat, dated Sep 6 display only: 423 impressions / 5 clicks / 1.18% CTR in the latest 28 days, versus 188 / 6 / 3.19% in the previous 28. Success is a defensible before/after on matched queries, not a promised rank increase.

---

## 10. Acceptance criteria

| #995 criterion | Status |
|---|---|
| Refresh `/events/` identity, owner, metadata, canonical/robots, modified/hash; say who owns title/description | **MET** from theme source + last live snapshot. This session did not re-fetch; §1 states the drift risk. |
| Compare exact-date GSC page-filtered query / device / country rows | **NOT MET** (access still missing). Gap recorded in §4a. Pull spec in §8. Not a live-write blocker. |
| Report with top opportunity queries or GSC-missing notes, plus change/no-change | **MET** as GSC-missing notes + ranked recommendation |
| If justified: one honest title + description; links only if discovery gap; exact fields; ownership; snapshot/readback/rollback | **MET** for title/description. Links: evidence-backed **no-add** |
| Preserve artboards, dates, registration destinations, page design; no invented availability | **MET** (no body write; dates kept out of the snippet) |
| Post-approval measurement protocol | **MET** in §9 |
| Reviewable Track A packet; no live write | **MET** |

This packet **closes #995**. Activate / reject of the snippet is a separate publisher decision.

---

## 11. Scope and safety

No POST, PATCH, PUT, or DELETE against kriskrug.co. No theme deploy, SFTP, snippet activate, cache purge, indexing request, or Validate Fix. No secrets printed. Other-lane proposal files (#274 / #331 / #339 / #402 / #994 / #996 / #997 / #1025) were not edited.

### Session verification (2026-09-20)

| Check | Result |
|---|---|
| Outbound live verification | **Skipped** (hard gate). |
| `make doctor` / `make status-readonly` / `make seo-publisher-smoke` | **Skipped** (those targets make live HTTP). |
| Theme / snippet ownership review | `seo-title.php`, `seo-meta-rest.php`, `functions.php` title/description/OG paths, `fixes/issue-995-events-search-snippet.php` |
| Events copy review | `scripts/events_page/shell-events-2250.html`, `events-catalog.yaml`, `scripts/events_page/README.md` |
| #832 routing review | `content/drafts/2026-08-02-seo-authority-hubs/fix-832/` + work-plan closed state |
| `php -l` snippet | **Skipped.** `php` is not on PATH in this image. Snippet logic is unchanged. CI `php-validation` already covers `fixes/`. |
| `git diff --check` | clean after these files |

### Follow-ups that are not this PR

1. KK Pull A–D in §8 so opportunity queries can be named (optional; can reject or confirm the snippet).
2. KK approve + activate `fixes/issue-995-events-search-snippet.php` in a publisher session, or reject it if Pull A shows branded/off-intent impressions.
3. Optional later: persist the same two strings into page 2250 post meta and deactivate the snippet. Needs a `page` meta registration or WP-CLI. Track A, separate approval.
4. `/ai-events/` contextual calendar sentence: park under #402. Not started here.
5. Catalog `bucket_hint: upcoming` rows whose dates are already past: #635 rolloff, not this lane.
