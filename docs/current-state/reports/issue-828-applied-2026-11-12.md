# #828 applied, 2026-11-12

**Issue:** [#828](https://github.com/WalksWithASwagger/kriskrug-wp/issues/828), child 3 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402).
**Lane:** Track A content only.
**Approval:** Kris read `fix-828/post-body.html` and replied in chat on 2026-11-12: "Approve and publish it". The approval covered this exact body replacing the 2007 stub at post 1210, plus its three inbound link updates (posts 1222, 1056 and page 12013), each write snapshot first, one at a time, with readback.
**Window:** 2026-11-13T03:10:22Z to 03:11:00Z (19:10 to 19:11 site time on 2026-11-12).
**Tooling:** Varlock-backed `scripts/apply_issue_828_negotiation_checklist.py`, one `--item-id` per write.

## Review record

- `post-body.html` SHA-256, file as stored: `ffb363eef9e4e46d8dd26d9a9e9794b71fa6dbb405a886961ac032bdfe48df98`. This is the hash posted on the issue at the 2026-08-28 review checkpoint and the body Kris read. It is recorded as `reviewed_body_sha256` in `fix-828/targets.json`.
- The tool's gate hashed the stripped body (`242974b2...`), so it refused the approved hash. It now hashes the file as stored, which is what `shasum -a 256` reports. The content sent to WordPress is unchanged.

## Preflight

- `make doctor` through Varlock: credentials resolve, Varlock, GitHub CLI, git tree and live site pass. The only failure was the worktree's missing `scripts/notion-to-wp/.venv`, which this tool does not use.
- `make status-readonly`: smoke and current-state drift checks exit 0.
- Offline: `pytest scripts/tests/test_apply_issue_828_negotiation_checklist.py` 14 passed; `--from-files` four transforms valid; `voice_check.py` 0 violations.
- Authenticated dry run: 1210, 1222 and 1056 planned. 12013 aborted on its stale needle, as expected after the #1205 redesign.
- Baseline drift, all explained: live 1210 differs from `fix-828/before/post-1210-content.raw.html` only by one trailing space; live 1222 differs from `fix-827/after/post-1222-content.raw.html` only by CRLF line endings (25 CRs); live 1056 matches `fix-827/after/post-1056-content.raw.html` exactly.
- Public preflight: 1210 carried the dead `thread_id=138265` href once; 1222, 1056 and `/photography/` had zero links to 1210; the ModelMayhem thread still returns 404.

## Applied objects

Each write sent only `content`. Hashes are SHA-256 of `content.raw`.

| ID | Slug | Raw chars | Before | After |
|---:|---|---:|---|---|
| 1210 | `checklist-of-model-photographer-negotiation-items` | 902 to 8,817 | `62dcbbde1322ae4acfd093b5d3f5746165e1f69b0d2c22f7b52c39ef18c140e9` | `0e33fa57b5e0e4238a51dd041fd4bafda9136c5d8ff758371e18f53fd630b443` |
| 1222 | `to-all-you-wannabe-fashion-photographers` | 4,621 to 4,783 | `d70335a81e1d81a856bc1bbcda2dd7b4db938186feb7820b7ecc773bbf21710a` | `afb13fe27a97da0c3204b88f2a813a3e53e360f0f7866857a734a594f0f1412f` |
| 1056 | `kk-on-modelmayhemcom` | 960 to 1,123 | `f44430694586d8c5715b5125f2c10990297fa86f12bed70035d47e96042dddda` | `b19777a1a9801010bcfa4c2dd9c08ce165a52ddf40c4cc096ad280b6a8422909` |
| 12013 | `photography` | 46,284, unchanged | `f91216481e7eec057fae6d64774690edc2a9d1528085d8666a6e3fa85b36076e` | not written |

The before hashes match the dry-run reads, so nothing changed between plan and write.

## Snapshots

Mode 0600 files in a mode 0700 folder. The apply wrote them to `backup/issue-828-negotiation-checklist/`, which the new `.gitignore` rule covers, in the agent worktree that ran it. Byte-identical copies are kept in the main checkout's ignored `.generated/current-state/issue-828-negotiation-checklist/`, which survives worktree cleanup, and the restore commands below point there. The repo is public, so the authenticated `context=edit` records are not committed.

| ID | Snapshot | File SHA-256 |
|---:|---|---|
| 1210 | `rest-post-1210-before-20261113T031022Z.json` | `e1800bdc563d8437fe9ea9a915314771bc828821d9f4bfc86a659ee629a61fd9` |
| 1222 | `rest-post-1222-before-20261113T031047Z.json` | `0d5a982685009ad1707bd9309d7e7c1ad3d05e74571dd12967bccf3bd9cd8b92` |
| 1056 | `rest-post-1056-before-20261113T031059Z.json` | `b8817b945772395723fab30bee214f1e5bbf895cbed90e58a3741d34a0cf3c8a` |

If a snapshot is lost, the committed baselines above are a second rollback source. They differ from the before state only by the whitespace noted in Preflight.

## Page 12013 skipped

The approved row-34 sentence, "The practical follow-through is the negotiation checklist I wrote in 2007 and still stand behind", was written to follow #827's line "For the fashion and model years, 2006 to 2008, start with the ModelMayhem note." The November redesign (#1205) removed that line and its archive link. Live `/photography/` equals the #1205 payload and now has no mention of ModelMayhem, models or fashion. In the redesigned coda the sentence would follow "To talk photography, get in touch." That would read as Kris's terms for anyone who books him, which he did not approve. Any other placement needs new copy. The tool was not forced, and the payload was not changed.

## Verification

- Authenticated per-item re-runs for 1210, 1222 and 1056: `[SKIP]` and `[OK] nothing pending` each. Title, slug, date, status and taxonomy read back unchanged.
- Logged-out, cache-busted checks:
  - 1210 returns 200 with title "Checklist of model-photographer negotiation items.", slug and date `2007-04-10T14:54:00` unchanged, category 1756 and tag 1212. Zero `thread_id=138265`. The lost-source note appears once, with 8 checklist sections and 1,311 rendered words. Row 37 links `/photography/`, which returns 200.
  - 1222: "the checklist version of this rant" appears once, before the collection footer, and resolves 200 to 1210's URL. #827's "how I found those people in the first place" link is kept.
  - 1056: "the one useful thing I posted over there" appears once, before the footer, and resolves 200 to 1210's URL. #827's "where all of that ended up" link and the ModelMayhem member-profile link are kept.
  - `/photography/` has zero links to 1210 (skipped).
- Plain cached URLs return the same results. 1210 was a Jetpack Boost cache hit already serving the new body, so no cache purge was needed.
- All three restore commands were run without `--apply` and each printed the exact approved ID and snapshot path. No rollback was applied.

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --restore .generated/current-state/issue-828-negotiation-checklist/rest-post-1210-before-20261113T031022Z.json'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --restore .generated/current-state/issue-828-negotiation-checklist/rest-post-1222-before-20261113T031047Z.json'
make varlock-run CMD='python3 scripts/apply_issue_828_negotiation_checklist.py --restore .generated/current-state/issue-828-negotiation-checklist/rest-post-1056-before-20261113T031059Z.json'
```

Each is a dry run. Add `--apply` to one command only with Kris's explicit rollback approval, after reconfirming the ID and slug.

## Scope boundary

Titles, slugs, dates, status, excerpts, taxonomy, featured media, SEO meta, schema, theme, page 12013 and #827's rows 11 to 14 were not written. Parent #402 was already closed on 2026-10-26.

## Open for Kris

1. Row 34 on `/photography/`: restore #827's coda line and add row 34 after it, approve new wording for the coda, or drop row 34. This decision is tracked in the November roadmap's "Decisions waiting on Kris" table, so #828 can close without losing it.
2. #827 rows 11 and 12 (the category-archive link and the 1056 fashion-years link) are no longer on live `/photography/` since the redesign. #827 is closed, so nothing tracks that loss.
3. Post 1210's Jetpack SEO description still quotes the 2007 stub. Refreshing it would be a separate approved write.
