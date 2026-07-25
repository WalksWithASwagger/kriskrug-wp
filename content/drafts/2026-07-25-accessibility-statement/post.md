---
title: "Accessibility"
slug: accessibility
post_date: '2026-07-25'
status: draft-only
post_type: page
author_wp_id: 1
featured: false
excerpt: "How accessible kriskrug.co actually is right now, what is known to be broken, how to tell me when you hit a barrier, and what I am doing about it."
issue: 288
refs: [48, 46, 4, 86, 127, 424, 277, 304]
notes:
  draft_scope: "Draft-only. Nothing has been written to WordPress. Do not create, publish, or link the live page until KK approves the copy and fills the [KK: ...] placeholders."
  supersedes:
    - content/drafts/2026-07-24-accessibility-statement/post.md
    - content/drafts/accessibility-statement-2026-07/README.md
    - content/drafts/accessibility-statement-2026-05/README.md
---

# REVIEWER BLOCK — NOT FOR PUBLICATION

**Everything above the `---- PUBLISHABLE COPY ----` marker is for KK only. Strip this entire block before the page body goes anywhere near WordPress.**

Drafted 2026-07-25 against issue #288 (draft) and #48 (publish umbrella). Repo-side only: no WordPress read/write was attempted, no credentials used, no theme or template file touched.

## 1. Why this draft exists when three others already do

| Existing draft | Problem with it |
|---|---|
| `content/drafts/2026-07-24-accessibility-statement/post.md` | **Overclaims.** Says "We aim for WCAG 2.2 Level AA", lists "Skip-to-content links on public pages" and "Keyboard-accessible primary navigation" as things already done, and hard-codes a personal email as the accessibility contact. The skip-link claim is not currently true (see limitation 2 below) and the standard was never confirmed by KK. Also written in "we" voice for a one-person site. |
| `content/drafts/accessibility-statement-2026-07/README.md` | Good, honest, and the basis for a lot of this draft — but its evidence is pinned to Aurora **1.3.37** and a 2026-07-16 pa11y run that returned zero contrast issues. Aurora is now **1.4.3** and that clean result no longer holds. Its copy is also long and reads more like a compliance memo than like Kris. |
| `content/drafts/accessibility-statement-2026-05/README.md` | Superseded in May by its own successor. Historical. |

This draft keeps the July packet's honesty and its publication/footer checklists (still valid — read them alongside this), refreshes the evidence to 1.4.3, adds the standard W3C/WAI statement sections that were missing (conformance status, technical specifications, assessment approach), and rewrites the copy in KK's first-person voice.

**Recommendation:** after KK approves, delete or banner the three superseded drafts so the next agent does not publish the wrong one.

## 2. Facts KK must confirm before this is published

Numbered so you can reply "1 yes, 2 no, 3 use X".

1. **Contact route.** I used the existing `/contact/` page as the reporting channel, with the `mailto:feelmoreplants@gmail.com` address that page already uses named as the direct alternative. Confirm this is the address you want publicly associated with accessibility complaints, or give a different one. (See section 4 for why I chose this.)
2. **Response-time commitment.** Left as a placeholder. Do not let anyone fill this in with "5 business days" unless you actually intend to meet it — a missed published SLA is worse than none.
3. **Escalation path.** Left as a placeholder. Canada/BC has no single mandatory route for a personal site; the honest options are (a) say nothing beyond "email me again and I will escalate it myself", (b) name the BC Human Rights Tribunal, or (c) name a lawyer/organization. I did **not** pick one for you. Option (a) is drafted in as the default because it is the only one I can write without inventing a relationship you may not have.
4. **WCAG version to name publicly.** I used **WCAG 2.1 Level AA** because that is what #46 and #48 are written against and what the repo's pa11y runs use (`--standard WCAG2AA`). The 2026-07-24 draft said 2.2 AA. Pick one; do not ship both.
5. **The conformance sentence itself.** This is the load-bearing legal line. It is quoted in section 3 below. Read it word for word.
6. **Hosting/platform disclosure.** I named WordPress and the Aurora theme (both already public in page source) but deliberately did **not** name Pagely, GA4, or the Meta pixel. Confirm you are fine with that level of disclosure.
7. **"Last reviewed" date.** Currently 2026-07-25 (draft date). Change it to the actual publish date, not the draft date.
8. **Whether the page itself must hit AAA.** #48's last acceptance box says "Page itself WCAG 2.1 AAA accessible". The `accessibility-statement-2026-07` packet's build guidance (one H1, plain lists, no embeds, descriptive link text, no required images) is written to satisfy that; the copy below follows it. Confirm AAA is still the gate, or relax it to AA + semantic structure. This is human gate #4 in `handoff-issue-304.md` and is still unanswered.

