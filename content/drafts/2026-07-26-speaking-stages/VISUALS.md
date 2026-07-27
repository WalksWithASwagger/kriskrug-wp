# Visuals + interactivity for `#stages`

## Photography brief

Issue #414 wants stage photos as the backbone. Portraits alone do not close the brief (`content/source-packs/site-photography-2026/README.md` already says so for #414/#419).

### Ready-now assets (public / already on site)

| Asset | Role | Limit |
|---|---|---|
| `kk-laSalle-both-hands-full-25-scaled.jpg` (media library) | Hero / LaSalle tile | Strong stage action; already used in masthead (vary crop if reused) |
| `kk-laSalle-both-hands-full-10-scaled.jpg` | Alternate LaSalle crop | Prefer different frame than masthead |
| Michelle Diamond CreativeMornings stage still (`punkrockai.com/.../195.webp`) | CreativeMornings tile | Hotlink today; **ingest to WP media before ship** |
| `vancouver-ai-meetup-30-kris-community.jpg` (theme asset) | Vancouver AI tile | Hands-raised community energy; move to media library for consistency |
| `kk-cmvan-keynote-header.png` | Punk Rock AI graphic fallback | Art, not documentary stage photo |

### Still needed from KK archive (curate before build)

Wide action frames with mic, slides, or audience context for:

- ChannelNext
- Whistler Institute
- Bass Coast Brain Stage
- Web Summit Vancouver (booth / renegade / stage)
- Futureproof Festival

Until those arrive, Concept C (one hero + text rows) is the safer ship path; Concept A needs the fuller set.

### Crop targets

| Breakpoint | Tile treatment |
|---|---|
| 375 | 4:5 or 1:1; face + mic priority; event label under image |
| 768 | 3:2; 2-column grid |
| 1440 | 3:2 or 16:9 rail; 5 to 7 tiles; title visible on hover and for `:focus-visible` |

### Alt text pattern

`Kris Krug [action] at [event], [context].`  
Photographer credit in caption or figcaption, not stuffed into alt.

Example: `Kris Krug presenting on stage at LaSalle College Vancouver.`  
Caption: `LaSalle College, Both Hands Full keynote.`

### No hotlinks rule

Acceptance criteria: images from media library. Before live build, ingest Michelle Diamond / event stills via the media manifest path. Draft markup may reference known public URLs as placeholders only.

---

## Interactivity spec (all concepts)

| State | Behavior |
|---|---|
| Rest | Photo readable; event name visible; talk title visible or truncated with ellipsis |
| Hover (pointer) | Image brightens or lifts 2%; title underline; cursor pointer |
| Focus-visible | 2px outline using Aurora focus token; same reveal as hover for title |
| Active | Slight press (translateY 1px) optional |
| Reduced motion | No marquee scroll; no scale animation; color/underline only |

### Accessibility

- One link per engagement (no nested buttons)
- Contrast AA for text on imagery: use bottom scrim (`linear-gradient` to ~60% black) or place text below the image
- Do not rely on hover alone for talk titles (keyboard users must see them)
- `aria-label` on tiles when visible text is incomplete: `"Punk Rock AI talk at CreativeMornings Vancouver"`

### Motion budget (2 to 3 intentional motions)

1. Tile lift / scrim reveal on hover-focus  
2. Section `data-reveal` entrance (already used on homepage)  
3. Optional: subtle accent bar slide on Concept C rows  

Skip infinite marquees unless KK insists; they fight reduced-motion and readability.

---

## Event / venue logos (optional secondary)

Only after photo backbone lands.

- Mono at rest, color on hover/focus (same interaction language as #413 client soup, but **separate section**)
- Prefer wordmarks KK already has rights to; do not scrape brand sites
- KK approval gate on which marks appear

Suggested first marks if cleared: CreativeMornings, Web Summit, Futureproof, Vancouver AI, BC + AI.
