# Notion → kriskrug.co publisher

A small, single-file CLI that pulls a Notion page from KK's "News & Content Database" and posts it to kriskrug.co as a WordPress draft. Purpose-built for this site only — not portable, no plugins to install, no admin UI to maintain.

## What it does

1. Fetches a Notion page via the Notion API (using KK's existing `NOTION_TOKEN`).
2. Converts Notion blocks into Gutenberg core-block HTML (paragraph, heading, list, quote, callout, image, code, separator, mark).
3. Downloads embedded images from Notion's expiring S3 URLs into `content/drafts/<slug>/images/`.
4. Drafts an SEO-prepped post locally (`content/drafts/<slug>/post.md` + `post.html` + `seo-meta.md` + `alt-text.md` + `internal-links.md`).
5. If `--publish` is passed: uploads each image to `kriskrug.co`'s Media Library (alt text set), rewrites image URLs, then `POST`s the post body to `/wp-json/wp/v2/posts` with `status=draft`.
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
5. WordPress shows the password ONCE — copy it immediately. It looks like `aBcD 1234 EfGh 5678 IjKl 9012`.
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

# Live: also uploads images, creates a DRAFT post on kriskrug.co
python kk_notion_to_wp.py https://www.notion.so/<page-id>

# Live + publish immediately (skip the draft step)
python kk_notion_to_wp.py --publish https://www.notion.so/<page-id>
```

## Notion property mapping

KK's "News & Content Database" has these properties; the connector reads them:

| Notion property | WP field | Notes |
|---|---|---|
| Title | post title | required |
| AI summary | excerpt (→ meta description) | falls back to Summary if absent |
| Tags | tags | auto-created if missing |
| Type | category routing | `Report` → "Vancouver AI Ecosystem"; others → "Misc" until categorized |
| Featured | post meta `kk_featured` | "YES" sets it |
| Status | publish gate | `Ready` + `--publish` flag → published; otherwise draft |
| Publication Date | post date | if absent, uses today |
| Author / Owner | post author | mapped to WP user ID 1 (kk) for now |

## Idempotency

On first publish, the script writes the Notion page ID to WP post meta `kk_notion_source_id`. Re-running with the same Notion URL **updates** that post rather than creating a duplicate. Safe to re-run after edits in Notion.

## Logs & debugging

Every run writes a `publish.log` next to the draft. Includes the exact REST requests and responses. If something fails, share that file and we'll fix the connector, not the post.

## Block conversion

See `block_rules.py` for the Notion → Gutenberg mapping. Each rule is a small function — tweak as the writing style evolves.

## Graduation path

After 2–3 successful publishes, this folder graduates to `skills/notion-to-wp/SKILL.md` so it can be invoked as a Claude Code skill (e.g., "publish my Notion post to kriskrug.co").
