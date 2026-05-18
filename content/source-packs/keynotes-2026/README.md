# Keynotes 2026 Source Pack

Curated source pack for the 2026 overhaul of the `Speaking`, `Work`, and `About` pages on kriskrug.co.

This is a selective publishing pack, not a Notion mirror. It keeps the useful public story, talk architecture, selected owned-site assets, and verification notes in one place so the WordPress pages can be updated safely and rolled back if needed.

## Scope

- `Speaking` becomes the booking-first authority page for AI keynotes.
- `Work` becomes the current-project portfolio hub while keeping the existing `/recent-projects-include/` slug for this pass.
- `About` keeps the voice/photo-story energy and makes the 2026 AI, community, and speaking story obvious.
- This is the next larger overhaul after the smaller owned-sites network rollout captured in `docs/current-state/OWNED-SITES-LINKING-RECOMMENDATION-2026-05-18.md`.

## Deploy Status

Applied and verified on 2026-05-18. See `verification/DEPLOY-VERIFICATION-2026-05-18.md`.

## Source Inputs

- Notion page: `Keynotes` (`cd4ce83f-afa5-440d-8405-4caf04a480d1`)
- Notion page: `Keynotes in Dev` (`2f8c6f799a338089b6f7f8a3adf9c69a`)
- Notion page: `Keynote: Creative Rebellion` (`272c6f799a338080a2ebf74ab32597d0`)
- Notion page: `KEYNOTE: Developing AI Mindset` (`6895c952cd674901b339dfbf9b153d1c`)
- Notion page: `Keynote: Compost AI` (`2e4c6f799a3380f989d3e890b7c6af75`)
- Notion page: `Dear AI: We Need to Talk About Your Soul` (`1bcc6f799a3380eda6ecc6f2b405be77`)
- Notion page: `World AI Film Festival Keynote 2026` (`312c6f799a3380c58860d1427d650f1c`)
- Local WAIFF materials: `/Users/kk/Code/notion-local/kk-ai-ecosystem/content/projects/03-theupgrade-ai-training/speaking-engagements/uai-film-festival-brazil-2026/`
- Public owned sites:
  - `https://www.bothhandsfull.com/`
  - `https://www.punkrockai.com/`
  - `http://developinganaimindset.com/`
  - `https://bc-ai.ca/`
  - `https://kriskrug.co/`

## Files

- `notion/keynotes-sanitized-snapshot.md` - curated public-safe Notion findings.
- `talk-topic-bank.md` - keynote and workshop topics suitable for public pages.
- `testimonial-bank.md` - verified or source-backed quotes only, plus rejected/unverified patterns.
- `assets/asset-manifest.md` - selected stable teaser assets and local copies.
- `wp-payloads/speaking.html` - publish-ready content for page `1887`.
- `wp-payloads/work.html` - publish-ready content for page `2672`.
- `wp-payloads/about.html` - publish-ready content for page `1208`.
- `wp-payloads/page-meta.json` - target titles, SEO meta, slugs, and comment settings.
- `wp-payloads/deploy-checklist.md` - live-write gate and verification checklist.
- `verification/DEPLOY-VERIFICATION-2026-05-18.md` - REST, URL, screenshot, and rollback verification after deploy.

## Safety Notes

- Raw WAIFF logistics material is deliberately not copied into this pack.
- Private/client talks are generalized unless there is public evidence.
- Notion-hosted temporary asset URLs are not used in live HTML.
- Only named, source-backed, or screenshot-backed testimonials are eligible for publication.
- Generic testimonial drafts stay out of the WordPress payload.

## Rollback Snapshots

Fresh page-level rollback snapshots were captured before preparing payloads:

- `backup/20260518-111546/page-snapshots/page-1208-about.json`
- `backup/20260518-111546/page-snapshots/page-1208-about.html`
- `backup/20260518-111546/page-snapshots/page-1887-speaking.json`
- `backup/20260518-111546/page-snapshots/page-1887-speaking.html`
- `backup/20260518-111546/page-snapshots/page-2672-work.json`
- `backup/20260518-111546/page-snapshots/page-2672-work.html`
- `backup/20260518-111546/page-snapshots/sha256sums.txt`

Full-site backup status: blocked on authenticated UpdraftPlus admin access at the time this pack was prepared. KK explicitly authorized the narrower rollback path on 2026-05-18, and the live deploy is documented in `verification/DEPLOY-VERIFICATION-2026-05-18.md`.

Continuation issue: https://github.com/WalksWithASwagger/kriskrug-wp/issues/76
