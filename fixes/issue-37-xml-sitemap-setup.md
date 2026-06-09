# Issue #37: XML Sitemap — Status & Search Console Runbook

> **TL;DR — kriskrug.co already has a working XML sitemap.** It is generated
> automatically by Jetpack at **`https://kriskrug.co/sitemap.xml`** and is
> healthy and current. There is nothing to "create." The only open work is
> (1) submitting/confirming it in Google Search Console and (2) a small
> robots.txt tidy-up. **Do not install Yoast/Rank Math just for a sitemap** —
> see the correction note at the bottom.

## Current state (verified live 2026-06-07)

| Endpoint | Status |
|---|---|
| `https://kriskrug.co/sitemap.xml` (Jetpack index) | ✅ HTTP 200, valid sitemap index |
| `sitemap-1.xml` (pages + posts) | ✅ **986 URLs**, `lastmod` 2026-06-05 — auto-updates on publish |
| `image-sitemap-index-1.xml` | ✅ HTTP 200, `lastmod` 2026-06-04 |
| `news-sitemap.xml` | ✅ HTTP 200 (Google News format) |
| `video-sitemap-1.xml` | ⚠️ `lastmod` 2025-03-02 — stale, newer videos missing |
| `wp-sitemap.xml` (WP core) | 404 — Jetpack disables core's sitemap, so **no duplicate** |
| `sitemap_index.xml` (Yoast/Rank Math) | 404 — confirms **no conflicting SEO plugin** |
| robots.txt declares sitemap | ✅ lists `/sitemap.xml` + `/news-sitemap.xml` |
| Google Search Console verification | ✅ verification meta tag live on homepage |

Verify any of the above yourself:

```bash
curl -s https://kriskrug.co/sitemap.xml | head -20          # index resolves
curl -s https://kriskrug.co/sitemap-1.xml | grep -c "<loc>" # URL count
curl -s https://kriskrug.co/robots.txt                      # what crawlers see
```

## Action 1 — Submit / confirm the sitemap in Google Search Console

The GSC property already exists (verification tag is live), so this is a
~2-minute dashboard task. There is no API submission wired into this repo;
do it by hand:

1. Open **[search.google.com/search-console](https://search.google.com/search-console)** and select the **kriskrug.co** property.
2. Left sidebar → **Sitemaps**.
3. Under "Add a new sitemap," enter **`sitemap.xml`** → **Submit**.
4. (Optional) Add **`news-sitemap.xml`** as a second entry.
5. You do **not** need to submit the image/video sitemaps separately — GSC discovers them from the index.
6. Status should move to "Success" within a day; "Discovered URLs" will track toward ~986.

> Bing is **not** set up (no `msvalidate.01` tag found). If KK wants Bing/Copilot
> coverage too: create the property at [bing.com/webmasters](https://www.bing.com/webmasters)
> (you can import directly from GSC), then submit `sitemap.xml` there as well.

## Action 2 — Add the image + video sitemaps to robots.txt

robots.txt currently advertises only the main and news sitemaps. The image and
video sitemaps exist but aren't declared, so some crawlers won't find them from
the index. This is a small discoverability gap, not a blocker.

**First, find out whether robots.txt is physical or virtual:**

```bash
# On Pagely SSH, at the site document root:
ls -la <site-root>/robots.txt
```

- **Physical file exists** → edit it directly, add these two lines under the existing `Sitemap:` lines:
  ```
  Sitemap: https://kriskrug.co/image-sitemap-index-1.xml
  Sitemap: https://kriskrug.co/video-sitemap-1.xml
  ```
- **No physical file (WordPress serves a virtual robots.txt)** → deploy the
  ready-made snippet **[`issue-37-robots-add-sitemaps.php`](issue-37-robots-add-sitemaps.php)**
  via the Code Snippets plugin or as an mu-plugin. It appends just those two
  lines, is idempotent, and is fully reversible (deactivate to undo).

Verify after either path:

```bash
curl -s https://kriskrug.co/robots.txt   # should now list all four sitemaps
```

> The bigger **AI-crawler stance** for robots.txt (whether to explicitly
> allow/deny GPTBot, ClaudeBot, Google-Extended, CCBot, etc.) is a separate
> strategic decision with two ready-to-paste options in
> [`robots-txt-update.txt`](robots-txt-update.txt). Action 2 here is deliberately
> scoped to *just* the sitemap lines so it can ship without making that call.

## Action 3 (low priority) — Refresh the stale video sitemap

`video-sitemap-1.xml` hasn't updated since 2025-03. Jetpack only lists videos it
detects in content; newer videos may be embedded in a form Jetpack's video
sitemap doesn't pick up. Low impact (videos still get indexed via the page they
live on). Revisit only if video SEO becomes a priority — not worth chasing now.

---

## Correction note (why this file changed)

The original version of this doc recommended **installing the Yoast SEO plugin**
to "create" a sitemap and pointed at a `…cloudwaysapps.com` staging URL. Both
were wrong for this site:

- kriskrug.co **already has** a Jetpack-generated sitemap — installing Yoast (or
  Rank Math) would produce a **second, conflicting** sitemap at a different URL
  and duplicate the meta-tag layer Jetpack already owns. Don't do it unless/until
  you're deliberately migrating *off* Jetpack for SEO (a much bigger project —
  see [`SEO_AUDIT.md`](../docs/current-state/SEO_AUDIT.md) §2.2 and the
  "Removing Jetpack" caution in [`FIX_QUEUE.md`](../docs/current-state/FIX_QUEUE.md)).
- The Cloudways URL is a dev box that was never used as production. Production is
  Pagely (`kriskrug.co`). See [`SITE_INVENTORY.md`](../docs/current-state/SITE_INVENTORY.md).

**Status:** sitemap exists and is healthy ✅ · GSC submission = manual dashboard step ·
robots.txt sitemap lines = snippet staged in this folder.