## 3. The conformance claim, verbatim

> kriskrug.co is **partially conformant** with WCAG 2.1 Level AA. "Partially conformant" means some parts of the site do not fully meet the standard. No independent audit has been done, so treat this as my own honest assessment rather than a certification.

That is the whole claim. It does not say the site meets AA, does not say it will by a date, and does not describe any testing that has not happened.

## 4. Decisions I made, and why

- **`/contact/` as the primary route, email as the backup.** `/contact/` is live (HTTP 200 as of the 2026-07-08 check in `handoff-issue-304.md`), is the site's only real inbound route, and per #277 the decision is explicitly to stay with a lightweight email CTA rather than add a form plugin. `content/drafts/2026-07-24-contact-421/NOTES.md` confirms the page has **no contact form** and routes to `mailto:feelmoreplants@gmail.com`. Naming both the page and the address matters for accessibility: a visitor who cannot use the contact page for the very reason they are writing needs an address they can reach directly. **Ambiguity flagged:** that address is a personal Gmail, not an `accessibility@` alias. If you would rather not publish it in this context, an alias is the cleaner answer — but do not publish an alias that does not exist yet.
- **First person, "I", not "we".** Every other page on the site is first person ("I build culture around emerging technology", "The fastest path is email"). A statement written in corporate "we" would be the one page on the site that sounds like someone else wrote it.
- **Plain language is a WCAG requirement, not a style preference.** Short sentences, no "endeavour to", no "in accordance with the aforementioned". Kept legalese to zero.
- **Limitations describe the user's experience first, the technical cause second, and always say what to do instead.** A limitation with no workaround is just an apology.
- **No roadmap dates.** #48 asks for a roadmap; I gave priorities, not deadlines. Published deadlines you miss are a liability.
- **No assistive-technology claims.** Nobody has tested this site with JAWS, NVDA, VoiceOver, or Dragon. The statement says so rather than implying coverage.
- **Both limitations sourced from live 1.4.3 (contrast + skip link) are stated as current and unfixed.** They are the newest and most user-visible problems and burying them would defeat the point of the page.

## 5. Known limitations and their sources

| # in copy | Limitation | Backing |
|---|---|---|
| 1 | Text/colour contrast failures on current theme | Aurora **1.4.3** QA pass 2026-07-25 (confirmed by the orchestrating session). Prior instance of the same class of defect: #293 (opal contrast, closed after the 2026-07-05 / 2026-07-16 pa11y runs) and the older AURORA P1 low-contrast body-text issue. **No open issue currently tracks the 1.4.3 regression — file one.** |
| 2 | Skip link does not work | Aurora **1.4.3** QA pass 2026-07-25. Repo corroboration: `theme/kk-aurora/parts/header.html` line 3 is only a comment ("WordPress core renders `#wp-skip-link`") — the theme ships `.skip-link` CSS in `style.css` and `#wp-skip-link:focus` styles in `assets/css/revive-port.css` but no skip-link markup of its own. **No open issue — file one.** |
| 3 | Missing/empty image alt text, mostly in the archive | #4 (open). Evidence: `docs/current-state/reports/issue-4-public-image-alt-20260716.md` — 8 images missing an alt attribute and 2 with empty non-decorative alt across 8 sampled public pages, including a crowd-shot JPEG on `/home/` and a legacy 2005 image on the Flickr badge page. |
| 4 | Hover/focus states missing or inconsistent across the site | #424 (open) — "There's no hovers or interactivity on any of that shit"; site-wide gap inventory not yet produced. |
| 5 | Mobile/responsive behaviour not fully QA'd | #127 (open, currently `blocked`) — keyboard reachability of the horizontal mobile nav, focus indicators, and overflow at 360/390/768 all still unverified. |
| 6 | No full audit; sampling only covers ~5 routes | #46 (open) — "Audit covers 100% of public pages" and "Audit by accessibility specialist" both unchecked. #86 (open) covers the post-Jetpack keyboard/contrast/reduced-motion spot checks that also remain incomplete. |
| 7 | Third-party embeds and legacy media | Newsletter (Beehiiv), video embeds, and a 20+ year WordPress archive. Also the Meta pixel `<noscript>` image, which is the source of most of the "missing alt attribute" hits in the #4 report — worth knowing that number is inflated by tracking pixels, not editorial images. |

