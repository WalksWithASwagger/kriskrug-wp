# Featured-image audit — kriskrug.co 2026 posts (2026-08-10)

Method: `featured-image-forge` skill audit mode. Mechanical gates (landscape, >=1200x630, aspect 1.3-2.1) run against media metadata for all **37 published 2026 posts**; every failure then visually inspected as an actual OG 1.91:1 center-crop preview. Trigger: KK ruling that featured crops were shipping bad with no checks (the Keep the Machine Strange portrait incident, since fixed with approved media 12720).

**Result: 25/37 PASS. 12 flagged**, ranked below by how broken they actually look as cards.

## Tier 1 — actively broken as social/theme cards (6)

| Post | Slug | Featured | What the card actually shows |
|---|---|---|---|
| 11936 | you-cant-drink-data | 1593x1600 square | Protest sign cropped mid-word to "FUCK AT!" — the message breaks, hands severed at edges, and raw profanity is the og:image on every share |
| 12357 | ethos-lab-block-party | 1500x1500 square | Poster title decapitated ("block party 2026" top-sliced); the Eth&#7885;&#769;s Lab name cropped out entirely |
| 11826 | web-summit-vancouver-2026 | 1280x500 banner | Baked-in title sliced at both edges: "MMIT, PUBLIC FUNDING & CIVIC ACCOUNTABILIT" / "S THE BADGE MATH", plus an orphaned logo fragment |
| 11358 | spa-at-the-end-of-time | 1280x500 banner | Title reduced to fragments: "TUB / TICISM / THE AI ERA" |
| 11171 | both-hands-full | 1280x500 banner | Title sliced ("ANDS FULL: REATIVES ACTUALLY NEED...") and both figures' heads cut at the top |
| 12363 | vancouver-made-world-cup | 896x1200 portrait | The kit design decapitated — crop shows headless jersey torso + shorts, patch text unreadable |

## Tier 2 — survives the crop but degraded (4)

| Post | Slug | Featured | Verdict |
|---|---|---|---|
| 11929 | data-center-protest-signs | 1024x1536 portrait | Cartoon server face survives and is fun, but the water-drop context is chopped and it upscales from 1024 |
| 12638 | no-one-knows-what-to-call-us-yet | 1024x1024 square | Claymation scene crops fine visually; under-resolution for cards |
| 12327 | storyhive-haus-of-owl-jordan-dack | 640x360 | Composition fine (both hosts intact) but it is a 640px video frame — soft everywhere it renders |
| 11700 | punk-rock-ai | 1280x500 banner | Real photo (VAG talk) that happens to survive the crop; only the 500px height upscale hurts it |

## Tier 3 — marginal, acceptable (1)

| 11765 | calling-us-all-in | 1102x712 | Booth photo reads well at every crop; 98px under the width gate. Leave unless retouched anyway. |

## Missing featured (1)

| 12184 | canada-ai-for-all-strategy-skeptical-guide | none | No featured image at all — no card art anywhere it is shared. Topically adjacent to the Postman essay, which now cites AI for All. |

## Recommended remediation (per post, pending KK approval — nothing changes live without it)

- **you-cant-drink-data / data-center-protest-signs:** swap to a landscape photo from each post's own gallery (real protest photos beat generated art here); whole sign legible in-frame. KK call on whether profanity stays the front-door image.
- **Text-baked banners (both-hands-full, spa-at-the-end-of-time, web-summit-vancouver-2026):** regenerate clean 16:9 heroes with NO baked text (titles belong to the card template, not the pixels), kriskrug style, through the forge gates. No source masters found in the repo.
- **ethos-lab-block-party:** landscape event photo if one exists in the post, else re-lay the poster motif at 16:9 without the text rows.
- **vancouver-made-world-cup:** re-frame a single kit centered at 16:9 (kit art was generated; the rafiki counter-FIFA presets can re-emit), or crop the existing art to the shirt.
- **storyhive:** pull the YouTube maxres frame (1280x720) of the same shot — passes gates, no re-art needed.
- **no-one-knows-what-to-call-us-yet / punk-rock-ai:** optional round 2 (upscale or re-source); both acceptable meanwhile.
- **calling-us-all-in:** leave.
- **canada-ai-for-all-strategy-skeptical-guide:** generate a hero through the forge (currently has nothing).

QC preview crops for every flagged post are in the session scratchpad (`audit-downloads/qc-*/`). Full machine-readable table: `featured-audit-2026.json` (same folder).
