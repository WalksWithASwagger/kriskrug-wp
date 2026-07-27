---
title: "Accessibility"
slug: accessibility
status: draft-only
post_type: page
draft_date: '2026-07-26'
issue: 288
refs: [48, 46, 4, 86, 127, 424, 277]
notes:
  draft_scope: "Draft-only for human review. Do not create, publish, or link /accessibility/ until KK fills the [KK: ...] placeholders and approves."
  live_probe: "2026-07-26: /accessibility/ 404; live Aurora 1.4.8; theme skip-link to #aurora-main present on homepage; no footer Accessibility link yet."
  supersedes:
    - content/drafts/2026-07-25-accessibility-statement/post.md
    - content/drafts/2026-07-24-accessibility-statement/post.md
    - content/drafts/accessibility-statement-2026-07/README.md
---

# REVIEWER BLOCK - NOT FOR PUBLICATION

Strip everything above the `---- PUBLISHABLE COPY ----` marker before any WordPress draft or publish.

Drafted 2026-07-26 for #288 (draft lane). Related publish umbrella: #48. Full audit: #46. Repo-side only. No WordPress writes. No credentials used.

## Live probe (2026-07-26, read-only)

| Check | Result |
|---|---|
| `GET /accessibility/` | **404** (still) |
| Live Aurora `style.css` Version | **1.4.8** (matches repo) |
| Homepage skip link | Present: `<a class="skip-link" href="#aurora-main">Skip to content</a>`; `#aurora-main` landmark present |
| Footer `Accessibility` link | **Absent** (Privacy/Contact still present; add only after page returns 200) |
| `/contact/` | **200** |

## What changed since the 2026-07-25 draft

The July 25 draft listed a broken skip link and theme contrast failures against live Aurora **1.4.3**. Those are outdated:

- **Skip link restored** in Aurora 1.4.4+ (`parts/header.html` targets `#aurora-main`; core `#wp-skip-link` suppressed). Confirmed live on the homepage today.
- **Contrast remediation** shipped across 1.4.4-1.4.6 (cream-system conversion, writing-card contrast, foreground/surface pairing). Do not claim site-wide WCAG AA contrast from that alone; residual and archive gaps remain.

This draft updates posture and limitations to match live 1.4.8 without overclaiming.

## Facts KK must confirm before publish

