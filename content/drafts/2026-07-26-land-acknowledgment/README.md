# Indigenous land acknowledgment draft package (#22)

Track A draft only. No live WordPress write. No theme publish from this packet.

**Issue:** [#22](https://github.com/WalksWithASwagger/kriskrug-wp/issues/22)  
**Related (coordinate, do not conflict):**
- [#290](https://github.com/WalksWithASwagger/kriskrug-wp/issues/290) About/bio payload: `content/drafts/2026-07-26-about-bio-payload/` (esp. `land-acknowledgment.md` + O6 snippet)
- [#418](https://github.com/WalksWithASwagger/kriskrug-wp/issues/418) About page unify: `content/drafts/2026-07-26-about-page/` on branch `cursor/418-about-page-draft-f196`

## Verdict for KK

Site chrome already carries a short territorial acknowledgment in the Aurora footer brand tile, plus a dedicated Reconciliation page with Nation links. Gap vs #22 is not "missing entirely." It is: (1) whether footer copy should name Coast Salish peoples and/or link Nations, (2) whether About should also carry a short values-adjacent module, (3) tone choice.

**Recommended path:** Keep footer as the always-on placement. Pick tone Option A (or B). Nation links stay on the Reconciliation page; footer already deep-links `Reconciliation`. Treat About-body land copy as the same optional O6 lane documented in the #290 package: skip on first About write unless KK wants narrative ownership; if approved, place after Receipts / before CTA, and only after #418 layout/copy lands.

## Package files

| File | Role |
|---|---|
| `AUDIT.md` | Live evidence (footer, About, Reconciliation page) |
| `copy-options.md` | Three tone options for KK picker |
| `placement.md` | Footer and/or About recommendation + #290/#418 coordination |
| `nation-links.md` | Optional Nation website links (verified 200) |
| `wcag-notes.md` | WCAG 2.1 AA notes for placement and markup |
| `proposed-footer-snippet.html` | Apply-ready footer paragraph variants (Track B later) |
| `proposed-about-section.html` | Optional About module (after #418; not for first About write) |
| `publish-gate.md` | Human gates before any live change |

## Acceptance mapping (#22)

| Criterion | Draft status |
|---|---|
| Visible (footer or About) | Footer already visible sitewide; About optional later |
| Coast Salish / Squamish / Tsleil-Waututh | Options name Coast Salish peoples + the three Host Nations (incl. Musqueam for Vancouver standard) |
| Respectful, authentic tone | Three options in `copy-options.md` |
| Optional Nation website links | Documented; recommended on Reconciliation page (already live) |
| Mobile responsive | Footer already in Aurora bento; About module uses existing page grid |
| WCAG 2.1 AA | Notes in `wcag-notes.md`; no conformance claim |

## Out of scope (this packet)

- Live WP REST updates
- Theme file edits (`theme/kk-aurora/parts/footer.html` is Track B)
- Rewriting the full Reconciliation page body
- Mixing into #418 About payload or #290 first About body slice
