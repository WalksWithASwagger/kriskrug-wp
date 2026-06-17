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
TESTS_DETECTED=false
TEMP_DIRS=""

cleanup() {
    for dir in $TEMP_DIRS; do
        rm -rf "$dir"
    done
}
trap cleanup EXIT

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

python_has_notion_deps() {
    "$1" - <<'PY' >/dev/null 2>&1
import dotenv
import requests
import yaml
PY
}

select_notion_python() {
    if [ -x "scripts/notion-to-wp/.venv/bin/python" ]; then
        echo "scripts/notion-to-wp/.venv/bin/python"
        return 0
    fi

    local candidate
    local python_bin
    for candidate in python3 python; do
        if ! command -v "$candidate" >/dev/null 2>&1; then
            continue
        fi
        python_bin="$(command -v "$candidate")"
        if python_has_notion_deps "$python_bin"; then
            echo "$python_bin"
            return 0
        fi
    done

    if ! command -v python3 >/dev/null 2>&1; then
        echo "No python3 found for Notion publisher tests" >&2
        return 1
    fi

    local temp_venv
    temp_venv="$(mktemp -d /tmp/kriskrug-notion-tests.XXXXXX)"
    TEMP_DIRS="$TEMP_DIRS $temp_venv"
    python3 -m venv "$temp_venv"
    PIP_DISABLE_PIP_VERSION_CHECK=1 "$temp_venv/bin/python" -m pip install -q -r scripts/notion-to-wp/requirements.txt
    echo "$temp_venv/bin/python"
}

# Detect and run PHPUnit
if [ -f "phpunit.xml" ] || [ -f "phpunit.xml.dist" ]; then
    TESTS_DETECTED=true
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
    TESTS_DETECTED=true
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
    TESTS_DETECTED=true
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

# Detect and run this repo's Notion publisher tests from the root checkout
if [ -d "scripts/notion-to-wp/tests" ]; then
    TESTS_DETECTED=true
    echo "Detected: Notion publisher tests"

    PYTHON_BIN="$(select_notion_python)"

    echo "Running unittest for scripts/notion-to-wp/tests..."
    if [ "$VERBOSE" = true ]; then
        "$PYTHON_BIN" -m unittest discover -s scripts/notion-to-wp/tests -v
    else
        "$PYTHON_BIN" -m unittest discover -s scripts/notion-to-wp/tests
    fi
    echo -e "${GREEN}✓ Notion publisher tests passed${NC}"
    echo
fi

# Detect and run root-level script tests
if [ -d "scripts/tests" ]; then
    TESTS_DETECTED=true
    echo "Detected: repo script tests"

    if command -v python3 >/dev/null 2>&1; then
        echo "Running unittest for scripts/tests..."
        if [ "$VERBOSE" = true ]; then
            python3 -m unittest discover -s scripts/tests -v
        else
            python3 -m unittest discover -s scripts/tests
        fi
        echo -e "${GREEN}✓ repo script tests passed${NC}"
        echo
    else
        echo -e "${YELLOW}⚠ scripts/tests found but python3 is not installed${NC}"
        echo
    fi
fi

# Detect and run Node.js tests
if [ -f "package.json" ]; then
    TESTS_DETECTED=true
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
if [ "$TESTS_DETECTED" = false ]; then
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
