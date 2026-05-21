# Issue #68 Work Page Verification - 2026-05-21

Issue: https://github.com/WalksWithASwagger/kriskrug-wp/issues/68

## Status

Prepared for human/live review. No live WordPress write, media upload, theme edit, or production activation was made in this pass.

## Scope

- Updated payload: `content/source-packs/keynotes-2026/wp-payloads/work.html`
- Updated metadata pointer: `content/source-packs/keynotes-2026/wp-payloads/page-meta.json`
- Verification note: `content/source-packs/keynotes-2026/verification/ISSUE-68-WORK-PAGE-VERIFICATION-2026-05-21.md`
- Out of scope and not edited: About, Speaking, Home, Services, live WP, theme files.

## Target

- Page ID: `2672`
- Current slug: `recent-projects-include`
- Proposed title in metadata: `Work`
- Public URL: `https://kriskrug.co/recent-projects-include/`
- Redirect URL: `https://kriskrug.co/work/` redirects to `/recent-projects-include/`
- Proposed SEO title: `Work | Kris Krüg`
- Proposed SEO description: `Explore Kris Krüg's work across BC+AI, Indigenomics AI, The Upgrade AI, keynote portals, photography, community infrastructure, and visual storytelling.`

## Audit Summary

The existing source-pack payload already covered the Work page, BC+AI, The Upgrade AI, keynote/public artifact portals, and a photography/archive layer. The remaining issue #68 gap was that Indigenomics AI was not present on the Work payload and the major current-project cards needed clearer impact, outcomes, and direct links.

## What Changed

- Added Indigenomics AI to the hero proof row and Featured work project layer.
- Expanded BC+AI with Executive Director positioning, current public metrics, outcome framing, and links to BC+AI plus the local founding note.
- Expanded Indigenomics AI with CTO positioning, sovereign-data/economic-technology framing, `$100B` Indigenous economy context, and links to Indigenomics.ai plus Kris's public project story.
- Expanded The Upgrade AI with Peter Bittner co-founder credit, training/coaching/cohort outcomes, and links to The Upgrade AI plus Services.
- Reframed the photography proof as `Photography credential`, with National Geographic, Rolling Stone, and Getty Images proof called out as background credibility rather than the main offer.
- Updated the Work SEO description in `page-meta.json` so Indigenomics AI and The Upgrade AI appear in the metadata.

## Acceptance Map

| Criterion | Status | Evidence |
|---|---:|---|
| Current projects content extracted | Done | `page-meta.json` maps page `2672`, slug `recent-projects-include`, title `Work`, content file `work.html`. Public read check returned `200`; `/work/` returned `301` then `200`. |
| Work page structured with the requested project spine | Done | Hero proof row names BC+AI, Indigenomics AI, The Upgrade AI, and Photography. Featured work now carries BC+AI, Indigenomics AI, and The Upgrade AI as current project cards; photography appears as a credential card under `How the work shows up`. |
| BC+AI section complete with metrics | Done | BC+AI card includes Executive Director role, `250+ members`, `3,000+ event attendees`, `94+ events`, `4 BC regions`, an outcome statement, and links. |
| Indigenomics section with CTO positioning | Done | Indigenomics AI card includes CTO language, sovereign data, Indigenous economic sovereignty, `$100B` economy context, and project links. |
| The Upgrade AI section with co-founder credit | Done | The Upgrade AI card names Peter Bittner and includes courses, coaching, team trainings, certification cohorts, outcomes, and links. |
| Photography as credential only | Done | Photography is in the proof row and credential card, not the main offer, and the archive remains supporting proof. |
| Each major section has description, impact, outcomes, links | Done | BC+AI, Indigenomics AI, and The Upgrade AI cards each include narrative description, `Impact`, `Outcome`, and link rows. Photography includes credential proof and remains supported by archive links. |
| Mobile responsive | Locally ready | Existing auto-fit grids and mobile media queries are retained; `h2=6`, `img=17`, `links=26`, `external=27` after edits. Full browser/mobile QA belongs to the live/staging review pass. |
| Professional presentation | Done | The payload keeps the existing Work page visual system and adds content without changing theme files. |
| Ready for publication | Prepared | JSON, content markers, URL checks, privacy scan, and `git diff --check` passed locally. Live publish still needs backup/snapshot and human approval per repo rules. |

