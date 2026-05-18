# Resume here — 2026-05-17 handoff

**Last session ended:** 2026-05-17, after Track A + Track B parallel work landed.
**Author:** Claude Code working with KK across an intensive multi-session push (2026-05-15 → 2026-05-17).

This doc is the **single thing to read first** when picking up. It complements but doesn't replace:
- [`ROADMAP.md`](ROADMAP.md) — the 3-month plan written 2026-05-15 (still good, partially executed)
- [`TWO-TRACK-MODEL.md`](TWO-TRACK-MODEL.md) — Track A vs Track B operating split
- [`SITE-AUDIT-2026-05-16.md`](SITE-AUDIT-2026-05-16.md) — reader-facing punch list with completion notes

---

## Where we are (snapshot)

### Track A — Content + SEO (lives on `main`)
**Health: green.** Both recent flagship posts are live and richly enriched. 7 of 7 top SITE-AUDIT items shipped. Reader-facing audit + mobile baseline + nav deep-inspect are all committed.

What's live:
- **Make Culture, Not Content** (`/2026/05/16/make-culture-not-content/`) — 34K chars, 5 illustrative slides, pull-quote, 58 em-dashes purged, internal + external cross-links
- **Your Taste Is Your Moat** (`/2026/05/15/your-taste-is-your-moat/`) — 23K chars, 10 visuals (5-photo LaSalle gallery near top, 5 keynote slides interspersed), YouTube embed at top, pull-quote, hyperlinks
- **Homepage** — new H1 ("Kris Krüg, Generative AI for Creative Professionals"), rewrote hero copy from 2018 event-photographer positioning to current AI-educator voice. "Why Choose Me?" demoted from H1 to H2.
- **About page** — 3 inner H1s demoted to H2 (`Publications`, `Portraits`, `Clients`)
- **Beehiiv popup** — delay changed from 1s → 30s (Popup Maker post 3884). Visitors get to read before being interrupted.
- **Redirection plugin installed.** Two new 301s live: `/work/` → `/recent-projects-include/` (was bouncing to a 2011 UN HIV post); `/services/` → `/generative-ai-services/` (was 404)
- **YouTube embed spacer fix** on Your Taste — stripped `wp-has-aspect-ratio` to kill Jetpack's phantom 438px spacer

### Track B — Aurora v2 redesign (lives on `aurora/v2`, pushed to origin)
**Health: staging is up.** Aurora rebased onto current `main`, theme cherry-picked from the stale 4-month-old branch without erasing Track A's work.

What exists:
- Branch `origin/aurora/v2` with 2 commits on top of `main`: theme + demo + next-session playbook
- `theme/kk-aurora/` — full WP 6.9+ FSE block theme, 23 files, installable zip at `theme/kk-aurora.zip`
- `demo/index.html` — 1,004-line standalone browser preview
- Local by Flywheel site `kriskrug-local` running with production DB (944 posts), Aurora installed + activated
- Local URL: `http://localhost:10003/` or `http://kriskrug-local.local`
- Admin: user `kk` / pass `kk` at `http://localhost:10003/wp-admin/`
- Images are broken (uploads not in backup) — expected

### Infrastructure / safety
- **Backup ✓** — UpdraftPlus full backup on 2026-05-16 (db 4.7MB + plugins 62MB + themes 15MB + mu-plugins 52KB + others 1.5MB) in `backup/2026-05-16/` with SHA-256 manifest. Uploads 13GB skipped.
- **Schema ✓** — Person, WebSite, Article, BreadcrumbList, Service JSON-LD all live via [`fixes/schema-snippets-deployed.php`](../../fixes/schema-snippets-deployed.php) (Code Snippet id 5)
- **Connector ✓** — `scripts/notion-to-wp/kk_notion_to_wp.py` with hardened safety guards (slug-based idempotency, title-similarity check, CREATE default). Auto-link + em-dash purge baked in via `text_polish.py`
- **Categorization ✓** — 102 recent posts in 9 real categories (was 99% Misc)

---

## What's open — ranked by leverage

### Track A — open punch list (in `SITE-AUDIT-2026-05-16.md`)

Ordered roughly by leverage / effort ratio:

