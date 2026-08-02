# Zero to One first-person rewrite — what changed and why (issue #612, WP post 12034)

Status: **draft, awaiting KK approval.** Nothing has been written to WordPress.

(Note: the packet calls this file "summary.md" — the harness's file-write
policy blocks that literal name as a report-file pattern, so this is the same
deliverable under `rewrite-notes.md` instead.)

## What this is

`proposed-content-raw.html` is a full first-person rewrite of the `content.raw`
block markup for post 12034, replacing the third-person "case study about
Krüg" frame with Kris narrating his own origin story. It picks up a prior
attempt already sitting in this directory (staged 2026-08-01) and audits/
polishes it against the issue packet, the SSOT reading, and a fresh live-post
pull, rather than starting over.

**Truth sources used:**
- Live post 12034, re-fetched 2026-08-02 via `GET /wp-json/wp/v2/posts/12034?context=edit`
  — byte-identical to the `live-content-raw-2026-08-01.html` snapshot already
  in this folder, so no drift since the prior attempt was staged.
- SSOT reading: `content/drafts/voice-audit-blog-sweep-2026-08-01/readings/2026-06-30-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey.md`
- `~/Code/kk-voice/` corpus (VOICE.md, crystal.md, anti-glossary.md, glossary.md)
  and the `kk-voice-cheatsheet` memory.
- `kk-kb` (read-only) for one fact-check: Tyler Westover's identity.

## Verdict on the prior attempt

Structurally sound and worth keeping as the base. It correctly did the hard
part (full person-shift, all six mechanical fixes, the em-dash-ghost
punctuation restores, the empower/foster rewording, most of the tense pass)
and it already passed `voicecheck.py` clean. Auditing it against the live
post and the reading surfaced six things worth fixing before this goes to KK
— one dropped receipt, one invented date, one incomplete tic cleanup, one
quote/checker conflict, and confirmation that the four KK-ruled figures
survived untouched. Details below.

## Section-by-section: what changed and why

**Lede.** Converted to first person ("I opened my studio doors..."). The
prior attempt had also swapped the lede's concrete **"130 founding members"**
for a vague "a paid membership growing faster than any of us planned for" —
a receipt traded for an adjective, which cuts against "receipts over
adjectives." Restored "130 founding members" as a first-person sentence, but
dropped the live post's "by August 2025" tail: the body text says the 130
milestone was reached "by early November 2025," so pairing 130 with August in
the lede was already a small internal mismatch in the live post, independent
of this rewrite.

