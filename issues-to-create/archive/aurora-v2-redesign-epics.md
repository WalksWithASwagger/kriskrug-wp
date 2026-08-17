# Aurora v2 Redesign Epic Drafts

**Created:** 2026-05-18
**Source brief:** `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`
**Status:** Filed in GitHub on 2026-05-19 as issues #80-#86.

These drafts replace the January-era broad design tickets with a smaller Track B set. The stale `auto-implement` labels were removed from issues `#24` through `#35` during the 2026-05-19 issue hygiene pass.

---

## 1. [AURORA P0] Rescue staging header/nav render

**Labels:** `enhancement`, `ux`, `mobile`, `accessibility`, `performance`, `track-b`, `aurora-v2`, `priority:high`

### Problem

Local Aurora staging renders real WordPress URLs, but the desktop header/nav appears broken: responsive overlay elements show on desktop, including mobile-style controls and a vertical CTA state. Aurora cannot be design-reviewed or cut over while navigation is unstable.

### Acceptance Criteria

- [ ] Header and navigation render cleanly on desktop and mobile.
- [ ] Primary nav supports About, Work, Services, Speaking, Events, Writing, Contact.
- [ ] Newsletter is treated as a utility CTA, not a peer IA item.
- [ ] Keyboard navigation and focus states are visible.
- [ ] Reduced-motion mode still produces a polished static header.
- [ ] Six-page Local smoke passes for `/`, `/about/`, two current posts, Calling Us All In, and Web Summit.
- [ ] Desktop and mobile screenshots are captured under `docs/current-state/aurora-smoke-YYYY-MM-DD/`.

### References

- `docs/current-state/AURORA-STAGING-REPORT-2026-05-18.md`
- `docs/current-state/NAV-IA-DECISION-PACK-2026-05-18.md`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 2. [AURORA P1] Define the 2026 visual system

**Labels:** `enhancement`, `ux`, `accessibility`, `track-b`, `aurora-v2`, `priority:high`

### Problem

Aurora has useful tokens and a dark/glass starting point, but the current visual language is still generic AI-site territory. The redesign needs a premium personal-brand system: editorial black, photographic depth, restrained glass, clear type hierarchy, media treatments, buttons, focus states, and motion tokens.

### Acceptance Criteria

- [ ] `theme.json` tokens reflect final type, color, spacing, button, radius, and focus-state decisions.
- [ ] CSS defines a restrained glass/liquid morphism system with clear usage rules.
- [ ] Typography hierarchy supports homepage hero, page titles, compact panels, long-form articles, metadata, and captions.
- [ ] Button/CTA system covers primary, secondary, ghost, icon/utility, disabled, hover, active, focus, and mobile tap states.
- [ ] Contrast is checked for all token pairs used in real templates.
- [ ] Motion tokens exist for reveal, depth, continuity, proof, micro-interaction, and reading states.
- [ ] Documentation points back to the visual redesign audit.

### References

- `theme/kk-aurora/theme.json`
- `theme/kk-aurora/assets/css/bleeding-edge.css`
- `theme/kk-aurora/assets/js/aurora-animations.js`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 3. [AURORA P1] Build a media-led homepage

**Labels:** `enhancement`, `ux`, `mobile`, `performance`, `track-b`, `aurora-v2`, `priority:high`

### Problem

The current Aurora homepage is structurally sensible but too text-first and abstract. KK's homepage should immediately show a high-end personal brand through real media, project proof, speaking/work pathways, and polished motion.

### Acceptance Criteria

- [ ] First viewport makes "Kris Krug" unmistakable through name, face/media, role, proof, and CTA.
- [ ] Hero uses a real photo/video/poster asset with accessible fallback and responsive crops.
- [ ] Primary CTA is explicit: Book a keynote, Work with Kris, or approved equivalent.
- [ ] Work, Speaking, Writing, and project-network paths are visible without cluttering the nav.
- [ ] Project proof uses real assets from the keynotes source pack or approved media inventory.
- [ ] Motion supports the story without hiding content or moving readable body text.
- [ ] Homepage works at mobile, tablet, desktop, and wide desktop sizes.
- [ ] Performance pass confirms lazy media and no heavy autoplay default.

### References

- `theme/kk-aurora/templates/home.html`
- `theme/kk-aurora/patterns/hero-gradient.php`
- `content/source-packs/keynotes-2026/README.md`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 4. [AURORA P1] Create Work and Speaking media templates

**Labels:** `enhancement`, `ux`, `content`, `mobile`, `track-b`, `aurora-v2`, `priority:high`

### Problem

