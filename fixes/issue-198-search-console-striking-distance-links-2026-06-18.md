# Search Console Striking-Distance Links - 2026-06-18

**Scope:** Repo-side SEO handoff only. Do not write live WordPress content from
this file without the normal backup/restore gate and public HTML readback.

## Source

- June 17 Search Console/GA4 digest flagged three KrisKrug.co query clusters:
  `you cant drink data`, `david zabowski nerdwallet mobile engineering`, and
  `lord of the rings drinking game`.
- Public/local search during this pass found a clear local draft target for
  `you cant drink data`.
- No repo-local KrisKrug.co page or source artifact was found for the David
  Zabowski/NerdWallet query, so that opportunity needs target confirmation
  before edits.

## Implemented Repo-Side

| Query cluster | Target | Repo-side action |
|---|---|---|
| `you cant drink data` | `content/drafts/2026-05-23-you-cant-drink-data/` | Tightened meta description to 146 characters and added backlink instructions in `internal-links.md`. |
| Kris homepage metadata | `content/source-packs/keynotes-2026/wp-payloads/page-meta.json` | Shortened homepage SEO title and refreshed the homepage meta description to 153 characters. |

## Next Safe WordPress Edits

1. Deploy the refreshed homepage title/description through the existing Jetpack
   SEO owner only; do not add another meta generator.
2. When `You Can't Drink Data` is live, add contextual backlinks from the two
   companion protest posts and one relevant hub/homepage/About surface.
3. Confirm whether the David Zabowski/NerdWallet query maps to an existing
   KrisKrug.co page, an external quote/testimonial, a podcast/media mention, or
   an irrelevant people-search artifact before creating or linking anything.
4. Keep `lord of the rings drinking game` parked as legacy/low-strategy unless
   KK explicitly wants entertainment/archive traffic.

## Suggested Anchors

- `you can't drink data`
- `Vancouver AI protest`
- `data centre protest`
- `cleaner AI infrastructure`

Avoid exact-match anchor stuffing. One strong contextual link from a relevant
page is better than repeating the same phrase across unrelated surfaces.
