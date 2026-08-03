# Internal-link plan for /events/ (issue #634)

**Status:** plan only. Nothing here has been applied. No page 2250 edit, no post edit, no redirect, no WordPress call was made producing this document.

**Written:** 2026-08-02, against live kriskrug.co.

---

## 1. What is actually live right now

Verified by reading `https://kriskrug.co/events/` logged out on 2026-08-02.

| Fact | Value | How checked |
|---|---|---|
| Cards rendered on /events/ | **65** | count of `data-event-id="…"` in the live HTML |
| Rows in `scripts/events_page/events-catalog.yaml` | 66 | 55 `confirmed` + 10 `scaffold` + 1 `proposed` |
| Why 65 and not 66 | `trunorth-ai-leadership-summit-2026` is `status: proposed`, so `public_status()` skips it | `render_events_page.py` line 65 |
| Body links out of /events/ that stay on kriskrug.co | **9** (excluding site nav and footer) | link extraction on the live page |

The issue says 66. The public number is 65. Use 65 in any copy.

### The 9 on-site links /events/ already has

| Source | Target | Anchor today |
|---|---|---|
| hero | `/speaking/` | Book Kris to speak |
| `waiff-sao-paulo-2026` card | `/speaking/` | Recap / details |
| `2025-03-20-data-storytelling-hackathon` card | `/2025/03/20/is-a-hotdog-a-sandwich-vancouver-aidata-storytelling-hackathon-w-andrew-reid/` | Recap / details |
| `enya-liftoff-keynote-2024` card | `/2024/09/11/the-human-algorithm-enya-learning-keynote/` | Recap / details |
| `bcama-vision-conference-panel-2024` card | `/2024/05/27/unpacking-ai-ethics-at-american-marketing-associationvisionconf2024/` | Recap / details |
| `yorkton-film-festival-panel-2024` card | `/2024/05/25/ai-in-filmmaking-at-the-yorkton-film-festival/` | Recap / details |
| `innovate-west-keynote-2024` card | `/2024/04/20/ai-mindset-keynote-at-innovate-west-2024-in-vancouver/` | Recap / details |
| "Stages I speak on" WAIFF card | `/speaking/` | See speaking topics |
| final CTA | `/speaking/` | Book Kris to speak |

So 5 of 65 dated cards route a reader to a kriskrug.co writeup. One more (`waiff-sao-paulo-2026`) is labelled "Recap / details" and delivers `/speaking/`, which is not a recap, and the reader only finds that out after the click.

### The other half of the dead end

Nothing points back. Checked the body content (not nav, not footer) of `/speaking/`, `/testimonials/`, `/ai-events/`, `/vancouver-ai/`, `/about/`, `/work/`, `/blog/`, `/contact/`, `/glossary/`, and 38 posts. **Zero** of them link to `/events/`.

Two of those are the sharpest miss:

- `/ai-events/` is titled "AI Events & Recaps: Web Summit, Hackathons, Meetups". It links to `/vancouver-ai/`, `/speaking/`, `/contact/`, a category archive, and three posts. It does not link to the events archive.
- `/speaking/` links to exactly two internal destinations in its body: `/responsible-ai-professional/` and `/contact/`. A person deciding whether to book Kris cannot get from the pitch to the 65 rooms that back it up.

---

## 2. Prerequisite: /events/ has no anchor ids

Direction 2 wants links like "the Squatchie Awards night" pointing at a specific card. **That is not possible today.**

`render_events_page.py` emits:

```html
<article class="aurora-event-card aurora-event-card--compact" data-event-end="…" data-event-id="van-ai-meetup-31">
```

`data-event-id` is a data attribute. It is not a fragment target. `https://kriskrug.co/events/#van-ai-meetup-31` scrolls nowhere.

### Proposed anchor contract (for the render issue, not this one)

1. **Emit `id="event-{catalog id}"`** on the same `<article>`, alongside the existing `data-event-id`. The `event-` prefix keeps it clear of the seven existing section ids on the page (`aurora-events-title`, `aurora-events-upcoming`, `aurora-events-past`, `aurora-events-host`, `aurora-events-stages`, `aurora-events-signature`, `aurora-events-cta`).
2. **Catalog ids become permanent once shipped.** Today they are two conventions in one file: `van-ai-meetup-31` and `2026-07-09-bc-ai-film-club-july-idea-lab`. Do not normalize them retroactively, that would break every link anyone ever made. New rows can follow one convention going forward.
3. **Re-fire the fragment scroll after `syncBuckets()`.** The rolloff script re-parents cards between the Upcoming and Past grids on `DOMContentLoaded`. The browser has already tried its fragment scroll by then, so a deep link will land in the wrong place. The script needs to read `location.hash` after the sort and scroll to the matching element itself.
4. **Add `scroll-margin-top`** to `.aurora-event-card` in the page-scoped CSS so a deep-linked card does not sit under the sticky header.
5. **Harvest merge must not renumber.** `meetup-editions.yaml` merges at render time and wins on date, url, and hero. It must not be allowed to change an `id`.

