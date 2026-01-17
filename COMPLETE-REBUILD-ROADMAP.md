# Complete WordPress Rebuild Roadmap

> From Old Site to Avant-Garde AI-Playful Masterpiece

**Last Updated:** 2026-01-17
**Status:** READY TO EXECUTE

---

## The Vision

Transform kriskrug.co from a photography-focused site into an **avant-garde, AI-playful digital hub** that positions Kris as a polymath bridging art, AI, Indigenous wisdom, and justice. Think: Cyberpunk meets community warmth. Bold typography meets accessibility. Experimental aesthetics meets rock-solid performance.

**Design Philosophy:**
- **AI-Playful:** Subtle generative elements, dynamic interactions, unexpected delights
- **Avant-Garde:** Bold typography, asymmetric layouts, striking color palettes
- **Accessible:** WCAG 2.1 AA minimum, keyboard navigable, screen reader friendly
- **Fast:** < 3 seconds load on 3G, mobile-first, progressive enhancement

---

## Phase 0: Content Extraction & Inventory
**Duration: Foundation step**

### 0.1 Blog Post Migration Setup

Your XML export is sitting at:
```
/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml
```

**Tasks:**
- [ ] Move XML export into this repo: `content/exports/wordpress-export-2026-01-03.xml`
- [ ] Run blog post inventory extraction
- [ ] Categorize posts by topic/type
- [ ] Identify posts to keep, archive, or retire
- [ ] Extract featured images and media assets
- [ ] Map old URLs for redirects

**Blog Post Categories to Create:**
| Category | Description |
|----------|-------------|
| AI & Technology | AI insights, tool reviews, future trends |
| BC+AI | Community updates, Vancouver AI stories |
| Indigenomics | Indigenous tech sovereignty, Indigenomics.ai |
| The Upgrade AI | Training, democratizing AI, Fortune 500 work |
| Photography | Visual work, creative process (de-emphasized) |
| Speaking & Events | Keynotes, workshops, conference appearances |
| Personal Essays | Philosophy, reflections, cyberpunk musings |

### 0.2 Current Site Audit

- [ ] Screenshot every current page for reference
- [ ] Export current navigation structure
- [ ] List all existing plugins
- [ ] Document any custom functionality
- [ ] Note any integrations (Luma, Notion, etc.)

---

## Phase 1: Infrastructure & Fresh WordPress
**Duration: First milestone**

### 1.1 Clean WordPress Installation

**On Cloudways (already running WordPress 6.9):**
- [ ] Back up current dev instance
- [ ] Clean install or import production site
- [ ] Configure WordPress basics:
  - Site title: "Kris Krug | Bridging Art, AI, Indigenous Wisdom & Justice"
  - Tagline: "Executive Director BC+AI | CTO Indigenomics.ai | Co-founder The Upgrade AI"
  - Timezone: PST
  - Permalink structure: /%postname%/
  - Canadian English locale

### 1.2 Essential Plugins

**Performance & Security:**
- [ ] Breeze (already installed) - caching
- [ ] Object Cache Pro (already installed) - Redis
- [ ] Wordfence or Solid Security - security
- [ ] UpdraftPlus - backups
- [ ] Redirection - URL redirects (critical for blog migration)

**SEO & Content:**
- [ ] Yoast SEO or Rank Math
- [ ] Schema Pro or manual schema (we have code ready)
- [ ] XML Sitemap generator

**Functionality:**
- [ ] WPForms or Gravity Forms - contact forms
- [ ] Social Warfare or similar - social sharing
- [ ] Lazy Load - images
- [ ] EWWW Image Optimizer - compression

**Accessibility:**
- [ ] WP Accessibility Helper
- [ ] One Click Accessibility (or build custom)

---

## Phase 2: Theme Selection & Customization
**Duration: Second milestone**

### 2.1 Theme Strategy

**Option A: Full Site Editing (FSE) Theme - RECOMMENDED**

