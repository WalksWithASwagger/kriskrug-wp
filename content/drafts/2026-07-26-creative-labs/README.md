# Creative Labs section redesign (#412)

**Status:** DRAFT proposal only. No live WP. No theme edit in this package.
**Lane:** Track A content packet (feeds Track B Aurora implement after KK pick).
**Branch:** `cursor/412-creative-labs-f196`
**Gate:** KK approve design + copy before Aurora package deploy.

## What this is

KK teardown called this area cryptic, with broken pill overlays and bad crops. On the live Revive homepage the target is the **Current work** triptych (`#work` / `.aurora-work-band`): BC + AI, Futureproof, Keynotes 2026.

This package proposes renaming/reframing that band as **Creative Labs**, moving copy off the image overlay, and art-directing crops with Media Library photos (no hotlinks).

## Package

| File | Purpose |
|---|---|
| [audit.md](./audit.md) | Live/repo diagnosis, 5-second test fail, collision notes |
| [copy-options.md](./copy-options.md) | Section + per-lab copy options A–D (Dark Crystal; no em dashes) |
| [layout-image-crops.md](./layout-image-crops.md) | Layout patterns + image/crop recommendations |
| [proposed-markup.html](./proposed-markup.html) | Staged HTML for `#work` (Option B copy + Layout 1) |

## Collision / why no theme patch

PR **#505** (`feat(#416)` newsletter) edits `theme/kk-aurora/templates/front-page.html` (newsletter band + related CSS). The Creative Labs band lives in the same template. Theme implement is deferred until KK picks copy/layout, then land in an isolated `#work` hunk after #505 merges (or rebase onto it).

Related but separate:

- Pill/overlay stylesheet bug (Ecosystem / Festival / Creative Labs shared root cause) ships elsewhere; this redesign **consumes** that fix and stops relying on overlay text.
- #411 Join BC / Futureproof is a different section (absent on current Revive home). Do not conflate.

## Acceptance map (proposal stage)

| AC | This draft |
|---|---|
| Design proposal approved by KK before live deploy | Ready for review |
| Every lab: clear title, one-line plain description, working link | See copy-options + markup |
| Images cropped correctly at breakpoints | See layout-image-crops (needs KK photo pick + Media Library ingest) |
| 5-second test: stranger knows what Creative Labs is | Section dek + plain lab lines |

## Next (after KK pick)

1. Confirm Option letter + Layout number.
2. Ingest/replace hotlinked images into Media Library with alt text.
3. Patch only the `#work` block in `front-page.html` + scoped CSS (no newsletter hunk).
4. Screenshot gate at 375 / 768 / 1440. Link 200s logged out. voice-slop-audit on final copy.
5. Aurora package deploy with rollback ref.
