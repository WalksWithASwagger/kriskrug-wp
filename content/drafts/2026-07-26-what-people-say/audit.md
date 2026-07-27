# Audit: What People Say / testimonials surface

Read date: 2026-07-26. Public HTTP only. No WP auth.

## Live homepage (`https://kriskrug.co/`)

| Finding | Detail |
|---|---|
| Section present? | **No.** `aurora-testimonial-band` / "What people say" / `fresh proof` all absent in rendered HTML. |
| Current order | Masthead → proof strip → archive → current work → services → writing → **newsletter** → footer |
| Testimonials link | Footer Utility tile only: `/testimonials/` |
| Theme CSS remnant | `theme/kk-aurora/style.css` still defines `.aurora-testimonial-band` and `.aurora-quote-grid-three` (dead styling until markup returns) |

Implication: #415 is a **rebuild**, not a polish. The band was removed during later homepage edits; CSS leftovers remain.

## Prior homepage band (repo backups / front-page reports, June-July 2026)

Snapshot pattern from `backup/20260623-163028Z/homepage.html` and `docs/current-state/reports/front-page-template-*-*.html`:

- Kicker: `What people say`
- H2: **`Fresh proof belongs here before launch.`** (inside-baseball placeholder)
- Dek: "The Stewart Butterfield quote can stay as an anchor…"
- Three quote cards with **placeholder cites**:
  - "Event organizer quote - replace with verified 2024-2026 attribution"
  - "Workshop host quote - replace with verified attribution"
  - "Leadership audience quote - replace with verified attribution"

Acceptance eval from the issue: `grep -ci 'fresh proof'` on rendered homepage must return **0**. Live already passes. Any redesign must keep that true.

## Attribution hazard (do not reintroduce)

Historical raw homepage pullquote (`docs/current-state/raw/homepage.html`) attributed a long conference/camera quote to **Stewart Butterfield, Slack**. The same wording appears on `/testimonials/` and contact snapshots as **Rob Cottingham**. Site audit (`SITE-AUDIT-2026-05-16.md`) already flagged Butterfield attribution as dated/credibility risk. Treat Butterfield-as-author of that quote as **unverified / conflicting** until KK decides.

## Live `/testimonials/` (page 2409)

Public page still exists. Content is a flat stack of older photography / community quotes (Danie Peace, Rob Cottingham, Joshua Dunford, Corey Dennis, Benjamin Random, Brian Auer, Novak Rogic, Claudine Co, Stephanie Vacher). No theme cards, no 2024-2026 AI/keynote proof, no schema. Useful as archive, weak as homepage booking proof.

## Repo testimonial bank

`content/source-packs/keynotes-2026/testimonial-bank.md` already separates:

- **Approved for live payload (speaking context):** Jai Djwa, Ed Kennedy, two generic audience lines
- **Legacy / About energy:** Cottingham, Dunford, Dennis, Benjamin Random
- **Do not publish without verification:** unnamed praise, synthetic sales tone, private client comments

Speaking payload (`content/source-packs/keynotes-2026/wp-payloads/speaking.html`) uses the Jai / Ed / audience trio under "Speaker proof." Live `/speaking/` render on 2026-07-26 did **not** show those blockquotes in the public HTML sample (section may not be live yet). Do not assume homepage can copy speaking until that page is verified.

## What is missing for #415 acceptance

1. Curated 2024-2026 set with sources + KK permission checkboxes (drafted in `curated-quotes.md`).
2. Section design that shows clusters / rotation without fake cites.
3. Standalone network diagram prototype for KK reaction (`network-diagram-spike/`).
4. Explicit kill of placeholder "fresh proof" language if the band returns.
