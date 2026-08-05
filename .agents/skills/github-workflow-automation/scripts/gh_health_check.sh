#!/usr/bin/env bash
#
# Health check for gh CLI authentication and permissions
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== GitHub CLI Health Check ==="
echo

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}✗ gh CLI not installed${NC}"
    echo
    echo "Install gh CLI:"
    echo "  macOS: brew install gh"
    echo "  Linux: See https://github.com/cli/cli#installation"
    echo
    exit 1
fi

echo -e "${GREEN}✓ gh CLI installed${NC}"
gh --version
echo

# Check authentication
echo "Checking authentication..."
if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo
    echo "Authenticate with:"
    echo "  gh auth login"
    echo
    exit 1
fi

echo -e "${GREEN}✓ Authenticated${NC}"
gh auth status
echo

# Check repo permissions (if in a repo)
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Checking repository..."

    # Get current repo
    REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")

    if [ -n "$REPO" ]; then
        echo -e "${GREEN}✓ Repository detected: $REPO${NC}"
        echo

        # Check permissions
        echo "Checking permissions..."

        # Try to create a test label (and delete it)
        if gh label create "__health-check-test__" --description "Test" --color "000000" --force &> /dev/null; then
            gh label delete "__health-check-test__" --yes &> /dev/null
            echo -e "${GREEN}✓ Write permissions confirmed${NC}"
        else
            echo -e "${YELLOW}⚠ Limited permissions (read-only?)${NC}"
            echo "Some operations may not work"
        fi
    else
        echo -e "${YELLOW}⚠ Not in a GitHub repository${NC}"
        echo "cd to a repository to check repo-specific permissions"
    fi
else
    echo -e "${YELLOW}⚠ Not in a git repository${NC}"
fi

echo
echo -e "${GREEN}=== Health check complete ===${NC}"
exit 0
