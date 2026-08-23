# Aurora Brand Reference

Generated 2026-08-23T01:14:33Z from KK Aurora 1.6.9.

This is a repository-derived reference, not proof of the live theme. Before publication, run `make status-readonly` and confirm live/repo Aurora version agreement.

Source aliases:

- `theme.json`: `theme/kk-aurora/theme.json`
- `02-tokens.css`: `theme/kk-aurora/assets/css/02-tokens.css`
- `style.css`: `theme/kk-aurora/style.css`

## Surfaces

| Role | Value | Source |
|---|---|---|
| Primary surface | `#efe6d2` | 02-tokens.css `--kk-surface` → theme.json `--wp--preset--color--paper` |
| Sunk surface | `#e6dcc2` | 02-tokens.css `--kk-surface-sunk` → theme.json `--wp--preset--color--surface` |
| Raised surface | `#e6dcc2` | 02-tokens.css `--kk-surface-raised` → theme.json `--wp--preset--color--elevated` |

## Ink and text

| Role | Value | Source |
|---|---|---|
| Primary ink | `#171310` | 02-tokens.css `--kk-ink` → theme.json `--wp--preset--color--text-primary` |
| Secondary ink | `#3d342c` | 02-tokens.css `--kk-ink-secondary` → theme.json `--wp--preset--color--text-secondary` |
| Muted ink | `#5c5044` | 02-tokens.css `--kk-ink-muted` → theme.json `--wp--preset--color--text-muted` |

## Accent and action

| Role | Value | Source |
|---|---|---|
| Primary accent | `#9a2f14` | 02-tokens.css `--kk-accent` → theme.json `--wp--preset--color--signal` |
| Accent text | `#9a2f14` | 02-tokens.css `--kk-accent-ink` → theme.json `--wp--preset--color--signal-text` |

## Semantic colors

| Role | Value | Source |
|---|---|---|
| Structure / line | `#d9cdb0` | 02-tokens.css `--kk-line` → theme.json `--wp--preset--color--muted` |
| Success | `#1f8a86` | theme.json `--wp--preset--color--success` |
| Warning | `#e8b53a` | theme.json `--wp--preset--color--warning` |
| Error | `#d94a1f` | theme.json `--wp--preset--color--error` |

## Font families

| Role | Value | Source |
|---|---|---|
| Display (Space Grotesk) | `'Space Grotesk', system-ui, -apple-system, sans-serif` | theme.json `--wp--preset--font-family--display` |
| Body (DM Sans) | `'DM Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` | theme.json `--wp--preset--font-family--body` |
| Monospace (JetBrains Mono) | `'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace` | theme.json `--wp--preset--font-family--mono` |

## Type scale

| Role | Value | Source |
|---|---|---|
| Extra Small | `0.75rem (fluid 0.75rem–0.875rem)` | theme.json `--wp--preset--font-size--xs` |
| Small | `0.875rem (fluid 0.875rem–1rem)` | theme.json `--wp--preset--font-size--sm` |
| Base | `1rem (fluid 1rem–1.125rem)` | theme.json `--wp--preset--font-size--base` |
| Large | `1.125rem (fluid 1.125rem–1.25rem)` | theme.json `--wp--preset--font-size--lg` |
| Extra Large | `1.25rem (fluid 1.25rem–1.5rem)` | theme.json `--wp--preset--font-size--xl` |
| 2X Large | `1.5rem (fluid 1.5rem–2rem)` | theme.json `--wp--preset--font-size--2xl` |
| 3X Large | `1.875rem (fluid 1.875rem–2.5rem)` | theme.json `--wp--preset--font-size--3xl` |
| 4X Large | `2.25rem (fluid 2.25rem–3rem)` | theme.json `--wp--preset--font-size--4xl` |
| 5X Large | `3rem (fluid 3rem–4.5rem)` | theme.json `--wp--preset--font-size--5xl` |
| Hero | `3.5rem (fluid 3.5rem–7rem)` | theme.json `--wp--preset--font-size--hero` |

## Layout widths

| Role | Value | Source |
|---|---|---|
| Content width | `800px` | theme.json `settings.layout.contentSize` |
| Wide width | `1280px` | theme.json `settings.layout.wideSize` |
| Reading measure | `66ch` | 02-tokens.css `--kk-measure` |

## Breakpoints

| Role | Value | Source |
|---|---|---|
| Small | `480px` | 02-tokens.css `--kk-bp-sm` |
| Medium | `768px` | 02-tokens.css `--kk-bp-md` |
| Large | `1200px` | 02-tokens.css `--kk-bp-lg` |

## Spacing