Use a modern block-based theme for maximum flexibility:

| Theme | Why Consider |
|-------|--------------|
| **Flavor** | Avant-garde aesthetic, bold typography, highly customizable |
| **Flavor Dark** | Moody cyberpunk vibes, perfect for AI-playful aesthetic |
| **Flavor Portfolio** | Showcase-focused, photography integration |
| **Developer-built custom** | Maximum control, built to spec |

**Option B: Page Builder Approach**

If more visual control needed:
- Breakdance Builder + custom CSS
- Bricks Builder + design system
- Elementor Pro + custom widgets

### 2.2 Design System Creation

**Typography:**
```css
/* AI-Playful Typography System */
--font-display: 'Space Grotesk', sans-serif;  /* Bold headers */
--font-body: 'Inter', sans-serif;              /* Clean readability */
--font-mono: 'JetBrains Mono', monospace;      /* Code/tech elements */

--text-hero: clamp(3rem, 8vw, 6rem);
--text-h1: clamp(2.5rem, 5vw, 4rem);
--text-h2: clamp(2rem, 4vw, 3rem);
--text-body: clamp(1rem, 2vw, 1.125rem);
```

**Color Palette:**
```css
/* Avant-Garde AI Palette */
--color-primary: #0D0D0D;      /* Near black - authority */
--color-accent: #00F0FF;        /* Cyan - AI/tech energy */
--color-warm: #FF6B35;          /* Coral - human warmth */
--color-indigenous: #8B4513;    /* Earth - Indigenous roots */
--color-gradient-ai: linear-gradient(135deg, #00F0FF, #8B5CF6);

/* Accessibility-First Neutrals */
--color-surface: #FAFAFA;
--color-surface-dark: #1A1A2E;
--color-text: #1A1A1A;
--color-text-muted: #6B7280;
```

**AI-Playful Elements:**
- Subtle animated gradients on hover
- Particle effects on hero (performance-conscious)
- Morphing shapes that respond to scroll
- "Glitch" text effects on special elements
- Dynamic cursor trails (opt-in, not default)

### 2.3 Component Library

Build these reusable blocks:

| Component | Purpose |
|-----------|---------|
| Hero Block | Bold headline + gradient + CTAs |
| Role Badge | BC+AI / Indigenomics / The Upgrade AI |
| Impact Counter | Animated stat display (2,000+ members) |
| Project Card | Work showcase with hover effects |
| Blog Card | Post preview with category badge |
| Testimonial | Social proof with subtle animation |
| CTA Block | Primary/secondary action buttons |
| Event Card | Luma integration or native |
| Contact Form | Accessible, styled form |
| Footer | Mega footer with links + social |

---

## Phase 3: Core Pages Build
**Duration: Third milestone**

### 3.1 Homepage

**Structure:**
```
┌─────────────────────────────────────────────┐
│ HERO                                         │
│ "Bridging Art, AI, Indigenous Wisdom         │
│  & Justice"                                  │
│ [BC+AI] [Indigenomics] [The Upgrade AI]      │
│ [Explore My Work] [Let's Connect]            │
├─────────────────────────────────────────────┤
│ IMPACT METRICS (animated counters)           │
│ 2,000+ Members | 250+ Monthly | Fortune 500  │
├─────────────────────────────────────────────┤
│ THREE PILLARS (expandable cards)             │
│ ┌───────┐ ┌───────┐ ┌───────┐               │
│ │ BC+AI │ │Indige │ │Upgrade│               │
│ │       │ │nomics │ │  AI   │               │
│ └───────┘ └───────┘ └───────┘               │
├─────────────────────────────────────────────┤
│ LATEST WRITING (blog posts slider)           │
├─────────────────────────────────────────────┤
│ UPCOMING EVENTS (Luma or native)             │
├─────────────────────────────────────────────┤
│ CTA: Newsletter / Contact                    │
├─────────────────────────────────────────────┤
│ LAND ACKNOWLEDGMENT                          │
└─────────────────────────────────────────────┘
```

