# Aurora Visual Redesign Audit - 2026-05-18

**Track:** Track B - Aurora v2 theme
**Scope:** Design audit, target direction, and issue rollout map. No WordPress writes. No production activation.
**Decision driver:** KK wants a significant visual redesign that reflects expert-level personal brand authority, uses photos and video of KK and his projects, and reaches a high-end 2026 interaction/polish bar.

## Executive Verdict

Aurora should be treated as a working prototype, not the final redesign.

The current Aurora branch has useful foundations: a WordPress block theme, `theme.json` tokens, dark/glass visual direction, progressive CSS, GSAP/ScrollTrigger, and block patterns. But it does not yet express KK's real brand power. It is still mostly "dark cyberpunk plus gradients." The next Track B pass should shift the center of gravity from decorative futurism to media-rich personal-brand authority: real photography, real speaking footage, project proof, editorial writing, and confident conversion paths.

**Cutover should stay blocked** until Aurora clears both gates:

1. **Mechanical gate:** Local/staging render is clean across real content, especially header/navigation, long-form posts, media-heavy posts, mobile, and plugin surfaces.
2. **Brand gate:** The site looks and feels like a premium personal-brand platform for an AI-era creative technologist, keynote speaker, community operator, photographer, and culture builder.

Fixing the desktop navigation bug is necessary, but it is not enough.

## Assumptions

1. Aurora remains Track B and belongs on `aurora/v2`, not `main`.
2. Track A can keep publishing and improving current content while Aurora is redesigned.
3. Existing production URLs remain stable unless KK approves a controlled redirect pass.
4. "High-end" means a site that earns trust through craft, proof, speed, and clarity, not only visual effects.
5. Motion and glass effects should frame the media and narrative, not compensate for missing media.
6. Any benchmark claim in this doc is current as of 2026-05-18 and should be refreshed before a summer 2026 launch push.

## Measurable Success Criteria

Aurora is ready for a serious staging review when:

| Area | Success criteria |
|---|---|
| Visual identity | First viewport makes KK unmistakable through name, face/media, role, project proof, and a clear offer path. |
| Media system | Homepage, About, Work, Speaking, and long-form posts support high-quality photos, video embeds, portrait crops, project teasers, and captions without layout breakage. |
| Motion | Motion has a defined language, respects `prefers-reduced-motion`, avoids scroll-jacking, and is visible in browser screenshots without hurting readability. |
| WordPress mechanics | FSE header/nav/footer render correctly on desktop and mobile; templates work with real posts, pages, featured images, embeds, and forms. |
| Performance | Homepage and article templates use progressive enhancement, lazy media, constrained JS, and no autoplay-heavy default. |
| Accessibility | Keyboard navigation, focus states, contrast, reduced motion, captions/alt text, and semantic headings pass manual smoke before production planning. |
| Content fit | The design supports the current IA: About, Work, Services, Speaking, Events, Writing, Contact, Newsletter CTA, and footer utility links. |

## 2026 Benchmark Signals

These are not instructions to copy any one site. They set the quality bar.

