# Archive sitemap policy — apply / rollback (#331)

Prepared 2026-08-16. Reconfirmed the same evening (logged-out curl,
2026-08-16 19:28 PT). **Nothing here has been applied.** Activating this
snippet is a live write and stays KK-gated. Do not change `robots.txt`. Do
not submit, resubmit, or remove anything in Search Console from this lane.

REST `/wp/v2/users` and `/?author=N` probes are **not** this packet. Those
are #767 / merged PR #793. This lane does not edit those files.

v2 PHP is unchanged: the evening readback matched the earlier 2026-08-16
inventory, so `fixes/issue-331-archive-sitemap-policy-v2.php` remains the
deploy candidate. Do not activate both v1 and v2.

---

## Live sitemap inventory (2026-08-16, logged out)

`/sitemap.xml` still `301`s to `/wp-sitemap.xml` (`x-redirect-by: WordPress`).
`robots.txt` still points at `/sitemap.xml` and still disallows only
`/wp-admin/`, `/?s=`, and `/search/`. That handoff is intentional; leave it.

| Child sitemap | URL count | What it is |
|---|---:|---|
| `wp-sitemap-posts-post-1.xml` | 973 | published posts — **keep** |
| `wp-sitemap-posts-page-1.xml` | 46 | published pages — **keep** |
| `wp-sitemap-taxonomies-category-1.xml` | 14 | category archives — drop |
| `wp-sitemap-taxonomies-post_tag-1.xml` | 633 | tag archives — drop |
| `wp-sitemap-users-1.xml` | 2 | author archives — drop |
| **Total** | **1,668** | |

No custom-taxonomy child sitemap exists. Public REST taxonomies are
`category`, `post_tag`, `nav_menu`, and `wp_pattern_category`. Only the first
two appear in `/wp-sitemap.xml`.

Sampled archives (category, tag, both authors, year/month/day, plus
`/category/vancouver-ai-ecosystem/page/2/`) all return `200`, emit
`meta robots=max-image-preview:large` only, and have **no** canonical. A
control post and `/about/` still have a self-canonical. Date archives are
**not** in the sitemap and are still indexable.

