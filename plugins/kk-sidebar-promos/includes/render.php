<?php
/**
 * Selection logic, widget, block, and shortcode for sidebar promos.
 *
 * Selection rules:
 *   - One Featured slot: the most-recent published, not-expired Featured promo
 *     (start date in the past, end date today or later). If none, that slot
 *     falls back to a rotating Pillar.
 *   - Up to 3 Pillar slots beneath, ordered by menu_order then date, but
 *     cycled by week so they don't always look identical.
 *   - Total visible promos defaults to 4; configurable via the block, widget,
 *     or shortcode.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_shortcode( 'kk_sidebar_promos', 'kk_sp_shortcode' );
add_action( 'widgets_init', 'kk_sp_register_widget' );
add_action( 'init', 'kk_sp_register_block' );

function kk_sp_get_promos( $limit = 4 ) {
	$limit = kk_sp_normalize_limit( $limit );
	$today = current_time( 'Y-m-d' );
	$out   = [];

	$featured = get_posts( [
		'post_type'      => KK_SP_POST_TYPE,
		'post_status'    => 'publish',
		'posts_per_page' => 1,
		'orderby'        => 'date',
		'order'          => 'DESC',
		'meta_query'     => [
			'relation' => 'AND',
			[
				'key'   => KK_SP_META_TYPE,
				'value' => 'featured',
			],
			[
				'relation' => 'OR',
				[
					'key'     => KK_SP_META_END,
					'value'   => $today,
					'compare' => '>=',
					'type'    => 'DATE',
				],
				[
					'key'     => KK_SP_META_END,
					'compare' => 'NOT EXISTS',
				],
			],
		],
		'no_found_rows'  => true,
	] );

	if ( $featured ) {
		$out[] = $featured[0];
	}

	$pillar_slots = max( 0, $limit - count( $out ) );
	if ( $pillar_slots > 0 ) {
		$pillars = get_posts( [
			'post_type'      => KK_SP_POST_TYPE,
			'post_status'    => 'publish',
			'posts_per_page' => 20,
			'orderby'        => [ 'menu_order' => 'ASC', 'date' => 'DESC' ],
			'meta_query'     => [
				[
					'key'   => KK_SP_META_TYPE,
					'value' => 'pillar',
				],
			],
			'post__not_in'   => wp_list_pluck( $out, 'ID' ),
			'no_found_rows'  => true,
		] );

		if ( $pillars ) {
			$week   = (int) gmdate( 'W' );
			$offset = $week % count( $pillars );
			$rotated = array_merge( array_slice( $pillars, $offset ), array_slice( $pillars, 0, $offset ) );
			$out    = array_merge( $out, array_slice( $rotated, 0, $pillar_slots ) );
		}
	}

	return $out;
}

function kk_sp_render( $args = [] ) {
	$args = wp_parse_args( $args, [
		'limit' => 4,
		'title' => '',
	] );

	$limit  = kk_sp_normalize_limit( $args['limit'] );
	$promos = kk_sp_get_promos( $limit );
	if ( ! $promos ) {
		return '';
	}

	wp_enqueue_style( 'kk-sidebar-promos' );

	ob_start();
		?>
		<div class="kk-sp">
			<?php if ( ! empty( $args['title'] ) ) : ?>
				<h2 class="kk-sp__heading"><?php echo esc_html( $args['title'] ); ?></h2>
			<?php endif; ?>
			<?php foreach ( $promos as $p ) :
				$type      = get_post_meta( $p->ID, KK_SP_META_TYPE, true ) ?: 'pillar';
				$tone      = get_post_meta( $p->ID, KK_SP_META_TONE, true ) ?: 'default';
				$link      = get_post_meta( $p->ID, KK_SP_META_LINK, true );
				$cta       = get_post_meta( $p->ID, KK_SP_META_CTA, true );
				$end       = get_post_meta( $p->ID, KK_SP_META_END, true );
				$thumb_id  = get_post_thumbnail_id( $p->ID );
				$has_image = (bool) $thumb_id;
				$image_alt = $has_image ? kk_sp_get_image_alt( $thumb_id ) : '';
				$classes   = [
					'kk-sp__card',
					'kk-sp__card--' . $type,
					'kk-sp__card--tone-' . $tone,
					$has_image ? 'kk-sp__card--has-image' : 'kk-sp__card--text-only',
				];
				?>
			<article class="<?php echo esc_attr( implode( ' ', $classes ) ); ?>">
				<?php if ( $link ) : ?>
					<a href="<?php echo esc_url( $link ); ?>" class="kk-sp__link" rel="noopener">
				<?php endif; ?>

				<?php if ( $has_image ) : ?>
					<div class="kk-sp__image-wrap">
						<?php echo wp_get_attachment_image(
							$thumb_id,
							'medium_large',
							false,
							[
								'class'   => 'kk-sp__image',
								'loading' => 'lazy',
								'alt'     => $image_alt,
							]
						); ?>
						<?php if ( $type === 'featured' && $end ) : ?>
							<span class="kk-sp__badge"><?php echo esc_html( kk_sp_format_until( $end ) ); ?></span>
						<?php endif; ?>
					</div>
				<?php endif; ?>

				<div class="kk-sp__body">
					<h3 class="kk-sp__title"><?php echo esc_html( get_the_title( $p ) ); ?></h3>
					<?php if ( $p->post_excerpt || $p->post_content ) : ?>
						<p class="kk-sp__excerpt">
							<?php echo esc_html( wp_strip_all_tags( $p->post_excerpt ?: wp_trim_words( $p->post_content, 18, '…' ) ) ); ?>
						</p>
					<?php endif; ?>
					<?php if ( $cta ) : ?>
						<span class="kk-sp__cta"><?php echo esc_html( $cta ); ?> <span aria-hidden="true">→</span></span>
					<?php endif; ?>
				</div>

				<?php if ( $link ) : ?>
					</a>
				<?php endif; ?>
			</article>
		<?php endforeach; ?>
	</div>
	<?php
	return (string) ob_get_clean();
}

function kk_sp_normalize_limit( $limit ) {
	$limit = (int) $limit;

	return max( 1, min( 8, $limit ) );
}

function kk_sp_get_image_alt( $thumb_id ) {
	$alt = trim( (string) get_post_meta( $thumb_id, '_wp_attachment_image_alt', true ) );

	return $alt;
}

function kk_sp_format_until( $end ) {
	$ts   = strtotime( $end . ' 23:59:59' );
	$now  = current_time( 'timestamp' );
	$days = (int) ceil( ( $ts - $now ) / DAY_IN_SECONDS );

	if ( $days <= 0 ) {
		return __( 'Today', 'kk-sidebar-promos' );
	}
	if ( $days === 1 ) {
		return __( '1 day left', 'kk-sidebar-promos' );
	}
	if ( $days <= 14 ) {
		/* translators: %d: number of days remaining */
		return sprintf( __( '%d days left', 'kk-sidebar-promos' ), $days );
	}
	return date_i18n( get_option( 'date_format' ), $ts );
}