Not surfaced in the public copy but worth knowing: `/accessibility/` returned **404** at the last check (2026-07-16), and a private WP draft page **11886** may still exist and should be reused or deleted rather than creating a duplicate — this is still an unanswered gate from `handoff-issue-304.md`.

## 6. Suggested slug, URL, and linking

- **Slug:** `accessibility` → `https://kriskrug.co/accessibility/` (matches #48's acceptance criterion exactly).
- **Page title:** `Accessibility`
- **SEO title:** `Accessibility | Kris Krug`
- **Meta description:** `Accessibility statement for kriskrug.co: current status, known problems, how to report a barrier, and what I am fixing next.`
- **Footer link:** add `Accessibility` to the **Utility** column of `theme/kk-aurora/parts/footer.html`, next to `Privacy` and `Contact`. That is a Track B theme edit and belongs in its own commit and its own session — **not this one**. Add it only after the page returns 200.
- Follow the build requirements in `content/drafts/accessibility-statement-2026-07/README.md` under "Page Accessibility Requirements" — one H1, lists and paragraphs only, no embeds, descriptive link text.

## 7. What I could not determine

- Whether anyone has ever tested the site with a screen reader. The copy says nobody has; if that is wrong, correct it.
- Whether WP draft page 11886 still exists (needs authenticated access I do not have and must not acquire).
- Whether `/accessibility/` is still 404 today, or whether a redirect or menu item already claims it.
- The current live Aurora version. Repo `theme/kk-aurora/style.css` says **1.4.3**; live has historically lagged repo. The copy avoids naming a version number for exactly this reason.
- Whether an `accessibility@` alias exists on the kriskrug.co domain.
- What escalation route, if any, KK wants named.

## 8. Does this close anything?

**Neither issue closes on this commit.**

- **#288** is the draft step and its acceptance criteria are all met by this file *except* the last one, "Keep the draft human-reviewed before publishing" — which by definition only KK can satisfy. Close #288 once KK has reviewed the copy and answered section 2, whether or not the page ships.
- **#48** is the publish umbrella. It needs a live `/accessibility/` returning 200, a footer link, and page-level a11y verification. None of that is possible from a repo-side draft. #48 stays open. Its own 2026-06-11 comment already reached this conclusion: "not a clean autonomous issue… This is content/legal/accessibility review plus a publish action, not blind repo automation."
- **Relationship:** #48 (opened 2026-01-02) is the parent/publish umbrella; #288 (opened 2026-07-01) is the draft-only child carved out of it so an agent could do the writing safely without touching production. Same page, two lanes. #304 was a third, packaging-focused sibling. They are not duplicates and should not be merged, but #288 should be closed first and #48 should reference this file as its input.

---- PUBLISHABLE COPY ----

# Accessibility

I want this site to work for you. Not in a badge-on-the-footer way — in a "you can actually read it, navigate it, and get what you came for" way.

This page tells you where the site honestly stands, what I know is broken, and how to tell me when you hit something I missed.

## What this covers

This statement applies to **kriskrug.co**, including the blog archive, project pages, photography, and everything else under that domain.

It does not cover other sites I link to or work on — BC + AI, Vancouver AI, Futureproof, my newsletter, or anything else with its own address. Those have their own owners and their own accessibility.

## Where the site actually stands

kriskrug.co is **partially conformant** with WCAG 2.1 Level AA. "Partially conformant" means some parts of the site do not fully meet the standard. No independent audit has been done, so treat this as my own honest assessment rather than a certification.

I would rather tell you that than put a compliance badge on a site I have not finished checking.

## What I know is broken right now

These are real, current, and mine to fix. If one of them is blocking you, the workaround is at the end of each item — and emailing me always works.

**Some text is too low-contrast to read comfortably.** A recent design update to the site's colours pushed some headings, intro paragraphs, and link text below the contrast level they need to be. If text is hard to read, your browser's reader mode strips the site's colours and gives you plain black on white — that will work on every article here.

**The "skip to content" link is not working.** If you navigate by keyboard, you currently have to tab through the whole header on every page instead of jumping straight to the article. Until I fix it, your browser's or screen reader's "jump to next heading" command is a faster route into the content.

**Some images are missing alt text.** Mostly older ones. This site has been publishing since 2003 and has been through several eras of WordPress, and a lot of that archive was written before I knew better. Recent posts are in better shape than old ones. If an image matters to a post and has no description, email me the URL and I will describe it for you.

**Hover and focus states are inconsistent.** On some pages it is not obvious which link or button you have currently selected with the keyboard. I am working through this site-wide rather than patching it page by page.

**Mobile and small-screen behaviour has not been fully checked.** The site is built to reflow, but I have not done a complete keyboard and zoom pass on phones and tablets. If something overlaps, gets cut off, or cannot be reached on your device, tell me what device it is.

**Older posts vary.** Heading structure, formatting, embedded video, and old media are inconsistent across two decades of archive. Some old video embeds have no captions or transcripts. If you need a transcript for something, ask — if one exists I will send it, and if it does not I will tell you that honestly.

**Embedded things from elsewhere.** The newsletter signup, video players, and other third-party embeds are not built by me and I cannot fully control how accessible they are. Everything important on this site is also available as plain text on the page itself.

## Tell me when something is broken

Seriously — please do. I cannot fix what I do not know about, and a full audit has not happened yet, so reports from real people are currently the best signal I have.

- **[Use the contact page](https://kriskrug.co/contact/)**, or
- **email me directly at [feelmoreplants@gmail.com](mailto:feelmoreplants@gmail.com)** — put "Accessibility" in the subject line so it does not get buried.

If you can, include:

- the page you were on;
- what you were trying to do;
- what got in the way;
- what you are using — browser, phone, screen reader, voice control, whatever. Only if you are comfortable sharing it.

You do not owe me a technical bug report. "The text on this page is unreadable" is a completely useful message.

I will read every one of these. **[KK: reply-time commitment — either state a real window you will actually meet, e.g. "I aim to reply within X business days", or delete this sentence entirely. Do not publish an SLA you will miss.]**

## If you need something in another format

If there is something on this site you cannot get to, ask me for it directly and I will find another way to get it to you — a plain-text version, a description of an image, a transcript, or just the answer in an email. That offer is open regardless of whether I have fixed the underlying problem yet.

## If I do not fix it

If you report a barrier and I do not resolve it, email me again and say so, and I will treat it as a priority rather than a ticket. **[KK: decide whether to name a formal escalation route here — e.g. the BC Human Rights Tribunal — or leave this as the informal path. Do not name any body or representative that has not actually agreed to that role.]**

## What I am working on next

In rough priority order:

1. Fixing the contrast and skip-link problems above.
2. A proper keyboard and focus pass across every page, not just the ones I happen to check.
3. A full mobile and zoom review.
4. Alt text — new images first, then working backwards through the archive that people actually read.
5. A complete audit across every public page rather than the handful I currently sample.

No dates on those, because I would rather do them than promise them.

## How the site is built and tested

- WordPress, with a theme I build and maintain myself.
- Standard HTML — headings, lists, links, and images, not custom widgets — wherever I can manage it.
- Reference standard: **WCAG 2.1 Level AA**.

Testing so far has been **self-evaluation**: automated accessibility scans on a handful of the most-visited pages, plus manual spot checks. That is not the same as an audit.

To be direct about the gaps: nobody has tested this site with a screen reader. No professional accessibility review has been done. No testing has been done with disabled users. Those are all things that should happen, and none of them have.

## About this statement

Last reviewed: **[KK: publish date — replace with the real date this goes live, not the draft date]**

I will update this page when the site's theme changes significantly, when an audit is completed, when someone reports a barrier, or when I fix something listed above. If this page has gone stale, that is a bug too — tell me.
