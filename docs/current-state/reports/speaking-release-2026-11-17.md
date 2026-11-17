# Speaking-page release · November 17, 2026

Kris approved the reviewed Speaking-page proposal for publication in chat.
WordPress page **1887**, exact slug **speaking**, was updated on November 17
at **18:19:45 UTC**. The canonical payload in this release records the saved
WordPress body, using the deploy tooling's whitespace normalization.
The existing page-map readback markers now identify the approved headline,
booking CTA and LaSalle recording. All eleven existing page-payload tests pass.

The page leads with “Both things are true,” expands the Both Hands Full
keynote, pairs its LaSalle image with the full LaSalle recording, and adds
the [November 5 Prompt Victoria programme](https://promptvictoria.ca/session/field-notes-from-the-rooms-where-ai-gets-real/).
Michelle Diamond's cleared close portrait appears beside a booking email
brief, with her photo credit. The six-talk catalogue and its audience filters
remain available. The essay “Both Things Are True” remains scheduled for
November 24, so the featured section links the published talk script and
Both/And exercise.

## Verification

- The published [Speaking page](https://kriskrug.co/speaking/) returned the
  approved content. Authenticated readback matched the submitted body except
  that WordPress self-closed the new portrait image tag.
- Live browser checks at 375 and 1440 CSS pixels found no horizontal
  overflow. The catalogue changed from six talks to four for Leaders and back
  to six for All talks. The section jump reached its heading. Booking-link
  contrast and keyboard order were checked.
- The preview's eleven public link checks passed. The LaSalle image and
  Michelle's portrait loaded. The voice check found zero violations, the
  WordPress character boundary passed, and the inline interaction script
  passed its JavaScript syntax check.
- The live visual comparison **exceeded the regression thresholds** for all
  three Speaking-page viewports. Baseline `20261117T181833Z` and candidate
  `20261117T182117Z` differ because the approved proposal adds the featured
  talk, November programme and portrait sections. Mobile, tablet and desktop
  pixel differences were 34.086%, 29.470% and 27.836%, with full-page height
  increases of 28.703%, 23.628% and 25.654%. This is an intended layout change
  approved in the reviewed proposal, followed by the manual checks above.
  It is **not a passing pixel comparison**. Theme styles and the Boost bundle
  were unchanged in this content-only update.

Screenshots cover rendering. Keyboard checks cover the interactions named
above. No booking email was sent and no attendee or conversion outcome is
claimed.

## Rollback

The exact prior WordPress body is retained in the private release evidence
with SHA-256
`7749aeabfa81145580e1c4aed5b20cd5dc35c524a9e9025373ecdf50ae334c12`.
The saved release body has SHA-256
`e38743e334ddc47ad6e07c2a4806470a8bd40accff8deb98012b708fd4996fa5`.
For a rollback, re-read page 1887 and verify its slug and current content,
restore only the captured body with Kris's approval, and check the stored
body and canonical public page. No theme rollback is needed for this page
update.
