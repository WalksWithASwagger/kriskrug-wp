# Fixes vs Live State Reconciliation - 2026-05-20

**Purpose:** Prevent duplicate, stale, or conflicting deploys from `fixes/` after the May 2026 content and schema work.
**Rule:** This is a repo-side audit only. The strict backup/restore proof gate was retired on 2026-05-22. Live work now requires task-specific target checks, rollback notes, and explicit deploy intent.

## Current live checks

Checked with public `curl` fetches on 2026-05-20:

- Homepage, About, Work, and Speaking return `200`.
- `/work/` redirects/resolves to `/recent-projects-include/`.
- `/llms.txt` returns `404`.
- `/robots.txt` returns `200` and references the sitemap, but does not yet carry the explicit AI-crawler stance from `fixes/robots-txt-update.txt`.
- Homepage still has two `<h1>` elements.
- Homepage, About, Work, and Speaking still contain empty image alts.
- Work still emits `https://s0.wp.com/i/blank.jpg` as `og:image`.
- Homepage, About, Work, and Speaking each include JSON-LD scripts, so schema appears live via the deployed Code Snippets path.

## File-by-file disposition

| File | Status | Next action |
|---|---|---|
| `fixes/schema-snippets-deployed.php` | Current source of truth for live schema. | Keep synced with the Code Snippets version. Verify in wp-admin before editing. |
| `fixes/schema-snippets.php` | SSH/mu-plugin version, not the live deploy path today. | Keep as deploy target for a future mu-plugin migration. Do not install blindly over the Code Snippet. |
| `fixes/issue-39-schema-markup.php` | Obsolete-replaced. | Keep historical only; do not deploy because the newer schema files supersede it. |
| `fixes/llms-txt-template.md` | Still needed. | Deploy with a target path and rollback note; verify `/llms.txt` returns `200` text. |
| `fixes/robots-txt-update.txt` | Still needed. | Pick the final AI-crawler stance, capture current robots output first, and verify with curl/Search Console. |
| `fixes/issue-12-new-homepage-hero.md` | Needs review. | Compare with the latest homepage polymath hero draft before any copy-paste. |
| `fixes/issue-13-14-15-project-sections.md` | Needs review. | Compare against current Work/About/Speaking source packs and live pages. |
| `fixes/UPDATED-ABOUT-PAGE-COMPLETE.md` | Likely superseded by May 2026 About updates. | Treat as historical unless a diff against live proves a missing section. |
| `fixes/issue-67-services-page-expanded.md` | Needs review. | Compare against the merged services role-positioning work before publishing. |
| `fixes/issue-68-work-page-complete.md` | Needs review. | Compare against live Work page and the Work OG/slug issue before publishing. |
| `fixes/owned-sites-network-rollout.md` | Applied. | Keep as rollback/audit record. |
| `fixes/issue-36-meta-descriptions.md` | Needs review. | Reconcile with Jetpack/OG behavior and Work blank OG before introducing another SEO source. |
| `fixes/issue-43-twitter-cards.php` | Needs review. | Do not deploy alongside Jetpack/Rank Math without duplicate meta checks. |
| `fixes/issue-37-xml-sitemap-setup.md` | Mostly historical. | Sitemaps already exist; revisit only if sitemap coverage breaks. |
| `fixes/issue-5-color-contrast.css` | Needs current visual audit. | Re-test against live theme and Aurora separately. |
| `fixes/issue-9-button-hover-states.css` | Needs current visual audit. | Re-test against live theme and Aurora separately. |
| `fixes/issue-22-land-acknowledgment.md` | Content guidance. | Review after IA decisions; do not apply as a standalone live edit without backup. |
| `fixes/README-FIXES-BATCH-1.md` | Historical index. | Keep bannered as historical; use this reconciliation doc as the current index. |

## Safe next deployment set

The smallest safe live batch is:

1. `/llms.txt`.
2. Robots AI-crawler stance.
3. Homepage H1 correction.
4. Highest-visibility image alt fixes.
5. Work OG/canonical/slug cleanup.

Schema should not be part of that first batch unless wp-admin verification shows the deployed Code Snippet is missing or stale.
