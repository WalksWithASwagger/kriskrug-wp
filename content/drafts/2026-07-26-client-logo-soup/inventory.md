# Source inventory (#413)

Searched 2026-07-26. Goal: locate Peter-era Upgrade AI logo + testimonial work before building.

## Searched

| Location | Result |
|----------|--------|
| `content/source-packs/` | Speaking testimonial bank (`keynotes-2026/testimonial-bank.md`); no client logo images |
| `content/source-packs/keynotes-2026/wp-payloads/about.html` | Text chip list under "Clients, collaborators, and rooms served" (see `client-list-for-kk.md`) |
| `theme/kk-aurora/` | No client logo assets; brand logo CSS only (`.aurora-brand-logo`) |
| Repo binary search (`*.svg` / `*.png` / `*logo*`) | No client logo files committed |
| kriskrug.co media API (`/wp-json/wp/v2/media?search=…`) | See media hits below |
| `https://www.theupgrade.ai/` | Site is a "We've moved" notice (brand wrapped). Only Upgrade wordmark + Peter/Kris portraits. No enterprise logo soup |
| Notion MCP | Unavailable this session (`needsAuth`). Prior issue comment (2026-07-19) already noted Upgrade testimonials live in `kk-kb` vault, not as logos |
| `kk-kb` sibling vault | Not mounted in this Cloud agent environment |

## What exists (usable as *text* / context, not logo soup)

### Upgrade / speaking testimonials (hover-note candidates)

From `content/source-packs/keynotes-2026/testimonial-bank.md` (already gated for live use):

- **Jai Djwa** (approved): design-orchestrator / student prototypes quote
- **Ed Kennedy** (approved): community organizing / event design quote
- Audience feedback lines (generic attribution only)

Prior issue inventory also listed `kk-kb/data/testimonials/TESTIMONIAL_20251018_00{1..10}.txt` and Upgrade case studies (`armin`, `lizzie`). Those paths are **not** in this repo checkout; treat as external until vault is available.

### Live / About name lists (not logos)

About wild-index clients (text spans only). Full candidate shortlist in `client-list-for-kk.md`.

Homepage today (`theme/kk-aurora/templates/front-page.html`):

- `#stages` / `.aurora-proof-outlets`: **stage names as text** (TED, SXSW, Adobe MAX, …). Not client logos.
- Historical template snapshots used the line **"Proof without the logo soup."** with media outlet *text* spans (BBC, WIRED, Forbes, …). That was deliberate avoidance of logo soup, not a logo asset library.

### Media library hits that look like "logo" but are the wrong set

| Media ID | Slug | What it actually is | Use for #413? |
|----------|------|---------------------|---------------|
| 5825 | `fpc-logo-5` | Future Proof Creatives brand exploration (skull / rose / FPC wordmark), 1024² PNG | No (own brand art) |
| 5528 | `fpc-logo-11` | Same FPC exploration set | No |
| 5195 | `fpc-logo-7` | Same FPC exploration set | No |
| 5194 | `fpc-logo-3` | Same FPC exploration set | No |
| 4381 | `logo_and_bug_sq` | Punk Rock AI / KK bug mark, 600² PNG | No (site brand) |
| 9377 | `bc-ai-header` | BC + AI own header art | No (unless KK wants ecosystem partners, not clients) |
| 7932 | `2024-recap-cbc` | CBC segment recap graphic (not a CBC logo lockup) | No |

Searches for `lululemon`, `hootsuite`, `microsoft`, `samsung`, `redbull`, `american-express`, `cibc`, `getty`, `pentagram`, `jones-soda` against the media API returned **no** logo files.

Partner/sponsor search returns unrelated photos and AI-synth stills, not logo marks.

## Blocker (unchanged from 2026-07-19 comment)

**No client-logo image assets** for the "drop-dead best clients" roster exist in this repo or in the public media library under searchable brand names.

## To unblock

1. KK/Peter provide logo files (SVG preferred; mono-friendly transparent PNG OK) or a Drive/Notion folder URL.
2. KK marks which names from `client-list-for-kk.md` may appear publicly with logos.
3. Upload approved logos to kriskrug.co media; record attachment IDs + dimensions in a follow-up row below.

## Media ID ledger (fill after upload)

| Client | File | Media ID | W×H | Alt | 200 OK |
|--------|------|----------|-----|-----|--------|
| _TBD_ | | | | | |

## Distinction to keep sharp

| Band | Purpose | Asset type |
|------|---------|------------|
| `#stages` proof strip | Stages / rooms spoken | Text names (keep) |
| `#clients` logo soup (this issue) | Clients / collaborators | Logo images, mono + interactive |
| `#415` What People Say | Named quotes | Text / optional portraits |
| `#newsletter` (#505 / #416) | Email signup | Untouched by this packet |
