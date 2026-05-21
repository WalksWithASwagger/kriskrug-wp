<?php
/**
 * Plugin Name:       KK Sidebar Promos
 * Plugin URI:        https://github.com/WalksWithASwagger/kriskrug-wp
 * Description:       Auto-managed sidebar promo system. Featured promos auto-expire on their end date; evergreen "pillar" promos rotate to fill the rest. Pulls the next Vancouver AI meetup from Luma automatically. Block, classic widget, and [kk_sidebar_promos] shortcode all available.
 * Version:           0.1.2
 * Requires at least: 6.2
 * Requires PHP:      7.4
 * Author:            Kris Krüg
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       kk-sidebar-promos
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'KK_SP_VERSION', '0.1.2' );
define( 'KK_SP_PATH', plugin_dir_path( __FILE__ ) );
define( 'KK_SP_URL', plugin_dir_url( __FILE__ ) );
define( 'KK_SP_FILE', __FILE__ );

require_once KK_SP_PATH . 'includes/cpt.php';
require_once KK_SP_PATH . 'includes/render.php';
require_once KK_SP_PATH . 'includes/luma-sync.php';
require_once KK_SP_PATH . 'includes/cron.php';
require_once KK_SP_PATH . 'includes/seed.php';
require_once KK_SP_PATH . 'includes/settings.php';

add_action( 'wp_enqueue_scripts', function () {
	wp_register_style(
		'kk-sidebar-promos',
		KK_SP_URL . 'assets/css/sidebar-promos.css',
		[],
		KK_SP_VERSION
	);
} );

register_activation_hook( __FILE__, 'kk_sp_on_activate' );
register_deactivation_hook( __FILE__, 'kk_sp_on_deactivate' );

function kk_sp_on_activate() {
	kk_sp_register_post_type();
	flush_rewrite_rules();
	kk_sp_schedule_events();
	kk_sp_seed_pillars_if_empty();
}

function kk_sp_on_deactivate() {
	kk_sp_unschedule_events();
	flush_rewrite_rules();
}
