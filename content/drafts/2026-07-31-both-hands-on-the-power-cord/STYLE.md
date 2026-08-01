# Style — Both Hands on the Power Cord

## Default for generated art

Use Rafiki **`--style kriskrug`** for any generated illustration / YouTube thumb / social card for this post.

- Guide: `/Users/kk/Code/rafiki/styles/kriskrug.md`
- Registry: `/Users/kk/Code/rafiki/styles/styles.yaml` → key `kriskrug`
- Compose kits when needed: `kriskrug+kk-blocks`, `kriskrug+kk-acid`, `kriskrug+cmvan`

**Never use `--style kk` for this post.** In Rafiki, `kk` is the **BC + AI** teal/purple recipe, not the personal kriskrug.co brand.

## Hard rules (KK 2026-08-01)

1. **Generative only for thumbs / editorial art.** No Pillow overlays, no “real photo + type composite.” Type lives *inside* the generative frame (or omit type).
2. **Likeness path:** Kris LoRA (`walkswithaswagger/kris-krug-final-elite-20260407`, trigger `KRISKRUG`) — not Gemini face invention from reference photos.
3. **Never Stewart Muir** (bald, short grey beard, thin glasses, plaid) as the face.
4. Documentary protest / march photos stay **real WP media** (do not fake crowds).

## Documentary images stay real media

Body/featured documentary photos stay real WP media already inventoried, e.g.:

- `11964` — KK on Granville Bridge
- `11999` — bridge skyline / march
- `11976` — FUCK AI / drink-data sign
- `11919`, `11915` — related art/signs

## YouTube thumb status

Video: `n_aGBFGnPzo` — Studio: https://studio.youtube.com/video/n_aGBFGnPzo/edit

| Round | Approach | Status |
|---|---|---|
| 1 | Gemini + `kriskrug` bakeoff (protest hand) | Rejected — hand/sign |
| 2 | Gemini ED variants | Rejected — not Kris / bad style |
| 3 | Real photo + type overlay | Rejected — **no overlays ever** |
| 4 | Generative + **KRISKRUG LoRA** | In flight / next |

Local evidence (gitignored under `content/drafts/**/images/`): `_rejected-ai-face/`, overlay REAL* files, earlier bakeoffs. Do not upload those.

Picker: `images/thumb-viewer.html` (update when Round 4 lands).
