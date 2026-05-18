# Deploy Checklist

Do not deploy these payloads until the live-write safety gate clears.

Continuation issue: https://github.com/WalksWithASwagger/kriskrug-wp/issues/76

## Safety Gate

- Complete a fresh full-site backup or get explicit KK approval to proceed with a narrower rollback path.
- Confirm rollback snapshots exist under `backup/20260518-111546/page-snapshots/`.
- Confirm target page IDs:
  - `1208` -> `/about/`
  - `1887` -> `/speaking/`
  - `2672` -> `/recent-projects-include/`
- Keep `/recent-projects-include/` slug unchanged. `/work/` already redirects there.
- Close comments and pings on `/speaking/`.

## Payload Fields

Use `page-meta.json` for titles, comment settings, ping settings, and Jetpack SEO meta.

Payload files:

- `speaking.html` -> page `1887`
- `work.html` -> page `2672`
- `about.html` -> page `1208`

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
- `/speaking/` does not contain `Leave a Reply`.
- Selected image URLs return `200`.
- Desktop and mobile pages show the new hero/CTA sections.

## Final Content Checks

- `/speaking/` contains `AI Keynote Speaker Kris Krüg`.
- `/speaking/` contains `Book Kris for a keynote`.
- `/speaking/` links to `Both Hands Full`, `Punk Rock AI`, `Developing an AI Mindset`, `BC + AI Ecosystem`, and `/contact/`.
- `/recent-projects-include/` title is `Work`.
- `/about/` title is `About Kris Krüg`.
- No temporary Notion asset URLs appear in any live page.
