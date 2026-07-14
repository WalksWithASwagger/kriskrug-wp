# Issue #345: WordPress and Open Graph Site-Name Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-345-og-site-name-handoff-2026-07-13.json`

## Decision

Change only the WordPress `blogname` option from
`Kris Krüg | Generative AI Tools & Techniques` to `Kris Krug` in a future,
separately approved production session.

No rendering-code change is required. Aurora already reads `blogname` for
`og:site_name`, while its document-title filter independently preserves the
longer `Kris Krug | AI Keynote Speaker & Creative Technologist` positioning.

No live WordPress write was performed in this worker lane.

## Live Evidence

Anonymous readback on 2026-07-13 established the current production state:

- `GET https://kriskrug.co/wp-json/` returned `200` and the encoded public name
  `Kris Krüg | Generative AI Tools &amp; Techniques`.
- The public Aurora stylesheet returned `200` with version `1.3.37`.
- The production receipt on issue #319 records Aurora 1.3.37 as the active
  social metadata owner and Code Snippet 12 as inactive.
- Homepage, About, Speaking, Blog, and a published article returned `200` in
  both normal and cache-busted reads.
- Every sample emitted exactly one `og:site_name`, always with the stale value.
- Every sample retained its keynote-first document title.

Owner receipt:
https://github.com/WalksWithASwagger/kriskrug-wp/issues/319#issuecomment-4953532560

The repo matches that ownership model. Aurora's `social_meta_tags()` maps
`og:site_name` to `get_bloginfo('name')`, and the inactive bridge mirror also
reads `get_bloginfo('name')`. The longer document-title descriptor is hardcoded
separately in `filter_document_title_parts()`.

## Exact Future Change

| Field | Before | After |
| --- | --- | --- |
| WordPress option | `blogname` | `blogname` |
| Value | `Kris Krüg | Generative AI Tools & Techniques` | `Kris Krug` |

The future production action may set only `blogname`. It must not change the
tagline, activate or edit Code Snippet 12, upload Aurora, edit schema Code
Snippet 5, or modify any content, analytics, Search Console, DNS, permissions,
or credentials.

## Separate Deployment Gate

Do not apply this handoff from the worker lane.

1. Obtain explicit approval for the exact `blogname` value `Kris Krug`.
2. Read the authenticated current option and stop if it no longer matches the
   public evidence in the manifest.
3. Capture the complete current value as the rollback snapshot.
4. Confirm Aurora still owns social metadata and Code Snippet 12 is inactive.
5. Confirm no concurrent WordPress settings edit is in progress.
6. Change only `blogname`, then stop all further writes.
7. Read back the authenticated option, public REST root, anonymous homepage,
   cache-busted homepage, and homepage document title immediately.
8. Purge PressCACHE only if the public value remains stale after the option is
   correct, then repeat the readback.
9. Restore the exact captured value and purge PressCACHE if the site name,
   title, owner, route status, or metadata-count invariant fails.

## Post-Change Evaluation

Check the homepage, About, Speaking, Blog, and the sampled Both Hands Full
article with normal, cache-busted, Twitterbot, Facebook, and Googlebot reads.

Expected results:

- public REST `name` is `Kris Krug`;
- every route returns `200`;
- every route emits exactly one `og:site_name` with value `Kris Krug`;
- every document title remains byte-for-byte unchanged from the manifest;
- Aurora remains the only active social metadata owner;
- Code Snippet 12 remains inactive;
- RSS titles reflect the concise site name as an expected consequence.

Do not spend priority Search Console indexing quota on this option-only change.
Natural recrawl is sufficient after the public checks pass.

## Adjacent Findings

The route matrix exposed two independent defects that must not be folded into
this one-option production action:

- Issue #346 tracks the homepage's missing `og:title` in both normal and
  cache-busted HTML.
- Issue #347 tracks the missing canonical on `/blog/`, which is a `200` URL
  listed in the page sitemap.

Issue #316 remains the separate Person and WebSite schema deployment lane. A
site-name approval does not authorize any of those three changes.
