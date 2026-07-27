# Optional draft body snippets (#290)

Draft only. Not apply-ready as a full page body. Graft into the post-#418 About pack after KK edits.

**Voice notes:** match live About (short, receipt-y, concrete). No em dashes. Prefer "I" statements over resume stacks.

**Base assumption:** sections use existing classes from the content-architecture pack (`aurora-proof-section`, `aurora-section-kicker`, `aurora-card`, etc.).

---

## M1 + M2 - Pilot school origin beat (must-have candidate)

Insert as its own section after Receipts, before CTA.

```html
<section class="aurora-proof-section">
  <p class="aurora-section-kicker">Origin beat</p>
  <h2 class="aurora-display-heading">Flying in the direction of my dreams</h2>
  <p class="aurora-page-lead">In 2013 I went to flight school in Helena, Montana, trained at Vetter Aviation, and earned my Private Pilot License.</p>
  <p>It started as a long-held kid dream that a conversation with Richard Branson nudged back into motion. Flying still feels like a complementary skill to photography: another way to change altitude, reframe the ground, and take decisive action on something you have wanted for decades. I wrote that chapter down at the time in <a href="/2013/09/14/pilot-school-flying-in-the-direction-of-my-dreams/">Pilot School: Flying in the Direction of My Dreams</a>.</p>
</section>
```

**Shorter alternate (if KK wants less section chrome):** one paragraph appended to the Lead section instead of a new block.

```html
<p>In 2013 I earned a Private Pilot License in Helena, Montana, after deciding a decades-old dream was worth chasing in public. Flying still sits beside photography for me: another craft for changing altitude and paying attention. <a href="/2013/09/14/pilot-school-flying-in-the-direction-of-my-dreams/">The 2013 note is here</a>.</p>
```

---

## O1 - Aerial bridge (optional add-on to M1)

Append inside the pilot section:

```html
<p>A couple of years later that license met the camera again through aerial and drone work. The throughline was simple: the luck of being alive when flying and making photos could intersect.</p>
```

Optional receipt link: `/2015/09/08/aerial-photography-combining-my-loves-for-flying-and-making-photos/`

---

## M3 - TEDxOilSpill enrichment (Receipts card 1)

Post-#418 card 1 title assumed: `Two decades in public rooms`.

**Current live body (approx):**  
National Geographic, CBC, Rolling Stone-adjacent rooms, TEDxOilSpill, Midway Journey, SXSW, the Olympics, and many smaller rooms that mattered just as much.

**Proposed enrichment (still one paragraph):**

```html
<p>National Geographic, CBC, Rolling Stone-adjacent rooms, leading a Static Photography team to the Gulf for TEDxOilSpill in 2010, Midway Journey, SXSW, the Olympics, and many smaller rooms that mattered just as much.</p>
```

Keep the list scannable. Do not turn the card into a Gulf essay (that belongs in the archive series post).

---

## M4 - Vancouver AI → BC+AI (Lead clause)

Add as the closing clause of Lead paragraph 2, or as a third short paragraph:

```html
<p>What began as the Vancouver AI Community Meetup in 2023 is now the BC+AI ecosystem: grassroots rooms, literacy, and infrastructure across the province.</p>
```

If Rooms BC+AI blurb is preferred instead of Lead:

```html
<p>From the Vancouver AI Community Meetup to a province-wide BC+AI ecosystem: literacy, events, and community infrastructure built in public.</p>
```

---

## M5 + M6 - Bryght + Northern Voice (one sentence)

Prefer a single compact sentence so early-web history does not dominate:

```html
<p>Before the camera and the AI rooms, I co-founded Bryght, an early Drupal / Web 2.0 company, and co-organized Northern Voice, Canada's pioneering blogging conference.</p>
```

Placement options:

1. New one-line paragraph in Lead after the capacity question, **or**
2. Prefix inside Receipts card 1 before the outlet list.

**Caution:** do not quote Richard Eriksson's "My Two Years at Bryght" as first-person Kris copy.

---

## O2 / O3 - COP15 + PopTech (optional list polish)

Only if KK wants denser receipts and accepts a longer card:

```html
<p>National Geographic, CBC, Rolling Stone-adjacent rooms, accredited photojournalism at COP15 in Copenhagen (2009), PopTech in Camden, TEDxOilSpill in the Gulf (2010), Midway Journey, SXSW, the Olympics, and many smaller rooms that mattered just as much.</p>
```

---

## O5 - BitTorrent line (gated; off by default)

Do **not** ship until KK confirms cover credit wording.

```html
<!-- GATED: confirm co-author vs contributor before use
<p>I co-authored <cite>BitTorrent For Dummies</cite> (Wiley, 2005) with Susannah Gardner.</p>
-->
```

---

## O6 - Land & values (optional About-body #22)

Only if KK wants page-local acknowledgment beyond the footer. Place after origin beat, before CTA.

```html
<section class="aurora-proof-section">
  <p class="aurora-section-kicker">Land &amp; values</p>
  <h2 class="aurora-display-heading">Work on unceded land</h2>
  <p>This work happens on the traditional, ancestral, and unceded territories of the Coast Salish peoples of the Musqueam, Squamish, and Tsleil-Waututh Nations. Indigenous sovereignty is not an add-on to the bio. It is part of how I think about community, technology, and futures.</p>
  <p><a class="aurora-button" href="/reconciliation-indigenous-land-acknowledgement/">Read the full land acknowledgment</a></p>
</section>
```

Shorter Lead-clause alternate:

```html
<p>I live and work on the traditional, ancestral, and unceded territories of the Musqueam, Squamish, and Tsleil-Waututh Nations. <a href="/reconciliation-indigenous-land-acknowledgement/">Reconciliation notes are here</a>.</p>
```

---

## Short author bio (separate lane; do not About-PATCH)

Current theme string:

```text
Kris Krug is an AI keynote speaker, creative technologist, photographer, and community builder working across BC + AI, Vancouver AI, and Futureproof Festival, and a living network of AI-era projects.
```

Optional #269 append for a later theme edit:

```text
Kris Krug is an AI keynote speaker, creative technologist, photographer, community builder, and licensed private pilot working across BC + AI, Vancouver AI, and Futureproof Festival, and a living network of AI-era projects.
```

---

## Suggested minimal first ship (if KK wants one tight pass)

1. M1 short alternate **or** full origin section + M2 link  
2. M3 TEDxOilSpill enrichment in Receipts card 1  
3. M4 Vancouver AI → BC+AI clause  
4. M5+M6 one-sentence early-web line  
5. Skip O1 through O5 and O6 unless KK checks them on

Then run `checklist.md` against a single HTML built on the #418 base from PR #504.
