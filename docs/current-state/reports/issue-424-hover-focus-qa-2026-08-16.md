# Issue #424 — live hover / focus / interactivity QA pass

**Captured:** 2026-08-16 (PDT), probe UTC `2026-08-17T02:24:34Z`  
**Mode:** public / read-only. No theme edits, no WordPress writes, no cache purge, no commit of PNGs.  
**Live theme readback:** Aurora **1.6.5** (`https://kriskrug.co/wp-content/themes/kk-aurora/style.css` `Version:`). Repo `main` is **1.6.6** and is **not** what this pass measured.  
**Served CSS:** Jetpack Boost bundle `https://s5102.pcdn.co/wp-content/boost-cache/static/8d99a2084d.min.css` (130,926 bytes). Public `style.css` / `revive-port.css` / `04-primitives.css` / `bleeding-edge.css` were fetched separately to quote source.  
**Branch:** `docs/424-hover-focus-qa-20260816`

Do not treat in-flight theme PRs as live. **#796 / #797 / #789 / #801** are open and were not measured.

Local screenshots (gitignored): `docs/current-state/reports/screenshots/issue-424-2026-08-16/`. Raw probe JSON lives next to them. A screenshot that missed its clip is called out below; those are not invented evidence.

## Verdict

**Keep #424 open. Re-scope it. Do not treat it as a site-wide emergency.**

KK's original teardown — *"There's no hovers or interactivity on any of that shit"* — **no longer reproduces** on live 1.6.5. Nav, buttons, work cards, service cards, writing cards, event CTAs, contact buttons, and in-prose links all change on hover and show a `:focus-visible` ring. A 35-stop keyboard sample on each of nine routes produced **zero** stops with no visible ring.

What still belongs on this issue is the **concentrated leftover**, not a new site-wide sweep:

1. `.aurora-footer-tile:hover` / `:focus-within` still lose to a Revive `!important` rest pin. Same mechanism as the 2026-07-25 inventory.
2. `.aurora-feed-link-grid a` and `.aurora-writing-pagination a` still lose their authored background hover to the cream-contrast `!important` block. Underline is the only computed change.
3. `#476` shipped `04-primitives.css` (`.kk-button`, `.kk-card`, `--focus-ring`), but **zero** sampled pages render those classes. Live interaction is still per-component, not the shared layer the issue asked for.

Close #424 only if KK wants the board cleaned and is willing to file a smaller follow-up for those three leftovers. Do not close it on the claim that the original items are gone — the footer-tile fight is still live.

## Original items — still reproduce?

Baseline: [`INTERACTION-STATES-GAP-INVENTORY.md`](../INTERACTION-STATES-GAP-INVENTORY.md) (live 1.4.3, 2026-07-25) plus the 2026-08-05 comment on #424.

| Original item | 2026-07-25 | Live 1.6.5 | Still a #424 defect? |
|---|---|---|---|
| "No hovers anywhere" | Half-right: 67/604 missing hover | **Does not reproduce.** Sampled cards/links/buttons change | No |
| Keyboard tab-through, visible focus | 438/438 rings | **Still pass.** 35 tabs × 9 routes, 0 no-ring | No |
| Outlines suppressed with no replacement | Zero | **Still zero.** Three `outline: none` rules still re-covered | No |
| `.aurora-footer-tile` hover / `:focus-within` cascade loss | Largest gap (48 instances) | **Still dead.** CDP hover diff empty. Same `!important` pin | **Yes** |
| `.aurora-feed-link-grid a` / pagination background hover | Cascade loss | **Background still dead.** Underline now lands | **Yes (weaker)** |
| `.aurora-service-card` no hover | Rule-missing | **Fixed** by #676: `:hover` / `:focus-within { transform: translateY(-2px) }` | No |
| `.aurora-work-card` focus | Partial | **Fixed** by #676: image scale + `:focus-within` outline | No |
| `.aurora-topic-card` no hover/focus | 2026-08-05 high-priority | **Gone.** Speaking now uses `.aurora-card`, which has `:hover` | No |
| `.aurora-section-head a` no hover | Specificity loss on color | **Underline now lands.** Color/border still do not use a component `:hover` | Low |
| `.kk-contact-card` no hover | Rule-missing | **Still no card hover.** Cards are not links | Low (not interactive) |
| Form-field states | No `<form>` on main-nav | **Still no form.** Contact is `mailto:` + Beehiiv | N/A |
| Media-card hover dies under `prefers-reduced-motion` | 16 cards | Rule still motion-only (`filter` + `transform`); not re-run under `reduce` this pass | Residual |
| Shared primitives cover links/buttons/cards/pills | Blocked on #476 | `#476` closed; file exists; **0 live consumers** | **Yes** |
| Focus-ring split (allowlist vs catch-all) | Two colours/thicknesses | **Still split.** Anchors: 2px `#9a2f14` @3px. Containers also keep `--focus-ring` box-shadow | Residual, not a 2.4.7 fail |

