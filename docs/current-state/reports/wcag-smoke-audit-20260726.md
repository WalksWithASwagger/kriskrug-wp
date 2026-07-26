# WCAG 2.1 AA smoke audit — Issue #46

**Captured:** `2026-07-26` (public HTML + `pa11y --standard WCAG2AA`; no live WP writes)  
**Live theme:** Aurora **1.4.8** (`style.css` Version readback)  
**Branch:** `cursor/46-wcag-smoke-audit-f196`  
**Scope:** Bounded smoke — not a whole-site conformance claim, not a multi-week consultancy.

## Verdict

Core public chrome is in good shape: `lang`, skip-link → `#aurora-main`, single `h1`, landmarks, brand name, and (on this sample) blank-link/blank-button hygiene all look solid. Automated contrast is **mostly clean** after the #5 / #293 lineage, with **two live residual failures** on this pass (homepage service roman numerals; contact mailto accent on card cream). Alt debt is **mostly off this route set** and is tracked in [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4) / [PR #524](https://github.com/WalksWithASwagger/kriskrug-wp/pull/524). Public `/accessibility/` is still **404** — statement work stays on [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288). Keyboard/hover consistency remains a follow-up lane for [#424](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424).

**This report does not close #46.** It is smoke evidence + a ranked remediation list for the next Track B / Track A packets.

## Method

