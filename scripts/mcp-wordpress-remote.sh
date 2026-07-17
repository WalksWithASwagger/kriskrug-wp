#!/usr/bin/env bash
# Launch @automattic/mcp-wordpress-remote with credentials from Varlock
# (~/.agents/env/wordpress) or the gitignored notion-to-wp/.env fallback.
# Used by Cursor MCP config — do not hardcode passwords in mcp.json.
#
# Supply-chain pin (issue #378): MCP_WP_REMOTE_VERSION below replaces the old
# floating tag so a registry publish cannot silently change what runs with WP
# credentials.
#
# Upgrade procedure — bump the pin only deliberately:
#   1. npm view @automattic/mcp-wordpress-remote version   # see current stable
#   2. Review the upstream release notes/diff for that version.
#   3. Update MCP_WP_REMOTE_VERSION here AND PINNED_VERSION in
#      scripts/tests/test_mcp_wordpress_remote.py (they must match).
#   4. Verify: bash -n scripts/mcp-wordpress-remote.sh
#      python3 -m unittest discover -s scripts/tests -p 'test_mcp_wordpress_remote.py'
# Upgrade when upstream ships a security fix or a feature we need — not on
# every release.

set -euo pipefail

# Pinned 2026-07-16 from `npm view @automattic/mcp-wordpress-remote version`.
MCP_WP_REMOTE_VERSION="0.3.5"
MCP_WP_REMOTE_PKG="@automattic/mcp-wordpress-remote@${MCP_WP_REMOTE_VERSION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_WP_ENV="${WP_MCP_AGENTS_ENV:-$HOME/.agents/env/wordpress}"
ENV_FILE="${WP_MCP_ENV_FILE:-$SCRIPT_DIR/notion-to-wp/.env}"

# Cursor spawns MCP commands with a minimal PATH, so fall back to known
# install locations when command -v misses.
find_bin() {
  local name="$1" found candidate
  shift
  found="$(command -v "$name" 2>/dev/null || true)"
  if [[ -n "$found" ]]; then
    printf '%s\n' "$found"
    return 0
  fi
  for candidate in "$@"; do
    if [[ -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

NPX_BIN="$(find_bin npx /opt/homebrew/bin/npx /usr/local/bin/npx)" || {
  echo "mcp-wordpress-remote: npx not found on PATH or in known install locations" >&2
  exit 1
}

# Prefer the shared agents Varlock contract when present and varlock is
# installed. Scrub ambient WP credentials first so only the contract's
# resolved values reach the server.
if [[ -f "$AGENTS_WP_ENV/.env.local" ]]; then
  if VARLOCK_BIN="$(find_bin varlock /opt/homebrew/bin/varlock "$HOME/.config/varlock/bin/varlock")"; then
    mkdir -p "$HOME/.agents/logs"
    export LOG_FILE="${LOG_FILE:-$HOME/.agents/logs/mcp-wordpress.log}"
    exec env -u WP_API_USERNAME -u WP_API_PASSWORD -u WP_USER -u WP_APP_PASSWORD \
      "$VARLOCK_BIN" run --path "$AGENTS_WP_ENV" --inject vars -- \
      "$NPX_BIN" -y "$MCP_WP_REMOTE_PKG"
  fi
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "mcp-wordpress-remote: missing $ENV_FILE (copy from .env.example) and no $AGENTS_WP_ENV/.env.local" >&2
  exit 1
fi

# shellcheck disable=SC1090
set -a
source "$ENV_FILE"
set +a

: "${WP_USER:?WP_USER not set in $ENV_FILE}"
: "${WP_APP_PASSWORD:?WP_APP_PASSWORD not set in $ENV_FILE}"

export WP_API_URL="${WP_API_URL:-https://kriskrug.co/wp-json/mcp/mcp-adapter-default-server}"
export WP_API_USERNAME="${WP_API_USERNAME:-$WP_USER}"
export WP_API_PASSWORD="${WP_API_PASSWORD:-$WP_APP_PASSWORD}"
export LOG_FILE="${LOG_FILE:-$HOME/.cursor/logs/mcp-wordpress.log}"

mkdir -p "$(dirname "$LOG_FILE")"

exec "$NPX_BIN" -y "$MCP_WP_REMOTE_PKG"
