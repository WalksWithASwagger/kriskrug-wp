# Connector Refactor Dry-Run Proof - 2026-06-17

Scope: #197 / PR #232 zero-behavior proof for splitting `scripts/notion-to-wp/kk_notion_to_wp.py` into focused modules.

## Summary

The old connector on `origin/main` and the PR #232 connector branch produced identical dry-run output for a deterministic Notion fixture.

No WordPress write flags were used. The harness monkeypatched Notion fetches, image download, config loading, and current time so the comparison exercised the real connector orchestration and file writers without relying on live Notion auth, expiring image URLs, or production WordPress credentials.

## Live Notion Attempt

A first attempt used the known page:

```text
https://www.notion.so/35ec6f799a33809a8a6ef6507b8e7b0a
```

That run was blocked before comparison by Notion API `401 Unauthorized` with the available environment token. No WordPress request was sent.

## Fixture Proof

Worktrees compared:

- base: `origin/main` at `048adc3`
- PR: `origin/codex/swarm-active-197-36-aurora-20260617` at `41f9d8b`

Fixture Notion URL:

```text
https://www.notion.so/Fixture-1234567890abcdef1234567890abcdef
```

Compared outputs:

- stdout
- `post.html`
- `seo-meta.md`
- `alt-text.md`
- `internal-links.md`
- `post.md`
- `publish.log`
- generated image names and SHA-256 digests

Result:

```text
FIXTURE_DRY_RUN_PROOF_PASS
compared stdout, post.html, seo-meta.md, alt-text.md, internal-links.md, post.md, publish.log, images
image_count 1
image 01-fixture-connector-refactor.jpg d7455096e268f821a6efd946af6f87467bfa3f7dede99d2409137ea666d1c307
```

Only temp worktree paths were normalized before comparison. The harness froze current time, so `publish.log` and `post.md` timestamp fields were compared as stable bytes rather than ignored.

## Additional Verification

Already passing on PR #232 before this report was added:

- `make test`
- `make docs-truth-check`
- `git diff --check`
- `scripts/notion-to-wp/.venv/bin/python -m py_compile scripts/notion-to-wp/*.py`
- GitHub Actions: `validate`, `security-scan`, `notion-tests`, `docs-truth-check`, `summary`, and `Trivy`

## Safety

- No production connector `--execute`, `--publish`, `--update`, or `--diff` write path was run.
- No WordPress create/update/delete request was sent.
- No plugin deploy, cache purge, wp-admin action, private inbox read, or title overwrite occurred.
