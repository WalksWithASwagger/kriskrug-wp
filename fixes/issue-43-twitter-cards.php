<?php
/**
 * Issue #43: Twitter/X Card tags for kriskrug.co.
 *
 * Deployment status: Jetpack owns the live Open Graph/Twitter layer today.
 * Use this as a Code Snippets or mu-plugin patch only while Jetpack remains
 * the meta provider. Do not deploy it alongside Rank Math/Yoast/AIOSEO social
 * metadata without first disabling the competing social tag output.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'KK_ISSUE_43_TWITTER_HANDLE', '@feelmoreplants' );
define( 'KK_ISSUE_43_CARD_WIDTH', 1200 );
define( 'KK_ISSUE_43_CARD_HEIGHT', 630 );
define( 'KK_ISSUE_43_FALLBACK_IMAGE_ID', 7548 );
define( 'KK_ISSUE_43_FALLBACK_IMAGE_URL', 'https://kriskrug.co/wp-content/uploads/2024/11/kriskrug-websute.png' );

add_filter( 'jetpack_open_graph_tags', 'kk_issue_43_twitter_cards', 20 );

function kk_issue_43_twitter_cards( $tags ) {
	if ( ! kk_issue_43_is_share_surface() ) {
		return $tags;
	}

	$title       = kk_issue_43_title();
	$desc        = kk_issue_43_description();
	$image       = kk_issue_43_card_image();
	$image_alt   = $image['alt'] ? $image['alt'] : $title;
	$card_width  = (string) KK_ISSUE_43_CARD_WIDTH;
	$card_height = (string) KK_ISSUE_43_CARD_HEIGHT;

	$tags['twitter:card']    = 'summary_large_image';
	$tags['twitter:site']    = KK_ISSUE_43_TWITTER_HANDLE;
	$tags['twitter:creator'] = KK_ISSUE_43_TWITTER_HANDLE;

	if ( $title ) {
		$tags['twitter:title']      = $title;
		$tags['twitter:text:title'] = $title;
	}

	if ( $desc ) {
		$tags['twitter:description'] = $desc;
	}

	if ( $image['url'] ) {
		$tags['twitter:image']     = $image['url'];
		$tags['twitter:image:alt'] = $image_alt;
		$tags['og:image']          = $image['url'];
		$tags['og:image:width']    = $card_width;
		$tags['og:image:height']   = $card_height;
		$tags['og:image:alt']      = $image_alt;
	}

	return $tags;
}

function kk_issue_43_is_share_surface() {
	return is_front_page() || is_home() || is_singular();
}

function kk_issue_43_title() {
	$post_id = kk_issue_43_object_id();

	if ( $post_id ) {
		return wp_strip_all_tags( get_the_title( $post_id ) );
	}

	return wp_strip_all_tags( get_bloginfo( 'name' ) );
}

function kk_issue_43_description() {
	$post_id = kk_issue_43_object_id();

	if ( ! $post_id ) {
		return wp_strip_all_tags( get_bloginfo( 'description' ) );
	}

	$description = get_the_excerpt( $post_id );

	if ( ! $description ) {
		$post = get_post( $post_id );
		$description = $post ? $post->post_content : '';
	}

	$description = html_entity_decode( wp_strip_all_tags( $description ), ENT_QUOTES, get_bloginfo( 'charset' ) );

	return wp_trim_words( $description, 35, '' );
}

function kk_issue_43_card_image() {
	$post_id  = kk_issue_43_object_id();
	$image_id = $post_id ? get_post_thumbnail_id( $post_id ) : 0;

	if ( ! $image_id ) {
		$image_id = KK_ISSUE_43_FALLBACK_IMAGE_ID;
	}

	$image_url = kk_issue_43_attachment_card_url( $image_id );
	$image_alt = $image_id ? get_post_meta( $image_id, '_wp_attachment_image_alt', true ) : '';

	if ( ! $image_url ) {
		$image_url = kk_issue_43_photon_resize_url( KK_ISSUE_43_FALLBACK_IMAGE_URL );
	}

	return [
		'url' => $image_url,
		'alt' => wp_strip_all_tags( $image_alt ),
	];
}

function kk_issue_43_object_id() {
	if ( is_home() && ! is_front_page() ) {
		return (int) get_option( 'page_for_posts' );
	}

	return (int) get_queried_object_id();
}

function kk_issue_43_attachment_card_url( $image_id ) {
	$image = wp_get_attachment_image_src( $image_id, 'full' );

	if ( ! $image || empty( $image[0] ) ) {
		return '';
	}

	return kk_issue_43_photon_resize_url( $image[0] );
}

function kk_issue_43_photon_resize_url( $url ) {
	$parts = wp_parse_url( $url );

	if ( empty( $parts['host'] ) || empty( $parts['path'] ) ) {
		return '';
	}

	$host = $parts['host'];
	$path = $parts['path'];

	if ( preg_match( '/^i[0-2]\.wp\.com$/', $host ) ) {
		return esc_url_raw( sprintf(
			'https://%s%s?resize=%d%%2C%d&ssl=1',
			$host,
			$path,
			KK_ISSUE_43_CARD_WIDTH,
			KK_ISSUE_43_CARD_HEIGHT
		) );
	}

	return esc_url_raw( sprintf(
		'https://i0.wp.com/%s%s?resize=%d%%2C%d&ssl=1',
		$host,
		$path,
		KK_ISSUE_43_CARD_WIDTH,
		KK_ISSUE_43_CARD_HEIGHT
	) );
}
