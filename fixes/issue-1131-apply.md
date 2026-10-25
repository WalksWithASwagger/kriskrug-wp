# Final-URL chrome and `/home/` sitemap drop — apply / rollback (#1131)

Prepared 2026-10-17 from
<https://github.com/WalksWithASwagger/kriskrug-wp/issues/1131>.
**Nothing here has been applied to production.** Theme files and this snippet
are repo-only until KK approves the [#1114](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1114)
deploy gate. Do not merge this PR as a deploy. Do not write live WordPress.
Do not change Person / sameAs JSON-LD (#1089 / #1104).

PHP source: [`issue-1131-exclude-home-sitemap.php`](issue-1131-exclude-home-sitemap.php).
Theme hrefs: `theme/kk-aurora/parts/header.html`, `parts/footer.html`,
`templates/front-page.html` (Aurora 1.6.13).

---

## Before (public readback, 2026-10-17)

| Surface | Live | Expected after deploy |
|---|---|---|
| Header / footer `href="/services/"` | 1,031 pages; 301 → `/generative-ai-services/` | `href="/generative-ai-services/"` |
| Footer `href="https://futureproof.website/"` | 1,031 pages; 308 → `https://www.futureproof.website/` | `href="https://www.futureproof.website/"` |
| `https://kriskrug.co/home/` in `wp-sitemap-posts-page-1.xml` | listed; 301 → `/` | not listed |
| Three posts linking `https://www.futureproof.website/festival/` | 308 → `/` | out of scope here (live post bodies) |

---

## What this PR changes in the repo

| Surface | After (repo) | Live until #1114 |
|---|---|---|
| Header Services + Work with me | `/generative-ai-services/` | still `/services/` |
| Footer Services + Work with me | `/generative-ai-services/` | still `/services/` |
| Footer Futureproof Festival | `https://www.futureproof.website/` | still apex host |
| Homepage CTAs in `front-page.html` | `/generative-ai-services/` | still `/services/` if the live FSE template has not been refreshed |
| Events catalog Futureproof row | `https://www.futureproof.website/` | live `/events/` body is a separate apply |
| Page sitemap | snippet ready to drop slug `home` (ID 2315) | `/home/` still listed |

Festival-card copy is unchanged (VOICE-CANON). Person schema is unchanged.

---

## Sitemap apply (human-gated; do not run from this PR)

`/home/` is a published page (slug `home`, ID 2315) that 301s to `/`. WordPress
core still emits it in the page sitemap. This repo now owns a **narrow**
filter for that one exclusion.

Do **not** activate [`issue-1025-crawl-hygiene.php`](issue-1025-crawl-hygiene.php)
just to drop `/home/`. That package also 301s tag/author feeds and author
pagination and stays gated on SEO LGTM.

1. Snapshot Code Snippets outside the repo.
2. Create an **inactive** snippet from `issue-1131-exclude-home-sitemap.php`,
   opening `<?php` stripped. Diff the saved body against the repo file.
   `php -l` the body.
3. Activate only after KK approval, that diff, and a named rollback owner.
4. Purge Pagely / Jetpack Boost cache.
5. Readback (cache-busted):
   - `/wp-sitemap-posts-page-1.xml` no longer lists `/home/`
   - `/home/` still single-hop 301 → `/` (`x-redirect-by: redirection`)
   - posts sitemap unchanged
   - `/robots.txt` unchanged
   - Person JSON-LD unchanged

WP-admin alternative if KK prefers not to add a snippet: edit page 2315 to
`noindex` or move it out of `publish`. That admin click is not in this PR.

---

## Theme apply

Aurora 1.6.13. Deploy only through #1114 (KK-owned vault/SFTP). Href-only;
no pixel-gate layout change.

After theme deploy, a logged-out sample of `/`, `/about/`, and one post should
show zero `href="/services/"` and zero `href="https://futureproof.website/"`
in header/footer.

---

## Leftovers this PR does not write live

- Three published posts still link `https://www.futureproof.website/festival/`,
  which 308s to `/`. That is post content, not theme chrome.
- Live FSE `front-page` (if it diverges from `templates/front-page.html`) needs
  the same href refresh during the theme deploy, not a REST content write here.

---

## Rollback

- Theme: restore Aurora 1.6.12 via the #1114 rollback seat, then purge cache.
- Snippet: deactivate it, purge cache. `/home/` returns to the page sitemap.
  Do not edit Redirection, snippet 8, #331, `robots.txt`, or Search Console.
