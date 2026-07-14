# Aurora 1.3.40 Search Title Handoff

Issue: [#357](https://github.com/WalksWithASwagger/kriskrug-wp/issues/357)

## Why This Exists

Aurora 1.3.39 restores standard descriptions, but the singular document-title path does not read the approved `jetpack_seo_html_title` post meta field. The June live-write receipt records the metadata as written, while production still emits the public post title plus the global site descriptor.

The July 14 Growth Mirror window surfaced the impact on post `5236`:

- Query: `"creator community specialist" openai`
- Current window: 31 impressions, 0 clicks, 0.00% CTR, average position 6.97
- Approved search title: `AI Skills for Storytellers: OpenAI's Souki Mansoor`
- Live title before this release: the longer public post title plus the global site descriptor

A deterministic public check covered all 19 batch-4 posts with approved search titles. None emitted its approved value as the exact document title.

## Release Behavior

- Singular posts and pages use the trimmed, tag-free `jetpack_seo_html_title` value when it is a non-empty string.
- The approved value is exact. Aurora does not append the site descriptor.
- Missing, empty, invalid, archive, search, taxonomy, front-page, and 404 paths retain existing behavior.
- Public H1s, post titles, slugs, canonicals, body copy, and Open Graph titles are unchanged.

## Regression Sample

| Shape | Post ID | Expected document title |
|---|---:|---|
| Search opportunity | 5236 | `AI Skills for Storytellers: OpenAI's Souki Mansoor` |
| Long public title | 4011 | `Brandt Designs: Pool Tables as Art Installations` |
| Short approved title | 6552 | `AI and Music: A Digital Renaissance` |
| Unicode punctuation | 4960 | `Broetry, Content Farms, TL;DR — Is the Internet OK?` |
| Proper-name correction | 4495 | `Inside the Inaugural Vancouver AI Community Meetup` |

## Verification

Local completion gate:

```bash
make verify
```

The theme smoke checks exact custom-title output plus empty, invalid, non-singular, and unexpected-object fallbacks. The operational static test verifies the module include, metadata key, sanitization, hook, and last-priority registration.

Future public readback after an explicitly approved deploy:

1. Confirm cache-busted `style.css` reports `Version: 1.3.40`.
2. Confirm every regression URL returns `200`, remains self-canonical, and retains one H1.
3. Confirm each `<title>` exactly matches the approved value.
4. Confirm standard, Open Graph, and Twitter descriptions retain one owner each.
5. Confirm front page, Blog archive, taxonomy, search, and 404 title behavior is unchanged.

## Deployment Gate

This handoff does not package or deploy the theme. It does not modify the already-hashed Aurora 1.3.39 artifact from #351. Any 1.3.40 package requires a fresh checksum, a rollback package based on the then-live version, exact action-time approval, cache purge, and anonymous readback.

After deployment and recrawl, compare query/page impressions, clicks, CTR, and average position after 14 and 28 full days. Do not claim causation before recrawl.