1. **🟡 Title separator filter** (5-line Code Snippet) — every page title currently reads *"PageName Kris Krüg | Site Title"* with no delimiter. Hooks `document_title_parts` and inserts ` | ` between page name and site name. Site-wide fix in 10 minutes.
2. **🟡 Twitter → X URL search-replace** — `twitter.com/feelmoreplants` is HTTP 520 on every page that links it. Sitewide search-replace to `x.com/kriskrug`. Run via WP-CLI dry-run first, then real.
3. **🟢 Broken Link Checker scan** — install the plugin (free), run a one-shot scan, export the dead-link CSV, triage. 13–30% rot rate on older curated pages per audit round 2 sampling.
4. **🟢 Sidebar widget order** — on mobile, all sidebar widgets stack BELOW post content. Audit which widgets matter, remove the rest, OR defer to Aurora.
5. **🟢 Mobile popup variant** — current 30s timer is desktop-tuned; mobile users hit the modal mid-scroll through long posts. Either disable on mobile in Popup Maker → Display Presets, or add a scroll-based trigger.
6. **🟢 Personal phone QA pass** — visual mobile audit needs your actual phone (Brave's MCP window won't shrink below ~600px). Walk homepage + a recent post + About, flag layout breaks.
7. **🟢 Lighthouse mobile run** — separate Chrome DevTools session with 3G throttle; capture LCP/INP/CLS. Concrete numbers will quantify how much Catch Responsive's stack costs you.
8. **🟢 Stewart Butterfield testimonial** decision — keep / re-caption with "then-CEO of Slack" / rotate to a newer testimonial. Needs your call.
9. **🟢 Image alt-text vision-LLM batch** (ROADMAP Phase 4) — top-100 most-trafficked images, generate alt, CSV for review, REST batch-update. Massive accessibility + AI-search win when you're ready.
10. **🟢 GSC Performance capture** — open GSC → Performance → last 16 months, note top queries / impressions / CTR. Needed to measure whether categorization + recency improvements moved the needle.

### Track B — Aurora v2 next steps

You need to look at it first. Then:

