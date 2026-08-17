# #342 Both Hands Full href-only repair

**Verdict:** STILL OPEN
**Write target:** post `11171`, slug `both-hands-full`, `https://kriskrug.co/2026/01/24/both-hands-full/`
**Live `modified`:** `2026-08-10T18:24:39` (refreshed; July handoff had `2026-06-28T20:26:51`)
**Evidence:** the exact closing sentence still uses the retired Notion keynote URL. Public `content.rendered` has **1** Notion href and **0** `bothhandsfull.com` hrefs. A different body link uses anchor `Both hands full` pointing at `/2026/05/16/make-culture-not-content/`. Do not conflate those.

External checks at capture time: `https://www.bothhandsfull.com` returns 200 with self-canonical `https://www.bothhandsfull.com`. The Notion URL still returns 200, so this is canonical routing, not a broken-link emergency.

Related confirm issue #736 is a separate KK gate. This payload is the #339/#342 href replacement only.

## FIND (exact, count must be 1)

```html
<a href="https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link">both hands full</a>
```

Rendered paragraph (NCR apostrophe as stored in HTML):

```html
<p class="wp-block-paragraph">So I&#8217;m asking you to walk forward with <a href="https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link">both hands full</a>.</p>
```

Prefer the short FIND above. It is unique in the body and survives raw-vs-rendered apostrophe differences. If `content.raw` uses a unicode apostrophe in `I'm` instead of `&#8217;`, the `<a href=...>` snippet still matches.

## REPLACE

```html
<a href="https://www.bothhandsfull.com">both hands full</a>
```

No `rel`. No sentence change. No title, slug, excerpt, or other href changes. Leave the `Both hands full` -> make-culture link alone.

## Snapshot-first apply

1. `GET /wp-json/wp/v2/posts/11171?context=edit&_fields=id,slug,status,modified,title,content`
2. Save to `backup/<UTC>-july-publisher/before-post-11171-edit.json` plus public HTML and SHA-256.
3. Abort unless `id=11171`, `slug=both-hands-full`, `status=publish`, and `modified=2026-08-10T18:24:39` (or a KK-acknowledged newer guard after reconfirming the Notion href is still present once).
4. Abort unless FIND occurs exactly once in `content.raw` and `bothhandsfull.com` count is 0.
5. `POST /wp-json/wp/v2/posts/11171` with `{"content": ...}` only.
6. Readback: Notion keynote href count 0; `https://www.bothhandsfull.com` appears once with anchor `both hands full`; post still 200 and self-canonical; `www.bothhandsfull.com` still 200.

## Rollback

Re-POST snapshotted `content.raw` to post 11171, content key only.
