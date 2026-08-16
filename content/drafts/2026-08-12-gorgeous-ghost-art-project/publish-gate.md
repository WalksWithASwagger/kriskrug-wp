# Gorgeous Ghost publish gate

Recommendation: **PUBLISH after preview**.

Repository state: local package prepared; no WordPress object created or updated; no provider state changed.

Public preflight on 2026-08-16: the dated canonical and legacy bare-slug route return `404`; unauthenticated WordPress REST returns no published post or page with the slug. This does not prove that no draft or private object exists.

## Locked editorial payload

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

- [ ] In an authenticated, read-only WordPress check, confirm no post or page in any status already owns `gorgeous-ghost`.
- [ ] Create or update a private WordPress draft through the snapshot-first publisher workflow; do not publish on creation.
- [ ] Compare the exact preview body against `post.html`, including the first image, credits, category, tags, date, canonical, OG metadata, and every link.
- [ ] Confirm the external OG image resolves correctly in the WordPress preview and generated metadata.
- [ ] Obtain fresh human approval for that exact preview.
- [ ] Publish only after approval, then verify the dated canonical returns 200 and read back the title, single H1, body, image, metadata, taxonomies, links, and rollback receipt.

Until every item above is complete, this package remains a local `status: draft` and publication must not be claimed.
