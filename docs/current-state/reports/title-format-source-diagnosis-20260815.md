# Sitewide `<title>` format: source diagnosis (#756)

**Date:** 2026-08-15
**Lane:** Round-2 swarm, Lane G
**Mode:** READ-ONLY diagnosis. No live writes, no theme edits, no settings changes.
**Issue:** [#756](https://github.com/WalksWithASwagger/kriskrug-wp/issues/756)

> Dash convention: this report writes U+2014 EM DASH as `{EMDASH}` so the report itself does not
> trip the voice gate. Wherever `{EMDASH}` appears inside a code block, the literal character in
> the file is U+2014.

---

## 1. Verdict

**The format is theme-owned. It is not Jetpack, not a Code Snippet, and not a plugin.**

Two hardcoded values in `theme/kk-aurora/functions.php` produce the entire string:

| What | File:line | Current literal |
|---|---|---|
| Site descriptor (the tail) | `theme/kk-aurora/functions.php:338` | `Kris Krug \| AI Keynote Speaker & Creative Technologist` |
| Title separator (the dash) | `theme/kk-aurora/functions.php:355` | `{EMDASH}` (U+2014) |

```php
// theme/kk-aurora/functions.php:337-357  (verbatim, {EMDASH} = U+2014 in the real file)
function filter_document_title_parts(array $title): array {
    $site_descriptor = 'Kris Krug | AI Keynote Speaker & Creative Technologist';

    unset($title['tagline']);

    if (is_front_page()) {
        $title['title'] = $site_descriptor;
        unset($title['site']);
        return $title;
    }

    $title['site'] = $site_descriptor;

    return $title;
}
add_filter('document_title_parts', __NAMESPACE__ . '\\filter_document_title_parts');

function filter_document_title_separator(string $separator): string {
    return '{EMDASH}';
}
add_filter('document_title_separator', __NAMESPACE__ . '\\filter_document_title_separator');
```

The descriptor string occurs **exactly once** in the whole theme, so this is a single-point fix:

```
$ grep -rn "AI Keynote Speaker & Creative Technologist" theme/
theme/kk-aurora/functions.php:338:    $site_descriptor = 'Kris Krug | AI Keynote Speaker & Creative Technologist';
```

**Why #756 missed it:** the issue grepped `theme/kk-aurora/inc/seo-title.php`, which is genuinely
innocent. That file only reads per-post `jetpack_seo_html_title` meta and passes everything else
through untouched. The format lives in `functions.php`, which was not grepped.

**Live/repo state:** live `kk-aurora` `style.css` Version **1.6.5**, repo `main` **1.6.5**, in sync.
The stale `AGENTS.md` version banner observed during capture was corrected by PR #754; no follow-up
edit is required here.

---

## 2. Evidence chain

Every step below is a public, logged-out, unauthenticated readback. No REST SEO-field read was
trusted as proof, per the #756 warning.

### 2.1 The dash is genuinely U+2014, not an en dash or hyphen

```
$ curl -s "https://kriskrug.co/this-page-does-not-exist-404-test/" | grep -o "<title>[^<]*</title>"
Page not found {EMDASH} Kris Krug | AI Keynote Speaker &#038; Creative Technologist
  NON-ASCII: U+2014  EM DASH
```

WordPress core's default `document_title_separator` is a plain hyphen `-`. U+2014 is therefore
injected by a filter, which matches `functions.php:355` exactly.

### 2.2 The tail is NOT the site title option

| Surface | Value |
|---|---|
| `blogname` (REST root `/wp-json/`, raw option) | `Kris Krüg \| Generative AI Tools & Techniques` |
| `blogdescription` (REST root) | `Empowering Events & Organizations for the AI Age` |
| Rendered `<title>` tail | `Kris Krug \| AI Keynote Speaker & Creative Technologist` |
| `og:site_name` | `Kris Krug` |

Three different strings on three surfaces. That rules out "someone typed it into Settings →
General". The rendered tail overrides the stored site title, which is precisely what
`$title['site'] = $site_descriptor` does. The code comment at `functions.php:331-332` even says so
out loud: *"the theme fallback should not inherit the old 'Generative AI Tools & Techniques' site
identity."*

`og:site_name` = `Kris Krug` is a separate theme constant, `public_site_name()` at
`functions.php:581-583`. That is a third independent fingerprint of theme ownership.

### 2.3 Context sweep: the format covers contexts Jetpack SEO cannot reach

```
https://kriskrug.co/                  [200] Kris Krug | AI Keynote Speaker & Creative Technologist
https://kriskrug.co/2026/08/          [200] August 2026 {EMDASH} <TAIL>
https://kriskrug.co/?s=vancouver      [200] Search Results for "vancouver" {EMDASH} <TAIL>
https://kriskrug.co/tag/ai/           [200] AI {EMDASH} <TAIL>
https://kriskrug.co/blog/             [200] Blog {EMDASH} <TAIL>
https://kriskrug.co/category/ai-ethics-philosophy/  [200] AI Ethics &amp; Philosophy {EMDASH} <TAIL>
https://kriskrug.co/<bogus-slug>/     [404] Page not found {EMDASH} <TAIL>
```

Jetpack SEO title formats only cover `front_page`, `posts`, `pages`, `groups`, and `archives`.
**Search results and 404 are not in that list, and both carry the format.** Only a
`document_title_parts` / `document_title_separator` filter pair reaches every context uniformly.

### 2.4 The front page proves it is this specific code, not a lookalike

The front page renders the descriptor **alone**, with no separator and no tagline:

```
<title>Kris Krug | AI Keynote Speaker &#038; Creative Technologist</title>
```

WordPress core on a front page builds `title = blogname` + `tagline = blogdescription`, which
would render `Kris Krüg | Generative AI Tools & Techniques {EMDASH} Empowering Events &
Organizations for the AI Age`. The observed output requires *both* `unset($title['tagline'])` *and*
`unset($title['site'])` plus the title replacement: the exact three-line front-page branch at
`functions.php:340-346`. Core emits no separator when only one part remains, which is why the
front page shows no dash.

This is a distinctive behavioural fingerprint. A competing snippet would have to reproduce all of
it by coincidence.

### 2.5 The per-post escape hatch confirms the whole mechanism

`inc/seo-title.php` filters `pre_get_document_title` at `PHP_INT_MAX` and returns the post's
`jetpack_seo_html_title` meta when non-empty, short-circuiting `wp_get_document_title()` before
`document_title_parts` ever runs. Public REST meta reads (registered for REST by the theme's
`inc/seo-meta-rest.php`, per #661) match the rendered titles exactly:

| Post | `jetpack_seo_html_title` meta | Rendered `<title>` |
|---|---|---|
| 12410 `keep-the-machine-strange` | `Keep the Machine Strange: Neil Postman, AI, and Technological Resistance \| Kris Krüg` | identical. **No em dash, umlaut present** |
| 12653 `ai-lands-inside-every-profession` | `''` (empty) | `AI Lands Inside Every Profession {EMDASH} <TAIL>` |

This closes the loop mechanistically: **posts with an approved SEO title escape the format; posts
without one fall through to `functions.php:338`.** `/about/` and `/glossary/` also escape it for
the same reason.

### 2.6 Not a stale edge cache

Cache-busted requests (`?cb<timestamp><rand>=1`) return the identical title on both the post and
the feed. The observed behaviour is live, not a stale Pagely ARES snapshot.

---

## 3. Candidates ruled out, with evidence

| Candidate | Ruled | Evidence |
|---|---|---|
| `theme/kk-aurora/inc/seo-title.php` | **OUT** as the format source | Contains no format string. Only reads per-post meta and passes through (§2.5). It is the *override* path, not the *format* path. |
| Jetpack `advanced_seo_title_formats` | **OUT** | Cannot reach search results or 404 (§2.3). Jetpack SEO was deactivated on this site (documented in `inc/seo-meta-rest.php:6-9`, #661). Decisive tell: `issues-to-create/batch-session-followups-2026-06-24.json:19` records the homepage title being set via `advanced_seo_title_formats.front_page` to `Kris Krüg | ...` **with the umlaut**. Live renders **without** the umlaut. The Jetpack setting is not winning; the theme is. |
| Live Code Snippet | **OUT on behaviour, not on direct read** | The theme code fully and exactly explains all eight observed contexts including the front-page special case. No residual behaviour is left for a snippet to explain. I could **not** perform the authenticated snippet GET (see §8). |
| Yoast / Rank Math / AIOSEO / SEOPress | **OUT** | No signature anywhere in `<head>`. The only SEO-adjacent plugins present are Google Site Kit (analytics/AdSense) and a Meta Pixel. Neither writes titles. |
| Settings → General site title | **OUT** | Stored `blogname` is a different string entirely (§2.2). |

---

## 4. Corrections to the issue's premises

Worth recording, because two acceptance criteria are built on them:

1. **"Every post" is not accurate.** Posts carrying an approved `jetpack_seo_html_title` already
   render clean titles with no em dash and with the umlaut (e.g. post 12410). The defect hits
   posts, pages, archives, search, and 404 that have **no** approved SEO title. The four posts
   named in #756 all have empty meta, which is why they show it.

2. **The umlaut is not unambiguously canonical for this string.** `fixes/schema-snippets-deployed.php`
   declares the two entities differently:

   ```php
   'site_name'            => 'Kris Krug',          // ASCII canonical
   'site_alternate_names' => array('Kris Krüg', 'kriskrug.co'),
   'person_name'          => 'Kris Krüg',          // umlaut canonical
   'person_alt'           => 'Kris Krug',
   ```

   The `<title>` tail is the **site/publisher** slot, where deployed schema currently declares
   **ASCII** canonical and the umlaut as the alternate. #756 cites lines 37-38 (`person_name`) as
   proof the umlaut is canonical, but that is the **Person** entity. So this is a genuine KK
   decision, not a self-evident bug fix. See §5.2.

---

## 5. Proposed replacement format

### 5.1 The two options

**Option A: minimal, separator only.**

```
AI Lands Inside Every Profession | Kris Krüg | AI Keynote Speaker & Creative Technologist
```

Smallest possible diff. But it yields a double pipe, reads poorly, and leaves the length problem
untouched.

**Option B (recommended): short site suffix, full descriptor kept on the front page.**

```
Front page:  Kris Krüg | AI Keynote Speaker & Creative Technologist   (unchanged wording)
Everything else:  AI Lands Inside Every Profession | Kris Krüg
```

Three reasons Option B is stronger:

1. **It matches the site's own approved convention.** The hand-approved per-post titles already in
   production use exactly this shape. Post 12410 is `... | Kris Krüg`, `/about/` is
   `About Kris Krüg | AI Speaker, ...`. Today the global fallback *disagrees* with the site's own
   curated titles. Option B makes the fallback consistent with what has already been approved.

2. **It fixes real SERP truncation.** The current tail is 54 characters on its own. Google
   truncates around 60. Measured examples:

   | Post | Current | Option B |
   |---|---|---|
   | 12653 | 89 chars | 44 chars |
   | 12656 | 126 chars | 81 chars |

   Right now the descriptor is eating the SERP headline on every untitled post and, in the 12656
   case, the post title itself is being cut before the tail is even reached.

3. **The front-page title is preserved.** This matters: a naive "shorten the descriptor" edit would
   also shorten the homepage title, which is the one page where the full keynote-speaker descriptor
   is doing SEO work. Option B splits the single `$site_descriptor` into two constants so the
   homepage keeps its wording and only the suffix shortens.

> Scope note: Option B changes the *placement* of the descriptor, not its *wording*. The descriptor
> wording is owned by #735. If #735 rules a new descriptor, only the front-page constant changes.

### 5.2 Umlaut: recommendation and the tradeoff KK must rule

**Recommendation: use `Kris Krüg`.**

Arguments for the umlaut:
- Matches `person_name` in deployed schema, matches the stored `blogname`, and matches every
  hand-approved per-post title already live.
- Google folds diacritics for matching, so `Krüg` still ranks for the query "kris krug". There is
  no measurable ranking penalty.
- **No encoding risk here.** `ü` is U+00FC, which *is* representable in latin1. The known
  latin1 boundary and the precomposed `ü` exception are recorded in
  `docs/current-state/reports/voice-sweep-live-readback-20260815.md`; this report supersedes that
  earlier report's source-location guess. Additionally, this is a **PHP source file in the theme,
  not a DB write**, so the latin1 DB path is not involved at all. Double-safe.

Argument for ASCII `Kris Krug`:
- Deployed schema currently declares `site_name` as ASCII, and this string occupies the site slot.
  Staying ASCII keeps `<title>`, `og:site_name`, and schema `site_name` byte-identical, which is
  tidy for entity consolidation.

**These two are mutually exclusive and KK should pick one.** If KK picks the umlaut, the follow-up
is to flip `site_name` / `site_alternate_names` in `fixes/schema-snippets-deployed.php` so schema
and title agree. If KK picks ASCII, the em-dash fix still ships and the umlaut question is closed
deliberately rather than by accident, which satisfies the #756 acceptance criterion either way.

### 5.3 The exact patch (Option B, umlaut variant)

```php
function filter_document_title_parts(array $title): array {
    $front_page_title = 'Kris Krüg | AI Keynote Speaker & Creative Technologist';
    $site_suffix      = 'Kris Krüg';

    unset($title['tagline']);

    if (is_front_page()) {
        $title['title'] = $front_page_title;
        unset($title['site']);
        return $title;
    }

    $title['site'] = $site_suffix;

    return $title;
}

function filter_document_title_separator(string $separator): string {
    return '|';
}
```

---

## 6. Blast radius

Anyone applying this must know the change is wider than `<title>`:

1. **RSS feeds inherit the same string.** Verified live and cache-busted:

   ```
   /feed/                              channel title: Kris Krug | AI Keynote Speaker & Creative Technologist
   /category/ai-ethics-philosophy/feed/ channel title: AI Ethics & Philosophy {EMDASH} Kris Krug | AI Keynote...
   ```

   So the em dash is currently shipping into every feed reader too, and the fix cleans that up for
   free. Note this contradicts what `filter_feed_bloginfo()` (`functions.php:589-600`) appears to
   intend: it returns `public_site_name()` = `Kris Krug` for `$show === 'name'`, yet the channel
   title renders the full descriptor. The feed `<description>` **does** correctly render
   `homepage_meta_description()`, proving that filter is live and firing. I did **not** fully trace
   which core call path supplies the feed channel title. Flagging as a loose thread, not a blocker.

2. **`og:title`** is built from `wp_get_document_title()` at `functions.php:696`, so Open Graph
   titles change with it. That is desirable, since it is the same defect.

3. **Front page is unaffected by the separator change** (single title part, so core emits no
   separator). Only the descriptor constant touches it.

4. **Posts with an approved `jetpack_seo_html_title` are unaffected** by any of this.

---

## 7. Apply steps and rollback

### Lane and gates

Track B (theme). Per `AGENTS.md`: theme PRs merge only after KK approval. This is a `<head>`
metadata change with no layout impact, so the pixel gate should come back clean; run it anyway
since it is a prod-rendering change.

### Apply

1. Land or otherwise disposition PR #751 first; it already owns Aurora 1.6.6. Do not cut a second
   parallel release with the same version.
2. Branch from the resulting `main`, edit **only** `theme/kk-aurora/functions.php:337-357`, and
   assign the next available patch version (expected 1.6.7 after #751).
3. `make validate` (phpcs) and `make test`.
4. Open the PR as a draft referencing #756. Get KK's ruling on §5.2 **before** deploy.
5. Deploy via `scripts/deploy_theme_sftp.py` in the next deploy window. Capture the server-side
   backup path it prints (`kk-aurora.bak-<timestamp>`).
6. Follow the cache gate in `docs/current-state/SEO-INDEXING-RUNBOOK.md`: purge Pagely PressCACHE
   in the approved admin window, then verify with a unique `?cachebust=$(date +%s)` request.
7. Verify logged-out with the #756 command across 6 posts plus an archive, search, the feed, and 404.

### Rollback

**Prior value, captured verbatim 2026-08-15 at live theme 1.6.5** (`{EMDASH}` = U+2014):

```php
// theme/kk-aurora/functions.php:338
    $site_descriptor = 'Kris Krug | AI Keynote Speaker & Creative Technologist';

// theme/kk-aurora/functions.php:354-356
function filter_document_title_separator(string $separator): string {
    return '{EMDASH}';
}
```

Rollback path, in order of preference:

1. `git revert` the PR commit, bump `style.css` back, redeploy via SFTP, purge cache.
2. If SFTP is unavailable, restore the server-side backup directory captured at deploy time
   (`kk-aurora.bak-<timestamp>`).

Rollback is fully reversible and touches no database state, no post content, and no plugin
settings. **No live setting is being changed by this fix**, which is a meaningful de-risk versus
the Jetpack-setting theory in the issue: there is no prior settings value to snapshot because the
source turned out to be tracked code under version control.

---

## 8. What I could not settle

Stated plainly rather than papered over:

1. **I could not read the live Code Snippets list.** `WP_USER` and `WP_APP_PASSWORD` are unset in
   this worktree's environment and `varlock run --inject vars` did not resolve them
   (`creds: NOT RESOLVED`). So the snippet candidate is ruled out **on behavioural evidence**
   (§2.3-§2.5 leave no unexplained behaviour) rather than by direct enumeration.
   **What would settle it definitively:** a read-only
   `GET https://kriskrug.co/wp-json/code-snippets/v1/snippets` with the app password, grepping for
   `document_title` and `AI Keynote Speaker`. I rate the residual risk low, because the theme code
   reproduces all eight observed contexts exactly, including the distinctive front-page branch.

2. **The feed channel-title call path is untraced** (§6.1). The observation is solid and
   cache-busted; the mechanism is not fully explained. It does not change the fix.

3. **I did not verify by reading live PHP**, which is not servable. Confidence rests on the
   live/repo version match (both 1.6.5) plus the four-way behavioural fingerprint.

---

## 9. Related: `templates/single.html:55` author bio

For whoever picks up the theme fix. `theme/kk-aurora/templates/single.html:55` renders on every
single post:

```html
<p>Kris Krug is an AI keynote speaker, creative technologist, photographer, and community builder
working across BC + AI, Vancouver AI, and Futureproof Festival, and a living network of AI-era
projects.</p>
```

Two notes:
- Same umlaut miss. If KK rules umlaut in §5.2, this is a **`person_name`** slot, where deployed
  schema already declares `Kris Krüg` canonical without ambiguity, so this one should take the
  umlaut regardless of how the site-name question lands.
- It is a sixth distinct descriptor variant, feeding #735.

It is a static FSE template edit, same theme PR, no extra risk.

---

## 10. Acceptance-criteria status for #756

| Criterion | Status |
|---|---|
| Source identified with proving readback | **DONE**. `functions.php:338` + `:355`, §1-§2 |
| Em dash removed sitewide | **NOT STARTED**. Patch proposed §5.3, needs KK go-ahead |
| Surname ruling recorded | **BLOCKED ON KK**. Options and tradeoff in §5.2 |
| `single.html:55` umlaut | **NOT STARTED**. See §9 |
| Descriptor reconciled with #735 | **DEFERRED** to #735; §5.3 isolates it to one constant |
| Spot-check 6 posts + archive + 404 | **NOT RUN**. Post-deploy step, §7 |

Voice-gate follow-up for #747: the gate should cover `<title>`, `og:title`, and RSS channel titles,
not just body payloads. All three carry this string.
