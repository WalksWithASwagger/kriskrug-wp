# Agent Swarm Operating Plan — 2026-05-18

**Purpose:** Turn the current issue backlog, draft-post pipeline, Aurora redesign, and content/nav audits into work lanes that agents can safely execute in parallel.

**Current repo baseline at planning time:** `main` was synced to `origin/main`; Track A lives on `main`; Track B lives on `aurora/v2`. Normalized on 2026-05-25, GitHub shows 66 open issues, 44 of which still carry the historical `auto-implement` label.

---

## Executive Read

The backlog is big, but it is not one clean queue. It contains:

- stale January issues from the old GitHub Actions agent-swarm era,
- duplicate issues,
- items already completed by the May 2026 Track A work,
- broad strategy epics that need scoping before implementation,
- a real near-term Track A cleanup queue,
- a real Track B redesign queue.

The best next move is not "turn the whole queue loose." The best next move is a controlled swarm with clear lanes, read/write boundaries, and one serialized publisher/cutover lane for anything that touches production WordPress.

---

## Operating Assumptions

1. **Do not mix tracks in one worker.**
   - Track A: content, SEO, redirects, schema snippets, draft publishing, nav/content cleanup on `main`.
   - Track B: Aurora theme, FSE templates, theme.json, staging/cutover on `aurora/v2`.

2. **Production writes are serialized.**
   - Many agents can audit, draft, validate, and prepare patches.
   - One publisher agent applies WordPress REST/wp-admin changes after dry-run, target checks, and an explicit rollback path. Full backup is still preferred for bulk, plugin, theme, schema, or destructive work, but it is no longer a blanket blocker for create-only draft/review work.

3. **Aurora should move fast, but not blind.**
   - `aurora/v2` is real and contains the theme.
   - Local staging at `http://localhost:10003/` is not currently running from this shell.
   - No cutover until rendered staging is verified on real content.

4. **Draft-post work should mostly continue before redesign.**
   - Publishing current posts helps recency and gives Aurora more real content to test.
   - Hold only visually important launch/portfolio posts if Aurora cutover is genuinely 24-48 hours away.

5. **The old `.github/agents/` swarm is dormant.**
   - Issue #69 and the old automation docs should not drive current work unless the project explicitly revives that system.

---

## Where The Draft-Post Pipeline Stands

Four recent posts from the previous publishing push are already live:

| Post | WP ID | Status | Local evidence |
|---|---:|---|---|
| `Calling Us All In` | 11765 | live | `content/drafts/2026-05-14-calling-us-all-in/` |
| `Web Summit Vancouver 2026` | 11826 | live restored/recreated | `content/drafts/2026-05-07-web-summit-vancouver-2026/` |
| `Your Taste Is Your Moat` | 11178 | live, enriched | `content/drafts/wp-draft-11178-post-11178/` |
| `Make Culture, Not Content` | 10594 | live, enriched | `content/drafts/wp-draft-10594-post-10594/` |

Authenticated WordPress REST counts normalized on 2026-05-25 show:

| Surface | Count | Notes |
|---|---:|---|
| Published posts | 944 | Public corpus |
| Draft posts | 71 | Current draft pile; requires private editorial triage before rescue |
| Published pages | 34 | Public pages |
| Draft pages | 5 | Old placeholders/page projects |

The next local/Notion candidates are not already present in WordPress by exact slug:

| Candidate | Current verdict |
|---|---|
| `sovereign-ai-for-whom` | Strongest next candidate, but high-risk and needs fact-check/human review |
| `why-we-built-the-responsible-ai-professional-certification` | Useful but must be compared against live RAP post `11620` first |
| `comox-valley-ai-is-becoming-its-own-thing` | Promising community recap, but needs editorial cleanup, links, and image decision |

The older authenticated WP draft queue should get a private editorial triage lane before rescue. Do not commit the full admin draft-title inventory to this public repo.

---

## Aurora Redesign Roadmap

Current Track B state:

- Branch: `aurora/v2` / `origin/aurora/v2`
- Worktree: `.claude/worktrees/agent-aec50fddbd7207f80`
- Theme: `theme/kk-aurora/`
- Installable zip: `theme/kk-aurora.zip`
- Demo: `demo/index.html`
- No open PR for `aurora/v2`
- Old branch `origin/claude/setup-wordpress-rebuild-KVLxh` remains archival; do not merge it.

Fast path:

1. Restart or recreate staging.
   - Preferred for speed: Local by Flywheel.
   - Alternate: Cloudways dev if credentials and target install are confirmed.

2. Install `theme/kk-aurora.zip` from `aurora/v2`.

3. Smoke-test real content:
   - `/`
   - `/about/`
   - `/2026/05/15/your-taste-is-your-moat/`
   - `/2026/05/16/make-culture-not-content/`
   - `/2026/05/14/calling-us-all-in/`
   - `/2026/05/07/web-summit-vancouver-2026/`

