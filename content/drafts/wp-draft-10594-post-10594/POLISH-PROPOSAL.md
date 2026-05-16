# Polish proposal — MAKE CULTURE, NOT CONTENT (post 10594)

**Current state:** draft, modified 2025-09-23, 3,443 words, no slug, no excerpt, no SEO meta, no featured image, uncategorized, no tags, **38 encoding artifacts** (`?` chars where hyphens should be), zero links, zero images.

Edit URL: https://kriskrug.co/wp-admin/post.php?post=10594&action=edit

## ⚠️ Encoding cleanup (auto-applied)

38 instances of `?` between word characters that should be hyphens. All look like compound modifiers (no em-dash usage detected). The fix is mechanical: `s/(\w)\?(\w)/\1-\2/g`. Sample:

| Currently reads | Should read |
|---|---|
| `mass?produce` | `mass-produce` |
| `clear?eyed` | `clear-eyed` |
| `hyper?partnered` ×4 | `hyper-partnered` |
| `state?platform` ×2 | `state-platform` |
| `consent?driven` | `consent-driven` |
| `community?owned` | `community-owned` |
| `red?team` ×3 | `red-team` |
| `proof?of` | `proof-of` |
| `Anti?Glossary` | `Anti-Glossary` |
| `Pro?move` | `Pro-move` |
| `Constraints?First` | `Constraints-First` |
| `voice?first` | `voice-first` |
| `90?DAY` | `90-DAY` |
| `0?5` | `0–5` (en-dash for ranges) |
| `30?second` | `30-second` |
| `Time?to` | `Time-to` |
| `2?sentence` | `2-sentence` |
| `one?paragraph` | `one-paragraph` |

(Plus 20 more — full list in publish.log when patched.)

## Proposed metadata

| Field | Current | Proposed |
|---|---|---|
| **Title (H1)** | "MAKE CULTURE, NOT CONTENT" | unchanged (or sentence-case to `Make Culture, Not Content` if you want a softer look) |
| **In-body subtitle** | `<h2>A FIELD MANUAL FOR CREATIVE PROS IN THE SYNTHETIC AGE</h2>` (italic) | keep as h2 OR demote to a `dek` paragraph below the title |
| **Slug** | _(empty)_ | `make-culture-not-content` |
| **SEO title** | _(empty)_ | `Make Culture, Not Content: AI Field Manual \| Kris Krüg` (54 chars) |
| **Meta description** | _(empty)_ | `Generative engines now spill out adequate everything. Your value is shifting from production to selection, orchestration, and meaning-making — a field manual.` (160 chars) |
| **Excerpt** | _(empty)_ | Same as meta description |
| **Social share text** | _(empty)_ | `The market doesn't need more artifacts; it's drowning in them. What it needs is authored judgment — taste that can be explained, defended, and taught.` |
| **Category** | Misc (id 1) | **AI for Creatives** *(needs to be created)* |
| **Tags** | _(none)_ | `ai-creatives`, `theupgrade-ai`, `manifesto`, `field-manual`, `creative-strategy`, `taste`, `human-plus-plus` |
| **Featured image** | none (id 0) | KK to pick — suggest something abstract/maximalist that signals "field manual" or "synthetic age". Photo of a workshop, lab, or symbolic creative-tech imagery |
| **Date** | 2025-09-23 | KK's call: keep original (looks like September 2025 thinking) or refresh to 2026-05-15 for ranking lift (Google likes recent) |

## Body fixes (auto-applied)

1. **Encoding cleanup:** all 38 `?`-char artifacts → hyphens (or en-dashes for `0?5` ranges)
2. **In-body H2 demotion:** the opening italic `<h2>A FIELD MANUAL...</h2>` could stay as h2 OR convert to a "dek"-style paragraph (`<p class="has-text-align-center"><em>A field manual for creative pros in the synthetic age</em></p>`). Visual call.
3. **`<cite>` on quotes:** the post has 5+ blockquotes (worldview injection prompt, weirdifier prompt, selector scoring prompt, humanize pass prompt) — these are KK's own prompt cards, no external citation needed
4. **Standardize ALL CAPS section headings**: KK's choice — keep ALL CAPS as a stylistic choice, OR convert to title case. ALL CAPS reads as shouting in 2026. Suggest title case throughout.

## Internal-link enrichment (KK confirms)

| Text in body | Suggested target |
|---|---|
| `BC + AI Ecosystem` (likely in author bio if present) | `https://bc-ai.ca/` |
| `TheUpgrade.ai` (likely in author bio) | `https://www.theupgrade.ai/` |
| References to "selectors" / "taste" | Cross-link to `/2026/01/28/your-taste-is-your-moat/` (after #11178 publishes — these two pieces are sibling content) |
| `mycelial network` reference (line 67) | Link to `/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/` (existing post) |
| `90-day program` | If KK has a TheUpgrade.ai cohort page, link to it |

## External-link enrichment (KK confirms)

The piece references these implicitly — no explicit external links currently:
- "Attention Cartel" (could link to coined-by source if known)
- "decolonial turn" (could link to a foundational text or thinker)
- "Hyper-partnered innovation" — KK's own framing; no external needed

## Things KK should review

- ALL CAPS or title case for section headings? (style call)
- Keep the September 2025 draft date or refresh to today?
- Any specific tags KK wants instead of my suggestions?
- Featured image preference: photographic (workshop/community) vs abstract (synthetic age aesthetic)?
- Want this to be the sister piece to "Your Taste Is Your Moat"? If yes, both should cross-link.

## Publish flow

1. Apply 38 encoding fixes via REST PATCH to body
2. Apply metadata via REST PATCH (slug, excerpt, all SEO meta, categories, tags)
3. Featured image: KK picks OR I select from media library
4. Status: `draft` → `publish`
5. Post-publish: curl + verify schema + GSC indexing request
