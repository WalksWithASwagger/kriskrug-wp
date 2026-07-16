# Accessibility Statement Page Package - July 2026

Status: review-ready local draft for GitHub issues #304, #288, and #48. Not published. Not legal advice. Do not treat this as a compliance claim until KK and an accessibility/legal reviewer approve the wording.

Target page: `/accessibility/`
Recommended page title: `Accessibility`
Recommended SEO title: `Accessibility | Kris Krug`
Recommended meta description: `Accessibility statement for KrisKrug.co, including current status, known issues, feedback options, accommodation requests, and planned improvements.`
Recommended excerpt: `KrisKrug.co is working to improve accessibility across current pages and a long-running WordPress archive. This statement explains current status, known issues, feedback options, and the improvement roadmap.`

## Package Boundaries

- Track A editorial page package only.
- Do not publish, create, or update any live WordPress page from this packet.
- No footer, menu, theme, plugin, schema, redirect, or production setting changes are included.
- The statement is intentionally transparent and review-gated. It does not claim full WCAG conformance.
- Supersedes the May 2026 draft package at `content/drafts/accessibility-statement-2026-05/` for current Aurora live evidence (1.3.37 as of 2026-07-16). Keep the May package as historical context.

## Evidence Used (2026-07-16 refresh)

- Live theme: `kk-aurora` **1.3.37** (`style.css` Version header; repo is ahead at **1.3.40**, undeployed).
- Public `/accessibility/` still returns **404** (reconfirmed 2026-07-16).
- Public `/contact/` remains the proposed reporting channel until KK confirms otherwise.
- Handoff closeout (2026-07-05): five-route `pa11y --standard WCAG2AA` plus browser smoke closed #289/#293 for `/`, `/about/`, `/blog/`, `/work/`, `/contact/`.
- Older archive/media alt-text debt remains open under #4; full WCAG audit remains open under #46.
- Original packet evidence date was 2026-07-08 against Aurora 1.3.36; theme bump since then does not change the open human gates below.

## Evidence Used (2026-07-08, historical)

## Draft Page Copy

# Accessibility

KrisKrug.co should be useful to as many people as possible, including people using screen readers, keyboard navigation, voice control, browser zoom, captions, high-contrast settings, reduced-motion settings, and other assistive technologies.

This site includes current writing, older blog posts, photography, event coverage, project pages, and AI education material built up across many years of WordPress publishing. The goal is to keep improving the experience while being honest about what has and has not been reviewed.

## Current Status

As of July 2026, KrisKrug.co has not completed an independent accessibility audit, and the site should not be described as fully compliant with WCAG or any other accessibility standard.

The site currently runs on WordPress with the Aurora theme (`kk-aurora` 1.3.37 live as of July 2026). Recent work improved contrast, skip links, keyboard smoke coverage, and core-route readability on the homepage, About, Blog, Work, and Contact pages. That work is progress, not a whole-site conformance claim.

WCAG 2.1 AA / WCAG 2.2 AA is the working reference for future improvements. **[NEEDS KK REVIEW]** Confirm which WCAG edition to name publicly before publish. This statement is not a WCAG conformance claim either way.

## Known Accessibility Issues

Known issues and review areas include:

- Some older images and image-heavy archive posts still need better alt text or clearer decorative-image handling (#4).
- Older archive posts and legacy media may still vary in heading structure and formatting after multiple WordPress/theme eras.
- Mobile and tablet behavior still needs a dedicated responsive QA pass across long posts, media-heavy pages, and forms (#127).
- Keyboard and visible-focus behavior needs ongoing review for navigation, search, popups, forms, embedded media, and third-party widgets.
- Some embedded third-party tools, tracking pixels, or external media may not provide the same accessibility controls as the main site.
- Older video and audio embeds may not always include captions, transcripts, or enough descriptive context.
- A full WCAG 2.1 AA audit remains open (#46).

## Reporting A Barrier

If something on this site is hard to read, navigate, hear, understand, or use, please contact Kris through the contact page:

[Contact Kris](https://kriskrug.co/contact/)

**[NEEDS KK REVIEW]** Confirm whether reporting should stay on `/contact/`, use a dedicated accessibility email, or both. Do not invent an email address.

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

**[NEEDS KK REVIEW]** Response timing should be confirmed before publication. Until a response-time commitment is approved, do not add language such as "within 5 business days."

## Accessibility Roadmap

Planned accessibility improvements include:

- Keep the most visible pages healthy: homepage, About, Work, Speaking, Contact, Blog, topic hubs, and high-traffic posts.
- Improve alt text for current images, recent posts, and high-value archive media.
- Complete dedicated mobile/responsive QA and keyboard/focus review.
- Prefer plain semantic page structures: one H1, logical H2/H3 headings, descriptive links, and no layout tables.
- Run automated checks with Lighthouse and at least one accessibility scanner, then follow with manual review.
- Publish this accessibility statement only after human review, then add a footer link.

## Updates To This Statement

This statement should be reviewed when:

- The site theme changes.
- Major plugins, forms, popups, or navigation patterns change.
- An accessibility audit is completed.
- A visitor reports an accessibility barrier.
- New accessibility work is completed and verified.

Last reviewed: July 2026 draft. Confirm the final publication date before this goes live.

## Footer Link Requirement

After the page is reviewed and published, add a footer link labeled `Accessibility` that points to:

`https://kriskrug.co/accessibility/`

Do not add the footer link before the page exists and returns 200.

## Page Accessibility Requirements

Build the WordPress page itself as the accessible reference implementation:

- Use exactly one H1: `Accessibility`.
- Use the H2 sections in the draft copy.
- Use paragraphs and unordered lists only; avoid tables, accordions, tabs, carousels, embeds, decorative media, and custom layout blocks.
- Keep link text descriptive. Use `Contact Kris`, not a bare URL as the visible link.
- Add no required images.
- Confirm browser zoom, mobile reflow, keyboard tab order, and visible focus before publication.

## Issue Checklist

| Acceptance item | Draft status | Notes |
|---|---|---|
| `/accessibility` statement | Ready for review | Draft page copy above; public URL still 404. |
| Current status | Ready for review | Names Aurora 1.3.36 progress without claiming full compliance. |
| Known issues | Ready for review | Lists alt text, archive variance, mobile QA, keyboard/focus, third-party embeds, full audit. |
| Reporting mechanism | Needs human confirmation | Uses `/contact/` as the proposed channel. |
| Accommodation process | Needs human/legal confirmation | Good-faith review; no timing SLA yet. |
| Roadmap | Ready for review | Practical near-term improvements. |
| Footer link | Publish task | Add only after the page is live. |
| Page itself accessible | Ready as build guidance | Plain semantic requirements included. |

## Publication Checklist

- [ ] Confirm no existing live page, redirect, or menu item already owns `/accessibility/`.
- [ ] Recheck whether old draft page `11886` still exists and should be reused.
- [ ] Create or update the page as a WordPress **draft** first, not published.
- [ ] Confirm page title, slug, SEO title, and meta description.
- [ ] Confirm reporting channel and response-time wording with KK.
- [ ] Confirm WCAG edition wording with KK.
- [ ] Get legal/accessibility review before publishing if compliance language is required.
- [ ] Run keyboard-only and mobile checks on the draft page.
- [ ] Publish only after review gates pass.
- [ ] Verify `https://kriskrug.co/accessibility/` returns 200.
- [ ] Add footer link only after publish.
- [ ] Update #48 / #288 / #304 with the published URL and remaining gaps.
