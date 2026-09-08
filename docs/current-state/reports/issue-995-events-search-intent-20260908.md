# Issue #995: Events search click-through diagnosis

**Captured:** 2026-09-08T06:18Z (UTC)
**Mode:** Track A, read-only. Public HTML (plain + cache-busted), public REST GET, sitemap/robots. Zero WordPress writes. Zero cache purges. Zero Search Console submits / Validate Fix.
**Refs:** #995 (this diagnosis), #832 (closed meetup → `/events/` routing), #331 / #767 (archive policy live 2026-09-03), #635 (exclusive events-catalog owner). Do not start #274, #339, #402, #994, #996, or #997 from this file.
**Target:** https://kriskrug.co/events/ (WordPress page **2250**, slug `events`)

## Ranked recommendation

**Prepare one page-2250 title + description overwrite.** Do not add internal links. Do not edit event artboards, dates, or registration destinations. Do not write live WordPress from this PR.

| Rank | Choice | Verdict |
|---|---|---|
| 1 | Scoped title + description for page 2250 | **SELECTED.** Live `<title>` is the theme fallback `Events \| Kris Krüg` (18). The standard description is a 200-character mash of kicker + H2 + opening copy, truncated mid-word. Impressions rose 188 → 423 while clicks stayed 6 → 5. That is a snippet / mix problem, not a crawl defect. |
| 2 | Add contextual internal links | **Not selected.** Discovery to `/events/` is already in place after #832. Recap posts, `/vancouver-ai/`, and `/speaking/` already carry contextual hrefs. Homepage / About / Contact only expose the nav item. Extra inbound will not fix a 5-vs-6 click sample. |
| 3 | No edit | **Not selected.** Leaving the generic fallback title in place wastes the impression gain. The proposed strings only name rooms the live page already lists. They do not invent dates or availability. |

Live publication remains out of scope. The paste-ready snippet is `fixes/issue-995-events-search-snippet.php` (**not live**). Activate it only after KK approval, a page-2250 snapshot, and a stated rollback.

---

## 1. Identity, verified 2026-09-08

Public REST `GET /wp/v2/pages?slug=events` and `GET /wp/v2/pages/2250`, plus public HTML.

| Field | Live 2026-09-08 |
|---|---|
| ID | **2250** |
| Slug | `events` |
| Status | `publish` |
| URL | `https://kriskrug.co/events/` |
| Page title (H1 / `title.rendered`) | `Events` |
| `date` | `2016-01-26T11:11:40` |
| `modified` | `2026-09-07T12:58:41` (`modified_gmt` `2026-09-07T20:58:41`) |
| Sitemap lastmod | `2026-09-07T12:58:41-08:00` in `wp-sitemap-posts-page-1.xml` (46 pages) |
| Public REST `meta` | `{"footnotes":""}` only |
| Public HTML SHA-256 (plain and `?cb=`) | `16b1426ed14735d4114c372992a4ae975f6a8a631925551950620aaee2a17e0e` (136,885 bytes; identical) |

`?p=2250` **301** → `https://kriskrug.co/events/` (`x-redirect-by: WordPress`), then 200. `http://` and `www.` variants 301 to the same canonical.

The `modified` stamp is **after** the Sep 6 GSC display. This diagnosis treats the Sep 6 click/impression pair as pre-this-save evidence. I did not retrieve a Sep 6 HTML snapshot, so I do not claim what the 2026-09-07 save changed.

#635 remains the only issue allowed to mutate the events catalog, event media, or page 2250 **body**. This lane proposes metadata only.

---

## 2. Metadata ownership (do not assume Jetpack)

Public HTML is authoritative. Jetpack is **not** the live title/description owner.

