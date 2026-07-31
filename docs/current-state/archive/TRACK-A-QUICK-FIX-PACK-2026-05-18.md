# Track A quick-fix pack — 2026-05-18

**Lane:** Track A — Content + SEO  
**Ownership:** planning artifact only. Do not touch production WordPress from this lane.  
**Sources inspected:** `SITE-AUDIT-2026-05-16.md`, `RESUME-HERE.md`, `fixes/schema-snippets-deployed.php`, `fixes/issue-43-twitter-cards.php`, live unauthenticated `curl` spot checks on 2026-05-18 and 2026-05-19.

## 2026-05-19 read-only refresh

No production writes were made in this refresh.

Still pending:

- Services `<title>` and `og:title` still render without the needed separator: `Generative AI Creative Services &amp; Strategy Kris Krüg | Generative AI Tools &amp; Techniques`.
- `twitter:site` still renders `@feelmoreplants`, and `feelmoreplants` is still present in live HTML.
- Popup Maker `pum-3884` still reports `delay=30000`, `disable_on_mobile=false`, `disable_on_tablet=false`.
- Homepage renders the intended H1, `Kris Krüg, Generative AI for Creative Professionals`, but Catch Responsive also emits an empty `<h1 class="entry-title"></h1>` wrapper.

Still good:

- `/services/` returns `301` to `/generative-ai-services/`, then `200`.
- `/work/` returns `301` to `/recent-projects-include/`, then `200`.
- About, Services, Work, and Speaking each showed one non-empty H1 in the spot check.

## Current live evidence

These checks are read-only and safe to repeat:

```bash
curl -Ls https://kriskrug.co/generative-ai-services/ \
  | perl -0777 -ne 'print "$1\n" if /<title>(.*?)<\/title>/s; print "$1\n" if /<meta property="og:title" content="([^"]+)"/s; print "$1\n" if /<meta name="twitter:site" content="([^"]+)"/s; print "feelmoreplants\n" if /feelmoreplants/; print "pum delay=$1 mobile=$2 tablet=$3\n" if /pum-3884.*?delay\":\"(\d+)\".*?disable_on_mobile\":(\w+).*?disable_on_tablet\":(\w+)/s'

curl -ILs https://kriskrug.co/services/ | rg -i '^(HTTP|location:)'
curl -ILs https://kriskrug.co/work/ | rg -i '^(HTTP|location:)'
curl -ILs http://www.twitter.com/feelmoreplants | sed -n '1,8p'
curl -ILs https://x.com/kriskrug | sed -n '1,8p'
```

Observed 2026-05-18:

- `<title>` and `og:title` still render without a separator between page title and site title: `Generative AI Creative Services &amp; Strategy Kris Krüg | Generative AI Tools &amp; Techniques`.
- `twitter:site` still renders `@feelmoreplants`.
- Old social link `http://www.twitter.com/feelmoreplants` is still present in live HTML and returns HTTP 520 on HEAD.
- Popup Maker `pum-3884` has `delay=30000`, `disable_on_mobile=false`, `disable_on_tablet=false`.
- `/services/` correctly 301s to `/generative-ai-services/`.
- `/work/` correctly 301s to `/recent-projects-include/`.

## 1. P1 title separator Code Snippet

**Goal:** make document titles and Jetpack-derived social titles read as `Page title | Kris Krüg | Generative AI Tools & Techniques`, not `Page title Kris Krüg | Generative AI Tools & Techniques`.

**Install path:** WordPress admin → Code Snippets → Add New. Name it `KK title separator fix`. Set to run on front end only. Paste without the opening `<?php` tag if Code Snippets adds PHP wrapping.

```php
<?php
/**
 * KK title separator fix.
 *
 * Catch Responsive / Jetpack currently concatenate the page title and site
 * title without a delimiter. Keep this as a front-end-only Code Snippet until
 * Aurora owns document titles natively.
 */
function kk_title_separator_primary_title() {
    if (is_singular()) {
        return single_post_title('', false);
    }

    if (is_category() || is_tag() || is_tax()) {
        return single_term_title('', false);
    }

    if (is_author()) {
        return get_the_author();
    }

    if (is_search()) {
        return sprintf('Search results for "%s"', get_search_query());
    }

    if (is_404()) {
        return 'Page not found';
    }

    if (is_archive()) {
        return wp_strip_all_tags(get_the_archive_title());
    }

    return '';
}

add_filter('pre_get_document_title', function ($title) {
    if (is_admin()) {
        return $title;
    }

    $site_name = get_bloginfo('name');
    $tagline = get_bloginfo('description');

    if (is_front_page() || is_home()) {
        return $tagline ? $site_name . ' | ' . $tagline : $site_name;
    }

    $primary = kk_title_separator_primary_title();

    return $primary ? $primary . ' | ' . $site_name : $title;
}, 99);
```

