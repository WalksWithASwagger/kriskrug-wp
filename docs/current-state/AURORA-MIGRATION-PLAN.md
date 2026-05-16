# KK Aurora migration plan — staging-first approach

**Decision (KK, 2026-05-15):** "Migrate to staging (Cloudways dev) + iterate before going live."

This doc captures the approach so the next session can execute without re-deciding.

---

## What is KK Aurora?

A complete WordPress 6.9+ Full Site Editing (FSE) block theme, sitting on the `origin/claude/setup-wordpress-rebuild-KVLxh` branch (last commit 2026-01-18, 9 commits ahead of `main`).

**Stack:** vanilla JS + GSAP, ~100KB JS budget, WCAG 2.1 AA, fluid typography, reduced-motion support, dark cyberpunk + Indigenous-wisdom aesthetic.

**Files (on the branch):**
- `theme/kk-aurora/` — full theme: `theme.json`, `style.css`, `functions.php`, `templates/*.html`, `patterns/*.php`, `assets/{css,js}/`. ~3,971 lines, 18 files.
- `theme/kk-aurora.zip` — installable WordPress theme zip
- `demo/index.html` — single-file browser preview (1,004 lines, no server needed). **You can preview at http://127.0.0.1:8765/ while the local Python server is running** (or just `open demo/index.html` from a fresh checkout)
- `theme/kk-aurora/IMPLEMENTATION-PLAN.md` — original design specification
- `THEME-PROPOSALS.md` — prior design proposals
- `COMPLETE-REBUILD-ROADMAP.md` — broader rebuild plan KK and a previous Claude session sketched

**Aesthetic (from the demo):** Deep void background (`#0D0D12`), gradient accents (cyan → teal → purple → pink), glass morphism + glow effects, "Kris Krüg" wordmark top-left, cyan "Let's Talk" CTA button top-right, generous whitespace.

---

## Why staging-first

1. **The branch predates this session's work.** It deletes our `content/drafts/`, `scripts/notion-to-wp/`, and incident postmortem. A direct merge into `main` would break the connector and erase audit + content artifacts.
2. **Catch Responsive has been customized** (per `SITE_INVENTORY.md`, possibly modified locally — needs SSH to verify against upstream). KK Aurora replacing it = some current customizations may not survive.
3. **The classic-theme to FSE-theme jump** changes how widgets, menus, header/footer, and homepage rendering work. Some pages may not render correctly without manual adjustment in the Site Editor.
4. **The 2026-05-15 incident** taught us not to make irreversible production changes without verified backup + dry-run validation.

Staging-first gives us a safe surface to validate the migration without putting the live site at risk.

---

## Staging server: Cloudways dev (24.144.80.107)

Per [`docs/cloudways-setup.md`](../cloudways-setup.md):
- Server IP: `24.144.80.107`
- SSH user: `master_qcteaefabe` (per the setup doc)
- Password OR SSH key auth (KK to confirm which is set up)
- The doc indicates this server already has WordPress installed and is intended as a dev/staging environment

