# Cursor WordPress MCP Fix — 2026-05-24

## Problem

`wordpress-kriskrug` in `~/.cursor/mcp.json` used stale credentials. MCP adapter returned **401**; Cursor showed "Connection Failed."

## Fix

1. **`scripts/mcp-wordpress-remote.sh`** — loads `scripts/notion-to-wp/.env` and launches `@automattic/mcp-wordpress-remote`.
2. **`~/.cursor/mcp.json`** — uses the wrapper; no passwords in JSON.
3. **`scripts/wordcamp-mcp-smoke.py`** — smoke test for REST + MCP adapter.

## Verify

```bash
cd /Users/kk/Code/kriskrug-wp
python3 scripts/wordcamp-mcp-smoke.py
```

2026-05-30 closeout result: posts `200`, abilities `200`, MCP adapter `400` auth OK.

Restart **wordpress-kriskrug** in Cursor MCP settings after config changes.

## WordCamp

Demo runbook: kk-ai-ecosystem `content/people/kris-krug/website/wordcamp-mcp-demo-runbook.md`
