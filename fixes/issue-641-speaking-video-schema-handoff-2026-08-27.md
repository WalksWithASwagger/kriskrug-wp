# Issue #641: Speaking Video Schema Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress or Code Snippets write
**Manifest:** `fixes/issue-641-speaking-video-schema-handoff-2026-08-27.json`

## Decision

Prepare two separate `VideoObject` records for the two recordings embedded in
the Speaking page payload. Emit them only on page `1887` through the existing
`kk_schema_emit()` owner in `fixes/schema-snippets-deployed.php`.

Reuse the canonical Person only through
`about: {"@id":"https://kriskrug.co/#person"}`. Do not add an inline Person,
Event, Service, creator, or publisher. The page lists recordings, not a set of
concrete future engagements, so Event schema would be unsupported.

## Public Evidence

Logged-out checks on 2026-08-27 returned `200` for `/speaking/`, `/events/`,
and `/testimonials/`. The Events and Testimonials pages both link to
`/speaking/` already. Both exact `maxresdefault.jpg` thumbnail URLs returned
`200 image/jpeg`.

Public YouTube metadata matched the prepared values:

| Recording | Upload date | Duration | Seconds |
|---|---|---|---:|
| `hYT-hsml_ds` | `2026-07-08` | `PT52M55S` | 3175 |
| `-c7mgY2aSgM` | `2026-03-05` | `PT1H19M34S` | 4774 |

The official Schema.org Markup Validator returned HTTP `200` for the two
prepared blocks and reported exactly two `VideoObject` objects, zero errors,
and zero warnings.

The visible descriptions and `youtube-nocookie.com` embed URLs match
`content/drafts/2026-07-26-speaking-page/payload-body.html`. The manifest is
the exact field-level contract for the PHP output.

## Review-Ready Records

| Field | CreativeMornings Vancouver | Both Hands Full |
|---|---|---|
| `@id` | `https://kriskrug.co/speaking/#video-creativemornings-vancouver` | `https://kriskrug.co/speaking/#video-both-hands-full` |
| `name` | `Kris Krüg: The perils and parallels of AI's future` | `Both Hands Full: What Creatives Actually Need to Know About AI` |
| `uploadDate` | `2026-07-08` | `2026-03-05` |
| `duration` | `PT52M55S` | `PT1H19M34S` |
| `embedUrl` | `https://www.youtube-nocookie.com/embed/hYT-hsml_ds` | `https://www.youtube-nocookie.com/embed/-c7mgY2aSgM?start=11` |
| `about.@id` | `https://kriskrug.co/#person` | `https://kriskrug.co/#person` |

## Proof Triangle

The final Speaking booking card now links to `/events/` with the anchor
`Kris Krüg's event archive` and to `/testimonials/` with the anchor
`testimonials about Kris Krüg's work`.

No target-page edit is needed. The current Events page links back with
`Book Kris to speak`, and the current Testimonials page links back with
`Speaking` and `Book a keynote`.

## Separate Deployment Gate

Do not apply this handoff from the worker lane. Production snippet ID `5` has
not been read or changed here. The Speaking body deployment must be completed
and verified first. A later schema session needs fresh approval of the exact
snippet diff.

1. Confirm the body-only deployment of page `1887` is complete and the two
   facades, visible descriptions, `/events/` link, and `/testimonials/` link
   are present in cache-busted public HTML.
2. Authenticated-read snippet ID `5`. Verify its name, active state, global PHP
   scope, complete body, and checksum. Stop on any mismatch with the expected
   schema owner.
3. Save the complete current snippet as the private rollback snapshot.
4. Compare the live body with the merged production mirror and present the
   exact #641-only diff for human approval.
5. After approval, make one bounded code save. Do not change another snippet,
   the page body, title, metadata, taxonomy, theme, or analytics.
6. Read the snippet back authenticated. Purge only the affected page cache and
   inspect anonymous cache-busted HTML.
7. Require exactly two valid `VideoObject` blocks on `/speaking/`, neither on
   `/about/`, and both `about` references pointing to the existing Person ID.
8. Validate the two records with Schema Markup Validator.
9. If any body, node count, field, route, or JSON parse differs, restore the
   full captured snippet and activation state, purge the affected cache, and
   repeat authenticated and cache-busted readback.

## Repo Verification

The focused test executes the PHP with WordPress stubs. It checks the page
guard, hook priority, exact two-block manifest parity, minimal schema shape,
Person reference, Event exclusion, proof links, backlink evidence, and the
deployment safety boundary.

- `python3 scripts/tests/test_issue_641_speaking_schema.py`: 6 tests passed.
- `php -l fixes/schema-snippets-deployed.php`: syntax passed.
- Schema.org Markup Validator: 2 objects, 0 errors, 0 warnings.
- `make voice-check`: 163 files scanned, 0 violations.
- `make python-test PYTHON=python3`: 564 operational tests, 12 SEO inventory
  tests, and 68 SEO backfill and link-safety tests passed.
- `make verify PYTHON=python3`: JavaScript harness, plugin and theme smokes,
  docs truth, 44 PHP syntax checks, and PHPCS/WPCS 7 of 7 passed.
- `git diff --check`: passed.
