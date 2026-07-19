# Varlock proof — 2026-07-16 (Cloud agent)

**Varlock:** 1.11.0 at `~/.config/varlock/bin/varlock`  
**Schema:** `.env.schema` (no plaintext secrets)

| Check | Result |
|---|---|
| `make env-check` without secrets | exit 0 — schema OK (WP secrets soft / absent) |
| `WP_USER`/`WP_APP_PASSWORD` in process env → `varlock load --agent` | redacted sensitive values shown |
| `varlock run --inject vars -- python3 …` | process env visible to child |
| `common.load_env()` process overlay | prefers OS env over file |
| Cursor Cloud secrets | **not** set in this VM (expected) — documented as separate channel |

Superseded follow-up: the current contract uses the human-managed
`~/.agents/env/values/` directory, not an external vault plugin. Cloud values
remain separate and require explicit approval.
