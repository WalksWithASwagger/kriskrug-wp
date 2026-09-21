# Crawl hygiene — apply / rollback (#1025 Track A)

Prepared 2026-09-18 from Sulu’s Track A comment
<https://github.com/WalksWithASwagger/kriskrug-wp/issues/1025#issuecomment-5723267397>.
**Nothing here has been applied.** Activating this snippet is a live write and
stays gated on **SEO LGTM**. Do not merge this PR as a deploy. Do not change
`robots.txt`. Do not Request Indexing. Do not broaden #331.

PHP source: [`issue-1025-crawl-hygiene.php`](issue-1025-crawl-hygiene.php).
Robots / sitemap / noindex recommendations (do not apply from here):
[`issue-1025-crawl-policy.json`](issue-1025-crawl-policy.json) and
[`../docs/current-state/CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md`](../docs/current-state/CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md).
Do not change `robots.txt`. Do not broaden #331.

---

## Before (public readback, 2026-09-18)

No Search Console counts are invented here. These are live HTTP reads.

| URL | Status | Notes |
|---|---|---|
| `https://kriskrug.co/home/` | **301** `x-redirect-by: redirection` → `/` → **200** | Single hop already. Page 2315 (`home`) is still published and still listed in `wp-sitemap-posts-page-1.xml`. |
| `https://kriskrug.co/home` | **301** `redirection` → `/` | Same rule, no trailing slash. |
| Homepage HTML | no `href` to `/home/` | Matches the 2026-08-25 authenticated scan (zero inbound `/home/` links). |
| `…/barcampearth-a-local-report/?share=twitter&nb=1` | **301** `x-redirect-by: KK GSC404` → clean permalink | Snippet 8 / [`gsc-404-query-param-canonicalize.php`](gsc-404-query-param-canonicalize.php). |
| `…/photography-and-generative-ai/?share=twitter` | **301** `KK GSC404` → clean permalink | Same snippet. |
| `https://kriskrug.co/?nb=1` | **301** `KK GSC404` → `/` | Same snippet. |
| `https://kriskrug.co/about/?amp=1` | **301** `KK GSC404` → `/about/` | Same snippet. |
| Homepage + sample post HTML | zero `?share=` / `nb=` hrefs | Internal minting already stopped. |
| `https://kriskrug.co/feed/` | **200** `application/rss+xml`, 20 `<item>`s | **Keep.** |
| `https://kriskrug.co/tag/sxsw-sxswi/feed/` | **200** RSS | Advertised via `rel="alternate"` on the tag archive. |
| `https://kriskrug.co/author/kk/feed/` | **200** RSS | Advertised via `rel="alternate"` on the author archive. |
| `https://kriskrug.co/author/kk/page/2/` | **200** HTML, `noindex, follow` | #331 v2 already noindexes it. Still a crawl sink. Author page 1 still links to `/page/2/` … `/page/41/`. |
| `/tag/sxsw-sxswi/`, `/category/ai-ethics-philosophy/`, `/author/kk/` | **200**, `noindex, follow` | #331 v2 (snippet 26). Do not change. |
| `/wp-sitemap.xml` | posts + pages only | #331 v2 already dropped users / category / tag children. |
| `/robots.txt` | physical file, sitemap + admin/search disallows | Healthy. Do not edit. |
| Category feeds, comments feed | **200** RSS | Out of tonight’s named list. Leave them. |

---

## What this snippet changes after activate

| Surface | After |
|---|---|
| `/home/` and `/home` | Still 301 → `/`. Repo-tracked fallback (`x-redirect-by: KK 1025`) if the Redirection rule is removed. `/home/?share=twitter` becomes one hop to `/` (snippet priority `-1`). |
| Page sitemap | `/home/` dropped (page slug `home` excluded). Posts sitemap unchanged. |
| Generated Home permalink | `page_link` for that page returns `/`, so internals stop minting `/home/`. |
| `?share=` / `nb=` / `amp=` | Inbound 301 stays on snippet 8. This file only strips those keys from generated permalinks. |
| Tag feed | 301 → the tag HTML archive. `rel="alternate"` for tag feeds is suppressed. |
| Author feed | 301 → `/author/{slug}/`. `rel="alternate"` for author feeds is suppressed. |
| Author `/page/{n}/` (n ≥ 2) | 301 → first author page. Page 1 stays 200 + existing #331 `noindex, follow`. |
| `https://kriskrug.co/feed/` | Unchanged 200 RSS. |
| Tag / category archive robots | Unchanged `#331` `noindex, follow`. |
| `robots.txt` | Unchanged. |

---

## How `/home/` → `/` is implemented

1. **Live today:** Redirection plugin rule. Public proof is `x-redirect-by: redirection` and `location: /` on both `/home` and `/home/`. That rule is not in this repo’s June 2026 Redirection import.
2. **This PR:** the same exact-path 301 in Code Snippets, plus sitemap exclusion and permalink rewrite. Do **not** add a second Redirection rule. The snippet is the reviewable copy.
3. Exact path only. `/home/generative-ai-1/` style attachment leftovers are not redirected.

---

## Sample parameter URL handling

Owned by **snippet 8**, already live:

```
GET /2006/08/28/barcampearth-a-local-report/?share=twitter&nb=1
→ 301 KK GSC404
→ https://kriskrug.co/2006/08/28/barcampearth-a-local-report/
```

```
GET /about/?amp=1
→ 301 KK GSC404
→ https://kriskrug.co/about/
```

Keys: `share`, `nb`, `amp`. This PR does not replace that snippet.

---

## Main RSS

`https://kriskrug.co/feed/` is intentionally untouched. The feed redirect
function returns early unless `is_feed()` is also `is_tag()` or `is_author()`,
and it never runs on `is_comment_feed()`.

---

## Apply (human-gated; do not run from this PR)

1. Snapshot Code Snippets outside the repo (same pattern as `issue-706-script-diet.md`).
2. Create an **inactive** snippet from this PHP, opening `<?php` stripped. Diff the saved body against the repo file. `php -l` the body.
3. Activate only after SEO LGTM, that diff, and a named rollback owner.
4. Purge Pagely / Jetpack Boost cache.
5. Readback (cache-busted):
   - `/home/` still single-hop 301 → `/` (Redirection or `KK 1025`)
   - `/wp-sitemap-posts-page-1.xml` no longer lists `/home/`
   - `/?share=twitter` still 301 via `KK GSC404`
   - `/tag/sxsw-sxswi/feed/` 301 → tag HTML
   - `/author/kk/feed/` 301 → `/author/kk/`
   - `/author/kk/page/2/` 301 → `/author/kk/`
   - `/feed/` still 200 RSS with items
   - `/tag/sxsw-sxswi/` and `/category/ai-ethics-philosophy/` still `noindex, follow`
   - `/robots.txt` unchanged
   - control post still indexable

---

## Rollback

Deactivate the snippet. Purge cache. Repeat the readback table. Rollback
restores prior feed and pagination 200s and puts `/home/` back in the page
sitemap. It must not edit content, Redirection rules, snippet 8, #331,
`robots.txt`, or Search Console rows.
