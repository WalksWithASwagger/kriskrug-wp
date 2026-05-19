# Internal Linking Strategy - Issue #38

**Date:** 2026-05-18
**Lane:** Track A content + SEO
**Scope:** Report-only strategy artifact for GitHub issue #38, "[SEO] Implement Internal Linking Strategy."
**Production status:** No WordPress writes, no theme edits, no connector run.

## Issue #38 Success Criteria

Issue #38 asks for a stronger internal-linking system:

| Acceptance criterion | Strategy translation |
|---|---|
| All pages have 2-5 internal links | Every page should link up to its parent hub, sideways to related pages/posts, and forward to one clear next action. |
| Important pages have 5+ links | About, Work/Projects, Services, Speaking, Blog, Events, Contact, and new topic pillars should each act as hubs with 5+ contextual internal links. |
| No orphaned pages | Every published page and priority post should have at least one inbound link from nav, a hub page, a related post, or footer/sidebar. |
| All pages reachable within 3 clicks | Top nav/footer to hubs, hubs to cluster pages/posts, posts back to hubs. |
| Anchor text descriptive | Use intent-rich anchors like "AI keynote speaking", "Vancouver AI meetup recaps", "BC + AI work", not "click here". |
| Related content cross-linked | Each topic cluster gets bidirectional links between pillar, recent posts, evergreen posts, and commercial/booking surfaces. |
| Session duration increased | Measurement depends on GA4/Jetpack Stats access and remains human-gated. |

## Source Surfaces Inspected

Primary required docs:

- `AGENTS.md`
- `docs/current-state/README.md`
- `docs/current-state/TWO-TRACK-MODEL.md`
- `docs/current-state/REPO_STATE.md`
- `docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`
- `docs/current-state/SEO_AUDIT.md`
- `docs/current-state/CONTENT_AUDIT.md`
- `docs/current-state/SITE_INVENTORY.md`

Supporting current-state docs:

- `docs/current-state/TRAFFIC-DIAGNOSTIC-2026-05-15.md`
- `docs/current-state/NAV-IA-DECISION-PACK-2026-05-18.md`
- `docs/current-state/OWNED-SITES-LINKING-RECOMMENDATION-2026-05-18.md`
- `docs/current-state/POST-ENRICHMENT-2026-05-16.md`
- `docs/current-state/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md`
- `docs/current-state/FIX_QUEUE.md`
- `docs/current-state/POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md`
- GitHub issue #38 via `gh issue view 38`

Local evidence:

- `docs/current-state/raw/pages.json`
- `docs/current-state/raw/posts-page1.json`
- `docs/current-state/raw/posts-page2.json`
- `docs/current-state/raw/categories.json`
- `docs/current-state/raw/tags.json`
- `scripts/notion-to-wp/text_polish.py`
- `scripts/notion-to-wp/README.md`
- Existing local link audits:
  - `content/drafts/2026-05-07-web-summit-vancouver-2026/internal-links.md`
  - `content/drafts/2026-05-14-calling-us-all-in/internal-links.md`
  - `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/internal-links.md`
  - `content/drafts/2026-05-13-sovereign-ai-for-whom/internal-links.md`
  - `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/internal-links.md`
  - `content/drafts/wp-draft-11178-post-11178/links.txt`
  - `content/drafts/wp-draft-10594-post-10594/links.txt`

Not inspected in this pass:

- wp-admin page editor screens
- authenticated WordPress database/link table
- GA4, Jetpack Stats, or Google Search Console behavior data
- a full live crawl of all 900+ posts
- production edits after 2026-05-18 unless represented in repo docs

## Current Link-Graph Baseline

The audits agree on the failure mode:

- The site has 34 published pages in the May 14 public snapshot, all top-level.
- The May 14 public category snapshot shows only `Misc` and `Oil Spill`; later docs note a few real categories were started, but the corpus remains largely uncategorized.
- The public archive has roughly 900+ posts, with the recent AI/community material concentrated in 2023-2026.
- `CONTENT_AUDIT.md` explicitly did not complete a full internal link graph.
- `SEO_AUDIT.md` flags internal linking/navigation as a weak surface and calls out the flat page hierarchy.
- `TRAFFIC-DIAGNOSTIC-2026-05-15.md` identifies the internal link graph as the secondary SEO lever after categorization.
- Local draft link audits show uneven internal-link coverage:
  - `web-summit-vancouver-2026`: 5 internal links, good start for a cluster post.
  - `calling-us-all-in`: 2 internal links.
  - `sovereign-ai-for-whom`: 1 internal link.
  - `why-we-built-the-responsible-ai-professional-certification`: 1 internal link.
  - `comox-valley-ai-is-becoming-its-own-thing`: 0 internal links.
  - `wp-draft-11178-post-11178/links.txt` and `wp-draft-10594-post-10594/links.txt`: empty local audit files even though later docs say the posts were enriched live.
- `scripts/notion-to-wp/text_polish.py` has a useful starter `LINK_MAP`, but it is term-based, not a complete cluster strategy.

## Priority Hub Pages

These are the pages that should receive and distribute the most internal link equity.

| Priority | Hub | Current URL | Status | Role in the graph |
|---|---|---|---|---|
| P0 | About | `/about/` | Existing | Entity hub for Kris Krug, credibility, current roles, and project network. |
| P0 | Work / Projects | `/recent-projects-include/` now, future `/work/` pending decision | Existing, awkward slug | Portfolio hub for BC + AI, speaking portals, AI projects, Indigenomics, and selected proof. |
| P0 | Services | `/generative-ai-services/` with `/services/` redirect noted in docs | Existing | Commercial hub linking to AI media, creative, coaching, workshop, speaking, testimonials, and contact. |
| P0 | Speaking | `/speaking/` | Existing and recently strengthened | Speaking/keynote hub; should link to talk portals, companion essays, testimonials, events, and contact. |
| P0 | Blog / Writing | `/blog/` | Existing but template has no H1 in audit | Archive hub for topic clusters and recent writing. |
| P0 | Contact | `/contact/` | Existing | Conversion endpoint linked from services, speaking, work, and high-intent posts. |
| P1 | Vancouver AI | Proposed `/vancouver-ai/` or `/vancouver-ai-meetup/` | Not yet created | Collection for Vancouver AI meetup recaps and BC ecosystem posts. |
| P1 | BC + AI | Proposed `/bc-ai/` | Not yet created | Personal-role page for KK's BC + AI work, linking out to `bc-ai.ca` with context. |
| P1 | Web Summit Vancouver | Proposed `/web-summit-vancouver/` | Not yet created | Evergreen annual coverage hub linking 2024, 2025, and 2026 Web Summit posts. |
| P1 | AI for Creatives | Proposed `/ai-for-creatives/` or service-child route | Not yet created | Bridge between creative AI posts and the creative professionals offer. |
| P1 | AI for Media | Proposed `/ai-for-media/` or service-child route | Not yet created | Bridge between journalism/media posts and the media leaders offer. |
| P2 | Podcast | `/motleykrug-podcast/` | Existing | Series hub for interviews, guest spots, and audio/video work. |
| P2 | Press | Proposed `/press/` | Not yet created | Media kit, bios, headshots, citations, and booking proof. |
| P2 | Worldview | `/the-kk-worldview/`, possible future `/worldview/` | Existing | Philosophy/entity reinforcement hub. |
| P2 | Reconciliation | `/reconciliation-indigenous-land-acknowledgement/`, possible future `/reconciliation/` | Existing | Values hub, especially for Indigenous tech and Indigenomics content. |

## Recommended Link Graph

Use a hub-and-spoke graph with bidirectional links:

