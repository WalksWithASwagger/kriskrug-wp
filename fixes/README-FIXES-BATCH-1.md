# Kris Krug Website Fixes - Batch 1 (10 Issues)

> **STATUS: Historical.** These January batch fixes need a fresh review against the May 2026 current-state docs before deployment.

**Status:** ✅ Ready to Deploy
**Location:** `/Users/kk/Code/kriskrug-wp/fixes/`

---

## ✅ Completed Fixes (Copy-Paste Ready)

### 1. Issue #5: Color Contrast Fix
**File:** `issue-5-color-contrast.css`
**What it does:** Changes text color from #404040 to #1a1a1a for WCAG AA compliance (7.3:1 ratio)
**How to apply:** Add CSS to Appearance → Customize → Additional CSS
**Time:** 1 minute

### 2. Issue #9: Button Hover States
**File:** `issue-9-button-hover-states.css`
**What it does:** Adds smooth hover transitions to all CTA buttons
**How to apply:** Add CSS to Appearance → Customize → Additional CSS
**Time:** 1 minute

### 3. Issue #43: Twitter Card Tags
**File:** `issue-43-twitter-cards.php`
**What it does:** Adds Twitter Card meta tags for better social sharing
**How to apply:** Add to functions.php OR create as plugin
**Time:** 2 minutes
**NOTE:** Update @YourTwitterHandle with your actual Twitter handle!

### 4. Issue #37: XML Sitemap
**File:** `issue-37-xml-sitemap-setup.md`
**What it does:** Creates automatic XML sitemap
**How to apply:** Install Yoast SEO plugin (automatic)
**Time:** 2 minutes

### 5. Issue #12: New Homepage Hero
**File:** `issue-12-new-homepage-hero.md`
**What it does:** Replaces hero with polymath positioning (BC+AI, Indigenomics, Upgrade AI)
**How to apply:** Edit homepage, paste HTML, add CSS
**Time:** 5 minutes

### 6-10: Content Sections (In Progress)
- Issue #13: BC+AI Leadership Section
- Issue #14: Indigenomics CTO Section
- Issue #15: The Upgrade AI Section
- Issue #22: Indigenous Land Acknowledgment
- Issue #65: Updated About Page

---

## 🚀 Quick Deploy Checklist

Once you import XML to Cloudways:

**Step 1: CSS Fixes (3 minutes)**
```
1. WordPress Admin → Appearance → Customize → Additional CSS
2. Copy-paste from: issue-5-color-contrast.css
3. Copy-paste from: issue-9-button-hover-states.css
4. Click: Publish
```

**Step 2: Twitter Cards (2 minutes)**
```
1. Appearance → Theme Editor → functions.php
2. Scroll to bottom (before closing ?>)
3. Paste from: issue-43-twitter-cards.php
4. Update @YourTwitterHandle to your actual handle
5. Click: Update File
```

**Step 3: XML Sitemap (2 minutes)**
```
1. Plugins → Add New
2. Search: "Yoast SEO"
3. Install + Activate
4. Done! (sitemap auto-creates)
```

**Step 4: Homepage Hero (5 minutes)**
```
1. Pages → Edit homepage
2. Switch to Code Editor
3. Paste HTML from: issue-12-new-homepage-hero.md
4. Go to: Appearance → Customize → Additional CSS
5. Paste CSS from same file
6. Publish
```

**Total Time:** 12 minutes to deploy 5 major fixes! ⚡

---

## 📊 Progress

- ✅ Issue #5: Color Contrast - FIXED
- ✅ Issue #9: Button Hovers - FIXED
- ✅ Issue #43: Twitter Cards - FIXED
- ✅ Issue #37: XML Sitemap - FIXED
- ✅ Issue #12: Homepage Hero - FIXED
- ⏳ Issue #13: BC+AI Section - IN PROGRESS
- ⏳ Issue #14: Indigenomics Section - IN PROGRESS
- ⏳ Issue #15: Upgrade AI Section - IN PROGRESS
- ⏳ Issue #22: Land Acknowledgment - IN PROGRESS
- ⏳ Issue #65: About Page Update - IN PROGRESS

**Next:** Finishing content sections (13-15, 22, 65) then moving to next 10 issues!
