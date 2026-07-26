# Homepage speaking stages redesign (#414)

**Status:** DRAFT only. Concept approval gate before any theme build or live WP write.  
**Lane:** Track A content packet (concept + copy + markup snippets). Track B theme build waits on KK pick.  
**Branch intent:** `cursor/414-speaking-stages-f196`  
**Issue:** [#414](https://github.com/WalksWithASwagger/kriskrug-wp/issues/414)

## What this package is

Ground-up redesign proposal for the homepage `#stages` band (`aurora-proof-strip` / "Recent stages"). KK teardown: black-on-white name soup, no links, no interactivity, good work hidden.

## Contents

| File | Purpose |
|---|---|
| [`AUDIT.md`](AUDIT.md) | Live + repo audit of the current strip |
| [`CONCEPTS.md`](CONCEPTS.md) | Three distinct art-direction concepts |
| [`COPY.md`](COPY.md) | Section copy options (kickers, titles, CTAs) |
| [`LINKS.md`](LINKS.md) | Verified destinations for every engagement |
| [`VISUALS.md`](VISUALS.md) | Photography, crops, hover/focus interactivity |
| [`NOTES.md`](NOTES.md) | Collision rules (#505 newsletter), safety, next steps |
| [`markup/`](markup/) | Drop-in HTML snippets for Concepts A / B / C |

## Ask for KK

1. Pick a concept direction (A, B, or C). Hybrid notes are in `CONCEPTS.md`.
2. Confirm the engagement set (recommended: verified recent stages, not the unverifiable logo soup).
3. Approve which stage photos move from owned media / media library into the section.
4. Only then authorize a Track B Aurora patch + package deploy with rollback ref.

## Explicit non-goals (this packet)

- No live WordPress writes.
- No edits to `theme/kk-aurora/` on this branch.
- No changes to the homepage newsletter band (owned by [#416](https://github.com/WalksWithASwagger/kriskrug-wp/issues/416) / PR [#505](https://github.com/WalksWithASwagger/kriskrug-wp/pull/505)).
- No Speaking page rebuild ([#419](https://github.com/WalksWithASwagger/kriskrug-wp/issues/419) is adjacent; share media inventory, do not merge scopes).
