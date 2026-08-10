# Join BC / Futureproof copy options (#411)

Voice: Plain. Specific. No em dashes. No "rooms." No trust-layer / frontier / operating-conditions fog.
Mechanical: zero em-dash characters (U+2014) in all options below.

**Recommended default:** Option B for both sections.

The work band card copy overlaps with #412 (Creative Labs). Those options are
mirrored here for completeness; pick one set and both issues close on the same
edit.

---

## Work band cards (lines 68-111 in front-page.html)

### Live (before)

| # | Title | One-line |
|---|---|---|
| 01 | BC + AI | Province-wide trust layer for responsible AI: meetups, certification, policy rooms, and practical adoption. |
| 02 | Futureproof | Pacific Northwest gathering where frontier tech, creative practice, and civic trust share one public room. |
| 03 | Keynotes 2026 | Stage sessions on taste, human agency, and the operating conditions for responsible AI. |

Problems: "trust layer," "policy rooms," "share one public room," "operating conditions." All fog.

### Option A  -  verbs

| # | Title | One-line | Door |
|---|---|---|---|
| 01 | BC + AI | The British Columbia community for people who actually ship AI with each other. | Join → |
| 02 | Futureproof | Pacific Northwest festival where tech, art, and civic practice share one floor. | Attend → |
| 03 | Keynotes 2026 | Stage talks on taste, agency, and what still belongs to humans. | Book → |

### Option B  -  plainest (RECOMMENDED)

| # | Title | One-line | Door |
|---|---|---|---|
| 01 | BC + AI | Meetups, certification, and policy work across BC. Come for the people. | bc-ai.ca |
| 02 | Futureproof | Annual festival in the Pacific Northwest. Frontier tools, creative practice, public trust. | futureproof.website |
| 03 | Keynotes | I speak on AI, creativity, and human agency. 140+ stages since 2004. Booking 2026. | /speaking/ |

Note on Option B lab 02: "Frontier tools" is concrete (tools), not "frontier tech" fog. If KK hates "frontier," swap to: `Annual PNW festival for builders, artists, and the people writing the rules.`

### Option C  -  first person

| # | Title | One-line | Door |
|---|---|---|---|
| 01 | BC + AI | I help run the province-wide network. Meetups to certification to policy. | Join the network |
| 02 | Futureproof | I curate the festival. Come if you want the real conversation, not the demo reel. | See the festival |
| 03 | Keynotes 2026 | Hire me for the stage session your audience actually needs. | Speaking |

---

## Services section (lines 113-146 in front-page.html)

### Live (before)

| Card | Body copy |
|---|---|
| Keynote | Plain-English stage sessions on AI, taste, and human agency. Custom-scoped for creative, civic, and executive rooms. |
| Workshop | Hands-on sessions for creative teams and leadership offsites. Everyone leaves having built something they can use Monday. |
| Ecosystem | Community infrastructure, sponsorship strategy, and public rooms where BC's AI practice actually meets. |

Problems: "executive rooms" and "public rooms" in two of three cards. "Custom-scoped" is corporate-speak.

### Option A  -  concrete and plain

| Card | Body copy |
|---|---|
| Keynote | Plain-English talks on AI, taste, and human agency. Built for creative, civic, and corporate audiences. |
| Workshop | Hands-on sessions for creative teams and leadership offsites. Everyone leaves with something they can use Monday. |
| Ecosystem | Community infrastructure, sponsorship strategy, and the spaces where BC's AI practice actually meets. |

### Option B  -  first person, no jargon (RECOMMENDED)

| Card | Body copy |
|---|---|
| Keynote | I talk about AI, taste, and human agency in plain English. Creative, civic, and corporate audiences. |
| Workshop | I run hands-on sessions for creative teams and leadership offsites. You leave with something you can use Monday. |
| Ecosystem | I build the infrastructure: community, sponsorship, and the spaces where BC's AI people actually meet. |

### Option C  -  shortest

| Card | Body copy |
|---|---|
| Keynote | Talks on AI, taste, and human agency. For creative, civic, and corporate audiences. |
| Workshop | Hands-on sessions. Your team leaves with something built. |
| Ecosystem | Community infrastructure and sponsorship for BC's AI practice. |

---

## Banned / watch list

Do not ship:

- rooms that need clarity / courage (KK's original callout)
- trust layer, operating conditions, civic trust share one public room (live fog)
- "custom-scoped" (corporate-speak)
- em dashes
- "Field notes" / "dispatch" (newsletter lane; keep out of this band)

Canonical spellings: **BC + AI** (spaces), **Futureproof** (one word), Kris Krug when the full name appears.

---

## CSS fixes already shipped in this branch

- [x] Drop cap retired (done in 1.5.9, `typography-refined.css:141`)
- [x] Alignment: removed `margin-top: -2.5rem` on 2nd work card; all 3 cards now share the same grid baseline
- [x] Focus states: added `:focus-within` to `.aurora-work-card` (mirrors hover image effect + outline ring)
- [x] Service card hover: added `translateY(-2px)` lift on `:hover` / `:focus-within`
- [x] Service card link hover: added color shift + underline on `:hover` / `:focus-visible`

## Pick note for KK

1. Choose work band option A/B/C (matches #412 pick).
2. Choose services option A/B/C.
3. Confirm door labels: verbs ("Join") or naked URLs/paths.
4. After KK picks, the template edit is a single content commit.
