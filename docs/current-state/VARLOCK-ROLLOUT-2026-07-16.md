# Varlock rollout — kriskrug-wp (2026-07-16)

**Status:** implemented for this repo’s Phase 0 / ops secrets path.  
**Does not authorize** live WordPress writes.  
**Does not** make Cursor Cloud pick up laptop 1Password automatically.

## Verdict (locked)

| Layer | Role |
|---|---|
| **Vault** (1Password / Infisical / Bitwarden) | Canonical secret store |
| **Varlock** (per repo `.env.schema`) | Schema + validation + AI-safe docs + `varlock run` injection |
| **Cursor Cloud secrets** | Separate injection path for remote agents |

Do **not** invent one global auto-loader. Cross-directory personal use is only via explicit `varlock run -p ~/.env.cursor -- …`.

## 1. Human inventory → 1Password (no paste into chat/git)

Create vault item group **`kk-dev`** with fields matching env names:

| Field / item path (suggested) | Env name | Used by |
|---|---|---|
| `op://kk-dev/kriskrug-wp/username` | `WP_USER` | REST / publisher / morning-truth auth |
| `op://kk-dev/kriskrug-wp/credential` | `WP_APP_PASSWORD` | same |
| `op://kk-dev/notion/credential` | `NOTION_TOKEN` | Notion → WP connector |
| (optional) service account | `OP_TOKEN` | Cloud/CI `op()` without desktop app |

Revoke any historically leaked WP application passwords still active.

**Agent cannot complete this step** — values never leave the vault into the repo.

## 2. This repo (done)

- Committed [`.env.schema`](../../.env.schema) — names, sensitivity, defaults; no plaintext secrets
- `!.env.schema` kept un-ignored in `.gitignore`
- `make env-check` — soft-OK when secrets absent (Cloud-safe)
- `make varlock-run CMD='…'` — wraps `varlock run --inject vars -- …`
- Compat loaders in `scripts/common.py` / `connector_config.py` still honor process env first

### Local operator loop

```bash
# once
curl -sSfL https://varlock.dev/install.sh | sh -s
export PATH="${XDG_CONFIG_HOME:-$HOME/.config}/varlock/bin:$PATH"

# optional 1Password plugin
varlock install-plugin @varlock/1password-plugin@latest
# uncomment @plugin / @initOp lines in .env.schema (see file header)

# gitignored local resolvers (never commit)
cp docs/current-state/templates/varlock.env.local.example .env.local
# edit op:// paths to match your vault

make env-check
make varlock-run CMD='make status-readonly'
```

Preferred: **`varlock run`** so process env is injected; existing `load_env()` keeps working.  
Bridge (temporary): write gitignored `scripts/notion-to-wp/.env` only for tools that cannot use process env (treat as cache).

## 3. Cursor Cloud (separate channel)

Same vault values, different delivery:

1. Cursor dashboard → Cloud Agent secrets / environment
2. Set `WP_USER`, `WP_APP_PASSWORD`, optional `NOTION_TOKEN` (and `OP_TOKEN` only if using service-account `op()` in Cloud)
3. Re-run `make status-readonly` — draft counts should stop being false zeros when auth works

Laptop Varlock ≠ Cloud injection.

## 4. Mirror into sibling repos

Copy the pattern (not the secrets):

1. Commit a `.env.schema` (start from [`templates/sibling.env.schema.example`](templates/sibling.env.schema.example))
2. Un-ignore it (`!.env.schema`)
3. Point `op://` paths at the **same** `kk-dev` vault items where names match
4. Keep repo-specific renames documented (e.g. sibling `NOTION_API_KEY` vs this repo’s `NOTION_TOKEN`)

Template file is the checklist; do not assume `kk-ai-ecosystem` is present in this workspace.

## 5. Retire plaintext `.env` as source of truth

| Keep | Deprecate as SoT |
|---|---|
| Process env / `varlock run` | Committing or sharing plaintext `.env` |
| Vault `op://` in `.env.local` | `~/Code/notion-local/kk-ai-ecosystem/.env` sibling fallback as primary |
| Cursor Cloud secrets | Pasting secrets into chat / PR / docs |

Loaders still accept `scripts/notion-to-wp/.env` and `KKAI_ENV_PATH` so nothing breaks mid-migration. Remove those fallbacks only after morning-truth, connector, and MCP are proven under `varlock run` / Cloud secrets.

## What not to do

- Global silent Varlock export into every shell
- Real secrets in `.env.schema`
- Assuming Varlock replaces Cursor Cloud secrets
- Mixing “collect secrets” with live WP content writes in the same session

## Proof this session

- Varlock **1.11.0** installed under `~/.config/varlock/bin`
- `make env-check` exits 0 with schema readable when WP secrets are absent
- Schema documents vault field map + plugin enable steps