1. **Contact route.** Draft uses `/contact/` plus `mailto:feelmoreplants@gmail.com` (already on the contact page). Confirm or replace. Prefer an `accessibility@` alias only if it already exists.
2. **Reply-time commitment.** Leave blank or state a window you will actually meet. A missed SLA is worse than none.
3. **Escalation path.** Placeholder. Default informal path is drafted; name BC Human Rights Tribunal or another body only if you intend that.
4. **WCAG edition.** Draft names **WCAG 2.1 Level AA** (matches #46/#48 and repo pa11y `--standard WCAG2AA`). Confirm vs 2.2.
5. **Conformance sentence.** Keep "partially conformant" until an independent audit says otherwise.
6. **Last reviewed date.** Replace with the real publish date.
7. **Page AAA gate.** #48 still asks for the page itself to be WCAG 2.1 AAA. Confirm or relax to AA + plain structure.

## Does this close anything?

**No.** Do not close #288, #48, or #46 from this commit.

- #288 closes only after KK reviews this copy and answers the gates above.
- #48 stays open until `/accessibility/` returns 200, footer link is added (Track B, separate session), and page a11y checks pass.
- #46 remains the full audit track.

---- PUBLISHABLE COPY ----

# Accessibility

I want this site to work for you. Not as a badge in the footer, but in a practical way: you can read it, move through it, and get what you came for.

This page says where kriskrug.co honestly stands, what I know is still rough, how to tell me when you hit a barrier, and what I am fixing next.

## What this covers

This statement applies to **kriskrug.co**, including the blog archive, project pages, photography, and other content under that domain.

It does not cover other sites I link to or help run, such as BC + AI, Vancouver AI, Futureproof, or my newsletter. Those have their own addresses and their own accessibility work.

## Where the site stands

kriskrug.co is **partially conformant** with WCAG 2.1 Level AA. "Partially conformant" means some parts of the site do not fully meet the standard. No independent accessibility audit has been completed, so treat this as my own honest assessment, not a certification.

I would rather say that plainly than put a compliance badge on work that is still unfinished.

## What is working better lately

Recent Aurora theme updates (through live version 1.4.8 as of this draft) improved several basics:

- A **Skip to content** link is present on public pages and jumps to the main content landmark.
- **Colour contrast** on core surfaces was reworked (cream-system conversion and related fixes) so more text meets usable contrast levels than it did earlier in 2026.
- Visible **keyboard focus** styles exist on primary navigation, buttons, and common interactive elements.
- New editorial posts are written with clearer structure and better image alt text habits than much of the older archive.

Those are improvements, not a whole-site pass.

## Known limitations

These are current and mine to fix. If one of them is blocking you, use the workaround at the end of the item, or email me.

**Some images are missing alt text.** Mostly older archive media. This site has published since 2003 across several WordPress eras. Recent posts are in better shape. If an image matters and has no description, send me the URL and I will describe it.

**Hover and focus states are still inconsistent in places.** On some modules it is not obvious which control is selected with the keyboard. Site-wide interaction-state work is still open.

**Mobile and small-screen behaviour has not had a full dedicated QA pass.** The layout is meant to reflow, but keyboard reachability, zoom, and overflow on phones and tablets are not fully verified. If something overlaps, gets cut off, or cannot be reached on your device, tell me what you were using.

**Older posts vary a lot.** Heading structure, formatting, embedded video, and legacy media are inconsistent across two decades of archive. Some older video embeds lack captions or transcripts. If you need a transcript, ask. If one exists I will send it; if not, I will say so.

**Third-party embeds and tools.** Newsletter signup, video players, social embeds, and tracking pixels are not fully under my control. Important content on this site should also be available as plain text on the page. Tracking pixels may appear as tiny images without meaningful alt text; they are not content.

**No full accessibility audit yet.** Automated checks and manual spot checks cover a sample of high-traffic routes, not every public URL. Nobody has completed a professional screen-reader or disabled-user testing pass on this site.

## Tell me when something is broken

Please do. Reports from real people are currently the strongest signal I have.

- **[Use the contact page](https://kriskrug.co/contact/)**, or
- **email me at [feelmoreplants@gmail.com](mailto:feelmoreplants@gmail.com)** with "Accessibility" in the subject line.

**[KK: confirm this email is the public accessibility contact, or replace it. Do not invent an alias.]**

If you can, include:

- the page URL;
- what you were trying to do;
- what got in the way;
- your browser, device, or assistive technology, only if you are comfortable sharing it.

You do not owe me a technical bug report. "The text on this page is hard to read" is useful.

I will read every accessibility report. **[KK: reply-time commitment. State a real window you will meet, or delete this sentence. Do not publish an SLA you will miss.]**

## If you need another format

If something on this site is unavailable to you, ask me directly. I will make a reasonable effort to provide it another way: plain text, an image description, a transcript when one exists, or the answer in an email. That offer stands whether or not the underlying page is fixed yet.

## If I do not resolve it

If you report a barrier and I do not resolve it, email me again and say so. I will treat the follow-up as a priority. **[KK: decide whether to name a formal escalation route here, such as the BC Human Rights Tribunal, or keep this informal path. Do not name a body that has not agreed to that role.]**

## What I am working on next

In rough priority order:

1. Keep contrast, skip-link, and focus behaviour healthy as the theme evolves.
2. A fuller keyboard and focus pass across primary templates and high-traffic pages.
3. Mobile, zoom, and small-screen review.
4. Alt text for new images first, then high-value archive media people still read.
5. A complete accessibility audit across public pages, not only a sample (#46).

No published deadlines on that list. I would rather do the work than promise dates I might miss.

## How the site is built and tested

- WordPress, with the Aurora theme I maintain.
- Standard HTML (headings, lists, links, images) wherever practical.
- Reference standard: **WCAG 2.1 Level AA**.

Testing so far is **self-evaluation**: automated accessibility scans on a handful of busy pages, plus manual spot checks. That is not the same as an independent audit.

Gaps to name plainly: no completed professional screen-reader test suite, no formal specialist audit, and no systematic testing with disabled users yet. Those should happen. They have not yet.

## About this statement

Last reviewed: **[KK: publish date. Use the day this page goes live, not the draft date.]**

I will update this page when the theme changes in a meaningful way, when an audit finishes, when someone reports a barrier, or when I clear something listed above. If this page goes stale, that is a bug too. Tell me.
