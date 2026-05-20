# Aurora Component Inventory - Issue #85

**Date:** 2026-05-20  
**Worker:** #85-docs  
**Track:** B - Aurora v2  
**Branch:** `codex/swarm-85-component-inventory-2026-05-20`  
**Base:** `origin/aurora/v2` at `28a32ef` (`docs: refresh aurora review packet (#102)`)  
**Issue:** [#85 `[AURORA P2] Build the restrained component library`](https://github.com/WalksWithASwagger/kriskrug-wp/issues/85)

## Scope

This is a docs-only foundation pass for issue #85. It does not edit theme files, production WordPress, Track A content payloads, or Worker #84's long-form article lane.

Future implementation should wait for Worker #84's long-form template work to merge before editing shared theme files, especially `theme/kk-aurora/templates/single.html` and prose CSS.

## Current Component Surface

| Component need from #85 | Current evidence | Current classes/selectors | Status |
|---|---|---|---|
| Project card | `theme/kk-aurora/templates/front-page.html` current fieldwork grid; `theme/kk-aurora/parts/work-proof-grid.html` project modules | `.aurora-media-card`, `.aurora-media-card-large`, `.aurora-text-card`, `.aurora-proof-module`, `.aurora-proof-media`, `.aurora-proof-body` | Partially present. Needs a documented reusable pattern and state matrix before more copies are added. |
| Talk card | `theme/kk-aurora/parts/speaking-proof-grid.html` topic modules and speaking reel; `theme/kk-aurora/templates/front-page.html` speaking format panel | `.aurora-speaking-reel`, `.aurora-topic-card`, `.aurora-speaking-panel` | Partially present. Topic cards exist, but no canonical talk-card contract yet. |
| Media band | `theme/kk-aurora/templates/front-page.html` hero, work grid, speaking band; `theme/kk-aurora/parts/speaking-proof-grid.html` reel | `.aurora-hero-2026`, `.aurora-hero-media`, `.aurora-feature-band`, `.aurora-speaking-band`, `.aurora-speaking-reel-media` | Present as page-specific sections. Needs restrained reuse rules so media bands do not become generic cards. |
| Proof chip | `theme/kk-aurora/templates/front-page.html` proof row; `theme/kk-aurora/parts/work-proof-grid.html`; `theme/kk-aurora/parts/speaking-proof-grid.html` | `.aurora-proof-row`, `.aurora-proof-tags`, `.aurora-proof-tags span`, `.aurora-card-label` | Present. Needs focus/active behavior where chips are links and a non-link chip rule where they are metadata. |
| CTA row | `theme/kk-aurora/templates/front-page.html`; `theme/kk-aurora/parts/work-proof-grid.html`; `theme/kk-aurora/parts/footer.html` | `.aurora-action-row`, `.aurora-proof-actions`, `.aurora-footer-actions`, `.aurora-button`, `.aurora-button-primary`, `.aurora-button-secondary` | Present. Hover styles exist; focus/active/disabled/loading variants are not systematized. |
| Article card | `theme/kk-aurora/templates/front-page.html` latest writing query | `.aurora-writing-query`, `.aurora-article-list`, `.aurora-article-row`, `.aurora-article-title`, `.aurora-article-excerpt`, `.aurora-article-date` | Present as a query-list row rather than a card. This matches the restrained direction and should stay list-first unless repeated media cards are needed. |
| Testimonial | `theme/kk-aurora/parts/speaking-proof-grid.html` quote grid | `.aurora-quote-grid`, `.aurora-quote-card` | Present. Needs empty/missing-cite guidance and mobile-state checks after implementation. |
| Form | No reusable Aurora form component found in the theme inventory. Contact/newsletter routes are currently links or external embeds in live snapshots. | None found in `theme/kk-aurora/style.css` for Aurora-specific form fields. | Missing. This is the largest #85 implementation gap. |
| Footer section | `theme/kk-aurora/parts/footer.html` | `.aurora-footer-2026`, `.aurora-footer-shell`, `.aurora-footer-brand`, `.aurora-footer-actions`, `.aurora-footer-nav`, `.aurora-footer-bottom` | Present. Supports primary site links, utility links, and project network links. |
| Newsletter utility | `theme/kk-aurora/templates/front-page.html` final CTA; `theme/kk-aurora/parts/footer.html` | Newsletter links via `.aurora-button` and footer nav/action links | Partially present as outbound links. Missing a reusable newsletter signup/utility component, loading/success/error state, and accessible embedded-form treatment. |
| Search utility | `theme/kk-aurora/templates/404.html` search block | Core `wp:search` block, no Aurora-specific wrapper class | Partially present. Search exists only as a 404 recovery utility and is not a documented reusable search component. |

## Acceptance Criteria Mapping

| #85 acceptance criterion | Inventory result | Future implementation note |
|---|---|---|
| Component inventory is documented before implementation. | Satisfied by this document. | Keep this document updated when #85 moves from docs foundation to theme edits. |
| Components cover project card, talk card, media band, proof chip, CTA row, article card, testimonial, form, footer section, newsletter utility, and search utility. | All components are mapped above. Form is missing; newsletter and search are partial utilities only. | Implement the missing/partial utilities after #84 merges. |
| Cards are only used for repeated items, not for every page section. | Current usage mostly aligns: cards appear in repeated project, proof, topic, quote, and article/list contexts; page sections remain bands or unframed layouts. | Preserve this rule in CSS/pattern naming. Do not promote every section into `.aurora-card`. |
| No card-inside-card layouts. | No intentional nested card pattern was found in the inventoried files. | Add this as a documented component rule before theme expansion: repeated item cards may contain media, labels, body, tags, and actions, but not another full `.aurora-*card` or `.aurora-proof-module`. |
| Components have hover, focus, active, disabled, loading/empty, mobile, and reduced-motion states where applicable. | Hover and mobile coverage exist for several components. Focus, active, disabled, loading, empty, and reduced-motion states are not consistently documented or implemented across the component surface. | Build a state matrix before editing CSS. Prioritize keyboard focus, disabled/loading button semantics, empty query/search/newsletter states, and reduced-motion behavior for reveal/hover transforms. |
| Forms are accessible and conversion-oriented. | No reusable Aurora form component exists yet. | Define labels, help text, error text, submit/loading/success states, keyboard focus, and spam/privacy copy. Use an embedded newsletter form only with clear fallback links. |
| Footer supports primary utility IA and project network links. | Satisfied in `parts/footer.html`: Site, Projects, and Utility columns plus brand CTAs. | Keep footer as a structured IA component, not a decorative mega-card. |

## Restrained Component Rules

- Use cards only for repeated items that users compare or scan: project entries, talk topics, testimonials, and article rows/cards.
- Do not wrap page-level bands, heroes, or full sections in card styling.
- Do not nest card components inside other card components.
- Prefer list or row treatment for article/query results unless the layout needs repeated media.
- Keep component radii aligned to the existing Aurora token value: `--aurora-radius-card: 8px` and `--aurora-radius-control: 8px`.
- Keep newsletter/search/form utilities visibly utilitarian: clear labels, clear actions, explicit feedback states, no marketing-widget bloat.
- Treat proof chips as metadata unless they are real links. If they become links, they need keyboard focus and active states.

## Missing State Matrix

| Component family | Hover | Focus | Active/current | Disabled | Loading | Empty/error | Mobile | Reduced motion |
|---|---|---|---|---|---|---|---|---|
| Buttons / CTA rows | Partial | Missing explicit system rule | Missing | Missing | Missing | Not applicable except form/search submit errors | Partial | Partial via existing motion constraints, needs audit |
| Project/talk/media cards | Partial | Missing explicit link-card focus | Missing | Not applicable unless cards become controls | Not applicable | Missing image/content fallback guidance | Partial | Needs transform/reveal audit |
| Proof chips | Mostly static | Missing if linked | Missing if linked | Not applicable | Not applicable | Missing no-tags behavior | Partial | Not applicable unless animated |
| Article list/card | Core link behavior | Missing explicit row focus | Current/category not defined | Not applicable | Query loading not represented in static templates | Empty query state missing | Partial | Not applicable unless animated |
| Testimonial | Static | Not applicable unless linked | Not applicable | Not applicable | Not applicable | Missing empty quote/cite guidance | Partial | Not applicable |
| Form | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| Newsletter utility | Link-only partial | Link focus depends on button styles | Missing | Missing | Missing | Missing success/error/fallback | Partial | Missing if embed animates |
| Search utility | Core 404 block only | Depends on core block/browser | Missing | Missing | Missing | Missing no-results guidance | Core responsive only | Not applicable |
| Footer | Link hover partial | Missing explicit footer focus | Missing current-page state | Not applicable | Not applicable | Not applicable | Partial | Not applicable |

## Future Write Set

Do not start this implementation until Worker #84's long-form article template lane has merged or been explicitly cleared.

Likely files for the implementation PR:

- `theme/kk-aurora/style.css` - component rules and state selectors.
- `theme/kk-aurora/parts/footer.html` - only if footer IA or newsletter utility markup needs a constrained adjustment.
- `theme/kk-aurora/parts/work-proof-grid.html` - only if proof/project markup needs canonicalized component hooks.
- `theme/kk-aurora/parts/speaking-proof-grid.html` - only if talk/testimonial markup needs canonicalized hooks.
- `theme/kk-aurora/templates/front-page.html` - only if homepage component markup needs class alignment.
- `theme/kk-aurora/templates/404.html` - likely search utility wrapper/state treatment.
- A new `theme/kk-aurora/patterns/` file only if WordPress needs reusable editor-facing patterns for form/newsletter/search utilities.

Avoid in the #85 implementation lane unless explicitly coordinated:

- `theme/kk-aurora/templates/single.html`
- Long-form/prose CSS
- Worker #84 evidence docs
- Track A content payloads and production WordPress state

## Verification

Commands run for this docs-only inventory:

```bash
git fetch --prune origin
git rev-parse origin/aurora/v2
git log -1 --oneline origin/aurora/v2
gh issue view 85 --json number,title,state,body,labels,url
find theme/kk-aurora -maxdepth 3 -type f | sort
rg -n "aurora-(proof|speaking|topic|quote|footer|button|card|media|actions|search|newsletter|form|empty|loading|disabled)" theme/kk-aurora/style.css
git diff --check
rg -n "project card|talk card|media band|proof chip|CTA row|article card|testimonial|form|footer section|newsletter utility|search utility|No card-inside-card|Browser smoke was not run|single.html|Worker #84" docs/current-state/AURORA-COMPONENT-INVENTORY-2026-05-20.md
```

Browser smoke was not run in this lane because no theme, CSS, template, JavaScript, or production WordPress files were changed.