4. Validate mechanics:
   - FSE navigation block
   - header/footer
   - CTA links
   - featured images
   - galleries
   - YouTube embeds
   - Popup Maker behavior
   - Jetpack
   - Site Kit
   - Redirection
   - Code Snippets schema
   - mobile layout
   - console errors

5. Decision gate:
   - If Aurora feels right, iterate on `aurora/v2`, open a draft PR, and plan cutover.
   - If Aurora feels too heavy, use PR #74 preview pages as design-direction input before deciding whether to pivot.

6. Cutover gate:
   - Fresh backup immediately before activation.
   - Catch Responsive stays installed for rollback.
   - Activate during low-traffic window.
   - Smoke test homepage, latest posts, About, Contact, Services.
   - Monitor 24 hours.

---

## Backlog Triage

### Close Or Update First

These should be handled before broad issue swarms start, otherwise agents will chase ghosts.

| Issue(s) | Recommended action | Reason |
|---|---|---|
| #1 | close as duplicate of #2 | exact duplicate |
| #2 | update/close with proof | `/services/` now redirects to `/generative-ai-services/` |
| #6 | update/close with proof | popup delay changed 1s to 30s |
| #12, #66 | update/possibly close | homepage hero/H1 work shipped; verify whether positioning is now enough |
| #13, #14, #15 | consolidate | overlap with page-level issues #65-#68 |
| #23 | update/close | 102 recent posts categorized into 9 real categories |
| #37 | close as stale | sitemap exists through Jetpack; new work is GSC diagnostics, not sitemap creation |
| #39 | close as superseded | schema is live via Code Snippet id 5 |
| #69 | close or reframe | old GitHub Actions swarm is dormant under the current operating model |

### Keep But Scope

| Issue(s) | Lane |
|---|---|
| #4, #40 | image alt-text and image SEO batch |
| #5, #8, #9, #46-#48 | accessibility audit/patch lane |
| #36, #38, #43, #45 | SEO metadata/link/social feed lane |
| #49-#58 | marketing strategy/docs lane, not code-first |
| #59-#64 | archive/portal discovery lane, needs scope reduction |
| #65-#68 | page-content improvement lane |
| #24-#35 | Track B/Aurora design lane only |

---

## First Swarm Slate

### Lane 0 — Queue Hygiene

**Goal:** Make GitHub reflect current reality so future swarms do not waste time.

**Write scope:** GitHub issue comments/state only.

**Tasks:**
- Comment on #1, #2, #6, #12, #23, #37, #39, #66 with doc-backed status.
- Close duplicates/completed issues where acceptance is satisfied.
- Re-label Track B design issues so they do not get implemented on `main`.
- Reframe #69 as historical/dormant or close it.

**Worker prompt:**
```
You are operating in WalksWithASwagger/kriskrug-wp. Refresh live issue state against docs/current-state. For each assigned issue, comment with evidence from current-state docs and recommend close, keep, or re-scope. Do not edit code. Do not close unless acceptance is clearly satisfied.
```

### Lane 1 — Track A Quick Fixes

**Goal:** Ship high-leverage current-site fixes that do not depend on Aurora.

**Write scope:** prepared snippets/docs first; production write only through publisher.

**Tasks:**
- Title separator Code Snippet.
- Twitter/X replacement plan and dry-run count.
- Broken-link scan plan and CSV output.
- Mobile popup recommendation.
- Verify remaining empty-title/Pinterest/meta issues before declaring obsolete.

**Worker prompt:**
```
Inspect docs/current-state/SITE-AUDIT-2026-05-16.md and the live site. Prepare a minimal Track A fix pack for title separators, stale Twitter/X links, and broken-link scan. Produce exact snippets/commands, verification commands, and rollback notes. Do not touch production.
```

### Lane 2 — Draft Publishing Relaunch

**Goal:** Restart the Notion-to-WP cadence with the hardened connector and separate the old WP admin draft queue from the current Notion batch.

**Write scope:** local draft artifacts only until publisher approval.

**Tasks:**
- Inventory Notion candidate posts and compare each against authenticated WordPress `status=any` by slug.
- Dry-run the next 3-5 candidates.
- Privately triage the 32 existing WordPress admin drafts by ID/title/readiness without committing private draft dumps to GitHub.
- For each generated draft pack, review body, images, alt text, SEO, links, category/tags.
- Prepare publish-ready checklists.

**Worker prompt:**
```
Work in scripts/notion-to-wp and content/drafts. For assigned Notion pages, run dry-run only, then review generated post.html, seo-meta.md, alt-text.md, and internal-links.md. Use authenticated read-only WordPress only for slug/status checks and private draft triage. Produce a publish-readiness report. Do not publish or update WordPress.
```

### Lane 3 — Connector Hardening

**Goal:** Make future publishing boring.

**Write scope:** `scripts/notion-to-wp/`, tests/docs.

