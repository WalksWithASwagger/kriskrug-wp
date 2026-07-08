# About / bio body-only payload plan — #290

Status: planning only. Do not update `/about/`, bios, footer, or live WordPress content from this document.  
Depends on: `about-bio-source-map-2026-07-07.md` (#307). Related: #269, #270, #22.

## Goal

Consolidate the archive-mining and pilot-school threads into one reviewable body-only About payload plan before any live WordPress update.

## Preserve

- Existing public page title (`About` / current rendered title). Do **not** send a REST `title` field unless KK explicitly approves a title change.
- Existing lead + rooms grid + public trail framing as the baseline.
- Current contact CTA.

## Must-have additions (first slice)

Insert one new section between **Public trail** and **Start with the work**:

### From the archive

Three short cards/paragraphs max:

1. **Flying in the direction of the work**  
   Pilot school (2013) → aerial photography (2015). Frame: learning a tool deeply, then using the human eye.  
   Links:
   - https://kriskrug.co/2013/09/14/pilot-school-flying-in-the-direction-of-my-dreams/
   - https://kriskrug.co/2015/09/08/aerial-photography-combining-my-loves-for-flying-and-making-photos/

2. **Before AI, there was community**  
   Early web/community organizing → Vancouver AI → BC + AI.  
   Links:
   - https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/
   - https://bc-ai.ca/

3. **Movement media**  
   TEDxOilSpill + COP15 as focused proof that the archive includes movement work, not only tech conferences.  
   Links:
   - https://kriskrug.co/2009/12/14/photo-essay-inside-the-negotiations-cop15/
   - Optional second: https://kriskrug.co/2009/12/14/photo-essay-streets-of-copenhagen-cop15-united-nations-climate-change-summit/

## Optional / later modules

- LaSalle / Both Hands Full teaching room proof.
- Expanded speaking/media appearances list (coordinate with #95).
- Longer photography credentials module.

## Indigenous land acknowledgment (#22)

Recommendation for this plan: **do not move or rewrite** the land acknowledgment in the first About body slice. It already appears in site chrome on the About page. Decide separately whether it also belongs in the About body, footer-only, or both. Any new wording needs KK review.

## Explicitly out of scope for the first write

- Author-bio field edits.
- REST `title` changes.
- “Licensed private pilot” or similar credential claims unless KK confirms exact wording.
- New stats, awards, client lists, or publication bibliographies.
- Footer/theme/menu changes.

## Snapshot / write / rollback checklist

1. Authenticated GET of the About page by ID/slug; record ID, status, slug, modified date.
2. Snapshot `content.raw` + rendered HTML to `backup/<timestamp>-about-bio/`.
3. Build body-only payload from `wp-payloads/about.html` plus the new module; keep title out of the payload.
4. Dry-run: print payload byte size, section headings, and link list; no write.
5. Human review of the dry-run HTML.
6. Execute body-only REST update only with explicit KK approval.
7. Cache-busted public smoke on https://kriskrug.co/about/ — confirm new module, old sections intact, no title regression.
8. If rollback needed: restore snapshot `content.raw` via body-only update.

## Acceptance mapping

| #290 criterion | Plan status |
|---|---|
| Review pilot-school (#269) + archive mining (#270) | Covered in source map + must-have module |
| Body-only payload plan; preserve title | This document |
| Land acknowledgment placement (#22) | Deferred; keep chrome; no first-slice body rewrite |
| Separate must-have vs optional | Sections above |
| Snapshot/write/rollback checklist | Section above |
| Human review before WP write | Required stop rule |
