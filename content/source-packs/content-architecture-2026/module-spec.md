# Aurora Content Module Spec

## Allowed Vocabulary

Use the existing Aurora content primitives:

- `aurora-page-lead`
- `aurora-section-kicker`
- `aurora-display-heading`
- `aurora-card-grid`
- `aurora-card`
- `aurora-media-card`
- `aurora-proof-section`
- `aurora-proof-grid`
- `aurora-proof-module`
- `aurora-button`

The payloads may also use Gutenberg wrapper comments such as `<!-- wp:html -->`. They must not add new page-specific CSS namespaces.

## Authoring Rules

- One template H1 only. Payloads must not include `<h1>`.
- One body display heading maximum per page.
- Body copy should be short enough to scan, but not reduced to tiny labels.
- Each first-wave page needs a lead, 2-5 scannable sections, proof or media where useful, and a clear next action.
- Use real image assets from the current page content where possible.
- Use plain links and `aurora-button` for calls to action.
- Do not include inline `<style>` blocks.
- Do not include Notion, temporary, or private asset URLs.
- Do not use retired class prefixes: `kk-*`, `kkp-*`, `kkx-*`, `kk-services-*`, or `kk-publications-*`.

## Page Families

| Family | Pages | Pattern |
|---|---|---|
| Offer | Services, Speaking, RAP | Lead, offer cards, proof, CTA |
| Trust | About | Lead, current rooms, proof trail, CTA |
| Portfolio / proof | Work | Featured systems, proof grid, creative lab, CTA |
| Media booking | Podcast EPK | Topics, appearances, producer assets, CTA |
| Utility | Contact | Routing cards, email CTA, response guidance |
