# Track A SEO/social prep for issues #36 and #43 - 2026-05-18

**Lane:** Track A - Content + SEO
**Scope:** implementation notes only; no production writes, no theme edits.
**Issues:** #36 unique meta descriptions, #43 Twitter/X card tags.

## Assumptions and success criteria

- This prep note is the only SEO/social file in this lane.
- Production remains untouched from this branch.
- Any later production session starts with read-only preflight checks and a change-appropriate rollback path; full backup is for higher-risk/bulk work, not an ordinary-content blocker.
- Jetpack is treated as the current meta, Open Graph, and Twitter-card owner unless admin verification proves otherwise.
- Success for this note means future implementers can decide what to apply, what to skip, and what evidence closes each issue.

## What is already prepared

### Issue #36

- `fixes/issue-36-meta-descriptions.md` contains draft descriptions for eight page surfaces: homepage, About, Services/Work, Blog/Insights, Contact, Vancouver AI Community, Photography Portfolio, and Speaking.
- `docs/current-state/SEO_AUDIT.md` says all inspected pages already had meta descriptions, though quality and length were mixed.
- The audit identifies Jetpack SEO Tools as the likely current surface for per-page descriptions. There is no confirmed dedicated SEO plugin in use.

### Issue #43

- `fixes/issue-43-twitter-cards.php` contains a PHP snippet intended to output Twitter card metadata.
- `docs/current-state/SEO_AUDIT.md` says Open Graph tags are present site-wide and `twitter:card` is present on most audited pages through Jetpack.
- The remaining audit gap is narrower than the issue title: the blog index was missing `twitter:card` and canonical, and social image/handle quality needed cleanup.
- `docs/current-state/TRACK-A-QUICK-FIX-PACK-2026-05-18.md` adds fresher live evidence: `twitter:site` still rendered as `@feelmoreplants`, and old `twitter.com/feelmoreplants` links still appeared in live HTML on 2026-05-18.

## Redundant or risky

### Issue #36

- The issue is not a blank-slate "add meta descriptions" task. The audited pages already have descriptions, so the safe implementation is a targeted refresh after current-value readback.
- The prepared descriptions are not deploy-ready as labeled. A UTF-8 character count of the eight code-block descriptions reads about 189-221 characters, not the stated 150-160.
- Several claims need owner/source verification before publication, including current roles, organizational names, "2,000+ community members", "250+ monthly attendees", and Fortune 500/Indigenous organization positioning.
- Adding descriptions through `functions.php` or a front-end Code Snippet would risk duplicate `<meta name="description">` output while Jetpack is already emitting metadata.
- Installing Yoast solely for this issue is too broad. If a future SEO plugin migration happens, Jetpack SEO/Open Graph ownership must be disabled or intentionally superseded first.

### Issue #43

- The PHP snippet is mostly redundant with Jetpack on singular pages where Jetpack already emits Open Graph and Twitter tags.
- The snippet does not fix the exact blog-index gap from the audit because it returns early unless `is_singular()` or `is_front_page()` is true.
- The snippet ships with `@YourTwitterHandle` placeholders and should not be activated as-is.
- The fallback logo path can set `$twitter_image` without defining `$image_id`, then later use `$image_id` for `twitter:image:alt`.
- `substr()` can split multibyte text and is not ideal for site copy that includes names like Kris Krug.
- Installing the snippet in theme `functions.php` is not appropriate for Track A. Theme files are out of scope on `main`, and this repo is not a live theme mirror.

## No-live-write verification plan

Run these from any shell with network access before any admin edits. They are read-only and do not require credentials.

### 1. Confirm target URLs before treating issue #36 copy as page-specific

Use confirmed audit URLs first, then resolve the Vancouver AI and Photography targets before applying those two drafts.

```bash
for url in \
  https://kriskrug.co/ \
  https://kriskrug.co/about/ \
  https://kriskrug.co/generative-ai-services/ \
  https://kriskrug.co/blog/ \
  https://kriskrug.co/contact/ \
  https://kriskrug.co/speaking/
do
  echo "### $url"
  curl -ILs "$url" | rg -i '^(HTTP|location:)'
done
```

### 2. Read current SEO/social descriptions without changing them

```bash
for url in \
  https://kriskrug.co/ \
  https://kriskrug.co/about/ \
  https://kriskrug.co/generative-ai-services/ \
  https://kriskrug.co/blog/ \
  https://kriskrug.co/contact/ \
  https://kriskrug.co/speaking/
do
  echo "### $url"
  curl -Ls "$url" \
    | perl -0777 -ne 'print "meta: $1\n" if /<meta name="description" content="([^"]*)"/s; print "og: $1\n" if /<meta property="og:description" content="([^"]*)"/s; print "twitter: $1\n" if /<meta name="twitter:description" content="([^"]*)"/s'
done
```

Expected pre-implementation evidence:

- exactly one standard meta description per target page,
- no duplicate metadata from competing SEO systems,
- current values captured before deciding whether the draft copy is an improvement.

### 3. Read current Twitter/X card state without changing it

```bash
for url in \
  https://kriskrug.co/ \
  https://kriskrug.co/about/ \
  https://kriskrug.co/generative-ai-services/ \
  https://kriskrug.co/blog/
do
  echo "### $url"
  curl -Ls "$url" \
    | rg -n 'Jetpack Open Graph|twitter:card|twitter:site|twitter:creator|twitter:title|twitter:description|twitter:image|feelmoreplants|x.com/kriskrug|twitter.com/kriskrug|rel="canonical"'
done
```

Expected pre-implementation evidence:

- Jetpack remains the active social-meta layer.
- Singular pages already have Twitter card tags.
- `/blog/` is checked separately for the missing card/canonical finding.
- `feelmoreplants` occurrences are inventoried before any search-replace or admin setting change.

### 4. Only after a separate authorized production session

Use the same commands before and after any approved admin change. Do not activate the issue #43 PHP snippet unless Jetpack social metadata has been intentionally disabled or proven absent. Do not add issue #36 descriptions through code while Jetpack is still outputting `<meta name="description">`.

## Recommended issue outcomes

### Issue #36

Recommended outcome: keep the issue, but narrow it to "verify and refresh Jetpack page meta descriptions" instead of "add missing descriptions."

Close #36 only when:

- each target URL has exactly one meta description,
- the value is unique and intentionally written for that page,
- the final copy is trimmed and fact-checked,
- no new SEO plugin or code snippet creates duplicate meta tags.

Do not close #36 by deploying the current `functions.php` example. Treat the existing file as copy draft material, not an implementation plan.

### Issue #43

Recommended outcome: mark the current PHP-snippet approach as superseded/redundant, then close or re-scope the issue based on read-only evidence.

Close #43 if:

- Jetpack already emits valid Twitter card tags for the intended share pages,
- `twitter:site` and `twitter:creator` use the current KK handle,
- stale `feelmoreplants` links/handles are removed through admin settings or a dry-run-verified search-replace,
- the blog index gap is either fixed through the owning meta layer or split into a smaller follow-up.

Do not close #43 by activating `fixes/issue-43-twitter-cards.php` as-is. The safer Track A work is handle cleanup plus targeted verification, not adding a second social-meta generator.
