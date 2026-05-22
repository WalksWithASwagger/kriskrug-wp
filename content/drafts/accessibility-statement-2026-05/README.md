# Accessibility Statement Page Package - May 2026

Status: review-ready local draft for GitHub issue #48. Not published. Not legal advice. Do not treat this as a compliance claim until KK and an accessibility/legal reviewer approve the wording.

Target page: `/accessibility/`
Recommended page title: `Accessibility`
Recommended SEO title: `Accessibility | Kris Krug`
Recommended meta description: `Accessibility statement for KrisKrug.co, including current status, known issues, feedback options, accommodation requests, and planned improvements.`
Recommended excerpt: `KrisKrug.co is working to improve accessibility across current pages and a long-running WordPress archive. This statement explains current status, known issues, feedback options, and the improvement roadmap.`

## Package Boundaries

- This is a Track A editorial page package only.
- WordPress draft creation is allowed after slug checks; public publish still needs review and QA.
- No footer, menu, theme, plugin, schema, redirect, or production setting changes are included.
- The statement is intentionally transparent and review-gated. It does not claim full WCAG conformance.
- The public page should be created as a WordPress draft first, then reviewed before publication.

## Draft Page Copy

# Accessibility

KrisKrug.co should be useful to as many people as possible, including people using screen readers, keyboard navigation, voice control, browser zoom, captions, high-contrast settings, reduced-motion settings, and other assistive technologies.

This site includes current writing, older blog posts, photography, event coverage, project pages, and AI education material built up across many years of WordPress publishing. The goal is to keep improving the experience while being honest about what has and has not been reviewed.

## Current Status

As of May 2026, KrisKrug.co has not completed an independent accessibility audit, and the site should not be described as fully compliant with WCAG or any other accessibility standard.

The site currently runs on WordPress with the Catch Responsive theme while a future theme direction is being evaluated separately. Recent maintenance work has identified accessibility issues that need cleanup across both the current site and future theme work.

WCAG 2.2 AA is the working reference for future improvements, but this statement is not a WCAG conformance claim.

## Known Accessibility Issues

Known issues and review areas include:

- Some older images and image-heavy posts need better alt text or clearer decorative-image handling.
- The live homepage and some archive views may still need heading-structure cleanup.
- Mobile and tablet behavior needs review across the current theme, long posts, media-heavy pages, and forms.
- Keyboard and visible-focus behavior needs review for navigation, search, popups, forms, embedded media, and third-party widgets.
- Some color contrast and focus states in older theme elements may need improvement.
- Older video and audio embeds may not always include captions, transcripts, or enough descriptive context.
- Some older links, buttons, and embedded content may not have enough accessible name or context.
- Future Aurora theme work needs accessibility testing before any production cutover.

## Reporting A Barrier

If something on this site is hard to read, navigate, hear, understand, or use, please contact Kris through the contact page:

