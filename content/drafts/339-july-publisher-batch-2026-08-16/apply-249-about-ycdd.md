# #249 About backlink to You Can't Drink Data

**Verdict:** STILL OPEN
**Write target:** page `1208`, slug `about`, `https://kriskrug.co/about/`
**Link target:** post `11936`, slug `you-cant-drink-data` (read-only; do not PATCH this post)
**Live `modified`:** `2026-08-01T09:59:39` (refreshed; July handoff had `2026-07-01T11:33:51` then `2026-07-24T17:22:59`)
**REST + HTML:** 200 / self-canonical `/about/`
**Evidence:** public HTML count of `you can't drink data` is **0**. Count of `you-cant-drink-data` hrefs is **0**. The reserved paragraph is still present exactly once.

The August 1 About rewrite added a new hero and a new first bio sentence. The original July paragraph is still there as the next `<p>` and still has no class attribute.

## FIND (exact, count must be 1)

```html
<p>I have spent two decades documenting technology, art, activism, conferences, communities, and the back rooms where culture actually changes. These days, most of that work points at one question: how do we use AI to increase human capacity instead of flattening human judgment?</p>
```

## REPLACE

```html
<p>I have spent two decades documenting technology, art, activism, conferences, communities, and the back rooms where culture actually changes. These days, most of that work points at one question: how do we use AI to increase human capacity instead of flattening human judgment? That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in <a href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">you can't drink data</a>.</p>
```

New sentence (plain text): `That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in you can't drink data.`

ASCII apostrophe in `can't`. No em dash. No other About copy.

## Snapshot-first apply

1. `GET /wp-json/wp/v2/pages/1208?context=edit&_fields=id,slug,status,modified,title,content`
2. Save to `backup/<UTC>-july-publisher/before-page-1208-edit.json` plus public `https://kriskrug.co/about/` HTML and SHA-256.
3. Abort unless `id=1208`, `slug=about`, `status=publish`, and `modified=2026-08-01T09:59:39` (or a KK-acknowledged newer guard after a fresh needle reconfirm).
4. Abort unless FIND occurs exactly once in `content.raw`. Gutenberg wrappers around the `<p>` are fine; do not replace unrelated hero copy.
5. `POST /wp-json/wp/v2/pages/1208` with `{"content": ...}` only.
6. Readback: authenticated raw contains the new sentence once; cache-busted `/about/` grep for `you can't drink data` returns 1; YCDD URL still 200; page slug/title/status unchanged.

## Rollback

Re-POST snapshotted `content.raw` to page 1208, content key only, after confirming `modified` still equals the post-write value.
