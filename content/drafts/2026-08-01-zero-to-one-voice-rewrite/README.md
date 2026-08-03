# Zero to One first-person rewrite (issue #612, WP post 12034)

**Status: draft only. Nothing has been written to WordPress. Live apply is gated on KK approval.**

Live target: WP post **12034**,
https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/

## Files in this directory

| File | What it is |
|---|---|
| `rewritten-body.md` | The full new post body in readable markdown. **Read this one.** |
| `proposed-content-raw.html` | The same body as WordPress block markup. This is what would ship as `content.raw`. |
| `diff-notes.md` | Paragraph-by-paragraph person shift, plus the mechanical, tense, and date tables. |
| `rewrite-notes.md` | Longer section-by-section rationale from the first pass on this draft. |
| `live-content-raw-2026-08-01.html` | Snapshot of live `content.raw`, unchanged. The rollback reference. |
| `README.md` | This file. |

`rewritten-body.md` and `proposed-content-raw.html` are kept in lockstep. Verified programmatically:
after stripping markup from both, the text is line-for-line identical (110 blocks each). If one
changes, change the other.

## The problem this fixes

The live post is a third-person case study about "Krüg" published under Kris's own byline. It reads
like a research report someone else wrote. On top of that it narrates from a November 2025 vantage
point while carrying a June 30, 2026 publish date, so it uses future tense about things that already
happened, and it contradicts itself on when the nonprofit registered.

The receipts underneath are excellent. The frame was the thing that was wrong. So this is a person
shift and a fact pass, not a rewrite of the reporting.

## What changed

1. **Frame: third person to first person, throughout.** "When Kris Krüg opened the doors" becomes
   "when I opened the doors." "As Krüg stated" becomes Kris saying the thing directly. "Hilton's work
   with Krüg (who serves as CTO of Indigenomics Institute)" becomes "as CTO of the Indigenomics
   Institute I worked with her on." Full map in `diff-notes.md`.
2. **Tense: stale future tense removed.** "The founding member period runs through December 31, 2025"
   becomes "ran through." "December's BC AI Awards will recognize" becomes "We aimed the December BC
   AI Awards at recognizing." "Spring 2026 brings the Creative AI Jam" becomes "lined up the Creative
   AI Jam for spring 2026."
3. **Dates: the August 2024 / August 2025 contradiction resolved.** See the next section for which
   date won and why.
4. **Six mechanical hard-rule hits fixed:** `seamless`, `cutting-edge`, `pivotal`, the
   "no X, no Y, just Z" cadence, the dangling first-name "Tyler," and the "Team BC home base" quote.
5. **Two arithmetic and internal-consistency fixes** the voice audit did not catch. Both flagged
   below rather than buried.
6. **Three broken inline lists rebuilt as real `wp:list` blocks.** The live HTML runs the
   nonprofit-rationale items, the board-member items, and the membership tiers together in single
   paragraphs with no separators, which renders as a wall of text. Item text is unchanged. This is a
   rendering fix.
7. **Redefinition-reveal tics thinned.** The audit counted roughly eight "this wasn't X but Y"
   constructions and five "proved X" instances. Both are now at zero.

## The date contradiction, and which date I treated as correct

The live post says three incompatible things about when BC + AI registered as a nonprofit:

- Section heading and body: **August 2024** ("By mid-August 2024, the decision was made")
- Lede: nonprofit status **by August 2025**
- Launch section: registration happened "approximately one week prior" to the August 27, **2025**
  launch, and then gives that week-earlier date as "around August 20, **2024**"

That last sentence contradicts itself inside its own parentheses. One week before August 27, 2025 is
August 20, 2025, not August 20, 2024.

**I treated August 2025 as correct.** The evidence is the post's own meetup numbering, which is
internally consistent everywhere it appears:

