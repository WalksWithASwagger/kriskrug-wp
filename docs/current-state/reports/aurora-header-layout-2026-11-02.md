# Responsive header repair: November 2, 2026

The inline critical-CSS guard reset `grid-template-areas` while the brand and
actions retained named areas from the responsive stylesheet. At 393 pixels,
the logo appeared on the lower right and the action appeared above the nav.
The repair keeps named areas paired at each breakpoint. Mobile navigation
also retains 44-pixel targets within the existing `components` cascade layer,
where the older important declarations were otherwise taking precedence.

Kris explicitly authorized repair and publication in the November 2 session.
Only the critical header CSS and its explanatory comment were deployed by
trusted, host-key-verified SFTP. The live site's other header markup and URLs
were preserved. This did not deploy the complete 1.6.13 theme over live 1.6.12.

## Verification

- Six final-URL Python tests and the PHP final-URL smoke passed.
- Signed-out public layout inspected at 375, 393, 768, 900 and 1440 pixels.
- Named brand/actions row and navigation row through 1200 pixels; one row
  on desktop. No page-width overflow at the measured widths.
- Every mobile navigation anchor measured 44 pixels high.
- The published essay, May archive, blog, feed and sitemap returned HTTP 200
  after PressCACHE and generated Boost HTML cache refresh.
- Scoped browser screenshots and computed-layout measurements were recorded
  locally. The full repository raster pixel gate was not run; this is a
  targeted responsive verification, not a full-site pixel-diff claim.

## Recovery

Final live header SHA-256:
`0ed13da6fc104c76963c1f0a69ad615a340a875ae17bf919d8f4580c38e37de1`.

Original header SHA-256:
`4a008b0e6a8812bf6b33925c64328c66079e3cfb0ba9935a84389a4ba4763b44`.

Original remote rollback copy:
`wp-content/themes/kk-aurora/parts/header.html.before-ubc-20261103T062403Z`.
An intermediate copy is also retained as
`header.html.before-ubc-20261103T063203Z` in the same directory.

The generated host HTML cache was moved, without deletion, to
`wp-content/boost-cache/header-purge-backup-20261103T063359Z` and its normal
empty host directory recreated. Static assets, cache configuration and plugin
code were untouched. The Boost REST clear action returned 403; no plugin
onboarding, settings or service agreement was changed.

State: live repair shipped; branch is retained for review and canonical merge.
Owner: Kris Krüg. Next check: November 3, 2026 for PR review. No automatic check
is scheduled.
