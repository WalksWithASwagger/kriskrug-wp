# BC+AI Local Development Setup Guide

**CRITICAL:** This is a production site. We must have a completely separate local development environment.

---

## 🚨 Safety First: The Golden Rules

1. **NEVER edit production directly**
2. **NEVER push untested code**
3. **ALWAYS test locally first**
4. **ALWAYS backup before changes**
5. **NEVER commit wp-config.php with production credentials**

---

## Step 1: Export Production Site (WordPress Admin Only)

Since you only have WordPress admin access, use a plugin-based export method.

### Recommended: All-in-One WP Migration (FREE)

**Why this plugin:**
- ✅ Simple one-click export
- ✅ Includes database, files, plugins, themes
- ✅ Easy import to local
- ✅ Free for sites under 512MB
- ✅ No server access needed

**Steps:**

1. **Install Plugin on Production**
   ```
   WordPress Admin → Plugins → Add New
   Search: "All-in-One WP Migration"
   Install and Activate
   ```

2. **Export Site**
   ```
   WordPress Admin → All-in-One WP Migration → Export
   Export To: File

   Wait for export to complete (may take 5-15 minutes)
   Download the .wpress file
   ```

3. **Save Export File**
   ```
   Save to: ~/Downloads/bc-ai-ca-export.wpress
   Size: Likely 100MB-2GB depending on media
   ```

### Alternative: Duplicator (Also FREE)

**If All-in-One has issues:**

1. Install "Duplicator" plugin
2. Packages → Create New
3. Name: `bc-ai-local-dev`
4. Build and download both files:
   - `installer.php`
   - `{site-name}_archive.zip`

---

## Step 2: Choose Local Environment

Let me help you choose between **Local (Flywheel)** and **Docker**.

### Option A: Local by Flywheel (Recommended for You)

