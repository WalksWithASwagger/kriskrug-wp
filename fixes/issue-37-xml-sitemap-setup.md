# Issue #37: Create XML Sitemap - Setup Guide

## Solution: Use Yoast SEO Plugin (Recommended)

### Installation

**In WordPress Admin:**
1. Go to: **Plugins → Add New**
2. Search: **"Yoast SEO"**
3. Click: **Install Now**
4. Click: **Activate**

### Configuration

**After activation:**
1. Yoast automatically creates XML sitemap
2. Access at: `https://kriskrug.co/sitemap_index.xml`
3. No configuration needed! (works out of box)

### Verify It Works

1. Visit: `https://wordpress-1569695-6109303.cloudwaysapps.com/sitemap_index.xml`
2. Should see XML sitemap with all pages/posts listed

### Submit to Search Engines

**Google Search Console:**
1. Go to: https://search.google.com/search-console
2. Select your property (kriskrug.co)
3. Click: **Sitemaps** (left sidebar)
4. Enter: `sitemap_index.xml`
5. Click: **Submit**

**Bing Webmaster Tools:**
1. Go to: https://www.bing.com/webmasters
2. Add your site
3. Submit sitemap: `sitemap_index.xml`

### Yoast Settings (Optional Optimization)

**SEO → General → Features:**
- ✅ XML sitemaps: ON
- ✅ SEO analysis: ON
- ✅ Readability analysis: ON

**SEO → Search Appearance:**
- Configure what's included in sitemap
- Typically include: Posts, Pages, Media
- Exclude: Categories, Tags (unless you want them)

## Alternative: Rank Math (Lighter Weight)

If you prefer a faster plugin:
1. Install "Rank Math" instead
2. Same sitemap features
3. More beginner-friendly interface

## Status

✅ **Ready to implement** - Just install Yoast SEO plugin
✅ **Automatic** - Sitemap updates when you publish content
✅ **Zero configuration** needed

**Time to implement:** 2 minutes
