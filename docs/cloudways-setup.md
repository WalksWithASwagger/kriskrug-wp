# Cloudways Development Server Setup

**Server:** Development/Staging for BC+AI WordPress
**IP:** 24.144.80.107
**Status:** NEW server (not production - safe to experiment)

---

## 🚨 Important: This is DEV, Not Production

✅ **Safe to experiment on this server**
✅ **Production bc-ai.ca is separate**
✅ **Can make mistakes here without affecting live site**

---

## Quick Start: 3 Ways to Connect

### Option 1: Cloudways Web Terminal (Easiest)

1. Log into Cloudways dashboard
2. Go to your server
3. Click "Launch SSH Terminal" button
4. Terminal opens in browser - no password needed!

**Pros:** No setup, works immediately, safe
**Recommended for:** Quick exploration and commands

### Option 2: SSH with Password (Manual)

```bash
ssh master_qcteaefabe@24.144.80.107
# Enter password when prompted
```

**Pros:** Standard SSH access
**Cons:** Need to enter password each time

### Option 3: SSH Key Authentication (Best Long-term)

**Setup once, never enter password again:**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "kris@bc-ai-dev"
# Save to: ~/.ssh/id_ed25519
# Passphrase: (optional but recommended)

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to Cloudways:
# Dashboard → Server → Settings & Packages → SSH Public Key
# Paste your public key → Save

# Test connection
ssh master_qcteaefabe@24.144.80.107
# Should connect without password!
```

**Pros:** Secure, convenient, enables automation
**Recommended for:** Regular development work

---

## Step 1: Explore the Server

**Run these commands** (via web terminal or SSH):

```bash
# Check what's installed
hostname
pwd
whoami
php -v
git --version
wp --version  # WP-CLI
mysql --version

# Find WordPress
ls -la
cd /home/master_qcteaefabe
ls -la
find . -name "wp-config.php" -type f 2>/dev/null | head -5

# Check server info
cat /etc/os-release | grep PRETTY_NAME
df -h  # Disk space
free -h  # Memory
```

**Share the output** and I'll help interpret what's there.

---

## Step 2: WordPress Installation

### Via Cloudways Dashboard (Recommended)

1. **Log into Cloudways**
2. **Go to Applications**
3. **Add Application** (if not already added)
   - Application name: `bc-ai-dev`
   - Choose: WordPress
   - Let it install

4. **Get Application Credentials**
   - Cloudways shows:
     - Application URL
     - Admin panel URL
     - Admin username
     - Admin password

5. **Access WordPress**
   - Visit the URL Cloudways provides
   - Log into wp-admin
   - You now have a fresh WordPress install!

### Check What's Already There

**If WordPress is already installed:**

```bash
# SSH into server
ssh master_qcteaefabe@24.144.80.107

# Find WordPress directory
cd ~/applications/
ls -la

# Usually something like:
cd qcteaefabe/public_html

# Check WordPress version
wp core version

# List what's installed
wp plugin list
wp theme list

# Check if this is fresh or has content
wp post list
wp user list
```

---

## Step 3: Configure for Development

### Set Development Mode

**Edit wp-config.php** (via SFTP, SSH, or Cloudways file manager):

```php
// Add these lines BEFORE "That's all, stop editing!"

// Development mode
define( 'WP_ENVIRONMENT_TYPE', 'development' );

// Enable debugging
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );  // Don't show errors on screen
define( 'SCRIPT_DEBUG', true );

// Save queries for debugging
define( 'SAVEQUERIES', true );

// Disable file modifications via admin
define( 'DISALLOW_FILE_EDIT', true );
define( 'DISALLOW_FILE_MODS', true );  // Force git-based deployments

// Prevent indexing by search engines
define( 'WP_ENVIRONMENT_TYPE', 'development' );
```

### Install Development Plugins

```bash
# Via WP-CLI
wp plugin install query-monitor --activate
wp plugin install debug-bar --activate

