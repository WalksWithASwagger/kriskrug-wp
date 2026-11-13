<?php
/**
 * KK archive sitemap and indexability policy.
 *
 * SUPERSEDED and never deployed. The live Code Snippet is 26, sourced from
 * fixes/issue-331-archive-sitemap-policy-v2.php (live since 2026-09-03, see
 * docs/current-state/reports/DEPLOY-767-331-2026-09-03.md). Do not activate
 * this file; it is kept as the 2026-07-12 receipt artifact.
 *
 * When pasting into Code Snippets, remove the opening PHP tag.
 *
 * Rollback: deactivate this snippet, purge the approved production cache, and
 * repeat the sitemap and representative archive readback.
 */

/**
 * Exclude author archives from the WordPress core sitemap registry.
 *
 * @param mixed  $provider Sitemap provider instance.
 * @param string $name     Sitemap provider name.
 * @return mixed
 */
function kk_archive_policy_sitemap_provider($provider, string $name) {
    if ('users' === $name) {
        return false;
    }

    return $provider;
}
add_filter('wp_sitemaps_add_provider', 'kk_archive_policy_sitemap_provider', PHP_INT_MAX, 2);

/**
 * Exclude category and tag archives from WordPress core taxonomy sitemaps.
 *
 * @param array $taxonomies Public taxonomy objects keyed by taxonomy name.
 * @return array
 */
function kk_archive_policy_sitemap_taxonomies(array $taxonomies): array {
    unset($taxonomies['category'], $taxonomies['post_tag']);

    return $taxonomies;
}
add_filter('wp_sitemaps_taxonomies', 'kk_archive_policy_sitemap_taxonomies', PHP_INT_MAX);

/**
 * Mark public author, tag, and category archives noindex while retaining links.
 *
 * @param array $robots Existing robots directives.
 * @return array
 */
function kk_archive_policy_robots(array $robots): array {
    if (!is_author() && !is_tag() && !is_category()) {
        return $robots;
    }

    unset($robots['index'], $robots['nofollow'], $robots['none']);
    $robots['noindex'] = true;
    $robots['follow']  = true;

    return $robots;
}
add_filter('wp_robots', 'kk_archive_policy_robots', PHP_INT_MAX);