If the server is reachable and KK has SSH credentials, the migration steps below work as written. If not, fall back to **Local by Flywheel** as the staging environment (slower setup but doesn't require the dev server).

---

## Migration steps (when next session starts this work)

### Step 1: Verify the dev server is alive

```bash
ssh master_qcteaefabe@24.144.80.107
# OR via Cloudways web terminal at https://platform.cloudways.com
hostname
ls -la
which wp                      # WP-CLI should be available
wp --info                     # confirm WP version
wp option get siteurl         # confirm what's installed
```

### Step 2: Pull production data into staging

If the dev server doesn't already mirror production, pull a fresh copy:

```bash
# On the dev server, after a Pagely/UpdraftPlus backup is downloaded to /tmp:
wp db import /tmp/kriskrug-prod-db.sql
rsync -avz /tmp/uploads/ wp-content/uploads/
wp search-replace 'https://kriskrug.co' 'https://dev.example.com' --all-tables
```

Alternative: use UpdraftPlus's "migrate to another site" flow if both sites have it installed.

### Step 3: Install KK Aurora on the dev server

```bash
# Get the theme zip onto the dev server (one of three ways):
# (a) Direct from the branch:
git clone https://github.com/WalksWithASwagger/kriskrug-wp.git /tmp/kk-wp-repo
cd /tmp/kk-wp-repo
git checkout claude/setup-wordpress-rebuild-KVLxh
cp theme/kk-aurora.zip /tmp/

# (b) scp from local:
# (run from local) scp /Users/kk/Code/kriskrug-wp-aurora/theme/kk-aurora.zip master_qcteaefabe@24.144.80.107:/tmp/

# (c) Upload via wp-admin → Appearance → Themes → Add New → Upload Theme
```

Then activate:

```bash
cd /path/to/wp/install
unzip /tmp/kk-aurora.zip -d wp-content/themes/
wp theme activate kk-aurora
wp theme list                  # confirm kk-aurora is "active"
```

### Step 4: First-render check

Open the dev server URL in a browser. Verify:
- [ ] Homepage renders without PHP errors
- [ ] At least one blog post renders correctly
- [ ] Header / footer / nav menu render (FSE themes use a different menu system than classic — KK may need to recreate the nav menu in the Site Editor)
- [ ] Featured images display
- [ ] The "Let's Talk" CTA from the demo is wired up (or needs to be)
- [ ] Mobile rendering works

### Step 5: Iteration list

Likely issues that will surface:
1. **Nav menu** — FSE uses a Navigation block. The classic-theme menu won't auto-port. Rebuild via Appearance → Editor → Navigation.
2. **Widgets** — classic widgets (sidebar widgets) don't exist in FSE. If KK was using any (Jetpack search widget, recent posts, etc.), they need to be added as blocks in the relevant template parts.
3. **Custom CSS in Customizer** — Catch Responsive's customizer settings won't transfer. Add as Additional CSS or in the `theme.json` global styles.
4. **Plugin compatibility** — Popup Maker, Zero BS CRM, Site Kit, Jetpack — most should work, but verify each loads cleanly. Popup Maker may need template changes.
5. **Schema mu-plugin** — already deployed via Code Snippets; theme-agnostic, should work.
6. **Pinned/sticky posts on homepage** — FSE templates handle this differently; verify the homepage template shows the right post mix.

### Step 6: Content reflow check

Walk through 5-10 of the most-trafficked posts on the dev server. Verify:
- Long-form posts (3,000+ words) render readably
- Image alignment (full-width, wide, default) all behave
- Pull-quotes, callouts, lists, code blocks all render
- The new schema mu-plugin still injects JSON-LD (no theme-side conflict)

### Step 7: Decide

Three paths after staging works:
- **Ship to production** — backup live, install Aurora on Pagely, activate, monitor
- **Iterate on staging** — KK requests changes; we modify the theme, push to the branch, redeploy to dev
- **Postpone** — staging looks OK but KK isn't ready. Document state, leave dev server with Aurora active for ongoing review

---

## What we ship to production with the migration

When the time comes for the live cutover (after staging is happy):

1. **Backup again** — full UpdraftPlus archive immediately before the theme switch
2. **Install Aurora zip** on production via wp-admin → Appearance → Themes → Add New → Upload
3. **Activate** during a low-traffic window (Sunday morning Pacific is a safe bet)
4. **Smoke test** — homepage, latest 3 posts, About, Contact, Services
5. **Monitor for 24h** — Pagely's stats panel + GSC for crawl errors + KK's user reports
6. **Roll back plan** — Catch Responsive stays installed (just not active). One click in wp-admin reverts. (Per [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) §A.)

---

## What we DON'T do as part of the migration

- **Permalink structure change** — leave at `/YYYY/MM/DD/slug/`. No URL rewrites.
- **Database schema changes** — Aurora is a theme, not a plugin. WP core stays untouched.
- **Plugin removal** — Jetpack, Popup Maker, etc. stay. Plugin housekeeping is a separate session.
- **Content reorganization** — categorization (Phase 2 of ROADMAP) is its own work; doesn't block the theme migration.

---

## Open decisions for next session

1. **Does the Cloudways dev server still exist and have valid SSH credentials?** If not, fall back to Local by Flywheel.
2. **Does KK want to brand-touch the Aurora demo before staging deploy?** (It mentions "Krug" copy that may be from a previous Claude session and could need a verified-facts pass.)
3. **Featured image strategy on the new theme** — does Aurora's hero work with KK's existing featured images, or do new ones need to be commissioned?
4. **The 9 commits on the branch beyond `kk-aurora`** — there's also a "standalone demo page for Discord showcase" commit and "verified facts" knowledge base. Are those still relevant or were they exploratory?
