# Issue #4 missing-alt visual review — 2026-08-28

## Scope and outcome

This is a repo-only review packet. It made no WordPress writes.

- All 18 non-pixel missing-`alt` findings from the 2026-08-25 residual audit
  were re-resolved to their exact post and image source.
- Seventeen sources were visually inspected and now have drafted
  `proposed_alt` values in `inventory.csv`.
- The remaining Midjourney hotlink on post 5371 is broken through both the
  public Jetpack URL and its origin. Its proposal remains blank rather than
  guessing from article context.
- None of these proposals is approved for live application by this packet.

## Evidence method

- The 13-image post-2287 gallery was inspected from the current public image
  files. Public WordPress media titles supplied the names; the pixels supplied
  the action and setting.
- The two old local `/images/` files on posts 54 and 61 and the current
  Googleusercontent image on post 7631 were inspected directly.
- The broken Blogspot source on post 41 was recovered from Internet Archive
  capture `20040714110151` and matched to the exact inventoried filename.
- The broken Midjourney UUID on post 5371 had no recoverable visual in the
  checked live/origin paths. A different filename-style image elsewhere in the
  same article was not used as a proxy.

No downloaded review image is committed to the repository.

## Read-only live verification

Authenticated dry runs were executed for all 13 post-2287 block rows, one
media ID at a time and without `--apply`. Every ID now verifies the exact post
ID, slug, URL, raw-content surface, one matching tag, and one `would-change`.

The first pass exposed a real inventory collision for media 2295: the same
page/media pair has both a media-library row and a post-content row. The exact
content selector initially refused the two-row result. It now filters to
`fix_surface=post-content-block`, and an offline regression plus the repeated
authenticated dry run prove that 2295 resolves to exactly one content tag.

## Drafted proposals

| Post | Media/file | Proposed alt |
|---:|---|---|
| 41 | `specstop06282004.jpg` | Apple Cinema Display shown from the front, side, and back against a black background |
| 54 | 12597 | Three-dimensional Spark Online logo with a blue and silver starburst |
| 61 | 12593 | Movable Type book cover reading An Eye to the Future with radiating pink and orange lines |
| 2287 | 2289 | Sharon Anderson Morris speaks into a microphone on the FiReFilms stage |
| 2287 | 2290 | Sally Anderson smiles during a Future in Review gathering |
| 2287 | 2291 | Berit Anderson and Evan Anderson smile together at Future in Review |
| 2287 | 2292 | Brett Horvath of Scout.ai laughs during an onstage conversation at Future in Review |
| 2287 | 2293 | Mark Anderson puts his arm around Sally Anderson at a Future in Review reception |
| 2287 | 2294 | Sharon Anderson Morris smiles while speaking with guests at Future in Review |
| 2287 | 2295 | Sharon Anderson Morris in a dark blazer and orange top at a documentary film event |
| 2287 | 2296 | Sharon Anderson Morris embraces Leah Boyer at Future in Review |
| 2287 | 2298 | Terri Orr and Sharon Anderson Morris smile together at Future in Review |
| 2287 | 2300 | Sharon Anderson Morris speaks at a FiRe 2015 podium |
| 2287 | 2301 | Sharon Anderson Morris and her daughter sit together at Future in Review |
| 2287 | 2302 | Sharon Anderson Morris talks with two attendees at FiRe 2016 |
| 2287 | 2303 | Berit Anderson, Sally Anderson, Sharon Anderson Morris, and Evan Anderson at FiRe 2016 |
| 7631 | Googleusercontent source | Layered digital collage of overlapping human faces and eyes in muted blue, peach, and black |

## Blocked source

| Post | Source | Status | Required decision |
|---:|---|---|---|
| 5371 | Midjourney `16e020d2-b069-4613-827a-f13233d3a392/0_3.webp` | Jetpack cannot fetch it; the origin currently fails | Recover the original, replace the broken image, or remove the tag before drafting alt |

## Apply surfaces and gates

- Post 2287: 13 `post-content-block` rows. PR #914's exact page+media
  selector can stage them individually, but each future apply remains a live
  write requiring fresh approval, a private snapshot, and exact readback.
- Posts 41, 54, and 61: legacy/raw HTML. They need a tested raw-HTML selector;
  post 41 also needs a live-image recovery or replacement decision because its
  current source is broken.
- Post 7631: raw HTML with a Google Docs hotlink. Ingest the reviewed image
  into the media library before rewriting its tag and adding the drafted alt.
- Post 5371: do not draft or apply alt until the missing visual is recovered or
  a replacement/removal is approved.

Do not combine these writes with the three pending media-library targets, the
archive batches 4–6 decision, or the authority-hub packs.

## Repository verification contract

`test_missing_attribute_visual_review_pins_17_proposals_and_one_blocker`
asserts the 18-row set, every page/media-to-proposal mapping, and the explicit
post-5371 blocker. `test_content_selector_ignores_same_page_media_library_row`
pins the surface collision found during live dry-run verification. A proposal
cannot silently move to another image ID or write surface.
