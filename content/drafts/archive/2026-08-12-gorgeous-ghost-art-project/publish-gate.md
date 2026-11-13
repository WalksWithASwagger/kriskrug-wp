# Gorgeous Ghost publish gate

Editorial recommendation: **PUBLISH after preview**. Kris's publish-or-park decision remains open.

Repository state: local package prepared; no WordPress object created or updated; no provider state changed. A refreshed authenticated, read-only all-status check on 2026-08-28 found no post or page owning `gorgeous-ghost`.

Public preflight refreshed 2026-08-28: the dated canonical and legacy bare-slug route both return `404`, and the public WordPress search endpoint returns no Gorgeous Ghost post or page. The authenticated check covered draft, private, pending, future, and published objects through `status=any` with edit context. Every source/network link returns `200` after redirects, and the external share image returns `200 image/jpeg`.

Exact reviewed sources for the preview gate:

- `post.md` sha256: `301a9baf87bad6bfc1385843f96c5f7c6dde2a17e420cdefb222d805d1414412`
- `post.html` sha256: `f1fdc8fd9761c04f5f24ecf30cd819b7b1a604634abe61f67f8030346f79326b`
- Guarded publisher dry-run: title/slug/category/four tags pass; voice check reports zero violations.
- Existing taxonomy IDs: category `1755`; tags `1804`, `1682`, `1785`, and `1395`. Preview creation would not create taxonomy terms.
- The package declares no local upload images. The external first body image remains external, so the guarded publisher would create no media and leave `featured_media` unset for the initial preview. Whether to keep that arrangement or stage a WordPress-hosted derivative remains part of exact-preview approval before publication.

## Proposed editorial payload

- Title: `I Made a Gorgeous Ghost`
- Slug: `gorgeous-ghost`
- Post date: `2026-08-12`
- Canonical: `https://kriskrug.co/2026/08/12/gorgeous-ghost/`
- Category: `Creative Technology & Making`
- Tags: `Gorgeous Ghost`, `Creative AI`, `AI Film Club`, `AI Music`
- First body image and OG source: `https://gorgeousghost.com/og/share.jpg`
- Credits: The Scallywags are Kris Krüg, Magenta Rune, Mayumi Rawlings, and Kevin Friel.
- Special thanks: Kaoru Yoshihira and Floyo.ai.
- Film Club wording: `The BC + AI Film Club Prompt Challenge`.

## Required human preview and publish gate

- [x] In an authenticated, read-only WordPress check, confirm no post or page in any status already owns `gorgeous-ghost`. Refreshed 2026-08-28 against both posts and pages; both returned an empty result.
- [ ] After exact approval, create one new unpublished WordPress post with status `draft` through the guarded publisher workflow; this is an admin preview, not WordPress status `private`, and the publisher cannot publish on creation.
- [ ] Compare the exact preview body against `post.html`, including the first image, credits, category, tags, date, canonical, OG metadata, and every link.
- [ ] Confirm the external OG image resolves correctly in the WordPress preview and generated metadata.
- [ ] Obtain fresh human approval for that exact preview.
- [ ] Publish only after approval, then verify the dated canonical returns 200 and read back the title, single H1, body, image, metadata, taxonomies, links, and rollback receipt.

Until every item above is complete, this package remains a local `status: draft` and publication must not be claimed.

For a new object there is no prior post snapshot to restore. The pre-write rollback proof is the empty all-status slug result; after creation, the recorded post ID can remain an unpublished draft or be moved to trash if the preview is rejected. No existing post/page, media record, or taxonomy term is in the write set.