[Contact Kris](https://kriskrug.co/contact/)

When possible, include:

- The page URL.
- What you were trying to do.
- The barrier you ran into.
- Your browser, device, and assistive technology, if you are comfortable sharing that information.
- The format or accommodation that would help.

Please do not include private medical information. Share only the details needed to understand the access barrier and the requested accommodation.

## Accommodation Requests

Kris will review accessibility feedback and accommodation requests in good faith and make a reasonable effort to provide the information or experience in a more accessible format.

Depending on the request, that may include clarifying page content, providing a text alternative, sharing a transcript or captioned media source when available, adjusting a broken interaction, or finding another practical way to access the information.

Response timing should be confirmed before publication. Until a response-time commitment is approved, do not add language such as "within 5 business days."

## Accessibility Roadmap

Planned accessibility improvements include:

- Review the most visible pages first: homepage, About, Work, Speaking, Contact, Blog, and high-traffic posts.
- Improve alt text for current images, recent posts, and high-value archive media.
- Test primary navigation, search, forms, popups, and key reader paths with keyboard-only navigation.
- Check desktop, tablet, and mobile layouts for zoom, reflow, focus visibility, and horizontal scrolling issues.
- Review color contrast and visible-focus styles on current theme elements.
- Prefer plain semantic page structures: one H1, logical H2 and H3 headings, descriptive links, and no layout tables.
- Carry accessibility checks into the Aurora v2 theme work before any production cutover.
- Run automated checks with Lighthouse and at least one accessibility scanner, then follow with manual review.

## Updates To This Statement

This statement should be reviewed when:

- The site theme changes.
- Major plugins, forms, popups, or navigation patterns change.
- An accessibility audit is completed.
- A visitor reports an accessibility barrier.
- New accessibility work is completed and verified.

Last reviewed: May 2026 draft. Confirm the final publication date before this goes live.

## Footer Link Requirement

After the page is reviewed and published, add a footer link labeled `Accessibility` that points to:

`https://kriskrug.co/accessibility/`

Do not add the footer link before the page exists and returns 200. After adding the footer link, verify it is keyboard reachable, has visible focus, is readable on mobile, and appears consistently on public pages where the footer is shown.

## Page Accessibility Requirements

Build the WordPress page itself as the accessible reference implementation:

- Use exactly one H1: `Accessibility`.
- Use the H2 sections in the draft copy.
- Use paragraphs and unordered lists only; avoid tables, accordions, tabs, carousels, embeds, decorative media, and custom layout blocks.
- Keep link text descriptive. Use `Contact Kris`, not a bare URL as the visible link.
- Add no required images. If an image is added later, give it reviewed alt text or mark it decorative correctly.
- Do not rely on color alone to convey status.
- Confirm browser zoom, mobile reflow, keyboard tab order, and visible focus before publication.

## Editorial Review Notes

- Confirm whether WCAG 2.2 AA is the right working reference before publication. The current wording names it only as a reference, not as a claim.
- Confirm the reporting channel. This draft uses `/contact/` instead of inventing a direct accessibility email address.
- Confirm expected response timing before adding any service-level commitment.
- Confirm whether legal language is needed for jurisdiction, statutory obligations, third-party content, or archived content.
- Do not claim the whole site is compliant. Current docs show known gaps, especially older image alt text, mobile checks, keyboard/focus checks, heading structure, and legacy theme behavior.
- Avoid blaming visitors, tools, age of content, plugins, or the current theme. Keep the tone accountable and practical.

## Issue #48 Checklist

| Acceptance item | Draft status | Notes |
|---|---|---|
| `/accessibility` statement | Ready for review | Draft page copy is included above for target slug `/accessibility/`. |
| Current status | Ready for review | States no independent audit and no full-compliance claim. |
| Known issues | Ready for review | Lists image alt text, headings, mobile, keyboard/focus, contrast, media, accessible names, and future theme QA. |
| Reporting mechanism | Needs human confirmation | Uses `/contact/` as the proposed reporting channel. |
| Accommodation process | Needs human/legal confirmation | Describes good-faith review and possible alternative formats without committing timing. |
| Roadmap | Ready for review | Lists practical near-term accessibility improvements. |
| Footer link | Publish task | Add after the page exists, is reviewed, and is published. |
| Page itself accessible | Ready as build guidance | Plain semantic page requirements are included. Must be verified in WordPress draft before publish. |

## Publication Checklist

- [ ] Confirm no existing live page, redirect, or menu item already owns `/accessibility/`.
- [ ] Create the page as a WordPress draft first, not published.
- [ ] Confirm page title: `Accessibility`.
- [ ] Confirm slug: `/accessibility/`.
- [ ] Add SEO title: `Accessibility | Kris Krug`.
- [ ] Add meta description from this package.
- [ ] Use exactly one H1: `Accessibility`.
- [ ] Use semantic H2 sections matching this draft.
- [ ] Add no required images, embeds, tables, accordions, or complex layout blocks.
- [ ] Check every link has descriptive text and a valid target.
- [ ] Confirm the contact path is correct and works.
- [ ] Confirm reporting and accommodation wording with KK.
- [ ] Get legal/accessibility review before publishing if compliance language is required.
- [ ] Run keyboard-only review: tab order, visible focus, skip links, menu access, and form access.
- [ ] Run automated checks with Lighthouse and one accessibility scanner such as WAVE or axe.
- [ ] Test at desktop, tablet, and mobile widths.
- [ ] Publish only after review gates pass.
- [ ] Verify `https://kriskrug.co/accessibility/` returns 200 and is crawlable.
- [ ] Add footer link only after the page content is reviewed and published.
- [ ] Verify the footer link is visible, keyboard reachable, and readable on mobile.
- [ ] Update issue #48 with the published URL, review notes, remaining gaps, and footer-link verification.