**Content Ready:** `/fixes/issue-12-new-homepage-hero.md`

### 3.2 About Page

**Structure:**
- Hero with professional photo
- Polymath introduction
- Three roles section (equal weight)
- Journey/timeline
- Philosophy section (cyberpunk anti-hero vibes)
- Photography as credential (not primary)
- CTA: Work together

**Content Ready:** `/fixes/UPDATED-ABOUT-PAGE-COMPLETE.md`

### 3.3 Work / Projects Page

**Structure:**
- Hero: "Creating Impact Through Technology"
- BC+AI Ecosystem section
- Indigenomics.ai section
- The Upgrade AI section
- Select Photography (credential)
- Case studies / success metrics

**Content Ready:** `/fixes/issue-68-work-page-complete.md`

### 3.4 Services Page

**Structure:**
- Hero: "How We Can Work Together"
- AI Strategy Consulting
- Community Building Services
- The Upgrade AI Training
- Indigenomics Advisory
- Speaking Engagements
- Photography (available, not primary)
- Booking CTA

**Content Ready:** `/fixes/issue-67-services-page-expanded.md`

### 3.5 Blog / Writing

**Structure:**
- Hero: "Thoughts on Art, AI & What Comes Next"
- Category filters
- Featured posts
- Grid/list toggle
- Pagination or infinite scroll
- Search functionality

**Categories:**
- AI & Technology
- BC+AI
- Indigenomics
- The Upgrade AI
- Photography
- Speaking & Events
- Personal Essays

### 3.6 Contact Page

**Structure:**
- Hero: "Let's Build Something Together"
- Contact form (accessible, tested)
- Direct email option
- Social links
- Speaking inquiry form
- Map or location (optional)

### 3.7 Additional Pages Needed

| Page | Purpose |
|------|---------|
| Newsletter | Email signup landing page |
| Events | Calendar / upcoming events |
| Resources | Downloads, guides, useful links |
| BC+AI Hub | Dedicated section or link out |
| Privacy Policy | Legal requirement |
| Accessibility Statement | Commitment + contact |
| 404 Page | Styled, helpful error page |

---

## Phase 4: Blog Migration Execution
**Duration: Fourth milestone**

### 4.1 XML Import Process

```bash
# 1. Copy XML to repo
cp "/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml" \
   content/exports/wordpress-export-2026-01-03.xml

# 2. Import to WordPress
# WordPress Admin → Tools → Import → WordPress Importer
# Upload the XML file
# Assign author to Kris Krug user
# Import attachments: YES

# 3. Post-import cleanup
# - Check all posts imported
# - Verify categories/tags
# - Test internal links
# - Check featured images
```

### 4.2 Blog Post Processing

**For Each Imported Post:**
- [ ] Review and categorize properly
- [ ] Update featured images (optimize)
- [ ] Add meta descriptions (Yoast)
- [ ] Set canonical URLs
- [ ] Update internal links
- [ ] Add schema markup
- [ ] Check accessibility (images have alt text)

### 4.3 URL Redirect Strategy

**Create redirect map:**
```
/old-post-url/ → /new-category/post-title/
/generative-ai-services/ → /services/
/recent-projects-include/ → /work/
```

**Implementation:**
- Use Redirection plugin
- 301 redirects for SEO preservation
- Test all old URLs after launch

### 4.4 Content Audit & Curation

**Keep:** Posts that align with polymath positioning
**Update:** Posts that need refreshed content
**Archive:** Outdated posts (keep but de-index)
**Retire:** Posts that no longer serve brand

---

## Phase 5: AI-Playful Design Implementation
**Duration: Fifth milestone**

### 5.1 Interactive Elements

**Hero Section:**
```javascript
// Subtle particle system that responds to mouse
// Performance budget: < 60fps, < 50KB
// Accessibility: decorative only, pause on reduce-motion
```

