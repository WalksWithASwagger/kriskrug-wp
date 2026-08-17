#!/usr/bin/env bash
# Repeatable logged-out check for issue #767 user-enumeration surfaces.
#
# Asserts the four verification curls from #767 against the desired
# post-apply state and prints PASS/FAIL. Never prints usernames, slugs,
# Location URLs, or response bodies.
#
# Safe by construction: GET/HEAD only. No POST, no xmlrpc.php, no login,
# no credential test.
#
# Usage:
#   scripts/check_user_enumeration.sh
#   KK_SITE_URL=https://kriskrug.co scripts/check_user_enumeration.sh
#
# Exit 0 only when all four checks PASS. Before the KK-approved apply,
# expect FAIL on every row.

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
# Desired: curl -s "$BASE/wp-json/wp/v2/users" returns no user list.
users_body="$tmpdir/users.json"
users_meta="$tmpdir/users.meta"
curl -sS --max-time 30 \
  -D "$tmpdir/users.hdr" \
  -o "$users_body" \
  -w "http_code=%{http_code}\n" \
  -A "kk-check-user-enumeration/1.0" \
  "$BASE/wp-json/wp/v2/users" >"$users_meta"

users_code="$(sed -n 's/^http_code=//p' "$users_meta")"
users_total="$(awk 'BEGIN{IGNORECASE=1} /^x-wp-total:/{gsub(/\r/,""); print $2; exit}' "$tmpdir/users.hdr")"
users_total="${users_total:-absent}"

users_eval="$(
  USERS_CODE="$users_code" USERS_TOTAL="$users_total" USERS_BODY="$users_body" python3 - <<'PY'
import json, os, sys
code = os.environ["USERS_CODE"]
total = os.environ["USERS_TOTAL"]
path = os.environ["USERS_BODY"]
body = open(path, "rb").read()
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
leaks_list = kind == "array" and length > 0
total_n = None
if total.isdigit():
    total_n = int(total)
if total_n is not None and total_n > 0:
    leaks_list = True
if code in {"401", "403", "404"} and not leaks_list:
    result = "pass"
elif code == "200" and kind == "array" and length == 0 and (total_n is None or total_n == 0):
    result = "pass"
elif code == "200" and kind == "object" and not leaks_list:
    result = "pass"
else:
    result = "fail"
print(f"{result} status={code} x-wp-total={total} json={kind} array_length={length if length >= 0 else 'n/a'}")
PY
)"

users_result="${users_eval%% *}"
users_detail="${users_eval#* }"
if [[ "$users_result" == "pass" ]]; then
  pass "REST /wp-json/wp/v2/users  ($users_detail)"
else
  fail "REST /wp-json/wp/v2/users  ($users_detail; expected 401/403/404 or empty list, no x-wp-total>0)"
fi

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
