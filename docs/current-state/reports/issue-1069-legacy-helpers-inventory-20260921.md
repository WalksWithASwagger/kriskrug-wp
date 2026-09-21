# #1069 inventory — unreferenced legacy helpers and superseded mobile QA plan

**Status:** evidence pack only. **No deletes, no moves, no Makefile wiring, no
live WordPress, no outbound HTTP from the listed tools.**
**Issue:** [#1069](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1069)
**Measured:** 2026-09-21 against `origin/main` `a333fe8`
**Lane:** Track A docs. Wave 5 leftover `verify-with-human` rows C12–C15, C18,
and D19 from [`docs/audits/stale-2026-09-21.md`](../../audits/stale-2026-09-21.md).

#1069 forbids deleting, moving, executing against production, or modifying any
listed artifact. This report names a recommended retain / archive / retire
disposition. It does not carry it out. KK approval is required before any
later archive, retire, or authenticated run.

Parent scouts: Wave 1 [`stale-2026-09-21.md`](../../audits/stale-2026-09-21.md),
Wave 3 [`stale-2026-09-22.md`](../../audits/stale-2026-09-22.md), Wave 5
[`stale-2026-09-23.md`](../../audits/stale-2026-09-23.md). Wave 5 left these
six paths on purpose until a human named them. This pack is that naming
evidence, not the cleanup.

---

## 0. Method and boundary

Source inspection plus existing receipts only.

1. Read each listed file and its nearest test, fix packet, or successor
   receipt.
2. `rg -n` for every basename (`category_coverage_audit`,
   `export_press_kit_brand`, `update_wp_draft_categories`, `verify_wp_draft`,
   `body_h1_migration`, `AURORA-MOBILE-QA-127`), excluding `backup/` and
   `.git/`.
3. Confirmed none of the six are Makefile targets.
4. Confirmed `#127` is closed and its 2026-08-16 receipt supersedes the old
   plan. Confirmed `#353` is closed after a recorded 2026-07-24 apply.
5. Did **not** execute any listed script, hit `kriskrug.co`, write WordPress,
   or remove/move any listed path.

Wave 1 called C12, C13, and C15 “zero references” and C18 “only cited from
the fix packet.” That was incomplete. The correction is in §2.

---

## 1. Summary

| ID | Path | Class | Tests | Makefile | Successor / receipt | Recommended disposition | KK needed |
|---|---|---|---|---|---|---|---|
| C12 | `scripts/category_coverage_audit.py` | Read-only public REST GET | 3 offline unit tests | no | none | **Retain** unused auditor | To retire only |
| C13 | `scripts/export_press_kit_brand.py` | Local file writer (no WP) | 6 offline unit tests | no | `#879` / PR `#890`; committed `press-kit/brand-reference.{json,md}` | **Retain** local regenerator | To retire, or to refresh the committed brand files |
| C14 | `scripts/update_wp_draft_categories.py` | Authenticated WP writer (`--apply`) | none | no | landed in `#579` | **Retain** as unused recovery helper | To retire **or** to `--apply` |
| C15 | `scripts/verify_wp_draft.py` | Authenticated WP reader (GET only) | none | no | theme comment in `inc/seo-meta-rest.php` (`#661`) | **Retain** as unused recovery helper | To retire; running it is still an authenticated live read |
| C18 | `scripts/body_h1_migration.py` | Authenticated reader + guarded writer | 16 + 2 writer-safety tests | no | `#353` closed; apply receipt `content/drafts/2026-07-24-issue-353-apply.json` | **Retain** spent apply helper (same shape as C01–C08) | To archive or to replay any target |
| D19 | `docs/current-state/AURORA-MOBILE-QA-127.md` | Superseded test plan | n/a | n/a | `#127` closed; [`issue-127-mobile-qa-2026-08-16.md`](issue-127-mobile-qa-2026-08-16.md) | **Archive** (move, do not delete) after KK | To move off the current-state top level |

No listed artifact has a zero-importer **and** issue-authorized delete. C14 is
the only Python helper with no importer and no test, and #1069 still forbids
removal.

---

## 2. Wave 1 scout correction

Wave 1 mapped basenames against Makefile / docs / tests / other scripts and
missed dedicated unit tests that `make test` already discovers under
`scripts/tests/`.

| ID | Wave 1 claim | Current evidence |
|---|---|---|
| C12 | “Zero references in Makefile, docs, tests, or other scripts.” | `scripts/tests/test_category_coverage_audit.py` imports it (3 tests). Still no Makefile target and no runbook. |
| C13 | “Zero references.” | `scripts/tests/test_export_press_kit_brand.py` imports it (6 tests). Committed outputs exist. Still no Makefile target. |
| C14 | “Zero references.” | Still true outside the three stale-scout files. |
| C15 | “Zero references.” | Incomplete: `theme/kk-aurora/inc/seo-meta-rest.php` names `verify_wp_draft.py` as a REST consumer. Still no Python importer and no test. |
| C18 | “Only cited from `fixes/issue-353-body-h1-migration-2026-07-13.md`.” | Also imported by `test_issue_353_body_h1_migration.py` (16 tests) and `test_writer_safety_contract.py` (2 body-H1 cases). Live apply receipt exists. |
| D19 | Bannered superseded, still top-level. | Still accurate. `#127` is now closed; the 2026-08-16 receipt is the live pass. |

---

## 3. Artifact cards

### C12 — `scripts/category_coverage_audit.py`

| Field | Evidence |
|---|---|
| Introduced | `05b66eb` (2026-06-11) “feat: add category coverage audit and events spike” |
| Lines | 313 |
| Executable? | Yes. CLI. Default `--base-url https://kriskrug.co`, `--limit` ≥ 100. |
| Write capability | **None.** Docstring and human report both say public REST GET only (`/wp-json/wp/v2/posts`, `/wp-json/wp/v2/categories`). Uses `urllib`, no credentials. |
| Current references | `scripts/tests/test_category_coverage_audit.py`; Wave 1/3/5 scout IDs. No docs runbook. |
| Test coverage | Offline fixture tests for Misc callout, empty categories, and missing `categories` fields. Does **not** mock `urlopen`; executing `main()` would be outbound. |
| Successor / receipt | None. |
| Disposition | **Retain.** Reusable read-only auditor with tests. Not current-path. |
| KK | Not needed to keep. Needed to retire. Do not run it from a docs session (public outbound). |

### C13 — `scripts/export_press_kit_brand.py`

| Field | Evidence |
|---|---|
| Introduced | `428a819` (2026-08-23) `content(#879): export Aurora press kit brand reference (#890)` |
| Lines | 652 |
| Executable? | Yes. Default writes two tracked files. `--check` is local compare-only. |
| Write capability | **Local files only**, not WordPress. Writes `content/source-packs/content-architecture-2026/press-kit/brand-reference.json` and `.md`. Reads `theme.json`, `02-tokens.css`, `style.css`. |
| Current references | `scripts/tests/test_export_press_kit_brand.py`. Press-kit payload tests read the **committed JSON**, not this module. `RELEASE-CHECKLIST.md` does not name the exporter. |
| Test coverage | 6 tests: semantic aliases, stable role order, provenance tokens, committed-source provenance, neon-value omission, `--check` drift. |
| Successor / receipt | `#879` / PR `#890`. Outputs generated `2026-08-23T01:14:33Z` from KK Aurora **1.6.9**. Repo `theme/kk-aurora/style.css` is now **1.6.12** (local header only; not a live readback). The committed export is therefore repo-stale. `--check` was not run. |
| Disposition | **Retain.** This is how the committed brand files get regenerated. Unwired, but not orphaned. |
| KK | Needed to retire, or to refresh the tracked brand files (local write, press-kit copy lane). Default mode must not be run casually. `--check` is safe locally and was not run here. |

### C14 — `scripts/update_wp_draft_categories.py`

| Field | Evidence |
|---|---|
| Introduced | `68a98a1` (2026-07-31) `content: archive Kris media appearances and stage article (#579)` |
| Lines | 92 |
| Executable? | Yes. Hard-exits if `WP_USER`/`WP_API_USERNAME` + app password are unresolved. |
| Write capability | **Authenticated writer.** Fetches `context=edit`, aborts unless status is `draft` and slug/title match, then `POST /wp-json/wp/v2/posts/{id}` with `{"categories": [...]}` only when `--apply` is passed. Default is dry-run after the authenticated GET. |
| Current references | Wave 1/3/5 scout IDs only. No test. No docs runbook. No other script imports it. `scripts/notion-to-wp/prepare_review_draft.py` has a different function named `update_wp_draft`. |
| Test coverage | None. |
| Successor / receipt | One-shot helper from the `#579` media-appearances / Both Hands staging commit. No dedicated receipt names this file. |
| Disposition | **Retain** as unused recovery helper. Closest thing to an orphan, and still not delete-eligible under #1069. |
| KK | Required to retire **or** to `--apply`. Do not execute. |

### C15 — `scripts/verify_wp_draft.py`

| Field | Evidence |
|---|---|
| Introduced | Same `#579` commit as C14 (`68a98a1`, 2026-07-31) |
| Lines | 95 |
| Executable? | Yes. Same credential hard-exit as C14. |
| Write capability | **None.** Authenticated `GET` `context=edit` only. Compares id / draft status / slug / title / content SHA-256 / featured-media unset, plus optional YouTube, list, block, category, and Jetpack SEO meta checks. Exit 0 if all pass, 2 if any fail. |
| Current references | Wave scouts; `theme/kk-aurora/inc/seo-meta-rest.php` lines 13–14 (theme restores REST registration of `jetpack_seo_html_title` and `advanced_seo_description` so the connector **and** this script can read/write those keys). The script itself never writes. |
| Test coverage | None. |
| Successor / receipt | `#661` theme REST comment. No dedicated verify receipt. |
| Disposition | **Retain** as unused recovery helper. The theme comment is a real inbound, not a runbook. |
| KK | Needed to retire. Running it is an authenticated live read (not a write) and is still out of scope here. |

### C18 — `scripts/body_h1_migration.py`

| Field | Evidence |
|---|---|
| Introduced | `9642056` (2026-07-13) `seo: add guarded body H1 migration` (PR `#354`) |
| Lines | 449 |
| Executable? | Yes. Default command is `audit` (authenticated full inventory). `plan` is read-only. `apply` requires `--target-id` plus exact `APPLY-ISSUE-353-TARGET-<id>` and writes one `content` POST after a mode-0600 snapshot. |
| Write capability | **Guarded authenticated writer** on `apply` only. Uses `common.WPClient`. Manifest: `fixes/issue-353-body-h1-migration-2026-07-13.json`. |
| Current references | Fix packet `fixes/issue-353-body-h1-migration-2026-07-13.md`; two test modules; Wave scouts. |
| Test coverage | 16 tests in `test_issue_353_body_h1_migration.py` (scope lock, homepage exclusion, Gutenberg/classic rewrite, drift abort, confirmation interlock, snapshot-before-write, content allowlist, failed readback, default audit). 2 additional cases in `test_writer_safety_contract.py`. |
| Successor / receipt | `#353` **closed** 2026-07-24 (`completed`) after owner comment: all 14 body-H1→H2 targets applied; homepage `3930` untouched; snapshots under `/private/tmp/kk-353-snapshots/`; receipt `content/drafts/2026-07-24-issue-353-apply.json` (14 `ok: true` rows, zero remaining body H1s on readback). Earlier public re-probe [`issue-353-public-h1-reprobe-20260716.md`](issue-353-public-h1-reprobe-20260716.md) is pre-apply. Manifest status text is still `repo-only-migration-packet` and is now historical relative to that apply comment. |
| Disposition | **Retain** in place as a spent apply helper, same ruling Wave 1 gave C01–C08: keep restore tests until KK says archive. Preferred later action is `scripts/archive/` plus a “spent; rollback only” banner — not delete, not replay. |
| KK | Required to archive or to run `audit` / `plan` / `apply` against production. This session did not. |

### D19 — `docs/current-state/AURORA-MOBILE-QA-127.md`

| Field | Evidence |
|---|---|
| Introduced | `211cc67` (2026-06-06) with the `#127` plan. Bannered superseded in `d4fae4f` (2026-08-16, PR `#804`). |
| Lines | 49 |
| Executable? | No. Historical checklist. First lines already say **STATUS: Superseded (2026-08-16)** and point at the live pass. Breakpoints and “≤700px” notes are pre-`#479` / pre-Revive. |
| Write capability | None. |
| Current references | Front-door one-shot table in [`docs/current-state/README.md`](../README.md); successor receipt; retired `#740` archive proposal (then claimed `#127` was still open — that sentence is stale); Wave 1/3/5. |
| Test coverage | n/a |
| Successor / receipt | [`issue-127-mobile-qa-2026-08-16.md`](issue-127-mobile-qa-2026-08-16.md). `#127` **closed** 2026-08-17 (`completed`) by PR `#804`. Original AC reproduced as pass on live Aurora 1.6.5. |
| Disposition | **Archive** (git mv into `docs/current-state/archive/` or leave a stub that points at the receipt) after KK. Do not delete. A move must retarget the README one-shot row in the same PR. Not this PR. |
| KK | Required to move it off the current-state top level. |

---

## 4. Read-only vs writer (do not blur)

| Path | Auth? | Network if executed | Mutates |
|---|---|---|---|
| C12 category coverage | No | Public GET to `--base-url` | No |
| C13 press-kit export `--check` | No | No | No |
| C13 press-kit export default | No | No | Tracked brand-reference files |
| C14 draft categories (default) | Yes | Authenticated GET | No |
| C14 draft categories `--apply` | Yes | Authenticated GET + POST | Draft `categories` only, after slug/title/status guards |
| C15 verify draft | Yes | Authenticated GET | No |
| C18 body H1 `audit` / `plan` | Yes | Authenticated GET | No |
| C18 body H1 `apply` | Yes | Authenticated GET + content POST | One reviewed published post/page body |
| D19 mobile QA plan | n/a | n/a | n/a |

Writers that can touch WordPress: **C14 `--apply`** and **C18 `apply`**. Both
need KK. C13 default is a local tracked-file writer and also needs an
intentional lane if anyone regenerates the brand files.

---

## 5. Verification required by #1069

- `#127` is **closed** (`completed`, 2026-08-17). Closing PR:
  [#804](https://github.com/WalksWithASwagger/kriskrug-wp/pull/804). The
  2026-08-16 receipt is the successor; the old plan is already bannered.
- `#353` is **closed** (`completed`, 2026-07-24) after the recorded 14-target
  apply. Tooling stays for rollback/audit, not as an open migration queue.
- No production access, no listed-artifact removal or move, no untracked
  cleanup, no `kriskrug.co` fetch, no script execution.
- `rg -n` unique files (excluding `backup/` / `.git/`), 2026-09-21:

  | Pattern | Files |
  |---|---|
  | `category_coverage_audit` | 3 stale scouts + `scripts/tests/test_category_coverage_audit.py` |
  | `export_press_kit_brand` | 3 stale scouts + `scripts/tests/test_export_press_kit_brand.py` |
  | `update_wp_draft_categories` | 3 stale scouts only |
  | `verify_wp_draft` | 3 stale scouts + `theme/kk-aurora/inc/seo-meta-rest.php` |
  | `body_h1_migration` | 3 stale scouts + fix packet + 2 test modules |
  | `AURORA-MOBILE-QA-127` | 3 stale scouts + current-state README + `#740` proposal + `#127` receipt |

---

## 6. What this pack does not decide

- Whether C01–C08, C10, C11, or C20 should archive. Out of scope.
- Whether C14/C15 should later grow tests or a one-line runbook. Out of scope.
- Whether to refresh C13’s 1.6.9 brand-reference files to repo 1.6.12. That
  is a separate local-write lane after KK.
- Whether `#353` routes still render one H1 on live. The apply receipt says
  they did on 2026-07-24; this session did not re-probe.

---

## 7. Recommended next human actions (not this PR)

1. Keep all six paths where they are until KK names one.
2. If KK wants less top-level noise: archive D19 and retarget the README
   one-shot row in the same docs PR.
3. If KK wants fewer unused scripts: archive C18 next to C01–C08 (spent
   apply + tests). Leave C12/C13 (tested, reusable). Leave C14/C15 until
   KK explicitly retires the `#579` recovery pair.
4. Do not delete any of them on a “zero Makefile target” rule. Wave 1 already
   under-counted importers.

**Created for:** #1069. Stop at the PR boundary.
