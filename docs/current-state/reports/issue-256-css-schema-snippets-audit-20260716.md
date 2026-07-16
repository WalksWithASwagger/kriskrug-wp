# Issue #256 — CSS / schema / snippets audit (repo-only)

**Captured:** 2026-07-16  
**Mode:** agent-safe. No live WP writes, no snippet deactivate, no theme CSS deletion.

## Acceptance checklist

| AC | Result this session |
|---|---|
| CSS coverage audit; remove or document unused selectors | **Documented** — heuristic inventory only; **no deletions** (coverage would false-flag FSE/DB classes) |
| Header marking deployed = canonical, mu-plugin = reference | **Done** in `fixes/schema-snippets-deployed.php` + `fixes/schema-snippets.php` |
| Resolve or ticket headshot-URL TODO | **Ticketed here** — headshot is public `/about/` portrait `…/2023/07/krug-1.jpg`; KK confirm if a newer asset is desired |
| Audit active Code Snippets after Jetpack removal | **Deferred** — needs secrets / wp-admin; reuse #256 comment inventory (active 5/7/8/10; keep 10) |
| Confirm snippet 5 schema still needed / not duplicating | **Repo stance** — keep snippet 5; theme does not own JSON-LD Person/WebSite stack; #316 is separate identity rewrite |
| Keep snippet 10 asset diet active | **Unchanged** — do not touch without replacement proof |
| No removal of tracking/verification/redirects/schema without evidence | **Honored** |

## CSS size inventory (live theme tree on `main`)

| File | Lines | Bytes |
|---|---:|---:|
| `theme/kk-aurora/style.css` | 4445 | 110602 |
| `assets/css/typography-refined.css` | 686 | 16781 |
| `assets/css/bleeding-edge.css` | 561 | 12390 |
| `assets/css/animations.css` | 352 | 7540 |
| `assets/css/editor.css` | 175 | 5343 |
| **Total** | **6219** | **152656** |

### `style.css` section map

| Approx lines | Banner |
|---|---|
| 20+ | Custom properties |
| 59+ | Base resets |
| 130+ | Typography |
| 161+ | Links |
| 190+ | Buttons |
| 234+ | Cards |
| 287+ | Glass |
| 298+ | Sections |
| 329+ | Badges |
| 376+ | Scroll / GSAP base |
| 406+ | Skeleton |
| 430+ | Accessibility |
| 465+ | Responsive utilities |
| 486–3233 | **AURORA 2026 REDESIGN SYSTEM** (bulk) |
| 3234–4320 | **ARTICLE + BLOG LUX COMPOSITION V2** (bulk) |
| 4321+ | Print |

### Heuristic “orphan” selectors (NOT delete list)

Repo-only scan: CSS class tokens vs class strings in theme HTML/PHP/JS/JSON.

- Unique CSS classes: **316**
- Tokens referenced in theme files: **248**
- Suspect orphans: **161** (mostly `aurora-*` utilities used from FSE content / patterns in WP DB, plus core `align*` / `wp-*`)

**Rule:** treat suspects as **documentation only**. Purging without browser coverage + theme deploy smoke will break live pages. Next Track B step (separate PR, KK-gated): coverage tool on five routes after 1.3.40 deploy, then prune only proven-dead rules.

### Theme ↔ `fixes/*.css` overlap

Staging CSS in repo: `issue-5-color-contrast.css`, `issue-9-button-hover-states.css`, `issue-10-cta-hover-states.css`.

Class overlap with theme CSS: only `entry-content`, `wp-block-button__link`. Live hover/contrast largely already in theme or inactive snippet #9 — do not re-activate without before/after evidence.

Plugin unused-CSS path remains snippet **10** / `ASSET-DIET` (separate from theme dead selectors).

## Schema file roles

| File | Role |
|---|---|
| `fixes/schema-snippets-deployed.php` | **Canonical live** Code Snippet source |
| `fixes/schema-snippets.php` | **Reference / future mu-plugin**; inert `VERIFY-ME` guard |
| `fixes/issue-39-schema-markup.php` | Older Person/Article-only ancestor |

### Drift summary (deployed vs mu-plugin draft)

| Topic | Deployed | Mu-plugin draft |
|---|---|---|
| Ready guard | none (baked values) | `kk_schema_is_ready()` blocks on `VERIFY-ME` |
| `same_as` | twitter/x/instagram verified | VERIFY-ME placeholders |
| `works_for` URLs | filled | VERIFY-ME |
| `logo_url` | (not used / filtered) | VERIFY-ME |
| `knows_about` | includes **Generative AI Tools** | same legacy token |
| Headshot | `…/2023/07/krug-1.jpg` | same |

Identity rewrite for site name / knows_about → **#316** (do not fold into #256 CSS lane).

## Snippets overlap (from prior #256 inventory; not re-fetched)

Active (do not remove without evidence): **5** schema, **7/8** (tracking/verification family per prior notes), **10** asset diet.  
Inactive: 1–4, 6, 9 — leave parked.

Authenticated re-audit waits on Cloud secrets.

## Recommended next slices

1. After Aurora 1.3.40 is live: optional CSS coverage capture on five routes (Track B).
2. #316 schema identity handoff → KK-approved snippet 5 replace with snapshot.
3. KK confirm headshot URL or supply replacement asset.
4. Authenticated Code Snippets inventory when `WP_*` secrets exist.

## Out of scope (honored)

Theme CSS deletion, live snippet edits, Jetpack module changes, public JSON-LD mutation.
