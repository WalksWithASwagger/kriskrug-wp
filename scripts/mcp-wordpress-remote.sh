#!/usr/bin/env bash
# Launch @automattic/mcp-wordpress-remote with credentials from gitignored .env.
# Used by Cursor MCP config — do not hardcode passwords in mcp.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${WP_MCP_ENV_FILE:-$SCRIPT_DIR/notion-to-wp/.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "mcp-wordpress-remote: missing $ENV_FILE (copy from .env.example)" >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${WP_USER:?WP_USER not set in $ENV_FILE}"
: "${WP_APP_PASSWORD:?WP_APP_PASSWORD not set in $ENV_FILE}"

export WP_API_URL="${WP_API_URL:-https://kriskrug.co/wp-json/mcp/mcp-adapter-default-server}"
export WP_API_USERNAME="${WP_API_USERNAME:-$WP_USER}"
export WP_API_PASSWORD="${WP_API_PASSWORD:-$WP_APP_PASSWORD}"
export LOG_FILE="${LOG_FILE:-$HOME/.cursor/logs/mcp-wordpress.log}"

mkdir -p "$(dirname "$LOG_FILE")"

exec npx -y @automattic/mcp-wordpress-remote@latest