Until 1 through 4 exist, **every direction-2 link in this plan targets `/events/` bare**, with no fragment. That is deliberate. Deep links are a follow-on, not a blocker.

---

## 3. Direction 1: events to elsewhere

### How the renderer constrains this

Two different shapes of change, with two different costs:

- **Zero code change:** swapping the `url:` value on a catalog row. The card already renders one link. Cost is a catalog edit, a re-render, and a page 2250 POST.
- **Small renderer change:** giving a compact card custom anchor text. `render_compact_card()` hard-codes the string `Recap / details` and ignores `cta_past`, which only the rich card honors. Making the compact template read `cta_past` is a few lines and unlocks every anchor below.

**Recommendation: do the small renderer change.** The live page is 62 compact archive cards and 3 rich Upcoming cards, so "Recap / details" appears 62 times and is most of why the page reads as a dead end. Specific anchor text is most of the value in this plan. Do **not** build a second-link-per-card feature; one good link per card is enough.

### Tier 1: apply these

Every target below returned HTTP 200 logged out on 2026-08-02.

| # | Source card (catalog id) | Target | Anchor text | Why it earns the slot |
|---|---|---|---|---|
| 1 | `creativemornings-perils-parallels-2026` | `/2026/05/04/punk-rock-ai/` | The recap: Punk Rock AI | Highest-value swap on the page. The card currently points at `creativemornings.com`, a generic org homepage that says nothing about Kris. The post opens "I gave a talk Friday morning at CreativeMornings/Vancouver. The title was Punk Rock AI." Same talk, on his own domain. The card hero file is even named `punk-rock-ai-creative-mornings.jpg`. |
| 2 | `waiff-sao-paulo-2026` | `/2026/01/24/both-hands-full/` | Both Hands Full, the argument behind the keynote | Fixes an anchor that currently says "Recap / details" and delivers `/speaking/`. The live page's own Stages card describes this keynote as "The Both Hands Full framework for filmmakers, students, and creative technologists". The essay is that framework. |
| 3 | `lasalle-college-keynote-2026` | `/2026/01/24/both-hands-full/` | Read the Both Hands Full argument | Card blurb is verbatim "Both Hands Full: what creatives actually need to know about AI." The post's H1 is "What Creatives Actually Need to Know About AI". Only swap if KK prefers text over the YouTube link currently there; otherwise hold this one and keep the video. |
| 4 | `futureproof-festival-2026` | `/2026/06/01/long-road-to-futureproof/` | How this festival got built | This is the only Upcoming card with real editorial depth behind it. Post confirms Futureproof Festival, the Space Centre, October. Keep `futureproof.website` as the primary CTA; this replaces nothing if the renderer stays single-link, so treat it as the one card worth a second link if that feature ever lands. |
| 5 | `van-ai-meetup-01` | `/2024/01/28/inside-the-innaugural-vancouver-ai-community-meetup/` | Night one, 80 people in a studio | The origin story card currently points at the generic `lu.ma/vancouver-ai`. The post is the recap of that night. Corroborated independently: the Zero to One post states "January 25, 2024, when Kris Krüg opened the doors of MØTLEYKRÜG Media headquarters for the first Vancouver AI Community Meetup (#VAI01). The event sold out immediately, 80 people". |
| 6 | `van-ai-meetup-12` | `/2024/12/28/system-check-vancouver-ai-community-meetups-december/` | The NeurIPS-week recap | Card label is "December 2024: NeurIPS Edition". Post is titled for December and names NeurIPS in body. |
| 7 | `van-ai-meetup-13` | `/2025/02/02/vancouver-ai-january-2025-recap-one-year-of-creative-rebellion-open-source-disruption/` | One year in, at the Space Centre | Card label is "January 2025: One Year Anniversary". Post body: "Standing in the Space Centre last night… One year ago, 80 pioneers showed up". Exact match. |
| 8 | `van-ai-meetup-14` | `/2025/03/02/vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap/` | The February recap | Card is February 2025. Post is titled a February meetup recap and published four days after. |
| 9 | `van-ai-meetup-16` | `/2025/05/11/vancouver-ai-meetup-16-where-tech-creativity-and-community-collide/` | Meetup #16, written up | The post names the edition number in its own title and first line. No inference needed. |
| 10 | `2025-05-06-bc-ai-ecosystem-launch` | `/2025/05/18/bc-ai-is-live-and-were-building-the-future-we-actually-want/` | The day BC + AI went live | Card is the launch session, currently pointing at `luma.com/BCai`. Post body confirms the launch, "May 6", and the association framing. |

