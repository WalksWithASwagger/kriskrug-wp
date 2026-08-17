# #335 LOTR search fields and 2004 footer pair

**Verdict:** STILL OPEN
**SEO write target:** post `35`, slug `the-lord-of-the-rings-drinking-game`
**Footer pair:** posts `35` and `58` (`mcsweeneys-lists`)
**Live titles:** `The Lord of the Rings Drinking Game | Kris Krüg` and `McSweeney's Lists | Kris Krüg`
**Evidence:** approved search title `...: 4 Original Rules` is absent. Public description is still the excerpt opener, not the approved rules summary. Both collection footers still recommend the 2023 AI companions post.

Live REST now exposes `jetpack_seo_html_title` and `advanced_seo_description` on posts (Aurora 1.6.5, `inc/seo-meta-rest.php`). Both keys on post 35 are already non-empty, so this is an **overwrite**, not an additive backfill.

Do not change the public post title, excerpt, slug, date, or taxonomies.

## A. SEO fields (post 35)

Use [`seo-meta-overwrite.json`](seo-meta-overwrite.json).

| Field | Live now | Approved overwrite |
|---|---|---|
| `jetpack_seo_html_title` | `The Lord of the Rings Drinking Game \| Kris Krüg` | `The Lord of the Rings Drinking Game: 4 Original Rules` |
| `advanced_seo_description` | excerpt opener about Return of the King | `Four original Lord of the Rings drinking game rules for Frodo, Sam, Legolas, and cliff falls, plus a trilogy marathon option. Play responsibly.` |

Modified guard: `2026-06-14T22:30:33`

Dry-run:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/seo-backfill/backfill_meta.py \
  --from-file content/drafts/339-july-publisher-batch-2026-08-16/seo-meta-overwrite.json \
  --kind post
```

No `--execute` until snapshot + KK overwrite tick. Apply the post 35 object first, then 8802 from the same file as part of #336.

Public readback after write: document title becomes the approved search title (theme uses the meta value as the full `<title>`). Standard and OG descriptions should pick up the new description on current 1.6.5 output. Confirm on a cache-busted fetch; do not assume 1.3.39 zip behavior.

## B. Footer pair

Identical live footer on both posts:

```html
<p class="kk-collection-footer wp-block-paragraph">Part of the <a href="https://kriskrug.co/category/web-early-blog/">Web and Early Blog archive</a> collection. See also: <a href="https://kriskrug.co/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/">Building AI Companions w/ John Anthony Hartman of IHAVEROBOTS</a>.</p>
```

Keep the category archive link. Replace only the "See also" destination.

### Post 35 FIND

```html
See also: <a href="https://kriskrug.co/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/">Building AI Companions w/ John Anthony Hartman of IHAVEROBOTS</a>.
```

### Post 35 REPLACE

```html
See also: <a href="https://kriskrug.co/2004/07/16/mcsweeneys-lists/">McSweeney's Lists</a>.
```

Modified guard: `2026-06-14T22:30:33`. Expected FIND count: 1. Expected LOTR->McSweeney's href count before: 0.

### Post 58 FIND

Same FIND string as post 35.

### Post 58 REPLACE

```html
See also: <a href="https://kriskrug.co/2004/05/27/the-lord-of-the-rings-drinking-game/">The Lord of the Rings Drinking Game</a>.
```

Modified guard: `2026-06-14T22:29:25`. Expected FIND count: 1. Expected McSweeney's->LOTR href count before: 0.

ASCII apostrophe in `McSweeney's`. No em dash. Do not add `rel`.

## Snapshot-first apply

1. Snapshot posts 35 and 58 (edit JSON + public HTML + SHA-256) before any write.
2. SEO overwrite on 35 first (`meta` only). Readback title/description.
3. Then content-only footer PATCH on 35, then 58.
4. Abort if FIND count is not 1 in `content.raw`, or if ID/slug/status/modified drifted.
5. Public readback: each footer points at the other 2004 post once; AI companions "See also" is gone from both; category archive link remains.

## Rollback

Restore prior `meta` values recorded in the overwrite dry-run `old` map, then re-POST each snapshotted `content.raw`.
