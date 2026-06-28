<?php
/**
 * Custom post type + meta for marquee boards.
 *
 * The board phrase is the post title; the rendered LED board HTML is the post content;
 * the dek is the excerpt; the OG card is the featured image. Meta carries the structured
 * fields the sync writes (lines, week, skin, after, source, tags) for fidelity + re-render.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KK_MB_POST_TYPE   = 'marquee_board';
const KK_MB_META_LINES  = '_kk_mb_lines';   // JSON array of board rows, e.g. ["THE MODEL","IS THE","MESSAGE"]
const KK_MB_META_WEEK   = '_kk_mb_week';    // e.g. 2026-W26
const KK_MB_META_SKIN   = '_kk_mb_skin';    // led | splitflap | letterpress | teletype
const KK_MB_META_AFTER  = '_kk_mb_after';   // attribution, e.g. "Marshall McLuhan"
const KK_MB_META_SOURCE = '_kk_mb_source';  // JSON {title, author, remixed_from}
const KK_MB_META_TAGS   = '_kk_mb_tags';    // comma-separated slugs

add_action( 'init', 'kk_mb_register_post_type' );
add_action( 'init', 'kk_mb_register_meta' );

function kk_mb_register_post_type() {
	register_post_type( KK_MB_POST_TYPE, [
		'labels' => [
			'name'          => __( 'Marquee Boards', 'kk-marquee-board' ),
			'singular_name' => __( 'Marquee Board', 'kk-marquee-board' ),
			'add_new_item'  => __( 'Add New Board', 'kk-marquee-board' ),
			'edit_item'     => __( 'Edit Board', 'kk-marquee-board' ),
			'new_item'      => __( 'New Board', 'kk-marquee-board' ),
			'view_item'     => __( 'View Board', 'kk-marquee-board' ),
			'search_items'  => __( 'Search Boards', 'kk-marquee-board' ),
			'menu_name'     => __( 'Marquee Boards', 'kk-marquee-board' ),
		],
		'public'       => true,
		'show_ui'      => true,
		'show_in_rest' => true,                 // required for sync.py REST writes + block editor
		'menu_icon'    => 'dashicons-format-gallery',
		'menu_position' => 21,
		'supports'     => [ 'title', 'editor', 'excerpt', 'thumbnail', 'custom-fields' ],
		'has_archive'  => true,                  // /marquee/ archive (Jetpack auto-sitemaps public CPTs)
		'rewrite'      => [ 'slug' => 'marquee', 'with_front' => false ],
	] );
}

function kk_mb_register_meta() {
	$string_keys = [
		KK_MB_META_LINES,
		KK_MB_META_WEEK,
		KK_MB_META_SKIN,
		KK_MB_META_AFTER,
		KK_MB_META_SOURCE,
		KK_MB_META_TAGS,
	];
	foreach ( $string_keys as $key ) {
		register_post_meta( KK_MB_POST_TYPE, $key, [
			'show_in_rest'  => true,
			'single'        => true,
			'type'          => 'string',
			'auth_callback' => static function () {
				return current_user_can( 'edit_posts' );
			},
		] );
	}
}