Sibling issues named in the brief: **#708 contrast CLOSED**, **#479 breakpoints CLOSED**, **#701 CLS CLOSED**. #708's cream-contrast `!important` block is still the reason pagination / feed-link backgrounds cannot hover.

## Method

- Public `curl` of `style.css` + linked sheets. Version claim is the public header, not repo `theme/kk-aurora/style.css`.
- Playwright 1.62.1 / Chromium 1234 against **live** `https://kriskrug.co` (logged out). `CSS.forcePseudoState` for computed hover / `:focus-visible`. Real `Tab` for the first 35 stops per route. `transition-duration: 0s` injected so color transitions do not read as rest.
- Viewports: 1440×900 for hover/focus; 390×844 for tap-target boxes.
- Routes: `/`, `/about/`, `/speaking/`, `/services/`, `/work/`, `/events/`, `/contact/`, `/2026/08/11/futureproof-festival-announcement/`, plus `/blog/` because that is where the feed-grid / pagination leftovers live.
- Screenshots used real `.hover()` / `.focus()`, not CDP. A few clips missed (footer-tile first match is 592×800 and painted the hero; feed-link hover clip drifted). Those are marked **not used**.

Limits: 35 tabs is a sample, not the full 66-stop home census from July. CDP reported `transform: none → matrix(1,0,0,1,0,0)` on some lift rules (identity, not a visible lift) — treat those as inconclusive and prefer CSS + screenshot. `.kk-contact-button` CDP said no hover; the screenshot disagrees (dark → signal orange). Screenshot wins.

## Acceptance criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Gap inventory | **Met** in July (PR #487). This pass is the re-verify, not a second inventory. |
| 2 | Shared interaction styles cover links, buttons, cards, pills | **Not met.** `04-primitives.css` exists. Live markup still uses `.aurora-button` / `.aurora-work-card` / page-pack `.kk-contact-button`. Count of `.kk-button` and `.kk-card` on every sampled route: **0**. |
| 3 | Every main-nav page passes keyboard tab-through with visible focus | **Met** on the sampled stops. Re-verify after any 1.6.6+ deploy. |
| Eval | Computed `:hover` / `:focus-visible` differ from rest on sampled elements | **Mostly met.** Failures concentrated on footer tiles (hover) and the intended *background* of feed/pagination chips. |
| Eval | No outline suppressed without replacement | **Met.** |

## Per-route

Severity for #424 only. Homepage chrome that #796 is rewriting is noted, not re-filed.

### `/` home