| Signal | What it means for Aurora | Source checked |
|---|---|---|
| Award-level sites are still motion- and craft-led. Recent Awwwards Sites of the Day list multiple daily winners with Developer Award recognition. | Aurora needs visible craft in transitions, interactions, responsiveness, and media behavior, not only a static dark palette. | [Awwwards Sites of the Day](https://www.awwwards.com/websites/sites_of_the_day/) |
| Portfolio and personal-brand sites are judged on UI, UX, and innovation together. CSS Design Awards highlights animated, responsive, scroll-based portfolio work under UI/UX/Innovation scoring. | The benchmark is not "cool animation"; it is polished interaction plus usable information architecture. | [CSS Design Awards example](https://www.cssdesignawards.com/sites/interactive-web-portfolio/48731/) |
| CSS scroll-driven animations are now a real progressive-enhancement path. They link keyframe progress directly to scroll and can avoid main-thread JS costs. | Use native scroll timelines for lightweight reveals/progress where possible; keep GSAP for richer orchestrated sequences. | [MDN scroll-driven animation timelines](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations/Timelines) |
| Cross-document view transitions can support same-origin page transitions with CSS opt-in. | Aurora's existing `@view-transition` direction is valid, but it must be tested on real same-origin WordPress navigation and reduced-motion behavior. | [Chrome cross-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document) |
| WordPress block themes use blocks for navigation, header, content, and footer. | Header/nav problems are not incidental; they are core FSE migration work and must be solved in templates plus Site Editor state. | [WordPress block themes](https://wordpress.org/documentation/article/block-themes/) |
| GSAP ScrollTrigger remains appropriate for complex scroll animation and explicitly avoids scroll-jacking by default. | GSAP is fine for hero/media/project reveals if used surgically and tested for mobile, reduced motion, and performance. | [GSAP ScrollTrigger docs](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) |

## Current Aurora Inventory

Evidence from `origin/aurora/v2` and current-state docs:

| Surface | Current state | Audit read |
|---|---|---|
| Theme | `theme/kk-aurora/` block theme with templates, parts, patterns, CSS, JS, and `theme.json`. | Real foundation exists. Not vapor. |
| Demo | `demo/index.html` previews a dark gradient/glass direction. | Useful mood board, but not a WordPress validation surface. |
| Tokens | `theme.json` defines dark colors, cyan/teal/purple/pink accents, gradients, typography, spacing. | Good start, but too generic to carry the personal brand by itself. |
| Homepage | `templates/home.html` uses hero, stats, three pillars, latest writing, CTA. | Structurally sensible, visually under-authored and not media-led enough. |
| Hero | `patterns/hero-gradient.php` centers type and badges with animated gradient text. | Clear but not distinctive enough. Needs KK media and sharper offer hierarchy. |
| Single post | `templates/single.html` focuses on clean prose, featured image, author card, related posts. | Solid base; needs richer long-form reading design and media affordances. |
| Header | `parts/header.html` uses an FSE navigation block and "Let's Talk" button. | Current staging report says desktop nav renders broken; this is a P0 Track B blocker. |
| Motion | `bleeding-edge.css`, `aurora-animations.js`, and `micro-interactions.js` include view transitions, scroll reveal, counters, header scroll, parallax, cursor/card interactions. | Ingredients are present, but no motion direction system or proof of rendered behavior yet. |
| Media | Existing Aurora templates do not center real portraits, speaking footage, project photos, video reels, or photography archive components. | Largest brand gap. |

## What Is Working

Aurora should keep these ideas:

- **FSE/block theme direction.** It matches WordPress's current direction and gives Track B a clean template and global-style surface.
- **Dark foundation.** A black/deep-space base still fits KK's AI, culture, and photographic edge.
- **Cyan/teal accent family.** It can stay as the interactive signal if it is restrained and paired with real media.
- **Progressive enhancement.** CSS view transitions, scroll timelines, container queries, and GSAP can coexist if each has a specific job.
- **Content pillars.** BC+AI, Indigenomics.ai, The Upgrade AI, speaking, writing, and photography are the right ingredients.

## What Is Not Good Enough Yet

| Gap | Why it matters | Direction |
|---|---|---|
| Media is not central. | KK is a photographer, speaker, founder/operator, and visible community builder. A text-first dark page undersells the brand. | Make photos/video the primary proof layer. |
| Visual language is generic. | "Dark + gradient + glass" is common in AI/startup sites. | Build a more specific system: editorial black, photographic depth, signal-grid overlays, restrained glass, sharp type, field-note texture. |
| Hero is too abstract. | "Bridging Art, AI..." is true, but not enough for first-impression authority. | First viewport should combine face/media, role proof, flagship projects, and one primary booking/work CTA. |
| Components are too card-heavy. | Repeated glass cards can make the site feel template-like. | Use cards only for repeated items; use full-bleed sections, media bands, and editorial layouts for primary storytelling. |
| Motion lacks narrative. | Existing animations are effects, not a brand language. | Define when motion means reveal, proof, transition, depth, or delight. |
| Header/nav is broken in staging. | No premium site can have unstable navigation. | Treat header/nav as the first implementation blocker. |
| Media governance is unclear. | Videos/photos need source, rights, alt/caption, crops, compression, and fallback rules. | Build a media inventory and component spec before heavy implementation. |

## Target Design Thesis

**Aurora should feel like a high-end field station for the AI age: black editorial precision, living media, human proof, and subtle future-facing interaction.**

The visual direction should combine:

- **Editorial authority:** strong type, decisive hierarchy, clean reading surfaces.
- **Photographic reality:** portraits, talks, event rooms, project artifacts, community images, and documentary texture.
- **Glass/liquid morphism with restraint:** glass surfaces used for navigation, overlays, media metadata, and project controls, not every section.
- **Signal systems:** small data-like annotations, source labels, project status, event recency, and linkable proof.
- **Motion as attention design:** content emerges, media breathes, project paths clarify, pages transition smoothly.
- **Human warmth:** not sterile AI SaaS. The photos, language, and pacing should show presence, taste, humor, and care.

## Recommended First-Viewport Direction

Do not make a text-only hero. Do not make a generic split hero card. Use an immersive first viewport with KK as the unmistakable signal.

Recommended composition:

| Layer | Description |
|---|---|
| Background media | Full-bleed or near-full-bleed cinematic still/video of KK speaking, shooting, teaching, or in a real community room. Darkened only enough for text contrast. |
| Primary type | "Kris Krug" or "Kris Krug: AI, Culture, Community" as the dominant identity signal. |
| Supporting line | One sentence: creative technologist, AI keynote speaker, photographer, and community builder working across BC+AI, Indigenomics.ai, and The Upgrade AI. |
| Proof chips | Three to five compact proof markers: BC+AI, The Upgrade AI, Indigenomics.ai, keynote portals, photography. |
| CTAs | Primary: Book a keynote / Work with Kris. Secondary: Explore work / Read latest. Newsletter stays utility, not main IA. |
| Motion | Subtle media parallax or mask reveal, proof chips entering in sequence, reduced-motion fallback to static hero. |

## Media System

Aurora needs a first-class media inventory before serious visual implementation.

Current local media evidence:

| Source | Assets observed | Use |
|---|---:|---|
| `content/source-packs/keynotes-2026/assets/` | 4 stable teaser images | Speaking/Work/About launch surfaces and project cards. |
| `content/drafts/2026-05-07-web-summit-vancouver-2026/images/` | 10 images | Web Summit case/story visuals and long-form stress tests. |
| `content/drafts/2026-05-14-calling-us-all-in/images/` | 6 images | Community/post media tests. |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/` | 6 images | AI/politics/sovereignty post media tests. |
| `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/images/` | 13 images | Training/product/media-heavy article tests. |
| `docs/current-state/raw/pages/*.html` | Existing live-site images and embeds | Extraction candidates, but many need alt/caption and rights checks. |

Missing media decisions:

1. **Hero portrait/video:** choose one canonical hero asset and two fallbacks.
2. **Speaking reel:** decide whether Aurora embeds a hosted reel, YouTube/Vimeo, or a poster-first video module.
3. **Project media rules:** every Work card needs image/video, source, alt, target URL, and proof label.
4. **Photography archive teaser:** decide whether photography is a short authority band or a full portal in v1.
5. **Compression path:** generate hero/poster sizes before staging, ideally WebP/AVIF with JPEG fallback.

## Motion System

Use a small motion vocabulary instead of ad-hoc effects.

| Motion type | Purpose | Implementation guidance |
|---|---|---|
| Reveal | Bring in sections, proof chips, and media captions. | CSS scroll-driven animations for simple reveals where support is good; IntersectionObserver fallback if needed. |
| Depth | Add cinematic parallax to hero/media bands. | Transform/opacity only; no layout thrash; disable for reduced motion. |
| Continuity | Smooth same-origin page transitions. | Keep `@view-transition`, but test real WordPress routes and browser support. |
| Proof | Animate counters and project status sparingly. | GSAP only where the sequence matters. |
| Micro-interaction | Make cards, buttons, forms, and media controls feel responsive. | Pointer-aware shine/morph effects on desktop only; simple hover/focus states on mobile. |
| Reading | Progress bar, sticky article metadata, table of contents if useful. | CSS-first; never interfere with normal scrolling. |

Rules:

- No scroll-jacking.
- No autoplay audio.
- No essential information hidden behind motion.
- No motion-only affordances.
- `prefers-reduced-motion: reduce` must produce a polished static site.
- Motion should never move body text while someone is trying to read it.

## Template Priorities

Build templates in this order:

1. **Header/navigation template.** Fix the known desktop FSE nav break first.
2. **Homepage.** High-end media-led hero, proof section, work/speaking lanes, latest writing, newsletter utility CTA.
3. **About.** Portrait/story page with photo bands, credibility timeline, current roles, worldview, and current CTAs.
4. **Work.** Project hub with media-rich case cards for BC+AI, The Upgrade AI, Indigenomics.ai, keynote portals, photography, and selected initiatives.
5. **Speaking.** Booking-first page with reel/media, talk topics, proof, testimonials, event logos/photos, and inquiry CTA.
6. **Single post.** Long-form reading, featured media, pull quotes, embeds, image galleries, author/proof footer, related writing.
7. **Archive/Writing.** Editorial index with filters, category rhythm, and article cards that do not all look identical.
8. **Contact/forms.** Accessible, conversion-focused forms and fallback contact paths.
9. **Footer.** Utility IA, project network, newsletter, policies, and credibility links.

## Issue Rollout Map

The current open design issues `#24` through `#35` are too granular and too old to drive this redesign without reframing. Recommended rollout:

| Track B epic | Roll up current issues | Acceptance |
|---|---|---|
| **Aurora P0: Staging render rescue** | `#28`, `#33` | Header/nav works on desktop and mobile, six-page Local smoke passes, screenshots captured. |
| **Aurora P1: 2026 visual system** | `#26`, `#27`, `#35` | Type, color, buttons, focus states, glass rules, media treatments, and motion tokens documented and implemented in theme. |
| **Aurora P1: Media-led homepage** | `#24`, `#34`, `#31`, `#30` | Homepage uses real KK/project media, clear first viewport, project proof, speaking/work pathways, and responsive media behavior. |
| **Aurora P1: Work and speaking templates** | `#31`, `#30`, plus issue `#76` context | Work and Speaking pages have reusable project/talk media components and conversion paths. |
| **Aurora P2: Long-form publishing experience** | new issue | Single-post template supports long-form writing, image-heavy posts, embeds, captions, author proof, and related posts. |
| **Aurora P2: Component library with restraint** | `#25`, `#29`, `#32`, `#35` | Component inventory exists, but avoids nested-card/card-everything design. Forms, footer, cards, CTAs, media modules complete. |
| **Aurora P2: Performance and accessibility QA** | `#33`, `#46`, `#47`, `#5` if scoped to Aurora | Reduced motion, keyboard nav, color contrast, media loading, and JS budget checked on real staging. |

Recommended GitHub handling:

- Leave existing issues open for now, but add a Track B comment pointing to this audit.
- Remove `auto-implement` from `#24-#35` until each is rewritten with current acceptance criteria.
- Use `issues-to-create/aurora-v2-redesign-epics.md` as the local draft pack if KK approves filing the new epics.
- Create 5 to 7 new Aurora v2 epics only after KK approves this direction.
- Use `Refs`, not `Closes`, in Aurora PRs unless the issue acceptance is truly satisfied.

## Immediate Next Sprint

**Goal:** Move Aurora from "prototype with broken render" to "staging-ready design surface."

Suggested sprint:

1. Create or reuse an isolated `aurora/v2` worktree.
2. Fix the header/nav render in `theme/kk-aurora/parts/header.html` and supporting CSS.
3. Re-run the six-page Local smoke from `AURORA-STAGING-REPORT-2026-05-18.md`.
4. Capture browser screenshots for desktop/mobile homepage, About, Speaking or Work, and two long-form posts.
5. Add a media inventory file for hero, project, speaking, portrait, and article stress-test assets.
6. Replace the current text-first hero with a media-led homepage concept.
7. Add a reduced-motion screenshot/pass/fail check.

Do not:

- Activate Aurora on production.
- Merge `aurora/v2` into `main`.
- Rewrite production URLs.
- Solve Track A content publishing inside the Track B sprint.

## Open Decisions For KK

These are worth answering before heavy implementation:

1. **Hero media:** Which asset should be the face of the redesign: keynote stage, portrait, community room, photography/action shot, or project montage?
2. **Primary conversion:** Is the main CTA "Book a keynote", "Work with me", "Explore my work", or a campaign-specific offer?
3. **Brand edge:** How far should Aurora lean into cyberpunk/AI weirdness versus editorial/premium human authority?
4. **Photography role:** Is photography a credential band, a full portfolio section, or a major pillar in v1?
5. **Video hosting:** Where should speaking/project videos live: YouTube, Vimeo, WordPress media, external keynote portals, or a mix?
6. **Issue hygiene:** Should we mutate the current GitHub design issues now, or keep this doc as the design brief until after the first visual prototype?

## Recommendation

Proceed with Aurora, but reset the bar.

The next Track B milestone should not be "make the existing dark theme work." It should be "prove the new personal-brand system on real content." Keep Aurora's technical foundation, fix the mechanical render bug, then rebuild the homepage and core templates around real media, stronger typography, purposeful motion, and project proof.

In short: less generic AI sheen, more unmistakable KK.
