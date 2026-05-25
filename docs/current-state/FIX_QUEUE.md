# Fix Queue — Prioritized Backlog

**As of:** 2026-05-14 baseline. Reconciled against live evidence on 2026-05-20 and Work metadata re-check on 2026-05-25 in [FIXES-LIVE-RECONCILIATION-2026-05-20.md](FIXES-LIVE-RECONCILIATION-2026-05-20.md).
**Source:** [SEO_AUDIT.md](SEO_AUDIT.md) + [CONTENT_AUDIT.md](CONTENT_AUDIT.md).

Ranked by **impact × effort**. P0 = highest impact / lowest friction. Do these first. Items list dependencies so we don't get tripped up.

**Operating prerequisite for production-visible or destructive changes below**: a target check, rollback note, and explicit deploy path. The strict backup/restore proof gate was retired on 2026-05-22; keep backup work moving as resilience, not as a blanket blocker.

## 2026-05-20 live-state addendum

- P0.1 is no longer a hard gate. Use `make backup-check` when a task needs backup inspection, but do not block ordinary Track A work solely on strict restore proof.
- `backup/2026-05-16/` is useful resilience evidence with known gaps: uploads were skipped and no restore drill is documented.
- P0.2 is still open: `/llms.txt` currently returns `404`.
- P0.3 has changed status: public HTML on homepage, About, Work, and Speaking now includes JSON-LD, so schema appears deployed through the Code Snippets path represented by `fixes/schema-snippets-deployed.php`. Verify in wp-admin before changing schema; do not blindly deploy `schema-snippets.php` over it.
- P0.4 is still open: `/robots.txt` exists but does not yet include the explicit AI-crawler stance from `fixes/robots-txt-update.txt`.
- P0.5/P0.6 are still open: homepage still has duplicate H1 behavior and the most visible pages still contain empty image alts.
- Work page social metadata remains a P0/P1 verification candidate: `/work/` resolves to `/recent-projects-include/`, and the page now emits a non-blank BC+AI ecosystem `og:image` on cache-busted readback.
- Use [FIXES-LIVE-RECONCILIATION-2026-05-20.md](FIXES-LIVE-RECONCILIATION-2026-05-20.md) before deploying any January-era `fixes/` file.

---

## P0 — do these first (high impact, low effort)

### P0.1 — Improve backup resilience [**NOT A BLOCKING GATE — INCIDENT 2026-05-15**]
- **Why:** Backups still matter, but the strict restore-proof gate is no longer allowed to clog ordinary publishing. The 2026-05-15 overwrite incident is addressed primarily through slug-based idempotency, dry-runs, target checks, and rollback notes; backup work remains the resilience layer.
- **Path:** UpdraftPlus (via wp-admin) → download archive → drop in `backup/YYYY-MM-DD/` → restore drill into Local by Flywheel.
- **Effort:** 1–2 hours.
- **Dependencies:** none.
- **Done when:** `backup/YYYY-MM-DD/` contains DB + themes + plugins + uploads archive AND `manifest.md` AND a `restore-notes.md` proving local restore works.
- **Blocks:** nothing by itself. High-blast-radius work should still choose an appropriate backup/snapshot path before execution.

### P0.2 — Add `llms.txt` at site root
- **Why:** Zero-cost AI-discoverability win. Curated map for ChatGPT, Claude, Perplexity browsing.
- **Path:** Take template from `fixes/llms-txt-template.md`, fill in verified URLs (BC + AI association URL, Indigenomics.ai, social handles), drop at server root via SSH/SFTP, OR use the mu-plugin rewrite approach from the template.
- **Effort:** 30 min (template is ready).
- **Dependencies:** target path and rollback note.
- **Verify:** `curl -i https://kriskrug.co/llms.txt` returns 200 + `Content-Type: text/plain`.

