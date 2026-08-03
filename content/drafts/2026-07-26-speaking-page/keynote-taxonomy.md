# Keynote taxonomy reconciliation - #638

**Status:** research + recommendation. Nothing decided. KK rules on the set.
**Prepared:** 2026-08-02
**Lane:** Track A, draft only. No live WP write was made. Every kriskrug.co call here was a read-only GET.

## Why this doc exists

There are four different answers to "what talks does Kris give," and they are all in active use right now. If the speaking-page rebuild starts before this is settled, it encodes whichever one the agent happened to read first. The apply-ready draft in this same folder (`content/drafts/2026-07-26-speaking-page/payload-body.html`) already encodes the live set, so a decision that goes any other way means that file gets reworked before it ships.

## The four sets

| Set | Where it lives | Date of record | Talks |
|---|---|---|---|
| A | `content/source-packs/keynotes-2026/talk-topic-bank.md` | committed 2026-05-18 (`7850234`) | Both Hands Full, Punk Rock AI, Developing an AI Mindset, Compost AI, Leadership After the AI Point of No Return, Power Taste and Trust |
| B | `~/Code/kk-kb/content/people/kris-krug/site-export/speaking.md` | committed 2026-07-02 (`71b99856f`) | Both Hands Full, Authored Judgment, BC's Real AI Advantage, Who Sets the Direction Now? (with Developing an AI Mindset and Punk Rock AI demoted to "also available") |
| B2 | `~/Code/kk-kb/content/people/kris-krug/website/2026-06-wordcamp-epk.md` lines 45-54 | committed 2026-07-02 (`71b99856f`) | Both Hands Full, Authored Judgment, Developing an AI Mindset, Punk Rock AI |
| C | Live WP page 1887, `https://kriskrug.co/speaking/` | `modified: 2026-07-24T17:22:56` | Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI |

The issue named three sets. There are four. **B and B2 were committed in the same kk-kb commit on the same day and they disagree with each other.** B2 keeps Punk Rock AI and Developing an AI Mindset as headline keynotes; B demotes both and promotes BC's Real AI Advantage and Who Sets the Direction Now? in their place. Whoever picks up "Set B" gets a coin flip. That is worth knowing before anyone treats Set B as the modern answer.

Set B is also the only set that contradicts what is actually on stage: it demotes Punk Rock AI, which is the single best-documented talk in the entire inventory (see below).

How Set C was verified: `GET https://kriskrug.co/wp-json/wp/v2/pages/1887` returned 200 on 2026-08-02 with the four `.aurora-media-card` blocks named above, and the public page at `https://kriskrug.co/speaking/` returned 200.

## Comparison table

Ten distinct talk titles across the four sets. Nothing omitted.

| # | Talk | A | B | B2 | C | Delivered publicly? | Proof |
|---|---|:-:|:-:|:-:|:-:|---|---|
| 1 | Both Hands Full | yes | yes | yes | yes | **Yes, twice** | LaSalle College Vancouver 2026-01-14; WAIFF São Paulo 2026-02-26 |
| 2 | Punk Rock AI | yes | also-available | yes | yes | **Yes** | CreativeMornings Vancouver 2026-05-01, Vancouver Art Gallery |
| 3 | Developing an AI Mindset | yes | also-available | yes | yes | **Yes, in 2024** | Innovate West 2024-04-20 |
| 4 | Responsible AI | no | no | no | yes | **No, not as a keynote** | `/responsible-ai-professional/` is a cohort certification, not a talk |
| 5 | Authored Judgment (aka Taste as Moat) | no | yes | yes | no | **No** | Full script package exists, zero appearance records |
| 6 | BC's Real AI Advantage | no | yes | no | no | **No** | Full script package exists, zero appearance records |
| 7 | Who Sets the Direction Now? | no | yes | no | no | **No, near-miss** | Moderated a near-identically-titled panel, did not keynote it |
| 8 | Compost AI | yes | no | no | no | **No, submitted only** | Bass Coast 2026 Brain Stage application, Jan 2026 |
| 9 | Leadership After the AI Point of No Return | yes | no | no | no | **No** | Zero hits anywhere outside the topic bank |
| 10 | Power, Taste, and Trust | yes | no | no | no | **No** | Zero hits anywhere outside the topic bank |

Score: three of ten titles have real delivery history. One of ten is a product mislabeled as a talk. Six of ten are concepts.

## Proof detail, talk by talk

### 1. Both Hands Full - delivered, best-rounded proof

