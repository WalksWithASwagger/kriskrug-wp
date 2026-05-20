# Deploy Checklist

Status: deployed and verified on 2026-05-18. See `../verification/DEPLOY-VERIFICATION-2026-05-18.md`.

Do not re-deploy these payloads unless a fresh readback shows drift or a rollback/reapply is intentional.

Continuation issue: https://github.com/WalksWithASwagger/kriskrug-wp/issues/76

## Safety Gate

- Complete a fresh full-site backup or get explicit KK approval to proceed with a narrower rollback path.
- Confirm rollback snapshots exist under `backup/20260518-111546/page-snapshots/`.
- Confirm target page IDs:
  - `1208` -> `/about/`
  - `1887` -> `/speaking/`
  - `2666` -> `/generative-ai-services/`
  - `2672` -> `/recent-projects-include/`
- Keep `/recent-projects-include/` slug unchanged. `/work/` already redirects there.
- Close comments and pings on `/speaking/`.

## Payload Fields

Use `page-meta.json` for titles, comment settings, ping settings, and Jetpack SEO meta.

Payload files:

- `speaking.html` -> page `1887`
- `services.html` -> page `2666`
- `work.html` -> page `2672`
- `about.html` -> page `1208`

## Homepage Hero Candidate

Status: prepared, not deployed. See `../verification/HOMEPAGE-HERO-VERIFICATION-2026-05-20.md`.

- `homepage-hero.html` -> page `3930`, public URL `/`
- Insert before existing page content unless KK approves replacing the current top copy.
- The separate `/home/` page ID `2315` is the old latest-posts page and is not the target for this hero.

## Services Page Candidate

Status: prepared, not deployed. See `../verification/SERVICES-ROLE-ALIGNMENT-VERIFICATION-2026-05-20.md`.

- `services.html` -> page `2666`, public URL `/generative-ai-services/`
- Replace the current page content after a fresh live backup or an explicitly approved narrower rollback path.
- Keep the existing `/generative-ai-services/` slug for this pass; menu label can remain `Services`.
- Close comments and pings on the page.

## Post-Deploy REST Checks

Check these fields after update:

- `id`
- `slug`
- `title.rendered`
- `status`
- `comment_status`
- `ping_status`
- `meta.jetpack_seo_html_title`
- `meta.advanced_seo_description`

## Browser / Curl Checks

- `/speaking/` returns `200`.
- `/recent-projects-include/` returns `200`.
- `/work/` redirects to `/recent-projects-include/`.
- `/about/` returns `200`.
- `/generative-ai-services/` returns `200`.
- `/speaking/` does not contain `Leave a Reply`.
- Selected image URLs return `200`.
- Desktop and mobile pages show the new hero/CTA sections.

## Final Content Checks

- `/speaking/` contains `AI Keynote Speaker Kris Krüg`.
- `/speaking/` contains `Book Kris for a keynote`.
- `/speaking/` links to `Both Hands Full`, `Punk Rock AI`, `Developing an AI Mindset`, `BC + AI Ecosystem`, and `/contact/`.
- `/recent-projects-include/` title is `Work`.
- `/about/` title is `About Kris Krüg`.
- `/generative-ai-services/` title is `AI Services, Training & Strategy`.
- `/generative-ai-services/` contains `AI Strategy Consulting`, `Community & Ecosystem Building`, `The Upgrade AI Training`, `Indigenomics Advisory`, and `Keynotes, Workshops & Executive Briefings`.
- No temporary Notion asset URLs appear in any live page.