| Output | What renders today | Owner |
|---|---|---|
| `<title>` | `Events \| Kris Krüg` | Aurora `filter_document_title_parts` + `filter_document_title_separator` (`theme/kk-aurora/functions.php`). Page title `Events` + pipe + `public_site_name()` `Kris Krüg`. |
| Approved-title override | **Not firing.** If `jetpack_seo_html_title` were non-empty, `theme/kk-aurora/inc/seo-title.php` would replace the whole document title. Live title is exactly the fallback, so that meta is empty or unused. |
| `<meta name="description">` | 200-char content trim with a trailing ellipsis | Aurora `public_meta_description()`: `advanced_seo_description` → excerpt → `wp_trim_words(content, 40)`. Matches the public excerpt, not a curated SEO string. |
| `og:title` | `Events` (bare page title) | Aurora `social_meta_tags()` uses `get_the_title()`, not the document title. Same pattern as other singulars. |
| `og:description` / Twitter | Same 200-char mash | Same `public_meta_description()` path. |
| REST read/write of those keys on **pages** | **Not registered.** `theme/kk-aurora/inc/seo-meta-rest.php` registers `jetpack_seo_html_title` and `advanced_seo_description` for `post` only. A REST PATCH of page 2250 `meta` would silently drop those keys. |
| Jetpack SEO plugin | Not the render path. Public `GET /wp-json/jetpack/v4/settings` is still a 404 `rest_no_route`. Site Kit `1.186.0` is in the head generators; that is analytics/GSC wiring, not the title tag. |
| Code Snippet 12 (`fixes/og-restore-snippet.php`) | Must stay **inactive**. Activating it makes the theme stand down and would fight this proposal. |

`make seo-audit` remains a false-negative instrument for missing Jetpack fields (see `SEO-STRIKING-DISTANCE-2026-08-02.md`). It was not used as evidence here.

**Apply implication:** do not invent a second `<meta name="description">`. Feed the two keys Aurora already reads. Because page meta is not REST-registered, the prep vehicle is a page-2250-only Code Snippet (`get_post_metadata` short-circuit), not a page PATCH.

---

## 3. Live head and journey, `/events/`

Plain and cache-busted fetches both HTTP 200 from `Pagely-ARES/1.22.28`. WordPress generator `7.0.4`. Live and repo Aurora `style.css` Version **1.6.11**.

| Field | Live 2026-09-08 |
|---|---|
| HTTP | 200 |
| Canonical | self, exactly one tag: `https://kriskrug.co/events/` |
| `robots` | `max-image-preview:large` (indexable; no `noindex`) |
| `googlebot` meta | absent |
| H1 | `Events` (one) |
| `<title>` | `Events \| Kris Krüg` (18) |
| Standard description | `Events I build, host & speak at I don’t just attend the AI conversation, I host the room. From a monthly Vancouver meetup to film-club screenings, weekly office hours, and keynote stages from São Pau…` (200, truncated) |
| In `wp-sitemap-posts-page-1.xml` | yes |
| `robots.txt` | allows `/events/`; disallows only `/wp-admin/`, `/?s=`, `/search/` |
| JSON-LD | Person + Organization + BreadcrumbList. No `Event` schema. Out of scope to add. |

Hero copy (unchanged vs `scripts/events_page/shell-events-2250.html`): monthly Vancouver meetup, film-club screenings, weekly office hours, keynote stages from São Paulo to Whistler. Primary CTA `https://lu.ma/vancouver-ai` (**301** → `https://luma.com/vancouver-ai`, then 200). Secondary CTA `/speaking/` (200).

**On the calendar when fetched (do not paste these dates into metadata):**

| Card | Label on page | Registration destination | Destination GET |
|---|---|---|---|
| How Can We Help? Pitch Night | Tuesday, Sept 8 · 6–9pm · BCIT Tech Collider | Eventbrite ticket URL | HTTP **429** from this session (rate-limited; not treated as down) |
| Vancouver AI Community Meetup | Wed, Sept 30 · Space Centre | `https://luma.com/sept-ai` | 200 |
| Futureproof Festival | Oct 28–30 · H.R. MacMillan Space Centre | `https://futureproof.website/` | 308 → `https://www.futureproof.website/` 200 |

Past grid is present (`data-event-end` count 67). Empty-hero class count **0**. Artboard markup is present. Recurring series still named on-page: Vancouver AI Community Meetup, BC + AI Office Hours, AI Film Club, SIGs. This proposal does not promise a room that is not already on the page, and it does not freeze the Sept 8 / Sept 30 / Oct 28 dates into the snippet.

---

## 4. Search Console: dated page totals vs blocked query rows

### 4a. Precise blocker for this session

I could not retrieve exact-date, page-filtered, query / device / country rows.

