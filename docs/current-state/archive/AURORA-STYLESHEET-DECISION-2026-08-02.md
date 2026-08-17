# Aurora stylesheet hierarchy: rebuild vs incremental repair

**Decision memo for [#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423). Read only.**
This document ships zero CSS, zero PHP, zero theme changes. Nothing under `theme/` was touched to produce it.

| | |
|---|---|
| Lane | Track B (Aurora theme), docs only |
| Measured against | worktree at `dd87d4a`, `theme/kk-aurora` **1.5.8** |
| Live readback | `https://kriskrug.co`, logged out, 2026-08-02, 16 routes fetched by HTTP GET, plus a re-scrape of `/about/` and `/`, the Jetpack Boost bundle, and a `code-snippets/v1` probe during the 2026-08-03 correction pass. All GET. |
| Live theme | **1.5.7** (`curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/style.css \| grep -i Version`) |
| Reproduce | `make css-inventory`, `make css-inventory-json`, `make css-coverage` |
| Status | **A vs B was decided on 2026-07-24 and reconfirmed 2026-07-25. This memo does not reopen it.** Section 10 asks five new questions (D-1 to D-5) raised by what changed since. |

---

## 0. The first thing this memo has to say

The A vs B question on #423 was already answered.

KK recorded **Path A, ground-up token-based rebuild** on 2026-07-24 and reconfirmed it on 2026-07-25 (both in the #423 comment thread). The implementation plan merged as [`docs/current-state/AURORA-STYLESHEET-REBUILD-PLAN.md`](AURORA-STYLESHEET-REBUILD-PLAN.md) (PR #467). Three of its nine steps have shipped:

| Step | Issue | State | Evidence |
|---|---|---|---|
| 0 CSS inventory metric + CI ratchet | #472 | CLOSED | `scripts/css_inventory.py`, `.css-budget.json`, `make css-inventory-check` |
| 1 Visual-regression baseline harness | #473 | CLOSED | `scripts/visual_baseline.py`, `docs/current-state/reports/visual-baseline/manifest-BASE1.json` |
| 2 Cascade `@layer` + token scaffold (1.5.0) | #474 | CLOSED | PR #493, merged 2026-07-27; `theme/kk-aurora/assets/css/02-tokens.css`, `09-late.css`; live `style.css:20` carries the `@layer` declaration |
| 3 Reset + base; drop cap (1.5.1) | **#475** | **OPEN** | not started |
| 4 to 8 | #476, #477, #478, #479, #480, #481 | OPEN, labelled `blocked` | blocked by the step above them |

So the six issues this memo was asked to unblock (#476, #477, #478, #479, #480, #481) are **not blocked on a decision**. They are blocked on **#475**, one link up a strictly sequential chain. Verified with `gh issue view`: #475 carries `priority:medium, refactor, swarm-ready, track-b` and **no** `blocked` label. Every one of #476 to #481 carries `blocked`.

Writing a fresh A vs B memo moves none of them. Shipping #475 moves all six.

**And #423's third acceptance criterion is already met, so this memo should not claim credit for it.** The criterion reads "KK decision recorded; implementation plan issued as follow-up tasks." Both halves were satisfied on 2026-07-24 and 2026-07-25: the decision comments are in this issue's thread, and the plan issued as #472 through #481. A 2026-07-27 status comment on the same thread already says so out loud: *"this issue's decision-prep AC is satisfied."* An earlier draft of this memo described that box as "not done, and deliberately not done," which reads as though the memo declined to record a decision it was asked for. That is not what happened. The decision exists. What this memo adds is five **new** questions (D-1 to D-5) that were not blockers before, raised by what has changed in the nine days since.

What this memo does instead: re-measures the whole CSS surface nine days after Path A was chosen, checks whether the fresh numbers still support it, prices the reversal honestly, and names the single issue that actually unsticks the queue.

---

## 1. Measured inventory, theme 1.5.8, 2026-08-02

From `make css-inventory` on this worktree. Every number is reproducible; nothing here is estimated.

| File | Bytes | Lines | Rule blocks | `@media` | `!important` (raw) | Custom props | `var()` | Hex | `px` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `style.css` | 124,925 | 4,919 | 657 | 17 | 72 | 82 | 527 | 64 | 282 |
| `assets/css/revive-port.css` | 32,213 | 1,316 | 160 | 11 | 95 | 66 | 153 | 46 | 51 |
| `assets/css/typography-refined.css` | 16,758 | 688 | 70 | 5 | 6 | 0 | 81 | 0 | 19 |
| `assets/css/bleeding-edge.css` | 12,413 | 564 | 73 | 3 | 0 | 12 | 42 | 7 | 31 |
| `assets/css/animations.css` | 7,563 | 355 | 66 | 2 | 0 | 2 | 7 | 0 | 19 |
| `assets/css/editor.css` (editor only) | 5,343 | 175 | 27 | 0 | 1 | 14 | 32 | 8 | 12 |
| `assets/css/02-tokens.css` | 1,358 | 38 | 1 | 0 | 0 | 13 | 9 | 0 | 3 |
| `assets/css/09-late.css` | 1,300 | 23 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| **Total (8 files)** | **201,873** | **8,078** | **1,054** | **38** | **176** | **189** | **851** | **125** | **417** |
| **Front-end subtotal (7)** | **196,530** | **7,903** | **1,027** | **38** | **175** | **175** | **819** | **117** | **405** |

**Column basis, stated once so the table foots.** The `!important` column is **raw** (`grep -o '!important'`), which is why `09-late.css` reads 2: both of its hits are prose inside the file's opening block comment, at `09-late.css:11` and `:12`. Every cell in that column is on the same raw basis, and the cells now sum to the 176 total. An earlier draft of this table printed `09-late.css` as 0, which is its code-only value, mixed into a raw column; the cells summed to 174 against a stated 176. Corrected here.

Independent cross-check by hand, not through the tool:

```
find theme/kk-aurora -name '*.css' | wc -l                     -> 8
find theme/kk-aurora -name '*.css' -exec cat {} + | wc -c       -> 201873
find theme/kk-aurora -name '*.css' -exec grep -o '!important' {} + | wc -l  -> 176
```

Three of the 176 sit inside comments (`revive-port.css:1167`, `09-late.css:11`, `09-late.css:12`), so **173 are real declarations, 172 of them front-end**. That matches the ratchet in `.css-budget.json` exactly (`metrics.front_end_important` = 172).

### 1.1 The trend, which is the part that matters

**Basis, because an earlier draft of this table got it wrong.** Every cell below is **front-end only** (all `.css` under `theme/kk-aurora/` except `assets/css/editor.css`, which is enqueued through `add_editor_style` and never reaches a visitor) and **code-only** for `!important` (CSS block comments stripped before counting). Both historical columns were recomputed from the git objects at that commit on that basis, not copied from another document.

| | 2026-07-19 (`33887e7c`) | 1.4.3 (`0064b4e`, committed 2026-07-24) | 2026-08-02 (`dd87d4a`, 1.5.8) |
|---|---:|---:|---:|
| CSS files, front-end | 4 | 5 | 7 |
| Front-end lines | 6,044 | 7,281 | **7,903** |
| Front-end `!important` (code only) | 78 | 159 | **172** |

Method, runnable:

```
for C in 33887e7c 0064b4e dd87d4a; do
  for F in $(git ls-tree -r --name-only $C -- theme/kk-aurora | grep '\.css$' | grep -v editor.css); do
    git show $C:$F
  done | python3 -c "import sys,re;s=sys.stdin.read();print(s.count(chr(10)), re.sub(r'/\*.*?\*/','',s,flags=re.S).count('!important'))"
done
```

Two corrections to the record, both mine:

1. An earlier draft printed **6,219 / 79** in the first column and labelled the row front-end. Those are the **all-files** totals at `33887e7c`, lifted from `AURORA-STYLESHEET-REBUILD-PLAN.md` §1.1 where they are correctly labelled "Total lines" and "`!important` in CSS files". At that commit `editor.css` was 175 lines carrying 1 `!important`, so the front-end figures are **6,044 / 78**. The plan doc footnotes exactly this class of care at its own §1.1 note ².
2. The middle column previously read **160**, which is the front-end **raw** count at `0064b4e` and also, by coincidence, the all-files code-only count. The front-end code-only count is **159**. The repo's own ratchet agrees: the pre-#618 `front_end_important` value recorded in `.css-budget.json` is 159 (`#416` waiver text: "`!important` held at 159"), and the #618 waiver moves it `"from": 159, "to": 172`.

Since KK chose Path A on 2026-07-24 and the safety net shipped, front-end CSS grew **+622 lines (+8.5%)** and **+13 `!important` (+8.2%)**. The plan's target for the same metrics is 3,000 lines and 5 `!important`.

Where those numbers came from is in `.css-budget.json` waivers, and it is worth reading out loud, because it is the whole argument in miniature:

- **All 13 of the new `!important` are from #618** (Aurora 1.5.7, full-bleed portrait hero, already deployed live): +90 lines, **+13 `!important`**, waived `159 -> 172` on 2026-08-02. Waiver reason, verbatim from the file: *"The `!important` block is the light-ink-over-dark-photo override the cream-paper system forces on hero h1/dek/kicker/ghost-button."* And: *"Freeze is retroactive bookkeeping: the merge landed without a ratchet gate and left main red, blocking every theme PR."*
- **The 622 lines came from five waivers plus one unwaived step**: #485 +51, #416 +87, #494 +79, #618 +90, #596 +268 (that last one adds zero `!important`). That is 575. The remaining 47 is the gap between the 7,281 measured at `0064b4e` and the 7,328 the ratchet chain starts from, which no waiver records.

Read the #618 waiver again. The ratchet from step 0 worked exactly as designed: it went red. It was then waived after the fact because the merge had already landed and main was blocked. That is the incremental failure mode reproducing itself **inside** the Path A rollout, because the rollout stopped after step 2 while feature work kept shipping.

**Nine days of Path A being the plan of record, with the plan paused, cost 13 more `!important` and 622 more lines than the day it was chosen.**

---

## 2. Does the 139 figure from #256 still hold? Substantially yes. On a like-for-like basis it is now 151.

#256's audit deliverable (`docs/current-state/CSS-DEADCODE-OVERLAP-AUDIT.md:263`) says:

> **Legitimate and out of scope for #423 removal: 14** (reduced-motion ×8 across `style.css` and `typography-refined.css`, focus outlines ×4, print ×2). **Cascade-war casualties: 139** [EM DASH IN ORIGINAL] 57 in `style.css`'s two hardening blocks and all 82 in `revive-port.css`. The remaining 7 are one-off overrides of WordPress block defaults and `theme.json` presets.

**One alteration, disclosed.** The source uses an em dash where this quote prints `[EM DASH IN ORIGINAL]`, because this repo's writing rules forbid that character. Nothing else is changed: the ×, the file names, the trailing sentence and all four numbers are as written at `CSS-DEADCODE-OVERLAP-AUDIT.md:263`. An earlier draft of this memo silently swapped the em dash for parentheses, downgraded × to x, dropped "across `style.css` and `typography-refined.css`", and dropped the final sentence. Quoting is not the place to be quiet about edits, so the full text is restored here.

Re-classified with one brace-tracking classifier run over **both** trees, so the two columns come from the same code rather than from two different people's judgement. Comments stripped, at-rule context tracked, `editor.css` excluded on both sides. A declaration counts as legitimate if it sits inside a `prefers-reduced-motion` / `print` / `forced-colors` / `prefers-contrast` at-rule, as focus if its property is `outline*` **or** its selector contains `:focus`, and as cascade war otherwise.

| Category | 1.4.3 (`0064b4e`) | 1.5.8 (`dd87d4a`) | Δ |
|---|---:|---:|---:|
| Legitimate: `prefers-reduced-motion`, `print`, `forced-colors`, `prefers-contrast` | 10 | 10 | 0 |
| Focus / outline declarations | 11 | 11 | 0 |
| **Cascade war** | **138** | **151** | **+13** |
| Front-end total (code only) | 159 | **172** | +13 |

Per file at 1.5.8: `style.css` 72 (6 legitimate, 4 focus, **62 cascade war**), `revive-port.css` 94 (0 legitimate, 7 focus, **87 cascade war**), `typography-refined.css` 6 (4 legitimate, **2 cascade war**).

**How this squares with #256's 139.** #256's own arithmetic is 14 + 139 + 7 = **160**, the all-files code-only count at 1.4.3. Its 21 non-cascade declarations (14 legitimate/focus plus 7 block-default one-offs) is the same 21 this classifier finds (10 legitimate + 11 focus), so the two classifications agree on the boundary and differ only on where `editor.css`'s single editor-only declaration lands. #256's **139 all-files is this pass's 138 front-end**. The figure was right when it was written.

Two corrections to an earlier draft of this section, both mine:

1. It reported **154** cascade war at 1.5.8. That is 3 too many. It counted only `outline` properties as focus declarations and so pushed `revive-port.css:163` (`box-shadow: none !important`), `:173` (`background`) and `:174` (`color`) into the cascade-war bucket, even though all three sit inside `:focus` / `:focus-visible` rules (`revive-port.css:152-175`). Correct figure: **151**, with `revive-port.css` at 7 focus, not 4.
2. It compared today's number against #256's 139 without re-running the classifier on the 1.4.3 tree, so the "+15" was a delta between two different classifications. Re-run on both trees, the delta is **+13**.

**So the finding is not that #256 was wrong. It is that cascade-war declarations went 138 to 151, up 9.4%, and that all 13 of the additions are exactly the 13 the #618 hero waiver booked.** Nothing else moved: legitimate held at 10, focus held at 11. The debt grew in one place, for one reason, and the ratchet named it.

### 2.1 Duplication, unchanged in kind, slightly worse in degree

From the same `make css-inventory` run:

| Metric | 1.4.3 (plan §1.5) | 1.5.8 (now) |
|---|---:|---:|
| Distinct selectors | 1,070 | 1,153 |
| Selectors declared more than once | 317 | **324** |
| Redundant declarations | 559 | **568** |
| Selectors in more than one file | 75 | 75 |
| Distinct custom-property names | 114 | **129** |
| Distinct `@media` width values | 12 | **12** |

Worst offenders now: `h3` 10x, `.aurora-page-title` 9x, `.aurora-card` 8x, `.aurora-writing-archive-title` 8x, `:root` 7x, `h2` 7x, `h4` 7x, `.aurora-page-2026` 7x.

The 12 breakpoints are unchanged: `min-width` 780, 782, 800, 900, 960 and `max-width` 360, 560, 700, 781, 900, 980, 1180. 780, 781 and 782 still coexist. That is #479's entire premise and it has not moved.

### 2.2 Coverage, from `make css-coverage` (live corpus, 14 routes, 13 HTTP 200)

| Metric | Value |
|---|---:|
| Theme-authored classes in front-end CSS | 286 |
| Unmatched in any rendered markup | 95 (33.2%) |
| High-confidence dead | 88 (30.8%) |
| Medium, needs eyeballs | 3 |
| Protected (WP/JS/PHP/editor) | 4 |
| Fully-removable rule blocks | **165 (21,559 bytes)** |

This is real data from live markup, not the 53% repo-only heuristic the plan warned about. 21,559 bytes is 11.0% of the 196,530-byte front-end surface. That is #478's actual size.

Caveat worth flagging, because it is a live false positive: the fresh dead list still contains `aurora-hero-2026`, which is the class the #618 hero shipped on 2026-08-01 and which renders on `/` and `/about/` today. The coverage tool is directionally right and individually wrong. Nothing gets deleted off this list without a per-class check, exactly as #478's body says.

---

## 3. The drop cap: confirmed, and slightly different from how #475 describes it

### 3.1 The rule

`theme/kk-aurora/assets/css/typography-refined.css`, lines 141 to 151:

```css
/* Drop cap for first paragraph */
article > p:first-of-type::first-letter,
.entry-content > p:first-of-type::first-letter {
  float: left;
  font-size: 3.5em;
  line-height: 0.8;
  padding-right: 0.1em;
  margin-top: 0.05em;
  font-weight: 700;
  color: var(--wp--preset--color--signal);
}
```

#475 cites "141 to 165". The rule itself is **142 to 151**. Lines 153 to 161 and 163 to 171 are two theme-side neutralizers (`.aurora-page-content > p:first-of-type::first-letter` and `.aurora-prose > p:first-of-type::first-letter`, both `color: inherit; float: none; font-size: inherit; ...`). So the cited range covers the rule plus one of its own antidotes. Minor, but worth correcting before someone deletes a range by line number.

This is the theme's **only** drop-cap source. `grep -rn "drop-cap\|dropCap\|initial-letter" theme/kk-aurora/` returns nothing. `theme.json` does not enable the core drop cap.

The theme therefore already fights its own rule in two places, without `!important`, because those two neutralizers have higher specificity than the wrappers used in page content.

### 3.2 What it actually hits on live pages

Verified by GET, logged out, 2026-08-02. `<article>` elements rendered on live pages:

```
/work/     8 x <article class="aurora-media-card">
/about/    8 x, mix of aurora-media-card and aurora-card
/contact/  4 x <article class="kk-contact-card">
/          6 x <article class="aurora-service-card">
```

Each of those cards contains a `<p>` as a direct child. `article > p:first-of-type::first-letter` matches all of them. The claim in #475 that the rule "hits every `<article class="aurora-card">` in the content packs, not just prose openings" is **confirmed against live markup**.

Homepage detail, because it is the sharpest example. Live `/` markup:

```html
<article class="aurora-service-card" style="--service-ribbon:linear-gradient(...)">
  <p class="aurora-kicker">I.</p>
  <h3>Keynote</h3>
  ...
```

`<p class="aurora-kicker">I.</p>` is the first-of-type `<p>` inside that article. There is no `::first-letter` neutralizer anywhere in theme CSS for `.aurora-kicker` or `.aurora-service-card` (only six `::first-letter` selectors exist in the whole theme; `grep -rn "first-letter" theme/kk-aurora/`). So the numeral "I" in the roman-numeral kicker is being rendered at 3.5em, floated left, in signal orange, on the live homepage. The cascade says so. I did not run a browser render to confirm it visually, and that render is precisely what #475's pixel gate is for. **Cascade-verified, not pixel-verified.**

### 3.3 Five pages carrying 12 to 17 `!important` each, purely to defeat it

Partly true. Measured directly from live HTML, counting only anonymous `<style>` blocks in `<body>` (that is, page-content CSS, not WP-generated inline styles):

| Route | Anon `<style>` bytes | `!important` total | of which inside a `::first-letter` rule |
|---|---:|---:|---:|
| `/about/` | 3,488 | **25** | 8 |
| `/contact/` | 5,422 | 17 | 10 |
| `/speaking/` | 959 | 14 | 8 |
| `/work/` | 959 | 14 | 8 |
| `/services/` (canonical `/generative-ai-services/`) | 4,418 | 13 | 8 |
| `/photography/` | 5,024 | 12 | 8 |
| `/publications/` | 15,386 | **0** | 0 |
| `/events/` | 2,182 | **0** | 0 |
| **Total, 8 routes** | **37,838** | **95** | **50** |

Three corrections to the record:

1. **It is six routes with `!important`, not five.** `/about/` is the sixth and it has the worst count.
2. **"Purely to defeat it" is an overstatement.** 50 of 95, just over half, are drop-cap suppression. The remaining 45 are button colour, card radius, box-shadow, and hero-ink overrides. Retiring the drop cap removes about half the problem, not all of it.
3. **The surface grew and the count fell.** #256's audit recorded 29,030 bytes with 113 `!important` across 8 routes. Today: **37,838 bytes with 95 `!important`** across 8 routes. `/publications/` alone accounts for 15,386 of those bytes with zero `!important`. So the page-content CSS layer is 30% larger by weight and 16% cleaner by `!important` than when #256 measured it.

The suppression block itself, byte for byte from live `/work/`:

```css
.kk-r9-pack :where(p, li)::first-letter {
  initial-letter: normal !important;
  font-size: inherit !important;
  font-weight: inherit !important;
  float: none !important;
  margin: 0 !important;
  line-height: inherit !important;
  color: inherit !important;
  background: transparent !important;
}
```

The `!important` here is **structurally forced, not lazy**. Specificity of the theme rule `article > p:first-of-type::first-letter` is (0,1,2). Specificity of the content rule `.kk-r9-pack :where(p, li)::first-letter` is (0,1,0), because `:where()` contributes zero. The content rule loses on specificity, so without `!important` it does nothing. Whoever wrote it had no cheaper option from inside page content.

### 3.4 `/about/` is the live proof that the problem is still growing

`/about/`'s inline block was 959 bytes with 14 `!important` when #480's table was written. It is now **3,488 bytes with 25 `!important`**. The added 11 arrived with the #618 portrait hero on 2026-08-01, and the block carries its own comment explaining why:

```css
.aurora-about-page .aurora-hero-2026 :where(#aurora-about-title, .aurora-hero-copy h2) {
  color: #f7f7f2 !important;
  -webkit-text-fill-color: #f7f7f2 !important;
}
```

The comment sitting directly above that rule in the live page source gives the reason: light ink over a dark portrait hero, because the cream-paper system forces dark `!important` on `h2` and `p`. (Declarations quoted verbatim; the comment line is paraphrased because it contains a character this repo's writing rules forbid.)

That is one page-content CSS block, on a pixel-gate route, growing by 2.5 KB and 11 `!important` **nine days after the site committed to deleting all six of these blocks in step 7 (#480)**. Same root cause as the theme-side +13 in the #618 waiver: the cream-paper system has no dark-surface token, so any dark-photo hero must be overridden by force, in whichever layer the author happens to be standing in.

---

## 4. The full CSS surface on a live page: eight layers, one of which the theme cannot see

Measured on `/about/`, logged out, 2026-08-02, in document order. Every `<style>` block on the page is enumerated, so the byte counts partition the page rather than overlapping:

| # | Surface | Bytes | `!important` | Owner |
|---|---|---:|---:|---|
| 1 | Jetpack Boost concatenated bundle (`s5102.pcdn.co/wp-content/boost-cache/static/ec2a031717.min.css`), the **only** `<link rel=stylesheet>` on the page | **142,406** | **172** | all 7 front-end theme sheets, minified into one file |
| 2 | 7 WP core inline `<style>` blocks that print before `global-styles` | **4,778** | 2 | WordPress |
| 3 | `global-styles-inline-css`, generated from `theme.json` | **27,348** | **137** | WordPress, from `theme/kk-aurora/theme.json` |
| 4 | `core-block-supports-inline-css` | 1,040 | 6 | WordPress |
| 5 | Anonymous `<style>` in `<body>`, from page content | **3,488** | **25** | Track A, WP database |
| 6 | Jetpack Boost critical CSS (`/` and `/blog/` only, `<style id="jetpack-boost-critical-css">`) | 7,474 on `/`, 15,332 on `/blog/` | 1 | Jetpack |
| 7 | `fixes/*.css` (4 files, 11,796 B, 17 `!important`) | not enqueued | 17 | repo, deployed by hand when needed |
| 8 | **Code Snippets CSS** (see §4.1) | **0 on the front end today** | 0 | live wp-admin, Code Snippets plugin |

**Surface 1 is now measured, not carried over.** An earlier draft printed `~138 KB / ~159` from `AURORA-STYLESHEET-REBUILD-PLAN.md` §1.6 (measured 2026-07-25 at 1.4.3) and flagged it as approximate. Re-fetched today: `curl -sSL https://s5102.pcdn.co/wp-content/boost-cache/static/ec2a031717.min.css` redirects to `kriskrug.co` and returns **142,406 bytes with 172 `!important`**. That 172 is the same number as the repo's front-end code-only count, which is the cleanest available confirmation that the bundle is the theme sheets and nothing else. The bundle's first bytes are `@layer reset,tokens,base,primitives,components,patterns,utilities,overrides;`, so step 2 is in production.

**Surface 2 is corrected.** An earlier draft printed `8 blocks / ~5.8 KB / 2`. The live scrape finds **7** blocks totalling **4,778 bytes** with 2 `!important`: six `wp-block-*-inline-css` blocks (4,643 B, the 2 `!important` both in `wp-block-library-inline-css`) plus `wp-img-auto-sizes-contain-inline-css` (135 B, 0). The 5,818 figure only reconciles by folding in `core-block-supports-inline-css` (1,040 B), which is surface 4 in the same table, and folding in its bytes while leaving out its 6 `!important`. Double count, now removed.

Two facts from this table drive everything:

- **Surface 3 prints after surface 1.** `theme.json`'s generated CSS lands after the entire theme bundle and is unlayered. At equal specificity it wins. That single ordering fact is the mechanical reason most of those 151 cascade-war `!important` declarations exist: the theme is fighting its own token layer from one document position too early. Step 2 (#474) already shipped the answer to this, `09-late.css`, and it is currently **empty by design** (23 lines, all comment). Nothing has needed it yet, which is a good sign for the mechanism and no evidence at all about the migration.
- **Surface 5 beats every enqueued sheet.** Inline `<style>` in `<body>` wins on source order at equal specificity, and 25 of those declarations carry `!important` on top. Any rebuild that changes `.aurora-button`, `.aurora-card`, or `.aurora-media-card` gets silently overridden on six routes. This is not a tidy-up item. It is a hard dependency in whichever direction the decision goes.

**Repo and live are in sync except for `style.css`.** md5 comparison of all 7 front-end sheets on 2026-08-02: `02-tokens.css`, `typography-refined.css`, `animations.css`, `bleeding-edge.css`, `revive-port.css`, `09-late.css` all **MATCH**. `style.css` **DIFFERS** (live 119,167 B at 1.5.7, repo 124,925 B at 1.5.8, delta is the 268-line `aurora-tstm` block from #596, gated on the #601 pixel gate). Live `style.css:20` already carries `@layer reset, tokens, base, primitives, components, patterns, utilities, overrides;`, so **step 2 is genuinely in production**, not just in the repo. The repo inventory in section 1 is production truth to within one undeployed component.

### 4.1 Code Snippets CSS, the fourth surface #423 names

#423's Scope names four surfaces: theme stylesheets, inline page-content style blocks, **Code Snippets CSS (KK Asset Diet)**, and Jetpack Boost critical CSS. An earlier draft of this memo inventoried three and skipped this one. Here it is.

**Source and its limits, stated up front.** `https://kriskrug.co/wp-json/code-snippets/v1/snippets` returns **HTTP 401** unauthenticated, and no `WP_USER` / `WP_APP_PASSWORD` resolved in this session (`varlock run --inject vars` returned zero-length for both), so there is **no authenticated live read here**. What follows is two things that are checkable: the repo-side snapshot of all 13 snippets, and a live front-end scrape of what actually reaches a logged-out browser today.

Snapshot: `backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json`, 13 snippets, captured 2026-07-24.

| id | Active | Scope | Name | Code bytes | `!important` | Emits CSS? |
|---:|---|---|---|---:|---:|---|
| 5 | yes | global | KK Schema | 9,446 | 0 | no, JSON-LD |
| 7 | yes | front-end | KK SEO root files | 6,517 | 0 | no |
| 8 | yes | front-end | GSC404 query param canonicalize | 2,330 | 0 | no |
| **10** | **yes** | front-end | **KK Asset Diet** | **2,867** | **0** | **no, and it removes CSS** |
| 13 | yes | front-end | KK News Sitemap | 2,809 | 0 | no |
| 9 | **no** | front-end | A11Y CTA contrast hotfix 2026-06-18 | 736 | 0 | **yes**, `<style id="kk-a11y-cta-contrast-20260618">` at `wp_head` priority 30 |
| 11 | **no** | front-end | TEMP Aurora 1.3.33 a11y contrast fallback | 1,950 | **15** | **yes**, `<style id="kk-aurora-a11y-133-fallback">` at `wp_head` default priority |
| 1, 2, 3, 4, 6, 12 | no | mixed | filename case, admin bar, smilies, current year, projects redirect, OG meta | 6,082 combined | 0 | no |

**KK Asset Diet is not a CSS surface. It is a negative one.** Snippet #10 is 2,867 bytes of PHP with zero CSS in it. Its four actions all subtract from what loads: it drops `search`, `carousel` and `sharedaddy` from `jetpack_active_modules`, drops jQuery Migrate, returns false from `pum_popup_is_loadable` and `wp_dequeue_style('popup-maker-site')`, and dequeues jQuery. `docs/current-state/archive/ASSET-DIET-2026-06-28.md:5` records the effect: the homepage went from 2 CSS + 12 JS requests to 1 CSS + 4 JS. That is why surface 1 is the only `<link rel=stylesheet>` on the page.

**Live confirmation, logged out, across 13 routes: all 11 pixel-gate routes plus `/publications/` and `/events/`.** Every `<style>` element carrying an `id` was enumerated on `/`, `/about/`, `/generative-ai-services/`, `/speaking/`, `/work/`, `/photography/`, `/blog/`, `/contact/`, `/publications/`, `/events/`, `/2026/07/18/i-am-nomad-ai-film/`, `/category/vancouver-ai-ecosystem/` and the `/definitely-not-a-page-404-probe/` 404 route, then filtered against the known WordPress and Jetpack handle set (`wp-*`, `global-styles-inline-css`, `core-block-supports-inline-css`, `jetpack-boost-critical-css`, `classic-theme-styles`). **Unknown ids: zero, on every route.** Neither `kk-a11y-cta-contrast-20260618` nor `kk-aurora-a11y-133-fallback` appears anywhere, and no id on any route contains `code-snippets`. So the two CSS-emitting snippets are still inactive in production, exactly as the 2026-07-24 snapshot says, and no snippet activated since that snapshot is emitting CSS either.

That last clause matters more than the first: because the check is "enumerate every id and subtract the known set" rather than "look for two specific ids," it would have caught a *new* CSS snippet too. This is a positive result about live state today, not just a re-read of a month-old file.

**Load order, for the record.** Both CSS snippets print from `wp_head`, at priority 30 and at the default 10. `wp_print_styles` runs at `wp_head` priority 8, so a snippet style block would land **after** every enqueued sheet and after `global-styles-inline-css`, i.e. between surface 4 and surface 5 in the section 4 table. It would beat the entire theme on source order without needing a single `!important`. Snippet #11's 15 `!important` were therefore belt-and-braces, not necessity. Worth knowing before anyone reaches for a snippet as a hotfix during the rebuild.

**Two caveats I will not paper over.**

1. The snapshot is provably stale by at least one snippet. Live Code Snippet **#14** (`TEMP Aurora 1.4.0 cream contrast file apply`) is not in it, and it is the R-3 risk in `AURORA-STYLESHEET-REBUILD-PLAN.md` §5. #14 is a PHP file-apply that overwrites `style.css` and `revive-port.css` on the production filesystem from media zip #12631 at `init`. That is not an eighth stylesheet; it is a mutation hazard **on surface 1**. It stays in D-5, unchanged.
2. Jetpack Boost concatenates enqueued stylesheets, so a snippet that *enqueued* a sheet rather than printing inline could hide inside surface 1. Both known CSS snippets print inline, so this does not apply to them, and surface 1's 172 `!important` matching the repo's front-end 172 exactly is evidence that nothing extra is folded into the bundle. It is evidence, not proof. An authenticated `code-snippets/v1/snippets` read is still the only way to close this to certainty, and it is the same wp-admin trip as D-5.

**Bottom line for the decision:** the Code Snippets surface contributes **zero bytes and zero `!important`** to the live front end today, and one active snippet actively shrinks the surface. It changes nothing about A vs B. It is inventoried here because #423 asked for it and because the reader deserves to know it was checked rather than assumed.

---

## 5. Pixel-gate exposure: what each path puts at risk across the 11 routes

The gate is `make visual-diff` against `scripts/visual_baseline.py`: 11 routes x 3 viewports (375, 768, 1440) at 2x device scale = **33 comparisons**. Tolerance: pass at or below 0.1% differing pixels, warn to 1.0%, fail above. Last recorded run (`report-BASE2.md`, 2026-07-25) was 33 pass, 0 warn, 0 fail, most of them sha256-identical.

Exposure measured per route by GET on 2026-08-02:

| Route | `<article>` | `.entry-content` | Drop-cap suppressor present | Page-content CSS | Exposed to a drop-cap change |
|---|---:|---:|---|---|---|
| `/` | 6 | 0 | **no** | none | **yes, unsuppressed** |
| `/about/` | 8 | 1 | yes | 3,488 B / 25 | no (already suppressed) |
| `/generative-ai-services/` | 4 | 1 | yes | 4,418 B / 13 | no |
| `/speaking/` | 8 | 1 | yes | 959 B / 14 | no |
| `/work/` | 8 | 1 | yes | 959 B / 14 | no |
| `/photography/` | 0 | 1 | yes | 5,024 B / 12 | no |
| `/blog/` | 19 | 0 | **no** | none | **yes, unsuppressed** |
| `/contact/` | 4 | 1 | yes | 5,422 B / 17 | no |
| `/2026/07/18/i-am-nomad-ai-film/` | 1 | 1 | **no** | none | **yes, unsuppressed** |
| `/definitely-not-a-page-404-probe/` | 0 | 0 | no | none | no article, no exposure |
| `/category/vancouver-ai-ecosystem/` | 0 | 0 | no | none | no article, no exposure |

Read across: **9 of 11 routes carry `<article>` or `.entry-content`. 6 of those already suppress the drop cap from page content, so deleting the theme rule is a no-op there. 3 of them (`/`, `/blog/`, single post) do not suppress it, so those are the three that will move pixels.** Two routes (404, category archive) are structurally immune.

That is a usefully small blast radius and it is why #475 is genuinely shippable: the change is expected-diff on 3 routes out of 11, and zero-diff on 8. The AC on #475 already says exactly that ("Drop-cap change reviewed and approved by KK as an expected visual diff", "No other visual diff on the 11 routes"). The measurement above tells you in advance which 3 to look at.

**Path-level exposure:**

| Path | Routes at risk per shipped increment | Comparisons per increment | Worst-case blast radius |
|---|---|---:|---|
| A, as sequenced now (#475 to #481) | 3 of 11 for #475; 11 of 11 for #476 (primitives touch every page); 1 to 4 for each #477 component PR; 11 for #478 and #481 | 33 per PR | Bounded per step, because each step is one deployable zip with a documented re-upload rollback |
| B, incremental repair | 1 to 3 per fix, but **unbounded over time** because there is no step boundary and no end state | 33 per PR if run, and #618 shows it is not always run | The #618 pattern: merge lands, ratchet goes red, waiver gets written after the fact |

The single most important row in that table is the last one. Path B has no worse per-PR pixel risk than Path A. It has worse **governance** risk, and there is a dated, in-repo example of exactly that failure from yesterday.

---

## 6. The two options, stated fairly

### Path A: ground-up token-based rebuild

Rebuild the hierarchy on `@layer` and `theme.json` tokens. Eight layers, one prefix (`kk-`), three breakpoints, zero authored `!important` outside a commented quarantine file. Nine steps, each one PR, each individually revertible by re-uploading the previous version's zip, each gated on a green 33-comparison pixel diff. Fully specified in `AURORA-STYLESHEET-REBUILD-PLAN.md`.

**The honest case for it:**

- The debt is measurably still growing under every non-rebuild regime tried so far: 78 to 159 to 172 `!important`, 6,044 to 7,281 to 7,903 lines, all front-end and code-only on both sides. Two separate measurement windows, same direction.
- The root cause is structural and named: `theme.json` prints after the theme bundle and is unlayered, so overriding it requires `!important` unless you change the layering. No amount of careful per-component work fixes that. #474 already proved the fix works and deployed it to production.
- The safety net is real and already paid for. #472's ratchet, #473's 33-comparison harness, `.css-budget.json` with an audit trail of every waiver. That was the expensive part of Path A and it is done.
- 21,559 bytes of provably removable CSS (11% of the front end) is sitting there with a per-class rollback note already written (#468's audit).
- Track A page content is 37,838 bytes of CSS that will silently override anything the theme does to `.aurora-button` / `.aurora-card` / `.aurora-media-card`. Only a plan that includes #480 addresses it. Path A includes it as step 7.

**The honest case against it:**

- It is 6 remaining steps of Track B work with zero user-visible benefit. Nobody visiting kriskrug.co gets anything from it.
- Path A has been the plan of record for nine days and has advanced by zero steps, while feature work shipped twice (1.5.7, 1.5.8) and made the numbers worse. The revealed constraint is not the plan, it is attention. A better plan does not create attention.
- Step 8 (#481, the rename) touches live database content that references `aurora-*` class names. That is the widest blast radius in the repo, and it is the one step whose rollback is a content restore, not a zip re-upload.
- The 172 `!important` are, right now, load-bearing. Every one of them is holding up a rendering that currently passes an accessibility contrast registry (`test_aurora_css_literal_contrast.py`). Removing them without a per-declaration replacement is how you ship a contrast regression.

### Path B: incremental repair

No teardown. Keep the current file layout. Fix components as they come up in content and design work. Enforce "no new `!important`" via the #472 ratchet. Let the numbers drift down through boy-scout work.

**The honest case for it:**

- The site works. Nothing on this list is a user-facing bug.
- Zero coordination cost. Any agent can take any Wave 2 issue at any time without waiting for a step above it. That is the opposite of today's situation, where six issues sit behind one.
- The two pieces of Path A that actually pay for themselves are already shipped and are path-independent: the ratchet (#472) and the pixel harness (#473). Keeping those and dropping the rest retains most of the value at none of the remaining cost.
- Two of the highest-value items do not need the rebuild at all. #479 (12 breakpoints to 3) and #478 (delete 21,559 bytes of dead CSS) are self-contained and would be worth doing under either path.

**The honest case against it:**

- It has been tried, measured, and it lost. Twice. 78 to 159 across the 1.4.x Revive port while B was nominally in force, then 159 to 172 across 1.5.7 and 1.5.8 while A was nominally in force but paused. In both windows a shipping feature added `!important` faster than cleanup removed it.
- `style.css` improved by exactly 1 declaration (72 to 71 to 72) across the whole period. Surgical fixes work where applied and are swamped by everything else.
- It leaves the `theme.json` ordering problem in place permanently, which means every future dark-surface component pays the same `!important` tax. The #618 hero paid it twice in one day, once in theme CSS (+13) and once in `/about/` page content (+11).
- It does nothing for the six Track A page-content blocks, which are the surface most likely to bite a future redesign.

### The third option nobody wrote down: what is actually happening

Path A is the recorded decision, steps 0 to 2 shipped, steps 3 to 8 are stalled, and feature work continues under de facto Path B rules with retroactive waivers. This is the **worst** of both: the coordination cost of A (six issues blocked behind one) plus the drift of B (+13 `!important` in nine days) plus a growing gap between the plan doc and reality.

Whatever KK decides, deciding is better than this. That is the real finding of this memo.

---

## 7. Cost and risk

| | Path A (finish it) | Path B (stop and repair) | Status quo (A on paper, B in practice) |
|---|---|---|---|
| Remaining work | 6 issues: #475, #476, #477 (8 sub-PRs), #478, #479, #480, #481 | 0 mandatory; #478 and #479 optional and worth doing | 0 planned, unbounded actual |
| Sequencing | Strictly serial. #476 needs #475, #477 needs #476, #481 needs #477 | Fully parallel | Serial and stalled |
| Deploys required | 6 or more theme uploads, each KK-gated, each with a zip rollback | 0 extra beyond normal work | as they come |
| Pixel gate runs | 33 comparisons per PR, roughly 14 PRs | per PR as today | inconsistent, see #618 |
| Track A involvement | Mandatory (#480, 6 live pages, snapshot + slug-verify each) | None | None |
| Live-content risk | Highest at #481 (rename touches DB content) | None | None |
| Rollback story | Re-upload the previous version's zip per step (each step is one deployable theme version); content snapshot + slug-verified restore for #480 and #481; `make visual-diff` against the pre-deploy live baseline is the detector | Per-PR `git revert` plus a re-upload of the last-good theme zip. No step boundary, so there is no "roll back to the last known-good architecture" move, only "roll back the last PR". If a Path B fix is later found to have been wrong, the detector is `make css-inventory-check` going red or someone noticing on the page, not a gate | Whatever the last PR's rollback was. #618 is the worked example: the merge landed, the ratchet went red, main was blocked for every theme PR, and the resolution was a retroactive waiver rather than a revert |
| End state | ~3,000 lines, 5 `!important`, 1 prefix, 3 breakpoints, 0 page-content blocks | ~7,900 lines, ~170 `!important`, drifting | drifting faster |
| Cost of being wrong | Weeks of Track B time with no user benefit; a bad step is one zip re-upload away from reverted | Debt keeps compounding at roughly +1.4 `!important` per day (13 over the 9 days from `0064b4e` to `dd87d4a`) | both |
| Blocks the redesign? | Yes, partially. #424 waits on #476, #127 waits on #479 | No | Yes |

Two things are true at once and both belong in the decision: **Path A's remaining work is real and unglamorous**, and **Path B's measured track record on this specific codebase is two consecutive losses**.

---

## 8. What each path does to the six blocked issues

| Issue | Path A (finish it) | Path B (stop and repair) |
|---|---|---|
| **#476** primitives + editor parity (1.5.2) | Unblocked the moment #475 merges. Also unblocks #424 | Rescope. The editor-canvas bug (editor loads `style.css` + `editor.css` only, so it renders the pre-Revive dark palette) is a real standalone bug worth fixing on its own. Split it out and ship it. Drop the "62 tokens behind semantic aliases" half |
| **#477** component migration (1.5.3+) | Unblocked after #476. 8 sub-PRs, worst-first: `.aurora-writing-card` (84 occurrences, 6 declaration sites in `style.css`) leads | Close as an epic. Keep `.aurora-writing-card` as a single standalone issue, because 6 declaration sites in one file is a defect regardless of architecture |
| **#478** delete dead CSS (1.6.0) | Unblocked after #477. Coverage data already exists: 165 blocks, 21,559 bytes | **Unblock immediately.** This needs no rebuild. It needs the live corpus and per-class care. Highest value-per-risk item on the whole list |
| **#479** 12 breakpoints to 3 | Lands alongside #477. Unblocks #127 | **Unblock immediately.** Also independent of the rebuild, also unblocks #127 |
| **#480** retire Track A page-content CSS | Unblocked after #475 removes the drop-cap cause. Deletes 50 of the 95 `!important` cheaply | Partially doable now. The 45 non-drop-cap declarations can go today. The 50 drop-cap ones cannot, because the theme rule beats them on specificity (section 3.3). **This is the one issue where Path B is genuinely blocked and Path A is not** |
| **#481** rename to `kk-` | Last, after everything. Widest blast radius | Close it. A cosmetic rename across live DB content, with no rebuild underneath it, is pure risk |

The asymmetry is sharp and worth saying plainly. **Under either path, #478 and #479 should be unblocked right now.** They are self-contained, they are the two largest measured wins (21,559 dead bytes, 12 breakpoints to 3), and neither depends on the layer architecture. Leaving them labelled `blocked` behind #475 is a sequencing artifact, not a technical dependency.

And **#475 is the keystone.** It is open, unblocked, swarm-ready, and it is what stands between the current state and six unblocked issues. Section 5 tells you its blast radius in advance: 3 of 11 routes will move, 8 will not.

---

## 9. Recommendation

**Finish Path A, but re-sequence it so it stops holding six issues hostage, and ship #475 this week.**

Concretely, four moves:

1. **Ship #475 now.** It is open, unblocked, and it is the single action that unblocks #476, #477, #480 and (through them) #424. Its blast radius is measured and small: 3 routes of 11 change, and the change is the deliberate one. Retire the drop cap outright rather than gating it behind an opt-in class. Nothing on the live site uses it intentionally, six pages pay `!important` to suppress it, and the three routes where it does render (`/`, `/blog/`, single post) render it on card kickers, which is not what a drop cap is for.
2. **Un-block #478 and #479 today, independent of everything else.** Neither needs the layer architecture. Together they are the largest measured win available (21,559 dead bytes, 12 breakpoints down to 3) and #479 also frees #127. Relabel them and let them run in parallel.
3. **Split the editor-canvas bug out of #476 and fix it separately.** "The block editor renders the pre-Revive dark palette while the front end is cream" is a live defect that hurts KK every time he edits a page. It should not wait behind a token-alias refactor.
4. **Defer #481 indefinitely.** It is a rename across live database content with the widest blast radius of anything on the list and the least payoff. Revisit it only after #477 completes, if it still looks worth it. It probably will not.

**Confidence: high on the measurements, medium on the recommendation.**

High on the measurements: every number in this memo is reproducible with a command printed next to it, cross-checked by hand against the tool output, and where it touches live rendering it was checked with a real GET on 2026-08-02.

Medium on the recommendation, for one specific reason I cannot measure: Path A has been the recorded decision for nine days and advanced zero steps. If the constraint is KK's attention rather than the plan's quality, then re-affirming Path A produces another nine days of the same, and the numbers say the status quo costs roughly **+1.4 `!important` per day**. Moves 2 and 3 above are hedges against exactly that: they extract the two largest wins on paths that do not depend on anyone finishing a nine-step sequence.

What would change my mind toward Path B: if KK's read is that no more than one or two Track B sessions are available over the next month. In that case the honest answer is to take #478 and #479, close the rest, and stop pretending the rebuild is queued.

---

## 10. DECISION BLOCK FOR KK

**Nothing below has been actioned. These are five new questions, not a re-run of the A vs B decision.**

You answered the headline question on 2026-07-24 and reconfirmed it on 2026-07-25, and #423's "KK decision recorded" criterion has been satisfied since then. This block does not reopen that. It asks about the things that have changed since, and about the sequencing that has six issues stuck behind one.

### D-1. Does Path A still stand?

- [ ] **A, as recorded.** Finish the nine steps. Next action: assign #475.
- [ ] **A, re-sequenced** (this memo's recommendation). Finish it, and un-block #478 and #479 to run in parallel now, and split the editor bug out of #476, and defer #481.
- [ ] **Switch to B.** Stop the rebuild. Take #478 and #479 as standalone work. Close #476, #477, #481. Rescope #480 to the 45 non-drop-cap declarations. Update `AURORA-STYLESHEET-REBUILD-PLAN.md` with a Historical banner.

### D-2. The drop cap (#475). This is the keystone and it needs your eye, not an agent's.

`article > p:first-of-type::first-letter` at `typography-refined.css:142`. It renders a 3.5em floated orange first letter on the first paragraph of every `<article>`. On live `/`, that means the "I" in the roman-numeral kicker of each service card.

- [ ] **Delete it.** Recommended. 3 of 11 pixel-gate routes change (`/`, `/blog/`, single post), 8 do not.
- [ ] **Gate it behind one opt-in class** (`.kk-dropcap`). Same diff, keeps the option.
- [ ] **Keep it.** Then #480 stays permanently blocked on its 50 drop-cap `!important` declarations, and every future content pack pays the same tax.

### D-3. Un-block #478 and #479 independent of the rebuild?

Neither depends on the layer architecture. Together: 21,559 measured dead bytes and 12 breakpoints to 3, and #479 also frees #127.

- [ ] Yes, relabel both and let them run in parallel
- [ ] No, keep them sequenced behind #477

### D-4. The ratchet waiver policy, after #618

On 2026-08-01, #618 merged with +13 `!important`, the #472 ratchet went red, main was blocked for every theme PR, and the waiver was written retroactively. The waiver text in `.css-budget.json` says so itself. The gate worked; the process routed around it.

- [ ] **Waivers must be pre-approved.** A PR that raises a budget number does not merge until KK has signed the waiver text.
- [ ] **Keep retroactive waivers** but require the PR body to state the delta up front, so nobody merges blind.
- [ ] Leave it as is.

### D-5. Anything that needs wp-admin, which no agent can check

Risk R-3 from `AURORA-STYLESHEET-REBUILD-PLAN.md` §5, still open and still only checkable by you: **live Code Snippet #14** (`TEMP Aurora 1.4.0 cream contrast file apply`) overwrites `style.css` and `revive-port.css` on the production filesystem from media zip **#12631** at `init`. If it is still active, any theme upload can be silently clobbered by a stale zip.

- [ ] Confirmed retired and media #12631 deleted
- [ ] Still active, needs handling before the next theme deploy
- [ ] Not checked yet

---

## Appendix: how to reproduce every number here

| Number | Command |
|---|---|
| Section 1 inventory table | `make css-inventory` |
| Same as JSON | `make css-inventory-json` |
| File count, bytes, raw `!important` | `find theme/kk-aurora -name '*.css' \| wc -l` ; `find theme/kk-aurora -name '*.css' -exec cat {} + \| wc -c` ; `find theme/kk-aurora -name '*.css' -exec grep -o '!important' {} + \| wc -l` |
| Section 2.2 coverage | `make css-coverage` |
| Section 3.1 drop-cap rule | `awk 'NR>=140 && NR<=172' theme/kk-aurora/assets/css/typography-refined.css` |
| Only drop-cap source in theme | `grep -rn "drop-cap\|dropCap\|initial-letter\|first-letter" theme/kk-aurora/` |
| Sections 3.3, 4, 5 live data | `curl -sS -L https://kriskrug.co<route>`, then extract `<style>` blocks in `<body>` with no `id` attribute and count `!important` |
| Live vs repo parity | `curl -sS https://kriskrug.co/wp-content/themes/kk-aurora/<f> \| md5` vs `md5 -q theme/kk-aurora/<f>` |
| Pixel-gate routes and viewports | `scripts/visual_baseline.py:96` (ROUTES), `:152` (VIEWPORTS) |
| Budget and waiver history | `.css-budget.json` |
| Prior-doc figures quoted in 1.1 and 2 | `AURORA-STYLESHEET-REBUILD-PLAN.md` §1.1, `CSS-DEADCODE-OVERLAP-AUDIT.md:263` |
| Section 1.1 historical columns | the `for C in 33887e7c 0064b4e dd87d4a` loop printed in §1.1 |
| Section 2 classification, both trees | brace-tracking classifier described in §2; re-runnable from the rule stated there |
| Section 4 surface-by-surface bytes | enumerate every `<style>` element on the fetched page by `id`, sum bytes and `!important` per element |
| Section 4 surface 1 | `curl -sSL https://s5102.pcdn.co/wp-content/boost-cache/static/ec2a031717.min.css \| wc -c` ; same piped to `grep -o '!important' \| wc -l` |
| Section 4.1 snippets | `backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json` ; `curl -o /dev/null -w '%{http_code}' https://kriskrug.co/wp-json/code-snippets/v1/snippets` |

**Not verified in this session, flagged rather than guessed:**

- Whether the homepage drop cap is *visually* apparent. The selector match and the absence of any neutralizing rule are both confirmed; no browser render was performed. That is what #475's pixel gate is for.
- Code Snippet #14 and media #12631 status. Requires wp-admin. See D-5.
- The **current** live Code Snippets list, by name and active flag. `code-snippets/v1/snippets` returns 401 and no WP credentials resolved in this session, so §4.1's per-snippet table is the 2026-07-24 repo snapshot. The 12-route id scrape does independently prove that **no snippet is emitting CSS to a logged-out visitor on any pixel-gate route today**, which is the part the CSS surface inventory needs. What it cannot show is a snippet that changed without touching CSS. Same wp-admin trip as D-5.

**Fixed in this revision after an adversarial verify pass**, listed so the diff is not silent: §1 `!important` column now foots to 176 (`09-late.css` was printed on a code-only basis inside a raw column); §1.1 both historical columns recomputed front-end and code-only (was 6,219 / 79 all-files, relabelled front-end); §2 cascade-war count corrected 154 to 151 and the delta re-derived from one classifier run over both trees; §2 blockquote restored to source with the single alteration marked; §4 surface 1 measured instead of carried over, surface 2 corrected from 8 blocks / ~5.8 KB to 7 blocks / 4,778 B with the `core-block-supports` double count removed; §4.1 added; §7 Path B and status-quo rollback rows written out instead of "n/a".
