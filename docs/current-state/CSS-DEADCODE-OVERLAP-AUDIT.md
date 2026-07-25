# CSS dead-code, overlap, and snippet-emission audit (2026-07-25)

**Issue:** [#256 — [OPS] CSS dead-code, schema snippet, and snippets-overlap audit](https://github.com/WalksWithASwagger/kriskrug-wp/issues/256)
**Feeds:** #423 ground-up stylesheet rebuild (Path A, KK-approved). This document is the *evidence base*; the target architecture is designed separately.
**Lane:** Track B measurement only. **Zero code changed.** No `.css`, `.php`, `.html`, or `theme.json` was modified by this pass.

**Bottom line:** the theme ships **180,893 bytes of CSS across six sheets**. **101 class selectors (22,788 bytes across 177 whole rule blocks, 12.6% of the CSS) have no matching markup anywhere** — not in the repo, not in the WordPress database as rendered on 80 live public routes, not in the theme JS. **160 `!important` declarations** exist in the theme; only 14 are legitimate (reduced-motion, print, focus outlines) and **139 sit in the two override layers that are explicitly fighting each other** — one of which carries a comment saying so. A further **29,030 bytes of page CSS with 113 `!important`** ships from inside *post content* on 8 routes, overriding the theme from a layer the theme cannot see. Schema JSON-LD is healthy: **no duplicate emission** was observed on any sampled route.

---

## How every number here was produced

A new repeatable checker lives at [`scripts/css_coverage_audit.py`](../../scripts/css_coverage_audit.py). It is read-only, needs no WordPress credentials, and runs under plain `python3` (no third-party packages).

```bash
# Repo-only coverage (fast, over-reports dead code — see the trap below)
python3 scripts/css_coverage_audit.py

# One section at a time
python3 scripts/css_coverage_audit.py --section summary|dead|candidates|duplicates|important|inline|tokens

# Machine-readable
python3 scripts/css_coverage_audit.py --format json --output /tmp/audit.json

# Authoritative run: fold saved public HTML into the "used" set
python3 scripts/css_coverage_audit.py --live-corpus /path/to/saved-html --min-confidence high
```

Every table below is reproducible with one of those invocations. The live corpus for this pass was 80 public pages fetched read-only on 2026-07-25:

```bash
curl -sS https://kriskrug.co/wp-sitemap-posts-page-1.xml   # 46 pages
curl -sS https://kriskrug.co/wp-sitemap-posts-post-1.xml   # + 25 newest posts
curl -sS https://kriskrug.co/wp-sitemap-taxonomies-category-1.xml  # + 8 category archives
#                                                          # + 1 synthetic 404 probe
```

All 80 returned `200` (the 404 probe returned `404`, as intended). No live writes were made.

### Live/repo parity check — the audit is valid against production

| Check | Result | Command |
|---|---|---|
| Live `kk-aurora` version | **1.4.3** | `curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/style.css \| head -1` → `Version: 1.4.3` |
| Repo `kk-aurora` version | **1.4.3** | `theme/kk-aurora/style.css` header |
| Live vs repo `style.css` | **byte-identical** | `diff -q livestyle.css theme/kk-aurora/style.css` → no differences |

This matters: it means the dead-code findings apply to production *as it is served today*, not to a repo line that has drifted ahead of live. **`AGENTS.md` is stale on this point** — it still claims live 1.3.37 / repo 1.3.40, last verified 2026-07-19. Live and repo are both 1.4.3 as of this readback. (Not corrected here; that is a docs commit, not a Track B audit commit.)

---

## 1. Stylesheet inventory and enqueue order

`theme/kk-aurora/functions.php:59-132` enqueues five sheets on the front end. `revive-port.css` declares an explicit dependency array on the other four, so it is guaranteed to load last — the cascade order is deterministic, not incidental.

| # | File | Handle | Lines | Bytes | Rules | `!important` |
|---|---|---|---:|---:|---:|---:|
| 1 | `theme/kk-aurora/style.css` | `kk-aurora-style` | 4,519 | 111,255 | 608 | 71 |
| 2 | `assets/css/typography-refined.css` | `kk-aurora-typography` | 685 | 16,735 | 69 | 6 |
| 3 | `assets/css/animations.css` | `kk-aurora-animations` | 352 | 7,540 | 44 | 0 |
| 4 | `assets/css/bleeding-edge.css` | `kk-aurora-bleeding-edge` | 561 | 12,390 | 52 | 0 |
| 5 | `assets/css/revive-port.css` | `kk-aurora-revive-port` | 1,164 | 27,630 | 139 | 82 |
| — | `assets/css/editor.css` | `kk-aurora-editor` (editor only) | 175 | 5,343 | 27 | 1 |
| | **Total** | | **7,456** | **180,893** | **939** | **160** |

`editor.css` is also passed to `add_editor_style()` alongside `style.css` (`functions.php:51-52`), so the block editor loads `style.css` **twice-over** in effect: once as an editor style and once as the `is-style-*` source. Editor-only selectors are excluded from the removal candidates below.

### What actually reaches a browser

Jetpack Boost concatenates and minifies everything into a single bundle. On 2026-07-25 the homepage served exactly one stylesheet:

```
https://s5102.pcdn.co/wp-content/boost-cache/static/78b2cf14fa.min.css   —  138,225 bytes
```

Spot-checking that bundle confirms the dead code is not theoretical — it ships to every visitor:

| Class | Confirmed dead | Present in live Boost bundle |
|---|---|---|
| `.aurora-hero-copy` | yes | **yes** |
| `.aurora-speaking-form` | yes | **yes** |
| `.aurora-skeleton` | yes | **yes** |
| `.aurora-glass-nav` | yes | **yes** |
| `.gform_wrapper` | yes | **yes** |
| `.jetpack-field-error` | yes | **yes** |
| `.kkm-board` (marquee) | n/a — not enqueued | no |

Two consequences for #423. First, Boost means you **cannot** verify which theme sheets loaded by reading public HTML — the handles disappear into the bundle. Second, dead selectors are paid for on every page load, so removing them is a measurable win, not cosmetic tidiness.

---

## 2. Selector coverage / dead code

**Method.** The script extracts every class token from every selector in the six sheets (364 distinct classes), then checks each against four corpora:

| Corpus | Files | What it proves |
|---|---:|---|
| Repo markup — `templates/*.html`, `parts/*.html`, `patterns/*.php`, `content/**`, `fixes/**` | 595 | class is authored somewhere tracked |
| Live HTML — 80 saved public pages, `<style>` blocks stripped before tokenising | 80 | class is *rendered on production* |
| PHP render code — `functions.php`, `theme/kk-aurora/inc/`, `plugins/**`, `inc/` | 15 | class is emitted server-side |
| Theme + plugin JS — `assets/js/*.js`, `plugins/**/*.js` | 4 | class is toggled at runtime |

### Results

| Confidence | Classes | Meaning |
|---|---:|---|
| **high** | **101** | No whole-token *and* no substring match in any corpus, and not a WordPress-generated class shape. Confidently dead. |
| medium | 2 | No whole-token match, but the string appears as a fragment somewhere. Needs eyes. |
| low | 32 | WordPress/core-generated shape, or referenced from JS/PHP. Not dead. |
| (used) | 229 | Matched in repo markup or live HTML. |

**Confidently dead: 101 classes → 177 fully-removable rule blocks → 22,788 bytes (12.6% of the theme's CSS).**

Reproduce: `python3 scripts/css_coverage_audit.py --section dead --min-confidence high --live-corpus DIR`

### Medium confidence — needs manual confirmation (2)

| Class | Bytes | Sites | Why it is not "high" |
|---|---:|---|---|
| `.aurora-badge` | 719 | `style.css:327,348,4414` | Appears only as a substring (e.g. inside longer words in docs). No `class="aurora-badge"` found in markup or on any live route. Very likely dead, but confirm on any unsampled page before removing. |
| `.aurora-meta` | 199 | `typography-refined.css:536` | Substring of `.aurora-metadata`-shaped tokens. Confirm it is not an editor-authored utility KK uses by hand. |

### Low confidence — do NOT treat as dead (32), with two refinements

The blanket `is-style-*` / `wp-*` rule correctly protects most of these, but it over-protects in two places worth calling out, because it is exactly the kind of nuance a naive PurgeCSS run gets wrong in both directions:

**Registered and alive** — `functions.php:196-267` registers `core/quote` styles `callout`, `callout-blue`, `callout-green`, `callout-yellow`, `callout-red`, `callout-gray`, `callout-purple`, plus `core/button` `aurora-primary` / `aurora-ghost`, `core/group` `aurora-card` / `aurora-glass` / `bookmark` / `aurora-source-trail` / `aurora-article-aside`, `core/cover` `aurora-hero`, `core/paragraph` `lead`, `core/pullquote` `aurora-pullquote`. `is-style-callout-blue` and `is-style-callout-green` were both observed rendering live on `/glossary/`. These are editor-selectable and must stay even where a given variant is unused today.

**Registered nowhere → actually dead despite the `is-style-` prefix:**

| Class | Location | Bytes | Evidence |
|---|---|---:|---|
| `.is-style-aurora-secondary` | `typography-refined.css:574,605` | 133 | No `register_block_style` call names `aurora-secondary`. Not selectable in the editor, so no post can carry it. |
| `.is-style-aurora-utility` | `typography-refined.css:586` | 107 | Same — unregistered. |
| `.is-style-aurora-icon` | `typography-refined.css:586` | 107 | Same — unregistered. |

Add ~347 bytes to the removal total once a human confirms KK does not intend to register them.

### The false-positive traps I hit, and how each was handled

1. **The markup is not in the repo.** This is the big one. Nearly all rendered markup for kriskrug.co lives in the WordPress database. A repo-only grep found *105* dead classes; folding in 80 live pages dropped that to *101* — meaning `.aurora-final-cta`, `.aurora-speaking-hero`, `.aurora-speaking-hero-copy`, and `.aurora-proof-body` are alive in page content and would have been wrongly deleted. **Mitigation:** `--live-corpus` is not optional for a real removal decision. Anyone acting on this list must re-run with a fresh fetch.
2. **80 routes is not every route.** The corpus covers all 46 published pages, the 25 newest posts, 8 category archives, and a 404. It does **not** cover older posts, tag archives, author archives, search results, or drafts. A class used only on a 2009 post would read as dead. **Mitigation:** every removal candidate below carries a rollback note, and the recommendation is to stage removals behind a version bump rather than trust the list blind.
3. **CSS inside the HTML would self-confirm.** Saved pages contain `<style>` blocks; tokenising them raw would let a class "prove" its own liveness from its own rule text. **Mitigation:** `build_live_corpus()` strips `<style>…</style>` before tokenising.
4. **JS-toggled state classes.** `classList.add('is-scrolled')`, `'is-revealed'`, `'is-visible'`, `'is-filled'`, `'is-focused'`, `'is-hidden'`, `'is-loaded'`, `'is-active'`, `'copied'`, `'dark'`, `'aurora-lazy'`, `'is-aurora-lux-reveal'` never appear in markup. **Mitigation:** the JS corpus is checked before anything is called dead; all of these land in `low`.
5. **WordPress-generated shapes.** `wp-block-*`, `has-*`, `is-*`, `wp-container-core-*`, body classes (`home`, `single`, `page-*`, `category-*`), `screen-reader-text`, `skip-link`, alignment classes. **Mitigation:** prefix/exact allowlist forces these to `low` — with the caveat above that `is-style-*` needs a registration cross-check to be trustworthy.
6. **Editor-only styles.** `editor.css` selectors like `.editor-styles-wrapper` (2,290 bytes) exist only inside wp-admin and can never appear in front-end HTML. **Mitigation:** classified `low`; `editor.css` is excluded from the removal candidates.
7. **Dynamically composed classes.** Handled by the substring fallback: a class absent as a whole token but present as a fragment is demoted to `medium`, never `high`.
8. **Third-party defensive styling.** `.gform_wrapper`, `.gform_confirmation_message`, `.gform_validation_errors` target **Gravity Forms**, which is not in the active plugin list (issue #256 comment, 2026-07-01). `.jetpack-field-error`, `.contact-form-submission`, `.wp-block-jetpack-contact-form` target **Jetpack**, whose core plugin is *installed but inactive* as rollback insurance. These are dead today but are cheap insurance. **Mitigation:** ranked separately, low priority, with the reactivation risk stated.

---

## 3. Duplication and overlap between the sheets

33 selectors are declared in more than one file. `revive-port.css` loads last and wins every tie. Reproduce with `--section duplicates`.

### The structural finding: two conflicting override layers

`style.css:4436-4519` is a **dark-theme** contrast-hardening block, self-labelled *"Aurora 1.3.32 public Boost cascade accessibility hardening"*. It paints near-black panes behind type (`rgba(9, 12, 17, 0.92)`) with `!important` on almost every declaration.

`revive-port.css:1060-1090` is a **cream/ink** layer whose own comment reads:

> ```
> Undo 1.3.33 dark-theme opaque contrast hardening on cream paper.
> Those rules used !important black panes behind type; they must not win here.
> ```

The second layer exists solely to defeat the first. That is the single clearest justification for the #423 rebuild in the entire codebase.

The mechanics are worth understanding, because they explain the `!important` count. Consider `.aurora-kicker`, which is coloured **four** times:

| Order | File:line | Selector | Specificity | `!important` | Wins? |
|---|---|---|---|---|---|
| 1 | `style.css:2349` | `body.aurora-theme :where(.aurora-kicker, …)` | (0,1,1) | yes | no |
| 2 | `style.css:4453` | `body.aurora-theme :where(.aurora-kicker, .aurora-section-kicker)` | (0,1,1) | yes | no |
| 3 | `revive-port.css:84` | `.aurora-kicker, .aurora-section-kicker` | (0,1,0) | yes | **no** — lower specificity than 1 & 2 |
| 4 | `revive-port.css:1084` | `body.aurora-theme :where(.aurora-kicker, .aurora-section-kicker)` | (0,1,1) | yes | **yes** — ties on specificity, loads last |

Rule 3 is the "natural" brand declaration and it loses. Rule 4 exists only because rule 3 lost. `:where()` contributes zero specificity, so the entire war is decided by `body.aurora-theme` (0,1,1) versus a bare class (0,1,0) — and then by source order. The same shape repeats for `.aurora-page-title`, the button styles, and the pagination links.

### Full cross-file duplicate list (33)

| Selector | Declared in | Winner |
|---|---|---|
| `:root` | `style.css:1`, `style.css:484`, `bleeding-edge.css:297,393,511`, `revive-port.css:1` | revive-port |
| `.aurora-card` | `style.css:232`, `bleeding-edge.css:140,150,156,516,537` | bleeding-edge |
| `body` | `style.css:89,4410`, `typography-refined.css:60,460`, `bleeding-edge.css:493` | bleeding-edge |
| `.aurora-page-title` | `style.css:2227,3149`, `typography-refined.css:510,524` | typography-refined (`!important`) |
| `html` | `style.css:67,76`, `typography-refined.css:49` | typography-refined |
| `a` | `style.css:159,4422`, `bleeding-edge.css:521` | bleeding-edge |
| `.aurora-header-2026` | `style.css:663,4319`, `revive-port.css:161` | revive-port |
| `.aurora-header-cta` | `style.css:739,3106`, `revive-port.css:275` | revive-port |
| `.aurora-article-list` | `style.css:1296`, `revive-port.css:812,819` | revive-port |
| `body.aurora-theme :where(.aurora-kicker, .aurora-section-kicker)` | `style.css:2349,4453`, `revive-port.css:1084` | revive-port |
| `body.aurora-theme .wp-block-button:not(.is-style-aurora-primary) .wp-block-button__link` | `style.css:2353,4464`, `revive-port.css:1140` | revive-port |
| `::selection` / `::-moz-selection` | `style.css:111,117`, `bleeding-edge.css:465,476` | bleeding-edge |
| `:focus-visible` | `style.css:122`, `bleeding-edge.css:418` | bleeding-edge |
| `.wp-block-button.is-style-aurora-primary .wp-block-button__link` (+`:hover`) | `style.css:188,204`, `typography-refined.css:568,600` | typography-refined |
| `.wp-block-button.is-style-aurora-ghost .wp-block-button__link` | `style.css:209`, `typography-refined.css:580` | typography-refined |
| `.aurora-theme` | `style.css:534`, `revive-port.css:66` | revive-port (`!important`) |
| `.aurora-theme :where(h1…h6)` | `style.css:544`, `revive-port.css:72` | revive-port |
| `.aurora-button-primary` / `-secondary` (+`:hover`) | `style.css:576,584,591,598`, `revive-port.css:92,104,112,123` | revive-port |
| `.aurora-primary-nav a, .aurora-utility-link` (+`:hover`) | `style.css:714,723`, `revive-port.css:260,270` | revive-port |
| `.aurora-action-row` | `style.css:880`, `revive-port.css:851` | revive-port |
| `.aurora-writing-band` | `style.css:1283`, `revive-port.css:786` | revive-port |
| `.aurora-article-row` | `style.css:1301`, `revive-port.css:824` | revive-port |
| `.aurora-footer-2026` | `style.css:2633`, `revive-port.css:857` | revive-port |
| `.aurora-footer-tile` | `style.css:2698`, `revive-port.css:898` | revive-port |
| `.aurora-footer-bottom` | `style.css:2940`, `revive-port.css:903` | revive-port |
| `.aurora-reading-progress` | `style.css:4399`, `bleeding-edge.css:67` | bleeding-edge |
| `*` | `typography-refined.css:680`, `bleeding-edge.css:459` | bleeding-edge |

### Duplicated design tokens

**114 CSS custom properties are defined across 166 definition sites.** 24 are defined in two files at once — and it is one clean block: `style.css:493-522` and `revive-port.css:31-54` both define the entire `--aurora-*` palette.

| Property | `style.css` | `revive-port.css` |
|---|---|---|
| `--aurora-ink`, `-soft`, `-muted` | 493-495 | 31-33 |
| `--aurora-paper`, `--aurora-signal`, `--aurora-readable-accent` | 496-498 | 34-36 |
| `--aurora-signal-dark`, `-control`, `-control-hover` | 499-501 | 37-39 |
| `--aurora-wildcard`, `--aurora-opal-*` (4) | 502-506 | 40-44 |
| `--aurora-black`, `-panel`, `-panel-solid` | 511-513 | 45-47 |
| `--aurora-reader-pane`, `-solid`, `-border` | 514-516 | 48-50 |
| `--aurora-line`, `-strong`, `--aurora-shadow-deep` | 517-522 | 51-53 |
| `--focus-ring` | 56 | 54 |

`revive-port.css` wins all 24 by load order, which makes the `style.css:493-522` block **entirely inert on the front end** — but *not* in the editor, where `add_editor_style('style.css')` loads it without `revive-port.css`. That asymmetry is a live editor/front-end colour divergence, not just redundancy.

**39 custom properties are never referenced by any `var()` in the theme.** Five of those *are* referenced from live pages (`--accent`, `--aurora-black`, `--aurora-panel`, `--kk-accent`, `--kk-muted`) — i.e. by CSS embedded in post content, which the theme cannot see. Removing them would silently break page-level styling. The remaining 34 (`--angle`, `--aurora-glow-{xs,lg,xl}`, `--aurora-opal-{gold,mint}`, `--ease-{spring,smooth,out-back,out-expo,out-quint}`, `--bg`, `--bg-card`, `--bg-deep`, `--border`, `--cyan`, `--fg`, `--muted`, `--surface`, `--text`, `--input-border`, `--input-glow`, `--kk-{bg,border,fg}`, `--revive-line-strong`, `--aurora-readable-wide`, `--aurora-reader-pane-solid`, `--aurora-signal-dark`, `--aurora-wildcard`, `--aurora-paper`) are unreferenced everywhere checked.

**Hex literals vs `theme.json`.** 23 hex colours appear more than once in the CSS. Nine of the most-repeated already have a `theme.json` palette slug and should be `var(--wp--preset--color--*)` instead:

| Hex | Occurrences | `theme.json` slug | Files |
|---|---:|---|---|
| `#efe6d2` | 12 | `paper` | style.css, revive-port.css |
| `#d94a1f` | 7 | `error` | style.css, revive-port.css |
| `#e8b53a` | 7 | `warning` | style.css, revive-port.css |
| `#e6dcc2` | 7 | `elevated` | style.css, revive-port.css |
| `#171310` | 5 | `text-primary` | style.css, revive-port.css |
| `#b53c18` | 3 | `signal-text` | style.css, revive-port.css |
| `#d6337a` | 2 | `pink` | style.css, revive-port.css |
| `#39a8d8` | 2 | `cyan` | style.css, revive-port.css |
| `#f15b43` | 6 | *(no slug)* | style.css, editor.css |
| `#050708`, `#030405`, `#07090b`, `#080b0d` | 13 total | *(no slug)* | style.css |

Reproduce with `--section tokens`.

---

## 4. `!important` inventory

**160 declarations in the theme.** Reproduce with `--section important`.

| File | Count | What it is fighting |
|---|---:|---|
| `revive-port.css` | **82** | Beating `style.css`'s dark hardening layer (which itself uses `!important`), plus `global-styles-inline-css` — the ~27 KB `theme.json`-generated `:root :where(…)` block WordPress injects inline into `<head>`. `:where()` has zero specificity, so on paper it should be easy to beat; in practice the previous layer's `!important` forced escalation. |
| `style.css` | **71** | Legitimate: 4 in `prefers-reduced-motion` (`L84-87`), 4 focus-outline hardening (`L3483-3490`), 2 print-style resets (`L4431-4432`). Other: 2 responsive `display:none` utilities (`L476,482`), 2 media sizing (`L1406,1432`). **57 in the contrast-hardening layers — 22 at `L2231-2376` and 35 at `L4436-4519`** — the ones `revive-port.css` then has to undo. |
| `typography-refined.css` | 6 | 2 forcing `--aurora-page-title-size` over `theme.json` `fontSize` presets (`L513,526`); 4 in `prefers-reduced-motion` (`L677-683`, legitimate). |
| `editor.css` | 1 | editor-only. |
| `animations.css` | **0** | clean. |
| `bleeding-edge.css` | **0** | clean. |

**Legitimate and out of scope for #423 removal: 14** (reduced-motion ×8 across `style.css` and `typography-refined.css`, focus outlines ×4, print ×2). **Cascade-war casualties: 139** — 57 in `style.css`'s two hardening blocks and all 82 in `revive-port.css`. The remaining 7 are one-off overrides of WordPress block defaults and `theme.json` presets.

The `-webkit-text-fill-color: currentColor !important` pattern appears 15 times in `style.css` alone. It exists because gradient-clipped text (`background-clip: text`) cannot be recoloured by `color` alone, so every colour override in the readability layer must ship a paired fill-colour override. Killing the gradient-text treatment in the #423 rebuild removes that whole class of declaration.

---

## 5. Inline `<style>` blocks

### In the theme's FSE markup — 1 block

Reproduce with `--section inline`.

| File | Line | Lines | Bytes | `!important` | Selectors |
|---|---:|---:|---:|---:|---|
| `theme/kk-aurora/parts/marquee-current.html` | 3 | 49 | 3,787 | 0 | `.kkm`, `.kkm-board`, `.kkm-cell`, `.kkm-dek`, `.kkm-frame`, `.kkm-kicker`, `.kkm-row`, `.kkm-src`, + `[data-skin]` variants |

**It duplicates `plugins/kk-marquee-board/assets/marquee.css` (49 lines) almost selector-for-selector** — both define `.kkm`, `.kkm-board`, `.kkm-cell`, `.kkm-cell.kkm-space`, `.kkm-dek`, `.kkm-frame`, `.kkm-kicker`, `.kkm-kicker::before`, `.kkm-row`, `.kkm-src`, and the three `[data-skin]` variants. Two independent copies of the same component styling in two deploy units.

**Neither is live.** `/marquee/` returns `404`, `wp-content/plugins/kk-marquee-board/assets/marquee.css` returns `404`, and no `kkm` markup appears on the live homepage. The partial is included by `theme/kk-aurora/patterns/marquee-hero.php`, which is registered as a pattern but is not inserted into any live page. Related dormant surface: `templates/single-marquee_board.html` and `templates/archive-marquee_board.html` both target the `marquee_board` CPT that only the undeployed plugin registers, and `assets/js/marquee.js` is enqueued on `is_front_page()` for a board that is not there.

`templates/*.html` and `patterns/*.php` contain **zero** inline `<style>` blocks. Good hygiene; the marquee partial is the sole exception.

### In page content — 34 blocks in the repo, 8 observed live

This is the finding with the largest blast radius for #423, and it is invisible if you only read the theme.

Tracked in the repo under `content/**/*.html`:

| Metric | Value |
|---|---:|
| Files with an inline `<style>` block | 34 |
| Blocks | 34 |
| Total lines | 2,642 |
| Total bytes | 140,862 |
| Total `!important` | 219 |

Largest: `keynotes-2026/wp-payloads/publications.html` (10,204 B), `work.html` (10,136 B / 17 `!important`), `about.html` and `podcast-guesting-page-epk.html` and `responsible-ai-professional.html` (9,853 B / 17 each), `content/drafts/2026-07-24-sponsor-deck/post.html` (7,752 B / 22).

Observed **live**, as unattributed `<style>` tags (no `id` attribute — i.e. not a WordPress enqueue) on 8 of 80 routes:

| Route | Bytes | `!important` | Class namespace |
|---|---:|---:|---|
| `/sponsor-deck/` | 7,752 | 22 | `.kk-sponsor*` |
| `/contact/` | 5,422 | 17 | `.kk-contact*` |
| `/photography/` | 5,024 | 12 | `.kkx*` |
| `/generative-ai-services/` | 4,418 | 13 | `.kk-services-2026*` |
| `/publications/` | 3,537 | 7 | `.kk-publications*` |
| `/about/`, `/work/`, `/speaking/` | 959 each | 14 each | `.kk-r9-pack` |
| **Total** | **29,030** | **113** | |

These blocks style **theme-owned selectors from a layer the theme cannot control**: `.kk-r9-pack .aurora-button`, `.kk-r9-pack .aurora-card`, `.kk-r9-pack .aurora-media-card`. They also consume theme custom properties (`--accent`, `--aurora-black`, `--aurora-panel`, `--kk-accent`, `--kk-muted`), which is why those tokens read as "unused" from inside the theme but must not be deleted.

Inline `<style>` in `<body>` beats every enqueued sheet on source order at equal specificity, and 113 of these declarations carry `!important` on top of that. **Any #423 rebuild that changes `.aurora-button` / `.aurora-card` / `.aurora-media-card` will be silently overridden on these 8 routes.** They are Track A content, not Track B theme, so they need a coordinated migration — this is the hard dependency between #423 and the content lane.

---

## 6. Schema JSON-LD and Code Snippets overlap

### What the repo emits

| File | Lines | Role | Hooks |
|---|---:|---|---|
| `fixes/schema-snippets-deployed.php` | 229 | **Canonical.** Header already states "CANONICAL LIVE SOURCE (Track A / Code Snippets)… historically snippet id 5". | `wp_head` @ 5 Person, 6 WebSite, 7 Article, 8 BreadcrumbList, 9 Service |
| `fixes/schema-snippets.php` | 270 | Reference / future mu-plugin. Contains `VERIFY-ME` placeholders and a `kk_schema_is_ready()` guard. | same shape |
| `fixes/issue-39-schema-markup.php` | 130 | Historical fix draft. | — |
| `plugins/kk-marquee-board/includes/schema.php` | 60 | Article + breadcrumb for `marquee_board` CPT, `wp_head` @ 7. **Plugin is not deployed** (`/marquee/` → 404). | `wp_head` @ 7 |

**Issue #256 acceptance criteria 2 and 3 are already satisfied in the repo.** The canonical header comment exists at `fixes/schema-snippets-deployed.php:1-27`, it explicitly names `fixes/schema-snippets.php` as reference/archive, and the headshot TODO is documented rather than silently resolved — `person_image` is set to `https://kriskrug.co/wp-content/uploads/2023/07/krug-1.jpg` with the note *"Headshot URL is the public /about/ portrait; confirm if KK wants a newer asset."* No code change needed; what remains is KK's decision on the asset.

### Live JSON-LD — measured, no duplicate emission

Across all 80 fetched routes, every JSON-LD block parsed cleanly (zero parse errors):

| Shape | Routes |
|---|---:|
| `Person` + `BreadcrumbList` | 53 |
| `Person` + `BreadcrumbList` + `BlogPosting` | 25 |
| `Person` + `BreadcrumbList` + `WebSite` | 1 (`/`) |
| `Person` + `WebSite` | 1 |

Exactly one `Person` and one `BreadcrumbList` per route. **No duplicate Person, Article, or Organization emission from Site Kit, WordPress core, or the theme.** This confirms the 2026-07-02 finding on the issue: snippet #5 is the schema *owner*, not schema noise.

One clean discrepancy worth recording: `kk_schema_service()` (deployed snippet, `wp_head` @ 9) emits `Service` only for pages carrying a `kk_service_audience` post meta. No sampled page emitted `Service`, including `/generative-ai-services/`. That is a **dormant code path, not drift** — the meta key is simply not set on any page. If Service schema is wanted, the fix is a post-meta backfill, not a snippet edit.

### Duplicate-emission risk surface — what a human must check in wp-admin

**Repo-side analysis can only identify the risk. It cannot read the live Code Snippets bodies.** The repo copy at `fixes/schema-snippets-deployed.php` is a *mirror*, and its own header warns to "keep wp-admin and this file in sync if either side is edited." Nothing in this audit verifies that they are currently in sync — the live public JSON-LD is consistent with the repo copy, which is evidence but not proof (the emitted output would look identical for several plausible edits).

Checklist for wp-admin (Snippets → All Snippets, and Settings for WPCode Lite):

1. **Snippet #5 (unnamed, active, global).** Diff its body against `fixes/schema-snippets-deployed.php`. Confirm `kk_schema_constants()` values match, especially `person_image` and `knows_about` (issue #316 flags legacy "Generative AI Tools" wording still present). Per the 2026-07-02 comment, rename it to `KK Schema JSON-LD` and add a description recording that it owns Person / WebSite / Article / Breadcrumb / Service.
2. **WPCode Lite (active, 2.3.6).** Its snippet bodies were **not** enumerable over the read-only REST pass on 2026-07-01 and are still unknown. Open WPCode → Code Snippets and confirm no entry emits JSON-LD, header/meta tags, or CSS. This is the single largest blind spot in this audit.
3. **Site Kit (active, 1.182.0).** Confirm no schema/structured-data output option is enabled that would add a second `Person` or `Organization` once page-level markup changes.
4. **Any snippet emitting CSS.** Snippet #9 (`A11Y CTA contrast hotfix 2026-06-18`) is recorded as **inactive**; confirm that is still true, because if it were reactivated it would inject CTA contrast CSS that collides directly with `revive-port.css`'s button layer. Check every active snippet for `wp_add_inline_style`, `wp_head`-echoed `<style>`, or `wp_enqueue_style`.
5. **Snippet #10 (`KK Asset Diet`, active).** Leave active — per #256 AC and `ASSET-DIET-2026-06-28.md`. Note for #423 planning that it plus Jetpack Boost concatenation is why live HTML shows one bundle instead of five theme handles; any before/after CSS-weight measurement must compare Boost bundle sizes, not enqueue counts.
6. **Snippets #7 and #8 (active).** Root files (`/robots.txt`, `/llms.txt`) and GSC query-param canonicalisation. Out of scope for CSS; leave alone.
7. **The 8 content-embedded `<style>` blocks** listed in §5. Confirm each lives in *post content* (Gutenberg custom HTML block) and not in a snippet — the audit inferred content because the same CSS is tracked in `content/**/wp-payloads/*.html`, but that inference should be spot-checked on `/photography/` (`.kkx*`) and `/sponsor-deck/` (`.kk-sponsor*`) before #423 assumes it can edit them via the content lane.

---

## 7. Prioritized removal candidates

Ranked by (bytes saved × confidence ÷ risk). **Nothing here has been removed.** This is the #423 shopping list.

Reproduce the grouping with `python3 scripts/css_coverage_audit.py --format json --live-corpus DIR` and read the `removable` array.

**Universal rollback note:** the theme is version-controlled and live `style.css` is byte-identical to `main`. Rollback for any item is `git revert` + redeploy + Boost cache purge. The real risk is not "can we undo it" but "will we notice" — so each item below states the specific route to eyeball after deploying.

| # | Candidate | Bytes | Rules | Confidence | Risk | Exact locations | Rollback / verification |
|---|---|---:|---:|---|---|---|---|
| 1 | **`animations.css` utility layer** — `.aurora-animate-*` (5), `.aurora-card-lift`, `.aurora-link-slide`, `.aurora-button-press`, `.aurora-dots`, `.aurora-spinner`, `.aurora-pulse`, `.aurora-gradient-animated`, `.aurora-hero-text` | 3,364 | 33 | high | **very low** | `animations.css:20,51,71,85,101,117,133,137,146,150,157,164,170,181,216,237,242,250,254,290,299,303,318,329,333,335-341,345` | 0 `!important` in this file, no JS references any of these, purely opt-in classes. This is 44% of `animations.css`. Verify: any page with motion — nothing should change. |
| 2 | **`.aurora-speaking-*` cluster** — `-band`, `-copy`, `-form`, `-hero-keynote`, `-panel`, `-reel-feature` | 2,477 | 17 | high | low | `style.css:1242,1252,1258,1262,1272,1279,1722,1730,1741,1799,1846,1852,1860,1873,1882,3046,3311` | `/speaking/` was fetched and renders none of these (it uses the `.kk-r9-pack` content layer instead). Verify `/speaking/` and `/podcast-guesting-page-epk/` after deploy. |
| 3 | **`.aurora-hero-*` cluster** — `-2026`, `-caption`, `-copy`, `-dek`, `-media`, `-scrim` | 2,346 | 18 | high | low | `style.css:760,767,775,780,785,792,802,811,822,884,892,905,3113,3119,3123,3131,3261,3320` | Superseded by the R9/marquee hero work. **Caveat:** `.aurora-hero-copy` and `.aurora-hero-dek` are also named inside the `style.css:4436-4519` `:where()` hardening lists — remove those list entries in the same commit or the rules become no-ops with dangling selectors. Verify `/` and `/about/`. |
| 4 | **`typography-refined.css` glass/utility** — `.aurora-glass-nav`, `.aurora-glass-media`, `.aurora-hero-title`, `.aurora-panel-title`, `.aurora-article-body`, `.aurora-caption`, `.display-text`, `.fractions`, `.ordinals` | 1,481 | 9 | high | low-med | `typography-refined.css:388,408,413,482,490,499,517,530,543` | `.fractions` / `.ordinals` / `.display-text` are hand-authoring utilities KK could type into a custom HTML block on an unsampled page. **Ask KK before removing those three** (~212 B); the six `.aurora-*` ones are safe. `.text-small` (91 B, `L347`) is also dead but is comma-joined with the element selector `small` — edit the selector list, do not delete the rule. |
| 5 | **`bleeding-edge.css` spec demos** — `.aurora-scroll-reveal`, `.aurora-parallax-subtle`, `.aurora-card-container`, `.aurora-stats-container`, `.aurora-stat-number`, `.aurora-link-variable`, `.aurora-grid`, `.aurora-grid-item`, `.aurora-nav`, `.aurora-content`, `.aurora-aside` | 1,435 | 11 | high | very low | `bleeding-edge.css:101,115,127,160,168,286,319,330,368,377,387` | 0 `!important` in this file. These are progressive-enhancement demos (`@supports` showcases) that were never wired to markup. Note `.aurora-nav` at `L368` also carries `.current-menu-item` — keep that WP-generated class if the rule is split. |
| 6 | **`.aurora-feature-band*` + `.aurora-offer-band`** | 1,067 | 3 | high | **medium** | `style.css:1105`, `4495`, `4503` | Two of the three rules live *inside* the `L4436-4519` hardening block and are among the longest single rules in the file (563 B and 364 B). Removing them touches the block that `revive-port.css:1060+` explicitly undoes. Best sequenced *with* the #423 cascade rewrite, not before it. |
| 7 | **`.aurora-proof-*`** — `-row`, `-media`, `-module-bhf` | 976 | 9 | high | low | `style.css:837,841,870,1917,1923,1931,1947,1951,3257` | `-module-bhf` is a one-off for the "Both Hands Full" packet (`fixes/issue-342-*`). Verify `/work/` and `/about/`. |
| 8 | **Grid family** — `.aurora-check-grid`, `.aurora-hired-grid`, `.aurora-epk-grid`, `.aurora-faq-grid` | 2,042 | 13 | high | low | `style.css:985,995,999,1010,1016,1025,1032,1036,1804,1810,1821,1887,1892` | Four grids sharing comma-joined selectors; remove as one unit or the shared rules go inconsistent. Verify `/podcast-guesting-page-epk/` (the EPK page) and `/work/`. |
| 9 | **`.aurora-footer-nav` + `.aurora-footer-brand`** | 765 | 7 | high | low-med | `style.css:2647,2656,2668,2674,2680,2688,2847` | The footer is a **global** part (`parts/footer.html`) — it renders on every route, so a regression is site-wide even though the classes are absent from all 80 sampled pages. Verify the footer on `/` and one post. |
| 10 | **Dead third-party form styling** — Gravity Forms (`.gform_wrapper`, `.gform_confirmation_message`, `.gform_validation_errors`) and Jetpack Forms (`.jetpack-field-error`, `.contact-form-submission`) | 252 fully-removable + 284 class-attributed | 2 | high | **medium** | Fully removable: `style.css:2930` (110 B), `style.css:2935` (142 B). Also present but comma-joined with the live `.wp-block-jetpack-contact-form`: `style.css:2876,2895` | Gravity Forms is not installed at all → safe. Jetpack core is installed-but-inactive as deliberate rollback insurance; if it is ever reactivated, `/contact/` loses its error/success styling. **Cheapest correct action: leave in place, add a comment naming the dependency.** Low value for real coupling risk. |

**Additional single-class candidates** (each < 650 B, all high confidence, all in `style.css` unless noted): `.aurora-path-row` (639 B, L852,859,875,3253,3265), `.aurora-writing-card-excerpt` (632 B, L1516,1524,1531,3612), `.aurora-card-gradient` (628 B, L257,265,281), `.aurora-topic-*` (603 B, L1758-1795), `.aurora-signal-strip` (572 B, L910,919,924,931), `.aurora-logo-row-wide` (375 B, L961,967), `.aurora-fade-up`/`.aurora-scale-in` (540 B, L374,383,391,396,4427 — note the print-style `!important` at L4427), `.aurora-link` (315 B, L167,173,184), `.aurora-skeleton` (283 B, L404), `.aurora-text-card` (234 B, L1232,1238), `.aurora-human-line` (195 B, L1746,1752), `.aurora-inline-link` (184 B, L1043,1050), `.aurora-section-heading-compact` (157 B, L953,957), `.aurora-quote-grid-three` (130 B, L1058), `.aurora-section-tight` (124 B, L305), `.aurora-featured-strip`/`.aurora-stage-strip` (116 B, L947), `.aurora-media-card-large` (104 B, L1160,3273), `.aurora-button-reel` (64 B, L888), `.aurora-hide-desktop` (56 B, L480), `.aurora-testimonial-band` (51 B, L1054), `.aurora-keynote-card` (48 B, L1762), `.kkp-display` (69 B, L2305).

**`revive-port.css` has zero fully-removable rules** even though `.kk-dark-island` (133 B, `revive-port.css:973`) and `.sponsor-deck-2026` (126 B, `revive-port.css:918,938,949,961`) are confidently dead — every rule naming them is comma-joined with a live selector, so removal means editing selector lists rather than deleting blocks. Treat as a hand edit during the #423 rewrite, not a mechanical delete.

### Non-selector cleanups worth folding into #423

| Item | Saving | Risk | Note |
|---|---:|---|---|
| Delete `style.css:493-522` duplicate token block | ~30 lines | **medium** | Inert on the front end (revive-port wins) but **live in the editor**, where `add_editor_style('style.css')` loads it without `revive-port.css`. Move both to a single source before deleting either. |
| Replace 9 palette hex literals with `var(--wp--preset--color--*)` | 0 bytes | low | Correctness, not weight. Removes the divergence risk between CSS and `theme.json`. |
| Delete 34 never-referenced custom properties | ~34 lines | low | **Keep** `--accent`, `--aurora-black`, `--aurora-panel`, `--kk-accent`, `--kk-muted` — used by content-embedded CSS. |
| Retire the `parts/marquee-current.html` inline `<style>` **or** `plugins/kk-marquee-board/assets/marquee.css` | 3,787 B | low | Pick one owner. Neither is live today. |
| Decide the fate of the dormant marquee surface | — | low | `templates/single-marquee_board.html`, `templates/archive-marquee_board.html`, `patterns/marquee-hero.php`, `assets/js/marquee.js` (enqueued on the front page for a board that is not rendered). Either deploy the plugin or park the templates. |
| Remove 3 unregistered `is-style-*` button variants | 347 B | low | `.is-style-aurora-secondary`, `.is-style-aurora-utility`, `.is-style-aurora-icon` — no `register_block_style` call exists, so no post can carry them. |

### Estimated total

| Bucket | Bytes |
|---|---:|
| Confidently-dead rule blocks (177 rules, 101 classes) | 22,788 |
| Unregistered `is-style-*` variants | 347 |
| Duplicate marquee CSS (one of two copies) | 3,787 |
| **Available now, high confidence** | **≈26,900** (14.9% of 180,893) |
| Plus: collapsing the two override layers into one | not estimated — architectural, belongs to #423 |

---

## Open questions for KK

1. `.fractions`, `.ordinals`, `.text-small`, `.display-text` — hand-authoring utilities, or leftovers? (~303 B, item 4.)
2. Jetpack Forms styling — Jetpack core is inactive but installed. Keep the defensive CSS, or accept that reactivation would need a style pass? (item 10.)
3. The marquee surface — deploy `kk-marquee-board`, or park the templates, partial, pattern, and front-page JS enqueue?
4. `person_image` in the deployed schema snippet is the 2023 `/about/` portrait. Newer asset wanted? (#256 AC 3 — documented, not resolved.)
5. The 8 content-embedded `<style>` blocks (29 KB, 113 `!important`) override theme selectors. Are those migrating into the #423 stylesheet, or staying as per-page content CSS? #423's scope depends on the answer.

---

**Scope confirmation:** this pass created two files — `scripts/css_coverage_audit.py` and this document. No `.css`, `.php`, `.html`, or `theme.json` file was modified. No WordPress writes were made; all live interaction was read-only `curl` against public URLs.

**Last verified:** 2026-07-25. Live `kk-aurora` **1.4.3**, byte-identical to repo `main`. Live corpus: 80 public routes fetched 2026-07-25. Re-run `python3 scripts/css_coverage_audit.py --live-corpus DIR` with a fresh fetch before acting on any removal candidate — the coverage claim is only as current as the corpus behind it.
