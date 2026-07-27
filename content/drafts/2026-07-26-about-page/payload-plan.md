# Payload plan - About page unify (#418)

**Mode:** DRAFT ONLY. Do not PATCH live WP from this package without KK approval + authenticated snapshot.  
**Target:** page ID `1208`, slug `about`, URL https://kriskrug.co/about/  
**Recommended copy:** Option A from `copy-options.md`  
**Apply-ready body:** `payload-body.html`

## Goals (acceptance criteria)

1. One consistent background treatment, or an intentional documented palette of at most 2.  
2. All content columns share one grid; widths consistent section to section.  
3. "Public trail" appears at most once in approved copy, or not at all.

## Background system (documented palette of 2)

| Token | Value | Use |
|---|---|---|
| `--kk-about-paper` | `#efe6d2` | Page / section canvas (matches site paper) |
| `--kk-about-panel` | `#e6dcc2` | Text cards + CTA card surface |

**Second treatment (intentional):** rooms media cards keep photo + dark scrim, but page-scoped CSS forces **light ink on the scrim** so "text on black" is readable and owned, not accidental dark-on-dark.

No navy band. No third gray island. Buttons stay ink/signal on the cream system.

## Column grid

Page-scoped under `.kk-r9-pack`:

```css
.kk-r9-pack {
  --kk-about-max: 860px; /* match WP content constraint on this template */
  --kk-about-gap: 1rem;
}
.kk-r9-pack .aurora-proof-section {
  max-width: var(--kk-about-max);
  margin-inline: auto;
  padding-inline: 0; /* avoid double pad with theme clamp */
}
.kk-r9-pack .aurora-proof-grid {
  display: grid;
  gap: var(--kk-about-gap);
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.kk-r9-pack .aurora-proof-grid--cta {
  grid-template-columns: 1fr; /* same max rail, full span */
}
```

CTA moves into `aurora-proof-grid aurora-proof-grid--cta` so its edges share the rooms/trail rail.

At `max-width: 720px`, grids collapse to 1 column (page CSS media query).

## Copy change (Option A)

- Kicker: `Public trail` → `Receipts`  
- H3: `A two-decade public trail` → `Two decades in public rooms`  
- Card 3 body: `leave a trail` → `leave receipts` (removes residual "trail" echo)

## What stays intact

- Lead section copy and H2  
- Four rooms media cards (URLs, images, titles, blurbs)  
- Remaining three proof cards (Community / Receipts over adjectives / Human capacity) titles + bodies except the optional trail→receipts polish  
- CTA heading, body, `/contact/` button  
- Pack marker `<!-- content-architecture-2026:about -->`  
- Wrapper `kk-page kk-r9-pack`

Out of scope: Beastie Boys / old "Five rooms" roster restore; theme file edits; title field.

## Apply procedure (after KK approval)

1. Confirm secrets: `WP_USER` + `WP_APP_PASSWORD` present (length check only).  
2. Authenticated GET page `1208`; write `backup/<timestamp>-about-418/page-1208-before.json` + rendered HTML.  
3. Dry-run: print payload bytes, section kickers, `public trail` count in payload (expect 0 for Option A).  
4. KK signs the chosen copy option + screenshots plan.  
5. Body-only REST update (`content` raw = `payload-body.html`). Do not send `title`.  
6. Purge Pagely page cache for `/about/`.  
7. Logged-out verification (checklist below).  
8. If bad: restore snapshot `content.raw`.

## Verification checklist (issue acceptance + evals)

### Acceptance

- [ ] One consistent background treatment, **or** documented palette of at most 2 (paper + panel; media scrim called out as intentional photo treatment).  
- [ ] Rooms, proof, and CTA share the same max-width rail; 2-col grids align; CTA full-span uses the same rail.  
- [ ] `public trail` appears ≤1 time in approved copy (Option A target: **0**).

### Evals

- [ ] `curl -sL https://kriskrug.co/about/ | grep -ci 'public trail'` → `0` (Option A) or `1` (B/C).  
- [ ] Full-page screenshots at **375 / 768 / 1440** reviewed for background + alignment.  
- [ ] Text contrast AA on paper, panel, and media-scrim text (light ink on scrim).  
- [ ] Rooms cards, proof cards, CTA, and `/contact/` link still present; no accidental wipe of pack sections.

### Safety

- [ ] Pre-edit snapshot under `backup/`  
- [ ] Pagely purge after write  
- [ ] Logged-out smoke  
- [ ] Rollback path documented (restore before JSON)