**Scroll Animations:**
- Fade-in text reveals
- Counter animations on scroll
- Parallax images (subtle)
- Progress indicator

**Hover Effects:**
- Card lift + shadow
- Button gradient shifts
- Image zoom + overlay
- Link underline animations

### 5.2 Micro-Interactions

| Element | Interaction |
|---------|-------------|
| Role badges | Subtle pulse on hover |
| Stats counters | Count up on viewport entry |
| Project cards | Tilt effect on hover |
| Navigation | Smooth underline transitions |
| Buttons | Ripple effect on click |
| Forms | Field focus animations |

### 5.3 Accessibility-First Animation

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Phase 6: Performance & SEO
**Duration: Sixth milestone**

### 6.1 Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| Page Size | < 1.5MB |
| Requests | < 50 |
| TTFB | < 600ms |

### 6.2 Performance Checklist

- [ ] Image optimization (WebP, lazy load, responsive)
- [ ] Critical CSS inlined
- [ ] JavaScript deferred/async
- [ ] Font loading optimized (FOUT/FOIT strategy)
- [ ] Caching configured (Breeze + Redis)
- [ ] CDN configured (optional: Cloudflare)
- [ ] Database optimized
- [ ] Gzip/Brotli compression

### 6.3 SEO Implementation

**Already Ready:**
- `/fixes/issue-36-meta-descriptions.md`
- `/fixes/issue-37-xml-sitemap-setup.md`
- `/fixes/issue-39-schema-markup.php`
- `/fixes/issue-43-twitter-cards.php`

**Additional SEO Tasks:**
- [ ] All pages have unique titles and meta descriptions
- [ ] Open Graph tags implemented
- [ ] Twitter Cards configured
- [ ] Schema markup for Person, Organization, Article
- [ ] XML sitemap submitted to Search Console
- [ ] Google Analytics / privacy-respecting analytics
- [ ] robots.txt configured
- [ ] Canonical URLs set

---

## Phase 7: Accessibility Audit
**Duration: Seventh milestone**

### 7.1 WCAG 2.1 AA Compliance

**Already Ready:**
- `/fixes/issue-5-color-contrast.css`
- `/fixes/issue-9-button-hover-states.css`

**Full Audit:**
- [ ] Color contrast (4.5:1 text, 3:1 large text)
- [ ] Keyboard navigation complete
- [ ] Focus indicators visible
- [ ] Alt text on all images
- [ ] ARIA labels where needed
- [ ] Form labels and errors accessible
- [ ] Skip navigation link
- [ ] Heading hierarchy correct
- [ ] Link text descriptive
- [ ] Video captions (if applicable)

### 7.2 Testing Tools

- WAVE browser extension
- axe DevTools
- Lighthouse accessibility audit
- Screen reader testing (NVDA, VoiceOver)
- Keyboard-only navigation test

---

## Phase 8: Pre-Launch Checklist
**Duration: Eighth milestone**

### 8.1 Content Review

- [ ] All pages proofread
- [ ] Links tested (internal and external)
- [ ] Images optimized and have alt text
- [ ] Forms tested and working
- [ ] Contact info correct
- [ ] Social links working

### 8.2 Technical Review

- [ ] SSL certificate valid
- [ ] Mobile responsive (test all devices)
- [ ] Cross-browser tested
- [ ] 404 page works
- [ ] Redirects working
- [ ] Sitemap accessible
- [ ] robots.txt correct
- [ ] Analytics tracking

### 8.3 Security Review

- [ ] Admin account secure (not "admin")
- [ ] Strong passwords
- [ ] Security plugin configured
- [ ] Backups automated
- [ ] Updates applied
- [ ] File permissions correct

### 8.4 Performance Review

- [ ] PageSpeed score > 90
- [ ] Core Web Vitals passing
- [ ] Mobile performance acceptable
- [ ] Image loading fast

---

## Phase 9: Launch & Post-Launch
**Duration: Ninth milestone**

### 9.1 Launch Day

