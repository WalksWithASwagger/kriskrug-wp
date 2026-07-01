<?php
/**
 * KK Asset Diet — kriskrug.co
 *
 * Cuts unused plugin CSS/JS flagged by Google PageSpeed ("Reduce unused CSS",
 * "Reduce unused JavaScript"). Deployed via the Code Snippets plugin on
 * production as the "KK Asset Diet" snippet (front-end scope). This file is the
 * source of truth — keep it in sync if either side is edited.
 *
 * Verified live 2026-06-28: every page was loading Jetpack Instant Search
 * (jp-search.js, served unminified), Jetpack Carousel + Swiper, Jetpack Sharing
 * (sharedaddy), Popup Maker (one site-wide auto-open popup #3884), and jQuery
 * Migrate. The kk-aurora theme itself is clean — its CSS/JS is concatenated and
 * minified by Jetpack Boost, so the reducible weight is all plugin JavaScript.
 *
 * Reversible by design: deleting this snippet (or Code Snippets safe-mode)
 * restores instant search, carousel, sharing, the popup, and jQuery Migrate.
 *
 * When pasting into Code Snippets: strip the opening <?php tag (Code Snippets
 * wraps the snippet automatically).
 */

/**
 * 1. Disable Jetpack modules KK doesn't use: Instant Search, Carousel, Sharing.
 *    Search reverts to the lightweight core search form.
 */
add_filter('jetpack_active_modules', function (array $modules): array {
    return array_values(array_diff($modules, ['search', 'carousel', 'sharedaddy']));
});

/**
 * 2. Drop jQuery Migrate on the front end. It is a legacy-API shim with no
 *    modern consumer once the plugins above stop loading.
 */
add_action('wp_default_scripts', function ($scripts): void {
    if (is_admin()) {
        return;
    }
    $jquery = $scripts->registered['jquery'] ?? null;
    if ($jquery && !empty($jquery->deps)) {
        $jquery->deps = array_diff($jquery->deps, ['jquery-migrate']);
    }
});

/**
 * 3. Retire the site-wide auto-open Popup Maker popup (#3884) and its assets.
 *    pum_popup_is_loadable => false stops Popup Maker rendering AND enqueuing
 *    any popup. The dequeue is belt-and-suspenders against PM's combined asset
 *    cache, whose real handle is "popup-maker-site" (not "pum-site-*").
 */
add_filter('pum_popup_is_loadable', '__return_false');
add_action('wp_enqueue_scripts', function (): void {
    wp_dequeue_style('popup-maker-site');
    wp_dequeue_script('popup-maker-site');
}, 100);
