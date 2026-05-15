<?php
/**
 * Scheduled tasks: auto-expire featured promos and trigger Luma sync.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KK_SP_CRON_EXPIRE = 'kk_sp_expire_featured';
const KK_SP_CRON_LUMA   = 'kk_sp_luma_sync';

add_action( KK_SP_CRON_EXPIRE, 'kk_sp_expire_featured_promos' );
add_action( KK_SP_CRON_LUMA, 'kk_sp_run_luma_sync' );

function kk_sp_schedule_events() {
	if ( ! wp_next_scheduled( KK_SP_CRON_EXPIRE ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', KK_SP_CRON_EXPIRE );
	}
	if ( ! wp_next_scheduled( KK_SP_CRON_LUMA ) ) {
		wp_schedule_event( time() + ( 2 * HOUR_IN_SECONDS ), 'daily', KK_SP_CRON_LUMA );
	}
}

function kk_sp_unschedule_events() {
	$timestamp = wp_next_scheduled( KK_SP_CRON_EXPIRE );
	if ( $timestamp ) {
		wp_unschedule_event( $timestamp, KK_SP_CRON_EXPIRE );
	}
	$timestamp = wp_next_scheduled( KK_SP_CRON_LUMA );
	if ( $timestamp ) {
		wp_unschedule_event( $timestamp, KK_SP_CRON_LUMA );
	}
}

/**
 * Move expired Featured promos to draft so they stop appearing
 * (and so the rotation falls back to Pillars). Logs the change to
 * the post for an audit trail.
 */
function kk_sp_expire_featured_promos() {
	$today = current_time( 'Y-m-d' );

	$expired = get_posts( [
		'post_type'      => KK_SP_POST_TYPE,
		'post_status'    => 'publish',
		'posts_per_page' => -1,
		'meta_query'     => [
			'relation' => 'AND',
			[
				'key'   => KK_SP_META_TYPE,
				'value' => 'featured',
			],
			[
				'key'     => KK_SP_META_END,
				'value'   => $today,
				'compare' => '<',
				'type'    => 'DATE',
			],
		],
		'fields'         => 'ids',
		'no_found_rows'  => true,
	] );

	foreach ( $expired as $post_id ) {
		wp_update_post( [
			'ID'          => $post_id,
			'post_status' => 'draft',
		] );
		/* translators: %s: today's date */
		$note = sprintf(
			__( 'Auto-expired by KK Sidebar Promos on %s.', 'kk-sidebar-promos' ),
			$today
		);
		wp_insert_comment( [
			'comment_post_ID' => $post_id,
			'comment_content' => $note,
			'comment_type'    => 'kk_sp_log',
			'comment_author'  => 'KK Sidebar Promos',
			'comment_approved' => 1,
		] );
	}
}
