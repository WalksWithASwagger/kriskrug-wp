<?php
/**
 * KK author-query probe hardening — kriskrug.co (#767)
 *
 * Closes the classic /?author=N 301-to-/author/<slug>/ enumeration probe.
 * Pretty /author/<slug>/ archives are left alone on purpose: issue #331
 * already decided those URLs stay publicly reachable and only lose sitemap
 * membership plus gain noindex,follow. This snippet must not silently
 * convert that into a 404.
 *
 * PREP ONLY. Not deployed as of 2026-08-16. Do not paste into Code Snippets
 * without KK approval and a snippets snapshot.
 *
 * When pasting into Code Snippets: strip the opening <?php tag. Front-end
 * scope is enough (template_redirect). Running everywhere is also safe.
 *
 * Optional stricter mode (NOT the default; KK decision, not an implied
 * #331 change): define KK_767_DISABLE_AUTHOR_ARCHIVES as true in this
 * snippet to 404 every is_author() request, including pretty permalinks.
 *
 * Rollback: deactivate the snippet, purge the Pagely page cache (author
 * redirects can be cached), and re-run scripts/check_user_enumeration.sh.
 */

/**
 * True when the request is the query-string author probe (/?author=N).
 *
 * Pretty /author/<slug>/ permalinks populate the author query var via
 * rewrite rules and do not set $_GET['author'].
 *
 * @return bool
 */
function kk_767_is_author_query_probe(): bool {
    if (is_admin()) {
        return false;
    }

    // phpcs:ignore WordPress.Security.NonceVerification.Recommended -- public GET key presence only; the value is never trusted or echoed.
    return isset($_GET['author']);
}

/**
 * Stop redirect_canonical from turning /?author=N into /author/<slug>/.
 *
 * @param string|false $redirect_url  Candidate redirect, or false to skip.
 * @param string       $requested_url Original request URL.
 * @return string|false
 */
function kk_767_stop_author_query_canonical($redirect_url, $requested_url) {
    unset($requested_url);

    if (kk_767_is_author_query_probe()) {
        return false;
    }

    return $redirect_url;
}
add_filter('redirect_canonical', 'kk_767_stop_author_query_canonical', 10, 2);

/**
 * 404 the query-string probe (and, only if explicitly enabled, all author archives).
 *
 * Hooked at priority 0 so it wins the race with redirect_canonical (priority 10).
 * The canonical filter above is still required: core will try to "fix" a 404
 * by redirecting ?author=N to the pretty author permalink.
 *
 * @return void
 */
function kk_767_404_author_enumeration_probe(): void {
    $block_pretty_archives = defined('KK_767_DISABLE_AUTHOR_ARCHIVES') && KK_767_DISABLE_AUTHOR_ARCHIVES;
    $is_probe              = kk_767_is_author_query_probe();
    $is_pretty_author      = function_exists('is_author') && is_author();

    if (!$is_probe && !($block_pretty_archives && $is_pretty_author)) {
        return;
    }

    global $wp_query;
    if ($wp_query instanceof WP_Query) {
        $wp_query->set_404();
    }

    status_header(404);
    nocache_headers();
}
add_action('template_redirect', 'kk_767_404_author_enumeration_probe', 0);
