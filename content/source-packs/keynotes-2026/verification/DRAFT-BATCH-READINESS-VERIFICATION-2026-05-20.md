# Draft Batch Readiness Verification - 2026-05-20

Issue: `#99`
Scope: repo-local keynote/source-pack draft batch only. No live WordPress writes, no media uploads, no page updates, no backlink changes.

## Files Verified

Draft folders:

- `content/drafts/2026-05-19-both-hands-full-ai-creatives-lasalle-college/`
- `content/drafts/2026-05-19-inside-vancouvers-ai-boom-whistler-institute/`
- `content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026/`
- `content/drafts/2026-05-19-horizons-ai-models-future-machine-learning/`
- `content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext/`
- `content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage/`

Source-pack files:

- `content/source-packs/keynotes-2026/post-packages/README.md`
- `content/source-packs/keynotes-2026/post-packages/review-ready-draft-batch-2026-05-20.md`

## Structure Check

Each selected draft folder has:

- `post.md`
- `post.html`
- `seo-meta.md`
- `internal-links.md`
- `alt-text.md`
- `publish-gate.md`
- `images/`

Word-count/line-count sanity check showed each package has substantive body copy plus separate SEO, link, image, and publish-gate notes.

## Link Check

Command:

```bash
urls=$(rg --no-filename -o 'https?://[^"`<> )\]]+' \
  content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext \
  content/drafts/2026-05-19-both-hands-full-ai-creatives-lasalle-college \
  content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026 \
  content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage \
  content/drafts/2026-05-19-horizons-ai-models-future-machine-learning \
  content/drafts/2026-05-19-inside-vancouvers-ai-boom-whistler-institute \
  content/source-packs/keynotes-2026/post-packages \
  | sed 's/[`),.;]*$//' \
  | sort -u)
printf '%s\n' "$urls" | while IFS= read -r url; do
  [ -n "$url" ] || continue
  code=$(curl -L -s -o /dev/null -w '%{http_code}' --max-time 20 "$url" || printf 'curl-failed')
  printf '%s %s\n' "$code" "$url"
done
```

Results:

```text
200 https://bc-ai.ca/
200 https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/
200 https://kriskrug.co/about/
200 https://kriskrug.co/contact/
200 https://kriskrug.co/podcast-guesting-page-epk/
200 https://kriskrug.co/recent-projects-include/
200 https://kriskrug.co/services/
200 https://kriskrug.co/speaking/
200 https://www.bothhandsfull.com/
200 https://www.punkrockai.com/
200 https://www.youtube.com/watch?v=-XEsqsEbpoo
200 https://www.youtube.com/watch?v=-c7mgY2aSgM
200 https://www.youtube.com/watch?v=1OcC-0X6Nb8
200 https://www.youtube.com/watch?v=EBGdM6T9Fr8
200 https://www.youtube.com/watch?v=T5ANAthZewE
200 https://www.youtube.com/watch?v=owtSPcpRinI
200 https://www.youtube.com/watch?v=pfecN8_1boA
200 https://www.youtube.com/watch?v=tfXkDhlqnrE
```

## Privacy Scan

Command:

```bash
rg -n -i 'visa|boarding|passport|hotel|whatsapp|phone|tel:|mailto:|app[_ -]?password|application password|token|nonce|secret|private email|@[A-Za-z0-9._%+-]+\.[A-Za-z]{2,}' \
  content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext \
  content/drafts/2026-05-19-both-hands-full-ai-creatives-lasalle-college \
  content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026 \
  content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage \
  content/drafts/2026-05-19-horizons-ai-models-future-machine-learning \
  content/drafts/2026-05-19-inside-vancouvers-ai-boom-whistler-institute \
  content/source-packs/keynotes-2026/post-packages
```

Result: no matches.

## Readiness Verdict

The six selected draft packages satisfy issue `#99` for repo-local readiness:

- title, slug, excerpt, SEO fields, category recommendations, and tag recommendations are present;
- internal-link notes and backlink targets are present;
- image/media decisions and rights/safety notes are present;
- per-package fact-check/privacy checklists are present in `publish-gate.md`;
- link checks passed for all selected public/internal URLs;
- privacy scan returned no matches.

Ready for WP draft? Created on 2026-05-22 after authenticated exact-slug checks and draft-payload review:

- `ai-keynote-chaos-creativity-channelnext` - WP draft `11880`
- `both-hands-full-ai-creatives-lasalle-college` - WP draft `11881`
- `both-hands-full-vancouver-ai-march-2026` - WP draft `11882`
- `dear-ai-bass-coast-brain-stage` - WP draft `11883`
- `horizons-ai-models-future-machine-learning` - WP draft `11884`
- `inside-vancouvers-ai-boom-whistler-institute` - WP draft `11885`

Public publishing, media upload, and live backlinks remain out of scope for this issue until KK review and a rollback note are complete.
