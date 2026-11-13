#!/usr/bin/env bash
# Repeatable logged-out check for issue #767 user-enumeration surfaces.
#
# Asserts the #767 verification curls against the desired post-apply state
# and prints PASS/FAIL: five spellings of the REST users route (core matches
# routes case-insensitively), the sitemap index, /?author=1 and HSTS. Never
# prints usernames, slugs, Location URLs, or response bodies.
#
# Safe by construction: GET/HEAD only. No POST, no xmlrpc.php, no login,
# no credential test.
#
# Usage:
#   scripts/check_user_enumeration.sh
#   KK_SITE_URL=https://kriskrug.co scripts/check_user_enumeration.sh
#
# Exit 0 only when every check PASSes.

set -euo pipefail

BASE="${KK_SITE_URL:-https://kriskrug.co}"
BASE="${BASE%/}"

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl is required" >&2
  exit 2
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required" >&2
  exit 2
fi

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/kk-767-enum.XXXXXX")"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT INT TERM

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

# --- 1. REST users: no public user list ------------------------------------
# Desired: no spelling of the users route returns user data. WordPress core
# matches REST routes case-insensitively, so mixed-case paths and the
# ?rest_route= form are probed as well as the canonical lowercase path.
check_users_route() {
  local label="$1" url="$2" slot="$3"
  local body="$tmpdir/users-$slot.json" meta="$tmpdir/users-$slot.meta" hdr="$tmpdir/users-$slot.hdr"
  curl -sS --max-time 30 \
    -D "$hdr" \
    -o "$body" \
    -w "http_code=%{http_code}\n" \
    -A "kk-check-user-enumeration/1.0" \
    "$url" >"$meta"

  local code total eval_out result detail
  code="$(sed -n 's/^http_code=//p' "$meta")"
  total="$(awk 'BEGIN{IGNORECASE=1} /^x-wp-total:/{gsub(/\r/,""); print $2; exit}' "$hdr")"
  total="${total:-absent}"

  eval_out="$(
    USERS_CODE="$code" USERS_TOTAL="$total" USERS_BODY="$body" python3 - <<'PY'
import json, os
code = os.environ["USERS_CODE"]
total = os.environ["USERS_TOTAL"]
body = open(os.environ["USERS_BODY"], "rb").read()
kind = "unparsed"
length = -1
try:
    data = json.loads(body.decode("utf-8", "replace"))
except Exception:
    data = None
if isinstance(data, list):
    kind = "array"
    length = len(data)
elif isinstance(data, dict):
    kind = "object"
    length = 0
leaks = kind == "array" and length > 0
# A single-user route returns one user object; an error object has "code".
if kind == "object" and ("slug" in data or "id" in data) and "code" not in data:
    leaks = True
total_n = int(total) if total.isdigit() else None
if total_n is not None and total_n > 0:
    leaks = True
if code in {"401", "403", "404"} and not leaks:
    result = "pass"
elif code == "200" and kind == "array" and length == 0 and (total_n is None or total_n == 0):
    result = "pass"
elif code == "200" and kind == "object" and not leaks:
    result = "pass"
else:
    result = "fail"
print(f"{result} status={code} x-wp-total={total} json={kind} array_length={length if length >= 0 else 'n/a'}")
PY
  )"

  result="${eval_out%% *}"
  detail="${eval_out#* }"
  if [[ "$result" == "pass" ]]; then
    pass "REST ${label}  ($detail)"
  else
    fail "REST ${label}  ($detail; expected 401/403/404 or empty list, no x-wp-total>0, no user object)"
  fi
}

# Pagely's ARES edge caches anonymous GET REST responses, including 200s. A
# unique query parameter bypasses the edge so each probe measures the origin,
# and keeps this check from seeding cache entries of its own.
nonce="kk_enum_check=$(date +%s)$RANDOM"
check_users_route "/wp-json/wp/v2/users" "$BASE/wp-json/wp/v2/users?$nonce" 1
check_users_route "/wp-json/wp/v2/Users" "$BASE/wp-json/wp/v2/Users?$nonce" 2
check_users_route "/wp-json/WP/V2/USERS" "$BASE/wp-json/WP/V2/USERS?$nonce" 3
check_users_route "/wp-json/wp/v2/Users/1" "$BASE/wp-json/wp/v2/Users/1?$nonce" 4
check_users_route "/?rest_route=/wp/v2/Users" "$BASE/?rest_route=/wp/v2/Users&$nonce" 5

