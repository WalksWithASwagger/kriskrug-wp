<?php
/**
 * Lightweight smoke tests for KK Marquee Board — stubs the small WP surface needed so it
 * runs in this repo with no WordPress install. Run: php plugins/kk-marquee-board/tests/smoke.php
 */

define( 'ABSPATH', __DIR__ . '/wp-stub/' );

$GLOBALS['kk_mb_registered_types'] = [];
$GLOBALS['kk_mb_registered_meta']  = [];
$GLOBALS['kk_mb_actions']          = [];

function register_post_type( $type, $args ) { $GLOBALS['kk_mb_registered_types'][ $type ] = $args; }
function register_post_meta( $type, $key, $args ) { $GLOBALS['kk_mb_registered_meta'][ $key ] = $args; }
function add_action( $hook, $cb, $prio = 10, $args = 1 ) { $GLOBALS['kk_mb_actions'][] = [ $hook, $cb ]; }
function __( $t, $d = null ) { return $t; }
function current_user_can( $c ) { return true; }

// Schema-path stubs
function is_singular( $t ) { return true; }
function home_url( $p = '' ) { return 'https://kriskrug.co' . $p; }
function get_permalink() { return 'https://kriskrug.co/marquee/the-model-is-the-message/'; }
function get_the_title() { return 'The Model Is the Message'; }
function get_the_excerpt() { return 'A marquee board.'; }
function get_the_date( $f = '' ) { return '2026-06-26T00:00:00+00:00'; }
function get_the_modified_date( $f = '' ) { return '2026-06-26T00:00:00+00:00'; }
function has_post_thumbnail() { return false; }
function get_post_thumbnail_id() { return 0; }
function wp_get_attachment_image_src( $id, $size ) { return false; }
function wp_json_encode( $data, $flags = 0 ) { return json_encode( $data, $flags ); }

function kk_mb_assert( $cond, $message ) {
	if ( ! $cond ) {
		fwrite( STDERR, "FAIL: $message" . PHP_EOL );
		exit( 1 );
	}
}

require_once dirname( __DIR__ ) . '/includes/cpt.php';
require_once dirname( __DIR__ ) . '/includes/schema.php';

// --- CPT registration ---
kk_mb_register_post_type();
$args = $GLOBALS['kk_mb_registered_types']['marquee_board'] ?? null;
kk_mb_assert( $args !== null, 'marquee_board CPT should register' );
kk_mb_assert( $args['public'] === true, 'CPT must be public (for /marquee/ + Jetpack sitemap)' );
kk_mb_assert( $args['has_archive'] === true, 'CPT must have an archive' );
kk_mb_assert( $args['show_in_rest'] === true, 'CPT must be REST-enabled for sync.py' );
kk_mb_assert( $args['rewrite']['slug'] === 'marquee', 'rewrite slug must be marquee' );
foreach ( [ 'title', 'editor', 'excerpt', 'thumbnail' ] as $s ) {
	kk_mb_assert( in_array( $s, $args['supports'], true ), "CPT must support $s" );
}

// --- meta registration ---
kk_mb_register_meta();
foreach ( [ '_kk_mb_lines', '_kk_mb_week', '_kk_mb_skin', '_kk_mb_after', '_kk_mb_source', '_kk_mb_tags' ] as $k ) {
	kk_mb_assert( isset( $GLOBALS['kk_mb_registered_meta'][ $k ] ), "meta $k should register" );
	kk_mb_assert( $GLOBALS['kk_mb_registered_meta'][ $k ]['show_in_rest'] === true, "meta $k must be show_in_rest" );
}

// --- schema output ---
ob_start();
kk_mb_emit_schema();
$out = ob_get_clean();
kk_mb_assert( strpos( $out, '"@type":"Article"' ) !== false, 'schema should emit an Article' );
kk_mb_assert( strpos( $out, 'https://kriskrug.co/#person' ) !== false, 'Article must link to the Person @id' );
kk_mb_assert( strpos( $out, '"@type":"BreadcrumbList"' ) !== false, 'schema should emit a BreadcrumbList' );
kk_mb_assert( strpos( $out, 'Marquee' ) !== false, 'breadcrumb should include Marquee' );

echo 'KK Marquee Board smoke tests passed.' . PHP_EOL;
