# Aurora stylesheet rebuild — Path A implementation plan (2026-07-25)

**Status:** Plan of record for [#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423). **Docs only — this commit ships zero CSS, PHP, HTML, or `theme.json` changes.**
**Lane:** Track B (Aurora theme)
**Decision being implemented:** KK, 2026-07-24 — **Path A, ground-up token-based rebuild.** The 2026-07-19 agent memo recommended B/C (incremental); KK overrode to A. This document plans A. It does not re-argue the decision.
**Measured against:** repo `main` @ `0064b4e` (`theme(aurora): 1.4.3 left-pin header and riso accents`), theme `kk-aurora` **1.4.3**.
**Live readback:** 2026-07-25, `https://kriskrug.co`, logged out. All eight key routes HTTP 200.

> **Safety gate carried forward from #423:** the rebuild itself does not land before the visual-regression baseline in §4 exists and its comparison gate is green. Writing this plan is not permission to start the teardown. Every step in §3 is individually revertible and individually KK-gated for the live upload.

---

## 0. How to reproduce every number in this document

All counts were produced on `0064b4e` in a clean worktree. Nothing here is estimated.

| Purpose | Command |
|---|---|
| Line counts | `wc -l theme/kk-aurora/style.css theme/kk-aurora/assets/css/*.css` |
| Byte counts | `find theme/ -name '*.css' -printf '%p %s\n'` |
| `!important` (raw) | `grep -c -o '!important' <file>` |
| Rule blocks, at-rules, tokens, literals | Python pass: strip `/* … */`, count `{`, subtract `@…{` blocks, regex the rest (script in §0.1) |
| Enqueue order | `grep -n 'wp_enqueue_style\|add_editor_style' theme/kk-aurora/functions.php` + read `functions.php:28–154` |
| Inline `<style>` in theme markup | `grep -rn 'style>' theme/kk-aurora/templates/ theme/kk-aurora/parts/ theme/kk-aurora/patterns/` |
| Inline `style=""` attributes | `grep -rno 'style="' theme/kk-aurora/{templates,parts,patterns}/ \| cut -d: -f1 \| sort \| uniq -c` |
| `theme.json` token surface | `python3 -c "import json; d=json.load(open('theme/kk-aurora/theme.json')); …"` |
| Live vs repo CSS identity | `curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/<f> \| md5sum` vs `md5sum theme/kk-aurora/<f>` |
| Live CSS surfaces per route | `curl -sS -L https://kriskrug.co<route>`, then regex `<link rel=stylesheet>` and `<style…>…</style>` |
| Dead-class estimate | Diff of class tokens in theme CSS vs `class="…"` tokens rendered across 10 live routes |

### 0.1 Measurement scripts

The four ad-hoc scripts used (CSS metrics, token overlap, selector duplication + breakpoint census, dead-class diff) were run from a scratch directory and are **not committed** — they are throwaway and fully described by the table above. Step 0 of §3 makes the durable versions of these checks a repo asset (`scripts/css_inventory.py` + `make css-inventory`) so the rebuild has a regression-proof metric, rather than a one-off audit.

---

## 1. Measured current-state inventory

### 1.1 The six CSS files

| File | Bytes | Lines | Rule blocks | At-rule blocks | `@media` | `!important` | Custom-prop decls | `var()` uses | Hex literals | `px` literals |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `style.css` | 111,255 | **4,519** | 613 | 18 | 15 | **71** | 80 | 474 | 57 | 270 |
| `assets/css/revive-port.css` | 27,630 | **1,164** | 141 | 10 | 9 | **83**¹ | 58 | 147 | 30 | 48 |
| `assets/css/typography-refined.css` | 16,735 | **685** | 70 | 11 | 5 | **6** | 0 | 81 | 0 | 19 |
| `assets/css/bleeding-edge.css` | 12,390 | **561** | 73 | 17 | 3 | 0 | 12 | 42 | 7 | 31 |
| `assets/css/animations.css` | 7,540 | **352** | 66 | 13 | 2 | 0 | 2 | 7 | 0 | 19 |
| `assets/css/editor.css` (editor only) | 5,343 | **175** | 27 | 0 | 0 | **1** | 14 | 32 | 8 | 12 |
| **Total** | **180,893** | **7,456** | **990** | **69** | **34** | **161** | **166** | **783** | **102** | **399** |
| **Front-end subtotal** (5 files) | 175,550 | 7,281 | 963 | 69 | 34 | 160 | 152 | 751 | 94 | 387 |

¹ 83 raw occurrences; 82 in live code, 1 inside a comment. Every other file's raw and code-only counts agree.

**Change since the 2026-07-19 memo.** Re-measured at `33887e7c` (`docs: record site-redesign batch that seeded epic #403`, the last commit before that memo was posted):

| | 2026-07-19 (`33887e7c`) | 2026-07-25 (`0064b4e`) | Δ |
|---|---:|---:|---:|
| CSS files | 5 | 6 | +1 |
| Total lines | 6,219 | 7,456 | **+20%** |
| `!important` in CSS files (code-only)² | **79** | **160** | **+103%** |
| `!important` in `style.css` | 72 | 71 | −1 |
| `!important` in theme markup (`front-page.html`) | 24 | 0 | −24 |

Reproduce: `git show 33887e7c:theme/kk-aurora/<file> \| grep -c -o '!important'`. The memo's own figure (6,219 lines / 5 files / 72 in `style.css`) reproduces exactly, so the comparison is like-for-like.

² **Counting note.** The growth row compares *code-only* counts on both sides. Today's raw grep total is **161**, of which one is inside a comment (`revive-port.css:1062`), giving **160** real declarations — the figure the #256 audit (PR #468) reports independently. At `33887e7c` no `!important` appeared in a comment in any file, so **79** is both its raw and code-only count. Comparing today's raw 161 against that 79 would overstate the growth slightly; 79 → 160 is the honest like-for-like figure. Elsewhere in this document the per-file table reports raw counts with the discrepancy footnoted at ¹.

The 1.4.0–1.4.3 Revive port added the sixth file and **more than doubled `!important` site-wide**, because the Revive brand layer overrides the 2026 layer rather than replacing it. Meanwhile the incremental approach did work where it was applied — `style.css` went down by one and the front-page inline block was deleted outright. But the net moved sharply the wrong way. **The debt is growing, not shrinking.** That is the strongest single argument for A over B, and the data did not exist when the B/C recommendation was written.

### 1.2 Enqueue and load order — `theme/kk-aurora/functions.php`

Six `wp_enqueue_style` calls plus two `add_editor_style` calls. Version string on all of them is `KK_AURORA_VERSION` = `'1.4.3'` (`functions.php:21`).

| # | Hook | Handle | Source | Declared deps | Line |
|---|---|---|---|---|---|
| 1 | `wp_enqueue_scripts` | `kk-aurora-style` | `get_stylesheet_uri()` → `style.css` | `[]` | 62 |
| 2 | `wp_enqueue_scripts` | `kk-aurora-typography` | `assets/css/typography-refined.css` | `[]` | 70 |
| 3 | `wp_enqueue_scripts` | `kk-aurora-animations` | `assets/css/animations.css` | `[]` | 78 |
| 4 | `wp_enqueue_scripts` | `kk-aurora-bleeding-edge` | `assets/css/bleeding-edge.css` | `[]` | 86 |
| 5 | `wp_enqueue_scripts` | `kk-aurora-revive-port` | `assets/css/revive-port.css` | `['kk-aurora-style','kk-aurora-typography','kk-aurora-animations','kk-aurora-bleeding-edge']` | 94 |
| 6 | `enqueue_block_editor_assets` | `kk-aurora-editor` | `assets/css/editor.css` | `[]` | 147 |
| — | `after_setup_theme` | `add_editor_style('style.css')` | editor canvas | — | 53 |
| — | `after_setup_theme` | `add_editor_style('assets/css/editor.css')` | editor canvas | — | 54 |

**The finding that matters:** handles 1–4 declare **no dependencies at all**. Their cascade position is an accident of registration order, not a contract. Only handle 5 declares deps, and it does so specifically to force itself last — the comment on line 93 says so out loud (`"loads last among theme styles"`). That is the whole load-order design: four unordered sheets and one that shoves itself to the end. There is no layer model to reason about, which is why overriding anything requires either a longer selector or `!important`.

**Editor divergence:** the editor canvas loads `style.css` + `editor.css` and **not** `typography-refined.css`, `animations.css`, or `revive-port.css`. The editor therefore renders the pre-Revive dark palette while the front end renders cream/ink. Any rebuild must fix this or the block editor keeps lying to whoever edits a page.

### 1.3 Inline `<style>` blocks in theme markup

Exactly **one**, and it is not on any key route:

| File | Lines | CSS lines | Rendered where |
|---|---|---|---|
| `theme/kk-aurora/parts/marquee-current.html` | 61 total | **49** (lines 3–51) | Only where the `kk-aurora/marquee-hero` pattern is inserted (`marquee_board` posts). `grep -c 'kkm' ` on the rendered homepage returns **0**. |

`templates/*.html` — **zero** `<style>` blocks. `parts/*.html` — one (above). `patterns/*.php` — zero.

**This contradicts the 2026-07-19 memo**, which said `templates/front-page.html` also carried a `<style>` block. It did; commit `819f182` (the 1.4.0 Revive port) deleted it — a 306-line rewrite that removed a `@media (max-width: 700px)` mobile-overflow block containing its own `!important` run. Re-verified: `git log -S'<style>' -- theme/kk-aurora/templates/front-page.html`.

`marquee-current.html` is a **generated** file (header line 1: `GENERATED by scripts/marquee/build.py`). Its CSS must be migrated at the generator (`scripts/marquee/`), not by hand-editing the partial.

Inline `style=""` attributes in theme markup (46 total): `patterns/hero-gradient.php` 16, `patterns/stats-counter.php` 13, `templates/404.html` 6, `patterns/shop-buy-button.php` 5, `templates/front-page.html` 3, `templates/index.html` 2, `templates/single-marquee_board.html` 1, `templates/archive-marquee_board.html` 1.

### 1.4 `theme.json` token surface vs what is hardcoded in CSS

`theme.json` is schema **version 3** and is already a real token source:

| Group | Count | Examples |
|---|---:|---|
| `color.palette` | 20 | `void`, `paper`, `signal`, `text-primary`, `wildcard`, `cyan`, … |
| `color.gradients` | 6 | `aurora-primary`, `depth-fade`, … |
| `color.duotone` | 2 | |
| `typography.fontFamilies` | 3 | `display`, `body`, `mono` |
| `typography.fontSizes` | 10 | `xs` … `5xl`, `hero`; `fluid: true` |
| `spacing.spacingSizes` | 14 | `10` (0.25rem) … `240` (8rem) |
| `shadow.presets` | 4 | `sm`, `md`, `lg`, `xl` |
| `custom.*` | 9 groups, ~54 values | `animation`, `motion`, `border`, `button`, `focus`, `glass`, `lineHeight`, `letterSpacing`, `zIndex` |
| `layout` | — | `contentSize: 800px`, `wideSize: 1280px` |
| `styles.elements` | 11 | `heading`, `h1`–`h6`, `link`, `button`, `caption`, `cite` |
| `styles.blocks` | 12 | `core/post-title`, `core/quote`, `core/navigation`, … |

The theme CSS consumes **62 distinct `--wp--*` preset tokens**, so `theme.json` is genuinely wired up.

**And then the CSS ignores it and redefines everything.** Across the five front-end sheets there are **114 distinct custom-property names in five competing namespaces**:

| Namespace | Distinct names | Declared in |
|---|---:|---|
| `--aurora-*` | 65 | `style.css`, `revive-port.css`, `bleeding-edge.css` |
| `--revive-*` | 19 | `revive-port.css` |
| `--ease-*` | 5 | `bleeding-edge.css` |
| `--kk-*` | 5 | `revive-port.css` (scoped remap for Track A page packs) |
| `--transition-*`, `--focus-*`, `--input-*`, bare `--bg/--fg/--text/--accent/--muted/--surface/--cyan/--border` | 20 | `style.css`, `revive-port.css` |

Concretely duplicated against `theme.json`:

- `theme.json` `custom.border.radius*` (6 values) vs `style.css` `--aurora-radius-card`, `--aurora-radius-control`.
- `theme.json` `custom.focus.ring*` (5 values) vs `--focus-ring` declared **twice** (`style.css:56`, `revive-port.css:54`) with different values.
- `theme.json` `custom.glass.*` (5 values) vs `--aurora-glass-bg/-blur/-border` in `style.css:27–29`.
- `theme.json` `custom.animation.*` (7 values) vs `--transition-fast/-normal/-slow` in `style.css:51–53` and `--ease-*` in `bleeding-edge.css`.
- Palette hex is re-hardcoded: `style.css:493–519` restates `#171310` (= `text-primary`), `#efe6d2` (= `paper`), `#d94a1f` (= `signal`), `#e8b53a` (= `wildcard`) as `--aurora-ink/-paper/-signal/-wildcard`.

**Then it is duplicated a second time.** `revive-port.css:31–54` re-declares **24 custom properties that `style.css` already declares at `:root`** — verbatim names, near-identical values:

```
--aurora-black  --aurora-ink  --aurora-ink-muted  --aurora-ink-soft  --aurora-line
--aurora-line-strong  --aurora-opal-ink  --aurora-opal-plum  --aurora-opal-void
--aurora-opal-warm  --aurora-panel  --aurora-panel-solid  --aurora-paper
--aurora-readable-accent  --aurora-reader-border  --aurora-reader-pane
--aurora-reader-pane-solid  --aurora-shadow-deep  --aurora-signal
--aurora-signal-control  --aurora-signal-control-hover  --aurora-signal-dark
--aurora-wildcard  --focus-ring
```

Every brand color therefore has **three** homes (`theme.json` palette → `--aurora-*` in `style.css` → `--aurora-*` again in `revive-port.css`), plus a fourth scoped remap (`--kk-*` at `revive-port.css:932`, bare `--bg/--fg/--accent` at `revive-port.css:1011`). Changing one brand color today means editing four places and hoping. `theme.json` alone cannot change the site's colors — that is the definition of a broken token system, and it is what Path A exists to fix.

Five `var()` references point at properties declared nowhere in the theme CSS: `--aurora-lux-delay`, `--mouse-x`, `--mouse-y`, `--scroll-progress`, `--service-ribbon`. Four are set by JS at runtime; `--aurora-lux-delay` and `--service-ribbon` need a live check (see §7).

### 1.5 Duplicated / doubled component layers

**The `.aurora-writing-card` doubling flagged on 2026-07-19 still exists**, and has grown a third and fourth pass:

- **84 occurrences of `aurora-writing-card` on 73 lines of `style.css`** (memo said 83 references; re-measured 84 occurrences).
- Base component layer: `style.css:1409–1543`.
- `.aurora-writing-archive .aurora-writing-card` override layer: `style.css:3557–3690` — redefines background, border, hover, focus-within, body, title, excerpt, meta, category, media, and the `:not(:has(…))::before` fallback that the base layer already defined at 1454.
- Breakpoint re-overrides: `style.css:2998–3016` (`@media`), `3174–3207` (`@media`), `4279–4290` (`@media`).
- Motion layer: `style.css:4153`, `4337–4361`, `4378–4379`.

That is one component defined across **six** locations in a single file.

The site-wide picture, measured across the five front-end sheets:

| Metric | Value |
|---|---:|
| Distinct selectors (comma-split) | 1,070 |
| Selectors declared more than once | **317** |
| Redundant declarations (occurrences beyond the first) | **559** |
| Selectors declared in more than one file | **75** |

Worst offenders: `h3` (10×, across 3 files), `.aurora-page-title` (9×, 3 files), `.aurora-card` (8×, 3 files), `.aurora-writing-archive-title` (8×), `h2`/`h4` (7× each, 3 files), `:root` (6×, 3 files).

**Breakpoints have no scale.** 20 distinct `@media` conditions, of which **12 distinct width values**: `max-width` 360, 560, 700, 781, 900, 980, 1180; `min-width` 780, 782, 800, 900, 960. Note 780 / 781 / 782 all exist as separate breakpoints. There is no shared responsive contract to reason about.

**Dead CSS is over half the authored surface.** Cross-referencing every class selector in the five front-end sheets against every `class="…"` token actually rendered on 10 live routes (`/`, `/about/`, `/speaking/`, `/services/`, `/work/`, `/photography/`, `/blog/`, `/contact/`, one single post, one 404):

- 268 theme-authored classes (`aurora-`, `kk-`, `kkm-`, `revive-`, `is-aurora` prefixes) referenced by the CSS.
- **142 (53%) never appear in any rendered markup.** Examples: `.aurora-glass-panel`, `.aurora-card-premium`, `.aurora-form-*` (9 classes), `.aurora-animate-*` (5), `.aurora-badge*`, `.aurora-counter`, `.aurora-epk-grid`, `.aurora-hero-2026`, `.aurora-feature-band*`, `.aurora-featured-strip`.
- Caveat, stated honestly: this over-counts slightly. Some classes are JS-applied state, and template coverage is 10 routes not all routes. Treat 53% as a floor-ish signal, not a precise dead-code figure; §3 step 0 replaces it with real coverage data.

### 1.6 Live-rendered verification (2026-07-25, logged out)

The issue's eval criteria require the inventory to be cross-checked against what actually loads. Done:

**Repo is live.** All six CSS files are **byte-identical** between `theme/kk-aurora/` at `0064b4e` and `https://kriskrug.co/wp-content/themes/kk-aurora/…` (md5 match on all six). Public `style.css` reports `Version: 1.4.3`. **This contradicts `AGENTS.md`**, which still says live 1.3.37 / repo 1.3.40. Live and repo are in sync at 1.4.3. The repo-side inventory above therefore *is* the production inventory — a rare and very useful condition for starting a rebuild.

**Nothing loads as a separate theme stylesheet.** Every one of the eight key routes serves exactly **one** `<link rel=stylesheet>`: `https://s5102.pcdn.co/wp-content/boost-cache/static/78b2cf14fa.min.css` — Jetpack Boost's concatenated, minified bundle on the Pagely CDN.

| Bundle | Bytes | Rule blocks | `!important` |
|---|---:|---:|---:|
| Boost concatenated `78b2cf14fa.min.css` | 138,225 | 1,032 | 159 |

It contains `revive` 166× and `aurora` 2,103×, confirming all five front-end sheets are inside it.

**Head order on `/` (document byte offsets):**

1. byte 70 — inline `<style id="jetpack-boost-critical-css">`, 7,474 bytes, 1 `!important`
2. byte 12,176 — `<link>` to the Boost bundle (plus a second `media="not all"` async copy at 12,364)
3. bytes 12,674 – 22,492 — 15 WP core block inline styles
4. byte 26,188 — `<style id="global-styles-inline-css">`, **28,067 bytes, 137 `!important`** (generated from `theme.json`)
5. byte 54,301 — `core-block-supports-inline-css`
6. byte 54,798 — `wp-block-template-skip-link-inline-css`

**`theme.json`'s generated global styles print AFTER the theme's entire authored CSS bundle.** At equal specificity, `theme.json` wins. That single ordering fact explains a large share of the 160 authored `!important`s: the theme is fighting its own token layer, one document position too late. A rebuild that does not account for it will simply re-create the problem.

**Per-route CSS surface, logged out:**

| Route | HTTP | HTML bytes | `<link>` sheets | `<style>` blocks | of which page-content (anonymous) | anon bytes | inline CSS total | `!important` in inline |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `/` | 200 | 81,891 | 1 | 18 | 0 | 0 | 49,310 | 146 |
| `/about/` | 200 | 55,387 | 1 | 11 | 1 | 959 | 34,664 | 162 |
| `/speaking/` | 200 | 55,236 | 1 | 11 | 1 | 959 | 34,664 | 162 |
| `/services/` | 200 | 58,989 | 1 | 11 | 1 | 4,418 | 38,123 | 161 |
| `/work/` | 200 | 57,447 | 1 | 11 | 1 | 959 | 34,664 | 162 |
| `/photography/` | 200 | 64,138 | 1 | 11 | 1 | 5,024 | 38,729 | 160 |
| `/blog/` | 200 | 124,850 | 1 | 18 | 0 | 0 | 55,850 | 148 |
| `/contact/` | 200 | 59,492 | 1 | 11 | 1 | 5,422 | 39,127 | 165 |

**The sixth CSS surface nobody has been counting: Track A page-content CSS.** Six of eight routes carry an unattributed `<style>` block injected from page content (`content/source-packs/content-architecture-2026/wp-payloads/*.html` and the R7–R11 packs), 959–5,422 bytes each, 12–17 `!important` each. And they are almost all doing the same thing:

```css
.kk-r9-pack :where(p, li)::first-letter {
  initial-letter: normal !important;
  font-size: inherit !important;
  ...
}
```

That is page content fighting the **theme's drop cap**, which lives at `typography-refined.css:141–165`. A theme decision made once is being defeated by hand, with `!important`, on five separate pages, in content KK's publisher lane has to maintain. Each pack also re-declares the same cream/ink palette a fifth time as `--kk-*` / `--ink` / `--paper` locals. **Any Path A plan that only touches `theme/` leaves this in place.** §3 step 7 addresses it.

**Code Snippets CSS:** the repo-side snapshot (`backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json`, 13 snippets) shows **no active CSS-injecting snippet**. The five active ones are PHP-only: KK Schema (#5), SEO root files (#7), GSC404 canonicalize (#8), KK Asset Diet (#10 — dequeues plugin JS/CSS, injects none), KK News Sitemap (#13). The two CSS contrast hotfixes (#9, #11) are **inactive**. This snapshot predates the creamfix apply and needs a live re-read (§7).

**One live snippet is a rebuild hazard.** Snippet **#14** (`TEMP Aurora 1.4.0 cream contrast file apply`) overwrites `style.css` and `assets/css/revive-port.css` on the production filesystem from media zip **#12631** at `init`. It self-guards on option `kk_aurora_creamfix_140=done` and the deploy handoff says it is now inactive, but it must be **verified retired and the media item deleted before any rebuild upload**, or a stale zip can silently clobber a deployed rebuild. See §5 R-3.

---

## 2. Target architecture

### 2.1 Principles

1. **One token source.** `theme.json` is the only place a design value is *defined*. CSS may read `--wp--preset--*` / `--wp--custom--*`; CSS may not restate them.
2. **Cascade layers replace specificity.** `@layer` gives explicit precedence, so overrides need position, not selector weight or `!important`.
3. **One component, one place.** A component's rules — including its states and its responsive behavior — live in one file, under one layer. No `.parent .component` override layers.
4. **No `!important` in authored theme CSS.** Target and budget: **0**. The one narrow exception is §2.5.
5. **Every step is independently shippable and independently revertible.** No big-bang cutover.

### 2.2 Layer order

Declared once, at the very top of the first-loaded sheet, before any rules:

```css
@layer reset, tokens, base, primitives, components, patterns, utilities, overrides;
```

| Layer | Contains | Source file |
|---|---|---|
| `reset` | box-sizing, margin normalization, media defaults, `prefers-reduced-motion` baseline | `assets/css/01-reset.css` |
| `tokens` | The **only** CSS custom properties: semantic aliases that resolve to `--wp--preset--*` / `--wp--custom--*`, plus the breakpoint scale | `assets/css/02-tokens.css` |
| `base` | Bare-element typography and links (`h1`–`h6`, `p`, `a`, `blockquote`, lists, tables, forms) | `assets/css/03-base.css` |
| `primitives` | Button, card, media, badge, kicker, prose measure, focus ring, surface — the shared vocabulary | `assets/css/04-primitives.css` |
| `components` | One block per named component (writing card, hero, marquee, proof grid, footer bento, …) | `assets/css/05-components.css` |
| `patterns` | Page-scoped composition only where a route genuinely differs | `assets/css/06-patterns.css` |
| `utilities` | Single-purpose helpers (`.u-flow`, `.u-measure`, `.u-visually-hidden`) | `assets/css/07-utilities.css` |
| `overrides` | Quarantine for third-party/plugin fights, each with a dated comment and an owning issue | `assets/css/08-overrides.css` |

Everything **unlayered** beats everything layered. This is the mechanism that solves the §1.6 head-order problem: `theme.json`'s `global-styles-inline-css` prints after the theme bundle, but it is unlayered, so it would still win. The fix is deliberate and documented, not accidental — see §2.4.

### 2.3 What belongs where

| Kind of value | Home | Never |
|---|---|---|
| Brand color, font family, font size, spacing step, shadow, layout width, radius, duration, easing, z-index tier | **`theme.json`** (`settings.color.palette`, `settings.typography`, `settings.spacing`, `settings.custom.*`) | Hardcoded hex/px in a CSS file |
| Semantic alias (`--kk-surface`, `--kk-ink`, `--kk-accent-text`, `--kk-line`, `--kk-measure`) | **`02-tokens.css`**, defined once at `:root` as `var(--wp--preset--color--paper)` etc. | Re-declared in any other file, or re-declared with a literal |
| Component-local variable (`--card-pad`, `--card-radius`) | Inside that component's rule in `05-components.css`, resolving to a semantic alias | At `:root` |
| Bare-element styling | `03-base.css` | `style.css` root + a second pass in a brand layer |
| Anything a block editor user should see | `theme.json` `styles.elements` / `styles.blocks`, so the editor canvas matches | Front-end-only CSS |

**Naming.** One prefix, `kk-`. Components `.kk-<component>`, elements `.kk-<component>__<element>`, modifiers `.kk-<component>--<modifier>`, utilities `.u-<purpose>`, JS-only state hooks `.is-<state>` / `.has-<state>` (never styled from JS-set inline styles). Semantic tokens `--kk-<role>[-<variant>]`. Retire `aurora-`, `revive-`, `kkm-`, and bare `--bg/--fg/--text` entirely — but only at the end of the migration (§3 step 8), so class-name churn never blocks a shipping step.

**Breakpoints.** Three, defined once in `02-tokens.css` and used nowhere else as literals: `--kk-bp-sm: 480px`, `--kk-bp-md: 768px`, `--kk-bp-lg: 1200px`. Mobile-first `min-width` only. The 12 current width values collapse into these three; any genuinely necessary fourth breakpoint gets a comment naming the component that needs it.

### 2.4 Beating `global-styles-inline-css` without `!important`

Measured constraint (§1.6): WP prints `theme.json`'s generated global styles **after** the theme bundle, and that output is unlayered.

The rebuild's answer, in priority order:

1. **Don't fight it — feed it.** If `theme.json` produces the right value, the theme CSS should not restate it at all. Most current fights exist only because CSS restates a token WP already emitted.
2. **Where the theme must win**, keep those rules **unlayered** in a small, explicitly-named `09-late.css` (a handful of rules, each with a comment saying which `global-styles` rule it is answering). Unlayered beats layered, and later-unlayered beats earlier-unlayered — the same result `!important` gives today, with none of the specificity ratchet.
3. **Where WP must win**, do nothing.

Step 1 of §3 spikes and proves this before anything is migrated. If the spike fails, the plan stops and returns to KK rather than reintroducing `!important` by the back door.

### 2.5 The `!important` rule

**Authored theme CSS: zero.** Enforced by a CI check (§3 step 0). One exception, narrowly scoped:

- `08-overrides.css` may use `!important` **only** to override a third-party plugin's own `!important`, and only with an inline comment giving the plugin, the date, and an issue number. Every entry is a tracked debt item.
- The forced-colors / `prefers-contrast` accessibility block may use it where the spec effectively requires it, documented in the same way.

Budget after cutover: **≤ 5 total**, all in `08-overrides.css`, all commented, down from **160**.

### 2.6 Editor parity

`add_editor_style()` must load the same layer stack as the front end (minus `09-late.css`, which answers a front-end-only ordering problem). Fixing the §1.2 divergence — editor currently sees only `style.css` + `editor.css` — is a step-4 deliverable, not an afterthought.

### 2.7 Target shape

| | Now (measured) | Target |
|---|---:|---:|
| Front-end CSS files | 5 | 8 layered + 1 late |
| Front-end CSS lines | 7,281 | ≤ 3,000 |
| Authored `!important` | 160 | ≤ 5 |
| Custom-property namespaces | 5 | 1 (`--kk-*`), all resolving to `--wp--*` |
| Custom-property names | 114 | ≤ 40 |
| Properties declared in ≥2 files | 24 | 0 |
| Selectors declared more than once | 317 | ≤ 40 (states/breakpoints only) |
| Distinct `@media` width values | 12 | 3 |
| Page-content CSS blocks on key routes | 6 routes | 0 |
| `style.css` role | 4,519-line monolith | Theme header + `@layer` declaration + `@import`s only |

---

## 3. Migration sequence

Nine steps. Each is one PR, one lane, individually shippable, individually revertible. **Steps 0–2 ship no visual change at all** — they build the safety net and prove the architecture before anything is torn out. Rollback for every theme step is identical and already proven: re-upload the previous version's zip via Appearance → Themes → Upload → Replace, then purge (see `backup/aurora-deploy-20260724/DEPLOY-HANDOFF.md`). Every step's zip is produced by `make aurora-package LABEL=… ROLLBACK_REF=…`, which records the rollback ref in the package report.

---

**Step 0 — Instrument before touching anything.** *(repo-only, no deploy)*
Land `scripts/css_inventory.py` + `make css-inventory` producing the §1 table as machine-readable JSON, and a CI check that fails on any *increase* in `!important` count or front-end CSS line count. Add real coverage data (Chrome DevTools Coverage or equivalent over the 10 routes) to replace the §1.5 dead-class heuristic.
*Rollback:* revert the commit; nothing shipped.
*Gate:* `make verify` green.

**Step 1 — Freeze the visual-regression baseline.** *(repo-only, no deploy)*
Implement §4 in full: `scripts/visual_baseline.py` + `make visual-baseline` / `make visual-diff`, baseline manifest committed, PNGs not committed. **This is the gate the whole rebuild ships behind.** No later step merges without a green diff.
*Rollback:* revert; nothing shipped.
*Gate:* baseline captured twice on unchanged production and diffs clean (proves the harness is stable before it is trusted).

**Step 2 — Layer + token scaffold, behavior-neutral.** *(deploy: Aurora 1.5.0)*
Add the `@layer` declaration and `02-tokens.css` defining the semantic `--kk-*` aliases over `--wp--*`. Wrap the five existing sheets in `@layer components` wholesale (a single `@layer components { … }` around each file's contents, contents untouched). Prove §2.4 with `09-late.css` on one concrete case. Fix the enqueue graph so every handle declares its dependency explicitly instead of relying on registration order. **Delete no rule, rename no class.**
*Why first:* it is the smallest change that makes every later step cheap, and it is the one step whose visual delta should be exactly zero — so it is also the harness's first real test.
*Rollback:* re-upload 1.4.3 zip.
*Gate:* visual diff 0 changed pixels above tolerance on all 8 routes × 3 viewports.

**Step 3 — Reset + base.** *(deploy: 1.5.1)*
Extract `01-reset.css` and `03-base.css` from the top ~490 lines of `style.css` and from `typography-refined.css`. Retire the drop cap or make it opt-in via a single class — this is the change that lets §3 step 7 delete the `::first-letter … !important` blocks from six pages of Track A content.
*Rollback:* re-upload 1.5.0 zip.
*Gate:* visual diff; drop-cap change is an **expected** diff, reviewed and approved by KK before merge.

**Step 4 — Primitives + editor parity.** *(deploy: 1.5.2)*
Build `04-primitives.css` (button, card, media, badge, kicker, prose, focus ring, surface). Move every one of the 62 consumed `--wp--*` tokens behind a semantic alias. Fix `add_editor_style()` so the editor canvas loads the same stack. Delete the duplicate `:root` blocks — `revive-port.css:31–54`'s 24 redeclarations go first.
*Rollback:* re-upload 1.5.1 zip.
*Gate:* visual diff; plus an editor-canvas screenshot pair (before/after) showing the editor now matches the front end.

**Step 5 — Component migration, one component per PR.** *(deploys: 1.5.3 … 1.5.n)*
In order of measured worst-first: **writing card** (6 locations), **card / `.aurora-card`** (8 declarations across 3 files), **buttons**, **hero**, **proof grid**, **footer bento**, **marquee** (at the `scripts/marquee/` generator, per §1.3), **forms**. Each PR: one component collapsed into one `@layer components` block with its states and its ≤3 breakpoints, old rules deleted, `!important` count strictly decreasing.
*Rollback:* re-upload previous zip. Because each PR is one component, a bad component reverts without losing the others.
*Gate:* visual diff per PR + `make css-inventory` showing line and `!important` counts down.

**Step 6 — Delete the dead layer.** *(deploy: 1.6.0)*
Using step 0's real coverage data, delete the unused classes (§1.5 floor estimate: 142 of 268). Retire `animations.css` and `bleeding-edge.css` into `05-components.css` / `07-utilities.css` — measured: they contribute **0** `!important` and mostly `@keyframes` and progressive-enhancement `@supports`, so they are the cheapest files to fold in. Reduce `style.css` to header + `@layer` + `@import`s.
*Rollback:* re-upload 1.5.n zip.
*Gate:* visual diff; coverage re-run showing no newly-unstyled elements.

**Step 7 — Retire Track A page-content CSS.** *(Track A lane — content, not theme)*
Once steps 3–5 have made the primitives real, delete the six inline page-content `<style>` blocks (§1.6) from the R7–R11 packs and their source in `content/source-packs/content-architecture-2026/wp-payloads/`. Their palette locals become the semantic tokens; their drop-cap suppression becomes unnecessary after step 3.
**Lane note:** this is Track A. It is a separate commit and a separate PR from every theme step, per `AGENTS.md`. Snapshot each page before edit; verify logged out after.
*Rollback:* restore the page snapshot via REST (slug-verified, per the incident rules).
*Gate:* visual diff on the six affected routes; `grep` for `!important` on rendered HTML trending to zero.

**Step 8 — Rename and close out.** *(deploy: 1.6.1)*
Rename `aurora-` / `revive-` / `kkm-` classes to `kk-` across theme CSS **and** the FSE templates/parts/patterns that reference them, in one atomic PR. Delete `09-late.css` if steps 2–6 removed its need. Publish the closeout doc and the final `make css-inventory` numbers against §2.7.
*Why last:* class renames touch markup and content simultaneously and have the widest blast radius. Doing it first would have blocked every Wave 2 page issue for weeks.
*Rollback:* re-upload 1.6.0 zip.
*Gate:* full visual diff at all viewports; `make verify`; KK sign-off.

### 3.1 Interleaving with Wave 2

The whole point of this ordering is that Wave 2 is **not** blocked. Steps 0–1 ship no CSS. Step 2 ships no visual change. Content-lane Wave 2 work never collides with the theme lane at all.

**Can proceed in parallel, immediately, no coordination needed** — content/copy lane, does not touch `theme/`:

| Issue | Why it's clear |
|---|---|
| **#410** Hero tagline copy | Pure copy. Text swap in page/template content. |
| **#415** 'What People Say' + network diagram spike | Content curation plus a standalone HTML prototype explicitly outside the live theme. |
| **#416** Newsletter section rename/copy/CTA | Copy and query settings; the thumbnail work rides existing card primitives. |
| **#419** Speaking page multimedia rebuild | Media inventory, curation, embeds — page content, not theme CSS. |
| **#418** About page unify | **Caveat:** its CSS is Track A page-content CSS (one of the six §1.6 blocks). It may proceed, but it should fix layout *in content* and **not** add new `!important`; its cleanup is finished by step 7. Coordinate so #418 and step 7 don't both rewrite the same block. |
| **#420** Services page rethink | Same caveat as #418 — its 4,418-byte content block is on the step-7 list. Copy and layout work proceeds now; the CSS block gets deleted later. |

**Can proceed in parallel with one constraint** — theme-touching, must land its CSS inside the new layer model once step 2 is live:

| Issue | Constraint |
|---|---|
| **#412** Creative Labs redesign | Fine before step 2. After step 2, its new rules go in `@layer components` with 0 `!important`. Art direction, image selection, and crops are unblocked today. |
| **#413** Client logo soup | New component; build it directly in the target architecture if step 2 has landed, otherwise build it conventionally and it gets migrated in step 5. |
| **#414** Speaking stages section redesign | Same. Concept/mockup phase is entirely unblocked. |

**Must wait:**

| Issue | Waits for | Why |
|---|---|---|
| **#424** Site-wide hover/focus/interactivity pass | **Step 4** (primitives + focus ring) | This is the one issue that genuinely collides. #424's whole premise is "fix gaps with shared styles, not per-element patches" — the shared styles it needs *are* step 4's `04-primitives.css` focus-ring and interactive-state primitives. Doing #424 first means writing the shared interaction layer twice. Its **audit half** (the page-by-page gap inventory, its first acceptance criterion) can and should start now — it produces exactly the requirement list step 4 needs. |
| **#127** Mobile/responsive QA pass | **Step 2** (breakpoint consolidation) | Currently labelled `blocked`. Testing against 12 ad-hoc breakpoints and then again against 3 is wasted work. Re-run it as the step-2 gate. |

**Also gated:** no Wave 2 issue may add a new `!important` to theme CSS from the moment step 0's CI check lands. That is the ratchet that stops the problem from regrowing mid-rebuild — the exact failure mode visible in §1.1, where the 1.4.x port doubled the `!important` count while the B/C recommendation was nominally in force.

---

## 4. Visual-regression baseline procedure

### 4.1 Environment

Chromium is preinstalled at `/opt/pw-browsers/chromium` with `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`. **Do not run `playwright install`.** Verified available: `npx playwright --version` → **1.62.0**; browser dirs present (`chromium`, `chromium-1194`, `chromium_headless_shell-1194`, `ffmpeg-1011`). The Python `playwright` package is **not** installed in this environment — either add it to `scripts/notion-to-wp/.venv` pinned to a matching driver, or drive the Node CLI. Node path: `/opt/node22/bin/node`.

### 4.2 Routes

The eight key logged-out routes, plus three that catch template regressions the eight miss:

```
/               /about/        /speaking/      /services/
/work/          /photography/  /blog/          /contact/
+ one single post (e.g. /2026/07/18/i-am-nomad-ai-film/)   — single.html
+ one 404 (/definitely-not-a-page-404-probe/)              — 404.html
+ one marquee board post                                    — the only inline <style> in the theme (§1.3)
```

All eleven captured logged out, no cookies, no auth.

### 4.3 Viewports and capture settings

| Viewport | Width × height | Device scale |
|---|---|---|
| mobile | 375 × 812 | 2 |
| tablet | 768 × 1024 | 2 |
| desktop | 1440 × 900 | 2 |

- **Full-page** screenshots (`fullPage: true`), PNG.
- `prefers-reduced-motion: reduce` forced — the theme has 6 `prefers-reduced-motion` blocks and 11 `@keyframes`; without this the baseline is nondeterministic.
- `colorScheme: 'light'` forced — one `prefers-color-scheme: dark` block exists.
- Wait for `networkidle` + an explicit settle delay, then scroll to bottom and back to top to trigger lazy-loaded images and IntersectionObserver reveals before capturing.
- Mask known-volatile regions by selector: the marquee board, any date/"now showing" strings, and the Beehiiv embed. Masks are declared in the manifest, not hardcoded.
- Cache-bust with a query param and confirm `style.css` version in the same run, so a baseline can never be silently captured against a stale edge cache.

### 4.4 Tolerance

- Pixel comparison via `pixelmatch` (or Playwright's built-in `toHaveScreenshot`) at **threshold 0.2** per-pixel antialiasing tolerance.
- **Pass:** ≤ 0.1% of pixels differ on a route/viewport pair.
- **Warn (human review required):** 0.1% – 1.0%.
- **Fail:** > 1.0%, or any change in full-page height greater than 2%.
- Expected diffs (e.g. the step-3 drop-cap removal) are approved by KK in the PR and the baseline is re-frozen in the same PR, with the re-freeze called out in the PR body. Never silently re-freeze.

### 4.5 Storage — without repeating #318

[#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318) is explicit that committed capture binaries are the repo's bloat problem. Measured today: `.git` is **301M**, `content/` is **277M**, **347 tracked image files**, of which **48 are screenshots under `backup/`** — including `backup/aurora-deploy-20260724/screenshots/` at 947 KB and 901 KB for two homepage PNGs. At 11 routes × 3 viewports × 2 (baseline + candidate), a naive run would add ~60 MB of PNG **per rebuild step**, times nine steps. That is unacceptable and it is exactly the mistake #318 exists to stop.

**Therefore:**

1. **Never commit baseline or candidate PNGs.** Extend `.gitignore` (which already ignores `docs/current-state/reports/**/*.png`) to cover the new artifact root.
2. Artifacts live at `docs/current-state/reports/visual-baseline/<iso-timestamp>/<route>-<viewport>.png` — inside the already-ignored tree, so the ignore rule is inherited rather than newly invented.
3. **Commit the manifest, not the pixels:** `docs/current-state/reports/visual-baseline/manifest-<timestamp>.json` — per capture, the route, viewport, SHA-256 of the PNG, byte size, full-page height, the theme version read back from live `style.css`, and the Boost bundle hash. That is a few KB of JSON and it is what actually proves "the baseline was frozen at X and the candidate matched." A hash manifest catches any change; the PNG is only needed to *look at* a change.
4. **Diff images only, only when failing, only in the PR.** A failing run uploads its diff PNGs as **PR comment attachments or CI artifacts** — GitHub-hosted, not repo-hosted. If a diff must persist, downscale to ≤ 1200 px wide and convert to WebP (~50–100 KB vs ~950 KB), and put it under `backup/` with a dated dir and a line in the reclaim list.
5. **Baseline regeneration is cheap** because the site is live and the repo matches it byte-for-byte (§1.6) — a lost baseline is one `make visual-baseline` away, so there is no archival argument for committing pixels.
6. Add the new artifact root to `docs/current-state/RECLAIM-LIST-2026-07-24.md` so #318's cleanup pass knows about it.

### 4.6 Interface

```
make visual-baseline           # capture + write manifest; refuses to run if live theme version != expected
make visual-diff BASE=<ts>     # capture candidate, compare against manifest, emit pass/warn/fail per pair
make visual-diff-report        # markdown summary table for pasting into the PR
```

The runner must **fail loudly** if `PLAYWRIGHT_BROWSERS_PATH` is unset or the Chromium path is missing, rather than attempting a download.

### 4.7 Honest limits

- This gates **rendered pixels on production**, which is the right gate given §1.6 (repo == live). It does **not** gate a staging build, because there is no staging environment (`docs/cloudways-setup.md` was never used). Every step therefore compares *post-deploy live* against *pre-deploy live* — meaning a regression is caught minutes after it ships, not before. That is the honest risk, and it is why every step's rollback is a pre-built zip (§5 R-1).
- Screenshot comparison cannot see focus states, hover states, or keyboard behavior. #424's manual tab-through remains a required separate gate.
- It cannot see the editor canvas. Step 4 adds a manual editor screenshot pair.

---

## 5. Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Rollback |
|---|---|---|---|---|---|
| **R-1** | No staging. Every step is verified against production after it ships. | Certain | High | Pre-build and verify the rollback zip **before** each upload (`make aurora-package ROLLBACK_REF=…`). Deploy in a low-traffic window. Run `make visual-diff` immediately post-purge. | Re-upload previous zip via Appearance → Themes → Upload → Replace, purge Pagely + Boost. Proven path, used for 1.4.0→1.4.3. |
| **R-2** | Jetpack Boost serves a **stale concatenated bundle**, so a deploy appears to do nothing (or a rollback appears not to take). | High | High | Read back the Boost bundle URL hash before and after every deploy; treat an unchanged hash as deploy-not-applied, not as no-visual-change. Record the hash in the visual-baseline manifest (§4.5). Purge Boost + PressCACHE explicitly in every deploy step. | N/A — detection control. |
| **R-3** | **Live Code Snippet #14** rewrites `style.css` and `revive-port.css` from media zip #12631 at `init`, silently clobbering a deployed rebuild. | Medium | Critical | **Before step 2:** verify snippet #14 is inactive, verify option `kk_aurora_creamfix_140 = done`, then delete snippet #14 and media #12631 (the deploy handoff already lists this as optional cleanup — the rebuild makes it mandatory). Re-audit all active snippets live, not from the 2026-07-24 backup. | Deactivate the snippet; re-upload the correct zip. |
| **R-4** | `theme.json` global styles print after the theme bundle and win unlayered (§1.6), so removing `!important` regresses styling. | High | High | Step 2 proves the §2.4 mechanism on a real case **before** any migration. If the spike fails, stop and return to KK. `09-late.css` is the escape hatch, and its rule count is a tracked metric. | Revert step 2 (no visual change was shipped, so the revert is free). |
| **R-5** | Class renames (step 8) break FSE templates, block patterns, **and live page content** that references `aurora-*` classes — including the Track A packs. | Medium | High | Rename last, atomically, after a repo-wide grep across `theme/`, `content/source-packs/`, and a live REST dump of page content. Keep old class names as no-op aliases for one release if the grep is not provably exhaustive. | Re-upload previous zip; content edits reverted from pre-edit snapshots. |
| **R-6** | Wave 2 issues land new `!important` / new duplicate layers mid-rebuild, exactly as happened between 2026-07-19 and 1.4.3 (§1.1: 79 → 161). | High | Medium | Step 0's CI ratchet: any PR increasing `!important` count or front-end CSS line count fails. Stated in §3.1 as a Wave 2 rule. | Revert the offending PR. |
| **R-7** | Deleting "dead" CSS deletes something that is only used on an unsampled route or a JS-applied state. | Medium | Medium | Do not delete on the §1.5 heuristic. Step 6 requires real coverage data from step 0 across a wider route set, plus a grep of every `classList.add` / `className` in `theme/kk-aurora/assets/js/`. | Re-upload previous zip; the deleted rules are one `git revert` away. |
| **R-8** | Visual-regression harness produces false diffs (fonts, lazy images, marquee, dates), the team stops trusting it, and the gate becomes theatre. | High | High | §4.3 determinism controls (reduced motion, forced color scheme, scroll-settle, selector masks). Step 1's gate is *two clean runs against unchanged production* before the harness is trusted. Tune masks until the false-positive rate is zero. | Widen masks or raise tolerance for the specific pair, documented in the manifest. |
| **R-9** | Baseline PNGs get committed and re-bloat the repo (#318). | Medium | Medium | §4.5: ignore rule inherited from the already-ignored reports tree; commit hash manifests only; CI check rejecting new `*.png` under the artifact root. | `git rm --cached` before the PR merges. |
| **R-10** | Rebuild consumes weeks and Wave 2 visibly stalls, souring KK on the whole effort. | Medium | High | §3.1's interleaving is the mitigation and should be reported on: six Wave 2 issues are unblocked today, three more after step 2, only two genuinely wait. Report the §2.7 metrics after every step so progress is legible. | Pause after any step — every step is a complete, shipped, stable state. |
| **R-11** | Repo and live drift apart mid-rebuild (they are byte-identical today), destroying the §1.6 premise that the repo inventory is the production inventory. | Medium | High | Re-run the md5 identity check (§0) as part of every `make visual-baseline` run; fail the gate on mismatch. | Reconcile before proceeding; never migrate on top of unknown live state. |

### 5.1 Rollback story, whole effort

Three independent layers:

1. **Per step, live:** the previous version's theme zip, built and hash-recorded before the upload. Restores production in minutes via wp-admin. This is the primary path and it has been exercised (1.3.41 rollback zip in `backup/aurora-deploy-20260724/`).
2. **Per step, repo:** each step is one squashed PR on `main`; `git revert` restores the tracked theme line. Repo and live are reconciled by re-packaging and re-uploading.
3. **Whole effort:** tag `main` at `0064b4e` as `aurora-pre-rebuild-1.4.3` before step 2 and keep a built 1.4.3 zip with a recorded SHA-256 in `backup/aurora-rebuild-<date>/`. Abandoning the rebuild at any point is one upload plus one `git revert` range.

**Non-negotiable:** no step merges without (a) a green `make visual-diff`, (b) a pre-built rollback zip with a recorded hash, (c) `make verify` green, (d) KK approval on the live upload. `AGENTS.md` forbids pushing prod-rendering changes without KK's go-ahead, and `allow_auto_merge` is `false` — green checks mean ready for review, not permission to merge.

---

## 6. Proposed follow-up issues

Ready to file. **Not created by this commit** — the orchestrator or KK files them. All are Track B unless noted. Each maps to a §3 step.

---

**1. `[TOOLING] CSS inventory metric + no-regression CI ratchet`**
Labels: `track-b`, `tech-debt`, `swarm-ready`, `priority:high`
Sub-issue of #423. Implements §3 step 0.
Body sketch: Add `scripts/css_inventory.py` emitting the §1.1 table as JSON (lines, rule blocks, `!important`, custom props, duplicate selectors, breakpoint census). Add `make css-inventory`. Add a CI check on `test-pr.yml` that fails any PR increasing front-end CSS line count or `!important` count vs `main`. Add real coverage data over ≥10 routes to replace the 53% dead-class heuristic. Baseline to record: 7,281 lines / 160 `!important` / 317 duplicate selectors / 114 custom props.
AC: `make css-inventory` reproduces §1.1 exactly; CI fails a deliberate test PR that adds one `!important`.

**2. `[QA] Visual-regression baseline harness for logged-out key routes`**
Labels: `track-b`, `swarm-ready`, `priority:high`, `blocked-by:#423`
Sub-issue of #423. Implements §3 step 1 / §4. **Gate for every subsequent rebuild step.**
Body sketch: `scripts/visual_baseline.py` + `make visual-baseline` / `make visual-diff` / `make visual-diff-report`. 11 routes × 3 viewports (375/768/1440), full-page, reduced-motion and light-scheme forced, scroll-settle, selector masks for marquee/dates/Beehiiv. Tolerance: pass ≤0.1% pixels, warn ≤1%, fail >1% or >2% height delta. **PNGs never committed** — hash manifest only, artifacts under the already-ignored `docs/current-state/reports/` tree (see #318). Uses preinstalled Chromium at `/opt/pw-browsers`; must fail loudly rather than attempt a download. Also verifies live-vs-repo md5 identity and records the Boost bundle hash per run.
AC: two consecutive runs against unchanged production produce zero diffs above tolerance; no new binaries tracked by git; manifest committed.

**3. `[THEME] Cascade layers + token scaffold (behavior-neutral)`**
Labels: `track-b`, `refactor`, `tech-debt`, `swarm-ready`, `priority:high`, `blocked-by:#423`
Implements §3 step 2. Ships as Aurora 1.5.0.
Body sketch: Declare `@layer reset, tokens, base, primitives, components, patterns, utilities, overrides`. Add `02-tokens.css` with semantic `--kk-*` aliases over `--wp--preset--*` / `--wp--custom--*`. Wrap the five existing sheets in `@layer components` without editing their contents. Make every `wp_enqueue_style` handle declare explicit deps (currently 4 of 5 declare none). Prove the §2.4 approach to `global-styles-inline-css` ordering with `09-late.css` on one real case. Delete no rule, rename no class.
AC: zero visual diff on all 11 routes × 3 viewports; `global-styles` override mechanism demonstrated without `!important`; if the mechanism fails, stop and report to KK.
**Preflight, blocking:** verify Code Snippet #14 inactive and `kk_aurora_creamfix_140=done`, then delete snippet #14 and media #12631 (risk R-3).

**4. `[THEME] Reset + base layer; retire or opt-in the drop cap`**
Labels: `track-b`, `refactor`, `swarm-ready`, `priority:medium`
Implements §3 step 3. Aurora 1.5.1.
Body sketch: Extract `01-reset.css` and `03-base.css`. Retire the `typography-refined.css:141–165` drop cap or gate it behind one opt-in class — it is currently defeated by hand with 12–17 `!important` on five separate live pages. Unblocks follow-up #9.
AC: drop-cap change reviewed and approved by KK as an expected diff; baseline re-frozen in the same PR with the re-freeze called out.

**5. `[THEME] Primitives layer + block-editor parity`**
Labels: `track-b`, `refactor`, `swarm-ready`, `priority:high`
Implements §3 step 4. Aurora 1.5.2. **Blocks #424.**
Body sketch: `04-primitives.css` — button, card, media, badge, kicker, prose measure, focus ring, surface. Move all 62 consumed `--wp--*` tokens behind semantic aliases. Delete `revive-port.css:31–54` (24 properties `style.css` already declares). Fix `add_editor_style()` so the editor canvas loads the same stack — today the editor sees only `style.css` + `editor.css` and renders the pre-Revive dark palette.
AC: `--focus-ring` declared once, not twice; zero properties declared in ≥2 files; editor before/after screenshot pair attached; visual diff green.

**6. `[THEME] Component migration epic: one component per PR`**
Labels: `track-b`, `refactor`, `epic`, `swarm-ready`, `priority:medium`
Implements §3 step 5. Aurora 1.5.3+. Sub-issues, worst-first by measurement:
- `.aurora-writing-card` — 84 occurrences, defined in **6** locations in `style.css` (1409–1543, 3557–3690, 2998–3016, 3174–3207, 4153, 4279–4290)
- `.aurora-card` — 8 declarations across 3 files
- buttons · hero · proof grid · footer bento · forms
- marquee — migrate at `scripts/marquee/build.py`, **not** by editing the generated `parts/marquee-current.html` (49 lines of inline CSS)
AC per sub-issue: one component, one `@layer components` block, states and ≤3 breakpoints included, old rules deleted, `!important` strictly decreasing, visual diff green.

**7. `[THEME] Delete dead CSS; fold animations + bleeding-edge into the layer stack`**
Labels: `track-b`, `tech-debt`, `swarm-ready`, `priority:medium`
Implements §3 step 6. Aurora 1.6.0. Builds on #256.
Body sketch: Using real coverage from follow-up #1 (not the 53% heuristic), delete unused rules. Fold `animations.css` (352 lines, 0 `!important`, 11 `@keyframes`) and `bleeding-edge.css` (561 lines, 0 `!important`, 2 `@supports`) into `05-components.css` / `07-utilities.css`. Reduce `style.css` to theme header + `@layer` declaration + `@import`s. Cross-check `theme/kk-aurora/assets/js/` for `classList.add` targets before deleting anything.
AC: coverage re-run shows no newly-unstyled elements; front-end CSS ≤3,000 lines.

**8. `[THEME] Consolidate 12 breakpoints into a 3-step scale`**
Labels: `track-b`, `mobile`, `refactor`, `swarm-ready`, `priority:medium`
Body sketch: Current width breakpoints — `max-width` 360/560/700/781/900/980/1180 and `min-width` 780/782/800/900/960 (780, 781, and 782 all exist separately). Target `--kk-bp-sm/md/lg` = 480/768/1200, mobile-first `min-width` only. Land alongside step 5 component migration. **Unblocks #127**, which is currently labelled `blocked`.
AC: ≤3 distinct width breakpoints outside documented exceptions; #127's mobile QA re-run passes at 360/390/768.

**9. `[CONTENT] Retire Track A page-content CSS blocks (six live routes)`**
Labels: `content`, `track-a`, `tech-debt`, `needs-human-review`, `priority:medium`
Implements §3 step 7. **Track A lane — separate commit and PR from every theme step.**
Body sketch: Delete the inline `<style>` blocks currently served on `/about/`, `/speaking/`, `/work/` (959 B, 14 `!important` each), `/services/` (4,418 B, 13), `/photography/` (5,024 B, 12), `/contact/` (5,422 B, 17). Their palette locals become semantic tokens; their `::first-letter … !important` drop-cap suppression becomes unnecessary once follow-up #4 lands. Source of truth: `content/source-packs/content-architecture-2026/wp-payloads/{about,speaking,work}.html` plus the R7–R11 packs. Snapshot each page before edit; slug-verify before any PATCH per the 2026-05-15 incident rules; purge and verify logged out.
AC: zero anonymous `<style>` blocks on the eight key routes; visual diff green on the six affected routes.

**10. `[THEME] Rename aurora-/revive-/kkm- classes to a single kk- convention`**
Labels: `track-b`, `refactor`, `needs-human-review`, `priority:low`
Implements §3 step 8. Aurora 1.6.1. **Last step — widest blast radius.**
Body sketch: Atomic rename across theme CSS, FSE templates, parts, patterns, **and** live page content that references `aurora-*` classes. Repo-wide grep plus a live REST dump of page content before renaming; keep old names as no-op aliases for one release if the grep is not provably exhaustive. Publish the closeout doc with final metrics against the §2.7 target table.
AC: one prefix site-wide; full visual diff green; `make verify` green; KK sign-off.

---

## 7. Open items — live verification still owed

Stated plainly, per the issue's eval criterion that the inventory be cross-checked against live rendered pages. The live pass in §1.6 covered stylesheet links, inline blocks, byte-identity, head order, and per-route surfaces. It did **not** cover:

1. **Live Code Snippets re-read.** §1.6's snippet analysis comes from a repo-side backup dated 2026-07-24T22:56Z, which predates the creamfix apply. Snippets #14 (creamfix file-apply) and #20 (full theme sync) exist and were described as inactive in the deploy handoff — **verify against the live Code Snippets list**, not the backup. Blocking preflight for follow-up #3 (risk R-3).
2. **Jetpack Boost critical-CSS provenance.** 7,474 bytes inline per page. Whether it is regenerated per deploy, its staleness window, and whether it pins rules that a rebuild will remove — all unknown. If Boost caches critical CSS against old selectors, a mid-rebuild page can render with orphaned above-the-fold styles.
3. **Real coverage data.** The 53% dead-class figure is a rendered-class-diff heuristic across 10 routes, not DevTools coverage. It over-counts JS-applied state classes and under-samples templates. Follow-up #1 replaces it.
4. **`--aurora-lux-delay` and `--service-ribbon`** are consumed via `var()` but declared nowhere in theme CSS. Confirm whether they are set by JS, by page content, or are simply dead.
5. **Logged-in / editor surfaces.** Everything above is logged out. The block-editor canvas (and its measured divergence, §1.2) has not been captured.
6. **Admin-side plugin CSS.** Out of scope for the rebuild but should be confirmed as not leaking to the front end.
7. **`AGENTS.md` is stale on versions.** It states live 1.3.37 / repo 1.3.40; measured 2026-07-25 both are **1.4.3** and byte-identical. Worth a one-line correction in a separate docs commit — deliberately **not** made here, to keep this commit single-concern.

---

## 8. What this plan does not do

- It does not modify any `.css`, `.php`, `.html`, or `theme.json` file. Not one line.
- It does not create GitHub issues. §6 is a filing queue.
- It does not re-argue Path A vs B/C. §1.1's measured `!important` growth (79 → 161 since the memo) is offered as *support* for the decision already made, not as a reopening of it.
- It does not start the teardown. #423's safety rule stands: the rebuild ships behind the §4 screenshot gate, and that gate does not exist yet.

**Tempted-but-didn't list** (noted here instead of fixed, per the docs-only constraint):

- `revive-port.css:31–54` re-declares 24 properties `style.css` already declares — a mechanical delete, but it changes rendering order semantics and belongs in follow-up #5.
- `--focus-ring` is declared twice with different values (`style.css:56`, `revive-port.css:54`). One-line fix; deliberately left for follow-up #5 so it lands behind the screenshot gate.
- `functions.php` handles 1–4 declare no dependencies. Adding them is three lines; it changes cascade order and therefore rendering, so it belongs in follow-up #3.
- `AGENTS.md`'s version line is wrong (§7 item 7). Separate commit, separate concern.

---

**Prepared:** 2026-07-25, against `0064b4e`, theme 1.4.3, live readback the same day.
**Related:** [#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423) (this decision), [#256](https://github.com/WalksWithASwagger/kriskrug-wp/issues/256) (CSS dead-code + snippets-overlap audit), [#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318) (repo bloat), [#424](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424) (hover/focus pass), [#127](https://github.com/WalksWithASwagger/kriskrug-wp/issues/127) (mobile QA), Wave 2 pages [#410–#420](https://github.com/WalksWithASwagger/kriskrug-wp/issues/410).
**Context docs:** [REVIVE-AURORA-PORT-2026-07-24.md](REVIVE-AURORA-PORT-2026-07-24.md) · [REVIVE-AURORA-REVISIONS-2026-07-24.md](REVIVE-AURORA-REVISIONS-2026-07-24.md) · [../../backup/aurora-deploy-20260724/DEPLOY-HANDOFF.md](../../backup/aurora-deploy-20260724/DEPLOY-HANDOFF.md) · [RECLAIM-LIST-2026-07-24.md](RECLAIM-LIST-2026-07-24.md) · [AURORA-RELEASE-CHECKLIST.md](AURORA-RELEASE-CHECKLIST.md)
