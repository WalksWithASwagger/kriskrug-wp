<?php
/**
 * Lightweight smoke tests for pure KK Sidebar Promos behavior.
 *
 * These tests intentionally stub the small WordPress surface they need so they
 * can run in this repo without a full WordPress install.
 */

define( 'ABSPATH', __DIR__ . '/wp-stub/' );
define( 'DAY_IN_SECONDS', 86400 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'KK_SP_POST_TYPE', 'kk_sidebar_promo' );
define( 'KK_SP_META_TYPE', '_kk_sp_type' );
define( 'KK_SP_META_TONE', '_kk_sp_tone' );
define( 'KK_SP_META_LINK', '_kk_sp_link' );
define( 'KK_SP_META_CTA', '_kk_sp_cta' );
define( 'KK_SP_META_END', '_kk_sp_end' );
define( 'KK_SP_META_SOURCE', '_kk_sp_source' );
define( 'KK_SP_META_SOURCE_ID', '_kk_sp_source_id' );

class WP_Widget {}

$GLOBALS['kk_sp_test_meta']  = [];
$GLOBALS['kk_sp_test_posts'] = [];
$GLOBALS['kk_sp_updated_posts'] = [];
$GLOBALS['kk_sp_inserted_comments'] = [];

function add_shortcode() {}
function add_action() {}
function register_widget() {}
function register_block_type() {}

function current_time( $type ) {
	if ( $type === 'Y-m-d' ) {
		return gmdate( 'Y-m-d', strtotime( '2026-05-20 12:00:00 UTC' ) );
	}
	if ( $type === 'timestamp' ) {
		return strtotime( '2026-05-20 12:00:00 UTC' );
	}
	return '';
}

function get_posts() {
	return $GLOBALS['kk_sp_test_posts'];
}

function wp_list_pluck( $list, $field ) {
	return array_map(
		static function ( $item ) use ( $field ) {
			return is_object( $item ) ? $item->{$field} : $item[ $field ];
		},
		$list
	);
}

function wp_parse_args( $args, $defaults ) {
	return array_merge( $defaults, $args );
}

function wp_next_scheduled() {
	return false;
}

function wp_schedule_event() {}
function wp_unschedule_event() {}

function wp_update_post( $post_data ) {
	$GLOBALS['kk_sp_updated_posts'][] = $post_data;

	return $post_data['ID'] ?? 0;
}

function wp_insert_comment( $comment_data ) {
	$GLOBALS['kk_sp_inserted_comments'][] = $comment_data;

	return count( $GLOBALS['kk_sp_inserted_comments'] );
}

function get_post_meta( $post_id, $key, $single = false ) {
	return $GLOBALS['kk_sp_test_meta'][ $post_id ][ $key ] ?? '';
}

function __( $text ) {
	return $text;
}

function wp_trim_words( $text, $num_words = 55, $more = null ) {
	$words = preg_split( '/\s+/', trim( $text ) );
	if ( count( $words ) <= $num_words ) {
		return $text;
	}
	return implode( ' ', array_slice( $words, 0, $num_words ) ) . ( $more ?? '...' );
}

require_once dirname( __DIR__ ) . '/includes/render.php';
require_once dirname( __DIR__ ) . '/includes/luma-sync.php';
require_once dirname( __DIR__ ) . '/includes/cron.php';

function kk_sp_assert_same( $expected, $actual, $message ) {
	if ( $expected !== $actual ) {
		fwrite( STDERR, $message . PHP_EOL );
		fwrite( STDERR, 'Expected: ' . var_export( $expected, true ) . PHP_EOL );
		fwrite( STDERR, 'Actual:   ' . var_export( $actual, true ) . PHP_EOL );
		exit( 1 );
	}
}

$GLOBALS['kk_sp_test_meta'][123]['_wp_attachment_image_alt'] = 'Kris speaking at a packed Vancouver AI meetup.';
kk_sp_assert_same( 1, kk_sp_normalize_limit( 0 ), 'Limit should never fall below one card.' );
kk_sp_assert_same( 4, kk_sp_normalize_limit( 4 ), 'Limit should preserve normal values.' );
kk_sp_assert_same( 8, kk_sp_normalize_limit( 99 ), 'Limit should never exceed eight cards.' );
kk_sp_assert_same( 1, kk_sp_normalize_limit( 'not-a-number' ), 'Limit should coerce invalid values to one card.' );

kk_sp_assert_same(
	'Kris speaking at a packed Vancouver AI meetup.',
	kk_sp_get_image_alt( 123 ),
	'Attachment alt text should be preserved.'
);

$GLOBALS['kk_sp_test_meta'][124]['_wp_attachment_image_alt'] = '   ';
kk_sp_assert_same( '', kk_sp_get_image_alt( 124 ), 'Blank attachment alt should stay decorative.' );
kk_sp_assert_same( '', kk_sp_get_image_alt( 999 ), 'Missing attachment alt should stay decorative.' );

kk_sp_assert_same( '', kk_sp_render(), 'Rendering should be empty when no promos are published.' );

$GLOBALS['kk_sp_test_posts'] = [ 321, 322 ];
kk_sp_expire_featured_promos();
kk_sp_assert_same(
	[
		[ 'ID' => 321, 'post_status' => 'draft' ],
		[ 'ID' => 322, 'post_status' => 'draft' ],
	],
	$GLOBALS['kk_sp_updated_posts'],
	'Expired featured promos should be moved to draft.'
);
kk_sp_assert_same( 2, count( $GLOBALS['kk_sp_inserted_comments'] ), 'Expired promos should get audit comments.' );
$GLOBALS['kk_sp_test_posts'] = [];

$ical = "BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:event-1\r\nDTSTART;TZID=America/Vancouver:20260605T183000\r\nSUMMARY:Vancouver AI\\, Community Night\r\nURL:https://lu.ma/example\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n";
$events = kk_sp_parse_ical( $ical );
kk_sp_assert_same( 1, count( $events ), 'One VEVENT should parse.' );
kk_sp_assert_same( 'event-1', $events[0]['uid'], 'VEVENT UID should parse.' );
kk_sp_assert_same( 'Vancouver AI, Community Night', $events[0]['summary'], 'Escaped commas should be unescaped.' );
kk_sp_assert_same( 'https://lu.ma/example', $events[0]['url'], 'VEVENT URL should parse.' );

echo "KK Sidebar Promos smoke tests passed." . PHP_EOL;
