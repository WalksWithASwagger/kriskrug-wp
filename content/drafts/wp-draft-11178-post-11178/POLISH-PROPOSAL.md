# Polish proposal — Why Judgment Beats "Creativity" in the AI Era (post 11178)

**Current state:** draft, modified 2026-01-28, 2,032 words, no slug, no excerpt, no SEO meta, no featured image, uncategorized, no tags, zero links in body.

Edit URL: https://kriskrug.co/wp-admin/post.php?post=11178&action=edit

## Proposed metadata

| Field | Current | Proposed |
|---|---|---|
| **Title (H1)** | "Why Judgment Beats 'Creativity' in the AI Era" | unchanged |
| **In-body H1** | "Your Taste Is Your Moat" (line 6) | demote to H2 (only one H1 per page) |
| **Slug** | _(empty)_ | `your-taste-is-your-moat` *(more memorable than the title)* |
| **SEO title** | _(empty)_ | `Your Taste Is Your Moat: Why Judgment Beats AI \| Kris Krüg` (60 chars) |
| **Meta description** | _(empty)_ | `Generation has been commoditized. Selection hasn't. The DJs figured this out in the '80s — taste is the moat.` (108 chars) |
| **Excerpt** | _(empty)_ | Same as meta description (Jetpack uses excerpt as fallback) |
| **Social share text** | _(empty)_ | `Generation is cheap. Selection is not. Your taste is your moat — what taste actually does in the age of AI.` |
| **Category** | Misc (id 1) | **AI for Creatives** *(needs to be created — see CONTENT_AUDIT proposed IA)* |
| **Tags** | _(none)_ | `ai-creatives`, `taste`, `judgment`, `theupgrade-ai`, `creative-professionals`, `selectors` |
| **Featured image** | none (id 0) | KK to pick — suggest a portrait of a DJ booth or hands selecting from records, OR a KK-at-EA-talk photo if available in media library |
| **Date** | 2026-01-28 | unchanged (draft date), or set to today (2026-05-15) for fresher publish date |

## Body fixes (auto-applied via PATCH)

1. **H1 → H2:** the in-body `<h1>Your Taste Is Your Moat</h1>` becomes `<h2>` (the post title is already the page H1)
2. **Section subheading parity:** all current `<h2>` headings stay `<h2>`. Visual hierarchy unchanged.
3. **Add `<cite>` to the two pull-quotes:**
   - The Kevin Friel quote ("There's something very punk rock about taking a tool…") gets `<cite>Kevin Friel</cite>`
   - The OpenAI/Dwarkesh quote gets `<cite>Anonymous, Dwarkesh Patel podcast</cite>`

## Internal-link enrichment (find anchors KK confirms before patching)

Strong opportunities — text that should hyperlink to existing kriskrug.co content:

| Text in body | Suggested target |
|---|---|
| `EA's headquarters last September` | If KK has a post about that EA visit, link to it. Otherwise leave |
| `Kevin Friel` | Link to `/cinematic-podcasts-…/` or his LinkedIn |
| `BC + AI Ecosystem` (author bio) | `https://bc-ai.ca/` or future `/bc-ai/` pillar page |
| `TheUpgrade.ai` (author bio) | `https://www.theupgrade.ai/` |
| `Maya Bruck` | her LinkedIn if KK can share |
| `Dwarkesh Patel's podcast` | The actual episode URL if KK has it |

## External-link enrichment (KK confirms before patching)

| Term | Suggested external link |
|---|---|
| `OpenAI` | https://openai.com/ |
| `Etsy` | https://www.etsy.com/ |

## Things KK should review

- Does "Your Taste Is Your Moat" work as the slug, or prefer `judgment-beats-creativity-ai-era`?
- Anyone Maya Bruck wouldn't want her name in this post linked publicly? (she's named explicitly so she presumably has consented)
- Is there a Kevin Friel cinematic-podcast page on kriskrug.co we should link to? (I see one referenced in the sitemap; needs slug verification)
- Want to update the date to 2026-05-15 so it appears as a recent post, or keep the original 2026-01-28 draft date?

## Publish flow once approved

1. Apply body fixes via REST PATCH (H1→H2, `<cite>` tags, link enrichments)
2. Apply metadata via REST PATCH (slug, excerpt, jetpack_seo_html_title, advanced_seo_description, jetpack_publicize_message, categories, tags)
3. KK uploads featured image OR I select one from existing media → set `featured_media`
4. Status: `draft` → `publish` (KK's call: live now, or stay as draft for one more review pass?)
5. Post-publish: curl + verify schema renders, submit URL to GSC for indexing