### P0.3 — Verify deployed schema and decide whether to migrate to mu-plugin
- **Current status:** Public HTML now appears to include the deployed Code Snippets schema path. Treat this as verification/migration work, not a first deploy.
- **Why:** Single highest-leverage SEO + AI change. Adds `Person`, `WebSite`, `Article`, `BreadcrumbList`, `Service` schema sitewide.
- **Path:**
  1. Verify constants in `fixes/schema-snippets.php` (LinkedIn, X, YouTube, headshot URL, BC + AI URL — all marked `VERIFY` in the file).
  2. Drop file into `wp-content/mu-plugins/kk-schema.php` (SSH/SFTP).
  3. Test with [Google Rich Results Test](https://search.google.com/test/rich-results) on homepage + a post + a service page.
- **Effort:** 1–2 hours (mostly verifying constants and rich-results testing).
- **Dependencies:** target path and rollback note.
- **Done when:** Person, WebSite, Article schemas all validate.
- **Note:** This supersedes `fixes/issue-39-schema-markup.php` (which has narrower scope and a stale org URL).

### P0.4 — Update `robots.txt` with AI-crawler stance
- **Why:** Explicit > implicit. Pick the "Be Cited" stance (recommended) so all AI crawlers know they're welcome.
- **Path:** Replace robots.txt with Option A from `fixes/robots-txt-update.txt`.
- **Effort:** 15 min.
- **Dependencies:** target path and rollback note.
- **Verify:** `curl https://kriskrug.co/robots.txt` + Google Search Console robots.txt tester.

### P0.5 — Fix the empty H1 + duplicate H1 problem on homepage
- **Why:** Confuses crawlers about page's main topic. The current state — empty H1 + "Why Choose Me?" — sends a noisy signal.
- **Path:** Edit theme template (`front-page.php` or `home.php` in a child theme — Catch Responsive). Replace logo wrapper from `<h1>` to `<p class="site-title">`. Set page H1 to a descriptive heading (e.g. the page title or first content heading).
- **Effort:** 30 min in a child theme.
- **Dependencies:** target path and rollback note; ideally do in a Local by Flywheel copy first.

### P0.6 — Add `alt` text to homepage hero + About page portrait
- **Why:** First-impression images are the most-shared and most-AI-cited. Empty `alt` makes them invisible to Google Images, Pinterest, AI image search.
- **Path:** wp-admin → Media → find each image → fill in `Alt Text` with descriptive sentence (not keyword stuffing).
- **Effort:** 30 min for the 5 most-visible.
- **Dependencies:** target path and rollback note.

### P0.7 — Fix the two empty-title pages (3930 and 2808)
- **Why:** They're in your sitemap with no title. Either fix or `noindex`.
- **Path:** Open each in wp-admin, set title (or trash/redirect if no longer needed).
- **Effort:** 15 min.
- **Dependencies:** target path and rollback note.

### P0.8 — Remove duplicate Pinterest verification meta tag
- **Why:** Two `p:domain_verify` tags is ugly and one of them is wrong/stale.
- **Path:** Find where each is being injected (likely one from Jetpack settings, one from a manual `<head>` snippet or Site Kit). Remove the stale one.
- **Effort:** 15–30 min to track down source.
- **Dependencies:** target path and rollback note.

**P0 total: ~5–8 hours of work for huge AI/SEO gains.**

---

## P1 — do these in the second week

### P1.1 — Install Rank Math (or SEOPress) for per-page SEO control
- **Why:** Today the SEO surface is Jetpack's SEO Tools module (it's what generates current meta descriptions and OG tags — confirmed by the `<!-- Jetpack Open Graph Tags -->` marker). Rank Math gives finer per-page control plus FAQ block plus a schema validator.
- **Path:**
  1. wp-admin → Jetpack → Settings → Traffic → **turn off "Search Engine Optimization"** (Jetpack's SEO Tools). Note: this will remove Jetpack's meta description handling, so do this immediately before step 2.
  2. wp-admin → Plugins → Add New → Rank Math → install + activate → run setup wizard.
  3. **Disable Rank Math's schema module** in the wizard (we're handling Person/Article/Service/Breadcrumb in the mu-plugin). Let it handle meta, OG, Twitter Cards.
  4. Spot-check 5 pages to confirm meta descriptions still render and aren't duplicated.
