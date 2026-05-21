# Issue 18 Vancouver AI Community Page Verification - 2026-05-21

## Scope

- Worker lane: Issue `#18` Vancouver AI community page.
- Allowed write scope honored:
  - Added `content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html`.
  - Added this verification note.
- No live WordPress writes, media uploads, theme edits, Aurora activation, or shared metadata edits were performed.
- Work, Home, Speaking, About, and shared `page-meta.json` were not edited.

## Target Recommendation

- Proposed page title: `Vancouver AI Community`
- Proposed slug: `vancouver-ai-community`
- Proposed URL after draft creation: `https://kriskrug.co/vancouver-ai-community/`
- Proposed WordPress status: `draft` until backup/restore proof and KK review are complete.
- Proposed content payload: `content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html`

## Source Grounding

- Existing source pack identifies Vancouver AI March 2026 as one of the strongest immediate speaking-authority proof points.
- Local package used: `content/source-packs/keynotes-2026/post-packages/vancouver-ai-march-2026-both-hands-full.md`.
- Local video metadata used: `content/source-packs/keynotes-2026/video-research/metadata/vancouver-ai-march-2026-appearance.json`.
- Local public-video draft used for tone and source alignment: `content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026/post.md`.
- Existing page payloads already position Kris as a BC+AI / Vancouver AI community builder in:
  - `content/source-packs/keynotes-2026/wp-payloads/about.html`
  - `content/source-packs/keynotes-2026/wp-payloads/work.html`
  - `content/source-packs/keynotes-2026/wp-payloads/speaking.html`
  - `content/source-packs/keynotes-2026/wp-payloads/homepage-hero.html`
- Current live BC+AI homepage source on 2026-05-21 exposed:
  - `250+` Members
  - `3,000+` Event Attendees
  - `94+` Events Hosted
  - `4` BC Regions
  - `Est. 2023` Community Founded

## Content Prepared

- Built a standalone, paste-ready WordPress HTML payload with scoped CSS.
- Added a page hero for Vancouver AI as a public AI-learning and community room.
- Added CTAs to:
  - `https://luma.com/vancouver-ai`
  - `https://bc-ai.ca/membership/`
  - `/speaking/`
- Added BC+AI public stats that were rechecked live in this pass.
- Added sections for:
  - why the room exists
  - what happens in the community
  - the public March 2026 Vancouver AI talk
  - ways to attend, join, partner, or book Kris
  - related starting points
- Embedded the public Vancouver AI YouTube video with a standard iframe:
  - `https://www.youtube.com/embed/T5ANAthZewE`
- Kept audience/person references general; no private attendee names from transcript material were published into the payload.

## SEO And Social Metadata Recommendation

Do not edit shared metadata until the WordPress draft exists and the target page ID is known. Recommended values for the live/draft creation lane:

```json
{
  "slug": "vancouver-ai-community",
  "title": "Vancouver AI Community",
  "comment_status": "closed",
  "ping_status": "closed",
  "content_file": "vancouver-ai-community.html",
  "meta": {
    "jetpack_seo_html_title": "Vancouver AI Community | Kris Krüg",
    "advanced_seo_description": "Vancouver AI community page for BC+AI gatherings, public AI literacy, member pathways, the March 2026 Both Hands Full talk, and ways to attend, join, partner, or book Kris Krüg."
  }
}
```

Recommended excerpt:

> Vancouver AI is where artists, founders, educators, researchers, policy people, technologists, and the AI-curious can wrestle with the technology together instead of swallowing the hype alone.

Recommended social image:

- Preferred: approved Vancouver AI event/stage photo already in the WordPress media library.
- Fallback: the public March 2026 YouTube thumbnail from `content/source-packs/keynotes-2026/video-research/thumbnails/vancouver-ai-march-2026-appearance.jpg`, after KK review.

## Internal Link Recommendations

Add links only after the draft exists and KK approves the page as a destination:

- From `/about/`: link the BC+AI / Vancouver AI role card to the new page as a local narrative hub, while keeping `bc-ai.ca` as the direct ecosystem destination.
- From `/recent-projects-include/`: add `Vancouver AI Community` as a supporting project link near the BC+AI card.
- From `/speaking/`: link the Vancouver AI appearance/media proof section to the new page.
- From `/generative-ai-services/`: link the Community & Ecosystem Building service card to the new page as a case-style proof point.
- Do not edit Work/Home/Speaking/About in the issue #18 worker lane without explicit approval.

## Publish And Deployment Checklist

Before any live WordPress draft or publish action:

