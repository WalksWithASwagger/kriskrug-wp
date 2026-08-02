# Diff notes: notable line-level before/after (live -> proposed)

Companion to `rewrite-notes.md`. Live = `live-content-raw-2026-08-01.html`
(re-verified byte-identical to a fresh 2026-08-02 API pull). Proposed =
`proposed-content-raw.html`.

## Person shift (representative sample; applies throughout)

- Live: `when Kris Krüg opened the doors of MØTLEYKRÜG Media headquarters`
  Proposed: `when I opened the doors of MØTLEYKRÜG Media`

- Live: `As Krüg stated: "Our ethos is simple yet profound: to welcome
  everyone intrigued by AI's potential. From seasoned researchers to budding
  artists, from tech enthusiasts to curious students."`
  Proposed: `My ethos was simple: welcome everyone intrigued by AI's
  potential, from seasoned researchers to budding artists, from tech
  enthusiasts to curious students.`

- Live: `Hilton's work with Krüg (who serves as CTO of Indigenomics
  Institute) produced the indigenomics.ai platform`
  Proposed: `Carol Ann and I also built together: as CTO of the Indigenomics
  Institute I worked with her on the indigenomics.ai platform`

- Live: `Kris Krüg - founder and community organizer` (board list)
  Proposed: `Kris Krüg (me): founder and community organizer` (list item)

## Mechanical (hard-rule) fixes

| # | Live | Proposed |
|---|---|---|
| 1 | `The nonprofit formation wasn't seamless.` | `The nonprofit formation wasn't smooth.` |
| 2 | `remained connected to cutting-edge research` | `kept BC + AI connected to the research frontier` |
| 3 | `Certain moments proved pivotal in BC + AI's evolution:` | `Certain moments changed BC + AI's trajectory:` |
| 4 | `No pitches, no pyramid schemes, just genuine peer-to-peer learning.` | `Nobody pitched. Nobody recruited. People taught each other.` |
| 5 | `Tyler and his team saw Surrey AI as essential infrastructure` | `Tyler Westover, who leads Invest Surrey as the City of Surrey's Director of Business and Government Relations, saw Surrey AI as essential infrastructure` |
| 6 | `offers opportunity for BC + AI to be "Team BC home base"` | `saw Web Summit Vancouver as a chance to make it BC + AI's home base` (quote dropped — see rewrite-notes.md "flagged trade-off") |

## Judgment-call fixes (checker-verified in the reading)

| Live | Proposed |
|---|---|
| `built something unprecedented in Canada's AI landscape` | `built something Canada had not seen before` |
| `By November 2025, BC + AI stood as proof that grassroots organizing could build...` | `By November 2025, BC + AI was proof that grassroots organizing could build...` |
| `proving that another way of building AI's future is not just possible but already happening in British Columbia` | `Another way of building AI's future is already happening in British Columbia.` |
| `The event sold out immediately, 80 people packed into a studio space...` | `The event sold out immediately: 80 people packed into my studio at 290 W. 3rd Avenue...` |
| `This partnership would prove crucial, Lowe would later join the nonprofit board, cementing the institutional relationship.` | `The partnership stuck: Lorraine later joined the nonprofit board.` |
| `empowering young leaders` / `fostered 40% average productivity gains` | `Young leaders ran it, local needs shaped it...` / `graduates reported average productivity gains of 40%` |

## Tense pass (all stale future tense -> past)

| Live | Proposed |
|---|---|
| `The founding member period runs through December 31, 2025` | `The founding member period ran through December 31, 2025` |
| `December's BC AI Awards will recognize British Columbia's AI innovators...` | `We aimed the December BC AI Awards at recognizing British Columbia's AI innovators...` |
| `Spring 2026 brings the Creative AI Jam with Creative Mornings Vancouver.` | `lined up the Creative AI Jam with Creative Mornings for spring 2026` |

## Date-contradiction fix (Aug 2024 -> Aug 2025), with source

Source for the correction: the post's own `#VAI` meetup numbering.
`#VAI01` = Jan 25, 2024. `#VAI13` = January 2025 (Schwartzman's direct
quote). `#VAI20` = August 27, 2025 (stated 4x in the post). Meetups are
monthly. `#VAI01` -> `#VAI20` = 19 months = August 2025, matching `#VAI20`'s
own stated date. Registration is described as "approximately one week
prior" to `#VAI20`, so registration is ~August 20, 2025, not 2024.

