<?php
/**
 * KK crawl hygiene — Track A (#1025)
 *
 * PREP ONLY. Soft-ship. Do not paste into Code Snippets without SEO LGTM,
 * KK approval, a snippets snapshot, and a stated rollback path.
 *
 * Live public readback 2026-09-18 (no GSC counts invented here):
 * - `/home/` already 301s to `/` via the Redirection plugin
 *   (`x-redirect-by: redirection`), single hop. Page slug `home` (ID 2315)
 *   is still listed in `wp-sitemap-posts-page-1.xml`.
 * - `?share=`, `nb=`, and `amp=` already 301 to the clean URL via snippet 8
 *   (`fixes/gsc-404-query-param-canonicalize.php`, `x-redirect-by: KK GSC404`).
 *   Homepage and a sample post mint zero `?share=` / `nb=` hrefs today.
 * - Tag and author feeds still return HTTP 200 RSS and are advertised with
 *   `rel="alternate"`. Category feeds and comments feeds are left alone.
 * - `/author/kk/page/2/` still returns HTTP 200. #331 v2 already marks
 *   author / tag / category archives `noindex, follow` and dropped them
 *   from the sitemap. Do not broaden that policy.
 * - `https://kriskrug.co/feed/` remains HTTP 200 RSS. Preserve it.
 * - `robots.txt` stays the physical file. Do not edit it here.
 *
 * This snippet:
 * 1. 301 exact `/home` and `/home/` to `/` (GET/HEAD). Repo-tracked fallback
 *    for the live Redirection rule. Does not touch `/home/{slug}/`.
 * 2. Rewrite `get_permalink()` for the `/home/` page to `/` so menus and
 *    other internals stop minting the alias.
 * 3. Exclude that page from the core page sitemap.
 * 4. 301 tag feeds and author feeds to their parent HTML archives.
 * 5. Stop advertising those feeds (`feed_links_extra_show_{tag,author}_feed`).
 * 6. 301 author archives at `paged >= 2` to the first author page.
 * 7. Strip `share` / `nb` / `amp` from generated permalinks. Snippet 8
 *    still owns the inbound 301.
 *
 * It does NOT:
 * - noindex tag or category archives (already #331 v2, snippet 26)
 * - change `robots.txt`
 * - redirect or disable `https://kriskrug.co/feed/`
 * - redirect comments feeds or category feeds
 * - replace snippet 8
 * - unpublish page 2315
 * - Request Indexing or delete thin posts
 *
 * When pasting into Code Snippets: strip the opening <?php tag.
 * Run on the front-end (not admin-only).
 *
 * Rollback: deactivate the snippet and purge Pagely / Boost cache.
 * `/home/` keeps the existing Redirection 301. Feeds and author pagination
 * return to 200. `/home/` reappears in the page sitemap after cache purge.
 *
 * @package KK_Fixes
 */

/**
 * Query keys snippet 8 already 301s. Reused here only to stop minting.
 *
 * @return array<int, string>
 */
function kk_1025_tracking_query_keys(): array {
	return array( 'share', 'nb', 'amp' );
}

/**
 * Normalize a request path for exact-alias compares.
 *
 * @param string $path Raw path, with or without a trailing slash.
 * @return string Trailing-slashed path, or `/`.
 */
function kk_1025_normalize_path( string $path ): string {
	$path = trim( $path );
	if ( '' === $path || '/' === $path ) {
		return '/';
	}

	return '/' . strtolower( trim( $path, '/' ) ) . '/';
}

/**
 * True only for `/home` and `/home/`, never `/home/{slug}/`.
 *
 * @param string $path Request path.
 * @return bool
 */
function kk_1025_is_home_alias_path( string $path ): bool {
	return '/home/' === kk_1025_normalize_path( $path );
}

/**
 * Strip share / tracking params from a generated URL.
 *
 * @param string $url Absolute or relative URL.
 * @return string
 */
function kk_1025_strip_tracking_query_args( string $url ): string {
	if ( ! function_exists( 'remove_query_arg' ) ) {
		return $url;
	}

	return (string) remove_query_arg( kk_1025_tracking_query_keys(), $url );
}

/**
 * Front-end GET/HEAD only. Skip admin, cron, Ajax, REST.
 *
 * @return bool
 */
function kk_1025_is_public_safe_request(): bool {
	if ( is_admin() || wp_doing_ajax() || wp_doing_cron() ) {
		return false;
	}

	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return false;
	}

	$method = isset( $_SERVER['REQUEST_METHOD'] )
		? strtoupper( sanitize_key( wp_unslash( (string) $_SERVER['REQUEST_METHOD'] ) ) )
		: 'GET';

	return in_array( $method, array( 'GET', 'HEAD' ), true );
}

/**
 * Current request path, defaulting to `/`.
 *
 * @return string
 */
function kk_1025_request_path(): string {
	$request_uri = isset( $_SERVER['REQUEST_URI'] )
		? sanitize_text_field( wp_unslash( (string) $_SERVER['REQUEST_URI'] ) )
		: '/';

	$path = (string) wp_parse_url( $request_uri, PHP_URL_PATH );
	if ( '' === $path ) {
		return '/';
	}

	return $path;
}

/**
 * Published page that owns the `/home/` alias, if it still exists.
 *
 * @return WP_Post|null
 */
