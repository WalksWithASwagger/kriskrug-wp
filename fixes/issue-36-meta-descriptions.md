# Issue #36: Unique Meta Descriptions

**Track:** A - Content + SEO
**Status:** review-ready copy pack; not live-deployed from this file.
**Last reviewed:** 2026-05-21 by Worker #36.

## Assumptions and Success Criteria

- The site already renders meta descriptions through Jetpack/WordPress metadata. This issue is a targeted refresh, not a blank-slate code install.
- `content/source-packs/keynotes-2026/wp-payloads/page-meta.json` is the freshest repo-side page-meta source for the 2026 key page overhaul.
- Live WordPress writes remain blocked until backup/restore proof is current or KK explicitly approves a narrower rollback path.
- Do not add a `functions.php`, Code Snippets, Yoast, Rank Math, or SEOPress path just for this issue while Jetpack is already emitting metadata.
- Done means each deployed target renders exactly one standard `<meta name="description">`, the value is unique, roughly 150-160 characters, natural-language keyworded, and verified from public HTML after the admin/REST update.

## Existing Artifact Audit

| Source | Finding | Action |
|---|---|---|
| `fixes/issue-36-meta-descriptions.md` before this update | Contained good topic direction but stale implementation advice. Several descriptions were actually 189-221 characters despite being labeled 150-160, and the PHP/Yoast guidance could create duplicate meta output. | Replaced with this review/deploy artifact. |
| `content/source-packs/keynotes-2026/wp-payloads/page-meta.json` | Contains Jetpack SEO titles and `advanced_seo_description` values for homepage, Speaking, Work, Services, About, and Podcast EPK. Current lengths range from 133-180 characters. | Use as the primary source for target identity, then trim where needed. |
| `docs/current-state/SEO_AUDIT.md` | Says audited pages already have meta descriptions and Jetpack appears to own the SEO/Open Graph layer. | Refresh existing values through the owning meta surface; do not add another generator. |
| `docs/current-state/TRACK-A-SEO-SOCIAL-PREP-2026-05-18.md` | Warns that #36 should be narrowed to Jetpack description refresh after current-value readback. | Keep the same deployment rule here. |
| `docs/current-state/FIXES-LIVE-RECONCILIATION-2026-05-20.md` | Marks this artifact as needing review before introducing another SEO source. | This file is now the reviewed copy sheet, not a deploy mechanism. |

## Ready Review/Deploy Table

Use these values as the proposed final copy. Length is counted as Unicode characters.

| Target | Page ID / slug | Current live readback | Proposed meta description | Chars | Deploy note |
|---|---:|---|---|---:|---|
| Homepage | `3930` / `/` | Standard meta was generic and 246 chars on 2026-05-21. | Kris Krüg bridges art, AI, Indigenous wisdom, and justice through BC+AI, Indigenomics AI, The Upgrade AI, keynote speaking, and community-first technology. | 155 | Matches the prepared homepage value in `page-meta.json`; deploy when homepage meta is refreshed. |
| About | `1208` / `/about/` | Standard meta matched `page-meta.json` but was 181 chars on 2026-05-21. | Meet Kris Krüg, an AI keynote speaker, creative technologist, photographer, and community builder working across BC+AI, AI education, and human-centered tech. | 158 | Trimmed from the current `page-meta.json` copy while preserving the page intent. |
| Speaking | `1887` / `/speaking/` | Standard meta matched `page-meta.json` but was 179 chars on 2026-05-21. | Book Kris Krüg for AI keynotes, workshops, podcast guesting, moderation, hosting, and emcee work on creativity, community, and responsible technology. | 150 | Trimmed from the current `page-meta.json` copy. |
| Work | `2672` / `/recent-projects-include/` | Standard meta matched `page-meta.json` but was 134 chars on 2026-05-21. `/work/` redirects here. | Explore Kris Krüg's work across BC+AI, keynote systems, community infrastructure, creative technology, training, visual storytelling, and media projects. | 153 | Keep slug unchanged for this pass unless the separate Work URL/canonical issue is approved. |
| Services | `2666` / `/generative-ai-services/` | Standard meta appeared auto-excerpted and 391 chars on 2026-05-21. | AI strategy, responsible AI consulting, BC+AI community building, The Upgrade AI training, Indigenomics advisory, and keynote/workshop support with Kris Krüg. | 158 | Uses the prepared services value from `page-meta.json`; live page may still need the services source-pack refresh. |
| Podcast EPK | `3609` / `/podcast-guesting-page-epk/` | Standard meta matched `page-meta.json` and was 153 chars on 2026-05-21. | Book Kris Krug for podcasts, interviews, broadcasts, panels, hosting, and emcee work on AI, creativity, community, media, ethics, and the future of work. | 153 | Already in target range; verify duplicate-free rendering before closing. |
| Blog | `2316` / `/blog/` | Standard meta was the same generic 246-char homepage-style copy on 2026-05-21. | Read Kris Krüg's field notes on responsible AI, creative technology, community building, Indigenous tech, media, culture, practical workflows, and events. | 154 | Add through the owning page/blog-index meta surface; confirm Jetpack supports the posts page field. |
| Contact | `2418` / `/contact/` | Standard meta was a 289-char body excerpt on 2026-05-21. | Contact Kris Krüg for AI keynotes, workshops, consulting, podcast guesting, community strategy, media projects, partnerships, or creative collaboration. | 152 | Replace the excerpt-style current value with action-oriented contact copy. |

