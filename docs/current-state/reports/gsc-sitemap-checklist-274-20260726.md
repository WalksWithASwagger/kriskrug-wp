# GSC sitemap submit + monitor checklist (#274)

**Captured:** `2026-07-26T20:39:48Z` (UTC)  
**Issue:** [#274](https://github.com/WalksWithASwagger/kriskrug-wp/issues/274)  
**Related:** [#273](https://github.com/WalksWithASwagger/kriskrug-wp/issues/273) (topic hubs), [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331) (taxonomy/archive sitemap bloat), [#222](https://github.com/WalksWithASwagger/kriskrug-wp/issues/222)  
**Property:** `sc-domain:kriskrug.co`  
**Agent constraint:** This lane cannot click Google Search Console. Public HTTP discovery only. KK (or a logged-in human) must execute the UI steps below.

---

## Verdict (public discovery)

**Canonical sitemap to submit:** `https://kriskrug.co/sitemap.xml`

- `robots.txt` advertises **only** that URL.
- Live handoff: `https://kriskrug.co/sitemap.xml` → **301** → `https://kriskrug.co/wp-sitemap.xml` (WordPress core sitemap index). Intentional; do not “fix” the redirect.
- Do **not** newly submit child `wp-sitemap-*.xml` URLs, Jetpack-era paths, `www`/`http` variants, or `sitemap_index.xml`.

---

## Public discovery (2026-07-26 probe)

### robots.txt

```text
Sitemap: https://kriskrug.co/sitemap.xml
```

No other `Sitemap:` lines. Source comment in file: `fixes/robots.txt`, last reviewed 2026-06-07.

### Endpoint matrix

| URL | HTTP | Final | XML? | Advertised? | Submit? |
|---|---:|---|---|---|---|
| `https://kriskrug.co/sitemap.xml` | 301→200 | `…/wp-sitemap.xml` | yes (index) | **yes** | **Yes — only this** |
| `https://kriskrug.co/wp-sitemap.xml` | 200 | same | yes (index) | no (implementation detail) | No (covered via redirect) |
| `https://kriskrug.co/sitemap_index.xml` | 404 | same | no | no | No |
| `https://kriskrug.co/sitemap-1.xml` | 404 | same | no | no | No |
| `https://www.kriskrug.co/sitemap.xml` | →200 | apex `wp-sitemap.xml` | yes | no | No (duplicate host) |
| `http://www.kriskrug.co/sitemap.xml` | →200 | apex `wp-sitemap.xml` | yes | no | No (legacy host/scheme) |
| `https://www.kriskrug.co/sitemap_index.xml` | →404 | apex 404 | no | no | No |
| `http://www.kriskrug.co/sitemap_index.xml` | →404 | apex 404 | no | no | No |
| `https://kriskrug.co/news-sitemap.xml` | 200 (empty urlset; trailing `/`) | `…/news-sitemap.xml/` | yes, **0 URLs** | **no** | **No** |
| `https://kriskrug.co/image-sitemap-index-1.xml` | 404 | same | no | no | No |
| `https://kriskrug.co/video-sitemap-1.xml` | 404 | same | no | no | No |

### WordPress core index children (via canonical)

| Child sitemap | URLs (2026-07-26) |
|---|---:|
| `wp-sitemap-posts-post-1.xml` | 968 |
| `wp-sitemap-posts-page-1.xml` | 46 |
| `wp-sitemap-taxonomies-category-1.xml` | 14 |
| `wp-sitemap-taxonomies-post_tag-1.xml` | 619 |
| `wp-sitemap-users-1.xml` | 2 |
| **Total** | **1,649** |

Tag archives alone are **37.5%** of submitted inventory → see pitfalls / #331.

### Priority page reachability (for URL Inspection)

All return **200** with no redirect on 2026-07-26:

| URL | Notes |
|---|---|
| `https://kriskrug.co/` | Home |
| `https://kriskrug.co/about/` | Core |
| `https://kriskrug.co/blog/` | Core |
| `https://kriskrug.co/work/` | Core (historically had stale “redirect / recent-projects” Google state in Jul 2 GSC pass) |
| `https://kriskrug.co/contact/` | Core — may still need first indexing request |
| `https://kriskrug.co/vancouver-ai/` | Topic hub (#273) |
| `https://kriskrug.co/ai-for-creatives/` | Topic hub |
| `https://kriskrug.co/ai-events/` | Topic hub |
| `https://kriskrug.co/ai-ethics/` | Topic hub |
| `https://kriskrug.co/ai-conversations/` | Topic hub |
| `https://kriskrug.co/ai-for-journalists/` | Topic hub |
| `https://kriskrug.co/ai-tools/` | Topic hub |
| `https://kriskrug.co/indigenous-ai/` | Topic hub — Jul 16 GSC readback still `Discovered - currently not indexed` |

---

## Prior GSC UI truth (do not invent new clicks)

From issue #274 comments (human Brave session, 2026-07-02):

| Sitemap row seen in GSC | Status then | Agent guidance now |
|---|---|---|
| `https://kriskrug.co/sitemap.xml` | Success; resubmitted Jul 2, 2026 | Keep as the only active canonical row |
| `https://kriskrug.co/sitemap-1.xml` | Success historically; **public is now 404** | Do not resubmit; remove if UI allows |
| `https://www.kriskrug.co/sitemap_index.xml` | Couldn't fetch | Do not resubmit; remove if UI allows |
| `http://www.kriskrug.co/sitemap_index.xml` | Couldn't fetch | Do not resubmit; remove if UI allows |
| `http://www.kriskrug.co/sitemap.xml` | Success (duplicate scheme/host) | Do not resubmit; remove if UI allows |
| Jetpack `news` / `image` / `video` | Not present in table Jul 2 | Do not newly submit (news is empty XML now, still not advertised) |

Core URL Inspection already done once for `/`, `/about/`, `/blog/`, `/work/`. Remaining queue from that pause: `/contact/` + the eight topic hubs above.

---

## KK runbook — submit

1. Open [Google Search Console](https://search.google.com/search-console) → property **`sc-domain:kriskrug.co`** (domain property, not a stray URL-prefix duplicate).
2. Left nav → **Sitemaps**.
3. Confirm whether `https://kriskrug.co/sitemap.xml` already shows **Success**.
   - If Success and last read is recent: **do not spam resubmit**. Optional one-time resubmit only if KK wants the UI “Submitted” date refreshed.
   - If missing / Couldn't fetch / error: enter `sitemap.xml` (or full `https://kriskrug.co/sitemap.xml`) → **Submit**.
4. **Do not submit** any of: `wp-sitemap.xml`, child `wp-sitemap-*.xml`, `sitemap_index.xml`, `sitemap-1.xml`, `news-sitemap.xml`, `image-sitemap-index-1.xml`, `video-sitemap-1.xml`, or any `www` / `http://` variant.
5. Cleanup (optional, only if the UI offers remove/delete):
   - Prefer removing dead or duplicate rows: `sitemap-1.xml`, `*sitemap_index.xml`, `http://www…` / `https://www…` duplicates.
   - If remove is unavailable, leave them; `robots.txt` no longer advertises them. Do not “fix” by submitting replacements.
6. Screenshot or note: Submitted URL, Type (expect **Sitemap index**), Status, Last read, Discovered pages. Paste into #274.

---

## KK runbook — URL Inspection / request indexing

Quota is limited. Request only high-value URLs; do not burn quota on tag archives.

### Pass A — core (if not already successful)

1. URL Inspection → paste URL → wait for result → **Request indexing** only if not already “URL is on Google” *or* Google’s stored state is wrong (redirect/canonical mismatch).
2. Order:

| # | URL | Prior evidence |
|---:|---|---|
| 1 | `https://kriskrug.co/` | Indexed; request already done Jul 2 — skip unless regressing |
| 2 | `https://kriskrug.co/about/` | Indexed + requested Jul 2 |
| 3 | `https://kriskrug.co/blog/` | Indexed + requested Jul 2 |
| 4 | `https://kriskrug.co/work/` | Was “not indexed / redirect to recent-projects”; public now 200 `/work/` — re-inspect; request only if still wrong |
| 5 | `https://kriskrug.co/contact/` | **Still in remaining queue** |

### Pass B — topic hubs (#273)

Resume exactly here (from #274 Jul 2 pause + Jul 16 note):

1. `https://kriskrug.co/contact/` (if not done in Pass A)
2. `https://kriskrug.co/vancouver-ai/`
3. `https://kriskrug.co/ai-for-creatives/`
4. `https://kriskrug.co/ai-events/`
5. `https://kriskrug.co/ai-ethics/`
6. `https://kriskrug.co/ai-conversations/`
7. `https://kriskrug.co/ai-for-journalists/`
8. `https://kriskrug.co/ai-tools/`
9. `https://kriskrug.co/indigenous-ai/` (still `Discovered - currently not indexed` as of 2026-07-16)

For each: record Google status, last crawl, user-declared vs Google-selected canonical, and whether indexing was requested.

---

## KK runbook — monitor (24–72h, then weekly)

| When | Where | What to record |
|---|---|---|
| T+0 | Sitemaps | Canonical row Status = Success; discovered page count (expect ~1.6k until #331 ships) |
| T+24h | Sitemaps | Last read advanced; no new Couldn't fetch on canonical |
| T+24–72h | Pages / Indexing | Coverage deltas; do **not** treat API “indexed” as literal zero if UI lags |
| T+24–72h | URL Inspection | Re-check Pass B hubs, especially `/work/` and `/indigenous-ai/` |
| Weekly | Performance | Impressions/clicks on hubs; feed #249 / #279 review windows |
| After #331 deploy | Sitemaps | Child list should drop users + category + tag; total ≈ posts+pages only — **read back, do not resubmit repeatedly** |

Suggested follow-up window if Pass B completes on/near 2026-07-26: **2026-07-29 → 2026-08-02** for first coverage check, then one weekly glance.

---

## What success looks like

- [ ] Only `https://kriskrug.co/sitemap.xml` is treated as the active submission.
- [ ] That row shows **Success**; Google follows the 301 to the WP index.
- [ ] No new submissions of Jetpack-era, empty news, or legacy `www`/`http`/`sitemap_index` URLs.
- [ ] Dead/duplicate rows removed **or** explicitly left alone with a note that remove was unavailable.
- [ ] Pass A/B indexing requests recorded (URL + date + result), without duplicate spam on already-queued URLs.
- [ ] 24–72h readback documented on #274 (status, last read, discovered count, hub inspection notes).
- [ ] Taxonomy bloat acknowledged as **#331 work**, not fixed by extra GSC submissions.

---

## Pitfalls

1. **Duplicate sitemaps** — Submitting both `sitemap.xml` and `wp-sitemap.xml`, or apex + `www`, or `http` + `https`, splits discovery and muddies Last read. One advertised URL only.
2. **Chasing dead Jetpack URLs** — `image-sitemap-index-1.xml` and `video-sitemap-1.xml` are 404. `news-sitemap.xml` is now an **empty** 200 XML and still must **not** be submitted (not in robots.txt; zero URLs).
3. **Taxonomy bloat → #331** — 619 tag + 14 category + 2 author URLs (~38%+ of inventory) dilute crawl/index reporting. Policy/snippet already drafted (`fixes/issue-331-archive-sitemap-policy.php` / report `issue-331-archive-policy-20260712.md`). GSC cannot fix this; deploy #331 separately, then read sitemap counts down without hammering Resubmit.
4. **Indexed count ≠ verified truth** — Search Console “indexed” / discovered counts lag and can look wrong after large inventory changes. Record numbers; don’t panic-resubmit.
5. **Request-indexing quota** — Prefer hubs and core IA. Never request tag/author archives.
6. **`/work/` stale Google state** — Public is clean 200; Google may still store an old redirect canonical. Inspect before requesting again.
7. **Agent stop rule** — No claimed GSC submission or indexing request without UI/API proof from a human session.

---

## Agent / repo boundary

| Done in this report | Not done (human-gated) |
|---|---|
| Live robots + sitemap probe | Click Submit in GSC |
| Canonical URL identification | Remove duplicate GSC rows |
| Step checklist + success criteria | URL Inspection / Request indexing |
| Pitfalls linked to #331 | Closing #274 |

No live WordPress writes. No Search Console API auth in this environment.

---

## One-line paste for #274

> 2026-07-26 public probe: robots advertises only `https://kriskrug.co/sitemap.xml` (301→`wp-sitemap.xml`, 5 children, **1,649** URLs: 968 posts / 46 pages / 14 cats / 619 tags / 2 authors). Submit/monitor that URL alone in `sc-domain:kriskrug.co`; do not submit news/image/video/legacy index duplicates. Resume indexing queue at `/contact/` + topic hubs; taxonomy shrink is #331, not more GSC submits. Full runbook: `docs/current-state/reports/gsc-sitemap-checklist-274-20260726.md`.
