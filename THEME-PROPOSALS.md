# Avant-Garde WordPress Theme Proposals

> Black on Black on Black with Cyberpunk Soul

**For:** Kris Krug - kriskrug.co rebuild
**Inspiration:** Perplexity Dark Mode, Vercel v0/Geist, Terminal Aesthetics
**Vibe:** Techartist. Quasi-sage. Cyberpunk anti-hero from the future.

---

## Design Research Summary

### Perplexity Dark Mode Palette
- **Background:** `#1A1A1A` (forced dark)
- **Surface:** `#242424`, `#3A3A3A` (layered depth)
- **Primary Accent:** `#20B8CD` / `#00C2FF` (signature cyan)
- **Secondary:** `#FF6F59` (coral warmth)
- **Tertiary:** `#3A86FF` (deep blue)

### Vercel/Geist Aesthetic
- **Pure black:** `#000000`
- **Near-black surfaces:** `#0A0A0A`, `#111111`
- **White text:** `#FAFAFA`, `#EDEDED`
- **Philosophy:** "Terminal-inspired precision that makes technical work feel both serious and elegant"
- **Minimal:** Zero visual noise, maximum focus

### 2026 WordPress Tech Stack
- **Theme:** Full Site Editing (FSE) block theme
- **Animations:** Motion.page + GSAP/ScrollTrigger
- **Components:** Custom blocks + theme.json + block patterns
- **Performance:** < 45KB animation load, conditional loading

---

## The Three Directions

---

## Direction A: "VOID"

### Black Hole Minimalism

**Philosophy:** The absence of light IS the design. Content emerges from pure darkness like stars forming in the void.

**Color Palette:**
```css
/* VOID */
--void-abyss: #000000;          /* True black - the void */
--void-surface: #0A0A0A;        /* Near-black cards */
--void-elevated: #111111;       /* Hover states */
--void-border: #1A1A1A;         /* Subtle separation */

--void-text: #FAFAFA;           /* Primary text */
--void-text-muted: #888888;     /* Secondary text */

--void-accent: #00F5D4;         /* Malachite/Teal glow */
--void-accent-dim: #00F5D420;   /* Glow at 12% */
--void-warm: #FF6B6B;           /* Human warmth (sparingly) */
```

**Visual Treatment:**
- True `#000000` background - unapologetically dark
- Content cards float on near-black surfaces with subtle borders
- Text emerges white-on-black, like a terminal
- Accent color ONLY for interactive elements and emphasis
- Subtle glow effects around focused elements
- Gradient borders that pulse subtly

**Typography:**
```css
--font-display: 'Space Grotesk', system-ui;    /* Bold, geometric */
--font-body: 'Inter', system-ui;                /* Clean, readable */
--font-mono: 'JetBrains Mono', monospace;       /* Code, data */
```

**Signature Elements:**
- **Hero:** Massive typography, single accent word glows
- **Cards:** Float on `#0A0A0A` with `1px` border, lift on hover
- **Buttons:** Ghost buttons with glow on hover
- **Links:** Underline on hover, accent color
- **Code blocks:** Terminal-style with scan line effect

**Animation Philosophy:**
- Minimal but meaningful
- Fade-in on scroll (content reveals itself)
- Subtle glow pulse on accent elements
- Cursor leaves faint trail (opt-in)

**Best For:** Maximum authority, developer credibility, "I know what I'm doing" energy

---

## Direction B: "AURORA"

### Cyberpunk Gradients

**Philosophy:** The future is iridescent. Light bends at the edges of the digital frontier.

