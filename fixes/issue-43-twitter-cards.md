# Issue #43 Twitter/X Cards - Deployment Note

**Scope:** Track A evidence and deployable snippet only. No live WordPress writes were made.

## Current Live Source

Jetpack is the active social metadata owner. Live HTML includes the `<!-- Jetpack Open Graph Tags -->` block, and Jetpack's documented `jetpack_open_graph_tags` filter is the smallest safe patch point because it edits the existing tag set instead of adding a second metadata generator.

Do not deploy the previous raw `wp_head` emitter. It would duplicate Jetpack tags, still miss `/blog/`, used `@YourTwitterHandle`, and did not guarantee 1200x630 card images.

## Public Evidence - 2026-05-21

Read-only curls against `https://kriskrug.co/` showed:

| URL | Current status |
|---|---|
| `/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x480` in OG metadata |
| `/about/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x450` |
| `/generative-ai-services/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x416` |
| `/blog/` | Jetpack OG block present, but no `twitter:card`, canonical, or 1200x630 image; current image is `s0.wp.com/i/blank.jpg` at `200x200` |
| `/2026/05/04/punk-rock-ai/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x469` |
| `/2026/05/07/web-summit-vancouver-2026/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x469` |
| `/2026/05/16/make-culture-not-content/` | `twitter:card=summary_large_image`, `twitter:site=@feelmoreplants`, image `1200x686` |

WP REST media evidence confirms several live featured images are not 1200x630 originals. The snippet therefore asks Jetpack's image CDN for exact `resize=1200%2C630` URLs. A local download check of the Punk Rock AI transformed image returned `1200 x 630`.

## Deployment Recommendation

1. Confirm backup/rollback proof before any production change.
2. Install `fixes/issue-43-twitter-cards.php` as a Code Snippets entry or mu-plugin only if Jetpack remains the active Open Graph/Twitter provider.
3. Do not install this snippet if Rank Math, Yoast, AIOSEO, or another plugin is taking over social metadata.
4. After deploy, purge Pagely/Jetpack caches and validate these surfaces with normal curl and `Twitterbot/1.0` user agent:

```bash
for url in \
  https://kriskrug.co/ \
  https://kriskrug.co/about/ \
  https://kriskrug.co/generative-ai-services/ \
  https://kriskrug.co/blog/ \
  https://kriskrug.co/2026/05/04/punk-rock-ai/ \
  https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/
do
  echo "### $url"
  curl -Ls -A 'Twitterbot/1.0' "$url" \
    | perl -0777 -ne 'while (/<(?:meta|link)\b[^>]+(?:twitter:card|twitter:site|twitter:creator|twitter:title|twitter:description|twitter:image|og:image|og:image:width|og:image:height|rel="canonical")[^>]*>/g) { print "$&\n" }'
done
```

## Close Criteria Remaining

- Live `twitter:site` and `twitter:creator` read `@feelmoreplants`, matching the current footer/social metadata source of truth.
- `/blog/` has a `summary_large_image` card or is explicitly split to a blog-index SEO follow-up.
- Representative page, post, and blog-index card images resolve to 1200x630.
- X Card Validator preview is manually checked after cache purge because X validation requires the live crawler.
