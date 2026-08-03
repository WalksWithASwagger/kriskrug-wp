# Stage photography inventory and rights ledger, Speaking page

**Issue:** [#637](https://github.com/WalksWithASwagger/kriskrug-wp/issues/637), sub-issue of #419
**Built:** 2026-08-02
**Status:** research artifact. No uploads, no page 1887 writes, no theme edits, no WordPress writes of any kind. Every live call was a read-only `GET`.
**Owner of this file:** #637 lane only.

---

## The one-line answer

The prior audit says the repo has **two** genuine stage-action frames. That is wrong, and it is wrong in the useful direction: there are **ten** frames already in the kriskrug.co media library that show Kris Krüg speaking or hosting with a mic in his hand, plus **two more already committed as tracked files in this repo**. Twelve total. Evidence and per-frame classification below.

**Correction pass, 2026-08-02.** An adversarial verifier audited the first version of this file and found eight defects. Six were real and are fixed here; two were partly right and are narrowed. The biggest miss: the first version said this repo held exactly one stage photograph. It holds two. `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg` is a tracked local copy of the same punkrockai.com frame that Section 4 treated as existing only as a third-party hotlink. Every count in this document has been re-derived from a fresh command, not carried forward. Dispositions are logged on PR #657.

The real blocker is not supply. It is **rights**: the five LaSalle frames, which are the strongest keynote-buyer frames on the site, carry **no photographer record anywhere** (no embedded IPTC credit, no kk-kb note, no manifest). That is the thing KK has to resolve before #419 can put one above the fold.

---

## How I verified

- **Live media library:** `GET https://kriskrug.co/wp-json/wp/v2/media?search=TERM&per_page=100` for `kk-laSalle`, `keynote`, `stage`, `speaking`, `panel`, `meetup`, `conference`, `ChannelNext`, `Whistler`, plus `bass coast`, `futureproof`, `web summit`, `creativemornings`, `workshop`, `audience`, `talk`, `summit`, `presenting`, `mic`, `crowd`, `room`, `festival`, `surrey`, `comox`, `vanai`. `speaking` and `ChannelNext` return zero results.
- **Per-item detail:** `GET /wp-json/wp/v2/media/<id>` for 68 candidates, reading `alt_text`, `caption`, `media_details.width/height`, and `media_details.image_meta.credit` / `.copyright` (the embedded IPTC fields).
- **HTTP status:** every one of the 68 `source_url` values returned **200** on 2026-08-02 (`curl -I`). Zero broken assets in the candidate set.
- **Visual inspection, and its exact boundary.** Every frame I make a "what it shows" claim about in this document was pulled through the public Photon resizer (`https://i0.wp.com/<host>/<path>?w=440`, read-only) and assembled into contact sheets that I looked at. That is how the misclassifications in the prior docs were caught. It is **not** true that I eyeballed all 131 candidates. The rosters in Sections 1, 3, 3b, 3c and 3d mark each row `viewed` or `metadata only`, and `metadata only` rows are classified from filename, stored alt, dimensions and IPTC credit alone. Do not treat those as visually confirmed.
- **Candidate sweep, re-run on 2026-08-02 for this correction pass:** 19 search terms (`meetup`, `keynote`, `conference`, `panel`, `workshop`, `audience`, `stage`, `crowd`, `talk`, `summit`, `festival`, `creativemornings`, `vanai`, `futureproof`, `surrey`, `comox`, `bass coast`, `web summit`, `whistler`) against `GET /wp-json/wp/v2/media?search=TERM&per_page=100&media_type=image`. **131 unique image IDs.** `audience` returns zero. `speaking` and `ChannelNext` returned zero in the first sweep and are not in the retained term list.
- **Repo:** `git ls-files | grep -Ei '\.(jpg|jpeg|png|gif|webp|svg|avif)$' | wc -l` returns **210** tracked image binaries, almost all QA screenshots and post illustrations. **Two** of the 210 are stage photographs of Kris Krüg. Both are named in Section 3.
- **Live page readback:** `GET https://kriskrug.co/speaking/` on 2026-08-02.

---

## Section 1: bucket A, stage-action

This is the first of three buckets. #637 asks for every candidate sorted into **stage-action**, **portrait**, or **event-ambience**. Bucket A is here, bucket B (portrait) is Section 3b, bucket C (ambience) is Section 3c, and the leftovers that are none of the three are Section 3d.

"Stage-action" means Kris Krüg is visibly speaking or hosting: mic in hand, or presenting to a room. That is the only class that satisfies #419. A frame of somebody *else* speaking is not stage-action for this purpose, it is ambience, and Section 3c has several.

All URLs below are `https://kriskrug.co/wp-content/uploads/` + the path shown. All returned **200** on 2026-08-02. Every row in this table was **viewed** during the 2026-08-02 correction pass, not taken on filename.

| ID | Path | Dims | What it actually shows | Embedded credit | Rights status |
|---|---|---|---|---|---|
| **11834** | `2026/05/kk-laSalle-both-hands-full-25-scaled.jpg` | 2560x1707 | KK at mic on the LaSalle stage, "Both Hands Full" title slide behind him, audience heads across the bottom third | none | **unknown, needs clearance** |
| **11833** | `2026/05/kk-laSalle-both-hands-full-20-scaled.jpg` | 2560x1440 | Wide from the house. KK small on stage, full seated audience, giant slide reading "What's the one thing you do that you would never want to give up to AI?" | none | **unknown, needs clearance** |
| **11831** | `2026/05/kk-laSalle-both-hands-full-10-scaled.jpg` | 2560x1440 | Tight on KK mid-gesture, mic in one hand, denim vest, slide reading "AI is the assistant, I'm the decider" behind. Best single-subject frame on the site. | none | **unknown, needs clearance** |
| **11830** | `2026/05/kk-laSalle-both-hands-full-2-scaled.jpg` | 2560x1707 | KK at mic, "The Fears Are Real" slide fully legible, audience foreground | none | **unknown, needs clearance** |
| **11832** | `2026/05/kk-laSalle-both-hands-full-15-scaled.jpg` | 2560x1707 | Very wide house shot. Room, rig, screen, packed rows. KK is small. | none | **unknown, needs clearance** |
| **12669** | `2026/08/vancouver-ai-meetup-november-2024-162-scaled.jpg` | 1707x2560 | KK at mic on a small stage, black beanie, red curtain and Futureproof art wall behind. Portrait orientation. | `michellediamond` | assumed, not on file |
| **12666** | `2026/08/surrey-ai-meetup-june-2025-080.jpg` | 2048x1366 | Dim room. KK (beard, patterned shirt, arms out) presenting at the front with a **second person** beside him, seated audience in silhouette across the bottom. **Narrowed on re-view:** a microphone is not resolvable at this size, so this is "presenting", not "at mic". | `michellediamond` | assumed, not on file |
| **5814** | `2024/06/VanAICommunity_KK_MichelleDiamond-48-2-scaled.jpg` | 2560x1707 | KK in a red cap holding a mic, hosting a standing room, whole crowd in frame | **`michellekoebke`** | **conflicted, see below** |
| **4518** | `2024/01/Kris-Krug-meetup.jpg` | 2226x1913 | KK at mic, full length, addressing a standing group in his Vancouver Biennale HQ studio. Warm, strong, very "him". | none | unknown |
| **11727** | `2026/05/kk-cmvan-keynote-header.png` | 1280x500 | **A real photograph, not artwork.** Banner crop of the CreativeMornings Vancouver marquee: audience from behind, the Punk Rock AI "MORE CREATIVE. MORE PRODUCTIVE. MORE POWERFUL." slide on a flat-panel screen left of centre, KK at the mic just right of centre, Vancouver Art Gallery lectern and the CreativeMornings Vancouver banner at the right. | none | unknown, Michelle Diamond strongly indicated (Section 4) |

**Media-library count: 10.**

Plus two tracked local files, both stage-action, neither in the media library:

| File | Dims | What it shows | Rights status |
|---|---|---|---|
| `theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg` | 1600x1066 | KK on the planetarium stage, fist up, roughly forty audience hands raised | **Best position in the inventory.** KK-approved in writing, photographer identified. Section 3. |
| `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg` | 1200x800 | KK at the mic beside the "STOP SAYING BIAS / NAME WHAT YOU'RE SEEING" Algorithmic Justice League slide, audience heads in the foreground | **No clearance on file.** It is a local copy of the punkrockai.com hotlink. Section 3a and Section 4. |

**Stage-action total: 12.**

One more, identity unresolved:

| ID | Path | Dims | Note |
|---|---|---|---|
| 12146 | `2026/06/vanai21-kris-jonny-stage.png` | 2048x1365 | Two men on a stage in front of a projected screen. The filename says `kris-jonny` and the stored alt says "Kris Krüg on stage during a Vancouver AI community event." Re-viewed on 2026-08-02: the left figure has the right build, glasses, tied-back hair and a beard, but the beard reads darker and fuller than in 11831 or 12669, and neither man is at a mic. **UNVERIFIED identity, and not stage-action either way.** Do not ship it with a Kris claim until KK looks at it. |

### The `michellekoebke` conflict (5814 and its 22 siblings)

**Corrected count.** The June 2024 set is **23 items, not 24.** `curl -sI "https://kriskrug.co/wp-json/wp/v2/media?search=VanAICommunity&per_page=100"` returns `x-wp-total: 23` on 2026-08-02, and enumerating the response gives exactly 23 IDs: 5774, 5775, 5776, 5777, 5778, 5786, 5787, 5790, 5791, 5792, 5793, 5794, 5795, 5796, 5797, 5799, 5800, 5804, 5807, 5808, 5809, 5810, 5814. The IDs run 5774 **to** 5814 but the range is not contiguous; the gaps are `FPCApr2024-*` files from a different shoot. The first version of this document said 24 in four places and the figure also went out in the issue comment on #637. A correction comment is posted there.

Every one of those 23 has `MichelleDiamond` in the **filename** and **`michellekoebke`** in the embedded IPTC `credit` and `copyright` fields. Verified by pulling `media_details.image_meta` for all 23 in one request and counting distinct `(credit, copyright)` pairs: one pair, `('michellekoebke', 'michellekoebke')`, 23 times. The string `koebke` appears **nowhere** in `kriskrug-wp` or `kk-kb` (grep, 2026-08-02).

Two readings, and I cannot pick between them from the data: either Michelle Koebke is Michelle Diamond's legal name behind the "Diamond's Edge Photography" business name, or a second photographer's frames were folded into a batch named for the first. **Do not print a credit line for any of those 23 frames until KK says which.** This is a one-question fix for KK and it unblocks 23 assets.

By contrast the August 2024 set (`2024/09/AI_Meetup_August2024_MichelleDiamond-*`, `x-wp-total: 10`) carries `michellediamond` in the same fields, consistent with the filename. **With one exception, and it matters:** media **6854** has an **empty** IPTC `credit` and `copyright`. Nine of the ten carry `michellediamond`; 6854 carries nothing. That is one of the two frames Section 2a analyses in detail, so it is not a row anyone should have skimmed. Two nearby items with non-matching filenames sit in the same ID range: 6846 and 6848 carry `michellediamond`, and 6845 is empty like 6854. Treat 6854's Michelle Diamond attribution as inherited from the batch filename, not from the file.

---

## Section 2: the frames the prior docs got wrong

These are the corrections that matter most, because two of them were queued to ship onto the live page with alt text asserting something false.

### 2a. The two "Michelle Diamond meetup" strip frames do not show Kris Krüg

`content/drafts/2026-07-26-speaking-page/multimedia-rebuild-plan.md` lines 57 and 58 list these as P0/P1 "on-stages strip" assets:

| ID | Path | Draft alt in the plan | What the frame actually is |
|---|---|---|---|
| 6854 | `2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg` | "Kris Krüg speaking at a Vancouver AI community event" | Posed two-person portrait. A grey-haired man in black glasses and a patterned shirt with his arm around a younger man, sticker wall behind. **Kris Krüg is not in this photograph.** |
| 6847 | `2024/09/AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg` | "Kris Krüg hosting a Vancouver AI Community Meetup" | Two men, one in a dark cap and jacket laughing, one bald in a purple patterned shirt holding a mic and a phone. **Kris Krüg is not in this photograph.** |

Both re-viewed on 2026-08-02 through the Photon resizer. Both still return 200. **This finding stands and it is the most load-bearing thing in this document.** They are genuine August 2024 meetup photos. They are just not photos of Kris. Shipping either with the drafted alt would have put a false claim on a public page and an inaccurate description in a screen reader. Strike both from the Speaking strip.

Attribution footnote on 6847 and 6854: 6847's file carries IPTC `credit` `michellediamond`; **6854's is empty**. Both sit in a batch whose filenames say MichelleDiamond, so 6854's attribution rests on the filename alone. Not a problem while both are struck, but it becomes one the moment somebody reuses 6854 elsewhere.

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

## Section 3: the first of two stage photographs already in this repo

**Correction.** The first version of this document titled this section "the one stage photograph already in this repo" and the "How I verified" block said "exactly one is a stage photograph." Both were wrong. There are two. The second is `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg` and it gets Section 3a. A `git ls-files` grep for the filename would have found it, and Section 4 was written as though that photograph existed only as a third-party hotlink.

**`theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg`**, 1600x1066, sha256 `86934e9268e7cb6e1ecc7df95bd502006cafb73e038676f9aacba59f3aef0714`.

Publicly served at `https://kriskrug.co/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg`, verified **200 image/jpeg, 231674 bytes**, 2026-08-02. It is **not** in the media library (`?search=vancouver-ai-meetup-30` returns zero).

The frame: KK on the H.R. MacMillan Space Centre planetarium stage, hand raised, red curtain and Meetup 30 projection behind him, and roughly forty audience hands up in response. It is the best "this person owns a room" photograph available anywhere in either repo.

**Photographer identified, with proof.** I matched it byte-for-frame against the BC + AI photo pipeline:

- Source file: `June25_2026_BC+AIEvent_MichelleDiamond-94.jpg`
- Manifest: `/Users/kk/Code/bcai-website/.local-clone/photo-galleries/vancouver-ai-meetup-2026-06/manifest.json`, gallery `event_date` `2026-06-24`, gallery photographer **Michelle Diamond**, per-photo `photographer` **Michelle Diamond**
- Manifest sha of the original: `d685ce1b23b377f356d91a78c3b4bf16741b0f44179eb2a5905fdae36e2f4c3f`
- Manifest `event_title` names Vancouver AI Meetup #30, June 2026; `event_date` `2026-06-24`
- Manifest caption: "A presenter raises a fist at the mic as dozens of hands shoot up across the packed planetarium theatre."
- **Re-verified numerically on 2026-08-02, not just by eye.** I fetched the R2 derivative `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-06/large/d685ce1b23b3.webp` (200, 2048x1365), downscaled it to the theme copy's 1600x1066, and diffed the two: **mean absolute per-channel difference 3.12 out of 255** on a 1-in-41 pixel sample. That is resampling and JPEG noise. It is the same frame.

The repo sha differs from the manifest sha because the theme copy is a downscaled progressive JPEG with all EXIF stripped. The stripping is why the credit was lost in the first place.

**Rights basis.** KK committed it himself as `feat(home): use the approved Vancouver AI community photo` (commit `6b0ae1d`, 2026-07-25), body text: "the canonical approved event photo". That is KK's own written approval for site use. What it does not do is name the photographer, which is exactly what Section 3 just supplied. Combined with the live Michelle Diamond precedent on this site, this is **the cleanest rights position of any stage frame in the inventory**. It still is not a licence, and the rights basis in the manifest says so in those words.

**Precedent, now verified directly.** The first version of this document cited media 12663 from `scripts/events_page/heroes/LEDGER-2026-MEETUP.md` lines 68 to 71 and admitted it had not read 12663 itself. It has now been read: `GET /wp-json/wp/v2/media/12663` on 2026-08-02 returns `2026/08/09-veggie-skewers-michelle-diamond.jpg` with `alt_text` = `Vancouver AI Meetup #31 (photo: Michelle Diamond / Diamond's Edge Photography)`. The precedent is real. Two caveats worth carrying forward: 12663 is a photo of food, not a stage frame, and the credit sits in the **alt text**, which violates the VISUALS.md rule that credit goes in the caption and never in alt. Copy the credit string, not the placement.

Recommended credit line, matching the convention already documented in kk-kb's `meetup-28-publishing-notes.md`: `Photo: Michelle Diamond, Diamond's Edge Photography.`

---

## Section 3a: the second stage photograph already in this repo

**`content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg`**, 1200x800 JPEG, 191933 bytes, sha256 `3c881402ffa3313b687a2570965c6d11313504d99bd24996a342fbbbb53f8d0e`. Tracked (`git ls-files` returns it).

**What it is.** KK at the mic in a cream denim shirt, beside a flat-panel screen showing the "STOP SAYING BIAS / NAME WHAT YOU'RE SEEING" Algorithmic Justice League slide, audience heads across the bottom third, white marquee fabric behind. Excellent stage-action frame. I opened the file to write that sentence.

**Where it came from.** `content/source-packs/keynotes-2026/assets/asset-manifest.md` line 12 records the source as `https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1`. So this is a Photon-resized local copy of exactly the file Section 4 flags as a hotlink. Confirmed numerically: I fetched `https://www.punkrockai.com/public/photos/michelle-diamond/195.webp` (200, 1800x1200), downscaled it to 1200x800 and diffed against the tracked file. **Mean absolute per-channel difference 2.18 out of 255.** Same photograph.

**What that changes.**

1. Section 4's "fix the hosting by ingesting to the media library" was written as though there were no local file. There is one. The hosting problem is a smaller job than stated.
2. It does **not** change the rights answer. A committed copy is not permission. This file is the reason `speaking-stage-manifest.json` has a `not_for_ingestion` block instead of a second `assets[]` row: putting it in `assets[]` would mean one `--execute` uploads an uncleared photograph.
3. If and when Michelle Diamond clears it, ingest the **1800x1200 original** from punkrockai.com, not this 1200px derivative. 1200px is not enough for a 1440 hero.

**Same-event proof, which used to be an inference.** The first version guessed that this frame and media 11727 were from the same CreativeMornings shoot, based on venue, wardrobe and poster style. It is now shown, not guessed. Comparing the two frames directly: the same CreativeMornings city-code bunting (`CT SG PRS UTR SYD ...`), the same white marquee, the same flat-panel screen on the same stand, and the same cream denim shirt with the same turquoise bracelets. 11727 additionally shows a **Vancouver Artgallery** lectern and a **CreativeMornings Vancouver** banner. That fixes the event: CreativeMornings Vancouver, Vancouver Art Gallery, 2026-05-01, which is exactly the `event` / `event_date` / `location` recorded for media 12627 and 12628 in `content/source-packs/site-photography-2026/media-manifest.json`, whose `creator` is **Michelle Diamond** and whose embedded IPTC credit is `michellediamond`.

**Rights status: still needs clearance.** The photographer is now strongly indicated rather than assumed (third-party host path `/photos/michelle-diamond/`, plus same-event portraits with embedded `michellediamond`). Nobody has asked her. Photographer identified is not the same as permission granted, and this document does not upgrade one into the other.

---

## Section 3b: bucket B, portrait

**This roster was missing entirely from the first version, and it was the worst omission in it.** These four are the only assets anywhere in either repo with a written, per-asset rights basis. #637 names the source pack that holds them. Leaving them out made the document look like the site had no rights-recorded photography at all, which is the opposite of true.

They were ingested to the media library on 2026-07-24. Source of truth for that: `content/source-packs/site-photography-2026/ingestion-live.json`, `summary.uploaded: 4`, `created_media_ids: [12626, 12627, 12628, 12629]`, every row `verified: true`.

| Media ID | Local file in `content/source-packs/site-photography-2026/assets/` | Dims (local) | Photographer | Embedded IPTC credit (live) | Rights basis |
|---|---|---|---|---|---|
| **12626** | `kris-krug-vancouver-magazine-power-50-2026.jpg` | 682x1023 | **Mark Kinskofer** / Vision Event Photography | not read for this row | User-supplied and approved for kriskrug.co. Embedded Artist and IPTC By-line name Mark Kinskofer. **No public licence asserted.** |
| **12627** | `kris-krug-creativemornings-portrait-close-2026.jpg` | 2048x3072 | **Michelle Diamond** | `michellediamond` | User-supplied and approved for kriskrug.co. Embedded Artist, Creator, By-line, Copyright and Rights all name Michelle Diamond. |
| **12628** | `kris-krug-creativemornings-portrait-staircase-2026.jpg` | 2048x3072 | **Michelle Diamond** | `michellediamond` | Same as 12627. |
| **12629** | `kris-krug-van-ai-portrait-2025.jpg` | 1220x1831 | **Michelle Diamond** | `michellediamond` | Same as 12627. Shot at CreativeMornings Vancouver, 2025-10-03. |

Live captions on 12627 and 12628 already read "Kris Krüg at CreativeMornings Vancouver for his Punk Rock AI keynote, Vancouver Art Gallery, May 1, 2026. Photo: Michelle Diamond." Credit in caption, not alt. That is the house pattern working correctly, and it is the model the stage frames should copy.

**Why none of them closes #419.** `content/source-packs/site-photography-2026/README.md` says it plainly: "These four files do not close the stage-photography requirement in issues #419 or #414." The manifest agrees per asset. 12626's `not_recommended_for` includes "Speaking-page stage proof". 12627's includes "Documentary claim that the photograph shows Kris speaking on stage". 12628's includes "Primary Speaking-page action image". 12629's includes "Speaking or workshop action proof". They are posed portraits. Correct for About, Contact and press. Wrong for the Speaking hero.

**The one thing they are worth for this lane:** 12627 and 12628 fix the CreativeMornings 2026-05-01 event, venue and photographer in writing, which is what turns Section 3a's photographer guess into a supported claim.

Two more library items sit near this bucket and are not portraits of Kris: **6844** (`AI_Meetup_August2024_MichelleDiamond-93-scaled.jpg`, 2560x1707, credit `michellediamond`) is a portrait of an attendee, and **6854** and **6847** (Section 2a) are candid portraits of other people. Filed as ambience below.

---

## Section 3c: bucket C, event-ambience

Rooms, crowds, conversations, food, and frames where somebody other than Kris is the speaker. Useful as a Speaking-page proof strip or a texture band. **None of them satisfies #419's above-the-fold criterion**, because #419 asks for a photo of Kris on a stage.

Every row here was viewed on 2026-08-02 through the Photon resizer at 400px. Dimensions and IPTC credit read from `GET /wp-json/wp/v2/media/<id>`.

| ID | Path | Dims | What it shows | IPTC credit | Rights status |
|---|---|---|---|---|---|
| 12646 | `2026/07/michelle-diamond-meetup30-room-115.webp` | 1800x1200 | Outdoor courtyard, dense standing crowd mingling before the talk. Kris not identifiable. | none | Filename says Michelle Diamond. Assumed, not on file. |
| 12647 | `2026/07/michelle-diamond-meetup30-crowd-327.webp` | 1800x1201 | Room from the back, red curtain, a speaker at the mic under a slide reading "EVERY MEANINGFUL INTERACTION ASSUMES A HUMAN ACTOR". Speaker too small to identify; **not Kris on the read**. | none | Filename says Michelle Diamond. Assumed, not on file. |
| 12648 | `2026/07/vancouver-ai-meetup-2026-06-room.webp` | 2048x1365 | Seated theatre audience, faces lit by the screen, engaged and laughing. Strong "full room" proof. | none | BC + AI pipeline. Assumed, not on file. |
| 12147 | `2026/06/vanai-feb2026-auditorium-wide.jpg` | 2048x1365 | Wide auditorium, curved ceiling, a speaker at the front under an "Artificial intimacy" slide. **Not Kris.** | `michellediamond` | Assumed, not on file. |
| 12658 | `2026/07/comox-valley-meetup-room.jpg` | 1182x665 | Banquet-style room, rows of blue chairs, a small group at the far end. Reads sparse. | none | Assumed, not on file. |
| 12659 | `2026/07/vanai-conversation-pair.jpg` | 1024x683 | Two attendees mid-conversation, hands up, warm light. The best "people actually talk here" frame in the set. | none | Assumed, not on file. |
| 12667 | `2026/08/surrey-ai-meetup-may-2025-027.jpg` | 2048x1365 | Two men presenting on a small stage, shot over an audience head. **Neither is Kris.** | `michellediamond` | Assumed, not on file. |
| 12668 | `2026/08/vancouver-ai-meetup-feb-2025-072-scaled.jpg` | 1707x2560 | A speaker at the mic against the art wall under red neon. **Not Kris.** | none | Assumed, not on file. |
| 12670 | `2026/08/vancouver-ai-meetup-april-2024-112.jpg` | 2048x1365 | A plate of sushi. Stored alt is "Vancouver AI Meetup #4". | `michellediamond` | Assumed, not on file. |
| 6835 | `2024/09/crowd-shot-vancovuer-ai.jpeg` | 2048x1365 | Group standing in blue and purple light, posing toward camera. | none | Assumed, not on file. |
| 6822 | `2024/09/ed-kennedy-future-proof-creatives-vanAI-scaled.jpg` | 2560x1707 | A young man at the mic presenting in front of a screen, art wall behind. Filename says Ed Kennedy. **Not Kris.** | `michellediamond` | Assumed, not on file. |
| 6824 | `2024/09/ed-kennedy-kriskrug-vanAI.jpeg` | 2048x1365 | Three people posing, one of them **is Kris** (beard, tattoos, printed tee), one holding a small dog. Social, not stage-action. | none | Assumed, not on file. |
| 6844 | `2024/09/AI_Meetup_August2024_MichelleDiamond-93-scaled.jpg` | 2560x1707 | Smiling attendee portrait, red background. Not Kris. | `michellediamond` | Assumed, not on file. |
| 6854 | `2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg` | 2560x1707 | Posed two-person candid at the sticker wall. **Not Kris.** Reclassified out of stage-action, Section 2a. | **empty** | Attribution rests on the batch filename only. |
| 6847 | `2024/09/AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg` | 2560x1707 | Two men laughing, one holding a mic and a phone. **Not Kris.** Reclassified out of stage-action, Section 2a. | `michellediamond` | Assumed, not on file. |
| 2705 | `2023/07/5637672371_fca291d598_o-1.jpg` | 800x1071 | Two people on a red couch, one holding a mic. Stored alt claims "Kris Krüg Keynote UN Global Youth Summit on HIV Bamako, Mali". It is not a keynote stage frame. | not read | Unknown. |

**Ambience count, viewed: 16.**

**The honest boundary.** The full sweep returned **131 unique image IDs**. The 12 stage-action library frames, 4 portraits and 16 ambience frames above account for 32 of them. The remaining 99 were classified from filename, stored alt and dimensions **without opening the image**, and they resolve into Section 3d. If any of those 99 later matters, view it first.

---

## Section 3d: not photographs at all

The single biggest reason the media library looks richer in stage photography than it is. These 99 candidates are graphics. Classified from filename, stored alt and dimensions, **not viewed**, except where an earlier section says otherwise.

| Group | Example IDs | What they are |
|---|---|---|
| Slide decks exported as images | 11816 to 11825 (`*-web-summit-vancouver-2026.png`, all 1672x941), 12041 to 12047 (`*-human-element-shane-loki-talk.png`) | Quote cards and deck slides. Every stored alt is a sentence of body copy. |
| YouTube thumbnails and video cards | 12715 (Whistler Institute), 12716 (Bass Coast Brain Stage), 8469, 7892, 6964 | Branded cards, usually with a cut-out subject and burned-in title text. Not frames. |
| Event banners and promo headers | 3427, 3435, 3526, 3642, 3891, 5233, 5816, 5817, 6858, 7219, 8874, 9202, 11781, 12664 | 2560x888, 1500x500, 1280x420 style letterbox headers. |
| Poster and key art | 12649, 12662 (Futureproof salmon starfield), 11724, 12267, 12098 | Illustration and editorial art. |
| Generated imagery | 4777, 4780, 5495, 2653 (filenames beginning `kriskrug_`) | Midjourney-style outputs. |
| Unrelated photography | 2888, 3577 (Okeechobee Music Festival 2016), 2233, 2234, 12004 (Dalai Lama, Vancouver Peace Summit), 12000 (bridge crowd) | Real photographs, wrong subject or wrong decade. |
| Workshop and residency documentation | 2471 (Galiano Island relief retreat), 2797 (KAN Festival residency with Ruganzu Bruno), 2662 | Real photographs of Kris working, but facilitation and residency context, not a speaking stage. Worth a second look if #419 ever widens to workshop proof. |

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

**What the file actually is.** I fetched `https://www.punkrockai.com/public/photos/michelle-diamond/195.webp` directly on 2026-08-02: **200 image/webp, 1800x1200**. KK at the mic beside the "STOP SAYING BIAS / NAME WHAT YOU'RE SEEING" Algorithmic Justice League slide at CreativeMornings Vancouver, audience heads in the foreground. It is a genuinely excellent stage-action frame, sitting on a third-party host under a directory literally named `michelle-diamond`.

**Correction: a copy of this file is already committed to this repo.** `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg`, 1200x800, tracked, with the punkrockai URL recorded as its source in `asset-manifest.md` line 12. Section 3a has the pixel diff proving it is the same photograph. The first version of this document did not know that, and the sentence below has been rewritten because of it.

**Rights status: needs clearance. The two problems are not equally hard.**

- **Hosting.** Smaller than it looked. A local 1200x800 copy is already tracked, so nothing has to be re-downloaded. If clearance lands, ingest the **1800x1200 original** from punkrockai.com rather than the tracked derivative, because 1200px will not carry a 1440 hero.
- **Permission.** Unchanged and still the blocker. No clearance record exists anywhere in either repo. The photographer is now strongly indicated as Michelle Diamond (Section 3a), which tells you **who to ask**, not that you may proceed.

Ingesting without asking fixes the smaller problem and makes the bigger one worse. That is why `speaking-stage-manifest.json` files this asset under `not_for_ingestion`, a key the ingester never reads, instead of under `assets[]`.

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

**Both 11833 and 11831 have no recorded photographer.** All five LaSalle frames (11830 to 11834) return an **empty** IPTC `credit` and `copyright` from `GET /wp-json/wp/v2/media/<id>`, checked individually on 2026-08-02. Nothing in the kk-kb appearance record `2026-01-14-lasalle-college-vancouver-keynote.md`. Nothing in `media-manifest.json`. Nobody wrote it down.

**Corrected citation for the artifact folder.** It is `/Users/kk/Code/kk-kb/content/knowledge/keynotes/2026-01-14-lasalle-college-vancouver/`, and it lives in **kk-kb, not this repo** (`content/knowledge/` does not exist in `kriskrug-wp`). The first version said "17 files", which is not a number that describes it either way. `ls -1` returns **16 top-level entries**: 15 files plus a `presentation/` directory. `find -type f` returns **57** recursively. Also wrong the first time: `seo-and-images.md` does not contain "only generative image prompts". It opens with an SEO title, a meta description, a primary keyword, five secondary keywords and a slug, and the Image Prompts section comes after that.

The substantive conclusion is unaffected and I re-ran it: `grep -rniE 'photograph|photo credit|photo by|credit:'` across all 57 files returns only prose about photography as a profession. No photographer is named for the LaSalle night anywhere in the folder.

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
2. **A media-library ingest of the Meetup 30 theme asset.** It is the only frame with both a named photographer and written KK approval, and it is sitting at a theme path where the crop system and Jetpack sizing cannot reach it. `content/drafts/2026-07-26-creative-labs/layout-image-crops.md` line 62 already flags this. **The manifest for it now exists** at `content/source-packs/site-photography-2026/speaking-stage-manifest.json` and dry-runs clean, so the apply lane's job is one `--execute` with credentials. The upload itself is still owned by a later apply issue, not this one.
3. **A page-architecture change.** Even with a cleared photo, nothing changes unless the hero band moves above the Formats grid. That is the #419 page lane, not this one. This inventory removes the excuse, it does not do the work.

**Coverage gaps by event.** `VISUALS.md` line 19 asks for wide action frames for five events. Where each stands after this sweep:

| Event | Status |
|---|---|
| ChannelNext | **Nothing.** `?search=ChannelNext` returns zero. No frame in either repo, no BC + AI gallery. The talk video exists; the photography does not. |
| Whistler Institute | **Nothing photographic.** Media 12715 is a YouTube thumbnail composite (branded card with KK cut out over a graphic background), not a frame. |
| Bass Coast Brain Stage | **Nothing photographic.** Media 12716 and `scripts/events_page/heroes/one-offs-2025/2025-07-11-bass-coast-brain-stage-youtube.jpg` are the same YouTube thumbnail with title text burned in. |
| Web Summit Vancouver | **Nothing.** `?search=web-summit-vancouver-2026` returns `x-wp-total: 11` (self-caught: the first version said twelve while listing eleven IDs). All eleven are graphics: 11816 to 11825 at 1672x941 and 11781 at 1280x500. No stage frames. |
| Futureproof Festival | **Nothing of KK on a Futureproof stage.** 12649 and 12662 are the salmon starfield poster art. The closest thing that exists is `vanai-july2026-69`, KK presenting *about* Futureproof at a Vancouver AI meetup, which is a different claim. |
| CreativeMornings | **Better covered than the first version said, and still blocked.** Two frames exist, both from 2026-05-01: library banner 11727 (1280x500, too letterboxed for a hero) and the Punk Rock AI frame, which exists as a tracked 1200x800 local file **and** as an 1800x1200 original on punkrockai.com. Neither is cleared. The photographer question is one ask (Section 3a). |

---

## Section 9: shooting and sourcing list for KK

Ordered by how much it unblocks per unit of KK effort.

1. **Answer the LaSalle question.** Who shot the January 2026 LaSalle College night, and are those five frames clear for the site? Unblocks the best hero available.
2. **Answer the Diamond / Koebke question.** Is `michellekoebke` in the IPTC of the June 2024 set the same person as Michelle Diamond? Unblocks **23** assets, one of which (5814) is a genuine hosting frame.
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
| **Michelle Diamond or Michelle Koebke** | the June 2024 set, IDs 5774 to 5814, **23 frames** (non-contiguous, enumerated in Section 1) | Resolve the name conflict first, then ask. |
| **Michael Caswell** | `vanai-july2026-58`, `-59`, `-69` | Named per-photo in the July 2026 manifest. No precedent on kriskrug.co. Courtesy check. |

**Existing outreach pattern to copy:** `content/drafts/2026-08-01-testimonials-overhaul/consent-outreach.md`. It is a testimonials-consent file, not a photo-rights file, but the shape is right and it already establishes the house rule at the top: *"Nothing here has been sent. This file is a shortlist and a set of drafts. Sending is a human action, and KK does the sending in his own words."* Its companion `consent-log.md` is the right model for a photo-rights log if this grows into one.

---

## Section 11: the manifest deliverable, now written

#637 names `content/source-packs/site-photography-2026/speaking-stage-manifest.json` as the output. The first version of this document declined to write it. **It is now written**, because the stated reason for declining had a factual error in it: it claimed only one local file needed uploading, and there are two (Section 3a). Once the reason is wrong, the refusal has to go.

**The file:** `content/source-packs/site-photography-2026/speaking-stage-manifest.json`.

**It validates against the existing schema, with proof.**

```
python3 scripts/notion-to-wp/ingest_media_manifest.py \
  --manifest content/source-packs/site-photography-2026/speaking-stage-manifest.json \
  --report content/source-packs/site-photography-2026/speaking-stage-dry-run.json
```

Exit code **0**. `validate_manifest()` at `scripts/notion-to-wp/ingest_media_manifest.py` lines 41 to 88 enforces `schema_version == 1`, a non-empty `assets` list, an existing local `file` per row, a matching `sha256`, a non-empty `credit`, all four `wordpress` fields (`title`, `alt_text`, `caption`, `description`), and the rule that the credit string must appear inside both the caption and the description. All of that passed. The dry-run report is committed at `content/source-packs/site-photography-2026/speaking-stage-dry-run.json`: `"assets": 1`, `"planned_uploads": 1`, `"existing_matches": 0`, `"live_write": false`.

**What is in `assets[]`: exactly one row.** The Meetup 30 theme asset. It is the only asset anywhere in this inventory that is both local to this repo and backed by a written rights basis (KK's own commit `6b0ae1d`, plus a photographer established by frame match). Its `file` is a relative path back up to the tracked theme copy rather than a duplicate binary inside the source pack, because the theme copy is the tracked original and copying it would create a second sha to keep in sync.

**What is deliberately not in `assets[]`.** The Punk Rock AI CreativeMornings frame, under a `not_for_ingestion` key. `validate_manifest()` reads `data["assets"]` and nothing else, so a key by any other name is inert: `--execute` cannot reach it. That preserves the original reasoning (do not build a loaded gun out of uncleared photography) while still recording the asset, its sha, its dimensions and the exact question that has to be answered before it moves into `assets[]`. A third key, `not_in_this_manifest`, records why the 10 library-resident stage frames, the 4 portraits and the 5 off-site R2 frames are absent.

**What the manifest does not do.** It does not upload anything. Dry-run is the default and `--execute` requires `WP_USER` and `WP_APP_PASSWORD`, which were never set in this session. No live write of any kind was made.

---

## Facts and inferences

**Facts, read directly from a source on 2026-08-02:**

- Every media ID, path, dimension, stored alt, stored caption, and embedded IPTC `credit` / `copyright` value, from `GET /wp-json/wp/v2/media/<id>`.
- Every count in this document, re-derived on 2026-08-02 from a command whose output is quoted next to it. The June 2024 set is **23** by `x-wp-total` and by enumeration. The August 2024 set is **10** by `x-wp-total`. Tracked image binaries are **210** by `git ls-files`. The candidate sweep is **131** unique IDs. The LaSalle artifact folder is **16** top-level entries and **57** files recursively.
- Every HTTP status in this document, from `curl`.
- Every visual classification in Sections 1, 2, 3, 3a, 3b and 3c. Those frames were pulled through the public Photon resizer and looked at. Section 3d was **not** viewed and says so.
- The live `/speaking/` structure: 4 images in `<main>`, first KK stage photo at position 4, 0 iframes, punkrockai hotlink present in an `aurora-media-card`, no `aurora-stage` class present.
- The theme-part hotlink at `theme/kk-aurora/parts/speaking-proof-grid.html` line 5.
- Commit `6b0ae1d` and its message, from `git log`.
- The Meetup 30 frame match: pipeline manifest entry, photographer field, caption, R2 URL, and a numeric pixel diff (mean absolute channel difference 3.12 of 255) between the R2 derivative and the theme file.
- That `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg` is a copy of punkrockai `195.webp`: recorded in `asset-manifest.md` line 12 and confirmed by a numeric pixel diff (2.18 of 255).
- That media 11727 and punkrockai `195.webp` are the same event: matching CreativeMornings city-code bunting, matching marquee, matching flat-panel screen and stand, matching wardrobe. **Promoted from inference to fact in this pass.** The venue is fixed by the Vancouver Art Gallery lectern and CreativeMornings Vancouver banner visible in 11727.
- The portrait rights rows and the 2026-07-24 ingest of media 12626 to 12629, from `media-manifest.json` and `ingestion-live.json`.
- The Michelle Diamond precedent, **now read directly**: `GET /wp-json/wp/v2/media/12663` returns `alt_text` = `Vancouver AI Meetup #31 (photo: Michelle Diamond / Diamond's Edge Photography)`. The first version cited only `LEDGER-2026-MEETUP.md` for this and admitted it had not checked.
- `koebke` returning zero hits across both repos.

**Inferences, mine, and challengeable:**

- That 11727's and punkrockai `195.webp`'s photographer is **Michelle Diamond**. Now resting on three legs rather than one: the third-party host path `/photos/michelle-diamond/`, the proven same-event match above, and the two portraits from that same event (media 12627 and 12628) carrying embedded IPTC `michellediamond` with a written rights basis. Strong, and still **recorded as needing clearance, not upgraded to cleared.**
- That the theme asset's Michelle Diamond credit transfers to the theme copy. The copy is EXIF-stripped, so the attribution rests entirely on the frame match, which is now numeric rather than visual, but a frame match is still not a licence.
- That the person in media 12146 may not be Kris Krüg. Re-viewed in this pass: right build, glasses, tied-back hair, beard, but the beard reads darker and fuller than 11831 or 12669. The filename and the stored alt both say Kris and I could be wrong. **Recorded as UNVERIFIED, not as a correction.**
- That 11833 plus 11831 is the right hero pair. An art-direction call. KK's to overrule.
- Every "assumed, not on file" rights row in Section 3c. Filename and IPTC agreement is evidence of authorship, not of permission.

**Known limits of this document.**

- 99 of the 131 sweep candidates were classified without opening the image (Section 3d). They read as graphics from filename, alt and dimensions. If one turns out to matter, view it first.
- The sweep is search-term based. A stage photograph with a filename and alt text that match none of the 19 terms would not be in it.
- The kk-kb side was searched for the LaSalle photographer specifically. It was not swept for stage photography end to end.

**Nothing in this document has been applied anywhere.** No upload, no media edit, no page write, no theme edit, no message sent. Every live call was a read-only `GET`.
