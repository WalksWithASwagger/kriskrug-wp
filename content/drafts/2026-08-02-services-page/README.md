# Services page rethink, issue #420

**Status:** draft only. No live write, no deploy.
**Measured:** 2026-08-02. **Payload:** 2026-08-17 `payload-body.html` is the apply-ready body (cream rail, four offers, no image plane).
**Live URL:** `GET /services/` returns 301 to `/generative-ai-services/` (200). WP page ID 2666.
**Evidence:** `evidence/height-before-after-2026-08-02.json`, `pack-proposed.html`

KK's teardown verdict, 2026-07-17:

> The language is weak and the boxes are weak. There's a lot of scroll. The stylesheet's fucked up. This page needs a rethinking from the ground up.

## First: nothing has shipped since the last audit

The live page body and its inline stylesheet are byte-identical to the snapshot taken on 2026-07-26 for the earlier #420 package (`content/drafts/2026-07-26-services-page/`). Same 4,418 byte inline `<style>`, same 237 words of copy. That package was correct and it was never applied. This one supersedes it with a measured before/after and an apply-ready HTML payload.

## What is on the page right now

Four sections inside one custom HTML block (`.kk-services-2026`), under the theme's own H1 block:

| # | Section | Words | Height at 1440 |
|---|---|---:|---:|
| 1 | Hero (kicker, display H2, two lead paragraphs) | 67 | 449 |
| 2 | How I can help (4 ribbon cards) | 89 | 426 |
| 3 | Proof in motion (2 photo cards) | 40 | 532 |
| 4 | Start here (CTA card) | 41 | 297 |
| | **Total pack** | **237** | **1819** |

Seven boxed surfaces total: 4 offer cards, 2 proof cards, 1 CTA card. Two images. Three links in the whole page.

## Problem 1: the page is the site's money page and it is the weakest one

`/services/` is linked three times from site chrome: the nav item **Services**, the header's primary CTA **Work with me** (that CTA was pointed here by #422), and a **Work with me** link in the footer. Every route into "hire this person" lands here.

## Problem 2: it repeats three other pages and adds nothing

Compared against the live text of `/speaking/`, `/work/`, and `/contact/`:

| Services offer | Already covered, better, on |
|---|---|
| AI strategy | `/speaking/` "Executive briefings", `/contact/` "Plan strategy or training" |
| Training and workshops | `/speaking/` "Workshops", `/contact/` "Book a talk or workshop" |
| Community systems | `/work/` "BC + AI Ecosystem", `/contact/` "Community collaborations" |
| Keynotes and briefings | `/speaking/` "Keynotes", `/work/` "AI keynotes" |

Four of four. The Services page does not describe a single offer that another page does not already describe in more concrete language. `/speaking/` says "rooms with too many acronyms" and "without hype theatre". `/contact/` says "A short brief beats a vague hello". Services says "sensemaking" and "creative courage".

Four pages also end with four differently worded versions of the same instruction:

- `/services/`: "Book an AI strategy session" then "Start a conversation"
- `/speaking/`: "Book Kris for a keynote" then "Start a booking conversation"
- `/work/`: "Bring this work into your room" then "Talk about a project"
- `/contact/`: "Email Kris" then "Send the note"

## Problem 3: it repeats itself inside its own first screen

Three titles stack before any content: the theme H1 "Generative AI Creative Services & Strategy", the kicker "AI services", and the display H2 "AI strategy for people who still care about culture". Three ways to say "services" in the first 180 vertical pixels.

Then the hero lead says the work is "part strategy, part training, part sensemaking, and part creative courage". The four cards 30 pixels below it are AI strategy, Training and workshops, Community systems, Keynotes and briefings. The lead paragraph is a table of contents for the grid directly underneath it.

"AI" appears 11 times in 237 words, 4.6 percent of every word on the page.

## Problem 4: the boxes fail the issue's own acceptance test

Acceptance says every service block must state what it is, who it is for, and what to do next.

