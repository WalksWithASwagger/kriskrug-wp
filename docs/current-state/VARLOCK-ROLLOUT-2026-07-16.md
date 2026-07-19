# Varlock rollout: kriskrug-wp

**Status:** the repository contract and process-injection path are implemented.
This does not authorize live WordPress writes or copy laptop values into cloud
environments.

## Contract

| Layer | Role |
|---|---|
| `~/.agents/env/values/.env.shared.local` | Human-managed reusable local values |
| `~/.agents/env/values/.env.kriskrug-wp.local` | Optional repo-specific local overrides |
| `.env.schema` | Committed variable names, sensitivity, defaults, and imports |
| `varlock run --inject vars -- ...` | Validated process injection |
| Cloud platform secret settings | Separate development or deployment copies |

Varlock is the repository contract and loader. The gitignored values directory
is the canonical source for this Mac. Cloud platforms retain only the values
their runtime needs.

## Local setup

Only the human operator should create or edit value files. Agents may inspect
`.env.schema`, but must not read `.env*` value files.

```bash
mkdir -p ~/.agents/env/values
chmod 700 ~/.agents/env/values
cp docs/current-state/templates/varlock.env.local.example \
  ~/.agents/env/values/.env.kriskrug-wp.local
chmod 600 ~/.agents/env/values/.env.kriskrug-wp.local
```

Store shared `WP_USER`, `WP_APP_PASSWORD`, and `NOTION_TOKEN` in
`.env.shared.local` when other repositories use the same value. Use the
repo-specific file only for overrides.

```bash
make env-check
make varlock-run CMD='make status-readonly'
```

Legacy `scripts/notion-to-wp/.env` and sibling-file fallbacks remain supported,
but process variables injected by Varlock take precedence.

## Cloud agents

Laptop value files are not copied to cloud agents automatically. Give each
remote environment only its required development values, then validate with:

```bash
varlock load --agent --show-all
varlock run --inject vars -- make status-readonly
```

Production values and live WordPress writes remain separately approved.

## Sibling repositories

Copy the contract pattern, not the values:

1. Commit a small `.env.schema` based on
   [`templates/sibling.env.schema.example`](templates/sibling.env.schema.example).
2. Import matching shared names from `.env.shared.local`.
3. Add a repo-specific override import only when needed.
4. Run secret-dependent commands through Varlock.

Do not add Varlock machinery to a repository with no secret consumers.

## Verification

- `make env-check` validates the committed schema when values are absent.
- Primary Notion and WordPress loaders prefer process-injected values.
- Legacy local files remain compatibility fallbacks.
- No secret values are committed in the contract or templates.
