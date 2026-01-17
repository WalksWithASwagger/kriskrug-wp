#!/bin/bash
# Create Blog Migration Issues for kriskrug-wp
# Run this locally after authenticating with: gh auth login

set -e

echo "Creating Blog Migration Issues..."
echo "================================="

# Issue 1: Import XML Export
gh issue create \
  --title "[MIGRATION] Import XML Export and Inventory Blog Posts" \
  --label "migration" --label "content" --label "priority:critical" \
  --body "## Objective

Import the WordPress XML export and create a complete inventory of all blog posts.

## Source File

XML export location: \`/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml\`

## Tasks

- [ ] Move XML export to repo
- [ ] Parse XML to extract posts
- [ ] Create inventory spreadsheet/markdown
- [ ] Count total posts
- [ ] Identify post categories
- [ ] Note posts with missing data

## Acceptance Criteria

- XML file in repo at content/exports/
- Complete inventory in content/blog-inventory.md
- Total post count documented
- Categories listed with post counts"

echo "✓ Issue 1 created"

# Issue 2: Define Categories
gh issue create \
  --title "[MIGRATION] Define Blog Categories and Tag Taxonomy" \
  --label "migration" --label "content" --label "priority:high" \
  --body "## Objective

Create the category and tag structure for the new site.

## Proposed Categories

- AI & Technology
- BC+AI
- Indigenomics
- The Upgrade AI
- Photography
- Speaking & Events
- Essays

## Tasks

- [ ] Review existing categories from XML
- [ ] Map old categories to new structure
- [ ] Define category descriptions for SEO
- [ ] Create tag taxonomy (max 30 tags)"

echo "✓ Issue 2 created"

# Issue 3: Categorize Posts
gh issue create \
  --title "[MIGRATION] Categorize and Curate Blog Posts" \
  --label "migration" --label "content" --label "priority:high" \
  --body "## Objective

Review all blog posts and categorize them for migration.

## Curation Criteria

- KEEP: Aligns with polymath positioning
- UPDATE: Good content but outdated
- ARCHIVE: Historically interesting
- RETIRE: No longer relevant

## Tasks

- [ ] Review each post against criteria
- [ ] Assign disposition
- [ ] Assign new category
- [ ] Create final migration list"

echo "✓ Issue 3 created"

# Issue 4: URL Redirect Map
gh issue create \
  --title "[MIGRATION] Create URL Redirect Map" \
  --label "migration" --label "seo" --label "priority:high" \
  --body "## Objective

Map all old URLs to new URLs to preserve SEO value.

## Tasks

- [ ] Extract all old URLs from XML
- [ ] Define new URL structure
- [ ] Create redirect mapping table
- [ ] Format for Redirection plugin import"

echo "✓ Issue 4 created"

# Issue 5: Execute Import
gh issue create \
  --title "[MIGRATION] Execute WordPress Blog Import" \
  --label "migration" --label "wordpress" --label "priority:critical" \
  --body "## Objective

Import blog posts into WordPress on Cloudways.

## Pre-Import Checklist

- [ ] WordPress Importer plugin installed
- [ ] Categories created in WordPress
- [ ] Author account exists
- [ ] Backup created

## Post-Import Tasks

- [ ] Verify post count
- [ ] Check featured images
- [ ] Verify categories"

echo "✓ Issue 5 created"

# Issue 6: Post-Import Cleanup
gh issue create \
  --title "[MIGRATION] Post-Import Blog Cleanup" \
  --label "migration" --label "content" --label "accessibility" --label "priority:high" \
  --body "## Objective

Clean up imported posts and prepare for publication.

## Tasks Per Post

- [ ] Check formatting
- [ ] Fix broken internal links
- [ ] Add meta descriptions
- [ ] Ensure all images have alt text
- [ ] Correct category assigned"

echo "✓ Issue 6 created"

# Issue 7: Redirection Plugin
gh issue create \
  --title "[MIGRATION] Install and Configure Redirection Plugin" \
  --label "migration" --label "seo" --label "wordpress" --label "priority:high" \
  --body "## Objective

Set up URL redirects to preserve SEO.

## Tasks

- [ ] Install Redirection plugin
- [ ] Import redirect CSV
- [ ] Test sample redirects
- [ ] Monitor 404 log"

echo "✓ Issue 7 created"

# Issue 8: Blog Landing Page
gh issue create \
  --title "[MIGRATION] Create Blog Landing Page Design" \
  --label "migration" --label "design" --label "wordpress" --label "priority:medium" \
  --body "## Objective

Design and build the main blog page with category filtering.

## Design Requirements

- Hero Section with headline
- Category filter bar
- Post grid with cards
- Pagination

## AI-Playful Elements

- Card hover effects
- Scroll reveal animation
- Gradient accents"

echo "✓ Issue 8 created"

# Issue 9: Single Post Template
gh issue create \
  --title "[MIGRATION] Design Single Blog Post Template" \
  --label "migration" --label "design" --label "wordpress" --label "priority:medium" \
  --body "## Objective

Create a beautiful, readable single post template.

## Structure

- Category badge + title + meta
- Featured image
- Post content (optimized typography)
- Tags + Author bio
- Related posts
- Newsletter CTA

## AI-Playful Elements

- Progress bar on scroll
- Share button animations"

echo "✓ Issue 9 created"

# Issue 10: Featured Images
gh issue create \
  --title "[MIGRATION] Extract and Process Featured Images" \
  --label "migration" --label "performance" --label "priority:medium" \
  --body "## Objective

Ensure all migrated posts have optimized featured images.

## Tasks

- [ ] Identify posts with featured images
- [ ] Optimize images (WebP, compression)
- [ ] Note posts missing featured images
- [ ] Create placeholder strategy"

echo "✓ Issue 10 created"

echo ""
echo "================================="
echo "All 10 Blog Migration issues created!"
