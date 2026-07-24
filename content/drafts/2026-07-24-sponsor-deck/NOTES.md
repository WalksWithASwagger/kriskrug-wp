# Sponsor Deck — Review Notes

**Issue:** [#459](https://github.com/WalksWithASwagger/kriskrug-wp/issues/459)  
**Intended slug:** `/sponsor-deck`  
**Post type:** WordPress page (not a blog post)  
**Status:** Draft only — do not publish without human approval.

## Human gates before publish

1. **Metrics approval** — Replace or confirm every number marked `[UNVERIFIED]` in `post.html`.
2. **Brand review** — Copy tone, package names, pricing tiers, and CTA destinations.
3. **Publish approval** — KK sign-off; then dry-run → slug-match → publish per `scripts/notion-to-wp/README.md`.

## Unverified claims (need source or replacement)

| Location | Claim | Notes |
|----------|-------|-------|
| Hero metrics | `5.4k+` Discord/community followers | No source cited in draft; confirm current count or remove. |
| Hero metrics | `32%` average engagement on sponsor-led moments | No methodology or sample; confirm or remove. |
| Hero metrics | "Top-tier" profiled for startup/AI networks | Qualitative; confirm acceptable or soften. |
| Packages | Starter `$2,500` | Pricing placeholder until KK confirms. |
| Packages | Growth `$7,500` | Pricing placeholder until KK confirms. |
| Packages | Command `$15,000` | Pricing placeholder until KK confirms. |
| CTA | `partnerships@kriskrug.co` | Confirm mailbox is live and monitored. |
| CTA | `/sponsor` media kit link | Confirm target page exists or update URL. |
| CTA | `/events` link | Confirm target page exists or update URL. |

## Coherence check

- `post.md` frontmatter matches intended slug `sponsor-deck` and page type.
- `post.html` is self-contained WP HTML block with inline styles; no external asset dependencies.
- No secrets or env values in this pack.

## Out of scope for this PR

- WordPress publish or live edits.
- Photography packs, media ingest scripts, or connector changes.
