<?php
/**
 * KK homepage /page/{n}/ canonicalize (#997)
 *
 * PREP ONLY. Not deployed as of 2026-09-08. Do not paste into Code Snippets
 * without KK approval and a stated rollback path.
 *
 * Diagnosis: docs/current-state/reports/issue-997-gsc-url-errors-20260908.md
 *
 * The static front page (page 3930, https://kriskrug.co/) accepts
 * /page/{n}/ for n >= 2 and returns HTTP 200 with the same homepage
 * cards and H1, a title suffix " | Page N", and a user-canonical of
 * https://kriskrug.co/{n}/. That numeric path is then slug-guessed by
 * WordPress onto an unrelated post (for example /2/ → post 4002).
 *
 * This snippet collapses the proven same-document alias:
 *   /page/{n}/  →  301  https://kriskrug.co/
 * and forces that canonical if a 200 still renders.
 *
 * It does NOT:
 * - redirect /blog/page/{n}/ (theme already self-canonicalizes)
 * - redirect /{n}/ slug-guesses (/2/, /4/, /5/, …) to the homepage
 * - redirect hard 404s (/3/, /], /*, tag overflow) to the homepage
 * - change snippet 8 (share/amp canonicalize) or Redirection 21–38
 * - change #331 archive noindex / sitemap policy
 *
 * This is same-document alias collapse, not a homepage catch-all.
 *
 * If Aurora later owns this in writing_archive_canonical_url(),
 * deactivate this snippet first. Do not run both.
 *
 * When pasting into Code Snippets: strip the opening <?php tag.
 * Run on the front-end (not admin-only).
 *
 * Rollback: deactivate the snippet. /page/{n}/ returns to the
 * 2026-09-08 200 + /{n}/ canonical. No database restore.
 *
 * @package KK_Fixes
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * True on the static front page when WordPress has stamped a page >= 2.
 */
function kk_997_is_front_paged(): bool {
	if ( is_admin() || wp_doing_ajax() || wp_doing_cron() ) {
		return false;
	}

	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return false;
	}

	if ( ! is_front_page() ) {
		return false;
	}

	$paged = max( (int) get_query_var( 'paged' ), (int) get_query_var( 'page' ) );

	return $paged >= 2;
}

/**
 * 301 /page/{n}/ to the homepage. GET/HEAD only.
 */
function kk_997_redirect_front_paged(): void {
	if ( ! kk_997_is_front_paged() ) {
		return;
	}

	$method = isset( $_SERVER['REQUEST_METHOD'] )
		? strtoupper( sanitize_key( wp_unslash( (string) $_SERVER['REQUEST_METHOD'] ) ) )
		: 'GET';

	if ( ! in_array( $method, array( 'GET', 'HEAD' ), true ) ) {
		return;
	}

	wp_safe_redirect( home_url( '/' ), 301, 'KK 997' );
	exit;
}
add_action( 'template_redirect', 'kk_997_redirect_front_paged', 1 );

/**
 * If a 200 still renders, do not emit the core /{n}/ canonical.
 *
 * @param string       $canonical Current canonical URL.
 * @param WP_Post|null $post      Unused; signature required by the filter.
 * @return string
 */
function kk_997_front_paged_canonical( $canonical, $post = null ) {
	unset( $post );

	if ( kk_997_is_front_paged() ) {
		return home_url( '/' );
	}

	return $canonical;
}
add_filter( 'get_canonical_url', 'kk_997_front_paged_canonical', 20, 2 );