| Probe | Detail |
|---|---|
| Routes | `/`, `/about/`, `/speaking/`, `/blog/`, `/contact/`, `/generative-ai-services/` ( `/services/` → same URL), article `/2026/07/18/i-am-nomad-ai-film/` |
| Extra | `/accessibility/` (expect 404), `/home/` (alt cross-check only) |
| Automated | `npx pa11y --standard WCAG2AA` per route |
| Structure | Public HTML: `lang`, skip-link + target, heading outline, `<main>`, images/`alt`, form controls, blank links/buttons |
| CSS (observable) | Live `style.css` + `revive-port.css`: `:focus-visible`, `.skip-link:focus`, `prefers-reduced-motion` |
| Contrast notes | Token math + pa11y ratios (not a full APCA / large-text matrix) |
| Out of scope | Authenticated WP, media PATCH, screen-reader session, full keyboard tab film, mobile QA (#127), archive inventory |

Prior refresh (for delta): `docs/current-state/reports/issue-46-pa11y-five-routes-20260716.md` (five routes, 0 issues on then-live 1.3.37).

## Route matrix

| Route | HTTP | `lang` | Skip → `#aurora-main` | `h1` | pa11y WCAG2AA | Notes |
|---|---:|---|---|---:|---:|---|
| `/` | 200 | `en-US` | yes | 1 | **3 errors** | `.aurora-kicker` I / II / III in services band |
| `/about/` | 200 | `en-US` | yes | 1 | 0 | clean |
| `/speaking/` | 200 | `en-US` | yes | 1 | 0 | clean |
| `/blog/` | 200 | `en-US` | yes | 1 | 0 | clean |
| `/contact/` | 200 | `en-US` | yes | 1 | **1 error** | `.kk-contact-email` mailto contrast |
| `/generative-ai-services/` | 200 | `en-US` | yes | 1 | 0 | `/services/` identical |
| `/2026/07/18/i-am-nomad-ai-film/` | 200 | `en-US` | yes | 1 | 0 | featured + inline imgs named |
| `/accessibility/` | **404** | — | — | — | — | statement unpublished; see #288 |

## Check results (requested axes)

### Skip link

- Theme-owned `<a class="skip-link" href="#aurora-main">Skip to content</a>` present on every sampled page (including the article).
- Target `#aurora-main` exists on `<main>`.
- CSS: `.skip-link` off-screen until `.skip-link:focus` (and global `:focus-visible` / `--focus-ring`).
- Core duplicate skip-link suppressed in theme `functions.php` (commented in public HTML).

### Headings

- Exactly one `h1` per sampled route; no blank `h1`.
- Sampled outlines step `h1 → h2 → h3` without skipped levels on the first dozen headings.
- Article sample: titled `h1`, section `h2`s, related-post `h3`s — coherent.

### Focus outlines (observable, not a live tab film)

- Live theme ships `:focus-visible` box-shadow / outline rules for links, buttons, inputs, and several card patterns; `prefers-reduced-motion` present.
- **Not verified in this smoke:** full keyboard tab order, focus trap/modals, or whether every interactive surface actually paints a visible ring in browser (KK teardown still calls out weak hover/interactivity — [#424](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424)).

### Contrast notes

| Pair / surface | Approx ratio | AA normal | Source |
|---|---:|---|---|
| `#171310` on `#efe6d2` (body) | 14.9:1 | pass | token |
| `#9a2f14` on `#efe6d2` (signal links) | 6.1:1 | pass | token |
| `#efe6d2` on `#9a2f14` (CTA) | 6.1:1 | pass | token |
| Services-band kickers `rgba(239,230,210,0.55)` on `#171310` | **~2.45:1** | **fail** | pa11y + `revive-port.css` |
| Contact `.kk-contact-email` `#b53c18` on card `#e6dcc2` | **4.24:1** | **fail** | pa11y + contact snippet vars |
| Rainbow / wildcard accents on cream (if used as text) | &lt;3:1 | risk | token math — do not use as body/link text |

### Alt text gaps (cross-ref #524)

On the **requested main-nav set**, content `<img>` alts are present and descriptive (homepage hero/work cards, about/speaking, services, blog cards, article featured + figures). Remaining noise:

| Severity | Finding | Owner |
|---|---|---|
| S0 (off this set, high visibility) | Media **6835** empty alt on `/home/` crowd-shot card | [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4) / [PR #524](https://github.com/WalksWithASwagger/kriskrug-wp/pull/524) |
| S1 | Flickr badge empty alt (`12604`) on legacy page | #4 / #524 |
| S3 (every page) | Facebook noscript pixel `<img>` **missing `alt`** | theme/snippet — decorative `alt=""` or stop emitting `<img>` |
| Note | Blog cards often use **post title as alt** when media alt empty — OK fallback, weak description | #4 polish |

No media PATCH in this session.

### Forms / labels

- Sampled routes expose **no native** `<input>` / `<textarea>` / `<select>` contact or newsletter fields.
- `/contact/` is **mailto + outbound CTAs** (`feelmoreplants@gmail.com`, Beehiiv subscribe links) — no on-page labeled form to fail.
- Newsletter is link-out to `kriskrug.beehiiv.com` (header, bands, footer), not an embedded subscribe form.
- Implication: form-label criteria are **N/A on this smoke set**; if a WP/Jetpack form is reintroduced later, re-check labels vs placeholder-only.

### `lang` attribute

- All sampled documents: `<html lang="en-US">`. Pass for this smoke.

## Severity-ranked findings

### S0 — Fix soon (live WCAG2AA failures on core routes)

1. **Homepage services roman kickers fail contrast**  
   - Where: `/` `#services` articles — `<p class="aurora-kicker">I.</p>` / `II.` / `III.`  
   - Evidence: pa11y `G18.Fail` @ **2.45:1** (need ≥4.5:1)  
   - Cause: `theme/kk-aurora/assets/css/revive-port.css` — `.aurora-services-band .aurora-kicker { color: rgba(239, 230, 210, 0.55) !important; }` on `--revive-ink` (`#171310`)  
   - Fix lane: Track B — raise opacity / use solid cream ≥4.5:1 (or mark purely decorative and move numbering out of readable text if design allows).  
   - Related: closed [#293](https://github.com/WalksWithASwagger/kriskrug-wp/issues/293) / [#5](https://github.com/WalksWithASwagger/kriskrug-wp/issues/5) (prior contrast work; this is a **residual** dark-band case).

2. **Contact mailto accent fails on card cream**  
   - Where: `/contact/` `.kk-contact-email`  
   - Evidence: pa11y **4.24:1** (need 4.5:1); snippet uses `--kk-accent-text: #b53c18` on `--kk-card: #e6dcc2`  
   - Fix lane: Track A snippet or Track B shared token — darken to ≥ `#9a2f14` / pa11y hint `#b03713` on that background.

### S1 — Content / statement gaps (not theme CSS)

3. **Empty content alt on `/home/` (media 6835)** — inventory + proposed alts in [PR #524](https://github.com/WalksWithASwagger/kriskrug-wp/pull/524); parent [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4). Creds + KK before PATCH.  
4. **No public accessibility statement** — `/accessibility/` **404**. Draft/review lane: [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288) (publish/footer still #48).

### S2 — Process / UX follow-ups

5. **Site-wide hover + focus consistency** — CSS focus rules exist; KK teardown still flags weak interactivity. Gap inventory + shared styles: [#424](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424). Needs a real keyboard tab-through (out of this smoke).  
6. **Facebook pixel missing `alt`** — every page; treat as decorative (`alt=""`) or non-`<img>` beacon. Not a media-library fix.  
7. **Archive alt debt** — ~47% empty in #524’s 500-image sample; batch under #4 after KK, not one-off smokes.

### S3 — Passed / non-issues on this sample

- `lang="en-US"`, skip-link + target, single `h1`, `<main id="aurora-main">`, brand `aria-label` + wordmark alt, no blank links/buttons found, article media alts descriptive, YouTube iframe has `title`, primary palette text/CTA tokens meet AA on paper.

## Remediation roadmap (bounded)

| Order | Action | Lane | Blocks closing #46? |
|---:|---|---|---|
| 1 | Darken / opaque services-band kickers (S0 #1) | Track B theme | Needed for clean pa11y on `/` |
| 2 | Darken `.kk-contact-email` accent (S0 #2) | Snippet or theme | Needed for clean pa11y on `/contact/` |
| 3 | PATCH media 6835 (+ flickr 12604) per #524 | Track A + KK | Content AA; parallel |
| 4 | Human-review + draft publish path for statement | #288 → #48 | Policy/comms, not theme |
| 5 | Keyboard/hover gap list + shared styles | #424 | Stronger #46 closeout |
| 6 | Optional: re-run pa11y five/seven-route refresh into this report’s twin JSON | docs | Evidence only |

## Links

- Parent: [#46 Full WCAG 2.1 AA Accessibility Audit](https://github.com/WalksWithASwagger/kriskrug-wp/issues/46)  
- Statement: [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288)  
- Alt text: [#4](https://github.com/WalksWithASwagger/kriskrug-wp/issues/4) · inventory PR [#524](https://github.com/WalksWithASwagger/kriskrug-wp/pull/524)  
- Hover/focus pass: [#424](https://github.com/WalksWithASwagger/kriskrug-wp/issues/424)  
- Prior pa11y: `docs/current-state/reports/issue-46-pa11y-five-routes-20260716.md`

## Explicit non-claims

- Not “100% of public pages.”  
- Not a certified specialist audit.  
- No live WordPress content, media, or snippet writes in this session.
