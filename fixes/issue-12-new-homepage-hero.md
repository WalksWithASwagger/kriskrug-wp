# Issue #12: New Homepage Hero Content

## NEW HERO SECTION (Copy-Paste Ready)

### Hero Headline
```
Bridging Art, AI, Indigenous Wisdom, and Justice
```

### Hero Subheading
```
Executive Director of BC+AI (250 members) • Indigenomics.ai ally •
Co-founder of The Upgrade AI • 25+ years creating technology that serves
communities, not extraction.
```

### Three Role Badges (Visual Pills/Tags)

```html
<div class="role-badges">
  <span class="badge badge-bcai">BC+AI Executive Director</span>
  <span class="badge badge-indigenomics">Indigenomics Ally</span>
  <span class="badge badge-upgrade">The Upgrade AI Co-founder</span>
</div>
```

### Impact Metrics Section

```html
<div class="impact-metrics">
  <div class="metric">
    <span class="number">250</span>
    <span class="label">BC+AI Community Members</span>
  </div>
  <div class="metric">
    <span class="number">2,400+</span>
    <span class="label">Vancouver AI Attendees (2024)</span>
  </div>
  <div class="metric">
    <span class="number">130K+</span>
    <span class="label">Photos Under CC License</span>
  </div>
  <div class="metric">
    <span class="number">Fortune 500</span>
    <span class="label">Clients Trained</span>
  </div>
  <div class="metric">
    <span class="number">25+</span>
    <span class="label">Years in Tech</span>
  </div>
</div>
```

### Primary & Secondary CTAs

```html
<div class="hero-ctas">
  <a href="/work" class="button button-primary">Explore My Work</a>
  <a href="/contact" class="button button-secondary">Let's Connect</a>
</div>
```

### Full Hero HTML Template

```html
<section class="hero-section">
  <div class="hero-content">
    <h1 class="hero-headline">
      Bridging Art, AI, Indigenous Wisdom, and Justice
    </h1>

    <div class="role-badges">
      <span class="badge badge-bcai">BC+AI Executive Director</span>
      <span class="badge badge-indigenomics">Indigenomics Ally</span>
      <span class="badge badge-upgrade">The Upgrade AI Co-founder</span>
    </div>

    <p class="hero-subheading">
      25+ years creating technology that serves communities, not extraction.
    </p>

    <div class="impact-metrics">
      <div class="metric">
        <span class="number">250</span>
        <span class="label">BC+AI Members</span>
      </div>
      <div class="metric">
        <span class="number">250+</span>
        <span class="label">Vancouver AI (2024)</span>
      </div>
      <div class="metric">
        <span class="number">$200B+</span>
        <span class="label">Indigenous Economic Discovery</span>
      </div>
      <div class="metric">
        <span class="number">Fortune 500</span>
        <span class="label">Clients Trained</span>
      </div>
    </div>

    <div class="hero-ctas">
      <a href="/work" class="button button-primary">Explore My Work</a>
      <a href="/contact" class="button button-secondary">Let's Connect</a>
    </div>
  </div>
</section>
```

### Suggested CSS (Optional Styling)

```css
.hero-section {
  padding: 80px 20px;
  text-align: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.hero-headline {
  font-size: 48px;
  line-height: 1.2;
  margin-bottom: 24px;
  color: #1a1a1a;
}

.role-badges {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 24px 0;
  flex-wrap: wrap;
}

.badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.impact-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 24px;
  margin: 40px 0;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.metric .number {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: #0052CC;
}

.metric .label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.hero-ctas {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

@media (max-width: 768px) {
  .hero-headline {
    font-size: 32px;
  }

  .impact-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .hero-ctas {
    flex-direction: column;
    align-items: center;
  }
}
```

## Implementation

**To apply this:**
1. In WordPress admin: Pages → Edit Homepage
2. Switch to HTML/Code editor
3. Replace hero section with above HTML
4. Add CSS to: Appearance → Customize → Additional CSS
5. Save and publish

**Status:** ✅ Ready to copy-paste into WordPress
