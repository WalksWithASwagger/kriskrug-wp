# Roadmap — Next 3 Months

**As of:** 2026-05-15
**Reads from:** [`FIX_QUEUE.md`](FIX_QUEUE.md), [`SEO_AUDIT.md`](SEO_AUDIT.md), [`CONTENT_AUDIT.md`](CONTENT_AUDIT.md), [`INCIDENT-2026-05-15-overwritten-post.md`](INCIDENT-2026-05-15-overwritten-post.md)

Six phases, ~2 weeks each. Each phase has a single shipping theme so progress is legible. Effort is rough; "S" ≈ half-day, "M" ≈ 1–2 days, "L" ≈ 3–5 days.

---

## Phase 0 — Insurance (THIS WEEK, blocker for everything else)

The 2026-05-15 incident proved we have to do this before more production changes.

| Item | Effort | Notes |
|---|---|---|
| Install UpdraftPlus + run first full backup | M | Per [`BACKUP_PLAN.md`](BACKUP_PLAN.md) Path B. Download archive to local `backup/YYYY-MM-DD/` |
| Verify restore drill into Local by Flywheel | M | Per [`BACKUP_PLAN.md`](BACKUP_PLAN.md) "restore drill" section. The backup isn't real until it's been restored at least once |
| Schedule recurring backups | S | UpdraftPlus daily → cloud destination (Dropbox / S3 / Drive) |

**Phase 0 done when:** `backup/<date>/manifest.md` + `restore-notes.md` confirm a successful local restore.

---

## Phase 1 — Quick AI/SEO wins (weeks 1–2)

Low-effort high-impact items that mostly close out FIX_QUEUE P0.

| Item | Effort | Source | Notes |
|---|---|---|---|
| Deploy `/llms.txt` | S | FIX_QUEUE P0.2 | Template in `fixes/llms-txt-template.md`. Verify URLs (BC + AI, Indigenomics, social handles) before publishing |
| Update `robots.txt` with explicit AI-crawler stance | S | FIX_QUEUE P0.4 | Two options in `fixes/robots-txt-update.txt`. "Be cited" is the recommended stance |
| Fix homepage H1 (currently empty + "Why Choose Me?" duplicate) | M | FIX_QUEUE P0.5 | Theme template fix in a Catch Responsive child theme |
| Add LinkedIn URL + headshot to Person schema | S | INCIDENT follow-up | KK confirms his actual LinkedIn URL; upload a real headshot to media library; edit the Code Snippets snippet |
| Rename "Untitled" Code Snippet → "KK Schema" | S | Cosmetic | wp-admin → Snippets → edit |
| Remove duplicate Pinterest verification meta tag | S | FIX_QUEUE P0.8 | Track down which integration is double-emitting |
| Fix two empty-title pages (IDs 3930, 2808) | S | FIX_QUEUE P0.7 | Open in wp-admin; set titles OR trash if no longer needed |
| Add real alt text to homepage hero + About page portrait | S | FIX_QUEUE P0.6 | Highest-leverage 5 images, manual |

**Phase 1 done when:** `curl https://kriskrug.co/llms.txt` returns 200 with our template; `robots.txt` lists AI crawlers explicitly; homepage has a single, descriptive H1; Person schema validates with `image` + LinkedIn `sameAs`.

---

## Phase 2 — Content infrastructure (weeks 3–4)

Foundations that make everything else easier. Right now 99% of posts are uncategorized, making topical authority invisible to Google + LLMs.

| Item | Effort | Source | Notes |
|---|---|---|---|
| Create 9 proposed categories | S | CONTENT_AUDIT §2.2 | `vancouver-ai-ecosystem` already exists from the Calling Us All In post. Add the other 8 |
| Categorize the 101 recent posts (2024+) | M | FIX_QUEUE P1.2 | Bulk-edit in wp-admin using search-by-keyword to batch-tag |
| Build pillar landing pages | L | CONTENT_AUDIT §3 | `/bc-ai/`, `/vancouver-ai-meetup/`, `/web-summit-vancouver/`, `/press/` |
| Restructure IA: parent/child hierarchy | M | FIX_QUEUE P2.1 | Move pages under parents per CONTENT_AUDIT §4. Set up 301 redirects on renamed slugs |
| Fix multilingual welcome pages | M-L | FIX_QUEUE P1.3 | Either Polylang + hreflang (formal) or `noindex` the 7 variants (informal) |

**Phase 2 done when:** every recent post has a real category; pillar pages live and indexed; multilingual variants are either properly linked via hreflang or `noindex`d.

---

## Phase 3 — SEO control + per-post optimization (weeks 5–6)

Once content is categorized, take per-post control of the SEO surface.

| Item | Effort | Source | Notes |
|---|---|---|---|
| Install Rank Math; disable Jetpack SEO Tools | S | FIX_QUEUE P1.1 | The two will conflict if both active; pick one path. Disable Rank Math's schema module (the mu-plugin handles it) |
| Audit Jetpack SEO meta across all 941 posts | L | `issues-to-create/jetpack-seo-audit-all-posts.md` | File the issue, then run the inventory CSV. Hand-curate top 20 by traffic, auto-derive long tail using the connector's `derive_excerpt` / `derive_seo_title` |
| Rewrite long titles (≥60 chars) to fit SERP window | M | FIX_QUEUE P1.5 | ~5 of the 34 pages today; Rank Math's snippet preview shows the truncation |
| Add FAQ blocks to the 4 AI Upgrade service pages | M | FIX_QUEUE P2.3 | 5–8 Q&As per service page. Triggers `FAQPage` rich-snippet eligibility |

