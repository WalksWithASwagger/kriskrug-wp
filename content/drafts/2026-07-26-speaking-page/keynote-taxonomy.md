# Keynote taxonomy reconciliation - #638

**Status:** research + recommendation. Nothing decided. KK rules on the set.
**Prepared:** 2026-08-02
**Corrected:** 2026-08-02 after adversarial verification. Set counts, two grep counts, and the Tier 4 evidence were wrong in the first pass. See the correction log at the bottom.
**Lane:** Track A, draft only. No live WP write was made. Every kriskrug.co call here was a read-only GET.

## Why this doc exists

There are six different answers to "what talks does Kris give," and they are all sitting in files an agent can reach today. If the speaking-page rebuild starts before this is settled, it encodes whichever one the agent happened to read first. The apply-ready draft in this same folder (`content/drafts/2026-07-26-speaking-page/payload-body.html`) already encodes the current live set, so a decision that goes any other way means that file gets reworked before it ships.

## The six sets

| Set | Where it lives | Date of record | Talks |
|---|---|---|---|
| A | `content/source-packs/keynotes-2026/talk-topic-bank.md` headings at lines 7, 17, 27, 37, 47, 57 | committed 2026-05-18 (`7850234`) | Both Hands Full, Punk Rock AI / Creative Rebellion, Developing an AI Mindset, Compost AI, Leadership After the AI Point of No Return, Power Taste and Trust |
| B | `~/Code/kk-kb/content/people/kris-krug/site-export/speaking.md` | committed 2026-07-02 (`71b99856f`) | Both Hands Full, Authored Judgment, BC's Real AI Advantage, Who Sets the Direction Now? (with Developing an AI Mindset and Punk Rock AI demoted to "also available") |
| B2 | `~/Code/kk-kb/content/people/kris-krug/website/2026-06-wordcamp-epk.md`, section heading line 45, table lines 47-52, source note line 54 | committed 2026-07-02 (`71b99856f`) | Both Hands Full, Authored Judgment, Developing an AI Mindset, Punk Rock AI |
| C | Live WP page 1887, `https://kriskrug.co/speaking/` | `modified: 2026-07-24T17:22:56` | Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI |
| D | **Prior live page 1887.** Readback: `backup/20260701T193335Z-content-architecture/page-snapshots/page-1887-speaking-before.html` lines 275-327, `modified: 2026-06-28T14:14:01`. Repo-side source still tracked at `content/source-packs/keynotes-2026/wp-payloads/speaking.html` lines 138-183 | snapshotted 2026-07-01, payload last touched 2026-06-16 (`1fa1999`) | Both Hands Full, Punk Rock AI, Developing an AI Mindset, Compost AI, Leadership After the AI Point of No Return, Power, Taste, and Trust |
| E | `content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md` lines 9-55 | committed 2026-05-18 (`7850234`), same commit as Set A | Notion-sourced. Variant titles, see the alias map below. Adds one talk nothing else lists: Dear AI: We Need to Talk About Your Soul |

The issue named three sets. There are six. Corrections that produced that number:

- **Set D is the big one.** The two titles this doc originally filed as Tier 4 "a title in one document" were on `kriskrug.co/speaking/` under an `<h2>Signature keynote topics</h2>` heading until the 2026-07-24 rewrite. Verified in `page-1887-speaking-before.html`: `<h2>Signature keynote topics</h2>` at line 275, then six `<h3>` cards at lines 282, 291, 300, 309, 318, 327, next `<h2>` at line 336. The six titles match Set A's six headings exactly, in the same order. **Set A was not a shelf document. It was the live page.**
- **Set E was in the same commit as Set A** and nobody reconciled them. It is a Notion extraction with its own title variants and one talk that never enters any other list.
- **B and B2 were committed in the same kk-kb commit on the same day and they disagree with each other.** B2 keeps Punk Rock AI and Developing an AI Mindset as headline keynotes; B demotes both and promotes BC's Real AI Advantage and Who Sets the Direction Now? in their place. Whoever picks up "Set B" gets a coin flip.

Set B is also the only set that contradicts what is actually on stage: it demotes Punk Rock AI, which is the single best-documented talk in the entire inventory (see below).

How Set C was verified: `GET https://kriskrug.co/wp-json/wp/v2/pages/1887` returned 200 on 2026-08-02, `modified: 2026-07-24T17:22:56`, with `<h3>` cards Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI.

### Set E alias map

Set E names the same talks differently. Every Set E label, mapped:

