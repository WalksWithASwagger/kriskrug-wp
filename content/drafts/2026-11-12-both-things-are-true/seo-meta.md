# SEO metadata

Status: scheduled as WordPress post 13004 for 2026-11-24 16:00 UTC (see `publish-gate.md`). Every field below is settled by Kris's 2026-11-12 rulings (`open-facts-for-kk.md`), and the readback matched each one.

- Title: `Both Things Are True` (question 7, default taken)
- Slug: `both-things-are-true` (question 4, ruled). `https://kriskrug.co/both-things-are-true/` returned 404 on 2026-11-13 00:47 UTC. That is not a slug check; the all-status authenticated check runs on the day of any write.
- Post date: the real publish day, no backdating (question 4, ruled). `post_date` is left out of `post.md` on purpose, so the staged draft floats its date until it is published.
- Canonical: `https://kriskrug.co/<yyyy>/<mm>/<dd>/both-things-are-true/`, using the publish date (question 4, ruled).
- Meta title (58 characters): `Both Things Are True: My AI Keynote in Writing | Kris Krüg`
- Meta description (152 characters): `The sentence my Both Hands Full keynote hangs on, the five fears it names, the third path it argues for, and how to bring the talk to your room in 2027.`
- Excerpt (160 characters): `Four minutes into my LaSalle keynote I said the sentence the whole talk hangs on. This is Both Hands Full in writing: the theft, the power, and why I hold both.`
- Category: `AI for Creatives`
- Tags: `Both Hands Full`, `Keynotes`, `speaking`, `taste`
- OG image: the featured image (question 5, ruled). The theme writes `og:image` from the featured image's `large` size, 1024x576 for these 16:9 frames. Kris approved LaSalle frame 10, media 11831, and it is set as the featured image on post 13004.

## Notes for the write

- The meta description and excerpt do not quote the LaSalle line, so they stay correct whichever wording Kris confirms in question 1.
- Jetpack SEO title and description persist through REST. The only character outside ASCII in these fields is the precomposed `ü` in Krüg, which is cp1252-safe and not a combining diacritic, so it avoids the known REST 500.
- Every field uses straight apostrophes. No em dashes, no en dashes.
- No meta field names a client, a fee, an audience size or a 2027 booking.

## Taxonomy evidence (2026-11-13 00:49 UTC, public pages only)

That first check made no REST call, so it recorded no term IDs; the term check below does. The names below are what the public archive pages show, and every archive returned 200.

| Package name | Public archive | Shown as |
|---|---|---|
| AI for Creatives | https://kriskrug.co/category/ai-creatives/ | category link text "AI for Creatives" on the Jan 24 post |
| Both Hands Full | https://kriskrug.co/tag/both-hands-full/ | page title "Both Hands Full" |
| Keynotes | https://kriskrug.co/tag/keynotes/ | page title "Keynotes" |
| speaking | https://kriskrug.co/tag/speaking/ | page title "speaking" |
| taste | https://kriskrug.co/tag/taste/ | tag link text "taste" on Your Taste Is Your Moat |

`ensure_term()` in `scripts/notion-to-wp/create_local_wp_draft.py` matches a name to an existing term by `slugify(name)` or by a case-insensitive name match. `AI for Creatives` slugifies to `ai-for-creatives`, but the live category slug is `ai-creatives`, so it can only resolve by name. On the day of the write, confirm by read-only REST that the live category name decodes to exactly `AI for Creatives`. If it does not, stop, because `--execute` would create a new category.

## Term check (2026-11-13 02:59 to 03:00 UTC, logged-out public REST)

Same `ensure_term()` rule. `slugify()` output comes from `scripts/notion-to-wp/notion_client.py`.

| Package name | `slugify()` | Live term | Resolves |
|---|---|---|---|
| AI for Creatives | `ai-for-creatives` | category 1665 `AI for Creatives`, slug `ai-creatives` | yes, by name only: `categories?slug=ai-for-creatives` returns nothing, and `categories?search=AI for Creatives` returns 1665 with the exact name |
| Both Hands Full | `both-hands-full` | tag 1683 `Both Hands Full` | yes |
| Keynotes | `keynotes` | tag 1696 `Keynotes` | yes |
| speaking | `speaking` | tag 89 `speaking` | yes |
| taste | `taste` | tag 1667 `taste` | yes |

No new term would be created. This is dated evidence and has to be rerun on the day of any write.
