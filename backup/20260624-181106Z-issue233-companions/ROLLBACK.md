# Rollback note — #233 companion publish (2026-06-24 18:11:06Z)

Snapshots captured **before** any write, via authenticated WP REST `context=edit`:
- `post-11882.edit.json` — status `draft`, slug `both-hands-full-vancouver-ai-march-2026`, title "We Trained AI On Stolen Work. I Am More Creative Than Ever.", featured_media 12370, date 2026-05-19T12:00:00
- `post-11929.edit.json` — status `draft`, slug `data-center-protest-signs`, title "Both Hands Full at the Data Center…", featured_media 11919, date 2026-05-23T12:00:00
- `post-11936.edit.json` — status `publish` (LIVE), slug `you-cant-drink-data`, title "You Can't Drink Data" — backup only; minor backlink edit planned

## Planned live writes this session
1. **11882**: slug `both-hands-full-vancouver-ai-march-2026` → `we-trained-ai-on-stolen-work`; status `draft` → `publish`. No `title` field in payload.
2. **11929**: status `draft` → `publish`. Body edit: replace internal link `/2026/05/19/both-hands-full-vancouver-ai-march-2026/` → `/2026/05/19/we-trained-ai-on-stolen-work/`.
3. **11936**: add one contextual backlink to 11882 (new slug). Otherwise untouched.

## To roll back
Re-PATCH each post from its snapshot JSON. Specifically:
- 11882: set `status:"draft"`, `slug:"both-hands-full-vancouver-ai-march-2026"`.
- 11929: set `status:"draft"`, restore `content.raw` from `post-11929.edit.json`.
- 11936: restore `content.raw` from `post-11936.edit.json`.
Then purge Pagely page cache for each affected URL.

## Guardrails honored
Slug-idempotency verified by ID+title before write. Jetpack remains the single SEO owner. No `title` field sent. Pagely purge + logged-out readback after each write.
