# Kris Krug WordPress Setup - Cloudways Development Server

**Server Type:** Development/Staging
**Environment:** Cloudways
**Status:** ✅ Active and Accessible

---

## Server Details

### Connection Information
- **Host:** 24.144.80.107 (1569695.cloudwaysapps.com)
- **SSH User:** master_qcteaefabe
- **SSH Key:** ~/.ssh/id_cloudways_bcai_rsa
- **Application ID:** fkgwevabgu

### WordPress Installation
- **WordPress Version:** 6.9 (latest)
- **PHP Version:** 8.2.29
- **WP-CLI:** 2.12.0
- **Git:** 2.39.5

### URLs
- **Frontend:** https://wordpress-1569695-6109303.cloudwaysapps.com
- **Admin:** https://wordpress-1569695-6109303.cloudwaysapps.com/wp-admin

### File Paths
- **WordPress Root:** `/home/1569695.cloudwaysapps.com/fkgwevabgu/public_html`
- **wp-content:** `/home/1569695.cloudwaysapps.com/fkgwevabgu/public_html/wp-content`
- **Custom Plugins:** `/home/1569695.cloudwaysapps.com/fkgwevabgu/public_html/wp-content/plugins/kk-*`
- **Custom Theme:** `/home/1569695.cloudwaysapps.com/fkgwevabgu/public_html/wp-content/themes/kk-*`

---

## Installed Plugins

### Active
1. **Breeze** (2.2.22) - Cloudways caching plugin
2. **Object Cache Pro** (1.24.5) - Redis object caching

### Inactive
1. **Akismet** (5.6) - Spam protection
2. **Hello Dolly** (1.7.2) - WordPress sample plugin

### Drop-ins
- **advanced-cache.php** - Breeze caching
- **object-cache.php** - Object Cache Pro

---

## Installed Themes

### Active
- **Twenty Twenty-Five** (1.4) - Default WordPress theme

### Inactive
- **Twenty Twenty-Four** (1.4)
- **Twenty Twenty-Three** (1.6)

---

## Server Capabilities

### Installed Tools
- ✅ PHP 8.2.29
- ✅ Git 2.39.5
- ✅ WP-CLI 2.12.0
- ✅ Composer (via Cloudways)
- ✅ ionCube Loader
- ✅ Zend OPcache

### Storage
- **Total Disk:** 50GB
- **Used:** 8.3GB
- **Available:** 39GB (plenty of space)

### Caching
- ✅ Redis object cache (Object Cache Pro)
- ✅ Breeze page caching
- ✅ OPcache enabled

---

## WordPress Configuration

### Current Settings
- **Site Title:** (Check in wp-admin)
- **Permalink Structure:** (Check in wp-admin)
- **Search Engine Visibility:** Should set to "Discourage" for dev

### Database
- **Type:** MySQL/MariaDB
- **Location:** localhost (Cloudways managed)
- **Credentials:** In wp-config.php (never commit this!)

---

## Development Configuration Needed

### wp-config.php Changes

Need to add these constants:

```php
// Development environment identifier
define( 'WP_ENVIRONMENT_TYPE', 'development' );

// Enable debugging
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', true );

// Save queries for debugging
define( 'SAVEQUERIES', true );

// Disable file editing
define( 'DISALLOW_FILE_EDIT', true );
define( 'DISALLOW_FILE_MODS', true );

// Memory limits (if needed)
define( 'WP_MEMORY_LIMIT', '256M' );
define( 'WP_MAX_MEMORY_LIMIT', '512M' );
```

### Recommended Development Plugins

Install via WP-CLI:
```bash
wp plugin install query-monitor --activate
wp plugin install debug-bar --activate
wp plugin install developer --activate
```

Or via WordPress admin.

---

## Git Repository Integration

### Strategy

**Track ONLY custom code in git:**
- `/wp-content/plugins/kk-*/` - Our custom plugins
- `/wp-content/themes/kk-*/` - Our custom theme
- NOT WordPress core
- NOT third-party plugins/themes