| Needed | Status in this Cloud session |
|---|---|
| GSC API / OAuth / service account | **Absent.** No `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_CREDENTIALS`, or Search Console env names. `.env.schema` does not define a GSC secret. |
| Signed-in GSC UI | **Not available** to this agent. |
| Committed page+query export for `/events/` | **Absent** from the repo. |
| WP credentials for Site Kit REST | **Absent.** `WP_USER` / `WP_APP_PASSWORD` and `WP_API_*` are unset. Site Kit is visible in public HTML (`1.186.0`) but its Search Console reports were not readable. |
| Context.dev MCP | Not used (auth not assumed). |
| Profound MCP | AI-visibility product, not `sc-domain:kriskrug.co` Search Console. Ready namespace, no GSC property client. |
| Ryze MCP | Not a GSC property client. |

Do not invent query names, positions, device splits, country splits, or branded/non-branded click counts. **Top opportunity queries: not available. Missing report is Pull A–D in §8.**

### 4b. Dated page-level aggregates that do exist

Human-recorded on issue #995 from a signed-in Search Console property `sc-domain:kriskrug.co`, displayed **2026-09-06**, Performance → Search results, page breakdown, `num_of_days=28&compare_date=PREV`.

| Source | Window | Page impressions | Page clicks | Implied CTR | Avg position |
|---|---|---:|---:|---:|---:|
| #995 issue body | GSC "last 28 days" vs previous period | 188 → **423** | 6 → **5** | 3.19% → **1.18%** | **not recorded** |

Exact inclusive calendar dates for that compare were **not independently retrieved**. Typical GSC "last 28 days" vs previous, viewed 2026-09-06, is two adjacent 28-day windows ending on the last complete data day (often 2026-08-09–2026-09-05 vs 2026-07-12–2026-08-08). Treat that pair as **inferred UI convention**, not as a pulled export. KK should save the report with the date chips visible.

Device, country, branded/non-branded, and query-mix: **not available here.**

Longer history beyond those two windows: **not available here.**

This is **not** the homepage seven-day impression-drop alert. Do not mix those windows.

### 4c. What the page totals can and cannot distinguish

| Effect | What the dated totals show | What they do not show |
|---|---|---|
| Exposure | Impressions more than doubled (+125%). | Whether the new impressions are event/booking queries, branded navigational queries, or low-relevance leftovers. |
| Clicks | 6 → 5. Absolute click change is noise on a single-digit sample. | Whether any named query gained or lost a click. |
| CTR | Supported at page level: 3.19% → 1.18%. Clicks did not rise with impressions. | Cannot split snippet CTR from position-driven CTR or from a mix shift toward low-CTR queries. |
| Ranking | Possible contributor. Average position was **not recorded** on the Sep 6 screen. | No query positions. |
| Event timing | Plausible. The live calendar still lists rooms in this window (meetup, festival, pitch night). | No query×date series. |

**Do not blame #331 / #767 archive cleanup.** Those snippets deployed 2026-09-03 ([receipt](DEPLOY-767-331-2026-09-03.md)). A 28-day window displayed 2026-09-06 is almost entirely pre-deploy. Public checks agree: `/events/` is 200, self-canonical, indexable, and in the page sitemap. `/category/events-reports/` is `noindex, follow` on a cache-busted fetch, as #331 requires, and is not a competing indexable Events URL.

---

## 5. Nearby URLs (cannibalisation candidates, not assumed)

| URL | ID | Live title | Role vs `/events/` |
|---|---:|---|---|
| `/events/` | 2250 | `Events \| Kris Krüg` | Live calendar + hosted-series page |
| `/ai-events/` | 12317 | `AI Events & Recaps: Web Summit, Hackathons, Meetups` | Recap / survival-guide hub. Indexable. Body has no contextual href to `/events/` (nav only). |
| `/vancouver-ai/` | 12315 | `Vancouver AI Ecosystem: BC's Grassroots AI Hub \| Kris Krüg` | Ecosystem hub. Contextual anchor `the calendar` → `/events/` (200). Also `Browse AI events` → `/ai-events/`. |
| `/speaking/` | 1887 | `AI Keynote Speaker Kris Krüg \| Humanizing AI, Creativity & Community` | Booking page. Contextual `Kris Krüg’s event archive` → `/events/` (200). |
| `/category/events-reports/` | n/a | `Events & Reports \| Kris Krüg` | Archive. Cache-busted robots: `max-image-preview:large, noindex, follow`. Keep the exclusion. |

