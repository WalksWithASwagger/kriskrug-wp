# SEO metadata

Status: draft. Fields marked "open" wait on `open-facts-for-kk.md`.

- Title: `I Made a Gorgeous Ghost` (question 10)
- Slug: `gorgeous-ghost` (question 2)
- Post date: open (question 1). Recommended: the real publish day, no backdating. `post_date` is left out of `post.md` on purpose.
- Canonical: open. With the recommended slug it becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/gorgeous-ghost/`, using the publish date.
- Meta title (35 characters): `I Made a Gorgeous Ghost | Kris Krüg`
- Meta description (155 characters): `Gorgeous Ghost is a 69.42-second glam space opera made with The Scallywags for the BC + AI Film Club: one locked song, one colour move, one signal machine.`
- Excerpt (170 characters): `Gorgeous Ghost is a 69.42-second glam space opera I made with The Scallywags for the BC + AI Film Club. The band, the locked song, the colour move and the signal machine.`
- Category: `Creative Technology & Making` (ID 1755)
- Tags: `Gorgeous Ghost` (1804), `Creative AI` (1682), `AI Film Club` (1785), `AI Music` (1395, live name `ai music`)
- Featured flag: `true`, carried over from the #771 package
- OG image: open (question 7). Recommended: a hosted 16:9 featured image from Kris's own film master, through featured-image-forge crop QC and his approval. If he keeps the external share image instead, its source is `https://gorgeousghost.com/og/share.jpg` and its alt text is in `alt-text.md`.

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
