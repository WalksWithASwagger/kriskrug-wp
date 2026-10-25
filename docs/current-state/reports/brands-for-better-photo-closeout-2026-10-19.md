# Brands for Better photo update closeout — 2026-10-19

**Status:** published on October 7; authenticated WordPress and public reads
reverified on October 19 at 18:59 UTC. This closeout makes no WordPress writes.

## Published change

[Who Pays for the Good Work?](https://kriskrug.co/2026/10/02/brands-for-better-pitch-night-vancouver-2026/)
is WordPress post `12904`, slug `brands-for-better-pitch-night-vancouver-2026`.
KK approved the two-photo replacement after reviewing the local preview.

| Placement | Original file | WordPress media |
|---|---|---|
| Lead and sharing image: Kris speaking | `_A749767.jpg` | `12926` |
| Wider judges panel | `_A749867.jpg` | `12927` |

Both photographs credit [Peter Holst](https://www.instagram.com/peter_holst_photography/).
The five presenter photographs and article prose remain unchanged. The article
still has seven photographs, including its featured image.

## Verification

- Authenticated slug lookup resolves uniquely to published post `12904`, with
  featured media `12926`. The title and original publication date are unchanged.
- Raw body matches the approved October 7 publication exactly. SHA-256:
  `fb60fd284315e0f168f8537907617a548ef57d78928a42ca3f20585f1af9fa47`.
- Normal and cache-busted public requests return HTTP 200, seven photographs,
  six body captions, both replacements, and neither superseded photograph.
- Open Graph and Twitter image tags use the new lead; the canonical URL is unchanged.
- Both replacement image URLs return HTTP 200 with image content types. Their
  WordPress alt text and photographer credits are present.
- `make doctor` completed with warnings about the existing dirty checkout and
  credentials supplied by Varlock. `make status-readonly` resolved all startup
  sources; its existing version assertion expects WordPress 7.0.5 and observes
  7.0.7. That baseline discrepancy is outside this photo closeout.

## Retained evidence and cleanup

The local evidence package is
`~/.codex/visualizations/2026/10/07/01a116c3-9a1c-7422-b86a-e615035d8142/brands-photo-update/`.
It retains the seven original assets, review preview, pre-publish snapshot,
`rollback-payload.json`, proposed payload, upload receipts, October 7 publication
receipt, and October 19 authenticated readback and closeout receipt.

Removed two byte-identical upload copies and the completed one-off publication
script: three files totaling 3,267,776 bytes. `cleanup-receipt-20261019.json`
records their hashes and the retained originals. No development server was started.
The September 30 source gallery and unrelated repository work remain untouched.

Before any future rollback, reverify the post ID, slug, and current content and
obtain approval for the specific live change; do not replay the old payload blindly.
