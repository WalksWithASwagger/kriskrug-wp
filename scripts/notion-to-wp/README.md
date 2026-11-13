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

Preferred: set `NOTION_TOKEN` in `~/.agents/env/values/.env.kriskrug-wp.local` (or the pick-restricted shared profile) and run the command through Varlock. See repo-root [`.env.schema`](../../.env.schema) and [`docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md`](../../docs/current-state/VARLOCK-ROLLOUT-2026-07-16.md).

Compat: a leftover `scripts/notion-to-wp/.env` or `NOTION_ENV_PATH` / `KKAI_ENV_PATH` sibling file still works if present but is **deprecated as secret source-of-truth**. Do not copy secrets into this repo.

### 2. WordPress Application Password

Generate one **once**:

1. Open https://kriskrug.co/wp-admin/profile.php
2. Scroll to **Application Passwords** (near the bottom of the page).
3. Application Name: `kk-notion-to-wp`
4. Click **Add New Application Password**.
5. WordPress shows the password once. Put it in the user-managed Varlock values file (`~/.agents/env/values/.env.kriskrug-wp.local`). Do not paste it into docs, issues, commits, or chat.
6. Run the connector through Varlock:

```bash
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run https://www.notion.so/<page-id>
# equivalent: make varlock-run CMD='python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run …'
```

If you ever lose the application password, just revoke and regenerate — no password recovery in WP.

### 3. Python deps

```bash
cd scripts/notion-to-wp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../..
```

## Usage

