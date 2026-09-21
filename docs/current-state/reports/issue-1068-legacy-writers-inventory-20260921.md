# Issue #1068: legacy WordPress writers — rollback-only inventory

**Issue:** [#1068](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1068)
**Date:** 2026-09-21
**Mode:** docs only. No deletes, no archives, no renames, no live WordPress
writes, no outbound HTTP, no secrets.
**Cross-check:** [`docs/audits/stale-2026-09-23.md`](../../audits/stale-2026-09-23.md)
(Wave 5 / #1063). Prior IDs from Wave 1 [`stale-2026-09-21.md`](../../audits/stale-2026-09-21.md)
and Wave 3 [`stale-2026-09-22.md`](../../audits/stale-2026-09-22.md).
**Closed-issue evidence:** local front-door docs and dated apply receipts only.
This file does not query GitHub or `kriskrug.co`.

Wave 5 left C01–C08, C10, C11, and C20 as `verify-with-human`: closed-issue
writers still include restore paths or can operate against production. This
report is the evidence packet for a later explicit KK disposition. It does
**not** authorize a file move, deletion, or replay.

A closed issue is not proof that its helper is safe to remove.

---

## Verdict

| Wave ID | Script | Closed issue | Disposition | KK before any move/delete |
|---|---|---|---|---|
| C01 | `scripts/apply_issue_829_ai_ethics_hub.py` | #829 | **archive** | **required** |
| C02 | `scripts/apply_issue_830_cyber_love_garden.py` | #830 | **archive** | **required** |
| C03 | `scripts/apply_issue_831_matt_mckenna.py` | #831 | **archive** | **required** |
| C04 | `scripts/apply_issue_832_events_routing.py` | #832 | **archive** | **required** |
| C05 | `scripts/apply_issue_833_mbo_links.py` | #833 | **archive** | **required** |
| C06 | `scripts/apply_issue_826_taxonomy.py` | #826 | **archive** | **required** |
| C07 | `scripts/apply_issue_827_photography_hub.py` | #827 | **archive** | **required** |
| C08 | `scripts/apply_issue_764_fix.py` | #764 | **archive** | **required** |
| C10 | `scripts/deploy_events_page.py` | none (page 2250 / #635 lane) | **retain** | **required** |
| C11 | `scripts/og_snippet_deploy.py` | retired snippet 12 | **retain** | **required** |
| C20 | `scripts/add_sky_smoked_back_work_card.py` | #1042 | **archive** | **required** |

**None of these eleven are `retire`.** Retire would mean delete. Wave 1 already
said not to delete C01–C08 on sight: each has `--restore` and a unit test.
C20 is the same shape. C10 is still the snapshot-first writer for published
`/events/`. C11 is the only in-repo deactivate switch for retired Code
Snippet 12. Zero-importer proof does not exist for any of them.

Preferred archive shape, if KK later says yes: `git mv` into
`scripts/archive/` plus a “spent; rollback only” banner, and keep the matching
`scripts/tests/test_*.py` import path working. That is a future lane, not this
PR. [`scripts/archive/README.md`](../../../scripts/archive/README.md) is the
convention for spent one-shot publishers.

C09 (`scripts/merge-swarm-safe-prs.sh`) is the Wave 5 `delete` leftover. It is
not in the #1068 list and is not inventoried here.

---

## Method

1. Re-read Wave 5 remainder rows C01–C08, C10, C11, C20. Confirmed each path
   still exists under `scripts/`.
2. Source-inspected all eleven files for write flags, restore behavior,
   identity gates, and credential prompts.
3. Ran `--help` only on the ten argparse helpers. That path exits in
   `parse_args()` before `auth_header()` / `WPClient.from_env()`.
4. Did **not** run `scripts/og_snippet_deploy.py --help`. `sys.argv` length 2
   is a live command: it sets `WP_AUTH_MODE=login` and calls
   `WPClient.from_env`. Source inspection is the credential-free check.
5. Cross-checked each closed-issue helper against its APPLY.md / receipt and
   the 2026-09-09 runbook. No helper was executed with credentials. No
   network mutation.

`git diff --check` is the eval for this docs PR.

---

## Shared facts (C01–C08)

These eight are one-shot Track A apply helpers. None is a Makefile target.
Default is dry-run. `--apply` is the write switch. `--restore PATH` previews
a snapshot restore and writes only with `--apply`. Live paths call
`auth_header()` (Varlock `WP_API_*` or `WP_USER` / `WP_APP_PASSWORD`) and
POST `https://kriskrug.co/wp-json/wp/v2/...`. Snapshots land under
`backup/issue-*-*/` (mode 0600, gitignored). `--from-files` / `--from-spec`
(where present) stay on disk.

`--allow-before-826` on C01–C04 and C07 bypasses the child-1 gate. Help text
says do not use it on production.

Wave 1 preferred action after KK confirms no replay: `scripts/archive/` plus
a rollback-only banner. That confirmation has not been given.

---

## C01 — `scripts/apply_issue_829_ai_ethics_hub.py`

| Field | Evidence |
|---|---|
| Wave ID | C01 (`stale-2026-09-21.md` §2.1; still open on Wave 5) |
| Closed issue | [#829](https://github.com/WalksWithASwagger/kriskrug-wp/issues/829). 2026-09-09 runbook: closed; You Can't Drink Data is live on `/ai-ethics/` |
| Apply receipt | [`issue-829-applied-20260829.md`](issue-829-applied-20260829.md). KK `approved proceed`. Four content-only writes 2026-08-29T20:23Z–20:24Z. Pack [`fix-829/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-829/APPLY.md): “Applied and verified 2026-08-29” |
| Write capability | Authenticated POST `content` on page 12318 and posts 12030, 6144, 11882. ID→slug gate, #826 category proof, text-match insert, fresh `context=edit` snapshot. `--item-id` limits to one object |
| Restore | `--restore` allowlists those four IDs, validates snapshot identity, dry-runs unless `--apply`, then snapshots live and POSTs snapshot `content.raw` |
| Tests / references | `scripts/tests/test_apply_issue_829_ai_ethics_hub.py` (rewrite, `--from-files`, dry-run, slug abort, #826 gate, snapshot-then-content POST, APPLY.md banner). APPLY.md still lists apply and restore commands. No Makefile |
| Disposition | **archive** after KK. Keep tests. Do not retire: restore is the documented rollback for the 2026-08-29 snapshots |
| KK approval | **Required** before any `git mv` or delete |

---

## C02 — `scripts/apply_issue_830_cyber_love_garden.py`

| Field | Evidence |
|---|---|
| Wave ID | C02 |
| Closed issue | #830. Runbook: closed; Cyber Love Garden is on `/ai-for-creatives/` |
| Apply receipt | No dated `reports/issue-830-applied-*.md`. Closeout is [`fix-830/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-830/APPLY.md) (“Applied and closed”; `--apply` is rollback-only now) plus the 2026-09-09 runbook. Wave 2b/4b banners and C19 tests lock that string |
| Write capability | Content POST on page 12316 and posts 2819, 2661, 3567. Does not PATCH destination 2650. Aborts unless #826’s 2819 `kriskrug.co/contact` href is live |
| Restore | Same allowlisted `--restore` / `--apply` pattern as C01. Snapshot dir `backup/issue-830-cyber-love-garden/` |
| Tests / references | `scripts/tests/test_apply_issue_830_cyber_love_garden.py` (including `test_apply_md_records_applied_and_closed`). APPLY.md restore commands. No Makefile |
| Disposition | **archive** after KK. Missing dedicated receipt is not a delete signal |
| KK approval | **Required** |

---

## C03 — `scripts/apply_issue_831_matt_mckenna.py`

| Field | Evidence |
|---|---|
| Wave ID | C03 |
| Closed issue | #831. Runbook: closed; Matt McKenna is on `/ai-conversations/` |
| Apply receipt | No dated `reports/issue-831-applied-*.md`. [`fix-831/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-831/APPLY.md): “Applied and closed” |
| Write capability | Content POST on page 12319 and posts 2833, 2423. #826 category gate. Does not recategorize 3330 |
| Restore | Allowlisted `--restore` / `--apply`. Dir `backup/issue-831-matt-mckenna/` |
| Tests / references | `scripts/tests/test_apply_issue_831_matt_mckenna.py`. APPLY.md. No Makefile |
| Disposition | **archive** after KK |
| KK approval | **Required** |

---

## C04 — `scripts/apply_issue_832_events_routing.py`

| Field | Evidence |
|---|---|
| Wave ID | C04 |
| Closed issue | #832. APPLY.md: closed 2026-09-03. Runbook: meetup recaps route to `/events/` |
| Apply receipt | No dated `reports/issue-832-applied-*.md`. [`fix-832/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-832/APPLY.md): “Applied and closed”. [`issue-995-events-search-intent-20260908.md`](issue-995-events-search-intent-20260908.md) repeats the 2026-09-03 close |
| Write capability | Content POST on seven recap posts plus page 12315. **Hard-refuses page 2250** on targets, `--item-id`, `--restore`, snapshot/write URLs, and any `/pages/2250` POST. #635 owns `/events/` |
| Restore | Allowlisted `--restore`; `refuse_write_id(2250)` first. Test `test_restore_refuses_page_2250` |
| Tests / references | `scripts/tests/test_apply_issue_832_events_routing.py`. APPLY.md. No Makefile |
| Disposition | **archive** after KK. Page-2250 refusal is a keep-the-script reason until C10’s retain decision is explicit, not a delete reason |
| KK approval | **Required** |

---

## C05 — `scripts/apply_issue_833_mbo_links.py`

| Field | Evidence |
|---|---|
| Wave ID | C05 |
| Closed issue | #833. Runbook: closed; Most Benevolent Outcomes links are live |
| Apply receipt | No dated `reports/issue-833-applied-*.md`. [`fix-833/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-833/APPLY.md): “Applied and closed” |
| Write capability | Content POST on page 3948 and posts 11936, 11358, 11700, 3814 (six exact anchors). `--apply` requires one `--item-id`. #826 category proof on 3814 before dry-run, apply, and restore. Shares post 11700 with open #834 |
| Restore | `--restore` dry-runs unless `--apply`; writes a pre-restore snapshot; readback must match snapshot `content.raw` |
| Tests / references | `scripts/tests/test_apply_issue_833_mbo_links.py` (asserts `--restore` remains in APPLY.md). No Makefile |
| Disposition | **archive** after KK. Do not retire while #834 may still need a 11700 rollback that this helper can preview |
| KK approval | **Required** |

---

## C06 — `scripts/apply_issue_826_taxonomy.py`

| Field | Evidence |
|---|---|
| Wave ID | C06 |
| Closed issue | #826. Runbook / front door: taxonomy apply is live |
| Apply receipt | [`issue-826-applied-20260818.md`](issue-826-applied-20260818.md). KK “proceed”. Stamp `20260818T021548Z`. Six `[SKIP]` on re-run. Pack [`fix-826/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-826/APPLY.md). Pre-apply receipt [`issue-826-apply-ready-20260817.md`](issue-826-apply-ready-20260817.md) is dated “not applied” and is not current |
| Write capability | Authenticated POST of `categories` and/or `content` on posts 3814, 3330, 1067, 1063, 1147, 2819. 3330 is category-only. 2819 is the contact-href repair later children must not regress |
| Restore | `--restore` POSTs snapshot **categories and content** (wider than the content-only hub helpers) |
| Tests / references | `scripts/tests/test_apply_issue_826_taxonomy.py`. Later hub helpers GET these posts as a live gate. No Makefile |
| Disposition | **archive** after KK. Do not retire first among C01–C08: C01–C05 and C07 still encode #826 as a write gate |
| KK approval | **Required** |

---

## C07 — `scripts/apply_issue_827_photography_hub.py`

| Field | Evidence |
|---|---|
| Wave ID | C07 |
| Closed issue | #827 |
| Apply receipt | [`issue-827-applied-20260818.md`](issue-827-applied-20260818.md). After live #826. Stamp `20260818T021841Z`. Pack [`fix-827/APPLY.md`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-827/APPLY.md) |
| Write capability | Content POST on page 12013 and posts 1222, 1056. Refuses unless the five #826 category fixes are live. Does not recategorize 1067 / 1063 / 1147 |
| Restore | Content-only allowlisted `--restore` / `--apply`. Dir `backup/issue-827-photography-hub/` |
| Tests / references | `scripts/tests/test_apply_issue_827_photography_hub.py` (`test_apply_md_records_the_live_write_and_keeps_restore`). Receipt notes #480 photography.html would collide if replayed |
| Disposition | **archive** after KK |
| KK approval | **Required** |

---

## C08 — `scripts/apply_issue_764_fix.py`

| Field | Evidence |
|---|---|
| Wave ID | C08 |
| Closed issue | #764 |
| Apply receipt | [`gate0-content-apply-20260817.md`](gate0-content-apply-20260817.md) §#764. Posts 12327 (em dashes) and 12032 (`?p=11876` → storyhive permalink). Snapshots `backup/issue-764-em-dash-404/rest-post-{12032,12327}-before-20260817T050342Z.json`. [`fix-764/APPLY.md`](../../../content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764/APPLY.md) and Wave 4b-bannered [`fix-764/README.md`](../../../content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/README.md) |
| Write capability | Content POST on allowlisted IDs 12327 and 12032 only. Slug match, baseline SHA-256, fresh snapshot, independent `context=edit` GET |
| Restore | Hash-strict: snapshot body must equal the approved **baseline** hash; live body must equal baseline (already restored) or payload hash. Refuses live drift. Takes a mode-0600 before-restore snapshot |
| Tests / references | `scripts/tests/test_apply_issue_764_fix.py` — the strongest restore suite in this set (allowlist, slug, hash drift, pre-restore snapshot, readback). No Makefile |
| Disposition | **archive** after KK. Do not retire: restore is the Gate 0 rollback printed in the receipt |
| KK approval | **Required** |

---

## C10 — `scripts/deploy_events_page.py`

| Field | Evidence |
|---|---|
| Wave ID | C10 (Wave 1 §2.2 “orphaned or one-shot”; still `verify-with-human` on Wave 5) |
| Closed issue | None. Writes published page 2250 (`/events/`). #635 exclusivity still holds in events docs: only that lane may mutate the catalog, event media, or page 2250 body. #832 hard-refuses this ID |
| Apply receipt | No closeout that retires this writer. [`scripts/events_page/README.md`](../../../scripts/events_page/README.md) still generates `out/events-2250.generated.html` and says apply-to-live is a separate approval. It does not name this filename. Wave 1 “zero references outside its own file” is still true for the basename |
| Write capability | `WPClient.from_env()` after argparse. Default: identity check + snapshot under `backup/page-snapshots/`, no POST. `--execute` POSTs artifact `content` only (not title, slug, status, template, featured media, meta). Readback mismatch auto-POSTs the pre-write body |
| Restore | **`--restore` writes immediately.** There is no `--execute` gate on restore. Snapshot `id` must be 2250 |
| Tests / references | No `scripts/tests/test_deploy_events_page.py`. Renderer tests cover HTML generation, not this deploy client. `--help` is credential-free |
| Disposition | **retain.** This is the snapshot-first live writer for an active generated page, not a spent hub apply. Archiving it would hide the only dedicated page-2250 POST helper. Do not treat “unreferenced basename” as spent |
| KK approval | **Required** before any move or delete. A later README citation would be a docs lane, not a delete |

---

## C11 — `scripts/og_snippet_deploy.py`

| Field | Evidence |
|---|---|
| Wave ID | C11 |
| Closed issue | Temporary OG bridge for Aurora 1.3.37. [`fixes/README.md`](../../../fixes/README.md) Table A: snippet **12**, name `Open Graph + Twitter Card meta (social link previews)`, **inactive**; theme is the current provider. Diagnosis [`og-restore-snippet-diagnosis-20260815.md`](og-restore-snippet-diagnosis-20260815.md). #995 receipts: snippet 12 must stay inactive |
| Apply receipt | 2026-08-15 diagnosis + fixes table. Not a content-apply helper |
| Write capability | `create` POSTs a new Code Snippet (`active=false`). `activate` / `deactivate` PATCH or POST `/activate` `/deactivate`. `status` is GET-only. No argparse. Commands other than the usage string call `WPClient.from_env` |
| Restore | **No snippet-state restore.** `write_snapshot` dumps the inventory to `/private/tmp/kriskrug-code-snippets-<stamp>.json` (0600) before create. There is no `--restore` |
| Tests / references | `scripts/tests/test_machine_local_defaults.py` only asserts `ENV_PATH` is repo-relative. Not a current runbook. `--help` is **unsafe** (see Method) |
| Disposition | **retain.** It is the only in-repo deactivate switch if snippet 12 is ever turned back on. `create` / `activate` would regress theme OG and must not be run. Archive only after KK names a replacement deactivate path |
| KK approval | **Required**. Do not retire on “snippet already inactive” |

---

## C20 — `scripts/add_sky_smoked_back_work_card.py`

| Field | Evidence |
|---|---|
| Wave ID | C20 (Wave 3 new; still open on Wave 5) |
| Closed issue | [#1042](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1042) |
| Apply receipt | [`sky-smoked-back-work-card-apply-20260920.md`](sky-smoked-back-work-card-apply-20260920.md). Page 2672 (`work`) 2026-09-20T18:05:25Z. Snapshot `backup/20260920T180523Z-sky-smoked-back-work-card/` |
| Write capability | Content POST inserting one project card before Photography. Identity gate id/slug/status/title. Dry-run default. `--apply` re-GETs, aborts on hash drift, snapshots, writes, authenticated + public cache-bypass verify. Idempotent no-op if the card is already present |
| Restore | `--restore` prints a diff and writes only with `--apply`. Snapshot must be page 2672 / slug `work`. Writes a before-restore snapshot. Receipt prints the exact restore command |
| Tests / references | `scripts/tests/test_add_sky_smoked_back_work_card.py` (insert, idempotent, apply snapshot; no dedicated restore-write test). Receipt only. No Makefile |
| Disposition | **archive** after KK. Same shape as C01–C08. Do not retire: restore is the receipt’s rollback |
| KK approval | **Required** |

---

## Inspection vs `--help`

| Script | `--help` | Why |
|---|---|---|
| C01–C08, C10, C20 | Ran. Argparse exits before auth or HTTP | Credential-free |
| C11 | **Not run** | `python3 scripts/og_snippet_deploy.py --help` is argv length 2, so `main()` calls `WPClient.from_env` |

No helper was invoked with `--apply`, `--execute`, `--restore`, `create`,
`activate`, or `deactivate`.

---

## Wave 5 status cross-check

Wave 5 remainder still matches disk:

| Wave 5 row | This inventory |
|---|---|
| C01–C08 `verify-with-human` | Confirmed. Recommend **archive**, not delete |
| C10 `verify-with-human` | Confirmed. Recommend **retain** (active page-2250 writer) |
| C11 `verify-with-human` | Confirmed. Recommend **retain** (deactivate switch) |
| C20 `verify-with-human` | Confirmed. Recommend **archive**, not delete |
| “C01–C08 and C20 still have `--restore` plus unit tests; do not delete on sight” | Still true |
| Suggested Wave 6 “after KK confirms rollback-only” | This report is that confirmation packet. KK has not confirmed |

C12–C15, C18, D19, and C09 stay out of scope, as Wave 5 instructed.

---

## What this PR did not do

- Move, rename, banner, or delete any writer or test
- Run a helper with credentials or against WordPress
- Close #1068 from chat (the PR `Closes` line is the close path)
- Replay #826–#833, #764, or #1042
- Touch C09 or the still-human p2 scripts
- Add this file to `docs/INDEX.md` (second-file change; same restraint Wave 5 used)

---

## Next human decision (not this lane)

1. KK: archive C01–C08 and C20 into `scripts/archive/` with rollback-only
   banners, or leave them in `scripts/` as named restore CLIs.
2. KK: keep C10 as the page-2250 deploy entry, or name a replacement and
   then reconsider archive.
3. KK: keep C11 for emergency deactivate of snippet 12, or name another
   path and then reconsider archive.
4. Do not start a delete lane from this file. Zero-importer proof is absent.
