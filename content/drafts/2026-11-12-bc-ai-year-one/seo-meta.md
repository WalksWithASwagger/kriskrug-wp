# SEO metadata

Status: draft. Fields marked "open" wait on `open-facts-for-kk.md`.

- Title: `The First 300` (question 8)
- Slug: `bc-ai-year-one` (question 6). `https://kriskrug.co/bc-ai-year-one/` returned 404 on 2026-11-13 03:13 UTC. That is not a slug check; the all-status authenticated check runs on the day of any write.
- Post date: open (question 6). Recommended: the real publish day in the week before the AGM, no backdating. `post_date` is left out of `post.md` on purpose.
- Canonical: open. With the recommended slug it becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/bc-ai-year-one/`.
- Meta title (49 characters): `BC + AI Year One: Zero to 300 Members | Kris Krüg`
- Meta description (129 characters): `One year in, BC + AI has 300+ members of the nonprofit. Here are the public numbers, the pricing lesson, and what changes at 300.`
- Excerpt (144 characters): `BC + AI is one year old and past 300 members. Here is the year in public numbers, the pricing lesson I paid for, and why 300 is a different job.`
- Category: `Vancouver AI Ecosystem`
- Tags: `bc ai`, `bc ai ecosystem`, `vancouver ai`, `Community Building`
- OG image: open (question 7). Recommended: a Michelle Diamond frame from the Meetup #32 gallery, credited, with her OK, through featured-image-forge crop QC and Kris's approval.

## Notes for the write

- The meta title, meta description and excerpt name no figure beyond 300 and no refund, price change, date or AGM detail, so they stay correct whichever way Kris answers questions 1 to 6.
- Jetpack SEO title and description persist through REST. The only character outside ASCII in these fields is the precomposed `ü` in Krüg, which is cp1252-safe and not a combining diacritic, so it avoids the known REST 500.
- Every field uses straight apostrophes. No em dashes, no en dashes.

## Taxonomy evidence (2026-11-13 03:13 UTC, public pages only)

No REST call was made, so term IDs are not recorded here. The names below are what the public archive pages show, and every archive returned 200.

| Package name | Public archive | Shown as |
|---|---|---|
| Vancouver AI Ecosystem | https://kriskrug.co/category/vancouver-ai-ecosystem/ | page title "Vancouver AI Ecosystem"; the category on Zero to One, AI Lands Inside Every Profession and Futureproof: Year One |
| bc ai | https://kriskrug.co/tag/bc-ai/ | page title "bc ai"; a tag on Zero to One |
| bc ai ecosystem | https://kriskrug.co/tag/bc-ai-ecosystem/ | page title "bc ai ecosystem"; a tag on AI Lands Inside Every Profession |
| vancouver ai | https://kriskrug.co/tag/vancouver-ai/ | page title "vancouver ai" |
| Community Building | https://kriskrug.co/tag/community-building/ | page title "Community Building"; a tag on Zero to One |

All five names slugify to their live slugs, so `ensure_term()` in `scripts/notion-to-wp/create_local_wp_draft.py` resolves each one by slug before it would ever create a term.

### The `BC + AI` tag trap

The site has two near-duplicate tags: `bc ai` (slug `bc-ai`) and `BC + AI` (slug `bc-ai-2`). `ensure_term()` looks up `slugify(name)` first, and `slugify("BC + AI")` is `bc-ai`. So putting `BC + AI` in this package's tags would silently attach the `bc ai` tag, never `BC + AI`. The package uses `bc ai` on purpose. If Kris wants the `BC + AI` tag as well, that is a separate, approved term edit after the draft exists, not a frontmatter change.