# Or via WordPress Admin:
# Plugins → Add New → Search "Query Monitor"
```

### Set Robots.txt

**Prevent Google from indexing dev site:**

```bash
# Via WP-CLI
wp option update blog_public 0

# Or WordPress Admin:
# Settings → Reading → "Discourage search engines" → Check box
```

---

## Step 4: Git Integration

### On Cloudways Server

```bash
# SSH into server
ssh master_qcteaefabe@24.144.80.107

# Navigate to WordPress wp-content
cd ~/applications/{app-name}/public_html/wp-content

# Initialize git (if not already)
git init

# Add our remote
git remote add origin https://github.com/WalksWithASwagger/bc-ai-wp.git

# Fetch our repo
git fetch origin

# Create .gitignore to prevent tracking everything
cat > .gitignore <<'EOF'
# Track ONLY custom code
/*
!plugins/bc-ai-*/
!themes/bc-ai-*/
!.gitignore
EOF

# Pull our repository structure
git pull origin main
```

### Create Custom Plugin/Theme Directories

```bash
# Make directories for our custom code
mkdir -p plugins/bc-ai-custom
mkdir -p themes/bc-ai-theme

# These will sync with our git repo
```

---

## Step 5: Deployment Workflow

### Option A: Git-Based (Recommended)

**On Cloudways server:**

```bash
cd ~/applications/{app-name}/public_html/wp-content

# Pull latest from git
git pull origin main

# Only custom code updates, WordPress core stays intact
```

**From local:**

```bash
# Make changes
# Commit to git
# Push to GitHub
# Then on Cloudways: git pull
```

### Option B: SFTP Deployment Script

**Create:** `scripts/deploy-to-cloudways.sh`

```bash
#!/bin/bash
# Deploy custom code to Cloudways via SFTP

HOST="24.144.80.107"
USER="master_qcteaefabe"
REMOTE_PATH="/home/master_qcteaefabe/applications/{app-name}/public_html/wp-content"

echo "🚀 Deploying to Cloudways Dev Server..."

# Deploy custom plugin
scp -r wp-content/plugins/bc-ai-custom \
    $USER@$HOST:$REMOTE_PATH/plugins/

# Deploy custom theme
scp -r wp-content/themes/bc-ai-theme \
    $USER@$HOST:$REMOTE_PATH/themes/

echo "✅ Deployment complete!"
echo "Test at: http://{your-cloudways-url}"
```

### Option C: GitHub Actions Auto-Deploy

**Create:** `.github/workflows/deploy-to-dev.yml`

```yaml
name: Deploy to Cloudways Dev