`/ai-events/` is the honest cannibalisation check for Pull C. Its title already names "AI Events". That is a reason to make the `/events/` title say **host / calendar**, not a reason to retitle `/ai-events/` in this lane.

---

## 6. Internal links: no discovery-gap write

#832 closed 2026-09-03. Live public HTML still has the matrix anchors:

| Source | Contextual `/events/` anchor | Extra nav `Events` |
|---|---|---|
| 4495 inaugural meetup | `we still do this every month, and the next one is on the calendar` | yes |
| 9197 meetup 16 | `the next one` | yes |
| 8418 February recap | `come to the next one` | yes |
| 6815 August recap | `the current calendar` | yes |
| 6251 June 2024 highlights | `where the next one lands` | yes |
| 5768 June recap | `still monthly, still free, still worth the trip` | yes |
| 4348 2024 directory | `the live calendar, which is the version that stays current` | yes |
| `/vancouver-ai/` (12315) | `the calendar` | yes |
| `/speaking/` (1887) | `Kris Krüg’s event archive` | yes |
| `/` , `/about/`, `/contact/` | nav only | yes |
| `/ai-events/` (12317) | **nav only** | yes |

Inbound from the recap cluster and the two hubs is already there. Homepage chrome is not a missing contextual wrap I will invent. A calendar sentence on `/ai-events/` would be a #402-shaped extras pass, not a demonstrated #995 discovery defect. `/events/` already has 423 impressions.

