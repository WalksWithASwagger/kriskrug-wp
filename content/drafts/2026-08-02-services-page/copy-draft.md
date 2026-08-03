# Services page copy draft, issue #420

**Status:** draft for KK approval. Not applied.
**Date:** 2026-08-02
**Target:** WP page 2666, `/generative-ai-services/`, served at `/services/`
**Em dashes:** 0. Verified by character scan of this file and of `pack-proposed.html`.

Rendered form is `pack-proposed.html`. This file is the copy plus the reasoning, so you can rule on wording without reading markup.

---

## Page title

**H1:** AI keynotes, training, and strategy

Replaces "Generative AI Creative Services & Strategy". Same keywords, no word salad, and it stops being the third thing on the screen that says "services".

Note: the `<title>` tag is separate and currently reads `Generative AI Creative Services & Strategy &mdash; Kris Krug | AI Keynote Speaker & Creative Technologist`. It has an em dash in it. It comes from the site-wide title pattern, not this page body, so it is flagged in the README rather than changed here.

---

## 1. Open

> # I get hired for four things.
>
> Talks, team training, strategy work, and building AI communities that actually meet. Pick the one you need, or send me the room and I will tell you what fits.
>
> **[ EMAIL KRIS ]** → `/contact/`

**Why this and not the current version.**

The live headline is "AI strategy for people who still care about culture." It is a mood. It does not tell a conference organizer with a budget and a date that they are on the right page. "I get hired for four things" does, and it sets up the grid directly below it so the lead paragraph no longer has to.

Killed from the live hero, with the reason:

| Phrase now live | Why it goes |
|---|---|
| still care about culture | vibe, not an offer |
| move from AI pressure to practical fluency | nobody has ever said "practical fluency" out loud |
| part strategy, part training, part sensemaking, and part creative courage | a table of contents for the four cards 30px below it |
| This is not generic prompt-hacking | defining yourself by what you are not |
| hands-on capacity building | NGO grant language |
| without surrendering judgment, taste, responsibility, or trust | four abstract nouns in a row |
| I help organizations, creative teams, schools, civic groups, and community builders | five audiences in one breath means none of them |

The audiences did not disappear. They moved into the cards, where each one sits next to the specific thing that audience buys.

---

## 2. The four offers

Each card is audience line, name, what it is, and where to go next. The audience line goes in the slot that currently holds a roman numeral.

### Card 1

> `CONFERENCES, FESTIVALS, OFFSITES`
>
> ### Keynote talks
>
> A 30 to 60 minute talk built for your room, with live demos and work from this month, not a stock deck from last year. [Topics and formats](/speaking/)

### Card 2

> `NEWSROOMS, STUDIOS, FACULTY, PUBLIC SECTOR`
>
> ### Team training
>
> Your people build real workflows in their own tools and leave with something they use the next day. Half day, full day, or a cohort. [Book a workshop](/contact/)

### Card 3

> `LEADERSHIP TEAMS, BOARDS, FUNDERS`
>
> ### Strategy and briefings
>
> I read how your team actually works, then tell you where AI helps, where it will embarrass you, and what to do first. Written down, so somebody can act on it. [Start a briefing](/contact/)

### Card 4

> `CITIES, ASSOCIATIONS, FESTIVALS`
>
> ### Community and ecosystem work
>
> The rooms, programs, and publishing loops that turn scattered people into a working AI community. BC + AI and Futureproof are this. [See the ecosystem work](/work/)

**Why these four and in this order.**

Same four offers as today, renamed to what a buyer would type into an email. Ordered by how often each one is the reason somebody arrives: talks first, training second, strategy third, ecosystem work fourth. The live order leads with "AI strategy", which is the hardest one to buy cold.

Two deliberate word choices worth defending:

- "where it will embarrass you" in card 3. It is the only line on the page that says something a consultant would not say, and it is the reason card 3 sounds like a person. If it goes, card 3 goes back to being beige.
- "not a stock deck from last year" in card 1. Every keynote buyer has been burned by one. Naming it does more work than any adjective would.

Card 4 names BC + AI and Futureproof because both are already public in the site footer and on `/work/`. No unverified receipts. See README decision gate 2 if you want venue names added.

---

## 3. How to start

> ## How to start
>
> Send the audience, the date, the format, and a budget range if you have one. A short brief beats a vague hello. Everything is quoted: talks price on room size, travel, and prep, training on how many people and how many sessions.
>
> **[ EMAIL KRIS ]** → `/contact/`

**Why this replaces "Book an AI strategy session".**

The live CTA is "Book an AI strategy session", which is one of the four offers wearing the hat of all four. Somebody who wants a keynote reads that and wonders if they are in the wrong place. "How to start" covers everything above it.

"A short brief beats a vague hello" is lifted verbatim from `/contact/`. It is already yours, it is the best line on that page, and repeating it here is deliberate: it is the one thing worth saying twice because it changes what lands in the inbox.

**On pricing.** No number is published anywhere on kriskrug.co today. The only pricing-adjacent language on the live site is `/contact/` asking for a "budget range if you have one", and the marketing docs forbid pricing promises without your sign-off. So this paragraph says how quoting works and invents nothing. It gives a buyer the two variables that actually move the number, which is more than "start a conversation" gives them.

If you want a floor published instead, the swap is one sentence:

> Everything is quoted. Talks start at $X, training at $Y per day. Tell me your range and I will tell you straight away whether it works.

Your number, your call.

---

## What got deleted

| Section | Reason |
|---|---|
| "AI services" kicker | The H1 directly above it already says services |
| Second hero paragraph | Defined the work by what it is not |
| Roman numerals I, II, III, IV | Zero information in a slot that costs vertical space |
| "Proof in motion" section, both photo cards | Proof moved into the cards as links to `/work/` and `/speaking/`, where the same images already live |
| "Book an AI strategy session" heading | One offer standing in for four |

## Counts, before and after

| | Live | Draft |
|---|---:|---:|
| Words in the block | 237 | 223 |
| Sections | 4 | 3 |
| Boxed surfaces | 7 | 5 |
| Images | 2 | 0 |
| Links | 3 | 6 |
| Offer cards with an audience | 0 of 4 | 4 of 4 |
| Offer cards with a next step | 0 of 4 | 4 of 4 |
| Uses of "AI" | 11 | 4 |
| Em dashes | 0 | 0 |

Roughly the same word count, 37 percent less height at 1440. The page did not get shorter by saying less. It got shorter by stopping the repetition and dropping the image plane.

## Voice check

Scanned and absent: unlock, delve, leverage, empower, journey, landscape, robust, seamless, holistic, synergy, elevate, fluency, sensemaking, capacity, courage. No "it's not just X, it's Y". No three-adjective stacks. The noun lists that remain are audiences and variables, which are load bearing.

Run `voice-slop-audit` against `pack-proposed.html` before apply.
