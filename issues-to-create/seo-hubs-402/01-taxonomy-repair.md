# [CONTENT] Recategorize five miscategorized posts and repair the dead contact link

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 1 of 9. **File this one first.**
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:high`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` (Category fixes + Dead links), `link-matrix.csv` data row 30
**Blocked by:** nothing

---

## Context

PR #670 mapped #402's ten search terms onto live URLs. Five ranking or cluster posts sit in the wrong category, so their `kk-collection-footer` ("Part of the X collection. See also: Y.") misleads readers and crawlers.

Worst case: post 1067 (2006 Hardcore Superstar photoshoot for a valet company) is filed under `vancouver-ai-ecosystem` and footers into The Long Road to Futureproof.

The 2026-08-15 grooming dossier (PR #769) split #402 into nine children and put this pass first because later children edit the same posts' link surface. Recategorize before those inserts.

This child also owns the one dead-link **repair** in the matrix: post 2819 still points at `http://www.kriskrug.com/contact` (wrong domain, connection failure). Repoint to `https://kriskrug.co/contact/`. That is data row 30. Child 5 later adds a Cyber Love Garden sentence on the same post; do not add that sentence here.

Declared term IDs (re-verify live before PATCH) from `scripts/seo-backfill/linkinject_lib.py`:

| Slug | Term ID |
|---|---|
| `web-early-blog` | 1757 |
| `ai-ethics-philosophy` | 1678 |
| `events-reports` | 1676 |
| `vancouver-ai-ecosystem` | 1662 |
| `ai-creatives` | 1665 |
| `photography-visual-storytelling` | 1756 |

## Owns (write)

- Categories on posts **3814, 3330, 1067, 1063, 1147** only (swap the listed primary; preserve any extra terms).
- Footer paragraph in those five posts **if** a cache-busted readback shows the old collection still baked into `post_content`.
- Href repair on post **2819** only (`kriskrug.com/contact` → `https://kriskrug.co/contact/`).

## Must not touch

- Any `link-matrix.csv` row except data row 30.
- Post 1210's ModelMayhem 404 (child 3).
- Page 12013, hub cards, meetup recaps, MBO spokes, brand-nav links.
- Titles, slugs, dates, status, featured images.
- Theme, `inc/`, schema, `AGENTS.md`.
- Page 2250 (`/events/`). That write surface belongs to #635.

## Acceptance Criteria

- [ ] Post 3814 primary category is `ai-ethics-philosophy` (1678), not `web-early-blog` (1757). Rendered footer no longer links `/category/web-early-blog/` as the collection hub.
- [ ] Post 3330 primary category is `events-reports` (1676), not `web-early-blog`.
- [ ] Post 1067 primary category is `photography-visual-storytelling` (1756), not `vancouver-ai-ecosystem` (1662). Rendered footer no longer presents the valet shoot as Vancouver AI ecosystem content.
- [ ] Post 1063 primary category is `photography-visual-storytelling` (1756), not `vancouver-ai-ecosystem`.
- [ ] Post 1147 primary category is `photography-visual-storytelling` (1756), not `ai-creatives` (1665).
- [ ] Post 2819 has no `kriskrug.com/contact` href. The replacement is `https://kriskrug.co/contact/` (data row 30). Surrounding copy is unchanged aside from the URL (and anchor text only if the dead URL was the visible text).
- [ ] Each of the six posts: slug and ID re-verified before PATCH; pre-write snapshot stored; rollback command recorded.
- [ ] No em dashes introduced. No other posts recategorized.

## Tests/Evals

- REST: `GET /wp-json/wp/v2/posts/<id>?_fields=id,slug,categories` for 3814, 3330, 1067, 1063, 1147, 2819. Assert expected category IDs (2819 categories unchanged).
- Rendered footer: cache-busted `curl` of each of the five recategorized permalinks; `grep -n kk-collection-footer` and assert the new collection name. If the footer is only in `post_content`, the category PATCH must be paired with a content-only footer edit in this same child.
- Dead link: `curl -sL https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/ | grep -o 'href="[^"]*contact[^"]*"'` contains `https://kriskrug.co/contact/` and does not contain `kriskrug.com`.
- Confirm `https://kriskrug.co/contact/` still returns 200.

## Verification

```bash
# Term IDs still match the map (logged-out)
curl -s 'https://kriskrug.co/wp-json/wp/v2/categories?slug=web-early-blog,ai-ethics-philosophy,events-reports,vancouver-ai-ecosystem,ai-creatives,photography-visual-storytelling&_fields=id,slug'

# Identity before any write
for id in 3814 3330 1067 1063 1147 2819; do
  curl -s "https://kriskrug.co/wp-json/wp/v2/posts/${id}?_fields=id,slug,link,status,categories"
done

# After apply (cache-bust)
curl -sL "https://kriskrug.co/2006/11/15/hardcore-superstar-photoshoot/?cb=$RANDOM" | grep -o 'kk-collection-footer[^<]*'
curl -sL "https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/?cb=$RANDOM" | grep -o 'kk-collection-footer[^<]*'
```

Authenticated category PATCH and snapshots use `WP_USER` + `WP_APP_PASSWORD` via Varlock. Default dry-run. Do not run `reassign_categories.py` (that tool is the #223 Misc classifier, not this five-post list).

## Agent Instructions

- Re-fetch each post by ID. Abort if slug is not the one in the table below.
- Snapshot `categories` plus `content.raw` before any write.
- Category write: replace only the listed primary ID; keep any additional category IDs.
- The 2026-08-02 plan said category change rewrites the footer for free. **Prove it on a cache-busted readback.** The 2026-06 link-inject wave baked `kk-collection-footer` into `post_content`. If the old collection is still in the body, edit that one paragraph in this child.
- Row 30: in-place href swap on 2819. Do not add the Cyber Love Garden sentence (child 5, data row 27).
- Payload-only PR first if KK has not approved live writes. Stop at the PR boundary.
- Do not close #402.

### Category table

| Post | ID | Slug (verify) | From | To |
|---|---|---|---|---|
| Most Benevolent Outcomes Prayer | 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `web-early-blog` | `ai-ethics-philosophy` |
| The Future Called: I Answered | 3330 | confirm via REST before write | `web-early-blog` | `events-reports` |
| Hardcore Superstar Photoshoot | 1067 | `hardcore-superstar-photoshoot` | `vancouver-ai-ecosystem` | `photography-visual-storytelling` |
| Made in Vancouver Photoshoot | 1063 | confirm via REST | `vancouver-ai-ecosystem` | `photography-visual-storytelling` |
| Fashion Photoshoot for Discollection | 1147 | confirm via REST | `ai-creatives` | `photography-visual-storytelling` |

### Data row 30

| source_url | target_url | anchor_text | section_hint |
|---|---|---|---|
| `https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/` | `https://kriskrug.co/contact/` | get in touch | Repair, replaces the dead `kriskrug.com/contact` link in place |

## Out of Scope

- Building a hub for `hardcore photoshoot` or changing that title.
- MBO inbound/outbound links (child 8), including the #328 / #339 unapplied inserts on 3814. Recategorize 3814 here; do not add worldview or `/ai-ethics/` sentences.
- Schema, Jetpack, theme title filters (#756), `AGENTS.md` SEO guardrails.
- Search Console.
- Filing or closing sibling #402 children.