**Pros:**
- ✅ Beautiful GUI, super easy
- ✅ One-click WordPress install
- ✅ Built-in SSL (https://bc-ai.local)
- ✅ Import .wpress files directly
- ✅ Easy database access (Adminer included)
- ✅ No terminal commands needed
- ✅ Perfect for Mac (you're on macOS)
- ✅ Site-specific PHP versions
- ✅ Built-in email testing

**Cons:**
- ❌ Uses more disk space (~1GB per site)
- ❌ Slightly slower than Docker on M1/M2 Macs
- ❌ Less customizable than Docker

**Best for:** You want easy setup, GUI management, quick start

**Download:** https://localwp.com/

### Option B: Docker with @wordpress/env

**Pros:**
- ✅ Official WordPress tool
- ✅ Lightweight and fast
- ✅ Consistent across all platforms
- ✅ Easy to script and automate
- ✅ Multiple environments (dev, staging, test)
- ✅ Integrates with our Makefile
- ✅ Version controlled config

**Cons:**
- ❌ Requires terminal/command-line comfort
- ❌ No GUI (all terminal-based)
- ❌ Manual import process
- ❌ Need to configure database access separately

**Best for:** You're comfortable with terminal, want automation

**Install:**
```bash
npm install -g @wordpress/env
```

### My Recommendation: **Local by Flywheel**

**Why for you:**
1. **You're downloading from production** - GUI makes import easier
2. **Safety** - Visual confirmation of what's running
3. **Speed** - Get up and running in 10 minutes vs 30 minutes
4. **Testing** - Easy to test in browser with SSL
5. **Our agent swarm** - Can work with either, but Local is clearer

**You can always switch to Docker later** if you want more automation.

---

## Step 3A: Setup with Local by Flywheel

### Installation

1. **Download Local**
   - Visit: https://localwp.com/
   - Download for macOS
   - Install (drag to Applications)

2. **Launch Local**
   - Open Local app
   - Click "Create a new site" (we'll delete this after import)

3. **Import Production Site**
   ```
   Local → Click "+" → "Create from site backup"
   Choose file: bc-ai-ca-export.wpress
   Site name: bc-ai-local

   Wait for import (5-10 minutes)
   ```

4. **Site is Ready!**
   ```
   URL: https://bc-ai-local.local
   Admin: Your production credentials
   Database: Access via Adminer in Local
   ```

### Configuration

5. **Disable Email Sending**
   ```
   Local → Site → Tools → MailHog (automatically enabled)

   All emails caught locally, won't send to real addresses
   ```

6. **Enable WP_DEBUG**
   ```
   Local → Site → Navigate to app/public/wp-config.php

   Add:
   define( 'WP_DEBUG', true );
   define( 'WP_DEBUG_LOG', true );
   define( 'SCRIPT_DEBUG', true );
   ```

7. **Link to Our Git Repo**
   ```bash
   cd ~/Local\ Sites/bc-ai-local/app/public

   # Copy our repo into WordPress directory
   # OR
   # Symlink custom plugins/themes to our repo
   ```

---

## Step 3B: Setup with Docker (Alternative)

### Installation

1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop
   - Install and launch

2. **Install wp-env**
   ```bash
   npm install -g @wordpress/env
   ```

3. **Create wp-env Config**

   In our repo, create `.wp-env.json`:
   ```json
   {
     "core": "WordPress/WordPress#6.4.2",
     "phpVersion": "8.2",
     "plugins": [],
     "themes": [],
     "port": 8888,
     "config": {
       "WP_DEBUG": true,
       "WP_DEBUG_LOG": true,
       "SCRIPT_DEBUG": true
     },
     "mappings": {
       "wp-content/plugins/bc-ai-custom": "./wp-content/plugins/bc-ai-custom",
       "wp-content/themes/bc-ai-theme": "./wp-content/themes/bc-ai-theme"
     }
   }
   ```

4. **Start WordPress**
   ```bash
   wp-env start

   # Site will be at:
   # Frontend: http://localhost:8888
   # Admin: http://localhost:8888/wp-admin
   # Username: admin
   # Password: password
   ```

5. **Import Production Data**
   ```bash
   # Install WP-CLI in container
   wp-env run cli wp --version

   # Import database
   wp-env run cli wp db import ~/Downloads/database-export.sql

   # Search-replace URLs
   wp-env run cli wp search-replace 'https://bc-ai.ca' 'http://localhost:8888'
   ```

---

## Step 4: Safe Development Workflow

### Directory Structure (Recommended)

```
/Users/kk/Code/bc-ai-wp/              # Our git repo
├── .git/                             # Git tracking
├── .github/                          # Workflows, agents
├── skills/                           # Custom skills
├── docs/                             # Documentation
├── .claude/                          # Context files
├── wp-content/                       # WordPress custom code (ONLY)
│   ├── plugins/
│   │   └── bc-ai-custom/            # Our custom plugin
│   └── themes/
│       └── bc-ai-theme/             # Our custom theme (if any)
└── README.md

/Users/kk/Local Sites/bc-ai-local/    # Local by Flywheel
└── app/
    └── public/                       # Full WordPress install
        ├── wp-admin/                 # NOT in git
        ├── wp-includes/              # NOT in git
        ├── wp-content/              # Link our custom code here
        └── wp-config.php            # NOT in git
```

### What to Track in Git

**DO track:**
- ✅ Custom plugins in `wp-content/plugins/bc-ai-*`
- ✅ Custom themes in `wp-content/themes/bc-ai-*`
- ✅ Custom must-use plugins in `wp-content/mu-plugins/`
- ✅ Documentation
- ✅ GitHub workflows and agents
- ✅ Test files

**DO NOT track:**
- ❌ WordPress core (`wp-admin`, `wp-includes`, `wp-*.php`)
- ❌ Third-party plugins
- ❌ Third-party themes
- ❌ `wp-config.php` (has sensitive credentials)
- ❌ `wp-content/uploads/` (media files)
- ❌ Database dumps with real data

### Development Workflow

**Safe process:**

1. **Pull latest from git**
   ```bash
   cd /Users/kk/Code/bc-ai-wp
   git pull origin main
   ```

2. **Make changes in local WordPress**
   ```bash
   cd ~/Local\ Sites/bc-ai-local/app/public
   # Edit files here, test in browser
   ```

3. **Copy ONLY custom code to git repo**
   ```bash
   # Copy custom plugin
   cp -r ~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/bc-ai-custom \
         /Users/kk/Code/bc-ai-wp/wp-content/plugins/

   # Copy custom theme
   cp -r ~/Local\ Sites/bc-ai-local/app/public/wp-content/themes/bc-ai-theme \
         /Users/kk/Code/bc-ai-wp/wp-content/themes/
   ```

4. **Test and validate**
   ```bash
   cd /Users/kk/Code/bc-ai-wp
   make validate        # PHPCS check
   make test           # PHPUnit tests
   ```

5. **Create feature branch**
   ```bash
   git checkout -b feature/issue-123-description
   git add wp-content/
   git commit -m "Description"
   git push -u origin feature/issue-123
   ```

6. **Create PR for review**
   ```bash
   gh pr create --draft
   # Review, test, then mark ready for review
   ```

7. **After PR approved and merged**
   - Download code from GitHub to production (via FTP or your developer)
   - OR have your developer pull from GitHub
   - Test on production
   - Monitor for issues

---

## Step 5: Security Considerations

### Environment Variables

**Create:** `.env.example` (in git)
```env
# BC+AI Local Development Environment Variables
# Copy this to .env and fill in values (never commit .env)

WP_HOME=http://localhost:8888
WP_SITEURL=http://localhost:8888

# Database (Local uses these automatically)
DB_NAME=local
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost

# API Keys (get from developer)
GRAVITY_FORMS_LICENSE=
NOTION_API_KEY=
# Add others as needed
```

**Create:** `.env` (NOT in git)
```env
# Your actual local credentials
# This file is in .gitignore and will never be committed
```

### Sanitize Production Data

**Before importing to local:**

```bash
# Use WP-CLI to sanitize emails (if you have access)
wp-env run cli wp user list --field=user_email
wp-env run cli wp db query "UPDATE wp_users SET user_email = CONCAT(user_login, '@example.local')"

# Or ask developer to export sanitized database
```

---

## Step 6: Linking Local WordPress to Git Repo

### Option A: Symlinks (Recommended)

**Create symbolic links** from Local WordPress to your git repo:

```bash
# Remove Local's empty directories
rm -rf ~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/bc-ai-custom
rm -rf ~/Local\ Sites/bc-ai-local/app/public/wp-content/themes/bc-ai-theme

# Create symlinks to git repo
ln -s /Users/kk/Code/bc-ai-wp/wp-content/plugins/bc-ai-custom \
      ~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/bc-ai-custom

ln -s /Users/kk/Code/bc-ai-wp/wp-content/themes/bc-ai-theme \
      ~/Local\ Sites/bc-ai-local/app/public/wp-content/themes/bc-ai-theme
```

**Benefits:**
- Edit files in git repo, changes immediately visible in Local
- No copying back and forth
- Always in sync

### Option B: Watch Script (Alternative)

**Create:** `scripts/sync-to-local.sh`

```bash
#!/bin/bash
# Watch for changes and sync to Local WordPress

fswatch -o /Users/kk/Code/bc-ai-wp/wp-content | while read; do
  rsync -av --delete \
    /Users/kk/Code/bc-ai-wp/wp-content/plugins/bc-ai-custom \
    ~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/

  echo "✓ Synced to Local"
done
```

---

## Step 7: Add to Makefile

**Add these commands to Makefile:**

```makefile
# Local WordPress shortcuts
local-start: ## Start Local WordPress (if using Docker)
	wp-env start

local-stop: ## Stop Local WordPress (if using Docker)
	wp-env stop

local-shell: ## SSH into Local WordPress (Docker)
	wp-env run cli bash

local-logs: ## View Local WordPress logs
	wp-env logs

sync-from-local: ## Copy custom code from Local to git repo
	@echo "Syncing custom code from Local..."
	@rsync -av --delete \
		~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/bc-ai-custom/ \
		./wp-content/plugins/bc-ai-custom/ || true
	@rsync -av --delete \
		~/Local\ Sites/bc-ai-local/app/public/wp-content/themes/bc-ai-theme/ \
		./wp-content/themes/bc-ai-theme/ || true
	@echo "✓ Sync complete"

local-db-export: ## Export local database (for testing)
	@echo "Exporting local database..."
	@wp-env run cli wp db export /tmp/local-export.sql
	@wp-env run cli cat /tmp/local-export.sql > local-db-backup.sql
	@echo "✓ Database exported to local-db-backup.sql"
```

---

## Recommended: Local by Flywheel Setup

**For your case (macOS, WordPress admin only, want easy GUI):**

### Installation Steps

1. **Download and Install**
   ```
   Visit: https://localwp.com/
   Download: Local for Mac
   Install: Drag to Applications folder
   Launch Local
   ```

2. **Import BC+AI Site**
   ```
   Local → File → Import Site
   Or drag .wpress file into Local window

   Site name: bc-ai-local
   Domain: bc-ai.local (automatic SSL)

   Wait for import (5-15 minutes depending on size)
   ```

3. **Site Running!**
   ```
   URL: https://bc-ai.local
   Admin: https://bc-ai.local/wp-admin
   Username: (your production username)
   Password: (your production password)
   ```

4. **Access Files**
   ```
   Right-click site → "Reveal in Finder"
   Or: ~/Local Sites/bc-ai-local/app/public/
   ```

5. **Create Symlinks to Git Repo**
   ```bash
   # Find what custom code exists
   ls ~/Local\ Sites/bc-ai-local/app/public/wp-content/plugins/
   ls ~/Local\ Sites/bc-ai-local/app/public/wp-content/themes/

   # Create directories in git repo for custom code
   mkdir -p wp-content/plugins/bc-ai-custom
   mkdir -p wp-content/themes/bc-ai-theme

   # Copy custom code to git repo (first time only)
   # Then create symlinks for live editing
   ```

---

## Step 8: Tell Your Developer

**Questions to ask your developer:**

1. **"Can you create a staging/dev export for me?"**
   - Sanitized database (no real emails)
   - All plugins and theme included
   - Using All-in-One WP Migration or Duplicator

2. **"What custom plugins/themes exist?"**
   - List of bc-ai-specific custom code
   - Which directories to track in git

3. **"What's the deployment process?"**
   - How do changes go from dev → production?
   - Is there a staging environment?
   - FTP, Git, or hosting panel?

4. **"Can we set up a git-based deployment?"**
   - Pull from GitHub to production
   - Or use tool like DeployHQ, DeployBot
   - Automated but safe

---

## Step 9: Development Workflow (Complete)

### Daily Workflow

```bash
# Morning: Start Local
Open Local app → Start bc-ai-local site

# Work on issue
git checkout -b feature/issue-123
# Edit files in Local WordPress (symlinked to git repo)
# Test in browser: https://bc-ai.local

# Validate changes
make validate
make test

# Commit and push
git add .
git commit -m "Fix: Issue #123"
git push

# Create PR
gh pr create

# Evening: Stop Local (optional)
Local → Stop site (saves resources)
```

### Testing Checklist

**Before creating PR:**
- [ ] Changes work in Local browser
- [ ] make validate passes (0 PHPCS errors)
- [ ] make test passes (if tests exist)
- [ ] Tested on mobile (Chrome DevTools)
- [ ] Checked console for JavaScript errors
- [ ] Verified no PHP errors in debug.log

---

## Step 10: Prepare for Agent Swarm

Once Local is set up:

1. **Document the setup** in `.claude/context/wordpress-setup.md`
2. **Map the codebase** in `.claude/context/codebase-map.md`
3. **Test agent with simple issue** (like #8)
4. **Refine based on results**

---

## Quick Start Script (After Setup)

**Add to `Makefile`:**

```makefile
setup-local: ## First-time local setup guide
	@echo "🌲 BC+AI Local Development Setup"
	@echo ""
	@echo "1. Download Local by Flywheel: https://localwp.com/"
	@echo "2. Install All-in-One WP Migration plugin on bc-ai.ca"
	@echo "3. Export site: WP Admin → All-in-One WP Migration → Export"
	@echo "4. Import to Local: Drag .wpress file into Local app"
	@echo "5. Create symlinks to this repo for custom code"
	@echo ""
	@echo "See docs/local-development-setup.md for detailed instructions"

check-local: ## Check if Local WordPress is running
	@if curl -s -o /dev/null -w "%{http_code}" https://bc-ai.local | grep -q "200\|301\|302"; then \
		echo "✅ Local WordPress is running at https://bc-ai.local"; \
	else \
		echo "❌ Local WordPress not running. Start it in Local app."; \
	fi
```

---

## Safety Checklist

Before you download anything:

- [ ] You have WordPress admin access ✅
- [ ] You'll use plugin-based export (All-in-One WP Migration)
- [ ] You'll set up Local by Flywheel (easy GUI)
- [ ] Local will be at bc-ai.local (different from production)
- [ ] Git repo will only track custom code
- [ ] Production credentials never committed
- [ ] Changes tested locally before any production deployment

---

## Next Steps

1. **Ask your developer for export** OR **install plugin yourself**
2. **Download export file** (may take time, could be large)
3. **Install Local by Flywheel** (while export is running)
4. **Import to Local** (drag and drop!)
5. **Tell me when ready** and I'll help with:
   - Symlinking custom code to git repo
   - Documenting the WordPress setup
   - Mapping the codebase
   - Testing the first agent automation!

---

**Remember:** Production stays safe. Local is our playground. Git tracks only custom code. Agents work in Local. We push only tested, reviewed code.

🌲 **Let's build BC+AI's future safely and responsibly!** 🤖
