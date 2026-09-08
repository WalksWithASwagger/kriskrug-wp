# Rank 2 — post 3082 Frank Yu image generation

**URL:** https://kriskrug.co/2023/09/06/exploring-the-world-of-ai-image-generation-with-artist-frank-yu/
**Slug:** `exploring-the-world-of-ai-image-generation-with-artist-frank-yu`
**Status:** publish
**GSC:** membership unconfirmed. Confirm against the current Crawled-not-indexed examples before apply.
**Action:** content improvement + internal-link repair
**Also:** inbound source 1 for 4539

## Identity guards (public REST 2026-09-08T05:54Z)

| Field | Value |
|---|---|
| id | 3082 |
| slug | `exploring-the-world-of-ai-image-generation-with-artist-frank-yu` |
| status | publish |
| link | `https://kriskrug.co/2023/09/06/exploring-the-world-of-ai-image-generation-with-artist-frank-yu/` |
| date | `2023-09-06T22:16:35` |
| modified | `2026-06-28T20:38:45` |
| modified_gmt | `2026-06-29T04:38:45` |
| featured_media | 3108 |
| categories | [1678] |
| public `content.rendered` sha256 | `29337159b700640316d9ee90f9a78f6d8d2c085ed01d318d9c158e7dc620a8f9` |
| public `content.rendered` bytes | 26403 |

Rendered HTML includes a YouTube iframe and share-button SVG. Byte hash can drift without an editor save. Apply uses `content.raw` + FIND.

## Live fields

| Field | Live 2026-09-08 | Proposal |
|---|---|---|
| HTTP / canonical / robots | 200 / self / indexable | no change |
| `jetpack_seo_html_title` | **empty** | **set** (below) |
| live `<title>` | post title + `\| Kris Krüg` (75) | will follow the new SEO title |
| `advanced_seo_description` | 148-char craft line | **keep** |
| href to 4539 | 0 | add one closing wrap |
| collection footer | unrelated ESG "See also" | leave; do not recategorize |

## A. SEO title (empty field, not an overwrite of a live custom title)

**Proposed `jetpack_seo_html_title`:**
`Frank Yu on AI Image Generation`

Optional description tighten (only if KK wants it in the same write):
`Frank Yu has been pushing cameras and models around for 15 years. Notes from our conversation on AI image generation, Midjourney, and keeping the craft.`

Default is: set the title, leave the description.

## B. Content wrap (inbound to 4539)

**FIND** (exactly once):

```html
Keep generating!
```

**REPLACE:**

```html
Keep generating! Months later we ran a Future Proof Creatives residency on that same question; I wrote it up in <a href="https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/">Photography Meets Generative AI</a>.
```

Skip if that href already exists.

## Inbound sources for this target

1. Post 4539 answer-first paragraph already links here (`01-post-4539-photography-generative-ai.md`).
2. No second source. A wrap on 4359 or 4826 would be a new invented sentence, not a repair of an existing mention.

## Rollback

Restore snapshotted `content.raw` and delete or restore `jetpack_seo_html_title` to empty.