**Color Palette:**
```css
/* AURORA */
--aurora-deep: #0D0D12;         /* Deep space purple-black */
--aurora-surface: #12121A;      /* Card background */
--aurora-elevated: #1A1A25;     /* Hover states */

--aurora-text: #F0F0F5;         /* Slightly warm white */
--aurora-text-muted: #8888AA;   /* Purple-tinted muted */

/* The gradient spectrum */
--aurora-cyan: #00E5FF;         /* Perplexity cyan */
--aurora-teal: #00BFA5;         /* Malachite green */
--aurora-purple: #8B5CF6;       /* Electric purple */
--aurora-pink: #EC4899;         /* Neon pink */

/* The signature gradient */
--aurora-gradient: linear-gradient(
  135deg, 
  #00E5FF 0%, 
  #00BFA5 25%, 
  #8B5CF6 75%, 
  #EC4899 100%
);
```

**Visual Treatment:**
- Deep purple-black base (`#0D0D12`)
- Gradient accents on borders, highlights, hover states
- Animated gradient that slowly shifts (like aurora borealis)
- Glassmorphism effects on elevated surfaces
- Subtle noise texture overlay for depth

**Typography:**
```css
--font-display: 'Instrument Sans', system-ui;  /* Modern, editorial */
--font-body: 'Inter', system-ui;
--font-mono: 'Fira Code', monospace;           /* Ligatures! */
```

**Signature Elements:**
- **Hero:** Animated gradient text, floating particles
- **Cards:** Gradient border on hover, glass effect
- **Buttons:** Solid with gradient shine on hover
- **Navigation:** Gradient underline flows on hover
- **Section dividers:** Horizontal gradient lines

**Animation Philosophy:**
- Flowing, organic movement
- Gradient shifts slowly (15-20s loops)
- Elements float slightly, like underwater
- Hover effects have momentum/easing
- Particle effects respond to scroll

**Best For:** Creative authority, "art meets tech" positioning, memorable visual identity

---

## Direction C: "MONOLITH"

### Editorial Brutalism

**Philosophy:** Bold typography IS the design. Content commands attention through sheer presence.

**Color Palette:**
```css
/* MONOLITH */
--mono-black: #0C0C0C;          /* Rich black */
--mono-surface: #141414;        /* Card background */
--mono-elevated: #1C1C1C;       /* Hover states */
--mono-border: #2A2A2A;         /* Visible borders */

--mono-white: #FFFFFF;          /* Pure white text */
--mono-gray: #999999;           /* Muted text */

--mono-accent: #00D9B5;         /* Single teal accent */
--mono-accent-hover: #00F5CD;   /* Brighter on hover */
```

**Visual Treatment:**
- Large, confident typography dominates
- Asymmetric layouts with intentional tension
- Heavy borders (2-3px) create structure
- Lots of whitespace (blackspace?) for breathing room
- Photos are high-contrast, duotone treatment
- Accent color is surgical - only for CTAs and key links

**Typography:**
```css
--font-display: 'Archivo Black', system-ui;    /* LOUD */
--font-body: 'Source Sans 3', system-ui;       /* Readable */
--font-mono: 'IBM Plex Mono', monospace;       /* Technical */

/* Massive display sizes */
--text-hero: clamp(4rem, 12vw, 10rem);
--text-h1: clamp(3rem, 8vw, 6rem);
```

**Signature Elements:**
- **Hero:** Text so large it crops at viewport edge
- **Cards:** Thick borders, no radius, raw edges
- **Buttons:** Solid blocks, uppercase, no curves
- **Links:** Bold underline, no color change needed
- **Pull quotes:** Oversized, overlapping other content

**Animation Philosophy:**
- Minimal and abrupt
- Elements snap into place (no soft easing)
- Scroll-triggered reveals are instant, not gradual
- Hover states are immediate, decisive
- Motion respects the brutalist ethos

**Best For:** Maximum statement, editorial authority, "I have something important to say"

---

## Comparison Matrix

