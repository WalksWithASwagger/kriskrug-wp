# Incident — Live blog post overwritten by Notion connector

**Date:** 2026-05-15
**Severity:** High (single live post body destroyed; URL became 404; broken inbound links from another live post; user-visible content loss)
**Resolution time:** ~2 hours from detection to full recovery
**Recovery quality:** Complete — full original content restored from Notion source

## What happened

At ~14:39 UTC on 2026-05-15, the Notion-to-WordPress connector at `scripts/notion-to-wp/kk_notion_to_wp.py` was run for the first time, to publish the post "Calling Us All In" from Notion to kriskrug.co. The run succeeded *visibly* — a new draft appeared at post ID 11765 with the correct content, was later promoted to publish, and post-publish verification (meta tags, OG, schema after deploy) all checked out.

What was not visible: **post ID 11765 was a pre-existing published post titled "Web Summit Vancouver 2026"**, dated 2026-05-07, with the slug `web-summit-vancouver-2026`. The connector did not CREATE a new post — it UPDATEd the existing post in place, replacing every field: title, slug, date, content, taxonomy, meta. The original post's URL `https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/` started returning 404. WordPress did not retain a revision (Pagely's setup either disables revisions or the full-payload UPDATE bypassed the revision system).

The mistake was discovered ~2 hours later when attempting to submit URLs to Google Search Console — the Web Summit URL returned 404 and GSC's live test rejected the re-index request. A search of the WP REST API for any post with the original title returned zero results across all statuses (including trash). Initial investigation thought post ID 11765 was an auto-draft we'd usefully filled in; only on returning to the missing-post problem and cross-referencing the May-8 audit data did the overwrite become unambiguous.

## Root cause

A broken idempotency check in the connector. The original `find_post_by_notion_id` function was implemented as:

```python
def find_post_by_notion_id(self, notion_id: str) -> int | None:
    r = self.s.get(
        f"{self.base}/wp-json/wp/v2/posts",
        params={"meta_key": "kk_notion_source_id", "meta_value": notion_id, ...},
    )
    for p in r.json():
        return p["id"]
    return None
```

This silently fails. WP REST does NOT honor arbitrary `meta_key`/`meta_value` query parameters unless the meta key has been registered via `register_post_meta()` with `show_in_rest: true`. For an unregistered key — like our brand-new `kk_notion_source_id` — the filter is silently ignored and WP returns the standard most-recent posts list. The first result is returned as the "matching existing post."

The most recent post at the time of the run was `web-summit-vancouver-2026` (id 11765, published a week earlier). The connector treated it as the existing post to update.

The downstream code did not validate the returned post in any way before issuing UPDATE — no title comparison, no date comparison, no "is this actually the post I think it is" check. The UPDATE went through with `POST /wp/v2/posts/11765`, replacing the full payload.

## Why our safety net didn't catch it

Several things failed at once:

1. **No verified backup** existed at the time of the run. FIX_QUEUE P0.1 ("take and verify the first backup") had been written into the audit recommendations specifically to be a hard prerequisite before any modification, and was not done. The session moved from "draft documentation" to "run the connector for real" without re-checking this gate.
2. **No dry-run + diff review** before live. The connector's `--dry-run` mode was used during development but not as a final verification step before the first live run.
3. **No CREATE-only default**. The connector treated UPDATE as a normal silent path rather than an explicit, opt-in destructive operation.
4. **No title/identity check** on UPDATE. The connector trusted whatever ID came back from `find_post_by_*` without sanity-checking that the post was the one we meant.
5. **No revision-based safety net**. WP usually saves a revision before UPDATEs; on this Pagely instance there were zero revisions. We did not check this assumption before running the connector for real.

The bug was *suspected and "fixed mid-flight"* — I rewrote `find_post_by_notion_id` to `find_post_by_slug` after spotting that the meta query was returning all posts. But by then the UPDATE had already happened, and the assumption was that the post we'd "updated" was a harmless auto-draft (the surrounding IDs in the 11760–11770 range were 404, supporting that). Only the May-8 audit data later showed unambiguously that 11765 had been a published post.

## How it was recovered

