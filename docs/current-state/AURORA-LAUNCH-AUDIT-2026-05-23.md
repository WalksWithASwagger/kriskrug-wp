# Aurora Launch Audit — Master Improvement List (2026-05-23)

Audit of the **now-live** Aurora theme (`kk-aurora` 1.1.0) on production kriskrug.co,
the day of cutover. Covers visual, console/logs, network, functional, and cross-cutting
(a11y/perf/SEO) across every distinct template + core pages, with a long-tail spot-check.
Severity follows `FIX_QUEUE.md` (P0 = high-impact/low-friction). Baseline tooling:
`make wp7-smoke`, `make wp7-admin-readiness` (outputs in `raw/aurora-audit-2026-05-23/`).

## Executive summary

The launch is **functionally sound** (every page 200, no PHP fatals, REST/OG/JSON-LD
survived the switch, FSE editor works) but has **two launch-blocking visual bugs** and a
band of polish/design debt. Custom-template pages (Work, Speaking, single posts, 404)
look **great**; the generic `page.html` pages and the homepage reveal system are where
the problems concentrate.

- 🔴 **Homepage content renders intermittently invisible** (reveal animation races Jetpack Boost).
- 🔴 **`/blog/` shows the marketing homepage, not a post list.**
- Everything else is contrast / duplicate-title / broken-image / undesigned-legacy-page work.

## Per-surface results

| Surface | Template | Verdict | Notes |
|---|---|---|---|
| `/` Home | `front-page` | 🔴 Broken | Hero photo loads, but copy + sections intermittently stuck `opacity:0` |
| `/blog/` | `home` (clone of front-page) | 🔴 Broken | Renders the marketing homepage, **not** a post archive |
| Single post | `single` | ✅ Excellent | Category badge, headline, working "12 MIN READ", featured image |
| `/about/` | `page` (generic) | ⚠️ | Duplicate title (H1 ×2), dim low-contrast body, big top whitespace, no portrait |
| `/recent-projects-include/` Work | `page-work` | ✅ Good | Proof grid issues: Upgrade-AI image 400/black; Both-Hands-Full text overlap |
| `/speaking/` | `page-speaking` | ✅ Good | Dek slightly dim |
| `/generative-ai-services/` Services | `page` (generic) | ⚠️ | Undesigned legacy content, awkward spacing (rebuild already flagged) |
| `/contact/` | `page` (generic) | ✅ Functional | Jetpack form works + styled; intro has giant drop-cap "P" glitch |
| 404 | `404` | ✅ Excellent | Gradient 404, copy, dual CTA, working search |
| Header / Footer | parts | ✅ Good | Nav resolves; "Work" → `/work/` 301-hops to `/recent-projects-include/` |
| wp-admin Site Editor | — | ✅ Works | Earlier 503 was transient during the switch |

## Filed GitHub issues

P0/P1/actionable-P2 findings are tracked as issues **#116–#127** (label `aurora-v2`):
#116 invisible hero (P0) · #117 /blog/ homepage clone (P0) · #118 duplicate title ·
#119 broken/hotlinked images · #120 BHF card overlap · #121 low contrast ·
#122 undesigned generic pages · #123 contact drop-cap · #124 Work nav hop + dup template ·
#125 perf + Boost CSS · #126 Work blank og:image · #127 mobile QA.

## Findings

### P0 — launch blockers (fix immediately)

- **P0.1 — Homepage (and all `[data-reveal]`) content intermittently invisible.**
  - **Why:** First impression on the live homepage is frequently a black/empty hero.
    GSAP loads fine; the cause is a **race** — CSS hides `[data-reveal]` at `opacity:0`
    and **Jetpack Boost defers the reveal JS** (`hasJpDeferAttr:true`), so on cache-cold
    loads the content never gets revealed in time (sometimes never on scroll).
  - **Effort:** 1–2 hrs. **Dependencies:** none.
  - **Verify:** hard-reload `/` 5× (cache-cold) → hero copy + all sections visible every time.
  - **Fix-pointer:** make reveal **progressive** (content visible by default; only animate
    when JS confirms it ran) in `assets/js/micro-interactions.js`/CSS, and/or exclude
    `theme.js`,`micro-interactions.js`,`aurora-animations.js` from Jetpack Boost
    "Defer JS/Concatenate", then regenerate Boost Critical CSS.

