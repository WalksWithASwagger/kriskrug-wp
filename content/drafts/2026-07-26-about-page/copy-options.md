# Copy options - kill / rewrite "public trail" (#418)

**Rule:** drafted replacements use no em dashes.  
**Live today:** kicker `Public trail` + H3 `A two-decade public trail` (count = 2).  
**Goal:** approved copy uses the phrase **at most once**, preferably **zero**.

## Option A - Recommended: drop the phrase entirely

Keeps the receipt-y voice without the hiking metaphor.

| Slot | Current | Proposed |
|---|---|---|
| Section kicker | Public trail | Receipts |
| Card 1 H3 | A two-decade public trail | Two decades in public rooms |
| Card 1 body | (unchanged) | National Geographic, CBC, Rolling Stone-adjacent rooms, TEDxOilSpill, Midway Journey, SXSW, the Olympics, and many smaller rooms that mattered just as much. |
| Card 3 body (optional polish) | …and leave a trail than inflate… | …and leave receipts than inflate a bio until it floats away. |

**Why recommend:** Matches KK ("weird way to talk about it") and hard-fails the double. Zero occurrences after apply. "Receipts" already appears as a card title, so the section kicker reinforces an existing frame instead of inventing a new metaphor.

**Post-apply grep expectation:** `grep -ci 'public trail'` → `0`

## Option B - Keep the idea once, only in the kicker

| Slot | Proposed |
|---|---|
| Section kicker | Public trail |
| Card 1 H3 | Two decades of rooms |
| Card 1 body | unchanged |

**Post-apply grep expectation:** `1`  
**Downside:** keeps the phrase KK called weird.

## Option C - Keep the idea once, only in the H3

| Slot | Proposed |
|---|---|
| Section kicker | Proof |
| Card 1 H3 | A two-decade public trail |
| Card 1 body | unchanged |

**Post-apply grep expectation:** `1`  
**Downside:** same phrasing objection; kicker "Proof" is colder than KK voice.

## Option D - Softer rewrite, still zero "trail"

| Slot | Proposed |
|---|---|
| Section kicker | On the record |
| Card 1 H3 | Twenty years of receipts |
| Card 3 body | I would rather show the work, name the collaborators, and leave receipts than inflate a bio until it floats away. |

**Post-apply grep expectation:** `0`

## Options explicitly not drafted

- Synonyms that still say "trail" twice (path / track / trail mix).  
- Long bio rewrites beyond this section.  
- Restoring Beastie Boys / gallery modules (separate decision).

## KK picker

- [ ] **A (recommended)** - kicker `Receipts`, H3 `Two decades in public rooms`, optional card-3 "leave receipts"  
- [ ] B - keep kicker only  
- [ ] C - keep H3 only  
- [ ] D - `On the record` / `Twenty years of receipts`  
- [ ] Custom: _______________________
