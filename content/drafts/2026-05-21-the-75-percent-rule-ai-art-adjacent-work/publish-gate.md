# Publish gate: The 75% Rule: Send AI After the Art-Adjacent Work

Status: **review-ready** WordPress private post `11876` — not schedule-ready until KK preview approval.

## Automated QA — 2026-06-16

`prepare_review_draft.py` gate: **PASS**

- Local words: 1791
- Links: 9
- Images: 1
- Blocks: 110
- No local path leaks, banned phrases, or open task markers in body scan

## WordPress readback — 2026-06-16

| Field | Value |
| --- | --- |
| Post ID | `11876` |
| Status | `private` (review package; not public draft) |
| Slug | `the-75-percent-rule-ai-art-adjacent-work` |
| WP title | `Send AI After the Art-Adjacent Work` |
| Local title | `The 75% Rule: Send AI After the Art-Adjacent Work` |
| Featured media | `11838` |
| Edit URL | https://kriskrug.co/wp-admin/post.php?post=11876&action=edit |
| Local paths in body | none |
| Link count | 9 |

**Title delta:** WP title omits "The 75% Rule:" prefix. Confirm with KK whether to align WP title to local YAML before scheduling.

## KB source verification — 2026-06-16

Storyhive transcript/recap confirmed in `kk-kb` at:

- `/Users/kk/Code/kk-kb/content/media/interviews/2026-05-20-storyhive-on-location-victoria-transcript.md`
- Symlink: `/Users/kk/Code/notion-local/kk-ai-ecosystem/...`

Transcript proper-noun cleanup applied (Kris Krug, Jordan Dack, Haus of Owl) against YouTube auto-captions.

## Required before scheduling

- KK approves the exact WordPress preview (desktop + mobile).
- Resolve title alignment if desired.
- WordPress readback remains clean after any title/body tweak.
- No private Notion URLs, local paths, open task markers, temporary alt notes, or em dashes in public body.