function kk_1025_home_alias_page() {
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
 * True when this request is the exact `/home/` alias.
 *
 * @return bool
 */
function kk_1025_should_redirect_home_alias(): bool {
	return kk_1025_is_public_safe_request() && kk_1025_is_home_alias_path( kk_1025_request_path() );
}

/**
 * True on a tag or author feed, never the site RSS or comments feed.
 *
 * @return bool
 */
function kk_1025_should_redirect_archive_feed(): bool {
	if ( ! kk_1025_is_public_safe_request() ) {
		return false;
	}

	if ( ! is_feed() || is_comment_feed() ) {
		return false;
	}

	return is_tag() || is_author();
}

/**
 * True on author HTML pagination at page 2 or later.
 *
 * @return bool
 */
function kk_1025_should_redirect_author_paged(): bool {
	if ( ! kk_1025_is_public_safe_request() ) {
		return false;
	}

	if ( ! is_author() || is_feed() ) {
		return false;
	}

	$paged = max( (int) get_query_var( 'paged' ), (int) get_query_var( 'page' ) );

	return $paged >= 2;
}

/**
 * Parent HTML archive for a tag or author feed. Empty if unresolved.
 *
 * @return string
 */
function kk_1025_archive_feed_target_url(): string {
	if ( is_tag() ) {
		$term = get_queried_object();
		if ( ! $term instanceof WP_Term ) {
			return '';
		}

		$link = get_term_link( $term );
		return is_wp_error( $link ) ? '' : (string) $link;
	}

	if ( is_author() ) {
		$author_id = (int) get_queried_object_id();
		if ( $author_id <= 0 ) {
			return '';
		}

		return (string) get_author_posts_url( $author_id );
	}

	return '';
}

/**
 * First page of the current author archive.
 *
 * @return string
 */
function kk_1025_author_first_page_url(): string {
	$author_id = (int) get_queried_object_id();
	if ( $author_id <= 0 ) {
		return '';
	}

	return (string) get_author_posts_url( $author_id );
}

/**
 * 301 `/home/` to `/`. Priority -1 so `/home/?share=twitter` is one hop,
 * not snippet 8 to `/home/` then Redirection to `/`.
 *
 * @return void
 */
function kk_1025_redirect_home_alias(): void {
	if ( ! kk_1025_should_redirect_home_alias() ) {
		return;
	}

	wp_safe_redirect( home_url( '/' ), 301, 'KK 1025' );
	exit;
}
add_action( 'template_redirect', 'kk_1025_redirect_home_alias', -1 );

/**
 * 301 tag/author feeds to the parent HTML archive. Main `/feed/` is not
 * `is_tag()` or `is_author()`, so it stays.
 *
 * @return void
 */
function kk_1025_redirect_archive_feed(): void {
	if ( ! kk_1025_should_redirect_archive_feed() ) {
		return;
	}

	$target = kk_1025_archive_feed_target_url();
	if ( '' === $target ) {
		return;
	}

	wp_safe_redirect( $target, 301, 'KK 1025' );
	exit;
}
add_action( 'template_redirect', 'kk_1025_redirect_archive_feed', 1 );

/**
 * 301 author `/page/{n}/` (n >= 2) to the first author page.
 *
 * @return void
 */
function kk_1025_redirect_author_paged(): void {
	if ( ! kk_1025_should_redirect_author_paged() ) {
		return;
	}

	$target = kk_1025_author_first_page_url();
	if ( '' === $target ) {
		return;
	}

	wp_safe_redirect( $target, 301, 'KK 1025' );
	exit;
}
add_action( 'template_redirect', 'kk_1025_redirect_author_paged', 1 );

/**
 * Point permalinks for the leftover Home page at `/`.
 *
 * @param string $link    Candidate permalink.
 * @param int    $post_id Page ID.
 * @return string
 */
function kk_1025_rewrite_home_page_link( $link, $post_id ) {
	$page = kk_1025_home_alias_page();
	if ( ! $page instanceof WP_Post ) {
		return $link;
	}

	if ( (int) $post_id !== (int) $page->ID ) {
		return $link;
	}

	return home_url( '/' );
}
add_filter( 'page_link', 'kk_1025_rewrite_home_page_link', 10, 2 );

/**
 * Drop the leftover Home page from the core page sitemap.
 *
 * @param array  $args      Sitemap query args.
 * @param string $post_type Post type for this sitemap provider.
 * @return array
 */
function kk_1025_exclude_home_from_page_sitemap( $args, $post_type ) {
	if ( 'page' !== $post_type ) {
		return $args;
	}

	$page = kk_1025_home_alias_page();
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
add_filter( 'wp_sitemaps_posts_query_args', 'kk_1025_exclude_home_from_page_sitemap', 10, 2 );

add_filter( 'feed_links_extra_show_tag_feed', '__return_false' );
add_filter( 'feed_links_extra_show_author_feed', '__return_false' );

add_filter( 'the_permalink', 'kk_1025_strip_tracking_query_args' );
add_filter( 'post_link', 'kk_1025_strip_tracking_query_args' );
add_filter( 'page_link', 'kk_1025_strip_tracking_query_args' );
add_filter( 'term_link', 'kk_1025_strip_tracking_query_args' );
add_filter( 'author_link', 'kk_1025_strip_tracking_query_args' );
