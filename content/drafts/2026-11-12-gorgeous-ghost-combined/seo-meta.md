# SEO metadata

Status: staged as WordPress draft 13003, not scheduled yet (see `publish-gate.md`). Every field below is settled by Kris's 2026-11-12 rulings (`open-facts-for-kk.md`), and the draft's readback matched each one.

- Title: `I Made a Gorgeous Ghost` (question 10, default taken)
- Slug: `gorgeous-ghost` (question 2, ruled)
- Post date: the real publish day in the Nov 19 to 30 window, no backdating (question 1, ruled). `post_date` is left out of `post.md` on purpose, so the staged draft floats its date until it is published.
- Canonical: `https://kriskrug.co/<yyyy>/<mm>/<dd>/gorgeous-ghost/`, using the publish date (question 2, ruled).
- Meta title (35 characters): `I Made a Gorgeous Ghost | Kris Krüg`
- Meta description (155 characters): `Gorgeous Ghost is a 69.42-second glam space opera made with The Scallywags for the BC + AI Film Club: one locked song, one colour move, one signal machine.`
- Excerpt (170 characters): `Gorgeous Ghost is a 69.42-second glam space opera I made with The Scallywags for the BC + AI Film Club. The band, the locked song, the colour move and the signal machine.`
- Category: `Creative Technology & Making` (ID 1755)
- Tags: `Gorgeous Ghost` (1804), `Creative AI` (1682), `AI Film Club` (1785), `AI Music` (1395, live name `ai music`)
- Featured flag: `true`, carried over from the #771 package
- OG image: the featured image (question 7, ruled). The theme writes `og:image` from the featured image's `large` size, 1024x576 for a 16:9 master. Kris approved the film's reveal art as a 1600x900 master; it is not uploaded yet (see `publish-gate.md`). Alt text is in `alt-text.md`.

## Notes for the write

- Jetpack SEO title and description persist through REST. The only character outside ASCII in these fields is the precomposed `ü` in Krüg, which is latin1-safe and not a combining diacritic, so it avoids the known REST 500.
- Every field uses straight apostrophes. No em dashes, no en dashes.
- No meta field claims a release month, a premiere date or a tool name.

## Term check (2026-11-12 21:21 UTC, public REST)

Rule from `ensure_term()` in `scripts/notion-to-wp/create_local_wp_draft.py` (lines 249 to 258 on `main` at `e66f72a`): a name resolves when an existing term's slug equals `slugify(name)` or the term's name matches ignoring case. REST names were HTML-decoded first.

| Package name | `slugify()` | Live term | Resolves |
|---|---|---|---|
| Creative Technology & Making | `creative-technology-making` | 1755 `Creative Technology &amp; Making` | yes, by slug |
| Gorgeous Ghost | `gorgeous-ghost` | 1804 `Gorgeous Ghost` | yes |
| Creative AI | `creative-ai` | 1682 `Creative AI` | yes |
| AI Film Club | `ai-film-club` | 1785 `AI Film Club` | yes |
| AI Music | `ai-music` | 1395 `ai music` | yes, by slug and case-insensitive name |

No new term would be created. This is dated evidence and has to be rerun on the day of any write.

Rerun 2026-11-13 02:59 UTC, logged-out public REST (`categories?slug=...` and `tags?slug=...`): the same five IDs came back with the same slugs, and `slugify()` from `scripts/notion-to-wp/notion_client.py` gives the slugs in the table. All five still resolve by slug.
