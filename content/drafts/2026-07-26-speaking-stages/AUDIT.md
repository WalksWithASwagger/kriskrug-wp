# Audit: homepage `#stages` strip (2026-07-26)

Public readback against live `https://kriskrug.co/` and repo `theme/kk-aurora/templates/front-page.html` on `origin/main`.

## What ships today

```html
<section class="aurora-proof-strip" id="stages" aria-labelledby="aurora-stages-label" data-reveal>
  <div class="aurora-proof-strip-inner">
    <p class="aurora-kicker" id="aurora-stages-label">Recent stages</p>
    <div class="aurora-proof-outlets" aria-label="Stage and outlet names">
      <span>TED</span>
      <span>SXSW</span>
      <span>Adobe MAX</span>
      <span>Web Summit</span>
      <span>FITC</span>
      <span>MIT Media Lab</span>
      <span>CreativeMornings</span>
      <span>UN</span>
    </div>
  </div>
</section>
```

Live HTML matches repo markup for this section (structure identical on 2026-07-26 readback).

## Visual / UX diagnosis (matches KK teardown)

| Problem | Evidence |
|---|---|
| Text-on-pale, high contrast, no image | `.aurora-proof-strip` uses cream wash (`rgba(230, 220, 194, 0.55)`); names are dark spans only (`revive-port.css`) |
| Zero links | Every outlet is a bare `<span>`, not an `<a>` |
| Zero interactivity | No hover, focus, or keyboard affordance on outlets |
| Name soup hides the work | Famous labels without talk titles, years, photos, videos, or writeups |
| "Recent" is inaccurate | Mix of legacy brand names and current rooms; no dates |
| Claim drift risk | About page public trail says **TEDxOilSpill**, not TED. Adobe MAX / FITC / MIT Media Lab do not appear on live About. SXSW appears as trail name only (no homepage destination) |

## Adjacent homepage surfaces (do not confuse with this strip)

| Surface | ID / class | Notes for #414 |
|---|---|---|
| Hero stage photo | `.aurora-stage-photo` | Full-bleed LaSalle image already strong; keep separate from `#stages` redesign |
| Contact sheet | `#archive` | Stage photos already live here but all link to `/photography/` only |
| Work card "Keynotes 2026" | `#work` | Links to `/speaking/`; not a stage inventory |
| Speaking page | `/speaking/` | Conversion page (#419). Homepage strip should tease + link out, not duplicate the full sell |

## CSS facts (current)

From `theme/kk-aurora/assets/css/revive-port.css`:

- Strip padding + cream background + hairline border
- Flex wrap of large Space Grotesk names at ~62% opacity
- No `:hover` / `:focus-visible` rules for `.aurora-proof-outlets span`

## Verdict

This is not a patchable band. Replace the name soup with an image-led, linked, interactive module. Prefer **verified recent engagements** (talk video, owned portal, or published writeup) over prestige labels without destinations.
