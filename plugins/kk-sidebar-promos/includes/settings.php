<?php
/**
 * Settings page (Settings → Sidebar Promos).
 *
 * Configure the Luma iCal feed and run a manual sync.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'admin_menu', 'kk_sp_settings_menu' );
add_action( 'admin_init', 'kk_sp_settings_register' );
add_action( 'admin_post_kk_sp_run_sync', 'kk_sp_handle_manual_sync' );

function kk_sp_settings_menu() {
	add_submenu_page(
		'edit.php?post_type=' . KK_SP_POST_TYPE,
		__( 'Sidebar Promos Settings', 'kk-sidebar-promos' ),
		__( 'Settings', 'kk-sidebar-promos' ),
		'manage_options',
		'kk-sp-settings',
		'kk_sp_settings_page'
	);
}

function kk_sp_settings_register() {
	register_setting( 'kk_sp_settings', KK_SP_OPT_LUMA_URL, [
		'type'              => 'string',
		'sanitize_callback' => 'esc_url_raw',
		'default'           => '',
	] );
	register_setting( 'kk_sp_settings', KK_SP_OPT_LUMA_LABEL, [
		'type'              => 'string',
		'sanitize_callback' => 'sanitize_text_field',
		'default'           => __( 'Vancouver AI Community', 'kk-sidebar-promos' ),
	] );
	register_setting( 'kk_sp_settings', KK_SP_OPT_LUMA_LINK, [
		'type'              => 'string',
		'sanitize_callback' => 'esc_url_raw',
		'default'           => 'https://lu.ma/vancouver-ai',
	] );
}

function kk_sp_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$ical_url   = get_option( KK_SP_OPT_LUMA_URL, '' );
	$label      = get_option( KK_SP_OPT_LUMA_LABEL, __( 'Vancouver AI Community', 'kk-sidebar-promos' ) );
	$link       = get_option( KK_SP_OPT_LUMA_LINK, 'https://lu.ma/vancouver-ai' );
	$next_cron  = wp_next_scheduled( KK_SP_CRON_LUMA );
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Sidebar Promos', 'kk-sidebar-promos' ); ?></h1>

		<?php if ( isset( $_GET['kk_sp_synced'] ) ) : // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			$result = sanitize_text_field( wp_unslash( $_GET['kk_sp_synced'] ) ); // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			$class  = $result === 'ok' ? 'notice-success' : 'notice-error';
			?>
			<div class="notice <?php echo esc_attr( $class ); ?> is-dismissible">
				<p><?php echo esc_html( $result === 'ok'
					? __( 'Luma sync ran. Check the promo list for the latest event.', 'kk-sidebar-promos' )
					: sprintf( __( 'Sync failed: %s', 'kk-sidebar-promos' ), $result )
				); ?></p>
			</div>
		<?php endif; ?>

		<form action="options.php" method="post">
			<?php settings_fields( 'kk_sp_settings' ); ?>
			<table class="form-table">
				<tr>
					<th><label for="kk_sp_luma_url"><?php esc_html_e( 'Luma iCal URL', 'kk-sidebar-promos' ); ?></label></th>
					<td>
						<input type="url" id="kk_sp_luma_url" name="<?php echo esc_attr( KK_SP_OPT_LUMA_URL ); ?>" value="<?php echo esc_attr( $ical_url ); ?>" class="regular-text" placeholder="https://api.lu.ma/ics/get?entity=calendar&id=...">
						<p class="description"><?php esc_html_e( 'Find this on lu.ma → calendar settings → "Subscribe via iCal".', 'kk-sidebar-promos' ); ?></p>
					</td>
				</tr>
				<tr>
					<th><label for="kk_sp_luma_label"><?php esc_html_e( 'Promo label', 'kk-sidebar-promos' ); ?></label></th>
					<td>
						<input type="text" id="kk_sp_luma_label" name="<?php echo esc_attr( KK_SP_OPT_LUMA_LABEL ); ?>" value="<?php echo esc_attr( $label ); ?>" class="regular-text">
						<p class="description"><?php esc_html_e( 'Prefixed to the next event date in the promo title.', 'kk-sidebar-promos' ); ?></p>
					</td>
				</tr>
				<tr>
					<th><label for="kk_sp_luma_link"><?php esc_html_e( 'Calendar fallback URL', 'kk-sidebar-promos' ); ?></label></th>
					<td>
						<input type="url" id="kk_sp_luma_link" name="<?php echo esc_attr( KK_SP_OPT_LUMA_LINK ); ?>" value="<?php echo esc_attr( $link ); ?>" class="regular-text">
						<p class="description"><?php esc_html_e( 'Used if a specific event URL is unavailable.', 'kk-sidebar-promos' ); ?></p>
					</td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>

		<hr>

		<h2><?php esc_html_e( 'Manual sync', 'kk-sidebar-promos' ); ?></h2>
		<p>
			<?php
			if ( $next_cron ) {
				/* translators: %s: human-readable date */
				echo esc_html( sprintf( __( 'Next automatic sync: %s', 'kk-sidebar-promos' ), wp_date( 'M j, Y g:i a', $next_cron ) ) );
			} else {
				esc_html_e( 'Automatic sync is not currently scheduled.', 'kk-sidebar-promos' );
			}
			?>
		</p>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<input type="hidden" name="action" value="kk_sp_run_sync">
			<?php wp_nonce_field( 'kk_sp_run_sync' ); ?>
			<?php submit_button( __( 'Run Luma sync now', 'kk-sidebar-promos' ), 'secondary', 'submit', false ); ?>
		</form>

		<hr>

		<h2><?php esc_html_e( 'Where this shows up', 'kk-sidebar-promos' ); ?></h2>
		<ul style="list-style:disc;margin-left:1.5em">
			<li><?php esc_html_e( 'Block: search "KK Sidebar Promos" in the block inserter.', 'kk-sidebar-promos' ); ?></li>
			<li><?php esc_html_e( 'Classic widget: Appearance → Widgets → KK Sidebar Promos.', 'kk-sidebar-promos' ); ?></li>
			<li><code>[kk_sidebar_promos limit="4"]</code></li>
		</ul>
	</div>
	<?php
}

function kk_sp_handle_manual_sync() {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( esc_html__( 'Insufficient permissions.', 'kk-sidebar-promos' ) );
	}
	check_admin_referer( 'kk_sp_run_sync' );

	$result   = kk_sp_run_luma_sync();
	$redirect = add_query_arg(
		'kk_sp_synced',
		is_wp_error( $result ) ? rawurlencode( $result->get_error_message() ) : 'ok',
		admin_url( 'edit.php?post_type=' . KK_SP_POST_TYPE . '&page=kk-sp-settings' )
	);
	wp_safe_redirect( $redirect );
	exit;
}
