<?php
/**
 * KK archive sitemap and indexability policy.
 *
 * Canonical source for the production Code Snippets entry. When pasting into
 * Code Snippets, remove the opening PHP tag. Production deployment remains a
 * separate human-approved step documented in the issue #331 receipt.
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