### Tier 2: hold until KK settles one question

These are real matches, but each one depends on a date or edition call that this plan will not guess. Every target verified 200.

| # | Source card | Target | Anchor text | Open question |
|---|---|---|---|---|
| 11 | `van-ai-meetup-05` (catalog date 2024-05-29) | `/2024/06/02/june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines/` | May 2024, 135 people at Future Proof | Post title says "June 2024" but its body says "the buzzing atmosphere we created together on **May 30th**" with "over 135 attendees". Post title, post body, and catalog date disagree three ways. |
| 12 | `van-ai-meetup-06` (catalog 2024-06-26) | `/2024/07/08/creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights/` | June 2024, written up | Post body cites "June 27th". Catalog says the 26th. |
| 13 | `van-ai-meetup-07` (catalog 2024-07-31) | `/2024/08/04/ai-meetup-mayhem-stickers-startups-and-squamish-songs/` | Stickers, startups, Squamish songs | Row is `status: scaffold` with blurb "Month folder empty/moved". Confirm the edition is real before linking a recap to it. |
| 14 | `van-ai-meetup-08` (catalog 2024-08-28) | `/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/` | Hackers, hustlers, heretics | Post body cites "August 29th". Catalog says the 28th. Row is `scaffold`. |
| 15 | `van-ai-meetup-03` **or** `van-ai-meetup-04` | `/2024/04/04/spaceport-vancouver-ai-community-meetup/` | Spaceport, inside the room | Published April 4, 2024, and it names no event date anywhere in the body. Could be the March 27 recap, or a general promo ahead of the April 24 night. Both rows are `status: scaffold`. Do not link until KK says which edition. |
| 16 | `2025-05-27-web-summit-indigenomics-ai` | `/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/` | What Indigenomics AI actually is | The post explains the platform and names Carol Anne. It does not mention Web Summit, and it predates the panel by seven weeks. Also: Indigenomics is framed as past work elsewhere on the site, so check the framing reads right before adding a fresh link. |
| 17 | `2025-05-25-calm-before-storm-websummit` | `/2025/04/13/web-summit-vancouver-2025-survival-guide/` | The locals' guide to Web Summit week | Thematically dead on (the post is about locals owning the room before the conference arrives) but it never names Calm Before the Storm or the Alibi Room. Adjacent, not a recap. KK's call whether that is honest enough. |

### No target: the remaining 42 cards

This is the expected verdict, not a failure. Split 21 meetup-series cards and 21 everything else.

**21 meetup-series cards** (`van-ai-meetup-02`, `09`, `10`, `11`, `15`, `17` through `31`, plus the upcoming `vancouver-ai-meetup-2026-09-30`). No matching on-site writeup exists. Editions #17 to #31 span May 2025 to July 2026, a window in which no meetup recap was published to kriskrug.co. They keep their Luma links, which is the correct destination for a night with no writeup.

**21 other cards:**

- **Upcoming with a live registration page:** `how-can-we-help-pitch-night-2026` (Eventbrite). The registration link is the job. Nothing on site to add.
- **Keynotes whose best destination is the tape:** `channelnext-2025`, `whistler-institute-2025`, `2025-07-11-bass-coast-brain-stage`. All three already point at YouTube. Do not downgrade a full talk video to a text page.
- **Private corporate work:** `2025-09-02-amd-media-copilot-workshop`, `2025-09-01-ea-creative-innovation-keynote`. No public destination by design.
- **2026 one-offs with no writeup:** `2026-07-09-sfu-ai-panel`, `2026-07-08-ai-ethical-futures-lab-morten`, `2026-04-12-yvr-ai-welcome-salon-ted2026`, `2026-04-01-global-ai-summit-vancouver-panel`, `2026-03-31-sea-to-sky-gondola-ai-ethics-workshop`, `2026-02-01-vibe-working-workshop`, `2026-01-31-first-tech-challenge-think-award`. Several have no external URL either.
- **2024 and 2025 community nights with no writeup:** `adplist-fireside-2024`, `dot-summit-autoloom-2024`, `2025-10-24-munda-mennuie-residency`, `2025-10-22-dama-day-ai-for-nonprofits-keynote`, `2025-08-10-calm-before-storm-siggraph`, `2025-04-09-ted2025-community-meetup`, `2025-02-05-thinking-game-premiere`.
- **`2026-07-09-bc-ai-film-club-july-idea-lab`.** `/2026/07/28/no-one-knows-what-to-call-us-yet/` and `/2026/07/18/i-am-nomad-ai-film/` both discuss AI Film Club, but neither is a recap of the July 9 idea lab. Linking them would be a topical link wearing a recap's clothes.

