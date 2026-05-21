# Issue #14 Indigenomics Section Verification - 2026-05-21

## Scope

- Worker lane: #14, Track A source-pack content only.
- Allowed write surface: `content/source-packs/keynotes-2026/wp-payloads/about.html` and this verification note.
- No live WordPress writes, media uploads, theme edits, Work/Home/Speaking payload edits, or connector runs were performed.

## Audit Result

The About payload already had an Indigenomics role card inside `Current operating roles`, with CTO framing, Indigenous economic sovereignty language, sovereign data language, and the source-backed `$100B Indigenous economy vision`.

The smallest useful improvement was to make the existing card more directly satisfy issue #14:

- Changed the role label to `CTO, Indigenomics.ai`.
- Changed the card heading link to `https://indigenomics.ai/`.
- Added explicit `technology for justice` copy tied to Indigenous-led strategy, sovereignty, and partnership.
- Kept the source-backed `$100B Indigenous economy vision` wording instead of silently upgrading to `$200B+`.
- Added `Read the source post` and `Partnership inquiry` CTAs.

Note: `about.html` already contained unrelated BC+AI card edits from another worker lane before this issue #14 patch. This lane preserved those edits and only changed the Indigenomics card.

## Evidence Boundary

Evidence used:

- `docs/kris-krug-roles-module.md` supports the `CTO, Indigenomics` role and the data sovereignty / digital self-determination frame.
- `content/source-packs/keynotes-2026/verification/ABOUT-ROLE-SECTIONS-VERIFICATION-2026-05-20.md` records that the public Indigenomics post supports dashboard, sovereign data, and `$100B Indigenous economy` language.
- `content/source-packs/keynotes-2026/verification/HOMEPAGE-HERO-VERIFICATION-2026-05-20.md` explicitly says the older issue text requested `$200B`, but the verified source-backed wording was `$100B`.
- `fixes/issue-13-14-15-project-sections.md` contains draft issue-copy claiming `$200B+`, but this pass treated that as proposed copy, not evidence.

KK review needed:

- The `$200B+ Indigenous economic discovery` claim should not be published as verified from this repo evidence alone. Use `$100B Indigenous economy vision` unless KK supplies source proof or approves the updated metric.

## Acceptance Mapping

| Criterion | Status | Note |
|---|---:|---|
| Dedicated Indigenomics.ai section | Locally ready | Existing dedicated role card now names and links `Indigenomics.ai`. No standalone duplicate section added. |
| CTO role | Done | Role label now says `CTO, Indigenomics.ai`. |
| `$200B+ Indigenous economic discovery` | Needs KK review | Existing verified source-pack evidence supports `$100B Indigenous economy vision`; `$200B+` remains unverified in this lane. |
| Indigenous sovereignty focus | Done | Existing copy covers Indigenous economic sovereignty, protocol, sovereign data, and non-extractive systems. |
| Technology for justice | Done | Added explicit technology-for-justice sentence. |
| Link to indigenomics.ai | Done | Heading links to `https://indigenomics.ai/`. |
| Partnership inquiry CTA | Done | Added `Partnership inquiry` link to `/contact/`. |
| Mobile readiness | Locally ready | Uses existing responsive `.kk-grid`, `.kk-role-card`, and mobile media-query patterns; browser render should happen before live publish. |
| WCAG readiness | Locally ready | Added text links and semantic copy only; no image/alt-text burden or color changes added. Full live/staging scan still belongs in the publish gate. |

## Verification

Commands run:

```bash
rg -n "CTO, Indigenomics\\.ai|https://indigenomics\\.ai/|technology for justice|Partnership inquiry|\\$100B Indigenous economy vision|Read the source post" content/source-packs/keynotes-2026/wp-payloads/about.html
curl -I -L --max-time 20 https://indigenomics.ai/
curl -I -L --max-time 20 https://kriskrug.co/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/
curl -I -L --max-time 20 https://kriskrug.co/contact/
rg -n "[ \\t]+$" content/source-packs/keynotes-2026/wp-payloads/about.html content/source-packs/keynotes-2026/verification/ISSUE-14-INDIGENOMICS-SECTION-VERIFICATION-2026-05-21.md
git diff --check -- content/source-packs/keynotes-2026/wp-payloads/about.html content/source-packs/keynotes-2026/verification/ISSUE-14-INDIGENOMICS-SECTION-VERIFICATION-2026-05-21.md
git diff --no-index --check -- /dev/null content/source-packs/keynotes-2026/verification/ISSUE-14-INDIGENOMICS-SECTION-VERIFICATION-2026-05-21.md
git diff --check
```

Observed results:

- Required markers were found in `about.html`.
- `https://indigenomics.ai/` returned `200 OK`.
- The source post returned `HTTP/2 200`.
- `/contact/` returned `HTTP/2 200`.
- Lane-scoped trailing-whitespace scan found no matches.
- Lane-scoped `git diff --check` passed for the tracked payload path. The new verification note was also checked with `git diff --no-index --check`; it produced no whitespace findings.
- Repo-level `git diff --check` passed; no other worker lane blocked the whitespace check.

## Closure Recommendation

Close issue #14 only if the reviewer accepts the verified `$100B Indigenous economy vision` wording as the safe replacement for the unverified `$200B+` issue text.

If `$200B+ Indigenous economic discovery` is mandatory, leave the issue open with `needs-human-review` until KK supplies source proof or explicitly approves that claim.
