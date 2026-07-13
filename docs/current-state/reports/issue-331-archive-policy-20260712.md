# Issue #331 Archive Sitemap and Indexability Receipt

**Date:** 2026-07-12 (America/Vancouver)

**Status:** Repo-only; production is human-gated

**Issue:** [WalksWithASwagger/kriskrug-wp#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331)

**Canonical implementation:** `fixes/issue-331-archive-sitemap-policy.php`

## Decision

No author, tag, or category archive has enough demonstrated query value for a sitemap allowlist. Exclude all three archive classes from WordPress core sitemap output and emit `noindex,follow` on their public landing pages. Keep every archive publicly accessible.

Posts and pages are outside this policy and remain unchanged. `/sitemap.xml` must keep its permanent handoff to `/wp-sitemap.xml`.

## Query Evidence Reviewed

The Growth Mirror live API rehearsal supplied these query-page aggregates:

| Window | Author archives | Tag archives | Category rows | Clicks |
|---|---:|---:|---:|---:|
| Current 28 days | 2 impressions | 4 impressions | 1 impression | 0 |
| Prior 28 days | 4 impressions | 2 impressions | 3 impressions | 0 |

The category rows were `/category/.../feed/` URLs, not category landing pages. Across both windows, the archive evidence totals 16 impressions and zero clicks. It therefore supports no retained category, tag, or author archive exception.

## Sitemap Counts

| URL class | Before | Expected after | Policy |
|---|---:|---:|---|
| Published posts | 967 | 967 | Unchanged |
| Published pages | 45 | 45 | Unchanged |
| Category archives | 14 | 0 | Exclude |
| Tag archives | 613 | 0 | Exclude |
| Author archives | 2 | 0 | Exclude |
| **Total** | **1,641** | **1,012** | **Remove 629 archive URLs** |

The expected post-change inventory is 1,012 URLs: 967 posts + 45 pages. Retained archive URLs: none. If the live post or page inventory changes before deployment, stop and refresh the baseline instead of treating 1,012 as a forced count.

## Exact Policy

- Filter the WordPress core `users` sitemap provider so author archives are absent.
- Remove only the `category` and `post_tag` subtypes from the WordPress core taxonomy sitemap provider.
- Do not filter `wp_sitemaps_post_types`; the shared `posts` provider and its `post` and `page` subtypes remain intact.
- On `is_author()`, `is_tag()`, or `is_category()`, preserve unrelated robots directives, remove conflicting `index`, `nofollow`, or `none`, and add `noindex,follow`.
- Do not redirect any archive. Do not delete terms or users. Do not change permalinks. Do not submit or remove Search Console rows.
- Do not change the existing `/sitemap.xml` redirect or any post/page membership from this policy.

## Deployment Gate

Do not deploy from this worker lane. A separate human-approved production pass must:

1. Reconfirm the live child-sitemap inventory and snapshot the Code Snippets inventory before any write.
2. Create an inactive Code Snippets entry from the canonical PHP file, with only the opening `<?php` removed, and compare the saved source back to the repository.
3. Activate only after the source comparison, PHP syntax check, and rollback owner are recorded.
4. Purge the approved WordPress/Pagely cache only after activation.

## Production Readback Gate

The approved deployer must record all of the following before calling the change complete:

1. `/sitemap.xml` still makes its permanent handoff to `/wp-sitemap.xml`.
2. The sitemap index contains post and page child sitemaps, contains no users child sitemap, and contains no category or tag child sitemap.
3. A complete crawl counts 967 post URLs and 45 page URLs from this baseline, for 1,012 total retained URLs, with no independently introduced redirect or deletion mixed into the result.
4. Representative author, tag, and category landing pages return `200`, do not redirect, and emit exactly one robots meta policy containing `noindex,follow` under normal, Googlebot, and cache-busted requests.
5. Representative posts and pages remain publicly reachable, indexable, and present in their WordPress core sitemap provider.
6. Search Console sitemap status is read back at 24 hours and 72 hours without repeated resubmission or temporary URL removals. API indexed counts are recorded as reported, not interpreted as a verified zero.

## Rollback Gate

If provider membership, robots output, public access, or post/page regression checks fail, deactivate the snippet, purge the approved production cache, and repeat the sitemap plus representative route readback. The rollback must restore the prior provider behavior without editing content, terms, users, permalinks, redirects, or Search Console rows.

No deployment, cache purge, WordPress content/settings write, Search Console action, or issue closure was performed by this repository-only implementation.
