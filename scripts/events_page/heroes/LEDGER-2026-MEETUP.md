# Hero source ledger: 2026 one-offs + Vancouver AI meetup series

**Issue:** #633
**Scope:** 34 catalog rows without a hero (2026 one-offs, the dated Vancouver AI
meetup series, plus `trunorth-ai-leadership-summit-2026`).
**Built:** 2026-08-02
**Status:** research artifact only. No catalog writes, no media uploads, no page
2250 writes, no WordPress calls, no image binaries downloaded. Everything below
is a *candidate* for the ship issue (#635) to act on.

Companion ledger for the 2024/2025 one-off stages lives in
`LEDGER-2024-2025.md` (issue #632, different owner).

---

## How candidates were resolved

Resolution order mirrors `scripts/events_page/fetch_event_heroes.py` (#587):

1. `repo-asset` tracked path already on the record
2. `youtube` maxres thumbnail when a YouTube id is on file
3. `og-image` from a local HTML snapshot or the live event page
4. gap

To that I added one source the engine does not know about yet, and it is what
carried this lane:

**5. `bcai-gallery` - the BC + AI photo-gallery pipeline.**
`/Users/kk/Code/bcai-website/.local-clone/photo-galleries/<slug>/manifest.json`
carries, per photo: `photographer`, `alt`, sometimes `caption`, plus public
Cloudflare R2 CDN URLs at `grid` (800px) and `large` (2048px+) sizes. Gallery
slugs are month-keyed (`vancouver-ai-meetup-2025-10`) and each manifest states
its own `event_date`, so rows were matched by **exact event date**, not by slug
guessing. That mapping resolved 16 of the 23 meetup rows to a real photo from
the actual night.

**Verification.** Every URL printed below was checked with a ranged GET
(`curl -r 0-0 -L -w '%{http_code} %{content_type}'`) on 2026-08-02. R2 assets
return `206 image/webp`, which is a successful ranged 200-class response. Any
URL that did not resolve was dropped, not listed. No unchecked URL appears here.

---

## Rights basis vocabulary

Used consistently in every row. Never upgraded past what the source evidences.

| Token | Meaning |
|---|---|
| `own-channel` | Published on a channel KK owns outright. Cleanest basis in this ledger. |
| `luma-own-event` | Luma cover/social art for an event KK hosts on his own Luma calendar. |
| `bcai-pipeline-credited` | BC + AI gallery pipeline asset on the public BC + AI R2 CDN with a **named** photographer in the manifest. Attribution required. **No explicit license field exists in any manifest.** |
| `bcai-pipeline-credit-unresolved` | Same pipeline, but the manifest names no individual photographer. |
| `bcai-published-credit-unconfirmed` | Already published on bc-ai.ca with a WP media id, but the source manifest itself flags photographer credit as unconfirmed. |
| `third-party-og` | og:image belonging to an outside organization. No license. Not proposed as a hero. |
| `none found` | No defensible source located. Correct answer, not a placeholder. |

### The one honest caveat on `bcai-pipeline-credited`

These photos are unambiguously *Vancouver AI / BC + AI community* photos with a
named photographer. What no manifest states is a license grant. Two supporting
facts, both real, neither a license:

- `content/projects/01-vancouver-ai-community/meetups/2025/10-october/meetup-22-complete-package/README.md`
  states usage rights for that package: internal use unrestricted, public
  sharing encouraged with attribution, media use approved. That is a documented
  BC + AI position, but it is scoped to that one package.
- Prior art exists on kriskrug.co: `van-ai-meetup-31` already ships a Michelle
  Diamond photo live as WP media **12663** with the credit line
  `Michelle Diamond / Diamond's Edge Photography`. So the Michelle Diamond
  reuse pattern is already established on this site.

No comparable precedent exists for **Peter Holst**, **Aaron Hockenstein**, or
**Tristan Brand**. Those three rows want a courtesy check before shipping.
Flagged per row.

Credit-line convention already documented in
`meetups/2026/04-april/meetup-28-publishing-notes.md`:
`Photos: Michelle Diamond, Diamond's Edge Photography`.

### The labelling rule this ledger obeys

Same file carries a standing rule: *do not embed a different month's images in
published posts without labeling them*. Every row below is therefore tagged
`night-specific` or `series-fallback`, and no `series-fallback` alt text claims
the date of the row it sits on.

---

## Alt text honesty note (read before shipping)

I did not download or open any image binary, per lane constraint. So:

- Where the manifest carries a real per-photo **caption**, the proposed alt
  describes the actual frame. Those rows are marked `alt: frame-grounded`.
- Where the manifest carries only a generic template alt (most rows), I could
  not see the frame. Those rows are marked `alt: PROVISIONAL (frame unseen)`
  and the proposed text states only what the record documents. **The ship agent
  must rewrite these to describe the real frame at upload time, when the image
  is on screen.** Do not paste a provisional alt into production as-is.

No proposed alt asserts a venue, an attendance number, or a role that the
catalog or manifest does not already state.

---

## Summary

| Outcome | Rows |
|---|---|
| Night-specific candidate, verified URL, named rights basis | 20 |
| Series-fallback candidate, verified URL, explicitly labelled | 7 |
| `NO SOURCE - needs KK` | 7 |
| **Total** | **34** |

Rights split across all 34:

| Rights basis | Rows |
|---|---|
| `own-channel` | 1 |
| `luma-own-event` | 2 |
| `bcai-pipeline-credited` | 22 |
| `bcai-pipeline-credit-unresolved` | 1 |
| `bcai-published-credit-unconfirmed` | 1 |
| `none found` | 7 |

---

## Section 1: Vancouver AI meetup series, night-specific

Sixteen rows matched a BC + AI gallery whose manifest `event_date` equals the
catalog date exactly. One more (#10) matched a video on KK's own channel.

Frame selection: lowest-`order` photo in the curated gallery whose `large`
derivative is landscape, since the events grid is a landscape card. Curated
`order` is the pipeline's own ranking, so low order means the pipeline already
liked it.

---

### `van-ai-meetup-02` - Vancouver AI Meetup #2, 2024-02-28
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2024-02/large/e5972793df37.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2024-02/manifest.json`, gallery order 1, 2400x1600
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (manifest gallery level; per-photo `photographer` field is null on this one)
- **Proposed alt:** `Vancouver AI Meetup #2, February 2024` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium-high. Date match is exact. Credit is gallery-level rather than per-photo, so the specific frame's shooter is asserted by the gallery, not by the photo record.
- **Note:** catalog `status: scaffold` on this row and `date_confidence: approximate` in `meetup-editions.yaml`. The gallery manifest independently says `2024-02-28`, which agrees with the catalog date and is the strongest date evidence I found for this row.

### `van-ai-meetup-05` - Vancouver AI Meetup #5, 2024-05-29
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2024-05/large/6d0aee1e1d80.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2024-05/manifest.json`, gallery order 0, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** **Peter Holst** (manifest gallery level)
- **Proposed alt:** `Vancouver AI Meetup #5, May 2024` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium-high on the match, **medium on rights**.
- **Flag:** Peter Holst has no existing photo credit anywhere on kriskrug.co. This is the only Peter Holst row in the lane. Courtesy check before shipping.
- **Note:** `meetup-editions.yaml` says this month's folder is "empty/moved" and had no local hero. The BC + AI gallery has 168 photos for it. This row was recorded as unsourced and is not.

### `van-ai-meetup-10` - Vancouver AI Meetup #10, 2024-10-30
- **Kind:** `night-specific`
- **Candidate:** `https://img.youtube.com/vi/bdMVM3LWmfw/maxresdefault.jpg`
- **Verified:** 206 image/jpeg, 2026-08-02
- **Source:** `photo-galleries/2024-10-31-vancouver-ai-community-meetup-10-october-30th/videos.json`, video "Vancouver's AI Community Is Out of Control", described in that file as a recap of the October 30 Space Centre meetup
- **Rights basis:** `own-channel`. Confirmed by reading the watch page: `ownerChannelName` is `Kris Krüg`.
- **Credit:** none required (KK's own channel)
- **Proposed alt:** `Vancouver AI Meetup #10, October 2024` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium. Rights are the cleanest in the ledger. The weakness is that a YouTube thumbnail is a video still or a title card, not a photograph, and I could not see which.
- **BLOCKER for the ship issue, unrelated to the hero:** the catalog `url` for this row is `https://luma.com/letsgo`. **That slug has been recycled.** It now returns HTTP 200 with `og:title` = `Test Event · Luma`. Any og-image path over that URL will pull an unrelated "Test Event" card onto the page. Do not let the hero engine resolve this row via og-image. The Luma link on the card is also now wrong and should be reviewed separately.
- **Note:** the only meetup row in the whole series with no photo gallery but a video. There is no `vancouver-ai-meetup-2024-10` gallery directory.

### `van-ai-meetup-12` - Vancouver AI Meetup #12 (NeurIPS special), 2024-12-15
- **Kind:** `night-specific`, with a caveat
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/2024-12-15-synthesis-vancouver-ai-community-meetup-afterparty-neur/large/4c6107d3bc6a.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/2024-12-15-synthesis-vancouver-ai-community-meetup-afterparty-neur/manifest.json`, gallery order 0, 2400x1601
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** **Tristan Brand** (manifest gallery level *and* per-photo)
- **Proposed alt:** `Synthesis afterparty for the NeurIPS edition of the Vancouver AI Community Meetup, December 2024` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium.
- **Caveat, do not smooth this over:** the gallery is titled *Synthesis: Vancouver AI Community Meetup Afterparty #NeurIPS*. It is the **afterparty**, same date, not the main-room meetup. `meetup-editions.yaml` corroborates: "NeurIPS special; also Synthesis afterparty KKBDAY". Shipping it under a `#12` card is defensible only if the alt says afterparty, as proposed above. If KK wants the main room instead, there is no gallery for it.
- **Flag:** Tristan Brand has no existing credit on kriskrug.co. Courtesy check.

### `van-ai-meetup-13` - Vancouver AI Meetup #13 (one-year anniversary), 2025-01-29
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-01/large/65f1882d2aa2.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-01/manifest.json`, gallery order 0, 2400x1601
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level)
- **Proposed alt:** `Vancouver AI Meetup #13, the one-year anniversary night, January 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match. `meetup-editions.yaml` calls this the numbering-lock anchor and `date_confidence: documented`, and the gallery `event_date` agrees.

### `van-ai-meetup-15` - Vancouver AI Meetup #15, 2025-03-26
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-03/large/76679c7faf5e.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-03/manifest.json`, gallery order 13, 2048x1536
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** manifest says `Michelle Diamond and Aaron Hockenstein` at gallery level. **Which of the two shot this specific frame is not recorded.**
- **Proposed alt:** `Vancouver AI Meetup #15, March 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium. Date match exact, credit ambiguous by two names.
- **Note:** only 7 of the 20 curated photos are landscape here, which is why order 13 rather than order 0. If a portrait crop is acceptable, order 0 is available.
- **Flag:** joint credit. Either credit both names or confirm the individual shooter before shipping. Do not pick one name at random.

### `van-ai-meetup-16` - Vancouver AI Meetup #16, 2025-04-30
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-04/large/725ad37f5d0e.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-04/manifest.json`, gallery order 0, 2400x1600
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** **Aaron Hockenstein** (gallery level)
- **Proposed alt:** `Vancouver AI Meetup #16, April 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** medium-high on the match, **medium on rights**.
- **Flag:** Aaron Hockenstein has no existing credit on kriskrug.co. Courtesy check.
- **Note:** `meetup-editions.yaml` says the April 2025 archive folder is missing entirely. The gallery has 99 photos.

### `van-ai-meetup-19` - Vancouver AI Meetup #19, 2025-07-30
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-07/large/32a828724874.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-07/manifest.json`, gallery order 5, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level **and** per-photo)
- **Proposed alt:** `Vancouver AI Meetup #19, July 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.
- **Note:** only 3 of 20 curated photos are landscape. Thin bench if this frame gets rejected.

### `van-ai-meetup-20` - Vancouver AI Meetup #20, 2025-08-27
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-08/large/b2524ecc24fc.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-08/manifest.json`, gallery order 0, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #20, August 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.
- **Note:** `meetup-editions.yaml` records this as the BC + AI launch night with a Peter Bittner keynote. If a frame of that moment is wanted specifically, it would need an eyeball pass over the 20-photo set. Do not put a keynote claim in the alt without seeing the frame.

### `van-ai-meetup-21` - Vancouver AI Meetup #21, 2025-09-24
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-09/large/106188794d38.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-09/manifest.json`, gallery order 0, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level)
- **Proposed alt:** `Vancouver AI Meetup #21, September 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.

### `van-ai-meetup-22` - Vancouver AI Meetup #22 (film festival + hackathon finale), 2025-10-29
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-10/large/3d97a29abad9.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-10/manifest.json`, gallery order 0, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #22, the first annual BC + AI Film Festival night, October 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.
- **Note:** this is the one row whose source package carries an explicit usage-rights statement (`meetup-22-complete-package/README.md`: public sharing encouraged with attribution). Strongest documented rights position in the lane.

### `van-ai-meetup-23` - Vancouver AI Meetup #23, 2025-11-26
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-11/large/2b26b49f8f84.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-11/manifest.json`, gallery order 1, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #23, November 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.

### `van-ai-meetup-24` - Vancouver AI Meetup #24 (Squatchie Awards), 2025-12-18
- **Kind:** `night-specific`, with two caveats
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2025-12-squatchie/large/e50764ad3bbf.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2025-12-squatchie/manifest.json`, gallery order 0
- **Rights basis:** `bcai-pipeline-credit-unresolved`
- **Credit:** manifest says `Various photographers` and names nobody. **This is the only meetup row in the lane with no attributable human.**
- **Proposed alt:** `Vancouver AI Meetup #24, the Squatchie Awards night, December 2025` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** low-medium.
- **Caveat 1, orientation:** **all 20** curated photos in this gallery are portrait. There is no landscape option. The events grid card is landscape, so this needs a crop decision, not just an upload.
- **Caveat 2, date:** manifest `event_date` is `2025-12-17`. Catalog and `meetup-editions.yaml` both say `2025-12-18`. One-day discrepancy, unresolved. `meetup-editions.yaml` also notes a separate Festivus social on 2025-12-14, so December 2025 has more than one nearby event and the gallery could belong to either date. Do not silently treat the gallery date as proof of the card date.
- **Recommendation:** `needs KK` on credit before this one ships with a photo credit line. It can ship uncredited only if KK says the "Various photographers" set is safe to use that way.

### `van-ai-meetup-25` - Vancouver AI Meetup #25, 2026-01-28
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-01/large/fe723e1105bf.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2026-01/manifest.json`, gallery order 5, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #25, January 2026` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match. 777 photos in the source set, 20 curated, so there is plenty of bench if this frame is rejected.

### `van-ai-meetup-26` - Vancouver AI Meetup #26 (MAC night), 2026-02-25
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-02/large/7c737986f4df.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2026-02/manifest.json`, gallery order 6, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #26, the Mind, AI and Consciousness takeover night, February 2026` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match. MAC framing comes from the catalog label and the event's own video title, not from me.

### `van-ai-meetup-27` - Vancouver AI Meetup #27, 2026-03-25
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-03/large/0e15e947202e.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2026-03/manifest.json`, gallery order 11, 2400x1600
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #27, March 2026` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.
- **Note:** `meetup-editions.yaml` marked this row `hero_hint: missing-no-source` with no Luma URL locked. That assessment is now out of date: there is a full 20-photo curated gallery dated exactly `2026-03-25`.

### `van-ai-meetup-29` - Vancouver AI Meetup #29 (Building the AI Commons), 2026-05-27
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-05/large/cdaad6d3c036.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/vancouver-ai-meetup-2026-05/manifest.json`, gallery order 3, 2048x1365
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Vancouver AI Meetup #29, the Building the AI Commons night, May 2026` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** high on the match.

---

## Section 2: Vancouver AI meetup series, series-fallback

Six 2024 rows have **no gallery, no video, and no per-event Luma URL**. Their
catalog `url` is the Vancouver AI calendar page `https://lu.ma/vancouver-ai`,
which is a calendar, not an event.

I checked what that calendar's og:image gives: a BC + AI Events calendar cover
card (`https://images.lumacdn.com/cdn-cgi/image/.../calendar-cover-images/02/9b27f4fa-6d7d-476f-b66a-c1ba1711e034.png`,
verified 200 image/jpeg, 1200x630). That is a brand card, not a meetup frame,
and six identical brand cards in a row would read as a broken grid. I am
recording it as an available alternative, not the recommendation.

**Recommended instead:** distinct real meetup frames drawn from the two 2024
galleries that do exist, each explicitly labelled `series-fallback` so nothing
implies the frame is from that specific night. Alt text below deliberately
carries **no date and no edition number**.

**KK decision gate for all six:** is a labelled 2024 series frame acceptable on
a numbered card, or do these six stay art-free until real photos surface? I did
not make that call.

| Row | Date | Candidate (all verified 206 image/webp, 2026-08-02) | Source gallery | Credit |
|---|---|---|---|---|
| `van-ai-meetup-01` | 2024-01-31 | `.../vancouver-ai-meetup-2024-02/large/4b0758e73e87.webp` | Feb 2024, order 2 | Michelle Diamond |
| `van-ai-meetup-03` | 2024-03-27 | `.../vancouver-ai-meetup-2024-02/large/c75e44fd2aed.webp` | Feb 2024, order 3 | Michelle Diamond |
| `van-ai-meetup-06` | 2024-06-26 | `.../vancouver-ai-meetup-2024-05/large/3fd7da541a28.webp` | May 2024, order 1 | Peter Holst |
| `van-ai-meetup-07` | 2024-07-31 | `.../vancouver-ai-meetup-2024-05/large/038ce86fee07.webp` | May 2024, order 2 | Peter Holst |
| `van-ai-meetup-08` | 2024-08-28 | `.../vancouver-ai-meetup-2024-05/large/f275651d6633.webp` | May 2024, order 3 | Peter Holst |
| `van-ai-meetup-09` | 2024-09-25 | `.../vancouver-ai-meetup-2024-02/large/b284705b172c.webp` | Feb 2024, order 4 | Michelle Diamond |

URL prefix for all six: `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/`

- **Kind:** `series-fallback` (all six)
- **Rights basis:** `bcai-pipeline-credited` (all six)
- **Proposed alt (all six, identical by design):** `A Vancouver AI Community Meetup night, 2024` - `alt: PROVISIONAL (frame unseen)`
- **Confidence:** low as night evidence, which is the point. High that the frame is a genuine 2024 Vancouver AI meetup photo.
- **Flag:** rows 06, 07, 08 carry the Peter Holst courtesy-check flag.
- **Alternative on file:** BC + AI Events Luma calendar cover, verified 200, if KK prefers one brand card over six photos.
- **Note:** none of these six frames is the same file as any night-specific candidate above, so the grid will not repeat itself.

---

## Section 3: 2026 one-offs and the upcoming meetup

### `2025-04-09-ted2025-community-meetup` - TED2025 Community Meetup
- **Kind:** `night-specific` (event's own cover art, not a photo of the night)
- **Candidate:** `https://images.lumacdn.com/gallery-images/de/a12a3146-d8ca-4e7d-865b-772a559a0a14`
- **Verified:** 200 image/jpeg, 5.57 MB, 2026-08-02
- **Source:** the `img=` parameter inside the og:image URL in the tracked Wayback snapshot at `kk_kb:content/projects/05-marketing-and-outreach/press-and-media/appearances/assets/2025-04-09-ted2025-community-meetup-page.html`
- **Rights basis:** `luma-own-event`. The snapshot's page JSON lists hosts Kris Krüg and Sean Cranbury, presented by Future Proof Creatives, on the Vancouver AI Luma calendar. This is KK's own event's own cover image.
- **Credit:** none identified. Uploader not recorded.
- **Proposed alt:** `Cover art for the TED2025 Community Meetup during TED week in Vancouver` - `alt: frame-grounded` (it is cover art, and the alt says so)
- **Confidence:** high on provenance, medium on suitability, since it is promo art rather than a photo.
- **ENGINE GOTCHA for the ship issue:** the snapshot's literal `og:image` value is the Wayback-rewritten composite
  `https://web.archive.org/web/20250324140102im_/https://social-images.lu.ma/.../api/event-one?...`
  and that URL **returns 404**. `fetch_event_heroes.py` resolving `og_html_path` on this row will fail. The live original at `lu.ma/TED-Vancouver` is gone (that is why the catalog points at Wayback). The working candidate above was recovered by unpacking the `img=` query parameter out of the dead composite URL. Hand this to the ship issue as a manual path, not an engine path.
- **File size note:** 5.57 MB source. Needs downsizing before upload. `heroes/meetups/README.md` asks for under 1 MB.

### `2026-07-09-bc-ai-film-club-july-idea-lab` - BC + AI Film Club July: Idea Lab
- **Kind:** `night-specific`
- **Candidate:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/2026-07-10-ai-film-club-07-09/large/1c73dfc424d5.webp`
- **Verified:** 206 image/webp, 2026-08-02
- **Source:** `photo-galleries/2026-07-10-ai-film-club-07-09/manifest.json`, gallery order 0, 2048x1365. Manifest `event_date` is `2026-07-09`, an exact match to the catalog row despite the directory being named for the 07-10 publish date.
- **Rights basis:** `bcai-pipeline-credited`
- **Credit:** Michelle Diamond (gallery level and per-photo)
- **Proposed alt:** `Wide view of the Film Club room at the Multimodal Media Lab, attendees spread across the tables trading ideas` - **`alt: frame-grounded`**
- **Confidence:** **high.** This is the best row in the lane: exact date match, per-photo credit, and a real per-photo caption ("Wide room view of the Film Club workshop as attendees share ideas, photo 136") that let me write frame-accurate alt without seeing the file. Venue comes from the catalog's own label.
- **Alternative on file:** `https://luma.com/summertime` og:image, verified 200 image/jpeg, og:title `AI Film Club: 07/09 · Luma`, correct event. Promo card rather than a photo.

### `vancouver-ai-meetup-2026-09-30` - Vancouver AI Community Meetup (upcoming)
- **Kind:** `night-specific` (event's own social card)
- **Candidate:** `https://images.lumacdn.com/cdn-cgi/image/format=auto,fit=cover,dpr=1,anim=false,background=white,quality=75,width=800,height=420/event-social/b4/895f0927-b11c-4887-b8ab-7515e2138d90.png`
- **Verified:** 200 image/jpeg, 2026-08-02
- **Source:** live og:image from `https://luma.com/sept-ai`, the exact URL on the catalog row. og:title reads `Vancouver AI Community Meetup: 09/30 · Luma`, which confirms the slug still points at the right event.
- **Rights basis:** `luma-own-event`
- **Credit:** none identified
- **Proposed alt:** `Promo card for the September 30 Vancouver AI Community Meetup` - `alt: frame-grounded` (it is a promo card and the alt says so)
- **Confidence:** high. Matches `hero_hint: luma-og` already on the merge row in `meetup-editions.yaml`. This is the one row where the existing hero engine will resolve correctly with no manual work.
- **Note:** 800x420 is small for the upcoming rich card. Worth checking whether it holds up at hero size.

### `2026-07-08-ai-ethical-futures-lab-morten` - AI Ethical Futures Lab w/ Morten Rand-Hendriksen
- **Kind:** `series-fallback`
- **Candidate:** `https://bc-ai.ca/wp-content/uploads/2026/06/2026-06-04-ai-ethical-futures-lab-4-aefl-room-discussion-wide-16x9-1.jpg`
- **Verified:** 200 image/jpeg, 2026-08-02
- **Source:** `photo-galleries/2026-06-04-ai-ethical-futures-lab-4/asset-manifest.json`, asset `aefl-room-discussion-wide-16x9.jpg`, role `inline_primary`, already published as bc-ai.ca WP media **102013**. Manifest note calls it the strongest public proof photo for the event page.
- **Rights basis:** `bcai-published-credit-unconfirmed`
- **Credit:** **unknown.** The manifest's own `credit_status` field reads: *"Kris/local community photos; confirm photographer credit before public gallery expansion."* I am not upgrading that.
- **Proposed alt:** `People seated in a discussion circle at an AI Ethical Futures Lab session` - `alt: frame-grounded` (from the manifest's own alt_text, which was written by someone who saw the frame)
- **Confidence:** low as a hero for this row.
- **Why it is only a fallback:** this is AI Ethical Futures Lab **#4 on 2026-06-04**. The catalog row is the **2026-07-08 session with Morten Rand-Hendriksen**. Different night, roughly a month apart. No photo set exists for the July 8 session; `series-ai-ethical-futures-lab.md` documents instances only through Meetup 4 in June, and the appearance note's own artifacts list is empty with an open checkbox to attach the session's Luma row and recap "once processed".
- **Alternative on file:** AEFL #4 cover artwork, bc-ai.ca WP media **99521**, `https://bc-ai.ca/wp-content/uploads/2026/04/cover-38.png`, verified 200 image/png. Also #4-specific, so the same wrong-night problem, but it is artwork rather than a photo of identifiable people, which is a lower-stakes reuse.
- **Recommendation:** `needs KK`. Two open questions: is a June-session photo acceptable on a July card, and who took it.

### `trunorth-ai-leadership-summit-2026` - TruNorth AI Leadership Summit
- **Kind:** n/a
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **What exists and why it is not proposed:** `https://www.trunorthai.ca/` serves an og:image at `https://files.cdn-files-a.com/uploads/11213006/800_6a0a22ed1d340.png` (verified 200 image/png, 916 KB). It is the summit organizer's own branded art on the organizer's own CDN. **No license, no permission, third party.** Listing it as a hero candidate would be exactly the rights upgrade this ledger is supposed to refuse. Recorded here only so the next agent does not rediscover it and assume it is usable.
- **#592 standing rule honored:** nothing in this row asserts or implies that KK speaks, keynotes, or panels at TruNorth. The catalog row itself still reads `role: TBD, confirm with Jimmy before claiming speaking slot` and `status: proposed`, which means the renderer skips it anyway. The available art is a generic summit brand card and carries no role claim on its face, but per the issue's instruction I am flagging rather than proposing it.
- **Recommendation:** leave art-free. If KK wants a card here, the correct path is asking the organizer for a usable image at the same time as confirming the role, not scraping the site.

### `2026-01-31-first-tech-challenge-think-award` - FIRST Tech Challenge: Think Award
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-01-31-first-tech-challenge-judge.md` (no images, artifacts point to a text recap); `kk_kb:content/projects/02-bc-ai-ecosystem-nonprofit/community-programs/stem-outreach/` (recap, transcript, dossier, all text, zero image files); BC + AI photo-galleries (no matching slug or date).
- **Extra caution:** this is a youth robotics qualifier at a secondary school. Any photo would carry minors-consent questions on top of rights. Do not source art for this row without KK explicitly steering it.

### `2026-02-01-vibe-working-workshop` - Vibe Working Workshop
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-02-01-vibe-working-workshop.md`; `kk_kb:content/projects/01-vancouver-ai-community/workshops/2026-02-01-vibe-working-workshop.md`; BC + AI photo-galleries.
- **Note:** the workshop doc is a **planning** document. It still reads `Date: February 2026 (TBD)` and proposes a hybrid format at Ethọ́s Lab. The catalog records the event as delivered on 2026-02-01. No photo, no Luma URL, no recording found.

### `2026-03-31-sea-to-sky-gondola-ai-ethics` - Sea to Sky Gondola AI-ethics workshop
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-03-31-sea-to-sky-gondola-ai-ethics-workshop.md`; BC + AI photo-galleries.
- **Why nothing exists:** the appearance note states it plainly. *"Private engagement, no public listing, which is why no sweep ever found it."* Corporate staff training at the Summit Lodge, reconstructed from KK's calendar. There is no public artifact to source from, and staff-training photos would be the client's to release.

### `2026-04-01-global-ai-summit-vancouver-panel` - Global AI Summit Vancouver panel
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-04-01-global-ai-summit-vancouver-moderator.md`; BC + AI photo-galleries.
- **Note:** external event, organizer contact Christine Ni, UBC Robson Square. The appearance record is calendar-derived and was surfaced only in the 2026-07-11 sweep. Any summit photography would be the organizer's, so this is a permission ask, not a search problem.

### `2026-04-12-yvr-ai-welcome-salon-ted2026` - YVR AI Welcome Salon (TED2026 week)
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-04-12-yvr-ai-welcome-salon-ted2026.md`; the full artifact tree at `kk_kb:content/projects/01-vancouver-ai-community/ted2026-yvr-ai-welcome/` (README, landing-page copy, comms portal, eight comms-asset markdown files, **zero image files**); BC + AI photo-galleries.
- **Note:** this one is KK's own event, so rights would be easy if art existed. It does not, in the places I can see. Worth a direct ask: a phone photo from the Alibi Room night would resolve this row instantly.

### `2026-07-09-sfu-ai-panel` - SFU AI panel
- **Candidate:** **NO SOURCE - needs KK**
- **Rights basis:** `none found`
- **Searched:** catalog row (no `url`, `image: {}`); `kk_kb:.../appearances/2026-07-09-sfu-ai-panel.md`; BC + AI photo-galleries.
- **Note:** the appearance note's own follow-up list is still open: *"Confirm exact date, panel title, other panelists, and venue from KK or SFU listing; attach any recording/recap."* and *"No repo artifact exists yet."* The row is thin on facts, not just on art. External organizer, so photography would be SFU's.

---

## Blockers and decision gates for the ship issue (#635)

1. **Photographer sign-off, three names with no precedent on kriskrug.co.**
   Peter Holst (rows 05, 06, 07, 08), Aaron Hockenstein (row 16, plus joint on
   15), Tristan Brand (row 12). Michelle Diamond already has live precedent via
   media 12663, so her rows are the low-risk set.
2. **`van-ai-meetup-24` has no attributable photographer** (`Various
   photographers`) and no landscape frame in the whole gallery. Needs a credit
   ruling and a crop ruling.
3. **`van-ai-meetup-24` date conflict**, manifest `2025-12-17` vs catalog
   `2025-12-18`. Unresolved.
4. **`van-ai-meetup-10`: `luma.com/letsgo` is a recycled slug** now serving
   `Test Event · Luma`. Block the og-image path on this row, and treat the card
   link itself as suspect.
5. **TED2025 og-image path is broken.** The Wayback composite 404s; the working
   candidate had to be extracted by hand from the dead URL's `img=` parameter.
   Do not expect `fetch_event_heroes.py` to resolve this row.
6. **Series-fallback approval** for the six 2024 meetup rows. Labelled 2024
   frames, or no art.
7. **AEFL Morten row**: wrong-night photo plus unconfirmed photographer. Two
   separate approvals needed.
8. **TruNorth stays art-free** unless the organizer grants an image. No role
   claim, in the art or anywhere near it.
9. **Every `PROVISIONAL` alt must be rewritten at upload**, when the image is
   actually visible. 26 of the 27 sourced rows are provisional. Only the film
   club row, the AEFL fallback, the TED2025 cover, and the Sept 30 promo card
   have alt text grounded in something a human actually saw.
10. **File sizes.** `heroes/meetups/README.md` asks for under 1 MB per file. The
    R2 `large` derivatives are 2048px and up; the TED2025 Luma original is
    5.57 MB. Resize on the way in. The `grid` derivative (800px) exists at the
    same key path with `/grid/` swapped for `/large/` if a smaller source is
    preferred.

---

## Facts vs inferences

**Facts, read directly from a source:**
- Every URL status code and content type in this file, checked 2026-08-02.
- Every `event_date`, `photographer`, `alt`, `caption`, and R2 URL, read from
  the BC + AI manifests under `/Users/kk/Code/bcai-website/.local-clone/photo-galleries/`.
- Every catalog date, title, status, and `url`, read from
  `scripts/events_page/events-catalog.yaml`.
- Every hero hint and edition note, read from `scripts/events_page/meetup-editions.yaml`.
- `ownerChannelName` = `Kris Krüg` on video `bdMVM3LWmfw`, read from the watch page.
- `luma.com/letsgo` og:title = `Test Event · Luma`, read live.
- The AEFL `credit_status` string, quoted verbatim from its asset manifest.
- The meetup-22 usage-rights lines and the meetup-28 credit-line convention,
  quoted from their kk-kb READMEs.

**Inferences, mine, and challengeable:**
- That a gallery whose manifest `event_date` equals a catalog row's date is a
  photo set of that row's night. Strong, and it holds for 16 rows, but it is an
  inference from date equality, not a stated link.
- That lowest-`order` landscape is the best hero frame. That is a proxy for the
  pipeline's own curation plus the grid's aspect ratio. I could not see the
  images, so this is a heuristic, not a judgement about the photographs.
- That gallery-level `photographer` applies to a photo whose own `photographer`
  field is null. Reasonable, and it is what the manifest's own alt strings do,
  but it is inherited rather than asserted per frame.
- That the December 2024 Synthesis afterparty set can stand in for the `#12`
  card. Same date, different room. Flagged rather than assumed.
- That six labelled 2024 frames beat six identical brand cards. Aesthetic call,
  KK's to overrule.

**Approval gates:** items 1 through 8 above are KK calls. Nothing in this
ledger has been applied anywhere. Nothing was uploaded, no catalog row was
touched, no page was written, and no image binary was downloaded or committed.
