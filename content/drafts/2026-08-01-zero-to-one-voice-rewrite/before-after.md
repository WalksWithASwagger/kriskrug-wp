# Before / after: voice-critical passages (post 12034)

Live quotes are from public REST `content.rendered` fetched 2026-08-16
(`live-content-rendered-2026-08-16.html`; post `modified` 2026-08-01T18:44:59).
Proposed quotes are from `proposed-content-raw.html`.

**Membership ruling (KK, #615, 2026-08-01):** publish **$340/year** and **300 members** as the current figures. Recast historical 130 / $240 lines rather than leave them sitting next to the current numbers.

The May 24 local package at
`content/drafts/2026-05-24-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/`
is **stale**. It is still third person, still prices Individual at $240/year, and
still closes on 130 paid members. Live is already a later rewrite of that source
(Individual $340, closer 300). This payload starts from live, not from May 24.

No `{EMDASH}` characters in live body or in the proposed copy.

## Opening

| Live (third person) | Proposed (first person) |
|---|---|
| **BC + AI transformed from an 80-person studio gathering into British Columbia's largest grassroots AI ecosystem in under two years**, registering as a nonprofit with Indigenous board leadership, 130 founding members, and multiple regional chapters by August 2025. This is the story of how ceremony, community, and careful optimism built something unprecedented in Canada's AI landscape. | **In January 2024 I opened my studio doors for a meetup and 80 people showed up.** Less than two years later, BC + AI was British Columbia's largest grassroots AI ecosystem: a registered nonprofit with Indigenous board leadership, 300 members, and regional chapters across the province. This is the story of how we built something Canada had not seen before. Receipts included. |

## Third-person "Kris" narration (must be gone)

| Live | Proposed |
|---|---|
| when **Kris Krüg opened the doors** of MØTLEYKRÜG Media headquarters | when **I opened the doors** of MØTLEYKRÜG Media |
| **As Krüg stated:** "Our ethos is simple yet profound: to welcome everyone intrigued by AI's potential..." | **My ethos was simple: welcome everyone intrigued by AI's potential**, from seasoned researchers to budding artists, from tech enthusiasts to curious students. Nobody pitched. Nobody recruited. People taught each other. |
| **Hilton's work with Krüg (who serves as CTO of Indigenomics Institute)** produced the indigenomics.ai platform | **as CTO of the Indigenomics Institute I worked with her** on the indigenomics.ai platform |
| **Kris Krüg** - founder and community organizer (board list) | **Kris Krüg (me):** founder and community organizer |

`rg -n "Krüg stated|As Krüg|serves as CTO"` on the proposed payload → 0.

The board-list "Kris Krüg (me)" is the only remaining name hit. It is a roster
line, not narration.

## Membership figures

| Site | Live | Proposed |
|---|---|---|
| Lede | 130 founding members | 300 members |
| Launch / growth | the association had enrolled **130 paid members**, an average of 50 members per month | Membership now sits at **300**. (34 first-night signups kept as a receipt. Did not invent "300 in 2.5 months.") |
| Individual tier | Individual: $340/year | Individual: $340/year (unchanged; already correct) |
| Core AI conversion | The new membership cost just **$240 annually** | The new membership cost **$340/year** |
| Turning points | **Reaching 130 paid members** within 2.5 months | **Reaching 300 paid members** |
| Closer | From 80 people in a studio to **300 paid members** | From 80 people in a studio to **300 paid members** (unchanged; already correct) |

`$200` in the Core AI paragraph stays as the one-time conversion offer to existing
$450 ticket holders. It is not the list price.
