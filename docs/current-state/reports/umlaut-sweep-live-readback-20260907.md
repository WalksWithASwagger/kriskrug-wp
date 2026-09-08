# Live sweep + readback: canonical "Kris Krüg" spelling

**Issue:** none. Ad-hoc request from KK, 2026-09-07. Lineage: the 2026-08-01 voice sweep (EPIC #603) flagged umlaut-less `Kris Krug` as a recurring miss but only remediated two posts.
**Lane:** Track A (live content, media, SEO meta) plus one Track B theme-source mirror.
**Scope approved by KK:** both custom template overrides, plus the "current surface" (all pages, posts id >= 11000, media id >= 11000). The pre-2011 archive was explicitly deferred.
**Method:** authenticated WP REST via `scripts/common.py` `WPClient`, operating on `content.raw` (`context=edit`) so block markup is preserved. Dry-run before every write, read-back after every write, then logged-out cache-bypassed public verification.

## Verdict up front

**The theme file was never the bug.** `theme/kk-aurora/templates/single.html:55` already read `Kris Krüg`, and repo Aurora 1.6.11 matched live Aurora 1.6.11. The live author bio still rendered `Kris Krug` because **`kk-aurora//single` is a `source=custom` DB template override** in `wp_template`, which shadows the theme file. The fix was a REST write, not a theme deploy.

Final authenticated re-scan of the current surface across content, title, excerpt, alt text, and SEO meta: **14 remaining occurrences, all third-party citations, 0 unexpected.**

## Template source audit

`GET /wp-json/wp/v2/templates` returned 8 templates and 3 template parts. Two were custom overrides carrying the wrong spelling; everything else was already clean.

| Template | `source` | Non-umlaut before | Fixed |
|---|---|---|---|
| `kk-aurora//single` | **custom** | 1 (author bio paragraph) | yes |
| `kk-aurora//front-page` | **custom** | 8 (1 hero dek + 7 photo `alt`) | yes |
| `kk-aurora//index`, `//page`, `//home`, `//404`, `//archive-marquee_board`, `//single-marquee_board` | theme | 0 | n/a |
| parts `//header`, `//footer`, `//marquee-current` | theme | 0 | n/a |

## What changed

Pass 1 covered content, title, and alt text. A `/sponsor-deck/` spot-check then exposed two surfaces pass 1 never touched, so pass 2 covered stored excerpts (which Jetpack renders into `og:description`) and Jetpack SEO meta.

| Pass | Surface | Objects | Changes |
|---|---|---|---|
| 1 | Custom templates | 2 | 9 replacements |
| 1 | Pages, `content` + `title` | 17 | 50 replacements |
| 1 | Posts (id >= 11000), `content` + `title` | 13 | 19 replacements |
| 1 | Media `alt_text` (incl. 12098) | 17 | 17 replacements |
| 2 | `jetpack_seo_html_title`, `advanced_seo_description` | 10 | 12 fields |
| 2 | `excerpt` | 4 | 4 fields |

**57 unique objects. 0 read-back mismatches. 0 write failures.**

Notable single items:

- **Media 12098** `01-vancouver-ai-data-centre-protest-editorial`, the item KK named. Alt text now reads `Stylized editorial crop of Kris Krüg and a Vancouver AI data centre protest crowd with Water Not Slop and UBI Before AI signs.` Verified rendering as the featured image on `/2026/09/07/ai-already-campaign-issue-vancouver/`.
- **Ten post `<title>` tags** read `| Kris Krug` before pass 2. Confirmed live, for example `/2026/09/03/what-i-showed-founders-about-ai-workflows/` now emits `What I showed a room of founders about AI workflows | Kris Krüg`.
- **Page 12625 `/sponsor-deck/`** was emitting `Kris Krug` into `og:description`, `<meta name="description">`, and `twitter:description` from a stored **excerpt**, not from page content. This is the surface a content-only sweep silently misses.

## Deliberately left as published

**14 occurrences are third-party headlines quoted verbatim.** Changing them would misquote the citation, which is the same reasoning KK applied to the oEmbed iframe titles.

| Page | Kept | Examples |
|---|---|---|
| 1895 `/publications/` | 11 | Medium `Kris Krug: Technology Game Changer`; YouTube `Are We Done Yet? Kris Krug on AI-Volution`; FOLIO.YVR; Apple Podcasts `Widen the Lens with Kris Krug`; archived 2006-2010 blog titles |
| 2389 `/news/` | 3 | two Georgia Straight `Geek Speak` pieces, one Vancouver Is Awesome |

`/news/` therefore received **zero** edits; all three of its hits were citations.

The applied rule, in `apply_umlaut.py`: an `alt` attribute is always KK's own descriptive copy even when the `<img>` sits inside an external anchor; only anchor **body text** pointing at a non-KK domain is a citation. That distinction mattered. Three occurrences on page 2672 `/work/` and one on 2828 `/motleykrug-podcast/` looked external but were KK's own alt text and his own Beehiiv CTA, so those **were** changed.

Also untouched by instruction: Person schema `alternateName: "Kris Krug"` (deliberate ASCII alternate), and YouTube oEmbed iframe titles. The latter exist only in rendered output, never in `content.raw`, so they cannot regress from a raw write.

## Open item for KK

**Schema `WebSite.name` is still ASCII.** The live Code Snippet (repo copy `fixes/schema-snippets-deployed.php:65`) hardcodes `'site_name' => 'Kris Krug'`, which feeds `WebSite.name` in the JSON-LD on every page. WordPress `settings.title` already reads `Kris Krüg | Generative AI Tools & Techniques`, so the snippet is out of step with the site title. It sits directly above the deliberate `'person_alt' => 'Kris Krug'` on line 72, so it may have been intentional in the same spirit. Changing it is a live Code Snippet deploy and needs its own approval.

## Deferred: pre-2011 archive

Per the approved scope: **93 posts (164 occurrences) and 47 media items** still carry the non-umlaut form. 24 of the media are the repeated `Vancouver Architecture Engineering Construction AI Synths by Kris Krug` batch, a single mechanical find/replace whenever KK wants it.

The judgment calls that kept this tier out of scope: several are post **titles** of historical record (1242 `kris-krug-artist-statement-crowd-sourcing-stylee`, 705 the BitTorrent For Dummies byline, plus 1116, 975, 1001, 1178, 635), and others are third-party quotes and podcast episode names. Slugs must not change in any case; URLs would break.

## Encoding

The site DB is latin1. `ü` is U+00FC, inside latin1, so it round-tripped cleanly. Live renders confirm **0 mojibake (`KrÃ¼g`) and 0 `?` substitution** across every page checked. No NCR entities were needed. See `docs`-adjacent note: NCR entities remain required only for codepoints outside latin1.

## Verification commands

```
# authenticated re-scan, current surface, all five fields
varlock run --inject vars -- python3 verify_final.py
#   CURRENT SURFACE remaining occurrences by kind:  14 citation
#   UNEXPECTED: 0

# logged-out public readback, cache-bypassed
curl -sL "https://kriskrug.co/<path>/?cb=$RANDOM$RANDOM"
```

Repo gate: `scripts/notion-to-wp/.venv/bin/python -m pytest scripts/tests/ -q` -> **660 passed, 227 subtests passed**, including `test_publications_editorial_payload.py` and `test_issue_316_schema_identity.py`.

`make validate` stops at `phpcs not found` (no local `composer install`). Pre-existing environment gap, unrelated to this change; the `php-syntax` step passed `php -l` on all 48 PHP files, and the only repo file touched is HTML.

## Rollback

Full pre-change snapshots were captured before every write and live in the session scratchpad, not the repo: `rollback-snapshots.json` (48 objects, raw content + titles), `rollback-meta-excerpt.json` (13 objects, excerpts + SEO meta), `rollback-media-12098.json`, plus `before-single.html` and `before-front-page.html` for the two template overrides.