- **Hover:** work cards (`a.aurora-work-card` ×3) and service cards (×3) have authored state. Nav / utility / header CTA underline. Section-head “Photography →” / “Full index →” underline on hover (screenshot `home-section-head-hover.png`). Footer tiles: **no computed hover**.
- **Focus:** sampled tabs all showed `outline: solid 2px rgb(154, 47, 20)` @ 3px (`--revive-accent-text`, darkened by the #708 line). Skip-link uses ink `rgb(23, 19, 16)`.
- **Tap / pointer (390):** `.aurora-button` is authored `min-height: 44px`. Desktop header CTA computes **38px** tall (`style.css:651–656`). Mobile nav pills in `style.css:2797–2808` are `min-height: 44px` but **lose** to `revive-port.css:1166–1172` (`min-height: 0 !important`). Same finding as the #127 mobile pass — product choice, not a missed pill deploy. Smallest mobile hits: “Reconciliation” / “Worldview” (17px) and section-head “PHOTOGRAPHY ?” / “FULL INDEX ?” (~22px).
- **Counts:** 79 anchors, 0 buttons, 0 forms. `.kk-button` / `.kk-card`: 0.

### `/2026/08/11/futureproof-festival-announcement/` (post)

- **Hover:** `.aurora-prose a` (×31) underline; `.aurora-article-map a` (×7) transform + underline. `button.lightbox-trigger` (×9): **no hover** in CSS or CDP.
- **Focus:** lightbox trigger gets a visible 2px signal ring, not clipped (`post-lightbox-focus.png`). Map links and prose links ring.
- **Tap:** lightbox hit box **20×44**. Below WCAG 2.5.8's 24px on the short axis. Core WP lightbox, not Aurora.
- **Counts:** 12 `<button>` (all lightbox). Still no form.

### `/work/`

- **Hover:** `.aurora-media-card a` (× cards) underline; card hover is on the descendant `img` (`style.css` `.aurora-media-card:hover img { filter: saturate(1.12); transform: scale(1.035); }`). Footer tiles still dead.
- **Focus:** media-card links ring. #676 work-card outline is on the homepage triptych, not this archive's media cards.
- **Tap:** same header/footer pattern as home.

### `/about/`

- **Hover:** `.aurora-card` has a lift rule; `.aurora-media-card a` underline; `.aurora-prose a` changes background to `rgb(232, 181, 58)` and `translateY(-1px)` — a real, visible hover, not underline-only.
- **Focus:** rings on sampled stops. Footer tiles dead.
- **Tap:** “Reconciliation” / “Worldview” 17px again (footer / legal).

### `/speaking/`

- **Hover:** topic-card gap is gone. Five `.aurora-card` blocks (Keynotes / Workshops / Executive briefings / Hosting / book-Kris) use `.aurora-card:hover`. Media cards same as About.
- **Focus:** fine on sampled stops.
- **Tap:** same header/footer leftovers.

### `/events/`

- **Hover:** event CTAs (`.aurora-event-card a` / `.aurora-proof-module a`) change fill `rgb(192, 63, 24)` → `rgb(232, 181, 58)` and lift 1px. This is the strongest button hover on the site.
- **Focus:** 2px `#9a2f14` ring on those CTAs.
- **Tap:** those CTAs compute **211×44**. Fine.
- **Note:** there is no `.aurora-event-card:hover` rule. The card is a `.aurora-proof-module`; interactivity lives on the inner buttons.

### `/services/`

- **Hover:** page-pack CSS, not theme primitives. `.kk-services-button:hover` fill `rgb(23, 19, 16)` → `rgb(217, 74, 31)`. `.kk-services-proof-card:hover` border `rgba(23,19,16,0.14)` → `rgba(181,60,24,0.4)`.
- **Focus:** rings present. Pack CSS has **no** `:focus-visible` of its own; the global Revive allowlist covers the `<a>`.
- **Tap:** services button **203×42**. Close to 44.

### `/contact/` — there is still no contact form

- Markup: `mailto:feelmoreplants@gmail.com` buttons + Beehiiv outbound. **0** `<form>`, `<input>`, `<textarea>`, `<select>`, `<button>`.
- **Hover:** `.kk-contact-button:hover` is authored and **visible** (screenshot rest = ink fill, hover = signal orange). CDP missed it; do not trust that row. `.kk-contact a:hover` underline is authored. `.kk-contact-card` has rest styles only — four info articles, not links.
- **Focus:** `EMAIL KRIS` shows the cream-gap + `#9a2f14` ring (`contact-button-focus.png`).
- **Tap:** contact buttons **113×44**. Fine.
- Form-field half of #424 remains **untestable** on this route. Same as July.

### `/blog/` (extra; original leftover host)

- **Hover:** writing-card links underline. Feed-grid (×8) and pagination (×4): **underline only**. Authored `background: rgba(217, 74, 31, 0.12)` does not win. Pagination hover screenshot shows an underline under “2”, not a fill change.
- **Focus:** rings on chips and page numbers.
- **Tap:** feed chips **172×36**; pagination **30×39**. Both under 44. Pagination width fails 2.5.8.

## Evidence (quoted live CSS / HTML)

Public theme version:

```
Version: 1.6.5
@layer reset, tokens, base, primitives, components, patterns, utilities, overrides;
```

Footer tile — rule exists, rest pin still kills it (live `style.css:2447–2451` vs live `revive-port.css:910–913`):

```css
.aurora-footer-tile:hover,
.aurora-footer-tile:focus-within {
  background: rgba(247, 247, 242, 0.05);
  border-color: var(--aurora-line-strong);
}

.aurora-footer-tile {
  border-color: var(--revive-line) !important;
  background: transparent !important;
}
```

CDP on `.aurora-footer-tile` (all 9 routes): `hoverChanged: false`. `hoverDiff: {}`.

Feed / pagination — hover authored, rest pinned twice (live `style.css:1317–1321` and `1258–1263`, killer at `4183–4188`, repeated again at `4214`):

```css
.aurora-feed-link-grid a:hover,
.aurora-feed-link-grid a:focus-visible {
  background: rgba(217, 74, 31, 0.12);
  border-color: var(--aurora-line-strong);
}

body.aurora-theme :where(.aurora-writing-pagination a, …, .aurora-feed-link-grid a) {
  background-color: var(--aurora-panel-solid) !important;
  border-color: var(--aurora-line-strong) !important;
  color: var(--aurora-ink) !important;
}
```

CDP hoverDiff on both selectors: `{ textDecorationLine: none → underline }` only. No `backgroundColor` change.

#676 work + service cards (live `revive-port.css:534–543` and `702–705`):

```css
.aurora-work-card:hover .aurora-work-card-media img,
.aurora-work-card:focus-within .aurora-work-card-media img {
  transform: scale(1.04);
  filter: grayscale(0);
}
.aurora-work-card:focus-within {
  outline: 2px solid var(--revive-accent-text);
  outline-offset: 4px;
}
.aurora-service-card:hover,
.aurora-service-card:focus-within {
  transform: translateY(-2px);
}
```

Focus ring that actually paints on anchors (live `revive-port.css:150–168`):

```css
body.aurora-theme :where(a, button, input, select, textarea, summary, .aurora-button, …):focus-visible {
  outline: 2px solid var(--revive-accent-text) !important;
  outline-offset: 3px !important;
  box-shadow: none !important;
}
```

Computed on a focused nav link: `outline: solid 2px rgb(154, 47, 20)` / `outline-offset: 3px`.

Contact is still not a form (live `/contact/` HTML):

```html
<a class="kk-contact-button" href="mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co">Email Kris</a>
<a class="kk-contact-button secondary" href="https://kriskrug.beehiiv.com/" …>Get the newsletter</a>
```

Tap-target authorship vs what wins at 768px (live `style.css:476` and `2797–2808` vs `revive-port.css:1166–1172`):

```css
.aurora-button { min-height: 44px; }

@media (max-width: 768px) {
  .aurora-primary-nav a { min-height: 44px; /* pills */ }
}

/* Nav: no dark-theme pill chips on cream */
body.aurora-theme .aurora-primary-nav a {
  min-height: 0 !important;
}
```

Primitives exist and are unused (live `04-primitives.css`, `#476`):

```css
@layer primitives {
  :root { --focus-ring: 0 0 0 2px var(--wp--preset--color--paper), 0 0 0 4px var(--wp--preset--color--signal); }
  .kk-button:hover { transform: translateY(-1px); }
  .kk-button:focus-visible { outline: none; box-shadow: var(--focus-ring); }
  .kk-card:hover { transform: translateY(-4px); border-color: var(--aurora-line-strong); }
}
```

Query on every sampled route: `.kk-button` count 0, `.kk-card` count 0.

## What I did not treat as a #424 bug

- Homepage band layout that **PR #796 / #797** are already rewriting.
- `#756` title em dash / umlaut (**PR #789**).
- Cream token aliases (**PR #801**).
- Nav not being a hamburger, and nav chips being 25–34px after the Revive `min-height: 0` pin — already recorded on #127.
- Contact cards without hover: they are not interactive.
- CDP identity-matrix “transform changes” on lift rules.
- Screenshots whose clip missed the target (footer-tile set, feed-link hover).

## Recommendation

**Keep #424 open.** Rewrite the title/body to the leftovers:

1. Unblock `.aurora-footer-tile:hover, :focus-within` by dropping or re-scoping the Revive rest `!important` (or author a cream-native tile hover that can win). This is still the largest real gap.
2. Let feed-grid / pagination hover backgrounds win, or delete the dead hover so the underline is the honest contract.
3. Either adopt `.kk-button` / `.kk-card` on live markup or close the “shared primitives” criterion as “shipped unused” and stop asking #424 to do #476's adoption.

Do **not** start another site-wide hover hunt. Do **not** edit theme files while #796 / #797 / #789 / #801 are in flight. After 1.6.6+ deploys, re-run the probe; do not assume this 1.6.5 readback still holds.

If KK prefers a clean issue tracker: close #424 as “original site-wide claim is false; keyboard passes” and open a small Track B issue for the footer-tile + cream-contrast hover leftovers only.
