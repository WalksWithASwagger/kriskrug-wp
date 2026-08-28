# Issue #481 — class-rename blast radius (read-only)

> **STATUS: HISTORICAL — ISSUE RETIRED 2026-08-28.** The audit below explains
> why the global rename was unsafe. Do not use its “when (if)” implementation
> notes as an active plan; a future naming migration requires a new issue and a
> complete current live-content corpus.

**Captured:** 2026-08-17T02:48Z, logged out, public GET only.
**Issue:** [#481](https://github.com/WalksWithASwagger/kriskrug-wp/issues/481). Step 8 of [`AURORA-STYLESHEET-REBUILD-PLAN.md`](../AURORA-STYLESHEET-REBUILD-PLAN.md).
**Lane:** Track B docs. **Zero theme edits. Zero live WordPress writes.** No REST POST/PATCH. No class rename.
**This session did not take page snapshots** and did not change a selector.

[#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423) is **closed** (2026-08-05). [#477](https://github.com/WalksWithASwagger/kriskrug-wp/issues/477) is **still open** (stated precondition). Homepage section issues [#411](https://github.com/WalksWithASwagger/kriskrug-wp/issues/411)–[#420](https://github.com/WalksWithASwagger/kriskrug-wp/issues/420) are open. Live Aurora is **1.6.5**; repo `main` is **1.6.7**.

## Verdict

**Still a live-DB-content landmine. Keep `blocked`. Do not start an unused-classes-first PR.**

A repo-only rename of `aurora-` / `revive-` / `kkm-` → `kk-` would break rendered pages whose class names live in WordPress `content.rendered`, which no theme grep can see. That is the same false-positive class as [#256](https://github.com/WalksWithASwagger/kriskrug-wp/issues/256): repo analysis said 105 dead classes, live corpus proved 101.

The [#423 decision memo](../AURORA-STYLESHEET-DECISION-2026-08-02.md) already said to **defer #481 indefinitely** (D-4). This pass re-measured the blast radius. The landmine is still there. The unused-class slice is not safe from a six-route sample.

## Live theme readback

Public `https://kriskrug.co/wp-content/themes/kk-aurora/style.css`:

| | Value |
|---|---|
| `Version` | **1.6.5** |
| Bytes | 111,718 |
| md5 | `af4097590b97f9dd703c3db97d670bf2` |
| Repo `main` `theme/kk-aurora/style.css` | **1.6.7** (`59505f1`, PR #789) |

Front-end class-prefix totals in **live 1.6.5 sheets** matched **repo 1.6.7** on this pass (`aurora-` 217 unique / 1,412 selector hits; `kk-` 22 / 48; `revive-` 0; `kkm-` 0). Version drift is real; the class-name surface is not what drifted.

## Method

Classes, not custom properties. A class use is a `.name` token in CSS selectors (comments stripped, `CLASS_IN_SELECTOR_RE` from `scripts/css_coverage_audit.py`) or a token in an HTML `class="…"` attribute.

| Surface | What was counted |
|---|---|
| Theme CSS | Front-end sheets in `theme/kk-aurora/` (same set as `make css-inventory`: `style.css`, `02-tokens.css`, `04-primitives.css`, `typography-refined.css`, `animations.css`, `bleeding-edge.css`, `revive-port.css`, `09-late.css`). Editor sheet excluded. |
| Live HTML | Logged-out GET of `/`, `/about/`, `/work/`, `/speaking/`, `/events/`, and post `/2026/08/11/futureproof-festival-announcement/` (WP 12732, newest public post at capture). |
| Live DB | Public `GET /wp-json/wp/v2/{pages,posts}?slug=…&_fields=id,slug,status,link,modified,content`. `content.rendered` class attrs **and** class selectors inside that HTML’s `<style>` blocks. |
| Not counted as classes | `--aurora-*` / `--revive-*` / `--kk-*` custom properties (footnote). `#aurora-*` IDs (footnote). |

Six routes are a blast-radius sample, not a full REST dump of every page and post. #481’s own method still requires that dump before any rename.

## Class-count table

**Unique names** / **occurrences** (selector hits in CSS; `class=""` tokens in HTML). Empty prefix = 0.

| Surface | `aurora-` unique | `aurora-` occ | `revive-` unique | `revive-` occ | `kkm-` unique | `kkm-` occ | `kk-` unique | `kk-` occ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Theme CSS (repo 1.6.7 = live 1.6.5 sheets) | **217** | **1,412** | **0** | **0** | **0** | **0** | **22** | **48** |
| Live HTML union (6 routes) | **135** | **1,095** | **0** | **0** | **0** | **0** | **2** | **8** |
| In both CSS and live HTML | **114** | — | 0 | — | 0 | — | **1** (`kk-page`) | — |
| CSS only (absent from these 6 HTML pages) | 103 | — | 0 | — | 0 | — | 21 | — |
| Live HTML only (not a theme CSS class) | 21 | — | 0 | — | 0 | — | 1 (`kk-r9-pack`) | — |

### Live HTML by route (`class=""` only)

| Route | HTTP | `aurora-` unique / occ | `kk-` unique / occ | `revive-` / `kkm-` |
|---|---:|---:|---:|---|
| `/` | 200 | 81 / 145 | 0 / 0 | 0 |
| `/about/` | 200 | 49 / 82 | 1 / 1 | 0 |
| `/work/` | 200 | 45 / 87 | 2 / 3 | 0 |
| `/speaking/` | 200 | 44 / 73 | 2 / 3 | 0 |
| `/events/` | 200 | 62 / **636** | 1 / 1 | 0 |
| `/2026/08/11/futureproof-festival-announcement/` | 200 | 54 / 72 | 0 / 0 | 0 |

Live `kk-` class tokens on this sample are only `kk-page` (6) and `kk-r9-pack` (2).

### REST `content.rendered` (the landmine)

| Route | ID | `modified` | `aurora-` unique / occ in content | Inline `<style>` `aurora-` unique | `kk-` in content |
|---|---:|---|---:|---:|---|
| `/` (`slug=home`, WP 2315) | 2315 | 2026-06-17 | **0 / 0** | 0 | 0 |
| `/about/` | 1208 | 2026-08-01 | **16 / 30** | 13 | 0 |
| `/work/` | 2672 | 2026-08-12 | **9 / 35** | 3 | `kk-page`, `kk-r9-pack` |
| `/speaking/` | 1887 | 2026-07-24 | **8 / 21** | 3 | `kk-page`, `kk-r9-pack` |
| `/events/` | 2250 | 2026-08-10 | **29 / 584** | 12 | 0 |
| Post 12732 | 12732 | 2026-08-12 | **0 / 0** | 0 | 0 |

**40 distinct `aurora-*` class names** sit in this REST sample’s HTML. **25** of those names (plus `kk-r9-pack`) are also **selectors inside DB-stored `<style>` blocks**.

Homepage chrome is FSE/theme-owned (page 2315 has no `aurora-` in content). The newest post’s body is also clean. About, work, speaking, and especially **events** store theme class names in the database. Events alone is 584 `aurora-` class tokens in `content.rendered`.

Named DB classes include the ones #481 already warned about: `aurora-button`, `aurora-card`, `aurora-media-card`, plus `aurora-about-page`, `aurora-hero-2026`, `aurora-event-card`, `aurora-proof-module`, `kk-r9-pack`.

Work/speaking inline CSS still targets `.kk-r9-pack .aurora-button` / `.aurora-card` / `.aurora-media-card` — theme-owned selectors from a layer the theme cannot control. That is unchanged from [`CSS-DEADCODE-OVERLAP-AUDIT.md`](../CSS-DEADCODE-OVERLAP-AUDIT.md) and from the #480 six-route readback.

## `revive-` and `kkm-` are not live classes

| Prefix | Theme CSS classes | Live HTML (6 routes) | Where it actually lives |
|---|---|---|---|
| `revive-` | **0** | **0** | Custom properties only: **22** unique `--revive-*` names, **161** `var()`/decl hits in front-end CSS. File name `revive-port.css`. |
| `kkm-` | **0** | **0** | Dormant marquee markup: `theme/kk-aurora/parts/marquee-current.html` (31 class attrs) and `patterns/marquee-hero.php` (6). Inline selectors `.kkm`, `.kkm-board`, `.kkm-cell`, … `/marquee/` is still 404; not on the homepage. |

Renaming “`revive-` classes” is a no-op. Renaming `--revive-*` tokens is a different, also-dangerous job (page-content CSS consumes theme tokens; see #256 / #480). Renaming `kkm-` is a theme-file edit on a board that is not live.

## Why “unused classes only” is not a first PR

103 `aurora-*` names appear in theme CSS and **not** on these six HTML pages. That is **not** a delete/rename list.

1. Six routes under-sample. #256’s repo-only miss was four classes. A 103-name “unused” PR would repeat that error at scale.
2. 21 live HTML `aurora-*` names are **absent from theme CSS** (`aurora-event-card*`, `aurora-about-page`, `aurora-header`, …). They are still rendered. Coverage-from-CSS cannot see them.
3. JS/PHP apply state classes the HTML sample may miss (`scripts/tests/test_events_render_contract.py` asserts `aurora-event-card`).
4. `make css-coverage`’s last recorded high-confidence-dead list in `.css-budget.json` is dated **2026-07-25** against theme **1.4.5**. It is stale. This session did not freeze a new coverage budget.
5. Any theme-file rename collides with open homepage issues #411–#420 and with live 1.6.5 vs repo 1.6.7 deploy drift.

## Recommendation

**Keep #481 labeled `blocked`.**

| Option | Do it? | Why |
|---|---|---|
| Full `aurora-`/`revive-`/`kkm-` → `kk-` rename | **No** | Live DB landmine (40 `aurora-*` names + 25 inline selectors in this sample alone). Needs a full REST dump, an alias window, pixel gate, and KK sign-off. |
| Re-scope to unused classes first | **No, not from this sample** | 103 CSS-only names are a six-page heuristic, not an exhaustive corpus. `revive-`/`kkm-` class rename in CSS is empty. |
| Drop `blocked` because #423 closed | **No** | Decision closed; the **content landmine and #477** did not. Memo D-4 still says defer indefinitely. |
| Start after #477 + #480 + homepage PRs + 1.6.7 live | Later, maybe | Sequencing preference in the issue body is still unmet. #480 still owns the inline page-content CSS that *is* the DB override layer. |

Keep `needs-human-review`, `track-b`, `refactor`, `priority:medium`, `blocked`. Do not add `swarm-ready`.

When (if) this is picked up, the first implementation step is still #481’s own method: live REST dump of **all** pages and posts, then one-release aliases, then visual diff. Not a repo grep.

## Footnotes (not in the class table)

- **Custom properties** in front-end CSS: `--aurora-*` 68 unique / 503 hits; `--revive-*` 22 / 161; `--kk-*` 17 / 22. Token rename is out of scope for a class PR and is also a content landmine (`--accent`, `--aurora-black`, `--kk-accent` are consumed from page CSS).
- **IDs** on the six live pages: `aurora-main` on every route (skip-link target), plus homepage `aurora-home-title` / `aurora-work-title` / … and events `aurora-events-*`. An ID rename is the same blast radius as a class rename.
- **Dormant `kkm-*`** stays in theme parts until someone ships or deletes the marquee. That is a theme edit. Not this PR.

## Verification

| Check | Result | Evidence |
|---|---|---|
| `gh issue view 481` labels include `blocked` | **pass** | `blocked`, `needs-human-review`, `track-b`, `refactor`, `priority:medium` |
| #423 closed | **pass** | closed 2026-08-05T05:39:19Z |
| #477 still open | **pass** | OPEN; labels do not include `blocked` |
| Public `style.css` Version | **pass** | 1.6.5, md5 `af4097590b97f9dd703c3db97d670bf2` |
| Six-route HTML GET | **pass** | all HTTP 200 |
| Public REST `content.rendered` | **pass** | pages 2315/1208/2672/1887/2250 + post 12732 |
| Theme files edited | **pass** (none) | docs-only |
| `make css-coverage` | **not-run** | emits unmatched-class %, not the prefix×route table this issue needed; last recorded coverage is 2026-07-25 / 1.4.5 |
| `make status-readonly` | **not-run** | live Version + six-route GETs already taken; no need for the full morning-truth printer |
| Full REST dump of every page/post | **not-run** | out of scope for a six-route blast-radius report; still required before any rename |

## Writes from this session

Repo-only: this report. No WordPress writes. No `theme/` edits. Cite `Refs #481`, not `Fixes`.
