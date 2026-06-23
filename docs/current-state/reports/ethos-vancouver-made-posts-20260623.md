# Handoff — Ethọ́s Block Party + Vancouver Made posts (2026-06-23)

Two new kriskrug.co project posts authored and staged as WordPress **drafts**, plus two project cards staged in the `kk-aurora` theme. Nothing public or deployed yet. This branch holds the local artifacts; publish + deploy are gated on KK.

## What shipped (local + WP drafts)

### Posts (live as drafts on kriskrug.co)
| Post | WP draft ID | Edit URL |
|------|-------------|----------|
| One Booth, One Afternoon, Eleven Songs: The Ethọ́s Lab Block Party Album | **12357** | https://kriskrug.co/wp-admin/post.php?post=12357&action=edit |
| Everyone Else Made a Souvenir. We Made the Receipt. (Vancouver Made / MADE ON) | **12363** | https://kriskrug.co/wp-admin/post.php?post=12363&action=edit |

- Draft packages: `content/drafts/2026-06-23-ethos-lab-block-party/`, `content/drafts/2026-06-23-vancouver-made-world-cup/` (post.md, post.html, seo-meta.md, alt-text.md, internal-links.md, images/, publish.log).
- Both: category `AI for Creatives`, showpiece blocks (pullquotes + separators + galleries), KK voice, zero em dashes, every hyperlink curl-checked 200, all images rewritten to kriskrug.co uploads.
- Ethọ́s: 7 album-art images (no faces), 13 links. Vancouver Made: 11 kit/award images, 17 links.

### Theme (staged, not deployed)
- `theme/kk-aurora/parts/work-proof-grid.html`: two new cards in the `/work/` proof grid (Ethọ́s Block Party, Vancouver Made / MADE ON), grid 4 → 6.
- `theme/kk-aurora/parts/footer.html`: two new "Projects" links.
- `theme/kk-aurora/style.css`: version 1.3.22 → **1.3.23**.

### Tooling
- `scripts/notion-to-wp/update_local_wp_draft.py`: new in-place draft updater (companion to the create-only `create_local_wp_draft.py`); reuses its build pipeline, guards on draft status + slug, dry-run default.

## Consent gate (honored)
Ethọ́s minors (Aster, Caleb) are first-name-only and never linked or shown as faces; only AI-generated album art used; nothing published that is not already on the public `/the-day` page. A blurry candid (`bts-v05-poster`) was pulled for showing real attendees.

## Gotcha + fix
Jetpack SEO post-meta REST writes 500 on the combining-diacritic "Ethọ́s" (U+1ECD + U+0301). Body/title keep the diacritics; SEO meta uses plain "Ethos"/"Krug". Recorded in memory `jetpack-seo-meta-combining-diacritic-500`.

## Next steps (gated on KK; not in this branch)
1. KK reviews drafts 12357 / 12363; approve copy + confirm Vancouver Made category (AI for Creatives vs Vancouver AI Ecosystem).
2. Publish both posts so `/ethos-lab-block-party/` and `/vancouver-made-world-cup/` resolve (the card "Read the story" buttons point there).
3. Deploy kk-aurora 1.3.23 (wp-admin zip re-upload; SFTP/SSH blocked).
4. Pagely purge `/work/`, the homepage, and both post URLs.
5. Verify logged-out: both posts live, both `/work/` cards visible, network links resolve, OG/SEO meta present.
6. Optional: open a PR for this branch; queue social (Vancouver Made Buffer drafts already exist in the vancouver-made repo).
