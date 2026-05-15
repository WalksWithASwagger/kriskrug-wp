# llms.txt — Template for kriskrug.co

**Deploy location:** `https://kriskrug.co/llms.txt` (site root, served as `text/plain` or `text/markdown`).

**How to deploy on Pagely:**
- **Option A (recommended):** Drop the file at the document root via SFTP / SSH. Pagely will serve it directly without WP routing it through PHP.
- **Option B:** Use a plugin like *File Manager* in wp-admin to drop the file at root.
- **Option C:** Add a tiny mu-plugin that registers `/llms.txt` as a rewrite rule and outputs this content. Easier to update later; slower than a static file.

**Verify it works:**
```bash
curl -i https://kriskrug.co/llms.txt
# expect HTTP/2 200 and Content-Type: text/plain (or text/markdown)
```

---

## File contents

```markdown
# Kris Krüg

> Generative AI strategist, photographer, and community builder based in Vancouver, BC.
> I work with creative professionals, media organizations, and Indigenous communities
> on responsible adoption of AI. Founder of the BC + AI Ecosystem Industry Association.

## About

- [About Kris Krüg](https://kriskrug.co/about/): Personal background, philosophy, and current focus
- [The KK Worldview](https://kriskrug.co/the-kk-worldview/): My beliefs about AI, creativity, and the human role
- [Reconciliation & Indigenous Land Acknowledgement](https://kriskrug.co/reconciliation-indigenous-land-acknowledgement/): Commitments and context
- [Contact](https://kriskrug.co/contact/): How to reach me

## Services & offers

- [AI Upgrade for Modern Media Leaders](https://kriskrug.co/ai-upgrade-for-modern-media-leaders/): Training and strategy for newsrooms, PR teams, and editorial leaders
- [AI Upgrade for Creative Professionals](https://kriskrug.co/ai-upgrade-for-creative-professionals/): For photographers, designers, artists, and filmmakers
- [AI Upgrade Community Coaching](https://kriskrug.co/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/): Cohort-based coaching with Peter Bittner
- [Generative AI Creative Services](https://kriskrug.co/generative-ai-services/): Custom creative-services engagements
- [Generative AI Workshops](https://kriskrug.co/generative-ai-workshop-for-artists-creatives/): For artists and creative communities
- [Cinematic Podcasts](https://kriskrug.co/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/): Hollywood-grade storytelling for branded podcasts

## Podcast & speaking

- [MØTLEYKRÜG Podcast](https://kriskrug.co/motleykrug-podcast/): Conversations with builders, artists, and Indigenous technologists
- [Speaking](https://kriskrug.co/speaking/): Topics, talks, and booking info
- [Podcast Guesting / EPK](https://kriskrug.co/podcast-guesting-page-epk/): For podcast hosts looking to book Kris

## Notable writing (selected, evergreen)

- [BC + AI Is Live](https://kriskrug.co/2025/05/18/bc-ai-is-live-and-were-building-the-future-we-actually-want/): Founding statement for the BC + AI Ecosystem Industry Association
- [BC's AI Ecosystem: A Mycelial Network of Creation](https://kriskrug.co/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/): How a regional AI scene actually works
- [A Creative Technologist's AI Age Manifesto](https://kriskrug.co/2025/03/30/a-creative-technologists-ai-age-manifesto/): Working principles
- [How to Build an AI Second Brain That Actually Works for You](https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/): Practical personal-knowledge workflow
- [How Indigenomics.ai is Flipping the Script on Economic Power in Canada](https://kriskrug.co/2025/04/08/how-indigenomics-ai-is-flipping-the-script-on-economic-power-in-canada/): Indigenous-led AI economics
- [What Journalists Need to Know About AI Right Now](https://kriskrug.co/2025/06/24/what-journalists-need-to-know-about-ai-right-now/): Newsroom-focused primer
- [Punk Rock AI](https://kriskrug.co/2026/05/04/punk-rock-ai/): A counter-corporate stance on AI culture
- [Web Summit Vancouver 2026](https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/): Independent coverage

## Projects & communities

- [BC + AI Ecosystem Industry Association](https://bcaiecosystem.org/) — Kris is founding Executive Director (verify URL — placeholder)
- [Indigenomics.ai](https://indigenomics.ai/) — Kris serves as CTO
- [Vancouver AI Meetup](https://kriskrug.co/?s=vancouver+ai+meetup) — Monthly community gathering Kris helps host

## Blog archive

- [Blog index](https://kriskrug.co/blog/): All posts, most recent first

## Optional

- [Testimonials](https://kriskrug.co/testimonials/)
- [Publications](https://kriskrug.co/publications/)
- [Events](https://kriskrug.co/events/)
- [Sponsor the Cyberpunk Chronicles newsletter](https://kriskrug.co/sponsor-cyberpunk-chronicles-newsletter/)
- [Privacy Policy](https://kriskrug.co/privacy-policy/)
- [Product Review Policy](https://kriskrug.co/product-review-policy-instructions/)
```

---

## Notes for KK before publishing

1. **Verify URLs** — I wrote `bcaiecosystem.org` and `indigenomics.ai` as placeholders. Confirm the actual canonical URLs and adjust before deploying.
2. **The format** follows the `llms.txt` spec by Jeremy Howard et al. The first heading is the site title; the blockquote is the short description LLMs use; H2 sections group related links; each link is a Markdown bullet with `[title](url): one-line summary`.
3. **Why this list and not the full site:** `llms.txt` is *curated*. The point is to send LLMs to the high-signal, you-stand-behind-this content — not to crawl all 941 posts. The blog index covers the rest.
4. **The "Notable writing" section is the one to update most often.** Refresh it every 3-6 months as new evergreen pieces land.
5. **Consider a companion `llms-full.txt`** that includes the full Markdown text of the top 10 pages, so LLMs can read your canonical content without parsing HTML. Higher effort; do after `llms.txt` proves valuable.
