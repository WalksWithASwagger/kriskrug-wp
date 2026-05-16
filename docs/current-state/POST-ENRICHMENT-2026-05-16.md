# Post enrichment pass — 2026-05-16

After KK's "do an SEO audit + enrich" brief, both live posts (Your Taste + Make Culture) received a comprehensive enrichment pass. This doc captures what changed and the new rules going forward.

## Changes applied to both posts

| Item | Your Taste (#11178) | Make Culture (#10594) |
|---|---|---|
| em-dashes purged (— → ", ") | 23 | 35 |
| internal cross-links added | 1 (Punk Rock AI) | 2 (Mycelial Network, Punk Rock AI) |
| external proper-noun links added | 6 (Kevin Friel, Maya Bruck, Etsy, Dwarkesh Patel, EA, OpenAI) | 0 (post is more conceptual, fewer name-drops) |
| slide image uploaded + inserted | id 11828 (`13-selector-taste-is-your-moat.png`) | id 11829 (`15-ship-culture-not-content.png`) |
| existing sister-piece cross-link | ✓ to Make Culture | ✓ to Your Taste |

## New rules for the connector going forward

These should become defaults in `scripts/notion-to-wp/kk_notion_to_wp.py`:

1. **No em-dashes.** KK: *"we gotta have a no-em-dash rule across the board and sweep for that shit. It just screams AI."* Replace `—` with `, ` (comma + space) by default. KK reviews any awkward conversions in wp-admin.

2. **Auto-link KK's prior posts** when their topic keywords appear in body. Maintain a small registry of `{phrase: kriskrug.co URL}`:
   - "both hands full" → `/2026/01/24/both-hands-full/`
   - "punk rock" → `/2026/05/04/punk-rock-ai/`
   - "calling us all in" → `/2026/05/14/calling-us-all-in/`
   - "web summit vancouver 2026" → `/2026/05/07/web-summit-vancouver-2026/`
   - "mycelium" / "mycelial network" → `/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/`
   - "your taste is your moat" → `/2026/05/15/your-taste-is-your-moat/`
   - "make culture, not content" → `/2026/05/16/make-culture-not-content/`

3. **Auto-link proper nouns** when they appear and we have a verified URL:
   - People: Kevin Friel, Maya Bruck, Dwarkesh Patel, Dr. Joy Buolamwini, Anthony Joseph, Corey Doctorow, Matt Lambert, etc.
   - Orgs/products: Etsy, EA, OpenAI, Anthropic Claude, Web Summit, BC + AI, TheUpgrade.ai, Indigenomics.ai
   - Auto-add `target="_blank" rel="noopener noreferrer"` for external

4. **Only first occurrence is linked.** Don't over-link the same term repeatedly.

5. **Respect existing `<a>` tags** — never link inside an existing link.

## Backup completed

UpdraftPlus first full backup completed 2026-05-16 06:53 Pacific.
- Database, Plugins, Themes, Uploads, Must-use plugins, Others — all present
- Server location: `/wp-content/updraft/` (Pagely)
- Web-server disk space used by UpdraftPlus: 13.1 GB
- Local download: pending (KK to click download buttons OR I drive Chrome MCP to do it)

## Outstanding items for KK to confirm

- [ ] YouTube URL for the embed KK mentioned
- [ ] Which photos from "that night" to use, and where they live (Notion / Drive / local?)
- [ ] Featured image swap? Currently Your Taste uses `ai-creatives-krug.jpeg`, Make Culture uses `06-mycelial-action-network.png`. Now that we have the on-brand punk-zine slides uploaded, KK can decide if those should be the featured images (vs in-body)
