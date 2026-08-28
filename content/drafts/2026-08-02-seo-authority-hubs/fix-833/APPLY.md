# #833 APPLY: Most Benevolent Outcomes links

**Prepared, not applied. No live write has been made.** This pack needs a fresh explicit live approval before any single-item `--apply` command.

Parent: #402. This is child 8 of 9. It owns six exact links across five objects and writes content only.

## Order and boundaries

- #826 must remain live: post 3814 must be in AI Ethics category 1678 and out of category 1757. The script checks this before every live dry-run, apply, and restore.
- Apply #833 before #834. Both touch post 11700, and #834 must rebase its exact selector after #833 is verified live.
- Do not recategorize post 3814, create a spiritual hub, alter titles, schema, theme files, or the collection footer.
- Do not touch #834's glossary link on post 11700. The script preserves the existing `/glossary/` href count.
- Do not close #833, #402, or #339 when this repo-only pack merges.

## Exact write set

| Row | Object | Exact anchor | Destination |
|---:|---|---|---|
| 1 | page 3948 | `there is a prayer I actually say about this` | post 3814 |
| 2 | post 11936 | `I say a prayer about this most mornings, which is either funny or the whole point` | post 3814 |
| 3 | post 11358 | `I have my own version of the seance` | post 3814 |
| 4 | post 11700 | `the optimistic version of the same argument` | post 3814 |
| 5 | post 3814 | `the rest of my lens, written out plainly` | `/the-kk-worldview/` |
| 6 | post 3814 | `the less mystical version of this, which is how I actually practice it` | `/ai-ethics/` |

Every live object is pinned by ID, slug, status, date, title, and categories where applicable. A missing or duplicate insertion marker aborts. Existing exact anchors are skipped.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_833_mbo_links

# Offline validation. No credentials or network.
python3 scripts/apply_issue_833_mbo_links.py --from-spec

# Authenticated live GET dry-run. No snapshot and no write.
make varlock-run CMD='python3 scripts/apply_issue_833_mbo_links.py'

# Only after reviewing the dry-run and giving fresh explicit live approval.
# Apply one object at a time, then independently verify it before continuing.
make varlock-run CMD='python3 scripts/apply_issue_833_mbo_links.py --apply --item-id 3948'
```

`--apply` refuses without exactly one `--item-id`. The payload contains only `content`. Immediately before writing, the script refetches the object, revalidates its identity, and recomputes the transform. It writes a private mode-0600 snapshot, sends one content update, and checks an independent authenticated `content.raw` readback.

## Rollback

Snapshots live under `backup/issue-833-mbo-links/` and are excluded from Git.

```bash
# Dry-run the restore first.
make varlock-run CMD='python3 scripts/apply_issue_833_mbo_links.py --restore backup/issue-833-mbo-links/rest-page-3948-before-<stamp>.json'

# A restore is also a live write and needs fresh explicit live approval.
make varlock-run CMD='python3 scripts/apply_issue_833_mbo_links.py --restore backup/issue-833-mbo-links/rest-page-3948-before-<stamp>.json --apply'
```

Restore refuses snapshots outside the five-object #833 write set, revalidates the snapshot and current live identity, snapshots the current state, restores content only, and checks authenticated readback.

## After each approved apply

1. Run the same item dry-run and expect `[SKIP]`.
2. Read the target page logged out and confirm the exact anchor once.
3. Confirm the collection footer still appears once on posts.
4. On post 11700, confirm the `/glossary/` href count is unchanged. Then and only then recut #834's selector.
5. Record the snapshot path and verification result on #833. Keep it open until all five objects are live and verified.
