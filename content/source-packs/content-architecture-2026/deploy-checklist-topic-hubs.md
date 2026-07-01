# Deploy Checklist - Topic Hubs Wave

## Preflight

- Confirm the branch is `codex/content-architecture-topic-hubs`.
- Confirm the Trust + Offers source pack is present in this branch.
- Confirm live CSS reports Aurora `1.3.27` and `--aurora-readable-measure`.
- Confirm unrelated performance, robots, sitemap, or cleanup artifacts remain unstaged.
- Run payload tests and the topic-hub deploy dry run before any live write.

## Target Pages

| Payload | Page ID | Slug | URL |
|---|---:|---|---|
| `vancouver-ai.html` | 12315 | `vancouver-ai` | `/vancouver-ai/` |
| `ai-for-creatives.html` | 12316 | `ai-for-creatives` | `/ai-for-creatives/` |
| `ai-events.html` | 12317 | `ai-events` | `/ai-events/` |
| `ai-ethics.html` | 12318 | `ai-ethics` | `/ai-ethics/` |
| `ai-tools.html` | 12321 | `ai-tools` | `/ai-tools/` |
| `ai-for-journalists.html` | 12320 | `ai-for-journalists` | `/ai-for-journalists/` |
| `ai-conversations.html` | 12319 | `ai-conversations` | `/ai-conversations/` |
| `indigenous-ai.html` | 12322 | `indigenous-ai` | `/indigenous-ai/` |

## Commands

```bash
python3 -m unittest scripts.tests.test_content_architecture_payloads
python3 scripts/content_architecture_deploy.py \
  --map content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/page-map.json
```

Live write command:

```bash
python3 scripts/content_architecture_deploy.py \
  --map content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/page-map.json \
  --execute
```

## Readback Gate

For each page:

1. Verify ID, slug, and `publish` status.
2. Snapshot authenticated edit JSON and public HTML immediately before write.
3. Write only the body payload with `{"content": "<payload>"}`.
4. Re-read authenticated raw content and public HTML.
5. Stop and restore that page if markers are missing, a body H1 appears, retired classes remain, or public HTML does not include the marker.

## Rollback

Use the generated snapshot directory from the live deploy report:

```bash
python3 scripts/content_architecture_deploy.py \
  --map content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/page-map.json \
  --restore \
  --snapshot-dir backup/<timestamp>-content-architecture/page-snapshots \
  --page vancouver_ai
```

Repeat `--page` for any affected key from the topic-hub `page-map.json`.
