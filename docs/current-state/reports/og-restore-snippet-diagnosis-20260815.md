# OG restore snippet diagnosis — issue #759

**Date:** 2026-08-15
**Lane:** K (Round-3 swarm)
**Scope:** READ-ONLY diagnosis. No live write, no snippet activation or deactivation, no deploy.
**Subject:** `fixes/og-restore-snippet.php`
**Live theme at time of readback:** Aurora `1.6.5` (public `style.css`), repo `main` `1.6.5` — in sync.

---

## Headline

**The snippet is not live, and has not been live since the day it was created.**

It is **Code Snippet ID 12**, named `Open Graph + Twitter Card meta (social link
previews)`, and it is **inactive**. Every Open Graph and Twitter Card tag on
kriskrug.co today is emitted by the **Aurora theme**, from
`theme/kk-aurora/functions.php`.

This inverts the premise of issue #759. The acceptance criteria still get
answered, but the answer to "is the retirement condition met" is not just yes —
the retirement already happened operationally on 2026-07-13 and was never
recorded. What is actually rotting is the **paper trail**, not production
behaviour.

There is a second, sharper finding underneath it. Because the theme deliberately
stands down whenever the snippet is present, **activating snippet 12 today would
regress the site's metadata**, not restore it. It is no longer a safety net. It
is a footgun with a friendly name. Details in "Why re-enabling it would be a
regression".

---

## 1. What OG tags the snippet was restoring

The snippet (`fixes/og-restore-snippet.php`, hooked to `wp_head` priority 5)
was written to emit, in this key order:

| Tag | Attribute | Source in snippet |
|---|---|---|
| `og:site_name` | `property` | `get_bloginfo('name')` |
| `og:title` | `property` | `wp_get_document_title()`, or `get_the_title()` when singular |
| `og:type` | `property` | `website`, or `article` when `is_singular('post')` |
| `og:url` | `property` | `home_url('/')`, or `get_permalink()` when singular |
| `og:description` | `property` | `get_bloginfo('description')`, or `get_the_excerpt()` when singular |
| `twitter:site` | `name` | hardcoded `@feelmoreplants` |
| `og:image` | `property` | featured image `large`, else first inline `<img>`, else site icon 512 |
| `og:image:secure_url` | `property` | same value as `og:image` |
| `twitter:title` | `name` | mirrors `og:title` |
| `twitter:description` | `name` | mirrors `og:description` |
| `twitter:image` | `name` | mirrors `og:image` |
| `twitter:card` | `name` | `summary_large_image` if an image exists, else `summary` |

Plus whatever the three `KKAurora\*` fallbacks add when they exist
(`work_page_open_graph_fallback`, `writing_archive_open_graph_fallback`,
`twitter_card_tag_fallbacks`) — the snippet calls them defensively through
`function_exists()`.

Note what the snippet **never** emits: a plain `<meta name="description">`.
There is no `description` key in its array, and its attribute ternary
(`str_starts_with($name, 'twitter:') ? 'name' : 'property'`) would print such a
key as `property="description"` even if one appeared. This is the single most
useful discriminator in this whole investigation and it does a lot of work below.

---

## 2. OG tags live today, with source attribution

Readback method (logged out, cache-busted, 2026-08-15):

```
curl -s -A "Mozilla/5.0" "https://kriskrug.co/?cb=$(date +%s)" \
  | grep -o '<meta \(property\|name\)="\(og:[^"]*\|twitter:[^"]*\|description\)"'
```

All three sampled routes returned **exactly one** of each tag — no duplicates,
which already tells us there is a single producer, not two stacked ones.

### Homepage — `https://kriskrug.co/`

