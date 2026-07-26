# #413 - Client logo soup (draft package)

Draft-first package for a monochromatic, interactive client logo band on the homepage. **No live WP writes. No theme file edits on this PR.**

Issue: [#413](https://github.com/WalksWithASwagger/kriskrug-wp/issues/413)

## Why draft-only

1. **Asset gate.** Repo + kriskrug.co media library do not currently hold a usable set of *client* logo files. Build is blocked until KK/Peter supply logos and KK approves the client list.
2. **Collision gate.** Sibling draft PR **#505** (`feat(#416): homepage newsletter section`) already edits `front-page.html`, `revive-port.css`, and `style.css`. This packet proposes a **separate** section (`#clients` / `aurora-logo-soup`) and must not rewrite the newsletter band. Theme apply waits until after #505 lands (or rebases onto it), then Aurora package flow.

## Package

| File | Purpose |
|------|---------|
| `inventory.md` | What was found (Peter-era Upgrade work, repo, media library, live site) |
| `client-list-for-kk.md` | Candidate roster from About wild-index; KK approval gate |
| `treatment.md` | Monochrome + interactive behavior, a11y, layout |
| `copy.md` | Section copy options (no em dashes) |
| `proposed-html.html` | Drop-in markup sketch (placeholders; no live assets) |
| `proposed-css.css` | Mono filter + hover/focus + wrap rules |
| `acceptance-checklist.md` | Issue AC + evals, mapped to this packet |

## Placement (separate from #505)

Insert **between** `aurora-proof-strip` (`#stages`) and `aurora-archive-band` (`#archive`), or between work-band and services-band if KK prefers proof lower. Do **not** touch `#newsletter` / `aurora-newsletter-band`.

Do **not** replace the existing text stage strip (`TED` / `SXSW` / …). Stages stay stages. Logo soup is client/collaborator proof.

## Apply after KK gates clear

1. KK approves client list in `client-list-for-kk.md` (at least 8 names).
2. KK/Peter deliver logo files (SVG preferred, or transparent PNG). Upload to WP media; record IDs in inventory.
3. Wire hover notes only from approved quote bank (or one-line engagement notes KK writes).
4. Paste chosen copy into `proposed-html.html`; fill `src` / `alt` from media IDs.
5. After #505 merges (or rebase), patch `front-page.html` with the new section only; append `proposed-css.css` into `revive-port.css`.
6. Run `acceptance-checklist.md`; screenshots at 375 / 768 / 1440; keyboard tab-through.

## Related

- Issue comment (2026-07-19): first source inventory; still accurate that client logo *images* are missing.
- About wild-index: text chip list of clients (source for candidate roster).
- `#415` What People Say: quote-forward band; keep logo soup visual, not a second testimonial wall.
- The Upgrade AI public site has wrapped (`theupgrade.ai` is a move notice). Enterprise logo proof previously cited there is not currently fetchable as assets.