| Aspect | VOID | AURORA | MONOLITH |
|--------|------|--------|----------|
| **Primary Vibe** | Terminal elegance | Cyberpunk iridescence | Editorial brutalism |
| **Background** | Pure `#000000` | Purple-black `#0D0D12` | Rich black `#0C0C0C` |
| **Accent Strategy** | Single glow color | Flowing gradients | Surgical single color |
| **Typography** | Space Grotesk | Instrument Sans | Archivo Black |
| **Animation** | Subtle, fade-based | Flowing, organic | Snappy, immediate |
| **Complexity** | Low | Medium-High | Low |
| **Best For** | Developer cred | Creative cred | Thought leader cred |
| **Perplexity-like** | ★★★★★ | ★★★☆☆ | ★★☆☆☆ |
| **Vercel-like** | ★★★★★ | ★★★☆☆ | ★★★☆☆ |

---

## Recommended Direction: VOID + AURORA Hybrid

### "SINGULARITY"

Take VOID's clean black foundation and add AURORA's accent treatment.

```css
/* SINGULARITY - The Best of Both */

/* VOID foundation */
--bg-primary: #000000;
--bg-surface: #0A0A0A;
--bg-elevated: #111111;
--border-subtle: #1A1A1A;
--border-visible: #2A2A2A;

/* Pure text */
--text-primary: #FAFAFA;
--text-secondary: #888888;
--text-muted: #555555;

/* AURORA accent system */
--accent-primary: #00E5FF;      /* Perplexity cyan */
--accent-secondary: #00BFA5;    /* Malachite teal */
--accent-gradient: linear-gradient(135deg, #00E5FF 0%, #00BFA5 100%);

/* Warm human touch */
--accent-warm: #FF6B6B;         /* For CTAs, urgency */

/* Glow effects */
--glow-accent: 0 0 20px #00E5FF40;
--glow-warm: 0 0 20px #FF6B6B40;
```

**Why This Works:**
1. **Authority:** Pure black says "I'm serious about what I do"
2. **Tech Credibility:** Terminal aesthetic resonates with AI/tech audience
3. **Visual Interest:** Gradient accents add life without chaos
4. **Accessibility:** High contrast, clear hierarchy
5. **Performance:** Minimal decorative elements = fast
6. **Recognizable:** Cyan accent becomes signature color

---

## Implementation Approach

### Phase 1: Foundation
1. Create FSE block theme with `theme.json`
2. Define design tokens (CSS custom properties)
3. Build base typography system
4. Create color palette with dark mode as default

### Phase 2: Components
1. Header/navigation with accent hover states
2. Hero block with large typography
3. Card component with hover glow
4. Button system (ghost + solid variants)
5. Footer with subtle gradient accent

### Phase 3: Interactions (Motion.page + GSAP)
1. Scroll-triggered fade-in reveals
2. Hero text animation on load
3. Card hover lift + glow
4. Navigation underline slide
5. Scroll progress indicator
6. Optional: cursor glow trail

### Phase 4: Content Templates
1. Homepage with impact metrics
2. About page (polymath story)
3. Work/Projects showcase
4. Services page
5. Blog listing with category filters
6. Single post (reading-optimized)

### Phase 5: Polish
1. Loading states
2. 404 page (styled)
3. Micro-interactions
4. Performance optimization
5. Accessibility audit

---

## Tech Stack Recommendation

| Layer | Choice | Why |
|-------|--------|-----|
| **Theme Type** | Custom FSE Block Theme | Maximum control, future-proof |
| **CSS** | CSS Custom Properties + Tailwind (optional) | Design tokens, utility classes |
| **Animations** | Motion.page + custom GSAP | Visual builder + code flexibility |
| **Icons** | Lucide or Phosphor | Clean, consistent, MIT licensed |
| **Fonts** | Google Fonts (subset) | Space Grotesk + Inter + JetBrains Mono |
| **Build** | @wordpress/scripts | Standard WP tooling |

---

## Next Steps

1. **Pick a direction** (or confirm SINGULARITY hybrid)
2. **I'll create the theme.json** with full design tokens
3. **Build the homepage** as proof of concept
4. **Iterate on components** based on feedback
5. **Layer in animations** with Motion.page

---

**The void awaits. What direction speaks to you?**
