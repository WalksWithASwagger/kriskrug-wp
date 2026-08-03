# Stage photography inventory and rights ledger, Speaking page

**Issue:** [#637](https://github.com/WalksWithASwagger/kriskrug-wp/issues/637), sub-issue of #419
**Built:** 2026-08-02
**Status:** research artifact. No uploads, no page 1887 writes, no theme edits, no WordPress writes of any kind. Every live call was a read-only `GET`.
**Owner of this file:** #637 lane only.

---

## The one-line answer

The prior audit says the repo has **two** genuine stage-action frames. That is wrong, and it is wrong in the useful direction: there are **ten** frames already in the kriskrug.co media library that show Kris Krüg speaking or hosting with a mic in his hand, plus an eleventh already committed in this repo as a theme asset. Evidence and per-frame classification below.

The real blocker is not supply. It is **rights**: the five LaSalle frames, which are the strongest keynote-buyer frames on the site, carry **no photographer record anywhere** (no embedded IPTC credit, no kk-kb note, no manifest). That is the thing KK has to resolve before #419 can put one above the fold.

---

## How I verified

- **Live media library:** `GET https://kriskrug.co/wp-json/wp/v2/media?search=TERM&per_page=100` for `kk-laSalle`, `keynote`, `stage`, `speaking`, `panel`, `meetup`, `conference`, `ChannelNext`, `Whistler`, plus `bass coast`, `futureproof`, `web summit`, `creativemornings`, `workshop`, `audience`, `talk`, `summit`, `presenting`, `mic`, `crowd`, `room`, `festival`, `surrey`, `comox`, `vanai`. `speaking` and `ChannelNext` return zero results.
- **Per-item detail:** `GET /wp-json/wp/v2/media/<id>` for 68 candidates, reading `alt_text`, `caption`, `media_details.width/height`, and `media_details.image_meta.credit` / `.copyright` (the embedded IPTC fields).
- **HTTP status:** every one of the 68 `source_url` values returned **200** on 2026-08-02 (`curl -I`). Zero broken assets in the candidate set.
- **I looked at every frame.** I pulled each candidate through the public Photon resizer (`https://i0.wp.com/<host>/<path>?w=520`, read-only) and built contact sheets. Classifications below are from looking at the image, not from the filename. That is how the misclassifications in the prior docs were caught.
- **Repo:** `find` over all tracked image binaries (210 files, almost all QA screenshots and post illustrations). Exactly one is a stage photograph.
- **Live page readback:** `GET https://kriskrug.co/speaking/` on 2026-08-02.

---

## Section 1: media library, genuine stage-action frames

"Stage-action" means Kris Krüg is visibly speaking or hosting: mic in hand, or presenting to a room. That is the only class that satisfies #419.

All URLs below are `https://kriskrug.co/wp-content/uploads/` + the path shown. All returned **200** on 2026-08-02.

| ID | Path | Dims | What it actually shows | Embedded credit | Rights status |
|---|---|---|---|---|---|
| **11834** | `2026/05/kk-laSalle-both-hands-full-25-scaled.jpg` | 2560x1707 | KK at mic on the LaSalle stage, "Both Hands Full" title slide behind him, audience heads across the bottom third | none | **unknown, needs clearance** |
| **11833** | `2026/05/kk-laSalle-both-hands-full-20-scaled.jpg` | 2560x1440 | Wide from the house. KK small on stage, full seated audience, giant slide reading "What's the one thing you do that you would never want to give up to AI?" | none | **unknown, needs clearance** |
| **11831** | `2026/05/kk-laSalle-both-hands-full-10-scaled.jpg` | 2560x1440 | Tight on KK mid-gesture, mic in one hand, denim vest, slide bokeh behind. Best single-subject frame on the site. | none | **unknown, needs clearance** |
| **11830** | `2026/05/kk-laSalle-both-hands-full-2-scaled.jpg` | 2560x1707 | KK at mic, "The Fears Are Real" slide fully legible, audience foreground | none | **unknown, needs clearance** |
| **11832** | `2026/05/kk-laSalle-both-hands-full-15-scaled.jpg` | 2560x1707 | Very wide house shot. Room, rig, screen, packed rows. KK is small. | none | **unknown, needs clearance** |
| **12669** | `2026/08/vancouver-ai-meetup-november-2024-162-scaled.jpg` | 1707x2560 | KK at mic on a small stage, black beanie, red curtain and Futureproof art wall behind. Portrait orientation. | `michellediamond` | assumed, not on file |
| **12666** | `2026/08/surrey-ai-meetup-june-2025-080.jpg` | 2048x1366 | KK at mic addressing a seated audience, shot over their heads. Dim. | `michellediamond` | assumed, not on file |
| **5814** | `2024/06/VanAICommunity_KK_MichelleDiamond-48-2-scaled.jpg` | 2560x1707 | KK in a red cap holding a mic, hosting a standing room, whole crowd in frame | **`michellekoebke`** | **conflicted, see below** |
| **4518** | `2024/01/Kris-Krug-meetup.jpg` | 2226x1913 | KK at mic, full length, addressing a standing group in his Vancouver Biennale HQ studio. Warm, strong, very "him". | none | unknown |
| **11727** | `2026/05/kk-cmvan-keynote-header.png` | 1280x500 | **A real photograph, not artwork.** Banner crop of the CreativeMornings Vancouver stage: audience from behind, poster on screen, KK at the mic on the right. | none | unknown, likely Michelle Diamond |

**Count: 10.**

One more, identity unresolved:

| ID | Path | Dims | Note |
|---|---|---|---|
| 12146 | `2026/06/vanai21-kris-jonny-stage.png` | 2048x1365 | Two men on a stage in front of a projected screen. The filename says `kris-jonny` and the stored alt says "Kris Krüg on stage during a Vancouver AI community event." Looking at the frame I could not confirm the left figure is KK: the beard and face read differently from 11831 and 12669. **UNVERIFIED identity.** Do not ship it with a Kris claim until KK looks at it. |

### The `michellekoebke` conflict (5814 and its 23 siblings)

Every frame in the June 2024 set (`2024/06/VanAICommunity_KK_MichelleDiamond-*`, media IDs 5774 through 5814, 24 items) has `MichelleDiamond` in the **filename** and **`michellekoebke`** in the embedded IPTC `credit` and `copyright` fields. The string `koebke` appears **nowhere** in `kriskrug-wp` or `kk-kb` (grep, 2026-08-02).

Two readings, and I cannot pick between them from the data: either Michelle Koebke is Michelle Diamond's legal name behind the "Diamond's Edge Photography" business name, or a second photographer's frames were folded into a batch named for the first. **Do not print a credit line for any 5774 to 5814 frame until KK says which.** This is a one-question fix for KK and it unblocks 24 assets.

By contrast the August 2024 set (`2024/09/AI_Meetup_August2024_MichelleDiamond-*`, IDs 6842 to 6854) carries `michellediamond` in the same fields, consistent with the filename.

---

## Section 2: the frames the prior docs got wrong

These are the corrections that matter most, because two of them were queued to ship onto the live page with alt text asserting something false.

### 2a. The two "Michelle Diamond meetup" strip frames do not show Kris Krüg

`content/drafts/2026-07-26-speaking-page/multimedia-rebuild-plan.md` lines 57 and 58 list these as P0/P1 "on-stages strip" assets:

| ID | Path | Draft alt in the plan | What the frame actually is |
|---|---|---|---|
| 6854 | `2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg` | "Kris Krüg speaking at a Vancouver AI community event" | Posed two-person portrait. A grey-haired man in black glasses and a patterned shirt with his arm around a younger man, sticker wall behind. **Kris Krüg is not in this photograph.** |
| 6847 | `2024/09/AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg` | "Kris Krüg hosting a Vancouver AI Community Meetup" | Two men, one in a suit laughing, one bald in a purple patterned shirt holding a mic and a phone. **Kris Krüg is not in this photograph.** |

Both are still 200 and both are genuine Michelle Diamond meetup photos. They are just not photos of Kris. Shipping either with the drafted alt would have put a false claim on a public page and an inaccurate description in a screen reader. Strike both from the Speaking strip.

### 2b. The CreativeMornings header is a photo, not artwork

Three separate docs call media 11727 (`kk-cmvan-keynote-header.png`) generated or promo art:

- `multimedia-rebuild-plan.md` line 59: "Punk Rock AI CreativeMornings Vancouver keynote artwork"
- `2026-07-26-speaking-stages/VISUALS.md` line 15: "Punk Rock AI graphic fallback ... Art, not documentary stage photo"
- `2026-07-26-speaking-page/video-set.md` line 143: "it is promo artwork, not a photo of KK on that stage"

It is a documentary photograph. A 1280x500 banner crop of the CreativeMornings Vancouver room: audience from behind, the "MORE CREATIVE MORE PRODUCTIVE MORE POWERFUL" poster on the screen, KK at the mic on the stage at the right. Same shoot, same shirt, same poster as the punkrockai frame in Section 4.

Practical consequence: video-set.md's conclusion ("there is no owned CreativeMornings stage still in the WP media library") is wrong. There is one. It is just too small and too letterboxed to be a hero, so the recommendation to use YouTube's own poster for that embed still holds. The reasoning was right, the fact was wrong.

### 2c. Alt text that overclaims

| ID | Stored alt | Frame |
|---|---|---|
| 12670 | "Vancouver AI Meetup #4" | A plate of sushi. Accurate in that it is from that meetup, useless as alt text. |
| 2705 | "Kris Krüg Keynote UN Global Youth Summit on HIV Bamako, Mali, Africa" | Two people sitting on a red couch, one holding a mic. Not a keynote stage frame. |
| 12666 | "Vancouver AI Meetup #18" | Filename says `surrey-ai-meetup-june-2025`. The number and the filename disagree. |

None of these are in the Speaking set. Logged so the next lane does not trip over them.

---

## Section 3: the one stage photograph already in this repo

**`theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg`**, 1600x1066, sha256 `86934e9268e7cb6e1ecc7df95bd502006cafb73e038676f9aacba59f3aef0714`.

Publicly served at `https://kriskrug.co/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg`, verified **200 image/jpeg, 231674 bytes**, 2026-08-02. It is **not** in the media library (`?search=vancouver-ai-meetup-30` returns zero).

The frame: KK on the H.R. MacMillan Space Centre planetarium stage, hand raised, red curtain and Meetup 30 projection behind him, and roughly forty audience hands up in response. It is the best "this person owns a room" photograph available anywhere in either repo.

**Photographer identified, with proof.** I matched it byte-for-frame against the BC + AI photo pipeline:

- Source file: `June25_2026_BC+AIEvent_MichelleDiamond-94.jpg`
- Manifest: `/Users/kk/Code/bcai-website/.local-clone/photo-galleries/vancouver-ai-meetup-2026-06/manifest.json`, gallery `event_date` `2026-06-24`, gallery photographer **Michelle Diamond**, per-photo `photographer` **Michelle Diamond**
- Manifest sha of the original: `d685ce1b23b377f356d91a78c3b4bf16741b0f44179eb2a5905fdae36e2f4c3f`
- Manifest caption: "A presenter raises a fist at the mic as dozens of hands shoot up across the packed planetarium theatre."
- I fetched the R2 derivative `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-06/large/d685ce1b23b3.webp` (200) and compared it side by side with the theme file. Identical frame.

The repo sha differs from the manifest sha because the theme copy is a downscaled progressive JPEG with all EXIF stripped. The stripping is why the credit was lost in the first place.

**Rights basis.** KK committed it himself as `feat(home): use the approved Vancouver AI community photo` (commit `6b0ae1d`, 2026-07-25), body text: "the canonical approved event photo". That is KK's own written approval for site use. What it does not do is name the photographer, which is exactly what Section 3 just supplied. Combined with the live Michelle Diamond precedent on this site (media **12663** ships with the credit line `Michelle Diamond / Diamond's Edge Photography`, per `scripts/events_page/heroes/LEDGER-2026-MEETUP.md` lines 68 to 71), this is **the cleanest rights position of any stage frame in the inventory**.

Recommended credit line, matching the convention already documented in kk-kb's `meetup-28-publishing-notes.md`: `Photo: Michelle Diamond, Diamond's Edge Photography.`

---

## Section 4: the hotlinks, flagged

Two live hotlinks to `punkrockai.com` for the same file. Neither is acceptable as a final asset under #419's "images from media library" rule.

**1. On the live page right now.** `GET https://kriskrug.co/speaking/` on 2026-08-02 returns four `<img>` in `<main>`, and image 2 is:

```
https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1
alt="Punk Rock AI portal preview"
```

It sits inside an `aurora-media-card` in the page 1887 content pack, not in a theme file.

**2. Tracked in the theme.** `theme/kk-aurora/parts/speaking-proof-grid.html` line 5:

```html
<img src="https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1800&amp;ssl=1" alt="Kris Krug speaking from stage at a live event" loading="lazy" decoding="async">
```

That part is **not currently rendering** on `/speaking/`: the live HTML contains no `aurora-stage` class. It would ship the hotlink if the part were ever adopted. Do not adopt the pattern.

**What the file actually is.** I fetched `https://www.punkrockai.com/public/photos/michelle-diamond/195.webp` directly: **200 image/webp, 254962 bytes, 1800x1200**. KK at the mic beside the "STOP SAYING BIAS / NAME WHAT YOU'RE SEEING" Algorithmic Justice League poster at CreativeMornings Vancouver, audience heads in the foreground. It is a genuinely excellent stage-action frame and it is Michelle Diamond's work, sitting on a third-party host under a directory literally named `michelle-diamond`.

**Rights status: needs clearance.** There is no clearance record for it anywhere in either repo. Two independent problems: the hosting (fix by ingesting to the media library) and the permission (fix by asking Michelle). Ingesting without asking fixes the smaller problem and makes the bigger one worse.

**Name collision warning.** `punkrockai.com/.../195.webp` (CreativeMornings, 1800x1200) and WP media 6847 `AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg` (August 2024 meetup, 2560x1707) are different photographs from different events that both end in "195". `VISUALS.md` line 13 and `multimedia-rebuild-plan.md` line 58 each refer to "195" meaning different files. Use IDs and full paths, not frame numbers.

---

## Section 5: material that exists but is not on kriskrug.co

Sourced from the BC + AI photo pipeline, same path the #633 hero ledger used. All URLs verified with a ranged `GET` on 2026-08-02 (`206 image/webp` is a successful ranged response).

| Frame | Event | Dims | Photographer | URL |
|---|---|---|---|---|
| `vanai-july2026-69` | Vancouver AI Meetup, 2026-07-29 | 2400x1600 | **Michael Caswell** | `.../vancouver-ai-meetup-2026-07/large/b4717426bf89.webp` |
| `vanai-july2026-59` | same | 2400x1600 | Michael Caswell | `.../vancouver-ai-meetup-2026-07/large/d5b5843b4fe0.webp` |
| `vanai-july2026-58` | same | 2400x1600 | Michael Caswell | `.../vancouver-ai-meetup-2026-07/large/87178a34685a.webp` |
| `April2026_BCAI_MichelleDiamond-82` | BC + AI Film Club, 2026-04-10 | 2048x1365 | Michelle Diamond | `.../2026-04-10-ai-film-club-04-09/large/c7260300e9f4.webp` |
| `April2026_BCAI_MichelleDiamond-165` | same | 2048x1365 | Michelle Diamond | `.../2026-04-10-ai-film-club-04-09/large/525ee90dc68d.webp` |

URL prefix for all five: `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/`

I looked at the three July frames. `-69` is the strongest wide hero candidate in this entire document: KK mid-gesture on stage in front of the full-bleed Futureproof "VANCOUVER, WE NEED TO TALK ABOUT AI" mural slide, red curtain, native 3:2, 2400px. `-59` and `-58` are tight portraits of KK at the mic under stage light, both clean.

**Rights caveat, do not smooth this over.** Michael Caswell has **no photo credit anywhere on kriskrug.co**. He is in the same category the #633 ledger flagged for Peter Holst, Aaron Hockenstein, and Tristan Brand: a named photographer in a BC + AI manifest with no license field and no precedent on this site. Rights basis is `bcai-pipeline-credited`, which means attribution is required and a licence is not evidenced. Courtesy check before anything ships.

---

## Section 6: hero recommendation for #419

#419's binding criterion: a stage photo or video visible **without scrolling** at 1440 and 390.

### The pick

One art-directed pair from the same night, so the two breakpoints read as one composition rather than two different photos:

| Breakpoint | Asset | Native | Crop |
|---|---|---|---|
| **1440** | media **11833** | 2560x1440, native 16:9 | Full-bleed, no crop needed at 1x, 1.78x DPR headroom. Keep the slide legible: it reads "What's the one thing you do that you would never want to give up to AI?", which does the selling on its own. Keep at least two rows of audience at the bottom. Text and CTA sit in an adjacent column or on a bottom scrim, not over the slide. |
| **390** | media **11831** | 2560x1440 | Crop to 4:5 around KK's face, mic hand, and gesturing hand. Anchor the crop box on the head, do not centre-crop (that loses the mic). At 4:5 from a 1440px-tall source you get roughly 1150x1440, so 2.9x DPR headroom at 390 CSS px. Event label below the image, per the VISUALS.md 375 row. |

Rationale: 11833 proves the room, 11831 proves the person, both are LaSalle, same lighting, same wardrobe, same green-and-teal palette. Alternate for 1440 if KK wants the talk title visible instead of the question: 11834 (2560x1707, "Both Hands Full" title slide), crop to 16:9 off the top.

### The gate on the pick

**Both 11833 and 11831 have no recorded photographer.** No IPTC credit in the file, nothing in the kk-kb appearance record `2026-01-14-lasalle-college-vancouver-keynote.md`, nothing in the full artifact folder `content/knowledge/keynotes/2026-01-14-lasalle-college-vancouver/` (17 files, all text and slides, `seo-and-images.md` contains only generative image prompts). Nothing in `media-manifest.json`. Nobody wrote it down.

That is a **KK question, not a research problem.** Who shot the LaSalle night, and is the site clear to use those five frames? One answer unlocks the best hero on the site.

### The fallback that needs no new answer

If the LaSalle photographer cannot be established quickly, ship the hero with the **theme asset from Section 3** (Meetup 30 planetarium, Michelle Diamond, KK-approved in commit `6b0ae1d`), ingested to the media library first.

- 1440: native 1600x1066 is 3:2. It covers 1440 CSS px at 1x with 160px to spare, and does **not** cover 2x DPR. Accept slight softness on retina, or ask Michelle for the original (the pipeline has a 2048px derivative and the source is larger still).
- 390: crop to 4:5 on KK plus the nearest raised hands. The composition survives it because the hands are close to him.
- Tradeoff to state plainly: it reads as community-host energy, not keynote-buyer energy. It answers "does this person command a room" better than it answers "will this person deliver my keynote". If the page has to lead with one photo and it is this one, the copy has to carry the keynote claim.

### If neither clears

Then #419's above-the-fold criterion cannot be met with a photo, and the page lane must lead with video. Report that early, per the issue's own instruction. The video lane already has a clean rights position: LaSalle, ChannelNEXT, and Bass Coast are on `@feelmoreplants` under Creative Commons Attribution, confirmed live in `video-set.md`.

---

## Section 7: alt text

Pattern from `VISUALS.md` line 39: `Kris Krug [action] at [event], [context].` Credit goes in the caption or figcaption, **never** in alt.

Spelling note: the pattern in VISUALS.md is written without the umlaut, but media 11830 to 11834 already store "Kris Krüg" in their live alt. I have used "Kris Krüg" throughout for consistency with what is already on the site. `ü` is inside latin1, so it is safe for this database (unlike the combining-diacritic problem logged for SEO meta fields).

| Asset | Alt | Caption |
|---|---|---|
| 11833 | `Kris Krüg speaking on stage at LaSalle College Vancouver, a full audience facing a slide that asks what one thing you would never give up to AI.` | `LaSalle College Vancouver, Both Hands Full keynote.` plus photographer once known |
| 11831 | `Kris Krüg speaking with a microphone at LaSalle College Vancouver, mid-gesture in front of a projected slide.` | `LaSalle College Vancouver, Both Hands Full keynote.` plus photographer once known |
| 11834 | `Kris Krüg speaking on stage at LaSalle College Vancouver, the Both Hands Full title slide behind him and the audience in the foreground.` | `LaSalle College Vancouver, Both Hands Full keynote.` plus photographer once known |
| 11830 | `Kris Krüg speaking on stage at LaSalle College Vancouver, a slide headed The Fears Are Real behind him.` | `LaSalle College Vancouver, Both Hands Full keynote.` plus photographer once known |
| 11832 | `Kris Krüg presenting to a packed theatre at LaSalle College Vancouver, seen from the back of the room.` | `LaSalle College Vancouver, Both Hands Full keynote.` plus photographer once known |
| theme asset, Meetup 30 | `Kris Krüg speaking on stage at the Vancouver AI Community Meetup, dozens of audience hands raised in the H.R. MacMillan Space Centre planetarium.` | `Vancouver AI Community Meetup 30, H.R. MacMillan Space Centre, June 2026. Photo: Michelle Diamond, Diamond's Edge Photography.` |
| 12669 | `Kris Krüg speaking with a handheld microphone at a Vancouver AI Community Meetup, a red curtain and community art wall behind him.` | `Vancouver AI Community Meetup, November 2024.` plus credit once the Diamond permission is confirmed |
| 4518 | `Kris Krüg speaking with a microphone at a Vancouver AI Community Meetup, addressing a standing crowd in his Vancouver Biennale studio.` | `Vancouver AI Community Meetup at the Vancouver Biennale HQ studio, January 2024.` |
| 12666 | `Kris Krüg speaking with a microphone at a Surrey AI Meetup, seen over the heads of a seated audience.` | `Surrey AI Meetup, June 2025.` plus credit once confirmed |
| 5814 | `Kris Krüg speaking with a microphone at a Vancouver AI Community Meetup, the room standing around him.` | **Hold.** Cannot write a caption until the Diamond / Koebke credit conflict is resolved. |
| `vanai-july2026-69` (R2) | `Kris Krüg speaking on stage at the Vancouver AI Community Meetup, a Futureproof Festival slide reading Vancouver, we need to talk about AI filling the screen behind him.` | `Vancouver AI Community Meetup, July 2026. Photo: Michael Caswell.` **Pending Caswell courtesy check.** |
| punkrockai 195 | `Kris Krüg speaking with a microphone at CreativeMornings Vancouver, an Algorithmic Justice League poster reading Stop Saying Bias on the screen beside him.` | `CreativeMornings Vancouver, Punk Rock AI. Photo: Michelle Diamond.` **Do not use until cleared and ingested.** |
| 11727 | `Kris Krüg speaking on stage at CreativeMornings Vancouver, seen across the seated audience.` | `CreativeMornings Vancouver, May 2026.` Low resolution, strip use only, not hero. |
| 12146 | **None written.** Identity unconfirmed. Do not write a Kris alt for a frame nobody has confirmed is Kris. |

Note: 11830 to 11834 currently ship alt text of the form "Kris Krüg presenting Both Hands Full keynote at LaSalle College Vancouver", followed by an em dash and "frame N". That is a filename with a label on it, not a description of the frame, and the em dash violates the house style. The strings above replace them.

---

## Section 8: the gap against #419

**What #419 needs:** a stage photo or video visible without scrolling at 1440 and 390.

**Where the live page stands today** (`GET https://kriskrug.co/speaking/`, 2026-08-02, still matching the 2026-07-26 audit):

- 4 `<img>` in `<main>`. The first photograph of KK on a stage is **#4** (media 11831 via Photon).
- Images 1 and 2 are third-party hotlinks. Image 3 is a keynote graphic.
- **0 `<iframe>`** in the entire document. No talk videos at all.
- Everything before image 4: page chrome, the Speaking kicker, the H2, the lead paragraph, and the four-card Formats grid. Nobody sees Kris on a stage at either breakpoint without scrolling.

**What is actually missing to close it.** Not photographs. Three things:

1. **A rights answer on LaSalle.** Five strong frames, zero recorded photographer. This is the single highest-leverage unblock in the issue and it is one question to KK.
2. **A media-library ingest of the Meetup 30 theme asset.** It is the only frame with both a named photographer and written KK approval, and it is sitting at a theme path where the crop system and Jetpack sizing cannot reach it. `content/drafts/2026-07-26-creative-labs/layout-image-crops.md` line 62 already flags this. Owned by a later apply issue, not this one.
3. **A page-architecture change.** Even with a cleared photo, nothing changes unless the hero band moves above the Formats grid. That is the #419 page lane, not this one. This inventory removes the excuse, it does not do the work.

**Coverage gaps by event.** `VISUALS.md` line 19 asks for wide action frames for five events. Where each stands after this sweep:

| Event | Status |
|---|---|
| ChannelNext | **Nothing.** `?search=ChannelNext` returns zero. No frame in either repo, no BC + AI gallery. The talk video exists; the photography does not. |
| Whistler Institute | **Nothing photographic.** Media 12715 is a YouTube thumbnail composite (branded card with KK cut out over a graphic background), not a frame. |
| Bass Coast Brain Stage | **Nothing photographic.** Media 12716 and `scripts/events_page/heroes/one-offs-2025/2025-07-11-bass-coast-brain-stage-youtube.jpg` are the same YouTube thumbnail with title text burned in. |
| Web Summit Vancouver | **Nothing.** The twelve `web-summit-vancouver-2026` items (11816 to 11825, 11781) are all 1672x941 or 1280x500 graphics, no stage frames. |
| Futureproof Festival | **Nothing of KK on a Futureproof stage.** 12649 and 12662 are the salmon starfield poster art. The closest thing that exists is `vanai-july2026-69`, KK presenting *about* Futureproof at a Vancouver AI meetup, which is a different claim. |
| CreativeMornings | Partially covered, badly. One low-res library banner (11727) and one uncleared hotlink (punkrockai 195). |

---

## Section 9: shooting and sourcing list for KK

Ordered by how much it unblocks per unit of KK effort.

1. **Answer the LaSalle question.** Who shot the January 2026 LaSalle College night, and are those five frames clear for the site? Unblocks the best hero available.
2. **Answer the Diamond / Koebke question.** Is `michellekoebke` in the IPTC of the June 2024 set the same person as Michelle Diamond? Unblocks 24 assets, one of which (5814) is a genuine hosting frame.
3. **Confirm reuse scope with Michelle Diamond, once, broadly.** She is the photographer on the Meetup 30 hero, the November 2024 frame, the Surrey frame, the CreativeMornings hotlink, and most of the BC + AI meetup archive. There is live precedent on this site (media 12663) and an open checkbox for exactly this in `content/drafts/2026-07-31-ai-lands-inside-every-profession/publish-gate.md` line 12. One conversation clears most of the inventory.
4. **Courtesy-check Michael Caswell.** Three good July 2026 stage frames, a name with no precedent on kriskrug.co.
5. **Shoot or source the missing five.** ChannelNext, Whistler, Bass Coast, Web Summit Vancouver, Futureproof. For the past ones, the organizer's photographer is the only path and it is a permission ask, not a search problem. For Futureproof, KK controls the event, so this is the easy one: brief a shooter before the next festival and specify **wide, mic visible, slides visible, audience in frame, landscape, shot from the house not the wings**. That is the frame class the whole Speaking page has been short of for a year.
6. **Get the Meetup 30 original from Michelle.** The theme copy is a downscaled, EXIF-stripped 1600px JPEG. The pipeline has a 2048px derivative and the camera original is bigger. Retina hero needs it.

---

## Section 10: who needs asking, and by whom

**Nothing has been drafted to send. No outreach of any kind has happened.** KK sends these in his own words.

| Person | For which frames | Why |
|---|---|---|
| **Unknown, KK to name** | media 11830, 11831, 11832, 11833, 11834 (LaSalle) | No photographer recorded anywhere. KK has to identify them before anyone can be asked. |
| **Michelle Diamond** | theme Meetup 30 asset, media 12669, 12666, punkrockai 195.webp, and the April 2026 Film Club frames | Named in every relevant manifest. Live precedent exists (media 12663, credit line `Michelle Diamond / Diamond's Edge Photography`). The ask is a scope confirmation, not a cold ask. |
| **Michelle Diamond or Michelle Koebke** | media 5774 to 5814, 24 frames | Resolve the name conflict first, then ask. |
| **Michael Caswell** | `vanai-july2026-58`, `-59`, `-69` | Named per-photo in the July 2026 manifest. No precedent on kriskrug.co. Courtesy check. |

**Existing outreach pattern to copy:** `content/drafts/2026-08-01-testimonials-overhaul/consent-outreach.md`. It is a testimonials-consent file, not a photo-rights file, but the shape is right and it already establishes the house rule at the top: *"Nothing here has been sent. This file is a shortlist and a set of drafts. Sending is a human action, and KK does the sending in his own words."* Its companion `consent-log.md` is the right model for a photo-rights log if this grows into one.

---

## Section 11: on the manifest deliverable

#637 names `content/source-packs/site-photography-2026/speaking-stage-manifest.json` as the output. **I did not create it, deliberately.**

`media-manifest.json` and `scripts/notion-to-wp/ingest_media_manifest.py` are an **ingestion** contract: every entry points at a local file under `assets/` with a sha256, and the tool's job is to upload it if it is not already there. That does not fit this inventory:

- Ten of the eleven stage frames are **already in the media library**. There is nothing to ingest and no local file to hash.
- The one that is not (the theme asset) is the only valid manifest row, and it is a single row.
- Every other candidate is either uncleared (punkrockai 195, the Caswell frames) or off-site. Writing them into an ingestion manifest, even with `rights_basis: "needs clearance"`, builds a loaded gun: one `--execute` and they are uploaded.

The honest artifact for uncleared assets is a ledger, which is this document. When KK answers the LaSalle and Diamond questions, a one-row or two-row manifest for the assets that genuinely need uploading is a five-minute job for the apply lane, and it can be written against real answers rather than placeholders.

If the reviewer wants the JSON anyway, say so and I will write it with `rights_basis` set to the literal strings in this document, no upgrades.

---

## Facts and inferences

**Facts, read directly from a source on 2026-08-02:**

- Every media ID, path, dimension, stored alt, stored caption, and embedded IPTC `credit` / `copyright` value, from `GET /wp-json/wp/v2/media/<id>`.
- Every HTTP status in this document, from `curl`.
- Every visual classification. I looked at each frame through the public Photon resizer before writing what it shows.
- The live `/speaking/` structure: 4 images in `<main>`, first KK stage photo at position 4, 0 iframes, punkrockai hotlink present in an `aurora-media-card`, no `aurora-stage` class present.
- The theme-part hotlink at `theme/kk-aurora/parts/speaking-proof-grid.html` line 5.
- Commit `6b0ae1d` and its message, from `git log`.
- The Meetup 30 frame match: manifest entry, photographer field, caption, R2 URL, and my own side-by-side comparison of the R2 derivative against the theme file.
- `koebke` returning zero hits across both repos.
- The Michelle Diamond precedent (media 12663, credit line) as recorded in `scripts/events_page/heroes/LEDGER-2026-MEETUP.md` lines 68 to 71. I did not independently re-verify 12663 on the live site.

**Inferences, mine, and challengeable:**

- That 11727 (`kk-cmvan-keynote-header.png`) and punkrockai `195.webp` are from the same CreativeMornings shoot. Based on matching venue, wardrobe, poster style, and subject. Not proven by metadata.
- That 11727's photographer is likely Michelle Diamond. Based on the same shoot inference. **Recorded as unknown, not upgraded.**
- That the theme asset's Michelle Diamond credit transfers to the theme copy. The copy is EXIF-stripped, so the attribution rests entirely on the frame match, which I did visually.
- That the person in media 12146 may not be Kris Krüg. My read of the frame against 11831, 12669, and the 12629 portrait. The filename and the stored alt both say Kris and I could be wrong. **Recorded as UNVERIFIED, not as a correction.**
- That 11833 plus 11831 is the right hero pair. An art-direction call. KK's to overrule.

**Nothing in this document has been applied anywhere.** No upload, no media edit, no page write, no theme edit, no message sent.
