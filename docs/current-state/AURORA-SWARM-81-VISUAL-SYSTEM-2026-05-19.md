# Aurora Swarm #81 - Visual System Checklist (2026-05-19)

Track: B (Aurora v2 theme)
Issue: [#81](https://github.com/WalksWithASwagger/kriskrug-wp/issues/81)
Branch: `codex/swarm-81-visual-system`
Scope: token, typography, interaction-state hardening only

## Acceptance Criteria Checklist

- [x] `theme.json` tokens reflect type, color, spacing, button, radius, and focus-state decisions.
  - Added token groups under `settings.custom`: `motion`, `button`, `focus`, `glass`.
  - Updated token `text-muted` from `#6B6B80` to `#7C7C98` to clear AA body/caption contrast on dark surfaces.
  - Wired link/button focus outlines to shared focus tokens and button spacing/radius to shared button tokens.

- [x] CSS defines a restrained glass/liquid morphism system with clear usage rules.
  - Added `.aurora-glass-nav` for nav chrome only.
  - Added `.aurora-glass-panel` / `.is-style-aurora-glass` for copy-bearing surfaces.
  - Added `.aurora-glass-media` for media containers with inset highlight.
  - Rule: one glass layer per surface; avoid stacked glass-in-glass.

- [x] Typography hierarchy supports homepage hero, page titles, compact panels, long-form articles, metadata, and captions.
  - Added hierarchy utilities: `.aurora-hero-title`, `.aurora-page-title`, `.aurora-panel-title`, `.aurora-article-body`, `.aurora-meta`, `.aurora-caption`.
  - All tiers are tied to theme tokens (`font-size`, `line-height`, `letter-spacing`, muted/meta color).

- [x] Button/CTA system covers primary, secondary, ghost, icon/utility, disabled, hover, active, focus, and mobile tap states.
  - Added variants:
    - `.is-style-aurora-primary`
    - `.is-style-aurora-secondary`
    - `.is-style-aurora-ghost`
    - `.is-style-aurora-utility` / `.is-style-aurora-icon`
  - Added states: `:hover` (fine pointer), `:active`, disabled, `:focus-visible`, coarse-pointer tap sizing.

- [x] Contrast is checked for token pairs used in real templates.
  - Checked from current `theme.json` palette:

| Pair | Ratio | Result |
|---|---:|---|
| `text-primary` on `deep` | 17.06 | Pass AA/AAA |
| `text-secondary` on `deep` | 9.90 | Pass AA/AAA |
| `text-muted` on `deep` | 4.79 | Pass AA |
| `text-primary` on `surface` | 16.40 | Pass AA/AAA |
| `text-secondary` on `surface` | 9.52 | Pass AA/AAA |
| `text-muted` on `surface` | 4.61 | Pass AA |
| `cyan` on `deep` | 12.60 | Pass AA/AAA |
| `teal` on `deep` | 8.30 | Pass AA/AAA |
| `deep` on `cyan` (primary CTA) | 12.60 | Pass AA/AAA |
| `deep` on `teal` (hover CTA) | 8.30 | Pass AA/AAA |

- [x] Motion tokens exist for reveal, depth, continuity, proof, micro-interaction, and reading states.
  - Added motion tokens: `revealDuration`, `depthDuration`, `continuityDuration`, `proofDuration`, `microDuration`, `readingDuration`, plus reduced-motion fallback token.

- [x] Documentation points back to the visual redesign audit.
  - This checklist references issue `#81` and the active Aurora review packet at `docs/current-state/AURORA-REVIEW-PACKET-2026-05-19.md`.
  - `docs/current-state/AURORA-VISUAL-REDESIGN-AUDIT-2026-05-18.md` has been restored to the Track B branch as the canonical audit anchor referenced by issue `#81`.
  - `docs/current-state/AURORA-REVIEW-PACKET-2026-05-19.md` now points at the current `origin/aurora/v2` review baseline and merged Wave 1/2 evidence.

## Reduced Motion + Focus Evidence

- Reduced motion:
  - `@media (prefers-reduced-motion: reduce)` now forces near-zero duration, no animation, and no transform for glass/button interaction surfaces.
- Focus:
  - `:focus-visible` treatment is tokenized via `--wp--custom--focus-*` values and applied consistently to links/buttons.
  - Offset-color + glow are included to preserve focus visibility on dark/glass backgrounds.

## Validation Commands Run

```bash
jq empty theme/kk-aurora/theme.json
rg -n "\"motion\"|\"focus\"|\"glass\"|\"button\"" theme/kk-aurora/theme.json
rg -n "aurora-glass|aurora-hero-title|is-style-aurora-secondary|focus-visible|prefers-reduced-motion" theme/kk-aurora/assets/css/typography-refined.css
python3 - <<'PY'
import json
from pathlib import Path
data=json.loads(Path('theme/kk-aurora/theme.json').read_text())
p={c['slug']:c['color'] for c in data['settings']['color']['palette']}
def h2r(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def lin(c): return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def lum(h): r,g,b=h2r(h); return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def contrast(a,b): L1,L2=sorted([lum(a),lum(b)],reverse=True); return (L1+0.05)/(L2+0.05)
for fg,bg in [('text-muted','deep'),('text-muted','surface'),('deep','cyan')]:
    print(fg,bg,round(contrast(p[fg],p[bg]),2))
PY
```