| # | Tag | Value | Source |
|---|---|---|---|
| 1 | `og:site_name` | `Kris Krug` | **Theme** |
| 2 | `og:title` | `Kris Krug \| AI Keynote Speaker & Creative Technologist` | Theme |
| 3 | `og:type` | `website` | Theme |
| 4 | `og:url` | `https://kriskrug.co/` | Theme |
| 5 | `og:description` | `Kris Krüg is an AI keynote speaker and creative technologist…` | Theme |
| 6 | `twitter:site` | `@feelmoreplants` | Theme |
| 7 | `description` | same string as `og:description` | **Theme only** |
| 8 | `og:image` | `…/kriskrug-websute.png?fit=1024,410` | Theme |
| 9 | `og:image:secure_url` | same | Theme |
| 10 | `twitter:title` | mirrors `og:title` | Theme (`twitter_card_tag_fallbacks`) |
| 11 | `twitter:description` | mirrors `og:description` | Theme (fallbacks) |
| 12 | `twitter:image` | mirrors `og:image` | Theme (fallbacks) |
| 13 | `twitter:card` | `summary_large_image` | Theme (fallbacks) |

### Post — `https://kriskrug.co/2026/08/10/keep-the-machine-strange/`

Same 13 tags, same order. `og:type` is `article`. `og:image` is the post hero.
`og:description` is `Neil Postman gave us a discipline for refusing
technological inevitability. In the age of AI, technological resistance is not
rejection. It is civic attention.`

### Page — `https://kriskrug.co/about/`

Same 13 tags, same order. `og:type` is `website`, `og:title` is `About Kris Krüg`.

### Bonus route — `https://kriskrug.co/work/`

17 tags. Adds `og:image:width` `1200`, `og:image:height` `630`,
`og:image:alt`, and `twitter:image:alt`, with the BC+AI ecosystem image. That is
`work_page_open_graph_fallback()` firing, and it also carries `name="description"`.

**Source attribution summary: 100% theme. 0% snippet. 0% Jetpack.**

Jetpack is ruled out independently: no `og:locale`, no `article:published_time`,
no `article:author`, no `og:image:width`/`height` on the routes where Jetpack
would add them. Jetpack OG output has a characteristic shape and none of it is
present. (Consistent with the standing note that Jetpack is deactivated.)

---

## 3. Proof it is the theme and not the snippet

Four independent discriminators, in descending order of strength. Any one of the
first three is sufficient on its own; together they are conclusive.

### D1 — `<meta name="description">` exists (structural, decisive)

Live output on all four routes contains `<meta name="description" …>`.

Only one code path in the entire codebase can emit that tag:
`render_social_meta_tags()` in `theme/kk-aurora/functions.php`, via

```php
// line 704
if ($description !== '') {
    $tags['description'] = $description;
}
// line 754
$attribute = $name === 'description' || str_starts_with($name, 'twitter:') ? 'name' : 'property';
```

The snippet has no `description` key and no `$name === 'description'` branch in
its ternary. It is structurally incapable of producing this tag. Its presence
proves the theme's loop ran.

The other `description` handling in the theme is
`suppress_jetpack_meta_description()` (line 804), which is a
`jetpack_seo_meta_tags` **filter** — it does not print to `<head>` and does not
affect this.

### D2 — `og:site_name` is `Kris Krug`, not the raw blogname (value, decisive)

- Theme: `og:site_name => public_site_name()`, and `public_site_name()` is a
  hardcoded `return 'Kris Krug';` (functions.php line 581-583).
- Snippet: `og:site_name => get_bloginfo('name')`.

The unfiltered blogname, read from the public REST root
(`GET https://kriskrug.co/wp-json/` → `.name`), is:

```
Kris Krüg | Generative AI Tools &amp; Techniques
```

Live `og:site_name` is `Kris Krug`. If the snippet were producing this tag it
would read `Kris Krüg | Generative AI Tools &amp; Techniques`. It does not.

This also quietly updates issue **#345**: that handoff was written on 2026-07-13
against Aurora 1.3.37, when the theme still mapped `og:site_name` to
`get_bloginfo('name')`. The theme has since hardcoded `public_site_name()`, so
the stale-`og:site_name` symptom #345 was chasing is **already gone from the
rendered output**. The `blogname` option itself is presumably still stale, which
may still matter elsewhere, but the OG symptom is resolved. Worth a look when
#345 next comes up — flagged, not actioned, out of this lane's scope.