### Implementation

```bash
# On Cloudways server
cd /home/1569695.cloudwaysapps.com/fkgwevabgu/public_html/wp-content

# Clone our repo (custom code only)
git clone https://github.com/WalksWithASwagger/kk-wp.git kk-repo

# Copy/link custom code
mkdir -p plugins/kk-custom
mkdir -p themes/kk-theme

# Or symlink (if we create custom code in our repo first)
```

---

## Deployment Workflow

### From Local → Cloudways Dev

**Option 1: Git Pull (Recommended)**
```bash
# On Cloudways
cd ~/applications/fkgwevabgu/public_html/wp-content/plugins/kk-custom
git pull origin main
```

**Option 2: SFTP Deploy Script**
```bash
# From local
bash scripts/deploy-to-cloudways.sh
```

**Option 3: GitHub Actions**
- Push to `develop` branch
- GitHub Actions auto-deploys to Cloudways
- See `.github/workflows/deploy-to-dev.yml`

### From Cloudways Dev → Production

**When ready for production:**

1. Test thoroughly on Cloudways dev
2. Create PR to `main` branch
3. Get code review
4. Merge PR
5. Your production developer pulls from git
6. Or use deployment tool (DeployHQ, etc.)

**NEVER** deploy directly without testing on Cloudways first!

---

## Quick Reference Commands

### SSH Connection
```bash
# Quick connect (after SSH config)
ssh cloudways-bcai-dev

# Or with full path
ssh -i ~/.ssh/id_cloudways_bcai_rsa master_qcteaefabe@24.144.80.107
```

### Navigate to WordPress
```bash
# WordPress root
cd /home/1569695.cloudwaysapps.com/fkgwevabgu/public_html

# Shorter (using symlink)
cd ~/applications/fkgwevabgu/public_html
```

### Common WP-CLI Commands
```bash
# Check WordPress version
wp core version

# List plugins
wp plugin list

# Activate plugin
wp plugin activate query-monitor

# Update WordPress
wp core update

# Clear cache
wp cache flush
```

---

## SSH Config (Optional but Recommended)

**Add to ~/.ssh/config:**

```
Host cloudways-bcai-dev
    HostName 24.144.80.107
    User master_qcteaefabe
    IdentityFile ~/.ssh/id_cloudways_bcai_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Then just use:**
```bash
ssh cloudways-bcai-dev
```

---

## Safety Notes

### This is DEV
- ✅ Safe to experiment
- ✅ Can make mistakes
- ✅ Can break things
- ✅ Has backups in Cloudways
- ✅ NOT connected to production

### Never
- ❌ Don't put production data here
- ❌ Don't commit wp-config.php
- ❌ Don't expose database credentials
- ❌ Don't allow search engine indexing

### Always
- ✅ Test here before production
- ✅ Use version control
- ✅ Create backups before risky changes
- ✅ Document changes
- ✅ Keep WordPress and plugins updated

---

## Cloudways Dashboard Features

### Useful Features
- **Backups:** One-click backup/restore
- **Staging:** Clone entire app for testing
- **SSL:** Free Let's Encrypt certificates
- **Monitoring:** Server metrics and uptime
- **Team:** Add collaborators
- **Git Deploy:** Native git deployment option

### Access Cloudways Features
1. Log into Cloudways dashboard
2. Select your server
3. Explore tabs: Applications, Monitoring, Backups, etc.

---

## Next Steps

1. ✅ SSH connection working
2. ✅ WordPress 6.9 installed
3. ⏳ Configure development settings
4. ⏳ Install development plugins
5. ⏳ Integrate with git repository
6. ⏳ Set up deployment workflow
7. ⏳ Test agent swarm deployment

---

**This is a perfect development environment for Kris Krug!** 🌲

WordPress is fresh, server is powerful, and we have all the tools we need to build and test safely before touching production.