| Set E label (line) | What it actually is |
|---|---|
| `Keynote: Creative Rebellion` (11) | Punk Rock AI. Set A already carries the alias in its heading, "Punk Rock AI / Creative Rebellion" (line 17). |
| `World AI Film Festival Keynote 2026` (18) | Both Hands Full at WAIFF, public title "How to Keep Our Souls Intact When the Machines Get Really Good at Making Everything." |
| `Both Hands Full` (54) | Same talk again, listed a second time in the same file under In-Development. |
| `KEYNOTE: Developing AI Mindset` (15) | Developing an AI Mindset. |
| `Your Moat Isn't Your Code Anymore (It's Your Taste)` (52) | **Third name for Authored Judgment.** Compare Set B's "Your moat isn't your code anymore. It's your taste." |
| `Power, Taste, and Trust When AI Becomes the Layer Nobody Audits` (47) | Longer form of Power, Taste, and Trust. |
| `BC's Real AI Advantage (What Silicon Valley Can't Copy)` (50) | Longer form of BC's Real AI Advantage. |
| `Leadership After the AI Point of No Return` (44) | Same title, verbatim. |
| `Compost AI` (36) | Same title. |
| `Dear AI: We Need to Talk About Your Soul` (40) | **New. Not in any other set.** And it is the only one of Set E's additions with a delivery record. |
| `AI for Good` (23), `Who Owns The Future?` (29) | Topic families, not talk titles. The file says so itself: "Public-safe as a topic family. Use broad framing unless a specific event page is verified." Neither appears as a `talk_title` in any appearance record. |
| `Whistler Institute` (25), `Social Media Camp Victoria` (27), `UN Global Youth Summit on HIV` (31) | Venues, not talks. Whistler has an appearance record (`2025-01-23-whistler-institute-keynote.md`, `status: "delivered"`) with no `talk_title` field set. |

## Comparison table

Eleven distinct talk titles across the six sets. Nothing omitted. Aliases are folded per the map above.

The `Delivered publicly?` column is graded against one authoritative list: every `talk_title` value in `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/*.md`. Command run 2026-08-02: `grep -rh "^talk_title:" .../appearances/*.md | sort | uniq -c`. It returned 20 rows: 19 distinct non-empty titles plus `talk_title: ""` on 3 records. Four of the 19 are in this table: `"Both Hands Full"`, `"Punk Rock AI"`, `"Developing an AI Mindset"`, and `"Dear AI, Before We Go Any Further… We Need To Talk About Your Soul"`. Every other title in this table has no matching `talk_title` anywhere in the appearance records.

