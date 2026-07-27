# Notes: safety, collisions, next steps

## Newsletter collision (PR #505 / #416)

Do **not** touch in this lane:

- `theme/kk-aurora/templates/front-page.html` newsletter block (`#newsletter`, `.aurora-newsletter-band`)
- `theme/kk-aurora/templates/home.html` newsletter copy
- `theme/kk-aurora/assets/css/revive-port.css` newsletter rules
- `content/drafts/2026-07-26-newsletter-section/`

`#stages` sits above the archive / work / services / writing / newsletter stack. Future Track B build for #414 should patch **only** the `aurora-proof-strip` section (and new CSS classes scoped to stages). Leave newsletter markup and Option C copy from PR #505 alone.

Also avoid reusing newsletter vocabulary ("field notes", "dispatch", "weekly email", Beehiiv CTA) inside the stages band.

## Adjacent issues (coordinate, do not merge)

| Issue | Relationship |
|---|---|
| #419 Speaking page multimedia | Share video + photo inventory; homepage teases, Speaking page sells |
| #413 Client logo soup | Different section; do not combine into `#stages` |
| #415 What People Say | Testimonials stay out of this strip |
| #412 Creative Labs | Separate band |

## Safety (from issue + AGENTS.md)

- Concept approval gate before build
- Aurora package deploy with rollback ref when theme lands
- No live WP writes from this draft packet
- Slug/URL verification before any publish of companion posts still in `content/drafts/`

## Suggested build sequence (after KK pick)

1. KK picks concept + copy option + engagement set  
2. Ingest missing stage photos to media library  
3. Track B branch: replace `#stages` markup + CSS only  
4. Logged-out link + contrast + breakpoint QA  
5. Before/after screenshots on the PR  
6. Package deploy with rollback; Pagely purge; logged-out verify  

## Em dash gate

This packet uses hyphens and periods only. Re-check any future copy paste from Notion for Unicode em dashes.
