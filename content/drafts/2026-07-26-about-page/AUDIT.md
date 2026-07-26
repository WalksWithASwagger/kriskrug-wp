# About page audit - #418

**Status:** draft only. Public HTML readback. No live WP write.  
**Fetched:** 2026-07-26 (public `GET https://kriskrug.co/about/`)  
**WP page ID:** 1208  
**Evidence:** `evidence/public-entry-content-2026-07-26.html`, `evidence/snapshot-meta.json`

## Issue claim (KK teardown 2026-07-17)

> The columns are different widths. 'Public trail' is a weird way to talk about it, and it says it twice. Text is on black, boxes on gray, then a navy background, then another gray. The alignment's lost.

## Live structure (2026-07-26)

Page body is a single `<!-- wp:html -->` pack:

1. Lead - kicker `About`, display H2, lead + body paragraphs  
2. Rooms - kicker `The rooms I am in now`, 4× `.aurora-media-card` in `.aurora-proof-grid`  
3. Trail - kicker `Public trail`, 4× `.aurora-card` in `.aurora-proof-grid`  
4. CTA - single full-width `.aurora-card` (`Start with the work`)

Inline page CSS (`.kk-r9-pack`) only resets drop-caps, styles `.aurora-button`, and forces card radius/shadow. Layout and surfaces mostly come from theme (`style.css` + `revive-port.css`).

## Finding 1 - Double "public trail" (confirmed)

`grep -ci 'public trail'` on rendered HTML = **2**

| # | Location | Exact text |
|---|---|---|
| 1 | Section kicker | `Public trail` |
| 2 | First card H3 | `A two-decade public trail` |

Source in entry content:

```text
<p class="aurora-section-kicker">Public trail</p>
...
<h3>A two-decade public trail</h3>
```

Fails acceptance: "appears at most once … or not at all."

## Finding 2 - Background system still multi-surface

Post-R9 cream revive softened the old dark pack, but the page still stacks distinct treatments:

| Layer | What renders | Source |
|---|---|---|
| Page paper | `#efe6d2` / `--revive-surface` | theme + `body` |
| Text cards / CTA card | cream panel `#e6dcc2` / `--revive-surface-2` | `.aurora-card` via revive-port |
| Media ("rooms") cards | photo + near-black bottom scrim `rgba(13,15,21,0.8→0.96)` | `.aurora-media-card::after` in theme |
| Primary CTA control | ink button `#171310` (hover `#d94a1f`) | page inline `.kk-r9-pack .aurora-button` |

That matches the teardown complaint in spirit: **lead text on paper**, **boxes on gray/cream**, **photo text over black**, plus a **dark control**. KK's "navy" read is consistent with the old dark elevated surfaces; live now reads as black scrim + cream, not a separate navy band.

Contrast spot-check (sRGB relative luminance math):

| Pair | Ratio | Notes |
|---|---|---|
| `#171310` on `#efe6d2` | 14.88:1 | AA pass |
| `#171310` on `#e6dcc2` | 13.53:1 | AA pass |
| `#efe6d2` on scrim `#0d0f15` | 15.43:1 | would pass **if** media-card titles used light ink |
| Media card titles use `--aurora-ink` (`#171310`) over dark scrim | ~1:1 risk | Theme still sets dark ink on `.aurora-media-card h3/p`; dark-on-dark is the a11y landmine |
| Button hover `#efe6d2` on `#d94a1f` | 3.42:1 | UI-component borderline; keep an eye in screenshots |

## Finding 3 - Column / alignment drift (confirmed)

Same class name, inconsistent rails:

1. **WP layout constraint** on `.aurora-page-content`: `max-width: 860px`  
2. **Theme** `.aurora-proof-section`: `max-width: var(--aurora-max)` (= `1200px`) + horizontal padding  
3. **Footer group** (page chrome): `max-width: 980px`  
4. **Grid cells unequal in visual weight:** rooms use tall image cards (`min-height: 24rem`); trail uses short text panels. Both are `repeat(2, 1fr)`, but they do not read as one column system.  
5. **CTA breaks the grid:** full-bleed single card under the 2-col sections, so left/right edges of half-cards vs full card feel misaligned once padding/gap differ.

## Finding 4 - Content integrity note for acceptance evals

Issue evals mention roster / Beastie Boys cards / galleries. Public HTML on 2026-07-26 does **not** contain Beastie Boys, "Five rooms", or gallery markup. Those lived in the pre-content-architecture overhaul (`backup/20260701T193335Z-.../page-1208-about-before.html`). Current live markers that **must** stay intact for this edit:

- Rooms grid (BC + AI, keynotes, visual storytelling, creative AI systems)  
- Four proof cards + CTA  
- Contact link `/contact/`

Restoring Beastie/gallery modules is **out of scope for #418** unless KK reopens that content.

## Root cause summary

| Problem | Root cause | Fix lane |
|---|---|---|
| Double "public trail" | Duplicate framing in pack HTML | Track A page content |
| Multi backgrounds | Theme media-card scrim + cream cards + paper; page CSS too thin to unify | Track A page-scoped CSS (preferred) / theme later |
| Column drift | Nested max-widths + mixed card types + CTA outside shared grid rail | Track A page-scoped CSS + light HTML wrap |

## Recommended direction

See `copy-options.md` (recommend **Option A**) and `payload-plan.md` / `payload-body.html` for the apply-ready body.