**Also dropped: the protest arc.** The issue named it as a candidate. Checked: `/2026/05/23/you-cant-drink-data/` is Kris marching in Vancouver's first anti-data-centre protest, and `/2026/05/23/data-center-protest-signs/` is its companion. Neither is an event Kris ran, and there is no protest in the catalog. Both posts belong to a different lane.

**Direction 1 arithmetic, against 65 live cards:** 10 links to apply now (10 source cards), 7 links held pending a ruling (8 candidate source cards, since item 15 has two possible sources and only one wins), 5 cards already linking to a post and left alone, 42 cards with no target. 10 + 8 + 5 + 42 = 65.

---

## 4. Direction 2: elsewhere to events

All five target `/events/` bare. No fragments until the anchor contract in section 2 exists.

| # | Source | Target | Anchor text | Why it earns the slot |
|---|---|---|---|---|
| 18 | `/speaking/` | `/events/` | See the rooms I actually run | The biggest gap on the site. A prospect on the speaking page has two internal exits, `/responsible-ai-professional/` and `/contact/`, and no path to the proof. /events/ links to /speaking/ three times. /speaking/ links back zero times. |
| 19 | `/ai-events/` | `/events/` | The full events archive | The page is literally called AI Events. It is a topic hub with three post links and no route to the 65-card archive. A reader who lands here from search is one click from the best surface on the site and cannot find it. |
| 20 | `/vancouver-ai/` | `/events/` | Every meetup night, in order | The page is the Vancouver AI ecosystem hub. It currently sends people to `/ai-events/` instead, which sends them nowhere. |
| 21 | `/testimonials/` | `/events/` | The rooms these lines came from | The page's own opening line is "Proof from the rooms, stages, and cohorts." One of its quotes is Ed Kennedy on Kris's "talk and event design". The rooms are one page away and unlinked. |
| 22 | `/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/` | `/events/` | Every night in the archive | This post is the narrative of the whole meetup arc from January 2024 forward. It is the one piece of writing whose central claim the events archive directly evidences. Best single post-to-page link available. |

**Direction 2 total: 5.**

Deliberately not proposed: a blanket "add /events/ to every meetup recap" pass. Fifteen more links of the same shape do not add fifteen times the value, and the recaps are old enough that editing them all is a bigger blast radius than the payoff.

---

## 5. Direction 3: page-level routing and the booking CTA

### Where the booking CTA belongs on /events/

**It is already right. Do not move it, and do not add a booking URL.**

`/events/` has two booking touchpoints, the hero and the final CTA, and both say "Book Kris to speak" pointing at `/speaking/`. That is the correct shape: `/events/` is the proof surface, `/speaking/` is the offer surface, and `/speaking/` owns the actual booking CTA.

The practical benefit: **this plan does not touch the unresolved `/contact/` vs `/book` decision at all.** Whenever KK settles it, only `/speaking/` changes. `/events/` inherits the fix for free. Putting a direct booking link on `/events/` would create a second place to update and a second place to get it wrong.

One receipt for that decision, since the issue frames it as an open choice: as of 2026-08-02, `https://kriskrug.co/book` and `/book/` both **301 to `/2005/10/19/book-review-bittorrent-for-dummies-by-susannah-gardner-and-kris-krug/`**. There is no booking page at `/book`; WordPress is permalink-guessing its way to a twenty-year-old book review. Creating a real `/book` page would take precedence over that guess, but the slug is not currently free and clear. That is context for whoever owns the CTA decision, not a recommendation from this plan.

### How /events/ and /speaking/ should relate

They overlap because they are two views of the same career. Give each one a job and make the handoff explicit.