**Preflight:**

```bash
curl -Ls https://kriskrug.co/generative-ai-services/ \
  | perl -0777 -ne 'print "$1\n" if /<title>(.*?)<\/title>/s; print "$1\n" if /<meta property="og:title" content="([^"]+)"/s'
```

**Verification after activating snippet:**

```bash
curl -Ls https://kriskrug.co/generative-ai-services/ \
  | perl -0777 -ne 'print "$1\n" if /<title>(.*?)<\/title>/s; print "$1\n" if /<meta property="og:title" content="([^"]+)"/s'

curl -Ls https://kriskrug.co/about/ \
  | perl -0777 -ne 'print "$1\n" if /<title>(.*?)<\/title>/s'

curl -Ls https://kriskrug.co/ \
  | perl -0777 -ne 'print "$1\n" if /<title>(.*?)<\/title>/s'
```

Expected:

- Services page: `Generative AI Creative Services & Strategy | Kris Krüg | Generative AI Tools & Techniques`
- About page: `Techartist, quasi-sage, cyberpunk anti-hero from the future. | Kris Krüg | Generative AI Tools & Techniques`
- Homepage remains readable and does not duplicate the tagline.

**Rollback:** deactivate or delete the `KK title separator fix` Code Snippet, purge Pagely/cache if needed, re-run the verification curl. Titles should return to pre-snippet behavior.

## 2. P1 Twitter/X replacement

**Goal:** replace legacy `twitter.com/feelmoreplants` links with `https://x.com/kriskrug`. The deployed schema already uses `twitter.com/kriskrug` and `x.com/kriskrug`; this fix targets inline links and theme/social widget settings that still expose `feelmoreplants`.

**Preferred if WP-CLI is available on the production host:**

```bash
wp search-replace 'http://www.twitter.com/feelmoreplants' 'https://x.com/kriskrug' --all-tables-with-prefix --dry-run
wp search-replace 'https://www.twitter.com/feelmoreplants' 'https://x.com/kriskrug' --all-tables-with-prefix --dry-run
wp search-replace 'http://twitter.com/feelmoreplants' 'https://x.com/kriskrug' --all-tables-with-prefix --dry-run
wp search-replace 'https://twitter.com/feelmoreplants' 'https://x.com/kriskrug' --all-tables-with-prefix --dry-run
wp search-replace '@feelmoreplants' '@kriskrug' --all-tables-with-prefix --dry-run
```

If counts look reasonable, repeat the same commands without `--dry-run`.

**Admin fallback if WP-CLI is not available:**

1. Appearance → Customize or theme social settings: update Twitter URL to `https://x.com/kriskrug`.
2. Jetpack or sharing/social settings: update Twitter handle from `@feelmoreplants` to `@kriskrug`.
3. Use a search-replace plugin only if it supports dry-run and serialized data.

**Verification:**

```bash
curl -Ls https://kriskrug.co/ | rg -n 'feelmoreplants|twitter.com/feelmoreplants|x.com/kriskrug|@kriskrug'
curl -Ls https://kriskrug.co/about/ | rg -n 'feelmoreplants|twitter.com/feelmoreplants|x.com/kriskrug|@kriskrug'
curl -Ls https://kriskrug.co/generative-ai-services/ | rg -n 'feelmoreplants|twitter.com/feelmoreplants|x.com/kriskrug|@kriskrug'
curl -ILs https://x.com/kriskrug | sed -n '1,8p'
```

Note: X may return 403/anti-bot responses to HEAD requests. The key regression check is that `feelmoreplants` no longer appears in site HTML and the public target URL is KK's current handle.

**Rollback:** run the inverse `wp search-replace` only for the exact patterns changed, or restore the affected theme/social widget settings from the preflight notes. Do not blanket-replace `kriskrug` with `feelmoreplants`.

## 3. P2 broken-link scan

**Goal:** produce a triage CSV of dead outbound links without leaving a heavy scanner running indefinitely.

**Recommendation:** use Broken Link Checker as a one-shot admin tool, then disable it after export. The May 17 sample found 13-30% dead or suspicious external links on older pages, which is enough to justify a full scan.

**Admin sequence:**

1. Plugins → Add New → install `Broken Link Checker` by WPMU DEV.
2. Run the scan against posts, pages, and comments if comments are enabled.
3. Export CSV of broken links.
4. Triage manually into:
   - replace URL,
   - unlink anchor text,
   - ignore HEAD-blocked but browser-valid target,
   - archive/link to Wayback.
5. Disable the plugin after cleanup to avoid background cron overhead.

