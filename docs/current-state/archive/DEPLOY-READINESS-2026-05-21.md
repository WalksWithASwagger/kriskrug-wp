# Staged-Lane Deploy Readiness — 2026-05-21

Phase 2 output from the v2 action plan. Read-only assessment of the 13 `swarm-ready` lanes:
which are verified ready to ship, which need work, what's missing. The strict backup/restore
proof gate was retired on 2026-05-22. Work now moves with dry-run/preview evidence, target
checks, rollback notes, and explicit deploy intent.

## Repo-side validation (done)
- `php -l` on all staged `fixes/*.php` → no syntax errors (6 files).
- `make test` → 11 cases pass. `kk-sidebar-promos` PHP smoke → pass. `git diff --check` → clean.

## Tier A — additive code, low-risk with preview/readback
| Issue | Artifact | Deploy method | Status |
|-------|----------|---------------|--------|
| #5 | `fixes/issue-5-color-contrast.css` | Additional CSS | ✅ ready |
| #10 | `fixes/issue-10-cta-hover-states.css` | Additional CSS | ✅ ready |
| #9 (hover) | `fixes/issue-9-button-hover-states.css` | Additional CSS | ✅ ready |
| #8 | `fixes/issue-8-aria-labels.php` | functions.php / helper plugin | ✅ lint-clean |
| #9 (search a11y) | `fixes/issue-9-search-accessibility.php` | functions.php / helper plugin | ✅ lint-clean |
| #43 | `fixes/issue-43-twitter-cards.php` | functions.php / helper plugin | ✅ ready — handle already set to `@kriskrug` (no placeholder edit needed; supersedes the plan note) |
| #36 | `fixes/issue-36-meta-descriptions.md` | per-page SEO fields | ✅ copy ready |

Batch the three CSS lanes (#5/#9-hover/#10) into one Additional CSS paste. Re-validate each
snippet against current live theme markup before pasting (`fixes/README-FIXES-BATCH-1.md` is
flagged Historical).

## Tier B — new pages, create-only, low-risk
| Issue | Artifact | Status |
|-------|----------|--------|
| #48 Accessibility Statement | `content/drafts/accessibility-statement-2026-05/` | ✅ WP page draft `11886` created |
| #44 AI Glossary | `content/drafts/ai-glossary-2026-05/` | ✅ WP page draft `11887` created |
| #18 Vancouver AI Community page | — | ⚠️ **NOT staged** — no deployable page artifact exists. Only unrelated Vancouver blog drafts. Needs authoring before it can ship. Reclassify out of "ready". |

## Tier C — touches existing live pages (dry-run + snapshot + sign-off)
- #13 / #14 / #15 role sections, #68 Work/Projects page. Reconcile against already-merged
  #108/#109/#110 content first to avoid duplication. Deploy via connector `--dry-run` → review
  → create-only live run → readback.

## Tier D — blocked elsewhere
- #86 Aurora staging QA → needs a deployed Aurora staging env (Track B / `aurora/v2`), not a
  kriskrug.co write. Defer to Phase 5.

## Corrections to the plan
1. #43 Twitter handle is already `@kriskrug` — the "update @YourTwitterHandle" step is moot.
2. #18 is **not** ready to ship (no page artifact); move it from Tier B to a "needs authoring" lane.

## Net
Tier A (7 lanes) is verified deploy-ready once each target path and rollback note is confirmed.
Tier B (#48, #44) now has private WordPress page drafts. #18 needs authoring. Tier C needs dry-run
reconciliation and sign-off.
Tier C (4 lanes) needs dry-run reconciliation. #86 is Track B.