1. Site spine: top nav and footer point to `About`, `Work`, `Services`, `Speaking`, `Events`, `Blog`, `Podcast`, and `Contact`.
2. Hub pages point down to their cluster posts/pages.
3. Cluster posts point back up to the hub.
4. Cluster posts cross-link to 2-3 sibling posts.
5. High-intent posts point to the relevant conversion page.

### Entity And Conversion Spine

| From | Link to | Anchor pattern | Why |
|---|---|---|---|
| About | Work / Projects | `current AI projects` or `project network` | Turns identity into proof. |
| About | Speaking | `AI keynote speaking` | Routes event/booker intent. |
| About | Services | `generative AI services` | Routes commercial intent. |
| About | Reconciliation | `reconciliation and Indigenous land acknowledgement` | Makes values visible and reachable. |
| Work / Projects | Services | `AI strategy and creative services` | Converts proof into inquiry. |
| Work / Projects | Speaking | `keynote portals and talks` | Connects project artifacts to stage work. |
| Services | Testimonials | `client testimonials` | Adds proof near conversion. |
| Services | Contact | `start a project conversation` | Clear next action. |
| Speaking | Contact | `book Kris for a keynote` | Primary conversion. |
| Speaking | Work / Projects | `current AI work` | Shows speaker proof beyond a speaking page. |
| Blog posts | About | `Kris Krug` | Entity reinforcement. |
| Blog posts | Contact | `bring Kris into your organization` | Only on high-intent posts; avoid spammy repetition. |

### Vancouver AI / BC + AI Cluster

Target hub: create `/vancouver-ai/` or `/vancouver-ai-meetup/`, then create `/bc-ai/` if KK wants a personal-role page separate from the external association.

Priority posts to link into the hub:

- `/2025/05/18/bc-ai-is-live-and-were-building-the-future-we-actually-want/`
- `/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/`
- `/2025/05/11/vancouver-ai-meetup-16-where-tech-creativity-and-community-collide/`
- `/2025/04/19/vancouvers-ai-how-grassroots-innovation-is-reshaping-british-columbias-tech-future/`
- `/2025/03/02/vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap/`
- `/2025/02/02/vancouver-ai-january-2025-recap-one-year-of-creative-rebellion-open-source-disruption/`
- `/2024/12/31/ais-next-chapter-notes-from-bcs-ai-ecosystem/`
- `/2024/12/28/system-check-vancouver-ai-community-meetups-december/`
- `/2024/10/10/future-proof-inside-vancouvers-thriving-ai-ecosystem/`
- `/2024/07/08/creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights/`
- `/2024/06/02/june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines/`
- `/2023/12/27/2024-vancouver-ai-community-meetups/`
- `/2023/11/20/empowering-community-in-the-ai-era-fostering-authentic-connections-and-creative-collaboration/`
- `/2023/10/20/vancouver-ai-community-lunch-meetup-fostering-community-in-vancouvers-budding-ai-landscape/`
- `/2023/10/05/teasing-the-launch-vancouver-ai-community-meetup/`

Recommended pattern:

- Hub links to the latest 6 recaps, then a chronological archive.
- Each recap links back to the hub using `Vancouver AI meetup recaps`.
- Each recap links sideways to the previous and next recap when available.
- BC + AI founding/strategy posts link to `Work`, `About`, and the external `bc-ai.ca` site.

### Web Summit Vancouver Cluster

Target hub: create `/web-summit-vancouver/`.

Priority posts:

- `/2026/05/07/web-summit-vancouver-2026/`
- `/2025/04/13/web-summit-vancouver-2025-survival-guide/`
- `/2024/09/05/the-outsiders-insider-guide-to-web-summit-vancouver/`
- `/2024/08/22/web-summit-vancouver-2025-and-how-you-can-shape-it/`
- `/2024/06/19/blog-rise-of-the-vancouver-technopunks-hosting-the-web-summit-on-our-terms/`

Recommended pattern:

- Hub explains the annual coverage and links each year/guide.
- Every Web Summit post links to the hub using `Web Summit Vancouver coverage`.
- Older posts should link forward to the 2026 post where context is still relevant.
- The 2026 post already has 5 internal links; keep it as the model for this cluster.

### AI For Creatives Cluster

Target hub: create `/ai-for-creatives/` or route through the existing `/ai-upgrade-for-creative-professionals/` offer until a hub exists.

Priority posts/pages:

- `/ai-upgrade-for-creative-professionals/`
- `/generative-ai-workshop-for-artists-creatives/`
- `/2026/05/04/punk-rock-ai/`
- `/2026/01/24/both-hands-full/`
- `/2026/05/15/your-taste-is-your-moat/`
- `/2026/05/16/make-culture-not-content/`
- `/2025/03/30/a-creative-technologists-ai-age-manifesto/`
- `/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/`
- `/2025/04/07/we-dont-do-panels-we-do-portals/`
- `/2024/11/22/great-creative-reckoning-a-techartists-manifesto-on-generative-artificial-intelligence/`
- `/2024/10/28/kicking-ass-in-2025-a-techartists-guide-to-creative-survival/`
- `/2024/07/19/fuck-the-status-quo-ais-messy-love-child-with-creativity/`

Recommended pattern:

- Creative offer page links to 3-5 proof essays.
- Proof essays link back to the offer with contextual anchors like `AI workshops for creative teams`.
- `Punk Rock AI`, `Both Hands Full`, `Your Taste Is Your Moat`, and `Make Culture, Not Content` should cross-link as one creative AI keynote/proof cluster.
- `scripts/notion-to-wp/text_polish.py` already links several of these terms; expand only after final hub URLs exist.

### AI For Media / Journalism Cluster

Target hub: use `/ai-upgrade-for-modern-media-leaders/` now; create `/ai-for-media/` only if KK wants a separate editorial landing page.

Priority posts/pages:

- `/ai-upgrade-for-modern-media-leaders/`
- `/2025/06/24/what-journalists-need-to-know-about-ai-right-now/`
- `/2025/07/08/ai-training-for-media-pr-and-creative-professionals/`
- `/2025/12/11/vancouver-tech-journal-isnt-journalism/`
- `/2023/10/31/deconstruct-your-business-model-on-a-lean-canvas-google-news-initiative-launch-lab-week-two-report/`
- `/2023/10/26/mapping-the-blueprint-the-genesis-of-a-media-venture-google-news-initiative-pre-launch-lab/`
- `/2023/10/26/embarking-on-a-digital-news-voyage-week-1-recap-of-the-google-news-initiative-pre-launch-lab/`
- `/2023/10/23/embarking-on-a-media-revolution-my-participation-in-the-google-news-initiative-pre-launch-lab/`

Recommended pattern:

- Media offer page links to journalism/training posts as proof.
- Journalism posts link back to the media offer using `AI training for media leaders` or similar.
- Add one link from this cluster to `Speaking` for media conference/booker intent.

### Responsible AI / Ethics Cluster

Target hub: no new hub until the RAP duplication question is resolved; temporarily use `/the-kk-worldview/`, `/reconciliation-indigenous-land-acknowledgement/`, and the live RAP/certification post as anchors.

Priority posts/pages:

- `/the-kk-worldview/`
- `/reconciliation-indigenous-land-acknowledgement/`
- `/2026/04/17/applied-ethical-ai-responsible-ai-professional-certification-rap/`
- local draft `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/`
- `/2026/02/03/name-the-bias/`
- `/2025/06/09/ai-ate-the-future/`
- `/2025/03/09/transcending-techs-darker-impulses/`
- `/2024/12/20/fears-hopes-and-dreams-for-our-relationship-with-ai/`
- `/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/`
- `/2023/10/22/ais-true-threats-corporate-control-centralization-of-power-and-cultural-adaptation/`

Recommended pattern:

- Do not publish the RAP draft until the live RAP post relationship is resolved.
- Ethics posts should link to `Worldview`, `Reconciliation`, and one commercial/service page only when the post naturally supports a training offer.
- RAP/certification posts should cross-link with descriptive anchors, not duplicate each other's role.

### Indigenous Tech / Reconciliation Cluster

Target hub: use `/reconciliation-indigenous-land-acknowledgement/` now; consider an Indigenomics section on Work before creating a standalone page.

Priority posts/pages:

- `/reconciliation-indigenous-land-acknowledgement/`
- `/recent-projects-include/`
- `/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/`
- `/2024/11/14/indigenomics-now-2024-redefining-the-future-of-indigenous-economic-and-digital-sovereignty-through-ai/`
- `/2024/10/15/indigenous-innovation-in-technology-and-the-future-of-indigenous-economies/`
- local draft `content/drafts/2026-05-13-sovereign-ai-for-whom/`

Recommended pattern:

- Indigenomics posts link to `Reconciliation` and `Work`.
- The Work page links to the external `indigenomics.ai` with context.
- Do not create or rename pages here without KK review because the topic is values-sensitive.

### Podcast / Conversations Cluster

Target hub: `/motleykrug-podcast/`.

Priority posts/pages:

- `/motleykrug-podcast/`
- `/podcast-guesting-page-epk/`
- `/2025/03/01/shane-gibsons-ai-sales-dojo/`
- `/2025/01/25/human-biography-podcast-w-sharad-khare/`
- `/2024/12/17/generative-ai-cinematic-podcasts-how-kevin-friel-is-hacking-the-future-of-media/`
- `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/`
- `/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/`

Recommended pattern:

- Podcast page lists or links notable episodes/appearances.
- Guesting/EPK page links to Speaking, Podcast, About, and Contact.
- Interview posts link back to Podcast or Guesting depending on user intent.

## Minimum Link Rules

Use these rules for every future Track A content edit:

1. Every pillar or page gets 5+ internal links.
2. Every standard page gets 2-5 contextual internal links.
3. Every new post gets:
   - one link up to a hub,
   - two links to sibling posts,
   - one link to About, Work, Services, Speaking, or Contact when intent fits.
4. Every cluster hub links to 6-12 high-priority child posts/pages, then to an archive/category page if available.
5. Avoid self-links and avoid linking headings.
6. Use exact, descriptive anchors:
   - Good: `Vancouver AI meetup recaps`, `AI keynote speaking`, `Responsible AI Professional certification`
   - Weak: `read more`, `here`, `this post`
7. Prefer body-copy links over sidebar-only links for SEO weight.
8. Preserve external links where they provide evidence, but each long post should have at least 2 internal links before publish.

## Quick Wins

These can be prepared without changing production, then applied by a publisher session after backup/target checks.

| Quick win | File/surface | Recommendation |
|---|---|---|
| Fix the zero-link Comox draft | `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/internal-links.md` | Add links to Vancouver AI/BC + AI posts, community-building posts, and Work or Contact before any publish attempt. |
| Strengthen RAP draft before publish decision | `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/` | Add links to the live RAP post, ethics/worldview material, and media/creative training surfaces, but only after duplicate-risk review. |
| Build the Sovereign AI bridge | `content/drafts/2026-05-13-sovereign-ai-for-whom/` | Add links to Reconciliation, Indigenomics-related posts, BC + AI, Web Summit, and Work. Human review required before publishing. |
| Use Web Summit as the model cluster | `content/drafts/2026-05-07-web-summit-vancouver-2026/internal-links.md` | Its 5 internal links are the closest existing local example of a cluster graph; older Web Summit posts should link forward and back when edited. |
| Update `LINK_MAP` after hubs exist | `scripts/notion-to-wp/text_polish.py` | Add final canonical hub URLs for `Vancouver AI`, `BC + AI`, `Web Summit Vancouver`, `AI for Creatives`, and `AI for Media` only after URLs are confirmed. |
| Add hub links to page copy | About, Work, Services, Speaking, Blog, Events | When those pages are next edited, add contextual links to the hub graph. Keep nav/footer changes separate from body copy changes. |
| Create a tracking checklist before production work | Future issue comment or follow-up doc | Track page/post URL, desired inbound links, desired outbound internal links, anchor text, owner, status, and verification date. |

