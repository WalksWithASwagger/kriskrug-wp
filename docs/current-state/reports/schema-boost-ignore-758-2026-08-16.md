# Schema JSON-LD `data-jetpack-boost="ignore"` — issue #758

**Date:** 2026-08-16
**Lane:** Track A (docs + canonical snippet header only)
**Scope:** READ-ONLY diagnosis. No live WordPress write, no Code Snippet
POST/PATCH, no theme deploy.
**Subject:** Why live JSON-LD script tags carry `data-jetpack-boost="ignore"`
when no repo file emits that attribute.

---

## Headline

**Jetpack Boost injects the attribute at output. The live snippet does not
need to author it, and the repo emit should stay bare.**

Boost's Defer JS / render-blocking pipeline stamps
`data-jetpack-boost="ignore"` onto `<script type="application/ld+json">`
(also `application/json` and `importmap`) so later passes do not move those
blocks. That is why every live JSON-LD tag has the attribute and no other
current script tag does.

Pasting `fixes/schema-snippets-deployed.php` over Code Snippet 5 will **not**
strip the rendered wrapper. Boost will stamp it again. Do not add the
attribute to `kk_schema_emit()`.

---

## Credential gap

`WP_USER` and `WP_APP_PASSWORD` are unset in this Cloud session (length 0).
`GET /wp-json/code-snippets/v1/snippets` returns **401**. This report does
**not** claim to have read the live Code Snippet body. Diagnosis is from
logged-out rendered HTML, public REST, repo files, historical authenticated
snippet captures already in the repo, and Jetpack Boost's published source.

---

## 1. Fresh logged-out counts (2026-08-16)

User-Agent `kriskrug-wp-758-readback/1.0`. Parser counts match raw
`grep` counts.

| Route | HTTP | `<script>` | JSON-LD | `data-jetpack-boost="ignore"` | JSON-LD with ignore | other scripts with ignore |
|---|---:|---:|---:|---:|---:|---:|
| `/2026/08/10/keep-the-machine-strange/` | 200 | 8 | 3 | 3 | 3 | 0 |
| `/` | 200 | 8 | 2 | 2 | 2 | 0 |
| `/about/` | 200 | 7 | 2 | 2 | 2 | 0 |

Exact opening tags on the post (the issue's verification URL):

```html
<script data-jetpack-boost="ignore" type="application/ld+json">  <!-- Person -->
<script data-jetpack-boost="ignore" type="application/ld+json">  <!-- BlogPosting -->
<script data-jetpack-boost="ignore" type="application/ld+json">  <!-- BreadcrumbList -->
<script id="google_gtagjs-js" src="https://www.googletagmanager.com/gtag/js?id=G-X7JE8B32L7" async>
<script id="google_gtagjs-js-after">
<script>   <!-- Meta Pixel inline -->
<script type="speculationrules">
<script type='text/javascript' src='https://s5102.pcdn.co/wp-content/boost-cache/static/4aba8ad99b.min.js'>
```

`@type` values are unchanged from the #741 / #425 contract:

| Route | JSON-LD `@type` set |
|---|---|
| post | `Person`, `BlogPosting`, `BreadcrumbList` |
| home | `Person`, `WebSite` |
| `/about/` | `Person`, `BreadcrumbList` |

Public REST: `/wp-json/` lists `jetpack-boost/v1`, `jetpack-boost-ds`, and
`code-snippets/v1`. `GET /wp-json/jetpack-boost/v1/status` is **404**
unauthenticated. `GET /wp-json/wp/v2/plugins` is **401**.

---

## 2. Decision: Boost-injected, not snippet-authored

Issue #758's 2026-08-15 observation still holds: only JSON-LD tags carry
the attribute. That observation alone does not prove the live snippet
authors it. Three further facts settle the source.

### 2.1 Repo and historical snippet bodies omit the attribute

`kk_schema_emit()` in `fixes/schema-snippets-deployed.php` and
`fixes/schema-snippets.php` still prints:

```php
echo "\n<script type=\"application/ld+json\">"
```

`grep` of `fixes/`, `theme/`, and `inc/` finds no emitter of
`data-jetpack-boost`. Authenticated captures already in the repo show the
same bare emit:

| Capture | Snippet 5 `kk_schema_emit` has `data-jetpack-boost`? |
|---|---|
| `backup/20260618-050328Z/page-snapshots/code-snippets.before-gsc404.json` | no |
| `backup/20260618-051950Z/page-snapshots/code-snippets.after-a11y-cta-hotfix.json` | no |
| `backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json` | no |

The 2026-07-24 body is the last durable authenticated read of snippet 5.
Its emit matches the current repo file.

### 2.2 Boost's Defer JS pipeline writes the attribute onto JSON-LD

Jetpack Boost `class-render-blocking-js.php::ignore_exclusion_scripts()`
runs a regex over the output buffer and calls `add_ignore_attribute()` on
matches. The published comment in that method is explicit: scripts whose
type is `application/json`, `application/ld+json`, or `importmap` are
stamped so later passes do not move them. `add_ignore_attribute()` inserts
`data-jetpack-boost="ignore"` immediately after `<script`. Changelog:
"Defer JS: Automatically exclude JSON-LD schemas" (PR #35417).

That produces exactly the live opening tag:

```html
<script data-jetpack-boost="ignore" type="application/ld+json">
```

from the bare emit in the snippet.

### 2.3 Why other live scripts are exempt

Boost does **not** blanket-stamp every `<script>`. It stamps the exclusion
set in §2.2 (plus shortcode output, exclusion-list handles, and
`document.write` inlines). Current non-JSON-LD tags are outside that set:

| Live tag | Why no ignore attribute |
|---|---|
| Site Kit `gtag` (`id=google_gtagjs-js`, external JS) | executable JS, not `ld+json` / `json` / `importmap` |
| Site Kit `gtag` inline (`id=google_gtagjs-js-after`) | same |
| Meta Pixel inline (`<script>` with no type) | same |
| `<script type="speculationrules">` | not in Boost's exclusion-type regex |
| Boost `boost-cache/static/*.min.js` | concatenator output, not an excluded type |

Older committed HTML under `docs/current-state/raw/` still shows Boost
stamping **other** excluded types: CDN jQuery and
`<script id="wp-emoji-settings" type="application/json">`. Those tags are
gone from today's logged-out markup (asset diet + current WP script
set), which is why a 2026-08-15/16 count sees the attribute only on
JSON-LD. That is type-set filtering, not proof the snippet authored it.

---

## 3. What this does *not* change

- Schema JSON-LD **content** (brand descriptors remain #735).
- `fixes/schema-snippets.php` (still the inert mu-plugin draft; #741
  deletion/pointer decision stands).
- Live Code Snippet 5. No paste, no activate, no deactivate.

The intended repo wrapper remains:

```html
<script type="application/ld+json">
```

The intended **rendered** wrapper remains:

```html
<script data-jetpack-boost="ignore" type="application/ld+json">
```

---

## 4. Follow-ups recorded elsewhere

- Canonical file header: `fixes/schema-snippets-deployed.php`
- Index: `fixes/README.md`
- Pre-deploy rendered-wrapper check:
  `docs/current-state/SEO-PUBLISHER-SCHEMA-2026-07-19.md`
- Authenticated snippet-body read is still owed for #741. It would
  confirm today's slot bytes; it is not required to explain the wrapper.
