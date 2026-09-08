# Rank 4 — post 4359 2024 Future Proof workshops

**URL:** https://kriskrug.co/2023/12/28/generative-ai-future-proof-creatives-online-training-workshops-2024/
**Slug:** `generative-ai-future-proof-creatives-online-training-workshops-2024`
**Status:** publish
**GSC:** membership unconfirmed. Confirm before apply.
**Action:** internal-link repair
**Also:** inbound source 1 for 4826

## Identity guards (public REST 2026-09-08T05:54Z)

| Field | Value |
|---|---|
| id | 4359 |
| slug | `generative-ai-future-proof-creatives-online-training-workshops-2024` |
| status | publish |
| link | `https://kriskrug.co/2023/12/28/generative-ai-future-proof-creatives-online-training-workshops-2024/` |
| date | `2023-12-28T09:30:58` |
| modified | `2026-07-01T16:24:12` |
| modified_gmt | `2026-07-02T00:24:12` |
| featured_media | 4361 |
| categories | [1662] |
| public `content.rendered` sha256 | `49d59fc7747f32c128a945bf476202ced6b5467e82e9406be8b3e1c7b889d4d8` |
| public `content.rendered` bytes | 12156 |

## Live fields

| Field | Live 2026-09-08 | Proposal |
|---|---|---|
| HTTP / canonical / robots | 200 / self / indexable | no change |
| SEO title / description | already set, lengths fine | **keep** |
| inbound hrefs to this slug | **0** | one outbound paragraph; inbound comes from 4826 |
| luma workshop URLs | still in the body | **do not rewrite or claim they still sell seats** |

A June 2025 link-inject report planned a footer from this post to 4539. That href is **not live**. This pack inserts a dated contextual paragraph instead of re-running bulk `inject_links.py`.

## Content insert

Insert immediately **before** the hashtag paragraph.

**FIND** (exactly once):

```html
<p class="wp-block-paragraph">#FutureProofCreatives #AIInnovation #CreativeTechCommunity</p>
```

**REPLACE:**

```html
<p class="wp-block-paragraph">The 2024 workshop series sat next to the residency work. For the photography-and-model side, start with <a href="https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/">Frank Yu's photography and generative AI residency</a>. The wider community frame is <a href="https://kriskrug.co/2024/03/05/join-the-future-proof-creatives-community/">Future Proof Creatives Community and Event Series</a>.</p>
<p class="wp-block-paragraph">#FutureProofCreatives #AIInnovation #CreativeTechCommunity</p>
```

Skip if either href already exists.

## Inbound sources for this target

1. Post 4826 opening sentence (`05-post-4826-future-proof-community.md`).
2. No second source.

## Rollback

Restore snapshotted `content.raw`. Meta was never in the write set.
