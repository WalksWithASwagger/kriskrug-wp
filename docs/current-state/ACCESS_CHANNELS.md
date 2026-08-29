# Access Channels — How We Can Reach kriskrug.co Today

> **Freshness:** Verified 2026-08-29. Run `make doctor` and `make status-readonly` before relying on any channel; credentials, browser sessions, and hosting access can change independently of this repo.

This document records the supported ways an agent can observe or modify kriskrug.co. The site runs on Pagely and is not file-synced with this repository.

## Available channels

### 1. Public WordPress REST API

- **URL:** `https://kriskrug.co/wp-json/`
- **Authentication:** None for public content.
- **Capability:** Read published posts, pages, media, taxonomies, types, and other publicly exposed data.
- **Limits:** Cannot read drafts, private content, plugin settings, or protected options. Cannot write.
- **Use it for:** Public inventory, route verification, and post-change readback.

### 2. Authenticated WordPress REST through Varlock

- **Status:** Authenticated reads, dry-runs, guarded writes, snapshots, and readbacks were verified on 2026-08-29.
- **Authentication:** Varlock is the source of truth. The repo accepts either `WP_USER` + `WP_APP_PASSWORD` or `WP_API_USERNAME` + `WP_API_PASSWORD`; never read, print, or commit secret values.
- **Capability:** Read draft/private status and supported admin endpoints; update exact posts, pages, and media through the guarded repo scripts.
- **Inventory:** Use `make status-readonly` for current draft and scheduled-post counts; do not copy those volatile values into this access guide.
- **Write gate:** Run an authenticated dry-run first, verify the exact ID and slug, capture a private rollback snapshot, obtain the approval required by the active issue, apply one bounded change, and perform authenticated plus public readback.
- **Preferred invocation:** `make varlock-run CMD='…'` or `varlock run --inject vars -- …` using a documented repository command.

### 3. Git and GitHub CLI

- **Repository:** `WalksWithASwagger/kriskrug-wp`.
- **Status:** `gh` authentication was verified by `make doctor` on 2026-08-29.
- **Capability:** Normal issue, PR, Actions, and git operations subject to repository conventions and branch protection.
- **Important:** The older GitHub Actions agent swarm is retired. Labels do not trigger it. `.github/workflows/test-pr.yml` remains the active PR validation workflow.

### 4. Browser or computer-use tools

- **Status:** Session-dependent; verify the active tool and authenticated browser state before relying on it.
- **Capability:** Operate `wp-admin` when a UI-only action or manual block-editor verification is required.
- **Risk:** Every Save, Update, Install, or Delete control is a real production action. Use an exact preview, rollback path, and the issue-specific approval gate.

### 5. Pagely SFTP theme deployment

- **Path:** `scripts/deploy_theme_sftp.py` supports the repository's bounded theme deployment workflow.
- **Authentication:** `WP_SFTP_PASSWORD` in the injected process environment or the documented macOS Keychain service.
- **Availability:** Must be verified at execution time; a public `style.css` readback only proves the live version, not write access.
- **Gate:** A merge is not a deployment. Theme deploys require explicit KK approval, a rollback path, and the applicable visual gate.

## Unverified or unavailable channels

### WordPress.com MCP

A May 2026 check found site-scoped operations disabled. Treat that result as historical and do not assume the connector is available now. The authenticated REST tooling above is the supported admin-data path.

### Production SSH and direct database access

No current production shell or database session is documented as verified. Do not claim that either channel is available without a fresh connection check.

### Pagely control panel

The control panel is not connected through this repository. Browser access, if needed, must be verified in the active session.

### Cloudways development server

The old Cloudways setup is historical and was not used as planned. Consult `docs/cloudways-setup.md` only if a future Track B staging task explicitly revives it.

## Capability matrix

| Action | Public REST | Auth REST + Varlock | Browser UI | Pagely SFTP | Notes |
|---|---|---|---|---|---|
| Read published content | Yes | Yes | Yes | No | Public REST is the preferred public readback |
| Read drafts/private status | No | Yes | Yes | No | Keep private content out of public logs |
| Create a draft | No | Guarded | Yes | No | Dry-run, identity check, and draft status required |
| Edit a post, page, or media record | No | Guarded | Yes | No | Snapshot and readback required |
| Change a plugin or WordPress setting | No | Endpoint-dependent | Yes | Sometimes | Requires an exact approved workflow |
| Deploy theme files | No | No | Avoid | Yes | Separate Track B deploy approval required |
| Export the full site or database | No | No | Plugin-dependent | No | No verified full-export channel today |
| Query the database directly | No | No | No | No | Requires separately verified SSH/database access |

## Recommended order of operations

1. Run `make doctor`, then `make status-readonly`.
2. Prefer public REST for observation and authenticated REST through Varlock for exact admin-data work.
3. Before every live write, follow the active issue's dry-run, identity, snapshot, approval, apply, and readback contract.
4. Use browser automation only when the REST path cannot perform or verify the required action.
5. Treat theme merge and theme deployment as separate acts; verify the live public `style.css` after any approved deploy.
