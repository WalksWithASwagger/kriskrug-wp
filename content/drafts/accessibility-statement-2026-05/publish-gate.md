# Accessibility Statement Publish Gate

Status: review-ready local package; do not publish without KK approval and accessibility/legal review as needed.

Issue: #48 `[A11Y] Create Accessibility Statement`
Target URL: `/accessibility/`
Draft source: `content/drafts/accessibility-statement-2026-05/README.md`

## Gate Summary

The accessibility statement package is ready for human review, not live publication. It includes transparent current-status language, known issues, a proposed reporting mechanism, an accommodation process, an accessibility roadmap, footer-link instructions, and page-level accessibility requirements.

No live WordPress writes were performed in this lane. The page and footer link remain blocked until the normal Track A backup/restore gate, WordPress draft creation, review, and live QA are complete.

## Acceptance Check

| Requirement | Status | Notes |
|---|---|---|
| `/accessibility` statement | Drafted | Page copy is ready for WordPress draft creation at `/accessibility/`. |
| Current status | Drafted | Says no independent audit and no full-compliance claim. |
| Known issues | Drafted | Names current review areas without overstating severity or completeness. |
| Reporting mechanism | Needs confirmation | Proposed mechanism is the existing contact page. Confirm before publish. |
| Accommodation process | Needs confirmation | Good-faith process is drafted; response timing is intentionally not committed. |
| Roadmap | Drafted | Near-term site, content, keyboard, mobile, contrast, media, and Aurora checks are listed. |
| Footer link | Blocked by live publish | Add only after the page exists and returns 200. |
| Page itself accessible | Drafted as gate | Requires one H1, semantic H2s, no complex layout, descriptive links, keyboard/zoom/mobile checks. |

## Required Reviews Before Publish

- KK editorial review for tone, accountability, and practical workflow.
- Accessibility review for accuracy, missing barriers, page structure, and support process.
- Legal review if the statement needs jurisdiction-specific compliance language.
- Publisher review that `/accessibility/` is available and does not collide with an existing page, redirect, menu item, or plugin route.

## WordPress Draft Gate

- [ ] Backup/restore proof gate is current before live WordPress editing.
- [ ] Page is created as a private or draft WordPress page before publication.
- [ ] Slug is exactly `/accessibility/`.
- [ ] Page title is `Accessibility`.
- [ ] SEO title is `Accessibility | Kris Krug`.
- [ ] Meta description matches the README package or an approved legal/editorial revision.
- [ ] Visible page content uses approved copy only.
- [ ] Contact link points to `https://kriskrug.co/contact/` or another approved reporting channel.

## Accessibility QA Gate

- [ ] Exactly one H1.
- [ ] Logical H2 sections.
- [ ] No tables, accordions, tabs, carousels, embeds, required images, or complex custom layout blocks.
- [ ] Descriptive link text.
- [ ] Keyboard-only navigation works from header to footer.
- [ ] Visible focus is present on links, header navigation, contact link, and footer link after it is added.
- [ ] Page reflows without horizontal scrolling at mobile widths and browser zoom.
- [ ] Automated checks run with Lighthouse and one scanner such as WAVE or axe.
- [ ] Manual review confirms status and process are not conveyed by color alone.

## Footer Link Gate

Add the footer link only after publication.

- [ ] `https://kriskrug.co/accessibility/` returns 200.
- [ ] Footer link label is `Accessibility`.
- [ ] Footer link points to `https://kriskrug.co/accessibility/`.
- [ ] Footer link appears on the intended public templates/pages.
- [ ] Footer link is keyboard reachable.
- [ ] Footer link has visible focus.
- [ ] Footer link remains readable and tappable on mobile.

## Closure Recommendation

Issue #48 should stay open after this draft pass. Close it only after the WordPress page exists at `/accessibility/`, KK and any required legal/accessibility reviewer approve the wording, accessibility QA passes on the page itself, the footer link is live and verified, and the issue is updated with the published URL plus remaining known gaps.
