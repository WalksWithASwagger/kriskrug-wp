# About/bio body-only payload plan - #290

Track A planning package only. Consolidates #269 (pilot school) and #270 (archive mine) into one reviewable About/bio payload plan.

**No live WordPress write from this package.**

| File | Role |
|---|---|
| `payload-plan.md` | Body-only plan, title freeze, sequencing with #418 / PR #504 |
| `modules.md` | Must-have vs optional archive/story modules |
| `land-acknowledgment.md` | Where #22 should live if it fits naturally |
| `checklist.md` | Snapshot / write / rollback for the eventual live update |
| `draft-snippets.md` | Optional draft copy modules for KK review |

## Sibling coordination (do not duplicate)

- **PR #504** / branch `cursor/418-about-page-draft-f196` owns layout, background/column unify, and the "public trail" copy fix for `/about/`.
- Package path there: `content/drafts/2026-07-26-about-page/`
- This #290 package owns **bio/archive content enrichment** only. Do not ship a competing full page body that re-implements #418 CSS or trail copy.
- Recommended order after KK review: apply #418 layout/copy first (or fold #290 modules into a post-#418 body), then apply #290 modules as a second body-only pass if not merged into one approved payload.

## Sources

- Issues: #290, #269, #270, related #22
- Archive catalog: `docs/archive-content-mine.md`
- Historical long-form About draft: `fixes/UPDATED-ABOUT-PAGE-COMPLETE.md` (pre-architecture; do not restore wholesale)
- Live page: https://kriskrug.co/about/ (WP page ID `1208`, slug `about`)
- Pilot source post: https://kriskrug.co/2013/09/14/pilot-school-flying-in-the-direction-of-my-dreams/

## Blocked on KK

- Which must-have modules to include
- Wording for any new credential lines
- Whether short author bio (`theme/kk-aurora/templates/single.html`) gets a pilot mention (Track B if theme file; keep out of this body-only About pass unless KK asks)
- Explicit approval before any title field change (default: preserve)
- Human review of final payload before any WordPress write
