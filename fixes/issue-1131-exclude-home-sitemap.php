<?php
/**
 * KK page-sitemap drop for leftover `/home/` — Track A (#1131)
 *
 * PREP ONLY. Do not paste into Code Snippets without KK approval, a snippets
 * snapshot, and a stated rollback path. Live deploy is the #1114 gate.
 *
 * Live public readback 2026-10-17:
 * - Page slug `home` (ID 2315) is still published.
 * - `https://kriskrug.co/home/` 301s to `/` (`x-redirect-by: redirection`).
 * - `wp-sitemap-posts-page-1.xml` still lists `/home/`.
 *
 * This snippet only excludes that published page from the core page sitemap.
 * It does NOT:
 * - unpublish page 2315
 * - add a second `/home/` redirect (Redirection already owns the 301)
 * - change Person / sameAs JSON-LD (#1089 / #1104)
 * - activate the broader #1025 crawl-hygiene package
 * - change `robots.txt` or #331 archive policy
 *
 * #1025 already contains the same sitemap filter plus feed and pagination
 * redirects. Prefer this file for #1131. Do not activate both unless KK
 * later approves the rest of #1025; duplicate `post__not_in` IDs are
 * harmless, colliding function names are not (these names are 1131-prefixed).
 *
 * When pasting into Code Snippets: strip the opening <?php tag.
 * Run on the front-end (not admin-only).
 *
 * Rollback: deactivate the snippet and purge Pagely / Boost cache.
 * `/home/` reappears in the page sitemap after cache purge. The existing
 * Redirection 301 is unchanged.
 *
 * @package KK_Fixes
 */

/**
 * Published page that owns the `/home/` alias, if it still exists.
 *
 * Historical ID is 2315. Lookup is by slug so a restored export with a
 * different ID still matches.
 *
 * @return WP_Post|null
 */
function kk_1131_home_alias_page() {
	if ( ! function_exists( 'get_page_by_path' ) ) {
		return null;
	}

	$page = get_page_by_path( 'home' );
	if ( ! $page instanceof WP_Post || 'publish' !== $page->post_status ) {
		return null;
	}

	return $page;
}

/**
 * Drop the leftover Home page from the core page sitemap.
 *
 * @param array  $args      Sitemap query args.
 * @param string $post_type Post type for this sitemap provider.
 * @return array
 */
function kk_1131_exclude_home_from_page_sitemap( $args, $post_type ) {
	if ( 'page' !== $post_type ) {
		return $args;
	}

	$page = kk_1131_home_alias_page();
	if ( ! $page instanceof WP_Post ) {
		return $args;
	}

	$excluded = isset( $args['post__not_in'] ) && is_array( $args['post__not_in'] )
		? $args['post__not_in']
		: array();
	$excluded[] = (int) $page->ID;
	$args['post__not_in'] = array_values( array_unique( array_map( 'absint', $excluded ) ) );

	return $args;
}
add_filter( 'wp_sitemaps_posts_query_args', 'kk_1131_exclude_home_from_page_sitemap', 10, 2 );
