# User enumeration diagnosis — kriskrug.co (#767)

**Issue:** #767 (`[SECURITY] Two WordPress usernames publicly enumerable via REST, sitemap, and ?author probes; no HSTS`)
**Status:** PREP ONLY. Diagnosis plus apply-ready drafts. No live WordPress write, no snippet enable, no Pagely/HSTS change.
**Captured:** 2026-08-16 20:58–21:00 UTC, unauthenticated and logged out, GET/HEAD only.
**Related:** #709 (headers; HSTS remains there), #331 (archive sitemap policy; sitemap AC of #767 is the deploy half of that issue), `docs/current-state/reports/security-headers-audit-2026-08-15.md` section 8.1.
**Stack at capture:** WordPress 7.0.4. Public `style.css` readback and repo `main` were drifted at this session's `make status-readonly` (live 1.6.5 / repo 1.6.6). Theme drift is out of scope here.

Usernames are redacted in this file. Live identifiers are written as `author-A` (public author, user id 1, slug-length 2) and `host-admin` (host-provisioned administrator, user id 18, slug-length 11). Those three public paths were confirmed to exist; the live username strings are not repeated here.

---

## 1. Headline

Three independent public paths still enumerate WordPress accounts. Combined with a reachable `wp-login.php` and no HSTS, that is the valid-username half of a credential-stuffing pair. Roles, capabilities, and email fields are **not** in the unauthenticated REST payload. The leak is identifiers and author-archive URLs, not privilege maps.

Nothing in this packet was applied.

---

## 2. Logged-out confirmation (2026-08-16)

Every row is a logged-out `curl` from this session. Response bodies and `Location` URLs were inspected only to classify status, counts, field names, and whether a path contained `/author/`. Identifiers below are labels and slug-lengths, not the live strings.

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

Single-user reads are also public: `GET /wp-json/wp/v2/users/1` and `GET /wp-json/wp/v2/users/18` both returned `200` with the same public key set and no `roles` / `capabilities`.

### 2.2 `/wp-sitemap.xml` — still links a users sitemap

| Signal | Result |
|---|---|
| HTTP status | `200` |
| Index `<loc>` count | 5 |
| Users child present | **yes** (`wp-sitemap-users-1.xml`) |
| `users` substring count in the index | 1 |

`GET /wp-sitemap-users-1.xml` returned `200` with 2 `<loc>` entries, both under `/author/`:

| label | slug-length |
|---|---:|
| `author-A` | 2 |
| `host-admin` | 11 |

This matches the 2026-08-15 #741 / #709 readback: `fixes/issue-331-archive-sitemap-policy.php` is **not live**.

### 2.3 `GET /?author=1` — still 301s to an author archive

| Probe | Status | `Location` contains `/author/` | Redirect target |
|---|---|---|---|
| `/?author=1` | `301` | **yes** | `author-A`, slug-length 2 |
| `/?author=18` (supporting; not required by the AC) | `301` | **yes** | `host-admin`, slug-length 11 |

`strict-transport-security` was absent on the author-probe response.

### 2.4 `strict-transport-security` — still absent

| Probe | Status | HSTS header count |
|---|---|---:|
| `https://kriskrug.co/` | `200` | 0 |
| `http://kriskrug.co/` | `301` | 0 |

HSTS is owned by #709. This issue only re-confirms the gap so the four-surface check script has a current baseline.

### 2.5 What was not probed

- No `xmlrpc.php` method call, no `system.multicall`, no POST to xmlrpc. Reachability alone was recorded in the #709 report; whether to disable it is a KK decision on that issue.
- No login attempt, no password spray, no Application Password test.
- No Code Snippets write, no user/role edit, no Pagely panel change.

---

## 3. Surfaces and what already exists

| Surface | Live today | Repo draft | Notes |
|---|---|---|---|
| REST `/wp/v2/users` | Public list of 2 | **New:** `fixes/issue-767-hide-rest-users.php` | Restricts unauthenticated GET/HEAD. Leaves authenticated editor / Site Kit traffic to core. |
| Users sitemap | Linked from the core index | **Existing, not live:** `fixes/issue-331-archive-sitemap-policy.php` | #767's sitemap acceptance criterion **is the deploy half of #331**. This packet does not invent a third archive policy and does not add a users-only sitemap fork. |
| `/?author=N` | 301 to `/author/<slug>/` | **New:** `fixes/issue-767-disable-author-probes.php` | Default 404s the query-string probe only. Pretty `/author/<slug>/` archives stay on #331's "keep reachable + noindex" decision. |
| HSTS | Absent | #709 packet | Out of scope to apply or redesign here. |

#331's snippet also excludes category and tag sitemaps and emits `noindex,follow` on those archives. Deploying it is a larger SEO change than "hide the users child sitemap." KK already has that decision on #331; #767 must not silently expand or replace it.

---

## 4. Proposed apply order (KK-gated; not performed)

Do not start this list until KK answers section 6. Snapshot first.

