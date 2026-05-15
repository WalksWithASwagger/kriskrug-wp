<?php
/**
 * Seed the four pillar promos on first activation.
 *
 * Idempotent: skips creation if any promos already exist. Each pillar
 * uses an internal slug stored in meta so we won't double-create on
 * re-activation even if titles change.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KK_SP_META_SEED_SLUG = '_kk_promo_seed_slug';

function kk_sp_pillar_definitions() {
	return [
		[
			'slug'    => 'animation-accelerator',
			'title'   => __( 'Animation Accelerator', 'kk-sidebar-promos' ),
			'excerpt' => __( 'Hands-on cohort for filmmakers and creative teams shipping AI-augmented animation.', 'kk-sidebar-promos' ),
			'cta'     => __( 'Learn more', 'kk-sidebar-promos' ),
			'link'    => 'https://kriskrug.co/animation-accelerator/',
			'tone'    => 'course',
			'order'   => 10,
		],
		[
			'slug'    => 'rap-certification',
			'title'   => __( 'RAP Certification', 'kk-sidebar-promos' ),
			'excerpt' => __( '4-week Responsible AI Professional cohort. Live sessions, real assessments, take-home toolkit.', 'kk-sidebar-promos' ),
			'cta'     => __( 'Apply for next cohort', 'kk-sidebar-promos' ),
			'link'    => 'https://lu.ma/ai-ethics',
			'tone'    => 'course',
			'order'   => 20,
		],
		[
			'slug'    => 'bc-ai-membership',
			'title'   => __( 'BC + AI Membership', 'kk-sidebar-promos' ),
			'excerpt' => __( 'Join the people building the most inclusive AI ecosystem in the world. Members get half off everything.', 'kk-sidebar-promos' ),
			'cta'     => __( 'Become a member', 'kk-sidebar-promos' ),
			'link'    => 'https://bc-ai.ca/members/',
			'tone'    => 'community',
			'order'   => 30,
		],
		[
			'slug'    => 'vancouver-ai-community',
			'title'   => __( 'Vancouver AI Community', 'kk-sidebar-promos' ),
			'excerpt' => __( 'Multi-modal, multi-cultural, radically local. Monthly meetups across BC.', 'kk-sidebar-promos' ),
			'cta'     => __( 'See upcoming events', 'kk-sidebar-promos' ),
			'link'    => 'https://lu.ma/vancouver-ai',
			'tone'    => 'community',
			'order'   => 40,
		],
	];
}

function kk_sp_seed_pillars_if_empty() {
	foreach ( kk_sp_pillar_definitions() as $def ) {
		$existing = get_posts( [
			'post_type'      => KK_SP_POST_TYPE,
			'post_status'    => [ 'publish', 'draft', 'pending' ],
			'posts_per_page' => 1,
			'meta_query'     => [
				[
					'key'   => KK_SP_META_SEED_SLUG,
					'value' => $def['slug'],
				],
			],
			'fields'         => 'ids',
			'no_found_rows'  => true,
		] );
		if ( $existing ) {
			continue;
		}

		$post_id = wp_insert_post( [
			'post_type'    => KK_SP_POST_TYPE,
			'post_status'  => 'publish',
			'post_title'   => $def['title'],
			'post_excerpt' => $def['excerpt'],
			'menu_order'   => $def['order'],
		] );

		if ( is_wp_error( $post_id ) || ! $post_id ) {
			continue;
		}

		update_post_meta( $post_id, KK_SP_META_TYPE, 'pillar' );
		update_post_meta( $post_id, KK_SP_META_LINK, esc_url_raw( $def['link'] ) );
		update_post_meta( $post_id, KK_SP_META_CTA, $def['cta'] );
		update_post_meta( $post_id, KK_SP_META_TONE, $def['tone'] );
		update_post_meta( $post_id, KK_SP_META_SOURCE, 'manual' );
		update_post_meta( $post_id, KK_SP_META_SEED_SLUG, $def['slug'] );
	}
}
