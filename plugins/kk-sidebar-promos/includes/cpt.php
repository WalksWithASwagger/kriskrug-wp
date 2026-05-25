<?php
/**
 * Custom post type and meta for sidebar promos.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KK_SP_POST_TYPE     = 'kk_promo';
const KK_SP_META_TYPE     = '_kk_promo_type';        // 'pillar' | 'featured'
const KK_SP_META_LINK     = '_kk_promo_link';
const KK_SP_META_CTA      = '_kk_promo_cta';
const KK_SP_META_END      = '_kk_promo_end';         // YYYY-MM-DD
const KK_SP_META_TONE     = '_kk_promo_tone';        // default | event | course | community
const KK_SP_META_SOURCE   = '_kk_promo_source';      // manual | luma
const KK_SP_META_SOURCE_ID = '_kk_promo_source_id';

add_action( 'init', 'kk_sp_register_post_type' );
add_action( 'init', 'kk_sp_register_meta' );
add_action( 'add_meta_boxes', 'kk_sp_add_meta_boxes' );
add_action( 'save_post_' . KK_SP_POST_TYPE, 'kk_sp_save_meta', 10, 2 );
add_filter( 'manage_' . KK_SP_POST_TYPE . '_posts_columns', 'kk_sp_admin_columns' );
add_action( 'manage_' . KK_SP_POST_TYPE . '_posts_custom_column', 'kk_sp_admin_column_content', 10, 2 );

function kk_sp_register_post_type() {
	register_post_type( KK_SP_POST_TYPE, [
		'labels' => [
			'name'               => __( 'Sidebar Promos', 'kk-sidebar-promos' ),
			'singular_name'      => __( 'Sidebar Promo', 'kk-sidebar-promos' ),
			'add_new_item'       => __( 'Add New Promo', 'kk-sidebar-promos' ),
			'edit_item'          => __( 'Edit Promo', 'kk-sidebar-promos' ),
			'new_item'           => __( 'New Promo', 'kk-sidebar-promos' ),
			'view_item'          => __( 'View Promo', 'kk-sidebar-promos' ),
			'search_items'       => __( 'Search Promos', 'kk-sidebar-promos' ),
			'menu_name'          => __( 'Sidebar Promos', 'kk-sidebar-promos' ),
		],
		'public'        => false,
		'show_ui'       => true,
		'show_in_rest'  => true,
		'menu_icon'     => 'dashicons-megaphone',
		'menu_position' => 22,
		'supports'      => [ 'title', 'editor', 'thumbnail', 'page-attributes' ],
		'has_archive'   => false,
		'rewrite'       => false,
	] );
}

function kk_sp_register_meta() {
	$keys = [
		KK_SP_META_TYPE,
		KK_SP_META_LINK,
		KK_SP_META_CTA,
		KK_SP_META_END,
		KK_SP_META_TONE,
		KK_SP_META_SOURCE,
		KK_SP_META_SOURCE_ID,
	];
	foreach ( $keys as $key ) {
		register_post_meta( KK_SP_POST_TYPE, $key, [
			'show_in_rest'  => true,
			'single'        => true,
			'type'          => 'string',
			'auth_callback' => static function () {
				return current_user_can( 'edit_posts' );
			},
		] );
	}
}

function kk_sp_add_meta_boxes() {
	add_meta_box(
		'kk_sp_settings',
		__( 'Promo Settings', 'kk-sidebar-promos' ),
		'kk_sp_render_meta_box',
		KK_SP_POST_TYPE,
		'side',
		'high'
	);
}

function kk_sp_render_meta_box( $post ) {
	wp_nonce_field( 'kk_sp_save_meta', 'kk_sp_nonce' );

	$type   = get_post_meta( $post->ID, KK_SP_META_TYPE, true ) ?: 'pillar';
	$link   = get_post_meta( $post->ID, KK_SP_META_LINK, true );
	$cta    = get_post_meta( $post->ID, KK_SP_META_CTA, true );
	$end    = get_post_meta( $post->ID, KK_SP_META_END, true );
	$tone   = get_post_meta( $post->ID, KK_SP_META_TONE, true ) ?: 'default';
	$source = get_post_meta( $post->ID, KK_SP_META_SOURCE, true );
	?>
	<p>
		<label><strong><?php esc_html_e( 'Type', 'kk-sidebar-promos' ); ?></strong></label><br>
		<select name="kk_sp_type" style="width:100%">
			<option value="pillar"   <?php selected( $type, 'pillar' ); ?>><?php esc_html_e( 'Pillar (evergreen)', 'kk-sidebar-promos' ); ?></option>
			<option value="featured" <?php selected( $type, 'featured' ); ?>><?php esc_html_e( 'Featured (time-bound)', 'kk-sidebar-promos' ); ?></option>
		</select>
	</p>
	<p>
		<label><strong><?php esc_html_e( 'Link URL', 'kk-sidebar-promos' ); ?></strong></label><br>
		<input type="url" name="kk_sp_link" value="<?php echo esc_attr( $link ); ?>" style="width:100%" placeholder="https://...">
	</p>
	<p>
		<label><strong><?php esc_html_e( 'CTA text', 'kk-sidebar-promos' ); ?></strong></label><br>
		<input type="text" name="kk_sp_cta" value="<?php echo esc_attr( $cta ); ?>" style="width:100%" placeholder="<?php esc_attr_e( 'Learn more', 'kk-sidebar-promos' ); ?>">
	</p>
	<p>
		<label><strong><?php esc_html_e( 'Active until', 'kk-sidebar-promos' ); ?></strong></label><br>
		<input type="date" name="kk_sp_end" value="<?php echo esc_attr( $end ); ?>" style="width:100%">
		<em><?php esc_html_e( 'Required for Featured. Promo is hidden the day after this date.', 'kk-sidebar-promos' ); ?></em>
	</p>
	<p>
		<label><strong><?php esc_html_e( 'Tone', 'kk-sidebar-promos' ); ?></strong></label><br>
		<select name="kk_sp_tone" style="width:100%">
			<?php foreach ( [ 'default', 'event', 'course', 'community' ] as $opt ) : ?>
				<option value="<?php echo esc_attr( $opt ); ?>" <?php selected( $tone, $opt ); ?>><?php echo esc_html( ucfirst( $opt ) ); ?></option>
			<?php endforeach; ?>
		</select>
	</p>
	<?php if ( $source && $source !== 'manual' ) : ?>
		<p style="background:#fff8e1;padding:8px;border-left:3px solid #f39c12">
			<em><?php
			/* translators: %s: source name */
			printf( esc_html__( 'Auto-managed (source: %s). Manual edits may be overwritten on the next sync.', 'kk-sidebar-promos' ), esc_html( $source ) );
			?></em>
		</p>
	<?php endif;
}