**Phase 3 done when:** every page has a controlled SEO title + meta description; FAQ schema validates on service pages; long titles no longer truncate in SERPs.

---

## Phase 4 — Connector hardening (weeks 7–8)

Pay back the connector debt from the 2026-05-15 incident. Make the next 50 publishes boring.

| Item | Effort | Source | Notes |
|---|---|---|---|
| Add unit tests for safety guards | M | INCIDENT follow-up | Use the May-15 collision as a fixture ("Web Summit Vancouver 2026" vs "Calling Us All In" should produce similarity ≈ 0.16 < 0.5 → abort) |
| Add `--diff` mode | M | INCIDENT follow-up | Show unified diff between existing post and proposed payload when `--update` is used. Belt-and-suspenders on top of similarity check |
| Post-publish verification step | S | INCIDENT follow-up | After CREATE, GET the post and confirm slug + title + date match what was sent. Catch silent backend rewrites |
| Image alt text via vision-LLM batch | M | FIX_QUEUE P1.4 | Run a vision model over 100 most-recent post images, generate alt text, KK reviews in batches. Massive accessibility + AI-search win |
| Connector graduates to a Claude Code skill | S | scripts/notion-to-wp/README.md | Auto-trigger on "publish my Notion post to kriskrug.co" |

**Phase 4 done when:** publishing a Notion post is one command + a confirm; the next 10 publishes happen without any production scare.

---

## Phase 5 — Content pipeline ramp (weeks 9–10)

Use the now-hardened connector to actually ship at cadence.

| Item | Effort | Notes |
|---|---|---|
| Establish weekly publish cadence | ongoing | Pick a day (Monday?), commit to it. The connector + the Notion content database make this routine |
| Build PodcastSeries + PodcastEpisode schema for MØTLEYKRÜG | M | FIX_QUEUE P2.4. Apple Podcasts + Spotify both surface this |
| Backfill `kk_service_audience` post-meta on the 4 service pages | S | The Service schema in the mu-plugin already supports this — just needs the wp-admin custom field set on each page |
| Stale-content sweep on the page set | S | FIX_QUEUE P2.5. Publications, Workshop, Events — refresh, archive, or redirect |
| Tag cleanup | S | FIX_QUEUE P2.6. 124 unique tags on recent posts; merge near-duplicates |

**Phase 5 done when:** 4 new posts have shipped via the connector in 4 weeks without incident; podcast page has structured data; tags are tidy.

---

## Phase 6 — Polish + measure (weeks 11–12)

Confirm we moved the needle. Decide what's next.

| Item | Effort | Notes |
|---|---|---|
| Deploy `llms-full.txt` with top-10 evergreen content | M | FIX_QUEUE P3.1. Auto-generated from the post list. Refresh quarterly |
| Lighthouse + INP pass | M | FIX_QUEUE P3.5. Catch Responsive + Jetpack JS likely costing performance. Identify and dequeue worst offenders |
| Old-post triage (pre-2024 long tail) | L | FIX_QUEUE P3.3. Pull GA4 top 50; `noindex` the bottom 700; 301-redirect duplicates |
| Author bio + related-posts blocks on every post | S | FIX_QUEUE P3.4. E-E-A-T signal, dwell-time signal |
| **Report card:** GSC clicks, AI Overviews appearances, Bing referrals, brand searches | S | Quick read of what changed since 2026-05-15 |

**Phase 6 done when:** we have a written before/after comparison. The decision for Q3 plans itself.

---

## What's intentionally NOT in this roadmap

- **Migrating to a block theme.** Catch Responsive is classic and old, but a theme migration is a 3-week project with high regression risk. Cost > benefit until we've finished the content infrastructure work.
- **Switching permalink structure.** The `/YYYY/MM/DD/slug/` pattern is dated but works; rewriting URLs across 941 posts is the kind of "improve everything" project that delivers nothing for a month and breaks half the inbound links if mismanaged.
- **A theme child + custom code rebuild.** Same reasoning. The schema mu-plugin handles the highest-leverage piece (structured data) without touching the theme.
- **Multi-site (kriskrug.co + bc-ai.ca shared admin).** Cool idea, not P0.

---

## How to use this roadmap next session

Two ways:
1. **Work from the roadmap directly.** Open this file, pick the next un-checked item from Phase 0 (Insurance), and start. Each item names its source doc so context is one click away.
2. **Turn it into GitHub issues.** For each row in a phase, file an issue using `issues-to-create/` as the staging area, then `gh issue create -F ...`. Pros: trackable in the issues board, can assign to agents. Cons: more ceremony.

Either works. The roadmap stays authoritative; issues are just a different *view* of the same items. Don't double-track.

---

## Open follow-ups not yet roadmapped

These need a decision before they get a phase:

- **31 sitemap errors in GSC** — flagged in the Sitemaps view but not investigated yet. Worth a half-day diagnostic session (likely stale URLs from posts that got slug-changed/trashed, like the original Web Summit 2026 path)
- **Headshot in Person schema** — needs a real photo uploaded; one-line fix in the snippet once the URL exists
- **LinkedIn URL** — `linkedin.com/in/kriskrug` is 404; KK to confirm actual handle
- **Other social accounts** — KK to confirm YouTube, GitHub presence (audit found those 404 too)
- **The 12 staged fixes in `fixes/issue-*.{css,php,md}`** — preserved from a January batch; need a review pass to decide deploy-as-is vs. update vs. obsolete-replace
