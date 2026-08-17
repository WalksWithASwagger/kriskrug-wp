# #826 APPLY: taxonomy repair + post 2819 contact href

**Prepared, not applied. Do not PATCH until KK says go.**
Script is dry-run by default. `--apply` is the only write switch.

Parent: #402. This is child 1 of 9. Later hub children edit the same posts, so this lands first.

## Live reconfirm (logged-out, 2026-08-17T06:30Z)

Same defects as the 03:30Z pass. Dated receipt: [`docs/current-state/reports/issue-826-apply-ready-20260817.md`](../../../../docs/current-state/reports/issue-826-apply-ready-20260817.md). Term IDs still match `scripts/seo-backfill/linkinject_lib.py`. `/contact/` returns 200.

| ID | Slug | Live categories | Defect |
|---|---|---|---|
| 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `[1757]` web-early-blog | 2023 MBO essay footers into the 2005 archive |
| 3330 | `the-future-called-i-answered` | `[1757]` web-early-blog | 2023 DENT writeup in the early-blog bucket. **No baked `kk-collection-footer` today.** |
| 1067 | `hardcore-superstar-photoshoot` | `[1662]` vancouver-ai-ecosystem | 2006 valet shoot footers into The Long Road to Futureproof |
| 1063 | `made-in-vancouver-photoshoot` | `[1662]` vancouver-ai-ecosystem | same |
| 1147 | `fashion-photoshoot-for-discollection` | `[1665]` ai-creatives | 2007 fashion shoot in the creatives collection |
| 2819 | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` | `[1680]` (unchanged) | one `http://www.kriskrug.com/contact` href. Categories stay. |

The 2026-06 link-inject wave baked `kk-collection-footer` into `post_content` on 3814, 1067, 1063, and 1147. Recategorizing those four without a content edit would leave the old collection sentence in the body. The script swaps that one pillar `<a>` and leaves the "See also" sibling alone.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

## What the script writes

| ID | REST body |
|---|---|
| 3814, 3330, 1067, 1063, 1147 | `categories` (replace listed primary, keep extras). Content only if a baked footer still names the old collection. |
| 2819 | `content` only: `http://www.kriskrug.com/contact` → `https://kriskrug.co/contact/`. One occurrence. Anchor text stays "connect with me". |

Titles, slugs, dates, status, featured media, tags, and SEO meta stay untouched. No Cyber Love Garden sentence on 2819 (that is #830). No MBO spokes on 3814 (that is #833).

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_826_taxonomy

# Dry run: authenticated GET + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py'

# Apply only after KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --apply'
```

`--post-id 1067` limits to one post. Re-run after a successful apply prints `[SKIP]`.

Snapshot dir (mode 0700, files 0600):
`backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --restore backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_826_taxonomy.py --restore backup/issue-826-taxonomy/rest-post-<id>-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the six IDs or a slug mismatch.

## After-apply logged-out gates

```bash
for id in 3814 3330 1067 1063 1147 2819; do
  curl -s "https://kriskrug.co/wp-json/wp/v2/posts/${id}?_fields=id,slug,categories"
done

curl -sL "https://kriskrug.co/2006/11/15/hardcore-superstar-photoshoot/?cb=$RANDOM" \
  | grep -o 'kk-collection-footer[^<]*'
curl -sL "https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/?cb=$RANDOM" \
  | grep -o 'kk-collection-footer[^<]*'

curl -sL "https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/?cb=$RANDOM" \
  | grep -o 'href="[^"]*contact[^"]*"'
```

Expect: 3814 categories `[1678]`; 3330 `[1676]`; 1067/1063/1147 `[1756]`; 2819 still `[1680]`. 1067 footer names Photography and Visual Storytelling, not Vancouver AI. 2819 href is `https://kriskrug.co/contact/` and has no `kriskrug.com`.

## Out of payload

- Post 1210 ModelMayhem 404 (#828)
- Hub cards on 12013 / 12318 / 12316 / 12319 (#827, #829, #830, #831)
- Meetup recaps → `/events/` (#832)
- Page 2250 (#635)
- `reassign_categories.py` (that is the #223 Misc classifier)
