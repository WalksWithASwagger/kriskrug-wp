# #336 AI second brain search fields and inbound wraps

**Verdict:** STILL OPEN
**SEO write target:** post `8802`, slug `how-to-build-an-ai-second-brain-that-actually-works-for-you`
**Inbound wraps:** posts `9774` and `12327`
**Live document title:** `Build an AI Second Brain That Actually Works` (missing "for You")
**Live description:** `Most digital systems are designed for neurotypical productivity zombies. What if you built one optimized for your actual thought patterns instead?`
**Evidence:** approved title and description are not live. `AI as a second brain` on 9774 is unlinked. `knowledge bases and named assistants` on 12327 is unlinked.

This is an **overwrite** of non-empty SEO fields. Additive `make seo-backfill` will skip 8802.

Do not change the public post title, excerpt, slug, date, or taxonomies.

## A. SEO fields (post 8802)

Use [`seo-meta-overwrite.json`](seo-meta-overwrite.json).

| Field | Live now | Approved overwrite |
|---|---|---|
| `jetpack_seo_html_title` | `Build an AI Second Brain That Actually Works` | `Build an AI Second Brain That Actually Works for You` |
| `advanced_seo_description` | productivity-zombies excerpt | `Build an AI second brain that works with your thought patterns, captures creative chaos, and turns scattered notes and voice memos into finished work.` |

Modified guard: `2026-06-28T20:27:34`

Same dry-run command as #335 (file contains both posts). Apply 8802 after 35.

Public readback on current Aurora 1.6.9, not against 1.3.39 zip assumptions. Cache-bust the permalink.

## B. Inbound wraps

Target href: `https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/`

### Patch 1: post 9774

- Slug: `what-journalists-need-to-know-about-ai-right-now`
- URL: `https://kriskrug.co/2025/06/24/what-journalists-need-to-know-about-ai-right-now/`
- Modified guard: `2026-06-14T20:05:53`
- Live needle count: 1
- Live target-href count: 0

**FIND:**

```html
AI as a second brain
```

**REPLACE:**

```html
<a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">AI as a second brain</a>
```

Live rendered context keeps an existing em dash after the phrase (`AI as a second brain` then the rest of the sentence). Wrap the phrase only. Do not edit that em dash.

### Patch 2: post 12327

- Slug: `storyhive-haus-of-owl-jordan-dack`
- URL: `https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/`
- Modified guard: `2026-08-16T21:03:50` (authenticated refresh)
- Current raw: 17,706 chars; SHA-256 `045c697906260becae376d39fcf0987911ac9c94e5d3b25def8a4f1b4a69981d`
- Planned raw: 17,812 chars; SHA-256 `32a77f548f700cde5edd77e8c6959dda04d9aa229e852b8f860c8ce87f09b4bd`
- Live needle count: 1
- Live target-href count: 0

**FIND:**

```html
knowledge bases and named assistants
```

**REPLACE:**

```html
<a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">knowledge bases and named assistants</a>
```

## Snapshot-first apply

1. Snapshot 8802 (meta + content), 9774, and 12327 before any write.
2. Confirm ID + slug + publish + modified on each.
3. Meta-only overwrite on 8802. Readback both keys.
4. Content-only wraps on 9774 then 12327. FIND count must be 1.
5. Public readback: approved title/description on 8802; each source has exactly one href to 8802; 8802 still 200 and self-canonical.

## Rollback

Restore prior meta from the overwrite `old` map, then re-POST each snapshotted `content.raw`.
