# R9 cream smell test — Track A

**When:** 2026-07-25 01:26 UTC  
**Pages patched (live):**

| Route | ID | Status |
|---|---|---|
| /speaking/ | 1887 | cream pack + `.kk-r9-pack` drop-cap kill |
| /about/ | 1208 | cream pack + `.kk-r9-pack` drop-cap kill |
| /work/ | 2672 | cream pack + `.kk-r9-pack` drop-cap kill |
| /photography/ | 12013 | cyan tokens removed; cream page chrome; cinematic hero retained |
| /sponsor-deck/ | 12625 | `.kk-sponsor` retokenized to cream/ink |

**Source packs:**
- `content/source-packs/content-architecture-2026/wp-payloads/{speaking,about,work,photography}.html`
- `content/source-packs/keynotes-2026/wp-payloads/photography.html` (mirror)
- `content/drafts/2026-07-24-sponsor-deck/post.html`

**Verify:**
- API `content.raw` for all five: **no** `#00E5FF` / `00e5ff`
- Public HTML: only remaining `00E5FF` is theme preset `--wp--preset--gradient--aurora-cyan-teal` (not pack chrome)
- Browser smell test: photography + sponsor-deck + speaking cream/ink; no cyan accents in pack UI

**Rollback:** before/after JSON under this directory (`page-*-before-*.json`).
