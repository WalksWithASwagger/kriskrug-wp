# Rank 5 — post 4826 Future Proof Creatives community series

**URL:** https://kriskrug.co/2024/03/05/join-the-future-proof-creatives-community/
**Slug:** `join-the-future-proof-creatives-community`
**Status:** publish
**GSC:** membership unconfirmed. Confirm before apply.
**Action:** internal-link repair
**Also:** inbound source 1 for 4359

## Identity guards (public REST 2026-09-08T05:54Z)

| Field | Value |
|---|---|
| id | 4826 |
| slug | `join-the-future-proof-creatives-community` |
| status | publish |
| link | `https://kriskrug.co/2024/03/05/join-the-future-proof-creatives-community/` |
| date | `2024-03-05T08:47:39` |
| modified | `2026-07-24T14:39:53` |
| modified_gmt | `2026-07-24T22:39:53` |
| featured_media | 4543 |
| categories | [1665] |
| public `content.rendered` sha256 | `cb370eb2dea6173bd3963264c252080bad8140a37f29c25925efa024b62f5e55` |
| public `content.rendered` bytes | 34337 |

## Live fields

| Field | Live 2026-09-08 | Proposal |
|---|---|---|
| HTTP / canonical / robots | 200 / self / indexable | no change |
| SEO title / description | already set | **keep** |
| inbound hrefs to this slug | **0** | inbound comes from 4359 |
| body mentions | workshop ×20; Frank / Hartman / photography / residency ×0 | add one opening sentence |
| luma CTAs / FAQ appendix | present | **leave** |

## Content insert

Append one sentence to the opening paragraph. Do not invent a new residency that is not already on-site.

**FIND** (exactly once):

```html
and it&#8217;s easy to feel left behind. </strong></p>
```

**REPLACE:**

```html
and it&#8217;s easy to feel left behind. </strong> That includes the camera-side work from the <a href="https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/">photography and generative AI residency</a> and the 2024 <a href="https://kriskrug.co/2023/12/28/generative-ai-future-proof-creatives-online-training-workshops-2024/">online training workshops</a>.</p>
```

Skip if either href already exists.

## Inbound sources for this target

1. Post 4359 new paragraph (`04-post-4359-workshops-2024.md`).
2. No second source.

## Rollback

Restore snapshotted `content.raw`. Meta was never in the write set.
