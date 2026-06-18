# Issue #233: Homepage Metadata and Striking-Distance Links

**Track:** A - Content + SEO
**Status:** repo-side review handoff; no live WordPress writes
**Control surface:** GitHub issue #233

## Scope

This file turns the June 17 Search Console/GA4 signals into a review-ready repo
handoff. It does not deploy metadata, publish posts, edit WordPress, or create
REST payloads.

## Existing Repo Evidence

| Surface | Source | Finding |
|---|---|---|
| Homepage metadata | `content/source-packs/keynotes-2026/wp-payloads/page-meta.json` | Canonical repo payload already contains the tightened homepage title and description for review. |
| Meta description context | `fixes/issue-36-meta-descriptions.md` | Jetpack is the existing metadata owner; do not introduce Yoast, Rank Math, SEOPress, Code Snippets, or a second generator for this pass. |
| Search Console handoff | `fixes/issue-198-search-console-striking-distance-links-2026-06-18.md` | June 17 query clusters were `you cant drink data`, `david zabowski nerdwallet mobile engineering`, and `lord of the rings drinking game`. |
| Article target | `content/drafts/2026-05-23-you-cant-drink-data/` | Local draft package has SEO metadata and post-publish internal-link notes. |

## Review-Ready Homepage Metadata

Use the existing Jetpack SEO owner only. Both values are already present in
`page-meta.json`; no repo JSON change is needed.

- `jetpack_seo_html_title`: `Kris Krüg | AI Keynote Speaker & Creative Technologist`
- `advanced_seo_description`: `Kris Krüg is an AI keynote speaker and creative technologist building community-first tools, talks, training, and media across BC+AI and Both Hands Full.`

Do not include a `title` field in any future REST update payload unless KK
explicitly confirms a page-title change. This handoff is about SEO metadata,
not the visible WordPress page title.

## Query Disposition

| Query cluster | Disposition | Next safe action |
|---|---|---|
| `you cant drink data` | Use `content/drafts/2026-05-23-you-cant-drink-data/` as the target. | After the article and companion protest posts are live, add contextual backlinks from the two companion posts and one relevant homepage/About/hub surface if the surrounding copy fits. |
| `david zabowski nerdwallet mobile engineering` | No repo-local KrisKrug.co target found in the existing handoff. | Do not create or link anything until the target is confirmed as an existing page, quote, testimonial, media mention, or irrelevant people-search artifact. |
| `lord of the rings drinking game` | Park as legacy/low-strategy traffic. | Ignore unless KK confirms an entertainment/archive business reason to refresh, redirect, or noindex it. |

## Suggested Anchors

- `you can't drink data`
- `Vancouver AI protest`
- `data centre protest`
- `cleaner AI infrastructure`

Use one strong contextual link from a relevant surface instead of repeating an
exact-match anchor across unrelated pages.

## Review Checklist

- [ ] Homepage metadata values above still match `page-meta.json`.
- [ ] The `You Can't Drink Data` draft package remains the correct target for
      the Search Console query.
- [ ] No live WordPress writes are made from this repo-only handoff.
- [ ] Any future deployment uses Jetpack SEO fields only and includes public
      HTML readback for title, description, canonical, and robots meta.