- **Effort:** 2 hours including the setup wizard and reviewing top 20 pages' meta.
- **Dependencies:** P0.3 (so schema isn't double-injected).
- **Watch out:** Running both Jetpack SEO Tools AND Rank Math at once will produce duplicate `<title>` and meta tags. Either run Jetpack SEO + our schema, OR Rank Math + our schema — but not all three sources for the same tags.

### P1.2 — Categorize the 101 recent posts
- **Why:** 99% in `Misc` = no topical authority signal. After this, the site has clear clusters Google and LLMs can reason about.
- **Path:**
  1. Create categories (see CONTENT_AUDIT §2.2 for the proposed 9). wp-admin → Posts → Categories.
  2. Bulk-edit posts in pages of 20: select → Quick Edit → assign category. Use the search filter to bulk-process by topic (e.g. search "vancouver" + apply Vancouver AI category).
  3. Keep `Misc` for true outliers.
- **Effort:** 3–4 hours.
- **Dependencies:** target path and rollback note.

### P1.3 — Fix the multilingual welcome pages
- **Why:** 7 variants + 1 duplicate + 0 hreflang = SEO confusion.
- **Path:** Two routes:
  - **Route A (formal):** Install Polylang. Set each variant as a translation of an English master. Polylang generates hreflang. Add language switcher in header.
  - **Route B (informal):** `noindex` each variant. Delete the Swahili duplicate. Add a single switcher widget pointing to them as fun easter eggs.
- **Effort:** 2-4 hours (Route A) or 30 min (Route B).
- **Dependencies:** target path and rollback note.

### P1.4 — Add `alt` text to the 100 most recent posts' featured images + in-line images
- **Why:** Recent posts get the most traffic and citations. Highest-leverage image-SEO target.
- **Path:** Either manual sweep (slow) or use a vision-LLM tool (e.g. AI Engine for WordPress, or a custom script using Claude API) to draft alt text in batches, then KK reviews and approves.
- **Effort:** 4-8 hours manually; 1 hour + review with LLM-assist.
- **Dependencies:** target path and rollback note.

### P1.5 — Rewrite long titles to fit 60-char SERP window
- **Why:** 5 of 17 audited titles are over 60 chars; they truncate in Google.
- **Path:** wp-admin → edit each long-title page → adjust to `{Page} | Kris Krüg` pattern. Use Rank Math's "snippet preview" to see SERP-rendered.
- **Effort:** 1-2 hours for the 34 pages.
- **Dependencies:** P1.1 (Rank Math gives the snippet preview).

### P1.6 — Audit the existing `fixes/` directory against post-audit state
- **Why:** 12 staged fixes were prepared in Jan 2026. Some now overlap with new schema/SEO work. Avoid duplicate or conflicting deploys.
- **Path:** Read every file in `fixes/`. Mark each: 🟢 deploy as-is, 🟡 needs update, 🔴 obsolete-replace.
- **Effort:** 1 hour.
- **Dependencies:** none.

---

## P2 — do these in the third week

### P2.1 — Restructure information architecture (parent/child pages)
- **Why:** Flat 34-page hierarchy doesn't communicate priorities.
- **Path:** Follow the IA proposal in CONTENT_AUDIT §4. Move pages under parents in wp-admin. Set up 301 redirects for any renamed slugs (Rank Math has a built-in redirect module).
- **Effort:** 1-2 days.
- **Dependencies:** P1.1 (for the redirect manager), P1.2 (so categories are in place).
- **Cross-reference with P0.3:** The schema mu-plugin's Service emitter is keyed off a `kk_service_audience` post_meta value, NOT slugs — so renaming `ai-upgrade-for-modern-media-leaders` → `services/ai-upgrade-media/` does NOT break the Service schema. **But:** if you migrate to a different schema implementation (e.g. Rank Math's Service schema) before P2.1, double-check the new implementation isn't slug-bound either, or you'll silently lose rich results on those pages after rename.

### P2.2 — Build the missing pillar pages
- **Why:** Topic clusters need anchor pages so categories aren't naked.
- **Path:** Create:
  - `/bc-ai/` — BC + AI association landing
  - `/web-summit-vancouver/` — annual recurring coverage
  - `/vancouver-ai-meetup/` — meetup recap collection
  - `/press/` — media kit
- **Effort:** 1 day of writing + page setup.
- **Dependencies:** P2.1.

### P2.3 — Add FAQ blocks to service pages
- **Why:** `FAQPage` schema is one of the most reliable rich-snippet triggers; AI Overviews quote FAQs heavily.
- **Path:** wp-admin → edit each AI Upgrade page → add an FAQ block at the bottom → 5-8 Q&As per service.
- **Effort:** 2-3 hours per service page × 4 pages = ~half day.
- **Dependencies:** P1.1 (Rank Math FAQ block is the simplest).

