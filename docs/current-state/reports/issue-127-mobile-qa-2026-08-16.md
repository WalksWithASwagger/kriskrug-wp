# Issue #127 — live mobile / responsive QA pass

**Captured:** 2026-08-16 (PDT), probe UTC `2026-08-17T01:48:09Z`  
**Mode:** public / read-only. No theme edits, no WordPress writes, no cache purge, no visual-baseline PNG corpus.  
**Live theme readback:** Aurora **1.6.5** (`https://kriskrug.co/wp-content/themes/kk-aurora/style.css` `Version:`). Repo `main` is **1.6.6** and is **not** what this pass measured.  
**WP generator:** `WordPress 7.0.4`  
**Branch:** `docs/127-mobile-qa-2026-08-16`

Parent swarm notes said live was 1.6.6. Public `style.css` disagrees. This report follows the public readback.

## Verdict

**#127 is substantially done.** The original acceptance criteria reproduce as **pass** on live 1.6.5. The dedicated QA pass does not need more theme work. Close #127 after KK skims this report. Do not keep it open as a catch-all mobile bucket.

What changed since the issue was filed (May 2026) and last kept open:

| Dependency / sibling | State now | Effect on #127 |
|---|---|---|
| #479 12→3 breakpoints (480 / 768 / 1200) | **CLOSED** | The original blocker is gone. Live `02-tokens.css` has `--kk-bp-sm: 480px`, `--kk-bp-md: 768px`, `--kk-bp-lg: 1200px`. |
| #701 homepage CLS / LCP | **CLOSED** | Perf, not this AC. Not re-audited here. |
| #708 homepage contrast | **CLOSED** | A11y contrast, not this AC. Not re-audited here. |
| PR #789 Aurora 1.6.7 title-format | **OPEN**, unmerged | Inner `<title>` em dash is a #756 bug, not mobile layout. |
| PR #796 homepage #411–#413 (Aurora 1.6.8) | **OPEN** | Will rewrite homepage bands. **Do not file homepage layout bugs against live 1.6.5 that #796 is already replacing.** |

June 2026 comments on #127 already had a public pass for keyboard nav, overflow, and one-H1. This run re-checked that contract on the **post-#479 token scale** and the current Revive cream header.

## Original acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Mobile primary nav reachable + usable with keyboard at 360 / 390 / 768 | **PASS** | Playwright dispatched `keydown` on `.aurora-primary-nav a`. 7 links: ABOUT → WORK → SPEAKING → SERVICES → PHOTOGRAPHY → WRITING → CONTACT. |
| 2 | ArrowLeft / ArrowRight move between primary nav links | **PASS** | 360 / 390 / 768: ABOUT → ArrowRight → WORK → ArrowLeft → ABOUT. |
| 3 | Home / End jump to first / last nav link | **PASS** | End → CONTACT, Home → ABOUT at all three widths. |
| 4 | Focus indicators visible on nav links and CTA | **PASS** | Focused nav link computed `outline: rgb(154, 47, 20) solid 2px` / `outline-offset: 3px` (`revive-port.css` cream-safe ring). Skip-link: `rgb(23, 19, 16) solid 2px`. Header CTA box is 44×125 at 390. |
| 5 | Hero image crop/scale acceptable at 360 / 390 / 768 | **PASS** (designed crop) | `krug-1.jpg` paints wider than the viewport (`488px` at 390, `960px` at 768) with `overflow-x: clip` and a negative left offset. Document `scrollWidth === clientWidth`. Headline “The model is the message.” is fully readable. Homepage hero will move under PR #796. |
| 6 | Work proof modules stack; no image/text overlap | **PASS** | `/work/` has `.aurora-proof-section` + 13 `.aurora-media-card`s. Cards stack in one column at 390 (`cardOverlaps: []`). Per-card “overlap” of caption vs image is the media-card overlay, not a bleed. The old `.aurora-proof-module` class is gone; this is the current Work surface (not `/recent-projects-include/`, which 301s to `/work/`). |
| 7 | No horizontal **page** overflow on home, work, speaking, contact | **PASS** | `document.documentElement.scrollWidth - clientWidth === 0` at 360 / 390 / 480 / 768 on `/`, `/work/`, `/about/`, `/speaking/`, `/contact/`, and `/2026/08/10/keep-the-machine-strange/`. |

Viewport meta is present on every sampled route: `width=device-width, initial-scale=1`. One visible `h1` per route.

## What looks like a bug and is not

