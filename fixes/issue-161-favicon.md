# Issue #161 Favicon / App Icons - Deployment Note

**Scope:** Track A evidence and a deploy-ready plan only. No live WordPress writes were made. The final install is gated on a KK-supplied square brand asset plus one Site Icon setting change.

## What #161 actually still needs

The other "missing social/SEO metadata" signals from #161 are already covered by shipped packets, so this issue narrows to the icon family only:

- `twitter:card`, `twitter:image`, `og:image` (+ width/height/alt) and a fallback card image (media ID `7548`): handled by `fixes/issue-43-twitter-cards.php`.
- `canonical`, meta descriptions: handled via `fixes/issue-36-meta-descriptions.md` and the Jetpack/SEO stack.
- Root files (`llms.txt`, `robots.txt`): verified live under #221.

The remaining gap is the **favicon / app-icon set**, which is the one explicit checkbox in #161 and the item `docs/current-state/SEO-OVERHAUL-2026-06-14.md` flags as "needs a square brand asset, gated on KK assets/approvals."

## Public Evidence - 2026-06-15

Read-only checks against `https://kriskrug.co/`:

| Check | Result |
|---|---|
| Homepage `<head>` icon tags | **None.** Only `<meta name="theme-color" content="#0D0D12">` is emitted. No `<link rel="icon">`, no `apple-touch-icon`, no `manifest`, no `msapplication-TileImage`. |
| `/favicon.ico` | `200`, but redirects to the **default WordPress mark** `https://kriskrug.co/wp-includes/images/w-logo-blue-white-bg.png` (`image/png`, 4119b). Browser tabs show the generic WP "W", not a Kris Krüg mark. |
| `/apple-touch-icon.png` | **404.** No iOS home-screen / bookmark icon. |
| WP REST site identity | `site_icon: 0` (per `docs/current-state/SITE_INVENTORY.md` and `AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md`). |

Verification command used:

```bash
curl -Ls "https://kriskrug.co/" \
  | perl -0777 -ne 'while (/<link\b[^>]*\brel="(?:icon|shortcut icon|apple-touch-icon|manifest|mask-icon)"[^>]*>/gi) { print "$&\n" }
                    while (/<meta\b[^>]*\bname="(?:msapplication[^"]*|theme-color)"[^>]*>/gi) { print "$&\n" }'
curl -Ls -o /dev/null -w "%{http_code} %{url_effective}\n" "https://kriskrug.co/favicon.ico"
curl -Ls -o /dev/null -w "%{http_code}\n" "https://kriskrug.co/apple-touch-icon.png"
```

## Asset KK needs to provide

A **square brand icon**, not the wide wordmark. `AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md` is explicit: "Do not set `site_icon` from this wide wordmark." Spec:

- **Shape:** square (1:1).
- **Size:** at least `512x512`px; `1024x1024` preferred so WordPress can downscale cleanly.
- **Format:** PNG (transparent or solid). WordPress generates the `.ico`, 32, 180, 192, and 270px variants from this one source.
- **Safe area:** keep the mark centered with padding; it will be cropped to a circle/rounded square by some platforms and shown as small as 16px in a tab.
- **Content:** a recognizable KK monogram or brand mark that reads at 16px, on a background that works in both light and dark browser chrome.

## Recommended deployment (WordPress-native, no custom code)

Setting the WordPress **Site Icon** is the preferred path because it is plugin-agnostic, survives theme changes, and auto-emits the full tag set (`<link rel="icon" sizes="32x32">`, `sizes="192x192">`, `<link rel="apple-touch-icon" sizes="180x180">`, and `<meta name="msapplication-TileImage">`):

1. Confirm a backup / rollback point before any production change.
2. Upload the square asset and set it as the Site Icon. Either:
   - **UI:** Appearance to Editor or Customize to Site Identity to Site Icon (FSE: Site Editor to Styles, or `/wp-admin/customize.php?autofocus[section]=title_tagline`), or
   - **WP-CLI:** `wp option update site_icon <ATTACHMENT_ID>` (where the attachment is the uploaded square PNG).
3. Purge Pagely / Jetpack caches.
4. Verify (below).

No custom PHP is needed for the standard case. A manual `wp_head` emitter is intentionally **not** recommended here: it would duplicate what WordPress already emits once `site_icon` is set, and is harder to roll back. Only fall back to a snippet if the Site Icon option cannot be used for some reason; if so, mirror the `fixes/issue-43-*` pattern (single emitter, no duplicate tags) and document it.

## Post-deploy verification

```bash
# Icon tags now present in <head>
curl -Ls "https://kriskrug.co/" \
  | perl -0777 -ne 'while (/<link\b[^>]*\brel="(?:icon|apple-touch-icon)"[^>]*>/gi) { print "$&\n" }'

# Apple touch icon now resolves (expect 200, image/png)
curl -Ls -o /dev/null -w "%{http_code} %{content_type}\n" "https://kriskrug.co/apple-touch-icon.png"

# REST site identity now non-zero
curl -Ls "https://kriskrug.co/wp-json/" | python3 -c 'import sys,json; d=json.load(sys.stdin); print("site_icon_url:", d.get("site_icon_url",""))'
```

Manual checks: open the site in a fresh browser tab and confirm the KK mark replaces the WordPress "W"; add to an iOS home screen and confirm the app icon.

## Rollback

- **UI:** Customize to Site Identity to Site Icon to remove image.
- **WP-CLI:** `wp option update site_icon 0`.
- Purge caches. The site reverts to the default WordPress favicon behavior (no brand regression beyond the pre-existing state).

## Close criteria remaining

- KK supplies the square brand asset to the spec above.
- Site Icon is set on production (one setting change) and caches purged.
- Live `<head>` emits `rel="icon"` and `apple-touch-icon`; `/apple-touch-icon.png` returns `200`; REST `site_icon_url` is non-empty.
- Browser-tab and iOS home-screen icons visually confirmed.

Until the asset and the live setting change land, #161 stays an inventoried, deploy-ready gap. This packet does not itself close #161.