## Not Deploy-Ready From This Issue

| Draft surface | Why it is parked |
|---|---|
| Vancouver AI Community | Current page inventory does not show a canonical owned `/vancouver-ai/`, `/bc-ai/`, or `/vancouver-ai-meetup/` landing page. `docs/current-state/CONTENT_AUDIT.md` recommends future pages for these topics, so do not paste the old draft into an unrelated page. |
| Photography Portfolio | Current page inventory does not show a canonical `/portfolio/` page. Work currently covers photography/media. Resolve the target URL before writing page-specific metadata. |

## Deployment Guidelines

1. Start only after the backup/restore proof gate is satisfied or KK approves a narrower rollback path.
2. Capture current values from public HTML before editing.
3. Edit the existing owning metadata field only: Jetpack SEO fields in wp-admin, or `meta.advanced_seo_description` if an approved REST payload path is being used.
4. Keep the metadata owner singular. Do not activate a PHP snippet or SEO plugin migration unless Jetpack SEO/Open Graph ownership is intentionally disabled first.
5. For `/recent-projects-include/`, verify both the canonical page and `/work/` redirect behavior; do not change the slug in this issue.
6. For `/blog/`, confirm whether WordPress/Jetpack stores the posts page description on page `2316` or through a global archive setting before writing.

## Verification Checklist

Before edit:

```bash
for url in \
  https://kriskrug.co/ \
  https://kriskrug.co/about/ \
  https://kriskrug.co/speaking/ \
  https://kriskrug.co/recent-projects-include/ \
  https://kriskrug.co/work/ \
  https://kriskrug.co/generative-ai-services/ \
  https://kriskrug.co/podcast-guesting-page-epk/ \
  https://kriskrug.co/blog/ \
  https://kriskrug.co/contact/
do
  printf '\n### %s\n' "$url"
  curl -ILs "$url" | rg -i '^(HTTP|location:)'
  curl -Ls "$url" \
    | perl -MHTML::Entities=decode_entities -0777 -ne 'while(/<meta\s+(?:name|property)=["'\''](description|og:description|twitter:description)["'\'']\s+content=["'\'']([^"'\'']*)["'\'']/gi){$d=decode_entities($2); print "$1\t".length($d)."\t$d\n"}'
done
```

After edit:

- [ ] Each target URL returns `200`, except `/work/` may redirect intentionally to `/recent-projects-include/`.
- [ ] Each canonical target renders exactly one `<meta name="description">`.
- [ ] The rendered standard meta description matches the approved copy above.
- [ ] Each approved copy remains unique across the target set.
- [ ] Each rendered value remains in the 150-160 character target range unless KK explicitly accepts a variance.
- [ ] `og:description` and `twitter:description`, when present, do not contradict the standard description.
- [ ] No Yoast/Rank Math/SEOPress/Code Snippet duplicate meta generator has been introduced.
- [ ] Browser share preview checks are run for homepage, Speaking, Work, Services, Blog, and Contact after cache clears.
- [ ] `git diff --check` passes for this repo-side artifact.

## Closeout Status

This artifact is ready for human review and a future deploy session. Issue #36 should not be closed from repo changes alone; it needs live WordPress readback after the metadata is applied and rendered without duplicates.
