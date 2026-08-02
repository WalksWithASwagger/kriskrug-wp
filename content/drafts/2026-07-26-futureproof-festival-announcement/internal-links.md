# Link audit: The Bat Signal (Futureproof network follow-up, #645)

Rewritten 2026-08-02 for #645. Supersedes the July 26 FP-4 link audit below the original speaker-list and FATALE links, which are no longer in the body copy (see `speakers.md` and `alt-text.md` addenda for why).

All links re-curled with `curl -sL -o /dev/null -w "%{http_code}"` on 2026-08-02. **17 unique URLs, all HTTP 200.**

## Internal links (1)

- https://kriskrug.co/2026/06/01/long-road-to-futureproof/ — the live origin post this piece follows up on; linked once, early, so this article doesn't retell it.

## External links

### Festival / RSVP / tickets

- https://futureproof.website/
- https://www.futureproof.website/speakers/
- https://www.futureproof.website/speakers/kevin-friel/
- https://www.futureproof.website/tickets/
- https://www.futureproof.website/call-for-talks/
- https://luma.com/futureproof-festival

The single named-speaker link (Kevin Friel) is the one exception to this piece's "link the roster, don't hard-code names" rule. It is there because the copy credits him by name for bringing the BC + AI Film Club into the festival, and a named credit should link to that person's own profile rather than a generic directory. He is publicly listed on the roster with a live profile (HTTP 200).

### Orgs

- https://bc-ai.ca/
- https://bc-ai.ca/events
- https://vancouver.ai/
- https://www.hrmacmillanspacecentre.com/

### Network-receipts lineage (#643 ledger, 6 of the recommended 6-link sequence used)

- https://en.wikipedia.org/wiki/Northern_Voice
- https://mediashift.org/2010/02/true-north-media-house-w2-provide-citizen-media-hub-at-olympics053/
- https://www.flickr.com/photos/kk/albums/72157608995273506/ (PopTech)
- https://blog.ted.com/what-does-tedx-mean-to-me-answering-tedxsummit-photographer-kris-krug/ (TEDxSummit)
- https://www.flickr.com/photos/kk/albums/72157649379627911/ (SXSW Interactive 2013)
- https://www.flickr.com/photos/kk/collections/72157691620626391/ (DENT)

The ledger's optional 7th link (kriskrug.co/about/) was not used in the body; the receipts section carries the "receipts over adjectives" framing in Kris's own words instead of linking out to it.

## Dropped from the July 26 audit (and why)

- **Individual speaker profile links (8 URLs)** — the FATALE/speaker-roster section that hard-coded these is gone. #645's acceptance criteria calls for linking the roster page rather than hard-coding volatile speaker lists; see `speakers.md`'s #645 addendum for the roster-growth reasoning.
- **https://fatalefestival.com/** and the second kriskrug.co post (`.../future-proof-inside-vancouvers-thriving-ai-ecosystem/`) — both belonged to the FATALE-renaming retelling, which this piece deliberately does not repeat (already told in full in *The Long Road to Futureproof*, linked above).
- **Org links for individual speakers** (calmtech.com, ocadu.ca, rxpx.health, zaro.me, tinyghoststudios.com, ethoslab.ca, byteplus.com, theupgrade.ai) — dropped along with the hard-coded speaker list.

## Notes for #500

- Re-curl every URL before draft create, same as the original package's guidance.
- External links open in a new tab with `rel="noopener noreferrer"` in `post.html`, except the single kriskrug.co internal link (no target/rel needed, same-site).
- After publish (KK-gated): click-check every internal and external link on the live post.
