# KK AURORA Theme - Implementation Plan

> Award-Winning Cyberpunk WordPress Theme for kriskrug.co

**Version:** 1.0.0
**Target:** WordPress 6.9+ Full Site Editing
**Status:** In Development

---

## Vision Statement

AURORA is a custom WordPress FSE theme that embodies the intersection of art, AI, and Indigenous wisdom. It features flowing cyberpunk gradients, deep space aesthetics, and purposeful motion design that creates an unforgettable digital experience while maintaining WCAG 2.1 AA accessibility.

**Design Philosophy:**
- Every pixel serves a purpose
- Motion enhances understanding, never distracts
- Accessibility is non-negotiable
- Performance is a feature
- The gradient is the signature

---

## Technical Architecture

### Theme Type: Full Site Editing (FSE) Block Theme

```
kk-aurora/
├── style.css                 # Theme header + base styles
├── theme.json                # Design tokens, settings, styles
├── functions.php             # Enqueues, block registration
├── screenshot.png            # Theme preview (1200x900)
├── readme.txt                # WordPress.org description
│
├── templates/                # Full page templates
│   ├── index.html            # Default/fallback
│   ├── home.html             # Homepage
│   ├── single.html           # Single post
│   ├── page.html             # Single page
│   ├── archive.html          # Archive/category
│   ├── search.html           # Search results
│   └── 404.html              # Error page
│
├── parts/                    # Reusable template parts
│   ├── header.html           # Site header
│   ├── footer.html           # Site footer
│   ├── sidebar.html          # Optional sidebar
│   └── comments.html         # Comments section
│
├── patterns/                 # Block patterns
│   ├── hero-gradient.php     # Hero with animated gradient
│   ├── card-glow.php         # Card with hover glow
│   ├── stats-counter.php     # Animated statistics
│   ├── cta-block.php         # Call to action
│   ├── testimonial.php       # Quote with attribution
│   └── ...
│
├── assets/
│   ├── css/
│   │   ├── custom-properties.css   # CSS variables
│   │   ├── animations.css          # Keyframes, transitions
│   │   ├── components.css          # Component styles
│   │   └── utilities.css           # Utility classes
│   ├── js/
│   │   ├── aurora-animations.js    # GSAP/ScrollTrigger
│   │   └── theme.js                # General functionality
│   ├── fonts/                      # Self-hosted fonts
│   └── images/                     # Theme images
│
└── blocks/                   # Custom blocks (if needed)
    └── ...
```

---

## Design System Specification

### Color Palette

```css
/* ============================================
   AURORA COLOR SYSTEM
   Deep space with iridescent accents
   ============================================ */

/* Background Layers (darkest to lightest) */
--aurora-void: #000000;           /* True black - reserved for borders/lines */
--aurora-deep: #0D0D12;           /* Deep space - primary background */
--aurora-surface: #12121A;        /* Elevated surfaces - cards, modals */
--aurora-elevated: #1A1A25;       /* Hover states, active elements */
--aurora-muted: #252532;          /* Disabled states, subtle dividers */

/* Text Hierarchy */
--aurora-text-primary: #F0F0F5;   /* Headlines, primary content */
--aurora-text-secondary: #B8B8C8; /* Body text, descriptions */
--aurora-text-muted: #6B6B80;     /* Captions, metadata, placeholders */
--aurora-text-disabled: #4A4A5A;  /* Disabled text */

/* The Gradient Spectrum */
--aurora-cyan: #00E5FF;           /* Primary accent - links, focus */
--aurora-teal: #00BFA5;           /* Secondary accent - success, CTAs */
--aurora-purple: #8B5CF6;         /* Tertiary - tags, badges */
--aurora-pink: #EC4899;           /* Quaternary - highlights, alerts */
--aurora-blue: #3B82F6;           /* Quinary - info states */

/* The Signature Gradient */
--aurora-gradient-primary: linear-gradient(135deg, #00E5FF 0%, #00BFA5 50%, #8B5CF6 100%);
--aurora-gradient-secondary: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
--aurora-gradient-subtle: linear-gradient(135deg, #00E5FF20 0%, #8B5CF620 100%);

/* Glow Effects */
--aurora-glow-cyan: 0 0 30px #00E5FF40, 0 0 60px #00E5FF20;
--aurora-glow-teal: 0 0 30px #00BFA540, 0 0 60px #00BFA520;
--aurora-glow-purple: 0 0 30px #8B5CF640, 0 0 60px #8B5CF620;

/* Semantic Colors */
--aurora-success: #00BFA5;
--aurora-warning: #F59E0B;
--aurora-error: #EF4444;
--aurora-info: #3B82F6;

/* Border Colors */
--aurora-border-subtle: #1F1F2E;
--aurora-border-default: #2A2A3D;
--aurora-border-strong: #3A3A50;
--aurora-border-gradient: linear-gradient(135deg, #00E5FF40 0%, #8B5CF640 100%);
```

