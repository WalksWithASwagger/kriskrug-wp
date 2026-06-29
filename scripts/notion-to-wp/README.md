# Notion → kriskrug.co publisher

A small connector CLI that pulls a Notion page from KK's "News & Content Database" and posts it to kriskrug.co as a WordPress draft. Purpose-built for this site only — not portable, no plugins to install, no admin UI to maintain.

## What it does

1. Fetches a Notion page via the Notion API (using KK's existing `NOTION_TOKEN`).
2. Converts Notion blocks into Gutenberg core-block HTML (paragraph, heading, list, quote, callout, image, code, separator, mark).
3. Downloads embedded images from Notion's expiring S3 URLs into `content/drafts/<slug>/images/`.
4. Drafts an SEO-prepped post locally (`content/drafts/<slug>/post.md` + `post.html` + `seo-meta.md` + `alt-text.md` + `internal-links.md`).
5. In live mode: uploads each image to `kriskrug.co`'s Media Library (alt text set), rewrites image URLs, then sends the post body to `/wp-json/wp/v2/posts`. Default status is `draft`; `--publish` sets `status=publish`.
6. Records the WP post ID + edit URL in `content/drafts/<slug>/publish.log`.

It does NOT inject schema. The `kk-schema` mu-plugin handles that sitewide. The connector just sets the fields the mu-plugin needs (featured_media, categories, tags, excerpt).

## Prerequisites

### 1. Notion token

Already set up. Lives at `/Users/kk/Code/notion-local/kk-ai-ecosystem/.env` as `NOTION_TOKEN=secret_…`. The script reads it automatically.

### 2. WordPress Application Password

Generate one **once**:

1. Open https://kriskrug.co/wp-admin/profile.php
2. Scroll to **Application Passwords** (near the bottom of the page).
3. Application Name: `kk-notion-to-wp`
4. Click **Add New Application Password**.
5. WordPress shows the password ONCE — copy it immediately into the local `.env`. Do not paste it into docs, issues, commits, or chat.
6. Paste it into `scripts/notion-to-wp/.env` (copy from `.env.example`):

```bash
cp scripts/notion-to-wp/.env.example scripts/notion-to-wp/.env
$EDITOR scripts/notion-to-wp/.env
# fill in WP_USER and WP_APP_PASSWORD
```

If you ever lose it, just revoke and regenerate — no password recovery in WP.

### 3. Python deps

```bash
cd scripts/notion-to-wp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Dry-run: writes content/drafts/<slug>/, prints REST payload, does NOT post
python kk_notion_to_wp.py --dry-run https://www.notion.so/<page-id>

# Dry-run with an explicit category decision
python kk_notion_to_wp.py --dry-run --category "AI Ethics & Philosophy" https://www.notion.so/<page-id>

# Live: also uploads images, creates a DRAFT post on kriskrug.co
python kk_notion_to_wp.py https://www.notion.so/<page-id>

# Live + publish immediately
python kk_notion_to_wp.py --publish https://www.notion.so/<page-id>

# Live update of an existing slug, guarded by title similarity
python kk_notion_to_wp.py --update https://www.notion.so/<page-id>

# No-write update review: fetches the existing slug target and prints a diff
python kk_notion_to_wp.py --diff https://www.notion.so/<page-id>
```

## Local draft package publisher

Use `create_local_wp_draft.py` when the reviewed package already exists under
`content/drafts/...` and `post.html` is the canonical Gutenberg body. This
path does not fetch Notion, defaults to dry-run, refuses post/page slug
collisions, uploads package images with alt text, rewrites local image paths to
WP media URLs, and creates only a WordPress `draft` when `--execute` is passed.
If a retry happens after media upload, it reuses media IDs already recorded in
`publish.log`.

```bash
# Validate slug availability and payload shape; no WordPress writes.
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/<date-slug>/post.md

# Explicit create-only WP draft run.
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/<date-slug>/post.md --execute
```

## Draft queue audit

Before promoting anything from the WordPress draft pile, refresh the read-only queue audit:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py
```

The audit reports live WP draft/future/pending/private counts, local `content/drafts/` package metrics, exact slug matches across published and draft posts/pages, and draft quality signals. It does not create, update, schedule, or publish anything.

Use `--local-only` when WordPress credentials are unavailable:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --local-only
```

## Live-write safety checks

2026-05-22 operating stance: the strict backup/restore proof gate is retired. The connector can create drafts and publish/update intentionally, but every live run must still be boringly explicit about target, intent, and rollback path.

Create-only draft runs are allowed when all of these are true:

1. A dry-run package has been reviewed in `content/drafts/<slug>/`.
2. The target slug is verified as a create-only draft target; do not pass `--update`.
3. The title, category, tags, excerpt, and create intent are verified.
4. For `Type=Feature`, the category is intentional: either the tags route it clearly or `--category` is passed.
5. The run keeps WordPress status as `draft`; do not pass `--publish`.
6. Media uploads are approved and have alt text, or the draft is image-free.
7. The resulting WP post ID, edit URL, and run notes are recorded in `publish.log`.

Public publish or `--update` runs require explicit KK sign-off, a fresh dry-run/review, authenticated slug/ID/status verification, and a rollback note. For updates, run `--diff` first and review the emitted diff before any `--update` command. `--diff` fetches the existing post by slug, applies the same title-similarity guard as `--update`, and exits before WordPress create/update/media/taxonomy write requests. Bulk edits, destructive cleanup, plugin/theme/schema/robots changes, and media-heavy imports need a narrower deploy plan before they run.

Without WordPress credentials the command is always effectively dry-run only.

## Notion property mapping

KK's "News & Content Database" has these properties; the connector reads them:

| Notion property | WP field | Notes |
|---|---|---|
| Title | post title | required |
| AI summary | excerpt (→ meta description) | falls back to Summary if absent |
| Tags | tags | auto-created if missing |
| Type | category routing | Known types map directly; `Feature` uses tag hints or requires `--category`; unknown types fall back to "Misc" only for non-Feature content. |
| Featured | post meta `kk_featured` | "YES" sets it |
| Status | publish context | recorded from Notion, but not a publish gate |
| Publication Date | post date | if absent, uses today |
| Author / Owner | post author | mapped to WP user ID 1 (kk) for now |

## Idempotency

The 2026-05-15 incident proved that Notion-ID meta lookups are not safe unless the meta key is registered with `show_in_rest`. The connector now uses **slug-based lookup** for identity checks.

Default behavior is CREATE-only:

- If no post with the slug exists, the connector creates a new WP post.
- If a post with the slug already exists, the connector aborts instead of silently updating.
- To update an existing post, pass `--update`. The update path also checks that the existing title is similar to the new title before it sends a REST update. The current threshold lives in `TITLE_SIMILARITY_UPDATE_THRESHOLD` and is covered by tests.
- Before using `--update`, run `--diff` to print a no-write comparison between the existing WP slug target and the proposed Notion payload. Treat the diff as evidence for human review, not approval to update.

This makes reruns safe by default. If you need a new version rather than an update, pass `--slug` with a new slug.

## Category routing

Known Notion types map directly:

| Notion Type | WP Category |
|---|---|
| `Report` | `Vancouver AI Ecosystem` |
| `Manifesto` | `AI Ethics & Philosophy` |
| `Interview` | `Conversations & Interviews` |
| `Tutorial` | `AI for Creatives` |
| `Field Note` | `Field Notes` |

`Feature` is intentionally guarded. It routes from obvious tags:

- community/event tags such as `BC + AI`, `Comox`, `Vancouver AI`, `Web Summit`, `Recap` → `Vancouver AI Ecosystem`
- ethics/certification tags such as `AI Ethics`, `Responsible AI`, `Certification` → `AI Ethics & Philosophy`
- creative workflow tags such as `Creative`, `Artist`, `Tools`, `Workflow` → `AI for Creatives`
- appearance tags such as `Interview`, `Podcast`, `Media` → `Conversations & Interviews`

If a `Feature` post has ambiguous tags, dry-run output is marked `NEEDS CATEGORY REVIEW`, and live mode aborts before uploading media or creating a WP draft. Re-run with `--category "..."` after the editorial decision.

## Local tests

The connector has focused stdlib tests for the post-incident safety guards:

```bash
scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests
```

These tests do not call Notion or WordPress.

## Logs & debugging

Every run writes a `publish.log` next to the draft. Includes the exact REST requests and responses. If something fails, share that file and we'll fix the connector, not the post.

## Block conversion

See `block_rules.py` for the Notion → Gutenberg mapping. Connector plumbing now lives in focused modules next to `kk_notion_to_wp.py` for config, Notion access, payload building, media handling, WordPress REST, update safety, category routing, and draft companion files.

## Shared block markup (`wp_blocks.py`)

Every post path emits Gutenberg blocks through **one** module, `wp_blocks.py`, instead of hand-rolling `<!-- wp:image -->` strings per script. `block_rules.py` (the main Notion pipeline) and the one-off `publish_*.py` scripts all import it, so a post looks the same no matter which path produced it.

Helpers:

- `image(media_id, url, alt, *, caption, width, align, lightbox)` — core. `media_id` may be an `int`, the string `"TBD"` (dry-run, before upload), or `None`.
- `inline_image(...)` — small, centered, click-to-zoom receipt (default width **460px**).
- `hero_image(...)` — full-width section hero.
- `gallery(items, columns)`, `separator()`, `heading(text, level=2)`, `pullquote(text)`, `inline(s)` (markdown links/bold/italic; external links get `target="_blank" rel="noopener noreferrer"`).

kk-aurora theme constraints baked into the defaults:

- The post prose column is **720px**. A wider image overflows the text column, so inline images set an explicit width (default 460px, ~64% of column).
- The theme has **no float CSS**, so inline images are centered (no text wrap).
- The native WP 6.4+ lightbox is on: images use `"lightbox":{"enabled":true}` (no `<a>` wrapper) and captions use `wp-element-caption`.

Markup is locked by `tests/test_wp_blocks.py`.

### Re-emitting an already-published post

Rebuilding a live post's body from its source markdown is only safe when that source is still in sync with what's live. If the live post has drifted (manual edits, a newer source), a rebuild **drops** those blocks. To upgrade image markup on a drifted live post, transform the fetched live content **in place** (e.g. swap `"linkDestination":"none"` → `"lightbox":{"enabled":true}` and `wp-block-image__caption` → `wp-element-caption`), and diff the block structure before/after to confirm only the intended markup changed.

`backfill_lightbox.py` does exactly this across the whole published catalog: it enables the native lightbox on every core image (none/media link destinations), unwraps click-to-open `<a><img></a>` anchors, drops gallery `linkTo:media`, and normalizes the caption class — leaving `linkDestination:custom` (deliberate outbound-link) images alone. Each write is guarded so the block structure must be identical before/after, and originals are appended to a rollback manifest first.

```bash
python backfill_lightbox.py                       # dry-run: what would change
python backfill_lightbox.py --execute             # apply; writes backfill-rollback.jsonl
python backfill_lightbox.py --rollback FILE.jsonl # restore originals from a manifest
```

Heads-up: REST content updates bump each post's modified date (sitemap `lastmod`). The 2026-06-28 run swept all 161 image-posts (~1,346 images); its manifest is `backfill-rollback-2026-06-28.jsonl` (gitignored).

## Polish pass (em-dash purge + auto-link)

After block rendering, every post goes through `text_polish.py`:

1. **Em-dash purge** — `—` becomes `, ` and prose en-dashes become `-`. Numeric en-dash ranges like `0–5` are preserved. KK's rule: em-dashes read as AI in 2026.
2. **Auto-link first occurrence** — proper nouns in `LINK_MAP` get hyperlinked the first time they appear in body HTML (skipped inside headings, captions, existing links, code blocks). Self-link guard prevents a post from linking to itself.

To add a new term, edit the `LINK_MAP` list in `text_polish.py` and add a tuple of `(regex, url, optional_title)`. Longer phrases should come first.

The polish report (which terms were linked) is written to the publish log so you can audit each run.

## Graduation path

After 2–3 successful publishes, this folder graduates to `skills/notion-to-wp/SKILL.md` so it can be invoked as a Claude Code skill (e.g., "publish my Notion post to kriskrug.co").