**Preferred for reviewed local packets:** `create_local_wp_draft.py` (see [Local draft package publisher](#local-draft-package-publisher)). Prefer that over minting new `publish_*.py` one-offs. Use `kk_notion_to_wp.py` when you still need a Notion fetch → local draft conversion.

```bash
# Dry-run: writes content/drafts/<slug>/, prints REST payload, does NOT post
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run https://www.notion.so/<page-id>

# Dry-run with an explicit category decision
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run --category "AI Ethics & Philosophy" https://www.notion.so/<page-id>

# Live: also uploads images, creates a DRAFT post on kriskrug.co
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py https://www.notion.so/<page-id>

# Live + publish immediately
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --publish https://www.notion.so/<page-id>

# Live update of an existing slug, guarded by title similarity
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --update https://www.notion.so/<page-id>

# No-write update review: fetches the existing slug target and prints a diff
varlock run --inject vars -- python scripts/notion-to-wp/kk_notion_to_wp.py --diff https://www.notion.so/<page-id>
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
varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/<date-slug>/post.md

# Explicit create-only WP draft run.
varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/<date-slug>/post.md --execute
```

## Draft queue audit

Before promoting anything from the WordPress draft pile, refresh the read-only queue audit:

```bash
varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py
# equivalent: make draft-queue-audit
```

The audit reports live WP draft/future/pending/private counts, local `content/drafts/` package metrics, exact slug matches across published and draft posts/pages, and draft quality signals. It does not create, update, schedule, or publish anything.

Use `--local-only` when WordPress credentials are unavailable:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --local-only
```

## Event coverage publish checklist

When publishing a recap or event-coverage post, complete the Events documentation
link in the same approved publishing pass:

1. Match the existing stable event ID, date and venue in
   `scripts/events_page/events-catalog.yaml` and its merged harvest/fragments.
   Do not add a duplicate event because a recap has a new title.
2. Verify the published post's exact slug/ID/status and public canonical URL.
   Append that URL to the event's `docs.recap` list. Retain earlier recaps for a
   multi-post series. Existing `recap_url` remains the primary local recap;
   never replace registration/source `url` with documentation.
3. Add `docs.photos` / `docs.video` only from verified public galleries or
   recordings. Verify the actual gallery anchor and retain photographer credits.
   A promo-card image is not proof of who photographed the event. Missing links
   remain empty; do not invent art, URLs, permissions or credits.
4. Load and render through the [Events pipeline](../events_page/README.md).
   All normalized records carry recap/photos/video lists, including empty ones.
   Check the exact diff and preserve live IDs, media, credits and shell content.
   Prepared catalog-only entries remain held unless their publication was
   separately approved.
5. With KK's approval covering the page update, snapshot and apply page **2250**
   through the existing guarded deploy helper, then verify authenticated and
   public link readbacks. A post approval alone is not approval to replace the
   entire Events page. If the page update is not yet approved, leave its exact
   patch and rollback packet ready and explicitly mark the link as pending.
6. Record the post URL, event ID, documentation links, page snapshot/hash and
   verification in the publishing receipt. A local render does not finish the
   public documentation-link step.

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
| Status | none | not read; only `--publish` sets WP status to publish |
| Publication Date | post date | if absent, uses today |
| Author / Owner | post author | mapped to WP user ID 1 (kk) for now |

## Idempotency

The 2026-05-15 incident proved that Notion-ID meta lookups are not safe unless the meta key is registered with `show_in_rest`. The connector now uses **slug-based lookup** for identity checks.

Default behavior is CREATE-only:

- If no post with the slug exists, the connector creates a new WP post.
- If a post with the slug already exists, the connector aborts instead of silently updating.
- To update an existing post, pass `--update`. The update path also checks that the existing title is similar to the new title before it sends a REST update. The current threshold lives in `TITLE_SIMILARITY_UPDATE_THRESHOLD` and is covered by tests.
- `--update` never changes the post's status. It sends no status, so a published, scheduled, private or draft post stays that way. Only `--update --publish` sets the status, to publish. Before this rule, `--update` alone sent `draft` and unpublished live posts.
- `--update` sends no date unless `--date` is given. WordPress publishes a scheduled post whose date has passed and schedules a published post whose date is in the future, so sending the Notion date (or today) could publish a scheduled post early. An explicit `--date` can still trigger either rule; the readback below then exits 7.
- Before using `--update`, run `--diff` to print a no-write comparison between the existing WP slug target and the proposed Notion payload. Treat the diff as evidence for human review, not approval to update.
- The slug lookup and both guards run before any media upload or term creation, so an abort leaves nothing behind on WordPress. A lookup that refuses to answer (`SlugVerificationFailed`, for example an ambiguous match) exits 8.
- After a create or update, the connector reads the post back. If the stored slug, status, title or date differs from what it sent, it logs each difference and exits 7. An update without `--publish` must find the post's status exactly as it was before the write, and `--update --publish` on a live post fails if WordPress scheduled it instead.

This makes reruns safe by default. If you need a new version rather than an update, pass `--slug` with a new slug.

## Characters outside cp1252

kriskrug.co's posts and postmeta tables use MySQL's `latin1`, which is really Windows-1252 (cp1252). Curly quotes, en and em dashes, the ellipsis, the bullet, `€` and `™` are stored as sent, and the edit-context snapshots under `backup/` hold them raw. Any other character above U+00FF sent raw is stored as `?` (#606). The connector, `create_local_wp_draft.py`, `update_local_wp_draft.py`, `prepare_review_draft.py`, the marquee sync and the event media sync all send text through `cp1252_text.py` (#1225):

- Title, content, excerpt, media alt text, caption and description, and term names go out with characters outside cp1252 as numeric references: `Ethọ́s` is sent as `Eth&#7885;&#769;s` and `→` as `&#8594;`. cp1252 text such as `Krüg` or `KK’s` and existing entities are left alone. The readback and the `--update` title guard compare titles after `html.unescape`, so a stored reference still matches.
- `<style>` and `<script>` bodies are never encoded, because browsers do not decode references there. A character outside cp1252 inside one is refused; write it as a CSS escape (`\2192`) or a JavaScript escape (`\u2192`).
- The SEO title, SEO description and Publicize message are plain text, so they must fit cp1252 (accents are composed with NFC first). A reference would show literally there, and combining marks make Jetpack's meta write fail with HTTP 500. What happens to any other character depends on who wrote the text (KK's ruling, 2026-11-12):
  - **Derived meta is folded.** The connector writes none of these fields by hand. It derives the SEO title from the post title (a `--title` override included), and the description and Publicize message from the excerpt (the first substantive paragraph, or the Notion summary fallback). Each character cp1252 cannot store becomes its base letter when it has one (`Ethọ́s` becomes `Ethos`, `Łódź` becomes `Lódz`) and is dropped when it has none (arrows, emoji), and doubled spaces collapse. cp1252 characters such as `Krüg`, curly quotes, dashes and `…` are never touched. The run logs one line per folded field, for example `seo: folded advanced_seo_description: "Ethọ́s Lab" -> "Ethos Lab"`, and carries on. The draft package's `seo:` frontmatter and `seo-meta.md` hold the folded text. The post title, excerpt and body keep the original characters as numeric references.
  - **Hand-written meta is refused.** `seo.meta_title` and `seo.meta_description` in a package's frontmatter are the operator's copy, and `create_local_wp_draft.py`, `update_local_wp_draft.py` and `prepare_review_draft.py` derive no meta of their own. Such a character there fails the local-draft quality gate (`create_local_wp_draft.py` exits 2) or stops `prepare_review_draft.py --wp-id` with exit 4, naming the field, before any upload, term or post write. Fix the copy by hand.
- C1 control characters (U+0080 to U+009F) are refused everywhere; they usually mean text was decoded with the wrong charset.
- Any other raw character outside cp1252 left in a request body raises `UnstorableText` before the request is sent.
- The connector, the local-draft quality gate and `prepare_review_draft.py` check every request a run will make (title, content, excerpt, alt text and term names as well as meta) before the first upload or term write, because media trash is off on this site and an orphaned upload is permanent. The connector exits 9 before any WordPress request when something cannot be sent. Its meta is always folded, so that now means the body, an alt text or a term name.

`scripts/common.py`'s `WPClient`, which `deploy_events_page.py`, `content_architecture_deploy.py` and several one-off writers in `scripts/` use, does not encode. The deploy tools compare the readback with their payload file exactly, and a reference added on the way out would fail that comparison. A POST, PUT or PATCH whose body or query params hold a character outside cp1252 raises `UnstorableText` before anything is sent, naming the field and the character, for example `payload.content has raw characters outside cp1252 that WordPress would store as '?': U+2192 RIGHTWARDS ARROW`. Fix the payload source: write `&#8594;` in HTML, or a CSS or JavaScript escape inside `<style>` or `<script>`.

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
make python-test
```

For this suite alone:

```bash
python3 -m pytest scripts/notion-to-wp/tests -v
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

## Shared publisher orchestration (`publish_common.py`)

`wp_blocks.py` owns the markup; `publish_common.py` owns everything the one-off
`publish_*.py` scripts do *around* it — front matter, marker dispatch, media
resolution, the slug guard, SEO meta, and declared IDs.

- `strip_frontmatter(raw)` — drop a leading `---` YAML block.
- `render_marker_blocks(body, handlers, *, paragraph=..., skip_first_h1=True)` —
  split on blank lines, drop the first `# ` (the title lives in the WP title
  field), then dispatch each block through ordered `(matcher, render)` handlers.
  A matcher is a compiled regex or a callable (`exact("---")`, `prefix("## ")`);
  a renderer returning `None` emits nothing. Unclaimed blocks fall through to
  `paragraph`.
- `standard_text_handlers(*, h3=True, pullquote_marker=False)` — the shared
  `---` / `## ` / `### ` / `>>> ` set every script starts from.
- `render_paragraph_from_markdown` (joins source lines with `<br>`) vs
  `raw_paragraph` (keeps the newline). Both exist because both are already
  shipped: `publish_dc_protest_draft.py` uses the latter, everything else the former.
- `find_or_upload_media(...)` — idempotent resolve-by-filename-stem, then upload.
  Dry-run returns `(0, "DRYRUN/<file>")` and never calls WordPress.
- `find_existing_post_by_slug(wp, slug)` — the create/update guard. Confirm the
  returned record is the intended target before any PATCH (2026-05-15 incident rule).
  It returns the one post whose slug is exactly `slug`, or `None` when there is
  none. A failed lookup, two posts sharing the slug, or any hit whose slug is not
  exactly `slug` raise `SlugVerificationFailed`. WordPress normalizes the slug it
  queries, so that last case means `slug` is not canonical. `slugify` folds Latin
  accents to ASCII so the connector asks for the slug WordPress stores. It wraps
  `wp_client.lookup_slug`, the single slug lookup that
  `WordPress.find_post_by_slug`, `create_local_wp_draft.assert_slug_available`
  and `scripts/marquee/wp_sync.py` also use.

### Declared IDs (`publisher-ids.json`)

Production category and media IDs are declared once in `publisher-ids.json` —
same shape as `content/source-packs/.../page-map.json` — instead of being typed
into each script. Loaders: `category_id(key)`, `media_id(key)`,
`media_group(key)`, `media_group_index(key)` (`{id: (url, alt)}` plus declared
order) and `media_group_keys(key)` (`{name: id}`, so a script can say
`SIGN["water-the-servers-last"]` instead of `11918`).

Unknown keys and non-positive IDs abort with `[ABORT]`. Live existence is still
proven separately at write time by `resolve_category_ids` / `validate_media_id`.
Every script default stays overridable (`--category-id`, `--featured-media-id`)
so a staging run never inherits a production ID.

Locked by `tests/test_publish_common.py`, `tests/test_publisher_ids.py` and
`tests/test_publisher_render_characterisation.py` (the last file keeps verbatim
copies of the pre-consolidation loops and asserts the shared dispatcher still
matches them byte for byte).

### Re-emitting an already-published post

Rebuilding a live post's body from its source markdown is only safe when that source is still in sync with what's live. If the live post has drifted (manual edits, a newer source), a rebuild **drops** those blocks. To upgrade image markup on a drifted live post, transform the fetched live content **in place** (e.g. swap `"linkDestination":"none"` → `"lightbox":{"enabled":true}` and `wp-block-image__caption` → `wp-element-caption`), and diff the block structure before/after to confirm only the intended markup changed.

`backfill_lightbox.py` does exactly this across the whole published catalog: it enables the native lightbox on every core image (none/media link destinations), unwraps click-to-open `<a><img></a>` anchors, drops gallery `linkTo:media`, and normalizes the caption class — leaving `linkDestination:custom` (deliberate outbound-link) images alone. Each write is guarded so the block structure must be identical before/after, and originals are appended to a rollback manifest first.

```bash
varlock run --inject vars -- python scripts/notion-to-wp/backfill_lightbox.py                       # dry-run: what would change
varlock run --inject vars -- python scripts/notion-to-wp/backfill_lightbox.py --execute             # apply; writes backfill-rollback.jsonl
varlock run --inject vars -- python scripts/notion-to-wp/backfill_lightbox.py --rollback FILE.jsonl # restore originals from a manifest
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