- **LaSalle College Vancouver, 2026-01-14.** Appearance record: `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2026-01-14-lasalle-college-vancouver-keynote.md`, `status: "delivered"`, `date_precision: "exact"`. The event was billed publicly as "How are creatives working with AI?" but the deck was Both Hands Full: `~/Code/kk-kb/content/knowledge/keynotes/2026-01-14-lasalle-college-vancouver/VIDEO-ASSETS.md` line 3 reads "Reusable video clips from the 'Both Hands Full' keynote presentation (January 14, 2026)."
- **Public video:** `https://www.youtube.com/watch?v=-c7mgY2aSgM`, "Both Hands Full: What Creatives Actually Need to Know About AI," 1:19:34. Indexed at `content/source-packs/keynotes-2026/video-research/README.md`. Fetched 2026-08-02, 200.
- **WAIFF São Paulo, 2026-02-26.** `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2026-02-26-waiff-sao-paulo-keynote.md`, `talk_title: "Both Hands Full"`, `status: "delivered"`, `date_precision: "approximate"` (exact festival day pending the WAIFF program, precision approximate within Feb 26 to Mar 2). Keynote 11:15 to 12:15 plus a 4:30pm panel.
- **Portal:** `https://www.bothhandsfull.com/`, fetched 2026-08-02, 200. Page states "World AI Film Festival · São Paulo," "44 minutes · 20 slides," slide reel plus dress-rehearsal audio, twelve exercise widgets, seven case studies.
- **Stage photo:** `https://kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg`, 200 on 2026-08-02. This is the only owned stage photo currently on the live speaking page, and it is currently attached to the Responsible AI card, not this one (`content/drafts/2026-07-26-speaking-page/AUDIT.md` lines 46-52).
- **Testimonial gap.** No testimonial in `content/source-packs/keynotes-2026/testimonial-bank.md` is attributed to a Both Hands Full delivery. The Jai Djwa quote is education/design-audience proof and could sit next to this talk honestly, but it is not a Both Hands Full quote. UNVERIFIED whether a LaSalle or WAIFF attendee quote exists.

**Verdict: flagship. Two stages, one long public video, a working portal, one owned stage photo. Missing a named testimonial.**

### 2. Punk Rock AI - delivered, strongest proof stack in the inventory

- **CreativeMornings Vancouver, 2026-05-01, Vancouver Art Gallery.** `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2026-05-01-creativemornings-perils-parallels.md`, `talk_title: "Punk Rock AI"`, `role: "keynote"`, `date_precision: "exact"`, `status: "delivered"`.
- **Official recording by CreativeMornings HQ:** `https://www.youtube.com/watch?v=hYT-hsml_ds`, published 2026-07-08, runtime 52:55 per YouTube metadata on 2026-07-16 (`~/Code/kk-kb/content/media/talks/2026-05-01-creativemornings-vancouver/README.md`). Fetched 2026-08-02, 200.
- **Third-party feature page:** `https://creativemornings.com/talks/kris-krug`, 200 on 2026-08-02 with a browser user agent. It returns 202 to a bare curl, so a naive link checker will flag it as a false failure. Worth noting for whoever wires the link audit.
- **Recap post on kriskrug.co:** `https://kriskrug.co/2026/05/04/punk-rock-ai/`, 200 on 2026-08-02.
- **Portal:** `https://www.punkrockai.com/`, 200 on 2026-08-02. Front page reads "Creative Mornings Vancouver · 01.05.2026" and "Photos by Michelle Diamond, Creative Mornings Vancouver, May 1 2026."
- **Professional stage photography:** `https://www.punkrockai.com/photos/michelle-diamond`, 200 on 2026-08-02. This is a full shot album by a working photographer.
- **Testimonial gap.** Same as above. Nothing in the testimonial bank is attributed to the CreativeMornings room. UNVERIFIED.

**Verdict: this is the best-evidenced talk Kris has. Official third-party video, third-party feature page, pro photos, owned recap, owned portal. Set B demotes it to a footnote. That is the single worst call in any of the four sets.**

### 3. Developing an AI Mindset - delivered, but the proof is two years old