- **P0.2 — `/blog/` renders the homepage clone, not a post archive.**
  - **Why:** The Writing/blog destination shows the marketing hero instead of articles —
    the blog is effectively missing. `home.html` is a duplicate of `front-page.html`; WP
    uses `home.html` for the Posts page.
  - **Effort:** 2–3 hrs. **Dependencies:** none.
  - **Verify:** `/blog/` lists recent posts with pagination.
  - **Fix-pointer:** rebuild `templates/home.html` as a real post-archive (the
    `templates/index.html` card layout already exists — base it on that), keeping
    `front-page.html` as the static front page.

### P1 — high impact, moderate effort

- **P1.1 — Generic `page.html` duplicate title.** Prints the WP page title H1 *above*
  content that already has its own hero heading (visible on `/about/`; affects every
  generic content page). Fix: drop the title block from `templates/page.html` or give
  key pages custom templates. Verify: one H1 per page.
- **P1.2 — Broken hotlinked image (Upgrade AI) + hotlink fragility.**
  `theupgrade.ai` share image returns **HTTP 400** → black card on Work + homepage. All
  hero/proof images are external hotlinks (one already dead). Fix per
  `AURORA-MEDIA-GAPS-2026-05-23.md`: upload canonical assets into the WP media library,
  rewrite `src`/`srcset`, set alt + rights. Verify: every proof image 200 from kriskrug.co.
- **P1.3 — Both Hands Full proof card text/image overlap.** og-image loads (200) but the
  caption/title overlaps it. Fix card layout in `parts/work-proof-grid.html` / CSS.
- **P1.4 — Low-contrast body text.** Dek/body paragraphs (About, Services, Speaking) are
  dim grey on near-black — WCAG AA risk. Fix: bump `text-secondary`/dek color or weight in
  `theme.json`/CSS. Verify: body text ≥ 4.5:1 contrast.
- **P1.5 — ~25 generic content pages are undesigned.** Services, marketing offer pages,
  authority pages, and multilingual intros render as bare title + legacy content on
  Aurora base styles (awkward spacing, old structure). Needs a design/template pass
  (Services rebuild already flagged separately).

### P2 — lower impact / higher effort

- **P2.1 — Contact intro drop-cap glitch** (giant "P" on "Pls fill out…"). Legacy
  first-letter styling; fix in page content/CSS.
- **P2.2 — "Work" nav → `/work/` 301 hop.** Point nav directly to
  `/recent-projects-include/` (or fix the slug) to drop the redirect.
- **P2.3 — `page-2672.html` redundant** — duplicate of `page-recent-projects-include.html`
  (both target the Work page). Remove one.
- **P2.4 — Regenerate Jetpack Boost Critical CSS** (was cleared by the theme change).
- **P2.5 — Homepage perf**: cold load ~4.3s; heavy JS + GSAP CDN. Run Lighthouse, measure
  LCP/INP/CLS, consider self-hosting GSAP and trimming.
- **P2.6 — Work page OG image blank** (`s0.wp.com/i/blank.jpg`) — set a real `og:image`.
- **P2.7 — Mobile/responsive QA not yet done** — couldn't reliably capture mobile in this
  pass; needs a dedicated device/breakpoint review (nav → hamburger, hero crop, grids).

### P3 — strategic / pre-existing

- **P3.1 — Hero/keynote photo reused 4×** (`michelle-diamond/195`) — source distinct images
  (see media-gaps doc); decide photography section.
- **P3.2 — Category disaster**: 98/101 recent posts in "Misc" (`CONTENT_AUDIT.md`) — now
  more visible once `/blog/` lists posts.
- **P3.3 — Monitor the transient `site-editor.php` 503** seen during the switch.

## What survived the switch (no action)

- ✅ JSON-LD schema (2 blocks/page, injected via Code Snippets — theme-independent).
- ✅ OpenGraph/Twitter tags (Jetpack) — except Work's blank og:image (P2.6).
- ✅ One H1 per page (Aurora templates resolved the old empty/duplicate-H1 issue).
- ✅ Reduced-motion fallback present in theme JS.
- ✅ REST namespaces, sitemap, contact form, FSE editor.

## Verification of this audit

- `make wp7-smoke` PASS (theme `kk-aurora 1.1.0`, WP 6.9.4, 8/8 paths 200).
- `make wp7-admin-readiness` — Aurora active, 13 plugins incl. Jetpack Boost 4.5.9; 2
  pre-existing Site Health criticals (background updates, page-cache) unchanged by switch.
- Hotlinked image statuses recorded: punkrockai 200, bc-ai 200, bothhandsfull 200,
  **theupgrade.ai 400**.
- No production writes performed during the audit (read-only inspection only).
