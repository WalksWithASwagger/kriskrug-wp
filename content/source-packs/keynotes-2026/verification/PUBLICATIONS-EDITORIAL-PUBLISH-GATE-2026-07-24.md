# Publications editorial publish gate

Status: review-ready, not approved for public deployment.

## Exact target

- Public URL: `https://kriskrug.co/publications/`
- WordPress page ID: `1895`
- Slug: `publications`
- Status: `publish`
- Live modified value observed through public REST: `2026-07-23T21:43:45`
- Review branch: `codex/publications-editorial-archive`
- Draft pull request: `#454`

## Current live evidence

A cache-bypassed fetch on July 24, 2026 returned the legacy Publications layout.
The live HTML contains `kk-publications-display` and does not contain the proposed
`kk-press-display` marker. The Tyee story is present as a card inside the older
layout.

Public HTML SHA-256 at the review point:

`c00d07f2138adca0e889e09c35b67e5bbd42e8a867aa9ae13d9f13ed72fa168d`

The hash is drift evidence, not a rollback source. An authenticated
`context=edit` snapshot is still required immediately before any write.

## Proposed media set

1. `press-2026-07-24-the-tyee-context.jpg`
2. `press-2026-06-15-biv-context.jpg`
3. `press-2026-05-20-storyhive.jpg`
4. `press-2026-02-09-tela-viva-context.jpg`
5. `press-2025-07-09-e-channelnews-context.jpg`
6. `press-2025-05-01-portfolio-yvr-context.jpg`

See `../assets/publications-press-media.md` for provenance, exclusions, and
credit requirements.

## Voice gate

- Voice source: `/Users/kk/Code/kk-voice/crystal.md`
- Dominant facet: The Host
- Secondary facet: The Anti-Hero, used lightly
- Mechanical audit: one quoted Popular Science headline exception
- Audit packet: `../wp-payloads/voice-audit/publications-editorial-20260724/`
- Human voice review: pending Kris

The two manual audit findings were applied and mechanically rechecked. Public
publication still requires Kris to confirm that the rendered page sounds like
him.

## Required approval

The exact approval needed for the next production step is:

> Approve the six-file Publications media set and publish PR #454 to WordPress page 1895.

Layout approval alone does not authorize media upload or public publication.

## Deployment sequence after approval

1. Refresh PR `#454`, required checks, and the live page modified value.
2. Fetch page `1895` with authenticated `context=edit`.
3. Save the complete raw page and SEO metadata as the rollback snapshot.
4. Upload only the six approved media files to the WordPress Media Library.
5. Apply the documented alt text, outlet credit, and photographer credit.
6. Replace every `../assets/` image path with its uploaded WordPress media URL.
7. Assert that no relative image paths or third-party image URLs remain.
8. Produce and review an exact content and SEO metadata diff.
9. Update only page `1895`.
10. Read back the raw WordPress content and metadata.
11. Fetch the public page with a fresh cache-bypass query.
12. Verify the new markers, all six images, 47 coverage links, desktop layout,
    390-pixel mobile layout, and zero horizontal overflow.
13. Record the after-state and the exact restore command.

## Rollback

Restore page `1895` from the authenticated pre-write `content.raw` and SEO
metadata snapshot. Do not delete uploaded media during emergency rollback. Media
cleanup is a separate destructive action and requires a later approval.

## Not yet run

- Authenticated pre-write snapshot
- WordPress Media Library uploads
- Final media URL substitution
- Production write
- Cache purge
- Cache-bypassed production visual verification
