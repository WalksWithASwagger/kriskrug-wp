# Access Channels — How We Can Reach kriskrug.co Today

Every way Claude / this repo can currently observe or modify the live site, and what's blocked.

## ✅ Available now

### 1. Public WP REST API (read-only)
- **URL:** `https://kriskrug.co/wp-json/`
- **Capability:** Read posts, pages, users, taxonomies, types, taxonomies, theme presets where exposed.
- **Auth:** None needed for public content.
- **Limits:** Cannot read draft/private content, plugin configs, options, or user PII. Can't write anything.
- **Used for:** Building this snapshot. Reusable for fingerprinting after any change.

### 2. Authenticated WordPress REST via local connector
- **Status:** Verified read-only on 2026-05-18 through `scripts/notion-to-wp/`. Application password rotated on 2026-05-18 at 11:14 PT; only the fresh connector credential remains active.
- **Auth:** WordPress application password loaded from the gitignored local `.env`; never paste or commit it.
- **Capability:** Read private draft status, authenticated `status=any` post/page lookups, categories, revisions, and other endpoints supported by the current app-password user.
- **Write capability:** Technically possible through the connector, but operationally blocked until backup confirmation, dry-run review, slug/ID verification, and category cleanup are complete.
- **Used for:** Confirming 944 published posts, 32 draft posts, 34 published pages, 3 draft pages, exact-slug status, and recent-post revision availability.

### 3. WordPress.com MCP — `claude.ai WordPress.com` connector
- **Status:** Authenticated as Kris on 2026-05-14.
- **Site visible:** kriskrug.co (blog ID 159424804).
- **Capability:** ⚠️ **Effectively zero** — every site-scoped operation (`posts.*`, `pages.*`, `media.*`, `theme.*`, `patterns.*`, etc.) returns *"This operation is disabled in your MCP settings."*
- **Why:** Site is on Jetpack **Free**. MCP requires **Jetpack AI** or **Jetpack Complete**. See `https://jetpack.com/pricing/`.
- **Unblock:** Upgrade Jetpack plan, then re-enable MCP operations in Jetpack settings.
- **Codex note:** On 2026-05-18, Codex tool discovery did not expose a dedicated WordPress MCP tool. The authenticated REST connector above is the verified admin-data path in this repo.

### 4. Chrome MCP (`mcp__claude-in-chrome__*`)
- **Status:** Available if the Chrome extension is connected.
- **Capability:** Drive `wp-admin` in a real browser session — log in, edit posts/pages/settings, install plugins, run any UI action. Verify with on-page screenshots.
- **Risk profile:** Every action is a real action. We should preview each change and confirm with you, especially anything that hits "Update" or "Save."
- **When to use:** Whenever a wp-admin action is the cleanest path (e.g. installing a backup plugin, exporting via UI, toggling a setting that has no REST endpoint).

### 5. Computer-use MCP
- **Status:** Available, but browser-tier (read-only) for Safari/Chrome/etc.
- **Capability:** Native macOS apps at full tier (Finder, Terminal at click-only, etc.). Useful for moving downloaded files, taking screenshots, opening apps.
- **Not useful for:** Driving wp-admin (that's a browser → use Chrome MCP).

### 6. Git + GitHub
- **Repo:** `kriskrug-wp` (this one)
- **Capability:** All standard git/gh operations. The agent swarm in `.github/` can be triggered via issues + labels.

## 🚫 Not available

### SSH to Pagely (production)
- **Why we need it:** Only path to a real `wp db export`, file diff against upstream Catch Responsive, and a true local mirror.
- **What we need from you:** Pagely SSH host + user + key auth (or password if that's all we have for now).
- **Substitute until then:** A WP-admin-installed backup plugin like UpdraftPlus or All-in-One WP Migration generates a downloadable archive (see `BACKUP_PLAN.md`).

### SSH to the Cloudways dev server (24.144.80.107)
- **Status:** Documented in `docs/cloudways-setup.md`, user `master_qcteaefabe`. Whether it's still running and whether the key is set up is unknown — needs verification.
- **Note:** This is a *separate* server from production. Useful for testing changes before pushing to Pagely.

### Direct database access
- None today. Will follow SSH.

### Pagely control panel
- Not connected here. Live admin lives at https://atomic.pagely.com (Pagely's customer dashboard).

## Modification matrix — which channel can do what

| Action | Public REST | Auth REST connector | WP.com MCP | Chrome MCP | SSH | Notes |
|---|---|---|---|---|---|---|
| Read public posts/pages | ✅ | ✅ | 🚫 (disabled) | ✅ | ✅ | Public REST is fine for public corpus checks |
| Read drafts/private status | 🚫 | ✅ | 🚫 (disabled) | ✅ | ✅ | Use authenticated connector for inventory; do not expose private draft dumps publicly |
| Create a post draft | 🚫 | ⚠️ gated | 🚫 (disabled) | ✅ | ✅ (via wp-cli) | Backup + dry-run + slug verification required |
| Edit a page | 🚫 | ⚠️ gated | 🚫 (disabled) | ✅ | ✅ (via wp-cli) | Chrome or SSH after backup; connector only after safety gates |
| Install plugin | 🚫 | 🚫 | 🚫 | ✅ | ✅ | Wp-admin > Plugins > Add New |
| Edit theme file | 🚫 | 🚫 | 🚫 | ⚠️ (Appearance > Editor, fragile) | ✅ | SSH strongly preferred |
| Update theme code permanently | 🚫 | 🚫 | 🚫 | 🚫 | ✅ | Needs file write |
| Export full site | 🚫 | 🚫 | 🚫 | ✅ (via plugin) | ✅ (cleanest) | UpdraftPlus / AIO-WP-Migration / wp-cli |
| Database query | 🚫 | 🚫 | 🚫 | 🚫 | ✅ | Via wp-cli or wp-admin's tools |
| Roll back a code change | 🚫 | 🚫 | 🚫 | ⚠️ (only if change made via UI) | ✅ | SSH + git on the server |

## Recommendation for ordering

1. **Today, without SSH:** use authenticated REST for read-only admin inventory and exact-slug checks; use Chrome MCP for wp-admin-driven actions such as backup plugins or UI-only settings. Treat every action as preview + confirm.
2. **For production writes:** verify backup, run dry-run/diff, verify target slug/ID/status, then use the least risky path for the specific change.
3. **Once SSH lands:** switch primary infrastructure channel to SSH + wp-cli. Use Chrome MCP only for things that genuinely need the UI (block editor, Jetpack settings, etc.).
4. **If Jetpack MCP is upgraded/enabled:** WordPress.com MCP may become a fast option for content edits, but it still cannot replace SSH for theme files, plugins, database export, or rollback.