## Source Grounding Notes

- BC+AI public evidence supports `250+` members, `3,000+` event attendees, `94+` events, and `4` BC regions. This avoids the older issue text's stale `2,000+ members` wording.
- Indigenomics AI public/source-backed framing supports the `$100B` Indigenous economy vision. `https://indigenomics.ai/` returned `200` but served a small JavaScript lander shell, so the payload also links to the substantive kriskrug.co Indigenomics AI story.
- The Upgrade AI public site returned `200` and supports live/on-demand courses, coaching, team trainings, and cohort framing.
- Photography proof is grounded in the About payload/source proof lists that name National Geographic, Rolling Stone, and Getty Images.

## Checks Run

```bash
gh issue view 68 --json number,title,state,body,labels,url
python3 -m json.tool content/source-packs/keynotes-2026/wp-payloads/page-meta.json >/dev/null
rg -n "BC\\+AI|BC \\+ AI|Indigenomics AI|Indigenomics\\.ai|The Upgrade AI|Peter Bittner|Photography credential|National Geographic|Rolling Stone|Getty Images|250\\+|3,000\\+|94\\+|\\$100B|Visit Indigenomics\\.ai|Visit The Upgrade AI|Read the founding note" content/source-packs/keynotes-2026/wp-payloads/work.html content/source-packs/keynotes-2026/wp-payloads/page-meta.json
rg -n -i "visa|boarding|passport|hotel|phone|whatsapp|[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}|notion\\.s3|amazonaws|X-Amz|wpcomstaging|password|secret|token" content/source-packs/keynotes-2026/wp-payloads/work.html content/source-packs/keynotes-2026/wp-payloads/page-meta.json
perl -ne 'while(/https?:\\/\\/[^\"< )]+/g){print "$&\\n"}' content/source-packs/keynotes-2026/wp-payloads/work.html | perl -pe 's/&amp;/&/g' | sort -u | while IFS= read -r url; do curl -L -o /dev/null -s -w "%{http_code} %{content_type} %{url_effective}\\n" --max-time 20 "$url"; done
printf '%s\\n' 'https://kriskrug.co/2025/05/18/bc-ai-is-live-and-were-building-the-future-we-actually-want/' 'https://kriskrug.co/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/' 'https://kriskrug.co/services/' 'https://kriskrug.co/speaking/' 'https://kriskrug.co/contact/' 'https://kriskrug.co/about/' 'https://kriskrug.co/blog/' | while IFS= read -r url; do curl -L -o /dev/null -s -w "%{http_code} %{url_effective}\\n" --max-time 20 "$url"; done
ruby -e 's=File.read("content/source-packs/keynotes-2026/wp-payloads/work.html"); puts({h2:s.scan(/<h2\\b/i).size,img:s.scan(/<img\\b/i).size,links:s.scan(/<a\\b/i).size,external:s.scan(%r{https?://}).size}.map{|k,v| "#{k}=#{v}"}.join(" "))'
git diff --check
```

Results:

- Issue `#68` is open and matches this acceptance lane.
- `page-meta.json` parsed successfully.
- Marker checks found BC+AI, Indigenomics AI, The Upgrade AI, Peter Bittner, photography credential proof, metrics, `$100B`, and key links.
- Sensitive-string scan returned no matches.
- External Work payload URLs and image URLs returned `200`.
- Internal kriskrug.co URLs used by new link rows returned `200`; `/services/` resolved to `/generative-ai-services/`.
- `git diff --check` passed.

## Publish Gate

Before applying this payload to live WordPress:

1. Take the required fresh backup/restore proof or stop.
2. Snapshot page ID `2672` to rollback JSON and HTML.
3. Verify REST target identity before PATCH: `id=2672`, slug `recent-projects-include`, title `Work`, status `publish`.
4. Apply only `work.html` plus the Work entry metadata from `page-meta.json`.
5. Read back title, slug, status, comment/ping settings, SEO metadata, and content markers.
6. Browser-check desktop and mobile for the Work page and `/work/` redirect.

## Closeout Recommendation

Issue `#68` can be closed after human/live review confirms the prepared payload is acceptable and the live WordPress page has been updated/read back successfully. Locally, the content-pack acceptance criteria are satisfied.
