# KK Aurora Theme

Cyberpunk FSE block theme for kriskrug.co

## Quick Install

### Option 1: WordPress Admin (Easiest)
1. Go to `wp-admin` → **Appearance** → **Themes** → **Add New** → **Upload Theme**
2. Upload `kk-aurora.zip`
3. Click **Activate**

### Option 2: Via SSH/SFTP
```bash
# From this repo directory
scp theme/kk-aurora.zip master_qcteaefabe@24.144.80.107:/tmp/

# SSH into server
ssh master_qcteaefabe@24.144.80.107

# Unzip to themes directory
cd ~/applications/*/public_html/wp-content/themes/
unzip /tmp/kk-aurora.zip
rm /tmp/kk-aurora.zip

# Activate via WP-CLI
wp theme activate kk-aurora
```

### Option 3: Cloudways File Manager
1. Log into Cloudways Dashboard
2. Go to **Applications** → Your App → **File Manager**
3. Navigate to `public_html/wp-content/themes/`
4. Upload `kk-aurora.zip` and extract

## Theme Features

- Dark cyberpunk aesthetic (black on black with cyan/teal/purple gradients)
- Full Site Editing (FSE) block theme
- Custom block patterns (hero, stats counter)
- Micro-interactions (cursor glow, card spotlights, scroll reveals)
- GSAP animations
- View Transitions API
- Scroll-driven CSS animations
- WCAG 2.1 AA accessible
- prefers-reduced-motion support

## Design Tokens

See `theme.json` for:
- Color palette (deep, surface, cyan, teal, purple, pink)
- Typography (Inter, JetBrains Mono)
- Spacing scale
- Shadow presets
- Gradient definitions

## Files

```
kk-aurora/
├── style.css           # Theme header + base styles
├── theme.json          # Design tokens
├── functions.php       # Asset loading
├── templates/          # FSE templates
│   ├── index.html
│   ├── home.html
│   ├── single.html
│   ├── page.html
│   └── 404.html
├── parts/              # Template parts
│   ├── header.html
│   └── footer.html
├── patterns/           # Block patterns
│   ├── hero-gradient.php
│   └── stats-counter.php
└── assets/
    ├── css/
    │   ├── animations.css
    │   ├── bleeding-edge.css
    │   └── typography-refined.css
    └── js/
        ├── theme.js
        ├── aurora-animations.js
        └── micro-interactions.js
```

## After Activation

1. Go to **Appearance** → **Editor** (Site Editor)
2. Customize the homepage hero text
3. Create navigation menu
4. Add pages (About, Work, Services, Contact)
5. Import blog posts from XML export