| # | Talk | A | B | B2 | C | D | E | Delivered publicly? | Proof |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| 1 | Both Hands Full | yes | yes | yes | yes | yes | yes | **Yes, once under this title** | WAIFF São Paulo 2026-02-26 (`talk_title: "Both Hands Full"`). LaSalle 2026-01-14 was billed "How are creatives working with AI?"; the deck was Both Hands Full per `VIDEO-ASSETS.md` line 3. Deck-level, not billing-level. |
| 2 | Punk Rock AI | yes | also-available | yes | yes | yes | as "Creative Rebellion" | **Yes** | CreativeMornings Vancouver 2026-05-01, Vancouver Art Gallery, `talk_title: "Punk Rock AI"` |
| 3 | Developing an AI Mindset | yes | also-available | yes | yes | yes | yes | **Yes, in 2024** | Innovate West 2024-04-20 |
| 4 | Responsible AI | no | no | no | yes | no | no | **No, not as a keynote** | `/responsible-ai-professional/` is a cohort certification, not a talk |
| 5 | Authored Judgment (aka Taste as Moat, aka Your Moat Isn't Your Code) | no | yes | yes | no | no | yes | **No** | Full script package exists, zero appearance records |
| 6 | BC's Real AI Advantage | no | yes | no | no | no | yes | **No** | Full script package exists, zero appearance records |
| 7 | Who Sets the Direction Now? | no | yes | no | no | no | no | **No, near-miss** | Moderated a near-identically-titled panel, did not keynote it |
| 8 | Compost AI | yes | no | no | no | yes | yes | **No, submitted only** | Bass Coast 2026 Brain Stage application, Jan 2026 |
| 9 | Leadership After the AI Point of No Return | yes | no | no | no | **yes, was live** | yes | **No** | No `talk_title` match. But it shipped on the live speaking page until 2026-07-24. |
| 10 | Power, Taste, and Trust | yes | no | no | no | **yes, was live** | yes | **No** | No `talk_title` match. Same: live until 2026-07-24. |
| 11 | Dear AI: We Need to Talk About Your Soul | no | no | no | no | no | yes | **Yes, as a workshop** | Bass Coast Festival 2025-07-11, `role: "workshop-lead"`, `status: "delivered"`, public video |

Score: four of eleven titles have a real delivery record, and one of those four (Dear AI) was delivered as a festival workshop, not a keynote. One of eleven is a product mislabeled as a talk. Six of eleven have never been in front of a room under that name.

## Proof detail, talk by talk

### 1. Both Hands Full - delivered, best-rounded proof

- **LaSalle College Vancouver, 2026-01-14.** Appearance record: `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2026-01-14-lasalle-college-vancouver-keynote.md`, `status: "delivered"`, `date_precision: "exact"`, `role: "keynote"`. **Caveat, and it matters for how the page prints this:** that record's `talk_title` is `"How are creatives working with AI?"`, not Both Hands Full. The deck was Both Hands Full. `~/Code/kk-kb/content/knowledge/keynotes/2026-01-14-lasalle-college-vancouver/VIDEO-ASSETS.md` line 3 reads verbatim: "Reusable video clips from the 'Both Hands Full' keynote presentation (January 14, 2026)." So the deck identity is sourced, the public billing is not. If the speaking page prints "Both Hands Full at LaSalle" as a delivery credit, it is making a deck-level claim under a billing-level frame. Print it as the LaSalle talk that used the Both Hands Full deck, or lead the credit with WAIFF, where `talk_title` is literally `"Both Hands Full"`.
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

**Verdict: this is the best-evidenced talk Kris has. Official third-party video, third-party feature page, pro photos, owned recap, owned portal. Set B demotes it to a footnote. That is the single worst call in any of the six sets.**

### 3. Developing an AI Mindset - delivered, but the proof is two years old

- **Innovate West 2024, 2024-04-20.** `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2024-04-20-innovate-west-ai-mindset.md`, `status: "delivered"`, `date_precision: "approximate"` (dated from KK's own post, exact conference day not stated).
- **Evidence link:** `https://kriskrug.co/2024/04/20/ai-mindset-keynote-at-innovate-west-2024-in-vancouver/`, 200 on 2026-08-02.
- **Microsite:** `http://developinganaimindset.com/` resolves 200 but **redirects to a Notion page**: `https://kriskrug.notion.site/Developing-an-AI-Mindset-1a357f0798e144f88a108424ac22edca`. Verified with `curl -L` on 2026-08-02. A booking page sending prospects to a raw Notion site is a downgrade from the bothhandsfull.com and punkrockai.com portals sitting next to it.
- **Card image on live page:** `https://kriskrug.co/wp-content/uploads/2024/04/AI-Immortality-w-Guy-Kawasaki.png`, 200. It is a keynote graphic, not a stage photo.
- **No video.** Nothing in `content/source-packs/keynotes-2026/video-research/README.md` maps to this title.
- **Testimonial:** the Jai Djwa quote in the testimonial bank ("turned lectures into podcasts, showed them how to be design orchestrators") is the closest fit for an AI-mindset team/education audience, but it is not attributed to this talk.

**Verdict: real, delivered, and aging. It is also the only delivered talk aimed at teams and leadership rather than creatives. Keeping it costs nothing; presenting it with 2024 proof and a Notion redirect costs credibility.**

### 4. Responsible AI - not a keynote, and this is live right now

**This is the finding with the shortest fuse in the doc. It is shipping on kriskrug.co today.**

`https://kriskrug.co/responsible-ai-professional/` returned 200 on 2026-08-02. Its `<title>` opens "Responsible AI Professional Certification" before the site-wide suffix. Body copy: "Responsible AI Professional is a cohort-based certification built to close that gap," with sections "What changes," "Who it is for," and a "Join the next cohort" CTA. It is the RAP program, a paid cohort you enrol in. It is not a talk.

The live speaking page presents it as the fourth signature keynote card. From the `GET https://kriskrug.co/wp-json/wp/v2/pages/1887` readback on 2026-08-02, the card markup is:

```html
<article class="aurora-media-card">
  <a href="/responsible-ai-professional/">
    <img src="https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg?w=1200&ssl=1"
         alt="Kris Krug speaking at LaSalle College Vancouver" />
    <div><h3>Responsible AI</h3><p>Bias, privacy, provenance, labor, trust, authenticity...</p></div>
  </a>
</article>
```

Read that carefully. A booker scanning the keynote grid sees a photo of Kris on a stage at LaSalle, captioned as a keynote topic, and clicks through to a cohort enrolment page.

All four card images from that same readback:

| Card | Image file | Alt |
|---|---|---|
| Both Hands Full | `opengraph-image?46af5f0ff830fe03` | Both Hands Full keynote portal graphic |
| Punk Rock AI | `195.webp` | Punk Rock AI portal preview |
| Developing an AI mindset | `AI-Immortality-w-Guy-Kawasaki.png` | Developing an AI Mindset keynote graphic with Guy Kawasaki |
| Responsible AI | `kk-laSalle-both-hands-full-10-scaled.jpg` | Kris Krug speaking at LaSalle College Vancouver |

Three real keynotes get portal graphics and a promo still. The certification gets the only human-on-a-stage photograph. And that photograph is a Both Hands Full photo, sitting on the wrong card, while Both Hands Full runs an OpenGraph asset.

Nearest real delivered thing with this subject matter: Sea to Sky Gondola staff workshop, 2026-03-31, `talk_title: "AI Ethics / Responsible Use Workshop"`, `status: "delivered"` (`~/Code/kk-kb/.../appearances/2026-03-31-sea-to-sky-gondola-ai-ethics-workshop.md`). That is a workshop, not a keynote, and it is a private corporate booking.

**Verdict: remove from the keynote grid. It belongs in the Workshops or programs lane.**

### 5. Authored Judgment (Taste as Moat) - concept, fully built, never delivered under this name

- Full package: `~/Code/kk-kb/content/knowledge/keynotes/kris-krug-keynote-concepts/02-taste-as-moat/` with `concept.md`, `full-script.md`, `slide-concepts.md`, and a taste-audit worksheet. The collection README marks it "Production-ready."
- `grep -ril "Authored Judgment" ~/Code/kk-kb/content/` returns **10 files**, run 2026-08-02. Eight are website drafts, booking templates, or the site-export itself: `people/kris-krug/booking/formal-speaker-invitation.md`, `people/kris-krug/site-export/speaking.md`, `website/2026-05-22-redesign-analysis.md`, `website/2026-05-22-redesign-brief.md`, `website/2026-06-15-hero-about-both-hands-full.md`, `website/2026-06-15-positioning-master-plan.md`, `website/2026-06-15-speaker-page.md`, `website/2026-06-wordcamp-epk.md`. Two are false positives on the phrase rather than the title: `admin/scheduled-task-reports/social-clip-growth-weekly/data/2026-06-18/normalized-buffer-social.json` (a post opener, "what it needs is authored judgment") and `projects/05-marketing-and-outreach/press-and-media/media-credits/assets/2009-01-02-kriskrug-photography-recap-2008.html` (an archived page capture whose Aurora footer carries the site tagline, "Authored judgment, human agency, and the camera-trained habit of paying attention").
- **Zero appearance records.** `grep -ril "Authored Judgment" .../press-and-media/appearances/` returns nothing, and no `talk_title` in any appearance record matches. Zero delivery evidence.
- It is the one concept-only talk that appears in **both** Set B and Set B2, and Set E carries it a third time under yet another name, "Your Moat Isn't Your Code Anymore (It's Your Taste)" (line 52). Three sets, three names, one talk.

**Verdict: strongest bench candidate. Zero stage proof. Needs one name before it ships anywhere.**

### 6. BC's Real AI Advantage - concept, fully built, never delivered

- Full package: `~/Code/kk-kb/content/knowledge/keynotes/kris-krug-keynote-concepts/01-bc-real-ai-advantage/` including two audience adaptations and two worksheets.
- `grep -ril "Real AI Advantage" ~/Code/kk-kb/content/` returns **15 files**, run 2026-08-02. Breakdown:
  - **Eight inside the concept folder:** `concept.md`, `full-script.md`, `slide-concepts.md`, `speaker-notes.md`, `adaptations/30-min-version.md`, `adaptations/government-audience.md`, `worksheets/4-test-questions.md`, `worksheets/extractive-vs-regenerative-checklist.md`.
  - **Three index files:** `knowledge/keynotes/kris-krug-keynote-concepts/README.md`, `knowledge/keynotes/kris-krug-keynote-concepts/NOTION-IMPORT-GUIDE.md`, `knowledge/README.md`.
  - **Four outside the concept folder, and this is the part that matters:** `people/kris-krug/booking/formal-speaker-invitation.md`, `people/kris-krug/site-export/speaking.md` (Set B), `people/kris-krug/website/2026-06-15-speaker-page.md`, `people/kris-krug/website/2026-06-15-positioning-master-plan.md`. A concept with zero stage history is already written into a booking invitation template and a positioning master plan. That is how an unstaged title turns into an implied credit.
- **Zero appearance records.** `grep -ril "Real AI Advantage" .../press-and-media/appearances/` returns nothing, and no `talk_title` matches.

**Verdict: concept. Real regional booking angle, no stage yet, and already leaking into booking collateral.**

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

### 9. Leadership After the AI Point of No Return - never delivered, but it was live on kriskrug.co

**Correction.** The first pass of this doc said "zero hits anywhere outside the topic bank" and "it exists in exactly one place." Both were wrong. Here is what the greps actually return, run 2026-08-02.

`grep -ril "point of no return" ~/Code/kk-kb/content/` returns **zero files**. That half was right. No appearance record, no `talk_title` match, no delivery evidence in the knowledge base.

`grep -ril "point of no return" .` inside this repo returns **28 files**. Excluding this doc and the `backup/` tree, four are live source files:

| File | Line | What it is |
|---|---|---|
| `content/source-packs/keynotes-2026/talk-topic-bank.md` | 47-55 | Set A. Self-caveated: "Available topic. Use as a program option, not as past-stage proof." |
| `content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md` | 44 | Set E, under In-Development Topics |
| `content/source-packs/keynotes-2026/wp-payloads/speaking.html` | 174 | **A tracked, apply-ready `kk-card` with an `<h3>` and an "Ask about this talk" contact link.** |
| `content/source-packs/keynotes-2026/wp-payloads/work.html` | 175 | Prose reuse of the phrase |

And in `backup/`: `20260701T193335Z-content-architecture/page-snapshots/page-1887-speaking-before.html` line 318, an `<h3>` card under `<h2>Signature keynote topics</h2>`, in a snapshot of live page 1887 with `modified: 2026-06-28T14:14:01`. Also present in the 2026-05-18 and 2026-06-04 snapshot sets.

So this title was on the public speaking page for months. It came down in the 2026-07-24 rewrite. It is not "a title in one document." It is a title that was on stage-adjacent public real estate without ever being on a stage, and the repo still holds an apply-ready payload that would put it back.

**Verdict: never delivered, and the risk is the opposite of what the first pass said. Not "harmless title in a shelf doc." An unstaged title with live history and a loaded payload file.**

### 10. Power, Taste, and Trust - same story as #9, and it duplicates #5

**Correction.** Same defect as #9: the first pass claimed zero hits outside the topic bank. Actual greps, run 2026-08-02.

`grep -ril "Power, Taste" ~/Code/kk-kb/content/` returns **zero files**. No appearance record, no `talk_title` match.

`grep -ril "Power, Taste" .` inside this repo returns **29 files**. Excluding this doc and `backup/`, three are live source files:

| File | Line | What it is |
|---|---|---|
| `content/source-packs/keynotes-2026/talk-topic-bank.md` | 57-65 | Set A. Same self-applied caveat as #9. |
| `content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md` | 47 | Set E, as "Power, Taste, and Trust When AI Becomes the Layer Nobody Audits" |
| `content/source-packs/keynotes-2026/wp-payloads/speaking.html` | 183 | **Apply-ready `kk-card` with an "Ask about this talk" contact link.** Its card image is `kk-laSalle-both-hands-full-15-scaled.jpg`, another Both Hands Full stage photo on a talk that has never been delivered. |

And in `backup/`: `page-1887-speaking-before.html` line 327, `<h3>` card, live until 2026-07-24.

It also says the same thing as Authored Judgment. Compare `talk-topic-bank.md` line 61 ("taste, trust, and power become the strategic layer when models, tools, and automation become cheap") against Set B's Authored Judgment ("Your moat isn't your code anymore. It's your taste") and Set E line 52 ("Your Moat Isn't Your Code Anymore (It's Your Taste)"). One thesis, three names.

**Verdict: merge into Authored Judgment. Three names for one talk is a taxonomy bug, not three offerings. And like #9, it was public.**

### 11. Dear AI: We Need to Talk About Your Soul - delivered, and missing from every set except E

This one only surfaces because Set E exists. Nothing in Sets A, B, B2, C, or D lists it.

- **Delivery record:** `~/Code/kk-kb/content/projects/05-marketing-and-outreach/press-and-media/appearances/2025-07-11-bass-coast-dear-ai-workshop.md`. `talk_title: "Dear AI, Before We Go Any Further… We Need To Talk About Your Soul"`, `status: "delivered"`, `role: "workshop-lead"`, `date_precision: "approximate"`, Bass Coast Festival 2025 Brain Stage, Merritt BC.
- **Public video:** `https://www.youtube.com/watch?v=owtSPcpRinI`, fetched 2026-08-02, 200. The record notes it was uploaded 2025-07-25.
- The record itself makes the taxonomy link explicit: "This is the delivered home of the 'Dear AI: We Need to Talk About Your Soul' talk from the Notion keynote library."
- It already appears on the repo-side payload at `content/source-packs/keynotes-2026/wp-payloads/speaking.html` line 208, but in the "Watch selected talks" video section, not the keynote grid. Same on the prior live page: `page-1887-speaking-before.html` line 349 embeds `https://www.youtube.com/embed/owtSPcpRinI?start=19` with the `<h3>` at line 352, under `<h2>Watch selected talks</h2>` at line 336. So the video was public on `/speaking/` while the talk itself appeared in no topic list.

**Read the role field before promoting this.** `role: "workshop-lead"`, not `keynote`. It is a delivered festival workshop with a public recording. That makes it real proof for a workshop menu and real proof of range. It does not make it a delivered keynote.

**Verdict: real delivered session, wrong shelf. It belongs on the workshops line with the video attached, not in the keynote grid. And the fact that a talk with a public video and a delivery record went missing from four of six sets is the clearest evidence that the sets are not being maintained against the appearance records.**

## What the proof actually says

Sort the eleven by evidence and the page writes itself:

**Tier 1, delivered with third-party proof:** Punk Rock AI, Both Hands Full.
**Tier 2, delivered, proof aging:** Developing an AI Mindset.
**Tier 2b, delivered as a workshop, not a keynote:** Dear AI: We Need to Talk About Your Soul.
**Tier 3, built but never on a stage:** Authored Judgment, BC's Real AI Advantage, Who Sets the Direction Now?, Compost AI.
**Tier 4, never delivered but shipped publicly anyway:** Leadership After the AI Point of No Return, Power Taste and Trust. (The first pass of this doc called Tier 4 "a title in one document." That was wrong. Both were `<h3>` cards on the live speaking page until the 2026-07-24 rewrite, and both still sit in a tracked apply-ready payload.)
**Not a talk:** Responsible AI.

None of the six sets matches that ordering. Set A and Set D pad Tier 4, and Set D shipped it. Set B leads with Tier 3 and buries Tier 1. Set C ships a certification as a keynote. Set E is the only one that lists a Tier 2b talk with a public video, and nobody is using Set E. Set B2 is closest to right and nobody is using that either.

## Recommendation

**A 3 + 1 set.** Three delivered talks in the keynote grid, plus one deliberately-labeled new talk, plus a short bench line.

| Slot | Talk | Why |
|---|---|---|
| 1 | **Punk Rock AI** | Best proof stack Kris has. Official CreativeMornings recording, CreativeMornings feature page, Michelle Diamond photo album, owned recap post, working portal. Lead with the receipts. |
| 2 | **Both Hands Full** | Two stages including an international one, an 80-minute public video, the richest portal, the one owned stage photo. This is the flagship thesis and it holds the other talks together. Credit WAIFF first, since that is the record whose `talk_title` literally reads "Both Hands Full"; LaSalle was billed differently. |
| 3 | **Developing an AI Mindset** | The only delivered talk pointed at teams, leadership, and associations. Without it the page only sells to creatives. Ship it with a 2026 refresh, not with 2024 proof. |
| 4 | **One new-for-2026 talk, KK's pick** | Recommend **Authored Judgment**. Complete script package, and it is the concept Sets B, B2, and E all reach for (under three different names). Label it plainly as new. Do not backfill a stage it has not been on. |

Plus a change that falls out of Set E and did not exist in the first pass of this doc: **Dear AI belongs on the workshop line, with its video.** It is a `status: "delivered"`, `role: "workshop-lead"` record with a public YouTube recording, and the recording was already embedded on the prior live speaking page. Four of the six sets forgot it exists. Putting it on the workshop menu costs nothing and adds a real receipt to the one part of the offer that currently has none.

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
| Dear AI: We Need to Talk About Your Soul | **Add to the workshop menu with its video.** Not the keynote grid. | Delivered 2025-07-11 at Bass Coast, `role: "workshop-lead"`, public recording `owtSPcpRinI`. Only Set E lists it. |
| Power, Taste, and Trust | **Retire the title, fold the content into Authored Judgment.** Then delete the card from `wp-payloads/speaking.html` (line 183) so it cannot be re-applied. | Same thesis, third name, zero delivery record. It was live until 2026-07-24 and the payload that put it there is still tracked. |
| Leadership After the AI Point of No Return | **Retire.** Same cleanup: delete the card at `wp-payloads/speaking.html` line 174. | Zero delivery record and zero kk-kb hits, but it was a live `<h3>` on `/speaking/` until 2026-07-24. Retiring the title is not enough on its own; the payload has to go too. |

## What is still missing, whichever set wins

- **No testimonial in the bank is attributed to a specific talk.** `content/source-packs/keynotes-2026/testimonial-bank.md` has four approved quotes and not one names a keynote. Acceptance criterion 3 on #638 asks for video + photo + testimonial per talk. Video and photo are covered for the top two. Testimonials are not, for any of the eleven. Someone has to go get named quotes from the CreativeMornings and LaSalle rooms. **This acceptance criterion is not met and I am not marking it met.**
- **Both Hands Full has no owned photo from WAIFF São Paulo** that I could find in the repo or the KB. The only stage photo in play is LaSalle.
- **Developing an AI Mindset has no video and no stage photo.**
- **WAIFF date precision is approximate.** The appearance record says the exact festival day is pending the WAIFF program. If the page prints a date, print February 2026, not February 26.

## Blast radius

Whatever KK picks drives all of these, and several of them are already written against Set C:

- `content/drafts/2026-07-26-speaking-page/payload-body.html` hardcodes the Set C four (Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI). Any other outcome means reworking this file before apply.
- `content/drafts/2026-07-26-speaking-page/multimedia-rebuild-plan.md` and `video-set.md` assign media per talk.
- Live WP page 1887 body, which is a single `wp:html` pack, so the whole thing gets replaced at once.
- Page schema and internal links. Right now the grid links out to two third-party portals plus one internal page. Changing the set changes the internal link graph and any per-talk structured data.
- The topic-bank source of truth at `content/source-packs/keynotes-2026/talk-topic-bank.md`, which should be rewritten to match the decision rather than left as a competing version.
- **`content/source-packs/keynotes-2026/wp-payloads/speaking.html`. This one was missing from the first pass of this doc and it is the most dangerous file in the list.** It is tracked on `main`, last touched 2026-06-16 (`1fa1999`), and it still contains the full six-card Set D grid at lines 138-183, including apply-ready cards for the two retired titles with live "Ask about this talk" contact links. If anyone applies this payload, the two titles KK is about to retire go straight back onto `/speaking/`. Whatever KK decides, this file has to be brought into line or explicitly marked historical.
- **`content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md` (Set E)**, which carries a third name for Authored Judgment and the only listing of Dear AI. Same treatment: reconcile or banner as historical.
- `backup/20260701T193335Z-content-architecture/page-snapshots/page-1887-speaking-before.html` is the readback proof that Set D was live. Leave it alone. It is evidence, not a source to sync.
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
*Recommend: Yes, and this one changed after verification. The first pass told you these were harmless shelf titles with zero sources. Wrong. Both were `<h3>` cards under "Signature keynote topics" on `kriskrug.co/speaking/` until the 2026-07-24 rewrite (`page-1887-speaking-before.html` lines 318 and 327, `modified: 2026-06-28`), and the payload that put them there is still tracked at `wp-payloads/speaking.html` lines 174 and 183 with live "Ask about this talk" links. Neither has a delivery record of any kind. So the honest question is not "retire a title," it is: were these ever pitched off that page, and is retiring them a correction to something a booker already saw? Retiring the title alone does not close it. The payload cards have to be deleted too, or the next apply puts them back.*

**D7b. New, and it needs your memory not mine.** While those two cards were live, did anyone book off them, or ask about them? If yes, that changes retire into replace, and one of them needs a real 2026 delivery rather than a deletion.
Yes / No / Do not remember.
*No recommendation. I have no way to check this.*

**D8. Move Compost AI to the workshop menu instead of the keynote grid?**
Yes / No.
*Recommend: Yes, unless you actually delivered it at Bass Coast in July 2026. I found no record either way. If it ran, tell me and I will file the appearance record and re-tier it.*

**D8b. New. Add "Dear AI: We Need to Talk About Your Soul" to the workshop menu with its video?**
Yes / No.
*Recommend: Yes. It is a `status: "delivered"` record (Bass Coast 2025-07-11, `role: "workshop-lead"`) with a public recording at `https://www.youtube.com/watch?v=owtSPcpRinI`, and that video was already embedded on the prior live speaking page. Only Set E lists it as a topic. Four of the six sets forgot it exists. It is the only real receipt available for the workshop line.*

**D9. Adopt the rule "a talk enters the keynote grid only with a named venue and date, or an explicit new-for-2026 label"?**
Yes / No.
*Recommend: Yes. Six sets is what happens without it. And note the rule has to bite on the payload files too, not just the live page, or the seventh set is already sitting in `wp-payloads/`.*

**D10. After you rule, rewrite `content/source-packs/keynotes-2026/talk-topic-bank.md` to match, and leave a pointer in the two kk-kb drafts?**
Yes / No.
*Recommend: Yes, and widen it. The first pass named two files. It should be four: `talk-topic-bank.md` (Set A), `notion/keynotes-sanitized-snapshot.md` (Set E), `wp-payloads/speaking.html` (Set D, the apply-ready one), and pointers into the two kk-kb drafts (Sets B and B2). Otherwise the losing sets stay live in the repo and the next agent picks one at random.*

**Open question, not a decision:** do named testimonials exist from the CreativeMornings Vancouver or LaSalle rooms? None are in the testimonial bank. If they exist in your inbox or DMs, that closes the last real gap in the proof stack for the top two talks.

---

## Correction log, 2026-08-02

This doc was audited after the first pass and six defects were found. All six are answered here. Nothing was quietly dropped.

| # | Charge | Disposition |
|---|---|---|
| 1 | Sections 9, 10 and table rows 9, 10 claimed "zero hits anywhere outside the topic bank" and "exists in exactly one place." False in this repo. | **Corrected.** Both sections rewritten with the real greps. `point of no return`: 28 files in kriskrug-wp, 4 of them live source. `Power, Taste`: 29 files, 3 live source. kk-kb half of the claim was true (0 hits) and is now stated as scoped rather than absolute. Table rows 9 and 10 rewritten. |
| 2 | Missed the prior live set in `backup/20260701T193335Z-content-architecture/page-snapshots/page-1887-speaking-before.html`, which lists six signature keynote topics. | **Corrected.** Added as Set D with line-level citations (h2 at 275, six h3 at 282/291/300/309/318/327, next h2 at 336, `modified: 2026-06-28T14:14:01`). Its still-tracked repo source `wp-payloads/speaking.html` lines 138-183 is now the top item in Blast radius. D7 rewritten around it. |
| 3 | Missed `content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md` as a fifth independent set, including the delivered talk "Dear AI." | **Corrected.** Added as Set E with a full alias map. "Dear AI" added as inventory row 11 with its own detail section, plus new decision D8b. Correctly graded as a delivered *workshop* (`role: "workshop-lead"`), not a keynote. |
| 4 | Headline framing "the issue named three sets, there are four" is now wrong. | **Corrected.** Recounted to six (A, B, B2, C, D, E) in the title, the intro, the set table, the tier summary, and D9. |
| 5 | Section 6 grep count for "Real AI Advantage" was wrong. Verifier counts 15 files. | **Corrected.** Re-ran it: 15 files. Itemized as 8 concept-folder, 3 index, 4 outside. Same defect found and fixed in section 5: "Authored Judgment" is 10 files, not 8, and 2 of those are false positives on the phrase rather than the title. The zero-appearance-record conclusion held in both cases and is now backed by a second check against every `talk_title` in the appearance records. |
| 6 | Comparison-table row 1 credited Both Hands Full at LaSalle with no caveat, though that record's `talk_title` is "How are creatives working with AI?" | **Corrected.** Caveat moved into the table row itself and expanded in section 1. Table now reads "Yes, once under this title" and credits WAIFF as the `talk_title` match. |
| 7 | Set B2 cited as "lines 45-54"; the table is not at those lines. | **Corrected, and the verifier's replacement number was also off.** Verified: section heading line 45, table header 47-48, four talk rows 49-52, source note line 54. The verifier proposed 45-52; the table starts at 47. Citation now spells out all three spans. |

One thing the first pass got right and this pass keeps: **live page 1887 ships the Responsible AI cohort certification as a signature keynote card**, wearing the only human-on-a-stage photograph on the page, which is a Both Hands Full photo. Re-verified by GET on 2026-08-02. See section 4.
