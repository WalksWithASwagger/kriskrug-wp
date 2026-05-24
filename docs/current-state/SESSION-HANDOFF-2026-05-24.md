# Session Handoff — Content/Track-A agent — 2026-05-24

Written to de-confuse the parallel agents (Aurora theme, WP7 ops) and let KK regroup. This is what the **content/messaging agent (Track A)** did, what's **live vs draft vs pending**, and **who owns what**. Then this agent stands down.

## Lane boundaries (the source of the confusion)

| Lane | Owner | Touches |
|---|---|---|
| **Track A — content** (this agent) | me | WP **page/post content** + inline `<style>`, media, drafts, SEO meta, docs. Edits via WP REST. |
| **Track B — Aurora theme** | Aurora agent | `kk-aurora` FSE **templates** (front-page, page-work, page-speaking, page-2672), theme CSS/JS, global styles, nav. |
| **WP7** | ops agent | WordPress 7 upgrade / staging readiness. |

**Critical interaction (`[[aurora-fse-template-ownership]]`):** Aurora's FSE theme has **slug/ID-specific templates that omit `core/post-content`** for **Work (page-2672), Speaking (page-speaking), Homepage (front-page)**. So Track-A page-content edits to those three **do not render publicly** — their content lives in the *theme templates* (Track B). Pages on the **generic `page` template** (About, Services, Podcast EPK, RAP, Photography) DO render Track-A content.

## LIVE & public (this session)
- **About** (1208) — true 2026 roster ("Five rooms"), Indigenomics→past, dark Aurora re-theme.
- **Services** (2666) — dark re-theme + Indigenomics reframed to advisory.
- **Podcast EPK** (3609) — dark re-theme.
- **RAP page** (11914, `/responsible-ai-professional/`) — NEW, published.
- **Photography** (12013, `/photography/`) — NEW, **just published**. Immersive showcase of KK's own CC-licensed photographs (Iggy Pop hero, Dalai Lama, Jack White, Bush@Beijing, Deepwater Horizon/TEDxOilSpill, Midway, Vancouver 2010, etc.), CSS-native `animation-timeline` reveal, masonry, glass captions. **NOT yet in nav** — needs adding to the Aurora header menu (Track B / KK).
- **Homepage** — un-blanked via a **force-visible safety net** in Customizer → Additional CSS (`custom_css[kk-aurora]`). See ⚠️ below.

## DRAFTS staged for KK (not published)
- `the-75-percent-rule` (11876), `sovereign-ai-for-whom` (11905), `data-center-protest-signs` (11929, OG=thirsty-data-center), plus `speak-it-into-existence` (11878), `i-wont-fake…` (11877). All block-formatted, review-ready. KK publishes.
- (A sibling agent separately shipped "You Can't Drink Data" 11936 — not mine.)

## ⚠️ Coordination flags for the Aurora agent
1. **Homepage reveal is broken in-theme** (`[[homepage-reveal-safety-net]]`): GSAP/ScrollTrigger scroll-reveal sets content `opacity:0` and never reveals (reduced-motion OFF → universal blank). My Customizer safety net force-shows it but **disables the entrance animation site-wide**. **Please implement a visible-by-default reveal in-theme** (self-host GSAP or use IntersectionObserver/`animation-timeline`), then **remove my safety net** from Additional CSS.
2. **Full front-end audit:** `docs/current-state/AURORA-FRONTEND-AUDIT-2026-05-23.md` (harsh, prioritized: reveal bug, CDN-gating fragility, missing `:focus-visible`, underused neon/gradient system, thin micro-interactions).
3. **Template content handoff:** `docs/current-state/AURORA-TEMPLATE-CONTENT-HANDOFF.md` — copy-ready Home/Work/Speaking content (new roster, RAP card, Indigenomics-as-past) to paste into the FSE templates.
4. **Pagely cache** (`[[pagely-page-cache-purge]]`): REST edits don't auto-purge; verify public renders logged-out.

## Open / next (for the regroup)
- Add **Photography** + **RAP** to the site nav (Track B).
- Aurora agent: fix homepage reveal in-theme + remove safety net; work the audit list.
- KK: publish the staged drafts when read; point me at more Flickr photo favorites to deepen `/photography/`.
- Track-A backlog (needs Pagely SSH): `/projects/`→`/work/` redirect, Work OG (#68), llms.txt, robots.txt.
- Contact-form triage: GitHub issue **#128** (do agentically later).

## Reference
Memories: `[[kk-current-roster-2026]]`, `[[kk-voice-cheatsheet]]`, `[[about-page-inline-style-block]]`, `[[aurora-fse-template-ownership]]`, `[[homepage-reveal-safety-net]]`, `[[pagely-page-cache-purge]]`. Docs: the audit + template-handoff above. Reusable script: `scripts/notion-to-wp/publish_dc_protest_draft.py`.

**This agent is standing down.** Track-A content surfaces are live and true-to-2026; the homepage is visible; the photography legacy is published. The ball is with the Aurora agent (theme reveal + nav) and KK (publish drafts, regroup).