### Typography System

```css
/* ============================================
   AURORA TYPOGRAPHY
   Modern, readable, technical
   ============================================ */

/* Font Families */
--font-display: 'Instrument Sans', 'Inter', system-ui, sans-serif;
--font-body: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* Font Sizes - Fluid Typography */
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);      /* 12-14px */
--text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);         /* 14-16px */
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);        /* 16-18px */
--text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);       /* 18-20px */
--text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);        /* 20-24px */
--text-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);         /* 24-32px */
--text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);     /* 30-40px */
--text-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3rem);         /* 36-48px */
--text-5xl: clamp(3rem, 2rem + 5vw, 4.5rem);               /* 48-72px */
--text-hero: clamp(3.5rem, 2.5rem + 7vw, 7rem);            /* 56-112px */

/* Font Weights */
--weight-normal: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
--weight-black: 900;

/* Line Heights */
--leading-none: 1;
--leading-tight: 1.15;
--leading-snug: 1.3;
--leading-normal: 1.5;
--leading-relaxed: 1.65;
--leading-loose: 1.8;

/* Letter Spacing */
--tracking-tighter: -0.03em;
--tracking-tight: -0.015em;
--tracking-normal: 0;
--tracking-wide: 0.015em;
--tracking-wider: 0.03em;
```

### Spacing System

```css
/* ============================================
   AURORA SPACING
   8px base unit system
   ============================================ */

--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */
--space-40: 10rem;    /* 160px */
--space-48: 12rem;    /* 192px */

/* Content Width */
--width-prose: 70ch;            /* Optimal reading width */
--width-content: 1280px;        /* Main content max */
--width-wide: 1440px;           /* Wide content max */
--width-full: 100%;             /* Full width */
```

### Border & Radius

```css
/* ============================================
   AURORA BORDERS & RADIUS
   Sharp with subtle curves
   ============================================ */

--radius-none: 0;
--radius-sm: 0.25rem;    /* 4px - buttons, inputs */
--radius-md: 0.5rem;     /* 8px - cards, modals */
--radius-lg: 0.75rem;    /* 12px - large cards */
--radius-xl: 1rem;       /* 16px - featured sections */
--radius-2xl: 1.5rem;    /* 24px - hero elements */
--radius-full: 9999px;   /* Pills, avatars */

--border-width-thin: 1px;
--border-width-default: 2px;
--border-width-thick: 3px;
```

### Shadows & Effects

```css
/* ============================================
   AURORA SHADOWS & EFFECTS
   Glows over traditional shadows
   ============================================ */

/* Elevation Shadows (subtle) */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.3);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.25);

/* Glow Shadows (signature) */
--glow-sm: 0 0 10px var(--aurora-cyan, #00E5FF)20;
--glow-md: 0 0 20px var(--aurora-cyan, #00E5FF)30;
--glow-lg: 0 0 30px var(--aurora-cyan, #00E5FF)40, 0 0 60px var(--aurora-cyan, #00E5FF)20;

/* Glass Effect */
--glass-bg: rgba(18, 18, 26, 0.8);
--glass-blur: blur(12px);
--glass-border: 1px solid rgba(255, 255, 255, 0.1);

/* Noise Texture */
--noise-opacity: 0.03;
```

### Animation Tokens

```css
/* ============================================
   AURORA ANIMATION
   Smooth, purposeful, respectful
   ============================================ */

/* Durations */
--duration-instant: 0ms;
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
--duration-slower: 700ms;
--duration-slowest: 1000ms;

/* Easings */
--ease-linear: linear;
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);

/* Gradient Animation */
--gradient-shift-duration: 15s;

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  --duration-instant: 0ms;
  --duration-fast: 0ms;
  --duration-normal: 0ms;
  --duration-slow: 0ms;
  --gradient-shift-duration: 0ms;
}
```

---

## Component Specifications

### 1. Header/Navigation

