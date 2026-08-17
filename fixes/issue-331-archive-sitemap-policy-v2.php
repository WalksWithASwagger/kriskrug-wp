<?php
/**
 * KK archive sitemap and indexability policy v2 (#331).
 *
 * Deploy candidate. Supersedes fixes/issue-331-archive-sitemap-policy.php for
 * any future Code Snippets activation. Keep the v1 file as the 2026-07-12
 * receipt artifact; do not activate both. Function names are v2-prefixed so
 * an accidental dual paste does not fatal, but only this file should be on.
 *
 * Why v2 exists (live readback 2026-08-16):
 * - v1 would drop wp-sitemap-users-1.xml, the category child, and the tag
 *   child. That part is correct and would close the sitemap half of #767.
 * - v1 does not noindex date archives. Those URLs are absent from
 *   /wp-sitemap.xml but still return 200 with only max-image-preview:large.
 * - v1 leaves unknown public taxonomies in the sitemap. Live has none today
 *   (only category and post_tag children). v2 drops leftovers so a future
 *   public taxonomy does not reintroduce sitemap bloat.
 *
 * Policy (Option A from docs/current-state/SEO-ARCHIVE-INDEXABILITY-2026-08-02.md):
 * exclude author, tag, and category archives from the core sitemap and emit
 * noindex,follow on those archives plus date archives and any leftover custom
 * taxonomy archives. Posts and pages are untouched. Do not change robots.txt
 * or the /sitemap.xml → /wp-sitemap.xml handoff.
 *
 * REST /wp/v2/users and ?author=N probes are #767 / PR #793, not this file.
 *
 * When pasting into Code Snippets, remove the opening PHP tag.
 * Do not activate without KK approval. See fixes/issue-331-apply.md.
 *
 * Rollback: deactivate this snippet, purge the approved production cache,
 * and repeat the sitemap plus representative archive readback.
 */

/**
 * Exclude author archives from the WordPress core sitemap registry.
 *
 * @param mixed  $provider Sitemap provider instance.
 * @param string $name     Sitemap provider name.
 * @return mixed
 */
function kk_archive_policy_v2_sitemap_provider( $provider, string $name ) {
	if ( 'users' === $name ) {
		return false;
	}

	return $provider;
}
add_filter( 'wp_sitemaps_add_provider', 'kk_archive_policy_v2_sitemap_provider', PHP_INT_MAX, 2 );

/**
 * Exclude every public taxonomy from WordPress core taxonomy sitemaps.
 *
 * Category and post_tag are named so the intent stays greppable. Any other
 * public taxonomy is also dropped: live /wp-sitemap.xml has none today.
 *
 * @param array $taxonomies Public taxonomy objects keyed by taxonomy name.
 * @return array
 */
function kk_archive_policy_v2_sitemap_taxonomies( array $taxonomies ): array {
	unset( $taxonomies['category'], $taxonomies['post_tag'] );

	return array();
}
add_filter( 'wp_sitemaps_taxonomies', 'kk_archive_policy_v2_sitemap_taxonomies', PHP_INT_MAX );

/**
 * Mark public author, tag, category, date, and custom-taxonomy archives
 * noindex while retaining links.
 *
 * is_category(), is_tag(), is_author(), is_date(), and is_tax() are also
 * true on their /page/N/ variants, so pagination inherits this policy.
 *
 * @param array $robots Existing robots directives.
 * @return array
 */
function kk_archive_policy_v2_robots( array $robots ): array {
	if ( ! is_author() && ! is_tag() && ! is_category() && ! is_date() && ! is_tax() ) {
		return $robots;
	}

	unset( $robots['index'], $robots['nofollow'], $robots['none'] );
	$robots['noindex'] = true;
	$robots['follow']  = true;

	return $robots;
}
add_filter( 'wp_robots', 'kk_archive_policy_v2_robots', PHP_INT_MAX );