on:
  push:
    branches: [ develop ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Cloudways
        uses: easingthemes/ssh-deploy@main
        env:
          SSH_PRIVATE_KEY: ${{ secrets.CLOUDWAYS_SSH_KEY }}
          REMOTE_HOST: 24.144.80.107
          REMOTE_USER: master_qcteaefabe
          SOURCE: "wp-content/"
          TARGET: "/home/master_qcteaefabe/applications/{app}/public_html/wp-content/"
          EXCLUDE: "/wp-content/uploads/, /wp-content/cache/"
```

---

## Step 6: SSH Key Setup (Recommended)

**On your local machine:**

```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "bc-ai-cloudways-dev"
# Save to: ~/.ssh/id_cloudways_bcai
# Add passphrase for security

# View public key
cat ~/.ssh/id_cloudways_bcai.pub
```

**In Cloudways Dashboard:**

1. Go to Servers → Your Server
2. Click "Settings & Packages"
3. Scroll to "SSH Public Key"
4. Paste your public key
5. Save

**Test connection:**

```bash
ssh -i ~/.ssh/id_cloudways_bcai master_qcteaefabe@24.144.80.107
# Should connect without password!
```

**Add to SSH config** for convenience:

```bash
# Edit ~/.ssh/config
cat >> ~/.ssh/config <<'EOF'

Host cloudways-bcai-dev
    HostName 24.144.80.107
    User master_qcteaefabe
    IdentityFile ~/.ssh/id_cloudways_bcai
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

# Now you can just:
ssh cloudways-bcai-dev
```

---

## Step 7: Cloudways-Specific Features

### Backups

**Cloudways has built-in backups:**

- Dashboard → Backup & Restore
- On-demand backups before major changes
- Scheduled automatic backups
- One-click restore if something breaks

**Before testing agent automation:**
```bash
# Create backup via dashboard
# Or via CLI if available
```

### Staging Environment

**Cloudways can clone your app:**

1. Dashboard → Applications
2. Click your app
3. "Clone This App"
4. Creates exact copy for testing

**Perfect for:**
- Testing risky changes
- Agent automation experiments
- Before deploying to dev server

### SSL Certificate

Cloudways provides free SSL:

1. Dashboard → SSL Certificate
2. Install Let's Encrypt certificate
3. Dev site will be https://

---

## Step 8: First Connection Checklist

**When you first SSH in, run these commands:**

```bash
# 1. Confirm you're on DEV (not production!)
hostname
# Should NOT say anything about bc-ai.ca

# 2. Check WordPress location
pwd
ls -la

# 3. Find WordPress install
find ~ -name "wp-config.php" 2>/dev/null | head -3

# 4. Check PHP version
php -v
# Should be 8.0+

# 5. Check WP-CLI
wp --version
# Cloudways pre-installs this

# 6. Check git
git --version

# 7. Check disk space
df -h

# 8. Check current WordPress status (if installed)
cd ~/applications/*/public_html
wp core version
wp plugin list
wp theme list
```

**Share this output** and I'll help with next steps!

---

## Step 9: Update Our .gitignore

**Add Cloudways-specific ignores:**

```
# Cloudways
.cloudways-credentials
*.pem
*.key

# WordPress on Cloudways
wp-config.php
.htaccess

# Development
error_log
debug.log
*.log
```

---

## Step 10: Create Secure Credentials File

**For storing Cloudways info safely:**

```bash
# Create encrypted credentials file (local only, never commit)
cat > .cloudways-credentials <<'EOF'
# BC+AI Cloudways Development Server
# NEVER COMMIT THIS FILE

Host: 24.144.80.107
Username: master_qcteaefabe
Password: [stored in password manager]
SSH Key: ~/.ssh/id_cloudways_bcai

# WordPress Admin (on dev server)
WP Admin URL: http://[cloudways-url]/wp-admin
WP Username: [from Cloudways]
WP Password: [from Cloudways]

# Database (on dev server)
DB Host: localhost
DB Name: [from Cloudways]
DB User: [from Cloudways]
DB Password: [from Cloudways]

# Application Path
App Path: /home/master_qcteaefabe/applications/[app-name]/public_html
EOF

# Encrypt it
gpg -c .cloudways-credentials
# Creates: .cloudways-credentials.gpg (can commit this if needed)

# Delete unencrypted
rm .cloudways-credentials
```

---

## Next Steps

**You choose:**

### Option A: I Do It (With Your Permission)

You provide the SSH password, I connect and explore the server carefully, document everything, and set it up.

**Safeguards:**
- I'll only run read-only commands first
- I'll show you what I'm doing
- You can stop me anytime
- I'll document every change

### Option B: You Do It (I Guide)

You run commands in Cloudways web terminal, share output, and I guide you through setup.

**Safeguards:**
- You have full control
- You see everything happening
- No automated changes without your approval

### Option C: SSH Key Setup First

Set up SSH key authentication so I can connect securely without passwords in plain text.

---

**Which approach would you prefer?**

1. Give me the password and I'll carefully explore (read-only first)
2. You run commands in Cloudways web terminal and share output
3. Set up SSH keys first for secure automation

Let me know and we'll proceed safely! 🌲