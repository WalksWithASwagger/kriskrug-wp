# Production Import Guide

How to import production bc-ai.ca to Cloudways and unleash the agent swarm on real issues.

---

## Current Status

**Infrastructure:** ✅ Complete and validated
**Cloudways:** ✅ WordPress 6.9 ready at https://wordpress-1569695-6109303.cloudwaysapps.com
**Agent Swarm:** ✅ Proven operational
**Waiting For:** Production bc-ai.ca export

---

## Step 1: Get Production Export

**Ask your developer for:**
- All-in-One WP Migration export (.wpress file)
- OR database dump + wp-content files
- Sanitized database (fake emails OK for dev)

**Or do it yourself:**
1. Log into bc-ai.ca WordPress admin
2. Install "All-in-One WP Migration" plugin
3. Export → File
4. Download .wpress file

---

## Step 2: Import to Cloudways

**Option A: Replace Current WordPress**
1. In Cloudways dashboard → Applications
2. Delete current test WordPress
3. Create new WordPress application
4. Import production data

**Option B: Add Second Application** (Recommended)
1. Keep current WordPress as clean dev
2. Add new application for production mirror
3. Import bc-ai.ca to new app
4. Now have: Clean dev + Production mirror

---

## Step 3: Point Agent Swarm at Production

Once production is imported:

```bash
# Update .claude/context/wordpress-setup.md with production paths
# Update Cloudways connection if using second app

# Then unleash on real issues!
gh issue edit 1 --add-label "auto-implement"  # Contact Form
gh issue edit 2 --add-label "auto-implement"  # WCAG Audit
gh issue edit 4 --add-label "auto-implement"  # Performance
```

---

## Step 4: Deploy Fixes

When agent creates PRs:
1. Review code
2. Test on Cloudways
3. Merge to main
4. Deploy to production bc-ai.ca (via your normal process)

---

**Infrastructure is ready. Waiting for production bc-ai.ca!** 🌲
