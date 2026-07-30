# kk-aurora Changelog

Version history for the `kk-aurora` theme, doubling as a deploy ledger. This
repo is adjacent to the live site, not a mirror of it, so the "Deployed" marker
on each entry is the single answer to "what is live, and what changed."

Format is loosely [Keep a Changelog](https://keepachangelog.com/). Newest first.
Deploy status uses:

- **LIVE** confirmed on production by a public `style.css` readback
- **On main** merged to `main`, deploy status not confirmed
- **Superseded** no longer the deploy target; kept for history

Entry detail is derived from `theme/kk-aurora/readme.txt` and the version-bump
commit subjects (`git log --oneline -- theme/kk-aurora/style.css`). Older
1.3.x history lives in `readme.txt`.

When you cut a new release, add a line here and follow
`docs/current-state/AURORA-RELEASE-CHECKLIST.md`.

---

## 1.5.0
**Deployed:** LIVE (PR #493 merged 2026-07-27; live==repo 1.5.0; #545 closed)
Cascade `@layer` scaffold plus `--kk-*` tokens (#474).

## 1.4.9
**Deployed:** On main; deploy status unknown
Homepage newsletter band rewritten with an honest weekly-email CTA and three recent-post thumbnails; blog-index band drops the dispatch/field-notes chrome (#416, #505).

## 1.4.8
**Deployed:** Superseded
Replace the "authored judgment" copy on the homepage (#410).

## 1.4.7
**Deployed:** Superseded
Responsive `srcset` for the homepage hero image (#407).

## 1.4.6
**Deployed:** Superseded
Convert `.aurora-writing-card` (the blog-index card) to the cream system across all six declaration sites, fixing an archive listing that was effectively blank under cream-era ink (#485).

## 1.4.5
**Deployed:** Superseded
Contrast fixes for inline-link hover, form validation errors, and submit labels; raise homepage work-card copy over the scrim; tokenize the control-label color; drop dead pre-cream literals; add a CSS literal-contrast test.

## 1.4.4
**Deployed:** Superseded
Darken the accent orange to #9a2f14 and the primary control fills so accent text clears AA on every cream surface; darken Ink Muted; restore the theme skip link and suppress the duplicate core one.

## 1.4.3
**Deployed:** Superseded
Full-bleed header shell so the brand pins left on ultrawide; larger italic rainbow "message" word and a riso gradient rule under homepage section heads (R5/R6).

## 1.4.2
**Deployed:** Superseded
Fix leftover dark meta with `color-scheme: light` and a cream `theme-color`; preload Space Grotesk and DM Sans instead of the unused Inter and Clash Display.

## 1.4.1
**Deployed:** Superseded
Cream accessibility polish: AA-safe accent text for kickers, visible focus rings on paper, removal of the duplicate theme skip link, and tighter header nav (R1 to R4).

## 1.4.0
**Deployed:** Superseded
Port the Revive cream/ink visual system into kk-aurora; retokenize `theme.json` and `style.css` (Space Grotesk / DM Sans / JetBrains Mono); rebuild the sticky header (woven marquee, scroll progress), footer, and homepage section order; add a global page CSS bridge so Track A packs inherit cream/ink.
