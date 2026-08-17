# Revive → Aurora port contract (2026-07-24)

**Source:** [project-kris-revive](https://github.com/WalksWithASwagger/project-kris-revive)  
**Target:** `theme/kk-aurora` **1.4.0** on Pagely WordPress  
**Non-goals:** TanStack/Lovable hosting, Supabase MCP, React SSR, Lovable CDN hotlinks, fake subscribe UI

## Token map

| Revive | Aurora CSS / theme.json | Role |
|---|---|---|
| `--color-ink` `#efe6d2` | `--revive-surface` / palette `paper` | Warm cream page surface |
| `--color-ink-2` `#e6dcc2` | `--revive-surface-2` / `muted` (remapped) | Panels |
| `--color-paper` `#171310` | `--revive-ink` / `text-primary` | Body text |
| `--color-gold` `#d94a1f` | `--revive-accent` / `signal` | Primary CTA |
| `--color-gold-soft` `#e8b53a` | `--revive-accent-soft` / `wildcard` | Hover / riso yellow |
| `--rainbow-1…7` | `--revive-rainbow-1…7` | Woven marquee + rules |

Readability: keep ~70ch prose measure; page titles clamp; focus rings must remain visible on cream (`ink` + `signal` double ring).

## Fonts

| Role | Family | Load |
|---|---|---|
| Display | Space Grotesk | Google Fonts enqueue (self-host follow-up) |
| Body | DM Sans | Google Fonts enqueue |
| Mono / kickers | JetBrains Mono | Already in theme; keep |

Clash Display is no longer the primary display face.

## Homepage sections (order)

1. Masthead + hero copy (no “Field notes” / “Dispatch” labels)
2. Stage photo (Media Library / CDN)
3. Stages proof strip
4. Archive contact sheet
5. Current work triptych
6. Services offers
7. Writing teasers (`core/query`)
8. Newsletter → Beehiiv

## Locked product rules

- Primary CTA: **Work with me → `/services/`**
- Newsletter language: plain **Newsletter** / **Subscribe free**
- Nav: About, Work, Speaking, Services, Photography, Writing (`/blog/`), Contact

## Implementation files

- Design layer: `theme/kk-aurora/assets/css/revive-port.css`
- Chrome: `parts/header.html`, `parts/footer.html`
- Home: `templates/front-page.html`
- Presets: `theme.json` + `style.css` Version **1.4.0**
