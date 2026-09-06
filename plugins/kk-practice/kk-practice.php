<?php
/**
 * Plugin Name: KK Practice
 * Description: A browser-only context brief with an ordinary-content worksheet fallback.
 * Version: 0.1.0
 * Requires at least: 7.0
 * Requires PHP: 8.1
 * License: GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function kk_practice_copy() {
	return json_decode( file_get_contents( __DIR__ . '/blocks/context-brief/copy.json' ), true );
}

function kk_practice_register() {
	wp_register_script( 'kk-practice-editor', plugins_url( 'blocks/context-brief/editor.js', __FILE__ ), array( 'wp-blocks', 'wp-element' ), '0.1.0', true );
	wp_localize_script( 'kk-practice-editor', 'KKPracticeCopy', kk_practice_copy() );
	register_block_type( __DIR__ . '/blocks/context-brief' );
}
add_action( 'init', 'kk_practice_register' );

function kk_practice_is_page() {
	return is_singular() && has_block( 'kk/context-brief', get_queried_object() );
}

function kk_practice_nonce() {
	static $nonce;
	if ( ! $nonce ) {
		$nonce = base64_encode( random_bytes( 24 ) );
	}
	return $nonce;
}

function kk_practice_privacy_headers() {
	if ( ! kk_practice_is_page() ) {
		return;
	}
	// A nonce grants execution only to this exercise, including when another plugin prints raw scripts.
	header( "Content-Security-Policy: default-src 'self'; script-src 'nonce-" . kk_practice_nonce() . "'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'" );
	header( 'Referrer-Policy: no-referrer' );
	nocache_headers();
}
add_action( 'template_redirect', 'kk_practice_privacy_headers' );

function kk_practice_scripts() {
	if ( ! kk_practice_is_page() ) {
		return;
	}
	// Run before the #706 capture at 999 so its delayed footer loader never receives gtag.
	foreach ( wp_scripts()->queue as $handle ) {
		if ( 'kk-context-brief-view-script' !== $handle ) {
			wp_dequeue_script( $handle );
		}
	}
}
add_action( 'wp_enqueue_scripts', 'kk_practice_scripts', 998 );
add_action( 'wp_print_scripts', 'kk_practice_scripts', 99 );

function kk_practice_script_tag( $tag, $handle ) {
	if ( ! kk_practice_is_page() ) {
		return $tag;
	}
	if ( 'kk-context-brief-view-script' !== $handle ) {
		return '';
	}
	return str_replace( '<script ', '<script nonce="' . esc_attr( kk_practice_nonce() ) . '" ', $tag );
}
add_filter( 'script_loader_tag', 'kk_practice_script_tag', PHP_INT_MAX, 2 );

function kk_practice_inline_attributes( $attributes ) {
	if ( kk_practice_is_page() ) {
		$attributes['type'] = 'application/json';
	}
	return $attributes;
}
add_filter( 'wp_inline_script_attributes', 'kk_practice_inline_attributes', PHP_INT_MAX );
