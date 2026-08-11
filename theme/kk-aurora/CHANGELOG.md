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

## 1.6.3
**Deployed:** Built, not deployed (live is 1.6.0)
PSI perf round: right-sized WebP theme assets (#702, PR #711), display-sized Photon variants in the contact sheet (#704, PR #714), self-hosted Futureproof key art (#705, PR #712), composited-only transitions (#707, PR #713), and the five homepage WCAG contrast fixes (#708, PR #715). Merged 2026-08-10.

## 1.6.2
**Deployed:** Built, not deployed (live is 1.6.0)
Collapse 12 width breakpoints to the 480/768/1200 token scale; CSS budget lowered to 6902 lines / 162 importants (#479, PR #703, merged 2026-08-10).

## 1.6.1
**Deployed:** Built, not deployed (live is 1.6.0; superseded in repo by 1.6.2 the same day)
Detach form error/success selectors the #681 purge left glued to the footer rule and restore their color rules (#698, PR #699, merged 2026-08-10).

## 1.6.0
**Deployed:** LIVE (public readback 2026-08-10; the 2026-08-10 SFTP window shipped 1.5.10 + 1.5.11 + 1.6.0 together, rollback `kk-aurora.bak-1786336956`)
Delete 97 dead CSS classes and 9 dead `@keyframes` from `style.css` (#478, PR #681, merged 2026-08-07).

## 1.5.11
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-10 1.6.0 deploy)
Primitives layer plus block-editor parity so the editor canvas renders cream/ink instead of the pre-Revive dark palette (#476, PR #680, merged 2026-08-05).

## 1.5.10
**Deployed:** Superseded (never live standalone; first reached production inside the 2026-08-10 1.6.0 deploy)
Focus-visible states on work and service cards for WCAG 2.4.7, plus the `functions.php` version catch-up missed in 1.5.9 (PR #676, merged 2026-08-05).

## 1.5.9
**Deployed:** Superseded (live 2026-08-05 to 2026-08-10 per public readbacks; replaced by the 1.6.0 deploy)
Retire the drop cap (#475, PR #672, merged 2026-08-05).

## 1.5.8
**Deployed:** Superseded (never live as 1.5.8; deploy was gated on #601, and its CSS first shipped inside the later 1.5.9 deploy)
`aurora-tstm` testimonials showpiece CSS (#596, PR #629, merged 2026-08-02).

## 1.5.7
**Deployed:** Superseded (SFTP-deployed live 2026-08-01 pre-merge; PR #618 synced the repo to live; replaced by the 1.5.9 deploy)
Full-bleed `krug-1` portrait hero on Home and About (PR #618, merged 2026-08-01).

## 1.5.1 through 1.5.6
**Deployed:** Never released (skipped numbers)
Reserved by the stylesheet rebuild plan (#475 as 1.5.1, #476 as 1.5.2, #477 as 1.5.3+) and skipped when the hero shipped straight to 1.5.7; the reserved work later landed as 1.5.9 and 1.5.11.

## 1.5.0
**Deployed:** Superseded (was live 2026-07-27 to 2026-08-01; source PR #493 merged 2026-07-27, resolving #545)
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
