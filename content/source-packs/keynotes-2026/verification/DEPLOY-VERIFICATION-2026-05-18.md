# Keynotes 2026 Deploy Verification - 2026-05-18

**Issue:** <https://github.com/WalksWithASwagger/kriskrug-wp/issues/76>
**Track:** A - Content + SEO
**Live-write gate:** KK approved the narrower page-level rollback path in-thread with "agreed proceed."
**Result:** Authenticated readback showed the live WordPress pages already matched the prepared payloads, so this pass verified the deploy rather than issuing a redundant overwrite.

## Rollback Evidence

Fresh page-level snapshots exist under:

- `backup/20260518-113350/page-snapshots/`

Checksum verification passed for:

- `all-pages-public-rest.json`
- `page-1208-about.html`
- `page-1208-about.json`
- `page-1887-speaking.html`
- `page-1887-speaking.json`
- `page-2672-work.html`
- `page-2672-work.json`
- `redirection-export-before.json`
- `redirection-list-before.json`

## REST Readback

Authenticated WordPress REST readback confirmed:

| Page | ID | Slug | Title | Modified | Content | SEO meta | Comments/pings |
|---|---:|---|---|---|---|---|---|
| Speaking | 1887 | `speaking` | `AI Keynote Speaker Kris Krüg` | `2026-05-18` | Matches `speaking.html` | Matches `page-meta.json` | Closed |
| Work | 2672 | `recent-projects-include` | `Work` | `2026-05-18` | Matches `work.html` | Matches `page-meta.json` | Closed |
| About | 1208 | `about` | `About Kris Krüg` | `2026-05-18` | Matches `about.html` | Matches `page-meta.json` | Closed |

## Redirect Readback

The existing Redirection plugin rule for `/work/` was updated so query-string traffic lands on the Work page instead of falling through to WordPress canonical guessing:

| Rule | Source | Target | Query handling |
|---:|---|---|---|
| 3 | `/work/` | `/recent-projects-include/` | `pass` |

## Public URL Checks

| URL | Result |
|---|---|
| `https://kriskrug.co/speaking/` | `200`, required markers present, no `Leave a Reply` |
| `https://kriskrug.co/recent-projects-include/` | `200`, required markers present, no `Leave a Reply` |
| `https://kriskrug.co/work/` | `301` to `/recent-projects-include/` |
| `https://kriskrug.co/work/?utm_source=codex-test` | `301` to `/recent-projects-include/` |
| `https://kriskrug.co/about/` | `200`, required markers present, no `Leave a Reply` |

Image URL checks returned `200` for the BC + AI, Punk Rock AI, Both Hands Full, and AI Mindset teaser images.

## Screenshots

Captured evidence lives under `content/source-packs/keynotes-2026/verification/screenshots/`:

- `about-desktop.png`
- `about-mobile.png`
- `speaking-desktop.png`
- `speaking-mobile.png`
- `work-desktop.png`
- `work-mobile.png`
- `work-redirect-desktop.png`
- `work-redirect-mobile.png`
- `contact-sheet-desktop.png`
- `contact-sheet-mobile.png`

## Notes

- Issue #76 was commented and closed after verification.
- Aurora can now use these pages as the real-content test set.
- The next publishing lane should return to the draft batch: `Sovereign AI for Whom?`, RAP follow-up, and the GNI/TheUpgrade origin story.