| Card | What | Who | Next |
|---|---|---|---|
| I. AI strategy | yes | no | no |
| II. Training and workshops | yes | no | no |
| III. Community systems | yes | no | no |
| IV. Keynotes and briefings | yes | no | no |

Zero of four offer cards contain a link. The card's top slot, which is already styled and already costs vertical space, holds a roman numeral. `I.` `II.` `III.` `IV.` carry no information. That slot is the fix, and it is free.

## Problem 5: the scroll, measured

Playwright Chromium headless, logged out, light scheme, reduced motion, scroll-settle pass, 2026-08-02.

| Viewport | Document | Entry content | `.kk-services-2026` | Theme footer |
|---|---:|---:|---:|---:|
| 1440 x 900 | 3737 | 1860 | 1819 | 1384 |
| 768 x 900 | 4812 | 2758 | 2716 | 1651 |
| 375 x 812 | 5326 | 2644 | 2602 | 2344 |

Two things fall out of this.

**The offers are below the fold.** At 1440 x 900 the first offer card starts at y=935. The viewport ends at 900. On the page the whole site points at, you cannot see a single thing you can hire him for without scrolling. At 375 the first card starts at y=941 against an 812 tall viewport.

**A third of the scroll is not this page's.** The theme footer is 1384px at 1440 and 2344px at 375, for 105 words. That is 37 percent of the desktop document and 44 percent of the mobile document. The page body cannot be held responsible for it and this lane cannot fix it. See "Where the acceptance criterion needs a ruling" below.

## Problem 6: the stylesheet, specifically

Not fixed here. #423 owns it and has an open draft PR. Recorded so that lane has the receipts:

1. **Proof cards render bold by accident.** The whole proof card is an `<a>`, and `.kk-services-2026 a:not(.kk-services-button) { font-weight: 700 }` therefore applies to the card's `h3` and `p`. Both proof blurbs render at weight 700. Visible in the 1440 before capture.
2. **Two stacked horizontal rules under "START HERE".** The previous section's 1px bottom border sits directly above `.kk-services-cta`'s own 2px accent `border-top`, which is clipped to `max-width: 40rem`. The result is a full-width hairline, a gap, then a short orange line.
3. **Eight `!important` declarations to undo the theme.** `.kk-services-2026 :where(p, li)::first-letter` overrides `initial-letter`, `font-size`, `font-weight`, `float`, `margin`, `line-height`, `color`, and `background`, all `!important`, purely to cancel a drop cap the theme applies to prose. Plus `max-width: 72rem` to escape the `aurora-prose` measure. This block is the page fighting the theme, which is the exact condition #423 exists to end.

`AURORA-STYLESHEET-REBUILD-PLAN.md` already lists this inline block for step 7 deletion. Nothing in this package adds CSS, so it survives that deletion as long as the class names get theme-side homes.

## The structural fix

**Services stops competing with `/speaking/` and `/work/` and becomes the routing layer.**

It is the page every CTA points at, so it should do what a front door does: name the four things you can buy, say who each is for, and send you one click deeper. The detail already exists elsewhere and is better written there. Restating it here is what produced both the filler language and the extra scroll.

That single decision does most of the work:

- The "Proof in motion" section disappears, because proof becomes the link target of each offer card. That is 532px at 1440 and 1175px at 768.
- The offer cards gain "who" and "next" by putting the audience in the slot currently holding a roman numeral and putting the link inline at the end of the blurb. Zero new CSS, zero added height.
- The hero drops to one lead and pulls the CTA button up, because it no longer has to summarize what the cards below already say.

## Result, measured the same way

Prototyped by replacing `.kk-services-2026` innerHTML on the live page with `pack-proposed.html` and re-measuring. Same stylesheet, same fonts, same theme chrome, same run conditions.

| Viewport | Scope | Before | After | Change |
|---|---|---:|---:|---:|
| 1440 | entry content | 1860 | 1184 | **-36.3%** |
| 1440 | pack | 1819 | 1143 | **-37.2%** |
| 1440 | full document | 3737 | 3061 | -18.1% |
| 768 | pack | 2716 | 1293 | **-52.4%** |
| 768 | full document | 4812 | 3389 | -29.6% |
| 375 | pack | 2602 | 1716 | **-34.1%** |
| 375 | full document | 5326 | 4440 | -16.6% |

