# AUDIT  -  #411 Join BC / Futureproof (`aurora-work-band`)

Date: 2026-07-26  
Scope: homepage Current work triptych (BC + AI, Futureproof, Keynotes 2026)  
Live readback: `https://kriskrug.co/` (public HTML)  
Repo theme: Aurora **1.4.8** (`origin/main` @ session start)

## Section map (post-Revive)

| Issue language | Live / repo class | Notes |
|----------------|-------------------|--------|
| Join BC / Future Proof | `section.aurora-work-band#work` | Primary target for this issue title + WORK-PLAN |
| Old "What I get hired for" | was `aurora-offer-band` | Removed in Revive port; #447 copy landed then section was replaced |
| Services / Keynote·Workshop·Ecosystem | `section.aurora-services-band#services` | Still says `rooms` twice; out of primary scope but related residual |

## Live markup (work-band)  -  current

- Kicker: `Current work`
- H2: `What Kris is building now.`
- Card 01 BC + AI → `https://bc-ai.ca/`  
  Body: `Province-wide trust layer for responsible AI: meetups, certification, policy rooms, and practical adoption.`
- Card 02 Futureproof → `https://www.futureproof.website/`  
  Body: `Pacific Northwest gathering where frontier tech, creative practice, and civic trust share one public room.`
- Card 03 Keynotes 2026 → `/speaking/`  
  Body: `Stage sessions on taste, human agency, and the operating conditions for responsible AI.`

`grep`-style `rooms` hits inside work-band: **2** (`policy rooms`, `public room`). Gate fails.

## Acceptance criteria status

| AC | Status | Evidence |
|----|--------|----------|
| Copy options drafted; KK picks one | Open | Options in `options.md` (A/B/C headings + card bodies). #447 posted an earlier A/B/C for the old offer-band; KK never locked a pick. Refresh for work-band below. |
| Word `rooms` gone from the section | Fail (live + repo) | Work-band has 2; services-band has 2 more |
| Columns align on a shared grid at desktop | Fail by design | `revive-port.css`: `.aurora-work-card:nth-child(2) { margin-top: -2.5rem; }` staggers Futureproof off the shared baseline |
| Drop cap removed or redesigned | Partial / ambiguous | No `::first-letter` on this section. Oversized `.aurora-work-card-num` (2.5rem, accent wash) reads as a decorative drop glyph on each card. Propose retire → small mono index |
| Interactive elements have hover + focus | Partial | Hover: image zoom + desaturate only. No `:focus-visible` / card chrome lift in `revive-port.css` for `.aurora-work-card` |

## Structural findings (CSS)

File: `theme/kk-aurora/assets/css/revive-port.css`

1. **Alignment**  -  `@media (min-width: 900px)` triptych is `repeat(3, minmax(0, 1fr))` (good) but child 2 is yanked up `-2.5rem` (bad for "shared grid").
2. **Drop glyph**  -  `.aurora-work-card-num` at `font-size: 2.5rem` + `color: rgba(217, 74, 31, 0.45)` sits top-left over media. Likely what KK called the ugly drop cap after the Revive remount (old heading-first-letter complaint from #447 is obsolete).
3. **Hover**  -  image transform only. Links need visible focus ring; cards need a light border/lift so keyboard users get the same cue.
4. **Headline typeface**  -  Space Grotesk on `.aurora-section-head h2`. Keep. Do not touch global type tokens.

## Collision with #505

PR #505 edits the newsletter band in the same `front-page.html` and adds newsletter rules in `revive-port.css`. Work-band rules sit a few hundred lines above newsletter rules in that file. Conflict risk on theme merge: **high** if both PRs touch `revive-port.css` / `front-page.html` in parallel.

**Decision for this swarm pass:** ship draft package only. No theme commits.

## Out of scope (note only)

- Services-band `rooms` copy (`executive rooms`, `public rooms`) and its ribbon cards.
- Dead `.aurora-offer-band` / `.aurora-hired-grid` CSS still in `style.css` (cleanup belongs with cascade rebuild #474, not here).
- Live deploy / Pagely purge.

## Verification checklist (when wiring)

- [ ] Chosen copy: zero em dashes, zero `rooms` in section HTML
- [ ] `grep -ci 'rooms'` on rendered work-band → `0`
- [ ] Desktop 1440: three card tops share one baseline
- [ ] 768 / 375: single column, no horizontal overflow
- [ ] Tab order: Full index link → card 01 → 02 → 03; focus ring visible on each
- [ ] `prefers-reduced-motion`: no transform lift (CSS included in proposed snippet)