# --- 2. Sitemap index: no users child --------------------------------------
# Desired: curl -s "$BASE/wp-sitemap.xml" | grep -c users  →  0
sitemap_body="$tmpdir/sitemap.xml"
sitemap_meta="$tmpdir/sitemap.meta"
curl -sS --max-time 30 \
  -o "$sitemap_body" \
  -w "http_code=%{http_code}\n" \
  -A "kk-check-user-enumeration/1.0" \
  "$BASE/wp-sitemap.xml" >"$sitemap_meta"

sitemap_code="$(sed -n 's/^http_code=//p' "$sitemap_meta")"
users_hits="$(
  python3 - "$sitemap_body" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
print(len(re.findall(r"users", text, flags=re.I)))
PY
)"

if [[ "$sitemap_code" == "200" && "$users_hits" == "0" ]]; then
  pass "sitemap /wp-sitemap.xml  (status=${sitemap_code} users_substring_count=${users_hits})"
else
  fail "sitemap /wp-sitemap.xml  (status=${sitemap_code} users_substring_count=${users_hits}; expected 200 and 0)"
fi

# --- 3. /?author=1: no /author/ Location -----------------------------------
# Desired: redirect_url exposes no username. We only inspect whether Location
# contains /author/ and the status code — never the URL itself.
author_hdr="$tmpdir/author.hdr"
author_meta="$tmpdir/author.meta"
curl -sS --max-time 30 \
  --max-redirs 0 \
  -D "$author_hdr" \
  -o /dev/null \
  -w "http_code=%{http_code}\nredirect_has_author=%{redirect_url}\n" \
  -A "kk-check-user-enumeration/1.0" \
  "$BASE/?author=1" >"$author_meta" || true

author_code="$(sed -n 's/^http_code=//p' "$author_meta")"
# redirect_url is captured only to test the /author/ substring, then discarded.
author_redir_raw="$(sed -n 's/^redirect_has_author=//p' "$author_meta")"
location_raw="$(awk 'BEGIN{IGNORECASE=1} /^location:/{sub(/^[^:]+:[[:space:]]*/, ""); gsub(/\r/,""); print; exit}' "$author_hdr")"

has_author="no"
case "$author_redir_raw" in
  */author/*) has_author="yes" ;;
esac
case "$location_raw" in
  */author/*) has_author="yes" ;;
esac
unset author_redir_raw location_raw

if [[ "$has_author" == "yes" ]]; then
  fail "author /?author=1  (status=${author_code} location_contains_/author/=yes; expected no /author/ in Location)"
elif [[ "$author_code" == "404" || "$author_code" == "410" || "$author_code" == "403" ]]; then
  pass "author /?author=1  (status=${author_code} location_contains_/author/=no)"
elif [[ "$author_code" =~ ^3[0-9][0-9]$ ]]; then
  pass "author /?author=1  (status=${author_code} location_contains_/author/=no)"
elif [[ "$author_code" == "200" ]]; then
  pass "author /?author=1  (status=${author_code} location_contains_/author/=no)"
else
  fail "author /?author=1  (status=${author_code} location_contains_/author/=${has_author}; unexpected status)"
fi

# --- 4. HSTS present (owned by #709; still asserted here) ------------------
# Desired: curl -sI "$BASE/" | grep -c strict-transport-security  →  1
hsts_hdr="$tmpdir/hsts.hdr"
curl -sSI --max-time 30 \
  -A "kk-check-user-enumeration/1.0" \
  "$BASE/" >"$hsts_hdr"
hsts_code="$(awk 'NR==1 {print $2; exit}' "$hsts_hdr")"
hsts_count="$(
  python3 - "$hsts_hdr" <<'PY'
import sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read().lower()
print(sum(1 for line in text.splitlines() if line.startswith("strict-transport-security:")))
PY
)"

if [[ "$hsts_count" -ge 1 ]]; then
  pass "HSTS homepage  (status=${hsts_code} strict-transport-security_count=${hsts_count})"
else
  fail "HSTS homepage  (status=${hsts_code} strict-transport-security_count=${hsts_count}; expected >=1; owned by #709)"
fi

echo
echo "Summary: ${pass_count} PASS / ${fail_count} FAIL (desired post-apply state for #767)"
if [[ "$fail_count" -gt 0 ]]; then
  exit 1
fi
exit 0