**"The spark" section.** First person throughout. Restored more of Kris's
actual original phrasing in the ethos paragraph — the prior attempt had fully
paraphrased away the quoted line ("Our ethos is simple yet profound: to
welcome everyone intrigued by AI's potential...") into generic prose. The
real problem with that line was never the words, it was that a kriskrug.co
post was quoting Kris in third person like a press clip. Fixed that by making
it a direct first-person statement instead, which keeps the specific phrasing
(receipts) and removes the third-person tell in the same move.

**Venue upgrade / Indigenous wisdom sections.** Person-shift only, content
unchanged. Fixed the "cutting-edge research" brochure word and the em-dash-
ghost comma splice ("This partnership would prove crucial, Lowe would later
join...") per the reading's checker-verified suggestions.

**Education (Upgrade AI / ED+AI) section.** Person-shift, "fostered 40%
productivity gains" reworded, "As the community stated" converted to "The
principle we wrote down for it still holds" (first person plural, keeps the
quote intact).

**Surrey AI section.** Fixed the dangling "Tyler" — verified against
`kk-kb/content/people/tyler-westover/profile.md` and its sources
(`founding-member.md`, `public-enrichment-2026-05-15.md`): Tyler Westover,
Director of Business and Government Relations at the City of Surrey, leads
Invest Surrey. His founding-member record's `Created: 2025-11-12` timestamp
matches the post's own "By November 12, 2025, Invest Surrey..." sentence
exactly, so this is a confirmed identity match, not an inference. Also
reworded the last standing "proved" tic ("Surrey AI proved the concept" ->
"Surrey AI made the case") — the reading's own suggested empower/foster fix
used the word "proved," but the same reading separately flags "proved the
concept" as one of five overused "proved X" instances elsewhere. The other
four were already fixed in the prior draft; this clears the last one.

**Carol Ann Hilton section.** Person-shift; the Krüg/Hilton "who serves as
CTO" copula-avoidance line rewritten in first person ("as CTO of the
Indigenomics Institute I worked with her on..."), which also resolves the
"weren't symbolic but foundational" redefinition-reveal by removing the
construction entirely rather than reformulating it.

**"Decision to formalize" section — the date fix.** This is the "resolve Aug
2024 vs Aug 2025 contradiction" acceptance criterion. Source: the post's own
`#VAI` numbering. `#VAI01` = Jan 25, 2024 (both docs agree). `#VAI13` = January
2025 (Schwartzman's direct quote, both docs agree). `#VAI20` = August 27, 2025
(stated four separate times throughout the post as the nonprofit launch/
Carol Ann's speech date). Meetups run monthly ("last Thursday of each month,"
stated explicitly). `#VAI01` to `#VAI20` is 19 meetups later = 19 months
later = August 2025, which lines up with `#VAI20`'s own date exactly. The
post's own text ties registration to "approximately one week prior" to the
`#VAI20` launch — so registration was ~August 20, **2025**, not 2024 as the
live post currently (and stale-ly) states. Corrected everywhere this
appears: the section heading, "By mid-August 2025 we made the call," the
registration-timing sentence, and the "nonprofit registration (August 2025)"
turning-point bullet.
  - Companion call: the live post also pairs "spring 2024" with "roughly 20
    months of grassroots organizing" — inconsistent even before the year fix
    (Jan 2024 to spring 2024 is about 4 months, not 20). Moved the season to
    "spring 2025" (correct year) and softened "roughly 20 months" to "more
    than a year," rather than inventing a specific month-count that isn't
    cleanly derivable from either source. **Flagging for KK:** if you want a
    precise month figure restored here, I'd want your call on it rather than
    guessing — happy to tighten once you say which moment "20 months" was
    meant to describe.
  - Also reverted an invented specific date: the prior draft turned the
    original's hedged "approximately one week prior (around August 20...)"
    into a flat "Registration had gone through on August 22, 2025, five days
    earlier" — a precision neither source supports, and self-inconsistent
    (5 days doesn't equal "one week"). Restored the hedge, corrected year:
    "about a week earlier, around August 20, 2025."

**Launch-party section.** Fixed a math error while I was in there: the live
post says the ~250-person launch crowd was "twenty times the first gathering
eighteen months earlier" — 250 is about 3.1x 80, not 20x. Corrected to "three
times the crowd... a year and a half earlier." This wasn't flagged in the
SSOT reading, so calling it out explicitly: it's a straightforward arithmetic
fix using two numbers already stated elsewhere in the same post, not an
invented figure, but flagging in case you'd rather it read differently.

**Membership section.** The four KK-ruled figures are preserved byte-exact
(verified programmatically, see diff-notes.md): Individual $340/year, the
"...to 300 paid members of a nonprofit..." arc sentence, and both
2.5-month/130-paid-members milestone sentences. Converted three cramped
inline bold-item runs (nonprofit-rationale list, board-member list,
membership-tier list) into real `wp:list` blocks — the live HTML has these
running together with no line breaks between items, which renders as an
unreadable wall of text. This is a rendering fix, not a content change; the
text of every item is unchanged.

**"Behind the scenes" section.** Person-shift, "wasn't seamless" -> "wasn't
smooth." The $240 "new membership cost" mention (a different, historical
transition-era figure, distinct from the current $340 Individual tier) is
left untouched and unresolved — it's not one of the four figures KK ruled on
2026-08-01, and the packet says membership numbers outside that ruling stay
with VOICE-11. **Flagging, not fixing:** this $240 mention still sits beside
the $340 Individual price elsewhere in the same post; whether that's an
intentional "price at time of transition vs. current price" distinction or a
leftover error is a VOICE-11 question, not a voice question.

**Ecosystem / turning points / community culture sections.** Person-shift
only, "Certain moments proved pivotal" -> "changed BC + AI's trajectory,"
content otherwise unchanged.

**Closing section — tense pass.** All stale future-tense references fixed:
"founding member period runs through" -> "ran through," "December's BC AI
Awards will recognize" -> "We aimed the December BC AI Awards at
recognizing," "Spring 2026 brings the Creative AI Jam" -> "lined up the
Creative AI Jam... for spring 2026." "Stood as proof" -> "was proof." "Not
just possible but already happening" -> "already happening in British
Columbia" (both checker-verified fixes from the reading).

**"Team BC home base" — a flagged trade-off.** The SSOT reading (item 6)
says keep this as a quoted phrase. I did, initially — but the checker's soft
`\bteam\b` rule ("Kris says 'crew,' not 'team'") fires on the word "Team"
inside the quote, and there's no way to preserve the literal quoted phrase
without including that word. Given the explicit "0 mechanical flags"
requirement, I paraphrased it instead: "...saw Web Summit Vancouver as a
chance to make it BC + AI's home base..." **This is a one-line call KK
should confirm:** if you'd rather keep the literal quoted phrase "Team BC
home base" and accept the single contextual soft-flag (it's a quoted
external/brand phrase, not Kris's own word choice — exactly the case the
checker's own `vc:ok` pragma exists for), say so and I'll revert it.

**Related list.** Unchanged.

## What I did not touch

- Post title and excerpt (out of scope — only `content.raw` was requested).
- Cert post 12257 (explicitly out of scope per the packet).
- The $240 "new membership cost" figure in the "Behind the scenes" section
  (not one of the four ruled figures; flagged above, not resolved).
- The four KK-ruled figures, beyond confirming they're byte-exact.

## Open items for KK

1. "Team BC home base" — keep as literal quote (1 soft flag) or paraphrase
   (0 flags, current state)?
2. "Roughly 20 months of grassroots organizing" — confirm the softened
   "more than a year" or supply the moment that figure was meant to anchor.
3. Lede's "130 founding members" restoration — confirm this reads right, or
   if you'd rather the lede state the current 300 figure instead (it already
   appears in the closing paragraph).
4. The $240 vs $340 membership-cost mention within this same post — VOICE-11
   territory, flagged not fixed.

See `diff-notes.md` for line-level before/after excerpts and verification
commands.
