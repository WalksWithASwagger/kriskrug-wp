# #767 apply-ready reconfirm — 2026-08-17

**Issue:** #767 (`[SECURITY] Two WordPress usernames publicly enumerable via REST, sitemap, and ?author probes; no HSTS`)
**Status:** PREP ONLY. Still not applied. Still not enabled. Diagnosis is unchanged from [`user-enumeration-767-2026-08-16.md`](user-enumeration-767-2026-08-16.md). This file is a dated reconfirm, not a new policy.
**Captured:** 2026-08-17 06:27–06:30 UTC, unauthenticated and logged out, GET/HEAD only.
**Related:** #709 (HSTS stays there), #331 (sitemap AC of #767 is still the deploy half of that issue). PR #793 merged the drafts; this pass does not close #767.

Usernames are redacted. Live identifiers stay labeled `author-A` (public author, user id 1, slug-length 2) and `host-admin` (host-provisioned administrator, user id 18, slug-length 11). No username, slug, Location URL, or response body is printed here.

---

## 1. Headline

The three public enumeration paths are still open. The two #767 snippets and the existing #331 sitemap snippet are still apply-ready drafts. Nothing in this packet was enabled, pasted into Code Snippets, or written to live WordPress.

Closing those paths still needs the three unanswered KK rulings in section 6 of the 2026-08-16 diagnosis. This reconfirm does not invent answers.

---

## 2. Check script (desired post-apply state)

`scripts/check_user_enumeration.sh` against `https://kriskrug.co`. Before apply it is expected to FAIL all four rows.

| Surface | Result |
|---|---|
| REST `/wp-json/wp/v2/users` | **FAIL** |
| sitemap `/wp-sitemap.xml` | **FAIL** |
| author `/?author=1` | **FAIL** |
| HSTS homepage | **FAIL** (#709) |

Summary: **0 PASS / 4 FAIL**. Exit 1.

---

## 3. Independent logged-out confirmation (redacted)

Same four surfaces, classified only. No Location URL, username, slug, or body was printed.

| Probe | Status | Classification |
|---|---|---|
| `GET /wp-json/wp/v2/users` | `200` | `x-wp-total: 2`; JSON array length 2; `roles` / `capabilities` / `email` absent; labels `author-A` (slug-length 2) and `host-admin` (slug-length 11) |
| `GET /wp-sitemap.xml` | `200` | users child present (`users` substring count 1); index `<loc>` count 5 |
| `GET /?author=1` | `301` | Location contains `/author/` (URL not printed) |
| `GET https://kriskrug.co/` | `200` | `strict-transport-security` absent |
| `GET http://kriskrug.co/` | `301` | `strict-transport-security` absent |

This matches the 2026-08-16 capture. HSTS remains #709.

What was not probed: no `xmlrpc.php` method, no `system.multicall`, no login, no credential test, no Code Snippets write, no user/role edit, no Pagely/HSTS change.

---

## 4. `php -l`

| File | Result |
|---|---|
| `fixes/issue-767-hide-rest-users.php` | No syntax errors detected |
| `fixes/issue-767-disable-author-probes.php` | No syntax errors detected |
| `fixes/issue-331-archive-sitemap-policy.php` | No syntax errors detected |

No PHP or script edit in this pass. No syntax defect, editor-break, or username-print defect was found.

---

## 5. Headers still say prep / not deployed

| File | Header still present |
|---|---|
| `fixes/issue-767-hide-rest-users.php` | **PREP ONLY. Not deployed as of 2026-08-16.** Warns: do **not** unset `rest_endpoints` based on `is_user_logged_in()` (that filter runs before REST auth and would 404 the editor). After any future apply: editor author dropdown, Site Kit dashboard, authenticated users GET still 200, logged-out GET is 401. |
| `fixes/issue-767-disable-author-probes.php` | **PREP ONLY. Not deployed as of 2026-08-16.** Default 404s the query-string probe only. Pretty `/author/<slug>/` 404 requires an explicit `KK_767_DISABLE_AUTHOR_ARCHIVES` ruling. |
| `fixes/issue-331-archive-sitemap-policy.php` | Production deploy remains a separate human-approved step. Still the sitemap implementation for #767. **Not rewritten.** Still excludes users **and** category/tag sitemaps and emits `noindex,follow` on those archives. |

`fixes/README.md` Table A still marks both #767 files **Not live; prep only** and the #331 file **Not live**.

---

## 6. Remaining KK rulings (still unanswered)

Copied from section 6 of the 2026-08-16 diagnosis. No new answer is recorded here.

1. **Host-provisioned admin** (`host-admin`, user id 18, slug-length 11): keep, rename, or demote? Closing the three public paths reduces disclosure; it does not decide whether the account should exist.
2. **Sitemap apply:** deploy the full existing #331 snippet, wait for #331's remaining SEO acceptance criteria, or approve a users-provider-only extract as a later #331 revision? This lane does not add a users-only fork.
3. **Author archives:** query-string 404 only (recommended; compatible with #331 "keep archives accessible"), or also 404 pretty `/author/<slug>/` (stricter; set `KK_767_DISABLE_AUTHOR_ARCHIVES` — that is a #331 expansion and needs an explicit yes)?

HSTS stays on #709. Do not treat a green #767 check as including transport pinning until that issue ships.

No live change ships until rulings 1–3 are answered.

---

## 7. Apply-ready verdict

| Artifact | Verdict |
|---|---|
| `fixes/issue-767-hide-rest-users.php` | Still apply-ready. **Not enabled.** |
| `fixes/issue-767-disable-author-probes.php` | Still apply-ready at the default (query-string 404). **Not enabled.** |
| `fixes/issue-331-archive-sitemap-policy.php` | Still the sitemap half. **Not applied.** Do not extract a users-only fork unless KK records that on #331. |
| `scripts/check_user_enumeration.sh` | Still the repeatable logged-out assert. Before apply: four FAILs. |

**Not enabled / not applied.** #767 stays open.