function kk_sp_save_meta( $post_id, $post ) {
	$nonce = isset( $_POST['kk_sp_nonce'] ) ? sanitize_text_field( wp_unslash( $_POST['kk_sp_nonce'] ) ) : '';
	if ( ! $nonce || ! wp_verify_nonce( $nonce, 'kk_sp_save_meta' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$type = isset( $_POST['kk_sp_type'] ) && in_array( $_POST['kk_sp_type'], [ 'pillar', 'featured' ], true )
		? sanitize_key( wp_unslash( $_POST['kk_sp_type'] ) )
		: 'pillar';
	update_post_meta( $post_id, KK_SP_META_TYPE, $type );

	$link = isset( $_POST['kk_sp_link'] ) ? esc_url_raw( wp_unslash( $_POST['kk_sp_link'] ) ) : '';
	update_post_meta( $post_id, KK_SP_META_LINK, $link );

	$cta = isset( $_POST['kk_sp_cta'] ) ? sanitize_text_field( wp_unslash( $_POST['kk_sp_cta'] ) ) : '';
	update_post_meta( $post_id, KK_SP_META_CTA, $cta );

	$end = isset( $_POST['kk_sp_end'] ) ? sanitize_text_field( wp_unslash( $_POST['kk_sp_end'] ) ) : '';
	if ( $type === 'featured' && preg_match( '/^\d{4}-\d{2}-\d{2}$/', $end ) ) {
		update_post_meta( $post_id, KK_SP_META_END, $end );
	} else {
		delete_post_meta( $post_id, KK_SP_META_END );
	}

	$tone = isset( $_POST['kk_sp_tone'] ) ? sanitize_key( wp_unslash( $_POST['kk_sp_tone'] ) ) : 'default';
	update_post_meta(
		$post_id,
		KK_SP_META_TONE,
		in_array( $tone, [ 'default', 'event', 'course', 'community' ], true ) ? $tone : 'default'
	);
}

function kk_sp_admin_columns( $cols ) {
	$new = [];
	foreach ( $cols as $k => $v ) {
		$new[ $k ] = $v;
		if ( $k === 'title' ) {
			$new['kk_sp_type']    = __( 'Type', 'kk-sidebar-promos' );
			$new['kk_sp_expires'] = __( 'Expires', 'kk-sidebar-promos' );
			$new['kk_sp_source']  = __( 'Source', 'kk-sidebar-promos' );
		}
	}
	return $new;
}

function kk_sp_admin_column_content( $col, $post_id ) {
	if ( $col === 'kk_sp_type' ) {
		$type = get_post_meta( $post_id, KK_SP_META_TYPE, true ) ?: 'pillar';
		echo esc_html( ucfirst( $type ) );
	}
	if ( $col === 'kk_sp_expires' ) {
		$end = get_post_meta( $post_id, KK_SP_META_END, true );
		if ( ! $end ) {
			echo '—';
			return;
		}
		$today   = current_time( 'Y-m-d' );
		$expired = $end < $today;
		printf(
			'<span style="color:%s">%s%s</span>',
			$expired ? '#b00' : '#070',
			esc_html( $end ),
			$expired ? ' (' . esc_html__( 'expired', 'kk-sidebar-promos' ) . ')' : ''
		);
	}
	if ( $col === 'kk_sp_source' ) {
		$source = get_post_meta( $post_id, KK_SP_META_SOURCE, true ) ?: 'manual';
		echo esc_html( $source );
	}
}