**Optional CLI-safe one-shot inventory before plugin install:**

```bash
curl -Ls https://kriskrug.co/wp-json/wp/v2/pages?per_page=100 \
  | jq -r '.[] | [.link, .title.rendered] | @tsv'

curl -Ls https://kriskrug.co/wp-json/wp/v2/posts?per_page=100 \
  | jq -r '.[] | [.link, .title.rendered] | @tsv'
```

**Verification:**

```bash
curl -Ls https://kriskrug.co/events/ | rg -o 'https?://[^"'\'' <)]+' | sort -u | wc -l
curl -Ls https://kriskrug.co/motleykrug-podcast/ | rg -o 'https?://[^"'\'' <)]+' | sort -u | wc -l
curl -Ls https://kriskrug.co/recent-projects-include/ | rg -o 'https?://[^"'\'' <)]+' | sort -u | wc -l
```

Success is not "zero broken links" immediately. Success is an exported CSV, high-confidence fixes applied first, and plugin disabled afterward.

**Rollback:** if the plugin causes admin slowness, deactivate it. If link edits regress content, restore the individual post/page revision in WordPress rather than broad database rollback.

## 4. P1 mobile popup recommendation

**Current state:** Popup Maker `pum-3884` auto-opens after 30 seconds and is enabled on mobile/tablet. That is better than the old 1-second desktop interruption, but it can fire mid-scroll on long mobile posts.

**Recommendation:** disable this popup on mobile and tablet for the current Catch Responsive theme. Let post bylines/internal links carry mobile conversion until Aurora can provide a more native newsletter placement.

**Admin sequence:**

1. Popup Maker → All Popups → `BEEHIIV POPUP`.
2. Display or targeting settings: enable "Disable on mobile" and "Disable on tablet" if available.
3. Keep the close cookie suppression at 1 month.
4. Keep desktop delay at 30 seconds unless KK wants to test scroll-trigger later.

**Verification:**

```bash
curl -Ls https://kriskrug.co/ \
  | perl -0777 -ne 'print "delay=$1 mobile=$2 tablet=$3\n" if /pum-3884.*?delay\":\"(\d+)\".*?disable_on_mobile\":(\w+).*?disable_on_tablet\":(\w+)/s'
```

Expected after change:

```text
delay=30000 mobile=true tablet=true
```

**Rollback:** uncheck the mobile/tablet disable settings and save. Re-run the curl check; expected rollback is `mobile=false tablet=false`.

## 5. Remaining P0/P1 current-site checks

These are the remaining high-signal checks for the current Catch Responsive site. None require theme changes.

| Priority | Check | Current evidence | Recommendation | Verification |
|---|---|---|---|---|
| P0 | Homepage hero/H1 and About H1 repairs | `RESUME-HERE.md` says shipped and verified on 2026-05-16 | No action unless live check regresses | `curl -Ls https://kriskrug.co/ | rg -n '<h1|Why Choose Me'; curl -Ls https://kriskrug.co/about/ | rg -n '<h1'` |
| P1 | `/services/` redirect | Live 2026-05-18: `301 location: /generative-ai-services/` then `200` | No action | `curl -ILs https://kriskrug.co/services/ | rg -i '^(HTTP|location:)'` |
| P1 | `/work/` redirect | Live 2026-05-18: `301 location: /recent-projects-include/` then `200` | No action now. Later, consider renaming `/recent-projects-include/` to `/work/` during a planned URL cleanup. | `curl -ILs https://kriskrug.co/work/ | rg -i '^(HTTP|location:)'` |
| P1 | Services/events/podcast/projects H1 hierarchy | May 17 audit: all four pages have exactly one H1 | Re-check after any editor changes | `for u in generative-ai-services events motleykrug-podcast recent-projects-include; do echo "$u"; curl -Ls "https://kriskrug.co/$u/" | rg -c '<h1'; done` |
| P1 | Mobile popup | Live 2026-05-18: enabled on mobile/tablet | Disable mobile/tablet variant now, revisit in Aurora | Popup verification command above |
| P1 | Title separator | Live 2026-05-18: still malformed | Add Code Snippet above | Title verification command above |
| P1 | Twitter/X | Live 2026-05-18: `feelmoreplants` still appears | Search-replace and social settings update | Twitter verification command above |

## Recommended execution order

1. Take/confirm fresh backup before production writes.
2. Add and verify `KK title separator fix`.
3. Dry-run Twitter/X replacements, then run them if counts are sane.
4. Disable Popup Maker on mobile/tablet.
5. Run Broken Link Checker as a one-shot scan; export CSV; disable plugin.
6. Update `RESUME-HERE.md` only after the production session actually completes.