Work and Speaking are the core authority and conversion pages for the redesign. They need reusable media-rich modules for project cards, keynote portals, talk topics, testimonials, and proof of current work.

### Acceptance Criteria

- [ ] Work page supports media-rich cards for BC+AI, The Upgrade AI, Indigenomics.ai, keynote portals, photography, and selected initiatives.
- [ ] Speaking page supports reel/video, keynote topics, proof markers, testimonials, event logos/photos, and booking CTA.
- [ ] Components can be reused as block patterns or template parts without duplicating large inline CSS.
- [ ] Each media item has alt text, caption/proof label when useful, source, and fallback behavior.
- [ ] Layout avoids card-inside-card and maintains readable hierarchy on mobile.
- [ ] The implementation respects existing URL strategy until KK approves canonical redirects.

### References

- `content/source-packs/keynotes-2026/wp-payloads/work.html`
- `content/source-packs/keynotes-2026/wp-payloads/speaking.html`
- `docs/current-state/NAV-IA-DECISION-PACK-2026-05-18.md`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 5. [AURORA P2] Upgrade long-form article and media-heavy post templates

**Labels:** `enhancement`, `ux`, `accessibility`, `performance`, `track-b`, `aurora-v2`, `priority:medium`

### Problem

Aurora's single-post template is clean but not yet a premium reading system. It needs to handle long-form essays, image-heavy event recaps, embedded media, captions, pull quotes, author proof, related writing, and mobile reading comfort.

### Acceptance Criteria

- [ ] Single-post template supports long-form reading without cramped line length or weak hierarchy.
- [ ] Featured images, galleries, embeds, pull quotes, lists, and captions render cleanly.
- [ ] Article metadata includes date, category, read time if reliable, and author/proof context.
- [ ] Reading progress or table of contents is optional and does not interfere with scrolling.
- [ ] `prefers-reduced-motion` disables nonessential reading motion.
- [ ] Template is tested against Make Culture, Your Taste, Calling Us All In, Web Summit, and one media-heavy draft pack.

### References

- `theme/kk-aurora/templates/single.html`
- `content/drafts/2026-05-07-web-summit-vancouver-2026/`
- `content/drafts/2026-05-14-calling-us-all-in/`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 6. [AURORA P2] Build the restrained component library

**Labels:** `enhancement`, `ux`, `accessibility`, `track-b`, `aurora-v2`, `priority:medium`

### Problem

The old "20+ components" goal risks turning Aurora into a card-heavy kit. The redesign needs a smaller, restrained component system that supports real workflows: media modules, CTAs, forms, footer IA, project cards, article cards, proof chips, and newsletter/search utility.

### Acceptance Criteria

- [ ] Component inventory is documented before implementation.
- [ ] Components cover project card, talk card, media band, proof chip, CTA row, article card, testimonial, form, footer section, newsletter utility, and search utility.
- [ ] Cards are only used for repeated items, not for every page section.
- [ ] No card-inside-card layouts.
- [ ] Components have hover, focus, active, disabled, loading/empty, mobile, and reduced-motion states where applicable.
- [ ] Forms are accessible and conversion-oriented.
- [ ] Footer supports primary utility IA and project network links.

### References

- `theme/kk-aurora/parts/footer.html`
- `theme/kk-aurora/patterns/`
- `docs/current-state/NAV-IA-DECISION-PACK-2026-05-18.md`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`

---

## 7. [AURORA P2] Run performance and accessibility QA on real staging

**Labels:** `enhancement`, `bug`, `accessibility`, `performance`, `mobile`, `track-b`, `aurora-v2`, `priority:high`

### Problem

Aurora uses rich visuals and animation. That can only ship if performance, accessibility, and real-content rendering hold up under staging conditions.

### Acceptance Criteria

- [ ] QA runs against Local or Cloudways/Pagely staging with Aurora active and production-like content.
- [ ] Desktop and mobile screenshots captured for homepage, About, Work or Speaking, and at least two posts.
- [ ] Keyboard navigation works through header, nav, CTAs, cards, forms, and footer.
- [ ] Reduced-motion pass confirms no essential content depends on animation.
- [ ] Contrast pass covers major components and template surfaces.
- [ ] Media loading strategy is documented, including hero/poster dimensions and lazy loading.
- [ ] Console errors are captured and resolved or documented.
- [ ] Cutover remains blocked until QA passes and activation rollback gates are ready.

### References

- `docs/current-state/AURORA-STAGING-REPORT-2026-05-18.md`
- `docs/current-state/BACKUP_PLAN.md`
- `docs/current-state/ROLLBACK_PLAYBOOK.md`
- `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md`