Public REST `search=kriskrug.co/events` returned 10 posts (the seven #832 recaps plus unrelated "events" uses). That is a search index, not a complete href census.

---

## 7. Proposed fields (prep only)

H1, page title, slug, body, artboards, `data-event-end` cards, and registration hrefs stay untouched.

| Field | Current (public HTML) | Proposed | Chars |
|---|---|---|---:|
| `<title>` / `jetpack_seo_html_title` | `Events \| Kris Krüg` | `Vancouver AI Events I Host \| Kris Krüg` | 18 → 38 |
| `<meta name="description">` / `advanced_seo_description` | 200-char kicker+H2+lede mash, ends `São Pau…` | `Monthly Vancouver AI meetups, film-club screenings, Friday office hours, and keynote stages I host or speak at. Registration links live on this page.` | 200 → 149 |
| `og:description` / Twitter | follows current description | will follow the new description through the theme | 149 |
| `og:title` | `Events` | **leave.** Theme uses `get_the_title()`. Changing it needs a page-title edit, which this lane does not do. | 6 |
| H1 | `Events` | leave | 6 |
| Body / catalog | live 2026-09-07 save | leave. #635 owns it. | n/a |

Why these strings:

- They name rooms the hero and "Series I produce & host" section already list (monthly Vancouver meetup, film club, Friday office hours, stages).
- They do not name Pitch Night, Sept 30, Futureproof dates, or "tickets still available".
- They distinguish the page from `/ai-events/` recaps without attacking that URL.
- They stay inside normal SERP truncation. No em dashes.

**Ownership of the future write**

| Step | Owner |
|---|---|
| Review + approve strings | KK |
| Snapshot page 2250 (`id`, `slug`, `modified`, `content.raw`) | Publisher session |
| Paste / activate snippet | KK in Code Snippets. Run everywhere (front-end). Strip the opening `<?php` on paste. |
| Render after activation | Aurora, via the existing `get_post_meta` reads |
| Pagely purge | KK, if edge HTML stays stale |
| Persist into post meta later | Optional follow-up. Requires registering the two keys for `page` or WP-CLI. Not this PR. |

**Snapshot / readback / rollback**

1. Before activate: authenticated GET page 2250. Abort if id ≠ 2250, slug ≠ `events`, or `modified` ≠ the then-current value (today: `2026-09-07T12:58:41`). Keep the snapshot until the measurement window ends.
2. Confirm public HTML SHA or at least title + description + canonical.
3. Activate the snippet. Do not PATCH `content`.
4. Logged-out readback, plain and `?cb=<ts>`: title and standard description must match the proposed strings; H1 still `Events`; registration hrefs unchanged; canonical still self; robots still indexable.
5. Rollback: deactivate the snippet. Title/description return to the current fallback. No database restore required unless a later session also wrote post meta.

---

## 8. Exact GSC pull for KK (unblocks named queries)

Search Console → Performance → Search results. Property `sc-domain:kriskrug.co`. All four metric toggles on.

**Pull A.** Filter Page = exact `https://kriskrug.co/events/`. Custom dates matching the Sep 6 compare (read the date chips; do not assume). Export Queries for each 28-day window. Note device and country only if one slice dominates.

**Pull B.** Same page filter, Queries contains `event` / `meetup` / `vancouver ai` (separate passes). Mark zero-click rows.

**Pull C.** Cannibalisation: keep a query filter, switch to Pages. Candidates to look at, not to assume: `/ai-events/`, `/vancouver-ai/`, `/speaking/`, individual recap posts.

**Pull D.** Sitewide Search results for the same two windows so the page movement stays in context. Keep the homepage seven-day alert on a different ticket.

Paste digest-safe aggregates onto #995. No raw export in git.

If Pull A shows the new impressions are branded navigational (`kris krug events`) with healthy CTR, KK can reject the snippet. If they are `vancouver ai meetup` / booking-shaped with impressions and no clicks, ship it. If they are off-intent junk, no-change is correct and this proposal stands down.

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

## 10. Acceptance criteria, marked honestly

| #995 criterion | Status |
|---|---|
| Refresh `/events/` identity, owner, metadata, canonical/robots, modified/hash; say who owns title/description | **MET** in §§1–3 |
| Compare exact-date GSC page-filtered query / device / country rows | **NOT MET.** Access missing; precise gap in §4a. Pull spec in §8 |
| Report with top opportunity queries or GSC-missing notes, plus change/no-change | **MET** as GSC-missing notes + ranked recommendation |
| If justified: one honest title + description; links only if discovery gap; exact fields; ownership; snapshot/readback/rollback | **MET** for title/description. Links: evidence-backed **no-add** |
| Preserve artboards, dates, registration destinations, page design; no invented availability | **MET** (no body write; dates kept out of the snippet) |
| Post-approval measurement protocol | **MET** in §9 |
| Reviewable Track A packet; no live write | **MET** |

Keep #995 open. `Refs #995`, not Closes.

---

## 11. Scope and safety

No POST, PATCH, PUT, or DELETE against kriskrug.co. No theme deploy, SFTP, snippet activate, cache purge, indexing request, or Validate Fix. No secrets printed. Other-lane proposal files (#274 / #331 / #339 / #402 / #994 / #996 / #997) were not edited.

### Session verification (2026-09-08)

| Command | Result |
|---|---|
| `make doctor` | **FAIL**, expected. WP credentials unresolved; `scripts/notion-to-wp/.venv` missing; `gh` authenticated as `cursor`; live `style.css` reachable. No authenticated write path. |
| `make status-readonly` | Ran. WP 7.0.4; Aurora live and repo `1.6.11`; draft-queue counts unavailable without creds. |
| `make seo-publisher-smoke` | **PASS** (sitemap, feed, news sitemap, three recent BlogPosting pages). |
| `curl -sSIL` `/events/` | HTTP/2 200; robots `max-image-preview:large`; self-canonical; title still `Events \| Kris Krüg`. |
| Destination GETs | `/speaking/`, `/vancouver-ai/`, `/ai-events/` 200; `luma.com/sept-ai` 200; `lu.ma/vancouver-ai` 301→200; Eventbrite 429 in this session. |
| `php -l` snippet | **Skipped.** `php` is not on PATH in this image. CI `php-validation` will lint the new file. |
| `git diff --check` | clean after these files |

### Follow-ups that are not this PR

1. KK Pull A–D in §8 so opportunity queries can be named.
2. KK approve + activate `fixes/issue-995-events-search-snippet.php` in a publisher session, or reject it if Pull A shows branded/off-intent impressions.
3. Optional later: persist the same two strings into page 2250 post meta and deactivate the snippet. Needs a `page` meta registration or WP-CLI. Track A, separate approval.
4. `/ai-events/` contextual calendar sentence: park under #402. Not started here.
