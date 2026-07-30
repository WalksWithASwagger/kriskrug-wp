# Navigation + IA Decision Pack — 2026-05-18

**Lane:** Swarm Lane 5 — content/nav structure decision pack  
**Scope:** docs-only recommendation. No WordPress writes.  
**Inputs read:** `CONTENT_AUDIT.md`, `SITE-AUDIT-2026-05-16.md`, `RESUME-HERE.md`, `SITE_INVENTORY.md`, live homepage nav HTML, live URL status checks.

## Assumptions

1. Track A current-theme work should improve visitor journeys now without requiring Aurora.
2. Track B Aurora work can rebuild the navigation and page hierarchy more cleanly, but should not change URL strategy without KK approval.
3. Existing URLs with inbound links should be preserved through 301 redirects, not deleted or silently repointed.
4. "Newsletter" is a conversion target, not an information-architecture pillar.

## Current Live Nav

As of 2026-05-18, the live primary and mobile nav both show:

1. About → `https://kriskrug.co/about/`
2. Blog → `https://kriskrug.co/blog/`
3. Podcast → `https://kriskrug.co/motleykrug-podcast/`
4. Services → `https://kriskrug.co/generative-ai-services/`
5. Projects → `https://kriskrug.co/recent-projects-include/`
6. Events → `https://kriskrug.co/events/`
7. Contact → `https://kriskrug.co/contact/`
8. NEWSLETTER → `https://kriskrug.beehiiv.com/`

Live status checks:

| URL | Status | Effective target |
|---|---:|---|
| `/recent-projects-include/` | 200 | `/recent-projects-include/` |
| `/work/` | 301 | `/recent-projects-include/` |
| `/events/` | 200 | `/events/` |
| `/blog/` | 200 | `/blog/` |
| `/news/` | 200 | `/news/` |
| `/services/` | 301 | `/generative-ai-services/` |
| `/generative-ai-services/` | 200 | `/generative-ai-services/` |
| `/motleykrug-podcast/` | 200 | `/motleykrug-podcast/` |
| `/speaking/` | 200 | `/speaking/` |
| `/publications/` | 200 | `/publications/` |
| `/the-kk-worldview/` | 200 | `/the-kk-worldview/` |
| `/reconciliation-indigenous-land-acknowledgement/` | 200 | `/reconciliation-indigenous-land-acknowledgement/` |

## Core IA Diagnosis

The current nav is functional but under-explains the actual site. It treats every major thing as a flat peer:

- commercial offers (`Services`)
- proof of work (`Projects`)
- writing (`Blog`)
- recurring media (`Podcast`)
- date-sensitive appearances (`Events`)
- identity pages (`About`, `Contact`)
- conversion (`Newsletter`)

That matches the old WordPress page structure, but not the current positioning: KK as BC + AI ecosystem builder, generative-AI educator, creative technologist, speaker, writer, and community operator.

The best fix is a two-step IA:

1. Current-theme: minimal nav label/target changes plus redirects. Keep it simple and reversible.
2. Aurora: rebuild as a clearer FSE navigation system with primary nav, utility nav, footer IA, and topic/pillar landing pages.

## Recommended Current-Theme Nav

Use the current Catch Responsive menu to make the least risky visitor-facing improvement:

| Position | Label | Target | Action |
|---:|---|---|---|
| 1 | About | `/about/` | Keep |
| 2 | Work | `/work/` | Rename `Projects` to `Work`; decide whether to rename the page slug now or keep redirect-only |
| 3 | Services | `/generative-ai-services/` | Keep target for now; nav label is fine |
| 4 | Speaking | `/speaking/` | Add to top nav |
| 5 | Events | `/events/` | Keep for now, but split later |
| 6 | Blog | `/blog/` | Keep |
| 7 | Podcast | `/motleykrug-podcast/` | Keep, unless KK wants it under Blog/Media instead |
| 8 | Contact | `/contact/` | Keep |

