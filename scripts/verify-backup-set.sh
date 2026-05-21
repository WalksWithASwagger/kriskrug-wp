#!/usr/bin/env bash
set -u

allow_incomplete=0

if [[ "${1:-}" == "--allow-incomplete" ]]; then
  allow_incomplete=1
  shift
fi

backup_dir="${1:-}"

if [[ -z "$backup_dir" ]]; then
  echo "Usage: $0 [--allow-incomplete] backup/YYYY-MM-DD" >&2
  exit 2
fi

errors=0
warnings=0

fail() {
  echo "ERROR: $*"
  errors=$((errors + 1))
}

warn() {
  echo "WARN: $*"
  warnings=$((warnings + 1))
}

ok() {
  echo "OK: $*"
}

has_match() {
  compgen -G "$backup_dir/$1" >/dev/null
}

require_match() {
  local pattern="$1"
  local label="$2"

  if has_match "$pattern"; then
    ok "$label present"
  else
    fail "$label missing ($pattern)"
  fi
}

if [[ ! -d "$backup_dir" ]]; then
  fail "Backup directory not found: $backup_dir"
  echo "Backup gate failed."
  exit 1
fi

if [[ -f "$backup_dir/manifest.md" ]]; then
  ok "manifest.md present"
else
  fail "manifest.md missing"
fi

if [[ -f "$backup_dir/manifest-checksums.txt" ]]; then
  ok "manifest-checksums.txt present"

  if command -v sha256sum >/dev/null 2>&1; then
    (cd "$backup_dir" && sha256sum -c manifest-checksums.txt) || fail "checksum verification failed"
  elif command -v shasum >/dev/null 2>&1; then
    (cd "$backup_dir" && shasum -a 256 -c manifest-checksums.txt) || fail "checksum verification failed"
  else
    warn "No sha256sum or shasum command found; checksum verification skipped"
  fi
else
  fail "manifest-checksums.txt missing"
fi

if has_match "*.wpress"; then
  ok "All-in-One WP Migration archive present"
else
  require_match "*-db.gz" "database archive"
  require_match "*-plugins.zip" "plugins archive"
  require_match "*-themes.zip" "themes archive"
  require_match "*-mu-plugins.zip" "mu-plugins archive"
  require_match "*-others.zip" "others archive"

  if has_match "*-uploads.zip" || has_match "uploads.*" || [[ -d "$backup_dir/uploads" ]]; then
    ok "uploads archive or uploads directory present"
  elif [[ -f "$backup_dir/manifest.md" ]] && grep -Eiq 'uploads.*(skipped|deferred|missing|pagely|ssh|scp)' "$backup_dir/manifest.md"; then
    warn "uploads are absent but explicitly accounted for in manifest.md"
  else
    fail "uploads archive missing and no explicit deferral found in manifest.md"
  fi
fi

if [[ -f "$backup_dir/restore-notes.md" ]]; then
  ok "restore-notes.md present"

  if [[ "$allow_incomplete" -eq 0 ]]; then
    if grep -Eiq '^(restore_status|production_write_gate):[[:space:]]*passed[[:space:]]*$' "$backup_dir/restore-notes.md"; then
      ok "restore proof is marked passed"
    else
      fail "restore-notes.md must include 'restore_status: passed' or 'production_write_gate: passed'"
    fi
  fi
else
  if [[ "$allow_incomplete" -eq 1 ]]; then
    warn "restore-notes.md missing; archive can be inspected but the production-write gate is not satisfied"
  else
    fail "restore-notes.md missing; restore proof is required before production writes"
  fi
fi

echo ""

if [[ "$errors" -gt 0 ]]; then
  echo "Backup gate failed with $errors error(s) and $warnings warning(s)."
  exit 1
fi

if [[ "$warnings" -gt 0 ]]; then
  echo "Backup set inspected with $warnings warning(s)."
else
  echo "Backup gate passed."
fi
