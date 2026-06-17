# Issue #36 Public Render Diagnosis - 2026-06-17

Scope: public/read-only diagnosis for the remaining #36 blocker after the 2026-06-17 SEO metadata backfill closed the missing-meta inventory.

## Summary

The remaining #36 blocker is not missing REST meta inventory. Public HTML readback shows the targeted page metadata is now populated for `/home/`, `/services/`, and `/contact/`, while the canonical front page `/` and `/blog/` still render a 246-character legacy description.

The `/blog/` surface also renders conflicting metadata channels:

- standard `description`: legacy 246-character homepage-style description
- `og:description`: 163-character post-like/social value
- `twitter:description`: 114-character blog description

This points to a public render owner, cache, or WordPress/Jetpack settings issue rather than a broad "missing descriptions" issue.

## Public Readback

Command shape:

```bash
python3 - <<'PY'
# urllib + HTMLParser public metadata probe against /, /blog/, /home/, /services/, /contact/
PY
```

Results:

| URL | Status | Standard description | OG description | Twitter description |
|---|---:|---:|---:|---:|
| `/` | 200 | 246 chars, legacy homepage-style text | 246 chars, same legacy text | none |
| `/blog/` | 200 | 246 chars, legacy homepage-style text | 163 chars, different post-like/social text | 114 chars, blog-specific text |
| `/home/` | 200 | 146 chars, latest-posts/field-notes text | 146 chars, same text | none |
| `/services/` -> `/generative-ai-services/` | 200 | 158 chars, services text | 158 chars, same text | none |
| `/contact/` | 200 | 152 chars, contact text | 152 chars, same text | none |

`FORMAT=json make seo-audit` was already clean for missing meta descriptions in the prior #36 closeout pass (`missing_meta_description: 0` across 997 audited items). This follow-up diagnosis was intentionally limited to public rendered HTML.

## Interpretation

#36 should stay open, but it is now narrowed:

- Do not reopen broad SEO backfill work.
- Do not add a duplicate theme/snippet metadata emitter while Jetpack is already emitting metadata.
- Diagnose the owner for `/` and `/blog/` public descriptions: WordPress reading settings, Jetpack SEO/social settings, a Code Snippets override, page-for-posts behavior, object/page cache, or template-level handling.
- Repeat public HTML readback after the owner/cache fix.

## Verification

- `make test` passed.
- `make docs-truth-check` passed.
- `make status-readonly` passed.
- No WordPress create/update/delete request was sent.
- No Search Console verification was attempted in this lane.