Move `NEWSLETTER` out of primary nav if possible and into one of:

- a styled header button if Catch Responsive supports it cleanly
- sidebar/footer only
- Aurora utility nav later

Do not add more top-level current-theme nav items until Aurora. The current header already has eight items, which is near the practical limit for the classic theme.

## Recommended Aurora Nav

Aurora should separate primary IA from conversion and utility links.

Primary nav:

1. About → `/about/`
2. Work → `/work/`
3. Services → `/services/` or `/generative-ai-services/`
4. Speaking → `/speaking/`
5. Events → `/events/`
6. Writing → `/blog/`
7. Contact → `/contact/`

Utility/header CTA:

- Newsletter → `https://kriskrug.beehiiv.com/`
- Search

Footer IA:

- Podcast → `/motleykrug-podcast/`
- Publications → `/publications/`
- Testimonials → `/testimonials/`
- Worldview → `/the-kk-worldview/` now, eventual `/worldview/`
- Reconciliation → `/reconciliation-indigenous-land-acknowledgement/` now, eventual `/reconciliation/`
- Privacy → `/privacy-policy/`
- Product Review Policy → `/product-review-policy-instructions/`
- International / language links only after multilingual decision

Rationale: top nav should answer "who is this, what does he do, why trust him, how do I hire/attend/read/contact him?" Footer can carry proof, policies, and secondary identity pages.

## Keep / Remove / Add

Keep in top nav:

- About
- Blog/Writing
- Services
- Work/Projects
- Events
- Contact

Rename:

- `Projects` → `Work`. "Work" is the visitor's natural URL and a stronger umbrella for projects, clients, collaborations, portfolio, and active affiliations.
- `Blog` → `Writing` in Aurora if the design can support a more editorial label. Keep `Blog` on current theme if changing it would create confusion with the existing page title.

Add:

- `Speaking` as a top-level item. It is a commercial/authority path and currently too buried.

Remove from top nav:

- `NEWSLETTER` as an all-caps peer nav item. Keep it as a CTA, not an IA pillar.

Do not add to top nav yet:

- Publications
- Testimonials
- Press
- Worldview
- Reconciliation
- International/language pages

These are important, but they are secondary or footer/pillar content unless KK decides one is central to the next campaign.

## `/recent-projects-include/` vs `/work/`

Recommended final state:

- Canonical page: `/work/`
- Old page redirect: `/recent-projects-include/` → `/work/`
- Existing temporary redirect becomes unnecessary: `/work/` should serve 200 after the rename

Why:

- `/work/` is natural, short, and memorable.
- `/recent-projects-include/` looks like an implementation artifact.
- The live `/work/` path already has intent and has been rescued from the old 2011-post redirect.

Current-theme option:

- Keep page slug as `/recent-projects-include/`.
- Change nav label from `Projects` to `Work`.
- Keep `/work/` → `/recent-projects-include/`.
- Low risk; no permalink rename yet.

Aurora/pre-cutover option:

- Rename the WordPress page slug to `work`.
- Add/flip redirect `/recent-projects-include/` → `/work/`.
- Update nav to point directly to `/work/`.
- Verify no redirect chain from `/work/`.

Decision needed from KK:

- Is "Work" the right umbrella, or does KK prefer "Projects", "Portfolio", or "Fieldwork"?

## `/events/` Split

The current `/events/` page mixes three jobs:

1. upcoming/current appearances
2. historical event archive and client/event history
3. recurring topical coverage such as Web Summit Vancouver

Recommended final structure:

```text
/events/                    current/upcoming events and appearances
/speaking/                  hire KK to speak, speaker topics, booking CTA
/web-summit-vancouver/      evergreen annual coverage pillar
/events/archive/            optional historical archive, only if worth maintaining
```

Current-theme action:

- Keep `/events/` in nav.
- Add `/speaking/` to nav.
- Do not create `/events/archive/` unless there is enough curated historical content to justify it.

Aurora action:

