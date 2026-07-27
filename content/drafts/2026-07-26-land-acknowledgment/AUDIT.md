# Audit - live land acknowledgment evidence (#22)

Read-only checks on 2026-07-26. No writes.

## Summary

| Surface | Status | Notes |
|---|---|---|
| Site footer (Aurora brand tile) | Present | Short Musqueam / Squamish / Tsleil-Waututh line |
| Footer bottom utility | Present | Link labeled `Reconciliation` → dedicated page |
| About page body | Absent | Land line not in About entry content (footer still shows) |
| Dedicated page | Present | `/reconciliation-indigenous-land-acknowledgement/` with Nation links |

## Footer (sitewide)

Source of truth in repo theme: `theme/kk-aurora/parts/footer.html` (Track B). Live homepage and About both render:

> AI keynotes, workshops, and ecosystem work from the traditional, ancestral, and unceded territories of the Musqueam, Squamish, and Tsleil-Waututh Nations.

Footer bottom also links:

- `/reconciliation-indigenous-land-acknowledgement/` (label: Reconciliation)
- `/the-kk-worldview/` (label: Worldview)

## About page (`/about/`, WP ID 1208)

- Entry content: no Musqueam / Squamish / Tsleil-Waututh / land acknowledgment copy in the page body (checked after stripping `<footer>`).
- The footer acknowledgment still appears because it is site chrome.
- #290 plan already deferred body placement: keep chrome; decide #22 separately; no first-slice About rewrite.
- #418 draft unifies backgrounds / kills double "public trail" and does not add land copy. Do not inject into that payload.

## Reconciliation page

URL: https://kriskrug.co/reconciliation-indigenous-land-acknowledgement/

Public body (compressed):

- Opening commitment to honour Indigenous presence and sovereignty; reconciliation language.
- Core acknowledgment (live text includes Coast Salish peoples + Musqueam / Squamish / Tsleil-Waututh with Nation site links). Live characters may mangle in some extracts; treat Nation English names + linked URLs as the stable public intent.
- Links: Musqueam, Squamish, Tsleil-Waututh Nation sites; Land Back campaign.
- Supporting photography captions (Tribal Journey / Squamish Nation Youths).

## Vancouver / Host Nation naming (verify for KK)

City of Vancouver and common local institutional wording name the **xʷməθkʷəy̓əm (Musqueam), Sḵwx̱wú7mesh (Squamish), and səlilwətaɬ (Tsleil-Waututh) Nations** on unceded traditional territories. Musqueam is appropriate for Vancouver context, not optional trivia.

"Coast Salish" names a broader cultural / linguistic grouping. Respectful Vancouver practice usually **names the three Host Nations** and may add "Coast Salish peoples" as the collective frame (as the Reconciliation page already does). Treating "Coast Salish" as a fourth Nation, or listing Coast Salish *instead of* Musqueam, is weaker than the local standard.

Issue #22 acceptance text lists Coast Salish, Squamish, Tsleil-Waututh. This packet includes Musqueam because that matches City of Vancouver practice, the live footer, and the live Reconciliation page.

## Earlier repo note (historical)

`fixes/issue-22-land-acknowledgment.md` suggested adding footer copy as if none existed. That note is outdated relative to current Aurora footer + Reconciliation page. Prefer this 2026-07-26 package.

## Gap vs #22 acceptance

1. Visibility: largely met via footer + dedicated page.
2. Tone / authenticity: KK still needs to pick stronger or quieter copy if the current one-liner feels too buried in brand blurb.
3. Nation links in the always-on surface: not in footer paragraph today; present on Reconciliation page.
4. About placement: optional; currently empty in body by design of #290/#418.
5. WCAG: see `wcag-notes.md` (contrast, link purpose, Unicode names, mobile).
