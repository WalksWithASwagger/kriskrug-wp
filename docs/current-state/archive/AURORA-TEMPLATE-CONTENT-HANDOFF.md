# Aurora Template Content Handoff — Home / Work / Speaking

**Date:** 2026-05-23 · **For:** whoever edits the `kk-aurora` FSE templates (site-editor / theme) — the Aurora agent or KK.

## Why this doc exists

After the Aurora theme switch, **Work (`page-2672`), the Homepage (`front-page`), and Speaking (`page-speaking`) are rendered by Aurora FSE templates that ignore WordPress page content.** So the 2026 roster/voice fixes I made to those pages' content **do not reach the public** — they have to be placed into the *templates* (Track B / theme), which I don't edit. This doc hands over the exact, copy-paste-ready content + assets so those three surfaces tell the true 2026 story.

Generic-template pages (About, Services, Podcast EPK, the new RAP page) are already done, dark-themed, and verified public — not in scope here.

**Source of truth:** roster `[[kk-current-roster-2026]]`, voice `[[kk-voice-cheatsheet]]` (deep wisdom + sassy swagger; receipts not adjectives; name names; no "excited to announce"). Em-dashes are stripped site-wide (house style).

**Aurora design tokens** (if a template wants the card look): bg `#030405`, text `#f0f0f5`, muted `#a6a6b3`, accent cyan `#00e5ff`, eyebrow red `#ff6a6a`, Inter. The full dark `kk-overhaul` `<style>` block (cards, eyebrows, 2×2 grids, glow CTA) is reusable from `content/source-packs/keynotes-2026/wp-payloads/about.html`.

---

## 1) Homepage (front-page template)

**Eyebrow:** Kris Krüg / AI, culture, community
**Title (H1):** Bridging art, AI, Indigenous wisdom, and justice.

**Lead 1:** I build technology programs, communities, keynotes, and learning systems that serve people instead of extraction. My work connects creative practice, responsible AI, and the messy human work of building trust.

**Lead 2 (replaces the stale "CTO for Indigenomics AI" line):** I'm the Executive Director of BC + AI Ecosystem, program lead for the Responsible AI Professional certification, co-founder of The Upgrade AI, and host of the Vancouver AI Meetup and AI Film Club — a creative technologist with 20+ years turning emerging tools into public learning, community infrastructure, and useful action.

**Current-work cards (new roster — replaces BC+AI / Indigenomics / Upgrade trio):**
1. **BC + AI Ecosystem** → https://bc-ai.ca/ — Executive Director building responsible, inclusive AI infrastructure across British Columbia.
2. **Responsible AI Professional** → https://lu.ma/ai-ethics — Program lead for BC + AI's four-week certification that turns AI ethics into daily practice.
3. **The Upgrade AI** → https://www.theupgrade.ai/ — Co-founder helping professionals and teams build practical AI fluency without losing judgment or taste.
4. **AI Film Club** → https://bc-ai.ca/ai-film-club/ — Co-host of the monthly room where filmmakers figure out AI without losing the plot.
5. **Vancouver AI Meetup** → https://bc-ai.ca/events/ — Host & curator of the room that started it all.

**Proof markers (drop the "$100B Indigenomics" one):** 250+ BC+AI members · 3,000+ event attendees · 94+ community events · **850+ BC+AI Discord community** · 20+ years bridging art/tech/media/community · Enterprise teams trained.

---

## 2) Work template (page-2672)

Add **Responsible AI Professional** to the featured set and reframe Indigenomics as past.

**RAP featured card:**
- Tag: Certification · Title: **Responsible AI Professional** → https://lu.ma/ai-ethics (or the new page `/responsible-ai-professional/`)
- Image (uploaded to media): `https://kriskrug.co/wp-content/uploads/2026/05/rap-why-we-built-cover.png`
- Copy: *Just launched. A four-week certification that closes the gap between how fast we deploy AI and how slowly we get responsible about it — built with **Martin Lopatka** and **Sarah Downey**. Every grad ships their own ethics assistant.*

**Current featured set:** BC + AI Ecosystem · Responsible AI Professional · The Upgrade AI · (optionally) AI Film Club → https://bc-ai.ca/ai-film-club/ · Vancouver AI Meetup → https://bc-ai.ca/events/

**Indigenomics → past-chapter note (not a current role):** *Past chapter, still load-bearing: through 2024–2025 I was CTO at Indigenomics.ai, building technology for Indigenous economic sovereignty. That work is now embedded in how BC + AI does governance — Indigenous protocol and data sovereignty as defaults, not afterthoughts.*

> Reference markup for these cards (dark `kk-overhaul` look) lives in `content/source-packs/keynotes-2026/wp-payloads/work.html` if useful.

---

## 3) Speaking template (page-speaking)

No new copy queued. Keep **Both Hands Full** as the signature keynote-framework spine; ensure videos/portals current; apply the Aurora dark look. Flag if you want a full voice rewrite of Speaking and I'll draft it (it's a generic-template-or-not question — confirm whether Speaking should move off its custom template).

---

## Links verified (HTTP 200, 2026-05-23)
bc-ai.ca/ai-film-club/ · bc-ai.ca/events/ · lu.ma/ai-ethics · kriskrug.co/2026/01/24/both-hands-full/ · the RAP cover PNG.

## Boundary
I own generic-template page **content** + drafts. The Aurora agent / KK own the **FSE templates** (Work/Speaking/Home) + theme. This doc bridges the two — paste this content into the templates and the whole site tells one true 2026 story.