### D3 — `og:description` on a post is the SEO meta, not the excerpt (value, decisive)

- Theme: `public_meta_description()` reads post meta `advanced_seo_description`
  first, and only falls back to `get_the_excerpt()` if that is empty.
- Snippet: `get_the_excerpt($post)` directly, no meta lookup.

For post 12410 (`keep-the-machine-strange`):

| | Value |
|---|---|
| Live `og:description` | `Neil Postman gave us a discipline for refusing technological inevitability. In the age of AI, technological resistance is not rejection. It is civic attention.` |
| Actual excerpt (public REST `/wp-json/wp/v2/posts?slug=…`) | `Neil Postman did not predict AI. He left us something more useful: a discipline for refusing to treat any technology as the weather. Here is what technological resistance looks like in 2026.` |

These are different strings. Live matches the curated SEO meta, which only the
theme reads. The snippet would have emitted the excerpt.

### D4 — mutual exclusion by design (architectural)

`render_social_meta_tags()` opens with a guard:

```php
// theme/kk-aurora/functions.php:740
if (defined('KK_OG_SNIPPET_ACTIVE') || is_feed()) {
    return;
}
```

The snippet defines `KK_OG_SNIPPET_ACTIVE` at load time. So the two are mutually
exclusive by construction: if the snippet runs, the theme prints nothing. Live
shows theme output, therefore `KK_OG_SNIPPET_ACTIVE` was never defined,
therefore the snippet did not execute.

The zero-duplicates result across all four routes corroborates this: exactly one
producer ran.

### Where the earlier reading went wrong

PR #757's `fixes/README.md` (Lane J, issue #741) lists this file as **Live** with
snippet ID *undetermined*, reasoning from tag order and the presence of a
hardcoded `twitter:site`. That inference is understandable but wrong: the theme's
`social_meta_tags()` is a near-superset of the snippet, hardcodes the same
`@feelmoreplants`, and calls the same three fallback functions in the same order.
Value-and-order matching cannot separate them, because the snippet was written as
a faithful mirror of the theme. Only the **presence/absence** discriminators
(D1) and the two places where the theme has since diverged (D2, D3) can. That is
Lane J's own structural-discriminator technique applied to a case where Lane J
did not have the diverging tags to hand.

That README row needs correcting. See "Ledger corrections owed".

---

## 4. The Code Snippet ID: **12** (found — no live access required)

The ID did not need the authenticated REST route. It is committed in this repo,
in an authenticated Code Snippets API capture taken during the 2026-07-24 Aurora
cream deploy:

`backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json`

Full snippet table from that capture:

| ID | Active | Scope | Name |
|---|---|---|---|
| 1 | false | global | Make upload filenames lowercase |
| 2 | false | front-end | Disable admin bar |
| 3 | false | global | Allow smilies |
| 4 | false | content | Current year |
| 5 | **true** | global | KK Schema |
| 6 | false | front-end | Hotfix 2026-05-24: Projects redirect + Work OG fallback |
| 7 | **true** | front-end | KK SEO root files: llms.txt + robots policy 2026-06-12 |
| 8 | **true** | front-end | GSC404 query param canonicalize |
| 9 | false | front-end | A11Y CTA contrast hotfix 2026-06-18 |
| 10 | **true** | front-end | KK Asset Diet |
| 11 | false | front-end | TEMP Aurora 1.3.33 a11y contrast fallback - remove after theme deploy |
| 12 | **false** | front-end | **Open Graph + Twitter Card meta (social link previews)** |
| 13 | **true** | front-end | KK News Sitemap |

Corroboration, three ways:

1. `backup/aurora-deploy-20260724/qa/snippets.json` — independent capture, same
   day, also reports `id=12, active=false`.
