# #826 apply-ready reconfirm, 2026-08-17

**Issue:** [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) (child 1 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)). Both stay **open**.
**Lane:** Track A. Gate 1 of [`WORK-PLAN-2026-08-17.md`](../WORK-PLAN-2026-08-17.md).
**Payload:** [`content/drafts/2026-08-02-seo-authority-hubs/fix-826/`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-826/)
**Script:** `scripts/apply_issue_826_taxonomy.py` (dry-run by default).
**Verdict:** **Still apply-ready. Not applied.** Do not PATCH until KK says go.

This session did public GET readback, unit tests, and one authenticated dry-run. No REST POST/PATCH/DELETE. No `--apply`. No `--restore --apply`.

## Public readback (logged-out, 2026-08-17T06:28Z-06:30Z)

Method: `GET /wp-json/wp/v2/posts/<id>?_fields=id,slug,link,status,categories,modified_gmt` plus cache-busted HTML (`?cb=20260817T062915Z`) and public `content.rendered`. Term IDs from `GET /wp-json/wp/v2/categories?slug=...`.

Term IDs still match `scripts/seo-backfill/linkinject_lib.py` and `targets.json`:

| Slug | Live ID |
|---|---|
| `web-early-blog` | 1757 |
| `ai-ethics-philosophy` | 1678 |
| `events-reports` | 1676 |
| `vancouver-ai-ecosystem` | 1662 |
| `ai-creatives` | 1665 |
| `photography-visual-storytelling` | 1756 |
| `generative-ai-tools` (2819, unchanged) | 1680 |

`https://kriskrug.co/contact/` returned **200**. Pillar destinations also 200: `/ai-ethics/`, `/ai-events/`, `/category/photography-visual-storytelling/`, `/vancouver-ai/`, `/ai-for-creatives/`.

| ID | Slug | Live categories (defect) | Target primary | Baked `kk-collection-footer` |
|---|---|---|---|---|
| 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `[1757]` web-early-blog | 1678 ai-ethics-philosophy | Yes. `Web and Early Blog archive` -> `/category/web-early-blog/` |
| 3330 | `the-future-called-i-answered` | `[1757]` web-early-blog | 1676 events-reports | None |
| 1067 | `hardcore-superstar-photoshoot` | `[1662]` vancouver-ai-ecosystem | 1756 photography-visual-storytelling | Yes. `Vancouver AI Ecosystem` -> `/vancouver-ai/`. See also Long Road to Futureproof |
| 1063 | `made-in-vancouver-photoshoot` | `[1662]` vancouver-ai-ecosystem | 1756 photography-visual-storytelling | Yes. `Vancouver AI Ecosystem` -> `/vancouver-ai/` |
| 1147 | `fashion-photoshoot-for-discollection` | `[1665]` ai-creatives | 1756 photography-visual-storytelling | Yes. `AI for Creatives` -> `/ai-for-creatives/` |
| 2819 | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` | `[1680]` generative-ai-tools (unchanged) | href only | Unchanged tools footer. One `http://www.kriskrug.com/contact` (anchor: connect with me) |

Rendered class is `kk-collection-footer wp-block-paragraph`. The apply script matches the pillar `<a>` only, so the extra `wp-block-paragraph` class is not a blocker.

Public `modified_gmt` is unchanged since the 03:30Z pass. Earlier `targets.json` values were eight hours behind actual GMT (PDT stored as if GMT). This receipt and `targets.json` now store the public REST GMT stamps.

No Cyber Love Garden sentence on 2819. No MBO spokes added on 3814.

## Unit tests

```bash
python3 -m unittest scripts.tests.test_apply_issue_826_taxonomy
```

**11 tests, OK** (0.066s). Offline only. Mocked `--apply` paths never touched live WordPress.

## Authenticated dry-run

```bash
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py'
```

Ran. Varlock resolved `WP_API_USERNAME` / `WP_API_PASSWORD`. Context=edit GET only. Script printed `[DRY-RUN] no WordPress writes`.

| ID | Dry-run plan |
|---|---|
| 3814 | categories `[1757] -> [1678]`; footer pillar swap; `content.raw` 10922 -> 10906 |
| 3330 | categories `[1757] -> [1676]` (no content) |
| 1067 | categories `[1662] -> [1756]`; footer pillar swap; `content.raw` 2041 -> 2082 |
| 1063 | categories `[1662] -> [1756]`; footer pillar swap; `content.raw` 1495 -> 1536 |
| 1147 | categories `[1665] -> [1756]`; footer pillar swap; `content.raw` 1290 -> 1333 |
| 2819 | href repair only; `content.raw` 7370 -> 7367 |

No snapshot directory was written. Nothing pending beyond those six plans.

## Rollback (after a future apply only)

Restore is dry-run unless `--apply` is passed. Refuse snapshots outside the six IDs or a slug mismatch.

```bash
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --restore backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --restore backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json --apply'
```

Snapshot dir (created only on a real `--apply`): `backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json`.

## Still out of payload

- Post 1210 ModelMayhem 404 (#828)
- Hub cards on 12013 / 12318 / 12316 / 12319 (#827, #829, #830, #831)
- Meetup recaps -> `/events/` (#832)
- Cyber Love Garden sentence on 2819 (#830)
- MBO spokes on 3814 (#833)
- Page 2250 (#635)

## Gate

**Do not PATCH until KK says go.** After approval:

```bash
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --apply'
```

Then run the logged-out gates in `APPLY.md`. Do not close #826 or #402 from this receipt.
