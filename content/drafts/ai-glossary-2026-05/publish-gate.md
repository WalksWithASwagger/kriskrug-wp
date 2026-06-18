# AI Glossary Publish Gate

Status: private WordPress page draft created; not ready for live WordPress publication.

Issue: #44 `[CONTENT] Create Glossary Page for AI Terminology`
Target URL: `/glossary/`
Draft source: `content/drafts/ai-glossary-2026-05/README.md`

## WordPress Draft

- WP page draft ID: `11887`
- Edit URL: <https://kriskrug.co/wp-admin/post.php?post=11887&action=edit>
- Verified readback: status `draft`, slug `glossary`

## Gate Summary

The glossary draft is review-ready but not publish-ready. It currently has 69 terms, alphabetical sections, SEO metadata, mobile/accessibility notes, a related-reading module, and a Gutenberg-ready `post.html` body with an accessible in-page search/filter.

Do not publish until the sensitive-term review is complete or the sensitive terms are removed from the first public version.

## Acceptance Check

| Requirement | Status | Notes |
|---|---|---|
| `/glossary` page | Draft created | Private WordPress draft exists at slug `/glossary/`. Public publish waits for review. |
| 50+ terms | Ready | Draft has 69 terms before editorial cuts. |
| Alphabetical | Ready | Letter sections and terms are sorted in-page. |
| Searchable | Ready for preview | `post.html` includes a visible search label, keyboard-usable input, term/definition filtering, result count, no-results state, and no-JS fallback. |
| Internal links | Drafted | Related-reading module and post-publication link map are in the README. |
| Mobile | Drafted | No tables; notes call out wrapping and mobile QA. |
| SEO | Drafted | Title, meta description, excerpt, keyphrases, and schema caution are in the README. |

## Required Reviews Before Publish

- KK editorial review for tone, audience, and scope.
- SME/source review for Indigenous governance, rights, legal, protocol, and cultural terms.
- Source/attribution check for FPIC, OCAP, Two-Eyed Seeing, Indigenous data sovereignty, Indigenomics, and land/territory language.
- Publisher check that `/glossary/` is available and does not collide with an existing page, redirect, or menu item.

## Search Gate

Built locally in `post.html`; verify in WordPress preview before closing issue #44.

Minimum acceptable filter behavior:

- Visible label: `Search glossary terms`.
- Filters term names and definitions.
- Keyboard usable.
- Screen-reader usable with result-count announcement.
- No-JS fallback keeps all terms visible.
- Clearing the search restores all terms.

Smoke searches:

- `data`
- `rights`
- `RAG`
- `water`
- `prompt`

## Accessibility Gate

- One H1 only.
- Letter sections as H2s.
- Definition content is not in a dense table.
- A-Z anchors work.
- Focus styles remain visible.
- Long terms wrap on mobile without horizontal scrolling.
- Search input has a visible label.
- No-results state is text, not color-only.

## SEO Gate

- SEO title: `AI Glossary | Kris Krug`
- Meta description: `Plain-language definitions for AI, local technology, data governance, Indigenous governance, and creative AI terms used on KrisKrug.co.`
- Slug: `/glossary/`
- Canonical: `https://kriskrug.co/glossary/`
- Suggested schema: `WebPage` plus `BreadcrumbList`.
- Hold `DefinedTermSet` schema until sensitive terms and source attribution are settled.

## Closure Recommendation

Issue #44 should stay open after this draft pass. Close it only after the WordPress page exists at `/glossary/`, the search behavior passes preview QA, internal links are added, mobile/accessibility checks pass, and sensitive terms have KK/SME approval or are removed from the first public version.
