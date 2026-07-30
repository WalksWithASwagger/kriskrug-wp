# Aurora Media Gaps — Sourcing Checklist (2026-05-23)

Current-state media inventory for the Aurora redesign, taken from the live
`aurora/v2` templates (commit `dd2f428`) as rendered on Local
(`http://localhost:10003`). Supersedes the media section of
`AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`, which predates the media-led
`front-page.html`.

## Status since the 2026-05-18 audit

- ✅ **Hero gap closed.** Homepage is now media-led: full-bleed keynote photo,
  role kicker, proof row, "Book a keynote" primary CTA.
- ✅ **Work grid populated** with real project imagery (BC + AI, Both Hands Full,
  Punk Rock AI, The Upgrade AI).
- ⚠️ **Two real gaps remain** (below): single-photo overuse, and zero media
  governance (everything is an external hotlink).

## Gap 1 — One photo is carrying the whole site

`punkrockai.com/.../michelle-diamond/195.webp` (CreativeMornings keynote shot)
is reused in **4 places**:

| Surface | Use | Needs |
|---------|-----|-------|
| Homepage hero | full-bleed | keep as canonical hero |
| Homepage "Punk Rock AI" card | thumbnail | a *different* Punk Rock AI image |
| Work proof grid — Punk Rock AI | thumbnail | same — distinct image |
| Speaking proof grid — "reel" | static, labelled "reel" | a real **keynote video/reel**, or relabel as photo |

→ Source **3–4 additional distinct images** so each surface is unique, plus one
real speaking-reel video (or fallback still + honest label).

## Gap 2 — Media governance (blocks production cutover)

Every image is hotlinked from an external origin via the Jetpack CDN:

- `i0.wp.com/www.punkrockai.com/...`
- `i0.wp.com/bc-ai.ca/...`
- `i0.wp.com/www.theupgrade.ai/...`
- `bothhandsfull.com/opengraph-image` (not even CDN-cached)

Risk: if any source site changes a path, the homepage breaks. No rights record,
no alt/caption governance, no crop/compression control.

→ Before cutover: **upload canonical assets into the kriskrug.co media library**,
rewrite `src`/`srcset` to local media URLs, set alt text + captions, confirm
rights for each. (`bothhandsfull.com/opengraph-image` especially must be
replaced with a stable uploaded asset.)

## Gap 3 — Pages with no media yet

| Page | Current media | Needs |
|------|---------------|-------|
| About | none in Aurora template; audit flagged ~13 images | portrait band, credibility/story photos |
| Work (`/work/`) | n/a — page absent from Local DB; exists on prod | confirm on staging-from-prod, then media-rich case cards |
| Speaking | static photo standing in for reel | keynote reel video + event/testimonial logos |
| Photography | none | **open decision** — credential band, full portfolio, or v1 pillar? |

## Open decisions for KK (carry into post-launch fine-tune)

1. **Speaking reel:** real video embed, or keep a still and drop the "reel" label?
2. **Punk Rock AI imagery:** pick distinct shots so `195.webp` isn't reused.
3. **Photography role in v1:** credential band / portfolio section / major pillar?
4. **About portraits:** which portrait + story images become canonical?

## Pre-cutover must-dos (the hard blockers)

- [ ] Upload all hero + card + proof images into the WP media library; rewrite to local URLs.
- [ ] Replace `bothhandsfull.com/opengraph-image` hotlink with a stable asset.
- [ ] De-duplicate `195.webp` across hero / 2 cards / reel.
- [ ] Alt text + captions + rights confirmed for every asset.
- [ ] Re-verify on real staging (production content + media), as part of QA gate #86.
