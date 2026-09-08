<?php
/**
 * KK Events search snippet — kriskrug.co (#995)
 *
 * PREP ONLY. Not deployed as of 2026-09-08. Do not paste into Code Snippets
 * without KK approval, a page-2250 snapshot, and a stated rollback path.
 *
 * Diagnosis: docs/current-state/reports/issue-995-events-search-intent-20260908.md
 *
 * Page 2250 (`/events/`) currently renders the theme fallback title
 * `Events | Kris Krüg` and a 200-character content-trim description.
 * Aurora already reads `jetpack_seo_html_title` and
 * `advanced_seo_description` via get_post_meta(). Those keys are not
 * REST-registered for the `page` type (`inc/seo-meta-rest.php` is
 * post-only), so a REST PATCH of page 2250 meta would silently drop.
 *
 * This snippet supplies the two approved strings for page 2250 only,
 * through `get_post_metadata`, so the theme emits one title and one
 * standard description. It does not print a second meta tag. It does
 * not change page content, artboards, dates, or registration hrefs.
 * It does not change `og:title` (theme uses get_the_title()).
 *
 * Do not activate snippet 12 (OG restore) with this file. Do not
 * hard-code upcoming event dates here.
 *
 * When pasting into Code Snippets: strip the opening <?php tag. Run
 * everywhere, not admin-only — search crawlers hit the front-end.
 *
 * Rollback: deactivate the snippet. Public title/description return to
 * the 2026-09-08 fallback. No database restore is required unless a
 * later session also wrote post meta.
 *
 * @package KK_Fixes
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Approved Events search title. Includes the site tail because
 * `pre_get_document_title` replaces the whole document title.
 */
const KK_995_EVENTS_TITLE = 'Vancouver AI Events I Host | Kris Krüg';

/**
 * Approved Events search description. Evergreen rooms already named
 * on the live page. No dates, no availability claim.
 */
const KK_995_EVENTS_DESCRIPTION = 'Monthly Vancouver AI meetups, film-club screenings, Friday office hours, and keynote stages I host or speak at. Registration links live on this page.';

/**
 * WordPress page ID for /events/. Abort-in-spirit: the filter no-ops
 * on any other object id.
 */
const KK_995_EVENTS_PAGE_ID = 2250;

/**
 * Supply approved SEO title/description for page 2250 only.
 *
 * @param mixed  $value     Current filter value. Null means "use storage".
 * @param int    $object_id Post ID.
 * @param string $meta_key  Meta key being read.
 * @param bool   $single    Whether a single value was requested.
 * @return mixed
 */
function kk_995_events_search_meta( $value, $object_id, $meta_key, $single ) {
	if ( (int) $object_id !== KK_995_EVENTS_PAGE_ID ) {
		return $value;
	}

	$map = array(
		'jetpack_seo_html_title'    => KK_995_EVENTS_TITLE,
		'advanced_seo_description'  => KK_995_EVENTS_DESCRIPTION,
	);

	if ( ! isset( $map[ $meta_key ] ) ) {
		return $value;
	}

	$approved = $map[ $meta_key ];

	return $single ? $approved : array( $approved );
}
add_filter( 'get_post_metadata', 'kk_995_events_search_meta', 10, 4 );