**Structure:**
```
┌─────────────────────────────────────────────────────────┐
│  LOGO          NAV LINKS              CTA BUTTON        │
│  [KK]    About  Work  Services  Blog    [Let's Talk]    │
└─────────────────────────────────────────────────────────┘
```

**Behavior:**
- Fixed position with glass blur on scroll
- Logo: Text "KK" with gradient on hover
- Nav links: Gradient underline slides in on hover
- CTA: Solid button with gradient border
- Mobile: Hamburger menu with full-screen overlay

**States:**
- Default: Transparent background
- Scrolled: Glass effect (`backdrop-filter: blur(12px)`)
- Mobile open: Full viewport gradient overlay

### 2. Hero Block

**Structure:**
```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│         Bridging Art, AI,                               │
│     Indigenous Wisdom & Justice                         │
│                                                          │
│     [BC+AI]  [Indigenomics]  [The Upgrade AI]          │
│                                                          │
│     [Explore My Work]  [Let's Connect]                  │
│                                                          │
│     ↓ Scroll to discover                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Visual Effects:**
- Animated gradient background (slow shift)
- Floating particles (WebGL or CSS, performance-conscious)
- Text reveal animation on load
- Role badges with gradient borders
- Scroll indicator pulses

### 3. Card Component

**Variants:**
- **Project Card:** Image + title + description + tags
- **Blog Card:** Image + category + title + excerpt + date
- **Stat Card:** Icon + number + label
- **Service Card:** Icon + title + description + CTA

**Hover Effects:**
- Lift: `transform: translateY(-4px)`
- Glow: Gradient shadow appears
- Border: Becomes gradient
- Content: Slight scale

### 4. Stats Counter

**Structure:**
```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  2,000+  │ │   250+   │ │  $200B+  │ │ Fortune  │
│ Members  │ │ Monthly  │ │Discovery │ │   500    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

**Animation:**
- Numbers count up when scrolled into view
- Staggered reveal (left to right)
- Subtle glow pulse on complete

### 5. CTA Block

**Variants:**
- **Primary:** Solid gradient background, white text
- **Secondary:** Transparent with gradient border
- **Ghost:** Text only with underline

**Hover:**
- Primary: Glow increases, slight scale
- Secondary: Background fills with gradient
- Ghost: Underline extends

### 6. Footer

**Structure:**
```
┌─────────────────────────────────────────────────────────┐
│  LOGO        LINKS           LINKS         NEWSLETTER   │
│  [KK]        About           BC+AI         [Email    ]  │
│              Work            Indigenomics  [Subscribe]  │
│  Bridging... Services        The Upgrade               │
│              Blog                                       │
├─────────────────────────────────────────────────────────┤
│  © 2026 Kris Krug    ·    Privacy    ·    Accessibility │
│                                                          │
│  [Twitter] [LinkedIn] [GitHub] [Instagram]              │
└─────────────────────────────────────────────────────────┘
```

**Visual:**
- Subtle gradient divider at top
- Glass effect background
- Social icons with hover glow

---

## Animation Specifications

### Page Load Sequence

```
0ms     - Page renders with minimal layout
100ms   - Header fades in
200ms   - Hero headline reveals (word by word)
500ms   - Hero description fades up
700ms   - Role badges stagger in
900ms   - CTA buttons fade in
1200ms  - Scroll indicator appears
```

### Scroll Animations (ScrollTrigger)

| Element | Trigger | Animation |
|---------|---------|-----------|
| Section headings | 20% viewport | Fade up + slide |
| Cards | 15% viewport | Stagger fade up |
| Stats | 50% viewport | Count up numbers |
| Images | 10% viewport | Fade + scale |
| Dividers | 30% viewport | Gradient reveal |

### Hover Animations

| Element | Animation | Duration |
|---------|-----------|----------|
| Links | Gradient underline slides | 300ms |
| Cards | Lift + glow | 300ms |
| Buttons | Glow increase | 200ms |
| Nav items | Background fade | 200ms |
| Social icons | Scale + glow | 200ms |

### Continuous Animations

| Element | Animation | Duration |
|---------|-----------|----------|
| Hero gradient | Color shift | 15s loop |
| Particles | Float + fade | Infinite |
| Scroll indicator | Pulse | 2s loop |
| Gradient borders | Rotate | 8s loop |

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance

**Color Contrast:**
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- UI components: 3:1 minimum

