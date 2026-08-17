# Issue #767 apply-ready reconfirm — 2026-08-17

**Issue:** [#767](https://github.com/WalksWithASwagger/kriskrug-wp/issues/767) (`[SECURITY] Two WordPress usernames publicly enumerable via REST, sitemap, and ?author probes; no HSTS`)
**Lane:** Gate 1 E of [`WORK-PLAN-2026-08-17.md`](../WORK-PLAN-2026-08-17.md). Docs only.
**Status:** **Still apply-ready. Still not authorized to enable.** No live WordPress write, no snippet POST/PATCH, no mu-plugin drop, no Pagely/HSTS change.
**Predecessor:** [`user-enumeration-767-2026-08-16.md`](user-enumeration-767-2026-08-16.md) (PR #793 merged the drafts; this pass reconfirms they are still the right apply).
**Captured:** 2026-08-17 06:29 UTC, unauthenticated and logged out, GET/HEAD only.
**Stack at capture:** WordPress **7.0.4**. Public `style.css` Version **1.6.8**, same as repo `theme/kk-aurora/style.css`. Theme drift is out of scope here.

Usernames are redacted. Live identifiers are written as `author-A` (public author, user id 1, slug-length 2) and `host-admin` (host-provisioned administrator, user id 18, slug-length 11).

**KK ruling 2026-08-17:** **KEEP host-admin id 18.** Do not delete, rename, or demote that account as part of this issue. Closing the three public paths is the remaining apply; account existence is decided.

---

## 1. Headline

The three public enumeration paths are **still live**. The two `fixes/issue-767-*.php` drafts still exist, still lint, and still match the intended filters. They are **not** live. HSTS is still absent and still owned by #709.

This packet does not enable anything.

---

## 2. Logged-out confirmation (2026-08-17)

Every row is a logged-out `curl` / urllib GET or HEAD from this session. Response bodies and `Location` URLs were inspected only to classify status, counts, field names, and whether a path contained `/author/`. Identifiers below are labels and slug-lengths, not the live strings.

Compared with the 2026-08-16 diagnosis: **no change** on any of the four surfaces.

### 2.1 `GET /wp-json/wp/v2/users` — still public

| Signal | Result |
|---|---|
| HTTP status | `200` |
| `x-wp-total` | `2` |
| JSON shape | array, length 2 |
| `roles` present | **no** |
| `capabilities` present | **no** |
| `email` present | **no** |
| Keys on each item | `id`, `name`, `url`, `description`, `link`, `slug`, `avatar_urls`, `meta`, `_links` |
| `strict-transport-security` | absent |

| Account | id | label | slug-length | display-name-length | `link` is `/author/…` |
|---|---:|---|---:|---:|---|
| Public author | 1 | `author-A` | 2 | 9 | yes |
| Host-provisioned admin | 18 | `host-admin` | 11 | 4 | yes |

Single-user reads are also still public: `GET /wp-json/wp/v2/users/1` and `GET /wp-json/wp/v2/users/18` both returned `200` with the same public key set and no `roles` / `capabilities` / `email`.

### 2.2 `/wp-sitemap.xml` — still lists a users sitemap

| Signal | Result |
|---|---|
| HTTP status | `200` |
| Index `<loc>` count | 5 |
| Users child present | **yes** (`wp-sitemap-users-1.xml`) |
| `users` substring count in the index | 1 |

Child filenames (no author slugs): `wp-sitemap-posts-post-1.xml`, `wp-sitemap-posts-page-1.xml`, `wp-sitemap-taxonomies-category-1.xml`, `wp-sitemap-taxonomies-post_tag-1.xml`, `wp-sitemap-users-1.xml`.

`GET /wp-sitemap-users-1.xml` returned `200` with 2 `<loc>` entries, both under `/author/`:

| label | slug-length |
|---|---:|
| `author-A` | 2 |
| `host-admin` | 11 |

`fixes/issue-331-archive-sitemap-policy.php` is still **not live**. Sitemap AC of #767 remains the deploy half of #331.

### 2.3 `GET /?author=1` and `/?author=18` — still 301 to `/author/`

| Probe | Status | `Location` contains `/author/` |
|---|---|---|
| `/?author=1` | `301` | **yes** |
| `/?author=18` | `301` | **yes** |

The username was not printed. `strict-transport-security` was absent on both probe responses.

### 2.4 `HEAD https://kriskrug.co/` — HSTS still 0

| Probe | Status | `strict-transport-security` count |
|---|---|---:|
| `https://kriskrug.co/` | `200` | **0** |

HSTS remains #709. This issue does not ship headers.

### 2.5 Repeatable check script (desired post-apply state)

`scripts/check_user_enumeration.sh` against live, 2026-08-17 06:29 UTC:

```
FAIL  REST /wp-json/wp/v2/users  (status=200 x-wp-total=2 json=array array_length=2; expected 401/403/404 or empty list, no x-wp-total>0)
FAIL  sitemap /wp-sitemap.xml  (status=200 users_substring_count=1; expected 200 and 0)
FAIL  author /?author=1  (status=301 location_contains_/author/=yes; expected no /author/ in Location)
FAIL  HSTS homepage  (status=200 strict-transport-security_count=0; expected >=1; owned by #709)

Summary: 0 PASS / 4 FAIL (desired post-apply state for #767)
```

Four FAILs is the expected pre-apply baseline. The script prints PASS/FAIL only; no usernames, slugs, or Location URLs.

### 2.6 What was not probed

- No `xmlrpc.php` method call, no `system.multicall`, no POST to xmlrpc.
- No login attempt, no password spray, no Application Password test.
- No Code Snippets write, no user/role edit, no Pagely panel change.
- No REST POST/PATCH/PUT/DELETE.

---

## 3. Drafts still exist and still match the intended filters

Both files are on `main` from PR #793 (`a9c56c1`). `php -l` on PHP 8.3.6 this session: no syntax errors.

| Path | Intended filter | Still present | Live? |
|---|---|---|---|
| `fixes/issue-767-hide-rest-users.php` | Unauthenticated GET/HEAD `/wp/v2/users` (collection and single-user) returns 401. Authenticated traffic left to core. | `add_filter('rest_pre_dispatch', 'kk_767_restrict_unauthenticated_users_rest', 10, 3)`. GET/HEAD only. `is_user_logged_in()` bypass. Does **not** unset `rest_endpoints` (that would race REST auth and break the editor). | **No.** Logged-out GET is still 200 with a 2-user array. |
| `fixes/issue-767-disable-author-probes.php` | `/?author=N` no longer 301s to `/author/<slug>/`. Pretty archives stay on #331. | `add_filter('redirect_canonical', …)` returns false for `$_GET['author']`. `add_action('template_redirect', …, 0)` 404s the query-string probe. `KK_767_DISABLE_AUTHOR_ARCHIVES` remains optional and off. | **No.** Both probes still 301 with `/author/` in Location. |
| `fixes/issue-331-archive-sitemap-policy.php` | Drop the users sitemap provider (and, as written, category/tag sitemaps). | Unchanged. Sitemap AC of #767 is still this file's deploy, not a third policy. | **No.** Index still lists `wp-sitemap-users-1.xml`. |

Issue #767 AC also named `rest_endpoints` as an option. The draft correctly uses `rest_pre_dispatch` instead: the file header documents that unsetting the route from `rest_endpoints` based on `is_user_logged_in()` runs before REST authentication and would 404 the block editor. That is still the right apply. Do not rewrite it to `rest_endpoints`.

Public smoke this session still lists Site Kit `1.185.0` on `/`. After any future KK-approved enable: editor author dropdown, Site Kit dashboard, authenticated GET `/wp-json/wp/v2/users` still 200, logged-out GET 401 and not a user array. If editor or Site Kit breaks, deactivate the REST snippet immediately.

---

## 4. What is still owed (not done here)

| #767 AC | This pass |
|---|---|
| Decision recorded on the host-provisioned admin account | **KEEP id 18** (KK 2026-08-17). Do not delete/rename/demote in this lane. |
| `/wp-json/wp/v2/users` no longer public | Draft still apply-ready. **Not applied.** |
| Author sitemap suppressed (deploy half of #331) | Still listed. Still #331's snippet. **Not deployed.** |
| `/?author=N` no longer redirects to a username-bearing URL | Draft still apply-ready. **Not applied.** |
| HSTS shipped per #709 | Re-confirmed count **0**. Still #709. Do not ship headers here. |
| Logged-out verification of all four surfaces with dates | This file, 2026-08-17 06:29 UTC. |
| Repeatable check script | Still `scripts/check_user_enumeration.sh`. Four FAILs as expected. |

Remaining KK apply decisions (unchanged from 2026-08-16 section 6, except item 1 is now ruled):

1. ~~Host-admin account~~ **KEEP id 18.**
2. **Sitemap apply:** full existing #331 snippet, wait for #331's remaining SEO AC, or a users-provider-only extract as a later #331 revision. Not a silent extract in this lane.
3. **Author archives:** query-string 404 only (recommended; compatible with #331 keep-reachable), or also 404 pretty `/author/<slug>/` (`KK_767_DISABLE_AUTHOR_ARCHIVES` — that *is* a #331 expansion and needs an explicit yes).
4. **HSTS** stays on #709.

No live change ships until KK authorizes the snippet enable (REST first, then author-probe, sitemap only as a #331 apply). Gate 1 of the 2026-08-17 work plan does **not** authorize that enable.

---

## 5. Proposed apply order (still KK-gated; not performed)

Same as the 2026-08-16 packet. Snapshot first.

1. Authenticated Code Snippets snapshot to a gitignored path. Restore source if a snippet misbehaves.
2. REST users restriction (`fixes/issue-767-hide-rest-users.php`). Run everywhere (or front-end/REST), not admin-only.
3. Logged-in editor + Site Kit check before the next surface.
4. Author-query probe (`fixes/issue-767-disable-author-probes.php`) at the default (query-string 404 only), unless KK chooses the stricter pretty-archive 404. Purge Pagely page cache after activate.
5. Sitemap: deploy `fixes/issue-331-archive-sitemap-policy.php` only as a #331 apply. Purge cache; confirm `/wp-sitemap.xml` has no `users` child and that post/page children remain.
6. HSTS: follow #709. Do not apply from this issue.
7. Re-run `scripts/check_user_enumeration.sh`. After steps 2–5, expect REST / sitemap / author PASS and HSTS FAIL until #709 ships.

Rollback: deactivate the snippet(s). Author-probe and sitemap need a Pagely page-cache purge. Host-admin id 18 is not a snippet and is not in scope to change.

---

## 6. Verification method

Unauthenticated GET/HEAD against production during the capture window, plus `php -l` on the two #767 PHP drafts and `make docs-truth-check` on the docs tree. `make status-readonly` this session: WordPress 7.0.4, Aurora live and repo **1.6.8**. No credentials were used. No request body was sent. No `POST` / `PUT` / `PATCH` / `DELETE` was issued. No xmlrpc method was called. No snippet was read or written live. No user, role, or host setting was changed.
