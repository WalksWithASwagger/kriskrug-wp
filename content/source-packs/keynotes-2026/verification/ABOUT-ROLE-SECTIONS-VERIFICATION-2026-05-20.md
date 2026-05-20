# About Role Sections Verification - 2026-05-20

## Scope

- Track A content payload only.
- No live WordPress write, media upload, theme edit, or production activation performed in this pass.
- Updated payload: `content/source-packs/keynotes-2026/wp-payloads/about.html`.

## What Changed

- Added a `Current operating roles` section with three equal-weight cards:
  - BC + AI Ecosystem: Executive Director / ecosystem builder.
  - Indigenomics AI: CTO / Indigenous economic technology.
  - The Upgrade AI: Co-founder / AI training.
- Reframed photography as `Visual storyteller` in the hero proof row.
- Added copy that explicitly positions photography as the visual storytelling background behind the AI/community/speaking work.
- Added responsive role-card CSS that follows the existing payload pattern: simple grid, high-contrast text, semantic headings, and compact fact chips.

## Source Grounding

- XML About source was confirmed in `/Users/kk/Desktop/kriskrggenerativeaitoolsamptechniques.WordPress.2026-01-03.xml`; the page item starts around line `156582` and preserves the original `Techartist, quasi-sage, cyberpunk anti-hero from the future.` title.
- Role mapping came from `docs/kris-krug-roles-module.md`, including the `CTO, Indigenomics`, `TheUpgrade.ai`, and `BC+AI Executive Director` role framework.
- BC + AI current stats were checked against the live `https://bc-ai.ca/` home page on 2026-05-20:
  - `250+` Members.
  - `3,000+` Event Attendees.
  - `94+` Events Hosted.
- The older XML source has the 2024 historical stat of `13 monthly meetups with over 2,000 total attendees`; the issue text said `2,000+ members`, but current public evidence supports `250+ members` and `3,000+ event attendees`, so the payload uses the current source-backed numbers.
- Indigenomics evidence came from the local XML/public post `https://kriskrug.co/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/`, including the dashboard, sovereign data, and `$100B Indigenous economy` language. The `indigenomics.ai` domain currently resolves to a parked/lander page, so the payload links to the owned kriskrug.co post instead of treating the parked domain as an authority page.
- The Upgrade evidence came from `https://www.theupgrade.ai/`, the XML source referencing Peter Bittner and TheUpgrade.ai, and the public Upgrade page copy around live/on-demand courses, group coaching, team trainings, certification cohorts, and enterprise logo proof. The payload uses `enterprise logos` instead of an unqualified `Fortune 500 training` claim.
- Policy influence evidence is supported by the local Vancouver AI March 2026 transcript phrase `community-based regional organization that is impacting national policy around AI`.

## Acceptance Notes

| Criterion | Status | Note |
|---|---:|---|
| Current About page content extracted from XML | Done | XML source located and old title/voice preserved. |
| BC+AI section added | Done | Uses current public stats rather than stale/mislabeled `2,000+ members`. |
| Indigenomics section added | Done | Uses CTO framing plus source-backed `$100B Indigenous economy` language. |
| The Upgrade AI section added | Done | Names Peter Bittner, cohorts, team trainings, and enterprise proof. |
| Photography positioned as visual storytelling background | Done | Hero proof and current-work copy updated. |
| Professional but warm tone throughout | Done | Keeps KK voice without turning the page into a formal resume. |
| All three roles featured equally | Done | Three same-level cards in the same section. |
| Mobile responsive | Locally ready | Uses existing auto-fit grid and mobile media query; full browser render still belongs in the live/staging publish pass. |
| WCAG 2.1 AA | Locally ready | Semantic headings, text-based CTAs, alt text retained, no low-contrast decorative text added; full automated scan belongs in the live/staging render pass. |
| Updated content ready to publish | Done | Payload is ready for the normal backup/snapshot gate before any WP write. |

## Verification

- External URL check from `about.html`: `20` unique `http(s)` URLs checked with `curl -L`; all returned `200`.
- Payload privacy scan: no sensitive-string matches found in `about.html`.
- Expected content checks found:
  - `Current operating roles`
  - `Executive Director / ecosystem builder`
  - `250+ members`
  - `3,000+ event attendees`
  - `CTO / Indigenous economic technology`
  - `$100B Indigenous economy vision`
  - `Co-founder / AI training`
  - `Peter Bittner`
  - `Visual storyteller`

## Publish Gate

Before applying this payload to live page ID `1208`, follow the repo live-write rules:

1. Take a fresh backup or stop.
2. Snapshot page ID `1208` to rollback JSON/HTML.
3. PATCH only after slug/title/id verification confirms the target is `/about/`.
4. REST-read back title, slug, status, comment settings, SEO meta, and content markers.
5. Browser-check desktop and mobile after publish.