2. `backup/aurora-deploy-20260724/qa/active-snippets-full.json` — the
   active-only list. Contains IDs `5, 7, 8, 10, 13`. **12 is absent.**
3. `fixes/issue-345-og-site-name-handoff-2026-07-13.md` states in prose: *"The
   production receipt on issue #319 records Aurora 1.3.37 as the active social
   metadata owner and Code Snippet 12 as inactive."* Owner receipt:
   `https://github.com/WalksWithASwagger/kriskrug-wp/issues/319#issuecomment-4953532560`

The snapshot body for ID 12 is byte-identical to `fixes/og-restore-snippet.php`
minus the opening `<?php` tag, with exactly one difference: the repo file gained
a `// phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped` comment in
commit `83fd304` (CI lint pass, #377/#391). Functionally identical, so the repo
file is a trustworthy record of what sits in slot 12.

The authenticated route was attempted once, as instructed, and is unavailable:

```
$ curl -s -o /dev/null -w "%{http_code}\n" https://kriskrug.co/wp-json/code-snippets/v1/snippets
401
```
`WP_USER` and `WP_APP_PASSWORD` both resolved EMPTY in this worktree, consistent
with every other lane in this swarm.

**Residual uncertainty, stated honestly:** the snapshots are from 2026-07-24, three
weeks old. They prove ID 12 and prove it was inactive then. They do not by
themselves prove it is still inactive *today*. Today's rendered output does that
independently, via D1/D2/D3/D4 — the theme is demonstrably the producer right
now, which cannot be true if snippet 12 is active. The two lines of evidence are
independent and agree. What a live authenticated
`GET /wp-json/code-snippets/v1/snippets` would add is confirmation that slot 12
still holds this snippet under this name and has not been repurposed. That is
the only open question, and it is a bookkeeping question, not a behavioural one.

---

## 5. Timeline

| Date | Event |
|---|---|
| 2026-06-18 | Snippet snapshots show IDs 1-9 only. Snippet 12 does not exist yet. |
| 2026-07-12 | `ba8101e` *fix: make Aurora own social metadata (#320)* — theme takes ownership, adds the `KK_OG_SNIPPET_ACTIVE` stand-down guard. |
| 2026-07-12 | `30d1657` *fix: restore Open Graph and Twitter metadata (#321)* — `fixes/og-restore-snippet.php` created as the temporary bridge. |
| 2026-07-12 | `07c6297` *fix: restore standard meta descriptions (#333)* — theme adds `$tags['description']`, the tag the snippet cannot emit. |
| 2026-07-13 | Issue #319 receipt records Aurora 1.3.37 as the active social metadata owner and **Code Snippet 12 as inactive**. |
| 2026-07-16 | Aurora **1.3.37** confirmed live. **The stated retirement condition is met on this date.** |
| 2026-07-24 | Two independent snapshots confirm ID 12 `active=false`; absent from the active-only list. |
| 2026-08-15 | Live Aurora **1.6.5**. Rendered output proves the theme is the sole OG producer. Snippet still inactive. |

The bridge was superseded within about 24 hours of being written, by the very
theme deploy it was bridging to, and switched off within a day or so of that.
Nobody wrote it down. That is the whole story.

---

## 6. Is the retirement condition genuinely met?

**Yes, unambiguously, and twice over.**

1. The literal condition — *"Retire it after Aurora 1.3.37 is live and
   verified"* — was satisfied on 2026-07-16 when 1.3.37 was confirmed live.
   Aurora is now 1.6.5, roughly thirty releases past it.
2. The condition behind the condition — *does the theme now emit these tags
   itself* — is satisfied and then some. The theme emits a **strict superset**:
   all 12 of the snippet's tags plus `name="description"`, with better sources
   for two of them (`public_site_name()` and the `advanced_seo_description` meta
   lookup) and the same three fallback functions.

There is no remaining function the snippet performs.

---

## 7. Why re-enabling it would be a regression

This is the part that makes the cleanup worth doing rather than merely tidy.

Because of the `KK_OG_SNIPPET_ACTIVE` guard, activating snippet 12 does not
*add* tags — it **replaces** the theme's output with the older, weaker version.
Concretely, activating it today would:

| Effect | Impact |
|---|---|
| `<meta name="description">` disappears from every route | SEO regression; this is a standard meta description, not a social tag |
| `og:site_name` reverts to `Kris Krüg \| Generative AI Tools &amp; Techniques` | Reintroduces exactly the stale value issue #345 was filed about |
| `og:description` on posts reverts from `advanced_seo_description` to raw excerpt | Loses every curated SEO description on the site |
| `suppress_jetpack_meta_description()` stands down too (it shares the same guard, line 805) | Jetpack's meta description would be allowed through again if Jetpack is ever reactivated |

So the file currently reads as a documented emergency rollback path
("deactivate the snippet" / "restore social previews") while actually being the
opposite. Anyone debugging missing OG tags at 2am who finds this file and
switches snippet 12 on would make things measurably worse and would have every
reason to believe they were helping. **That mismatch between what the file
promises and what it does is the real defect in #759**, more than the stale
version number.

---

## 8. Recommendation

**Retire it — but note that no live disable is required, because it is already
disabled.** The snapshot-first disable + rollback dance that #759 anticipates is
a no-op here. This is a documentation and ledger fix, plus one optional live
cleanup.

### Recommended, in order

**A. Correct the record (repo-only, no live write, agent-safe).**

1. Rewrite the header of `fixes/og-restore-snippet.php` to state the truth:
   Code Snippet **ID 12**, **INACTIVE since 2026-07-13**, superseded by Aurora
   `render_social_meta_tags()` as of 1.3.37, and — prominently — **do not
   activate, activating it regresses metadata** with the four-row table from
   section 7. Keep the code body untouched.
2. Correct the `og-restore-snippet.php` row in `fixes/README.md` Table A (on
   PR #757's branch, or as a follow-up if #757 merges first): `Live?` becomes
   **Not live**, `Snippet ID` becomes **12**, evidence pointing at this report.
3. Add the full ID/active table from section 4 to `fixes/README.md`. It answers
   the "no recorded ID" complaint for the *whole* directory, not just this file,
   and it was sitting in `backup/` the entire time.

**B. Optional live cleanup (needs KK approval, Track A).**

Delete Code Snippet 12 from production, or rename it to
`RETIRED 2026-08-15 — do not activate — see fixes/og-restore-snippet.php`.
Deleting is cleaner; renaming is lower risk and preserves the audit trail.
Either way it removes the footgun.

- **Blast radius:** zero on rendered output. The snippet is inactive; deleting an
  inactive snippet changes nothing that renders.
- **Rollback:** recreate it from the committed body at
  `backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json`
  (`id: 12`), or from `fixes/og-restore-snippet.php` minus the `<?php` tag. The
  body is preserved in git regardless, so this is fully reversible.
- **Snapshot first anyway:** capture a fresh
  `GET /wp-json/code-snippets/v1/snippets` before touching anything, both to
  confirm slot 12 still holds this snippet and to refresh the ledger. Snippet 11
  (`TEMP Aurora 1.3.33 a11y contrast fallback - remove after theme deploy`) is
  the same species of dead temporary snippet and could reasonably be swept in
  the same approved session.

**C. The corrected retirement condition, if KK prefers to keep the file.**

If the file stays in `fixes/` as an archived reference — which is defensible,
since it documents what the bridge did — its header condition should be replaced
with something actually checkable, not a version number that silently expires:

> Retire when `theme/kk-aurora/functions.php` `render_social_meta_tags()` is the
> live producer of OG tags. Check: `curl -s https://kriskrug.co/ | grep 'meta
> name="description"'` returns a match. A match means the theme's loop ran, which
> means this snippet is inactive and unnecessary. If that command ever returns
> nothing, the theme has stood down and something re-activated snippet 12.

That is a one-line command with a binary answer that stays true across theme
versions, instead of a version number nobody re-reads.

---

## 9. Ledger corrections owed

| Location | Says | Should say |
|---|---|---|
| `fixes/README.md` Table A (PR #757) | `og-restore-snippet.php` — **Live**, ID undetermined | **Not live**, ID **12**, inactive since 2026-07-13 |
| `fixes/og-restore-snippet.php` header | "Retire after Aurora 1.3.37 is live and verified" | Retired. ID 12, inactive. Do not activate. |
| Issue #759 title/body | "is live 30 releases past its stated retirement condition" | Was never live post-1.3.37; the *record* is what drifted |

**Out of scope, flagged only:** the same snapshot shows Code Snippet **13**
(`KK News Sitemap`) as **active=true** on 2026-07-24, while `fixes/README.md`
Table A lists `kk-news-sitemap-snippet.php` as *"Not live (draft)"* on the
grounds that `/news-sitemap.xml` returns 301. Both observations can be true at
once — I re-confirmed the 301 today (`301 → https://kriskrug.co/news-sitemap.xml/`,
a trailing-slash redirect, which is a routing issue rather than proof the snippet
is off). An active snippet whose route does not serve is worth a look under issue
**#425**. Not investigated here; not actioned.

---

## 10. Before/after verification commands

For whoever applies the change. If only option A (docs) is applied, the "after"
output must be **byte-identical** to "before" — a docs change must not move
production. If option B (delete/rename snippet 12) is applied, the output must
*also* be byte-identical, because the snippet is inactive.

Run logged out, cache-busted, across a post, a page, and the homepage.

### Capture before

```bash
mkdir -p /tmp/og-759
for u in "https://kriskrug.co/" \
         "https://kriskrug.co/2026/08/10/keep-the-machine-strange/" \
         "https://kriskrug.co/about/" \
         "https://kriskrug.co/work/"; do
  slug=$(echo "$u" | sed 's|https://kriskrug.co/||; s|/$||; s|/|_|g'); slug=${slug:-home}
  curl -s -A "Mozilla/5.0" "${u}?cb=$(date +%s)$RANDOM" \
    | grep -o '<meta \(property\|name\)="\(og:[^"]*\|twitter:[^"]*\|description\|article:[^"]*\)"[^>]*>' \
    > "/tmp/og-759/before-$slug.txt"
  echo "$slug: $(wc -l < /tmp/og-759/before-$slug.txt) tags"
done
```

Expected counts: `home` 13, post 13, `about` 13, `work` 17.

### Capture after, then diff

```bash
for u in "https://kriskrug.co/" \
         "https://kriskrug.co/2026/08/10/keep-the-machine-strange/" \
         "https://kriskrug.co/about/" \
         "https://kriskrug.co/work/"; do
  slug=$(echo "$u" | sed 's|https://kriskrug.co/||; s|/$||; s|/|_|g'); slug=${slug:-home}
  curl -s -A "Mozilla/5.0" "${u}?cb=$(date +%s)$RANDOM" \
    | grep -o '<meta \(property\|name\)="\(og:[^"]*\|twitter:[^"]*\|description\|article:[^"]*\)"[^>]*>' \
    > "/tmp/og-759/after-$slug.txt"
  if diff -q "/tmp/og-759/before-$slug.txt" "/tmp/og-759/after-$slug.txt" >/dev/null; then
    echo "PASS $slug — identical"
  else
    echo "FAIL $slug"; diff "/tmp/og-759/before-$slug.txt" "/tmp/og-759/after-$slug.txt"
  fi
done
```

### The one-line canary

The fastest single check that the theme is still the producer. Must return a
match on every route:

```bash
curl -s -A "Mozilla/5.0" "https://kriskrug.co/?cb=$(date +%s)" | grep -c 'meta name="description"'
```

`1` = theme is producing, snippet 12 is off, all is well.
`0` = the theme stood down, which means `KK_OG_SNIPPET_ACTIVE` got defined,
which means someone activated snippet 12. Roll that back.

### Duplicate guard

Should print `x1` for every tag. Anything higher means both producers ran.

```bash
curl -s -A "Mozilla/5.0" "https://kriskrug.co/?cb=$(date +%s)" \
  | grep -o '<meta \(property\|name\)="\(og:[^"]*\|twitter:[^"]*\|description\)"' \
  | sort | uniq -c | awk '{print "x"$1"  "$2" "$3}'
```

### The issue's own command, for the record

Issue #759 proposed this, and it passes — but note it is **not** sufficient on
its own, because it filters out `name="description"`, which is the tag that
actually discriminates theme from snippet. Use the canary above alongside it.

```bash
curl -s https://kriskrug.co/<post> | grep -o '<meta property="og:[^"]*"' | sort -u
```

---

## 11. Verification status

| Check | Result |
|---|---|
| Live OG readback, 3 required routes + `/work/`, logged out, cache-busted | **PASS** — all tags inventoried, zero duplicates |
| Source attribution theme vs snippet vs Jetpack | **PASS** — theme, by four independent discriminators |
| Retirement condition met | **PASS** — met 2026-07-16; snippet already inactive since 2026-07-13 |
| Code Snippet ID identified | **PASS** — ID **12**, from three committed captures + the #319 receipt |
| Snippet body matches repo file | **PASS** — identical but for one phpcs comment added in `83fd304` |
| Authenticated `GET /wp-json/code-snippets/v1/snippets` | **BLOCKED** — `401`; `WP_USER`/`WP_APP_PASSWORD` empty. Attempted once per lane instructions |
| Live confirmation that slot 12 is unchanged *today* | **NOT RUN** — needs the authenticated route; rendered-output evidence covers the behavioural question |
| Any live write, activate, deactivate, deploy | **NOT PERFORMED** — read-only lane, by design |

---

## 12. Evidence index

| Artifact | What it establishes |
|---|---|
| `fixes/og-restore-snippet.php` | What the snippet emits; the stale 1.3.37 retirement condition |
| `theme/kk-aurora/functions.php:686-763` | `social_meta_tags()` + `render_social_meta_tags()`, the live producer, incl. the `KK_OG_SNIPPET_ACTIVE` guard at 740 and the `description` branch at 704/754 |
| `theme/kk-aurora/functions.php:581-583` | `public_site_name()` hardcodes `Kris Krug` — discriminator D2 |
| `theme/kk-aurora/functions.php:622-652` | `public_meta_description()` reads `advanced_seo_description` — discriminator D3 |
| `theme/kk-aurora/functions.php:771-812` | `work_page_open_graph_fallback()`; `suppress_jetpack_meta_description()` sharing the guard |
| `backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json` | **Snippet ID 12, active=false**, full 13-snippet table, full body |
| `backup/aurora-deploy-20260724/qa/snippets.json` | Independent same-day confirmation of ID 12 inactive |
| `backup/aurora-deploy-20260724/qa/active-snippets-full.json` | Active-only list `5,7,8,10,13` — 12 absent |
| `fixes/issue-345-og-site-name-handoff-2026-07-13.md` | Prose record of "Code Snippet 12 as inactive"; #319 receipt link |
| `GET https://kriskrug.co/wp-json/` | Raw blogname `Kris Krüg \| Generative AI Tools &amp; Techniques` — D2 |
| `GET https://kriskrug.co/wp-json/wp/v2/posts?slug=keep-the-machine-strange` | Post 12410 excerpt, differs from live `og:description` — D3 |
| Commits `ba8101e`, `30d1657`, `07c6297`, `83fd304` | The 2026-07-12 timeline |

---

*Read-only diagnosis. No live writes were performed. Options A and B in section 8
are proposals for KK, not applied changes.*
