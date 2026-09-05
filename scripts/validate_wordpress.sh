#!/usr/bin/env bash
#
# Validate WordPress code using PHP CodeSniffer and WordPress Coding Standards
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Defaults
STANDARD="WordPress"
if [ -f "phpcs.xml.dist" ]; then
    STANDARD="phpcs.xml.dist"
fi
FIX=false
FILES=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX=true
            shift
            ;;
        --standard)
            STANDARD="$2"
            shift 2
            ;;
        --files)
            FILES="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--fix] [--standard WordPress|WordPress-Core|WordPress-Extra] [--files path]"
            exit 1
            ;;
    esac
done

echo "=== WordPress Code Validation ==="
echo "Standard: $STANDARD"
echo "Files: ${FILES:-ruleset default}"
echo

PHPCS_BIN="phpcs"
PHPCBF_BIN="phpcbf"
if [ -x "vendor/bin/phpcs" ]; then
    PHPCS_BIN="vendor/bin/phpcs"
fi
if [ -x "vendor/bin/phpcbf" ]; then
    PHPCBF_BIN="vendor/bin/phpcbf"
fi

if ! command -v "$PHPCS_BIN" &> /dev/null; then
    echo -e "${RED}✗ phpcs not found${NC}"
    echo
    echo "Install repo-owned PHPCS and WordPress Coding Standards:"
    echo "  composer install"
    echo
    echo "If Composer is not installed, install it first:"
    echo "  https://getcomposer.org/download/"
    echo
    exit 1
fi

# Check if WordPress standards are installed
if ! "$PHPCS_BIN" -i | grep -q "WordPress"; then
    echo -e "${YELLOW}⚠ WordPress Coding Standards not found${NC}"
    echo
    echo "Install repo-owned standards:"
    echo "  composer install"
    echo
    exit 1
fi

# Run phpcs
echo "Running phpcs..."
PHPCS_ARGS=(--standard="$STANDARD" --report=summary)
if [ -n "$FILES" ]; then
    PHPCS_ARGS+=("$FILES")
fi

if "$PHPCS_BIN" "${PHPCS_ARGS[@]}"; then
    echo
    echo -e "${GREEN}✓ No coding standard violations found${NC}"
    exit 0
else
    PHPCS_EXIT=$?
    echo
    echo -e "${RED}✗ Coding standard violations found${NC}"
    echo

    if [ "$FIX" = true ]; then
        if command -v "$PHPCBF_BIN" &> /dev/null; then
            echo "Attempting to auto-fix violations..."
            PHPCBF_ARGS=(--standard="$STANDARD")
            if [ -n "$FILES" ]; then
                PHPCBF_ARGS+=("$FILES")
            fi
            if "$PHPCBF_BIN" "${PHPCBF_ARGS[@]}"; then
                echo
                echo -e "${GREEN}✓ Auto-fix completed${NC}"
                echo
                echo "Re-running phpcs to check remaining violations..."
                if "$PHPCS_BIN" "${PHPCS_ARGS[@]}"; then
                    echo
                    echo -e "${GREEN}✓ All violations fixed${NC}"
                    exit 0
                else
                    echo
                    echo -e "${YELLOW}⚠ Some violations remain and require manual fixing${NC}"
                    exit 1
                fi
            else
                echo
                echo -e "${YELLOW}⚠ Auto-fix completed with warnings${NC}"
                echo "Some violations require manual fixing"
                exit 1
            fi
        else
            echo -e "${YELLOW}⚠ phpcbf not found, cannot auto-fix${NC}"
            echo "Install with: composer install"
            exit $PHPCS_EXIT
        fi
    else
        echo "Run with --fix to attempt automatic fixes"
        exit $PHPCS_EXIT
    fi
fi
