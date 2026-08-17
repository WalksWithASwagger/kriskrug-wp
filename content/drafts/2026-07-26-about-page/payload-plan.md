# Payload plan - About page unify (#418)

**Mode:** DRAFT ONLY. Do not PATCH live WP from this package without KK approval + authenticated snapshot.
**Target:** page ID `1208`, slug `about`, URL https://kriskrug.co/about/
**Recommended copy:** Option A from `copy-options.md` (zero "public trail")
**Apply-ready body:** `payload-body.html`
**2026-08-17 revision:** one cream system, one 860px rail, rooms restyled as panel cards so the dark media-card scrim is gone.

## Goals (acceptance criteria)

1. One consistent background treatment, or an intentional documented palette of at most 2.
2. All content columns share one grid; widths consistent section to section.
3. "Public trail" appears at most once in approved copy, or not at all.

## Background system (documented palette of 2)

| Token | Value | Use |
|---|---|---|
| `--kk-about-paper` | `#efe6d2` | Page / section canvas (matches site paper) |
| `--kk-about-panel` | `#e6dcc2` | Every card: rooms, receipts, CTA |

No navy band. No third gray island. No dark photo scrim. Room images sit on top of the same panel the receipt cards use, so text is always ink on cream.

Contrast (sRGB relative luminance):

| Pair | Ratio |
|---|---|
| `#171310` on `#efe6d2` | 14.88:1 |
| `#171310` on `#e6dcc2` | 13.53:1 |
| `#3d342c` on `#e6dcc2` | 8.4:1 |

All AA.

## Column grid

Page-scoped under `.kk-r9-pack`:

- `--kk-about-max: 860px` matches the WP content constraint on this template
- Every `.aurora-proof-section` uses that max and zero extra inline pad
- Rooms and receipts share `repeat(2, minmax(0, 1fr))` with the same gap
- CTA uses `aurora-proof-grid--cta` so it spans the same rail
- At `max-width: 720px`, grids collapse to one column

## Copy change (Option A)

- Kicker: `Public trail` → `Receipts`
- H3: `A two-decade public trail` → `Two decades in public rooms`
- Card 3 body: `leave a trail` → `leave receipts`
- Lead name: `Kris Krug` → `Kris Krüg`
- Ecosystem label stays `BC + AI`

`grep -ci 'public trail'` on this payload is **0**.

## What stays intact

- Lead section H2 and the two-decade question
- Four rooms (BC + AI, keynotes, visual storytelling, creative AI systems) with the same destinations and images
- Remaining three proof cards (Community / Receipts over adjectives / Human capacity)
- CTA heading, body, `/contact/` button
- Pack marker `<!-- content-architecture-2026:about -->`
- Wrapper `kk-page kk-r9-pack`

Live `/about/` on 2026-07-26 (and still on 2026-08-17) does not contain Beastie Boys cards or the old gallery roster. Those lived in the pre-content-architecture overhaul. This edit does not restore them and does not delete anything that is on the live page today except the double "public trail" framing and the dark media-card scrim.

Out of scope: theme file edits; title field; homepage lanes #411 to #416.

## Apply procedure (after KK approval)

1. Confirm secrets: `WP_USER` + `WP_APP_PASSWORD` present (length check only).
2. Authenticated GET page `1208`; write `backup/<timestamp>-about-418/page-1208-before.json` + rendered HTML.
3. Dry-run: print payload bytes, section kickers, `public trail` count in payload (expect 0).
4. KK signs the copy + screenshots plan.
5. Body-only REST update (`content` raw = `payload-body.html`). Do not send `title`.
6. Purge Pagely page cache for `/about/`.
7. Logged-out verification (checklist below).
8. If bad: restore snapshot `content.raw`.

## Verification checklist

### Acceptance

- [ ] Palette of 2: paper + panel. No navy, no dark scrim.
- [ ] Rooms, receipts, and CTA share the same max-width rail; 2-col grids align.
- [ ] `public trail` appears 0 times in the payload.

### Evals

- [ ] `grep -ci 'public trail'` on the payload → `0`
- [ ] After a future apply: `curl -sL https://kriskrug.co/about/ | grep -ci 'public trail'` → `0`
- [ ] Text contrast AA on paper and panel
- [ ] Rooms cards, proof cards, CTA, and `/contact/` still present
- [ ] Zero em dashes. Brand: Kris Krüg, BC + AI

### Safety

- [ ] Pre-edit snapshot under `backup/`
- [ ] Pagely purge after write
- [ ] Logged-out smoke
- [ ] Rollback path documented
- [ ] No live write from this draft package without KK sign-off
