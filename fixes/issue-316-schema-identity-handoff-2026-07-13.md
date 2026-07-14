# Issue #316: Schema Identity Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-316-schema-identity-handoff-2026-07-13.json`

## Decision

Align the existing Person and WebSite JSON-LD with the public keynote-first
identity. Keep the current schema ownership model and entity IDs. Do not add a
second schema plugin, a second Person node, or a theme-side JSON-LD owner.

Google's current site-name guidance recommends one concise, commonly recognized
`WebSite.name` on the homepage, with legitimate alternatives in
`alternateName`. The preferred site name is therefore `Kris Krug`, not the
long document-title descriptor. The accented name and domain are ordered
alternatives. The keynote positioning belongs on the Person node.

Guidance: https://developers.google.com/search/docs/appearance/site-names

## Live Evidence

Anonymous public HTML on 2026-07-13 showed:

- Homepage document title: `Kris Krug | AI Keynote Speaker & Creative Technologist`
- WebSite schema name: `Kris Krüg | Generative AI Tools & Techniques`
- Person job title: `Generative AI Strategist, Photographer, Community Builder`
- Person image: absent
- Exactly one Person node on the homepage, About page, and sampled article
- Exactly one WebSite node on the homepage and none on the internal samples
- All three sampled routes returned `200`

The output matches `fixes/schema-snippets-deployed.php`, confirming that the
repo already has the correct production mirror to update.

## Review-Ready Identity

| Field | Proposed value |
| --- | --- |
| `WebSite.name` | `Kris Krug` |
| `WebSite.alternateName` | `Kris Krüg`, then `kriskrug.co` |
| `Person.name` | `Kris Krüg` unchanged |
| `Person.alternateName` | `Kris Krug` unchanged |
| `Person.jobTitle` | `AI Keynote Speaker and Creative Technologist` |
| `Person.image` | `https://kriskrug.co/wp-content/uploads/2023/07/krug-1.jpg` |
| `Person.description` | `Vancouver-based AI keynote speaker, creative technologist, photographer, and community builder. Executive Director of BC + AI, founder of Vancouver AI, and lead curator of Futureproof Festival.` |

The portrait is already rendered on the public About page with alt text
`Portrait of Kris Krug`. Direct readback returned `200`, `image/jpeg`, and a
1,226,854-byte body. Visual review confirmed it is a clear portrait of Kris.

Both the production Code Snippets mirror and the future mu-plugin source now
share these identity constants. The future mu-plugin remains inert while its
unrelated `VERIFY-ME` fields exist.

## Separate Deployment Gate

Do not apply this handoff from the worker lane. A future production session
needs explicit approval for the exact Code Snippets change.

1. Open Code Snippets and verify that snippet ID 5 is still the active global
   PHP owner whose public output matches the repo mirror. Stop on any mismatch.
2. Capture the complete current snippet, name, activation state, scope, and a
   checksum as the rollback snapshot.
3. Rename the snippet to `KK Schema` if it is still unnamed.
4. Replace its code with the reviewed contents of
   `fixes/schema-snippets-deployed.php`, stripping only the opening PHP tag as
   required by Code Snippets.
5. Save one change, then perform authenticated, anonymous, and cache-busted
   readback before doing anything else.
6. Verify one Person node sitewide, one homepage-only WebSite node, unchanged
   Article author/publisher references, the exact identity values above, and a
   reachable portrait URL.
7. Validate the homepage and one article with Schema Markup Validator. Google's
   Rich Results Test does not support site names, so do not use it as the sole
   site-name check.
8. Restore the full captured snippet and purge only the affected cache surface
   if any identity, node-count, JSON parse, or route invariant fails.

The active priority indexing queue remains ahead of this homepage recrawl. Do
not consume RAP, FutureProof, or Indigenous AI quota for this schema-only
change. Natural recrawl is acceptable unless spare quota remains later.

## Remaining Identity Lane

The homepage Open Graph site-name mismatch is real but intentionally separate.
It currently comes from the WordPress site-title value through Aurora's social
metadata owner. This Track A schema change does not alter a WordPress option or
mix in Track B theme work. File and verify that correction separately.