| Live | Proposed |
|---|---|
| Heading: `The decision to formalize: nonprofit status in August 2024` | `The decision to formalize: nonprofit status in August 2025` |
| `By spring 2024, after roughly 20 months of grassroots organizing...` | `By spring 2025, after more than a year of grassroots organizing...` (see rewrite-notes.md for why "20 months" was softened rather than corrected to a specific number) |
| `The debate played out in planning meetings through early summer 2024.` | `The debate ran through planning meetings into early summer 2025.` |
| `By mid-August 2024, the decision was made.` | `By mid-August 2025 we made the call.` |
| `Registration had occurred approximately one week prior (around August 20, 2024)` | `Registration had gone through about a week earlier, around August 20, 2025` |
| `The nonprofit registration (August 2024) enabled sustainable operations...` | `The nonprofit registration (August 2025) opened up sustainable operations...` |

## Arithmetic fix (not in the SSOT reading; found independently)

| Live | Proposed |
|---|---|
| `Approximately 250 people filled the Space Centre planetarium on August 27, 2025, twenty times the first gathering eighteen months earlier.` | `Approximately 250 people filled the Space Centre planetarium on August 27, 2025, three times the crowd from the first studio night a year and a half earlier.` |

250 / 80 ≈ 3.1x, not 20x. "A year and a half" (18 months) matches the live
post's own figure and is unchanged.

## Protected figures — confirmed byte-exact (KK's 2026-08-01 rulings)

Verified with direct string search against both files; all four present
verbatim in the proposed draft:

1. `Individual</strong>: $340/year (1 seat for freelancers and independent practitioners)`
2. `From 80 people in a studio to 300 paid members of a nonprofit with regional chapters, Indigenous board leadership, and national recognition`
3. `by early November 2025), the association had enrolled <strong>130 paid members</strong>, an average of 50 members per month`
4. `Reaching 130 paid members</strong> within 2.5 months validated the membership model`

## Structural fix: broken inline lists -> real wp:list blocks

Live has three places where multiple bolded items run together in a single
`<p>` with no separators (renders as an unreadable wall of text), e.g.:

```
<p><strong>Credibility for funding</strong>: Government grants and corporate
sponsorships required formal entities<strong>Collective voice</strong>:
Aggregate community power for policy advocacy<strong>Sustainable
operations</strong>: Move beyond "duct tape and vibes"...</p>
```

Proposed converts these to `wp:list` / `wp:list-item` blocks (rationale-for-
nonprofit list, board-member list, membership-tier list). Text of every item
is unchanged; only the markup structure changed, matching the "keep valid
WordPress block markup" requirement.

## Fact-check performed (not a text change, a verification)

"Tyler" (live, no surname/title) -> confirmed as Tyler Westover against
`kk-kb/content/people/tyler-westover/profile.md`: Director, Business and
Government Relations, City of Surrey / Invest Surrey. His founding-member
record (`kk-kb/content/people/tyler-westover/sources/founding-member.md`)
shows `Created: 2025-11-12T10:15:00`, which matches the live post's own
"By November 12, 2025, Invest Surrey... had committed to joining BC + AI"
sentence exactly — confirms this is the same person and event, not a guess.

## Verification commands run

```
# WP block markup balance (open/close tag pairing)
python3 -c "... parses <!-- wp:X --> / <!-- /wp:X --> pairs, confirms empty stack"

# Third-person tells
rg -n "Krüg stated|As Krüg|serves as CTO" proposed-content-raw.html   # 0 matches

# Em dashes
rg -n "—" proposed-content-raw.html   # 0 matches

# Full anti-glossary sweep (landscape, testament, tapestry, delve, realm,
# robust, myriad, plethora, boasts, utilize, harness, garner, glean, "not
# just X but Y", "no X no Y just Z", soft-flag "team", "when it comes to",
# "cannot be overstated", "studies show")   # all 0 matches

# voicecheck.py on stripped text (WP block comments + HTML tags removed)
python3 ~/Code/kk-voice/scripts/voicecheck.py stripped.txt
# -> OK: sounds like Kris (0 flags), exit code 0
```
