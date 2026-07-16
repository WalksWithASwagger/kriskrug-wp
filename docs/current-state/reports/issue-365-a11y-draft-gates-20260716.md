# #365 Accessibility statement → WP draft — gate status

**Captured:** `2026-07-16T00:43:21Z`  
**Primary:** #288 / #48  
**Packet:** `content/drafts/accessibility-statement-2026-07/`

## Public facts

- `/accessibility/` → **404** (reconfirmed)
- Live theme **1.3.37**; packet README already notes repo ahead at 1.3.40
- Do **not** publish; do **not** add footer/menu links in this issue

## Human gates still open (`[NEEDS KK REVIEW]` in packet)

1. Which WCAG edition to name publicly (working reference vs claim language).
2. Reporting channel: keep `/contact/`, dedicated email, or both (do not invent an address).
3. Response-time / SLA language — none may be invented.
4. Whether to reuse old draft page ID `11886` if it still exists (requires authenticated lookup).

## Agent-safe status

- Local draft copy + README evidence refresh already on `main` (via #359 lineage); 2026-07-16 orchestra pass re-cited five-route pa11y 0 + #4 alt inventory in the packet README.
- No WordPress draft create/update attempted (secrets absent + gates unanswered).

## When unlocked

1. Confirm gates answered in the issue thread.
2. With `WP_USER` / `WP_APP_PASSWORD`: create or update **draft** only; status stays `draft`.
3. Record preview + edit URLs on #365 / packet.
4. Leave publish + footer/menu work on #48.

## Out of scope

Full WCAG audit (#46), alt-text sweep (#4), live publish, theme/footer changes.