**Tested Combinations:**
| Background | Foreground | Ratio | Pass |
|------------|------------|-------|------|
| #0D0D12 | #F0F0F5 | 15.2:1 | ✓ |
| #0D0D12 | #B8B8C8 | 8.9:1 | ✓ |
| #0D0D12 | #00E5FF | 8.7:1 | ✓ |
| #12121A | #F0F0F5 | 14.1:1 | ✓ |
| #1A1A25 | #F0F0F5 | 12.3:1 | ✓ |

**Motion:**
- All animations respect `prefers-reduced-motion`
- No auto-playing video/audio
- Animations can be paused
- No flashing content (< 3 flashes/second)

**Keyboard:**
- All interactive elements focusable
- Visible focus indicators (cyan glow ring)
- Logical tab order
- Skip navigation link
- No keyboard traps

**Screen Readers:**
- Semantic HTML structure
- ARIA labels where needed
- Alt text on all images
- Heading hierarchy (h1 → h2 → h3)
- Link text is descriptive

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| LCP | < 2.5s | Largest Contentful Paint |
| FID | < 100ms | First Input Delay |
| CLS | < 0.1 | Cumulative Layout Shift |
| TTI | < 3.8s | Time to Interactive |
| Total Page Weight | < 1.5MB | Including images |
| JS Bundle | < 100KB | Gzipped |
| CSS Bundle | < 50KB | Gzipped |
| Font Load | < 100KB | Subset + swap |

### Performance Strategies

1. **Critical CSS inlined** in `<head>`
2. **Fonts:** `font-display: swap`, subset to Latin
3. **Images:** WebP with JPEG fallback, lazy load
4. **JS:** Deferred, code-split by route
5. **Animations:** GPU-accelerated (transform, opacity)
6. **Particles:** Canvas-based, max 50 particles
7. **Gradient animations:** CSS-only where possible

---

## Testing Checklist

### Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Safari iOS
- [ ] Chrome Android

### Devices
- [ ] Desktop 1920px
- [ ] Desktop 1440px
- [ ] Laptop 1280px
- [ ] Tablet 768px
- [ ] Mobile 375px
- [ ] Mobile 320px

### Accessibility
- [ ] WAVE audit (0 errors)
- [ ] axe DevTools (0 critical)
- [ ] Lighthouse Accessibility > 95
- [ ] Keyboard navigation complete
- [ ] Screen reader test (VoiceOver)
- [ ] Reduced motion test

### Performance
- [ ] Lighthouse Performance > 90
- [ ] Core Web Vitals all green
- [ ] PageSpeed Insights > 90
- [ ] WebPageTest (3G test)

---

## Implementation Phases

### Phase 1: Foundation (Current)
- [x] Directory structure
- [ ] theme.json with design tokens
- [ ] style.css with base styles
- [ ] functions.php setup
- [ ] Custom properties CSS

### Phase 2: Template Parts
- [ ] header.html
- [ ] footer.html
- [ ] Basic templates (index, page, single)

### Phase 3: Components
- [ ] Hero block pattern
- [ ] Card patterns (project, blog, stat)
- [ ] CTA patterns
- [ ] Navigation patterns

### Phase 4: Animations
- [ ] Base transitions CSS
- [ ] GSAP/ScrollTrigger integration
- [ ] Scroll animations
- [ ] Hover effects
- [ ] Page load sequence

### Phase 5: Templates
- [ ] Homepage template
- [ ] About page
- [ ] Work/Projects
- [ ] Services
- [ ] Blog listing
- [ ] Single post
- [ ] 404 page

### Phase 6: Polish
- [ ] Micro-interactions
- [ ] Loading states
- [ ] Error states
- [ ] Print styles
- [ ] Final accessibility audit

---

## File Naming Conventions

- **Templates:** `kebab-case.html` (e.g., `single-post.html`)
- **Parts:** `kebab-case.html` (e.g., `header.html`)
- **Patterns:** `kebab-case.php` (e.g., `hero-gradient.php`)
- **CSS:** `kebab-case.css` (e.g., `custom-properties.css`)
- **JS:** `kebab-case.js` (e.g., `aurora-animations.js`)

---

## Version Control

All theme files will be committed to:
```
/home/user/kriskrug-wp/theme/kk-aurora/
```

Commit messages follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `style:` Styling changes
- `refactor:` Code refactoring
- `docs:` Documentation
- `test:` Testing
- `chore:` Maintenance

---

**Let's build something award-winning.**
