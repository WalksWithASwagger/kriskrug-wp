# #826 applied, 2026-08-18

**Issue:** [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) (child 1 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)).
**Lane:** Track A. KK go: "proceed" after Gate 1 prep was on `main`.
**Script:** `make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --apply'`
**Stamp:** `20260818T021548Z`

Dry-run printed six planned writes, then `--apply`. Re-run after write: all six `[SKIP]`. No titles, slugs, dates, or SEO meta changed. #830 / #833 copy was not added.

## Live readback (logged-out, 2026-08-18T02:16Z)

| ID | Slug | Categories | Footer pillar |
|---|---|---|---|
| 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `[1678]` | AI Ethics and Philosophy |
| 3330 | `the-future-called-i-answered` | `[1676]` | none (unchanged) |
| 1067 | `hardcore-superstar-photoshoot` | `[1756]` | Photography and Visual Storytelling |
| 1063 | `made-in-vancouver-photoshoot` | `[1756]` | Photography and Visual Storytelling |
| 1147 | `fashion-photoshoot-for-discollection` | `[1756]` | Photography and Visual Storytelling |
| 2819 | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` | `[1680]` | unchanged; href is `https://kriskrug.co/contact/`; no `kriskrug.com/contact` |

"See also" siblings were left alone (1067 still points at Long Road to Futureproof). `/contact/` is 200.

## Snapshots / rollback

`backup/issue-826-taxonomy/rest-post-{3814,3330,1067,1063,1147,2819}-before-20260818T021548Z.json`

```bash
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --restore backup/issue-826-taxonomy/rest-post-<id>-before-20260818T021548Z.json --apply'
```