- [ ] DNS updated if changing hosts
- [ ] SSL certificate active
- [ ] Cache cleared and warmed
- [ ] Final content review
- [ ] Backup created
- [ ] Monitoring active

### 9.2 Post-Launch (First Week)

- [ ] Monitor analytics for issues
- [ ] Check Search Console for errors
- [ ] Gather user feedback
- [ ] Fix any reported bugs
- [ ] Submit sitemap to search engines
- [ ] Announce on social media

### 9.3 Ongoing

- [ ] Regular content updates (blog)
- [ ] Monthly performance review
- [ ] Quarterly accessibility audit
- [ ] Security updates maintained
- [ ] Analytics review

---

## Issue Tracking Integration

All tasks above should become GitHub issues for agent automation.

**Batch Structure:**
1. **Batch: Infrastructure** - WordPress setup, plugins, hosting
2. **Batch: Theme & Design** - Theme selection, design system, components
3. **Batch: Core Pages** - Homepage, About, Work, Services, Contact
4. **Batch: Blog Migration** - XML import, categorization, redirects
5. **Batch: Interactive Design** - Animations, micro-interactions, AI-playful elements
6. **Batch: Performance** - Optimization, caching, CDN
7. **Batch: SEO** - Meta, schema, sitemaps, analytics
8. **Batch: Accessibility** - WCAG audit, fixes, testing
9. **Batch: Launch** - Final review, deployment, post-launch

---

## Resource Needs

### Design Assets Needed

- [ ] Professional headshot (high res)
- [ ] BC+AI logo/assets
- [ ] Indigenomics.ai logo/assets
- [ ] The Upgrade AI logo/assets
- [ ] Select photography portfolio images (8-12)
- [ ] Favicon and app icons
- [ ] Open Graph image (1200x630)
- [ ] Brand pattern/texture (optional)

### External Services

| Service | Purpose | Status |
|---------|---------|--------|
| Cloudways | Hosting | Ready |
| Domain (kk.ca) | DNS | Existing |
| GitHub | Code/Issues | Ready |
| Cloudflare | CDN/Security | Consider |
| Luma | Events | Existing integration |
| Notion | Content sync | Existing |

---

## Timeline Dependencies

```
Phase 0 ─────► Phase 1 ─────► Phase 2
(Content)     (WordPress)    (Theme)
                    │
                    ▼
              Phase 3 ◄────── Phase 4
              (Pages)         (Blog Migration)
                    │
                    ▼
              Phase 5 ─────► Phase 6 ─────► Phase 7
              (Design)       (Perf/SEO)    (A11y)
                                                │
                                                ▼
                                          Phase 8 ─────► Phase 9
                                          (Pre-Launch)   (Launch)
```

**Critical Path:**
XML Export → WordPress Import → Theme → Pages → Blog → Launch

---

## Success Metrics

### Technical Success
- [ ] Lighthouse Performance > 90
- [ ] Lighthouse Accessibility > 95
- [ ] Core Web Vitals all green
- [ ] Zero critical accessibility issues
- [ ] All blog posts migrated with redirects

### Brand Success
- [ ] Three roles featured equally
- [ ] Photography de-emphasized
- [ ] Community-first messaging
- [ ] AI-playful aesthetic achieved
- [ ] Professional but warm tone

### User Success
- [ ] Contact form working
- [ ] Events discoverable
- [ ] Blog searchable by category
- [ ] Mobile experience excellent
- [ ] Accessibility verified by real users

---

## Next Steps

**Immediate Actions:**

1. **Move XML export into repo**
   ```bash
   cp "/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml" \
      content/exports/
   ```

2. **Run blog post inventory** - Create list of all posts

3. **Choose theme direction** - FSE vs Page Builder

4. **Create Phase 0-2 GitHub issues** - Feed the agent swarm

5. **Start building** - Homepage first

---

**The future is avant-garde, AI-playful, and accessible as fuck. Let's build it.**