## Verification Plan

This is the verification path for a future implementation pass.

### 1. Preflight

- Confirm current branch and clean/known worktree.
- Confirm Track A scope only.
- Confirm full backup status before any production write.
- Pull current page/post inventory through authenticated WordPress if available.
- Export a pre-change list of candidate URLs and their current body links.

### 2. Local Strategy Checks

- For each proposed hub, confirm whether it exists.
- For each post in a cluster, record:
  - inbound hub link exists: yes/no
  - outbound hub link exists: yes/no
  - sibling links count
  - conversion link count
  - anchor text quality
- Update the Notion connector `LINK_MAP` only after final URLs exist and self-link behavior is still covered by tests.

### 3. Production Application Checks

- Apply changes in small batches by cluster, not site-wide all at once.
- After each page/post edit, GET the live URL and confirm 200.
- Click-check or curl-check every new internal link.
- Confirm no links point to draft/private/404 URLs.
- Confirm canonical URLs remain unchanged unless a separate redirect/IA task explicitly handles a rename.
- Do not use the connector against production without dry-run first.

### 4. Crawl Checks

- Run a crawler pass over the changed URLs and verify:
  - no 404 internal links,
  - no redirect chains for new links,
  - no orphaned target pages in the changed set,
  - each hub reachable from nav/footer within 1-2 clicks,
  - each cluster child reachable from hub within 1 click.

Suggested tooling:

- `curl -I` for individual URLs
- a small script using `requests` + BeautifulSoup for changed URLs
- Screaming Frog/Sitebulb if KK has access
- Google Search Console URL inspection for new/updated pillar pages

### 5. Measurement

Needs GA4, Jetpack Stats, or GSC access:

- Baseline before implementation:
  - top landing pages,
  - engagement time/session duration,
  - clicks to Contact/Speaking/Services,
  - GSC impressions/clicks by cluster query.
- Re-check 2-4 weeks after implementation:
  - internal pathing from posts to hubs,
  - hub impressions,
  - long-tail queries for Vancouver AI, Web Summit Vancouver, AI for creatives, AI media training.

## Human-Gated Decisions

These should not be silently decided by an agent:

1. Final URL for the Work hub: keep `/recent-projects-include/`, rename to `/work/`, or choose `/projects/`/`/portfolio/`.
2. Whether `/services/` becomes the canonical service URL or remains a redirect to `/generative-ai-services/`.
3. Whether to create both `/vancouver-ai/` and `/bc-ai/`, or combine them.
4. Whether `/web-summit-vancouver/` should be a permanent annual hub.
5. Whether `AI for Creatives` and `AI for Media` are editorial hubs, service pages, or both.
6. Whether multilingual pages become a real international IA set, creative artifacts, or noindex pages.
7. Whether `Reconciliation` and `Worldview` get shorter canonical slugs.
8. Whether RAP draft content supplements, replaces, or redirects to the existing live RAP post.
9. Which analytics source defines "session duration increased" for issue #38 closeout.
10. Any production WordPress write, redirect, category migration, or page slug rename.

## Recommended Closeout Path For Issue #38

Issue #38 should not close on this report alone. This report scopes the work.

Close #38 only after a future implementation pass can show:

1. A current crawl confirms no orphaned priority pages.
2. All 34 published pages have 2-5 contextual internal links or documented exceptions.
3. The important hubs have 5+ internal links.
4. Priority clusters have bidirectional hub/post links.
5. Changed links have been click-checked.
6. Analytics has a baseline and a dated follow-up plan for session duration.

Until then, this artifact should be treated as the implementation map for #38, not the completed implementation.
