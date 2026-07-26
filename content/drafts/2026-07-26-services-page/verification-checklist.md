# Verification checklist - Services page (#420)

**Mode:** DRAFT ONLY until KK approval. No live WP write from this package.

## Acceptance criteria

- [ ] Copy drafted, voice-audited, **approved by KK** (picker in `language-options.md`)  
- [ ] Total page height reduced by **at least one third at 1440** without losing offers  
  - Before: document **3548 px** (Playwright 2026-07-26)  
  - Target: document ≤ **2365 px**  
  - Pack guide: ≤ **1376 px** (before pack **2064 px**)  
  - Before/after numbers recorded in the apply PR  
- [ ] Every service block states **what**, **who**, and **what to do next**

## Evals

- [ ] voice-slop-audit passes on approved copy  
- [ ] **Zero em dashes** in pack body (and in drafted options)  
- [ ] Before/after page-height measurement at **1440** in the PR  
- [ ] Screenshots at **375 / 768 / 1440** (full page)  
- [ ] All CTAs and links **200** logged out:
  - [ ] `/services/` → 301 → `/generative-ai-services/` 200  
  - [ ] `/contact/` 200  
  - [ ] `/work/` 200  
  - [ ] `/speaking/` 200  
  - [ ] Proof image URLs 200  
  - [ ] Beehiiv checked in a real browser if linked (curl may 403)

## Stylesheet / rebuild

- [ ] No new theme CSS file for Services  
- [ ] No new `!important` in page CSS  
- [ ] Inline block changes are temporary and compatible with #423 step 7 deletion  
- [ ] Layout choice documented (Plan A/B/C)

## Safety (when applying later)

- [ ] KK signed copy option + layout plan  
- [ ] Authenticated GET page `2666`; snapshot under `backup/<timestamp>-services-420/`  
- [ ] Dry-run: payload bytes, offer titles, em dash count (expect 0), height estimate  
- [ ] Body-only REST update; do not send title unless KK approved a title change  
- [ ] Pagely purge for `/generative-ai-services/` and `/services/`  
- [ ] Logged-out smoke + screenshots  
- [ ] Rollback: restore snapshot `content.raw`

## Draft package completeness (this commit)

- [x] `AUDIT.md` with public evidence  
- [x] `language-options.md` with KK picker  
- [x] `layout-scroll-plan.md` with scroll math  
- [x] `verification-checklist.md`  
- [x] `evidence/` snapshot + Playwright baseline  
- [x] No live WP write
