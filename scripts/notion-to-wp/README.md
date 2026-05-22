# Notion → kriskrug.co publisher

A small, single-file CLI that pulls a Notion page from KK's "News & Content Database" and posts it to kriskrug.co as a WordPress draft. Purpose-built for this site only — not portable, no plugins to install, no admin UI to maintain.

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
```

## Live-write gate

Temporary 2026-05-22 operating stance: private, create-only WordPress drafts may be created without strict backup/restore proof so review URLs can move again.

Private draft creation is allowed only when all of these are true:

1. A dry-run package has been reviewed in `content/drafts/<slug>/`.
2. The target slug is verified as a create-only draft target; do not pass `--update`.
3. The title, category, tags, excerpt, and create intent are verified.
4. For `Type=Feature`, the category is intentional: either the tags route it clearly or `--category` is passed.
5. The run keeps WordPress status as `draft`; do not pass `--publish`.
6. Media uploads are approved and have alt text, or the draft is image-free.
7. The resulting WP post ID, edit URL, and run notes are recorded in `publish.log`.

Strict backup/restore proof is still required before public publish, updates to existing posts/pages, destructive cleanup, plugin/theme/schema/robots changes, bulk writes, or any `--update` run.

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

See `block_rules.py` for the Notion → Gutenberg mapping. Each rule is a small function — tweak as the writing style evolves.

## Polish pass (em-dash purge + auto-link)

After block rendering, every post goes through `text_polish.py`:

1. **Em-dash purge** — `—` becomes `, ` and prose en-dashes become `-`. Numeric en-dash ranges like `0–5` are preserved. KK's rule: em-dashes read as AI in 2026.
2. **Auto-link first occurrence** — proper nouns in `LINK_MAP` get hyperlinked the first time they appear in body HTML (skipped inside headings, captions, existing links, code blocks). Self-link guard prevents a post from linking to itself.

To add a new term, edit the `LINK_MAP` list in `text_polish.py` and add a tuple of `(regex, url, optional_title)`. Longer phrases should come first.

The polish report (which terms were linked) is written to the publish log so you can audit each run.

## Graduation path

After 2–3 successful publishes, this folder graduates to `skills/notion-to-wp/SKILL.md` so it can be invoked as a Claude Code skill (e.g., "publish my Notion post to kriskrug.co").