The first offer card moves from y=935 to y=799 at 1440, which puts it above the 900px fold. At 375 it moves from y=941 to y=700, above the 812px fold.

Word count barely moves, 237 to 223. The height comes out of stacked blocks and an image plane, not out of deleted sentences. That matters: the page did not get thinner, it got denser.

## Where the acceptance criterion needs a ruling

The issue says "Total page height reduced by at least a third at 1440". Measured against the whole document that is 3737 down to 2491, a cut of 1246px. The entire page body is 1819px and the footer alone is 1384px. Hitting it would mean deleting 68 percent of everything this page owns, footer untouched.

Recommendation: score acceptance on **entry content at 1440**, where this proposal delivers 36.3 percent. Then file the footer separately. 1384px of chrome at 1440 and 2344px at 375, for 105 words, is a site-wide problem that shows up on every page, and it is theme territory, not Track A. I have not touched it.

## Decision gates for KK

1. **Pricing.** There is no published price anywhere on kriskrug.co. The only pricing language on the site is `/contact/` asking for a "budget range if you have one", and `docs/current-state/marketing/community-advocate-program-v1-2026-06-17.md` explicitly forbids pricing promises without your approval. So the draft states how quoting works and asks for a range. It invents no numbers. If you want a floor published instead, say the number and I will swap the paragraph.
2. **Receipts.** The draft names only BC + AI and Futureproof, both already public in the site footer and on `/work/`. Venue names exist in repo drafts (Web Summit Vancouver, ChannelNEXT, LaSalle College, Bass Coast, SFU SIAT, Whistler Institute) but I could not confirm they are publicly claimed on the live site, so I left them out. Adding two or three would make the cards stronger. Your call which.
3. **The two photos get deleted.** The BC + AI network graph and the Both Hands Full stage shot come off this page. Both still live on `/work/` and `/speaking/`, which is where the cards now point. Confirm you are fine losing the image plane here, since it is the single largest scroll item.
4. **H1 and the title tag.** Proposed H1 is "AI keynotes, training, and strategy" in place of "Generative AI Creative Services & Strategy". Separately, the live `<title>` is `Generative AI Creative Services & Strategy &mdash; Kris Krug | AI Keynote Speaker & Creative Technologist`. That contains an em dash. It comes from the site-wide title pattern, not this page's body, so I did not touch it, but it is a standing-rule violation on a public string and somebody should own it.

## What this package does not do

No CSS. No theme files. No live write. No deploy. The layout depends on three existing class behaviours that #423 must preserve or rehome: `.kk-services-kicker` (now carries the audience line), `.kk-services-ribbon-card::before` (the colour ribbon), and `.kk-services-button`. Details in `layout-proposal.md`.

## Files

- `copy-draft.md`: the rewritten copy, block by block, with the voice notes
- `layout-proposal.md`: section order, the four height mechanisms, before/after counts, the #423 handoff
- `pack-proposed.html`: inner-HTML fragment from the 2026-08-02 measure pass
- `payload-body.html`: **apply-ready** WP `content.raw` body (2026-08-17). Cream rail, four offers, no image plane, no live write.
- `evidence/height-before-after-2026-08-02.json`: raw measurements, both variants, three viewports

## Apply gates, when KK approves

1. Snapshot page 2666 before any write, slug-verified.
2. Dry run first. `/services/` must still 301 to `/generative-ai-services/`.
3. Non-ASCII goes in as numeric character references. The DB is latin1 and REST writes corrupt raw codepoints, so "Krüg" must be written as an entity. See the latin1 note in repo memory.
4. Purge Pagely page cache and confirm the render logged out. REST edits do not auto-purge.
5. Capture 375, 768, 1440 after the purge and record the real document heights against this file's numbers.
6. Confirm the six links return 200 logged out: `/speaking/`, `/work/`, `/contact/` (x2 buttons, x2 card links).
