# Issue #22: Indigenous Land Acknowledgment

## Good News!

You already have a page: **"Reconciliation & Indigenous Land Acknowledgement"**
Location: https://kriskrug.co/reconciliation-indigenous-land-acknowledgement/

## What to Do

### Option 1: Feature in Footer (Recommended)

Add this to your site footer:

```html
<div class="land-acknowledgment">
  <p>
    I live and work on the unceded traditional territories of the Coast Salish,
    Squamish (Sḵwx̱wú7mesh), and Tsleil-Waututh (səl̓ilw̓ətaʔɬ) peoples. I'm
    grateful for the opportunity to build community on these lands and committed
    to Indigenous sovereignty.
  </p>
  <a href="/reconciliation-indigenous-land-acknowledgement/">Learn more about reconciliation →</a>
</div>
```

### Option 2: Feature on About Page

Add this section to your About page:

```html
<section class="land-values">
  <h2>Land & Values</h2>
  <p>
    This work happens on the unceded territories of the Coast Salish, Squamish,
    and Tsleil-Waututh nations. Indigenous wisdom and sovereignty are foundational
    to how I think about community, technology, and futures.
  </p>
  <p>
    I'm committed to amplifying Indigenous voices in AI discourse and building
    technology that honors Indigenous futures. My work with Indigenomics.ai
    centers Indigenous economic sovereignty and data governance.
  </p>
  <a href="/reconciliation-indigenous-land-acknowledgement/" class="button">
    Read Full Land Acknowledgment →
  </a>
</section>
```

### Suggested CSS

```css
.land-acknowledgment {
  padding: 24px;
  background: #f5f5f5;
  border-left: 4px solid #0052CC;
  margin: 40px 0;
  font-size: 14px;
  line-height: 1.6;
}

.land-acknowledgment a {
  color: #0052CC;
  text-decoration: none;
  font-weight: 600;
}

.land-acknowledgment a:hover {
  text-decoration: underline;
}
```

## Implementation

**Recommended:** Add to footer so it appears on every page

1. Appearance → Widgets
2. Find "Footer" widget area
3. Add HTML widget
4. Paste above HTML
5. Save

OR

1. Appearance → Theme Editor → footer.php
2. Add before closing `</footer>` tag
3. Save

## Status

✅ **Content already exists!**
✅ **Just needs better visibility**
✅ **Ready to implement**

**Time:** 3 minutes