- `#VAI01` = January 25, 2024 (stated twice)
- `#VAI13` = January 2025 (inside Matthew Schwartzman's direct quote)
- `#VAI20` = August 27, 2025 (stated four separate times as the launch date)
- Meetups are monthly, "the last Thursday of each month" (stated explicitly)

`#VAI01` to `#VAI20` is nineteen monthly meetups, which is nineteen months. January 2024 plus
nineteen months is August 2025. That lands exactly on `#VAI20`'s own stated date, and `#VAI13` in
January 2025 falls exactly where it should on the same line. The numbering is self-consistent and it
only works with an August 2025 registration. The "2024" is a year typo that propagated through one
section.

Corrected in four places: the section heading, "By mid-August 2025 we made the call," the
registration-timing sentence, and the "nonprofit registration (August 2025)" turning point.

Two companion date problems in the same section:

- **"By spring 2024, after roughly 20 months of grassroots organizing."** Wrong on both halves. The
  community launched January 2024, so spring 2024 is about four months in, not twenty. Moved to
  spring 2025 (correct year, consistent with a summer 2025 decision and an August 2025 registration)
  and softened "roughly 20 months" to "more than a year," which is what a January 2024 start actually
  supports. I did not invent a replacement month count. Flagged for KK below.
- **"Twenty times the first gathering eighteen months earlier."** 250 people is roughly three times
  80, not twenty times. Corrected to "three times the crowd from the first studio night a year and a
  half earlier." Both numbers were already stated elsewhere in the same post. This one was not in the
  voice audit, so it is called out rather than slipped in.

## Facts preserved

Verified programmatically against the live snapshot: **zero numbers, zero named people or
organizations, and zero calendar dates were dropped.** The only date that changed is
`August 20, 2024`, which is the contradiction above.

Every name the audit praised is intact and still carries its specific contribution: Gabriel George Sr.
(Tsleil-Waututh Nation, Eagle Song, grandson of Chief Dan George), Carol Ann Hilton (Indigenomics
Institute, board), Lorraine Lowe (H.R. MacMillan Space Centre, board), Matthew Schwartzman (19, Maple
Ridge, Surrey AI), Ryv Valiquette (White Rock), Sev Geraskin ("Hot Dogma"), Peter Bittner (The Upgrade
AI, Seattle), Jos Duncan-Asé (Philadelphia), Mark Busse (Creative Mornings Vancouver), Mike Klassen
(Vancouver City Councillor), and Tyler Westover (Invest Surrey).

Numbers intact: 80 people at 290 W. 3rd Avenue, 135+ by #VAI05, 250 at the launch, 34 signups the
first night, 130 paid members in 2.5 months, 50 members/month, $2,500 hackathon prizes, $10,000 from
Rival Technologies, $15,000+ from MetaCreation Lab, 1,000+ trained, 50+ workshops, 92% / 88% / 95% /
40%, 40% underrepresented participants, 30% RISE co-funding, 15,000+ contacts, $450 legacy ticket,
$200 transition offer, 480 organizations, 200+ funding programs, 1,001 survey respondents, the
35/25/20/10 demographic split, all five membership tier prices, and the three BC women on the national
AI Task Force.

**KK's 2026-08-01 membership rulings from #615 are preserved byte-exact:** Individual `$340/year`, the
`300 paid members` arc sentence, and both `130 paid members` / 2.5-month milestone sentences, which
stay as time-stamped history per that ruling's instruction 3.

## The one change I made on top of the earlier pass

The lede said "130 founding members" with no date attached, while the closing paragraph says "300 paid
members." A reader hits both and asks which it is. Rather than overwrite either figure, I time-stamped
the lede: "130 founding members **by that November**." That is KK's own instruction 3 from #615
(time-stamp the historical figure) applied to the one place it had not been. It keeps the receipt,
resolves the apparent contradiction, and invents nothing.

One-line revert if KK disagrees: drop "by that November" from the lede paragraph in both
`rewritten-body.md` and `proposed-content-raw.html`.

## Gate results

```
python3 ~/Code/kk-voice/scripts/voicecheck.py rewritten-body.md
  -> OK: sounds like Kris (0 flags), exit 0

python3 ~/Code/kk-voice/scripts/voicecheck.py <stripped proposed-content-raw.html>
  -> OK: sounds like Kris (0 flags), exit 0
```

Also verified by direct search against `proposed-content-raw.html`:

| Check | Result |
|---|---|
| Em dashes | 0 |
| `Krüg stated` / `As Krüg` / `serves as CTO` | 0 |
| `proved <word>` tic | 0 |
| `seamless` / `cutting-edge` / `pivotal` / `empower*` / `foster*` / `landscape` / `unprecedented` | 0 |
| `not just X but Y` / `wasn't just` / `not only` | 0 |
| Numbers, names, dates dropped vs live | 0 (except the corrected `August 20, 2024`) |
| Markdown body vs block markup text | identical, 110 blocks each |

## Open items for KK

1. **"Team BC home base."** The audit says keep it as a quoted brand phrase. But the word "Team" sits
   inside the quote and trips the checker's soft `team` rule, and the acceptance criteria ask for a
   clean run. It is currently paraphrased to "a chance to make it BC + AI's home base." Say the word
   and it goes back to the literal quote with one accepted contextual flag.
2. **"Roughly 20 months of grassroots organizing"** is softened to "more than a year" rather than
   replaced with a guessed figure. If you know which moment that count was anchored to, it can be made
   precise.
3. **The lede's time-stamped "130 founding members by that November."** Confirm, or say you would
   rather the lede lead with the current 300.
4. **The `$240` "new membership cost" sentence** in the behind-the-scenes section still sits in the
   same post as the `$340` Individual tier. That is a historical transition-era figure, it was not one
   of the four figures ruled on in #615, and it is left untouched. Flagged, not fixed. That is a
   numbers question, not a voice question.
5. **"Twenty times" to "three times."** Arithmetic fix found outside the audit. Confirm the phrasing.

## What was not touched

- Post title, slug, excerpt, featured image, categories, tags. Only `content.raw` is in scope.
- Cert post **12257**. Explicitly out of scope.
- The live site. No REST writes were made or attempted from this lane.

## If KK approves, the apply path

Not executed here. For whoever runs it:

1. Re-pull `GET /wp-json/wp/v2/posts/12034?context=edit` and diff against
   `live-content-raw-2026-08-01.html`. If it drifted, stop and re-reconcile.
2. Write that fresh pull to a rollback file before any PATCH.
3. PATCH `content` with `proposed-content-raw.html`, verifying the ID is 12034 and the slug matches
   before the write.
4. Purge Pagely page cache, then verify logged out with a cache-bypass query string. First rendered
   paragraph should open in first person.
5. Post the live opening paragraph back on issue #612.
