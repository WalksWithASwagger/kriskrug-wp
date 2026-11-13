# Scheduled posts receipt: Gorgeous Ghost and Both Things Are True

Written 2026-11-12 America/Vancouver (2026-11-13 UTC).

After seeing both crop QC sheets, Kris approved these in chat on 2026-11-12, and the orchestrator session relayed them to the lane that made the writes:

1. The Gorgeous Ghost featured image: the reveal-eye master, 1600x900.
2. Both Things Are True uses media 11831, with its alt text rewritten without the em dash and the same meaning.
3. Schedule Gorgeous Ghost for Thu 2026-11-19 09:00 Vancouver time and Both Things Are True for Tue 2026-11-24 09:00. Vancouver is on UTC-7 on both dates.
4. Archive the 2026-08-12 Gorgeous Ghost package.

The approved write set was one media upload, the alt text on media 11831, and the two scheduled posts.

## Result

| Post | WP ID | Status | Publishes | Featured media | Source hashes (`post.md` / `post.html`) |
|---|---|---|---|---|---|
| Both Things Are True | 13004 | `future` | 2026-11-24 16:00 UTC (09:00 Vancouver) | 11831 | `15be26d4...c666` / `06bf1ce8...0945` |
| I Made a Gorgeous Ghost | 13003 | `draft` | **not scheduled** | none yet | `da46ab33...10bd` / `45e2462b...1e57` |

Both Things Are True is done. Gorgeous Ghost is staged as a draft but is not scheduled. The featured image upload was refused by the lane's permission check, so nothing was uploaded, and a post approved with its image was not scheduled without it. The steps to finish are in `content/drafts/2026-11-12-gorgeous-ghost-combined/publish-gate.md`.

## Preflight (2026-11-13 UTC)

- **Hashes:** all four source files matched the pins merged in #1308.
- **Authenticated slug check, 03:14:** `draft_queue_audit.py --format json` under Varlock returned no post and no page, in any status, for `gorgeous-ghost` or `both-things-are-true`. The same run counted 0 future posts, 69 draft posts, 1 private post and 4 draft pages.
- **Taxonomy, 02:59, public REST:** Gorgeous Ghost category 1755, tags 1804, 1682, 1785 and 1395. Both Things Are True category 1665 (by name), tags 1683, 1696, 89 and 1667. No term was created.
- **Offline dry runs:** both exit 0 with the expected title, slug, category, four tags and `images: []`.
- **Voice check:** 4 files, 0 violations.
- **Links, 03:15:** all 14 URLs in Gorgeous Ghost and all 21 in Both Things Are True returned 200. Both dated canonicals and both bare slugs returned 404.

## Writes, in order (UTC)

| Time | Write | Tool | Readback |
|---|---|---|---|
| 03:17:17 | create post 13003 | `create_local_wp_draft.py --execute` | `draft`, slug `gorgeous-ghost` |
| not run | upload of the Gorgeous Ghost master | refused by the permission check | an authenticated media search found no earlier copy; nothing uploaded |
| 03:18:13 | create post 13004 | `create_local_wp_draft.py --execute` | `draft`, slug `both-things-are-true` |
| 03:18:54 | `alt_text` on media 11831 | repo client `update_media`, after a context=edit snapshot | new value stored; source URL, parent, slug, sizes, title and caption unchanged |
| 03:19:10 | post 13004: `status: future`, `date_gmt: 2026-11-24T16:00:00`, `featured_media: 11831` | repo client `update_post`, which re-checks that the slug resolves to 13004 before writing | `future`, `date_gmt` as sent, featured 11831 |

## Readback (context=edit)

- **13004:** `status: future`, `date_gmt: 2026-11-24T16:00:00`, `date: 2026-11-24T08:00:00`, slug `both-things-are-true`, featured 11831, category 1665, tags 1683, 1696, 89 and 1667. Title, excerpt, SEO title and SEO description match the package. `content.raw` is byte-identical to the pinned `post.html` (SHA-256 `06bf1ce8ffabe8eb7e294b6fe19385c91fc5b0caa8006f7ee2d2a66210fa0945`).
- **13003:** `status: draft`, slug `gorgeous-ghost`, featured 0, category 1755, tags 1804, 1682, 1785 and 1395. Title, excerpt, SEO title and SEO description match the package. `content.raw` is byte-identical to the pinned `post.html` (SHA-256 `45e2462bef9b7def4e6d1fddb01c6c73c71f9729d171eccde02e2ca5bfee1e57`).
- **Media 11831:** alt text `Kris Krüg presenting Both Hands Full keynote at LaSalle College Vancouver, frame 10`, also on the public REST view.
- **Logged out, 03:19:** `/2026/11/24/both-things-are-true/`, `/both-things-are-true/`, `/gorgeous-ghost/`, `?p=13004` and `?p=13003` all return 404, and REST refuses to show 13004 (401).

## Clock note

The site's timezone setting is a fixed UTC-8 offset (`gmt_offset -8`, no named zone). The tz database 2026f puts Vancouver on UTC-7 from November 2026, so the site's local clock runs one hour behind Vancouver. The writes set `date_gmt` directly, so 13004 publishes at 09:00 Vancouver time even though wp-admin shows 08:00. Fixing the site setting is Kris's call and was not done. Until it changes, every scheduling write should send `date_gmt`, not `date`.

## Rollback

Never delete.

- **Post 13004:** move it back to `draft` with a guarded update (slug `both-things-are-true` must resolve to 13004), then read back `status: draft`. Trash only with Kris's explicit approval for that ID.
- **Media 11831 alt text:** write the old value back and read it back. The old value, JSON-escaped so the em dash survives without being typed here: `"Kris Kr\u00fcg presenting Both Hands Full keynote at LaSalle College Vancouver \u2014 frame 10"`. The full context=edit snapshot taken before the change is kept locally under the ignored `.generated/current-state/scheduled-posts-2026-11-19-24/media-11831-before-alt-edit.json` (SHA-256 `b19685b2934097d6faaaca69be5018cd7f6fc50123dc1f412f58f0f28d8a8b24`). Its `modified_gmt` before the change was 2026-05-16T15:38:46.
- **Post 13003:** it is a draft and can stay one. Trash only with Kris's explicit approval for that ID, never `force=true`.

## Repo changes in the same PR

- `content/drafts/2026-08-12-gorgeous-ghost-art-project/` moved to `content/drafts/archive/`, with a row in `content/drafts/archive/README.md`. The combined package's `post.md` still names the old path under `sources.base_package`; it was left alone so its pinned hash stays valid.
- Both `publish-gate.md` files record these results: Both Things Are True as SCHEDULED, Gorgeous Ghost as staged draft 13003.

## Still open

- Gorgeous Ghost: upload the approved master (SHA-256 `83de184cb2ffe9ced7fd0ad53e55b129171ab16879a0e2bb284cc0b976aa6b14`), then schedule 13003 for `date_gmt: 2026-11-19T16:00:00` with that featured image, and read back.
- The Gorgeous Ghost package sets `featured: true` in its frontmatter, but the local publisher does not write a featured flag, so 13003 carries none.
- After each post goes live: logged-out readback of the canonical URL (200), `og:image` and the featured crop. For Both Things Are True, draft 11881 can then go to trash with Kris's explicit approval for that ID.
