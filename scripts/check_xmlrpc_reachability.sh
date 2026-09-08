#!/usr/bin/env bash
# Repeatable logged-out XML-RPC reachability check for issue #1002.
#
# Asserts the desired post-apply host/WAF-deny state: GET and HEAD
# https://kriskrug.co/xmlrpc.php return 403, 404, or 410.
#
# Safe by construction: GET and HEAD only. No POST, no request body,
# no method names, no response-body dump.
#
# A Code Snippet that only flips xmlrpc_enabled does not change GET/HEAD
# 405. This script will still FAIL after a snippet-only apply. That is
# intentional — host deny is the recommended control.
#
# Usage:
#   scripts/check_xmlrpc_reachability.sh
#   KK_SITE_URL=https://kriskrug.co scripts/check_xmlrpc_reachability.sh
#
# Exit 0 only when both verbs are closed. Before a KK-approved host deny,
# expect FAIL (current live 2026-09-08: GET/HEAD 405).

set -euo pipefail

BASE="${KK_SITE_URL:-https://kriskrug.co}"
BASE="${BASE%/}"
TARGET="${BASE}/xmlrpc.php"

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required" >&2
  exit 2
fi

pass_count=0
fail_count=0

pass() {
  echo "PASS  $*"
  pass_count=$((pass_count + 1))
}

fail() {
  echo "FAIL  $*"
  fail_count=$((fail_count + 1))
}

is_closed() {
  case "$1" in
    403|404|410) return 0 ;;
    *) return 1 ;;
  esac
}

is_reachable() {
  case "$1" in
    200|405) return 0 ;;
    *) return 1 ;;
  esac
}

probe() {
  local verb="$1"
  local extra=()
  case "$verb" in
    GET) extra=() ;;
    HEAD) extra=(-I) ;;
    *)
      echo "ERROR: unsupported verb" >&2
      exit 2
      ;;
  esac

  curl -sS --max-time 30 \
    "${extra[@]}" \
    -o /dev/null \
    -w "%{http_code}" \
    -A "kk-check-xmlrpc-reachability/1.0" \
    "$TARGET"
}

get_code="$(probe GET)"
head_code="$(probe HEAD)"

# Never print bodies. Status codes only.
if is_closed "$get_code" && is_closed "$head_code"; then
  pass "GET ${TARGET}  (status=${get_code}; closed)"
  pass "HEAD ${TARGET}  (status=${head_code}; closed)"
elif is_reachable "$get_code" || is_reachable "$head_code"; then
  fail "GET ${TARGET}  (status=${get_code}; reachable — expected 403/404/410 after host deny)"
  fail "HEAD ${TARGET}  (status=${head_code}; reachable — expected 403/404/410 after host deny)"
else
  fail "GET ${TARGET}  (status=${get_code}; unexpected — expected 403/404/410; 405 means reachable)"
  fail "HEAD ${TARGET}  (status=${head_code}; unexpected — expected 403/404/410; 405 means reachable)"
fi

echo
echo "Summary: ${pass_count} PASS / ${fail_count} FAIL (desired post-apply host/WAF deny for #1002)"
if [[ "$fail_count" -gt 0 ]]; then
  exit 1
fi
exit 0
