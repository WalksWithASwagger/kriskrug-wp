# SEO metadata

Status: draft. Fields marked "open" wait on `open-facts-for-kk.md`.

- Title: `Both Things Are True` (question 7)
- Slug: `both-things-are-true` (question 4). `https://kriskrug.co/both-things-are-true/` returned 404 on 2026-11-13 00:47 UTC. That is not a slug check; the all-status authenticated check runs on the day of any write.
- Post date: open (question 4). Recommended: the real publish day, no backdating. `post_date` is left out of `post.md` on purpose.
- Canonical: open. With the recommended slug it becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/both-things-are-true/`.
- Meta title (58 characters): `Both Things Are True: My AI Keynote in Writing | Kris Krüg`
- Meta description (152 characters): `The sentence my Both Hands Full keynote hangs on, the five fears it names, the third path it argues for, and how to bring the talk to your room in 2027.`
- Excerpt (160 characters): `Four minutes into my LaSalle keynote I said the sentence the whole talk hangs on. This is Both Hands Full in writing: the theft, the power, and why I hold both.`
- Category: `AI for Creatives`
- Tags: `Both Hands Full`, `Keynotes`, `speaking`, `taste`
- OG image: open (question 5). Recommended: an existing LaSalle keynote frame from the media library, through featured-image-forge crop QC and Kris's approval.

## Notes for the write

- The meta description and excerpt do not quote the LaSalle line, so they stay correct whichever wording Kris confirms in question 1.
- Jetpack SEO title and description persist through REST. The only character outside ASCII in these fields is the precomposed `ü` in Krüg, which is cp1252-safe and not a combining diacritic, so it avoids the known REST 500.
- Every field uses straight apostrophes. No em dashes, no en dashes.
- No meta field names a client, a fee, an audience size or a 2027 booking.

## Taxonomy evidence (2026-11-13 00:49 UTC, public pages only)

No REST call was made, so term IDs are not recorded here. The names below are what the public archive pages show, and every archive returned 200.

| Package name | Public archive | Shown as |
|---|---|---|
| AI for Creatives | https://kriskrug.co/category/ai-creatives/ | category link text "AI for Creatives" on the Jan 24 post |
| Both Hands Full | https://kriskrug.co/tag/both-hands-full/ | page title "Both Hands Full" |
| Keynotes | https://kriskrug.co/tag/keynotes/ | page title "Keynotes" |
| speaking | https://kriskrug.co/tag/speaking/ | page title "speaking" |
| taste | https://kriskrug.co/tag/taste/ | tag link text "taste" on Your Taste Is Your Moat |

`ensure_term()` in `scripts/notion-to-wp/create_local_wp_draft.py` matches a name to an existing term by `slugify(name)` or by a case-insensitive name match. `AI for Creatives` slugifies to `ai-for-creatives`, but the live category slug is `ai-creatives`, so it can only resolve by name. On the day of the write, confirm by read-only REST that the live category name decodes to exactly `AI for Creatives`. If it does not, stop, because `--execute` would create a new category.