1. **Authenticated Code Snippets snapshot** to a gitignored path (same shape as the #706 runbook). Restore source if a snippet misbehaves.
2. **REST users restriction first** (`fixes/issue-767-hide-rest-users.php`). Highest stuffing-value close, lowest SEO blast. Configure the snippet to run everywhere (or front-end/REST), not admin-only.
3. **Logged-in editor + Site Kit check** before touching the next surface: author dropdown on Posts → Add New still populated; Site Kit dashboard still loads; authenticated `GET /wp-json/wp/v2/users` still 200; logged-out GET is 401 and not a user array. If the editor or Site Kit breaks, deactivate the REST snippet and stop.
4. **Author-query probe** (`fixes/issue-767-disable-author-probes.php`) at the default (query-string 404 only), unless KK chooses the stricter pretty-archive 404. Purge Pagely page cache after activate — author 301s can be cached.
5. **Sitemap:** deploy the existing `fixes/issue-331-archive-sitemap-policy.php` only if KK treats that as the #331 apply (full archive policy). If KK wants users-sitemap-only and wants to keep category/tag sitemaps for now, that is a #331 decision, not a silent extract in this lane. Purge cache; confirm `/wp-sitemap.xml` has no `users` child and that post/page children remain.
6. **HSTS:** do not apply from this issue. Follow #709's phase-1 `max-age=86400` plan on the surface KK picks there.
7. **Re-run** `scripts/check_user_enumeration.sh`. After steps 2–5, expect REST / sitemap / author PASS and HSTS FAIL until #709 ships.

---

## 5. Rollback

| Change | Rollback |
|---|---|
| REST users snippet | Deactivate it. Re-run the check script. No page-cache purge required for REST unless a cache is later observed on `/wp-json/`. |
| Author-probe snippet | Deactivate it, purge Pagely page cache, re-run the check script. Pretty author archives should match pre-change 200s. |
| #331 sitemap snippet | Deactivate it, purge cache, confirm the users (and, if the full snippet was live, taxonomy) children return. Follow the rollback gate already written in `docs/current-state/reports/issue-331-archive-policy-20260712.md`. |
| HSTS | #709 rollback only. Do not raise `max-age` or add `preload` from this issue. |
| Host-admin account | Not a snippet. Any rename / demote / removal needs its own KK plan and is not started here. |

---

## 6. What KK needs to rule on

1. **Host-provisioned admin account** (user id 18, label `host-admin`, slug-length 11): still needed for host support, or removable / renamed / demoted? **This packet does not answer that.** Closing the three public paths reduces disclosure; it does not decide whether the account should exist. Record the decision on #767 before calling the issue done.
2. **Sitemap apply:** deploy the full existing #331 snippet, wait for #331's remaining SEO acceptance criteria (GSC evidence, retained-category fork), or approve a users-provider-only extract as a later #331 revision? #767's sitemap AC is the deploy half of #331, not a new policy.
3. **Author archives:** query-string 404 only (recommended here; compatible with #331 "keep archives accessible"), or also 404 pretty `/author/<slug>/` (stricter; set `KK_767_DISABLE_AUTHOR_ARCHIVES` — that *is* a #331 expansion and needs an explicit yes)?
4. **HSTS** stays on #709. Do not treat a green #767 check as including transport pinning until that issue ships.

No live change ships until 1–3 are answered. Item 4 is informational.

---

## 7. Repo artifacts in this packet

| Path | Role |
|---|---|
| `fixes/issue-767-hide-rest-users.php` | Apply-ready REST restriction. Inactive. |
| `fixes/issue-767-disable-author-probes.php` | Apply-ready `/?author=N` 404. Inactive. |
| `fixes/issue-331-archive-sitemap-policy.php` | Already in-repo; still the sitemap implementation. Not live. Unchanged in this packet except a ledger pointer. |
| `scripts/check_user_enumeration.sh` | Repeatable logged-out assert of the four #767 curls. Prints PASS/FAIL only. |
| `fixes/README.md` | Table A rows for the two new drafts; #331 row notes the #767 deploy-half relationship. |

The check script asserts the **desired** post-apply state. On this capture window it is expected to print four FAILs.

---

## 8. Acceptance criteria vs this packet

| #767 AC | This packet |
|---|---|
| Decision recorded on the host-provisioned admin account | **Question written** (section 6.1). Not answered. |
| `/wp-json/wp/v2/users` no longer public | Snippet drafted. Not applied. Site Kit / editor verify steps are in the file header. |
| Author sitemap suppressed (deploy half of #331) | Confirmed still live; pointed at the existing #331 snippet. Not deployed. |
| `/?author=N` no longer redirects to a username-bearing URL | Snippet drafted. Not applied. |
| HSTS shipped per #709 | Re-confirmed absent. Still #709. |
| Logged-out verification of all four surfaces with dates | Section 2. |
| Repeatable check script | `scripts/check_user_enumeration.sh`. |

---

## 9. Verification method

Unauthenticated `curl` against production during the capture window, plus `php -l` on the new PHP and `make docs-truth-check` on the docs tree. No credentials were used. No request body was sent. No `POST` / `PUT` / `PATCH` / `DELETE` was issued. No xmlrpc method was called. No snippet was read or written live. No user, role, or host setting was changed.
