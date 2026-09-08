# #996 indexing-recovery pack (prep only)

**Status:** PREP ONLY. Public read-only guards captured 2026-09-08. No live WordPress write.
**Issue:** [#996](https://github.com/WalksWithASwagger/kriskrug-wp/issues/996)
**Evidence:** [`docs/current-state/reports/issue-996-unindexed-primary-triage-20260908.md`](../../../docs/current-state/reports/issue-996-unindexed-primary-triage-20260908.md)

This folder is the exact local proposal for at most five primary URLs and at most two inbound source pages per target. Inbound sources are other members of the same five so the write set stays at five posts.

Do not deploy, PATCH, purge, request indexing, submit/remove sitemaps, or click Validate Fix from this pack. `Refs #996` only.

## Files

| File | What it is |
|---|---|
| `manifest.json` | Machine-readable identities, hashes, FIND/REPLACE, proposed fields |
| `APPLY.md` | Future snapshot-first apply + rollback (KK-gated) |
| `checklist-readback.md` | Post-approval public readback and measurement |
| `01-post-4539-photography-generative-ai.md` | Rank 1 target |
| `02-post-3082-frank-yu.md` | Rank 2 target and inbound source for 4539 |
| `03-post-4372-hartman-companions.md` | Rank 3 target and inbound source for 4539 |
| `04-post-4359-workshops-2024.md` | Rank 4 target and inbound source for 4826 |
| `05-post-4826-future-proof-community.md` | Rank 5 target and inbound source for 4359 |

## Must not

- Edit `content/drafts/339-july-publisher-batch-2026-08-16/` or any #994 / #995 / #997 / #402 / #830 / #274 / #331 proposal.
- Touch `/ai-for-creatives/` (page 12316), Second Brain (8802 / 9774 / 12327), `/events/`, About 1208.
- Duplicate the existing 3820 and 3219 footers into 4539.
- Recategorize 4372 off the early-blog footer.
- Invent GSC last-crawl or Inspection rows.

## Shared apply rules (INCIDENT-2026-05-15)

1. Snapshot first.
2. Match **ID + slug + status + modified** before every PATCH.
3. Body writes: top-level `content` only. Meta writes: allowlisted keys only.
4. FIND must match exactly once in `content.raw`.
5. One write, then readback, then the next.
6. Rollback is the snapshotted raw/meta.
