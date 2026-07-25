# Interaction states gap inventory — hover, focus, and keyboard (2026-07-25)

**Issue:** [#424 — [QA] Site-wide hover, focus, and interactivity pass](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424). This document delivers **only the first acceptance criterion**, the gap inventory.
**Deliberately not done here:** the shared interaction styles. [`AURORA-STYLESHEET-REBUILD-PLAN.md`](AURORA-STYLESHEET-REBUILD-PLAN.md) §3.1 sequences #424's *implementation* behind step 4 (`04-primitives.css`), because the shared focus-ring and interactive-state layer #424 asks for **is** that primitives layer. Building it now means writing it twice. §3.1 says the audit half should start now; this is that half. See §10 for whether I still agree after doing the work.
**Lane:** Track B measurement only. **Zero `.css`, `.php`, `.html`, or `theme.json` changed.** One new read-only script was added under `scripts/`.
**Measured against:** **live** `https://kriskrug.co`, logged out, 2026-07-25, Aurora **1.4.3**. Not the repo — see §1.2.

---

## Bottom line

The premise the issue was filed on — *"there's no hovers or interactivity on any of that shit"* — is **half right, and wrong in the half that matters most for accessibility.**

- **Focus is in far better shape than the issue assumes.** Of **604** interactive elements rendered across the eight main-nav routes, **604 receive a visible `:focus-visible` ring**. A real keyboard tab-through of all eight routes produced **438 tab stops** and **every single one had a visible focus indicator** that matched `:focus-visible`. **Zero** elements have an outline suppressed without an equal-or-better replacement. **Zero** focus rings fall below WCAG 1.4.11's 3:1 (the weakest measured is 3.11:1). The theme's three competing `outline: none` declarations are all correctly re-covered downstream. **WCAG 2.4.7 passes on all eight routes.**
- **Hover is where the gaps are, and they are concentrated, not site-wide.** **67 of 604 elements (11.1%)** have no hover affordance at all.
- **The single most important finding is the shape of those gaps, not their count.** Only **5 of 67** are "nobody wrote a hover rule." The other **62 (92.5%)** have a hover rule that matches the element, declares a visibly different value, and **loses the cascade to an `!important` declaration on the element's own rest state.** These are not missing styles. They are styles that were silently switched off by later contrast patches. A primitives layer that only *adds* rules will not fix any of them.
- **27 of the 98 interaction rules in the served CSS match nothing on any of the eight routes** — 27.6% of the authored interaction surface is dead.
- **16 hover affordances are deleted outright for `prefers-reduced-motion` users**, because those affordances are motion-only and the reduced-motion block removes the motion without substituting anything.

---

## 1. Method — how every number here was produced

A grep for `:hover` cannot answer this issue. The five front-end sheets contain **118 `:hover` occurrences** and **80 `:focus` / `:focus-visible` / `:focus-within` occurrences** (`grep -o ':hover' … | wc -l`), but the questions that matter are *does the rule apply to a rendered element*, *does it win*, and *does the pixel actually change*. All three need a browser. Of those 198 occurrences, the number that produce a measurable state change on a rendered element is what this document reports — and it is not the same number.

### 1.1 The probe

New reusable script: [`scripts/interaction_state_probe.js`](../../scripts/interaction_state_probe.js).

```bash
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node scripts/interaction_state_probe.js --out /tmp/probe

# reuse an existing mirror, no re-fetch
node scripts/interaction_state_probe.js --out /tmp/probe --skip-mirror

# the reduced-motion comparison run in §6
node scripts/interaction_state_probe.js --out /tmp/probe-rm --skip-mirror --reduced-motion
```

It writes `probe.json` (full per-element data) and `summary.md`. It is read-only: no WordPress writes, no theme writes, and it **refuses to download a browser** — if `PLAYWRIGHT_BROWSERS_PATH` is unset it exits 2 rather than triggering `playwright install`, per rebuild-plan §4.6.

What it does, in order:

1. **Mirror.** Chromium in this sandbox cannot reach the public internet — the agent HTTPS proxy resets browser connections (`net::ERR_CONNECTION_RESET` on every proxy configuration tried; `curl` to the same URL returns `200`). So the script fetches each route's live HTML with `curl`, downloads every stylesheet and script it links, rewrites those URLs to local paths, and serves the result from `127.0.0.1`. Serving same-origin is not a workaround, it is a requirement: cross-origin stylesheets throw on `.cssRules`, and reading the rules is how the probe knows which rules *exist*.
2. **Freeze timing.** A `transition-duration: 0s !important` sheet is injected before any measurement. **This is not cosmetic.** The theme transitions `color` over 0.15s; reading `getComputedStyle` immediately after a state change returns the *start* of the transition, i.e. the rest value. Before this fix the probe scored the entire primary nav as having no hover state. Verified both ways: without the freeze, `.aurora-primary-nav a` reads `rgba(23,19,16,0.78)` on hover (unchanged); with the freeze — or after a 700ms settle — it reads `rgb(181,60,24)`.
3. **Force each state.** Per element, `:hover` and then `:focus`+`:focus-visible` are forced via CDP `CSS.forcePseudoState` — the mechanism behind DevTools' `:hov` panel. This is geometry-independent, so occluded, off-screen, and below-the-fold elements are measured exactly like visible ones. No mouse positioning, no scroll dependence.
4. **Diff computed style.** ~40 visual properties on the element, plus 14 properties each on `::before` and `::after`, plus a fingerprint of the first 40 descendants. The pseudo-element and subtree passes exist because several Aurora components put their whole affordance somewhere other than the element (`.aurora-link:hover::after`, `.aurora-media-card:hover img`). Measuring only the element would have reported those as missing.
5. **Attribute the cause.** For every state rule that matches the element, the declared value is resolved *on that element* by applying it inline for one frame. That separates three cases a grep collapses into one — see §1.3.
6. **Tab through for real.** After the per-element pass, the script presses `Tab` up to 400 times per route and records `document.activeElement`, whether it matches `:focus-visible`, its computed outline and box-shadow, and the ring's contrast against the surface it is painted on.

### 1.2 Live/repo parity — and why this audit is against live

| Check | Result | Command |
|---|---|---|
| Live theme version | **1.4.3** | `curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/style.css \| grep -m1 -i '^Version'` |
| Repo `main` theme version | **1.4.4** | `theme/kk-aurora/style.css` header |
| Live vs repo `style.css` | **differ** (13 changed lines) | `diff live-style.css theme/kk-aurora/style.css` |
| Live vs repo `revive-port.css` | **differ** | `diff live-revive.css theme/kk-aurora/assets/css/revive-port.css` |

This is a change since PR #468, which found them byte-identical. Repo `main` is now one undeployed version ahead. **The entire 1.4.3→1.4.4 delta is token *values*** — the #464/#465/#466 contrast work darkening `--aurora-signal`, `--revive-accent-text`, and the control fills. `diff` over both files returns **zero** changed lines containing `:hover`, `:focus`, or `outline`.

Consequence, stated precisely: **every structural finding in this document holds for both 1.4.3 and 1.4.4** — the cascade conflicts, the missing rules, and the dead rules are all identical in the repo line. Only the focus-ring *contrast numbers* in §4 will shift when 1.4.4 deploys, and they shift **upward** (the ring colour darkens from `#b53c18` to `#9a2f14` against the same cream), so the "all rings clear 3:1" conclusion strengthens rather than weakens.

Line references below cite **live** line numbers, with the repo equivalent where they differ.

### 1.3 The distinction that matters: missing vs losing vs no-op

The task of #424 is "fix gaps with shared styles, not per-element patches." Whether a shared style *can* fix a gap depends entirely on why the gap exists:

| Cause | What was measured | What a fix has to do |
|---|---|---|
| `rule-missing` | No rule in any loaded sheet targets this element in this state. | **Add** a rule. A primitives layer fixes this for free. |
| `rule-loses-cascade` | A rule targets it, and applying its declared value to the element *does* change the computed value — but under the forced state nothing changes. It is being outranked. | **Remove or re-scope the winning `!important`.** Adding another rule does nothing unless it also carries `!important` — which is the exact ratchet the rebuild is trying to stop. |
| `rule-no-op` | A rule targets it, but its declared value resolves to the value the element already has. | **Change the value.** Specificity is irrelevant. |

Zero `rule-no-op` cases survived into the final numbers; the split is 62 losing / 5 missing.

### 1.4 Corpus and settings

- Routes: `/`, `/about/`, `/speaking/`, `/services/`, `/work/`, `/blog/`, `/photography/`, `/contact/`. `/writing/` 301s to `/blog/` (`curl -sS -o /dev/null -w '%{url_effective}' -L https://kriskrug.co/writing/`), so it is one route, not two.
- Viewport 1440×900, `colorScheme: light`, `prefers-reduced-motion: no-preference` for the primary run (see §6 for why that default matters), captured 2026-07-25T19:14Z.
- CSS surface per route as loaded: 23 stylesheets on `/`, **all readable**, containing **98 distinct interaction rules** — 83 from the Jetpack Boost concatenated bundle (`78b2cf14fa.min.css`, 138,229 bytes, md5 `8dad4baf6c2e420e8cb83000247f75fd`, which carries all five front-end theme sheets), 6 from `global-styles-inline-css` generated from `theme.json`, and 9 from other WordPress inline block styles.
- Images are fulfilled locally with a 1×1 PNG so layout is not distorted by broken-image boxes; fonts and media are aborted. Neither affects computed interaction states.

### 1.5 Internal consistency check

The per-element pass and the keyboard pass are independent code paths. They agree exactly:

| | Value |
|---|---|
| Elements in the inventory with `tabIndex >= 0` | **438** |
| Tab stops reached by pressing Tab | **438** |
| Tab stops that could not be matched back to an inventory element | **0** |
| Tab stops matching `:focus-visible` | **438 / 438** |

### 1.6 Honest limits

- **One viewport.** 1440×900 only. A mobile pass is not covered; note that the markup contains **zero** `<button>` elements (§3), so there is no nav toggle to miss, but a mobile run should still be done before #424 is closed.
- **No JavaScript from the live origin executes.** Theme JS is mirrored and served locally, but anything fetched from a third-party origin does not run. `micro-interactions.js` attaches one `mousemove` handler for a card-tilt effect (`theme/kk-aurora/assets/js/micro-interactions.js:26`); that is a JS-driven affordance this CSS-focused probe does not score.
- **Logged out only.** No admin bar, no editor canvas. The editor's divergent stylesheet set (rebuild plan §1.2) is out of scope here.
- **`:hover` on touch devices** is not modelled. Every hover finding below should be read as "pointer users."
- The **eight main-nav routes only**. Single posts, archives, and 404 are not covered; `/blog/` is the only archive sampled.

---

## 2. Summary — the inventory

| Route | interactive elements | own `:hover` | hover on a descendant | hover inherited from a card | **no hover** | `:focus-visible` ring | **no focus** | tab stops | stops with no visible ring |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `/` | 76 | 64 | 0 | 0 | **12** | 76 | 0 | 66 | 0 |
| `/about/` | 55 | 45 | 4 | 0 | **6** | 55 | 0 | 44 | 0 |
| `/speaking/` | 55 | 45 | 4 | 0 | **6** | 55 | 0 | 44 | 0 |
| `/services/` | 48 | 42 | 0 | 0 | **6** | 48 | 0 | 42 | 0 |
| `/work/` | 63 | 49 | 8 | 0 | **6** | 63 | 0 | 48 | 0 |
| `/blog/` | 208 | 115 | 0 | 75 | **18** | 208 | 0 | 108 | 0 |
| `/photography/` | 47 | 41 | 0 | 0 | **6** | 47 | 0 | 41 | 0 |
| `/contact/` | 52 | 45 | 0 | 0 | **7** | 52 | 0 | 45 | 0 |
| **All 8** | **604** | **446** | **16** | **75** | **67** | **604** | **0** | **438** | **0** |

"hover inherited from a card" means the element has no hover rule of its own but sits inside a probed ancestor that does — hovering the card lights the card, and the title inside it is part of that affordance, so it is not a gap. All 75 are `.aurora-writing-card` internals on `/blog/`.

Cause split for the 67 gaps: **62 `rule-loses-cascade`, 5 `rule-missing`, 0 `rule-no-op`.**

Full per-route element tables are in §8.

---

## 3. What is actually on these pages

Worth stating plainly, because it changes what "shared interaction styles cover links, buttons, cards, and pills" has to mean:

```
grep -c '<form\|<input\|<textarea\|<select\|<button' over all 8 mirrored routes  ->  0
```

**There are no form controls and no native `<button>` elements on any of the eight main-nav routes.** Every "button" on this site is an `<a>` carrying `.aurora-button`, `.kk-contact-button`, `.kk-services-button`, or `.kkx-btn`. The newsletter CTA is an outbound link to Beehiiv, not an embedded form. The contact page has no form; it offers a `mailto:` link and two link-buttons.

Two consequences for step 4:

1. The **form-field half of #424's scope is currently untestable and unshippable on these routes.** The theme's nine `.aurora-form-*` classes are among the dead code PR #468 identified, and `.aurora-search-form … button:hover` is on the dead-rule list in §5. Writing form-field interaction primitives now would be writing code with no consumer.
2. The **button primitive must be authored for `<a>` first**, not for `<button>`. A primitives layer keyed on `button, input[type=submit]` would style nothing on this site.

There are also no `[role="button"]`, `[role="link"]`, `[tabindex]`, or `[contenteditable]` elements. The interactive surface is: **anchors, and card/tile containers that wrap anchors.** That is a small, tractable vocabulary — which is good news for a shared layer.

---

## 4. Focus states (WCAG 2.4.7) — ranked first, as the issue requires

### 4.1 The result

**All eight routes pass a keyboard tab-through with a visible focus indicator on every stop.** 438 of 438 stops matched `:focus-visible` and rendered a solid 2px outline. Zero stops rendered `outline-style: none` with no `box-shadow` replacement. Zero stops were on hidden or zero-size elements.

### 4.2 The three `outline: none` declarations, and why none of them is a defect

The issue asks specifically for outlines suppressed without an equal-or-better replacement. The theme contains three suppressions. All three are covered:

| # | Where | Declaration | Covered by | Verdict |
|---|---|---|---|---|
| 1 | `style.css:125` (live and repo) | `:focus-visible { outline: none; box-shadow: var(--focus-ring) }` | Declares its own replacement (`--focus-ring` = `0 0 0 2px #efe6d2, 0 0 0 4px #b53c18`), and its `outline: none` is in turn overridden by #2 and #3, both later in the cascade at equal or higher specificity | **Not a defect** — a replacement is declared *and* the suppression loses |
| 2 | `bleeding-edge.css:416` | `:focus { outline: none }` | `bleeding-edge.css:420` `:focus-visible { outline: 2px solid var(--wp--preset--color--signal); outline-offset: 3px }` | **Not a defect** — this is the correct `:focus` / `:focus-visible` split; mouse clicks get no ring, keyboard does |
| 3 | `revive-port.css:132–160` (repo `:138–166`) | R2 "cream-safe focus rings" block, `outline: 2px solid var(--revive-accent-text) !important; box-shadow: none !important` | Itself — it *is* the replacement, and it explicitly cancels #1's box-shadow | **Not a defect** |

The comment on #3 reads *"must win over dark-theme outline:none"*, which is exactly what it does. This is the one place in the whole stylesheet where the `!important` war is being fought **for** accessibility rather than against it.

`--focus-ring` itself is one of the 24 custom properties the rebuild plan §1.4 flags as declared twice: `style.css:56` sets it with `#d94a1f`, `revive-port.css:60` redeclares it with `--revive-accent-text`. The measured computed value is the second one. The ring people actually see is decided by which of two identical token declarations loads last.

### 4.3 Which ring lands where

Measured, not inferred:

| Ring | Source | Elements | Contrast range vs the surface behind it |
|---|---|--:|---|
| `2px solid rgb(181,60,24)` @3px offset | `revive-port.css:132` R2 block, `--revive-accent-text` `#b53c18` | **400** | 3.19 – 4.67:1 |
| `2px solid rgb(217,74,31)` @3px offset | `bleeding-edge.css:420` fallback, `--wp--preset--color--signal` `#d94a1f` | **196** | 3.11 – 4.76:1 |
| `2px solid rgb(23,19,16)` @2px offset | `revive-port.css` skip-link block, `--revive-ink` | **8** | 14.88:1 |

The split is structural and worth knowing before step 4 touches it: the R2 block's selector is `body.aurora-theme :where(a, button, input, select, textarea, summary, .aurora-button, .wp-block-button__link, .aurora-primary-nav a, .aurora-utility-link, .aurora-header-cta, .aurora-brand):focus-visible`. That is an **allowlist**. Anchors match it; card and tile *containers* (`article`, `section`, `nav`, `figure`, `div`, `h2`) do not, and fall through to the `bleeding-edge.css` catch-all.

The consequence is measurable and nobody designed it. Because the R2 block also carries `box-shadow: none !important`, allowlisted elements get **a single 2px outline**, while the 196 non-allowlisted containers keep `style.css:127`'s `box-shadow` as well and get **a double indicator** — outline *plus* a 2px cream + 2px accent shadow ring:

| | Allowlisted (anchors, 400) | Not allowlisted (containers, 196) |
|---|---|---|
| `outline` | `2px solid #b53c18` @3px | `2px solid #d94a1f` @3px |
| `box-shadow` | `none` (forced) | `rgb(239,230,210) 0 0 0 2px, rgb(181,60,24) 0 0 0 4px` |

Two rings, two colours, two thicknesses, one accidental boundary. Since every real tab stop today is an anchor (§1.5), the visible effect is nil — but the moment any container becomes focusable, it silently gets the other treatment. **One ring token, applied without an allowlist, is the step-4 deliverable this implies.**

### 4.4 A contrast trap worth recording

The primary CTA `a.aurora-button.aurora-button-primary` appears on all eight routes and first measured at **1.37:1** — which would have been the headline finding of this document. It is a false positive, and the reason is instructive.

The ring is `#b53c18` and the button's fill is `#d94a1f`. Measuring the ring against the *element's own* background gives 1.37:1. But `outline-offset` is `3px`, so the ring is painted in the gap **outside** the border box, on the cream page (`#efe6d2`), which gives **4.67:1**. WCAG 1.4.11 asks about adjacent colours, and both of this ring's neighbours are cream.

The probe now picks the baseline from `outline-offset`: positive offset measures against the ancestor background; zero or negative measures both and takes the worse. **After the fix, zero rings on the site fall below 3:1** (minimum 3.11:1). Anyone re-running this check by hand should be aware that measuring an offset ring against its own element manufactures failures.

### 4.5 The one focus state that *is* broken

`.aurora-footer-tile:hover, .aurora-footer-tile:focus-within` (live `style.css:2711`) is killed by `!important` — see §5.1. The `:hover` half is the visible symptom, but the `:focus-within` half is the accessibility one: **tabbing into a footer tile produces no container-level feedback on any of the eight routes.** The link inside still gets its own ring, so this does not fail 2.4.7 — but it is the only measured case where a keyboard-relevant state rule exists, matches, and is switched off. It belongs at the top of the step-4 list for that reason.

---

## 5. Hover gaps, ranked

### 5.1 `.aurora-footer-tile` — 48 instances, all 8 routes, cascade loss

The largest single gap on the site, and the cleanest example of the pattern.

```css
/* live style.css:2700 — base */
.aurora-footer-tile { background: rgba(247,247,242,0.035); border: 1px solid var(--aurora-line); … }

/* live style.css:2711 — the state */
.aurora-footer-tile:hover,
.aurora-footer-tile:focus-within { background: rgba(247,247,242,0.05); border-color: var(--aurora-line-strong); }

/* live revive-port.css:900 — the killer */
.aurora-footer-tile { border-color: var(--revive-line) !important; background: transparent !important; }
```

The Revive port pinned the tile's **rest** background and border with `!important`. Because the `:hover` / `:focus-within` rule is not `!important`, it can never win, no matter that it is more specific in intent. Measured: forced hover leaves `background-color` at `rgba(0,0,0,0)` and `border-top-color` at `rgba(23,19,16,0.14)` — identical to rest. The declared hover value resolves to `rgba(247,247,242,0.05)`, so the rule genuinely wants to change something.

Worth noting for step 4: `rgba(247,247,242,0.05)` is a *dark-theme* hover — a near-white wash at 5% opacity, designed to sit on a dark panel. On cream it would be close to invisible even if it won. **The fix is not to restore this rule; it is to author a cream-native tile hover in the primitives layer and delete both sides of the fight.**

### 5.2 `.aurora-feed-link-grid a` (×8) and `.aurora-writing-pagination a` (×4) on `/blog/` — cascade loss

```css
/* live style.css:1627 — the state, covering BOTH hover and focus */
.aurora-feed-link-grid a:hover,
.aurora-feed-link-grid a:focus-visible { background: rgba(200,255,61,0.08); border-color: rgba(200,255,61,0.35); }

/* live style.css:1570 */
.aurora-writing-pagination a:hover,
.aurora-writing-pagination .page-numbers.current { background: rgba(247,247,242,0.06); }

/* live style.css:4459 AND live style.css:4490 — the killer, declared twice */
body.aurora-theme :where(.aurora-writing-pagination a, …, .aurora-feed-link-grid a) {
  background-color: var(--aurora-panel-solid) !important;
  border-color: var(--aurora-line-strong) !important;
  color: var(--aurora-ink) !important;
  -webkit-text-fill-color: currentColor !important;
}
```

The "Aurora 1.4.0 cream contrast" block at the end of `style.css` pins background, border, **and colour** on the rest state with `!important`, twice, at two different specificities. It takes out the hover rule, the `:focus-visible` background rule, and WordPress's own `a:hover` (which would otherwise supply colour + underline from `global-styles-inline-css`). Measured: nothing changes on hover — colour, background, and border are all identical to rest.

`rgba(200,255,61,0.08)` is acid green — another dark-theme leftover that should not be restored as-is.

This is the mechanism the rebuild plan predicts in §2.4, caught in the act: **a contrast fix, applied late and with `!important`, silently deleted three interaction states as a side effect.** Nothing in the process noticed, because a contrast fix is not expected to change hover.

### 5.3 `.aurora-section-head a` — 2 instances on `/`, cascade loss, *not* an `!important` fight

The "Photography →" and "Full index →" section links.

```css
/* live revive-port.css:557 */
.aurora-section-head a { color: var(--revive-ink); text-decoration: none; border-bottom: 1px solid var(--revive-accent); … }
```

There is no `:hover` rule for this component anywhere. The only matching hover rule is WordPress's own, from `theme.json`:

```css
:root :where(a:where(:not(.wp-element-button)):hover) { color: var(--wp--preset--color--signal); text-decoration: underline; }
```

That selector's specificity is `(0,1,0)` — `:root` plus a zero-weight `:where()`. The theme's base rule is `(0,1,1)`. **The base rule outranks the hover rule by one class, with no `!important` involved at all.** Measured: colour and border-bottom identical on hover.

This is a distinct failure mode from §5.1/§5.2 and it matters for step 4's design: **not every lost state is an `!important` casualty.** Any component rule written as `.component a { color: … }` with no matching `.component a:hover` silently defeats WordPress's default link hover. A primitives layer must either supply the hover for every component that styles a link, or keep component link rules at a specificity WordPress's default can still beat.

**Relation to #470:** that issue is fixing `.aurora-section-head a`'s *rest* contrast (~1.05:1). This is a different defect on the same selector — its *hover* state. They should be fixed together, and #470's fix should not be considered to have closed this. Flagging so the two are not double-counted or, worse, one assumed to cover the other.

### 5.4 `.aurora-service-card` — 3 instances on `/`, rule missing

Genuinely no `:hover` rule anywhere in any loaded sheet. `revive-port.css` styles `.aurora-service-card`, `::before`, `h3`, `p`, `.aurora-service-meta`, and `a` — six rules, no state. The card wraps a link, so the link inside responds; the card does not. Clean primitives-layer win.

### 5.5 `.kk-contact-card` — 1 instance on `/contact/`, rule missing

Same shape, but this is **Track A page-content CSS**, not theme CSS — it ships from inside the page's own `<style>` block, one of the six the rebuild plan's §3 step 7 retires. Its hover should be authored as part of that migration, not patched in the content block, or it will just be deleted twice.

### 5.6 `div.aurora-writing-actions` — 1 instance on `/`, rule missing (low value)

A `wp-block-buttons` layout wrapper the probe picked up because its class list contains "button". It contains buttons that do have hover states. **Not a real gap** — recorded for completeness and so a future re-run does not treat it as a regression.

---

## 6. Reduced motion deletes 16 hover affordances

The primary run uses `prefers-reduced-motion: no-preference`, which is what most visitors get. Re-running with `--reduced-motion` and diffing element-for-element:

| Component | Instances losing hover | Routes |
|---|--:|---|
| `article.aurora-media-card` | **16** | `/about/`, `/speaking/`, `/work/` |

Mechanism, verified at source:

```css
/* live style.css:1194 — the only hover affordance this card has */
.aurora-media-card:hover img { filter: saturate(1.12); transform: scale(1.035); }

/* live style.css:4380, inside @media (prefers-reduced-motion: reduce) */
.aurora-media-card:hover img, .aurora-writing-card:hover, … , .aurora-button:hover { transform: none; }
```

The card's affordance is a 3.5% image scale. The reduced-motion block cancels the transform — correctly, motion should be reduced. The companion `filter: saturate(1.12)` should have survived as a static fallback, but it does not land either: the image's computed `filter` reads `blur(0px)` in **both** rest and hover, so something later in the cascade is already overriding it. The net result for a reduced-motion user is **a card with no hover feedback at all**.

Fourteen other selectors share that `transform: none` rule. Only the media card was measured losing its hover entirely — the rest either carry a non-motion affordance as well, or (per §7) render on none of these eight routes, so they were not exercised.

This is the correct pattern stated wrongly: reduced motion should *substitute* a static affordance (border, background, underline), not subtract the only one. A primitives layer is exactly the right place to guarantee "every interactive component has at least one non-motion state change."

**Methodological note for anyone re-running this:** the rebuild plan §4.3 recommends forcing `prefers-reduced-motion: reduce` for screenshot determinism. That is right for visual regression and **wrong for an interaction audit** — under `reduce` the media card scores as a hover gap for everyone. The probe therefore defaults to `no-preference` and takes reduced motion as an explicit second pass.

---

## 7. Dead interaction CSS

Of **98** distinct interaction rules in the CSS actually served to these routes, **27 (27.6%) match zero elements** on any of the eight. Measured per route with `document.querySelectorAll()` on the state-stripped selector (pseudo-elements stripped before matching, so `.x:hover::after` is counted against `.x`), then unioned.

These must not be inventoried as coverage, and they should not be migrated into the primitives layer — they should be deleted at rebuild step 6.

| Dead interaction rule | Sheet |
|---|---|
| `.aurora-article-map a:hover` | Boost bundle |
| `.aurora-article-map a:hover, .aurora-article-map a:focus-visible` | Boost bundle |
| `.aurora-article-map:hover, .aurora-article-map:focus-within, .aurora-author-panel:hover, .aurora-author-panel:focus-within, …` | Boost bundle |
| `.aurora-article-meta a:hover` | Boost bundle |
| `.aurora-badge:hover` | Boost bundle |
| `.aurora-button-press:active` | Boost bundle |
| `.aurora-card-gradient:hover::before` | Boost bundle |
| `.aurora-card-lift:hover` | Boost bundle |
| `.aurora-featured-media:hover, .aurora-featured-media:focus-within` | Boost bundle |
| `.aurora-featured-media:hover::after, .aurora-featured-media:focus-within::after, .aurora-article-map:hover::after, …` | Boost bundle |
| `.aurora-footer-nav a:hover` | Boost bundle |
| `.aurora-hero-headline:hover` | Boost bundle |
| `.aurora-hired-grid article:hover, .aurora-hired-grid article:focus-within` | Boost bundle |
| `.aurora-inline-link:hover` | Boost bundle |
| `.aurora-link-slide:hover::after` | Boost bundle |
| `.aurora-link:hover::after` | Boost bundle |
| `.aurora-path-row a:hover` | Boost bundle |
| `.aurora-photo-image img:focus-visible, .aurora-photo-tile:focus-within` | Boost bundle |
| `.aurora-photo-tile:hover, .aurora-photo-tile:focus-within` | Boost bundle |
| `.aurora-proof-row a:hover` | Boost bundle |
| `.aurora-related-row:hover, .aurora-related-row:focus-within` | Boost bundle |
| `.aurora-related-row:hover::before, .aurora-related-row:focus-within::before` | Boost bundle |
| `.aurora-search-form .wp-block-search__button:hover, .aurora-theme .wp-block-search__button:hover, .aurora-form button:hover` | Boost bundle |
| `.wp-block-button.is-style-aurora-primary .wp-block-button__link:hover` | Boost bundle |
| `::-webkit-scrollbar-thumb:hover` | Boost bundle |
| `.has-drop-cap:not(:focus)::first-letter` | WP `wp-block-paragraph-inline-css` |
| `body.rtl .has-drop-cap:not(:focus)::first-letter` | WP `wp-block-paragraph-inline-css` |

Two cross-checks against PR #468's findings:

- `.aurora-photo-tile:hover` is dead **on `/photography/`** — the photography page renders `a.kkx-btn` and pack-authored markup, not `.aurora-photo-tile`. This is consistent with #468's dead-class list.
- The `.aurora-writing-archive .aurora-writing-card:hover…` override layer that the rebuild plan §1.5 flags as a sixth duplicate definition **does match** on `/blog/` — the archive wrapper class is present. It is redundant, not dead. Worth correcting the expectation before step 5 deletes it as unused.

`::-webkit-scrollbar-thumb:hover` and the two `has-drop-cap` rules are not defects; they are listed for completeness because the census counts them.

---

## 8. Per-route inventory

Elements are grouped by tag + theme-authored classes and by verdict, so a row reading `× 17 yes` and a row reading `× 2 none` for the same selector means those two instances genuinely behave differently. WordPress-generated classes (`wp-*`, `post-1234`, `type-post`, `tag-*`, `has-*`, `is-*`) are stripped from signatures; wrappers whose entire class list is WordPress-generated are excluded as template artefacts rather than components.

"ring contrast" is the lowest value measured in that group, against the surface the ring is painted on (§4.4).

### `/` — 76 interactive elements, 66 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.aurora-service-card` | card | 3 | **none** | theme-ring | 4.35 | rule-missing |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a.aurora-work-card` | card-link | 3 | yes | theme-ring | 4.67 |  |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a` | link | 17 | yes | theme-ring | 3.19 |  |
| `a` | link | 2 | **none** | theme-ring | 4.67 | rule-loses-cascade |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 4 | yes | theme-ring | 4.24 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 3 | yes | theme-ring | 4.24 |  |
| `a` | link-button | 1 | yes | theme-ring | 4.67 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `div.aurora-writing-actions` | other | 1 | **none** | theme-ring | 3.42 | rule-missing |

### `/about/` — 55 interactive elements, 44 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.aurora-media-card` | card | 4 | yes (on descendant) | theme-ring | 3.42 |  |
| `div.aurora-card` | card | 1 | yes | theme-ring | 3.42 |  |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a` | link | 4 | yes | theme-ring | 3.11 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.aurora-button` | link-button | 1 | yes | theme-ring | 3.11 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/speaking/` — 55 interactive elements, 44 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.aurora-media-card` | card | 4 | yes (on descendant) | theme-ring | 3.42 |  |
| `div.aurora-card` | card | 1 | yes | theme-ring | 3.42 |  |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a` | link | 4 | yes | theme-ring | 3.11 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.aurora-button` | link-button | 1 | yes | theme-ring | 3.11 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/services/` — 48 interactive elements, 42 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a.kk-services-proof-card` | card-link | 2 | yes | theme-ring | 3.42 |  |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.kk-services-button` | link-button | 1 | yes | theme-ring | 3.42 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/work/` — 63 interactive elements, 48 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.aurora-media-card` | card | 8 | yes (on descendant) | theme-ring | 3.42 |  |
| `div.aurora-card` | card | 1 | yes | theme-ring | 3.42 |  |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a` | link | 8 | yes | theme-ring | 3.11 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.aurora-button` | link-button | 1 | yes | theme-ring | 3.11 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/blog/` — 208 interactive elements, 108 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.aurora-writing-card` | card | 19 | yes | theme-ring | 3.42 |  |
| `div.aurora-writing-card-body` | card | 19 | inherited from card | theme-ring | 4.76 | via `article.aurora-writing-card` |
| `div.taxonomy-category.aurora-writing-card-category` | card | 19 | inherited from card | theme-ring | 4.76 | via `article.aurora-writing-card` |
| `h2.aurora-writing-card-title` | card | 19 | inherited from card | theme-ring | 4.76 | via `article.aurora-writing-card` |
| `figure.aurora-writing-card-media` | card | 18 | inherited from card | theme-ring | 4.76 | via `article.aurora-writing-card` |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a` | link | 56 | yes | theme-ring | 3.48 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 2 | yes | theme-ring | 3.44 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 12 | **none** | theme-ring | 4.67 | rule-loses-cascade |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/photography/` — 47 interactive elements, 41 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a` | link | 1 | yes | theme-ring | 3.42 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.kkx-btn` | link-button | 1 | yes | theme-ring | 3.11 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

### `/contact/` — 52 interactive elements, 45 tab stops

| Element | Category | n | `:hover` | `:focus-visible` | ring contrast | note |
|---|---|--:|---|---|--:|---|
| `article.kk-contact-card` | card | 1 | **none** | theme-ring | 3.42 | rule-missing |
| `section.aurora-footer-tile.aurora-footer-tile-brand` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `section.aurora-footer-tile.aurora-footer-tile-newsletter` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-projects` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-site` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-utility` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `nav.aurora-footer-tile.aurora-footer-tile-social` | card | 1 | **none** | theme-ring | 3.11 | rule-loses-cascade |
| `a` | footer-link | 2 | yes | theme-ring | 4.24 |  |
| `a.skip-link` | link | 1 | yes | theme-ring | 14.88 |  |
| `a` | link | 1 | yes | theme-ring | 3.11 |  |
| `a.kk-contact-email` | link | 1 | yes | theme-ring | 3.11 |  |
| `a.kk-contact-button` | link-button | 2 | yes | theme-ring | 3.11 |  |
| `a.kk-contact-button.secondary` | link-button | 2 | yes | theme-ring | 3.11 |  |
| `a.aurora-button.aurora-button-secondary` | link-button | 2 | yes | theme-ring | 4.24 |  |
| `a.aurora-button.aurora-button-primary` | link-button | 1 | yes | theme-ring | 4.24 |  |
| `a` | nav-link | 30 | yes | theme-ring | 4.24 |  |
| `a.aurora-brand` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-utility-link` | nav-link | 1 | yes | theme-ring | 4.67 |  |
| `a.aurora-button.aurora-button-primary.aurora-header-cta` | nav-link | 1 | yes | theme-ring | 4.67 |  |

---

## 9. Prioritised gap list for step 4

Ranked by user impact, keyboard-affecting first. Every row is a measured finding above.

| # | Priority | Element / route | Gap | Cause | What step 4 has to do |
|---|---|---|---|---|---|
| 1 | **Keyboard** | `.aurora-footer-tile` `:focus-within` — 6 tiles × 8 routes | Tabbing into a footer tile gives no container feedback | cascade loss to `revive-port.css:900` `background: transparent !important` | Delete the `!important` rest pin; author one cream-native tile surface with `:hover` and `:focus-within` in the primitives layer |
| 2 | **Keyboard** | `.aurora-feed-link-grid a` `:focus-visible` background — 8 links, `/blog/` | The focus *ring* lands, but the intended focus background never does | cascade loss to `style.css:4459` + `:4490` | Same block, same fix; the two duplicate `!important` blocks both have to go |
| 3 | **Keyboard (structural)** | Ring allowlist — site-wide | Two different ring colours (`#b53c18` / `#d94a1f`) depending on whether the element is in `revive-port.css:132`'s `:where()` list | Design accident | One ring token, one rule, no allowlist. Any element that becomes focusable later must inherit it automatically |
| 4 | Pointer | `.aurora-footer-tile` `:hover` — 48 instances, all 8 routes | Largest hover gap on the site | cascade loss | Covered by #1 |
| 5 | Pointer | `.aurora-feed-link-grid a` + `.aurora-writing-pagination a` — 12 instances, `/blog/` | Pagination and category links are inert to the pointer | cascade loss | Covered by #2 |
| 6 | Pointer | `.aurora-section-head a` — 2 instances, `/` | No hover; WordPress's default link hover is defeated by base-rule specificity, **no `!important` involved** | cascade loss (specificity) | Give the component an explicit hover; coordinate with #470, which is fixing the same selector's rest contrast |
| 7 | Reduced motion | `.aurora-media-card` — 16 instances, 3 routes | Only affordance is a transform, and reduced motion removes it | motion-only affordance | Guarantee a non-motion state change per component; make the reduced-motion block *substitute*, not subtract |
| 8 | Pointer | `.aurora-service-card` — 3 instances, `/` | No hover rule at all | rule missing | Card primitive |
| 9 | Pointer | `.kk-contact-card` — 1 instance, `/contact/` | No hover rule at all | rule missing | Card primitive — but land it with rebuild step 7 (Track A page-content CSS), not before |
| 10 | Hygiene | 27 dead interaction rules | 27.6% of the interaction surface matches nothing | dead code | Delete at step 6; do not migrate |
| — | None | `div.aurora-writing-actions` | Probe artefact, not a gap | — | No action |

**The one-line brief for step 4:** the interaction layer this site needs is not mostly new rules. It is **one ring token and one hover token applied to a vocabulary of roughly six components (link, link-button, card, tile, nav-link, pill), delivered together with the deletion of the four `!important` rest-state blocks that are currently switching the existing states off.** If step 4 adds primitives without removing those blocks, 62 of the 67 measured gaps will still be there afterwards.

---

## 10. Does the sequencing behind step 4 still hold?

**Yes, and the evidence strengthens it.** Recorded here because the task asked me to say so if I disagreed.

Three reasons from the measurements:

1. **92.5% of the gaps cannot be fixed by adding CSS.** They are cascade losses to `!important` on rest states. Shipping #424 as a standalone patch today would mean either adding `!important` to the state rules — the exact ratchet §1.1 of the rebuild plan shows doubled the count between 2026-07-19 and 1.4.3 — or writing longer selectors. Both are debt the rebuild then has to unwind. The rules that need deleting live in the same two blocks step 4 is already rewriting.
2. **The primitives vocabulary is now known and it is small.** Six component shapes, all anchors or anchor-wrapping containers, zero form controls (§3). That is a concrete, measured input to `04-primitives.css` that did not exist before this audit — which is exactly what the plan predicted the audit would produce.
3. **The urgent half is already done.** The plan's implicit worry is that keyboard users are stranded. Measured: they are not. 438/438 tab stops have a visible ring, zero unreplaced outline suppressions, zero rings below 3:1. **There is no accessibility emergency forcing #424 ahead of the rebuild.** The one keyboard-relevant defect (`:focus-within` on footer tiles, §4.5) is a cascade loss in the same block as gap #1, so it is fixed by the same edit.

One caveat that is **not** an argument for resequencing but should be tracked: gap #9 (`.kk-contact-card`) lives in Track A page-content CSS and is bound to step 7, not step 4. If #424 is closed on step 4 alone, that one instance stays open. It should be listed on step 7's checklist rather than held against step 4.

---

## 11. Reproducing this

```bash
# 1. full capture + audit (mirrors live, ~6 min)
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node scripts/interaction_state_probe.js --out /tmp/probe

# 2. reduced-motion comparison run for section 6
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node scripts/interaction_state_probe.js --out /tmp/probe-rm --skip-mirror --reduced-motion

# 3. dead-class cross-check against the same mirrored corpus (PR #468's script)
python3 scripts/css_coverage_audit.py --live-corpus /tmp/probe/mirror --min-confidence high

# 4. live/repo parity, section 1.2
curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -m1 -i '^Version'
```

`probe.json` carries every measurement behind every number here: per element, the rest / hover / focus computed styles, every state rule that matched it with each declaration's resolved value, and the full ordered tab-stop list per route. It is ~15 MB per run and is **not committed** — regenerate it, do not archive it (#318).

**Cross-check this document against the theme itself with:**

```bash
sed -n '2700,2716p' theme/kk-aurora/style.css              # footer tile base + state
grep -n 'aurora-footer-tile' theme/kk-aurora/assets/css/revive-port.css   # the !important pin
sed -n '4459,4470p' theme/kk-aurora/style.css              # the cream-contrast override block
sed -n '416,424p'  theme/kk-aurora/assets/css/bleeding-edge.css           # focus / focus-visible split
```

(Repo is 1.4.4; live line numbers cited in §4–§5 differ by up to 6 lines in `revive-port.css`. §1.2 explains why the findings are identical in both.)