### P2.4 — Add `PodcastSeries` schema to MØTLEYKRÜG page
- **Why:** Apple Podcasts, Spotify, and Google all surface podcast structured data. Currently invisible.
- **Path:** Extend `kk-schema.php` mu-plugin with a PodcastSeries block. Each episode page gets PodcastEpisode.
- **Effort:** 2-3 hours.
- **Dependencies:** P0.3.

### P2.5 — Stale-content sweep (publications, workshop, events)
- **Why:** Audit flagged three pages whose currency wasn't verified.
- **Path:** Read each. Either refresh, archive (noindex), or trash with 301 to a successor.
- **Effort:** 1 hour each.
- **Dependencies:** none.

### P2.6 — Tag cleanup
- **Why:** 124 unique tags on recent posts. Some are near-duplicates.
- **Path:** wp-admin → Tags → sort by count → merge low-volume (<3 uses) duplicates into the dominant tag.
- **Effort:** 2 hours.
- **Dependencies:** P1.2.

---

## P3 — nice-to-haves / strategic

### P3.1 — `llms-full.txt` with full content of top 10 evergreen pages
- **Why:** Some LLMs read this; faster than parsing HTML; preserves your canonical wording.
- **Path:** Concat Markdown of top 10 pages into a single file at `/llms-full.txt`. Auto-generate via a small WP-CLI command or a build script.
- **Effort:** 2-4 hours setup; minutes to regenerate.
- **Dependencies:** P0.2.

### P3.2 — Theme migration to a modern block theme (or refresh Catch Responsive)
- **Why:** Catch Responsive is from 2023, classic-theme architecture, heavy CSS/JS, hard to control headings/markup. A block theme (or a child theme on a leaner classic theme like Blocksy / Kadence / Frost) modernizes markup and speeds up the site.
- **Effort:** 2-4 weeks of careful migration. Not P0 because risk is high.
- **Dependencies:** Multiple full backups; Local by Flywheel test environment.

### P3.3 — Old post triage (pre-2024)
- **Why:** 840 posts in the long tail. Some are still useful, some are dead, some are wrong link targets.
- **Path:** Pull GA4 data → keep top 50 → noindex bottom 700 → 301-redirect duplicates to canonical pieces.
- **Effort:** 1-2 days with traffic data.
- **Dependencies:** GA4 access.

### P3.4 — Author bio + related-posts blocks on every post
- **Why:** E-E-A-T signal, dwell-time signal, internal-linking signal.
- **Path:** Theme template or a plugin like Co-Authors Plus + a related-posts plugin (Jetpack has one — already on).
- **Effort:** 2 hours.
- **Dependencies:** none.

### P3.5 — Lighthouse / Core Web Vitals pass
- **Why:** Heavy theme + jQuery + Popup Maker is likely costing INP. CWV is a ranking factor.
- **Path:** Run Lighthouse → identify worst offender → dequeue / defer / replace.
- **Effort:** Variable; 1 day for a meaningful pass.
- **Dependencies:** target path and rollback note.

### P3.6 — Hreflang for English variants
- **Why:** If P1.3 goes the formal route, extend to mark the main site as `en-CA` or `en-US` and any future translations.
- **Effort:** half day.
- **Dependencies:** P1.3.

---

## Items intentionally NOT in this queue

- **Switching permalink structure** from `/YYYY/MM/DD/slug/` to `/slug/` — too risky for the ranking benefit. Existing structure is fine.
- **Removing Jetpack** — site relies on it for sitemap, OG, search, stats. Don't rip out until a replacement is fully in place.
- **Migrating away from Pagely** — no SEO reason to.
- **Rebuilding the 7 multilingual welcome pages from scratch** — keep them as art (Route B in P1.3) unless there's a real audience case.

---

## How to use this queue

1. **One P0 per session** until P0 is done. They're small and independent enough to ship individually.
2. **Backup before every change** during the P0 sprint (the changes are small, but discipline first).
3. **After each change**, run the appropriate validator:
   - Schema: https://search.google.com/test/rich-results
   - Robots: Google Search Console robots.txt tester
   - General: `curl` the page and grep the head for what you expected to add
4. **Mark items done in this file** as we go (or move them to `docs/current-state/CHANGELOG.md` once we start one).
