# #411  -  Join BC / Futureproof section (draft package)

Draft-first package for homepage `aurora-work-band` (BC + AI · Futureproof · Keynotes). No live WP writes. No theme file edits on this PR.

## Why draft-only

Sibling draft PR **#505** (`feat(#416): homepage newsletter section`) already edits:

- `theme/kk-aurora/templates/front-page.html`
- `theme/kk-aurora/assets/css/revive-port.css`
- `theme/kk-aurora/style.css`

Work-band CSS lives in `revive-port.css`. Shipping theme diffs here would collide on merge. Apply the snippets in this folder **after** #505 lands (or rebase onto it), then bump Aurora via the usual package flow.

## Package

| File | Purpose |
|------|---------|
| `AUDIT.md` | Live vs repo truth, AC status, collision notes |
| `options.md` | Copy options (KK pick required); zero `rooms`; zero em dashes |
| `proposed-html.html` | Drop-in section markup (Option A wired) |
| `proposed-css.css` | Alignment + drop-cap retire + hover/focus |

## Apply after KK pick + #505

1. KK picks heading (A/B/C) and any card tweaks in `options.md`.
2. Paste chosen copy into `proposed-html.html`.
3. Patch `front-page.html` work-band only (lines around `aurora-work-band`).
4. Append `proposed-css.css` into `revive-port.css` near `.aurora-work-triptych` (or replace the stagger rule).
5. `grep -ci 'rooms'` on the section HTML → must be `0`.
6. Voice-slop-audit on chosen copy; screenshots at 375 / 768 / 1440; keyboard tab-through.

## Related history

- **#447** (merged): rewrote the old `aurora-offer-band` ("What I get hired for"). That markup is gone after the Revive cream home. Residual CSS for `.aurora-hired-grid` still lives in `style.css` but is unused on the live home.
- Live home still has `rooms` in work-band + services-band copy (see `AUDIT.md`).