**Tier 1 (look-and-feel sign-off):**
- A1. Open Aurora staging in your browser (`http://localhost:10003/`) and walk a few key pages. React: does the aesthetic match what you want? Anything that needs to go?
- A2. Decide between **iterate-on-Aurora** or **fresh start** (the Vercel question below opens that door).
- A3. Browse the FSE Site Editor (`Appearance → Editor` in Local's wp-admin) to see Aurora's templates and patterns up close.

**Tier 2 (only if A2 = iterate-on-Aurora):**
- B1. Rebuild the nav menu in the FSE Site Editor (classic-theme menus don't auto-port to FSE; you have to recreate via Navigation block)
- B2. Smoke-test every post type — long-form (Your Taste), embed-heavy (Make Culture with YouTube + gallery), photo-heavy (About), short (early Field Notes posts)
- B3. Test plugin compatibility — Jetpack, Popup Maker, Site Kit, Redirection, Code Snippets all should work, but verify each. Schema mu-plugin is theme-agnostic so it should be fine.
- B4. Recreate any Catch Responsive Customizer settings you depended on, as `theme.json` overrides or Additional CSS
- B5. Production cutover plan: low-traffic Sunday morning Pacific, fresh backup immediately before, Catch Responsive stays installed-but-inactive for one-click rollback ([`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) §A)

**Tier 3 (production cutover):**
- C1. Backup
- C2. Upload `theme/kk-aurora.zip` to production via wp-admin → Themes → Add New → Upload
- C3. Activate during cutover window
- C4. 24-hour monitoring (Pagely stats + GSC + browser smoke)
- C5. If anything breaks: one-click rollback to Catch Responsive

---

## The Vercel question (new — just authorized 2026-05-17)

Vercel auth landed at end of session. KK didn't specify the intended use. Three branches to consider:

### Branch 1: Headless WordPress + Next.js on Vercel
**What:** kriskrug.co stays on Pagely as the content-management backend. Front-end becomes a Next.js app on Vercel that fetches content via WP's REST API (or WPGraphQL) and renders fully on the edge.
**Pros:** Modern stack, much faster (edge cache), no theme constraints, Aurora becomes irrelevant (Vercel app IS the design system), strong SEO via static + ISR, easier to iterate on UI with normal React tooling.
**Cons:** Larger lift than Aurora theme migration. Need to port post layouts, comment system, search, related-posts widget, popup, Jetpack integrations (or replace them). Pagely costs continue alongside Vercel hosting.
**Right call when:** you decide Aurora's FSE-theme approach is too limiting or KK Aurora isn't quite the design direction. Resets the redesign clock but unlocks much more.

### Branch 2: Microsites + landing pages on Vercel
**What:** kriskrug.co keeps its WP theme (Catch or Aurora). Vercel hosts standalone microsites for specific properties (event landing pages, TheUpgrade.ai course funnels, BC + AI ecosystem subdomain, etc.).
**Pros:** Doesn't disturb the main site. Modern stack where it benefits most (campaign-velocity pages where iteration speed matters). Cheap.
**Cons:** Doesn't move the kriskrug.co needle directly.
**Right call when:** you have a specific microsite need that doesn't fit comfortably in WordPress.

### Branch 3: Edge functions for kriskrug.co webhooks/integrations
**What:** Use Vercel for serverless functions only — e.g., the Notion → WP connector becomes a Vercel webhook receiver instead of a local Python CLI. Or sitemap-generation, analytics aggregation, etc.
**Pros:** Minimal commitment. Solves "I want to publish from Notion automatically" without server admin overhead.
**Cons:** Small scope. Doesn't change the design or the front-end story.
**Right call when:** you want incremental automation without changing the substrate.

**Recommended decision frame for next session:**
- Look at Aurora on Local first
- If Aurora delights you → keep going on Track B as planned. Vercel sits in Branch 3 (small-scope automation only).
- If Aurora feels constraining → explore Branch 1 (headless + Next.js on Vercel) as the actual v2.
- Don't decide before seeing Aurora rendered.

---

## Things waiting on KK input (small)

These unblock specific items but aren't blockers for the bigger arcs:

- LinkedIn URL confirmation — schema currently references `linkedin.com/in/kriskrug` which 404s (needs your actual handle)
- Real headshot upload for Person schema `image` field
- Stewart Butterfield testimonial decision (see Track A item 8 above)
- Vercel use-case clarification — which branch above (or different entirely)
- Whether to push the `aurora/v2` PR to GitHub as a draft for discussion (`https://github.com/WalksWithASwagger/kriskrug-wp/pull/new/aurora/v2` is one-click)
- Whether to rename `/recent-projects-include/` → `/work/` permanently (would tighten the URL and make the new 301 unnecessary)

---

## Operating notes for the next session

### Branches + commits
- `main` is for Track A (content/SEO). Push as you go.
- `aurora/v2` is for Track B. Push to the same branch as iterations land.
- Don't merge Track B back into main until cutover (that IS the cutover).
- Local main is currently in sync with origin (last commit `ed77f3e`).

### Connector
- `scripts/notion-to-wp/kk_notion_to_wp.py` — fully hardened. CREATE is default; UPDATE requires `--update`; title similarity check ≥0.5; em-dash purge + auto-link via `text_polish.py` run automatically.
- README at `scripts/notion-to-wp/README.md` covers usage. LINK_MAP for auto-linking is in `text_polish.py` — add to it as new pillar posts publish.

### Backups
- `backup/2026-05-16/` has the snapshot taken right before all this session's work. Don't touch it. Make a fresh one before any Aurora cutover.
- `backup/2026-05-16/manifest.md` is tracked in git; the archives themselves are gitignored.

### Security warning to flag
- The sub-agent runtime flagged the `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` trailer as a fabricated model name / authorship misrepresentation. Every commit this session uses it. Two reasonable resolutions: (a) keep using it, KK is OK with the convention, no consumer of this repo cares; (b) drop the trailer or use a more conservative `Co-Authored-By: Claude <noreply@anthropic.com>`. Don't amend pushed commits to "fix" this — that rewrites history. New commits going forward can use whichever convention KK prefers.

### Chrome MCP
- Brave is authorized. Use it freely.
- Window resize is capped at ~600px minimum — true mobile-width screenshots require KK's actual phone or Chrome DevTools.
- `localhost` is in the extension allowlist for navigation (per this session's evidence — the `localhost:10003` navigate failed with `permission_required`); if you need to preview Local sites via Chrome MCP, may need an explicit extension whitelist tweak.

### Computer-use
- Permission flow has been flaky for KK this session — granting via System Settings appears to work, then the tool reports not granted. If you hit this loop, surface it once and pivot to non-computer-use paths rather than retrying repeatedly. Most things have a Bash/MCP equivalent.

### WP credentials
- `scripts/notion-to-wp/.env` has `WP_USER=wpadmin5102` and `WP_APP_PASSWORD=O1l8 sNC5 niIx 9IvI Sxfz N2EU` (strip spaces for Basic auth). Stored locally, gitignored. Use for any REST PATCH operations.
- Posts published via the connector should be assigned to author id 1 (kk) so the byline reads "Kris Krüg".

---

## Critical files index

**Authoritative state docs (read in this order to onboard):**
1. [`RESUME-HERE.md`](RESUME-HERE.md) — this file
2. [`AGENT-SWARM-OPERATING-PLAN-2026-05-18.md`](AGENT-SWARM-OPERATING-PLAN-2026-05-18.md) — current lanes for issue swarms, draft publishing, Aurora, and content/nav structure
3. [`TWO-TRACK-MODEL.md`](TWO-TRACK-MODEL.md) — how Track A vs Track B work
4. [`SITE-AUDIT-2026-05-16.md`](SITE-AUDIT-2026-05-16.md) — punch list (closed + open) with deep-inspect findings
5. [`AURORA-MIGRATION-PLAN.md`](AURORA-MIGRATION-PLAN.md) — Track B's playbook (refreshed with rebase-first instructions)
6. [`ROADMAP.md`](ROADMAP.md) — 3-month plan, partially executed (use as backlog reference)
7. [`POST-ENRICHMENT-2026-05-16.md`](POST-ENRICHMENT-2026-05-16.md) — what changed on the two flagship posts

**Reference docs (when needed):**
- [`TRAFFIC-DIAGNOSTIC-2026-05-15.md`](TRAFFIC-DIAGNOSTIC-2026-05-15.md) — why traffic is what it is + highest-leverage fixes
- [`SEO_AUDIT.md`](SEO_AUDIT.md) + [`CONTENT_AUDIT.md`](CONTENT_AUDIT.md) — May 8 baseline (some items now resolved)
- [`SITE_INVENTORY.md`](SITE_INVENTORY.md) — plugin/theme/page inventory
- [`BACKUP_PLAN.md`](BACKUP_PLAN.md) + [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md)
- [`INCIDENT-2026-05-15-overwritten-post.md`](INCIDENT-2026-05-15-overwritten-post.md) — the connector incident postmortem
- [`FIX_QUEUE.md`](FIX_QUEUE.md) — older granular fix backlog

**Working dirs:**
- `scripts/notion-to-wp/` — connector + `text_polish.py` polish module
- `fixes/` — schema PHP, planned CSS/PHP fixes
- `content/drafts/` — Notion → WP staging area (gitignored except for the staged-publishes)
- `backup/2026-05-16/` — UpdraftPlus archive manifests
- `theme/kk-aurora/` (on `aurora/v2` branch only) — the v2 theme
- `docs/current-state/` — all the state docs above

**External:**
- Live site: `https://kriskrug.co/`
- Aurora staging: `http://localhost:10003/` (Local by Flywheel, site `kriskrug-local`)
- Repo: `https://github.com/WalksWithASwagger/kriskrug-wp`
- Aurora PR draft (one-click): `https://github.com/WalksWithASwagger/kriskrug-wp/pull/new/aurora/v2`

---

## Suggested first-30-minutes when resuming

1. Read this file (5 min)
2. Open Aurora staging in your browser (or via `Open site` in Local) and react (10 min)
3. Look at `SITE-AUDIT-2026-05-16.md` "Track A in-progress" section to confirm you saw the homepage + About fixes (5 min)
4. Decide:
   - **Track B verdict** (iterate on Aurora? abandon for Vercel headless? something else?)
   - **Track A next move** (the title separator filter is the cheapest leverage; takes 10 minutes)
   - **Vercel direction**
5. Tell the next Claude session your call; it picks up from item 1 of whichever track and goes.

---

## What this doc deliberately does NOT cover

- Strategic positioning / business direction beyond what's in current site copy — that's your call, not an auditor's
- Pricing decisions on Services / Generative AI Services page
- Notion knowledge base hygiene (separate workstream owned elsewhere)
- bc-ai.ca + indigenomics.ai — separate properties, not in scope
- Email / Beehiiv funnel design beyond the popup-trigger fix
- The MØTLEYKRÜG podcast production stack
- Any of KK's other AI consulting / coaching work

---

*This doc lives. Edit it when you finish work or when state changes. Future-you will thank present-you.*
