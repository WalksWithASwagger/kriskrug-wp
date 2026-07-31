# Draft publishing discovery - 2026-05-18

**Lane:** Swarm Lane 2 - next-batch draft publishing discovery  
**Scope honored:** local Notion inventory, connector dry-runs, and local draft/report artifacts only. No WordPress publish, update, media upload, taxonomy creation, or post mutation was performed.

## Inputs Found

- Connector: `scripts/notion-to-wp/kk_notion_to_wp.py`
- Connector env:
  - `NOTION_TOKEN` available from `/Users/kk/Code/notion-local/kk-ai-ecosystem/.env`
  - `WP_USER`, `WP_APP_PASSWORD`, and `WP_DEFAULT_AUTHOR_ID` present in `scripts/notion-to-wp/.env`, but not used beyond dry-run payload generation
- Notion database found through Notion search:
  - Name: `News & Content Database`
  - ID: `5c4935df-c592-4fb1-88e7-f15665728a68`
  - Relevant properties: `Title`, `Status`, `Publication Date`, `Type`, `Tags`, `Featured`, `Summary`, `AI summary`

## Candidate Inventory

Recent relevant rows from `News & Content Database`:

| Priority | Notion page | Status | Date | Type | Tags | Decision |
|---:|---|---|---|---|---|---|
| 0 | `Calling Us All In` (`697c980d3faa45b8966be2fb937271e1`) | Review | 2026-05-14 | Report | Vancouver AI, BC + AI, Web Summit Vancouver | Already live/local pack exists; skipped. |
| 0 | `Welcome to Web Summit. Now Show Us the Numbers.` (`359c6f799a33806c8250ce401eeab2c4`) | Review | 2026-05-07 | Feature | Web Summit Vancouver | Already restored/live as `Web Summit Vancouver 2026`; skipped. |
| 1 | `Sovereign AI for Whom?` (`35ec6f799a33809a8a6ef6507b8e7b0a`) | Review | 2026-05-13 | Feature | Industry, BC + AI, Web Summit Vancouver | Dry-run created. |
| 2 | `Comox Valley AI Is Becoming Its Own Thing` (`d2c709d563934053934bf63de4dbd47a`) | Draft | 2026-05-06 | Feature | BC, Comox, BC + AI, Recap, AI Ethics, Community Spotlight | Dry-run created. Needs editorial cleanup. |
| 3 | `Why We Built the Responsible AI Professional Certification` (`344c6f799a33806087b0cb917682912a`) | Review | 2026-05-16 | Feature | AI, AI Ethics | Dry-run created. Needs excerpt/SEO cleanup. |
| 4 | `The AI Values Gap` (`344c6f799a33809bb6aed2d185a6ce56`) | Published | 2026-04-14 | Feature | BC + AI | Published in Notion; not dry-run in this pass. |

## Dry-Runs Created

All commands used `--dry-run` and only wrote local files under `content/drafts/`.

| Draft pack | Notion source | Blocks | Images | Notes |
|---|---|---:|---:|---|
| `content/drafts/2026-05-13-sovereign-ai-for-whom/` | `35ec6f799a33809a8a6ef6507b8e7b0a` | 121 | 6 | Strongest publish candidate. Auto-linked 3 terms. Category currently falls to `Misc` because connector has no `Feature` mapping. One generated alt string includes HTML and should be hand-edited before publish. |
| `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/` | `d2c709d563934053934bf63de4dbd47a` | 110 | 0 | No images in source. Auto-linked 4 terms. Excerpt/meta currently uses a draft-status callout and must be replaced before publish. |
| `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/` | `344c6f799a33806087b0cb917682912a` | 83 | 13 | Image-heavy RAP pack. Auto-linked 1 term. Excerpt/meta currently uses the byline, not the article pitch; needs manual replacement before publish. |

Generated files in each pack:

- `post.md`
- `post.html`
- `seo-meta.md`
- `alt-text.md`
- `internal-links.md`
- `publish.log`
- `images/` where Notion image blocks existed

## Commands

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run https://www.notion.so/35ec6f799a33809a8a6ef6507b8e7b0a
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run https://www.notion.so/d2c709d563934053934bf63de4dbd47a
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py --dry-run https://www.notion.so/344c6f799a33806087b0cb917682912a
```

Ready-to-run publisher commands after human review:

```bash
# Create WP drafts only. Do not add --publish unless KK explicitly approves immediate publication.
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py https://www.notion.so/35ec6f799a33809a8a6ef6507b8e7b0a
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py https://www.notion.so/d2c709d563934053934bf63de4dbd47a
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/kk_notion_to_wp.py https://www.notion.so/344c6f799a33806087b0cb917682912a
```

## Blockers And Publisher Checks

No Notion access blocker in this lane; the token could read the database and page bodies.

Before any WordPress write:

- Re-run the same page with `--dry-run` immediately before publish and diff the regenerated pack if Notion changed.
- Confirm `scripts/notion-to-wp/.env` is still gitignored before any commit; it contains WP credentials.
- Decide category behavior for `Feature`. Current connector maps only `Report`, `Manifesto`, `Interview`, `Tutorial`, and `Field Note`, so these three candidates would create/use `Misc` unless the publisher applies a code/config fix first.
- Replace weak generated excerpts:
  - Comox: remove `Draft status...` from excerpt/meta.
  - RAP: replace the byline excerpt/meta with a real summary.
- Review `alt-text.md` for image-heavy posts. `Sovereign AI for Whom?` has one alt string with embedded HTML from an auto-linked phrase; RAP has several long slide-derived alt strings.
- Check `internal-links.md` and external links in each pack before creating WP drafts.
- Keep live mode create-only unless intentionally updating an existing slug; do not use `--update` in the next publisher pass without fresh slug/WP ID verification.