The header is a **horizontal, scrollable text nav**, not a hamburger. That is the shipped contract (#127 body, #28). At **390px** the nav scrollport is ~250px wide; PHOTOGRAPHY / WRITING / CONTACT sit in `overflow-x: auto` (scrollbar hidden). That **clips in a viewport screenshot** and is easy to misread as overflow. It is not page overflow. Keyboard Home/End/Arrows reach those links. Logo (`.aurora-brand` 290–374) and nav (16–266) **do not overlap** at 390.

`body.aurora-theme .aurora-primary-nav a { min-height: 0 !important; … }` in live `revive-port.css` (“Nav: no dark-theme pill chips on cream”) is why the 44px pill rule in `style.css` `@media (max-width: 768px)` does not win. Computed nav link: `min-height: 0px`, `10.24px` type, **25×34–86**. That is **above WCAG 2.2 AA 2.5.8 (24px)** and **below AAA 2.5.5 (44px)**. The header CTA is already 44px. This is a product choice, not a missed deploy of the pill CSS.

The woven marquee track is wider than the viewport by design (`overflow-x: hidden` on the document). Reduced-motion was forced for the probe (`prefers-reduced-motion: reduce`); the track still occupies extra width, it just does not animate.

## 480 / 768 token boundaries

| Width | Nav | Page overflow | Notes |
|---|---|---|---|
| 360 | CONTACT + WRITING in the scrollport (`right` 367 / 428 vs `vw` 360) | 0 | Same contract as 390. |
| 390 | CONTACT in the scrollport (`right` 428 vs `vw` 390) | 0 | Tightest real-phone width in this pass. |
| **480** (`--kk-bp-sm`) | All 7 links in view (`CONTACT.right` 428 < 480) | 0 | This is the width where the row stops clipping. |
| **768** (`--kk-bp-md`) | All 7 links in view; same left-aligned row | 0 | No awkward wrap. Overflow-x remains `auto` (harmless when content fits). |

## Per-route findings (390 unless noted)

Severity: **none** that belong in #127. Residual notes are P3 / optional.

### `/` home

- **Severity:** n/a for #127. Homepage chrome is in scope of **PR #796** (#411–#413 Join BC / Labs / logo soup). Do not file live-homepage layout issues that that PR is rewriting.
- Hero copy, dual CTAs (WORK WITH ME + CURRENT WORK), and crop are readable at 360 / 390 / 480 / 768.
- Small tap targets besides nav: footer / marquee wordmarks (~24px tall), text links like “FULL INDEX”. Not unique to home.

### `/work/`

- H1 “Work”. Intro stacks. Proof cards one-column, no card-on-card collision.
- Same header nav contract as home.

### `/2026/08/10/keep-the-machine-strange/` (latest long-form sample)

- H1 intact; tags wrap; article map `<summary>` is 322×27 (wide, short — P3). Inline links ~22px tall (normal prose).
- HTML contains `width: 2560px` in an image-related rule; it did **not** widen the document at 360–768.

### `/about/`

- Photo hero + “I build culture around emerging technology.” readable. Dual CTAs (CONTACT KRIS / SEE THE WORK) sit side by side and stay in the viewport.
- Same header nav contract.

### `/speaking/`

- H1 “AI Keynote Speaker Kris Krüg”. Body measure is comfortable. No page overflow.
- Same header nav contract.

### `/contact/` (form)

- **No `<form>`.** Live contact is mailto + Beehiiv, not Jetpack/Gravity/WPForms. CTAs “EMAIL KRIS” / “GET THE NEWSLETTER” stack full-width (~42px tall — 2px under 44, not worth an issue). `mailto:feelmoreplants@gmail.com`. Newsletter → `https://kriskrug.beehiiv.com/`.
- Original AC only required no overflow on the contact template. **PASS.** Form-usability is “mailto buttons work; there is nothing to fill in.”

## Optional follow-ups (do **not** file from this lane)

These are the only leftovers. None of them is a failed original AC. KK can file later if wanted:

1. **P3 a11y — nav hit area under Revive.** Restore a ≥44px hit box on `.aurora-primary-nav a` without bringing back dark pills (`revive-port.css` currently forces `min-height: 0`). Only if AAA 2.5.5 is a goal; AA 2.5.8 already passes.
2. **P3 UX — scroll affordance below 480.** Hidden scrollbar + clipped PHOTOGRAPHY/CONTACT at 390. Keyboard already works. A fade/peek hint would help thumbs. Do not replace with a hamburger unless product direction changes (issue body already says that would be a **new** issue).
3. **Post-#796 homepage re-QA.** After 1.6.8 homepage bands ship, re-check home at 390 / 480 / 768 only. Not a reason to keep #127 open.
4. **Physical device swipe.** This pass used Playwright viewports + dispatched keyboard events, not a thumb on glass. Low residual risk given overflow-x auto + keyboard proof.

Do **not** file: hamburger-menu requests, “PHOTO is truncated” as page overflow, homepage hero crop, Work card caption-on-image, contact “missing form,” or live 1.6.5 vs repo 1.6.6 as a mobile bug.

## Method

| Check | Status | Why |
|---|---|---|
| Public `style.css` Version readback | **pass** | 1.6.5 |
| HTML viewport / h1 / form / nowrap grep | **pass** | six routes + one post |
| Playwright overflow + tap + keyboard | **pass** | 6 routes × 360 / 390 / 480 / 768 |
| Viewport screenshots home / work / post @ 390 | **pass** | see disk note |
| `make visual-baseline` / `visual-diff` | **not-run** | #749 just pruned ~2GB of PNGs; harness is 11 routes × 3 viewports. Too expensive for this QA. |
| Cursor browser MCP | **blocked** | `browser_navigate` returned “No browser tab available.” |
| Real phone / OS Safari | **not-run** | no device in this lane |
| Contrast / Lighthouse / CLS | **not-run** | owned by #708 / #701 |
| Reduced-motion beyond `emulate` | **skipped** | screenshots forced `reduce`; CSS rules exist, not a full motion film |

## Disk

Nothing from this pass is in git.

Left on disk (gitignored / tmp, delete whenever):

```
/tmp/kriskrug-127-mobile-qa-20260816/
  home-390.png      ~1.2M
  work-390.png      ~1.0M
  post-390.png      ~1.1M
  qa-results.json
  followup.json
```

Extra 480/768 and about/speaking/contact/proof screenshots were captured for inspection, then deleted. Total remaining ~3.3M PNG + JSON.

`docs/current-state/AURORA-MOBILE-QA-127.md` is the old undated test plan (≤700px pills, 12-breakpoint list). It is superseded by this report.

## Recommendation

Close #127 as the dedicated mobile/responsive QA pass. Remaining items are optional P3 follow-ups or other open PRs (#789, #796), not failed acceptance criteria.
