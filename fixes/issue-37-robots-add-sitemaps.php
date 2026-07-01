<?php
/**
 * Historical artifact for Issue #37.
 *
 * Do not deploy this snippet.
 *
 * Before the 2026-07-01 Jetpack-off cleanup, this file appended Jetpack-only
 * image and video sitemap URLs to robots.txt. Jetpack core is now inactive, and
 * those endpoints return 404. The live robots.txt source is Code Snippets entry
 * 7, mirrored in fixes/robots.txt and fixes/robots-txt-ai-policy.php.
 *
 * This file is intentionally no-op so an accidental paste/deploy cannot
 * reintroduce dead sitemap URLs.
 */
