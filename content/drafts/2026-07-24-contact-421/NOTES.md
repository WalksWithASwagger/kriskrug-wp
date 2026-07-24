# Contact page — #421

**WP page ID:** `2418`  
**Live:** https://kriskrug.co/contact/  
**Payload source:** `content/source-packs/content-architecture-2026/wp-payloads/contact.html`

## Change (2026-07-24)

- Add Michelle Diamond close portrait from media ID `12627`
- Services-aligned layout: hero + photo, what-to-include cards, email + newsletter panels
- Plain “newsletter” language + Beehiiv CTA (`https://kriskrug.beehiiv.com/`)
- Preserve mailto recipient: `feelmoreplants@gmail.com` (no form routing change — page had no contact form)

## Snapshot / rollback

- `rest-page-2418-before-portrait-*.json`
- `content-before.html`

Restore by POSTing `content-before.html` to page `2418`.

## Out of scope (theme)

Site header/footer still say “Dispatch” / “Join the dispatch” — Track B / new theme. Content pack itself has zero “dispatch”.