- **Innovate West 2024, 2024-04-20.** `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2024-04-20-innovate-west-ai-mindset.md`, `status: "delivered"`, `date_precision: "approximate"` (dated from KK's own post, exact conference day not stated).
- **Evidence link:** `https://kriskrug.co/2024/04/20/ai-mindset-keynote-at-innovate-west-2024-in-vancouver/`, 200 on 2026-08-02.
- **Microsite:** `http://developinganaimindset.com/` resolves 200 but **redirects to a Notion page**: `https://kriskrug.notion.site/Developing-an-AI-Mindset-1a357f0798e144f88a108424ac22edca`. Verified with `curl -L` on 2026-08-02. A booking page sending prospects to a raw Notion site is a downgrade from the bothhandsfull.com and punkrockai.com portals sitting next to it.
- **Card image on live page:** `https://kriskrug.co/wp-content/uploads/2024/04/AI-Immortality-w-Guy-Kawasaki.png`, 200. It is a keynote graphic, not a stage photo.
- **No video.** Nothing in `content/source-packs/keynotes-2026/video-research/README.md` maps to this title.
- **Testimonial:** the Jai Djwa quote in the testimonial bank ("turned lectures into podcasts, showed them how to be design orchestrators") is the closest fit for an AI-mindset team/education audience, but it is not attributed to this talk.

**Verdict: real, delivered, and aging. It is also the only delivered talk aimed at teams and leadership rather than creatives. Keeping it costs nothing; presenting it with 2024 proof and a Notion redirect costs credibility.**

### 4. Responsible AI - not a keynote, this is a category error on the live page

`https://kriskrug.co/responsible-ai-professional/` returned 200 on 2026-08-02. Its `<title>` is "Responsible AI Professional Certification." Body copy: "Responsible AI Professional is a cohort-based certification built to close that gap," with sections "What changes," "Who it is for," and a "Join the next cohort" CTA. It is the RAP program, not a talk.

The live speaking page presents it as the fourth signature topic, in the same card grid as three real keynotes, illustrated with the LaSalle Both Hands Full stage photo. So the one owned stage shot on the page is doing duty for the one item on the page that is not a talk.

Nearest real delivered thing with this subject matter: Sea to Sky Gondola staff workshop, 2026-03-31, `talk_title: "AI Ethics / Responsible Use Workshop"`, `status: "delivered"` (`~/Code/kk-kb/.../appearances/2026-03-31-sea-to-sky-gondola-ai-ethics-workshop.md`). That is a workshop, not a keynote, and it is a private corporate booking.

**Verdict: remove from the keynote grid. It belongs in the Workshops or programs lane.**

### 5. Authored Judgment (Taste as Moat) - concept, fully built, never delivered under this name

- Full package: `~/Code/kk-kb/content/knowledge/keynotes/kris-krug-keynote-concepts/02-taste-as-moat/` with `concept.md`, `full-script.md`, `slide-concepts.md`, and a taste-audit worksheet. The collection README marks it "Production-ready."
- Grep for "Authored Judgment" across all of `~/Code/kk-kb/content/` returns eight files. Every one of them is a website draft, booking template, or the site-export itself. Zero appearance records. Zero delivery evidence.
- It is the one concept-only talk that appears in **both** Set B and Set B2, so it is the concept KK's own drafts keep reaching for.

**Verdict: strongest bench candidate. Zero stage proof.**

### 6. BC's Real AI Advantage - concept, fully built, never delivered

- Full package: `~/Code/kk-kb/content/knowledge/keynotes/kris-krug-keynote-concepts/01-bc-real-ai-advantage/` including two audience adaptations and two worksheets.
- Grep for "Real AI Advantage" across `~/Code/kk-kb/content/` returns only files inside that concept folder plus two README index files. No appearance record.

**Verdict: concept. Real regional booking angle, no stage yet.**

### 7. Who Sets the Direction Now? - concept, with a near-miss that is not what it looks like

- Full package: `~/Code/kk-kb/content/knowledge/keynotes/kris-krug-keynote-concepts/05-who-sets-direction/`.
- The near-miss: Global AI Summit Vancouver 2026, 2026-04-01, UBC Robson Square, panel titled "Who Shapes the AI Future: Markets, Policy, or Culture?" That is the same thesis and almost the same title. But `~/Code/kk-kb/.../appearances/2026-04-01-global-ai-summit-vancouver-moderator.md` records `role: "moderator"`, 11:10 to 11:50 with a 3 to 5 minute Q&A close. Kris moderated the panel. He did not keynote it. The record's only evidence is his own Google Calendar, surfaced by the 2026-07-11 calendar sweep, with no public listing captured.

This is exactly the kind of thing that turns into a fabricated delivery claim if nobody checks. Moderating a panel with your talk's title is not delivering the talk.

**Verdict: concept. Do not let the panel become "proof."**

### 8. Compost AI - submitted, not delivered

- `~/Code/kk-kb/content/knowledge/keynotes/2026-basscoast-application/README.md`: "Status: Submitted / Ready to Submit," date January 10, 2026, "Selected Concept: Compost AI," a 75-minute Brain Stage run-of-show script, deadline Jan 10 2026, theme "Into the Deep Blue."
- The appearances index lists "Bass Coast 2026 - submission package" and there is no `2026-07-*-bass-coast` appearance file. The only delivered Bass Coast record is 2025-07-11, "Dear AI, Before We Go Any Further... We Need To Talk About Your Soul," a different session.
- Set A already labels it honestly: "Treat as in development until a public delivered-event source is verified" (`talk-topic-bank.md` line 45).

**Verdict: UNVERIFIED whether it ran at Bass Coast in July 2026. I found no delivery record. If KK knows it ran, that changes its tier and someone needs to file the appearance record.**

### 9. Leadership After the AI Point of No Return - no source anywhere

Grep for "point of no return" across all of `~/Code/kk-kb/content/` returns zero files. It exists in exactly one place: `talk-topic-bank.md` lines 47-55, where Set A itself says "Available topic. Use as a program option, not as past-stage proof."

**Verdict: a title, not a talk.**

### 10. Power, Taste, and Trust - no source anywhere, and it duplicates #5

Grep for "Power, Taste" across all of `~/Code/kk-kb/content/` returns zero files. Same single-source situation as #9, same self-applied caveat in `talk-topic-bank.md` lines 57-65.

It also says the same thing as Authored Judgment. Compare `talk-topic-bank.md` line 61 ("taste, trust, and power become the strategic layer when models, tools, and automation become cheap") against Set B's Authored Judgment ("Your moat isn't your code anymore. It's your taste"). One thesis, two names.

**Verdict: merge into Authored Judgment. Two names for one talk is a taxonomy bug, not a second offering.**

## What the proof actually says

Sort the ten by evidence and the page writes itself:

**Tier 1, delivered with third-party proof:** Punk Rock AI, Both Hands Full.
**Tier 2, delivered, proof aging:** Developing an AI Mindset.
**Tier 3, built but never on a stage:** Authored Judgment, BC's Real AI Advantage, Who Sets the Direction Now?, Compost AI.
**Tier 4, a title in one document:** Leadership After the AI Point of No Return, Power Taste and Trust.
**Not a talk:** Responsible AI.

None of the four sets matches that ordering. Set A pads Tier 4. Set B leads with Tier 3 and buries Tier 1. Set C ships a certification as a keynote. Set B2 is closest to right and nobody is using it.

## Recommendation

**A 3 + 1 set.** Three delivered talks in the keynote grid, plus one deliberately-labeled new talk, plus a short bench line.

| Slot | Talk | Why |
|---|---|---|
| 1 | **Punk Rock AI** | Best proof stack Kris has. Official CreativeMornings recording, CreativeMornings feature page, Michelle Diamond photo album, owned recap post, working portal. Lead with the receipts. |
| 2 | **Both Hands Full** | Two stages including an international one, an 80-minute public video, the richest portal, the one owned stage photo. This is the flagship thesis and it holds the other talks together. |
| 3 | **Developing an AI Mindset** | The only delivered talk pointed at teams, leadership, and associations. Without it the page only sells to creatives. Ship it with a 2026 refresh, not with 2024 proof. |
| 4 | **One new-for-2026 talk, KK's pick** | Recommend **Authored Judgment**. Complete script package, and it is the only concept both Set B and Set B2 agree on. Label it plainly as new. Do not backfill a stage it has not been on. |

Rationale in one line: the page should be ordered by what a booker can verify in thirty seconds, and right now it is ordered by nothing in particular.

Two rules that fall out of this:

1. **A talk goes in the keynote grid only if it has a named venue and date, or an honest "new for 2026" label.** No third state.
2. **Programs and certifications do not go in the keynote grid.** They get their own row.

### Disposition of everything that does not make the cut

| Talk | Disposition | Reason |
|---|---|---|
| Responsible AI | **Move out of keynotes.** Give RAP a program card or fold it under the Workshops format card, still linking `/responsible-ai-professional/`. | It is a cohort certification. Verified by fetching the page. |
| BC's Real AI Advantage | **Bench.** Keep the script. Surface it as "also available" only if KK is chasing regional and economic-development bookings. | Real angle, complete script, zero stage. |
| Who Sets the Direction Now? | **Merge into Both Hands Full and Punk Rock AI, or bench.** Its BC+AI governance story already appears inside both delivered talks. | The only near-proof is a moderated panel, and moderating is not keynoting. |
| Compost AI | **Move to the workshop menu.** It is a 75-minute session format, not a keynote. | Bass Coast 2026 submission. Delivery UNVERIFIED. |
| Power, Taste, and Trust | **Retire the title, fold the content into Authored Judgment.** | Same thesis, second name, zero sources. |
| Leadership After the AI Point of No Return | **Retire.** | Zero sources outside one line in one file. |

## What is still missing, whichever set wins

- **No testimonial in the bank is attributed to a specific talk.** `content/source-packs/keynotes-2026/testimonial-bank.md` has four approved quotes and not one names a keynote. Acceptance criterion 3 on #638 asks for video + photo + testimonial per talk. Video and photo are covered for the top two. Testimonials are not, for any of the ten. Someone has to go get named quotes from the CreativeMornings and LaSalle rooms.
- **Both Hands Full has no owned photo from WAIFF São Paulo** that I could find in the repo or the KB. The only stage photo in play is LaSalle.
- **Developing an AI Mindset has no video and no stage photo.**
- **WAIFF date precision is approximate.** The appearance record says the exact festival day is pending the WAIFF program. If the page prints a date, print February 2026, not February 26.

## Blast radius

Whatever KK picks drives all of these, and several of them are already written against Set C:

- `content/drafts/2026-07-26-speaking-page/payload-body.html` hardcodes the Set C four (Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI). Any other outcome means reworking this file before apply.
- `content/drafts/2026-07-26-speaking-page/multimedia-rebuild-plan.md` and `video-set.md` assign media per talk.
- Live WP page 1887 body, which is a single `wp:html` pack, so the whole thing gets replaced at once.
- Page schema and internal links. Right now the grid links out to two third-party portals plus one internal page. Changing the set changes the internal link graph and any per-talk structured data.
- The topic-bank source of truth at `content/source-packs/keynotes-2026/talk-topic-bank.md`, which should be rewritten to match the decision rather than left as a fifth competing version.
- `~/Code/kk-kb` Set B and Set B2 should get a pointer to the decision so the next agent does not resurrect them.

---

# DECISION BLOCK FOR KK

Nothing below is decided. Each item is a yes/no or a pick-one. My recommendation is flagged, and it is only a recommendation.

**D1. Order the keynote grid by verifiable public proof rather than by thesis?**
Yes / No.
*Recommend: Yes.*

**D2. Lead the page with Punk Rock AI rather than Both Hands Full?**
Yes / No.
*Recommend: Yes. Punk Rock AI has an official third-party recording, a third-party feature page, and a pro photo album. Both Hands Full is the bigger idea; Punk Rock AI is the better proof. If you would rather lead with the idea, say so and I will not argue.*

**D3. Ship three delivered talks plus one clearly-labeled new one, or three only, or four including an unlabeled new one?**
Pick one: 3+1 labeled / 3 only / 4 unlabeled.
*Recommend: 3+1 labeled.*

**D4. If 3+1, which talk fills slot 4?**
Pick one: Authored Judgment / BC's Real AI Advantage / Who Sets the Direction Now? / none.
*Recommend: Authored Judgment.*

**D5. Remove Responsible AI from the keynote grid and give RAP its own program card?**
Yes / No.
*Recommend: Yes. It is a certification page, not a talk, and it is currently wearing the only owned stage photo on the page.*

**D6. Keep Developing an AI Mindset in the top set?**
Yes / No.
*Recommend: Yes, with a condition. It is the only delivered talk aimed at teams and leadership. But its microsite redirects to a raw Notion page and its only proof is a 2024 post. Keep it and fix the destination, or bench it until there is a 2026 delivery.*

**D7. Retire "Leadership After the AI Point of No Return" and "Power, Taste, and Trust" as standalone titles?**
Yes / No.
*Recommend: Yes. Zero sources anywhere. Fold Power Taste and Trust into Authored Judgment.*

**D8. Move Compost AI to the workshop menu instead of the keynote grid?**
Yes / No.
*Recommend: Yes, unless you actually delivered it at Bass Coast in July 2026. I found no record either way. If it ran, tell me and I will file the appearance record and re-tier it.*

**D9. Adopt the rule "a talk enters the keynote grid only with a named venue and date, or an explicit new-for-2026 label"?**
Yes / No.
*Recommend: Yes. This is the rule that stops the four sets from becoming five.*

**D10. After you rule, rewrite `content/source-packs/keynotes-2026/talk-topic-bank.md` to match, and leave a pointer in the two kk-kb drafts?**
Yes / No.
*Recommend: Yes, otherwise the losing sets stay live in the repo and the next agent picks one at random.*

**Open question, not a decision:** do named testimonials exist from the CreativeMornings Vancouver or LaSalle rooms? None are in the testimonial bank. If they exist in your inbox or DMs, that closes the last real gap in the proof stack for the top two talks.
