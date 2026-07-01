# Issue #37: XML Sitemap and Search Console Runbook

> **TL;DR:** kriskrug.co has one working sitemap submission target:
> `https://kriskrug.co/sitemap.xml`. Jetpack core is inactive, so do not submit
> or advertise the former Jetpack news/image/video sitemap URLs.

## Current state verified 2026-07-01

| Endpoint | Status |
|---|---|
| `https://kriskrug.co/sitemap.xml` | HTTP 200, valid XML, resolves to WordPress core `/wp-sitemap.xml` |
| `https://kriskrug.co/wp-sitemap.xml` | HTTP 200, valid WordPress sitemap index |
| `https://kriskrug.co/news-sitemap.xml` | HTTP 404, not advertised in robots.txt |
| `https://kriskrug.co/image-sitemap-index-1.xml` | HTTP 404, not advertised in robots.txt |
| `https://kriskrug.co/video-sitemap-1.xml` | HTTP 404, not advertised in robots.txt |
| `https://kriskrug.co/sitemap_index.xml` | HTTP 404, confirms no Yoast/Rank Math sitemap |
| `https://kriskrug.co/robots.txt` | HTTP 200, advertises only `https://kriskrug.co/sitemap.xml` |
| Site Kit GA4 | Connected, `G-X7JE8B32L7`, injected sitewide |
| Search Console | Connected through Site Kit to `sc-domain:kriskrug.co` |

Full sitemap marker verification on 2026-07-01 checked 1,628 public HTML URLs:

```txt
Missing GA4: 0
Missing gtag: 0
Missing Search Console verification: 0
```

## Search Console action

1. Open Google Search Console and select `sc-domain:kriskrug.co`.
2. Go to **Sitemaps**.
3. Submit only `sitemap.xml`.
4. Remove old submitted entries for `news-sitemap.xml`, `image-sitemap-index-1.xml`, and `video-sitemap-1.xml` if the UI allows removal.
5. If the UI does not allow removal, leave those old rows alone; they are no longer advertised and should age out.
6. Use URL Inspection to request indexing for `/`, `/about/`, `/blog/`, `/work/`, `/contact/`, and the highest-value updated pages.
7. Expect 24-72 hours before Search Console coverage reflects the cleanup.

## Validation commands

```bash
curl -fsSL https://kriskrug.co/robots.txt
curl -I https://kriskrug.co/sitemap.xml
curl -I https://kriskrug.co/wp-sitemap.xml
curl -I https://kriskrug.co/news-sitemap.xml
curl -I https://kriskrug.co/image-sitemap-index-1.xml
curl -I https://kriskrug.co/video-sitemap-1.xml
```

Expected:

```txt
/robots.txt lists only Sitemap: https://kriskrug.co/sitemap.xml
/sitemap.xml and /wp-sitemap.xml return 200
old Jetpack sitemap endpoints return 404 and are not advertised
```

## Do not install another SEO plugin

Do not install Yoast, Rank Math, or another SEO plugin just to recreate the old Jetpack sitemap endpoints. The current sitemap is working, Site Kit covers Analytics/Search Console wiring, and extra SEO plugins would add duplicate metadata and performance risk.

## Historical correction

Earlier versions of this runbook described a Jetpack-generated sitemap index and recommended adding image/video sitemap lines to robots.txt. That was correct only while Jetpack core owned the sitemap surface.

After the 2026-07-01 Jetpack-off performance cleanup, WordPress core owns the sitemap and the old Jetpack news/image/video sitemap endpoints return 404. The correct cleanup is to stop advertising those endpoints, not to recreate them.
