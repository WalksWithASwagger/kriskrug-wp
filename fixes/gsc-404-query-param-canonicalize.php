<?php
/**
 * GSC 404 cleanup — canonicalize legacy tracking query params.
 *
 * Jetpack sharing turns ?share=twitter URLs into off-site 302s. Google indexed
 * those variants separately and reports them in Search Console Coverage.
 *
 * Deploy via Code Snippets on production (Track A). Keep this repo copy in sync.
 * Run early on template_redirect so it wins over Jetpack sharing handlers.
 *
 * When pasting into Code Snippets: strip the opening <?php tag.
 */

declare(strict_types=1);

/**
 * Query keys that should never be indexed as separate URLs.
 */
function kk_gsc404_tracking_query_keys(): array {
    return array('share', 'nb', 'amp');
}

/**
 * Return true when the request carries legacy tracking params we should strip.
 */
function kk_gsc404_has_tracking_query(): bool {
    if (empty($_GET) || !is_array($_GET)) {
        return false;
    }

    foreach (kk_gsc404_tracking_query_keys() as $key) {
        if (array_key_exists($key, $_GET)) {
            return true;
        }
    }

    return false;
}

/**
 * Build the canonical URL for the current request without tracking params.
 */
function kk_gsc404_canonical_target_url(): string {
    $request_uri = isset($_SERVER['REQUEST_URI'])
        ? sanitize_text_field(wp_unslash((string) $_SERVER['REQUEST_URI']))
        : '/';

    $path = (string) wp_parse_url($request_uri, PHP_URL_PATH);
    if ($path === '') {
        $path = '/';
    }

    $path = '/' . ltrim(untrailingslashit($path), '/');
    if ($path !== '/') {
        $path = trailingslashit($path);
    }

    return home_url($path);
}

/**
 * 301 redirect tracking-param variants to the clean canonical URL.
 */
function kk_gsc404_redirect_tracking_query_params(): void {
    if (is_admin() || wp_doing_ajax() || wp_doing_cron()) {
        return;
    }

    if (defined('REST_REQUEST') && REST_REQUEST) {
        return;
    }

    if (!kk_gsc404_has_tracking_query()) {
        return;
    }

    $method = isset($_SERVER['REQUEST_METHOD'])
        ? strtoupper(sanitize_key(wp_unslash((string) $_SERVER['REQUEST_METHOD'])))
        : 'GET';

    if (!in_array($method, array('GET', 'HEAD'), true)) {
        return;
    }

    wp_safe_redirect(kk_gsc404_canonical_target_url(), 301, 'KK GSC404');
    exit;
}
add_action('template_redirect', 'kk_gsc404_redirect_tracking_query_params', 0);
