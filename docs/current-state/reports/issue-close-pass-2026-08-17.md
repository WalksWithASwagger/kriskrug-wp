# Issue close pass — 2026-08-17

**Lane:** docs only. No live WordPress write. No theme deploy.
**Trigger:** KK: if an issue already has a PR, close the issue and keep the board tidy.
**Blocker:** this Cloud session's GitHub App token returns 403 on `closeIssue` and `addComment`. Issues cannot be closed from here. GitHub will auto-close them when a merged PR body contains `Fixes #N` / `Closes #N`.

## What this PR does

Closes the leftover issues whose **repo work already merged** but stayed open because the landing PR used `Refs` instead of `Fixes`:

| Issue | Why it can close | Evidence |
|---|---|---|
| #741 | Schema-snippets pair collapsed; `fixes/` indexed | PR #757 |
| #733 | Five live Aurora em dashes stripped in 1.6.6 source | PR #751 (on `main`; live theme is still 1.6.5 until SFTP) |
| #743 | `parts/speaking-proof-grid.html` dropped from 1.6.6 | PR #751 |
| #637 | Stage photography inventory + rights ledger filed | PR #657 |

Deploy of 1.6.6 remains on the runbook / #731 Boost regen, not on these issues.

## Open PRs retargeted to `Fixes` so merge closes the rest

| Issue | PR | Note |
|---|---|---|
| #411 #412 #413 | #796 | Homepage Join BC / Labs / logo soup |
| #414 #415 #416 | homepage-414 branch PR | Stages / What People Say / newsletter |
| #418 #419 #420 #638 | page-cluster branch PR | About / speaking / services payloads + six-talk ruling |
| #740 #738 #749 | #795 | Archive execute, remote deletes, prune note |
| #742 | #788 | Already `Fixes` |
| #756 | #789 | Already `Closes` |
| #758 | #792 | Already `Fixes` |
| #759 | #784 | Header warning; keyword tightened to `Fixes #759` |
| #730 | #791 | Decision + runway recorded; Luma/welcome still KK's hands |

## Left open on purpose (PR exists, live apply still the issue)

These stay open until a session with `WP_USER` + `WP_APP_PASSWORD` (and SFTP where needed) applies them. Closing now would hide a live defect.

| Issue | PR | Remaining |
|---|---|---|
| #729 | #790 | Futureproof post 12732 still shows the expired Aug 15 Call for Talks |
| #480 | #794 | Six-route inline CSS still live; parked until 1.6.7 |
| #767 | #793 | REST `users` + `?author=` still public; snippets drafted only |
| #764 | #768 (merged) | Post 12327 em dashes + 12032 dead link not PATCHed |
| #771 | #776 (merged) | Gorgeous Ghost slug still 404 |
| #706 | #760 (merged) | GTM delay + pixel removal not applied |
| #709 | #766 (merged) | HSTS/CSP/COOP/XFO not on the live responses |
| #744 | #786 | Archive slice only; rewrite/relabel/split still owed |

## Also not closed

Epics, inventories, and work with no dedicated implementation PR: #4, #122, #127, #274, #276, #277, #318, #331, #339, #402, #403, #424, #477, #481, #585, #593, #602, #603, #612, #635, #639–#642, #690, #731, #735, #736, #737, #745.

## If a write-access PAT is available

```bash
gh issue close 741 733 743 637 --reason completed
```

Do not close the live-apply row from this session.
