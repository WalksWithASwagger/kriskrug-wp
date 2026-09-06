# Favicon #985 — verified gap and native settings release packet

Verified 2026-09-06. Preparation only; no live setting, theme, or media changes.

## Current evidence

Fresh Chromium context, followed by warm revisits of `/`, `/speaking/`, and `/contact/`, found no `link[rel*="icon"]` declarations on any route. Each page emitted exactly one theme-color, `#efe6d2`. Public REST root returned `site_icon: 0` and `site_icon_url: ""`. A GET/redirect check of `/favicon.ico` ended at `/wp-includes/images/w-logo-blue-white-bg.png`, HTTP 200, `image/png`; the initial response is HTTP 302 from WordPress. This confirms the audit's default-W defect, not merely an old browser cache.

`make doctor` and `make status-readonly` completed; live public stylesheet and repository both report Aurora 1.6.11. The August press-kit brand-reference provenance still says 1.6.9; its cream surface agrees with current `theme_color_meta()` in `theme/kk-aurora/functions.php`.

## Ownership and asset gate

WordPress Site Icon owns the standard icon family and favicon fallback. Use its native setting; do not add a second theme emitter. The prior [#161 packet](../../fixes/issue-161-favicon.md) describes the same unresolved asset gap, while closed #221 was inventory/coordinating work, not evidence of icon installation.

The approved [asset manifest](../../content/source-packs/content-architecture-2026/press-kit/assets/manifest.json) offers a 468x229 raster rainbow wordmark. It does not supply an approved square KK mark or master SVG. The [header closeout](archive/AURORA-HEADER-LOGO-CLOSEOUT-2026-06-03.md) explicitly says not to set Site Icon from the wide wordmark. A wordmark adaptation is therefore a new owner decision, not an already approved square asset. The current swarm asked KK whether to adapt that wordmark or receive a square mark; selection is pending.

Required source: square PNG at least 512x512 (1024 preferred), with legible mark and safe padding; also obtain the corresponding genuine SVG master to fulfill #985's SVG deliverable. Do not wrap a PNG in SVG and call it a vector master, or invent replacement lettering. After selection, review exports at actual 16/32px sizes on light/dark backgrounds and 180px touch size before any upload. No exports or asset visual approval are claimed by this packet.

## Theme-color discrepancy

The audit requests `#030405`, but current Aurora deliberately uses cream `#efe6d2` with `color-scheme: light`. The source comment requires browser chrome to match cream/ink surfaces, not legacy dark Aurora. Retain the existing color for this favicon fix unless KK explicitly chooses a brand-color change. This is an unresolved audit-spec discrepancy, not a missing meta tag.

## Exact release sequence after asset selection

1. Record authenticated current `site_icon` option and attachment metadata privately; cross-check public REST state. Current public value is zero, but re-read at execution rather than assuming it remains zero.
2. Inspect the selected source's format, dimensions, provenance and rendered 16/32/180px previews. Keep the approved source and checksums in the lane. WordPress should generate the 32/192/180/270px PNG variants from the square source. WordPress does not generate a true ICO file; `/favicon.ico` redirects to an icon image.
3. Preview a native Site Icon change in the current authenticated WordPress UI or approved settings API. Confirm uploaded attachment ID and exact source identity before saving. Do not change unrelated settings or bulk-update a settings response.
4. With the concrete asset/settings change approved, upload that one source and set `site_icon` to its verified attachment ID. Capture response and old value privately for rollback. Do not remove the prior attachment.
5. Purge the affected public pages and favicon redirect at Pagely through the supported owner channel. Browser icon caches may outlive page-cache purges; verify in a new profile.
6. Read back all three routes, public REST identity and `/favicon.ico`; validate every declared asset's HTTP status, MIME type and dimensions. Confirm one canonical set, no W target, and exactly one unchanged theme-color.
7. Review fresh and warm browser tabs on desktop and a real iOS home-screen addition (or explicitly mark the device check pending). The declared apple-touch-icon URL must return 200; a physical `/apple-touch-icon.png` root file is not required when the link points elsewhere.

The SVG master is a separate required deliverable. Native WordPress Site Icon supplies raster declarations, not an SVG declaration. Once an approved master exists, specify and review the minimal single SVG declaration alongside native raster fallbacks; it must not disable native Site Icon or introduce an independent fallback source. That theme change requires its own tested diff and release approval. Do not deploy broad SVG-upload support for one icon.

## Rollback

Restore the exact saved Site Icon ID (zero only if the pre-change read proves zero), purge affected caches, and recheck all routes plus the favicon redirect. Retain new media until rollback verification is complete; avoid destructive cleanup. If a later SVG declaration is added, revert that exact scoped code change separately. No theme deployment is necessary for the native raster stage.

## Verification and remaining work

Executed: startup checks; public homepage markup and stylesheet GET; REST identity GET; fresh/warm Chromium DOM readbacks on three routes; favicon redirect/status/type check. Browser: Playwright Chromium, headless, default desktop viewport; not a claim of visible browser-tab or iOS device verification.

Reproduce public checks:

```sh
make doctor
make status-readonly
curl -fsSL https://kriskrug.co/wp-json/
curl -sS -L -D - -o /dev/null https://kriskrug.co/favicon.ico
curl -fsSL https://kriskrug.co/
curl -fsSL https://kriskrug.co/speaking/
curl -fsSL https://kriskrug.co/contact/
git diff --check
```

Browser check: create a new Chromium context; navigate to each route, collect `link[rel*="icon"]` and `meta[name="theme-color"]`, revisit each route in the same context, then GET `/favicon.ico` with redirects enabled. Both visits currently have zero icon links and cream theme-color.

Issue #985 remains open: square/vector asset selection, exports and actual-size visual inspection, explicit resolution of the dark-color request, native settings apply, optional SVG code path, and post-release visual/readback checks are not complete. This packet does not claim a shipped favicon fix.
