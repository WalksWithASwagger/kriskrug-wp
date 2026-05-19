# Accessibility Statement Draft - May 2026

Status: editorial draft for GitHub issue #48. Not published. Not legal advice. Do not treat this as a compliance claim until KK and an accessibility/legal reviewer approve the wording.

Target page: `/accessibility/`

## Draft Page Copy

# Accessibility

KrisKrug.co should be useful to as many people as possible, including people using screen readers, keyboard navigation, voice control, browser zoom, captions, high-contrast settings, and other assistive technologies.

This site is a long-running WordPress archive with current writing, older posts, photography, event coverage, project pages, and AI education material. The goal is to keep improving the experience while being honest about what has and has not been reviewed.

## Current Status

As of May 2026, the site has not completed an independent accessibility audit. Recent site work has improved parts of the content structure, including heading hierarchy on the homepage and About page, and the newsletter popup was changed so it no longer appears immediately after page load.

Known areas that still need review or cleanup include:

- Alt text coverage on older images and image-heavy posts.
- Mobile and tablet behavior across the current Catch Responsive theme.
- Keyboard and focus behavior for menus, popups, forms, search, and embedded media.
- The blog index heading structure, which may need theme-level work or the Aurora theme migration.
- Colour contrast and focus states across older theme elements and legacy content.
- Captions, transcripts, or descriptive context for older video and audio embeds where available.

## What We Are Working Toward

The working accessibility target is WCAG 2.1 AA for the site, with the published Accessibility page itself built as a simple, semantic page that can meet a higher bar where practical. Do not publish a sitewide WCAG 2.1 AAA claim unless an audit verifies it.

Near-term improvements:

- Write and review descriptive alt text for the most visible images first, then continue through recent posts and the older archive.
- Run mobile checks at phone and tablet widths.
- Test the main navigation, newsletter popup, contact paths, and forms with keyboard-only navigation.
- Keep page headings to one clear H1 followed by logical H2 and H3 sections.
- Use descriptive link text instead of vague "click here" links.
- Carry these checks into the Aurora v2 theme work before any production cutover.

## Feedback And Accommodation Requests

If something on this site is hard to read, navigate, hear, understand, or use, please contact Kris through the contact page:

https://kriskrug.co/contact/

When possible, include:

- The page URL.
- What you were trying to do.
- The barrier you hit.
- Your browser, device, and assistive technology if you are comfortable sharing it.
- The format or accommodation that would help.

Kris will review accessibility feedback and make a reasonable effort to respond or fix the issue. Response timing should be confirmed before publication.

## Review Cycle

This statement should be reviewed whenever the site theme changes, major plugins change, a new accessibility audit is completed, or a user reports a barrier.

Last reviewed: May 2026 draft. Confirm the final publication date before this goes live.

## Editorial Review Notes

- Confirm whether the target standard should be worded as WCAG 2.1 AA, WCAG 2.2 AA, or another standard before publishing.
- Confirm the reporting channel. The draft uses `/contact/` instead of inventing a direct accessibility email address.
- Confirm expected response timing before adding any commitment such as "within 5 business days."
- Do not claim the whole site is compliant. Current docs show known gaps, especially older image alt text, mobile checks, keyboard/focus checks, and legacy theme behaviour.
- If legal compliance language is needed, get legal review before publication.
- Avoid tables, decorative images, embeds, accordions, or complex layout on this page. The issue requires the page itself to be highly accessible.

## Publication Checklist

- [ ] Verify backup/snapshot path before editing production WordPress.
- [ ] Confirm no existing live page already owns `/accessibility/`.
- [ ] Create the page as a WordPress draft first, not published.
- [ ] Use exactly one H1: `Accessibility`.
- [ ] Use semantic H2 sections matching this draft.
- [ ] Add no required images. If an image is added, give it reviewed alt text or mark it decorative correctly.
- [ ] Check every link has descriptive text and a valid target.
- [ ] Confirm the contact path is correct and works.
- [ ] Run keyboard-only review: tab order, visible focus, skip links, menu access, form access.
- [ ] Run automated checks with at least Lighthouse and one accessibility scanner such as WAVE or axe.
- [ ] Test at desktop, tablet, and mobile widths.
- [ ] Add footer link only after the page content is reviewed.
- [ ] After publication, verify `https://kriskrug.co/accessibility/` returns 200 and is crawlable.
- [ ] Add the published URL to issue #48 with review notes and remaining gaps.