**Tasks:**
- Fix README idempotency drift.
- Add tests for title-similarity guard and em-dash polish.
- Add `--diff` mode for guarded updates.
- Add post-publish verification GET.
- Consider graduating connector to a repo skill after the next successful batch.

**Worker prompt:**
```
Own scripts/notion-to-wp only. Add focused tests/docs for connector safety after the 2026-05-15 incident. Keep changes small. Do not change live WordPress data. Preserve existing CLI behavior except for documented safety improvements.
```

### Lane 4 — Aurora Staging

**Goal:** Get the redesign rendered on real content and decide fast.

**Write scope:** `aurora/v2` branch/worktree only.

**Tasks:**
- Start/recreate Local by Flywheel or Cloudways staging.
- Install `theme/kk-aurora.zip`.
- Smoke-test real posts and pages.
- Capture screenshots under `docs/current-state/aurora-smoke-YYYY-MM-DD/`.
- Open a draft PR for `aurora/v2` after smoke starts.

**Worker prompt:**
```
Work only on aurora/v2. Do not edit main. Bring up Aurora staging, install theme/kk-aurora.zip, and smoke-test homepage, About, Your Taste, Make Culture, Calling Us All In, and Web Summit. Record screenshots/findings in docs/current-state. No production activation.
```

### Lane 5 — Content/Nav Structure

**Goal:** Decide and prepare the structural changes KK mentioned.

**Write scope:** docs and prepared issue drafts first.

**Tasks:**
- Propose final top nav for current theme and Aurora.
- Decide `/recent-projects-include/` vs permanent `/work/`.
- Decide `/events/` upcoming-first vs archive.
- Plan pillar pages: `/bc-ai/`, `/vancouver-ai-meetup/`, `/web-summit-vancouver/`, `/press/`.
- Plan multilingual welcome-page handling.

**Worker prompt:**
```
Read CONTENT_AUDIT.md, SITE-AUDIT-2026-05-16.md, and live nav pages. Propose a concrete navigation/IA update plan with exact URL changes, redirect needs, and which changes should wait for Aurora. Do not modify WordPress.
```

### Lane 6 — Accessibility And Image SEO

**Goal:** Convert broad accessibility tickets into verifiable work.

**Write scope:** audit report and prepared patches.

**Tasks:**
- Re-audit #5, #8, #9, #46-#48 against live site.
- Inventory image alt-text gaps for top pages/recent posts.
- Generate reviewable alt-text CSV, not direct media updates.
- Prepare CSS/snippet patches only where live violations are confirmed.

**Worker prompt:**
```
Take an audit-first stance. Verify current accessibility/image issues on the live site before proposing patches. Produce evidence, affected URLs, recommended fix, and verification method. Do not update production media or theme files.
```

### Lane 7 — Archive/Marketing Scoping

**Goal:** Reduce the very broad strategy epics into implementable projects.

**Write scope:** docs/issue drafts.

**Tasks:**
- Break #49-#58 into strategy/docs deliverables.
- Break #59-#64 into archive/portal discovery deliverables.
- Identify data sources, owners, and minimum viable public surfaces.

**Worker prompt:**
```
Do not implement a portal. Scope the archive/marketing issues into realistic first deliverables, required source material, and acceptance criteria. Produce issue comments or draft child issues.
```

---

## Recommended Sequence

### Next 24 Hours

1. Lane 0: clean/update the issue queue.
2. Lane 4: restart Aurora staging and capture first smoke screenshots.
3. Lane 2: inventory the next Notion posts and the private WP draft queue; dry-run only.
4. Lane 3: fix connector README drift and add first safety tests.

### Next 3 Days

1. Decide Aurora direction after seeing the rendered staging site.
2. Ship Track A title/Twitter/link hygiene if Aurora cutover is not immediate.
3. Prepare 3-5 publish-ready draft packs.
4. Open a draft PR for `aurora/v2`.

### Next 1-2 Weeks

1. Cut over Aurora if staging and KK review are good.
2. Publish at least 2 more posts through the hardened pipeline.
3. Convert stale GitHub issues into a smaller current queue.
4. Start IA/pillar-page work against the new design or confirmed current theme.

---

## Human Decisions Needed

- Should `/recent-projects-include/` become `/work/` permanently?
- Should `/events/` be upcoming-first, archive-first, or split?
- Should the Stewart Butterfield testimonial stay, be re-captioned, or be replaced?
- Should multilingual welcome pages be formal translations or noindexed creative artifacts?
- Does Aurora's current visual direction feel right after rendered staging review?
- Are there specific Notion pages KK wants in the next publishing batch?

---

## Safety Checklist For Any Production Writer

Before a production WordPress write:

1. Confirm the task is Track A, not Track B.
2. Confirm backup posture and rollback path.
3. Run dry-run or prepare exact patch/snippet.
4. Verify target by slug/ID/title before PATCH.
5. Keep a local artifact of the before/after.
6. Apply one change type at a time.
7. Curl or browser-verify the live result.
8. Update the relevant current-state doc or issue comment.
