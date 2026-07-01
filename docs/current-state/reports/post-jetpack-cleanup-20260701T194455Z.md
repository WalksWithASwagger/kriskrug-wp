# Post-Jetpack Performance + Search Cleanup - 20260701T194455Z

**Mode:** snapshot-first live cleanup
**Base URL:** https://kriskrug.co
**Snapshot:** `backup/20260701T194455Z-post-jetpack-cleanup`

## Executive summary

- Site Kit remains the analytics/search owner: GA4 `G-X7JE8B32L7`, Analytics property `311967290`, Search Console property `sc-domain:kriskrug.co`.
- Public pages still contain GA4/gtag and Google site verification markers.
- Jetpack core remains inactive and installed for rollback.
- Deleted stale inactive plugins: wpcat2tag-importer/wpcat2tag-importer, mobilemonkey-x-ray-installer/mobilemonkey-x-ray-installer, amp/amp, regenerate-thumbnails/regenerate-thumbnails.
- Active plugins were left unchanged: PASS.
- Contact replacement: PASS.
- Plugin delete failures: 0.

## Plugin cleanup

| Plugin | Result | HTTP | Note |
| --- | --- | --- | --- |
| wpcat2tag-importer/wpcat2tag-importer | deleted | 200 |  |
| mobilemonkey-x-ray-installer/mobilemonkey-x-ray-installer | deleted | 200 |  |
| amp/amp | deleted | 200 |  |
| regenerate-thumbnails/regenerate-thumbnails | deleted | 200 |  |

### Active plugins after cleanup

`abilities-api/abilities-api, akismet/akismet, code-snippets/code-snippets, google-site-kit/google-site-kit, insert-headers-and-footers/ihaf, jetpack-boost/jetpack-boost, jetpack-protect/jetpack-protect, mcp-adapter/mcp-adapter, popup-maker/popup-maker, redirection/redirection, zero-bs-crm/ZeroBSCRM`

### Inactive plugins after cleanup

`jetpack/jetpack`

## Site Kit and search coverage

- Analytics setting read status: `200`.
- Search Console setting read status: `200`.
- Site Verification setting read status: `400`.
- PageSpeed setting read status: `200`.
- GA snippet enabled in Site Kit settings: `True`.

| Route | HTTP | GA4 ID | gtag | GSC verification | wp.com stats | Jetpack core asset |
| --- | --- | --- | --- | --- | --- | --- |
| / | 200 | True | True | True | False | False |
| /about/ | 200 | True | True | True | False | False |
| /work/ | 200 | True | True | True | False | False |
| /blog/ | 200 | True | True | True | False | False |
| /contact/ | 200 | True | True | True | False | False |

## Sitemap and robots coverage

Robots advertised sitemap lines:

```text
Sitemap: https://kriskrug.co/sitemap.xml
Sitemap: https://kriskrug.co/news-sitemap.xml
Sitemap: https://kriskrug.co/image-sitemap-index-1.xml
Sitemap: https://kriskrug.co/video-sitemap-1.xml
```

| Sitemap | HTTP | Redirects | Final URL | XML? | Advertised in robots |
| --- | --- | --- | --- | --- | --- |
| /sitemap.xml | 200 | 1 | https://kriskrug.co/wp-sitemap.xml | xml | True |
| /wp-sitemap.xml | 200 | 0 | https://kriskrug.co/wp-sitemap.xml | xml | False |
| /news-sitemap.xml | 404 | 0 | https://kriskrug.co/news-sitemap.xml | not xml | True |
| /image-sitemap-index-1.xml | 404 | 0 | https://kriskrug.co/image-sitemap-index-1.xml | not xml | True |
| /sitemap_index.xml | 404 | 0 | https://kriskrug.co/sitemap_index.xml | not xml | False |

## Route and redirect QA

| Route | HTTP | Redirects | Final URL |
| --- | --- | --- | --- |
| / | 200 | 0 | https://kriskrug.co/ |
| /about/ | 200 | 0 | https://kriskrug.co/about/ |
| /blog/ | 200 | 0 | https://kriskrug.co/blog/ |
| /work/ | 200 | 0 | https://kriskrug.co/work/ |
| /contact/ | 200 | 0 | https://kriskrug.co/contact/ |
| /robots.txt | 200 | 0 | https://kriskrug.co/robots.txt |
| /llms.txt | 200 | 0 | https://kriskrug.co/llms.txt |
| /projects/ | 200 | 1 | https://kriskrug.co/work/ |
| /recent-projects-include/ | 200 | 1 | https://kriskrug.co/work/ |

## Performance probes after cleanup

| Route | HTTP | Redirects | Cold TTFB p50 | Warm TTFB p50 | Bytes | Cache |
| --- | --- | --- | --- | --- | --- | --- |
| / | 200 | 0 | 0.580s | 0.527s | 83694 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT |
| /about/ | 200 | 0 | 0.646s | 0.520s | 49693 | x-jetpack-boost-cache=rebuild, x-gateway-cache-status=HIT |
| /blog/ | 200 | 0 | 0.851s | 0.524s | 125724 | x-gateway-cache-status=HIT |
| /work/ | 200 | 0 | 0.488s | 0.548s | 49500 | x-jetpack-boost-cache=rebuild, x-gateway-cache-status=HIT |
| /contact/ | 200 | 0 | 0.664s | 0.551s | 47527 | x-jetpack-boost-cache=rebuild, x-gateway-cache-status=HIT |

## Replacement watchlist

- Contact: keep the current mailto CTA unless form conversion friction shows up.
- Analytics: Site Kit GA4 replaces Jetpack Stats.
- Sitemaps: WordPress core sitemap is live; news/image sitemap status is captured above.
- Sharing/likes/newsletter/publicize: intentionally not replaced in this pass.
- Image CDN: no Jetpack core asset markers were present in sampled public pages; revisit source media only if image regressions appear.

## Future work plan

- Keep Jetpack inactive but installed through the next stability window; delete it later only after analytics, contact, sitemap, and cache behavior remain stable.
- If the email CTA creates lead friction, add one lightweight form solution deliberately; do not replace Jetpack Forms by reflex.
- If social sharing is desired, add static share links in Aurora rather than another broad plugin.
- Review Popup Maker, MCP Adapter, and Jetpack CRM by product need, not TTFB, because the measured cold-load culprit was Jetpack core.
- Revisit Jetpack Boost Critical CSS only if warnings remain visible after the cleanup; do not treat tag-archive CSS warnings as the homepage TTFB cause.

## Rollback notes

- Deleted inactive plugin rollback is reinstall-by-plugin-slug/version using `plugins-before.json` from the snapshot directory.
- Jetpack rollback remains available by reactivating `jetpack/jetpack`, restoring the pre-Jetpack `/contact/` page snapshot from the earlier Jetpack-off backup if needed, and purging PressCACHE.
- No Site Kit, Search Console, Analytics, active plugin, snippet, theme, or page content settings were changed in this cleanup pass.


## GitHub issue updates

- Issue #125: PASS - https://github.com/WalksWithASwagger/kriskrug-wp/issues/125#issuecomment-4859477519
- Issue #86: PASS - https://github.com/WalksWithASwagger/kriskrug-wp/issues/86#issuecomment-4859477624
