# Layout + image crop proposals (#412)

## Layout options

### Layout 1  -  Text below image (RECOMMENDED)

Kill overlay copy. Photo is photo. Title, one-line, and door sit under the frame in ink on cream.

```
┌─────────────┐
│             │
│   PHOTO     │  aspect 4/5 or 3/4, object-fit cover, explicit object-position
│             │
└─────────────┘
01  BC + AI
Meetups, certification...
Join →
```

Why: passes the 5-second test; survives bad lighting in the photo; no scrim/pill fight; works at 375 without tiny overlay type.

CSS direction (implement later, scoped to `.aurora-work-band`):

- `.aurora-work-card-body` → static flow under media (not absolute)
- remove or neutralize `.aurora-work-card-media::after` gradient for this band
- keep hover zoom on image only
- drop desktop `nth-child(2) { margin-top: -2.5rem }` unless KK wants stagger with text-below

### Layout 2  -  Title chip on image, body below

Only the title (or title + number) stays on a small bottom bar; description never overlays the face/subject.

Use when KK wants some drama but readable crops. Still depends on shared pill/overlay fix for the chip.

### Layout 3  -  Keep full overlay (not recommended)

Only if crops are perfect and copy is ≤1 short line. Still fails "pill sections are broken" until shared CSS lands. Do not pick unless KK insists after seeing Layout 1 mock.

---

## Aspect + breakpoints

| Breakpoint | Grid | Crop notes |
|---|---|---|
| 375 | 1 column | Full-bleed card width; prefer `object-position` that protects faces |
| 768 | 1 or 2 col | If 2-col, keep equal heights; no negative margin stagger |
| 1440 | 3 col | Equal tops; optional mild stagger only with Layout 1 |

Recommended frame: **4 / 5** (slightly less aggressive than 3 / 4 for landscape source photos). If sources are true portraits, 3 / 4 is fine.

---

## Image proposals (no hotlinks)

Acceptance: Media Library, alt text, no off-site hosts.

### Lab 01  -  BC + AI (community)

| | |
|---|---|
| **Reject** | `bcai-living-ecosystem.webp` graphic from bc-ai.ca (hotlink + diagram crop) |
| **Primary candidate** | Theme asset already on home contact sheet: `/wp-content/themes/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg` (1600×1066). Hands-up room energy. **Ingest a copy into Media Library** (do not keep theme-path as long-term source of truth). |
| **Crop** | `object-fit: cover; object-position: center 35%;` protect raised hands + stage figure; avoid chopping the front row at mobile. |
| **Alt** | Kris Krüg onstage at a Vancouver AI meetup as the room raises hands |

### Lab 02  -  Futureproof (festival)

| | |
|---|---|
| **Reject** | `futureproof-salmon-starfield-share-20260527.jpg` OG art (1200×630, hotlink, not a room) |
| **Primary candidate** | Pending KK / #497 Futureproof design assets once in Media Library. Prefer a real crowd, stage, or venue frame over key art. |
| **Interim (proposal only)** | Reuse a strong stage/crowd frame from the contact sheet (e.g. LaSalle both-hands or CreativeMornings crowd) **only if** KK accepts it as stand-in until festival photography is ingested. Label interim in deploy notes. |
| **Crop** | For landscape stage: `object-position: center 25%` (heads safe). For key art (if forced): do not use 3/4; switch that card to 16/9 or 3/2. |
| **Alt** | (after pick) concrete: who/where/what in the frame |

### Lab 03  -  Keynotes (stage)

| | |
|---|---|
| **Current** | Michelle Diamond CreativeMornings frame via punkrockai CDN (hotlink) |
| **Primary candidate** | Same photograph **after** Media Library ingest from a rights-cleared master, or LaSalle `kk-laSalle-both-hands-full-25` already on Media Library CDN (`kriskrug.co/wp-content/uploads/2026/05/...`). |
| **Crop** | Speaking portrait: `object-position: center top` or `center 20%` so head/hands stay in frame under 4/5. |
| **Alt** | Kris Krug speaking at CreativeMornings Vancouver (or LaSalle College Vancouver, if that asset wins) |

---

## Focal-point checklist (screenshots)

Before KK sign-off, capture 375 / 768 / 1440 and confirm:

- [ ] No cut-off heads on lab 01 and 03
- [ ] Lab 02 shows a readable subject (not a sliced logo or empty gradient)
- [ ] Text not over faces (Layout 1/2)
- [ ] Alts present; `src` hosts are `kriskrug.co` Media Library (or i0.wp.com mirror of same)
- [ ] Logged-out link check: bc-ai.ca, futureproof.website, /speaking/ → 200

---

## Implement isolation (when theme opens)

Touch only:

1. `templates/front-page.html`  -  `#work` block
2. Scoped rules under `.aurora-work-band` in `revive-port.css` (or post-#474 `@layer components`)

Do **not** edit the newsletter band (PR #505 collision). Do not retouch services Ecosystem card in this issue.