- Make `/events/` visibly current: upcoming appearances, recent recaps, and a link to Web Summit Vancouver.
- Move booking language to `/speaking/`.
- Link old event-report posts into topic collections instead of making the Events page carry everything.

Redirect implications:

- No redirect required for `/events/`; keep it stable.
- If old event pages are renamed later, add one 301 per renamed slug.
- If a new `/web-summit-vancouver/` pillar is created, link all annual Web Summit posts to it. Do not redirect individual year posts unless a duplicate page is created.

Decision needed from KK:

- Should `/events/` mean "where Kris will be next" or "archive of events Kris has covered/produced"? Recommended: current/upcoming first, archive second.

## Pillar Pages

Create or strengthen these as topical anchors. They do not all belong in top nav.

| Pillar | URL | Type | Nav placement | Notes |
|---|---|---|---|---|
| Work | `/work/` | existing page rename | Top nav | Canonical portfolio/projects hub |
| Services | `/services/` or `/generative-ai-services/` | existing service hub | Top nav | Current `/services/` redirects to long slug |
| Speaking | `/speaking/` | existing page | Top nav | Add talks, topics, reel, booking CTA |
| Writing | `/blog/` | existing archive | Top nav | Aurora should give it an H1/hero |
| Vancouver AI | `/vancouver-ai/` | new | Work or footer | Connects meetup recaps, BC + AI, community posts |
| BC + AI | `/bc-ai/` | new | Work section | Canonical personal-role page linking to association |
| AI for Creatives | `/ai-for-creatives/` | new or service child | Services/footer | Could point to AI Upgrade creative offer |
| AI for Media | `/ai-for-media/` | new or service child | Services/footer | Could point to media leaders offer |
| Web Summit Vancouver | `/web-summit-vancouver/` | new | Events section | Permanent annual coverage hub |
| Podcast | `/motleykrug-podcast/` | existing | Footer or top nav | Keep top nav only if podcast is an active growth channel |
| Press | `/press/` | new | Footer/utility | Headshots, bios, links, EPK |
| Worldview | `/worldview/` | eventual rename | Footer | 301 from `/the-kk-worldview/` if renamed |
| Reconciliation | `/reconciliation/` | eventual rename | Footer | 301 from long existing slug if renamed |

## Services URL Decision

There are two viable final states:

Option A — keep current canonical:

- `/generative-ai-services/` remains the service hub.
- `/services/` keeps 301 redirecting to it.
- Lowest risk; no page rename.

Option B — clean canonical:

- Rename `/generative-ai-services/` to `/services/`.
- Add `/generative-ai-services/` → `/services/`.
- Stronger nav and offline URL.

Recommendation:

- Current theme: keep Option A.
- Aurora: consider Option B only if KK wants a broad service hub page with child pages for media, creatives, workshops, and coaching.

Decision needed from KK:

- Should the main offer be a broad "Services" page or specifically "Generative AI Services"?

## Blog vs News

`/blog/` and `/news/` both return 200. The audits do not show a clear reader-facing distinction.

Recommendation:

- Keep `/blog/` as the main writing archive.
- Do not put `/news/` in top nav.
- Decide whether `/news/` is:
  - a legacy archive, left published but unlinked
  - a future press/news page
  - a redirect to `/blog/`

Decision needed from KK:

- Is "News" a real editorial category, or should it collapse into Blog/Writing?

## Multilingual Handling

The multilingual welcome pages are currently an unfinished set:

- no hreflang network
- no visible language switcher
- two overlapping Swahili pages
- creative/persona slugs that are charming but poor for discoverability

Do not add multilingual links to primary nav until KK chooses a strategy.

Option 1 — Make them real:

- Add `/international/` as the parent page.
- Standardize child slugs:
  - `/international/japanese/`
  - `/international/chinese/`
  - `/international/farsi/`
  - `/international/russian/`
  - `/international/hindi/`
  - `/international/urdu/`
  - `/international/swahili/`
