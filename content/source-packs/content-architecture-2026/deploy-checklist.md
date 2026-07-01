# Deploy Checklist - Content Architecture Trust + Offers

## Preflight

- Confirm branch is `codex/content-architecture-trust-offers`.
- Confirm PR #272 is merged and live CSS reports Aurora `1.3.27`.
- Confirm performance lane artifacts remain untracked and untouched.
- Run payload tests before any live write.

## Target Pages

| Payload | Page ID | Slug | URL |
|---|---:|---|---|
| `services.html` | 2666 | `generative-ai-services` | `/generative-ai-services/` |
| `contact.html` | 2418 | `contact` | `/contact/` |
| `work.html` | 2672 | `work` | `/work/` |
| `about.html` | 1208 | `about` | `/about/` |
| `speaking.html` | 1887 | `speaking` | `/speaking/` |
| `responsible-ai-professional.html` | 11914 | `responsible-ai-professional` | `/responsible-ai-professional/` |
| `podcast-guesting-page-epk.html` | 3609 | `podcast-guesting-page-epk` | `/podcast-guesting-page-epk/` |

## Live Write Gate

For each page:

1. Fetch `context=edit` with `id,slug,status,title,content,excerpt,meta,modified,link`.
2. Stop unless ID, slug, and status match the target.
3. Save JSON and current rendered public HTML under `backup/<timestamp>-content-architecture/page-snapshots/`.
4. Write only `{"content": "<payload>"}` to `/wp-json/wp/v2/pages/{id}`.
5. Do not include `title` in the payload.
6. Re-read REST and public HTML.
7. Verify required markers from `page-map.json`.
8. If verification fails, restore the saved `content.raw` for that page before moving on.

## Readability Acceptance

After all pages are updated:

- No horizontal overflow at `1440`, `768`, `390`, or `360` widths.
- Standard page H1 is at least `48px` on tablet/desktop and `32px` on mobile.
- Prose/body/card text is at least `16px` except captions/meta.
- Primary nav/buttons meet `44px` touch target on mobile.
- No body H1s.
- No retired `kk-*`, `kkp-*`, `kkx-*`, `kk-services-*`, or `kk-publications-*` classes in updated page raw content.
