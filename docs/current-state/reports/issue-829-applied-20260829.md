# #829 applied, 2026-08-29

**Issue:** [#829](https://github.com/WalksWithASwagger/kriskrug-wp/issues/829), child 4 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402).
**Lane:** Track A content only.
**Approval:** KK replied `approved proceed` to the exact `Approve #829 live apply` gate.
**Window:** 2026-08-29T20:23:00Z through 2026-08-29T20:24:45Z.
**Tooling:** Varlock-backed `scripts/apply_issue_829_ai_ethics_hub.py`, one `--item-id` per write.

## Preflight

- `make doctor`: OK; Varlock schema, GitHub authentication, clean `main`, one worktree, and live style readback passed.
- `make status-readonly`: WordPress 7.0.4, Aurora live/repo 1.6.9, zero open PRs, clean drift checks, and zero WP smoke failures.
- `python3 -m unittest scripts.tests.test_apply_issue_829_ai_ethics_hub -v`: 13/13 passed.
- Authenticated dry run planned exactly four content-body changes and no others.
- #826 dependency gate passed for posts 3814, 3330, 1067, 1063, and 1147.
- Cache-bypassed public preflight found zero occurrences of each new anchor; target post 11936 returned 200.

## Applied objects

| ID | Slug | Raw characters | Snapshot | Public acceptance |
|---:|---|---:|---|---|
| 12318 | `ai-ethics` | 3,731 → 4,270 | `backup/issue-829-ai-ethics-hub/rest-page-12318-before-20260829T202300Z.json` | One You Can't Drink Data card and blurb, before Punk Rock AI; Punk Rock AI, RAP, and archive cards preserved |
| 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | 17,822 → 17,954 | `backup/issue-829-ai-ethics-hub/rest-post-12030-before-20260829T202333Z.json` | Exact street-level anchor once; `just a faster leak` preserved; zero `/about/` body links |
| 6144 | `ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence` | 15,628 → 15,772 | `backup/issue-829-ai-ethics-hub/rest-post-6144-before-20260829T202405Z.json` | Exact protest anchor once, before the single preserved collection footer |
| 11882 | `we-trained-ai-on-stolen-work` | 4,353 → 4,485 | `backup/issue-829-ai-ethics-hub/rest-post-11882-before-20260829T202432Z.json` | Exact guild anchor once; all three 11936 links present, including both older anchors |

Every snapshot file is mode 0600 and remains local-only under the narrow
`.gitignore` rule for `backup/issue-829-ai-ethics-hub/`; this repository is
public, so the authenticated edit-context dumps are not committed. Integrity
hashes for the local rollback files:

| ID | SHA-256 |
|---:|---|
| 12318 | `75d767bc617a53ceedd63ca84c30bfee8a0ab34e1ddd704e8dbef690c3086962` |
| 12030 | `dae51d126d10c8c65b360aa16a950f17aae56aabb706106bb2a266d20bcd407d` |
| 6144 | `d5ac95434e7be600fdf9c082980374e55b1f69881e2014c8aa468d31ff817993` |
| 11882 | `ac3ffe804caab46eee6080b8f25abb474c0c826c56b88a8990a9710092c149b7` |

Every write used a payload containing only `content`; title, slug, status,
dates, excerpt, taxonomy, featured media, SEO, schema, theme, and post 11936
were not written.

## Verification and rollback

- Authenticated aggregate re-run: four `[SKIP]` rows and `[OK] nothing pending.`
- Public REST and cache-bypassed rendered output passed exact ID, slug, count,
  order, footer, closing-paragraph, and preserved-link assertions.
- Ordinary cached URLs also returned one occurrence of each new anchor, so no
  manual Pagely cache purge was required.
- All four restore commands were run without `--apply`; each printed the exact
  approved ID and snapshot path. No rollback was applied.

Rollback one object, if needed:

```bash
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py --restore backup/issue-829-ai-ethics-hub/<snapshot>.json'
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py --restore backup/issue-829-ai-ethics-hub/<snapshot>.json --apply'
```

The first command is a dry-run preview. Use the second only with explicit
rollback approval and after reconfirming the exact ID/slug.

## Scope boundary

#830-#834, #828, issue #4 residuals, post 11936, `/about/`, taxonomy, theme,
plugins, schema, and titles were not touched. Parent #402 remains open.
