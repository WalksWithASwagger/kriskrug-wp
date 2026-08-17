# Issue #585 — leftover dark-neon / ghost-palette islands

**Issue:** [#585](https://github.com/WalksWithASwagger/kriskrug-wp/issues/585) (`[DESIGN] Kill leftover dark-neon page islands + cohesion audit`)
**Captured:** 2026-08-16 19:18–19:25 PT (2026-08-17 02:18–02:25 UTC), logged-out `curl` with cache-bypass `?cb=`.
**Status:** READ-ONLY diagnosis. No live WordPress writes. No `theme/` edits. Homepage PRs #796/#797 and theme PRs #789/#801 were in flight and were not touched.
**Stack at capture:** WordPress public HTML on Pagely-ARES; live Aurora **1.6.5** (`style.css` `Version: 1.6.5`, `Last-Modified: Fri, 14 Aug 2026 18:52:23 GMT`); `origin/main` Aurora **1.6.6**. That live/repo drift is real and is not treated as proof that 1.6.6 already shipped.

---

## 1. Headline

**The original live page islands are gone.** Every high-value route named in #585 now ships cream/ink page HTML. There is no live `.kk-overhaul` skin, no `#ff6a6a`, no `--press-night`, and no `#00e5ff` / `#ff6a6a` **page-content** island. `/publications/` remains the PR #583 tear-sheet (`.kk-press` on cream tokens).

Do not manufacture a live restyle wave from this ticket. What remains is repo hygiene plus already-owned Track B leftovers, not a second dark-neon outbreak on cream-era pages.

**#585 should stay open**, but only as hygiene: stale keynotes payloads that would re-poison live pages if someone applied them, and the missing neon-forbid regression test. It should not stay open as if kriskrug.co still looks like the 2026-08-01 publications ghost.

---

## 2. Method

Checks selected (narrowest that answers “are ghost islands still live?”):

| Check | Why | Result |
|---|---|---|
| Logged-out cache-bypass GET of #585 routes + adjacent high-value pages | Reproduce the original live island claim | **pass** — no page-content neon islands |
| Marker scan: `#00e5ff`, `#ff6a6a`, `--press-night`, `kk-publications`, `kk-overhaul`, inline `#0`/`#1` fills | Exact issue forbidden set + requested dark-fill hunt | **pass** for page HTML; **pass-with-note** for shared chrome |
| `origin/main` `theme/kk-aurora` grep for the same markers | Would 1.6.6 still ship leftovers after deploy? | **pass-with-note** — neon hexes gone from `style.css`; presets/fallbacks remain |
| Keynotes payload files named in the issue | Wave A leftover inventory | **fail** as repo source, **not live** |
| `python3 -m unittest scripts.tests.test_publications_editorial_payload` | Existing publications forbid test | **not-run** — diagnosis only; test still covers publications payload, not the leftover keynotes files |
| `python3 -m unittest discover -s scripts/tests -p 'test_*neon*'` | Issue-requested broader forbid test | **fail / absent** — no `test_*neon*` files exist |
| Theme file edits / live PATCH | Explicitly out of scope | **not-run** (disallowed) |

Commands run (representative):

```bash
curl -sL "https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=$TS" | head -20
# live Version: 1.6.5

for path in / /about/ /work/ /generative-ai-services/ /services/ \
  /podcast-guesting-page-epk/ /responsible-ai-professional/ /publications/ \
  /speaking/ /contact/ /photography/ /events/ /sponsor-deck/ /ai-events/ \
  /vancouver-ai/; do
  curl -sL -o "/tmp/kk-585-audit/${slug}.html" \
    "https://kriskrug.co${path}?cb=$TS"
done

git grep -n -E '#00e5ff|#00E5FF|#ff6a6a|#030405|#0D0D12|#1A1A25' origin/main -- \
  theme/kk-aurora/style.css theme/kk-aurora/theme.json \
  theme/kk-aurora/parts/marquee-current.html
```

`/services/` is a 200 that serves the same HTML as `/generative-ai-services/` (page 2666).

---

## 3. Per-route verdict (live HTML)

**PASS** here means: no pre-Revive dark-neon **page island** (no `.kk-overhaul` with cyan/hot tokens, no `#00e5ff`/`#ff6a6a` in page-owned `<style>`, no `--press-night`, no `kk-publications`). Shared WordPress `global-styles-inline-css` still *declares* unused preset gradients that contain `#00E5FF` / `#0D0D12` on every route; that is scored in section 5, not as a per-page FAIL.

| Route | ID | Live island? | Verdict | Severity | Evidence |
|---|---:|---|---|---|---|
| `/publications/` | 1895 | No | **PASS** | — | Page-owned skin is cream `.kk-press`. Tokens: `--press-paper: … #efe6d2`; `--press-ink: … #171310`; `--press-signal: … #9a2f14`. No `kk-publications`, no `#ff6a6a`. |
| `/about/` | 1208 | No | **PASS** | — | `.aurora-about-page` + `.aurora-hero-2026` + `.aurora-proof-grid`. No `.kk-overhaul`. Page-owned CSS hides the generic page header; cream Aurora primitives, not neon cards. |
| `/work/` | 2672 | No | **PASS** | — | `.kk-r9-pack` cream CTA, not neon: `border: 1px solid #171310; background: #171310; color: #efe6d2`. Dark fill is **ink-on-cream button**, not a near-black page skin. |
| `/generative-ai-services/` | 2666 | No | **PASS** | — | `.kk-services-2026` cream tokens: `--kk-ink: #171310; --kk-card: #e6dcc2; --kk-paper: #efe6d2; --kk-accent: #d94a1f`. Class family `kk-services*` survives as a name, not as the old cyan island. |
| `/services/` | 2666 | No | **PASS** | — | Same document as `/generative-ai-services/`. |
| `/podcast-guesting-page-epk/` | 3609 | No | **PASS** | — | `.aurora-proof-grid` / `.aurora-page-lead`. One `#111` YouTube embed placeholder (`background:#111` around the iframe) — media chrome, not a palette island. |
| `/responsible-ai-professional/` | 11914 | No | **PASS** | — | Same Aurora proof primitives. No `.kk-overhaul`. |
| `/speaking/` | 1887 | No | **PASS** | — | `.kk-r9-pack` with the same cream ink button as `/work/`. |
| `/contact/` | 2418 | No | **PASS** | — | `.kk-contact-2026` cream: `--kk-accent: #d94a1f; --kk-paper: #efe6d2`. Matches the R7 “no `#00e5ff`” closeout. |
| `/photography/` | 12013 | No | **PASS** | — | No neon markers in page content. Boost critical CSS not present on this route. |
| `/events/` | 2250 | No | **PASS** | — | Cream page body. `.aurora-final-cta` is theme chrome (see section 5); not a Track A HTML island. |
| `/sponsor-deck/` | 12625 | No | **PASS** | — | `.kk-sponsor` cream: `--kk-hot: #b53c18` (burnt orange), not `#ff6a6a`. |
| `/ai-events/` | 12317 | No | **PASS** | — | Topic hub on `aurora-prose` / cream primitives. |
| `/vancouver-ai/` | 12315 | No | **PASS** | — | Topic hub on `aurora-prose` / cream primitives. |
| `/` | 3930 | No page island | **PASS** (FOUC note) | Low, already owned | Page markup is cream-era (`theme-color #efe6d2`, woven SVG `#efe6d2` / `#171310` / `#d94a1f`). Jetpack Boost **critical CSS** on `/` (and `/blog/`) still snapshots pre-cream tokens. Owned by [#731](https://github.com/WalksWithASwagger/kriskrug-wp/issues/731); homepage visual work is #796/#797. Do not fork that into a new #585 child. |

Exact fragments:

**Publications (PASS) — cream press tokens, not neon:**

```css
.kk-press {
  --press-paper: var(--aurora-paper, var(--wp--preset--color--paper, #efe6d2));
  --press-ink: var(--aurora-ink, var(--wp--preset--color--ink, #171310));
  --press-signal: var(--aurora-signal, var(--wp--preset--color--signal, #9a2f14));
}
```

**Services (PASS) — cream island, not cyan:**

```css
.kk-services-2026 {
  --kk-ink: #171310;
  --kk-card: #e6dcc2;
  --kk-paper: #efe6d2;
  --kk-accent: #d94a1f;
}
```

**Homepage Boost critical CSS (not a page island; first-paint snapshot):**

```css
:root{
  --aurora-ink:#f7f7f2;
  --aurora-ink-soft:#c8cac8;
  --aurora-black:#030405;
}
.aurora-theme{background:radial-gradient(...),var(--aurora-black)}
.aurora-header-2026{background:rgb(3 4 5/.76)}
.aurora-hero-scrim{background:linear-gradient(90deg,rgb(3 4 5/.94) 0,...)}
```

After the full sheet loads, `assets/css/revive-port.css` paints cream with `!important` (`.aurora-theme { background-color: var(--revive-surface) !important; }`, `.aurora-header-2026 { background: rgba(239, 230, 210, 0.92) !important; }`). The stale Boost block is a first-paint / regen debt (#731), not a Track A HTML rewrite.

**Shared false positive on every route:** `global-styles-inline-css` still emits

```css
--wp--preset--gradient--aurora-cyan-teal: linear-gradient(135deg, #00E5FF 0%, #00BFA5 100%);
--wp--preset--gradient--aurora-radial: radial-gradient(ellipse at center, #1A1A25 0%, #0D0D12 100%);
```

No audited page applies `has-aurora-cyan-teal-gradient` (etc.) as an HTML class. The utility *rules* exist because `theme.json` still lists those presets.

---

## 4. Payload files vs live (Wave A leftovers)

Issue #585 listed five keynotes payloads still carrying cyan/hot. Live pages have moved on. The files on `origin/main` have **not**.

| Payload | Live route | Payload still neon? | Live still neon? | Disposition |
|---|---|---|---|---|
| `content/source-packs/keynotes-2026/wp-payloads/about.html` | `/about/` | **Yes** — `.kk-overhaul { --kk-accent:#00e5ff; --kk-hot:#ff6a6a; }` | **No** | **Do not apply.** Treat as historical. Clean or quarantine in a scoped follow-up. |
| `…/work.html` | `/work/` | **Yes** — same `.kk-overhaul` cyan/hot block | **No** | Same. |
| `…/services.html` | `/generative-ai-services/` | **Yes** — `.kk-services { … --kk-accent:#00e5ff; --kk-hot:#ff6a6a; }` | **No** (live is `.kk-services-2026` cream) | Same. |
| `…/podcast-guesting-page-epk.html` | `/podcast-guesting-page-epk/` | **Yes** — `.kk-overhaul` cyan/hot | **No** | Same. |
| `…/responsible-ai-professional.html` | `/responsible-ai-professional/` | **Yes** — `.kk-overhaul` cyan/hot | **No** | Same. |
| `…/speaking.html` | `/speaking/` | No neon hexes (cream `--kk-accent:#0f766e`) | No | Already restyled in repo; still uses the `.kk-overhaul` *class name*. Low risk. |
| `…/publications.html` | `/publications/` | Covered by `test_publications_editorial_payload` forbid list | No | Already the good example. |
| `…/homepage-hero.html`, `…/vancouver-ai-community.html` | n/a / hub | Cream tokens, not neon | — | Not the leftover set. |

Applying any of the five neon payloads to production would recreate the original bug. That is the only remaining **high-severity** #585 risk, and it is a repo foot-gun, not a live visual.

`backup/` snapshots and `docs/current-state/AURORA-TEMPLATE-CONTENT-HANDOFF.md` still describe the dark `kk-overhaul` card look (`bg #030405`, accent `#00e5ff`). Those are historical / stale docs, not live HTML.

---

## 5. What `origin/main` (Aurora 1.6.6) would still ship

Neon hexes are **gone from `theme/kk-aurora/style.css`**. Cream baseline is `--aurora-ink: #171310`, `--aurora-paper: #efe6d2`, `--aurora-black: #171310`, `.aurora-theme { background: var(--aurora-opal-void); }` (`--aurora-opal-void: #efe6d2`).

Remainders that would still be in the 1.6.6 tarball:

| Remainder | Where | Painted on cream pages today? | Own a new issue? |
|---|---|---|---|
| Hardcoded `#030405` on `.aurora-testimonial-band`, `.aurora-writing-band`, `.aurora-footer-2026` | `style.css` L827, L966, L2412 | **Mostly no.** `revive-port.css` overrides footer to `--revive-surface-2 !important` and writing-band to `transparent`. Dead layered rules. | **No new issue.** Fold into existing stylesheet-hierarchy / dead-CSS work (#423 / CSS deadcode audit). Do not block 1.6.6. Do not touch while #796/#797/#789/#801 are in flight. |
| Pre-cream `rgba(9, 12, 17, …)` plates, including `!important` at L4155 | `style.css` | Later cream block at L4197+ sets `#aurora-main` headers/titles to `transparent !important`. Residual risk is selectors *not* under `#aurora-main`. | Same — Track B hygiene, not #585 Wave A. |
| `theme.json` gradients `aurora-subtle`, `aurora-cyan-teal`, `aurora-radial`, `depth-fade` + duotones `#0D0D12`/`#00E5FF` | `theme.json` | Declared on every page via `global-styles`; **not used as content classes** on audited routes. Ghost-button hover still references `--wp--preset--gradient--aurora-subtle` (faint cyan wash). | **Maybe**, tiny Track B child under #423 after homepage PRs merge — not a live island ticket. |
| Marquee LED fallbacks `--kkm-cyan: … #00E5FF`, `--kkm-deep: … #0D0D12` | `parts/marquee-current.html` | **Not live** on audited routes (no `.kkm` board; header/footer use `.aurora-woven-marquee`). Preset cyan is already `#39a8d8`, so the `#00E5FF` is only a fallback. | **No.** Leave until someone ships the LED marquee. |
| Jetpack Boost critical CSS dark snapshot on `/` and `/blog/` | Live WP, not the theme tarball | First paint only; full CSS cream-overrides | **Already #731.** Regen after the next theme deploy. |

1.6.6 vs 1.6.5 does **not** by itself remove the `theme.json` neon presets or the `#030405` layered leftovers. Deploying 1.6.6 will not reintroduce page HTML islands, and it will not finish #585.

---

## 6. Cohesion notes for Track B (Wave B, read-only)

- Page HTML no longer fights Aurora with a second neon theme. Remaining cohesion is **double systems inside the theme**: layered pre-cream fills in `style.css` vs cream `!important` in `revive-port.css`, plus unused neon presets in `theme.json`.
- `/about/` still uses a page-owned `<style>` to break the hero out of the prose column and hide `.aurora-page-header`. That is layout, not a ghost palette. Homepage hero work is #796/#797 — do not mix it here.
- `/work/` and `/speaking/` share `.kk-r9-pack` cream ink buttons (`#171310` on `#efe6d2`). Fine. Do not confuse those with near-black page skins.
- `kk-services*` / `kk-contact*` / `kk-sponsor*` / `kk-press` are cream-token class families. Renaming them is #481, out of scope.

Priority if KK wants leftover cleanup after 1.6.6 + homepage PRs:

1. **#731** Boost critical-CSS regen (ops, post-deploy).
2. **Payload freeze + neon forbid test** (this ticket’s remaining acceptance criteria).
3. Optional: delete unused `theme.json` neon gradients/duotones (#423 child).
4. Optional: delete layered `#030405` / `rgba(9,12,17)` rules once pixel gate proves revive-port already wins.

---

## 7. What deserves its own issue vs close #585

| Remainder | New issue? | Why |
|---|---|---|
| Live `.kk-overhaul` / `#00e5ff` / `#ff6a6a` page islands | **No** | Not present. Manufacturing this work would duplicate a finished live fix. |
| Homepage dark first-paint / Boost snapshot | **No** | [#731](https://github.com/WalksWithASwagger/kriskrug-wp/issues/731) + homepage PRs #796/#797. |
| `theme.json` unused neon gradients | Only if KK wants a tiny Track B after in-flight theme PRs | Child of #423, not a live emergency. |
| Hardcoded `#030405` in `style.css` | No | Superseded by revive-port; deadcode pass, not a user-facing island. |
| Stale neon keynotes payloads + missing `test_*neon*` | **Keep on #585** | Last unmet acceptance criteria. Repo-only. No live write. |

**Recommended close path for #585:** add a forbid test over `content/source-packs/keynotes-2026/wp-payloads/*.html` (same markers as `test_publications_editorial_payload`: `#00e5ff`, `#ff6a6a`, `--press-night`, `kk-publications`), then either delete/quarantine the five neon payloads or mark them `STATUS: Historical` in-file so agents cannot treat them as apply-ready. After that, close #585. Do not PATCH live pages for this ticket.

---

## 8. Verification ledger

| Check | State | Notes |
|---|---|---|
| Live style.css version readback | **pass** | 1.6.5, not 1.6.6 |
| Logged-out route GETs (15 URLs) | **pass** | All HTTP 200 |
| Page-content neon island scan | **pass** | Zero `#ff6a6a`, zero `.kk-overhaul`, zero `--press-night`, zero `kk-publications` |
| Shared `#00E5FF` in `global-styles` | **pass-with-note** | Preset declaration only |
| Homepage Boost critical CSS | **pass-with-note** | Stale dark tokens; owned by #731 |
| `origin/main` style.css neon hexes | **pass** | None |
| `origin/main` theme.json neon presets | **fail as leftover, not as live island** | Still present |
| Keynotes payloads vs live | **fail (repo) / pass (live)** | Five files still neon |
| `test_*neon*` | **absent** | Acceptance criterion unmet |
| Publications payload unittest | **not-run** | Existing lock still applies to publications.html only |
| Theme / live writes | **not-run** | Disallowed this session |

---

## 9. Next verification step

If KK wants #585 closable: implement the payload forbid test and quarantine the five neon HTML files on a docs/content PR that does not touch `theme/` or live WordPress. After the next Aurora deploy, #731 should regenerate Boost critical CSS and confirm `/` critical CSS no longer contains `--aurora-black:#030405` / `--aurora-ink:#f7f7f2`.
