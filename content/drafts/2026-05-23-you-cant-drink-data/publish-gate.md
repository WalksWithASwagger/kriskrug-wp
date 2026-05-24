# Publish Gate

Status: staged; WordPress DRAFT to be created via `publish_you_cant_drink_data.py --execute`.
Do NOT publish without KK review. Part of a **coordinated 3-post drop** (11882, 11929, this).

## Source

- kk-kb PR #1994, branch `claude/vancouver-ai-protest-piece-5Ax2i`
- `content/communications/blog-posts/2026-05-23-you-cant-drink-data-first-ai-protest.md`

## Editorial decisions (KK, 2026-05-23)

- [x] All 33 em-dashes rewritten in KK's voice (not regex-purged into comma run-ons).
- [x] Trailing "About" bio paragraph stripped (redundant with WP author metadata). Closing disclaimer note kept.
- [x] 4 pull quotes: "You can't drink data" / "A 17-year-old just turned my footnote into a chant on a bridge..." / "Refusal and boosterism are the same move wearing different costumes" / "...they're not the opposition. They're the recruiting pool."
- [x] In-body signs: WE ARE THE TRAINING DATA (11920), WATER THE SERVERS LAST (11918), I LOVE THE CLOUD I JUST WANT IT TO RAIN (11928).
- [x] AI-sign gallery (14 signs, reused media — no re-upload).
- [x] **Real march-photo gallery DONE.** From KK's 182-photo zip: triaged all 182 via contact sheets, selected **26 unique signs** (deduped), web-optimized (2000px, gentle auto-contrast, EXIF/GPS stripped), uploaded (media 11937–11962) + 3 in-body narrative photos (Granville march 11963, KK on the bridge 11964, City Hall crowd 11965). Draft 11936 updated via `--update`; all 13 checks green; gallery + in-body verified rendering in Aurora.
- [x] Links hand-placed + verified; companion cross-links to 11882 / 11929.

## Required review before coordinated publish

- [ ] KK reviews preview (`?p=<id>&preview=true`).
- [ ] Drop real protest-sign photos into `photos/` (+ optional `photos/captions.txt`: `filename|alt`), re-run to add the photo gallery.
- [ ] Confirm SEO title + meta description.
- [ ] Coordinated publish: flip 11882, 11929, and this to `publish` together.
- [ ] Purge Pagely page cache; logged-out render check of all 3 + every cross-link.

## Safety notes

- Draft-first; `--execute` creates DRAFT only. Script never publishes.
- Create-only slug guard (aborts on existing `you-cant-drink-data`).
- No private Notion/material in the body; first-person dispatch from KK's own audio + photos.