Evening reconfirm (2026-08-16 19:28 PT): child counts still 973 / 46 / 14 /
633 / 2. Same 14 category slugs. `/sitemap.xml` still `301`s with
`x-redirect-by: WordPress`. REST `/wp/v2/users` still returns `200` with
`x-wp-total: 2` (out of scope; #767 / PR #793). No v3 snippet: v2 still
covers the live surface.

---

## Is v1 enough?

`fixes/issue-331-archive-sitemap-policy.php` is **not live** (confirmed again
by the users/category/tag children above). If activated as written it would:

- **Yes — drop the author sitemap.** `wp_sitemaps_add_provider` returns
  `false` for `users`, so `wp-sitemap-users-1.xml` leaves the index. That is
  the sitemap half of #767. It does **not** hide REST users or `?author=N`.
- **Yes — drop all 14 category URLs and all 633 tag URLs** from the sitemap.
- **Yes — `noindex,follow`** on author, tag, and category HTML, including
  `/page/N/` variants.
- **No — date archives stay indexable.** `/2026/`, `/2026/07/`, and
  `/2003/10/14/` would keep today's permissive robots meta. That is the hole
  the 2026-08-02 proposal called out.
- **No — a future public taxonomy would still get a sitemap child.** v1 only
  unsets `category` and `post_tag`.

Use **v2** as the deploy candidate:
`fixes/issue-331-archive-sitemap-policy-v2.php`. Leave v1 in the repo as the
receipt artifact. Do not activate both.

---

## Blast radius if v2 is activated

Sitemap membership after a cache purge should be **973 posts + 46 pages =
1,019 URLs**. Re-count immediately before deploy; these numbers move.

| Class | Sitemap | Also noindex? | URLs that drop from the sitemap |
|---|---|---|---|
| Posts | keep | no | none |
| Pages | keep | no | none |
| Author archives | drop | **yes** (`noindex,follow`) | 2 (`/author/<redacted>/`) |
| Tag archives | drop | **yes** | 633 (`/tag/{slug}/`) |
| Category archives | drop | **yes** (Option A) | 14 (list below) |
| Date archives | already absent | **yes** (v2 only) | 0 from sitemap; HTML still 200 |
| Custom taxonomies | none live; v2 would drop any | **yes** via `is_tax()` | none today |

Category URLs that leave the sitemap (and should be noindexed until a later
content project gives a named slug a self-canonical, unique title, meta
description, and H1 that is not `Category: {name}`):

- `/category/vancouver-ai-ecosystem/`
- `/category/ai-creatives/`
- `/category/indigenous-reconciliation-in-tech/`
- `/category/events-reports/`
- `/category/conversations-interviews/`
- `/category/ai-ethics-philosophy/`
- `/category/ai-for-journalism-media/`
- `/category/generative-ai-tools/`
- `/category/field-notes/`
- `/category/keynotes-speaking/`
- `/category/responsible-ai-policy/`
- `/category/creative-technology-making/`
- `/category/photography-visual-storytelling/`
- `/category/web-early-blog/`

Issue #331's acceptance criteria still allow a curated category keep-list.
The 2026-07-12 Growth Mirror rehearsal found 16 archive impressions and zero
clicks; none of the 14 categories currently has a term description or
canonical. **Option A (exclude all now)** is what v1 and v2 implement.
Promoting a category later is a copy project plus a snippet change, not a
reason to ship v1.

Do **not** `Disallow` these paths in `robots.txt`. Google needs to crawl the
`noindex`. Archives stay publicly reachable; links still pass.

---

## Apply (human-gated; do not run from this PR)

1. Re-count live child sitemaps. Do not treat 1,668 / 1,019 as frozen.
2. Snapshot the Code Snippets inventory outside the repo (same pattern as
   `fixes/issue-706-script-diet.md`).
3. Create an **inactive** snippet from v2, opening `<?php` stripped. Diff
   the saved body against the repo file. `php -l` the body.
4. Activate only after that diff, a PHP syntax check, and a named rollback
   owner.
5. Purge Pagely / Jetpack Boost cache.
6. Readback:
   - `/sitemap.xml` still `301` → `/wp-sitemap.xml`
   - index contains post + page children only (no `users`, `category`,
     `post_tag`, or other taxonomy children)
   - post and page URL counts match the pre-deploy recount
   - representative category, tag, author, **and date** archives, including
     one `/page/2/`, return `200` with `noindex,follow`
   - a control post and page still have a self-canonical and remain in their
     sitemap children
7. Search Console: read status at 24h and 72h. Do not resubmit in between.
   Do not use temporary URL removals.

---

## Rollback

Deactivate the snippet. Purge cache. Repeat the sitemap index plus the
representative archive and post/page readback. Rollback restores prior
provider and robots behavior. It must not edit content, terms, users,
permalinks, redirects, `robots.txt`, or Search Console rows.

---

## Pre-deploy evidence review, 2026-09-02

Added by the kk-kb SEO/AEO audit. This section exists to close the **first**
acceptance criterion on issue #331, which gates the whole change:

> Search Console query-to-page evidence is reviewed for category, tag, and
> author archive traffic before changing policy.

That review had not been done. It is done now, and it did not need production
access: the evidence is in the committed weekly-digest export at
`kk-kb:content/admin/scheduled-task-reports/seo-growth-weekly/data/2026-08-31/normalized-search-console.json`.

### The archives have no measurable search value

Window 2026-08-22 to 2026-08-28 against the prior seven days. Search Console
returns page rows only for URLs that drew at least one impression, so the
denominator below is "URLs with any search activity at all".

| Group | URLs with data | Clicks | Impressions |
|---|---:|---:|---:|
| Posts and pages | 276 | 48 | 2,370 |
| Tag, category, author archives | **2** | **1** | **1** |

649 archive URLs are submitted in the sitemap. Two of them registered anything:

```
1 click,  1 impression   https://kriskrug.co/author/kk/page/36/
0 clicks, 0 impressions  https://kriskrug.co/tag/shout-outs/
```

The single click is on page 36 of a paginated author archive.

### What that settles

- **No allowlist exception is warranted.** The acceptance criteria allow
  retaining a tag or category archive that has "demonstrated search value" or
  "real query demand". None has any. There is nothing to put on the list.
- **The `noindex, follow` policy costs no measured traffic.** The archives are
  39% of the submitted sitemap and about 2% of measured clicks, all of it from
  one paginated author page.
- **`follow` remains load-bearing** and is not affected by this evidence. These
  archives are internal-link hubs into the 973 posts; the finding is that nobody
  arrives *on* them from search, not that they carry no link value.

### Limits of this evidence

One 7-day window plus its prior week. It is not a seasonal picture, and a tag
with a once-a-year spike would not appear. The margin is wide enough that this
is unlikely to change the decision: 649 URLs produced one impression across two
weeks. If a seasonal argument is wanted before deploying, the 28-day context
window in the same export is the next place to look.

## Behavioural verification of the v2 snippet, 2026-09-02

Run against PHP 8.4 with minimal WordPress shims for `add_filter()` and the
conditional tags, exercising each filter body directly. This proves the snippet
does what the acceptance criteria ask; it does not replace the post-deploy live
readback below.

| Filter | Input | Result |
|---|---|---|
| `wp_sitemaps_taxonomies` | `category, post_tag, portfolio_type` | empty, every taxonomy dropped |
| `wp_sitemaps_add_provider` | `users` | `false`, provider dropped |
| `wp_sitemaps_add_provider` | `posts`, `terms` | kept, so `posts-post` and `posts-page` survive |
| `wp_robots` | author / tag / category / date / tax | `noindex, follow` with `follow` present |
| `wp_robots` | single post or page | unchanged, `index` preserved |

`php -l` passes. The repo's `make validate` could not be used as a check here:
it fails after a clean `composer install` because `phpcs.xml.dist` references
five sniffs (`WordPress.Security.EscapeOutput`, `.NonceVerification`,
`.SafeRedirect`, `.ValidatedSanitizedInput`, `WordPress.WP.Capabilities`) that
do not exist in the pinned `wp-coding-standards/wpcs` 3.4.1, so no sniffs
register. That is a pre-existing repository defect, unrelated to #331, and
worth its own issue.

## One code change made to the deploy candidate

`kk_archive_policy_v2_sitemap_taxonomies()` called
`unset( $taxonomies['category'], $taxonomies['post_tag'] )` and then returned
`array()` unconditionally, discarding the variable it had just modified. The
behaviour was correct, but the dead `unset()` made the function look like it
returned the filtered array. A maintainer tidying it by returning `$taxonomies`
would silently revert v2 to v1 behaviour and let any future public taxonomy back
into the sitemap, which is the exact regression v2 exists to prevent.

The `unset()` is gone and the two taxonomy names are kept in a body comment, so
the intent stays greppable. Verified above that the return is still empty.

**Activation is still KK-gated and unchanged.** Nothing here has been applied.