| Role | Value | Source |
|---|---|---|
| 1 | `0.25rem` | theme.json `--wp--preset--spacing--10` |
| 2 | `0.5rem` | theme.json `--wp--preset--spacing--20` |
| 3 | `0.75rem` | theme.json `--wp--preset--spacing--30` |
| 4 | `1rem` | theme.json `--wp--preset--spacing--40` |
| 5 | `1.25rem` | theme.json `--wp--preset--spacing--50` |
| 6 | `1.5rem` | theme.json `--wp--preset--spacing--60` |
| 7 | `1.75rem` | theme.json `--wp--preset--spacing--70` |
| 8 | `2rem` | theme.json `--wp--preset--spacing--80` |
| 9 | `2.5rem` | theme.json `--wp--preset--spacing--90` |
| 10 | `3rem` | theme.json `--wp--preset--spacing--100` |
| 12 | `4rem` | theme.json `--wp--preset--spacing--120` |
| 16 | `5rem` | theme.json `--wp--preset--spacing--160` |
| 20 | `6rem` | theme.json `--wp--preset--spacing--200` |
| 24 | `8rem` | theme.json `--wp--preset--spacing--240` |

## Radii

| Role | Value | Source |
|---|---|---|
| Small | `0.25rem` | theme.json `settings.custom.border.radiusSm` |
| Medium | `0.5rem` | theme.json `settings.custom.border.radiusMd` |
| Large | `0.75rem` | theme.json `settings.custom.border.radiusLg` |
| Extra Large | `1rem` | theme.json `settings.custom.border.radiusXl` |
| 2X Large | `1.5rem` | theme.json `settings.custom.border.radius2xl` |
| Full / pill | `9999px` | theme.json `settings.custom.border.radiusFull` |

## Shadows

| Role | Value | Source |
|---|---|---|
| Small | `0 1px 2px rgba(0, 0, 0, 0.5)` | theme.json `--wp--preset--shadow--sm` |
| Medium | `0 4px 6px rgba(0, 0, 0, 0.4)` | theme.json `--wp--preset--shadow--md` |
| Large | `0 10px 15px rgba(0, 0, 0, 0.3)` | theme.json `--wp--preset--shadow--lg` |
| Extra Large | `0 20px 25px rgba(0, 0, 0, 0.25)` | theme.json `--wp--preset--shadow--xl` |

## Buttons

| Role | Value | Source |
|---|---|---|
| Background | `#9a2f14` | theme.json `styles.elements.button.color.background` → theme.json `--wp--preset--color--signal` |
| Text | `#efe6d2` | theme.json `styles.elements.button.color.text` → theme.json `--wp--preset--color--deep` |
| Font family | `'DM Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` | theme.json `styles.elements.button.typography.fontFamily` → theme.json `--wp--preset--font-family--body` |
| Font size | `1rem` | theme.json `styles.elements.button.typography.fontSize` → theme.json `--wp--preset--font-size--base` |
| Font weight | `600` | theme.json `styles.elements.button.typography.fontWeight` |
| Letter spacing | `0` | theme.json `styles.elements.button.typography.letterSpacing` → theme.json `--wp--custom--letter-spacing--normal` |
| Inline padding | `1.5rem` | theme.json `settings.custom.button.paddingInline` → theme.json `--wp--preset--spacing--60` |
| Block padding | `0.75rem` | theme.json `settings.custom.button.paddingBlock` → theme.json `--wp--preset--spacing--30` |
| Radius | `0.5rem` | theme.json `settings.custom.button.radius` → theme.json `--wp--custom--border--radius-md` |
| Pill radius | `9999px` | theme.json `settings.custom.button.radiusPill` → theme.json `--wp--custom--border--radius-full` |
| Minimum height | `44px` | theme.json `settings.custom.button.minHeight` |
| Mobile minimum height | `48px` | theme.json `settings.custom.button.mobileMinHeight` |
| Icon size | `1.125rem` | theme.json `settings.custom.button.iconSize` |

## Missing or noncanonical

| Concept | Status | Why |
|---|---|---|
| icon_system | missing | The canonical Aurora sources do not define an icon family or usage rules. |
| logo_usage_rules | missing | Logo files, clear-space rules, and lockups belong to the rights-cleared asset manifest. |
| photography_treatment | missing | The canonical Aurora token sources do not define editorial photography rules. |
| brand_gradients | noncanonical_for_press_kit | Gradient presets exist in theme.json but have no current --kk-* semantic role; they are intentionally omitted from press-kit guidance. |
| duotone_treatments | noncanonical_for_press_kit | Duotone presets exist in theme.json but have no current --kk-* semantic role; they are intentionally omitted from press-kit guidance. |
