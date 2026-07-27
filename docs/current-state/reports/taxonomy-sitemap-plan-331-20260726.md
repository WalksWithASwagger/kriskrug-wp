# Taxonomy Sitemap + Archive Indexability Plan — #331

**Date:** 2026-07-26  
**Status:** DRAFT PLAN ONLY — no live robots.txt, sitemap, snippet, cache, or Search Console changes without KK approval  
**Issue:** [WalksWithASwagger/kriskrug-wp#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331)  
**Lane:** Track A (ops / Code Snippets) — docs only this pass  
**Related:** #274 (GSC sitemap checklist), #383 (decision batch; closed), prior receipt `issue-331-archive-policy-20260712.md`, snippet `fixes/issue-331-archive-sitemap-policy.php` (merged via PR #334, **not deployed**)

---

## 1. Verdict

Live kriskrug.co still serves WordPress **core** sitemaps with **1,649** URLs. Taxonomy + author archives are **37% of the inventory** (635 URLs), remain **indexable**, and emit **no self-canonical**. Repo policy + snippet from PR #334 already encode “exclude archives from sitemap + `noindex,follow`”; production has not received that snippet. This document refreshes public evidence and asks KK to pick the category keep/noindex fork before any deploy.

---

## 2. Public probe (2026-07-26, read-only)

### 2.1 robots.txt

- `Sitemap: https://kriskrug.co/sitemap.xml`
- Disallows: `/wp-admin/` (with `admin-ajax` allow), `/?s=`, `/search/`
- No taxonomy/archive Disallow (correct — do **not** robots-block archives; use sitemap + robots meta)

### 2.2 Sitemap surface

| Path | Result |
|---|---|
| `/sitemap.xml` | **301** → `/wp-sitemap.xml` (`x-redirect-by: WordPress`) — keep this handoff |
| `/wp-sitemap.xml` | **200** core sitemap index |
| `/sitemap_index.xml`, `/category-sitemap.xml`, `/post_tag-sitemap.xml`, `/post-sitemap.xml`, `/page-sitemap.xml` | **404** HTML — Yoast-style paths are **not** live |

Index children:

| Child sitemap | URL count |
|---|---:|
| `wp-sitemap-posts-post-1.xml` | 968 |
| `wp-sitemap-posts-page-1.xml` | 46 |
| `wp-sitemap-taxonomies-category-1.xml` | 14 |
| `wp-sitemap-taxonomies-post_tag-1.xml` | 619 |
| `wp-sitemap-users-1.xml` | 2 |
| **Total** | **1,649** |

Drift vs 2026-07-12 baseline (1,641 = 967+45+14+613+2): **+8** (mostly +1 post, +1 page, +6 tags). After any deploy, re-count live children; do not hard-code 1,012.

SEO stack signal: WordPress 7.0.2 + Site Kit generators; Jetpack present (Boost cache headers / theme Jetpack SEO hooks); **no Yoast** sitemap or meta fingerprints. Core `wp_sitemaps_*` + Code Snippets are the realistic control plane.

### 2.3 Archive indexability inventory

Sampled **all 14** category archives, **both** author archives, and **8** tag archives (legacy thin + higher-count). Pattern was uniform:

| Signal | Categories | Tags | Authors |
|---|---|---|---|
| HTTP | 200 | 200 | 200 |
| robots meta | `max-image-preview:large` only (**indexable**) | same | same |
| `x-robots-tag` | absent | absent | absent |
| `<link rel="canonical">` | **none** | **none** | **none** |
| `<meta name="description">` | **none** | **none** | **none** |
| Document `<title>` | present (`{Name} — Kris Krug \| …`) | present | present |
| H1 | 1× `Category: …` | 1× `Tag: …` | 1× `Author: …` |
| Term description in HTML | none observed | none | n/a |

Contrast: homepage **does** emit a self-canonical. Archives do not.

`og:description` on archives falls back to the site tagline (“Empowering Events & Organizations for the AI Age”), not term-specific copy.

Author note: `/author/wpadmin5102/` (display name “Krüg”) is a second public author URL with no distinct brand purpose — high-priority exclude.

---

## 3. Taxonomy size / thinness (public REST)

### 3.1 Categories (14, all in sitemap)

| Posts | Slug | Term description |
|---:|---|---|
| 344 | `web-early-blog` | empty |
| 158 | `photography-visual-storytelling` | empty |
| 116 | `vancouver-ai-ecosystem` | empty |
| 101 | `events-reports` | empty |
| 90 | `ai-creatives` | empty |
| 37 | `ai-ethics-philosophy` | empty |
| 35 | `field-notes` | empty |
| 29 | `conversations-interviews` | empty |
| 18 | `ai-for-journalism-media` | empty |
| 13 | `creative-technology-making` | empty |
| 11 | `generative-ai-tools` | empty |
| 8 | `keynotes-speaking` | empty |
| 5 | `indigenous-reconciliation-in-tech` | empty |
| 3 | `responsible-ai-policy` | empty |

All 14 lack WP term descriptions. Volume alone is not proof of search value.

### 3.2 Tags (619 in sitemap; REST `hide_empty=true` also 619)

- **499** tags have count = 1; **65** count = 2; **27** count = 3
- Only **9** tags have count ≥ 10
- Top tag `/tag/misc/` has **690** posts — a dumping ground, not a curated hub
- High-count topical tags (`vancouver-ai`, `bc-ai`, `generative-ai`, etc.) still compete with real posts/pages and category hubs

### 3.3 Authors (2)

- `/author/kk/` — Kris Krüg
- `/author/wpadmin5102/` — admin/alternate account

---

## 4. Prior query evidence (do not redeploy without KK reconfirm)

From the 2026-07-12 Growth Mirror rehearsal (recorded in `issue-331-archive-policy-20260712.md`):

| Window | Author | Tag | Category rows | Clicks |
|---|---:|---:|---:|---:|
| Then-current 28d | 2 impr. | 4 impr. | 1 impr. | 0 |
| Prior 28d | 4 impr. | 2 impr. | 3 impr. | 0 |

Category rows were `/category/.../feed/` URLs, not landing pages. **16 impressions / 0 clicks** across both windows — no demonstrated archive landing value.

**Gate before live change:** KK (or an authenticated GSC pass) should refresh query→page evidence for `/category/`, `/tag/`, `/author/` in the latest 28/90 days. This draft does **not** claim fresh GSC numbers for 2026-07-26 (no Search Console write/read from this worker).

---

## 5. Proposed keep / noindex / remove rules

**Vocabulary**

- **Remove (sitemap):** drop from core sitemap providers; URL may still 200 for humans.
- **noindex,follow:** robots meta; keep link equity flowing to posts; do not `Disallow` in robots.txt; do not use temporary GSC removals.
- **Keep (indexable + sitemap):** only with self-canonical, unique title, meta description, single H1, and query/editorial justification.

### 5.1 Default recommended policy (aligns with merged snippet)

| Class | Sitemap | Robots | Notes |
|---|---|---|---|
| Posts / pages | **Keep** | index (unchanged) | Out of scope for membership changes |
| Author archives | **Remove** | `noindex,follow` | Especially `wpadmin5102`; no distinct search purpose |
| Tag archives | **Remove** | `noindex,follow` | Allowlist empty unless KK names exceptions |
| Category archives | **Remove** | `noindex,follow` | Matches 2026-07-12 evidence; see fork below |
| `/sitemap.xml` → `/wp-sitemap.xml` | **Keep** | n/a | Do not break handoff |

Expected shape after deploy (re-count live): post + page children only; **no** `taxonomies-category`, `taxonomies-post_tag`, or `users` children. Approximate target ≈ **1,014** (968+46) on 2026-07-26 inventory — refresh at deploy time.

Retained archive allowlist under this default: **none**.

### 5.2 Category fork (issue AC vs evidence)

Issue acceptance criteria allow **retained** categories (sitemap + self-canonical + meta description + H1) and only noindex thin/redundant ones. Evidence so far supports **no** retained category. KK must pick:

| Option | Categories in sitemap | Robots | Extra work |
|---|---|---|---|
| **A — Exclude all (recommended / already coded)** | 0 | all `noindex,follow` | Deploy existing `fixes/issue-331-archive-sitemap-policy.php` |
| **B — Curated keep-list** | Explicit slugs only | keep-list indexable; others `noindex,follow` | Filter taxonomy sitemap by term ID/slug; add self-canonical + meta description + non-“Category:” H1 for keepers; write term descriptions |
| **C — Keep all 14 categories** | 14 | indexable + self-canonical each | Same enrichment for all 14; still remove tags/authors |

If Option B, candidate keepers (editorial hubs, **not** yet evidence-backed) for KK to accept/reject:  
`vancouver-ai-ecosystem`, `ai-creatives`, `indigenous-reconciliation-in-tech`, `keynotes-speaking`, `ai-ethics-philosophy`, `generative-ai-tools`.  
Do **not** auto-keep `web-early-blog` / `photography-visual-storytelling` on volume alone — they are long-tail buckets.

Tag allowlist default: **empty**. Even high-count tags (`misc`, `creativity`, `vancouver-ai`) should stay noindex unless KK documents a curated exception.

### 5.3 Explicit non-actions

- Do not delete terms, posts, pages, or users
- Do not 301 archive URLs in this lane
- Do not change post/page permalinks
- Do not temporary-remove URLs in Search Console
- Do not rewrite archive copy without editorial review
- Do not change robots.txt Sitemap line or Disallow taxonomy paths

---

## 6. Implementation options

| Option | Fit | Pros | Cons | Recommendation |
|---|---|---|---|---|
| **A. Code Snippets + core filters** (repo file ready) | Best | Matches existing ops pattern (#5 schema, #7 SEO root, #8 GSC404, #13 news sitemap); reversible deactivate; unit-tested | Needs human paste/activate + cache purge | **Preferred** |
| **B. Theme (`kk-aurora`) PHP** | Possible | Versioned with theme deploy | Couples Track B release to Track A SEO policy; slower rollback | Avoid for this issue |
| **C. Jetpack SEO UI** | Weak | Already installed | Does not own core sitemap providers; archive noindex coverage is incomplete vs core `wp_robots`; hard to unit-test in repo | Not primary |
| **D. Yoast / Rank Math** | Poor | Full taxonomy sitemap toggles | Not installed; Yoast paths already 404; plugin install is out of scope and adds SEO-ownership conflict with Jetpack/theme | Do not install for #331 |
| **E. robots.txt Disallow** | Wrong tool | Fast | Blocks crawl of URLs still linked on-site; does not set noindex; fights “AI/search discovery” robots stance | Reject |

### 6.1 Preferred implementation (Option A)

Canonical source: `fixes/issue-331-archive-sitemap-policy.php`

Behavior already implemented:

1. `wp_sitemaps_add_provider` — return `false` for `users`
2. `wp_sitemaps_taxonomies` — `unset` `category`, `post_tag`
3. `wp_robots` — on `is_author() || is_tag() || is_category()`, force `noindex,follow` while preserving unrelated directives (e.g. `max-image-preview`)

Tests: `scripts/tests/test_issue_331_archive_policy.py` (PHP harness around the snippet).

If KK chooses category Option B/C, **do not** deploy the current snippet as-is; extend it with an allowlist filter + separate canonical/meta helpers, then re-test.

### 6.2 Deploy package (human-gated; not this session)

1. Snapshot live Code Snippets list + current sitemap index XML
2. Create **inactive** snippet from repo file (strip opening `<?php` for Code Snippets paste)
3. Diff saved body ↔ repo; PHP lint
4. Activate → purge Pagely/Jetpack Boost cache
5. Readback:
   - `/sitemap.xml` still 301 → `/wp-sitemap.xml`
   - Index contains only post + page children
   - Representative category/tag/author: 200, no redirect, robots contains `noindex,follow`
   - Representative post + page still in sitemap and indexable
6. GSC: observe existing sitemap submission at 24h / 72h — **no** forced resubmit loop; do not treat API “indexed” count as gospel
7. Rollback: deactivate snippet → purge → re-read sitemap + robots

---

## 7. Decision checklist for KK

- [ ] Refresh GSC query→page for `/category/`, `/tag/`, `/author/` (28d + 90d)
- [ ] Pick category fork: **A exclude all** (recommended) / **B allowlist** / **C keep all 14**
- [ ] Confirm tag allowlist = empty (or name exceptions)
- [ ] Confirm authors: both noindex + sitemap-remove (including `wpadmin5102`)
- [ ] Approve Code Snippets deploy of `fixes/issue-331-archive-sitemap-policy.php` (or revised allowlist variant)
- [ ] Assign deployer + rollback owner; schedule cache purge window

Until those boxes are checked: **no live robots/sitemap/snippet changes**.

---

## 8. Completion receipt template (post-deploy)

Record:

| Metric | Before (2026-07-26 probe) | After |
|---|---:|---:|
| Total sitemap URLs | 1,649 | |
| Posts | 968 | |
| Pages | 46 | |
| Categories | 14 | |
| Tags | 619 | |
| Authors | 2 | |
| Retained archive URLs (list) | — | |

Plus: snippet ID, activation time, cache purge time, representative HTML robots samples (normal / Googlebot / cache-busted), GSC 24h/72h notes.

---

## 9. Out of scope (unchanged from issue)

Deleting content; temporary GSC removals; bulk taxonomy rename/consolidation; new archive copy without evidence + editorial review; post/page permalink changes; worker-lane production writes.

---

## 10. Sources

- Live HTTP probes 2026-07-26: robots.txt, `/sitemap.xml`, `/wp-sitemap.xml`, all five child sitemaps, archive HTML samples, public REST categories/tags/users
- Issue #331 + comments (PR #334 merged undeployed; 2026-07-13/14 crawl notes; #383 decision reminder)
- Repo: `fixes/issue-331-archive-sitemap-policy.php`, `docs/current-state/reports/issue-331-archive-policy-20260712.md`, `scripts/tests/test_issue_331_archive_policy.py`
