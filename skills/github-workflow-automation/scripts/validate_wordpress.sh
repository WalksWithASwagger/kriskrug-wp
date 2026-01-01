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
FIX=false
FILES="."

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
echo "Files: $FILES"
echo

# Check if phpcs is installed
if ! command -v phpcs &> /dev/null; then
    echo -e "${RED}✗ phpcs not found${NC}"
    echo
    echo "Install PHPCS and WordPress Coding Standards:"
    echo "  composer global require wp-coding-standards/wpcs"
    echo "  phpcs --config-set installed_paths ~/.composer/vendor/wp-coding-standards/wpcs"
    echo
    exit 1
fi

# Check if WordPress standards are installed
if ! phpcs -i | grep -q "WordPress"; then
    echo -e "${YELLOW}⚠ WordPress Coding Standards not found${NC}"
    echo
    echo "Install WordPress Coding Standards:"
    echo "  composer global require wp-coding-standards/wpcs"
    echo "  phpcs --config-set installed_paths ~/.composer/vendor/wp-coding-standards/wpcs"
    echo
    exit 1
fi

# Run phpcs
echo "Running phpcs..."
if phpcs --standard="$STANDARD" --report=summary "$FILES"; then
    echo
    echo -e "${GREEN}✓ No coding standard violations found${NC}"
    exit 0
else
    PHPCS_EXIT=$?
    echo
    echo -e "${RED}✗ Coding standard violations found${NC}"
    echo

    if [ "$FIX" = true ]; then
        if command -v phpcbf &> /dev/null; then
            echo "Attempting to auto-fix violations..."
            if phpcbf --standard="$STANDARD" "$FILES"; then
                echo
                echo -e "${GREEN}✓ Auto-fix completed${NC}"
                echo
                echo "Re-running phpcs to check remaining violations..."
                if phpcs --standard="$STANDARD" --report=summary "$FILES"; then
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
            echo "Install with: composer global require squizlabs/php_codesniffer"
            exit $PHPCS_EXIT
        fi
    else
        echo "Run with --fix to attempt automatic fixes"
        exit $PHPCS_EXIT
    fi
fi
