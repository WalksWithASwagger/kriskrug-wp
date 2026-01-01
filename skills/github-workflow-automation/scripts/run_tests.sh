#!/usr/bin/env bash
#
# Run test suites with automatic framework detection
# Supports: PHPUnit, pytest, npm test, WordPress test suite
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--verbose]"
            exit 1
            ;;
    esac
done

echo "=== Test Runner ==="
echo

# Detect and run PHPUnit
if [ -f "phpunit.xml" ] || [ -f "phpunit.xml.dist" ] || [ -f "composer.json" ]; then
    echo "Detected: PHPUnit"

    if command -v vendor/bin/phpunit &> /dev/null; then
        echo "Running PHPUnit tests..."
        if [ "$VERBOSE" = true ]; then
            vendor/bin/phpunit --verbose
        else
            vendor/bin/phpunit
        fi
        echo -e "${GREEN}✓ PHPUnit tests passed${NC}"
        echo
    elif command -v phpunit &> /dev/null; then
        echo "Running PHPUnit tests (global)..."
        if [ "$VERBOSE" = true ]; then
            phpunit --verbose
        else
            phpunit
        fi
        echo -e "${GREEN}✓ PHPUnit tests passed${NC}"
        echo
    else
        echo -e "${YELLOW}⚠ PHPUnit configuration found but phpunit not installed${NC}"
        echo "Install with: composer install"
        echo
    fi
fi

# Detect and run WordPress tests
if [ -n "${WP_TESTS_DIR:-}" ] || [ -f "tests/bootstrap.php" ]; then
    echo "Detected: WordPress Test Suite"

    if command -v vendor/bin/phpunit &> /dev/null; then
        echo "Running WordPress tests..."
        if [ "$VERBOSE" = true ]; then
            vendor/bin/phpunit --verbose
        else
            vendor/bin/phpunit
        fi
        echo -e "${GREEN}✓ WordPress tests passed${NC}"
        echo
    else
        echo -e "${YELLOW}⚠ WordPress tests found but PHPUnit not installed${NC}"
        echo
    fi
fi

# Detect and run Python tests
if [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
    echo "Detected: Python project"

    if command -v pytest &> /dev/null; then
        echo "Running pytest..."
        if [ "$VERBOSE" = true ]; then
            pytest -v
        else
            pytest
        fi
        echo -e "${GREEN}✓ pytest tests passed${NC}"
        echo
    elif [ -d "tests" ] && command -v python &> /dev/null; then
        echo "Running Python unittest..."
        python -m unittest discover tests
        echo -e "${GREEN}✓ Python tests passed${NC}"
        echo
    else
        echo -e "${YELLOW}⚠ Python project but no test runner found${NC}"
        echo
    fi
fi

# Detect and run Node.js tests
if [ -f "package.json" ]; then
    echo "Detected: Node.js project"

    if command -v npm &> /dev/null; then
        # Check if test script exists
        if grep -q '"test"' package.json; then
            echo "Running npm test..."
            npm test
            echo -e "${GREEN}✓ npm tests passed${NC}"
            echo
        else
            echo -e "${YELLOW}⚠ package.json found but no test script defined${NC}"
            echo
        fi
    else
        echo -e "${YELLOW}⚠ package.json found but npm not installed${NC}"
        echo
    fi
fi

# If no tests detected
if [ ! -f "phpunit.xml" ] && [ ! -f "phpunit.xml.dist" ] && \
   [ ! -f "pytest.ini" ] && [ ! -f "package.json" ] && \
   [ ! -f "composer.json" ]; then
    echo -e "${YELLOW}⚠ No test configuration detected${NC}"
    echo "Supported: PHPUnit, pytest, npm test, WordPress tests"
    echo
    echo "To add tests:"
    echo "  PHP: composer require --dev phpunit/phpunit"
    echo "  Python: pip install pytest"
    echo "  Node: npm install --save-dev jest"
    echo
    exit 1
fi

echo -e "${GREEN}=== All tests completed ===${NC}"
exit 0
