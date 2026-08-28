<?php
/**
 * KK users sitemap restriction — kriskrug.co (#767)
 *
 * Removes only the WordPress core users sitemap provider. Post, page, taxonomy,
 * and other sitemap providers remain unchanged. This is the narrow alternative
 * when #767 should ship without adopting the broader #331 archive policy.
 *
 * PREP ONLY. Not deployed as of 2026-08-28. Do not paste into Code Snippets
 * without KK approval, a snippets snapshot, and the post-apply checks below.
 *
 * When pasting into Code Snippets: strip the opening <?php tag. Run this
 * snippet everywhere so the public sitemap registry receives the filter.
 * Enable this file or issue-331-archive-sitemap-policy.php, not both; the full
 * #331 policy already removes the same provider.
 *
 * Rollback: deactivate the snippet, purge the Pagely page cache, and run
 * scripts/check_user_enumeration.sh. The sitemap row should return while the
 * other three #767 checks remain unchanged.
 */

/**
 * Remove the users provider without changing any other sitemap provider.
 *
 * @param mixed  $provider Sitemap provider instance.
 * @param string $name     Sitemap provider name.
 * @return mixed
 */
function kk_767_sitemap_provider($provider, string $name) {
    if ('users' === $name) {
        return false;
    }

    return $provider;
}
add_filter('wp_sitemaps_add_provider', 'kk_767_sitemap_provider', PHP_INT_MAX, 2);
