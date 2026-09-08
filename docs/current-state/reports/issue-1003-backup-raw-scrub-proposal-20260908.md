# #1003 backup/ + raw/ public-capture scrub proposal

**Status:** proposal only. **No `git rm --cached`, no deletes, no history rewrite, no force-push, no `git filter-repo`.**
**Issue:** [#1003](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1003)
**Measured:** 2026-09-08 against `origin/main` `7b68b28`
**Lane:** Track A docs. Inventory + keep-vs-untrack packet. No live WordPress, header, or XML-RPC changes.

Related lanes that this packet does **not** expand: [#767](https://github.com/WalksWithASwagger/kriskrug-wp/issues/767) (user-enum apply), [#1002](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1002) (XML-RPC prep), [#1001](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1001) (#709 runbook). The broader `backup/**/*.html` + leftover PNG cached-rm allow-list already lives on [#737](https://github.com/WalksWithASwagger/kriskrug-wp/issues/737) / [`issue-737-backup-tree-archive-proposal-20260816.md`](issue-737-backup-tree-archive-proposal-20260816.md) and is still waiting on a KK reply.

---

## 0. Secret-scan result (values never printed)

Scanned every tracked text file under `backup/` and `docs/current-state/raw/` for pattern **types** only.

| Pattern type | Hits in these two trees |
|---|---|
| `.env` / `WP_APP_PASSWORD` / `NOTION_TOKEN` assignments | none |
| `sk_live` / `sk_test` | none |
| PEM private key / certificate | none |
| `Authorization: Basic` / `Bearer` | none |
| `wordpress_logged_in_` / `wordpress_sec_` cookies | none |
| Filled `pwd` / `user_pass` value on the login capture | none (empty form fields) |
| WP REST `password` key on `*.rest-edit.json` / `*.edit.json` | present as an empty string on 10 of 11 files; missing on the template record |

No suspected secret **value** was found. This packet does **not** trip the stop-and-escalate rule. Residual risk is **identity / authenticated-context HTML and JSON**, not a committed credential dump.

False-positive notes (names only, not values):

- `docs/current-state/raw/wp-json-root.json` lists the public REST route catalog, including route **names** under `application-passwords`. That is a method/route index, not a password.
- `docs/current-state/raw/posts-headers.txt` advertises the header **name** `X-WP-Nonce` in `access-control-expose-headers`. No nonce value is stored.
- `backup/20260903T174920Z-767-331-snippets/snippets-after.json` mentions the header name `X-WP-Nonce` inside snippet source. That directory is #767 rollback evidence; leave it on that lane.

---

## 1. Current tracked counts (`origin/main` `7b68b28`)

| Tree | Files | Bytes | MiB |
|---|---:|---:|---:|
| `backup/` | 477 | 19,087,407 | 18.20 |
| `docs/current-state/raw/` | 46 | 3,880,077 | 3.70 |

`backup/` grew from the 2026-08-16 #737 snapshot (403 files / 14.72 MiB) by later content-architecture and hub-apply rollback JSON. HTML count is now **133** (was 129). PNG count is still **2**.

`docs/current-state/raw/` has **no** `.gitignore` rules today. After any future `git rm --cached`, those paths can be re-added with a plain `git add`.

---

## 2. Inventory — login / admin / edit-context / env-adjacent

Path + reason only. No secret values, no usernames, no slugs. Where a user record is implied, labels match the #767 redaction convention (`author-A` = public author id 1; `host-admin` = host-provisioned administrator id 18).

### 2.1 Priority A — treat as scrub candidates (~580 KiB, 14 files)

These are the files that look like login, admin, edit-context, or user-enum captures.

| Path | Reason |
|---|---|
| `docs/current-state/raw/login-page.html` | Public `wp-login.php` HTML capture: `loginform`, empty `log` / `pwd` fields, Jetpack SSO chrome. No filled password. Still a login-surface dump in a public repo. |
| `docs/current-state/raw/aurora-audit-2026-05-23/admin-readiness.txt` | Authenticated admin-readiness probe: capability flags, administrator role, and `host-admin` identity (id 18). Do not reprint the slug. |
| `docs/current-state/raw/users.json` | Unauthenticated REST `/wp/v2/users` dump (2 records: `author-A` and `host-admin`). Same disclosure #767 already tracks on the live site. Inventory only; do not expand #767 here. |
| `backup/20260525-201025Z/page-snapshots/about.rest-edit.json` | Authenticated WP REST `context=edit` page payload (`permalink_template` + `generated_slug` present). |
| `backup/20260525-201025Z/page-snapshots/blog.rest-edit.json` | Same edit-context page payload. |
| `backup/20260525-201025Z/page-snapshots/publications.rest-edit.json` | Same edit-context page payload. |
| `backup/20260525-201025Z/page-snapshots/services.rest-edit.json` | Same edit-context page payload. |
| `backup/20260525-201025Z/page-snapshots/speaking.rest-edit.json` | Same edit-context page payload. |
| `backup/20260525-201025Z/page-snapshots/work.rest-edit.json` | Same edit-context page payload. |
| `backup/20260525-220404Z/page-snapshots/events.rest-edit.json` | Same edit-context page payload. |
| `backup/20260624-181106Z-issue233-companions/post-11882.edit.json` | Authenticated edit-context **draft** post payload. |
| `backup/20260624-181106Z-issue233-companions/post-11929.edit.json` | Authenticated edit-context **draft** post payload. |
| `backup/20260624-181106Z-issue233-companions/post-11936.edit.json` | Authenticated edit-context published-post payload. |
| `backup/20260817T045123Z-front-page-template-12661/template-edit.json` | Authenticated `wp_template` edit record (front-page template). |

### 2.2 Priority B — already on the #737 HTML/PNG allow-list (do not re-own)

`backup/**/*.html` (133 files, 6.55 MiB) and the two leftover Aurora 1.4.0 home PNGs are public page / screenshot captures. They are **not** login or admin surfaces. #737 already proposed `git rm --cached` for that exact class and is still waiting on KK. This issue does not replace that allow-list.

| Path glob | Count | Reason this issue leaves them on #737 |
|---|---:|---|
| `backup/**/*.html` | 133 | Public/marketing page snapshots. New adds already ignored (`backup/**/*.html`). |
| `backup/aurora-deploy-20260724/screenshots/aurora-140-home-1440.png` | 1 | Public homepage screenshot. New adds already ignored. |
| `backup/aurora-deploy-20260724/screenshots/aurora-140-home-375.png` | 1 | Public homepage screenshot. New adds already ignored. |

### 2.3 Inspected and not Priority A

| Path | Why it is not a login/admin/edit-context capture |
|---|---|
| `docs/current-state/raw/pages/*.html` (16 files) + `homepage.html` + `404-page.html` | Public rendered pages. Not wp-login, not wp-admin, not `context=edit`. Optional later hygiene, not this packet's allow-list. |
| `docs/current-state/raw/wp-json-root.json` | Public REST index (route **names** only). |
| `docs/current-state/raw/{categories,tags,taxonomies,types,pages,posts-page1,posts-page2}.json` | Public REST catalog captures. |
| `docs/current-state/raw/*.{xml,txt}` except `admin-readiness.txt` | Public sitemaps, robots, `llms.txt`, unauthenticated header **names**. |
| `docs/current-state/raw/aurora-audit-2026-05-23/public-smoke.{txt,json}` | Public smoke, not admin. |
| `backup/20260623-163028Z/homepage.headers` and raw `*-headers.txt` | Gateway/cache header **names** only. No `Set-Cookie` auth cookies. |
| `backup/20260903T174920Z-767-331-snippets/*` | #767 / #331 snippet rollback JSON. Leave on #767. |
| `backup/issue-829-ai-ethics-hub/` | **Not tracked.** `.gitignore` already denies the whole directory. |
| Remaining `backup/**/*.json` / `*.md` / `*.txt` / `*.diff` | Deploy handoffs, checksums, public REST readbacks, rollback manifests. Same keep-set as #737 §3. |

---

## 3. Recommended keep vs `git rm --cached`

Execute **only** after KK approval. Archive-copy first if KK wants a local rollback of the untracked blobs. Files stay on disk when using `--cached`.

### 3.1 This issue's proposed cached-rm allow-list (14 files)

The 14 Priority A paths in §2.1. After that PR: those paths leave the index; they remain in git **history** until a separate, KK-opened history-rewrite issue.

### 3.2 Keep tracked (this issue)

Everything else under the two trees, including:

- All `backup/**/*.md`, checksum `.txt`, public REST / rollback `.json` that is not in §2.1
- Public `docs/current-state/raw/` catalogs, sitemaps, and marketing HTML
- #767 snippet rollback directory (not this lane)

### 3.3 Do not do in the follow-up cached-rm PR

- `git rm` (working-tree delete) of local rollback evidence
- History rewrite / `git filter-repo` / force-push
- Live WordPress, header, or XML-RPC changes
- Rotating credentials (no secret **value** was found; rotation is not justified by this scan)
- Executing the #737 HTML/PNG allow-list (still #737's KK reply)

---

## 4. History note (required)

`git rm --cached` only drops a path from the **current tree**. Blobs remain reachable from earlier commits on `main` and in every existing clone/fork.

A history purge (`git filter-repo`, BFG, force-push of rewritten `main`) is **out of scope** unless KK explicitly opens a separate needs-human issue. That rewrite would need a backup, a coordinated force-push exemption, and a credential-rotation decision if any later scan found a real secret. This scan did not.

Until that separate issue exists, treat cached-rm as "stop cloning the files onto new checkouts," not as "the files are gone."

---

## 5. Ignore rules — confirm re-add prevention

Probes on 2026-09-08 (`git check-ignore -v` / `git check-ignore -v --no-index`):

| Probe path | Result |
|---|---|
| `backup/test.html` | ignored — `.gitignore:121` `backup/**/*.html` |
| `backup/foo.png` / `.jpg` / `.jpeg` | ignored — `.gitignore:102-104` |
| `backup/issue-829-ai-ethics-hub/x.json` | ignored — `.gitignore:125` |
| `docs/current-state/reports/foo.html` | ignored — `.gitignore:82` |
| `docs/current-state/reports/screenshots/x.png` | ignored — `.gitignore:80` |
| already-tracked `backup/**/*.html` and the two PNGs | rule still matches (`--no-index`); they stay in the index until an approved cached-rm |
| `docs/current-state/raw/login-page.html` | **not ignored** |
| `docs/current-state/raw/newpage.html` | **not ignored** |
| `docs/current-state/raw/users.json` | **not ignored** |
| `docs/current-state/raw/aurora-audit-2026-05-23/admin-readiness.txt` | **not ignored** |
| `backup/new.rest-edit.json` | **not ignored** (JSON-keep decision from #737 still stands for *new* rollback JSON; edit-context filenames are a subset) |

**Gap:** `.gitignore` already blocks new `backup/` HTML/PNG spill (#737 / #829). It does **not** block re-adding `docs/current-state/raw/**` HTML or the admin/user captures. Propose a follow-up ignore add (KK-approved, same PR as the cached-rm or a tiny sibling) along the lines of:

```gitignore
# #1003: raw login/admin captures stay local after cached-rm
docs/current-state/raw/login-page.html
docs/current-state/raw/users.json
docs/current-state/raw/aurora-audit-2026-05-23/admin-readiness.txt
docs/current-state/raw/**/*.html
```

Do not add a blanket `backup/**/*.json` ignore. #737 already recorded why: rollback/readback JSON is the audit trail, and `make backup-check` does not consume it.

---

## 6. Out-of-git archive (if KK wants a local copy before cached-rm)

Workspace policy: non-git recovery material lives under `/Users/kk/Code/_archive/<repo>/`.

**Destination:** `/Users/kk/Code/_archive/kriskrug-wp/issue-1003-priority-a-2026-09-08/`

Suggested copy of the 14-file allow-list only (run from a clean `main` checkout on KK's laptop):

```bash
mkdir -p /Users/kk/Code/_archive/kriskrug-wp/issue-1003-priority-a-2026-09-08
printf '%s\n' \
  docs/current-state/raw/login-page.html \
  docs/current-state/raw/aurora-audit-2026-05-23/admin-readiness.txt \
  docs/current-state/raw/users.json \
  backup/20260525-201025Z/page-snapshots/about.rest-edit.json \
  backup/20260525-201025Z/page-snapshots/blog.rest-edit.json \
  backup/20260525-201025Z/page-snapshots/publications.rest-edit.json \
  backup/20260525-201025Z/page-snapshots/services.rest-edit.json \
  backup/20260525-201025Z/page-snapshots/speaking.rest-edit.json \
  backup/20260525-201025Z/page-snapshots/work.rest-edit.json \
  backup/20260525-220404Z/page-snapshots/events.rest-edit.json \
  backup/20260624-181106Z-issue233-companions/post-11882.edit.json \
  backup/20260624-181106Z-issue233-companions/post-11929.edit.json \
  backup/20260624-181106Z-issue233-companions/post-11936.edit.json \
  backup/20260817T045123Z-front-page-template-12661/template-edit.json \
  | rsync -a --files-from=- /Users/kk/Code/kriskrug-wp/ \
      /Users/kk/Code/_archive/kriskrug-wp/issue-1003-priority-a-2026-09-08/
```

---

## 7. KK reply template

```text
#1003 approve shape: git rm --cached the 14 Priority A paths only
Allow-list = §3.1 / §2.1 in
docs/current-state/reports/issue-1003-backup-raw-scrub-proposal-20260908.md
Also add the four raw/ ignore lines in §5.
Archive copy to /Users/kk/Code/_archive/kriskrug-wp/issue-1003-priority-a-2026-09-08/
before the cached-rm PR.
No filter-repo / force-push. No #737 HTML/PNG execution. No #767/#1001/#1002 work.
```

Until that reply lands, this issue can close on the inventory + proposal alone. The cached-rm is a separate, approval-gated PR.

---

## 8. What this PR did / did not do

**Did:** committed this proposal. Confirmed ignore probes. Recorded path + reason for every login/admin/edit-context candidate.

**Did not:** untrack files, rewrite history, print secret or username values, touch live WordPress, expand #767 / #1001 / #1002, or execute #737.