- Add hreflang between variants.
- Add a language switcher on `/international/` and each variant.
- Pick one Swahili canonical and 301 the duplicate.

Option 2 — Position as creative/persona art:

- Keep pages published.
- Add copy explaining the artistic/persona framing.
- Remove from primary nav and possibly noindex.
- Link from Worldview or footer only if desired.

Option 3 — Minimize SEO confusion:

- Noindex variants.
- Remove from sitemap if possible.
- Keep only for direct links and creative archive value.

Recommendation:

- Choose Option 1 only if KK wants real multilingual discovery and maintenance.
- Otherwise choose Option 2 or 3. Half-built multilingual IA is worse than hidden creative artifacts.

Decision needed from KK:

- Are these pages meant to serve real non-English readers, or are they creative persona pieces?

## Redirect Plan

Only add redirects when the target page exists and KK has approved the canonical label.

Recommended near-term redirects:

| Source | Target | Timing | Notes |
|---|---|---|---|
| `/work/` | `/recent-projects-include/` | Already live | Temporary rescue redirect |
| `/services/` | `/generative-ai-services/` | Already live | Keep unless service hub is renamed |

Recommended Aurora/canonical redirects:

| Source | Target | Timing | Notes |
|---|---|---|---|
| `/recent-projects-include/` | `/work/` | After page slug rename | Replace current temporary `/work/` redirect |
| `/generative-ai-services/` | `/services/` | Only if service hub is renamed | Avoid redirect chain |
| `/the-kk-worldview/` | `/worldview/` | Optional later | Only if title/slug cleanup is approved |
| `/reconciliation-indigenous-land-acknowledgement/` | `/reconciliation/` | Optional later | Keep old URL if external links are strong |
| duplicate Swahili page | chosen Swahili canonical | After multilingual decision | Required if Option 1 |
| old multilingual creative slugs | standardized `/international/<language>/` | Only if Option 1 | One 301 per language page |

Do not redirect `/events/` or `/blog/`.

## Decisions Needed From KK

Highest-priority:

1. Should the public portfolio hub be called `Work`, `Projects`, or `Portfolio`? Recommended: `Work`.
2. Should `/work/` become the canonical page, replacing `/recent-projects-include/`? Recommended: yes, during Aurora or a controlled Track A permalink pass.
3. Should `Speaking` be added to the top nav now? Recommended: yes.
4. Should `Newsletter` leave the primary nav and become a CTA/utility item? Recommended: yes.
5. Should `/events/` prioritize upcoming/current appearances or historical event archive? Recommended: upcoming/current.
6. Should the main service hub eventually become `/services/`? Recommended: decide during Aurora, not immediately.
7. Are multilingual welcome pages real language-service pages or creative persona artifacts? Recommended: decide before adding any language nav.
8. Is `/news/` a distinct destination or legacy duplicate of Blog? Recommended: keep unlinked until decided.

## Implementation Sequence

Current-theme safe sequence:

1. Rename nav label `Projects` → `Work`, leaving target as `/recent-projects-include/`.
2. Add `Speaking` to the top nav.
3. Move `NEWSLETTER` out of primary nav if the theme can make it a button/utility link cleanly.
4. Leave redirects as-is.

Aurora sequence:

1. Rebuild FSE Navigation block with primary nav + utility CTA.
2. Decide canonical `/work/` and `/services/` URLs before cutover.
3. Create or update pillar pages in this order: Work, Speaking, Services, Web Summit Vancouver, Vancouver AI/BC + AI, Press.
4. Add redirect map in Redirection plugin.
5. Smoke-test top nav, mobile nav, footer links, redirects, and search.

## Bottom Line

The immediate nav fix is small: make `Work` visible, add `Speaking`, and stop treating `Newsletter` as a peer content pillar. The bigger Aurora decision is URL canon: whether `/work/` and `/services/` become the clean permanent URLs. The multilingual pages should stay out of nav until KK decides whether they are real international IA or creative artifacts.