- **`/speaking/` is the offer.** Topics, formats, what you get, one booking CTA. It gains one link out: to `/events/`, as the receipts (#18).
- **`/events/` is the receipt.** 65 dated rooms, the recurring series, the archive. It keeps handing off to `/speaking/` for anyone who wants to hire, which it already does three times honestly (hero, Stages card, final CTA) plus the mislabelled fourth that item 2 fixes.

The Stages I speak on section of `/events/` duplicates five events that also exist as dated catalog cards (WAIFF, LaSalle, Whistler, ChannelNext, Calm Before the Storm). That duplication is out of scope here, but flag it for whoever owns the page: the same event appears twice with two different destinations, and after this plan lands, the WAIFF Stages card would point at `/speaking/` while the WAIFF dated card points at the Both Hands Full essay. Not wrong, but worth a deliberate look in a future pass.

### One new link

| # | Source | Target | Anchor text | Why |
|---|---|---|---|---|
| 23 | `/events/` final CTA section | `/testimonials/` | What people said after | Completes the triangle. Proof (events) to voice (testimonials) to offer (speaking). All three pages exist, all three return 200, and today only one edge of the triangle is drawn. |

---

## 6. Safe now versus gated

**Safe now, no dependency on any open decision (14 links):**

- Direction 1 tier 1, items 1, 2, 5, 6, 7, 8, 9, 10 (8 links). All are catalog `url:` swaps.
- Direction 2, items 18 through 22 (5 links).
- Direction 3, item 23 (1 link).

**Safe but a preference call for KK (2 links):** item 3 (text versus the existing YouTube link for LaSalle) and item 4 (Futureproof needs a second link per card, or it displaces `futureproof.website`).

**Gated on a small renderer change** (compact card honors `cta_past`): every specific anchor text above for a compact card. Without it, all archive-card anchors read "Recap / details" and roughly half the value of direction 1 is lost. This is a Track B edit to `scripts/events_page/render_events_page.py`, plus a re-render and a page 2250 POST with a snapshot first.

**Gated on KK's ruling:** direction 1 tier 2, items 11 through 17.

**Gated on the anchor-id contract:** nothing in this plan. Every direction-2 link targets `/events/` bare on purpose. Deep links are strictly additive later.

**Not gated on the Speaking CTA decision:** nothing. That is by design, see section 5.

---

## 7. Found while verifying, not fixed here

Flagging, not touching. Each of these is a catalog question, not a link question.

1. **`van-ai-meetup-01` date looks wrong.** Catalog says `2024-01-31` with blurb "No month folder; first-of-2024 slot by anniversary-anchored numbering". Two live posts say **January 25, 2024**: the Zero to One post names the date and the venue (MØTLEYKRÜG Media HQ, 80 people, sold out), and the inaugural recap was published January 28.
2. **Three more editions are a day off** from the dates cited in their own recaps: #5 (post says May 30, catalog says May 29), #6 (June 27 versus June 26), #8 (August 29 versus August 28). Small, but it is the kind of drift that makes an archive stop being trustworthy, and it is the reason items 11 through 14 are held.
3. **`waiff-sao-paulo-2026` has `url: /speaking/`** in the catalog, which renders as an anchor labelled "Recap / details" that lands on the speaking page. That is the one actively misleading link on /events/ today. Item 2 fixes it.
4. **`creativemornings-perils-parallels-2026` points at `creativemornings.com`**, the org's global homepage, not the Vancouver chapter and not the talk. Item 1 fixes it.

---

## 8. Verification log

Every URL cited in this plan as a link target was fetched logged out on 2026-08-02.

- **48 candidate link targets checked. 48 returned HTTP 200.** Zero dead targets, so nothing in this plan was dropped for being dead. Every URL that appears in a Target column above is in that 48.
- Five extra routing URLs status-checked but not used as targets: `/book` (301), `/book/` (301), `/services/` (301 to `/generative-ai-services/`), `/category/events-reports/` (200), `/category/vancouver-ai-ecosystem/` (200).
- Live `/events/` HTML pulled and parsed for card count, card ids, rich versus compact split, and body links.
- `/speaking/`, `/testimonials/`, `/ai-events/`, `/vancouver-ai/` parsed for existing internal links, to confirm the missing edges rather than assume them.
- Post bodies read, not just titles, for every match claimed in tier 1, to confirm the event and the writeup are the same night.
- `scripts/events_page/render_events_page.py` read to confirm the absence of `id` attributes, the hard-coded compact anchor text, and the `public_status()` filter that produces 65 from 66.

**Link count: 23 proposed (10 events to elsewhere, 7 held pending a ruling, 5 elsewhere to events, 1 page-level). 42 of the 65 live cards get an explicit `no target`.**
