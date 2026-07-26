# Optional Nation website links (#22)

Verified HTTP 200 on 2026-07-26 (follow redirects).

| Nation (English) | Autonym (common orthography) | Official site | Live on Reconciliation page? |
|---|---|---|---|
| Musqueam | xʷməθkʷəy̓əm | https://www.musqueam.bc.ca/ | Yes |
| Squamish | Sḵwx̱wú7mesh | https://www.squamish.net/ | Yes |
| Tsleil-Waututh | səlilwətaɬ / səl̓ilw̓ətaʔɬ (orthographies vary) | https://twnation.ca/ | Yes |

Related (already linked on Reconciliation page, not a Host Nation government site):

| Resource | URL |
|---|---|
| Land Back | https://landback.org/ |

## Recommendation

1. **Keep Nation links on the Reconciliation page** as the canonical place for autonyms + external sites.
2. **Footer:** link the word `Reconciliation` (already present) or add a short "Full acknowledgment" text link next to the acknowledgment sentence. Avoid three external Nation URLs in the brand tile (crowded, easy to miss focus styles, harder on mobile).
3. **About Option C (if used):** one internal link to the Reconciliation page; optional secondary line with Nation links only if KK wants them in-body.

## Markup pattern (About or Reconciliation polish)

Use clear link text (Nation English names), not "click here". Open in same tab by default. Mark external destinations with visible text or an accessible external-link pattern only if the rest of the site already does so consistently.

Example (draft; not applied):

```html
<p>
  I live and work on the traditional, ancestral, and unceded territories of the
  Coast Salish peoples of the
  <a href="https://www.musqueam.bc.ca/">Musqueam</a>,
  <a href="https://www.squamish.net/">Squamish</a>, and
  <a href="https://twnation.ca/">Tsleil-Waututh</a> Nations.
  <a href="/reconciliation-indigenous-land-acknowledgement/">Full acknowledgment</a>.
</p>
```

## KK picker

- [ ] Nation links stay on Reconciliation page only (recommended with footer Option A)
- [ ] Footer gets internal "Full acknowledgment" link beside Option A sentence
- [ ] About Option C includes Nation links in-body
- [ ] Other: _______________________
