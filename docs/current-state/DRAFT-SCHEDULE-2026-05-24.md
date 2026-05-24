# Draft Schedule - 2026-05-24

**Track:** Track A content + SEO
**Status:** implemented in WordPress on 2026-05-24
**Operator note:** WordPress has a blank/fixed-offset timezone setting. The `date` value in REST readback appears one hour earlier than Vancouver/PDT, but `date_gmt` below resolves to the requested `America/Vancouver` release time.

## Scheduled Posts

| WP ID | Title | Slug | Status | Vancouver release time | REST `date` | REST `date_gmt` | Category | Featured media | Metrics |
|---:|---|---|---|---|---|---|---|---:|---|
| 6348 | The AI Mindset: Adapting to the New Creative Paradigm | `ai-mindset-creative-paradigm` | `future` | 2026-05-24 4:00 PM PDT | `2026-05-24T15:00:00` | `2026-05-24T23:00:00` | AI for Creatives | 6657 | 1,933 words; 11 links; 12 images; 76 blocks |
| 8021 | End of the Tech Bro Kingdom: How AI Might (Finally) Let Us All Code | `end-of-the-tech-bro-kingdom-ai-code` | `future` | 2026-05-25 9:00 AM PDT | `2026-05-25T08:00:00` | `2026-05-25T16:00:00` | AI Tools & Training | 6048 | 2,467 words; 9 links; 0 inline images; 58 blocks |
| 2749 | Future In Review Podcast | `future-in-review-podcast` | `future` | 2026-05-27 9:00 AM PDT | `2026-05-27T08:00:00` | `2026-05-27T16:00:00` | Conversations & Interviews | 2416 | 1,540 words; 34 links; 0 inline images; 118 blocks |

## Prep Applied

- Confirmed all three target IDs were still `draft` before mutation.
- Confirmed title matches for each target ID.
- Replaced empty slugs with intentional slugs.
- Replaced `Misc` category with intentional category.
- Set featured media and ensured featured alt text exists.
- Replaced weak/missing excerpts and SEO/publicize descriptions.
- Opened wp-admin edit and preview URLs for review.
- Final readback caught `6348` with an incorrect 2025 timestamp; corrected it back to `future` for the intended 2026 release slot before closeout.

## Remaining Watch Item

The site timezone should eventually be corrected to a named timezone such as `America/Vancouver`. Until then, schedule checks should verify `date_gmt` and convert it back to Vancouver time instead of trusting the REST `date` display alone.