1. **Detection** — the post was found missing while submitting URLs to GSC. The URL was 404; REST search returned no posts with the original slug or title in any status (including trash).
2. **Cross-reference** — the May-8 audit data at `docs/current-state/raw/posts-page1.json` recorded post 11765's original identity (title, slug, date), proving it had been a published post before the connector run.
3. **Source recovery** — searched the Notion workspace for the post's content. Found it at `https://www.notion.so/359c6f799a33806c8250ce401eeab2c4` under the title "Welcome to Web Summit. Now Show Us the Numbers." (this had been the working title in Notion; the WP version was titled "Web Summit Vancouver 2026"). Cross-referenced a quoted phrase from the "Calling Us All In" post confirmed the same source content.
4. **Local capture** — downloaded all 10 source images from Notion's expiring S3 URLs to `content/drafts/2026-05-07-web-summit-vancouver-2026/images/`, plus saved post.md, post.html, SEO meta, alt-text, internal links to disk.
5. **Connector hardening** — added safety guards (see below) before re-running.
6. **Restore via the hardened connector** — used CLI overrides (`--title`, `--slug`, `--date`, `--publish`) to recreate the post with the original WP title, the original slug `web-summit-vancouver-2026`, and the original date `2026-05-07T11:37:33`. The post got a new WP post ID (the old 11765 remains the "Calling Us All In" post). The URL `https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/` returned to 200.
7. **Verification** — curl-checked the restored URL, confirmed schema renders, confirmed meta and content.

## Safety guards added to the connector

Permanent changes to `scripts/notion-to-wp/kk_notion_to_wp.py`:

1. **Slug-based idempotency.** `find_post_by_slug` uses WP's `?slug=` filter, which REST genuinely honors. Returns the ID only if exactly one post matches (to avoid the original "first of many" pitfall).
2. **CREATE is the default.** UPDATE requires explicit `--update` on the CLI. Just running the connector again with the same Notion source no longer touches the existing post — it aborts with a helpful error.
3. **Title-similarity check on UPDATE.** Even with `--update`, if the existing post's title is wildly different from the new title (similarity < 0.5 by `difflib.SequenceMatcher`), the run aborts. The 2026-05-15 overwrite had similarity ≈ 0.16 between "Web Summit Vancouver 2026" and "Calling Us All In", which would have triggered this guard.
4. **CLI overrides.** `--title`, `--slug`, `--date` flags allow precise control during recovery and republish scenarios without editing the Notion source.
5. **`create_or_update_post` split.** The single method was split into `create_post` and `update_post` so it's impossible to "accidentally update" — UPDATE is now a distinct code path that requires the guards to pass.

The simpler `--publish` gate was also tightened: it no longer requires `Status: Ready` in Notion, since the explicit `--publish` flag is enough of a barrier.

## Lessons

| Lesson | Action |
|---|---|
| WP REST's `meta_key`/`meta_value` filters silently ignore unregistered keys. | Avoid them entirely. Use `slug`, `id`, `date` filters that REST officially honors. Or `register_post_meta` with `show_in_rest: true` if a custom meta filter is needed. |
| Idempotency lookups must never blindly trust the first result. | Always validate identity after lookup (title match, date match, custom-meta match) before issuing UPDATE. |
| First-run of any destructive tool should be in CREATE-only mode. | Default to CREATE; require explicit opt-in for UPDATE. |
| Backups are not optional. They're a precondition for modification. | FIX_QUEUE P0.1 (UpdraftPlus or similar) becomes a hard prerequisite gated in the README / playbook. |
| Auto-drafts are not "safe to update." | An auto-draft can be safely cleaned up via DELETE, never via UPDATE-with-full-payload. |

## Open follow-ups

- [ ] FIX_QUEUE P0.1: take and verify the first full backup. Hard prerequisite for the next modification session.
- [ ] Add a `--diff` mode to the connector that shows a unified diff between the existing post and the proposed payload when `--update` is used. Belt-and-suspenders on top of the title-similarity check.
- [ ] Add a post-publish verification step: after CREATE, GET the post and confirm slug + title + date match what was sent.
- [ ] Add a unit test for the title-similarity guard using the exact 2026-05-15 case ("Web Summit Vancouver 2026" vs "Calling Us All In" → expected 0.16).
- [ ] Document the slug-based lookup pattern in connector README so future contributors don't re-introduce the meta-key approach.

## What did NOT need to change

- The block conversion logic (`block_rules.py`) was unaffected by the incident; content rendered correctly both times.
- The auth model (Application Password) worked as designed.
- The image pipeline worked as designed.
- The audit data we captured on May 8 was the single most useful artifact in diagnosing the issue. Keeping fingerprint snapshots at regular intervals is now clearly worth the effort.