function kk_sp_shortcode( $atts ) {
	$atts = shortcode_atts(
		[ 'limit' => 4, 'title' => '' ],
		$atts,
		'kk_sidebar_promos'
	);
	return kk_sp_render( $atts );
}

function kk_sp_register_widget() {
	register_widget( 'KK_SP_Widget' );
}

function kk_sp_register_block() {
	if ( ! function_exists( 'register_block_type' ) ) {
		return;
	}
	register_block_type( 'kk/sidebar-promos', [
		'api_version'     => 2,
		'title'           => __( 'KK Sidebar Promos', 'kk-sidebar-promos' ),
		'category'        => 'widgets',
		'icon'            => 'megaphone',
		'description'     => __( 'Auto-managed promotional cards. Featured promos auto-expire; pillars rotate.', 'kk-sidebar-promos' ),
		'attributes'      => [
			'limit' => [ 'type' => 'number', 'default' => 4 ],
			'title' => [ 'type' => 'string', 'default' => '' ],
		],
		'render_callback' => static function ( $attrs ) {
			return kk_sp_render( [
				'limit' => isset( $attrs['limit'] ) ? kk_sp_normalize_limit( $attrs['limit'] ) : 4,
				'title' => isset( $attrs['title'] ) ? (string) $attrs['title'] : '',
			] );
		},
	] );
}

class KK_SP_Widget extends WP_Widget {
	public function __construct() {
		parent::__construct(
			'kk_sp_widget',
			__( 'KK Sidebar Promos', 'kk-sidebar-promos' ),
			[ 'description' => __( 'Auto-managed promotional cards.', 'kk-sidebar-promos' ) ]
		);
	}

	public function widget( $args, $instance ) {
		$title = $instance['title'] ?? '';
		$limit = kk_sp_normalize_limit( $instance['limit'] ?? 4 );
		echo $args['before_widget']; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		echo kk_sp_render( [ 'limit' => $limit, 'title' => $title ] ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
		echo $args['after_widget']; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
	}

	public function form( $instance ) {
		$title = $instance['title'] ?? '';
		$limit = kk_sp_normalize_limit( $instance['limit'] ?? 4 );
		?>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"><?php esc_html_e( 'Heading (optional):', 'kk-sidebar-promos' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>" type="text" value="<?php echo esc_attr( $title ); ?>">
		</p>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'limit' ) ); ?>"><?php esc_html_e( 'Max promos:', 'kk-sidebar-promos' ); ?></label>
			<input class="tiny-text" id="<?php echo esc_attr( $this->get_field_id( 'limit' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'limit' ) ); ?>" type="number" min="1" max="8" value="<?php echo esc_attr( $limit ); ?>">
		</p>
		<?php
	}

	public function update( $new, $old ) {
		return [
			'title' => sanitize_text_field( $new['title'] ?? '' ),
			'limit' => kk_sp_normalize_limit( $new['limit'] ?? 4 ),
		];
	}
}