1. Confirm full-site backup and restore proof, or stop.
2. Create a WordPress draft, not a published page.
3. Confirm the draft slug is exactly `vancouver-ai-community`.
4. Paste only `wp-payloads/vancouver-ai-community.html` into the draft content.
5. Set comments and pings to closed.
6. Add the recommended SEO/social metadata only after the draft page ID is known.
7. Choose and verify a featured/social image.
8. Preview desktop and mobile.
9. Check the YouTube embed, Luma link, BC+AI link, membership link, and internal links.
10. Get KK approval before publishing or adding links from existing live pages.

Post-publish checks:

- `https://kriskrug.co/vancouver-ai-community/` returns `200`.
- The page title is `Vancouver AI Community`.
- The page contains `250+`, `3,000+`, `94+`, `Est. 2023`, and `T5ANAthZewE`.
- No temporary Notion URLs appear in public HTML.
- Source links return expected statuses.
- Public HTML exposes the intended SEO title, description, and social image.

## Closure Criteria

Issue `#18` should remain open after this repo-side package because live deployment, image selection, draft readback, internal links, and public evidence verification are still blocked by the production-write gate and KK review.

It can close after:

- the WordPress draft or published page exists,
- backup/restore proof is documented,
- target slug/title/content readback passes,
- selected image and social metadata are verified,
- approved internal links are applied or explicitly deferred,
- KK accepts the page as the issue #18 deliverable.

## Verification Commands

Commands run from `/Users/kk/Code/kriskrug-wp`:

```sh
git status --short --branch
curl -L --max-time 20 -I https://bc-ai.ca/
curl -L --max-time 20 -I https://bc-ai.ca/membership/
curl -L --max-time 20 -I https://vancouver.bc-ai.net/
curl -L --max-time 20 -I https://luma.com/vancouver-ai
curl -L --max-time 20 -I https://www.youtube.com/embed/T5ANAthZewE
curl -L --max-time 25 https://bc-ai.ca/ | rg -n -i "250\+|3,000\+|3000|94\+|Members|Event Attendees|Events Hosted|BC Regions|Vancouver AI|membership|bcai-stat"
rg -n "Vancouver AI|BC\+AI|Both Hands Full|community|Web Summit" content/source-packs/keynotes-2026/wp-payloads/about.html content/source-packs/keynotes-2026/wp-payloads/speaking.html content/source-packs/keynotes-2026/wp-payloads/work.html content/source-packs/keynotes-2026/wp-payloads/homepage-hero.html content/drafts/2026-05-07-web-summit-vancouver-2026/post.md content/drafts/2026-05-14-calling-us-all-in/post.md
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

class Parser(HTMLParser):
    pass

path = Path("content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html")
parser = Parser()
parser.feed(path.read_text())
parser.close()
print("html.parser ok")
PY
rg -n "Vancouver AI|bc-ai\.ca|luma\.com/vancouver-ai|T5ANAthZewE|250\+|3,000\+|94\+|Est\. 2023|Notion" content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html content/source-packs/keynotes-2026/verification/ISSUE-18-VANCOUVER-AI-COMMUNITY-VERIFICATION-2026-05-21.md
rg -n "Notion|notion\.so|notionusercontent|s3" content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html
rg -n "[ \t]+$" content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html content/source-packs/keynotes-2026/verification/ISSUE-18-VANCOUVER-AI-COMMUNITY-VERIFICATION-2026-05-21.md
git diff --no-index --check /dev/null content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html
git diff --no-index --check /dev/null content/source-packs/keynotes-2026/verification/ISSUE-18-VANCOUVER-AI-COMMUNITY-VERIFICATION-2026-05-21.md
git diff --check -- content/source-packs/keynotes-2026/wp-payloads/vancouver-ai-community.html content/source-packs/keynotes-2026/verification/ISSUE-18-VANCOUVER-AI-COMMUNITY-VERIFICATION-2026-05-21.md
git diff --check
```

Results:

- `https://bc-ai.ca/` returned `200`.
- `https://bc-ai.ca/membership/` returned `200`.
- `https://vancouver.bc-ai.net/` returned `200`.
- `https://luma.com/vancouver-ai` returned `200`.
- `https://www.youtube.com/embed/T5ANAthZewE` returned `200`.
- Live BC+AI homepage source contained the public stat markers used in the payload.
- Existing repo source scan found Vancouver AI / BC+AI grounding across current page payloads and draft posts.
- `html.parser ok` for `vancouver-ai-community.html`.
- Marker scan found the expected Vancouver AI, BC+AI, Luma, YouTube, stat, and `Est. 2023` strings.
- Temporary Notion/cloud-asset scan against the new payload found no matches.
- Lane-scoped trailing whitespace scan found no matches.
- `git diff --no-index --check` against each new file produced no whitespace warnings. It exits `1` for `/dev/null` comparisons because the files differ from an empty file; the useful result is no warning output.
- Lane-scoped `git diff --check` passed for tracked-path checks.
- Repo-level `git diff --check` passed in the current dirty multi-worker checkout.
