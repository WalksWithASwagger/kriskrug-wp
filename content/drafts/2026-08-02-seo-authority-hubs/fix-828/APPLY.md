# Issue #828: negotiation checklist draft and guarded apply path

Status: **draft for Kris review; not approved for WordPress**

No live write has been made. This package replaces the dead 2007 ModelMayhem stub with a substantive checklist and prepares link-matrix rows 34 through 37. It preserves post 1210's title, slug, date, taxonomy, tags, and generated collection footer.

## Evidence and limits

- Live authenticated readback on 2026-08-28 confirmed post 1210 still has ID 1210, the expected slug, category 1756, tag 1212, and the dead `thread_id=138265` body.
- A live dry run of issue #827 confirmed its page-12013, post-1222, and post-1056 links are already exact. Their committed `after/` files are the baselines for the three new spoke sentences.
- The vanished forum thread has no Wayback copy. The draft does not pretend to reconstruct it.
- The `generate-article` skill's canonical `content/reference/kk-voice-profile.md` file is absent from this repository. The draft instead uses the live 2007 text, the current photography page, adjacent photography posts, and the repository voice gate. Kris's read is therefore mandatory.
- This is practical working guidance, not a contract template.

## Review gate

1. Kris reviews `post-body.html` for voice, lived accuracy, and any boundary he would phrase differently.
2. Apply requested revisions in a separate review commit.
3. Record the SHA-256 of the approved `post-body.html` as `reviewed_body_sha256` in `targets.json`.
4. Re-run the offline and live dry-run checks below.

Until `reviewed_body_sha256` is committed and matches the draft, `--apply` aborts before authentication or network access.

## Offline verification

```bash
python3 -m unittest scripts.tests.test_apply_issue_828_negotiation_checklist
python3 scripts/apply_issue_828_negotiation_checklist.py --from-files
python3 scripts/voice_check.py content/drafts/2026-08-02-seo-authority-hubs/fix-828/post-body.html
```

## Read-only live dry run

```bash
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py'
```

Expected: four exact identities and four plans, with no snapshots and no POST requests.

## Future application gate

A reviewed hash is necessary but not sufficient. Obtain fresh explicit live approval before any mutation. Then apply one item at a time, snapshot first, and verify authenticated readback:

```bash
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --apply --item-id 1210'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --apply --item-id 12013'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --apply --item-id 1222'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --apply --item-id 1056'
```

Stop on any identity, body, footer, style, snapshot, or readback mismatch. Do not combine this with issues #829 through #834.

## Rollback

Each write creates a private mode-0600 `context=edit` snapshot under `backup/issue-828-negotiation-checklist/`. Restore only the exact matching item after inspecting the snapshot:

```bash
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --restore backup/issue-828-negotiation-checklist/EXACT-SNAPSHOT.json'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --restore backup/issue-828-negotiation-checklist/EXACT-SNAPSHOT.json --apply'
```

The first command is a restore dry run. The second is a live restore and requires a fresh explicit live approval.
