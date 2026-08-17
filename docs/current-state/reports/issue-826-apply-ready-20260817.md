# #826 live reconfirm — still apply-ready (2026-08-17)

**Issue:** [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) (parent [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402); both stay **open**)
**Verdict:** **still apply-ready. Still not applied. KK must run `--apply`.**
**Captured:** 2026-08-17 06:29 UTC, logged-out GET only. No REST POST/PATCH/DELETE. Helper `--apply` was not run.
**Prep on `main`:** PR #841 (`35cf161`). Helper `scripts/apply_issue_826_taxonomy.py` (dry-run default). Targets `content/drafts/2026-08-02-seo-authority-hubs/fix-826/targets.json`. Playbook `…/fix-826/APPLY.md` (prior live reconfirm 2026-08-17T03:30Z).
**Lane:** Track A docs receipt. Gate 1 of `WORK-PLAN-2026-08-17.md`.

This pass does **not** recategorize extra posts and does **not** add Cyber Love Garden copy on 2819 (#830).

## Headline

Live kriskrug.co still matches the APPLY.md defect table. Slugs for 3814, 3330, 1067, 1063, 1147, and 2819 match `targets.json`. Term IDs for the six category slugs are unchanged. Baked `kk-collection-footer` still names the old collection on 3814/1067/1063/1147; 3330 still has no baked footer; 2819 still has exactly one `http://www.kriskrug.com/contact` href. `/contact/` still returns 200.

APPLY.md numbers did not change, so that file was left alone. This report is the dated evidence.

## Term IDs (logged-out REST)

`GET /wp-json/wp/v2/categories?slug=<slug>&_fields=id,slug` for each slug, plus the comma-combined query from the issue body. All six IDs match `targets.json` / `scripts/seo-backfill/linkinject_lib.py`.

| Slug | Expected ID | Live ID | HTTP |
|---|---:|---:|---:|
| `web-early-blog` | 1757 | 1757 | 200 |
| `ai-ethics-philosophy` | 1678 | 1678 | 200 |
| `events-reports` | 1676 | 1676 | 200 |
| `vancouver-ai-ecosystem` | 1662 | 1662 | 200 |
| `ai-creatives` | 1665 | 1665 | 200 |
| `photography-visual-storytelling` | 1756 | 1756 | 200 |

Combined query returned the same six `{id,slug}` pairs (order differs; IDs match).

## Posts (logged-out REST)

`GET /wp-json/wp/v2/posts/<id>?_fields=id,slug,link,status,categories,modified_gmt`. All six `status=publish`. **No slug drift vs `targets.json`.** Categories still the recorded defect, not the desired end state.

| ID | Slug | Live categories | Defect (unchanged) |
|---|---|---|---|
| 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `[1757]` web-early-blog | 2023 MBO essay footers into the 2005 archive |
| 3330 | `the-future-called-i-answered` | `[1757]` web-early-blog | 2023 DENT writeup in the early-blog bucket. **No baked `kk-collection-footer` today.** |
| 1067 | `hardcore-superstar-photoshoot` | `[1662]` vancouver-ai-ecosystem | 2006 valet shoot footers into The Long Road to Futureproof |
| 1063 | `made-in-vancouver-photoshoot` | `[1662]` vancouver-ai-ecosystem | same (See also: Vancouver Tech Journal) |
| 1147 | `fashion-photoshoot-for-discollection` | `[1665]` ai-creatives | 2007 fashion shoot in the creatives collection |
| 2819 | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` | `[1680]` (unchanged) | one `http://www.kriskrug.com/contact` href. Categories stay. |

Permalink `link` values match `targets.json` `url` fields.

Live `modified_gmt` values are the UTC form of the PDT stamps already recorded in `targets.json` (`modified_gmt_at_reconfirm`). Example: 3814 live `2026-06-29T04:37:13` vs stored `2026-06-28T20:37:13`. That offset is pre-existing from PR #841, not a new write.

## Cache-busted public HTML

Cache buster `?cb=312148` (and a second fetch for footer windows). Count is occurrences of the class `kk-collection-footer` in the rendered body.

| ID | Footer count | Baked pillar (still OLD) |
|---|---:|---|
| 3814 | 1 | Part of the [Web and Early Blog archive](https://kriskrug.co/category/web-early-blog/) |
| 3330 | **0** | none |
| 1067 | 1 | Part of the [Vancouver AI Ecosystem](https://kriskrug.co/vancouver-ai/). See also: The Long Road to Futureproof |
| 1063 | 1 | Part of the [Vancouver AI Ecosystem](https://kriskrug.co/vancouver-ai/) |
| 1147 | 1 | Part of the [AI for Creatives](https://kriskrug.co/ai-for-creatives/) |
| 2819 | 1 (out of payload) | Generative AI Tools — not rewritten here |

Post 2819 body window: `href="http://www.kriskrug.com/contact"` around anchor text `connect with me`. Count of that exact URL in the HTML: **1**. Site chrome also has `href="/contact/"` (nav). Replacement `https://kriskrug.co/contact/` is **not** in the body yet. `GET https://kriskrug.co/contact/` → **200**.

## Tests and authenticated dry-run

```text
python3 -m unittest scripts.tests.test_apply_issue_826_taxonomy
Ran 11 tests in 0.011s
OK
```

Authenticated helper dry-run was **skipped**: `WP_USER` / `WP_APP_PASSWORD` (and `WP_API_*` aliases) were unset in this Cloud session (`WP_USER_LEN=0`). Do not invent a dry-run plan from public REST; `context=edit` `content.raw` needs creds.

## What KK runs (not this session)

```bash
python3 -m unittest scripts.tests.test_apply_issue_826_taxonomy
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py'          # dry-run GET + printed diffs
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --apply'  # only after KK approves that diff
```

Desired end state after `--apply` (from APPLY.md; **not** live today): 3814 categories `[1678]`; 3330 `[1676]`; 1067/1063/1147 `[1756]`; 2819 still `[1680]`. 1067 footer names Photography and Visual Storytelling. 2819 href is `https://kriskrug.co/contact/` with no `kriskrug.com`.

## Out of this receipt

- No WordPress write
- No close of #826 or #402
- No extra recategorization
- No Cyber Love Garden sentence on 2819 (#830)
- No theme / plugins / `inc/` edits
- No new audit issues
