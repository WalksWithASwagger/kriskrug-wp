<?php
/**
 * Plugin Name:       KK Marquee Board
 * Plugin URI:        https://github.com/WalksWithASwagger/kriskrug-wp
 * Description:       Serves The Marquee at /marquee/ — a custom post type for the self-improving marquee boards (the LED "now showing" line that leads the homepage). Public, REST-enabled (synced by scripts/marquee/sync.py), and indexed via the Jetpack sitemap. Source of truth stays content/marquee/marquee.json.
 * Version:           0.1.0
 * Requires at least: 6.2
 * Requires PHP:      7.4
 * Author:            Kris Krüg
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       kk-marquee-board
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'KK_MB_VERSION', '0.1.0' );
define( 'KK_MB_PATH', plugin_dir_path( __FILE__ ) );
define( 'KK_MB_URL', plugin_dir_url( __FILE__ ) );
define( 'KK_MB_FILE', __FILE__ );

require_once KK_MB_PATH . 'includes/cpt.php';
require_once KK_MB_PATH . 'includes/schema.php';

/**
 * Enqueue the board CSS/JS only where a board renders: marquee_board single + archive.
 * (The homepage hero is served by the theme, which enqueues its own copy.) Assets are
 * generated from scripts/marquee/render.py by build.py — single source of truth.
 */
add_action( 'wp_enqueue_scripts', 'kk_mb_enqueue_assets' );
function kk_mb_enqueue_assets() {
	if ( ! ( is_singular( KK_MB_POST_TYPE ) || is_post_type_archive( KK_MB_POST_TYPE ) ) ) {
		return;
	}
	wp_enqueue_style(
		'kk-marquee-board',
		KK_MB_URL . 'assets/marquee.css',
		[],
		KK_MB_VERSION
	);
	wp_enqueue_script(
		'kk-marquee-board',
		KK_MB_URL . 'assets/marquee.js',
		[],
		KK_MB_VERSION,
		[
			'strategy'  => 'defer',
			'in_footer' => true,
		]
	);
}

register_activation_hook( __FILE__, 'kk_mb_on_activate' );
register_deactivation_hook( __FILE__, 'kk_mb_on_deactivate' );

function kk_mb_on_activate() {
	kk_mb_register_post_type();
	flush_rewrite_rules();
}

function kk_mb_on_deactivate() {
	flush_rewrite_rules();
}
